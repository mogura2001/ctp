$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit helper required' }
$candidatePackage=Split-Path $PSScriptRoot -Parent
$repositoryRoot=Split-Path (Split-Path (Split-Path $candidatePackage -Parent) -Parent) -Parent
Add-Type -Path (Join-Path $PSScriptRoot 'NativeCaller.dll')
$calls=[ScienceFilterCaller]::Run($repositoryRoot,$candidatePackage)
$labels=@([IO.File]::ReadAllLines((Join-Path $PSScriptRoot 'PASS.txt')) | ForEach-Object { [string]$_ })
[ordered]@{
 stage='OWN_CALLER_ONLY_NOT_ENGINE_OR_GAMEPLAY'
 native_calls=[int]$calls
 pass_labels=$labels
 engine_science_measured=$false
 actual_deficit_measured=$false
 gameplay_measured=$false
} | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $PSScriptRoot 'native-caller-result.json')
