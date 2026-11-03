param(
 [Parameter(Mandatory=$true)][ValidateSet('control','candidate')][string]$Arm,
 [Parameter(Mandatory=$true)][ValidatePattern('^[A-Za-z0-9-]+$')][string]$Name,
 [ValidateSet('Capture','Click','Key')][string]$Action='Capture',
 [int]$X,[int]$Y,[int]$FromX,[int]$FromY,[string]$Keys
)
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../../..'))
$folder=Join-Path $PSScriptRoot $Arm
$s=Get-Content (Join-Path $folder 'start.json') -Raw|ConvertFrom-Json
$g=Get-Process -Id $s.pid -ErrorAction Stop
if($g.Path -ne $s.path -or $g.StartTime.ToUniversalTime().ToFileTimeUtc() -ne $s.creation_filetime){throw 'Process identity changed'}
$elapsed=([DateTime]::UtcNow-$g.StartTime.ToUniversalTime()).TotalSeconds
if($elapsed -ge 900 -or ($Action -ne 'Capture' -and $elapsed -ge 780)){throw 'Proof deadline; close normally'}
if(-not $s.window){
 if($g.MainWindowHandle -eq 0){throw 'No main window; wait without input'}
 $s | Add-Member -NotePropertyName window -NotePropertyValue $g.MainWindowHandle.ToInt64() -Force
 $s | ConvertTo-Json | Set-Content (Join-Path $folder 'start.json') -Encoding UTF8
}
$log=Join-Path $folder ($Name+'.log')
$png=Join-Path $folder ($Name+'.png')
$actionLog=Join-Path $folder ($Name+'-action.log')
if((Test-Path -LiteralPath $log) -or (Test-Path -LiteralPath $png) -or (Test-Path -LiteralPath $actionLog)){throw 'Step name already used; inspect prior outcome'}
$helper=Join-Path $root 'PROEVEN/Bedien-CTP.ps1'
if($Action -eq 'Click'){
 & $helper -Action Click -X $X -Y $Y -FromX $FromX -FromY $FromY > $actionLog
 if(-not $?){throw 'Click outcome unknown; do not resend'}
} elseif($Action -eq 'Key'){
 if($Keys -ne 'n'){throw 'This proof allows only the registered single n'}
 $token=Join-Path $folder 'N1-consumed.json'
 $stream=[IO.File]::Open($token,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
 try{
  $bytes=[Text.Encoding]::UTF8.GetBytes(([ordered]@{pid=$s.pid;creation_filetime=$s.creation_filetime;at_utc=[DateTime]::UtcNow.ToString('o');maximum_inputs=1} | ConvertTo-Json))
  $stream.Write($bytes,0,$bytes.Length)
 }finally{$stream.Dispose()}
 & $helper -Action Key -Keys n > $actionLog
 if(-not $?){throw 'N1 outcome unknown; never resend'}
}
& $helper -Action Capture -CaptureWaitForForeground -CaptureWaitTimeoutMs 3000 -ExpectedProcessId $s.pid -ExpectedCreationUtcMs $s.creation_utc_ms -ExpectedWindowHandle $s.window > $log
if(-not $?){throw 'Capture failed; do not reuse coordinates'}
Copy-Item -LiteralPath (Join-Path $root 'PROEVEN/automatisering/ctp-window.png') -Destination $png
Write-Output $png

