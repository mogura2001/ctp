$ErrorActionPreference='Stop'
$workspace='C:\GIT\ctp';Set-Location -LiteralPath $workspace
$package=$PSScriptRoot;$c4=Join-Path $workspace 'PROEVEN/pad-lokaal-onbekend/20261026c-host';$hostDir=Join-Path $c4 'host'
function Hash($p){(Get-FileHash -LiteralPath $p).Hash.ToLowerInvariant()}
function NewJson($p,$value){$s=[IO.File]::Open($p,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None);try{$b=[Text.Encoding]::UTF8.GetBytes(($value|ConvertTo-Json -Depth 30));$s.Write($b,0,$b.Length);$s.Flush()}finally{$s.Dispose()}}
if(@(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0){throw 'Game running; no restore'}
$gate=Get-Content (Join-Path $package 'ROOT-HOST.json') -Raw|ConvertFrom-Json
if($gate.restore_allowed -ne $true -or $gate.arm -cne 'local4' -or $gate.run_id -cne 'pad-local4-20261026c-host' -or (Hash (Join-Path $package 'SOURCE-PINS.json')) -cne $gate.source_pins_sha256){throw 'Exact own C5 restore gate required'}
foreach($p in (Get-Content (Join-Path $package 'SOURCE-PINS.json') -Raw|ConvertFrom-Json).sources){if((Hash (Join-Path $workspace $p.path)) -cne $p.sha256){throw 'Restore source changed'}}
foreach($p in @((Join-Path $c4 'local4/ROOT-READER.json'),(Join-Path $c4 'ROOT-CONTROL.json'))){$g=Get-Content $p -Raw|ConvertFrom-Json;if($g.allowed -ne $false -or ($g.PSObject.Properties.Name -contains 'control_allowed' -and $g.control_allowed -ne $false)){throw 'Close C4 input/read gates before restore'}}
if($gate.allowed -ne $false -or $gate.install_allowed -ne $false -or $gate.start_allowed -ne $false -or $gate.close_allowed -ne $false){throw 'Close C5 start/close gates before restore'}
if(Test-Path -LiteralPath (Join-Path $hostDir 'restore-attempt.json')){throw 'Restore already attempted; inspect checkpoint, no retry'}
$beforePath=Join-Path $hostDir 'before.json';$before=Get-Content $beforePath -Raw|ConvertFrom-Json
$verified=Get-Content (Join-Path $hostDir 'backup-verified.json') -Raw|ConvertFrom-Json
if($before.run_id -cne $gate.run_id -or (Hash $beforePath) -cne $verified.before_sha256){throw 'Beforemanifest binding changed'}
if(Test-Path -LiteralPath (Join-Path $hostDir 'start.json')){
 $binding=Get-Content (Join-Path $hostDir 'start-binding.json') -Raw|ConvertFrom-Json;$start=Get-Content (Join-Path $hostDir 'start.json') -Raw|ConvertFrom-Json
 $close=Get-Content (Join-Path $hostDir 'close.json') -Raw|ConvertFrom-Json
 if((Hash (Join-Path $hostDir 'start.json')) -cne $binding.start_sha256 -or $close.start_sha256 -cne $binding.start_sha256 -or $close.exited -ne $true -or $close.all_civctp_count -ne 0 -or $close.pid -ne $start.pid -or $close.creation_filetime -ne $start.creation_filetime){throw 'Exact normal own exit proof required'}
}
$dll='CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll';$auto='CTP-proef/ctp_program/ctp/save/games/Julius/AUTOSAVE-Julius';$profile='CTP-proef/ctp_program/ctp/userprofile.txt'
$release='eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890';$candidate='acfeec096ea39e1ff38435214769f4d24074e640b856e08d1c82cc09ea7a4984'
$beforeByPath=@{};foreach($row in $before.files){$beforeByPath[$row.path]=$row;if((Hash (Join-Path (Join-Path $hostDir 'backup') $row.path)) -cne $row.sha256){throw 'Changed beforebackup'};if($row.path -notin @($dll,$auto,$profile) -and (Hash $row.path) -cne $row.sha256){throw "Unexpected user change; preserve and stop $($row.path)"}}
if($beforeByPath[$dll].sha256 -cne $release -or (Hash $dll) -notin @($release,$candidate)){throw 'Unexpected DLL; no overwrite'}
if((Hash $profile) -cne $beforeByPath[$profile].sha256 -and (Hash $profile) -cne $gate.expected_after_profile_sha256){throw 'Changed profile requires exact root afterhash; preserve'}
if(Test-Path -LiteralPath $before.alias){if((Hash $before.alias) -cne $before.alias_sha256){throw 'Unexpected alias changed; preserve'}}
$newSaves=@($gate.preserve_new_saves);foreach($row in $newSaves){if((Hash $row.path) -cne $row.sha256 -or $beforeByPath.ContainsKey($row.path)){throw 'New named save preservation mismatch'}}
$saveRoot=Join-Path $workspace 'CTP-proef/ctp_program/ctp/save'
$current=@(Get-ChildItem -LiteralPath $saveRoot -Recurse -File|ForEach-Object {$_.FullName.Substring($workspace.Length+1).Replace('\','/')})
foreach($path in $current){if($path -notin @($before.save_paths)+@($before.alias)+@($newSaves.path)){throw "Unexpected new save/archive; preserve and root inspect $path"}}
$archiveA='CTP-proef/ctp_program/ctp/save/games/Julius/PAD-LOCAL4-20261026C-AUTOSAVE-A';$archiveB='CTP-proef/ctp_program/ctp/save/games/Julius/PAD-LOCAL4-20261026C-AUTOSAVE-B';$packageAuto=Join-Path $hostDir 'AUTOSAVE-after'
foreach($p in @($archiveA,$archiveB,$packageAuto)){if(Test-Path -LiteralPath $p){throw 'Fresh unique archive destination required'}}
if(@(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0){throw 'Game appeared before restore'}
NewJson (Join-Path $hostDir 'restore-attempt.json') @{before_sha256=(Hash $beforePath);at_utc=[DateTime]::UtcNow.ToString('o');count0=$true}
$autoHash=Hash $auto
foreach($p in @($archiveA,$archiveB,$packageAuto)){$destination=if([IO.Path]::IsPathRooted($p)){$p}else{Join-Path $workspace $p};[IO.File]::Copy((Join-Path $workspace $auto),$destination,$false);if((Hash $destination) -cne $autoHash){throw 'Archive hash mismatch; no restore'}}
foreach($row in $before.files){if(@(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0){throw 'Game appeared; no further restore'};if((Hash $row.path) -cne $row.sha256){[IO.File]::Copy((Join-Path (Join-Path $hostDir 'backup') $row.path),(Join-Path $workspace $row.path),$true)}}
if(Test-Path -LiteralPath $before.alias){if((Hash $before.alias) -cne $before.alias_sha256){throw 'Alias changed during restore'};Remove-Item -LiteralPath $before.alias}
foreach($row in @($before.files)+@($before.config19)+@($before.effective118)){if((Hash $row.path) -cne $row.sha256){throw 'Restore19/118/allbefore mismatch'}}
$expected=@($before.save_paths)+@($newSaves.path)+@($archiveA,$archiveB)
$actual=@(Get-ChildItem -LiteralPath $saveRoot -Recurse -File|ForEach-Object {$_.FullName.Substring($workspace.Length+1).Replace('\','/')}|Sort-Object)
if(($actual -join "`n") -cne (($expected|Sort-Object -Unique) -join "`n")){throw 'Complete restored save inventory mismatch'}
foreach($row in $newSaves){if((Hash $row.path) -cne $row.sha256){throw 'Named endsave changed'}}
$gate.restore_allowed=$false;$gate|ConvertTo-Json -Depth 30|Set-Content -LiteralPath (Join-Path $package 'ROOT-HOST.json') -Encoding utf8
NewJson (Join-Path $hostDir 'restore.json') @{state='RESTORED';all_before_files=$before.files.Count;config19=19;effective118=118;before29=29;saves_before=@($before.save_paths).Count;additional_named_preserved=$newSaves.Count;autosave_sha256=$autoHash;autosave_exact_turn_proven=$false;double_archives=@($archiveA,$archiveB);packagecopy=$packageAuto;alias_removed=(-not(Test-Path -LiteralPath $before.alias));release_sha256=(Hash $dll);all_gates_false=$true;all_civctp_count=@(Get-Process civctp -ErrorAction SilentlyContinue).Count;pc_stays_on=$true;at_utc=[DateTime]::UtcNow.ToString('o')}
