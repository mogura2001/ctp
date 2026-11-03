param([Parameter(Mandatory=$true)][ValidateRange(85,85)][int]$Turn,[Parameter(Mandatory=$true)][string]$Previous,[Parameter(Mandatory=$true)][ValidateSet('U30-40')][string]$Arm)
$ErrorActionPreference='Stop'
$workspace='C:/GIT/ctp';$recoveryFolder=$PSScriptRoot;$package='C:/GIT/ctp/PROEVEN/uitbreiding-lang/20261022T122400';$armDir=Join-Path $package $Arm
$python='C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe'
$tool=Join-Path $workspace 'PROEVEN/Bedien-CTP.ps1'
$hostDir=Join-Path $workspace ('PROEVEN/uitbreiding-lang-host/20261022/'+$Arm)
$expectedAI=@{'release-v1'='eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890';'U30-40'='df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e'}[$Arm]
$exe=Join-Path $workspace 'CTP-proef/ctp_program/ctp/civctp.exe'
$gate=Get-Content (Join-Path $armDir 'ROOT-READER.json') -Raw|ConvertFrom-Json
if(-not $gate.allowed -or -not $gate.control_allowed -or $gate.variant -cne $Arm -or $gate.ai_sha256 -cne $expectedAI -or $gate.manifest_sha256 -cne '5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152' -or $gate.turn_min -ne 0 -or $gate.turn_max -ne 100 -or $gate.max_n -ne 100 -or [IO.Path]::GetFullPath($gate.output_directory) -cne [IO.Path]::GetFullPath($armDir)){throw 'Separate exact duration control gate required'}
$pinPath=Join-Path $package 'SOURCE-PINS.json'
if((Get-FileHash -LiteralPath $pinPath).Hash.ToLowerInvariant() -ne $gate.source_pins_sha256){throw 'Duration source pins changed'}
foreach($pin in (Get-Content $pinPath -Raw|ConvertFrom-Json).sources){if((Get-FileHash -LiteralPath (Join-Path $workspace $pin.path)).Hash.ToLowerInvariant() -ne $pin.sha256){throw "Duration input changed: $($pin.path)"}}
$started=Get-Content (Join-Path $hostDir 'start.json') -Raw|ConvertFrom-Json
$window=Get-Content (Join-Path $hostDir 'window.json') -Raw|ConvertFrom-Json
function Elapsed {([DateTime]::UtcNow-[DateTime]::Parse($started.start_utc).ToUniversalTime()).TotalSeconds}
function Budget {
 $value=& $python (Join-Path $workspace 'PROEVEN/Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d;$code=$LASTEXITCODE
 if($code -eq 2){$value=& $python (Join-Path $workspace 'PROEVEN/Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d;$code=$LASTEXITCODE}
 $value|Set-Content -LiteralPath (Join-Path $armDir 'latest-budget.json') -Encoding utf8
 if($code -notin @(0,25)){throw 'Budget stop/unknown; root must close/restore; PC stays on'}
 if($code -eq 25){Write-Warning 'Weekbudget25%ofminder resterend'}
}
function OwnState {
 if((Elapsed) -ge 4500){throw 'Hard4500s deadline; no turn acceptance'}
 $rows=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'")
 if($rows.Count -ne 1 -or $rows[0].ProcessId -ne $gate.pid -or $rows[0].ExecutablePath -cne $exe -or ([DateTimeOffset]$rows[0].CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $started.creation_utc_ms){throw 'Exact unique own process identity changed'}
 $own=[Diagnostics.Process]::GetProcessById([int]$gate.pid)
 try{$own.Refresh();if($own.Path -cne $exe -or $own.StartTime.ToUniversalTime().ToFileTimeUtc() -ne $gate.creation_filetime -or $own.MainWindowHandle.ToInt64() -ne $window.window){throw 'Exact own process/time/window changed'}}finally{$own.Dispose()}
 if((Elapsed) -ge 4500){throw 'Late process query'}
}
function CheckSnapshot($value,$expectedTurn){
 if(!$value.stable_twice -or $value.run_id -cne $gate.run_id -or $value.variant -cne $Arm -or $value.turn -ne $expectedTurn -or $value.instance.pid -ne $gate.pid -or $value.instance.creationtime_filetime -ne $gate.creation_filetime -or $value.binding.ai_sha256 -cne $gate.ai_sha256 -or $value.binding.manifest_sha256 -cne $gate.manifest_sha256){throw 'Own stable snapshot instance/arm/turn/binary mismatch'}
 $civs=@($value.state.civilizations|Sort-Object civ_id)
 if(($civs.civ_id -join ',') -cne '2,3,4,5,6,7,8'){throw 'Missing civ'}
 $requiredChecks=@('headers_sections_sizes','all_three_scorecalls','payload_and_original_ranges','only_original_HIGHLOW_relocation_adjustment','all_five_B2_hooks','N30_payload_bound')
 $allChecks=$requiredChecks+@('new_payload_and_all_nine_windows_bound')
 if((@($value.loaded_checks.PSObject.Properties.Name|Sort-Object) -join ',') -cne (@($allChecks|Sort-Object) -join ',')){throw 'Exact arm loaded check names required'}
 foreach($name in $requiredChecks){if($value.loaded_checks.$name -ne $true){throw 'Required loaded check failed'}}
 if($value.loaded_checks.new_payload_and_all_nine_windows_bound -ne ($Arm -ceq 'U30-40')){throw 'Exact arm-only payload check required'}
 foreach($civ in $civs){if($civ.processed_round -ne $expectedTurn-1){throw 'Snapshot not exact native round T-1'}}
}
function RecoveryPins {
 $authorization=Get-Content (Join-Path $recoveryFolder 'ROOT-RECOVERY.json') -Raw|ConvertFrom-Json
 if($authorization.allowed -ne $true -or $authorization.failure_before_key_confirmed -ne $true -or $authorization.turn -ne 85 -or $authorization.arm -cne 'U30-40' -or $authorization.pid -ne 40488 -or $authorization.creation_filetime -ne 134371535950250712 -or $authorization.window -ne 395504 -or $authorization.run_id -cne 'uitbreiding-lang-20261022-U30-40'){throw 'Separate exact root recovery gate required'}
 if($gate.pid -ne 40488 -or $gate.creation_filetime -ne 134371535950250712 -or $gate.run_id -cne $authorization.run_id -or $window.window -ne 395504){throw 'Recovery exact live identity mismatch'}
 $ownPins=Join-Path $recoveryFolder 'SOURCE-PINS.json'
 if((Get-FileHash -LiteralPath $ownPins).Hash.ToLowerInvariant() -cne $authorization.source_pins_sha256){throw 'Recovery source manifest changed'}
 foreach($pin in (Get-Content $ownPins -Raw|ConvertFrom-Json).sources){if((Get-FileHash -LiteralPath (Join-Path $workspace $pin.path)).Hash.ToLowerInvariant() -cne $pin.sha256){throw 'Recovery pinned evidence/source changed'}}
}
function FileHash($path){return (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
$oldStartHash='f9b6099e7ef664581a25dcf1682c01657586b7c7bd1b2b2f815dcc49be1b0aa8'
$oldTokenHash='46770c6a31da687e164522a10cebca6c0eadbfc7d2e9fcc8eaf405fee7fb942f'
$oldSnapshotHash='a9c9cb52e23c0cc14ae4e9b75fc1b4e6ceb509658fe00cb58b861f6442d0de5a'
$oldRecheckHash='f649e8638bf5df625ab44a70a391b43d7b277d26cb1534e1bd35ca9182480ad1'
$startPath=[IO.Path]::GetFullPath((Join-Path $hostDir 'start.json'))
$exactStart=[IO.Path]::GetFullPath('C:/GIT/ctp/PROEVEN/uitbreiding-lang-host/20261022/U30-40/start.json')
if($startPath -cne $exactStart -or -not $startPath.StartsWith(([IO.Path]::GetFullPath($workspace)+'\'),[StringComparison]::OrdinalIgnoreCase)){throw 'Metadata destination outside exact own workspace host'}
RecoveryPins
if((FileHash $startPath) -cne $oldStartHash -or (FileHash (Join-Path $hostDir 'start-pre-T85-registratieherstel.json')) -cne $oldStartHash){throw 'Original84 metadata bytes changed'}
if((FileHash (Join-Path $armDir 'T85-consumed.json')) -cne $oldTokenHash -or (FileHash (Join-Path $armDir 'T84.json')) -cne $oldSnapshotHash -or (FileHash (Join-Path $armDir 'T84-preinput-recheck.json')) -cne $oldRecheckHash){throw 'Original pre-input evidence changed'}
if(Test-Path -LiteralPath (Join-Path $armDir 'T85-n.txt')){throw 'Prior input evidence exists; no recovery'}
$incident=Get-Content (Join-Path $hostDir 'INCIDENT-T85.json') -Raw|ConvertFrom-Json
if($incident.status -cne 'PROVEN_PREINPUT_METADATA_FAILURE_PENDING_REVIEWED_RECOVERY' -or $incident.pid -ne 40488 -or $incident.creation_filetime -ne 134371535950250712 -or $incident.accepted_turn -ne 84 -or $incident.native_round -ne 83 -or $incident.no_T85_n_log -ne $true -or $incident.failed_token_retained -ne $true){throw 'Root pre-input incident binding required'}
if($started.pid -ne $gate.pid -or $started.path -cne $exe -or $started.max_n -ne 100 -or $started.n_consumed -ne $Turn-1 -or $window.pid -ne $gate.pid -or $window.creation_utc_ms -ne $started.creation_utc_ms -or [Math]::Floor(([decimal]$gate.creation_filetime-[decimal]116444736000000000)/10000) -ne $started.creation_utc_ms){throw 'Root start/window/token count mismatch'}
$previousPath=[IO.Path]::GetFullPath($Previous)
if($previousPath -cne [IO.Path]::GetFullPath((Join-Path $armDir ('T'+($Turn-1)+'.json')))){throw 'Exact preceding own accepted snapshot required'}
$before=Get-Content -LiteralPath $previousPath -Raw|ConvertFrom-Json;CheckSnapshot $before ($Turn-1)
if(Test-Path -LiteralPath (Join-Path $armDir ('T'+$Turn+'.json'))){throw 'Never repeat accepted turn'}
Budget;OwnState
if((Elapsed) -ge 4380){throw 'No new n from4380s; root close reserve'}
# One bound T1 foreground capture before consuming its token; no extra key input.
if($Turn -eq 1){
 $focusLog=Join-Path $armDir 'T1-focus-before-token.log'
 & $tool -Action Capture -CaptureWaitForForeground -CaptureWaitTimeoutMs 3000 -ExpectedProcessId $gate.pid -ExpectedCreationUtcMs $started.creation_utc_ms -ExpectedWindowHandle $window.window > $focusLog
 if(-not $?){throw 'T1 bound foreground unavailable before token; no input'}
}
# One fresh bound read before the separate recovery token; original token is immutable.
$priorRecheck=Get-Content (Join-Path $armDir 'T84-preinput-recheck.json') -Raw|ConvertFrom-Json
CheckSnapshot $priorRecheck 84
if(($priorRecheck.state|ConvertTo-Json -Depth 100 -Compress) -cne ($before.state|ConvertTo-Json -Depth 100 -Compress) -or ($priorRecheck.instance|ConvertTo-Json -Compress) -cne ($before.instance|ConvertTo-Json -Compress)){throw 'Preserved recheck differs from accepted84'}
$freshLabel='T84-herstel85-immediate';$freshPath=Join-Path $armDir ($freshLabel+'.json')
if(Test-Path -LiteralPath $freshPath){throw 'Fresh recovery read path already used'}
& $python -X utf8 (Join-Path $package 'Lees-Duur.py') --pid $gate.pid --creation-filetime $gate.creation_filetime --variant $Arm --run-id $gate.run_id --snapshot-label $freshLabel --turn 84 --pass-label passive-human-native-round --manifest (Join-Path $workspace 'PROEVEN/selectie-pad-diagnose/20261020T192500/reader/participants.json') --output $freshPath > (Join-Path $recoveryFolder 'immediate-read.log')
if(-not $?){throw 'Fresh pre-input recovery snapshot rejected'}
$fresh=Get-Content $freshPath -Raw|ConvertFrom-Json;CheckSnapshot $fresh 84
if(($fresh.state|ConvertTo-Json -Depth 100 -Compress) -cne ($before.state|ConvertTo-Json -Depth 100 -Compress) -or ($fresh.instance|ConvertTo-Json -Compress) -cne ($before.instance|ConvertTo-Json -Compress)){throw 'Live state no longer exact accepted84; no input'}
Budget;OwnState;RecoveryPins
if((Elapsed) -ge 4380 -or (FileHash $startPath) -cne $oldStartHash -or (Test-Path -LiteralPath (Join-Path $armDir 'T85-n.txt'))){throw 'Recovery pre-token state/deadline changed'}
$tokenPath=Join-Path $recoveryFolder 'T85-recovery-consumed.json'
$token=[ordered]@{run_id=$gate.run_id;turn=85;pid=$gate.pid;creation_filetime=$gate.creation_filetime;at_utc=[DateTime]::UtcNow.ToString('o');original_failed_token_sha256=$oldTokenHash;previous_sha256=$oldSnapshotHash;preserved_recheck_sha256=$oldRecheckHash;immediate_recheck_sha256=(FileHash $freshPath);old_start_sha256=$oldStartHash;helper_sha256=(FileHash $PSCommandPath);root_preinput_incident_sha256=(FileHash (Join-Path $hostDir 'INCIDENT-T85.json'))}
$stream=[IO.File]::Open($tokenPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=[Text.Encoding]::UTF8.GetBytes(($token|ConvertTo-Json));$stream.Write($bytes,0,$bytes.Length);$stream.Flush()}finally{$stream.Dispose()}
# Only metadata replacement may retry; never retry input or an ambiguous outcome.
$started.n_consumed=85;$expectedBytes=[Text.Encoding]::UTF8.GetBytes(($started|ConvertTo-Json))
$digest=[Security.Cryptography.SHA256]::Create()
try{$expected85Hash=([BitConverter]::ToString($digest.ComputeHash($expectedBytes))).Replace('-','').ToLowerInvariant()}finally{$digest.Dispose()}
$tempPath=[IO.Path]::GetFullPath((Join-Path $hostDir ('start-T85-recovery-'+[Guid]::NewGuid().ToString('N')+'.tmp')))
if([IO.Path]::GetDirectoryName($tempPath) -cne [IO.Path]::GetDirectoryName($exactStart) -or -not $tempPath.StartsWith(([IO.Path]::GetFullPath($workspace)+'\'),[StringComparison]::OrdinalIgnoreCase)){throw 'Temp outside exact own host'}
$stream=[IO.File]::Open($tempPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$stream.Write($expectedBytes,0,$expectedBytes.Length);$stream.Flush($true)}finally{$stream.Dispose()}
$attempts=[Collections.Generic.List[object]]::new();$replaced=$false
for($attempt=1;$attempt -le 4;$attempt++){
 if((FileHash $startPath) -cne $oldStartHash -or (FileHash $tempPath) -cne $expected85Hash){throw 'Unexpected destination/temp; no replace or input retry'}
 try{[IO.File]::Replace($tempPath,$exactStart,$null);$replaced=$true}
 catch{
  $cause=$_.Exception;while($cause.InnerException){$cause=$cause.InnerException}
  $attempts.Add(@{attempt=$attempt;error=$cause.Message;at_utc=[DateTime]::UtcNow.ToString('o')})
  @{stage='REPLACE_EXCEPTION';attempt=$attempt;destination=$startPath;temp_path=$tempPath;old84_sha256=$oldStartHash;expected85_sha256=$expected85Hash;error=$cause.Message;error_type=$cause.GetType().FullName;at_utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content -LiteralPath (Join-Path $recoveryFolder 'REGISTRATION-ERRORS.jsonl') -Encoding utf8
  if($cause -isnot [IO.IOException]){throw}
  if((FileHash $startPath) -cne $oldStartHash -or -not (Test-Path -LiteralPath $tempPath) -or (FileHash $tempPath) -cne $expected85Hash){throw 'Ambiguous IO replacement outcome; no rollback/input'}
  if($attempt -ge 4){throw 'Four metadata IO attempts failed; stop without input'}
  Start-Sleep -Milliseconds 100
 }
 if($replaced){break}
}
if(-not $replaced -or (FileHash $startPath) -cne $expected85Hash -or (Test-Path -LiteralPath $tempPath)){throw 'Atomic metadata85 readback not exact; no input'}
@{destination=$startPath;temp_path=$tempPath;old84_sha256=$oldStartHash;expected85_sha256=$expected85Hash;attempts=$attempt;io_failures=$attempts.ToArray();replaced=$true;readback_exact=$true;at_utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $recoveryFolder 'REGISTRATION.json') -Encoding utf8
Budget;OwnState;RecoveryPins
foreach($pin in (Get-Content $pinPath -Raw|ConvertFrom-Json).sources){if((Get-FileHash -LiteralPath (Join-Path $workspace $pin.path)).Hash.ToLowerInvariant() -ne $pin.sha256){throw 'Parent source changed before recovery Key'}}
if((Elapsed) -ge 4380 -or (FileHash $startPath) -cne $expected85Hash -or (Test-Path -LiteralPath (Join-Path $armDir 'T85-n.txt')) -or (Test-Path -LiteralPath (Join-Path $armDir 'T85.json'))){throw 'Final recovery guards failed; token remains consumed'}
$inputResult=& $tool -Action Key -Keys n
$inputOK=$?
$inputResult|Set-Content -LiteralPath (Join-Path $armDir ('T'+$Turn+'-n.txt')) -Encoding utf8
if(-not $inputOK){throw 'n input failed; consumed token remains; no retry'}
$poll=[Diagnostics.Stopwatch]::StartNew();$attempt=0;$accepted=$false
while($poll.Elapsed.TotalSeconds -lt 30){
 Budget;OwnState;Start-Sleep -Milliseconds 400;$attempt++
 $name='T'+$Turn+'-poll'+$attempt;$output=Join-Path $armDir ($name+'.json')
 $oldPreference=$ErrorActionPreference
 try{$ErrorActionPreference='Continue';$text=& $python -X utf8 (Join-Path $package 'Lees-Duur.py') --pid $gate.pid --creation-filetime $gate.creation_filetime --variant $Arm --run-id $gate.run_id --snapshot-label $name --turn $Turn --pass-label passive-human-native-round --manifest (Join-Path $workspace 'PROEVEN/selectie-pad-diagnose/20261020T192500/reader/participants.json') --output $output 2>&1;$readCode=$LASTEXITCODE}finally{$ErrorActionPreference=$oldPreference}
 $text|Set-Content -LiteralPath (Join-Path $armDir ($name+'.stdout.txt')) -Encoding utf8
 if($readCode -ne 0){
  if(Test-Path -LiteralPath $output){$failure=Get-Content $output -Raw|ConvertFrom-Json;if($failure.status -ceq 'rejected' -and $failure.error -ceq 'Unstable complete snapshot; no turn acceptance'){continue}}
  throw 'Fatal snapshot rejection; no retry/additional n; root capture and normal close'
 }
 $after=Get-Content -LiteralPath $output -Raw|ConvertFrom-Json
 OwnState;if($poll.Elapsed.TotalSeconds -ge 30){break}
 $rounds=@($after.state.civilizations|Sort-Object civ_id)
 if(($rounds.civ_id -join ',') -cne '2,3,4,5,6,7,8'){throw 'Missing/extra civ; no retry'}
 foreach($old in $before.state.civilizations){$new=@($rounds|Where-Object{$_.civ_id -eq $old.civ_id});if($new[0].processed_round -gt $old.processed_round+1 -or $new[0].processed_round -lt $old.processed_round){throw 'Native round skipped/reversed'}}
 if(@($rounds|Where-Object{$_.processed_round -ne $Turn-1}).Count){continue}
 CheckSnapshot $after $Turn
 Copy-Item -LiteralPath $output -Destination (Join-Path $armDir ('T'+$Turn+'.json'));$accepted=$true;break
}
@{turn=$Turn;one_n=$true;recovery_after_proven_preinput_metadata_failure=$true;original_failed_token_preserved=$true;recovery_token=$tokenPath;registration_sha256=(FileHash (Join-Path $recoveryFolder 'REGISTRATION.json'));helper_sha256=(FileHash $PSCommandPath);root_incident_sha256=(FileHash (Join-Path $hostDir 'INCIDENT-T85.json'));plain_100_token_protocol=$false;native_all_round_plus_one=$accepted;polls=$attempt;elapsed_seconds=$poll.Elapsed.TotalSeconds;at=(Get-Date).ToString('o')}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $armDir ('T'+$Turn+'-pass.json')) -Encoding utf8
if(!$accepted){throw 'No completed all-seven round within30s; root capture/normal close; no further n'}
Write-Output ('Accepted native completed round T'+$Turn)
