$ErrorActionPreference = 'Stop'
$outdir = $PSScriptRoot
$workspace = 'C:\GIT\ctp'
$armDir=Split-Path $outdir
$started=Get-Content -LiteralPath (Join-Path $armDir 'start-record.json') -Raw -Encoding utf8|ConvertFrom-Json
$final=Get-Content -LiteralPath (Join-Path $armDir 'final-window-binding.json') -Raw -Encoding utf8|ConvertFrom-Json
$targetPid=[int]$started.pid
$expectedCreationMs=[long]$started.creation_utc_ms
$expectedExe = 'C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe'
$expectedHandle=[long]$final.sample.handle
$expectedToolHash = 'd2dbbfcad3d9d8bec8e6a99a399d59561d8f9c4e9a48576a2aefc32e5997bc74'
$expectedDesignHash = '21fcf7cadf2c459f99ed45047f612aba11fe98a0234d1d898c496d3e2f64ecec'
$profilePath = Join-Path $workspace 'CTP-proef\ctp_program\ctp\userprofile.txt'
$request = [ordered]@{attempted=$false;call_count=0;called_at=$null;bool_return=$null;exception=$null}
$checks = [Collections.Generic.List[object]]::new()
$summary = [ordered]@{began_at=(Get-Date).ToString('o');outcome='NOT_APPLIED';error=$null;exit_confirmed=$false;has_exited=$null;exit_code=$null;last_successful_query=$null;pid=$targetPid;creation_utc_ms=$expectedCreationMs;exe=$expectedExe;handle=$expectedHandle}
$ownProcess = $null
$clock = $null
$profileBeforeSaved = $false
if (Test-Path -LiteralPath (Join-Path $outdir 'close-request.json')) { throw 'Existing cleanup request evidence; no second execution.' }

# All types and binding/observation routines are ready before a request is possible.
Add-Type @'
using System; using System.Runtime.InteropServices; using System.Text;
public class CtpCleanupOwnWindow {
    public delegate bool Callback(IntPtr h, IntPtr p);
    [DllImport("user32.dll")] public static extern bool EnumWindows(Callback cb, IntPtr p);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int max);
}
'@

function Read-PinnedFiles {
    param([switch]$Temporary)
    $source = Get-Content -LiteralPath (Join-Path $workspace 'PROEVEN\activatie-h3-runtime\2026-10-09\avond\poging2\eindhashes.json') -Raw -Encoding utf8 | ConvertFrom-Json
    if ($source.records.Count -ne 15) { throw 'Expected fifteen pins.' }
    foreach ($pin in $source.records) {
        $hash = (Get-FileHash -LiteralPath (Join-Path $workspace $pin.path) -Algorithm SHA256).Hash.ToLowerInvariant()
        [ordered]@{name=$pin.name;path=$pin.path;sha256=$hash;expected=$(if($Temporary -and $pin.name -eq 'dll'){'59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0'}else{$pin.sha256});match=($hash -eq $(if($Temporary -and $pin.name -eq 'dll'){'59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0'}else{$pin.sha256}))}
    }
}

function Read-OwnBinding {
    param([string]$Stage)
    if(-not $request.attempted -and (([Diagnostics.Stopwatch]::GetTimestamp()-[long]$started.start_monotonic_ticks)*1000.0/[long]$started.monotonic_frequency) -ge 470000){throw 'Insufficient10s reserve within480s; no request.'}
    $state = [ordered]@{stage=$Stage;query_started_at=(Get-Date).ToString('o');query_succeeded=$false;original_pid_absent=$false}
    $checks.Add($state)
    $row = @(Get-CimInstance Win32_Process -Filter "ProcessId=$targetPid" -ErrorAction Stop)
    $all = @(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop)
    $state.query_succeeded = $true
    $state.query_completed_at = (Get-Date).ToString('o')
    $state.original_pid_count = $row.Count
    $state.all_civctp_count = $all.Count
    $summary.last_successful_query = $state.query_completed_at
    if ($row.Count -eq 0) { $state.original_pid_absent=$true; return $state }
    if ($row.Count -ne 1) { throw 'Original PID query ambiguous.' }
    $creationMs = ([DateTimeOffset]$row[0].CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds()
    $state.pid = [int]$row[0].ProcessId
    $state.creation_utc_ms = $creationMs
    $state.exe = $row[0].ExecutablePath
    if ($state.pid -ne $targetPid -or $creationMs -ne $expectedCreationMs -or $state.exe -cne $expectedExe) { throw 'Original PID identity differs; no reused PID targeting.' }
    if ($all.Count -ne 1 -or $all[0].ProcessId -ne $targetPid -or $all[0].ExecutablePath -cne $expectedExe) { throw 'All-civctp gate is not exclusively the original instance.' }
    if ($null -eq $script:ownProcess) { $script:ownProcess=[Diagnostics.Process]::GetProcessById($targetPid);$script:ownProcess.Handle | Out-Null }
    $ownProcess.Refresh()
    $state.process_path = $ownProcess.MainModule.FileName
    $state.process_start_utc_ms = ([DateTimeOffset]$ownProcess.StartTime.ToUniversalTime()).ToUnixTimeMilliseconds()
    $state.main_window_handle = $ownProcess.MainWindowHandle.ToInt64()
    if ($state.process_path -cne $expectedExe -or $state.process_start_utc_ms -ne $expectedCreationMs -or $state.main_window_handle -eq 0 -or $state.main_window_handle -ne $expectedHandle) { throw 'Original Process path/start/handle binding changed.' }
    $ownerPid = [uint32]0
    $ownerThread = [CtpCleanupOwnWindow]::GetWindowThreadProcessId($ownProcess.MainWindowHandle, [ref]$ownerPid)
    $state.owner_matches = ($ownerThread -ne 0 -and $ownerPid -eq $targetPid)
    if (-not $state.owner_matches) { throw 'Original main-window owner unreadable or changed.' }
    $windows = [Collections.Generic.List[object]]::new()
    $enumOk = [CtpCleanupOwnWindow]::EnumWindows({param($h,$p)
        $windowOwner = [uint32]0
        [CtpCleanupOwnWindow]::GetWindowThreadProcessId($h,[ref]$windowOwner) | Out-Null
        if ($windowOwner -eq $targetPid) {
            $title = [Text.StringBuilder]::new(1024)
            [CtpCleanupOwnWindow]::GetWindowText($h,$title,1024) | Out-Null
            $windows.Add([ordered]@{handle=$h.ToInt64();visible=[CtpCleanupOwnWindow]::IsWindowVisible($h);title=$title.ToString()})
        }
        return $true
    },[IntPtr]::Zero)
    $state.window_enumeration_succeeded = $enumOk
    $state.own_windows = @($windows)
    if (-not $enumOk) { throw 'Own window enumeration failed.' }
    $visible = @($windows | Where-Object {$_.visible})
    $state.own_visible_count = $visible.Count
    if ($visible.Count -ne 1 -or $visible[0].handle -ne $expectedHandle -or [string]::IsNullOrWhiteSpace($visible[0].title) -or $visible[0].title -match 'Error|CD-ROM|Call to Power CD') { throw 'Possible modal, extra visible own window or unreadable main-window state.' }
    $state.binding_completed_at = (Get-Date).ToString('o')
    return $state
}

try {
    $budget = & 'C:\Users\Stephan\AppData\Local\Programs\Python\Python312\python.exe' (Join-Path $workspace 'PROEVEN\Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d
    $budgetCode = $LASTEXITCODE
    $budget | Set-Content -LiteralPath (Join-Path $outdir 'budget-preflight.json') -Encoding utf8
    if ($budgetCode -eq 2) {
        $budget = & 'C:\Users\Stephan\AppData\Local\Programs\Python\Python312\python.exe' (Join-Path $workspace 'PROEVEN\Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d
        $budgetCode = $LASTEXITCODE
        $budget | Set-Content -LiteralPath (Join-Path $outdir 'budget-preflight-retry.json') -Encoding utf8
    }
    if ($budgetCode -ne 0 -and $budgetCode -ne 25) { $summary.outcome='BUDGET_STOP_CHECKPOINT';throw "Budget gate stopped: $budgetCode" }
    if ($budgetCode -eq 25) { Write-Output 'WARNING: account weekly remaining budget <=25%.' }
    $designHash = (Get-FileHash -LiteralPath (Join-Path $workspace 'ONTWERP\H3-T0-HERVATTING.md') -Algorithm SHA256).Hash.ToLowerInvariant()
    $toolHash = (Get-FileHash -LiteralPath (Join-Path $workspace 'PROEVEN\Bedien-CTP.ps1') -Algorithm SHA256).Hash.ToLowerInvariant()
    $oldNoCall = Get-Content -LiteralPath (Join-Path (Split-Path $outdir) 'close-request.json') -Raw -Encoding utf8 | ConvertFrom-Json
    if ($designHash -ne $expectedDesignHash -or $toolHash -ne $expectedToolHash -or $oldNoCall.call_count -ne 0) { throw 'Frozen design/tool/no-call evidence mismatch.' }
    $pins = @(Read-PinnedFiles -Temporary)
    $profileItem = Get-Item -LiteralPath $profilePath
    $profileHash = (Get-FileHash -LiteralPath $profilePath -Algorithm SHA256).Hash.ToLowerInvariant()
    Copy-Item -LiteralPath $profilePath -Destination (Join-Path $outdir 'userprofile.before.txt')
    $profileBeforeSaved = $true
    $preflight = [ordered]@{checked_at=(Get-Date).ToString('o');design_sha256=$designHash;tool_sha256=$toolHash;c1_close_call_count=$oldNoCall.call_count;records=$pins;profile=@{sha256=$profileHash;mtime_utc=$profileItem.LastWriteTimeUtc.ToString('o');length=$profileItem.Length;snapshot_sha256=(Get-FileHash -LiteralPath (Join-Path $outdir 'userprofile.before.txt') -Algorithm SHA256).Hash.ToLowerInvariant()};budget=($budget|ConvertFrom-Json)}
    $preflight | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath (Join-Path $outdir 'preflight.json') -Encoding utf8
    if (@($pins|Where-Object {-not $_.match}).Count -ne 0 -or $preflight.profile.snapshot_sha256 -ne $profileHash) { throw 'Pin/profile snapshot mismatch.' }
    $first = Read-OwnBinding 'preflight-binding'
    if ($first.original_pid_absent) {
        $summary.outcome='TARGET_PID_ABSENT_NO_CLOSE_NEEDED'
    } else {
        $beforeRequest = Read-OwnBinding 'immediately-before-request'
        if ($beforeRequest.original_pid_absent) {
            $summary.outcome='TARGET_PID_ABSENT_NO_CLOSE_NEEDED'
        } else {
            $clock = [Diagnostics.Stopwatch]::StartNew()
            $request.called_at = (Get-Date).ToString('o')
            $request.attempted = $true
            $request.call_count = 1
            try { $request.bool_return=$ownProcess.CloseMainWindow() }
            catch { $request.exception=$_.Exception.Message;throw }
            finally { $request.return_elapsed_ms=$clock.Elapsed.TotalMilliseconds;$request|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $outdir 'close-request.json') -Encoding utf8 }
            $summary.outcome='EXIT_NOT_CONFIRMED'
            if (-not $request.bool_return) { throw 'CloseMainWindow returned false; no retry.' }
            foreach ($offset in @(1000,5000,9900)) {
                while ($clock.Elapsed.TotalMilliseconds -lt $offset) {
                    $remaining = [Math]::Floor($offset-$clock.Elapsed.TotalMilliseconds)
                    if ($remaining -lt 1) { break }
                    Start-Sleep -Milliseconds ([int][Math]::Min(100,$remaining))
                }
                if ($clock.Elapsed.TotalMilliseconds -ge 10000) { break }
                $observed = Read-OwnBinding ("after-request-around-$offset-ms")
                $observed.request_elapsed_ms = $clock.Elapsed.TotalMilliseconds
                $observed.late_os_return = ($observed.request_elapsed_ms -gt 10000)
                if ($observed.original_pid_absent) {
                    $ownProcess.Refresh()
                    $observed.has_exited = $ownProcess.HasExited
                    $summary.has_exited = $observed.has_exited
                    if ($observed.has_exited) {
                        try { $observed.exit_code=$ownProcess.ExitCode;$summary.exit_code=$observed.exit_code }
                        catch { $observed.exit_code_error=$_.Exception.Message }
                    }
                    $observed.request_elapsed_ms = $clock.Elapsed.TotalMilliseconds
                    $observed.late_os_return = ($observed.request_elapsed_ms -gt 10000)
                    if (-not $observed.late_os_return -and $observed.all_civctp_count -eq 0 -and $observed.has_exited) {
                        $summary.exit_confirmed=$true
                        $summary.outcome='EXIT_CONFIRMED_CAUSE_UNKNOWN'
                    }
                    break
                }
                if ($observed.late_os_return) { break }
            }
        }
    }
} catch {
    $summary.error = $_.Exception.Message
    if ($summary.outcome -eq 'NOT_APPLIED') { $summary.outcome='GATE_FAILED_NO_REQUEST' }
} finally {
    if ($null -ne $clock) { $summary.observation_elapsed_ms=$clock.Elapsed.TotalMilliseconds;$summary.late_observation_return=($summary.observation_elapsed_ms -gt 10000);$clock.Stop() }
    $summary.observation_ended_at = (Get-Date).ToString('o')
    $request | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $outdir 'close-request.json') -Encoding utf8
    $checks | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $outdir 'process-checks.json') -Encoding utf8
    $eventsRecord = [ordered]@{queried=$false;query_succeeded=$false;window_start=$request.called_at;window_end=$summary.observation_ended_at;events=@();error=$null}
    if ($request.attempted) {
        $eventsRecord.queried=$true
        try {
            $events = @(Get-WinEvent -FilterHashtable @{LogName='Application';Id=@(1000,1001);StartTime=[DateTimeOffset]::Parse($request.called_at).LocalDateTime;EndTime=[DateTimeOffset]::Parse($summary.observation_ended_at).LocalDateTime} -ErrorAction Stop)
            $relevant = [Collections.Generic.List[object]]::new()
            foreach ($event in $events) {
                $xml = [xml]$event.ToXml();$fields=[ordered]@{};$index=0
                foreach ($data in @($xml.Event.EventData.Data)) { $name=[string]$data.Name;if(-not $name){$name='unnamed_'+$index};$fields[$name]=[string]$data.'#text';$index++ }
                if (@($fields.Values) -contains $expectedExe) {
                    $relevant.Add([ordered]@{id=$event.Id;record_id=$event.RecordId;at=$event.TimeCreated.ToString('o');exact_path_match=$true;pid_match=(@($fields.Values) -contains ([string]$targetPid) -or @($fields.Values) -contains ('0x'+$targetPid.ToString('x')));fields=$fields;report_id=$fields.ReportId})
                }
            }
            $eventsRecord.query_succeeded=$true;$eventsRecord.events=@($relevant)
        } catch {
            if ($_.FullyQualifiedErrorId -like 'NoMatchingEventsFound*') {$eventsRecord.query_succeeded=$true;$eventsRecord.no_matching_events=$true} else {$eventsRecord.error=$_.Exception.Message}
        }
    }
    $eventsRecord | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $outdir 'application-events.json') -Encoding utf8
    if ($summary.exit_confirmed -and $summary.exit_code -eq 0 -and $eventsRecord.query_succeeded -and $eventsRecord.events.Count -eq 0) { $summary.outcome='EXIT_CONFIRMED_NO_CRASH_OBSERVED' }
    $restore=[ordered]@{attempted=$false;restored=$false;reason=$null}
    if($summary.exit_confirmed -or $summary.outcome -eq 'TARGET_PID_ABSENT_NO_CLOSE_NEEDED'){
        try{
            $freshBudget=& 'C:\Users\Stephan\AppData\Local\Programs\Python\Python312\python.exe' (Join-Path $workspace 'PROEVEN\Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d
            $freshCode=$LASTEXITCODE;$freshBudget|Set-Content -LiteralPath (Join-Path $outdir 'budget-before-restore.json') -Encoding utf8
            if($freshCode -eq 2){$freshBudget=& 'C:\Users\Stephan\AppData\Local\Programs\Python\Python312\python.exe' (Join-Path $workspace 'PROEVEN\Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d;$freshCode=$LASTEXITCODE;$freshBudget|Set-Content -LiteralPath (Join-Path $outdir 'budget-before-restore-retry.json') -Encoding utf8}
            if($freshCode -ne 0 -and $freshCode -ne 25){throw 'Budget stop/unknown: no restore mutation.'}
            $dll=Join-Path $workspace 'CTP-proef\ctp_program\ctp\dll\ai\robotcom.dll';$backup=Join-Path $armDir 'robotcom.before.dll'
            if((Get-FileHash -LiteralPath $dll -Algorithm SHA256).Hash.ToLowerInvariant() -ne '59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0' -or (Get-FileHash -LiteralPath $backup -Algorithm SHA256).Hash.ToLowerInvariant() -ne '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'){throw 'Restore candidate/backup mismatch.'}
            $fresh=@(Get-CimInstance Win32_Process -Filter "Name='civctp.exe'" -ErrorAction Stop);$restore.query_at=(Get-Date).ToString('o');$restore.all_civctp_count=$fresh.Count
            if($fresh.Count -ne 0){throw 'Fresh restoration gate not count0.'}
            $restore.attempted=$true;Copy-Item -LiteralPath $backup -Destination $dll;$restore.sha256=(Get-FileHash -LiteralPath $dll -Algorithm SHA256).Hash.ToLowerInvariant()
            if($restore.sha256 -ne '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'){throw 'Restored original mismatch.'};$restore.restored=$true
        }catch{$restore.reason=$_.Exception.Message}
    }else{$restore.reason='Open/unknown instance: no restore.'}
    $restore|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $outdir 'restore.json') -Encoding utf8
    if ($profileBeforeSaved) {
        try {
            Copy-Item -LiteralPath $profilePath -Destination (Join-Path $outdir 'userprofile.after.txt')
            $afterHash=(Get-FileHash -LiteralPath $profilePath -Algorithm SHA256).Hash.ToLowerInvariant()
            $endPins=@(Read-PinnedFiles)
            $endToolHash=(Get-FileHash -LiteralPath (Join-Path $workspace 'PROEVEN\Bedien-CTP.ps1') -Algorithm SHA256).Hash.ToLowerInvariant()
            [ordered]@{checked_at=(Get-Date).ToString('o');records=$endPins;all_fifteen_pins_match=(@($endPins|Where-Object{-not $_.match}).Count -eq 0);tool_sha256=$endToolHash;tool_match=($endToolHash -eq $expectedToolHash);profile=@{sha256=$afterHash;before_sha256=$profileHash;byte_unchanged=($afterHash -eq $profileHash);mtime_utc=(Get-Item -LiteralPath $profilePath).LastWriteTimeUtc.ToString('o');snapshot_sha256=(Get-FileHash -LiteralPath (Join-Path $outdir 'userprofile.after.txt') -Algorithm SHA256).Hash.ToLowerInvariant();state_preserved=$true}} | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath (Join-Path $outdir 'eindhashes.json') -Encoding utf8
            if (@($endPins|Where-Object{-not $_.match}).Count -ne 0 -or $endToolHash -ne $expectedToolHash) {$summary.postflight_error='Final pin/tool mismatch; preserved without repair'}
        } catch {$summary.postflight_error=$_.Exception.Message}
    }
    if ($null -ne $ownProcess) { $ownProcess.Dispose() }
    $summary.finished_at=(Get-Date).ToString('o')
    $summary | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath (Join-Path $outdir 'afwikkeling-resultaat.json') -Encoding utf8
    Write-Output ($summary|ConvertTo-Json -Depth 7)
}
