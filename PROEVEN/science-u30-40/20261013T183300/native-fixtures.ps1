param([Parameter(Mandatory=$true)][string]$Attempt)
$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit existing fixture method required' }
if ($Attempt -notmatch '^attempt[0-9]+$') { throw 'Bounded own result prefix required' }
$package = $PSScriptRoot
$output = Join-Path $package ("native-$Attempt.json")
if (Test-Path -LiteralPath $output) { throw 'Preserve earlier attempt' }
$manifest=Get-Content -LiteralPath (Join-Path $package 'candidate-manifest.json') -Raw | ConvertFrom-Json
$u30=Get-Content -LiteralPath (Join-Path $package '../../uitbreiding-30-40/20261012T181500/candidate-manifest.json') -Raw | ConvertFrom-Json
$rx=[int]$manifest.payload_rva
$h3=[Convert]::ToInt32($u30.components.internal_H3_rva.Substring(2),16)
$ranges=[int[]]@($rx,($rx+$manifest.payload_size),($rx+$manifest.labels.H3Capacity),($rx+$manifest.labels.H3FoodReader),($rx+$manifest.labels.H3FoodReader),($rx+$manifest.labels.H3PosCompare),($rx+$manifest.labels.H3DevelopmentTile),($h3+$u30.h3_labels.development_model),($rx+$manifest.labels.H3Host))
$fix=Get-Content -LiteralPath (Join-Path $package 'fixture-shim5-fixups.json') -Raw | ConvertFrom-Json
$rvas=[int[]]@($manifest.spatial_pins | ForEach-Object { $_.rva })
$hex=[string[]]@($manifest.spatial_pins | ForEach-Object { $_.bytes })
$fixAt=[int[]]@($fix | ForEach-Object { $_.at })
$fixOff=[int[]]@($fix | ForEach-Object { $_.context_offset })
try {
 Add-Type -TypeDefinition (Get-Content -LiteralPath (Join-Path $package 'native-fixtures.cs') -Raw) -Language CSharp
 $result=[ScienceNative]::Run($package,$ranges,$rvas,$hex,$fixAt,$fixOff)
 $result | ConvertTo-Json -Depth 14 | Set-Content -Encoding UTF8 -LiteralPath $output
 @{pass=$result.pass;native_calls=$result.native_calls;result=$output} | ConvertTo-Json
} catch {
 @{pass=$false;error=$_.Exception.ToString();cases=[ScienceNative]::Results;patches=[ScienceNative]::Patches;bitness=32;helper_pid=$PID;gameplay_measured=$false} | ConvertTo-Json -Depth 14 | Set-Content -Encoding UTF8 -LiteralPath $output
 throw
}
