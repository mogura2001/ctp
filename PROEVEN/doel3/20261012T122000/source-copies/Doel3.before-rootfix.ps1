param(
 [Parameter(Mandatory=$true)][ValidateSet('InstallStart','Guard','Capture','Read','Pass','Finish')][string]$Action,
 [ValidateSet('variant','baseline')][string]$Arm='variant',
 [int]$Turn=0,[string]$Previous='', [string]$Label='checkpoint'
)
$ErrorActionPreference='Stop'
$workspace='C:\GIT\ctp';$package=$PSScriptRoot;$armDir=Join-Path $package $Arm
$exe=Join-Path $workspace 'CTP-proef\ctp_program\ctp\civctp.exe'
$tool=Join-Path $workspace 'PROEVEN\Bedien-CTP.ps1'
$python='C:\Users\Stephan\AppData\Local\Programs\Python\Python312\python.exe'
$manifest=Get-Content (Join-Path $package 'manifest.json') -Raw -Encoding utf8|ConvertFrom-Json
$toolHash='d2dbbfcad3d9d8bec8e6a99a399d59561d8f9c4e9a48576a2aefc32e5997bc74'
$variant=if($Arm -eq 'variant'){'B2a-N30-TECHNICAL'}else{'original'}
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
public class Goal3Window {
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
function Elapsed($started){([Diagnostics.Stopwatch]::GetTimestamp()-[long]$started.start_monotonic_ticks)/[double]$started.monotonic_frequency}
function OwnState($started,[switch]$RequireFocus,[switch]$BindWindow){
 if((Elapsed $started) -ge 1785){throw '30min arm deadline; retain15s normal-close reserve.'}
 $rows=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
 if($rows.Count -ne 1 -or $rows[0].ProcessId -ne $started.pid -or $rows[0].ExecutablePath -cne $exe -or ([DateTimeOffset]$rows[0].CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $started.creation_utc_ms){throw 'Exact own process identity/unique civctp changed.'}
 $own=[Diagnostics.Process]::GetProcessById([int]$started.pid)
 try {
  $own.Refresh();$owner=[uint32]0;$h=$own.MainWindowHandle
  if($own.MainModule.FileName -cne $exe -or ([DateTimeOffset]$own.StartTime.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $started.creation_utc_ms){throw 'Retained process path/time mismatch.'}
  if($h -eq [IntPtr]::Zero -or [Goal3Window]::GetWindowThreadProcessId($h,[ref]$owner) -eq 0 -or $owner -ne $started.pid){throw 'Own HWND absent/unbound.'}
  if($BindWindow -and $h.ToInt64() -ne $started.handle){throw 'Bound HWND changed.'}
  if($RequireFocus -and [Goal3Window]::GetForegroundWindow() -ne $h){throw 'Own game not foreground; no input.'}
  $windows=[Collections.Generic.List[object]]::new()
  if(-not [Goal3Window]::EnumWindows({param($wh,$unused)
   $pidOwner=[uint32]0;[Goal3Window]::GetWindowThreadProcessId($wh,[ref]$pidOwner)|Out-Null
   if($pidOwner -eq $started.pid -and [Goal3Window]::IsWindowVisible($wh)){$title=[Text.StringBuilder]::new(1024);[Goal3Window]::GetWindowText($wh,$title,1024)|Out-Null;$windows.Add(@{handle=$wh.ToInt64();title=$title.ToString()})};return $true
  },[IntPtr]::Zero)){throw 'Own-window enumeration failed.'}
  if($windows.Count -ne 1 -or $windows[0].handle -ne $h.ToInt64() -or !$windows[0].title -or $windows[0].title -match 'Error|CD-ROM|Call to Power CD'){throw 'Modal/error/extra own window; stop.'}
  $r=New-Object Goal3Window+Rect;if(-not [Goal3Window]::GetWindowRect($h,[ref]$r)){throw 'Bounds unreadable.'}
  if((Elapsed $started) -ge 1785){throw 'Late OS query; no next action.'}
  return [ordered]@{pid=$started.pid;handle=$h.ToInt64();creation_utc_ms=$started.creation_utc_ms;foreground_handle=[Goal3Window]::GetForegroundWindow().ToInt64();elapsed_seconds=(Elapsed $started);bounds=@{left=$r.Left;top=$r.Top;right=$r.Right;bottom=$r.Bottom;width=$r.Right-$r.Left;height=$r.Bottom-$r.Top};title=$windows[0].title}
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
function ReadSnapshot($started,$name,$turn){
 OwnState $started -BindWindow|Out-Null
 $output=Join-Path $armDir $name
 $result=& $python -X utf8 (Join-Path $package 'Lees-Doel3.py') --pid $started.pid --variant $variant --run-id ('doel3-20261012T122000-'+$Arm) --snapshot-label $name --turn $turn --pass-label 'passive-human-native-round' --manifest (Join-Path $package 'participants.json') --output $output
 $result|Set-Content -LiteralPath (Join-Path $armDir ($name+'.stdout.txt')) -Encoding utf8
 if($LASTEXITCODE -ne 0){throw 'Snapshot rejected; no turn acceptance.'}
 $value=Get-Content $output -Raw -Encoding utf8|ConvertFrom-Json
 if($value.instance.pid -ne $started.pid -or [Math]::Floor(([decimal]$value.instance.creationtime_filetime-[decimal]116444736000000000)/10000) -ne $started.creation_utc_ms){throw 'Reader process creationtime mismatch.'}
 return $value
}
Budget
if((Hash $tool) -ne $toolHash){throw 'Reviewed Bedien-CTP changed.'}
if($Action -eq 'InstallStart'){
 if(Test-Path -LiteralPath (Join-Path $armDir 'execution.json')){throw 'Arm already attempted; no automatic retry/start.'}
 CountZero
 if((Hash (Join-Path $workspace 'ONTWERP\DOEL3-GAMEPLAYBEWIJS.md')) -ne $manifest.proposal_sha256){throw 'Reviewed goal3 proposal changed.'}
 foreach($pin in $manifest.input_manifests){if((Hash (Join-Path $workspace $pin.path)) -ne $pin.sha256){throw 'Pinned B1/B2a/B2b input manifest changed.'}}
 foreach($savePath in $manifest.T0_paths){if((Hash (Join-Path $workspace $savePath)) -ne $manifest.T0_sha256){throw 'Fixed T0 changed; no install/start.'}}
 foreach($pin in $manifest.protected){if((Hash (Join-Path $workspace $pin.path)) -ne $pin.sha256){throw 'Pre-run protected/current pin changed; no install.'}}
 foreach($entry in $manifest.files){
  $target=Join-Path $workspace $entry.path
  if($entry.existed){if((Hash $target) -ne $entry.before_sha256 -or (Hash (Join-Path (Join-Path $package 'backups') $entry.path)) -ne $entry.before_sha256){throw 'True pre-run/backup identity changed.'}}
  elseif(Test-Path -LiteralPath $target){throw 'Previously absent FLI now exists; no overwrite.'}
  $expected=$entry.("${Arm}_sha256");if($null -ne $expected){$source=Join-Path (Join-Path $package ('candidate\'+$Arm)) $entry.path;if((Hash $source) -ne $expected){throw 'Candidate changed before any installation.'}}
 }
 JsonFile @{at=(Get-Date).ToString('o');install_attempted=$true;arm=$Arm} 'execution.json'
 CountZero
 foreach($entry in $manifest.files){
  $source=Join-Path (Join-Path $package ('candidate\'+$Arm)) $entry.path;$target=Join-Path $workspace $entry.path;$expected=$entry.("${Arm}_sha256")
  if($null -ne $expected){if((Hash $source) -ne $expected){throw 'Prepared candidate hash changed.'};Copy-Item -LiteralPath $source -Destination $target}
 }
 CheckInstalled;Budget;CountZero
 $ticks=[Diagnostics.Stopwatch]::GetTimestamp()
 $result=& powershell.exe -NoProfile -File $tool -Action Start 2>&1;$code=$LASTEXITCODE
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
 OwnState $started -BindWindow|Out-Null;CheckInstalled
 $own=[Diagnostics.Process]::GetProcessById([int]$started.pid)
 try {
  if((Elapsed $started) -ge 1785){throw 'No normal-close reserve.'}
  $own.Refresh();if($own.MainModule.FileName -cne $exe -or ([DateTimeOffset]$own.StartTime.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $started.creation_utc_ms -or $own.MainWindowHandle.ToInt64() -ne $started.handle){throw 'Direct-before-close identity mismatch.'}
  $clock=[Diagnostics.Stopwatch]::StartNew();$ok=$own.CloseMainWindow();JsonFile @{called_at=(Get-Date).ToString('o');bool_return=$ok;call_count=1} 'close-request.json'
  if(!$ok){throw 'CloseMainWindow false; no force/retry.'}
  while($clock.Elapsed.TotalSeconds -lt 10){$own.Refresh();if($own.HasExited){break};Start-Sleep -Milliseconds 100}
  $own.Refresh();if(!$own.HasExited){throw 'No normal exit within10s; leave original process/files.'}
  $exitCode=$own.ExitCode;CountZero;Budget
  foreach($entry in $manifest.files){
   $target=Join-Path $workspace $entry.path
   if($entry.existed){$backup=Join-Path (Join-Path $package 'backups') $entry.path;if((Hash $backup) -ne $entry.before_sha256){throw 'Restore backup changed.'};Copy-Item -LiteralPath $backup -Destination $target}
   else{if(Test-Path -LiteralPath $target){if((Hash $target) -ne $entry.variant_sha256){throw 'New FLI changed; preserve.'};Remove-Item -LiteralPath $target}}
  }
  $checks=@(foreach($entry in $manifest.files){$target=Join-Path $workspace $entry.path;$present=Test-Path -LiteralPath $target;$hash=if($present){Hash $target}else{$null};@{path=$entry.path;present=$present;sha256=$hash;match=($present -eq $entry.existed -and $hash -eq $entry.before_sha256)}})
  JsonFile @{at=(Get-Date).ToString('o');exit_code=$exitCode;all_civctp_count=0;files=$checks;profile_sha256=(Hash (Join-Path $workspace 'CTP-proef\ctp_program\ctp\userprofile.txt'));saves_preserved=$true} 'restore.json'
  if(@($checks|Where-Object{!$_.match}).Count){throw 'Restoration mismatch.'}
 }finally{$own.Dispose()};exit
}
CheckInstalled
OwnState $started -BindWindow -RequireFocus|Out-Null
switch($Action){
 'Guard'{OwnState $started -BindWindow -RequireFocus|ConvertTo-Json -Depth 6}
 'Capture'{
  $result=& powershell.exe -NoProfile -File $tool -Action Capture
  if($LASTEXITCODE -ne 0){throw 'Capture failed.'}
  Copy-Item -LiteralPath (Join-Path $workspace 'PROEVEN\automatisering\ctp-window.png') -Destination (Join-Path $armDir ($Label+'.png'))
 }
 'Read'{$value=ReadSnapshot $started ($Label+'.json') $Turn;$value|ConvertTo-Json -Depth 12}
 'Pass'{
  if(!$Previous){throw 'Previous accepted snapshot required; never blind n spam.'}
  $path=[IO.Path]::GetFullPath($Previous);if((Split-Path $path) -cne $armDir){throw 'Previous outside own arm.'}
  $before=Get-Content -LiteralPath $path -Raw -Encoding utf8|ConvertFrom-Json
  if(!$before.stable_twice -or $before.instance.pid -ne $started.pid -or $before.variant -cne $variant -or $Turn -ne $before.turn+1){throw 'Previous instance/variant/turn mismatch.'}
  OwnState $started -BindWindow -RequireFocus|Out-Null
  $inputResult=& powershell.exe -NoProfile -File $tool -Action Key -Keys n
  $inputResult|Set-Content -LiteralPath (Join-Path $armDir ('T'+$Turn+'-n.txt')) -Encoding utf8
  if($LASTEXITCODE -ne 0){throw 'n input failed; no retry.'}
  $poll=[Diagnostics.Stopwatch]::StartNew();$attempt=0;$accepted=$false
  while($poll.Elapsed.TotalSeconds -lt 30){
   Start-Sleep -Milliseconds 400;$attempt++
   try{$after=ReadSnapshot $started ('T'+$Turn+'-poll'+$attempt+'.json') $Turn}catch{continue}
   $complete=$true
   foreach($old in $before.state.civilizations){$new=@($after.state.civilizations|Where-Object{$_.civ_id -eq $old.civ_id});if($new.Count -ne 1 -or $new[0].processed_round -ne $old.processed_round+1){$complete=$false}}
   if($complete){Copy-Item -LiteralPath (Join-Path $armDir ('T'+$Turn+'-poll'+$attempt+'.json')) -Destination (Join-Path $armDir ('T'+$Turn+'.json'));$accepted=$true;break}
  }
  JsonFile @{turn=$Turn;one_n=$true;native_all_round_plus_one=$accepted;polls=$attempt;elapsed_seconds=$poll.Elapsed.TotalSeconds;at=(Get-Date).ToString('o')} ('T'+$Turn+'-pass.json')
  if(!$accepted){throw 'No proved all-AI completed round; inspect screen; no additional n.'}
  Write-Output ('Accepted native completed round T'+$Turn)
 }
}
