param(
 [Parameter(Mandatory=$true)][ValidateSet('InstallStart','Guard','Capture','Read','Pass','Finish','RestoreNoStart')][string]$Action,
 [ValidateSet('variant','baseline')][string]$Arm='variant',
 [int]$Turn=0,[string]$Previous='', [string]$Label='checkpoint'
)
$ErrorActionPreference='Stop'
$workspace='C:\GIT\ctp';$package=$PSScriptRoot;$armDir=Join-Path $package $Arm
$exe=Join-Path $workspace 'CTP-proef\ctp_program\ctp\civctp.exe'
$tool=Join-Path $workspace 'PROEVEN\Bedien-CTP.ps1'
$python='C:\Users\Stephan\AppData\Local\Programs\Python\Python312\python.exe'
$manifest=Get-Content (Join-Path $package 'manifest.json') -Raw -Encoding utf8|ConvertFrom-Json

$gatePath=Join-Path $package 'C6-ROOT-VRIJGAVE.json'
if(!(Test-Path -LiteralPath $gatePath)){throw 'C6 source only: no root activation release.'}
$gate=Get-Content -LiteralPath $gatePath -Raw -Encoding utf8|ConvertFrom-Json
if(!$gate.allowed -or $gate.candidate_sha256 -cne 'f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810'){throw 'C6 root release absent/disabled.'}
foreach($pin in $gate.sources){if((Get-FileHash -LiteralPath (Join-Path $package $pin.path) -Algorithm SHA256).Hash.ToLowerInvariant() -cne $pin.sha256){throw 'Released C6 source changed.'}}
if($Arm -eq 'baseline' -and !$gate.baseline_allowed){throw 'First activation is variant only; baseline needs later release.'}
if($Turn -notin @(0,1)){throw 'First C6 stage only T0/T1.'}
if($Action -eq 'Pass' -and $Turn -ne 1){throw 'Only the first native T1 pass is released.'}

$toolHash='d2dbbfcad3d9d8bec8e6a99a399d59561d8f9c4e9a48576a2aefc32e5997bc74'
$variant=if($Arm -eq 'variant'){'U30-40'}else{'release-v1'}
if(!(Test-Path -LiteralPath $armDir)){New-Item -ItemType Directory -Path $armDir|Out-Null}
function JsonFile($value,$name){$value|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $armDir $name) -Encoding utf8}
function Hash($p){(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()}
function CountZero {if(@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop).Count -ne 0){throw 'All-civctp fresh gate not count0.'}}
function Budget {
 $value=& $python (Join-Path $workspace 'PROEVEN\Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d
 $code=$LASTEXITCODE
 if($code -eq 2){$value=& $python (Join-Path $workspace 'PROEVEN\Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d;$code=$LASTEXITCODE}
 JsonFile ($value|ConvertFrom-Json) 'latest-budget.json'
 if($code -ne 0 -and $code -ne 25){throw 'Budget stop/unknown; checkpoint only; PC stays on.'}
}
Add-Type @'
using System;using System.Text;using System.Runtime.InteropServices;
public class ExpansionWindow {
 [DllImport("user32.dll")]public static extern bool SetProcessDPIAware();
 public delegate bool Callback(IntPtr h,IntPtr p);
 [DllImport("user32.dll")]public static extern uint GetWindowThreadProcessId(IntPtr h,out uint pid);
 [DllImport("user32.dll")]public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")]public static extern bool EnumWindows(Callback cb,IntPtr p);
 [DllImport("user32.dll")]public static extern bool IsWindowVisible(IntPtr h);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)]public static extern int GetWindowText(IntPtr h,StringBuilder s,int max);
 [StructLayout(LayoutKind.Sequential)]public struct Rect{public int Left,Top,Right,Bottom;}
 [DllImport("user32.dll")]public static extern bool GetWindowRect(IntPtr h,out Rect r);
}
'@
[ExpansionWindow]::SetProcessDPIAware() | Out-Null
function Elapsed($started){([Diagnostics.Stopwatch]::GetTimestamp()-[long]$started.start_monotonic_ticks)/[double]$started.monotonic_frequency}
function OwnState($started,[switch]$RequireFocus,[switch]$BindWindow,[switch]$ForClose){
 $limit=if($ForClose){470}else{420}
 if((Elapsed $started) -ge $limit){throw '8min activation deadline; retain normal-close reserve.'}
 $rows=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
 if($rows.Count -ne 1 -or $rows[0].ProcessId -ne $started.pid -or $rows[0].ExecutablePath -cne $exe -or ([DateTimeOffset]$rows[0].CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $started.creation_utc_ms){throw 'Exact own process identity/unique civctp changed.'}
 $own=[Diagnostics.Process]::GetProcessById([int]$started.pid)
 try {
  $own.Refresh();$owner=[uint32]0;$h=$own.MainWindowHandle
  if($own.MainModule.FileName -cne $exe -or ([DateTimeOffset]$own.StartTime.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $started.creation_utc_ms){throw 'Retained process path/time mismatch.'}
  if($h -eq [IntPtr]::Zero -or [ExpansionWindow]::GetWindowThreadProcessId($h,[ref]$owner) -eq 0 -or $owner -ne $started.pid){throw 'Own HWND absent/unbound.'}
  if($BindWindow -and $h.ToInt64() -ne $started.handle){throw 'Bound HWND changed.'}
  if($RequireFocus -and [ExpansionWindow]::GetForegroundWindow() -ne $h){throw 'Own game not foreground; no input.'}
  $windows=[Collections.Generic.List[object]]::new()
  if(-not [ExpansionWindow]::EnumWindows({param($wh,$unused)
   $pidOwner=[uint32]0;[ExpansionWindow]::GetWindowThreadProcessId($wh,[ref]$pidOwner)|Out-Null
   if($pidOwner -eq $started.pid -and [ExpansionWindow]::IsWindowVisible($wh)){$title=[Text.StringBuilder]::new(1024);[ExpansionWindow]::GetWindowText($wh,$title,1024)|Out-Null;$windows.Add(@{handle=$wh.ToInt64();title=$title.ToString()})};return $true
  },[IntPtr]::Zero)){throw 'Own-window enumeration failed.'}
  if($windows.Count -ne 1 -or $windows[0].handle -ne $h.ToInt64() -or !$windows[0].title -or $windows[0].title -match 'Error|CD-ROM|Call to Power CD'){throw 'Modal/error/extra own window; stop.'}
  $r=New-Object ExpansionWindow+Rect;if(-not [ExpansionWindow]::GetWindowRect($h,[ref]$r)){throw 'Bounds unreadable.'}
  if((Elapsed $started) -ge $limit){throw 'Late OS query; no next action.'}
  return [ordered]@{pid=$started.pid;handle=$h.ToInt64();creation_utc_ms=$started.creation_utc_ms;foreground_handle=[ExpansionWindow]::GetForegroundWindow().ToInt64();elapsed_seconds=(Elapsed $started);bounds=@{left=$r.Left;top=$r.Top;right=$r.Right;bottom=$r.Bottom;width=$r.Right-$r.Left;height=$r.Bottom-$r.Top};title=$windows[0].title}
 }finally{$own.Dispose()}
}
function CheckInstalled {
 foreach($pin in $manifest.protected){
  $entry=@($manifest.files|Where-Object{$_.path -ceq $pin.path})
  $expected=$pin.sha256;if($entry.Count){$expected=$entry[0].("${Arm}_sha256")}
  if((Hash (Join-Path $workspace $pin.path)) -ne $expected){throw "Installed/protected pin mismatch: $($pin.path)"}
 }
 foreach($entry in $manifest.files){
  $expected=$entry.("${Arm}_sha256");$target=Join-Path $workspace $entry.path
  if($null -eq $expected){if(Test-Path -LiteralPath $target){throw 'New FLI unexpectedly present in baseline.'}}
  elseif((Hash $target) -ne $expected){throw "Installed changed-file mismatch: $($entry.path)"}
 }
}
function SaveAutosaveBefore {
 CountZero
 $saveDir=(Get-Item -LiteralPath (Join-Path $workspace 'CTP-proef\ctp_program\ctp\save\games\Julius')).FullName
 $autoPath=Join-Path $saveDir 'AUTOSAVE-Julius'
 $version=if($Arm -eq 'variant'){'U30-40-N30'}else{'RELEASE-V1-N30'}
 $labelPath=Join-Path $saveDir ('UITBREIDING-20261014-C6-'+$version+'-AUTOSAVE')
 if(Test-Path -LiteralPath $labelPath){throw 'Owned visible autosave label already exists; do not overwrite.'}
 $exists=Test-Path -LiteralPath $autoPath;$hash=$null
 if($exists){$hash=Hash $autoPath;Copy-Item -LiteralPath $autoPath -Destination (Join-Path $armDir 'AUTOSAVE.before');if((Hash (Join-Path $armDir 'AUTOSAVE.before')) -ne $hash){throw 'Pre-run autosave backup mismatch.'}}
 JsonFile @{path=$autoPath;existed=$exists;sha256=$hash;visible_label=$labelPath;version=$version} 'autosave-before.json'
}
function ArchiveAndRestoreAutosave {
 CountZero
 $beforePath=Join-Path $armDir 'autosave-before.json'
 if(!(Test-Path -LiteralPath $beforePath)){throw 'Missing real pre-run autosave record; no restore.'}
 $before=Get-Content -LiteralPath $beforePath -Raw -Encoding utf8|ConvertFrom-Json
 $saveDir=(Get-Item -LiteralPath (Join-Path $workspace 'CTP-proef\ctp_program\ctp\save\games\Julius')).FullName
 $autoPath=Join-Path $saveDir 'AUTOSAVE-Julius'
 $version=if($Arm -eq 'variant'){'U30-40-N30'}else{'RELEASE-V1-N30'}
 $labelPath=Join-Path $saveDir ('UITBREIDING-20261014-C6-'+$version+'-AUTOSAVE')
 if($before.path -cne $autoPath -or $before.visible_label -cne $labelPath -or [IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($autoPath)) -cne $saveDir -or [IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($labelPath)) -cne $saveDir){throw 'Exact autosave/label targets escaped the named save directory.'}
 $present=Test-Path -LiteralPath $autoPath;$current=if($present){Hash $autoPath}else{$null}
 if($present -eq $before.existed -and $current -eq $before.sha256){JsonFile @{status='UNCHANGED_DEFAULT';before_sha256=$before.sha256;after_sha256=$current;named_saves_not_reverted=$true} 'autosave-archive.json';return}
 if(!$present){throw 'Default autosave unexpectedly absent; preserve state, no DLL restoration.'}
 if(Test-Path -LiteralPath $labelPath){throw 'Visible autosave label exists; do not overwrite.'}
 $archive=Join-Path $armDir ('AUTOSAVE.after-'+$version)
 Copy-Item -LiteralPath $autoPath -Destination $archive
 if((Hash $archive) -ne $current -or (Hash $autoPath) -ne $current){throw 'Own autosave archive/source changed; no default restore.'}
 Copy-Item -LiteralPath $autoPath -Destination $labelPath
 if((Hash $labelPath) -ne $current -or (Hash $autoPath) -ne $current){throw 'Visible versioned autosave copy/source mismatch.'}
 JsonFile @{status='ARCHIVED_BOTH_COPIES_BEFORE_DEFAULT_RESTORE';before_sha256=$before.sha256;generated_sha256=$current;archive=$archive;visible_label=$labelPath;version=$version;required_dll_sha256=if($Arm -eq 'variant'){'f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810'}else{'eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'};named_saves_not_reverted=$true} 'autosave-archive.json'
 CountZero
 if((Hash $autoPath) -ne $current){throw 'Default autosave changed after archival; preserve.'}
 if($before.existed){$backup=Join-Path $armDir 'AUTOSAVE.before';if((Hash $backup) -ne $before.sha256){throw 'Pre-run autosave backup changed.'};Copy-Item -LiteralPath $backup -Destination $autoPath;if((Hash $autoPath) -ne $before.sha256){throw 'Default autosave restore mismatch.'}}
 else{Remove-Item -LiteralPath $autoPath}
 JsonFile @{status='GENERATED_SAVE_ARCHIVED_DEFAULT_RESTORED';before_sha256=$before.sha256;generated_sha256=$current;archive=$archive;visible_label=$labelPath;version=$version;required_dll_sha256=if($Arm -eq 'variant'){'f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810'}else{'eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'};default_restored=$true;named_saves_not_reverted=$true} 'autosave-archive.json'
}
function ExactAliasPaths {
 $saveDir=[IO.Path]::GetFullPath((Join-Path $workspace 'CTP-proef\ctp_program\ctp\save\games\Julius'))
 $source=[IO.Path]::GetFullPath((Join-Path $workspace $manifest.T0_alias.source))
 $target=[IO.Path]::GetFullPath((Join-Path $workspace $manifest.T0_alias.path))
 if($source -cne (Join-Path $saveDir 'QUOTA-START-T0') -or $target -cne (Join-Path $saveDir '000-U30-40-START-T0') -or [IO.Path]::GetDirectoryName($target) -cne $saveDir){throw 'Alias exact absolute targets escaped named Julius folder.'}
 return @{source=$source;target=$target}
}
function CreateOwnT0Alias {
 CountZero
 $paths=ExactAliasPaths;$ownerRecord=Join-Path $armDir 'T0-alias-owner.json'
 if(Test-Path -LiteralPath $ownerRecord){throw 'Own alias creation already attempted; no retry.'}
 if(Test-Path -LiteralPath $paths.target){throw 'Alias existed before own creation; never overwrite.'}
 if((Hash $paths.source) -cne $manifest.T0_alias.sha256){throw 'Pinned alias source changed.'}
 JsonFile @{at=(Get-Date).ToString('o');owner='C6_UI_LOAD_ALIAS_ONLY';path=$paths.target;source=$paths.source;initially_absent=$true;source_sha256=$manifest.T0_alias.sha256;copy_attempted=$true} 'T0-alias-owner.json'
 Copy-Item -LiteralPath $paths.source -Destination $paths.target
 if((Hash $paths.target) -cne $manifest.T0_alias.sha256){throw 'Own alias byteexact verification failed; preserve.'}
 JsonFile @{at=(Get-Date).ToString('o');created=$true;path=$paths.target;sha256=(Hash $paths.target);source_sha256=(Hash $paths.source)} 'T0-alias-created.json'
}
function RemoveOwnT0Alias {
 CountZero
 $paths=ExactAliasPaths;$ownerRecord=Join-Path $armDir 'T0-alias-owner.json'
 if(!(Test-Path -LiteralPath $ownerRecord)){JsonFile @{status='NO_OWN_ALIAS_ATTEMPT';removed=$false} 'T0-alias-cleanup.json';return}
 $record=Get-Content -LiteralPath $ownerRecord -Raw -Encoding utf8|ConvertFrom-Json
 if($record.owner -cne 'C6_UI_LOAD_ALIAS_ONLY' -or !$record.initially_absent -or !$record.copy_attempted -or $record.path -cne $paths.target -or $record.source -cne $paths.source -or $record.source_sha256 -cne $manifest.T0_sha256){throw 'Alias ownership/preimage mismatch; preserve.'}
 if(!(Test-Path -LiteralPath $paths.target)){JsonFile @{status='OWN_ALIAS_ALREADY_ABSENT';removed=$false} 'T0-alias-cleanup.json';return}
 $current=Hash $paths.target
 if($current -cne $manifest.T0_alias.sha256){JsonFile @{status='PRESERVED_UNEXPECTED_ALIAS_BYTES';removed=$false;path=$paths.target;sha256=$current} 'T0-alias-cleanup.json';throw 'Own alias unexpectedly changed; preserved for review.'}
 # Exact checked named target only, never recursive or another shell.
 Remove-Item -LiteralPath $paths.target
 if(Test-Path -LiteralPath $paths.target){throw 'Own alias removal not confirmed.'}
 JsonFile @{at=(Get-Date).ToString('o');status='OWN_BYTEEXACT_ALIAS_REMOVED_AFTER_RELEASE_RESTORE';removed=$true;path=$paths.target;verified_sha256=$current} 'T0-alias-cleanup.json'
}

function RestoreOwnInstallation {
 $execution=Join-Path $armDir 'execution.json'
 if(!(Test-Path -LiteralPath $execution)){throw 'No own recorded installation attempt; no restoration.'}
 $record=Get-Content -LiteralPath $execution -Raw -Encoding utf8|ConvertFrom-Json
 if(!$record.install_attempted -or $record.arm -cne $Arm){throw 'Installation record is not this arm.'}
 CountZero;Budget
 # Validate every current file and true backup before the first restore mutation.
 foreach($entry in $manifest.files){
  $target=Join-Path $workspace $entry.path;$present=Test-Path -LiteralPath $target
  $armHash=$entry.("${Arm}_sha256");$current=if($present){Hash $target}else{$null}
  if($current -ne $entry.before_sha256 -and $current -ne $armHash){throw "User/unexpected file change; preserve: $($entry.path)"}
  if($entry.existed){$backup=Join-Path (Join-Path $package 'backups') $entry.path;if((Hash $backup) -ne $entry.before_sha256){throw 'True restore backup changed.'}}
 }
 ArchiveAndRestoreAutosave
 CountZero
 foreach($entry in $manifest.files){
  $target=Join-Path $workspace $entry.path
  if($entry.existed){Copy-Item -LiteralPath (Join-Path (Join-Path $package 'backups') $entry.path) -Destination $target}
  elseif(Test-Path -LiteralPath $target){Remove-Item -LiteralPath $target}
 }
 $checks=@(foreach($entry in $manifest.files){$target=Join-Path $workspace $entry.path;$present=Test-Path -LiteralPath $target;$hash=if($present){Hash $target}else{$null};@{path=$entry.path;present=$present;sha256=$hash;match=($present -eq $entry.existed -and $hash -eq $entry.before_sha256)}})
 JsonFile @{at=(Get-Date).ToString('o');mode='OWN_INSTALLATION_COUNT0_RESTORE';all_civctp_count=0;files=$checks;profile_sha256=(Hash (Join-Path $workspace 'CTP-proef\ctp_program\ctp\userprofile.txt'));autosave_report=(Join-Path $armDir 'autosave-archive.json');save_bytes_preserved_in_original_and_versioned_archives=$true;named_saves_not_reverted=$true} 'restore.json'
 if(@($checks|Where-Object{!$_.match}).Count){throw 'Restoration mismatch.'}
 foreach($saved in $manifest.preserved_saves_before){if((Hash (Join-Path $workspace $saved.path)) -ne $saved.sha256){throw 'Protected named save changed; preserve for review.'}}
 if((Hash (Join-Path $workspace $manifest.profile_before.path)) -ne $manifest.profile_before.sha256){throw 'Profile changed; preserve current bytes for review.'}
 RemoveOwnT0Alias

}
function ReadSnapshot($started,$name,$turn){
 OwnState $started -BindWindow|Out-Null
 $output=Join-Path $armDir $name
 $oldErrorAction=$ErrorActionPreference
 try{
  $ErrorActionPreference='Continue'
  $result=& $python -X utf8 (Join-Path $package 'Lees-Uitbreiding.py') --pid $started.pid --variant $variant --run-id ('uitbreiding-20261014-c6-'+$Arm) --snapshot-label $name --turn $turn --pass-label 'passive-human-native-round' --manifest (Join-Path $package 'participants.json') --output $output 2>&1
  $readerCode=$LASTEXITCODE
 }finally{$ErrorActionPreference=$oldErrorAction}
 $result|Set-Content -LiteralPath (Join-Path $armDir ($name+'.stdout.txt')) -Encoding utf8
 if($readerCode -ne 0){
  if(Test-Path -LiteralPath $output){$rejected=Get-Content -LiteralPath $output -Raw -Encoding utf8|ConvertFrom-Json;if($rejected.status -ceq 'rejected' -and $rejected.error -ceq 'Unstable complete snapshot; no turn acceptance'){throw 'UNSTABLE_DATASET_RETRY_ONLY'}}
  throw 'Fatal snapshot rejection; no turn acceptance/retry.'
 }
 $value=Get-Content $output -Raw -Encoding utf8|ConvertFrom-Json
 if($value.instance.pid -ne $started.pid -or [Math]::Floor(([decimal]$value.instance.creationtime_filetime-[decimal]116444736000000000)/10000) -ne $started.creation_utc_ms){throw 'Reader process creationtime mismatch.'}
 OwnState $started -BindWindow|Out-Null
 return $value
}
Budget
if((Hash $tool) -ne $toolHash){throw 'Reviewed Bedien-CTP changed.'}
if($Action -eq 'RestoreNoStart'){RestoreOwnInstallation;exit}
if($Action -eq 'InstallStart'){
 if(Test-Path -LiteralPath (Join-Path $armDir 'execution.json')){throw 'Arm already attempted; no automatic retry/start.'}
 CountZero
 if((Hash (Join-Path $workspace 'ONTWERP\UITBREIDING-30-40.md')) -ne $manifest.proposal_sha256){throw 'Reviewed goal3 proposal changed.'}
 foreach($pin in $manifest.input_manifests){if((Hash (Join-Path $workspace $pin.path)) -ne $pin.sha256){throw 'Pinned B1/B2a/B2b input manifest changed.'}}
 foreach($savePath in $manifest.T0_paths){if((Hash (Join-Path $workspace $savePath)) -ne $manifest.T0_sha256){throw 'Fixed T0 changed; no install/start.'}}
 foreach($pin in $manifest.protected){if((Hash (Join-Path $workspace $pin.path)) -ne $pin.sha256){throw 'Pre-run protected/current pin changed; no install.'}}
 foreach($saved in $manifest.preserved_saves_before){if((Hash (Join-Path $workspace $saved.path)) -ne $saved.sha256 -or (Hash (Join-Path (Join-Path $package 'protected-backups') $saved.path)) -ne $saved.sha256){throw 'Protected9saves/truebackup changed; no install.'}}
 if((Hash (Join-Path (Join-Path $package 'protected-backups') $manifest.profile_before.path)) -ne $manifest.profile_before.sha256){throw 'Protected profile truebackup changed; no install.'}
 foreach($entry in $manifest.files){
  $target=Join-Path $workspace $entry.path
  if($entry.existed){if((Hash $target) -ne $entry.before_sha256 -or (Hash (Join-Path (Join-Path $package 'backups') $entry.path)) -ne $entry.before_sha256){throw 'True pre-run/backup identity changed.'}}
  elseif(Test-Path -LiteralPath $target){throw 'Previously absent FLI now exists; no overwrite.'}
  $expected=$entry.("${Arm}_sha256");if($null -ne $expected){$source=Join-Path (Join-Path $package ('candidate\'+$Arm)) $entry.path;if((Hash $source) -ne $expected){throw 'Candidate changed before any installation.'}}
 }
 SaveAutosaveBefore
 JsonFile @{at=(Get-Date).ToString('o');install_attempted=$true;arm=$Arm} 'execution.json'
 CreateOwnT0Alias
 CountZero
 foreach($entry in $manifest.files){
  $source=Join-Path (Join-Path $package ('candidate\'+$Arm)) $entry.path;$target=Join-Path $workspace $entry.path;$expected=$entry.("${Arm}_sha256")
  if($null -ne $expected){if((Hash $source) -ne $expected){throw 'Prepared candidate hash changed.'};if((Hash $target) -ne $expected){Copy-Item -LiteralPath $source -Destination $target}}
 }
 CheckInstalled;Budget;CountZero
 $ticks=[Diagnostics.Stopwatch]::GetTimestamp()
 $result=& powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $tool -Action Start 2>&1;$code=$LASTEXITCODE
 $result|Set-Content -LiteralPath (Join-Path $armDir 'start-stdout.txt') -Encoding utf8
 $match=[regex]::Match(($result -join "`n"),'process (\d+)\.')
 if($code -ne 0 -or !$match.Success){throw 'Start failed; no retry. Preserve install state for reviewed cleanup.'}
 $targetPid=[int]$match.Groups[1].Value;$rows=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
 if($rows.Count -ne 1 -or $rows[0].ProcessId -ne $targetPid -or $rows[0].ExecutablePath -cne $exe){throw 'Immediate start binding failed.'}
 $started=[ordered]@{pid=$targetPid;exe=$exe;creation_utc_ms=([DateTimeOffset]$rows[0].CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds();start_monotonic_ticks=$ticks;monotonic_frequency=[Diagnostics.Stopwatch]::Frequency;handle=0}
 JsonFile $started 'start-record.json'
 # Intro is already known to take about180s; no input/focus tricks during it.
 $until=[DateTime]::UtcNow.AddSeconds(210);$stable=$null;$stableSince=$null;$lastBudget=[DateTime]::UtcNow
 while([DateTime]::UtcNow -lt $until){
  if(([DateTime]::UtcNow-$lastBudget).TotalSeconds -ge 90){Budget;$lastBudget=[DateTime]::UtcNow}
  $liveRows=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
  if($liveRows.Count -ne 1 -or $liveRows[0].ProcessId -ne $started.pid -or $liveRows[0].ExecutablePath -cne $exe -or ([DateTimeOffset]$liveRows[0].CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $started.creation_utc_ms){throw 'Started process terminal/identity changed during intro; no retry.'}
  try{$state=OwnState $started -RequireFocus;if((Elapsed $started) -lt 180){$stable=$null;$stableSince=$null}else{$key=($state.handle.ToString()+($state.bounds|ConvertTo-Json -Compress));if($key -ceq $stable){if(([DateTime]::UtcNow-$stableSince).TotalSeconds -ge 2){$started.handle=$state.handle;JsonFile $started 'start-record.json';JsonFile $state 'final-window-binding.json';break}}else{$stable=$key;$stableSince=[DateTime]::UtcNow}}}catch{$stable=$null;$stableSince=$null}
  Start-Sleep -Milliseconds 250
 }
 if($started.handle -eq 0){throw 'Intro/foreground did not stabilize; no automatic second start.'}
 JsonFile @{status='STARTED_BOUND_AWAITING_REVIEWED_T0_GUI_LOAD';at=(Get-Date).ToString('o')} 'start-result.json'
 Write-Output ($started|ConvertTo-Json);exit
}
$started=Get-Content (Join-Path $armDir 'start-record.json') -Raw -Encoding utf8|ConvertFrom-Json
if($Action -eq 'Finish'){
 if(Test-Path -LiteralPath (Join-Path $armDir 'close-request.json')){throw 'One normal-close request already attempted; no retry.'}
 $live=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
 if($live.Count -eq 0){RestoreOwnInstallation;exit}
 OwnState $started -BindWindow -ForClose|Out-Null;CheckInstalled
 $own=[Diagnostics.Process]::GetProcessById([int]$started.pid)
 try {
  if((Elapsed $started) -ge 470){throw 'No10s normal-close reserve.'}
  $own.Refresh();if($own.MainModule.FileName -cne $exe -or ([DateTimeOffset]$own.StartTime.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $started.creation_utc_ms -or $own.MainWindowHandle.ToInt64() -ne $started.handle){throw 'Direct-before-close identity mismatch.'}
  $clock=[Diagnostics.Stopwatch]::StartNew();$ok=$own.CloseMainWindow();JsonFile @{called_at=(Get-Date).ToString('o');bool_return=$ok;call_count=1} 'close-request.json'
  if(!$ok){throw 'CloseMainWindow false; no force/retry.'}
  while($clock.Elapsed.TotalSeconds -lt 10){$own.Refresh();if($own.HasExited){break};Start-Sleep -Milliseconds 100}
  $own.Refresh();if(!$own.HasExited){throw 'No normal exit within10s; leave original process/files.'}
  $exitCode=$own.ExitCode;JsonFile @{at=(Get-Date).ToString('o');has_exited=$true;exit_code=$exitCode} 'exit.json';RestoreOwnInstallation
 }finally{$own.Dispose()};exit
}
CheckInstalled
if($Action -eq 'Capture'){OwnState $started -BindWindow|Out-Null}else{OwnState $started -BindWindow -RequireFocus|Out-Null}
switch($Action){
 'Guard'{OwnState $started -BindWindow -RequireFocus|ConvertTo-Json -Depth 6}
 'Capture'{
  $beforeCapture=OwnState $started -BindWindow
  if($beforeCapture.foreground_handle -ne $started.handle){
   $attemptPath=Join-Path $armDir 'focus-restore-attempt.json'
   if(Test-Path -LiteralPath $attemptPath){throw 'Second focus loss; no repeat focus attempt.'}
   JsonFile @{at=(Get-Date).ToString('o');attempt_count=1;action='UNCHANGED_BEDIEN_CTP_CAPTURE';own_state=$beforeCapture} 'focus-restore-attempt.json'
  }
  $result=& powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $tool -Action Capture
  if($LASTEXITCODE -ne 0){throw 'Capture failed.'}
  $imagePath=Join-Path $armDir ($Label+'.png')
  Copy-Item -LiteralPath (Join-Path $workspace 'PROEVEN\automatisering\ctp-window.png') -Destination $imagePath
  $physicalState=OwnState $started -BindWindow -RequireFocus
  Add-Type -AssemblyName System.Drawing
  $picture=[Drawing.Image]::FromFile($imagePath)
  try{if($picture.Width -ne $physicalState.bounds.width -or $picture.Height -ne $physicalState.bounds.height){throw 'Captured physical PNG/window dimensions mismatch.'};JsonFile @{image=$imagePath;pixel_width=$picture.Width;pixel_height=$picture.Height;physical_window=$physicalState;coordinate_system='SetProcessDPIAware physical pixels; inspect original image or explicitly rescale';at=(Get-Date).ToString('o')} ($Label+'-physical-bounds.json')}finally{$picture.Dispose()}
 }
 'Read'{$value=ReadSnapshot $started ($Label+'.json') $Turn;$value|ConvertTo-Json -Depth 12}
 'Pass'{
  if(!$Previous){throw 'Previous accepted snapshot required; never blind n spam.'}
  $path=[IO.Path]::GetFullPath($Previous);if((Split-Path $path) -cne $armDir){throw 'Previous outside own arm.'}
  $before=Get-Content -LiteralPath $path -Raw -Encoding utf8|ConvertFrom-Json
  if(!$before.stable_twice -or $before.instance.pid -ne $started.pid -or $before.variant -cne $variant -or $Turn -ne $before.turn+1){throw 'Previous instance/variant/turn mismatch.'}
  OwnState $started -BindWindow -RequireFocus|Out-Null
  $inputResult=& powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $tool -Action Key -Keys n
  $inputResult|Set-Content -LiteralPath (Join-Path $armDir ('T'+$Turn+'-n.txt')) -Encoding utf8
  if($LASTEXITCODE -ne 0){throw 'n input failed; no retry.'}
  $poll=[Diagnostics.Stopwatch]::StartNew();$attempt=0;$accepted=$false
  while($poll.Elapsed.TotalSeconds -lt 30){
   Budget;OwnState $started -BindWindow|Out-Null
   Start-Sleep -Milliseconds 400;$attempt++
   try{$after=ReadSnapshot $started ('T'+$Turn+'-poll'+$attempt+'.json') $Turn}catch{if($_.Exception.Message -ceq 'UNSTABLE_DATASET_RETRY_ONLY'){continue};throw}
   $complete=$true
   foreach($old in $before.state.civilizations){$new=@($after.state.civilizations|Where-Object{$_.civ_id -eq $old.civ_id});if($new.Count -ne 1 -or $new[0].processed_round -ne $old.processed_round+1){$complete=$false}}
   if($complete){Copy-Item -LiteralPath (Join-Path $armDir ('T'+$Turn+'-poll'+$attempt+'.json')) -Destination (Join-Path $armDir ('T'+$Turn+'.json'));$accepted=$true;break}
  }
  JsonFile @{turn=$Turn;one_n=$true;native_all_round_plus_one=$accepted;polls=$attempt;elapsed_seconds=$poll.Elapsed.TotalSeconds;at=(Get-Date).ToString('o')} ('T'+$Turn+'-pass.json')
  if(!$accepted){throw 'No proved all-AI completed round; inspect screen; no additional n.'}
  Write-Output ('Accepted native completed round T'+$Turn)
 }
}
