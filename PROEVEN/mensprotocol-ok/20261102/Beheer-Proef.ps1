param([Parameter(Mandatory=$true)][ValidateSet('Prepare','Restore')][string]$Mode,
 [ValidateSet('control')][string]$Arm='control')
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$runFolder=Join-Path $PSScriptRoot $Arm
$baseline=Get-Content (Join-Path $root 'VERSIES/wondergewicht-2026-10-30/live-baseline.json') -Raw|ConvertFrom-Json
$pins=@($baseline.aidata)+@($baseline.saves)+@($baseline.dll)+@($baseline.extra_pins)
$sourceRel='PROEVEN/land-stad-defensie/20261028/AUTOSAVE-after'
$sourceHash='522b829d517b1d9e7d0f96f13632118aaeee59c70b31655ac54c8950bd819b9e'
$aliasRel='CTP-proef/ctp_program/ctp/save/games/Julius/000-MENSPROTOCOL-OK-20261102-T0'
function Hash($p){(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()}
function Inventory($group,$rows,$aliasAllowed){
 $base=if($group -eq 'aidata'){'CTP-proef/ctp_data/default/aidata'}else{'CTP-proef/ctp_program/ctp/save'}
 $actual=@(Get-ChildItem -LiteralPath (Join-Path $root $base) -File -Recurse|ForEach-Object {$_.FullName.Substring($root.Length+1).Replace('\','/')})
 if($aliasAllowed){$actual=@($actual|Where-Object {$_ -ne $aliasRel})}
 if(@(Compare-Object @($rows.path|Sort-Object) @($actual|Sort-Object)).Count){throw "Full $group inventory mismatch"}
}
if(@(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0){throw 'Close CTP normally before file operations'}
foreach($pin in (Get-Content (Join-Path $PSScriptRoot 'pins.json') -Raw|ConvertFrom-Json).files){if((Hash (Join-Path $root $pin.path)) -ne $pin.sha256){throw "Source pin mismatch: $($pin.path)"}}
if($pins.Count -ne 162 -or $baseline.aidata.Count -ne 118 -or $baseline.saves.Count -ne 38){throw 'Unexpected baseline dimensions'}
if($Mode -eq 'Prepare'){
 if(Test-Path (Join-Path $runFolder 'before.json')){throw 'Preparation already used'}
 if(Test-Path (Join-Path $root $aliasRel)){throw 'Alias already exists'}
 if((Hash (Join-Path $root $sourceRel)) -ne $sourceHash -or (Get-Item (Join-Path $root $sourceRel)).Length -ne 159906){throw 'Source522b mismatch'}
 Inventory 'aidata' $baseline.aidata $false
 Inventory 'saves' $baseline.saves $false
 foreach($pin in $pins){if((Hash (Join-Path $root $pin.path)) -ne $pin.sha256){throw "Before pin mismatch: $($pin.path)"}}
 foreach($pin in $pins){
  $dst=Join-Path $runFolder ('backup/'+$pin.path)
  [IO.Directory]::CreateDirectory((Split-Path $dst))|Out-Null
  Copy-Item -LiteralPath (Join-Path $root $pin.path) -Destination $dst
  if((Hash $dst) -ne $pin.sha256){throw 'Backup mismatch'}
 }
 [ordered]@{at_utc=[DateTime]::UtcNow.ToString('o');arm=$Arm;pins=$pins;alias=$aliasRel;source=$sourceRel;source_sha256=$sourceHash;max_n=1;close_seconds=780;maximum_seconds=900}|ConvertTo-Json -Depth 10|Set-Content (Join-Path $runFolder 'before.json') -Encoding UTF8
 Copy-Item -LiteralPath (Join-Path $root $sourceRel) -Destination (Join-Path $root $aliasRel)
 if((Hash (Join-Path $root $aliasRel)) -ne $sourceHash){throw 'Alias mismatch'}
 'Prepared control alias/backups only; no AI text or DLL installed.'
}else{
 $before=Get-Content (Join-Path $runFolder 'before.json') -Raw|ConvertFrom-Json
 if($before.alias -ne $aliasRel -or $before.source_sha256 -ne $sourceHash){throw 'Unexpected restore record'}
 Inventory 'aidata' $baseline.aidata $true
 Inventory 'saves' $baseline.saves $true
 $changed=@()
 foreach($pin in $pins){
  if((Hash (Join-Path $runFolder ('backup/'+$pin.path))) -ne $pin.sha256){throw 'Backup pin mismatch'}
  $target=Join-Path $root $pin.path
  if((Hash $target) -eq $pin.sha256){continue}
  if($pin.path -notin @('CTP-proef/ctp_program/ctp/save/games/Julius/AUTOSAVE-Julius','CTP-proef/ctp_program/ctp/userprofile.txt')){throw "Unexpected change: $($pin.path)"}
  $archive=Join-Path $runFolder ('after/'+$pin.path)
  if(Test-Path $archive){throw 'Archive already exists; inspect before restore'}
  [IO.Directory]::CreateDirectory((Split-Path $archive))|Out-Null
  Copy-Item -LiteralPath $target -Destination $archive
  $changed+=@{path=$pin.path;after_sha256=(Hash $archive)}
 }
 $alias=[IO.Path]::GetFullPath((Join-Path $root $aliasRel))
 $saves=[IO.Path]::GetFullPath((Join-Path $root 'CTP-proef/ctp_program/ctp/save'))
 if(-not $alias.StartsWith($saves+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Alias outside save directory'}
 if(Test-Path -LiteralPath $alias){if((Hash $alias) -ne $sourceHash){throw 'Alias modified'};Remove-Item -LiteralPath $alias}
 foreach($entry in $changed){Copy-Item -LiteralPath (Join-Path $runFolder ('backup/'+$entry.path)) -Destination (Join-Path $root $entry.path)}
 foreach($pin in $pins){if((Hash (Join-Path $root $pin.path)) -ne $pin.sha256){throw 'Restore mismatch'}}
 Inventory 'aidata' $baseline.aidata $false
 Inventory 'saves' $baseline.saves $false
 [ordered]@{at_utc=[DateTime]::UtcNow.ToString('o');restored_pins=162;aidata=118;saves=38;alias_removed=(-not(Test-Path $alias));archived_changes=$changed;ctp_processes=0;pc_left_on=$true}|ConvertTo-Json -Depth 8|Set-Content (Join-Path $runFolder 'ROOT-RESTORE.json') -Encoding UTF8
 'Restore verified; PC remains on.'
}
