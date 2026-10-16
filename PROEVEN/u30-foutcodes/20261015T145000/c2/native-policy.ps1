param([ValidateSet('r4')][string]$Label='r4')
$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit helper required' }
$package=$PSScriptRoot
$candidatePackage=Split-Path $package -Parent
$root=Split-Path (Split-Path (Split-Path $candidatePackage -Parent) -Parent) -Parent
$manifest=Get-Content -LiteralPath (Join-Path $candidatePackage 'candidate-manifest.json') -Raw | ConvertFrom-Json
$dll=Join-Path $candidatePackage 'U30-40.prepared.dll'
if ((Get-FileHash -LiteralPath $dll -Algorithm SHA256).Hash.ToLowerInvariant() -ne $manifest.candidate_sha256) { throw 'Candidate pin' }
Add-Type -TypeDefinition (Get-Content -LiteralPath (Join-Path $package 'NativeU40.cs') -Raw) -Language CSharp
$base=[Convert]::ToInt32($manifest.components.extension_rva.Substring(2),16)
$names=@();$offsets=@()
foreach ($property in $manifest.labels.PSObject.Properties) {$names+=$property.Name;$offsets+=($base+[int]$property.Value)}
$rw=[Convert]::ToInt32($manifest.components.state_rva.Substring(2),16)
$result=[U40Producer]::Run($root,$package,$dll,[int[]]$offsets,[string[]]$names,($rw+0x55000),$false)
$result['candidate_sha256']=$manifest.candidate_sha256
$result | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $package "native-policy-result-$Label.json")
$result | ConvertTo-Json -Depth 8
