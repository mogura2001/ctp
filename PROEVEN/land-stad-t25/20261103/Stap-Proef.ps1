param(
 [Parameter(Mandatory=$true)][ValidateSet('control','candidate')][string]$Arm,
 [Parameter(Mandatory=$true)][ValidatePattern('^[A-Za-z0-9-]+$')][string]$Name,
 [ValidateSet('Capture','Click','Key','Complete','ResearchOK','SaveName')][string]$Action='Capture',
 [int]$X,[int]$Y,[int]$FromX,[int]$FromY,[string]$Keys,
 [ValidateRange(1,25)][int]$NIndex,[string]$BeforeSnapshot,
 [switch]$ConfirmedNoModal,[switch]$ConfirmedRoutineClick,
 [switch]$ConfirmedWarriorOnRome,[ValidatePattern('^[A-Za-z0-9-]+$')][string]$WarriorLabel,
 [string]$ObservedResearch,[string]$ChangeToResearch,[switch]$ConfirmedVisibleResearchOK,
 [switch]$ConfirmedSaveNameField
)
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$folder=Join-Path $PSScriptRoot $Arm
$python='C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe'
$guard=Join-Path $PSScriptRoot 'guard.py'
& $python $guard --mode pins
if($LASTEXITCODE -ne 0){throw 'Source pins rejected'}
$s=Get-Content (Join-Path $folder 'start.json') -Raw|ConvertFrom-Json
$exe=Join-Path $root 'CTP-proef/ctp_program/ctp/civctp.exe'
$g=Get-Process -Id $s.pid -ErrorAction Stop
if($s.arm -ne $Arm -or $s.path -cne $exe -or $g.Path -cne $exe -or $g.StartTime.ToUniversalTime().ToFileTimeUtc() -ne $s.creation_filetime){throw 'Process identity changed'}
$elapsed=([DateTime]::UtcNow-$g.StartTime.ToUniversalTime()).TotalSeconds
if($elapsed -ge 1800 -or ($Action -notin @('Capture','Complete') -and $elapsed -ge 1500)){throw 'Proof deadline; close normally'}
if(-not $s.window){
 if($g.MainWindowHandle -eq 0){throw 'No main window; wait without input'}
 $s|Add-Member -NotePropertyName window -NotePropertyValue $g.MainWindowHandle.ToInt64() -Force
 $s|ConvertTo-Json|Set-Content (Join-Path $folder 'start.json') -Encoding UTF8
}
if($g.MainWindowHandle.ToInt64() -ne $s.window){throw 'Main window changed'}
$log=Join-Path $folder ($Name+'.log')
$png=Join-Path $folder ($Name+'.png')
$actionLog=Join-Path $folder ($Name+'-action.log')
$preLog=Join-Path $folder ($Name+'-pre-focus.log')
if(@($log,$png,$actionLog,$preLog,(Join-Path $folder ($Name+'-reader.log')))|Where-Object {Test-Path -LiteralPath $_}){throw 'Step name used; inspect prior outcome'}
$helper=Join-Path $root 'PROEVEN/Bedien-CTP.ps1'
function Capture($dest){
 & $helper -Action Capture -CaptureWaitForForeground -CaptureWaitTimeoutMs 3000 -ExpectedProcessId $s.pid -ExpectedCreationUtcMs $s.creation_utc_ms -ExpectedWindowHandle $s.window > $dest
 if(-not $?){throw 'Capture binding failed; no coordinate reuse'}
}
function Read-AfterN {
 if(([DateTime]::UtcNow-$g.StartTime.ToUniversalTime()).TotalSeconds -ge 1800){throw 'Host deadline; keep pending N'}
 $after=Join-Path $root ('PROEVEN/wondergewicht/20261030/land-t25-'+$Arm+'-'+$Name+'-after-N'+$NIndex.ToString('00')+'.json')
 if(Test-Path -LiteralPath $after){throw 'After output exists; never overwrite'}
 & $python (Join-Path $root 'PROEVEN/wondergewicht/20261030/Lees-Wondergewicht.py') --pid $s.pid --creation-filetime $s.creation_filetime --wonder-arm $Arm --variant B2a-N30-TECHNICAL --run-id LAND-STAD-T25-20261103 --snapshot-label ('AFTER-N'+$NIndex) --turn $NIndex --pass-label quiet --manifest (Join-Path $root 'PROEVEN/wondergewicht/20261030/participants.json') --output $after > (Join-Path $folder ($Name+'-reader.log'))
 if($LASTEXITCODE -ne 0){throw 'Reader rejected; pending consumed N, never resend'}
 & $python $guard --mode complete --start (Join-Path $folder 'start.json') --snapshot $after --index $NIndex
 if($LASTEXITCODE -ne 0){throw 'Native round gate rejected; pending consumed N, never resend'}
 Write-Output $after
}
if($Action -eq 'Complete'){
 if(-not $PSBoundParameters.ContainsKey('NIndex')){throw 'Explicit NIndex required'}
 if(-not(Test-Path (Join-Path $folder ('N'+$NIndex.ToString('00')+'-consumed.json'))) -or (Test-Path (Join-Path $folder ('N'+$NIndex.ToString('00')+'-completed.json')))){throw 'Expected pending consumed N'}
 Read-AfterN
}elseif($Action -ne 'Capture'){
 & $python (Join-Path $root 'PROEVEN/Controleer-Weekbudget.py') --thread 01a0f7b4-4751-7513-b510-3835ce43f47d
 if($LASTEXITCODE -notin @(0,25)){throw 'Budget unknown/stop; no input sent'}
 Capture $preLog
 $g=Get-Process -Id $s.pid -ErrorAction Stop
 if($g.Path -cne $exe -or $g.StartTime.ToUniversalTime().ToFileTimeUtc() -ne $s.creation_filetime -or $g.MainWindowHandle.ToInt64() -ne $s.window -or ([DateTime]::UtcNow-$g.StartTime.ToUniversalTime()).TotalSeconds -ge 1500){throw 'Identity/deadline changed; no input sent'}
 $token=$null
 if($Action -eq 'Key'){
  if($Keys -notin @('n','{ENTER}','f','{ESC}')){throw 'Unregistered key'}
  if($Keys -eq 'n'){
   if(-not $ConfirmedNoModal -or -not $PSBoundParameters.ContainsKey('NIndex') -or -not $BeforeSnapshot){throw 'N requires no-modal evidence, index and snapshot'}
   & $python $guard --mode consume --start (Join-Path $folder 'start.json') --snapshot $BeforeSnapshot --index $NIndex
   if($LASTEXITCODE -ne 0){throw 'Sequence gate rejected; no N sent'}
  }elseif($Keys -in @('{ENTER}','f')){
   if(-not $ConfirmedWarriorOnRome -or -not $WarriorLabel){throw 'Observed new active Warrior on Rome and unique label required'}
   $token=$(if($Keys -eq 'f'){'F-'}else{'SELECT-'})+$WarriorLabel+'-consumed.json'
  }elseif(-not $ConfirmedRoutineClick){throw 'ESC only for observed normal menu/panel route'}
 }elseif($Action -eq 'ResearchOK'){
  if(-not $ConfirmedVisibleResearchOK -or -not $ObservedResearch -or $ObservedResearch -cne $ChangeToResearch){throw 'Visible preselection and CHANGE TO must agree'}
  $token='RESEARCH-'+$Name+'-consumed.json'
 }elseif($Action -eq 'SaveName'){
  if(-not $ConfirmedSaveNameField -or -not(Test-Path (Join-Path $folder 'N25-completed.json'))){throw 'Observed normal Save name field at completed T25 required'}
  $token='SAVE-NAME-consumed.json'
 }elseif(-not $ConfirmedRoutineClick){throw 'Observed normal route required; strategic popup stops'}
 if($token){
  $stream=[IO.File]::Open((Join-Path $folder $token),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
  try{$bytes=[Text.Encoding]::UTF8.GetBytes(([ordered]@{pid=$s.pid;creation_filetime=$s.creation_filetime;at_utc=[DateTime]::UtcNow.ToString('o');action=$Action;keys=$Keys;warrior=$WarriorLabel;research=$ObservedResearch;visual_assertion=$true}|ConvertTo-Json));$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
 }
 $g=Get-Process -Id $s.pid -ErrorAction Stop
 if($g.Path -cne $exe -or $g.StartTime.ToUniversalTime().ToFileTimeUtc() -ne $s.creation_filetime -or $g.MainWindowHandle.ToInt64() -ne $s.window -or ([DateTime]::UtcNow-$g.StartTime.ToUniversalTime()).TotalSeconds -ge 1500){throw 'Identity/deadline changed after token; consumed action must not be resent'}
 if($Action -eq 'Key'){& $helper -Action Key -Keys $Keys > $actionLog}
 elseif($Action -eq 'SaveName'){& $helper -Action Key -Keys ('^aLAND-T25-20261103-'+$Arm.ToUpperInvariant()) > $actionLog}
 else{& $helper -Action Click -X $X -Y $Y -FromX $FromX -FromY $FromY > $actionLog}
 if(-not $?){throw 'Input outcome unknown; never resend consumed action'}
 if($Action -eq 'Key' -and $Keys -eq 'n'){Read-AfterN}
}
Capture $log
Copy-Item -LiteralPath (Join-Path $root 'PROEVEN/automatisering/ctp-window.png') -Destination $png
Write-Output $png
