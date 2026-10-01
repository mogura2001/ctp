$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$reportRoot = Join-Path $projectRoot 'ANALYSE/INVENTARIS'
[IO.Directory]::CreateDirectory($reportRoot) | Out-Null
$originalRoot = Join-Path $projectRoot 'CTP-og/ctp_data/default'
$modifiedRoot = Join-Path $projectRoot 'CTP-AAIP/ctp_data/default'
$rows = @()
$structure = @('# AI-bestanden: declaraties en afhankelijkheden', '', 'Automatisch gegenereerd. Commentaren verwijderd voor declaraties; geen bewijs van runtimebereikbaarheid.', '')
$differences = @('# Tekstverschillen origineel -> AAIP', '', 'Alle gewijzigde AI-bestanden, met git-context. Geen semantische effectmeting.', '')
foreach ($scope in @('aidata','gamedata')) {
    $paths = @{}
    foreach ($root in @($originalRoot,$modifiedRoot)) {
        Get-ChildItem (Join-Path $root $scope) -File -Recurse | ForEach-Object {
            $relative = $_.FullName.Substring($root.Length+1).Replace('\','/')
            $paths[$relative] = $true
        }
    }
    foreach ($relative in ($paths.Keys | Sort-Object)) {
        $original = Join-Path $originalRoot $relative
        $modified = Join-Path $modifiedRoot $relative
        $hasOriginal = Test-Path -LiteralPath $original
        $hasModified = Test-Path -LiteralPath $modified
        $state = if (!$hasOriginal) {'Alleen AAIP'} elseif (!$hasModified) {'Alleen origineel'} elseif ((Get-FileHash $original).Hash -eq (Get-FileHash $modified).Hash) {'Gelijk'} else {'Gewijzigd'}
        $rows += [pscustomobject]@{Bestand=$relative;Status=$state}
        if ($scope -ne 'aidata') { continue }
        if ($hasOriginal) {
            $body = [IO.File]::ReadAllText($original)
            $body = [regex]::Replace($body,'(?s)/\*.*?\*/','')
            $body = [regex]::Replace($body,'(?m)//.*$','')
            $structure += "## $relative"
            foreach ($pattern in @('(?m)^\s*#include\s+"[^"]+"','(?m)^\s*(?:input|output)\s+\w+','(?m)^\s*action\s+load\s*\([^\r\n]+','(?m)^\s*(?:double|int|Build_List_Class|Build_List_Element|Building_Build_List_Element|Advancement_Element)\s+\w+[^\r\n]*','(?m)^\s*#define\s+\w+[^\r\n]*')) {
                foreach ($match in [regex]::Matches($body,$pattern)) { $structure += '- `' + $match.Value.Trim() + '`' }
            }
            $structure += ''
        }
        if ($state -eq 'Gewijzigd') {
            $differences += "## $relative"
            $differences += '```diff'
            $differences += @(& git diff --no-index -- $original $modified 2>&1 | ForEach-Object {"$_"})
            $differences += '```'
            $differences += ''
        }
    }
}
$rows | Export-Csv (Join-Path $reportRoot 'bestanden.csv') -NoTypeInformation -Encoding UTF8
$structure | Set-Content (Join-Path $reportRoot 'declaraties.md') -Encoding UTF8
$differences | Set-Content (Join-Path $reportRoot 'aaip-ai-diff.md') -Encoding UTF8
$rows | Group-Object Status | Select-Object Name,Count | Format-Table
