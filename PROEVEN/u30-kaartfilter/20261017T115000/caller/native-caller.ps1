$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit helper required' }
$candidatePackage=Split-Path $PSScriptRoot -Parent
$root=Split-Path (Split-Path (Split-Path $candidatePackage -Parent) -Parent) -Parent
$manifest=Get-Content -LiteralPath (Join-Path $candidatePackage 'candidate-manifest.json') -Raw | ConvertFrom-Json
if ($manifest.components.extension_rva -ne '0xd9000') { throw 'Reviewed hardcoded fixture extension changed' }
if ($manifest.candidate_sha256 -ne '738be4098dadc6657b121519213e794ce3ec095025fdc940f6c30a5d89661d66') { throw 'Candidate pin' }
Add-Type -TypeDefinition (Get-Content -LiteralPath (Join-Path $PSScriptRoot 'NativeCaller.cs') -Raw) -Language CSharp
$calls=[KaartfilterCaller]::Run($root,$candidatePackage)
[ordered]@{stage='OWN_CALLER_ONLY_NOT_ENGINE_OR_GAMEPLAY';native_calls=$calls;candidate_sha256=$manifest.candidate_sha256;pass_labels=(Get-Content -LiteralPath (Join-Path $PSScriptRoot 'PASS.txt'));supported_h3_slots_certified=$false} | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $PSScriptRoot 'native-caller-result.json')
