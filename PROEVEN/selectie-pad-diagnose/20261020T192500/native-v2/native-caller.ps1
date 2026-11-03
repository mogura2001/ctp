$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit own helper required' }
$pathLoggerPackage=Split-Path $PSScriptRoot -Parent
$pathLoggerRoot=Split-Path (Split-Path (Split-Path $pathLoggerPackage -Parent) -Parent) -Parent
$pathLoggerGate=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'NATIVE-ROOT-REVIEW.json') -Raw | ConvertFrom-Json
if (-not $pathLoggerGate.native_allowed) { throw 'Separate root native release missing' }
$pathLoggerPinPath=Join-Path $PSScriptRoot 'NATIVE-SOURCE-PINS.json'
if ((Get-FileHash -LiteralPath $pathLoggerPinPath).Hash.ToLowerInvariant() -ne $pathLoggerGate.source_pins_sha256) { throw 'Native source pins changed' }
$pathLoggerPins=Get-Content -LiteralPath $pathLoggerPinPath -Raw | ConvertFrom-Json
foreach ($pathLoggerPin in $pathLoggerPins.sources) {
    if ((Get-FileHash -LiteralPath (Join-Path $pathLoggerRoot $pathLoggerPin.path)).Hash.ToLowerInvariant() -ne $pathLoggerPin.sha256) { throw "Native input pin changed: $($pathLoggerPin.path)" }
}
$pathLoggerAssembly=Join-Path $PSScriptRoot 'NativePathLoggerCaller.dll'
if ((Get-FileHash -LiteralPath $pathLoggerAssembly).Hash.ToLowerInvariant() -ne $pathLoggerGate.compiled_assembly_sha256) { throw 'Reviewed helper assembly changed' }
$pathLoggerOutput=Join-Path $PSScriptRoot 'native-caller-result.json'
if (Test-Path -LiteralPath $pathLoggerOutput) { throw 'Preserve prior run evidence' }
Add-Type -Path $pathLoggerAssembly
# The copied caller independently requires ROOT-BRONREVIEW.native_allowed.
# Root must explicitly release both gates for this separate own-image run.
$pathLoggerExit=[NativePathLoggerCaller]::Main([string[]]@($pathLoggerRoot,$pathLoggerPackage,$pathLoggerGate.fixture_sha256,$pathLoggerGate.fixture_recipe_sha256))
@{exit_code=$pathLoggerExit;fixture_sha256=$pathLoggerGate.fixture_sha256;fixture_recipe_sha256=$pathLoggerGate.fixture_recipe_sha256;gameplay_proven=$false;own_logger_only=$true} | ConvertTo-Json | Set-Content -Encoding UTF8 -LiteralPath $pathLoggerOutput
if ($pathLoggerExit -ne 0) { throw "Native logger returned failure: $pathLoggerExit" }
