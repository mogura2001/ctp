param([Parameter(Mandatory=$true)][ValidateRange(1,100)][int]$Turn,[Parameter(Mandatory=$true)][string]$Previous,[Parameter(Mandatory=$true)][ValidateSet('release-v1','U30-40')][string]$Arm)
$ErrorActionPreference='Stop'
$workspace='C:/GIT/ctp';$package=$PSScriptRoot;$armDir=Join-Path $package $Arm;$completionFolder=$armDir
$python='C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe'
$tool=Join-Path $workspace 'PROEVEN/Bedien-CTP.ps1'
$hostDir=Join-Path $armDir 'host'
$expectedAI=if($Arm -ceq 'U30-40'){'df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e'}else{'eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'}
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
 $media=[IO.DriveInfo]::new('E:')
 if($media.DriveType -ne [IO.DriveType]::CDRom -or -not $media.IsReady -or $media.VolumeLabel -cne 'CCTP'){throw 'Ordinary CD media unavailable'}
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
function FileHash($path){return (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
function CompletionAuthorization {
 $approval=Get-Content (Join-Path $completionFolder 'ROOT-CONTROL.json') -Raw|ConvertFrom-Json
 if($approval.allowed -ne $true -or $approval.arm -cne $Arm -or $approval.turn_min -ne 1 -or $approval.turn_max -ne 100 -or $approval.max_n -ne 100 -or $approval.pid -ne $gate.pid -or $approval.creation_filetime -ne $gate.creation_filetime -or $approval.window -ne $window.window -or $approval.run_id -cne $gate.run_id){throw 'Separate own root control gate required'}
 if($approval.source_pins_sha256 -cne (FileHash $pinPath)){throw 'Own source pins changed'}
 if($approval.start_sha256 -cne (FileHash (Join-Path $hostDir 'start.json')) -or $approval.window_sha256 -cne (FileHash (Join-Path $hostDir 'window.json'))){throw 'Immutable complete start/window hash changed'}
 if($Turn -ge 2 -and $approval.review_T1 -ne $true){throw 'Pause beforeT2: root T1 review required'}
 if($Turn -ge 27 -and $approval.review_T26 -ne $true){throw 'Pause beforeT27: root T26 review required'}
 if($Turn -ge 2 -and ($approval.review_T1_snapshot_sha256 -cne (FileHash (Join-Path $armDir 'T1.json')) -or $approval.review_T1_pass_sha256 -cne (FileHash (Join-Path $completionFolder 'TURN-T1-pass.json')))){throw 'Exact root-reviewed T1 snapshot/pass required'}
 if($Turn -ge 27 -and ($approval.review_T26_snapshot_sha256 -cne (FileHash (Join-Path $armDir 'T26.json')) -or $approval.review_T26_pass_sha256 -cne (FileHash (Join-Path $completionFolder 'TURN-T26-pass.json')))){throw 'Exact root-reviewed T26 snapshot/pass required'}
 $t0=Join-Path $armDir 'T0.json'
 if($approval.accepted_T0_sha256 -cne (FileHash $t0)){throw 'Accepted own T0 anchor changed'}
 foreach($pin in (Get-Content $pinPath -Raw|ConvertFrom-Json).sources){if((FileHash (Join-Path $workspace $pin.path)) -cne $pin.sha256){throw 'Own source changed'}}
}

CompletionAuthorization
$ownTokenPath=Join-Path $completionFolder ('TURN-T'+$Turn+'-consumed.json')
$ownPassPath=Join-Path $completionFolder ('TURN-T'+$Turn+'-pass.json')
if((Test-Path -LiteralPath $ownTokenPath) -or (Test-Path -LiteralPath $ownPassPath) -or (Test-Path -LiteralPath (Join-Path $armDir ('T'+$Turn+'-n.txt')))){throw 'Current completion turn/token/pass/input already exists'}
if($started.pid -ne $gate.pid -or $started.path -cne $exe -or $started.max_n -ne 100 -or $started.n_consumed -ne 0 -or $window.pid -ne $gate.pid -or $window.creation_utc_ms -ne $started.creation_utc_ms -or [Math]::Floor(([decimal]$gate.creation_filetime-[decimal]116444736000000000)/10000) -ne $started.creation_utc_ms){throw 'Root start/window/token count mismatch'}
$previousPath=[IO.Path]::GetFullPath($Previous)
if($previousPath -cne [IO.Path]::GetFullPath((Join-Path $armDir ('T'+($Turn-1)+'.json')))){throw 'Exact preceding own accepted snapshot required'}
$before=Get-Content -LiteralPath $previousPath -Raw|ConvertFrom-Json;CheckSnapshot $before ($Turn-1)
if(Test-Path -LiteralPath (Join-Path $armDir ('T'+$Turn+'.json'))){throw 'Never repeat accepted turn'}
$previousOwnPassHash=$null;$previousOwnTokenHash=$null
if($Turn -eq 1){
 if((FileHash $previousPath) -cne ((Get-Content (Join-Path $completionFolder 'ROOT-CONTROL.json') -Raw|ConvertFrom-Json).accepted_T0_sha256)){throw 'Exact accepted T0 anchor required'}
}else{
 $priorTokenPath=Join-Path $completionFolder ('TURN-T'+($Turn-1)+'-consumed.json')
 $priorPassPath=Join-Path $completionFolder ('TURN-T'+($Turn-1)+'-pass.json')
 $priorToken=Get-Content $priorTokenPath -Raw|ConvertFrom-Json;$priorPass=Get-Content $priorPassPath -Raw|ConvertFrom-Json
 $helperHash=FileHash $PSCommandPath
 if($priorPass.success -ne $true -or $priorPass.turn -ne $Turn-1 -or $priorPass.run_id -cne $gate.run_id -or $priorPass.pid -ne $gate.pid -or $priorPass.creation_filetime -ne $gate.creation_filetime -or $priorPass.accepted_snapshot_sha256 -cne (FileHash $previousPath) -or $priorPass.token_sha256 -cne (FileHash $priorTokenPath) -or $priorPass.helper_sha256 -cne $helperHash){throw 'Exact successful previous completion pass required'}
 if($priorToken.turn -ne $Turn-1 -or $priorToken.run_id -cne $gate.run_id -or $priorToken.pid -ne $gate.pid -or $priorToken.creation_filetime -ne $gate.creation_filetime -or $priorToken.helper_sha256 -cne $helperHash -or $priorToken.previous_snapshot_sha256 -cne (FileHash (Join-Path $armDir ('T'+($Turn-2)+'.json')))){throw 'Exact previous completion token required'}
 if($priorToken.start_sha256 -cne (FileHash (Join-Path $hostDir 'start.json')) -or $priorPass.start_sha256 -cne $priorToken.start_sha256){throw 'Prior immutable start mismatch'}
 if($priorPass.previous_pass_sha256 -cne $priorToken.previous_completion_pass_sha256 -or $priorPass.previous_token_sha256 -cne $priorToken.previous_completion_token_sha256){throw 'Prior token/pass chain fields differ'}
 if($Turn -eq 2){if($null -ne $priorPass.previous_pass_sha256 -or $null -ne $priorPass.previous_token_sha256){throw 'T1 chain must anchor directly in accepted T0'}}else{
  if($priorPass.previous_pass_sha256 -cne (FileHash (Join-Path $completionFolder ('TURN-T'+($Turn-2)+'-pass.json'))) -or $priorPass.previous_token_sha256 -cne (FileHash (Join-Path $completionFolder ('TURN-T'+($Turn-2)+'-consumed.json')))){throw 'Earlier chain link changed'}
 }
 $previousOwnPassHash=FileHash $priorPassPath;$previousOwnTokenHash=FileHash $priorTokenPath
}

Budget;OwnState
if((Elapsed) -ge 4380){throw 'No new n from4380s; root close reserve'}
# One bound T1 foreground capture before consuming its token; no extra key input.
if($Turn -eq 1){
 $focusLog=Join-Path $armDir 'T1-focus-before-token.log'
 & $tool -Action Capture -CaptureWaitForForeground -CaptureWaitTimeoutMs 3000 -ExpectedProcessId $gate.pid -ExpectedCreationUtcMs $started.creation_utc_ms -ExpectedWindowHandle $window.window > $focusLog
 if(-not $?){throw 'T1 bound foreground unavailable before token; no input'}
}
# Own tokens alone register input; complete host/start.json stays read-only/n0.

Budget;OwnState;CompletionAuthorization
if((Elapsed) -ge 4380){throw 'No late completion token/input'}
$token=[ordered]@{run_id=$gate.run_id;turn=$Turn;pid=$gate.pid;creation_filetime=$gate.creation_filetime;at_utc=[DateTime]::UtcNow.ToString('o');previous_snapshot_sha256=(FileHash $previousPath);previous_completion_pass_sha256=$previousOwnPassHash;previous_completion_token_sha256=$previousOwnTokenHash;helper_sha256=(FileHash $PSCommandPath);start_sha256=(FileHash (Join-Path $hostDir 'start.json'));accepted_T0_sha256=(FileHash (Join-Path $armDir 'T0.json'))}
$stream=[IO.File]::Open($ownTokenPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=[Text.Encoding]::UTF8.GetBytes(($token|ConvertTo-Json));$stream.Write($bytes,0,$bytes.Length);$stream.Flush()}finally{$stream.Dispose()}
Budget;OwnState;CompletionAuthorization
foreach($pin in (Get-Content $pinPath -Raw|ConvertFrom-Json).sources){if((FileHash (Join-Path $workspace $pin.path)) -cne $pin.sha256){throw 'Parent source changed before completion Key'}}
if((Elapsed) -ge 4380 -or (Test-Path -LiteralPath (Join-Path $armDir ('T'+$Turn+'-n.txt'))) -or (Test-Path -LiteralPath (Join-Path $armDir ('T'+$Turn+'.json')))){throw 'Final completion guards failed; token remains consumed'}
$inputResult=& $tool -Action Key -Keys n
$inputOK=$?
$inputResult|Set-Content -LiteralPath (Join-Path $armDir ('T'+$Turn+'-n.txt')) -Encoding utf8
if(-not $inputOK){throw 'n input failed; consumed token remains; no retry'}
$poll=[Diagnostics.Stopwatch]::StartNew();$attempt=0;$accepted=$false
while($poll.Elapsed.TotalSeconds -lt 30){
 Budget;OwnState;Start-Sleep -Milliseconds 400;$attempt++
 $name='T'+$Turn+'-poll'+$attempt;$output=Join-Path $armDir ($name+'.json')
 $oldPreference=$ErrorActionPreference
 try{$ErrorActionPreference='Continue';$text=& $python -X utf8 (Join-Path $package 'Lees-Duur.py') --pid $gate.pid --creation-filetime $gate.creation_filetime --variant $Arm --run-id $gate.run_id --snapshot-label $name --turn $Turn --pass-label passive-human-native-round --manifest (Join-Path $workspace 'PROEVEN/landbenchmark/20261027/participants.json') --output $output 2>&1;$readCode=$LASTEXITCODE}finally{$ErrorActionPreference=$oldPreference}
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
 $target=[IO.File]::Open((Join-Path $armDir ('T'+$Turn+'.json')),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None);try{$raw=[IO.File]::ReadAllBytes($output);$target.Write($raw,0,$raw.Length);$target.Flush()}finally{$target.Dispose()};$accepted=$true;break
}
$pass=[ordered]@{turn=$Turn;run_id=$gate.run_id;pid=$gate.pid;creation_filetime=$gate.creation_filetime;success=$accepted;one_n=$true;native_all_round_plus_one=$accepted;accepted_snapshot_sha256=$(if($accepted){FileHash (Join-Path $armDir ('T'+$Turn+'.json'))}else{$null});token_sha256=(FileHash $ownTokenPath);helper_sha256=(FileHash $PSCommandPath);polls=$attempt;elapsed_seconds=$poll.Elapsed.TotalSeconds;at=(Get-Date).ToString('o');operation='own_immutable_turn';start_sha256=(FileHash (Join-Path $hostDir 'start.json'));previous_pass_sha256=$previousOwnPassHash;previous_token_sha256=$previousOwnTokenHash;immutable_turn_protocol=$true}
$stream=[IO.File]::Open($ownPassPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=[Text.Encoding]::UTF8.GetBytes(($pass|ConvertTo-Json));$stream.Write($bytes,0,$bytes.Length);$stream.Flush()}finally{$stream.Dispose()}
if(!$accepted){throw 'No completed all-seven round within30s; root capture/normal close; no further n'}
Write-Output ('Accepted native completed round T'+$Turn)
