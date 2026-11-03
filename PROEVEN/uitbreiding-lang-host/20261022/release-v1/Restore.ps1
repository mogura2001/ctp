$ErrorActionPreference='Stop'
$workspace='C:/GIT/ctp'
Set-Location -LiteralPath $workspace
$armDir=$PSScriptRoot
if(@(Get-Process civctp -ErrorAction SilentlyContinue).Count -ne 0){throw 'Game running; no restore'}
$gate=Get-Content "$armDir/gate.json" -Raw|ConvertFrom-Json
$gate.allowed=$false
$gate|ConvertTo-Json -Depth 12|Set-Content "$armDir/gate.json"
$before=Get-Content "$armDir/before.json" -Raw|ConvertFrom-Json
$dll='CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll'
$auto='CTP-proef/ctp_program/ctp/save/games/Julius/AUTOSAVE-Julius'
$alias='CTP-proef/ctp_program/ctp/save/games/Julius/000-U30-40-START-T0'
$archive='CTP-proef/ctp_program/ctp/save/games/Julius/U30-LANG-20261022-release-v1-AUTOSAVE'
$sha={param($path) (Get-FileHash -LiteralPath $path).Hash.ToLower()}
foreach($row in @($before.protected)+@($before.extra_preserved_files)){
 if((& $sha (Join-Path "$armDir/backup" $row.path)) -ne $row.sha256){throw "Changed backup $($row.path)"}
 if($row.path -notin @($dll,$auto) -and (& $sha $row.path) -ne $row.sha256){throw "Unexpected user change; not overwriting $($row.path)"}
}
$dllRow=$before.protected|Where-Object path -eq $dll
$autoRow=$before.protected|Where-Object path -eq $auto
if(($null -eq $dllRow) -or ($null -eq $autoRow)){throw 'Missing baseline'}
$dllNow=& $sha $dll
if($dllNow -notin @($dllRow.sha256,$gate.candidate_sha256)){throw 'Unexpected DLL change; not overwriting'}
if(Test-Path -LiteralPath $alias){if((& $sha $alias) -ne '8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26'){throw 'Unexpected alias change'}}
$autoNow=& $sha $auto
$changed=$autoNow -ne $autoRow.sha256
if($changed){
 if(Test-Path -LiteralPath $archive){throw 'Archive destination exists; not overwriting'}
 Copy-Item -LiteralPath $auto -Destination "$armDir/AUTOSAVE-after"
 Copy-Item -LiteralPath $auto -Destination $archive
 if((& $sha "$armDir/AUTOSAVE-after") -ne $autoNow -or (& $sha $archive) -ne $autoNow){throw 'Archive hash mismatch'}
}
foreach($path in @($dll,$auto)){Copy-Item -LiteralPath (Join-Path "$armDir/backup" $path) -Destination $path}
if(Test-Path -LiteralPath $alias){Remove-Item -LiteralPath $alias}
foreach($row in @($before.protected)+@($before.extra_preserved_files)){if((& $sha $row.path) -ne $row.sha256){throw "Restore mismatch $($row.path)"}}
@{state='RESTORED';at_utc=[DateTime]::UtcNow.ToString('o');restored_hashes=@($before.protected).Count;existing_archives_preserved=@($before.extra_preserved_files).Count;game_count_before_restore=0;default_autosave_changed=$changed;autosave_after_sha256=$autoNow;autosave_archive=$archive;autosave_exact_turn_proven=$false;alias_removed=(-not(Test-Path -LiteralPath $alias));gate_allowed=$false;release_dll_sha256=(& $sha $dll)}|ConvertTo-Json|Set-Content "$armDir/restore.json"
