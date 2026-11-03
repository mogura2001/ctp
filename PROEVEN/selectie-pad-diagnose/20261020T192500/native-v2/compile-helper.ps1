$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit compiler helper required' }
$pathLoggerPackage=Split-Path $PSScriptRoot -Parent
$pathLoggerRoot=Split-Path (Split-Path (Split-Path $pathLoggerPackage -Parent) -Parent) -Parent
$pathLoggerGate=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'NATIVE-ROOT-REVIEW.json') -Raw | ConvertFrom-Json
if (-not $pathLoggerGate.compilation_allowed) { throw 'Separate root compile release missing' }
$pathLoggerPinPath=Join-Path $PSScriptRoot 'NATIVE-SOURCE-PINS.json'
if ((Get-FileHash -LiteralPath $pathLoggerPinPath).Hash.ToLowerInvariant() -ne $pathLoggerGate.source_pins_sha256) { throw 'Reviewed native source pins changed' }
$pathLoggerPins=Get-Content -LiteralPath $pathLoggerPinPath -Raw | ConvertFrom-Json
foreach ($pathLoggerPin in $pathLoggerPins.sources) {
    if ((Get-FileHash -LiteralPath (Join-Path $pathLoggerRoot $pathLoggerPin.path)).Hash.ToLowerInvariant() -ne $pathLoggerPin.sha256) { throw "Source pin changed: $($pathLoggerPin.path)" }
}
$pathLoggerAssembly=Join-Path $PSScriptRoot 'NativePathLoggerCaller.dll'
if (Test-Path -LiteralPath $pathLoggerAssembly) { throw 'Preserve prior compilation' }
Add-Type -TypeDefinition ([IO.File]::ReadAllText((Join-Path $PSScriptRoot 'NativePathLoggerCaller.cs'))) -Language CSharp -OutputAssembly $pathLoggerAssembly
Write-Output 'Compiled only; no Run invocation'
