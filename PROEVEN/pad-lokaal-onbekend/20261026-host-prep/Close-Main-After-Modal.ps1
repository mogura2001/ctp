# The previous normal close dismissed the owned CD-ROM modal, not the app.
$ErrorActionPreference='Stop'
$workspace='C:\GIT\ctp';Set-Location -LiteralPath $workspace
$hostDir=Join-Path $workspace 'PROEVEN/pad-lokaal-onbekend/20261026-host/host'
function NewJson($path,$value){$stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None);try{$bytes=[Text.Encoding]::UTF8.GetBytes(($value|ConvertTo-Json -Depth 10));$stream.Write($bytes,0,$bytes.Length);$stream.Flush()}finally{$stream.Dispose()}}
$start=Get-Content (Join-Path $hostDir 'start.json') -Raw|ConvertFrom-Json
$binding=Get-Content (Join-Path $hostDir 'start-binding.json') -Raw|ConvertFrom-Json
$previous=Get-Content (Join-Path $hostDir 'close.json') -Raw|ConvertFrom-Json
if((Get-FileHash (Join-Path $hostDir 'start.json')).Hash.ToLowerInvariant() -cne $binding.start_sha256 -or $previous.operation -cne 'normal_close_observed_own_CDROM_modal' -or $previous.observed_owned_modal -ne 526300 -or $previous.exited -ne $false){throw 'Exact previous modal-dismissal evidence required'}
if((Test-Path (Join-Path $hostDir 'MAIN-CLOSE-ATTEMPT.json')) -or (Test-Path (Join-Path $hostDir 'MAIN-CLOSE-RESULT.json'))){throw 'Main application close already attempted'}
$rows=@(Get-Process civctp -ErrorAction SilentlyContinue)
if($rows.Count -ne 1 -or $rows[0].Id -ne 28916){throw 'Exact one own process required'}
$probe=$rows[0]
if($probe.Path -cne $start.path -or $probe.StartTime.ToUniversalTime().ToFileTimeUtc() -ne $start.creation_filetime -or $probe.MainWindowHandle.ToInt64() -ne $start.window -or $probe.MainWindowTitle -cne 'CivCTP'){throw 'Original own main window required after modal dismissal'}
NewJson (Join-Path $hostDir 'MAIN-CLOSE-ATTEMPT.json') @{pid=$start.pid;creation_filetime=$start.creation_filetime;window=$start.window;operation='normal_close_original_app_after_CDROM_modal_dismissal';start_sha256=$binding.start_sha256;at_utc=[DateTime]::UtcNow.ToString('o')}
$requested=$probe.CloseMainWindow();$exited=$probe.WaitForExit(10000)
$count=@(Get-Process civctp -ErrorAction SilentlyContinue).Count
NewJson (Join-Path $hostDir 'MAIN-CLOSE-RESULT.json') @{close_requested=$requested;exited=$exited;all_civctp_count=$count;pid=$start.pid;creation_filetime=$start.creation_filetime;start_sha256=$binding.start_sha256;operation='normal_close_original_app_after_CDROM_modal_dismissal';elapsed_seconds=([DateTime]::UtcNow-[DateTime]::Parse($start.start_utc).ToUniversalTime()).TotalSeconds;at_utc=[DateTime]::UtcNow.ToString('o')}
if(-not $exited -or $count -ne 0){throw 'Main normal close not confirmed; no force kill or restore'}
