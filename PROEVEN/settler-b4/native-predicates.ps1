param([ValidateSet(25,30)][int]$N=25)
$ErrorActionPreference='Stop'
if ([IntPtr]::Size -ne 4) { throw '32-bit helper required' }
$package=$PSScriptRoot
$root=Split-Path (Split-Path $package -Parent) -Parent
Add-Type -TypeDefinition (Get-Content -LiteralPath (Join-Path $package 'NativePredicates.cs') -Raw) -Language CSharp
$manifest=Get-Content -LiteralPath (Join-Path $package "B4-N$N.manifest.json") -Raw | ConvertFrom-Json
$base=[Convert]::ToInt32($manifest.components.B4.rva.Substring(2),16)
$cases=[B4Predicates]::Run($root,(Join-Path $package "B4-N$N.payload.bin"),($base+$manifest.labels.owner_gate),($base+$manifest.labels.plan_conflict),($base+$manifest.labels.order_roles))
$result=@{N_fixture=$N;candidate_sha256=$manifest.candidate_sha256;bitness=32;cases=$cases;pass=$true;scope='actual emitted owner/conflict/order only; full producer/wrappers acceptance pending';no_real_engine_calls=$true;gameplay_measured=$false}
$result | ConvertTo-Json | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $package "B4-N$N.native-predicates.json")
$result | ConvertTo-Json
