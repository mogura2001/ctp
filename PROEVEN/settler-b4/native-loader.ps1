param([ValidateSet(25,30)][int]$N=25,[switch]$Baseline,[switch]$Rebase)
$ErrorActionPreference='Stop'
Add-Type -TypeDefinition (Get-Content -LiteralPath (Join-Path $PSScriptRoot 'NativeLoader.cs') -Raw) -Language CSharp
$name="$(if($Baseline){'BASELINE'}else{'B4'})-N$N"
$manifest=Get-Content -LiteralPath (Join-Path $PSScriptRoot "$name.manifest.json") -Raw | ConvertFrom-Json
$sites=@();$targets=@()
foreach($row in $manifest.changes){if($row.reason -match 'score adapter|B4 '){$sites+=[Convert]::ToInt32($row.offset.Substring(2),16)+0xc00; $bytes=[byte[]](-split ($row.after -replace '..','$0 ') | ForEach-Object {[Convert]::ToByte($_,16)});$targets+=($sites[-1]+5+[BitConverter]::ToInt32($bytes,1))}}
# The original text raw->RVA delta is c00 for the documented hook range.
$size=if($Baseline){0xd9000}else{[Convert]::ToInt32($manifest.components.state_rva.Substring(2),16)+0x55000}
$base=[B4Loader]::Run((Join-Path $PSScriptRoot "$name.prepared.dll"),(Join-Path $PSScriptRoot "$name.payload.bin"),$size,[int[]]$sites,[int[]]$targets,[bool]$Rebase)
$result=@{variant=$name;candidate_sha256=$manifest.candidate_sha256;module_base=$base;ordinary_imports_DllMain=$true;actual_rebase=[bool]$Rebase;PIC_payload_and_hook_targets=$true;gameplay_measured=$false;pass=$true}
$result|ConvertTo-Json|Set-Content -Encoding UTF8 (Join-Path $PSScriptRoot "$name.native-loader$(if($Rebase){'-rebase'}).json")
$result|ConvertTo-Json
