param([ValidateSet('Gui','Read','Pass')][string]$Purpose='Gui')
$ErrorActionPreference='Stop'
$armDir=$PSScriptRoot
$started=Get-Content -LiteralPath (Join-Path $armDir 'start-record.json') -Raw -Encoding utf8|ConvertFrom-Json
$final=Get-Content -LiteralPath (Join-Path $armDir 'final-window-binding.json') -Raw -Encoding utf8|ConvertFrom-Json
$elapsed=([Diagnostics.Stopwatch]::GetTimestamp()-[long]$started.start_monotonic_ticks)*1000.0/[long]$started.monotonic_frequency
if($elapsed -ge 470000){throw 'No10s afwikkelreserve within480s; no further GUI/read/pass.'}
$python='C:\Users\Stephan\AppData\Local\Programs\Python\Python312\python.exe'
$budget=& $python 'C:\GIT\ctp\PROEVEN\Controleer-Weekbudget.py' --thread 01a0f7b4-4751-7513-b510-3835ce43f47d
$budgetCode=$LASTEXITCODE
if($budgetCode -eq 2){$budget=& $python 'C:\GIT\ctp\PROEVEN\Controleer-Weekbudget.py' --thread 01a0f7b4-4751-7513-b510-3835ce43f47d;$budgetCode=$LASTEXITCODE}
if($budgetCode -ne 0 -and $budgetCode -ne 25){throw 'Budget stop/unknown; checkpoint, no further action.'}
Add-Type @'
using System;using System.Runtime.InteropServices;
public class H1T0GuardWindow {
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h,out uint pid);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
}
'@
$rows=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
if($rows.Count -ne 1 -or $rows[0].ProcessId -ne $started.pid -or $rows[0].ExecutablePath -cne 'C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe' -or ([DateTimeOffset]$rows[0].CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $started.creation_utc_ms){throw 'Original process identity changed/absent or extra civctp.'}
$own=[Diagnostics.Process]::GetProcessById([int]$started.pid)
try{
    $own.Refresh();$owner=[uint32]0
    $processPath=$own.MainModule.FileName
    $processCreationMs=([DateTimeOffset]$own.StartTime.ToUniversalTime()).ToUnixTimeMilliseconds()
    if($started.exe -cne 'C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe' -or $processPath -cne $started.exe -or $processCreationMs -ne $started.creation_utc_ms){throw 'Retained Process path/start differs from original start-record; no further action.'}
    if($own.MainWindowHandle.ToInt64() -ne $final.sample.handle -or [H1T0GuardWindow]::GetWindowThreadProcessId($own.MainWindowHandle,[ref]$owner) -eq 0 -or $owner -ne $started.pid -or [H1T0GuardWindow]::GetForegroundWindow() -ne $own.MainWindowHandle){throw 'Original HWND/owner/foreground guard failed.'}
    $elapsed=([Diagnostics.Stopwatch]::GetTimestamp()-[long]$started.start_monotonic_ticks)*1000.0/[long]$started.monotonic_frequency
    if($elapsed -ge 470000){throw 'Late guard result; no further action.'}
    [ordered]@{purpose=$Purpose;checked_at=(Get-Date).ToString('o');pid=$started.pid;creation_utc_ms=$started.creation_utc_ms;handle=$final.sample.handle;elapsed_ms=$elapsed;remaining_ms=480000-$elapsed;foreground_verified=$true;budget=($budget|ConvertFrom-Json)}|ConvertTo-Json -Depth 6
}finally{$own.Dispose()}
