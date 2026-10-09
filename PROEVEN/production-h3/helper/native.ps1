param([ValidateSet('fixture','loader')][string]$Mode='fixture')
$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit helper required' }
$package=Split-Path $PSScriptRoot -Parent
Add-Type -TypeDefinition (Get-Content -LiteralPath (Join-Path $PSScriptRoot 'Native.cs') -Raw) -Language CSharp
try {
 $result=[H3Native]::Run($package,$Mode)
 $result | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $package "H3-SCORE_CURRENT.native-$Mode.json")
 $result | ConvertTo-Json -Depth 10
} catch {
 @{mode=$Mode;pass=$false;error=$_.Exception.ToString();bitness=32} | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $package "H3-SCORE_CURRENT.native-$Mode.json")
 throw
}
