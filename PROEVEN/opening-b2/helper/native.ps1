param([ValidateSet('fixture','loader')][string]$Mode='fixture',[ValidateSet(25,30)][int]$N=25)
$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit helper required' }
$package=Split-Path $PSScriptRoot -Parent
Add-Type -TypeDefinition (Get-Content -LiteralPath (Join-Path $PSScriptRoot 'Native.cs') -Raw) -Language CSharp
try {
 $result=[B2Native]::Run($package,$N,$Mode)
 $result | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $package "B2a-N$N-TECHNICAL.native-$Mode.json")
 $result | ConvertTo-Json -Depth 10
} catch {
 @{mode=$Mode;N_fixture=$N;pass=$false;error=$_.Exception.ToString();bitness=32} | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $package "B2a-N$N-TECHNICAL.native-$Mode.json")
 throw
}
