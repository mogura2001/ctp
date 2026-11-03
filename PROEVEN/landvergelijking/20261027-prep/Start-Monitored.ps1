param([Parameter(Mandatory=$true)][ValidateSet('release-v1','U30-40')][string]$Arm)
$ErrorActionPreference='Stop'
$workspace='C:\GIT\ctp';Set-Location -LiteralPath $workspace
$package=$PSScriptRoot;$c4=Join-Path $workspace 'PROEVEN/landvergelijking/20261027';$armDir=Join-Path $c4 $Arm;$hostDir=Join-Path $armDir 'host'
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
$gate=Get-Content (Join-Path (Join-Path $package $Arm) 'ROOT-HOST.json') -Raw|ConvertFrom-Json
if($gate.allowed -ne $true -or $gate.install_allowed -ne $true -or $gate.start_allowed -ne $true -or $gate.arm -cne $Arm -or $gate.run_id -cne ('land-20261027-'+$Arm) -or $gate.max_n -ne 100 -or $gate.hard_seconds -ne 4500 -or $gate.no_new_n_seconds -ne 4380){throw 'Separate exact C5 root host gate required'}
$pinPath=Join-Path $package 'SOURCE-PINS.json'
if((Hash $pinPath) -cne $gate.source_pins_sha256){throw 'C5 source pins changed'}
foreach($p in (Get-Content $pinPath -Raw|ConvertFrom-Json).sources){if((Hash (Join-Path $workspace $p.path)) -cne $p.sha256){throw "Changed source $($p.path)"}}
if((Hash (Join-Path $c4 'SOURCE-PINS.json')) -cne $gate.c4_source_pins_sha256){throw 'C4 frozen source manifest changed'}
$budget=Budget
if(@(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0){throw 'Game already running'}
$media=[IO.DriveInfo]::new('E:')
if($media.DriveType -ne [IO.DriveType]::CDRom -or -not $media.IsReady -or $media.VolumeLabel -cne 'CCTP'){throw 'Ordinary CD unavailable; no bypass or Retry'}
if(Test-Path -LiteralPath $hostDir){throw 'Unique own host directory already exists; no retry'}
$candidate=if($Arm -ceq 'U30-40'){Join-Path $workspace 'VERSIES/uitbreiding-2026-10-22-T100/files/CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll'}else{Join-Path $workspace 'PROEVEN/selectie-pad-diagnose/20261020T192500/reader/candidate/baseline/CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll'}
$candidateHash=if($Arm -ceq 'U30-40'){'df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e'}else{'eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'}
if((Hash $candidate) -cne $candidateHash){throw 'Candidate mismatch'}
$manifest=Get-Content (Join-Path $workspace 'VERSIES/uitbreiding-2026-10-22-T100/manifest.json') -Raw|ConvertFrom-Json
$plan=Get-Content (Join-Path $c4 'HOST-PLAN.json') -Raw|ConvertFrom-Json
$releasePins=$plan.config19
if((Hash (Join-Path $workspace 'VERSIES/uitbreiding-2026-10-22-T100/manifest.json')) -cne 'c665c92f19e37abe49d627a86070306b93519a7088399e90763a2a102a36e950' -or @($manifest.files).Count -ne 19){throw 'Exact tested package19 required'}
foreach($row in $manifest.files){if((Hash (Join-Path $workspace ('VERSIES/uitbreiding-2026-10-22-T100/files/'+$row.path))) -cne $row.sha256){throw 'Package file mismatch'};if($row.path -cne 'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll' -and (Hash (Join-Path $workspace $row.path)) -cne $row.sha256){throw 'Non-DLL package file differs'}}
if(@($releasePins).Count -ne 19 -or @($plan.effective_protected118).Count -ne 118 -or $plan.overlap16 -ne 16 -or @($plan.before29).Count -ne 29){throw 'Exact19/118/16/29 required'}
foreach($row in @($releasePins)+@($plan.effective_protected118)){if((Hash (Join-Path $workspace $row.path)) -cne $row.sha256){throw "Current effective config/protected mismatch $($row.path)"}}
$saveRoot=Join-Path $workspace 'CTP-proef/ctp_program/ctp/save'
$profile='CTP-proef/ctp_program/ctp/userprofile.txt'
$all=@{};$savePaths=@(Get-ChildItem -LiteralPath $saveRoot -Recurse -File|ForEach-Object {$_.FullName.Substring($workspace.Length+1).Replace('\','/')})
foreach($path in @($releasePins.path)+@($plan.effective_protected118.path)+@($plan.before29.path)+$savePaths+@($profile)){$all[$path]=$true}
$rows=@(foreach($path in @($all.Keys|Sort-Object)){$full=Join-Path $workspace $path;if(-not(Test-Path -LiteralPath $full -PathType Leaf)){throw "Missing beforefile $path"};[ordered]@{path=$path;existed=$true;size=(Get-Item -LiteralPath $full).Length;sha256=(Hash $full)}})
$alias=if($Arm -ceq 'U30-40'){'CTP-proef/ctp_program/ctp/save/games/Julius/000-LAND-R1-U30-T0'}else{'CTP-proef/ctp_program/ctp/save/games/Julius/000-LAND-R1-CONTROLE-T0'}
$save='PROEVEN/landbenchmark/20261027/UITBREIDING-LAND-T0.original'
$saveHash='a670867460bae5d8d9196856d5ca88163b0eff951e9a9db42a05b83ee38d2301'
if((Test-Path -LiteralPath $alias) -or (Hash $save) -cne $saveHash){throw 'Unique exact start alias/source required'}
New-Item -ItemType Directory -Path $hostDir|Out-Null
NewJson (Join-Path $hostDir 'before.json') ([ordered]@{run_id=$gate.run_id;at_utc=[DateTime]::UtcNow.ToString('o');files=$rows;save_paths=$savePaths;before29_paths=@($plan.before29.path);config19=$releasePins;effective118=$plan.effective_protected118;alias=$alias;alias_sha256=$saveHash})
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
foreach($row in @($releasePins)+@($plan.effective_protected118)){if($row.path -eq 'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll'){continue};if((Hash $row.path) -cne $row.sha256){throw 'Non-DLL effective pin changed'}}
NewJson (Join-Path $hostDir 'install.json') @{candidate_sha256=$candidateHash;alias=$alias;alias_sha256=$saveHash;before_sha256=(Hash (Join-Path $hostDir 'before.json'));only_dll_config_changed=$true}
$budget=Budget
$media=[IO.DriveInfo]::new('E:')
if($media.DriveType -ne [IO.DriveType]::CDRom -or -not $media.IsReady -or $media.VolumeLabel -cne 'CCTP' -or @(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0){throw 'Media/count0 changed before Start'}
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
Write-Output 'Immutable start/window binding ready; root Capture/menu before240s and load/T0 before360s from start_utc. No automatic input; hard4500s/no-new4380s remain.'
