# Alleen na rootreview uitvoeren; geen spelstart of spelbediening.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$planPath = 'PROEVEN/landvergelijking/20261027/HOST-PLAN.json'
$sourcePath = 'PROEVEN/landbenchmark/20261027/UITBREIDING-LAND-T0.original'
$saveRoot = 'CTP-proef/ctp_program/ctp/save'
$aliasName = '000-LAND-STAD-START-T0'
$newSaveName = 'UITBREIDING-LAND-STAD-T0'
$aliasPath = "$saveRoot/games/Julius/$aliasName"
$sourceHash = 'a670867460bae5d8d9196856d5ca88163b0eff951e9a9db42a05b83ee38d2301'
function FileRecord([string]$relative) {
    $file = Get-Item -LiteralPath (Join-Path $root $relative) -Force
    if ($file.PSIsContainer -or ($file.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw "Geen gewoon bestand: $relative" }
    [pscustomobject]@{path=$relative; size=$file.Length; sha256=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function AssertHash([string]$relative, [string]$expected) {
    if ((FileRecord $relative).sha256 -ne $expected) { throw "Hash wijkt af: $relative" }
}
function SaveInventory {
    @(Get-ChildItem -LiteralPath (Join-Path $root $saveRoot) -Recurse -File -Force | Sort-Object FullName | ForEach-Object {
        FileRecord ($_.FullName.Substring($root.Length + 1).Replace('\','/'))
    })
}
function AssertIdleMedia {
    if (@(Get-Process -Name civctp -ErrorAction SilentlyContinue).Count -ne 0) { throw 'CTP draait; geen voorbereiding' }
    $disc = [IO.DriveInfo]::new('E:')
    if (!$disc.IsReady -or $disc.DriveType -ne [IO.DriveType]::CDRom -or $disc.VolumeLabel -ne 'CCTP') { throw 'E: is geen leesbare CCTP-cd' }
}
AssertIdleMedia
AssertHash $planPath '7bc2f000e8bef1b5a1b40dd7ab5bb3377f6b97a947f0d6bb7212f1423061d1e4'
AssertHash $sourcePath $sourceHash
AssertHash 'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll' 'eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'
$plan = Get-Content -LiteralPath (Join-Path $root $planPath) -Raw | ConvertFrom-Json
if (@($plan.config19).Count -ne 19 -or @($plan.effective_protected118).Count -ne 118 -or @($plan.before29).Count -ne 29) { throw 'Onverwachte plangroepen' }
foreach ($pin in @($plan.config19) + @($plan.effective_protected118)) { AssertHash $pin.path $pin.sha256 }
# before29 is historisch; alleen deze twee actuele pins vervangen de oude records.
$currentPins = @{
    'CTP-proef/ctp_program/ctp/userprofile.txt' = '64ff5e641a7117715af34f8bbd114af51943aeb62bdb06910d7fab2d443a00d2'
    'CTP-proef/ctp_program/ctp/save/games/Julius/AUTOSAVE-Julius' = '91a14c73cf68fcf63397e4c383af1777dc24c40f0c049a1f1da9c703ba6ed528'
}
foreach ($pin in $plan.before29) {
    $expected = if ($currentPins.ContainsKey($pin.path)) { $currentPins[$pin.path] } else { $pin.sha256 }
    AssertHash $pin.path $expected
}
$saves = @(SaveInventory)
if (@($saves | Where-Object { [IO.Path]::GetFileName($_.path) -in @($aliasName,$newSaveName) }).Count -ne 0) { throw 'Alias of nieuwe savenaam bestaat al' }
if (Test-Path -LiteralPath (Join-Path $root $aliasPath)) { throw 'Aliasdoel bestaat al' }
$paths = @(@($plan.config19) + @($plan.effective_protected118) + @($plan.before29) + $saves | ForEach-Object { $_.path })
$paths += 'CTP-proef/ctp_program/ctp/userprofile.txt'
$paths = @($paths | Sort-Object -Unique)
$before = @($paths | ForEach-Object { FileRecord $_ })
$runName = 'before-' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ') + '-' + [guid]::NewGuid().ToString('N')
$run = Join-Path $PSScriptRoot $runName
if (Test-Path -LiteralPath $run) { throw 'Unieke backupmap bestaat al' }
[IO.Directory]::CreateDirectory($run) | Out-Null
foreach ($record in $before) {
    $target = Join-Path (Join-Path $run 'files') $record.path
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($target)) | Out-Null
    [IO.File]::Copy((Join-Path $root $record.path), $target, $false)
    if ((Get-Item -LiteralPath $target).Length -ne $record.size -or (Get-FileHash -LiteralPath $target).Hash -ne $record.sha256) { throw "Backup niet gelijk: $($record.path)" }
}
foreach ($record in $before) { AssertHash $record.path $record.sha256 }
if ((ConvertTo-Json -InputObject @(SaveInventory) -Compress) -ne (ConvertTo-Json -InputObject $saves -Compress)) { throw 'Save-inventaris tijdens backup gewijzigd' }
AssertIdleMedia
AssertHash $sourcePath $sourceHash
$manifest = [ordered]@{
    stage='BACKUP_VERIFIED_BEFORE_ALIAS_NO_GAMEPLAY'; at_utc=[DateTime]::UtcNow.ToString('o'); root=$root
    source=(FileRecord $sourcePath); plan=(FileRecord $planPath); script=(FileRecord 'PROEVEN/land-stad-start/20261028/Voorbereid.ps1')
    alias_name=$aliasName; alias_path=$aliasPath; alias_sha256=$sourceHash; intended_new_save_name=$newSaveName
    config19_paths=@($plan.config19.path); protected118_paths=@($plan.effective_protected118.path); before29_paths=@($plan.before29.path)
    historical_before29_current_pin_overrides=$currentPins; files=$before; save_inventory=$saves; save_count=$saves.Count
    backup_relative_root='files'; n_count=0; game_started=$false
}
$manifest | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $run 'before.json') -Encoding UTF8
[IO.File]::Copy((Join-Path $root $sourcePath), (Join-Path $root $aliasPath), $false)
AssertHash $aliasPath $sourceHash
[ordered]@{stage='ALIAS_READY_NO_GAMEPLAY'; at_utc=[DateTime]::UtcNow.ToString('o'); alias=(FileRecord $aliasPath); before_manifest_sha256=(Get-FileHash -LiteralPath (Join-Path $run 'before.json')).Hash.ToLowerInvariant()} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $run 'alias-ready.json') -Encoding UTF8
Write-Output "Voorbereid: $run ; $($saves.Count) oorspronkelijke saves ; geen spel gestart"
