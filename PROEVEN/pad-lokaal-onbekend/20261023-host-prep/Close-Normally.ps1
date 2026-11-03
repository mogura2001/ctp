$ErrorActionPreference='Stop'
$workspace='C:\GIT\ctp';Set-Location -LiteralPath $workspace
$package=$PSScriptRoot;$hostDir=Join-Path $workspace 'PROEVEN/pad-lokaal-onbekend/20261023-host/host'
function Hash($p){(Get-FileHash -LiteralPath $p).Hash.ToLowerInvariant()}
function NewJson($p,$value){$s=[IO.File]::Open($p,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None);try{$b=[Text.Encoding]::UTF8.GetBytes(($value|ConvertTo-Json -Depth 20));$s.Write($b,0,$b.Length);$s.Flush()}finally{$s.Dispose()}}
$gate=Get-Content (Join-Path $package 'ROOT-HOST.json') -Raw|ConvertFrom-Json
if($gate.close_allowed -ne $true -or $gate.arm -cne 'local4' -or $gate.run_id -cne 'pad-local4-20261023-host' -or (Hash (Join-Path $package 'SOURCE-PINS.json')) -cne $gate.source_pins_sha256){throw 'Exact C5 close gate required'}
foreach($p in (Get-Content (Join-Path $package 'SOURCE-PINS.json') -Raw|ConvertFrom-Json).sources){if((Hash (Join-Path $workspace $p.path)) -cne $p.sha256){throw 'Close source changed'}}
$binding=Get-Content (Join-Path $hostDir 'start-binding.json') -Raw|ConvertFrom-Json
if((Hash (Join-Path $hostDir 'start.json')) -cne $binding.start_sha256 -or (Hash (Join-Path $hostDir 'window.json')) -cne $binding.window_sha256){throw 'Immutable own start/window changed'}
$start=Get-Content (Join-Path $hostDir 'start.json') -Raw|ConvertFrom-Json
if($start.run_id -cne $gate.run_id -or $start.n_consumed -ne 0 -or $start.max_n -ne 100){throw 'Wrong own immutable start'}
if((Test-Path -LiteralPath (Join-Path $hostDir 'close-attempt.json')) -or (Test-Path -LiteralPath (Join-Path $hostDir 'close.json'))){throw 'Close already attempted; no retry'}
$rows=@(Get-Process civctp -ErrorAction SilentlyContinue)
if($rows.Count -ne 1 -or $rows[0].Id -ne $start.pid){throw 'Exact unique own process required'}
$probe=$rows[0]
if($probe.Path -cne (Join-Path $workspace 'CTP-proef/ctp_program/ctp/civctp.exe') -or $probe.StartTime.ToUniversalTime().ToFileTimeUtc() -ne $start.creation_filetime -or $probe.MainWindowHandle.ToInt64() -ne $start.window){throw 'Instance/window changed'}
NewJson (Join-Path $hostDir 'close-attempt.json') @{state='ONE_NORMAL_CLOSE_REQUEST_PENDING';pid=$start.pid;creation_filetime=$start.creation_filetime;start_sha256=$binding.start_sha256;at_utc=[DateTime]::UtcNow.ToString('o')}
$requested=$probe.CloseMainWindow();$exited=$probe.WaitForExit(10000)
$count=@(Get-Process civctp -ErrorAction SilentlyContinue).Count
NewJson (Join-Path $hostDir 'close.json') @{close_requested=$requested;exited=$exited;all_civctp_count=$count;pid=$start.pid;creation_filetime=$start.creation_filetime;start_sha256=$binding.start_sha256;elapsed_seconds=([DateTime]::UtcNow-[DateTime]::Parse($start.start_utc).ToUniversalTime()).TotalSeconds;at_utc=[DateTime]::UtcNow.ToString('o')}
if(-not $exited -or $count -ne 0){throw 'Normal close not confirmed/count not zero; no forcekill or restore'}
