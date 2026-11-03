$ErrorActionPreference='Stop'
$workspace='C:/GIT/ctp'
Set-Location -LiteralPath $workspace
$armDir=$PSScriptRoot
$python='C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe'
$budgetText=& $python PROEVEN/Controleer-Weekbudget.py --thread 01a0f7b4-4751-7513-b510-3835ce43f47d
if(($budgetText|ConvertFrom-Json).state -notin @('ok','warn')){throw 'Budget unavailable or stop'}
$budgetText|Set-Content "$armDir/budget-before-start.json"
if(@(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0){throw 'Game already running'}
if(@(Get-CimInstance Win32_LogicalDisk|Where-Object {$_.DriveType -eq 5 -and $_.VolumeName -eq 'CCTP'}).Count -ne 1){throw 'CD unavailable'}
$gate=Get-Content "$armDir/gate.json" -Raw|ConvertFrom-Json
if(-not $gate.allowed -or $gate.arm -ne 'host2' -or $gate.max_n -ne 26){throw 'Wrong host gate'}
foreach($pin in $gate.sources){if((Get-FileHash -LiteralPath (Join-Path $workspace $pin.path)).Hash.ToLower() -ne $pin.sha256){throw "Changed source $($pin.path)"}}
$before=Get-Content "$armDir/before.json" -Raw|ConvertFrom-Json
foreach($file in @($before.protected)+@($before.extra_preserved_files)){if((Get-FileHash -LiteralPath $file.path).Hash.ToLower() -ne $file.sha256){throw "Changed $($file.path)"}}
$alias='CTP-proef/ctp_program/ctp/save/games/Julius/000-U30-40-START-T0'
if(Test-Path -LiteralPath $alias){throw 'Alias exists'}
$candidate=Join-Path $workspace $gate.candidate_path
$candidateHash=(Get-FileHash -LiteralPath $candidate).Hash.ToLower()
if($candidateHash -ne $gate.candidate_sha256){throw 'Wrong candidate'}
Copy-Item -LiteralPath CTP-proef/ctp_program/ctp/save/games/Julius/QUOTA-START-T0 -Destination $alias
Copy-Item -LiteralPath $candidate -Destination CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll
@{alias_created=$true;installed_sha256=$candidateHash;at_utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$armDir/install.json"
& ./PROEVEN/Bedien-CTP.ps1 -Action Start
if(-not $?){throw 'Start failed'}
$probeProcess=Get-Process civctp
$startedUtc=$probeProcess.StartTime.ToUniversalTime()
$creationMs=([DateTimeOffset]$startedUtc).ToUnixTimeMilliseconds()
$probePid=$probeProcess.Id
$exe=$probeProcess.Path
if($exe -cne 'C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe'){throw 'Wrong executable'}
@{pid=$probePid;creation_utc_ms=$creationMs;path=$exe;start_utc=$startedUtc.ToString('o');max_n=26;n_consumed=0}|ConvertTo-Json|Set-Content "$armDir/start.json"
while($probeProcess.MainWindowHandle -eq 0){
 if(([DateTime]::UtcNow-$startedUtc).TotalSeconds -ge 15){throw 'No initial window'}
 Start-Sleep -Milliseconds 250
 $probeProcess.Refresh()
}
$window=[long]$probeProcess.MainWindowHandle
@{pid=$probePid;creation_utc_ms=$creationMs;path=$exe;start_utc=$startedUtc.ToString('o');max_n=26;n_consumed=0}|ConvertTo-Json|Set-Content "$armDir/start.json"
@{pid=$probePid;creation_utc_ms=$creationMs;window=$window}|ConvertTo-Json|Set-Content "$armDir/window.json"
Write-Output "INTRO_MONITOR_STARTED pid=$probePid creation=$creationMs window=$window"
foreach($target in @(45,90,135,180)){
 while(([DateTime]::UtcNow-$startedUtc).TotalSeconds -lt $target){
  $remaining=$target-([DateTime]::UtcNow-$startedUtc).TotalSeconds
  if($remaining -gt 0){Start-Sleep -Milliseconds ([int][Math]::Ceiling([Math]::Min(45,$remaining)*1000))}
 }
 $current=Get-Process -Id $probePid
 if($current.Path -cne $exe -or ([DateTimeOffset]$current.StartTime.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $creationMs){throw 'Instance changed'}
 $begin=[DateTime]::UtcNow
 if(($begin-$startedUtc).TotalSeconds -ge 195){throw 'No timely capture possible'}
 & ./PROEVEN/Bedien-CTP.ps1 -Action Capture -CaptureWaitForForeground -CaptureWaitTimeoutMs 3000 -ExpectedProcessId $probePid -ExpectedCreationUtcMs $creationMs -ExpectedWindowHandle $window > "$armDir/intro-$target.log"
 if(-not $?){throw 'Intro capture failed'}
 Copy-Item -LiteralPath PROEVEN/automatisering/ctp-window.png -Destination "$armDir/intro-$target.png"
 $end=[DateTime]::UtcNow
 $trace=[ordered]@{pid=$probePid;creation_utc_ms=$creationMs;window=$window;original_start_utc=$startedUtc.ToString('o');target_seconds=$target;capture_begin_utc=$begin.ToString('o');capture_end_utc=$end.ToString('o');actual_begin_seconds=($begin-$startedUtc).TotalSeconds;actual_end_seconds=($end-$startedUtc).TotalSeconds;no_automatic_menu_action=$true}
 $trace|ConvertTo-Json|Set-Content "$armDir/intro-$target.json"
 Write-Output ('INTRO_CAPTURE '+($trace|ConvertTo-Json -Compress))
 if(($end-$startedUtc).TotalSeconds -gt 195){throw 'Captured frame too late'}
}
@{terminal=$true;captures=4;no_menu_input=$true;at_utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$armDir/intro-monitor.json"
Write-Output 'INTRO_MONITOR_FINISHED; root must inspect frame before input'
