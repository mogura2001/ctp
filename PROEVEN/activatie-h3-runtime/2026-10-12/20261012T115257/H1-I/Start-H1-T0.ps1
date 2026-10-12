$ErrorActionPreference = 'Stop'
$outdir = $PSScriptRoot
$workspace = 'C:\GIT\ctp'
$exePath = Join-Path $workspace 'CTP-proef\ctp_program\ctp\civctp.exe'
$dllPath = Join-Path $workspace 'CTP-proef\ctp_program\ctp\dll\ai\robotcom.dll'
$candidatePath = Join-Path $workspace 'PROEVEN\score-h1\candidates\H1-I\robotcom.dll'
$toolPath = Join-Path $workspace 'PROEVEN\Bedien-CTP.ps1'
$profilePath = Join-Path $workspace 'CTP-proef\ctp_program\ctp\userprofile.txt'
$capturePath = Join-Path $workspace 'PROEVEN\automatisering\ctp-window.png'
$originalHash = '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
$candidateHash = '59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0'
$toolHash = 'd2dbbfcad3d9d8bec8e6a99a399d59561d8f9c4e9a48576a2aefc32e5997bc74'
$designHash = '21fcf7cadf2c459f99ed45047f612aba11fe98a0234d1d898c496d3e2f64ecec'
$originalProbe = Join-Path $workspace 'PROEVEN\hoststart-controle\2026-10-10\original-menu-focus-20261010T121931869'
$python = 'C:\Users\Stephan\AppData\Local\Programs\Python\Python312\python.exe'
$installed=$false;$budgetStopped=$false;$profileSaved=$false
$ownProcess=$null;$targetPid=$null;$creationMs=$null;$finalHandle=$null;$liveClock=$null
$summary=[ordered]@{began_at=(Get-Date).ToString('o');start_count=0;capture_count=0;close_call_count=0;outcome='PREPARATION_ONLY';error=$null;exit_confirmed=$false;has_exited=$null;exit_code=$null;restored=$false;image_review='NOT_PERFORMED_BY_BATCH';pid=$null;creation_utc_ms=$null;handle=$null}
$request=[ordered]@{attempted=$false;call_count=0;called_at=$null;bool_return=$null;exception=$null}
$closeChecks=[Collections.Generic.List[object]]::new()
if(Test-Path -LiteralPath (Join-Path $outdir 'execution.json')){throw 'Existing execution record; no second run.'}
[ordered]@{called_at=(Get-Date).ToString('o');execution_count=1}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $outdir 'execution.json') -Encoding utf8

# Prepare every window query before installation/Start. No focus or input APIs.
Add-Type @'
using System; using System.Runtime.InteropServices; using System.Text;
public class H1MenuOwnWindow {
    public delegate bool Callback(IntPtr h,IntPtr p);
    [StructLayout(LayoutKind.Sequential)] public struct Rect { public int Left,Top,Right,Bottom; }
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out Rect r);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h,out uint pid);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] public static extern bool EnumWindows(Callback cb,IntPtr p);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h,StringBuilder s,int max);
}
'@
function Check-Budget {
    param([string]$Name)
    $data=& $python (Join-Path $workspace 'PROEVEN\Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d
    $code=$LASTEXITCODE
    $data|Set-Content -LiteralPath (Join-Path $outdir "$Name.json") -Encoding utf8
    if($code -eq 2){$data=& $python (Join-Path $workspace 'PROEVEN\Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d;$code=$LASTEXITCODE;$data|Set-Content -LiteralPath (Join-Path $outdir "$Name-retry.json") -Encoding utf8}
    if($code -ne 0 -and $code -ne 25){$script:budgetStopped=$true;throw "Budget stop/unknown: $code; checkpoint only, PC stays on."}
    if($code -eq 25){Write-Output 'WARNING: weekly account budget <=25% remaining.'}
}
function Read-Pins {
    param([switch]$Temporary)
    $source=Get-Content -LiteralPath (Join-Path $workspace 'PROEVEN\activatie-h3-runtime\2026-10-09\avond\poging2\eindhashes.json') -Raw -Encoding utf8|ConvertFrom-Json
    if($source.records.Count -ne 15){throw 'Expected fifteen pins.'}
    foreach($pin in $source.records){$expected=$pin.sha256;if($Temporary -and $pin.name -eq 'dll'){$expected=$candidateHash};$hash=(Get-FileHash -LiteralPath (Join-Path $workspace $pin.path) -Algorithm SHA256).Hash.ToLowerInvariant();[ordered]@{name=$pin.name;path=$pin.path;sha256=$hash;expected=$expected;match=($hash -eq $expected)}}
}
function Read-OwnState {
    param([string]$Stage,[switch]$Modal)
    if($liveClock.Elapsed.TotalMilliseconds -ge 480000){throw 'Live480s deadline; no further live query.'}
    $rows=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
    $ownRows=@($rows|Where-Object{$_.ProcessId -eq $targetPid})
    $state=[ordered]@{stage=$Stage;at=(Get-Date).ToString('o');elapsed_ms=$liveClock.Elapsed.TotalMilliseconds;query_succeeded=$true;all_civctp_count=$rows.Count;original_pid_count=$ownRows.Count;original_pid_absent=($ownRows.Count -eq 0)}
    if($ownRows.Count -eq 0){
        if($null -ne $ownProcess){$ownProcess.Refresh();$state.has_exited=$ownProcess.HasExited;$summary.has_exited=$state.has_exited;if($state.has_exited){try{$state.exit_code=$ownProcess.ExitCode;$summary.exit_code=$state.exit_code}catch{$state.exit_code_error=$_.Exception.Message}}}
        $state.completed_at=(Get-Date).ToString('o');$state.completed_elapsed_ms=$liveClock.Elapsed.TotalMilliseconds;$state.late_os_return=($state.completed_elapsed_ms -ge 480000)
        if($rows.Count -eq 0 -and -not $state.late_os_return -and ($null -eq $ownProcess -or $state.has_exited)){$summary.exit_confirmed=$true}
        $state|ConvertTo-Json -Depth 6 -Compress|Add-Content -LiteralPath (Join-Path $outdir 'window-timeline.jsonl') -Encoding utf8
        return $state
    }
    if($rows.Count -ne 1 -or $ownRows.Count -ne 1 -or $ownRows[0].ExecutablePath -cne $exePath -or ([DateTimeOffset]$ownRows[0].CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds() -ne $creationMs){throw 'Original process identity changed or extra civctp; stop.'}
    $ownProcess.Refresh()
    $state.pid=$targetPid;$state.creation_utc_ms=$creationMs;$state.exe=$ownRows[0].ExecutablePath
    $state.process_path=$ownProcess.MainModule.FileName
    $state.process_start_utc_ms=([DateTimeOffset]$ownProcess.StartTime.ToUniversalTime()).ToUnixTimeMilliseconds()
    if($state.process_path -cne $exePath -or $state.process_start_utc_ms -ne $creationMs){throw 'Retained Process identity changed.'}
    $state.handle=$ownProcess.MainWindowHandle.ToInt64();$state.foreground_handle=[H1MenuOwnWindow]::GetForegroundWindow().ToInt64();$state.owner_matches=$false;$state.bounds=$null
    if($state.handle -ne 0){
        $owner=[uint32]0;$thread=[H1MenuOwnWindow]::GetWindowThreadProcessId($ownProcess.MainWindowHandle,[ref]$owner);$state.owner_matches=($thread -ne 0 -and $owner -eq $targetPid)
        $rect=New-Object H1MenuOwnWindow+Rect
        if([H1MenuOwnWindow]::GetWindowRect($ownProcess.MainWindowHandle,[ref]$rect)){$state.bounds=[ordered]@{left=$rect.Left;top=$rect.Top;right=$rect.Right;bottom=$rect.Bottom;width=$rect.Right-$rect.Left;height=$rect.Bottom-$rect.Top}}
    }
    if($null -ne $finalHandle -and ($state.handle -ne $finalHandle -or -not $state.owner_matches)){throw 'Definitively bound HWND/owner changed.'}
    if($Modal){
        $windows=[Collections.Generic.List[object]]::new()
        $ok=[H1MenuOwnWindow]::EnumWindows({param($h,$p)
            $pidOwner=[uint32]0;[H1MenuOwnWindow]::GetWindowThreadProcessId($h,[ref]$pidOwner)|Out-Null
            if($pidOwner -eq $targetPid){$title=[Text.StringBuilder]::new(1024);[H1MenuOwnWindow]::GetWindowText($h,$title,1024)|Out-Null;$windows.Add([ordered]@{handle=$h.ToInt64();visible=[H1MenuOwnWindow]::IsWindowVisible($h);title=$title.ToString()})}
            return $true
        },[IntPtr]::Zero)
        $state.own_windows=@($windows);$state.window_enumeration_succeeded=$ok
        $visible=@($windows|Where-Object{$_.visible});$state.own_visible_count=$visible.Count
        if(-not $ok -or $visible.Count -ne 1 -or $visible[0].handle -ne $finalHandle -or [string]::IsNullOrWhiteSpace($visible[0].title) -or $visible[0].title -match 'Error|CD-ROM|Call to Power CD'){throw 'Possible modal/extra visible own window/unreadable state; no request.'}
    }
    $state.completed_at=(Get-Date).ToString('o');$state.completed_elapsed_ms=$liveClock.Elapsed.TotalMilliseconds
    $state|ConvertTo-Json -Depth 6 -Compress|Add-Content -LiteralPath (Join-Path $outdir 'window-timeline.jsonl') -Encoding utf8
    if($liveClock.Elapsed.TotalMilliseconds -ge 480000){throw 'Late live OS query; no further live action.'}
    return $state
}

try {
    Check-Budget 'budget-preflight'
    foreach($name in @('activatie-h3-runtime-20261012-115257-h1-A.json','activatie-h3-runtime-20261012-115257-h1-B.json','activatie-h3-runtime-20261012-115257-h3-A.json','activatie-h3-runtime-20261012-115257-h3-B.json')){if(Test-Path -LiteralPath (Join-Path $workspace ('PROEVEN\ai-uitlezen\'+$name))){throw 'Existing observer output; no overwrite/start.'}}
    if((Get-FileHash -LiteralPath (Join-Path $workspace 'PROEVEN\ai-uitlezen\Lees-Onderzoeksactivatie.py') -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'ff43655e52ddc2a9c593ff64ef564c6cda54a2c11e04cc364cfbd5fface69365' -or (Get-FileHash -LiteralPath (Join-Path $workspace 'PROEVEN\ai-uitlezen\activatie-h3-package.json') -Algorithm SHA256).Hash.ToLowerInvariant() -ne '8786005d046b0a99fc6907af6b99b1e134ecb90668e021494beac8e5b1ad7564'){throw 'Observer/package pin mismatch.'}

    if((Get-FileHash -LiteralPath (Join-Path $workspace 'ONTWERP\H3-T0-HERVATTING.md') -Algorithm SHA256).Hash.ToLowerInvariant() -ne $designHash -or (Get-FileHash -LiteralPath $toolPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $toolHash){throw 'Frozen design/tool hash mismatch.'}
    $cleanup=Get-Content -LiteralPath (Join-Path $originalProbe 'close-mainwindow\afwikkeling-resultaat.json') -Raw -Encoding utf8|ConvertFrom-Json
    if(-not $cleanup.exit_confirmed){throw 'Original cleanup evidence not confirmed.'}
    $beforeProcs=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
    if($beforeProcs.Count -ne 0){throw 'Preflight all-civctp gate not count0.'}
    $pins=@(Read-Pins)
    if(@($pins|Where-Object{-not $_.match}).Count -ne 0){throw 'Original fifteen pins mismatch.'}
    $manifestPath=Join-Path $workspace 'PROEVEN\score-h1\H1-I.manifest.json'
    $packagePath=Join-Path $workspace 'PROEVEN\score-h1\package-manifest.json'
    if((Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '77b1ad5b88343c18ecf7b67de6b2402900b0b39f7edcd0bbd53e1b2bbac7f49e' -or (Get-FileHash -LiteralPath $packagePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'cf334df116b5d22aa480f73fab4e715418a2a02da375c7196d65ed7006914a24'){throw 'Pinned H1 variant/package manifest mismatch.'}
    $manifest=Get-Content -LiteralPath $manifestPath -Raw -Encoding utf8|ConvertFrom-Json
    if($manifest.variant -cne 'H1-I' -or $manifest.original_sha256 -ne $originalHash -or $manifest.candidate_sha256 -ne $candidateHash -or (Get-FileHash -LiteralPath $candidatePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $candidateHash){throw 'H1-I candidate/manifest binding mismatch.'}
    Copy-Item -LiteralPath $dllPath -Destination (Join-Path $outdir 'robotcom.before.dll')
    if((Get-FileHash -LiteralPath (Join-Path $outdir 'robotcom.before.dll') -Algorithm SHA256).Hash.ToLowerInvariant() -ne $originalHash){throw 'Original DLL backup mismatch.'}
    $reference=Get-Content -LiteralPath (Join-Path $originalProbe 'preflight.json') -Raw -Encoding utf8|ConvertFrom-Json
    $referenceEnd=Get-Content -LiteralPath (Join-Path $originalProbe 'close-mainwindow\eindhashes.json') -Raw -Encoding utf8|ConvertFrom-Json
    $profileHash=(Get-FileHash -LiteralPath $profilePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if($profileHash -ne $referenceEnd.profile.sha256){throw 'Profile changed relative to original menu endstate.'}
    Copy-Item -LiteralPath $profilePath -Destination (Join-Path $outdir 'userprofile.before.txt');$profileSaved=$true
    if((Get-FileHash -LiteralPath (Join-Path $outdir 'userprofile.before.txt') -Algorithm SHA256).Hash.ToLowerInvariant() -ne $profileHash){throw 'Profile snapshot mismatch.'}
    $layers=@(foreach($layer in $reference.start_inputs.layers){if(Test-Path -LiteralPath $layer.key -ErrorAction Stop){$key=Get-Item -LiteralPath $layer.key -ErrorAction Stop;$has=$key.GetValueNames() -contains $exePath;$value=$null;if($has){$value=$key.GetValue($exePath)};$actual=[ordered]@{key=$layer.key;key_exists=$true;value_exists=$has;value=$value;read_succeeded=$true}}else{$actual=[ordered]@{key=$layer.key;key_exists=$false;value_exists=$false;value=$null;read_succeeded=$true}};if($actual.key_exists -ne $layer.key_exists -or $actual.value_exists -ne $layer.value_exists -or $actual.value -cne $layer.value){throw 'Compat Layers changed; no self-correction.'};$actual})
    $compat=[Environment]::GetEnvironmentVariable('__COMPAT_LAYER','Process')
    if($compat -cne $reference.start_inputs.compat_layer){throw 'Inherited compat layer changed.'}
    $oldScreenshot=[ordered]@{path=$capturePath;exists=(Test-Path -LiteralPath $capturePath)}
    if($oldScreenshot.exists){Copy-Item -LiteralPath $capturePath -Destination (Join-Path $outdir 'capture.before.png');$oldScreenshot.sha256=(Get-FileHash -LiteralPath $capturePath -Algorithm SHA256).Hash.ToLowerInvariant();$oldScreenshot.backup_sha256=(Get-FileHash -LiteralPath (Join-Path $outdir 'capture.before.png') -Algorithm SHA256).Hash.ToLowerInvariant();$oldScreenshot.mtime_utc=(Get-Item -LiteralPath $capturePath).LastWriteTimeUtc.ToString('o');if($oldScreenshot.sha256 -ne $oldScreenshot.backup_sha256){throw 'Screenshot backup mismatch.'}}
    [ordered]@{checked_at=(Get-Date).ToString('o');all_civctp_query_succeeded=$true;all_civctp_count=0;records=$pins;design_sha256=$designHash;tool_sha256=$toolHash;manifest_sha256='77b1ad5b88343c18ecf7b67de6b2402900b0b39f7edcd0bbd53e1b2bbac7f49e';package_sha256='cf334df116b5d22aa480f73fab4e715418a2a02da375c7196d65ed7006914a24';start_inputs=@{exe=$exePath;working_directory=(Split-Path $exePath);arguments=@();window_style='Normal';compat_layer=$compat;layers=$layers;profile_fields=$reference.start_inputs.profile_fields};profile=@{sha256=$profileHash;length=(Get-Item -LiteralPath $profilePath).Length;mtime_utc=(Get-Item -LiteralPath $profilePath).LastWriteTimeUtc.ToString('o')};screenshot=$oldScreenshot}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $outdir 'preflight.json') -Encoding utf8
    Check-Budget 'budget-before-install'
    if(@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop).Count -ne 0){throw 'Fresh install gate not count0.'}
    if((Get-FileHash -LiteralPath $dllPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $originalHash){throw 'DLL changed before installation.'}
    $installed=$true
    Copy-Item -LiteralPath $candidatePath -Destination $dllPath
    if((Get-FileHash -LiteralPath $dllPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $candidateHash){throw 'Installed H1-I hash mismatch; no Start.'}
    $temporaryPins=@(Read-Pins -Temporary)
    [ordered]@{installed_at=(Get-Date).ToString('o');dll_sha256=$candidateHash;original_backup_sha256=$originalHash;records=$temporaryPins}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $outdir 'temporary-install.json') -Encoding utf8
    if(@($temporaryPins|Where-Object{-not $_.match}).Count -ne 0){throw 'Temporary DLL/other fourteen pins mismatch.'}
    Check-Budget 'budget-before-start'
    if(@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop).Count -ne 0){throw 'Fresh Start gate not count0.'}
    $startTicks=[Diagnostics.Stopwatch]::GetTimestamp();$liveClock=[Diagnostics.Stopwatch]::StartNew();$startCalled=(Get-Date).ToString('o');$summary.start_count=1
    $startOut=& powershell.exe -NoProfile -File $toolPath -Action Start 2>&1;$startCode=$LASTEXITCODE
    $startOut|Set-Content -LiteralPath (Join-Path $outdir 'start-stdout.txt') -Encoding utf8
    $match=[regex]::Match(($startOut -join "`n"),'process (\d+)\.')
    if($startCode -ne 0 -or -not $match.Success){throw 'Start lacks successful PID evidence; no retry.'}
    $targetPid=[int]$match.Groups[1].Value;$rows=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
    if($rows.Count -ne 1 -or $rows[0].ProcessId -ne $targetPid -or $rows[0].ExecutablePath -cne $exePath){throw 'Immediate start binding failed.'}
    $creationMs=([DateTimeOffset]$rows[0].CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds()
    $summary.pid=$targetPid;$summary.creation_utc_ms=$creationMs
    [ordered]@{start_monotonic_ticks=$startTicks;monotonic_frequency=[Diagnostics.Stopwatch]::Frequency;called_at=$startCalled;bound_at=(Get-Date).ToString('o');pid=$targetPid;creation_utc_ms=$creationMs;exe=$exePath;helper_exit_code=$startCode;bound_elapsed_ms=$liveClock.Elapsed.TotalMilliseconds}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $outdir 'start-record.json') -Encoding utf8
    try{$ownProcess=[Diagnostics.Process]::GetProcessById($targetPid);$ownProcess.Handle|Out-Null}catch{
        $vanished=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
        [ordered]@{at=(Get-Date).ToString('o');query_succeeded=$true;all_civctp_count=$vanished.Count;original_pid_count=@($vanished|Where-Object{$_.ProcessId -eq $targetPid}).Count;process_object_error=$_.Exception.Message}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $outdir 'early-exit.json') -Encoding utf8
        if($vanished.Count -eq 0){$summary.exit_confirmed=$true};throw
    }
    Write-Output "START_PID=$targetPid CreationUtcMs=$creationMs; H1-I intro observation active."
    $lastNotice=0;$budget90Checked=$false
    while($liveClock.Elapsed.TotalMilliseconds -lt 180000){
        $cycleStarted=$liveClock.Elapsed.TotalMilliseconds
        $state=Read-OwnState 'intro'
        if($state.original_pid_absent){throw 'Original PID disappeared during intro; stop live observation.'}
        if(-not $budget90Checked -and $liveClock.Elapsed.TotalMilliseconds -ge 90000){Check-Budget 'budget-90s';$budget90Checked=$true}
        if($liveClock.Elapsed.TotalMilliseconds-$lastNotice -ge 30000){Write-Output "INTRO elapsed=$([Math]::Round($liveClock.Elapsed.TotalSeconds,1))s PID=$targetPid HWND=$($state.handle) foreground=$($state.foreground_handle)";$lastNotice=$liveClock.Elapsed.TotalMilliseconds}
        $remaining=[Math]::Floor([Math]::Min(180000-$liveClock.Elapsed.TotalMilliseconds,500-($liveClock.Elapsed.TotalMilliseconds-$cycleStarted)));if($remaining -gt 0){Start-Sleep -Milliseconds ([int]$remaining)}
    }
    $stableSince=$null;$stableSignature=$null;$stableState=$null
    while($liveClock.Elapsed.TotalMilliseconds -lt 190000){
        $cycleStarted=$liveClock.Elapsed.TotalMilliseconds
        $state=Read-OwnState 'stabilize'
        if($state.original_pid_absent){throw 'Original PID disappeared during stabilization.'}
        $good=($state.handle -ne 0 -and $state.owner_matches -and $null -ne $state.bounds -and $state.bounds.width -gt 0 -and $state.bounds.height -gt 0 -and $state.foreground_handle -eq $state.handle)
        $signature=$state.handle.ToString()+'|'+($state.bounds|ConvertTo-Json -Compress)
        if($good){if($signature -ne $stableSignature){$stableSignature=$signature;$stableSince=$state.completed_elapsed_ms};if($state.completed_elapsed_ms-$stableSince -ge 2000){$stableState=$state;break}}else{$stableSince=$null;$stableSignature=$null}
        $remaining=[Math]::Floor([Math]::Min(190000-$liveClock.Elapsed.TotalMilliseconds,500-($liveClock.Elapsed.TotalMilliseconds-$cycleStarted)));if($remaining -gt 0){Start-Sleep -Milliseconds ([int]$remaining)}
    }
    if($null -eq $stableState){throw 'NOT_OBSERVABLE_STARTUP_NOT_SETTLED; no definitive HWND or close request.'}
    $finalHandle=[long]$stableState.handle;$summary.handle=$finalHandle
    [ordered]@{bound_at=(Get-Date).ToString('o');stable_for_ms=$stableState.completed_elapsed_ms-$stableSince;sample=$stableState}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $outdir 'final-window-binding.json') -Encoding utf8
    Check-Budget 'budget-before-capture'
    $captureFailure=$null
    try {
        if($liveClock.Elapsed.TotalMilliseconds -ge 188000){throw 'Insufficient time for30s Capture plus helper overhead before220s; no Capture.'}
        $state=Read-OwnState 'before-capture'
        if($state.original_pid_absent){throw 'Original PID disappeared before Capture.'}
        $summary.capture_count=1
        [ordered]@{called_at=(Get-Date).ToString('o');pid=$targetPid;creation_utc_ms=$creationMs;handle=$finalHandle;timeout_ms=30000}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $outdir 'capture-request.json') -Encoding utf8
        $captureOut=& powershell.exe -NoProfile -File $toolPath -Action Capture -CaptureWaitForForeground -CaptureWaitTimeoutMs 30000 -ExpectedProcessId $targetPid -ExpectedCreationUtcMs $creationMs -ExpectedWindowHandle $finalHandle 2>&1;$captureCode=$LASTEXITCODE
        $captureOut|Set-Content -LiteralPath (Join-Path $outdir 'capture-trace.txt') -Encoding utf8
        [ordered]@{completed_at=(Get-Date).ToString('o');helper_exit_code=$captureCode;elapsed_ms=$liveClock.Elapsed.TotalMilliseconds;late_return=($liveClock.Elapsed.TotalMilliseconds -gt 220000)}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $outdir 'capture-result.json') -Encoding utf8
        if($captureCode -ne 0){throw "Capture exit$captureCode; no retry."}
        Copy-Item -LiteralPath $capturePath -Destination (Join-Path $outdir 'menu-01.png')
        [ordered]@{copied_at=(Get-Date).ToString('o');sha256=(Get-FileHash -LiteralPath (Join-Path $outdir 'menu-01.png') -Algorithm SHA256).Hash.ToLowerInvariant();requires_actual_review=$true;late_return=($liveClock.Elapsed.TotalMilliseconds -gt 220000)}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $outdir 'capture-image.json') -Encoding utf8
        $summary.image_review='SAVED_REQUIRES_ACTUAL_IMAGE_REVIEW'
    } catch {$captureFailure=$_.Exception.Message;[ordered]@{at=(Get-Date).ToString('o');error=$captureFailure;elapsed_ms=$liveClock.Elapsed.TotalMilliseconds}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $outdir 'capture-error.json') -Encoding utf8}
    if($null -ne $captureFailure){throw $captureFailure}
    $summary.outcome='MENU_READY_LOAD_T0_REQUIRED'
} catch {$summary.error=$_.Exception.Message;$summary.outcome='STOPPED_WITH_EVIDENCE'}
finally {
    $summary.live_ended_at=(Get-Date).ToString('o');if($null -ne $liveClock){$summary.live_elapsed_ms=$liveClock.Elapsed.TotalMilliseconds;$liveClock.Stop()}
    $request|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $outdir 'close-request.json') -Encoding utf8
    $closeChecks|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $outdir 'process-checks.json') -Encoding utf8
    $eventsRecord=[ordered]@{query_succeeded=$false;events=@();error=$null;start=$startCalled;end=$summary.live_ended_at}
    if($summary.start_count -eq 1){
        try{
            $events=@(Get-WinEvent -FilterHashtable @{LogName='Application';Id=@(1000,1001);StartTime=[DateTimeOffset]::Parse($startCalled).LocalDateTime;EndTime=[DateTimeOffset]::Parse($summary.live_ended_at).LocalDateTime} -ErrorAction Stop)
            $relevant=[Collections.Generic.List[object]]::new()
            foreach($event in $events){$xml=[xml]$event.ToXml();$fields=[ordered]@{};$index=0;foreach($data in @($xml.Event.EventData.Data)){$name=[string]$data.Name;if(-not $name){$name='unnamed_'+$index};$fields[$name]=[string]$data.'#text';$index++};if(@($fields.Values) -contains $exePath){$pidMatch=$false;if($null -ne $targetPid){$pidMatch=(@($fields.Values) -contains ([string]$targetPid) -or @($fields.Values) -contains ('0x'+$targetPid.ToString('x')))};$relevant.Add([ordered]@{id=$event.Id;record_id=$event.RecordId;at=$event.TimeCreated.ToString('o');exact_path_match=$true;pid_match=$pidMatch;report_id=$fields.ReportId;fields=$fields})}}
            $eventsRecord.query_succeeded=$true;$eventsRecord.events=@($relevant)
        }catch{if($_.FullyQualifiedErrorId -like 'NoMatchingEventsFound*'){$eventsRecord.query_succeeded=$true;$eventsRecord.no_matching_events=$true}else{$eventsRecord.error=$_.Exception.Message}}
    }
    $eventsRecord|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $outdir 'startup-application-events.json') -Encoding utf8
    $restore=[ordered]@{attempted=$false;restored=$false;reason=$null}
    if($installed -and -not $budgetStopped -and ($summary.start_count -eq 0 -or $summary.exit_confirmed)){
        try{
            Check-Budget 'budget-before-restore'
            if((Get-FileHash -LiteralPath $dllPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $candidateHash -or (Get-FileHash -LiteralPath (Join-Path $outdir 'robotcom.before.dll') -Algorithm SHA256).Hash.ToLowerInvariant() -ne $originalHash){throw 'Restore current-H1-I/backup-original hash gate failed.'}
            $restoreRows=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
            $restore.query_at=(Get-Date).ToString('o');$restore.all_civctp_count=$restoreRows.Count;$restore.query_succeeded=$true
            if($restoreRows.Count -ne 0){throw 'Fresh restoration process gate not count0.'}
            $restore.attempted=$true
            Copy-Item -LiteralPath (Join-Path $outdir 'robotcom.before.dll') -Destination $dllPath
            $restore.sha256=(Get-FileHash -LiteralPath $dllPath -Algorithm SHA256).Hash.ToLowerInvariant()
            if($restore.sha256 -ne $originalHash){throw 'Restored original hash mismatch.'}
            $restore.restored=$true;$summary.restored=$true
        }catch{$restore.reason=$_.Exception.Message}
    }else{$restore.reason='No installation, or live/unknown instance, or budget stop; no restoration copy.'}
    $restore|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $outdir 'restore.json') -Encoding utf8
    if($profileSaved){
        try{Copy-Item -LiteralPath $profilePath -Destination (Join-Path $outdir 'userprofile.after.txt');$afterHash=(Get-FileHash -LiteralPath $profilePath -Algorithm SHA256).Hash.ToLowerInvariant();$endPins=@(Read-Pins);[ordered]@{checked_at=(Get-Date).ToString('o');records=$endPins;all_fifteen_original_pins_match=(@($endPins|Where-Object{-not $_.match}).Count -eq 0);tool_sha256=(Get-FileHash -LiteralPath $toolPath -Algorithm SHA256).Hash.ToLowerInvariant();profile=@{sha256=$afterHash;before_sha256=$profileHash;byte_unchanged=($afterHash -eq $profileHash);mtime_utc=(Get-Item -LiteralPath $profilePath).LastWriteTimeUtc.ToString('o');state_preserved=$true}}|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $outdir 'startup-eindhashes.json') -Encoding utf8}catch{$summary.postflight_error=$_.Exception.Message}
    }
    $summary.installation_attempted=$installed;$summary.installed=(Test-Path -LiteralPath (Join-Path $outdir 'temporary-install.json'));$summary.budget_stopped=$budgetStopped
    $summary.exit_classification='EXIT_NOT_CONFIRMED'
    if($summary.exit_confirmed){$summary.exit_classification='EXIT_CONFIRMED_CAUSE_UNKNOWN';if($summary.exit_code -eq 0 -and $eventsRecord.query_succeeded -and $eventsRecord.events.Count -eq 0){$summary.exit_classification='EXIT_CONFIRMED_NO_CRASH_OBSERVED'}}
    if($null -ne $ownProcess){$ownProcess.Dispose()}
    $summary.finished_at=(Get-Date).ToString('o')
    $summary|ConvertTo-Json -Depth 7|Set-Content -LiteralPath (Join-Path $outdir 'startup-resultaat.json') -Encoding utf8
    Write-Output ($summary|ConvertTo-Json -Depth 7)
}
