$ErrorActionPreference='Stop'
Set-Location C:/GIT/ctp
$hostDir=$PSScriptRoot
$package='C:/GIT/ctp/PROEVEN/science-duurproef/20261021T150600'
$python='C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe'
$start=Get-Content "$hostDir/start.json" -Raw|ConvertFrom-Json
$window=Get-Content "$hostDir/window.json" -Raw|ConvertFrom-Json
$gate=Get-Content "$package/ROOT-READER.json" -Raw|ConvertFrom-Json
if($start.n_consumed -ne 1 -or $start.pid -ne $gate.pid -or (Test-Path "$package/variant/T1.json") -or (Test-Path "$package/variant/T1-n.txt") -or -not (Test-Path "$package/variant/T1-consumed.json")){throw 'Not exact pre-input failure state'}
if(([DateTime]::UtcNow-[DateTime]::Parse($start.start_utc).ToUniversalTime()).TotalSeconds -ge 1200){throw 'Insufficient duration reserve'}
$budget=& $python PROEVEN/Controleer-Weekbudget.py --thread 01a0f7b4-4751-7513-b510-3835ce43f47d
if(($budget|ConvertFrom-Json).state -notin @('ok','warn')){throw 'Budget unavailable/stop'}
$budget|Set-Content "$hostDir/budget-before-focus-recovery.json" -Encoding utf8
function ReadOwn($label,$turn){
 $output="$package/variant/$label.json"
 & $python "$package/Lees-Duur.py" --pid $gate.pid --creation-filetime $gate.creation_filetime --variant U30-40 --run-id $gate.run_id --snapshot-label $label --turn $turn --pass-label passive-human-native-round --manifest PROEVEN/selectie-pad-diagnose/20261020T192500/reader/participants.json --output $output > "$hostDir/$label.log"
 if(-not $?){throw 'Recovery snapshot rejected'}
 $value=Get-Content $output -Raw|ConvertFrom-Json
 if(-not $value.stable_twice -or $value.instance.pid -ne $gate.pid -or $value.instance.creationtime_filetime -ne $gate.creation_filetime -or @($value.state.civilizations).Count -ne 7 -or (($value.state.civilizations|Sort-Object civ_id).civ_id -join ',') -cne '2,3,4,5,6,7,8' -or @($value.state.civilizations|Where-Object processed_round -ne ($turn-1)).Count){throw 'Exact recovery round/instance not proved'}
 return $value
}
$before=ReadOwn 'T0-focus-recheck' 0
# Preserve failed T1 token. A distinct one-shot recovery requires fresh proof
# that all seven native rounds are still -1; never retry an ambiguous action.
$tokenPath=Join-Path $hostDir 'focus-recovery-T1-consumed.json'
$token=@{pid=$gate.pid;creation_filetime=$gate.creation_filetime;run_id=$gate.run_id;turn=1;earlier_failure='SetForegroundWindow returned false before SendWait';before_sha256=(Get-FileHash "$package/variant/T0-focus-recheck.json").Hash.ToLower();original_failed_token_sha256=(Get-FileHash "$package/variant/T1-consumed.json").Hash.ToLower();at_utc=[DateTime]::UtcNow.ToString('o')}
$stream=[IO.File]::Open($tokenPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=[Text.Encoding]::UTF8.GetBytes(($token|ConvertTo-Json));$stream.Write($bytes,0,$bytes.Length);$stream.Flush()}finally{$stream.Dispose()}
& ./PROEVEN/Bedien-CTP.ps1 -Action Capture -CaptureWaitForForeground -CaptureWaitTimeoutMs 3000 -ExpectedProcessId $gate.pid -ExpectedCreationUtcMs $start.creation_utc_ms -ExpectedWindowHandle $window.window > "$hostDir/immediate-before-recovery.log"
if(-not $?){throw 'No bound foreground, token consumed, no input'}
& ./PROEVEN/Bedien-CTP.ps1 -Action Key -Keys n > "$hostDir/recovery-T1-n.log"
$inputOK=$?
if(-not $inputOK){throw 'Recovery input failed/ambiguous; no retry'}
Start-Sleep -Milliseconds 800
$after=ReadOwn 'T1-focus-recovery' 1
Copy-Item "$package/variant/T1-focus-recovery.json" "$package/variant/T1.json"
@{turn=1;one_n=$true;native_all_round_plus_one=$true;polls=1;recovery_after_proven_no_input=$true;failed_token_preserved=$true;recovery_token=$tokenPath;at=(Get-Date).ToString('o')}|ConvertTo-Json|Set-Content "$package/variant/T1-pass.json" -Encoding utf8
Write-Output 'RECOVERY_T1_ACCEPTED: all seven rounds0; original failed token preserved; one recovery n proved'
