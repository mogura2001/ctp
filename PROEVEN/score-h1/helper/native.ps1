param([Parameter(Mandatory=$true)][ValidateSet('H1-I','H1-M')][string]$Variant,
      [Parameter(Mandatory=$true)][ValidateSet('fixture','loader')][string]$Mode)
$ErrorActionPreference = 'Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit helper required' }
$package = Split-Path $PSScriptRoot -Parent
$source = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'Native.cs') -Raw
Add-Type -TypeDefinition $source -Language CSharp
try {
    $result = [H1Native]::Run($package,$Variant,$Mode)
    $result | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $package "$Variant.native-$Mode.json")
    $result | ConvertTo-Json -Depth 8
} catch {
    @{ variant=$Variant;mode=$Mode;pass=$false;error=$_.Exception.ToString();bitness=32 } | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $package "$Variant.native-$Mode.json")
    throw
}
