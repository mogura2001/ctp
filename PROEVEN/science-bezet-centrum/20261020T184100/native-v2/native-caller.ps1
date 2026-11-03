$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit own helper required' }
$foodPackage=Split-Path $PSScriptRoot -Parent
$foodRoot=Split-Path (Split-Path (Split-Path $foodPackage -Parent) -Parent) -Parent
$foodGate=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'NATIVE-ROOT-REVIEW.json') -Raw | ConvertFrom-Json
if (-not $foodGate.native_allowed) { throw 'Separate root native release missing' }
$foodPinPath=Join-Path $PSScriptRoot 'NATIVE-SOURCE-PINS.json'
if ((Get-FileHash -LiteralPath $foodPinPath).Hash.ToLowerInvariant() -ne $foodGate.source_pins_sha256) { throw 'Native source pins changed' }
$foodPins=Get-Content -LiteralPath $foodPinPath -Raw | ConvertFrom-Json
foreach ($foodPin in $foodPins.sources) {
    if ((Get-FileHash -LiteralPath (Join-Path $foodRoot $foodPin.path)).Hash.ToLowerInvariant() -ne $foodPin.sha256) { throw "Native input pin changed: $($foodPin.path)" }
}
$foodAssembly=Join-Path $PSScriptRoot 'NativeFoodCaller.dll'
if ((Get-FileHash -LiteralPath $foodAssembly).Hash.ToLowerInvariant() -ne $foodGate.compiled_assembly_sha256) { throw 'Reviewed helper assembly changed' }
$foodOutput=Join-Path $PSScriptRoot 'native-caller-result.json'
if (Test-Path -LiteralPath $foodOutput) { throw 'Preserve prior run evidence' }
Add-Type -Path $foodAssembly
$foodResult=[NativeFoodCaller]::Run($foodRoot,$foodPackage,$foodGate.candidate_sha256,$foodGate.manifest_sha256)
$foodResult | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath $foodOutput
