$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$sourceRoot = Join-Path $projectRoot 'CTP-og/ctp_data/default/aidata/AIPs'
$variantRoot = Join-Path $PSScriptRoot 'settlerquota'
foreach ($variant in @(@{Name='vast-min2';Quota='-2.0'},@{Name='ratio-half';Quota='0.5'},@{Name='controle-nul';Quota='0.0'})) {
    $targetRoot = Join-Path $variantRoot ($variant.Name+'/AIPs')
    [IO.Directory]::CreateDirectory($targetRoot) | Out-Null
    foreach ($source in (Get-ChildItem $sourceRoot -Filter '*.aip')) {
        $body = [IO.File]::ReadAllText($source.FullName)
        $changed = $body
        foreach ($listName in @('Land_Settler_Troops_Primary','Settler_Troops_Core','Settler_Troops_Overflow')) {
            $quota = if ($listName -eq 'Land_Settler_Troops_Primary') {$variant.Quota} else {'0.0'}
            $pattern = '(?s)(Build_List_Element\s+'+[regex]::Escape($listName)+'\[MAX_ELEMENTS\];.*?#DATA\s*)(.*?)(#END_DATA)'
            $replacement = '$1'+[Environment]::NewLine+'"UNIT_SETTLER", '+$quota+';'+[Environment]::NewLine+'$3'
            $changed = [regex]::Replace($changed,$pattern,$replacement)
        }
        # Keep competing core/overflow classes inactive even if zero quotas
        # have unexpected semantics. Primary priority is identical in all variants.
        $changed = [regex]::Replace($changed,'"Land_Settler_Troops_Primary",\s*[\d.]+;','"Land_Settler_Troops_Primary", 30000.0;')
        $changed = [regex]::Replace($changed,'"Settler_Troops_(Core|Overflow)",\s*[\d.]+;','"Settler_Troops_$1", 0.0;')
        if ($changed -ne $body) {
            [IO.File]::WriteAllText((Join-Path $targetRoot $source.Name),$changed,[Text.UTF8Encoding]::new($false))
        }
    }
    Write-Output "Prepared $($variant.Name); not installed."
}
