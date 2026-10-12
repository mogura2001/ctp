param([ValidateSet(25,30)][int]$N=25,[switch]$OldSafety)
$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit helper required' }
$package=$PSScriptRoot
$root=Split-Path (Split-Path $package -Parent) -Parent
Add-Type -TypeDefinition (Get-Content -LiteralPath (Join-Path $package 'NativeProducer.cs') -Raw) -Language CSharp
$source=if ($OldSafety) { Join-Path $package 'checkpoint-pre-validatie' } else { $package }
$manifest=Get-Content -LiteralPath (Join-Path $source "B4-N$N.manifest.json") -Raw | ConvertFrom-Json
$base=[Convert]::ToInt32($manifest.components.B4.rva.Substring(2),16)
$names=@();$offsets=@()
foreach ($property in $manifest.labels.PSObject.Properties) { $names+=$property.Name; $offsets+=($base+[int]$property.Value) }
$result=[B4Producer]::Run($root,$package,(Join-Path $source "B4-N$N.prepared.dll"),[int[]]$offsets,[string[]]$names,([Convert]::ToInt32($manifest.components.state_rva.Substring(2),16)+0x55000),[bool]$OldSafety)
$result['candidate_sha256']=$manifest.candidate_sha256
$result['N_fixture']=$N
$result | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $package "B4-N$N.native-producer$(if($OldSafety){'-old-safety'}).json")
$result | ConvertTo-Json -Depth 8
