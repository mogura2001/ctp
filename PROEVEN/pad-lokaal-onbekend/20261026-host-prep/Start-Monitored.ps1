$ErrorActionPreference='Stop'
$workspace='C:\GIT\ctp';Set-Location -LiteralPath $workspace
$package=$PSScriptRoot;$c4=Join-Path $workspace 'PROEVEN/pad-lokaal-onbekend/20261026-host';$hostDir=Join-Path $c4 'host'
$python='C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe'
function Hash($p){(Get-FileHash -LiteralPath $p).Hash.ToLowerInvariant()}
function NewJson($p,$value){$s=[IO.File]::Open($p,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None);try{$b=[Text.Encoding]::UTF8.GetBytes(($value|ConvertTo-Json -Depth 30));$s.Write($b,0,$b.Length);$s.Flush()}finally{$s.Dispose()}}
function Budget {
 $v=& $python PROEVEN/Controleer-Weekbudget.py --thread 01a0f7b4-4751-7513-b510-3835ce43f47d;$code=$LASTEXITCODE
 if($code -eq 2){$v=& $python PROEVEN/Controleer-Weekbudget.py --thread 01a0f7b4-4751-7513-b510-3835ce43f47d;$code=$LASTEXITCODE}
 if($code -notin @(0,25)){throw 'Budget stop/unknown; PC stays on'}
 if($code -eq 25){Write-Warning 'Weekbudget25%ofminder resterend'}
 return ($v|ConvertFrom-Json)
}
$gate=Get-Content (Join-Path $package 'ROOT-HOST.json') -Raw|ConvertFrom-Json
if($gate.allowed -ne $true -or $gate.install_allowed -ne $true -or $gate.start_allowed -ne $true -or $gate.arm -cne 'local4' -or $gate.run_id -cne 'pad-local4-20261026-host' -or $gate.max_n -ne 100 -or $gate.hard_seconds -ne 4500 -or $gate.no_new_n_seconds -ne 4380){throw 'Separate exact C5 root host gate required'}
$pinPath=Join-Path $package 'SOURCE-PINS.json'
if((Hash $pinPath) -cne $gate.source_pins_sha256){throw 'C5 source pins changed'}
foreach($p in (Get-Content $pinPath -Raw|ConvertFrom-Json).sources){if((Hash (Join-Path $workspace $p.path)) -cne $p.sha256){throw "Changed source $($p.path)"}}
if((Hash (Join-Path $c4 'SOURCE-PINS.json')) -cne '2f9f3ec2b96160d075820b83ac4570f75969834915d4f6543f37ce52d00107fe'){throw 'C4 frozen source manifest changed'}
$budget=Budget
if(@(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0){throw 'Game already running'}
$media=[IO.DriveInfo]::new('E:')
if($media.DriveType -ne [IO.DriveType]::CDRom -or -not $media.IsReady -or $media.VolumeLabel -cne 'CIV_CTP'){throw 'Ordinary CD unavailable; no bypass or Retry'}
if(Test-Path -LiteralPath $hostDir){throw 'Unique own host directory already exists; no retry'}
$candidate=Join-Path $workspace 'PROEVEN/pad-lokaal-onbekend/20261023T155300-build/U30-40.prepared.dll'
$candidateHash='acfeec096ea39e1ff38435214769f4d24074e640b856e08d1c82cc09ea7a4984'
if((Hash $candidate) -cne $candidateHash){throw 'Candidate mismatch'}
$manifest=Get-Content (Join-Path $workspace 'PROEVEN/pad-lokaal-onbekend/20261023T155300-build/candidate-manifest.json') -Raw|ConvertFrom-Json
$plan=Get-Content (Join-Path $c4 'HOST-PLAN.json') -Raw|ConvertFrom-Json
if(@($manifest.release_pins).Count -ne 19 -or @($plan.effective_protected118).Count -ne 118 -or $plan.overlap16 -ne 16 -or @($plan.before29).Count -ne 29){throw 'Exact19/118/16/29 required'}
foreach($row in @($manifest.release_pins)+@($plan.effective_protected118)){if((Hash (Join-Path $workspace $row.path)) -cne $row.sha256){throw "Current effective config/protected mismatch $($row.path)"}}
$saveRoot=Join-Path $workspace 'CTP-proef/ctp_program/ctp/save'
$profile='CTP-proef/ctp_program/ctp/userprofile.txt'
$all=@{};$savePaths=@(Get-ChildItem -LiteralPath $saveRoot -Recurse -File|ForEach-Object {$_.FullName.Substring($workspace.Length+1).Replace('\','/')})
foreach($path in @($manifest.release_pins.path)+@($plan.effective_protected118.path)+@($plan.before29.path)+$savePaths+@($profile)){$all[$path]=$true}
$rows=@(foreach($path in @($all.Keys|Sort-Object)){$full=Join-Path $workspace $path;if(-not(Test-Path -LiteralPath $full -PathType Leaf)){throw "Missing beforefile $path"};[ordered]@{path=$path;existed=$true;size=(Get-Item -LiteralPath $full).Length;sha256=(Hash $full)}})
$alias='CTP-proef/ctp_program/ctp/save/games/Julius/000-PAD-LOCAL4-20261026-START-T0'
$save='CTP-proef/ctp_program/ctp/save/games/Julius/QUOTA-START-T0'
$saveHash='8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26'
if((Test-Path -LiteralPath $alias) -or (Hash $save) -cne $saveHash){throw 'Unique exact start alias/source required'}
New-Item -ItemType Directory -Path $hostDir|Out-Null
NewJson (Join-Path $hostDir 'before.json') ([ordered]@{run_id=$gate.run_id;at_utc=[DateTime]::UtcNow.ToString('o');files=$rows;save_paths=$savePaths;before29_paths=@($plan.before29.path);config19=$manifest.release_pins;effective118=$plan.effective_protected118;alias=$alias;alias_sha256=$saveHash})
foreach($row in $rows){$dst=Join-Path (Join-Path $hostDir 'backup') $row.path;New-Item -ItemType Directory -Path (Split-Path $dst) -Force|Out-Null;[IO.File]::Copy((Join-Path $workspace $row.path),$dst,$false);if((Hash $dst) -cne $row.sha256 -or (Hash (Join-Path $workspace $row.path)) -cne $row.sha256){throw 'Fresh backup/source mismatch'}}
$nowSave=@(Get-ChildItem -LiteralPath $saveRoot -Recurse -File|ForEach-Object {$_.FullName.Substring($workspace.Length+1).Replace('\','/')}|Sort-Object)
if(($nowSave -join "`n") -cne (($savePaths|Sort-Object) -join "`n")){throw 'Save inventory changed during backup'}
$budget=Budget
if(@(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0){throw 'Game appeared before installation'}
foreach($row in $rows){if((Hash (Join-Path $workspace $row.path)) -cne $row.sha256){throw 'Beforefile changed before installation'}}
NewJson (Join-Path $hostDir 'backup-verified.json') @{before_sha256=(Hash (Join-Path $hostDir 'before.json'));files=$rows.Count;budget=$budget;at_utc=[DateTime]::UtcNow.ToString('o')}
[IO.File]::Copy((Join-Path $workspace $save),(Join-Path $workspace $alias),$false)
$dll=Join-Path $workspace 'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll'
[IO.File]::Copy($candidate,$dll,$true)
if((Hash $dll) -cne $candidateHash -or (Hash $alias) -cne $saveHash){throw 'Installed DLL/alias mismatch'}
foreach($row in @($manifest.release_pins)+@($plan.effective_protected118)){if($row.path -eq 'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll'){continue};if((Hash $row.path) -cne $row.sha256){throw 'Non-DLL effective pin changed'}}
NewJson (Join-Path $hostDir 'install.json') @{candidate_sha256=$candidateHash;alias=$alias;alias_sha256=$saveHash;before_sha256=(Hash (Join-Path $hostDir 'before.json'));only_dll_config_changed=$true}
$budget=Budget
$media=[IO.DriveInfo]::new('E:')
if($media.DriveType -ne [IO.DriveType]::CDRom -or -not $media.IsReady -or $media.VolumeLabel -cne 'CIV_CTP' -or @(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0){throw 'Media/count0 changed before Start'}
& ./PROEVEN/Bedien-CTP.ps1 -Action Start
if(-not $?){throw 'Start failed; no retry, root inspect/normalclose/restore'}
$processes=@(Get-Process civctp);if($processes.Count -ne 1){throw 'Exact one process required'};$probe=$processes[0]
$exe=Join-Path $workspace 'CTP-proef/ctp_program/ctp/civctp.exe'
$start=$probe.StartTime.ToUniversalTime();$filetime=$start.ToFileTimeUtc();$ms=([DateTimeOffset]$start).ToUnixTimeMilliseconds()
if($probe.Path -cne $exe){throw 'Wrong executable'}
while($probe.MainWindowHandle -eq 0){if(([DateTime]::UtcNow-$start).TotalSeconds -ge 15){throw 'No initial window; root inspect; no input'};Start-Sleep -Milliseconds 250;$probe.Refresh()}
$window=$probe.MainWindowHandle.ToInt64()
NewJson (Join-Path $hostDir 'start.json') ([ordered]@{pid=$probe.Id;path=$exe;start_utc=$start.ToString('o');creation_utc_ms=$ms;creation_filetime=$filetime;window=$window;max_n=100;n_consumed=0;run_id=$gate.run_id})
(Get-Item -LiteralPath (Join-Path $hostDir 'start.json')).IsReadOnly=$true
NewJson (Join-Path $hostDir 'window.json') @{pid=$probe.Id;creation_utc_ms=$ms;creation_filetime=$filetime;window=$window;run_id=$gate.run_id}
NewJson (Join-Path $hostDir 'start-binding.json') @{start_sha256=(Hash (Join-Path $hostDir 'start.json'));window_sha256=(Hash (Join-Path $hostDir 'window.json'));before_sha256=(Hash (Join-Path $hostDir 'before.json'));n_consumed=0}
# Capture only, no automatic menu/load/key. Clock remains original process start.
foreach($target in @(45,90,135,175)){
 while(([DateTime]::UtcNow-$start).TotalSeconds -lt $target){Start-Sleep -Milliseconds 400}
 $budget=Budget
 $probe.Refresh();if($probe.HasExited -or $probe.Path -cne $exe -or $probe.StartTime.ToUniversalTime().ToFileTimeUtc() -ne $filetime -or $probe.MainWindowHandle.ToInt64() -ne $window){throw 'Own process/window changed'}
 if(([DateTime]::UtcNow-$start).TotalSeconds -ge 180){throw 'Intro deadline; no blind input'}
 & ./PROEVEN/Bedien-CTP.ps1 -Action Capture -CaptureWaitForForeground -CaptureWaitTimeoutMs 3000 -ExpectedProcessId $probe.Id -ExpectedCreationUtcMs $ms -ExpectedWindowHandle $window > (Join-Path $hostDir "intro-$target.log")
 if(-not $?){throw 'Intro capture failed'}
 [IO.File]::Copy((Join-Path $workspace 'PROEVEN/automatisering/ctp-window.png'),(Join-Path $hostDir "intro-$target.png"),$false)
 if(([DateTime]::UtcNow-$start).TotalSeconds -ge 180){throw 'Late intro capture; no input'}
}
Write-Output 'Intro complete; root inspect before normal load (<=300s), T0 and separate C4 gates. No automatic input.'
