# Recovery of the observed owned CD-ROM modal only; no input or force kill.
$ErrorActionPreference='Stop'
$workspace='C:\GIT\ctp'
Set-Location -LiteralPath $workspace
$hostDir=Join-Path $workspace 'PROEVEN/pad-lokaal-onbekend/20261026-host/host'
function NewJson($path,$value){$stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None);try{$bytes=[Text.Encoding]::UTF8.GetBytes(($value|ConvertTo-Json -Depth 10));$stream.Write($bytes,0,$bytes.Length);$stream.Flush()}finally{$stream.Dispose()}}
$start=Get-Content (Join-Path $hostDir 'start.json') -Raw|ConvertFrom-Json
$binding=Get-Content (Join-Path $hostDir 'start-binding.json') -Raw|ConvertFrom-Json
if((Get-FileHash (Join-Path $hostDir 'start.json')).Hash.ToLowerInvariant() -cne $binding.start_sha256){throw 'Immutable start changed'}
$rows=@(Get-Process civctp -ErrorAction SilentlyContinue)
if($rows.Count -ne 1 -or $rows[0].Id -ne 28916){throw 'Exact one owned process required'}
$probe=$rows[0]
if($probe.Path -cne 'C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe' -or $probe.StartTime.ToUniversalTime().ToFileTimeUtc() -ne 134375007599474449 -or $probe.MainWindowHandle.ToInt64() -ne 526300 -or $probe.MainWindowTitle -cne 'CD-ROM'){throw 'Observed owned modal identity changed'}
if((Test-Path (Join-Path $hostDir 'close-attempt.json')) -or (Test-Path (Join-Path $hostDir 'close.json'))){throw 'No second close attempt'}
& (Join-Path $workspace 'PROEVEN/Bedien-CTP.ps1') -Action Status > (Join-Path $hostDir 'cdrom-status.txt')
$dialog=[Collections.Generic.List[string]]::new()
[CtpWindow]::EnumChildWindows([IntPtr]526300,{param($child,$extra) $text=New-Object Text.StringBuilder 4096;[CtpWindow]::GetWindowText($child,$text,4096)|Out-Null;$dialog.Add($text.ToString());return $true},[IntPtr]::Zero)|Out-Null
NewJson (Join-Path $hostDir 'CDROM-INCIDENT.json') @{at_utc=[DateTime]::UtcNow.ToString('o');pid=$probe.Id;creation_filetime=$start.creation_filetime;original_window=$start.window;observed_owned_modal=526300;modal_title='CD-ROM';dialog_text=@($dialog);original_capture_rejected=$true;modal_foreground_capture_rejected=$true;accepted_T0=$false;n_sent=0;no_retry=$true;normal_close_only=$true;start_sha256=$binding.start_sha256}
NewJson (Join-Path $hostDir 'close-attempt.json') @{state='ONE_NORMAL_CLOSE_REQUEST_PENDING';pid=$probe.Id;creation_filetime=$start.creation_filetime;owned_modal=526300;operation='normal_close_observed_own_CDROM_modal';start_sha256=$binding.start_sha256;at_utc=[DateTime]::UtcNow.ToString('o')}
$requested=$probe.CloseMainWindow()
$exited=$probe.WaitForExit(10000)
$count=@(Get-Process civctp -ErrorAction SilentlyContinue).Count
NewJson (Join-Path $hostDir 'close.json') @{close_requested=$requested;exited=$exited;all_civctp_count=$count;pid=$start.pid;creation_filetime=$start.creation_filetime;start_sha256=$binding.start_sha256;operation='normal_close_observed_own_CDROM_modal';original_window=$start.window;observed_owned_modal=526300;elapsed_seconds=([DateTime]::UtcNow-[DateTime]::Parse($start.start_utc).ToUniversalTime()).TotalSeconds;at_utc=[DateTime]::UtcNow.ToString('o')}
if(-not $exited -or $count -ne 0){throw 'Normal close did not exit; no force kill or restore'}
