$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit compiler helper required' }
$foodPackage=Split-Path $PSScriptRoot -Parent
$foodRoot=Split-Path (Split-Path (Split-Path $foodPackage -Parent) -Parent) -Parent
$foodGate=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'NATIVE-ROOT-REVIEW.json') -Raw | ConvertFrom-Json
if (-not $foodGate.compilation_allowed) { throw 'Separate root compile release missing' }
$foodPinPath=Join-Path $PSScriptRoot 'NATIVE-SOURCE-PINS.json'
if ((Get-FileHash -LiteralPath $foodPinPath).Hash.ToLowerInvariant() -ne $foodGate.source_pins_sha256) { throw 'Reviewed native source pins changed' }
$foodPins=Get-Content -LiteralPath $foodPinPath -Raw | ConvertFrom-Json
foreach ($foodPin in $foodPins.sources) {
    if ((Get-FileHash -LiteralPath (Join-Path $foodRoot $foodPin.path)).Hash.ToLowerInvariant() -ne $foodPin.sha256) { throw "Source pin changed: $($foodPin.path)" }
}
$foodAssembly=Join-Path $PSScriptRoot 'NativeFoodCaller.dll'
if (Test-Path -LiteralPath $foodAssembly) { throw 'Preserve prior compilation' }
Add-Type -TypeDefinition ([IO.File]::ReadAllText((Join-Path $PSScriptRoot 'NativeFoodCaller.cs'))) -Language CSharp -OutputAssembly $foodAssembly
Write-Output 'Compiled only; no Run invocation'
