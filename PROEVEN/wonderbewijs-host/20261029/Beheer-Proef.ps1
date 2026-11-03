param([ValidateSet('Prepare','Restore')][string]$Mode, [Parameter(Mandatory=$true)][ValidateSet('control','candidate')][string]$Arm)
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$runFolder=Join-Path $PSScriptRoot $Arm
[IO.Directory]::CreateDirectory($runFolder) | Out-Null
$pkg=Join-Path $root 'VERSIES/wonders-2026-10-28'
$live=Join-Path $root 'CTP-proef'
$manifest=Get-Content (Join-Path $pkg 'manifest.json') -Raw | ConvertFrom-Json
$baseline=Get-Content (Join-Path $pkg 'live-baseline.json') -Raw | ConvertFrom-Json
$aliasRel='CTP-proef/ctp_program/ctp/save/games/Julius/000-WONDERPROOF-'+$Arm.ToUpperInvariant()+'-T0'
$sourceRel='PROEVEN/landvergelijking/20261027/U30-40/host/AUTOSAVE-after'
$sourceHash='9280c97a41e6363ca9c5339cf2eba64388b63a811089d63c6d9fb30cca13336e'
function Hash($p) { (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() }
if (@(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0) {throw 'Close CTP normally before file operations'}
$pins=@($baseline.aidata)+@($baseline.saves)+@($baseline.dll)+@($baseline.extra_pins)
if ($Mode -eq 'Prepare') {
 if (Test-Path (Join-Path $runFolder 'before.json')) {throw 'This preparation has already been used'}
 foreach($pin in $pins) {
  $src=Join-Path $root $pin.path
  if((Hash $src) -ne $pin.sha256){throw "Before pin mismatch: $($pin.path)"}
  $dst=Join-Path $runFolder ('backup/'+$pin.path)
  [IO.Directory]::CreateDirectory((Split-Path $dst)) | Out-Null
  Copy-Item -LiteralPath $src -Destination $dst
 }
 foreach($f in $manifest.files) {
  $target=Join-Path $live $f.target_rel
  if($f.before_existed) {if((Hash $target) -ne $f.before_sha256){throw 'Before mismatch'}}
  elseif(Test-Path -LiteralPath $target){throw 'New target already exists'}
  if((Hash (Join-Path $pkg $f.candidate_package_rel)) -ne $f.after_sha256){throw 'Candidate mismatch'}
 }
 if(Test-Path (Join-Path $root $aliasRel)){throw 'Alias already exists'}
 if((Hash (Join-Path $root $sourceRel)) -ne $sourceHash){throw 'T0 source mismatch'}
 [ordered]@{at_utc=[DateTime]::UtcNow.ToString('o');arm=$Arm;pins=$pins;alias=$aliasRel;source_sha256=$sourceHash;max_n=1;close_seconds=780;maximum_seconds=900} | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $runFolder 'before.json') -Encoding UTF8
 if($Arm -eq 'candidate'){foreach($f in $manifest.files){Copy-Item -LiteralPath (Join-Path $pkg $f.candidate_package_rel) -Destination (Join-Path $live $f.target_rel)}}
 Copy-Item -LiteralPath (Join-Path $root $sourceRel) -Destination (Join-Path $root $aliasRel)
 if($Arm -eq 'candidate'){foreach($f in $manifest.files){if((Hash (Join-Path $live $f.target_rel)) -ne $f.after_sha256){throw 'Installed file mismatch'}}}
 Write-Output ('Prepared '+$Arm+' arm with hash-equal T0 alias; no DLL change.')
} else {
 $before=Get-Content (Join-Path $runFolder 'before.json') -Raw | ConvertFrom-Json
 foreach($f in $manifest.files) {
  $target=[IO.Path]::GetFullPath((Join-Path $live $f.target_rel))
  if(-not $target.StartsWith($live+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Target outside CTP-proef'}
  if($f.before_existed){if((Hash $target) -notin @($f.before_sha256,$f.after_sha256)){throw 'Unexpected modified FLI'}}
  elseif(Test-Path -LiteralPath $target){if((Hash $target) -ne $f.after_sha256){throw 'Unexpected modified partial'}}
 }
 $changed=@()
 foreach($pin in $before.pins) {
  $target=Join-Path $root $pin.path
  if((Hash $target) -eq $pin.sha256){continue}
  if($pin.path -like 'CTP-proef/ctp_data/default/aidata/beginturn*.fli'){continue}
  if($pin.path -notin @('CTP-proef/ctp_program/ctp/save/games/Julius/AUTOSAVE-Julius','CTP-proef/ctp_program/ctp/userprofile.txt')){throw "Unexpected change: $($pin.path)"}
  $archive=Join-Path $runFolder ('after/'+$pin.path)
  [IO.Directory]::CreateDirectory((Split-Path $archive)) | Out-Null
  Copy-Item -LiteralPath $target -Destination $archive
  $changed+=@{path=$pin.path;after_sha256=(Hash $archive)}
 }
 foreach($f in $manifest.files){$target=Join-Path $live $f.target_rel;if($f.before_existed){Copy-Item -LiteralPath (Join-Path $pkg $f.backup_package_rel) -Destination $target}elseif(Test-Path -LiteralPath $target){Remove-Item -LiteralPath $target}}
 $alias=Join-Path $root $before.alias
 if(Test-Path -LiteralPath $alias){if((Hash $alias) -ne $sourceHash){throw 'Alias modified'};Remove-Item -LiteralPath $alias}
 foreach($entry in $changed){Copy-Item -LiteralPath (Join-Path $runFolder ('backup/'+$entry.path)) -Destination (Join-Path $root $entry.path)}
 foreach($pin in $before.pins){if((Hash (Join-Path $root $pin.path)) -ne $pin.sha256){throw 'Restore hash mismatch'}}
 [ordered]@{at_utc=[DateTime]::UtcNow.ToString('o');restored_pins=$before.pins.Count;candidate_files_removed=$(if($Arm -eq 'candidate'){8}else{0});arm=$Arm;alias_removed=(-not(Test-Path -LiteralPath $alias));archived_changes=$changed;ctp_processes=0;pc_left_on=$true} | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $runFolder 'ROOT-RESTORE.json') -Encoding UTF8
 'Restore verified; PC remains on.'
}
