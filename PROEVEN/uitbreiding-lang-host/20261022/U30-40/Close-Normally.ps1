$ErrorActionPreference='Stop'
Set-Location -LiteralPath 'C:/GIT/ctp'
$armDir=$PSScriptRoot
if(Test-Path "$armDir/close.json"){throw 'Close already attempted; inspect existing record'}
$start=Get-Content "$armDir/start.json" -Raw|ConvertFrom-Json
$probe=Get-Process -Id $start.pid
$creation=([DateTimeOffset]$probe.StartTime.ToUniversalTime()).ToUnixTimeMilliseconds()
if($probe.Path -cne 'C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe' -or $creation -ne $start.creation_utc_ms){throw 'Instance changed'}
@{state='ONE_NORMAL_CLOSE_REQUEST_PENDING';pid=$start.pid;at_utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$armDir/close.json"
$requested=$probe.CloseMainWindow()
$exited=$probe.WaitForExit(10000)
@{close_requested=$requested;exited=$exited;all_civctp_count=@(Get-Process civctp -ErrorAction SilentlyContinue).Count;at_utc=[DateTime]::UtcNow.ToString('o');elapsed_seconds=([DateTime]::UtcNow-([DateTime]::Parse($start.start_utc)).ToUniversalTime()).TotalSeconds;n_consumed=$start.n_consumed}|ConvertTo-Json|Set-Content "$armDir/close.json"
if(-not $exited){throw 'Normal close did not exit; no force kill or DLL restore'}
