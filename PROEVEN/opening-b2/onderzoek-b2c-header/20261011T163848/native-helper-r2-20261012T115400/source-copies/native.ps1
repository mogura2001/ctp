param([Parameter(Mandatory=$true)][string]$CaseId)
$ErrorActionPreference='Stop'
if([IntPtr]::Size -ne 4){throw 'Own x86 subprocess required'}
$helper=$PSScriptRoot
$plan=Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $helper 'cases.json') | ConvertFrom-Json
$case=@($plan.cases | Where-Object {$_.id -ceq $CaseId})
if($case.Count -ne 1){throw 'Unknown or duplicate case'}
$case=$case[0]
$output=Join-Path $helper ('results/'+$CaseId+'.json')
$trace=Join-Path $helper ('results/'+$CaseId+'.trace')
if((Test-Path -LiteralPath $output) -or (Test-Path -LiteralPath $trace)){throw 'Existing own case output; no retry/overwrite'}
# Every input including this source is pinned by the runner's reviewed-source approval gate.
foreach($pin in $plan.input_pins){
 $actual=(Get-FileHash -LiteralPath $pin.path -Algorithm SHA256).Hash.ToLowerInvariant()
 if($actual -cne $pin.sha256){throw 'Pinned input mismatch: '+$pin.path}
}
$approval=Join-Path $helper 'C3-ROOT-VRIJGAVE.json'
if(-not (Test-Path -LiteralPath $approval)){throw 'C3 native calls are not root-approved'}
$approved=Get-Content -Raw -Encoding UTF8 -LiteralPath $approval | ConvertFrom-Json
if($approved.native_execution_approved -ne $true -or $approved.plan_sha256 -cne (Get-FileHash -LiteralPath (Join-Path $helper 'cases.json') -Algorithm SHA256).Hash.ToLowerInvariant()){throw 'Wrong C3 approval'}
foreach($pin in $approved.reviewed_source_pins){if((Get-FileHash -LiteralPath (Join-Path $helper $pin.path) -Algorithm SHA256).Hash.ToLowerInvariant() -cne $pin.sha256){throw 'Reviewed source changed'}}
$fixture=[string[]]$plan.fixture_names
$expected=[string[][]]@($case.expected | ForEach-Object {,@([string[]]$_)})
$f1=[int[][]]@($plan.shim1_fixups | ForEach-Object {,@([int[]]@($_.at,$_.context_offset))})
$f2=[int[][]]@($plan.shim2_fixups | ForEach-Object {,@([int[]]@($_.at,$_.context_offset))})
$rvas=[int[]]@($plan.entrypoints | ForEach-Object {$_.rva})
$preimages=[string[]]@($plan.entrypoints | ForEach-Object {$_.original_24_bytes_hex})
$relocations=[int[][]]@($plan.entrypoints | ForEach-Object {,@([int[]]$_.highlow_offsets_in_24_bytes)})
Add-Type -TypeDefinition (Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $helper 'Native.cs')) -Language CSharp
$result=$null
try{
 $result=[B2cParserNative]::Run($helper,$plan.dll,$case.staging,$case.kind,[string[]]$case.files,$expected,$fixture,$f1,$f2,$rvas,$preimages,$relocations,$trace)
}catch{
 $result=[B2cParserNative]::Evidence
 if($null -eq $result){$result=@{pass=$false}}
 $result['pass']=$false
 $result['error']=$_.Exception.ToString()
}finally{
 if($null -ne $result){
  $json=$result | ConvertTo-Json -Depth 20
  if([Text.Encoding]::UTF8.GetByteCount($json) -gt 4194304){throw 'Own result exceeds 4MiB bound; no PASS output'}
  $json | Set-Content -LiteralPath $output -Encoding UTF8
 }
}
if($result['pass'] -ne $true){exit 2}
Write-Output ('NATIVE_CASE_COMPLETED='+$CaseId)
exit 0
