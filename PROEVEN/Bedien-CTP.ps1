param(
    [ValidateSet('Start','Restart','Status','Capture','Key','Click','Drag','DismissError')][string]$Action = 'Status',
    [string]$Keys,
    [int]$X,
    [int]$Y,
    [int]$ToX,
    [int]$ToY,
    [Nullable[int]]$FromX,
    [Nullable[int]]$FromY,
    [switch]$ResetCursor,
    [switch]$CaptureWaitForForeground,
    [ValidateRange(1,30000)][int]$CaptureWaitTimeoutMs = 30000,
    [int]$ExpectedProcessId,
    [long]$ExpectedCreationUtcMs,
    [long]$ExpectedWindowHandle
)
$ErrorActionPreference = 'Stop'
$captureParameterNames = @('CaptureWaitForForeground','CaptureWaitTimeoutMs','ExpectedProcessId','ExpectedCreationUtcMs','ExpectedWindowHandle')
$boundCaptureParameters = @($captureParameterNames | Where-Object { $PSBoundParameters.ContainsKey($_) })
if ($boundCaptureParameters.Count -gt 0) {
    if ($Action -ne 'Capture') { throw 'Capture wait parameters require Action Capture.' }
    if (-not $CaptureWaitForForeground) { throw 'Capture binding/timeout parameters require CaptureWaitForForeground.' }
    foreach ($bindingName in @('ExpectedProcessId','ExpectedCreationUtcMs','ExpectedWindowHandle')) {
        if (-not $PSBoundParameters.ContainsKey($bindingName)) { throw "Capture wait requires $bindingName." }
    }
    if ($ExpectedProcessId -le 0 -or $ExpectedWindowHandle -eq 0) { throw 'Capture wait requires a positive PID and nonzero window handle.' }
}
$probeRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../CTP-proef'))
$exePath = Join-Path $probeRoot 'ctp_program/ctp/civctp.exe'
$outputRoot = Join-Path $PSScriptRoot 'automatisering'
[IO.Directory]::CreateDirectory($outputRoot) | Out-Null
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class CtpWindow {
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
    public delegate bool WindowCallback(IntPtr h, IntPtr p);
    [DllImport("user32.dll")] public static extern bool EnumWindows(WindowCallback cb, IntPtr p);
    [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr h, WindowCallback cb, IntPtr p);
    [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint message, IntPtr wparam, IntPtr lparam);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, System.Text.StringBuilder text, int max);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
    [StructLayout(LayoutKind.Sequential)] public struct Rect { public int Left, Top, Right, Bottom; }
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out Rect r);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint flags, int x, int y, uint data, UIntPtr extra);
}
'@
[CtpWindow]::SetProcessDPIAware() | Out-Null
if ($Action -eq 'Restart') {
    $runningProbes = @(Get-Process civctp -ErrorAction SilentlyContinue | Where-Object { $_.Path -eq $exePath })
    foreach ($runningProbe in $runningProbes) {
        $runningProbe.Kill()
        $runningProbe.WaitForExit(5000) | Out-Null
    }
    $Action = 'Start'
}
if ($Action -eq 'Start') {
    $existing = @(Get-Process civctp -ErrorAction SilentlyContinue)
    if ($existing.Count -gt 0) { throw 'CTP is already running; inspect it before launching another instance.' }
    $newProcess = Start-Process -FilePath $exePath -WorkingDirectory (Split-Path $exePath) -WindowStyle Normal -PassThru
    Write-Output "Started probe installation, process $($newProcess.Id)."
    exit
}
try {
    $candidates = @(Get-Process civctp -ErrorAction SilentlyContinue | Where-Object { $_.Path -eq $exePath })
    if ($candidates.Count -ne 1) { throw 'Expected exactly one running civctp from CTP-proef.' }
    $gameProcess = $candidates[0]
    $gameProcess.Refresh()
    $windowHandle = $gameProcess.MainWindowHandle
} catch {
    if ($CaptureWaitForForeground) {
        Write-Output ('CaptureForegroundTrace ' + ([ordered]@{expected_pid=$ExpectedProcessId;expected_creation_utc_ms=$ExpectedCreationUtcMs;expected_window_handle=$ExpectedWindowHandle;checked_at_utc=[DateTime]::UtcNow.ToString('o');result='REJECTED';error=$_.Exception.Message} | ConvertTo-Json -Compress))
    }
    throw
}
if ($Action -eq 'DismissError') {
    [CtpWindow]::EnumWindows({ param($h,$p)
        $ownerPid = [uint32]0
        [CtpWindow]::GetWindowThreadProcessId($h, [ref]$ownerPid) | Out-Null
        $windowText = New-Object Text.StringBuilder 1024
        [CtpWindow]::GetWindowText($h,$windowText,1024) | Out-Null
        if ($ownerPid -eq $gameProcess.Id -and $windowText.ToString() -eq 'Slic Error') {
            [CtpWindow]::PostMessage($h, 0x111, [IntPtr]1, [IntPtr]::Zero) | Out-Null
            Write-Host 'Dismissed the probe SLIC error dialog.'
        }
        return $true
    }, [IntPtr]::Zero) | Out-Null
    exit
}
if ($Action -eq 'Status') {
    $gameProcess | Select-Object Id,Path,MainWindowHandle,MainWindowTitle,Responding | Format-List
    [CtpWindow]::EnumWindows({ param($h,$p)
        $ownerPid = [uint32]0
        [CtpWindow]::GetWindowThreadProcessId($h, [ref]$ownerPid) | Out-Null
        if ($ownerPid -eq $gameProcess.Id) {
            $windowText = New-Object Text.StringBuilder 1024
            [CtpWindow]::GetWindowText($h,$windowText,1024) | Out-Null
            Write-Host "Window $h visible=$([CtpWindow]::IsWindowVisible($h)) title=$windowText"
            if ($windowText.ToString() -eq 'Slic Error') {
                [CtpWindow]::EnumChildWindows($h, { param($child,$extra)
                    $childText = New-Object Text.StringBuilder 4096
                    [CtpWindow]::GetWindowText($child,$childText,4096) | Out-Null
                    Write-Host "Dialog text: $childText"
                    return $true
                }, [IntPtr]::Zero) | Out-Null
            }
        }
        return $true
    }, [IntPtr]::Zero) | Out-Null
    exit
}
if ($CaptureWaitForForeground) {
    $waitClock = [Diagnostics.Stopwatch]::StartNew()
    $waitBeginUtc = [DateTime]::UtcNow
    $captureTrace = [ordered]@{
        expected_pid=$ExpectedProcessId; expected_creation_utc_ms=$ExpectedCreationUtcMs
        expected_exe=$exePath; expected_window_handle=$ExpectedWindowHandle
        wait_begin_utc=$waitBeginUtc.ToString('o'); deadline_utc=$waitBeginUtc.AddMilliseconds($CaptureWaitTimeoutMs).ToString('o')
        timeout_ms=$CaptureWaitTimeoutMs; samples=[Collections.Generic.List[object]]::new()
        bounds=$null; result='REJECTED'; error=$null
    }
    $checkCaptureDeadline = {
        if ($waitClock.Elapsed.TotalMilliseconds -ge $CaptureWaitTimeoutMs) { throw 'Capture foreground deadline exceeded.' }
    }
    $readCaptureBinding = {
        param([string]$Stage)
        & $checkCaptureDeadline
        $sample = [ordered]@{stage=$Stage;at_utc=[DateTime]::UtcNow.ToString('o');elapsed_ms=$waitClock.Elapsed.TotalMilliseconds}
        $captureTrace.samples.Add($sample)
        $metadata = @(Get-CimInstance Win32_Process -Filter "ProcessId=$ExpectedProcessId" -ErrorAction Stop)
        if ($metadata.Count -ne 1) { throw 'Original capture PID is absent or ambiguous.' }
        $creationMs = ([DateTimeOffset]$metadata[0].CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds()
        $sample.pid = [int]$metadata[0].ProcessId
        $sample.creation_utc_ms = $creationMs
        $sample.exe = $metadata[0].ExecutablePath
        if ($sample.pid -ne $ExpectedProcessId -or $creationMs -ne $ExpectedCreationUtcMs -or $sample.exe -cne $exePath) { throw 'Original capture process identity changed.' }
        $gameProcess.Refresh()
        $sample.process_object_pid = $gameProcess.Id
        $sample.process_object_exe = $gameProcess.Path
        $sample.window_handle = $gameProcess.MainWindowHandle.ToInt64()
        if ($gameProcess.Id -ne $ExpectedProcessId -or $sample.process_object_exe -cne $exePath -or $sample.window_handle -eq 0 -or $sample.window_handle -ne $ExpectedWindowHandle) { throw 'Original capture main-window binding changed.' }
        $ownerPid = [uint32]0
        $ownerThread = [CtpWindow]::GetWindowThreadProcessId($gameProcess.MainWindowHandle, [ref]$ownerPid)
        $sample.owner_matches = ($ownerThread -ne 0 -and $ownerPid -eq $ExpectedProcessId)
        if (-not $sample.owner_matches) { throw 'Original capture window owner changed or is unreadable.' }
        $sample.foreground_handle = [CtpWindow]::GetForegroundWindow().ToInt64()
        $sample.completed_at_utc = [DateTime]::UtcNow.ToString('o')
        $sample.completed_elapsed_ms = $waitClock.Elapsed.TotalMilliseconds
        & $checkCaptureDeadline
        return $sample.foreground_handle
    }
    try {
        if ($gameProcess.Id -ne $ExpectedProcessId -or $windowHandle.ToInt64() -ne $ExpectedWindowHandle) { throw 'Selected probe is not the original capture binding.' }
        while ((& $readCaptureBinding 'poll') -ne $ExpectedWindowHandle) {
            $remainingMs = [Math]::Floor($CaptureWaitTimeoutMs - $waitClock.Elapsed.TotalMilliseconds)
            if ($remainingMs -lt 1) { throw 'Capture foreground deadline exceeded.' }
            Start-Sleep -Milliseconds ([int][Math]::Min(100, $remainingMs))
        }
        if (($CaptureWaitTimeoutMs - $waitClock.Elapsed.TotalMilliseconds) -lt 350) { throw 'Capture deadline leaves insufficient time for 350ms foreground settling.' }
        $captureTrace.settle_begin_elapsed_ms = $waitClock.Elapsed.TotalMilliseconds
        Start-Sleep -Milliseconds 350
        if ((& $readCaptureBinding 'after-350ms') -ne $ExpectedWindowHandle) { throw 'Original capture window lost foreground during settling.' }
        $bounds = New-Object CtpWindow+Rect
        if (-not [CtpWindow]::GetWindowRect($windowHandle, [ref]$bounds)) { throw 'Cannot read original capture window bounds.' }
        $width = $bounds.Right - $bounds.Left
        $height = $bounds.Bottom - $bounds.Top
        $captureTrace.bounds = [ordered]@{left=$bounds.Left;top=$bounds.Top;right=$bounds.Right;bottom=$bounds.Bottom;width=$width;height=$height;at_utc=[DateTime]::UtcNow.ToString('o');elapsed_ms=$waitClock.Elapsed.TotalMilliseconds}
        & $checkCaptureDeadline
        if ($width -le 0 -or $height -le 0) { throw 'Invalid original capture window size.' }
        $bitmap = New-Object Drawing.Bitmap($width, $height)
        $graphics = $null
        try {
            $graphics = [Drawing.Graphics]::FromImage($bitmap)
            if ((& $readCaptureBinding 'before-copy') -ne $ExpectedWindowHandle) { throw 'Original capture window is not foreground before copy.' }
            $graphics.CopyFromScreen($bounds.Left, $bounds.Top, 0, 0, $bitmap.Size)
            $captureTrace.after_copy_foreground = [ordered]@{handle=[CtpWindow]::GetForegroundWindow().ToInt64();at_utc=[DateTime]::UtcNow.ToString('o');elapsed_ms=$waitClock.Elapsed.TotalMilliseconds}
            if ($captureTrace.after_copy_foreground.handle -ne $ExpectedWindowHandle) { throw 'Original capture window lost foreground during copy; capture rejected.' }
            if ((& $readCaptureBinding 'after-copy') -ne $ExpectedWindowHandle) { throw 'Original capture window lost foreground during copy; capture rejected.' }
            & $checkCaptureDeadline
            $capturePath = Join-Path $outputRoot 'ctp-window.png'
            $bitmap.Save($capturePath, [Drawing.Imaging.ImageFormat]::Png)
            & $checkCaptureDeadline
            $captureTrace.result = 'CAPTURE_SAVED_REQUIRES_IMAGE_REVIEW'
            $captureTrace.capture_path = $capturePath
            Write-Output $capturePath
        } finally {
            if ($null -ne $graphics) { $graphics.Dispose() }
            $bitmap.Dispose()
        }
    } catch {
        $captureTrace.error = $_.Exception.Message
        throw
    } finally {
        $captureTrace.finished_at_utc = [DateTime]::UtcNow.ToString('o')
        $captureTrace.elapsed_ms = $waitClock.Elapsed.TotalMilliseconds
        $waitClock.Stop()
        Write-Output ('CaptureForegroundTrace ' + ($captureTrace | ConvertTo-Json -Depth 8 -Compress))
    }
    exit
}
if ($windowHandle -eq [IntPtr]::Zero) { throw 'The probe process has no main window.' }
if ([CtpWindow]::GetForegroundWindow() -ne $windowHandle) {
    if (-not [CtpWindow]::SetForegroundWindow($windowHandle)) { throw 'Unable to foreground the game window.' }
}
Start-Sleep -Milliseconds 350
if ([CtpWindow]::GetForegroundWindow() -ne $windowHandle) { throw 'Game is not foreground; refusing input/capture.' }
$bounds = New-Object CtpWindow+Rect
if (-not [CtpWindow]::GetWindowRect($windowHandle, [ref]$bounds)) { throw 'Cannot read game window bounds.' }
if ($Action -eq 'Capture') {
    $width = $bounds.Right - $bounds.Left
    $height = $bounds.Bottom - $bounds.Top
    if ($width -le 0 -or $height -le 0) { throw 'Invalid window size.' }
    $bitmap = New-Object Drawing.Bitmap($width, $height)
    $graphics = [Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.CopyFromScreen($bounds.Left, $bounds.Top, 0, 0, $bitmap.Size)
        $capturePath = Join-Path $outputRoot 'ctp-window.png'
        $bitmap.Save($capturePath, [Drawing.Imaging.ImageFormat]::Png)
        Write-Output $capturePath
    } finally { $graphics.Dispose(); $bitmap.Dispose() }
} elseif ($Action -eq 'Key') {
    if (-not $Keys) { throw 'Keys is required.' }
    [Windows.Forms.SendKeys]::SendWait($Keys)
    Write-Output "Sent keys to probe game: $Keys"
} elseif ($Action -in @('Click','Drag')) {
    if ($X -lt 0 -or $Y -lt 0 -or $X -ge ($bounds.Right-$bounds.Left) -or $Y -ge ($bounds.Bottom-$bounds.Top)) { throw 'Click outside window.' }
    if ($Action -eq 'Drag' -and ($ToX -lt 0 -or $ToY -lt 0 -or $ToX -ge ($bounds.Right-$bounds.Left) -or $ToY -ge ($bounds.Bottom-$bounds.Top))) { throw 'Drag destination outside window.' }
    $cursorPosition = [Windows.Forms.Cursor]::Position
    if ($ResetCursor) {
        # Clamp the internal cursor to the top-left before targeting a control.
        $resetSteps = [int]([Math]::Ceiling([Math]::Max(($bounds.Right-$bounds.Left), ($bounds.Bottom-$bounds.Top)) / 5.0) + 20)
        for ($resetIndex = 0; $resetIndex -lt $resetSteps; $resetIndex++) {
            [CtpWindow]::mouse_event(1, -5, -5, 0, [UIntPtr]::Zero)
            Start-Sleep -Milliseconds 10
        }
        $FromX = 0
        $FromY = 0
    }
    # DirectInput can keep its own cursor independent of the Windows cursor.
    if ($null -ne $FromX -and $null -ne $FromY) {
        $cursorPosition = [Drawing.Point]::new(($bounds.Left + $FromX), ($bounds.Top + $FromY))
    }
    $moveX = $bounds.Left + $X - $cursorPosition.X
    $moveY = $bounds.Top + $Y - $cursorPosition.Y
    # Small movements avoid Windows acceleration on large relative jumps.
    while ($moveX -ne 0 -or $moveY -ne 0) {
        $stepX = [Math]::Max(-5, [Math]::Min(5, $moveX))
        $stepY = [Math]::Max(-5, [Math]::Min(5, $moveY))
        [CtpWindow]::mouse_event(1, $stepX, $stepY, 0, [UIntPtr]::Zero)
        $moveX -= $stepX
        $moveY -= $stepY
        Start-Sleep -Milliseconds 10
    }
    Start-Sleep -Milliseconds 150
    [CtpWindow]::mouse_event(2, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 150
    if ($Action -eq 'Drag') {
        try {
            $moveX = $ToX - $X
            $moveY = $ToY - $Y
            while ($moveX -ne 0 -or $moveY -ne 0) {
                $stepX = [Math]::Max(-5, [Math]::Min(5, $moveX))
                $stepY = [Math]::Max(-5, [Math]::Min(5, $moveY))
                [CtpWindow]::mouse_event(1, $stepX, $stepY, 0, [UIntPtr]::Zero)
                $moveX -= $stepX
                $moveY -= $stepY
                Start-Sleep -Milliseconds 10
            }
        } finally { [CtpWindow]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero) }
    }
    [CtpWindow]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 500
    if ($Action -eq 'Drag') { Write-Output "Dragged probe window from $X,$Y to $ToX,$ToY." }
    else { Write-Output "Clicked probe window at $X,$Y." }
}
