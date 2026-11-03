$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit compiler helper required' }
$nativeSource = [IO.File]::ReadAllText((Join-Path $PSScriptRoot 'NativeCaller.cs'))
$nativeAssembly = Join-Path $PSScriptRoot 'NativeCaller.dll'
if (Test-Path -LiteralPath $nativeAssembly) { throw 'Preserve prior compilation' }
Add-Type -TypeDefinition $nativeSource -Language CSharp -OutputAssembly $nativeAssembly
Write-Output 'Compiled only; no Run invocation'
