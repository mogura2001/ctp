param(
    [ValidateSet('Start','Restart','Status','Capture','Key','Click','DismissError')][string]$Action = 'Status',
    [string]$Keys,
    [int]$X,
    [int]$Y,
    [Nullable[int]]$FromX,
    [Nullable[int]]$FromY
)
$ErrorActionPreference = 'Stop'
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
$candidates = @(Get-Process civctp -ErrorAction SilentlyContinue | Where-Object { $_.Path -eq $exePath })
if ($candidates.Count -ne 1) { throw 'Expected exactly one running civctp from CTP-proef.' }
$gameProcess = $candidates[0]
$gameProcess.Refresh()
$windowHandle = $gameProcess.MainWindowHandle
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
} elseif ($Action -eq 'Click') {
    if ($X -lt 0 -or $Y -lt 0 -or $X -ge ($bounds.Right-$bounds.Left) -or $Y -ge ($bounds.Bottom-$bounds.Top)) { throw 'Click outside window.' }
    $cursorPosition = [Windows.Forms.Cursor]::Position
    # DirectInput can keep its own cursor independent of the Windows cursor.
    if ($null -ne $FromX -and $null -ne $FromY) {
        $cursorPosition = [Drawing.Point]::new(($bounds.Left + $FromX), ($bounds.Top + $FromY))
    }
    [CtpWindow]::mouse_event(1, $bounds.Left + $X - $cursorPosition.X, $bounds.Top + $Y - $cursorPosition.Y, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 150
    [CtpWindow]::mouse_event(2, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 150
    [CtpWindow]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 500
    Write-Output "Clicked probe window at $X,$Y."
}
