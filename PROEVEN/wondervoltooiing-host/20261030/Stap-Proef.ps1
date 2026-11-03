param(
 [Parameter(Mandatory=$true)][ValidateSet('control','candidate')][string]$Arm,
 [Parameter(Mandatory=$true)][ValidatePattern('^[A-Za-z0-9-]+$')][string]$Name,
 [ValidateSet('Capture','Click','Key','Complete')][string]$Action='Capture',
 [int]$X,[int]$Y,[int]$FromX,[int]$FromY,[string]$Keys,
 [ValidateRange(1,21)][int]$NIndex,
 [string]$BeforeSnapshot
)
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$folder=Join-Path $PSScriptRoot $Arm
$python='C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe'
$guard=Join-Path $PSScriptRoot 'guard.py'
& $python $guard --mode pins
if($LASTEXITCODE -ne 0){throw 'C0 source pins rejected'}
if($Arm -ne 'candidate'){throw 'Completion proof uses only candidate30000'}
if($Action -in @('Key','Complete') -and -not $PSBoundParameters.ContainsKey('NIndex')){throw 'Explicit NIndex required'}
if($Action -eq 'Key' -and -not $BeforeSnapshot){throw 'Explicit checked BeforeSnapshot required'}
$s=Get-Content (Join-Path $folder 'start.json') -Raw|ConvertFrom-Json
$g=Get-Process -Id $s.pid -ErrorAction Stop
if($g.Path -ne $s.path -or $g.StartTime.ToUniversalTime().ToFileTimeUtc() -ne $s.creation_filetime){throw 'Process identity changed'}
$elapsed=([DateTime]::UtcNow-$g.StartTime.ToUniversalTime()).TotalSeconds
if($elapsed -ge 900 -or ($Action -in @('Key','Click') -and $elapsed -ge 780)){throw 'Proof deadline; close normally'}
if(-not $s.window){
 if($g.MainWindowHandle -eq 0){throw 'No main window; wait without input'}
 $s | Add-Member -NotePropertyName window -NotePropertyValue $g.MainWindowHandle.ToInt64() -Force
 $s | ConvertTo-Json | Set-Content (Join-Path $folder 'start.json') -Encoding UTF8
}
$log=Join-Path $folder ($Name+'.log')
$png=Join-Path $folder ($Name+'.png')
$actionLog=Join-Path $folder ($Name+'-action.log')
if((Test-Path -LiteralPath $log) -or (Test-Path -LiteralPath $png) -or (Test-Path -LiteralPath $actionLog) -or (Test-Path -LiteralPath (Join-Path $folder ($Name+'-pre-focus.log'))) -or (Test-Path -LiteralPath (Join-Path $folder ($Name+'-reader.log')))){throw 'Step name already used; inspect prior outcome'}
$helper=Join-Path $root 'PROEVEN/Bedien-CTP.ps1'
function Read-AfterN {
 if(([DateTime]::UtcNow-$g.StartTime.ToUniversalTime()).TotalSeconds -ge 900){throw 'Host deadline; close normally, keep pending N'}
 $after=Join-Path $root ('PROEVEN/wondergewicht/20261030/completion-'+$Name+'-after-N'+$NIndex.ToString('00')+'.json')
 $readerLog=Join-Path $folder ($Name+'-reader.log')
 if((Test-Path -LiteralPath $after) -or (Test-Path -LiteralPath $readerLog)){throw 'After snapshot name used; never overwrite'}
 & $python (Join-Path $root 'PROEVEN/wondergewicht/20261030/Lees-Wondergewicht.py') --pid $s.pid --creation-filetime $s.creation_filetime --wonder-arm candidate --variant B2a-N30-TECHNICAL --run-id WONDERCOMPLETE-20261030 --snapshot-label ('AFTER-N'+$NIndex) --turn (26+$NIndex) --pass-label quiet --manifest (Join-Path $root 'PROEVEN/wondergewicht/20261030/participants.json') --output $after > $readerLog
 if($LASTEXITCODE -ne 0){throw 'After-N reader rejected; pending consumed N, never resend'}
 & $python $guard --mode complete --start (Join-Path $folder 'start.json') --snapshot $after --index $NIndex
 if($LASTEXITCODE -ne 0){throw 'After-N gate rejected; pending consumed N, never resend'}
 Write-Output $after
}
if($Action -eq 'Click'){
 & $helper -Action Click -X $X -Y $Y -FromX $FromX -FromY $FromY > $actionLog
 if(-not $?){throw 'Click outcome unknown; do not resend'}
} elseif($Action -eq 'Key'){
 if($Keys -ne 'n'){throw 'This proof allows only the registered n'}
 & $python (Join-Path $root 'PROEVEN/Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d
 if($LASTEXITCODE -notin @(0,25)){throw 'Budget unknown/stop; no input sent'}
 & $helper -Action Capture -CaptureWaitForForeground -CaptureWaitTimeoutMs 3000 -ExpectedProcessId $s.pid -ExpectedCreationUtcMs $s.creation_utc_ms -ExpectedWindowHandle $s.window > (Join-Path $folder ($Name+'-pre-focus.log'))
 if(-not $?){throw 'Before-N foreground binding rejected; no input sent'}
 & $python $guard --mode consume --start (Join-Path $folder 'start.json') --snapshot $BeforeSnapshot --index $NIndex
 if($LASTEXITCODE -ne 0){throw 'Before-N gate rejected; no input sent'}
 $g=Get-Process -Id $s.pid -ErrorAction Stop
 if($g.Path -ne $s.path -or $g.StartTime.ToUniversalTime().ToFileTimeUtc() -ne $s.creation_filetime -or ([DateTime]::UtcNow-$g.StartTime.ToUniversalTime()).TotalSeconds -ge 780){throw 'Identity/deadline changed; N consumed but not sent, never resend'}
 & $helper -Action Key -Keys n > $actionLog
 if(-not $?){throw 'N outcome unknown; never resend'}
 Read-AfterN
} elseif($Action -eq 'Complete'){
 # Read-only recovery for an already consumed N; this branch sends no key.
 if(-not(Test-Path -LiteralPath (Join-Path $folder ('N'+$NIndex.ToString('00')+'-consumed.json')))){throw 'No consumed N to complete'}
 if(Test-Path -LiteralPath (Join-Path $folder ('N'+$NIndex.ToString('00')+'-completed.json'))){throw 'N already completed; no resample needed'}
 Read-AfterN
}
& $helper -Action Capture -CaptureWaitForForeground -CaptureWaitTimeoutMs 3000 -ExpectedProcessId $s.pid -ExpectedCreationUtcMs $s.creation_utc_ms -ExpectedWindowHandle $s.window > $log
if(-not $?){throw 'Capture failed; do not reuse coordinates'}
Copy-Item -LiteralPath (Join-Path $root 'PROEVEN/automatisering/ctp-window.png') -Destination $png
Write-Output $png
