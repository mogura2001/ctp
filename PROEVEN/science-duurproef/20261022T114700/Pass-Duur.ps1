param([Parameter(Mandatory=$true)][ValidateRange(1,26)][int]$Turn,[Parameter(Mandatory=$true)][string]$Previous)
$ErrorActionPreference='Stop'
$workspace='C:/GIT/ctp';$package=$PSScriptRoot;$armDir=Join-Path $package 'variant'
$python='C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe'
$tool=Join-Path $workspace 'PROEVEN/Bedien-CTP.ps1'
$hostDir=Join-Path $workspace 'PROEVEN/science-duur-host/20261021/host3'
$exe=Join-Path $workspace 'CTP-proef/ctp_program/ctp/civctp.exe'
$gate=Get-Content (Join-Path $package 'ROOT-READER.json') -Raw|ConvertFrom-Json
if(-not $gate.allowed -or -not $gate.control_allowed -or $gate.variant -cne 'U30-40' -or $gate.turn_min -ne 0 -or $gate.turn_max -ne 26 -or [IO.Path]::GetFullPath($gate.output_directory) -cne [IO.Path]::GetFullPath($armDir)){throw 'Separate exact duration control gate required'}
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
 if((Elapsed) -ge 1500){throw 'Hard1500s deadline; no turn acceptance'}
 $rows=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'")
 if($rows.Count -ne 1 -or $rows[0].ProcessId -ne $gate.pid -or $rows[0].ExecutablePath -cne $exe -or ([DateTimeOffset]$rows[0].CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $started.creation_utc_ms){throw 'Exact unique own process identity changed'}
 $own=[Diagnostics.Process]::GetProcessById([int]$gate.pid)
 try{$own.Refresh();if($own.Path -cne $exe -or $own.StartTime.ToUniversalTime().ToFileTimeUtc() -ne $gate.creation_filetime -or $own.MainWindowHandle.ToInt64() -ne $window.window){throw 'Exact own process/time/window changed'}}finally{$own.Dispose()}
 if((Elapsed) -ge 1500){throw 'Late process query'}
}
function CheckSnapshot($value,$expectedTurn){
 if(!$value.stable_twice -or $value.run_id -cne $gate.run_id -or $value.variant -cne 'U30-40' -or $value.turn -ne $expectedTurn -or $value.instance.pid -ne $gate.pid -or $value.instance.creationtime_filetime -ne $gate.creation_filetime -or $value.binding.ai_sha256 -cne $gate.candidate_sha256 -or $value.binding.manifest_sha256 -cne $gate.manifest_sha256){throw 'Own stable snapshot instance/arm/turn/binary mismatch'}
 $civs=@($value.state.civilizations|Sort-Object civ_id)
 if(($civs.civ_id -join ',') -cne '2,3,4,5,6,7,8' -or @($value.loaded_checks.PSObject.Properties|Where-Object{$_.Value -ne $true}).Count){throw 'Missing civ or failed loaded check'}
 foreach($civ in $civs){if($civ.processed_round -ne $expectedTurn-1){throw 'Snapshot not exact native round T-1'}}
}
if($started.pid -ne $gate.pid -or $started.path -cne $exe -or $started.max_n -ne 26 -or $started.n_consumed -ne $Turn-1 -or $window.pid -ne $gate.pid -or $window.creation_utc_ms -ne $started.creation_utc_ms -or [Math]::Floor(([decimal]$gate.creation_filetime-[decimal]116444736000000000)/10000) -ne $started.creation_utc_ms){throw 'Root start/window/token count mismatch'}
$previousPath=[IO.Path]::GetFullPath($Previous)
if($previousPath -cne [IO.Path]::GetFullPath((Join-Path $armDir ('T'+($Turn-1)+'.json')))){throw 'Exact preceding own accepted snapshot required'}
$before=Get-Content -LiteralPath $previousPath -Raw|ConvertFrom-Json;CheckSnapshot $before ($Turn-1)
if(Test-Path -LiteralPath (Join-Path $armDir ('T'+$Turn+'.json'))){throw 'Never repeat accepted turn'}
Budget;OwnState
if((Elapsed) -ge 1440){throw 'No new n from1440s; root close reserve'}
# One bound T1 foreground capture before consuming its token; no extra key input.
if($Turn -eq 1){
 $focusLog=Join-Path $package 'T1-focus-before-token.log'
 & $tool -Action Capture -CaptureWaitForForeground -CaptureWaitTimeoutMs 3000 -ExpectedProcessId $gate.pid -ExpectedCreationUtcMs $started.creation_utc_ms -ExpectedWindowHandle $window.window > $focusLog
 if(-not $?){throw 'T1 bound foreground unavailable before token; no input'}
}
# Exclusive consumption BEFORE input; survives errors/interruption, no retry.
$tokenPath=Join-Path $armDir ('T'+$Turn+'-consumed.json')
$token=[ordered]@{run_id=$gate.run_id;turn=$Turn;pid=$gate.pid;creation_filetime=$gate.creation_filetime;at_utc=[DateTime]::UtcNow.ToString('o');previous_sha256=(Get-FileHash -LiteralPath $previousPath).Hash.ToLowerInvariant()}
$stream=[IO.File]::Open($tokenPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=[Text.Encoding]::UTF8.GetBytes(($token|ConvertTo-Json));$stream.Write($bytes,0,$bytes.Length);$stream.Flush()}finally{$stream.Dispose()}
$started.n_consumed=$Turn;$started|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $hostDir 'start.json') -Encoding utf8
Budget;OwnState;if((Elapsed) -ge 1440){throw 'Consumed token but no late input; root close'}
$inputResult=& $tool -Action Key -Keys n
$inputOK=$?
$inputResult|Set-Content -LiteralPath (Join-Path $armDir ('T'+$Turn+'-n.txt')) -Encoding utf8
if(-not $inputOK){throw 'n input failed; consumed token remains; no retry'}
$poll=[Diagnostics.Stopwatch]::StartNew();$attempt=0;$accepted=$false
while($poll.Elapsed.TotalSeconds -lt 30){
 Budget;OwnState;Start-Sleep -Milliseconds 400;$attempt++
 $name='T'+$Turn+'-poll'+$attempt;$output=Join-Path $armDir ($name+'.json')
 $oldPreference=$ErrorActionPreference
 try{$ErrorActionPreference='Continue';$text=& $python -X utf8 (Join-Path $package 'Lees-Duur.py') --pid $gate.pid --creation-filetime $gate.creation_filetime --variant U30-40 --run-id $gate.run_id --snapshot-label $name --turn $Turn --pass-label passive-human-native-round --manifest (Join-Path $workspace 'PROEVEN/selectie-pad-diagnose/20261020T192500/reader/participants.json') --output $output 2>&1;$readCode=$LASTEXITCODE}finally{$ErrorActionPreference=$oldPreference}
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
@{turn=$Turn;one_n=$true;native_all_round_plus_one=$accepted;polls=$attempt;elapsed_seconds=$poll.Elapsed.TotalSeconds;at=(Get-Date).ToString('o')}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $armDir ('T'+$Turn+'-pass.json')) -Encoding utf8
if(!$accepted){throw 'No completed all-seven round within30s; root capture/normal close; no further n'}
Write-Output ('Accepted native completed round T'+$Turn)
