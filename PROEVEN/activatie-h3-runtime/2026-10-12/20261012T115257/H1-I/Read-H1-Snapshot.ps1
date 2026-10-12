param([Parameter(Mandatory=$true)][ValidateSet('A','B')][string]$SnapshotLabel)
$ErrorActionPreference='Stop'
$armDir=$PSScriptRoot
$started=Get-Content -LiteralPath (Join-Path $armDir 'start-record.json') -Raw -Encoding utf8|ConvertFrom-Json
$reader='C:\GIT\ctp\PROEVEN\ai-uitlezen\Lees-Onderzoeksactivatie.py'
if((Get-FileHash -LiteralPath $reader -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'ff43655e52ddc2a9c593ff64ef564c6cda54a2c11e04cc364cfbd5fface69365'){throw 'Frozen observer changed; no read.'}
$aPath='C:\GIT\ctp\PROEVEN\ai-uitlezen\activatie-h3-runtime-20261012-115257-h1-A.json'
$bPath='C:\GIT\ctp\PROEVEN\ai-uitlezen\activatie-h3-runtime-20261012-115257-h1-B.json'
$output=$aPath;$turn=0
if($SnapshotLabel -eq 'B'){$output=$bPath;$turn=1;if(-not (Test-Path -LiteralPath $aPath)){throw 'Own A source missing; no B.'};$aAcceptance=Get-Content -LiteralPath (Join-Path $armDir 'A-archive.json') -Raw -Encoding utf8|ConvertFrom-Json;if($aAcceptance.instance_verified -ne $true){throw 'Own A instance rejected/unverified; no B.'}}
if(Test-Path -LiteralPath $output){throw 'Snapshot output exists; no overwrite/retry.'}
& powershell.exe -NoProfile -File (Join-Path $armDir 'Guard-H1-T0.ps1') -Purpose Read 2>&1|Set-Content -LiteralPath (Join-Path $armDir "$SnapshotLabel-guard.txt") -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Original binding/deadline/budget guard failed; no reader.'}
# A only after proven loaded4000BC; B only after proven sole n/pass→3950BC.
# Procedure evidence is reviewed separately; CLI labels do not prove these facts.
$readerArgs=@($reader,'--pid',[string]$started.pid,'--variant','H1-I','--run-id','h1-20261012-115257','--snapshot-label',$SnapshotLabel,'--turn',[string]$turn,'--pass-label','T0-to-T1','--output',$output)
if($SnapshotLabel -eq 'B'){$readerArgs+=@('--before',$aPath)}
[ordered]@{at=(Get-Date).ToString('o');executable='C:\Users\Stephan\AppData\Local\Programs\Python\Python312\python.exe';argv=$readerArgs;labels_are_external_procedure_labels=$true}|ConvertTo-Json -Depth 4|Set-Content -LiteralPath (Join-Path $armDir "$SnapshotLabel-command.json") -Encoding utf8
$readerCode=$null;$readerError=$null;$instanceVerified=$false;$instanceCreationMs=$null
try{
    & 'C:\Users\Stephan\AppData\Local\Programs\Python\Python312\python.exe' @readerArgs 2>&1|Set-Content -LiteralPath (Join-Path $armDir "$SnapshotLabel-trace.txt") -Encoding utf8
    $readerCode=$LASTEXITCODE
    if($readerCode -eq 0){
        $snapshot=Get-Content -LiteralPath $output -Raw -Encoding utf8|ConvertFrom-Json
        $instanceCreationMs=([DateTimeOffset][DateTime]::FromFileTimeUtc([long]$snapshot.instance.creationtime_filetime)).ToUnixTimeMilliseconds()
        if($started.exe -cne 'C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe' -or $snapshot.instance.pid -ne $started.pid -or $instanceCreationMs -ne $started.creation_utc_ms -or $snapshot.instance.executable -cne $started.exe){throw 'Snapshot instance differs from original PID/creation/executable; procedure rejected, no n/B.'}
        $instanceVerified=$true
    }
}catch{$readerError=$_.Exception.Message;throw}
finally{
    if(Test-Path -LiteralPath $output){
        $archive=Join-Path $armDir "$SnapshotLabel.json"
        if(Test-Path -LiteralPath $archive){throw 'Archive exists; no overwrite.'}
        Copy-Item -LiteralPath $output -Destination $archive
        $sourceHash=(Get-FileHash -LiteralPath $output -Algorithm SHA256).Hash.ToLowerInvariant();$archiveHash=(Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant()
        [ordered]@{copied_at=(Get-Date).ToString('o');source=$output;archive=$archive;source_sha256=$sourceHash;archive_sha256=$archiveHash;byte_match=($sourceHash -eq $archiveHash);reader_exit_code=$readerCode;reader_error=$readerError;instance_verified=$instanceVerified;instance_creation_utc_ms=$instanceCreationMs;procedure_accepted=($readerCode -eq 0 -and $instanceVerified -and $null -eq $readerError)}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $armDir "$SnapshotLabel-archive.json") -Encoding utf8
        if($sourceHash -ne $archiveHash){throw 'Snapshot archive mismatch.'}
    }
}
if($readerCode -ne 0){throw 'Reader rejected/failed; no pass/B acceptance search.'}
