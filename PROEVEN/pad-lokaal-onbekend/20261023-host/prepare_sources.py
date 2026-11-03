"""Historical one-shot clone, NOT a final-source regenerator.

Final sources contain subsequent root-review fixes captured in their diffs.
Never rerun this historical helper: existing outputs cause refusal, no overwrite.
No game, binary composition or runtime calls.
"""
from pathlib import Path
import json,difflib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=ROOT/'PROEVEN/uitbreiding-lang/20261022T122400'
CHAIN=ROOT/'PROEVEN/uitbreiding-lang/20261022T171500-afronding'
def put(name,text):
 p=HERE/name
 if p.exists():raise ValueError('No overwrite '+name)
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(text,'utf-8',newline='\n')
def clone(name,old,text):
 put(name,text)
 put(name+'.diff',''.join(difflib.unified_diff(old.splitlines(True),text.splitlines(True),fromfile='historical/'+name,tofile='20261023-host/'+name)))
s=(OLD/'Lees-Duur.py').read_text('utf-8')
s=s.replace("OLD_READER=OUTPUT_FOLDER.parents[1]/'selectie-pad-diagnose/20261020T192500/reader'", "ROOT=OUTPUT_FOLDER.parents[2]\nOLD_READER=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500/reader'\nC1=ROOT/'PROEVEN/pad-lokaal-onbekend/20261022T180000'")
s=s.replace("sys.path[:0]=[str(OUTPUT_FOLDER),str(OLD_READER)]", "sys.path[:0]=[str(OUTPUT_FOLDER),str(C1/'reader'),str(C1),str(OLD_READER)]")
s=s.replace("RUNTIME_PINS=json.loads((FOLDER/'runtime-pins.json').read_text('utf-8'))", "RUNTIME_PINS=json.loads((OUTPUT_FOLDER/'runtime-pins.json').read_text('utf-8'))")
s=s.replace("sys.path.insert(0,str(FOLDER.parent))", "sys.path.append(str(FOLDER.parent)) # legacy scalar/food/selected layouts only")
s=s.replace('from path_failure_decoder import stable_record,decode_path', "sys.path[:0]=[str(C1/'reader'),str(C1)] # legacy partial import prepends PACK\nfrom path_failure_decoder import stable_record,decode_path")
start=s.index('def trusted_binding(variant):')
end=s.index('\n\ndef verify_loaded',start)
adapter=s[start:end]
adapter=adapter.replace("pins=json.loads((FOLDER/'READER-PINS.json').read_text('utf-8'))", "pins=json.loads((HERE/'SOURCE-PINS.json').read_text('utf-8'))")
adapter=adapter.replace("if variant not in ('release-v1','U30-40')", "if variant!='local4'")
adapter=adapter.replace("mp=FOLDER.parent/'candidate-manifest.json'", "mp=ROOT/RUNTIME_PINS['manifest_path']")
adapter=adapter.replace("cpbytes=(FOLDER.parent/'reader/candidate'/('variant' if variant=='U30-40' else 'baseline')/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll').read_bytes()", "cpbytes=(ROOT/RUNTIME_PINS['candidate_path']).read_bytes()")
adapter=adapter.replace("expected=NEW_HASH if variant=='U30-40' else BASE_HASH", "expected=NEW_HASH")
adapter=adapter.replace("if variant=='U30-40':known += [(int(r['rva'],16),len(bytes.fromhex(r['preimage']))) for r in json.loads((FOLDER.parent/'preparation-manifest.json').read_text())['windows']]", "windows=[]\n    for row in manifest['allowed_changes']:\n        if row['reason'].startswith('named new hook '):\n            rva=cp.get_rva_from_offset(row['offset']);raw=bytes.fromhex(row['after'])\n            if len(raw)!=row['length'] or cp.get_data(rva,len(raw))!=raw:raise ValueError('Own manifest sitebytes mismatch')\n            windows.append(dict(name=row['reason'].split()[-1],rva=rva,raw=raw))\n    if len(windows)!=9:raise ValueError('Exact own nine site windows required')\n    known += [(r['rva'],len(r['raw'])) for r in windows]")
adapter=adapter.replace("if variant=='U30-40':", "if variant=='local4':")
adapter=adapter.replace("for row in json.loads((FOLDER.parent/'preparation-manifest.json').read_text())['windows']:\n            rva=int(row['rva'],16);raw=cp.get_data(rva,len(bytes.fromhex(row['preimage'])))", "for row in windows:\n            rva=row['rva'];raw=row['raw']")
adapter=adapter.replace("binding['shared_plan_size']=state_size", "binding['shared_plan_size']=state_size\n        sections=[dict(name=s.Name.rstrip(b'\\0').decode(),rva=s.VirtualAddress,virtual_size=s.Misc_VirtualSize,raw_offset=s.PointerToRawData,raw_size=s.SizeOfRawData,flags=s.Characteristics) for s in cp.sections]\n        if sections!=manifest['sections']:raise ValueError('Own manifest sections mismatch')\n        for name,call in manifest['path_diagnostic']['calls'].items():\n            raw=cp.get_data(call['call_rva'],5)\n            if raw[0]!=0xe8 or call['return_rva']!=call['call_rva']+5:raise ValueError('Own diagnostic actual call pair mismatch '+name)")
header="""\"\"\"Own runtime binding; disk bytes only until separately authorized reader main.\"\"\"
from pathlib import Path
import json,hashlib
from original_core import trusted_binding as original_binding
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
FOLDER=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500/reader'
RUNTIME_PINS=json.loads((HERE/'runtime-pins.json').read_text('utf-8'))
NEW_HASH=RUNTIME_PINS['candidate_sha256'];MANIFEST_HASH=RUNTIME_PINS['manifest_sha256']
"""
put('runtime_adapter.py',header+'\n'+adapter+'\n')
s=s[:start]+"from runtime_adapter import trusted_binding"+s[end:]
s=s.replace("args[1]['variant']=='U30-40'", "args[1]['variant']=='local4'")
s=s.replace("choices=('release-v1','U30-40')", "choices=('local4',)")
s=s.replace("if args.variant=='U30-40':", "if args.variant=='local4':")
s=s.replace("if binding['variant']!='U30-40':", "if binding['variant']!='local4':")
clone('Lees-Duur.py',(OLD/'Lees-Duur.py').read_text('utf-8'),s)
s=(OLD/'scope.py').read_text('utf-8')
s=s.replace('df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e','acfeec096ea39e1ff38435214769f4d24074e640b856e08d1c82cc09ea7a4984')
s=s.replace("ARMS={'release-v1':RELEASE,'U30-40':CANDIDATE}","ARMS={'local4':CANDIDATE}")
s=s.replace('5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152','0a10a7c7f1af1ecd0d71e549296a4e31ea850f100812515d519fa4055e497d4d')
clone('scope.py',(OLD/'scope.py').read_text('utf-8'),s)
put('runtime-pins.json',json.dumps(dict(stage='SOURCE_ONLY_ALL_RUNTIME_GATES_FALSE',candidate_path='PROEVEN/pad-lokaal-onbekend/20261023T155300-build/U30-40.prepared.dll',manifest_path='PROEVEN/pad-lokaal-onbekend/20261023T155300-build/candidate-manifest.json',candidate_sha256='acfeec096ea39e1ff38435214769f4d24074e640b856e08d1c82cc09ea7a4984',manifest_sha256='0a10a7c7f1af1ecd0d71e549296a4e31ea850f100812515d519fa4055e497d4d',state_rva=0xef000,state_size=497924),indent=2)+'\n')
(HERE/'local4').mkdir(exist_ok=True)
old=(CHAIN/'Afronding-85-100.ps1').read_text('utf-8')
s=old.replace('[ValidateRange(85,100)]','[ValidateRange(1,100)]').replace("[ValidateSet('U30-40')]","[ValidateSet('local4')]")
s=s.replace("$workspace='C:/GIT/ctp';$completionFolder=$PSScriptRoot;$package='C:/GIT/ctp/PROEVEN/uitbreiding-lang/20261022T122400';", "$workspace='C:/GIT/ctp';$completionFolder=$PSScriptRoot;$package=$PSScriptRoot;")
s=s.replace("$hostDir=Join-Path $workspace ('PROEVEN/uitbreiding-lang-host/20261022/'+$Arm)","$hostDir=Join-Path $package 'host'")
a=s.index('$expectedAI=');b=s.index('\n$exe=',a)
s=s[:a]+"$expectedAI='acfeec096ea39e1ff38435214769f4d24074e640b856e08d1c82cc09ea7a4984'"+s[b:]
s=s.replace('5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152','0a10a7c7f1af1ecd0d71e549296a4e31ea850f100812515d519fa4055e497d4d')
s=s.replace("($Arm -ceq 'U30-40')","($Arm -ceq 'local4')")
a=s.index('function CompletionAuthorization {');b=s.index('\nCompletionAuthorization',a)
s=s[:a]+'''function CompletionAuthorization {
 $approval=Get-Content (Join-Path $completionFolder 'ROOT-CONTROL.json') -Raw|ConvertFrom-Json
 if($approval.allowed -ne $true -or $approval.arm -cne 'local4' -or $approval.turn_min -ne 1 -or $approval.turn_max -ne 100 -or $approval.max_n -ne 100 -or $approval.pid -ne $gate.pid -or $approval.creation_filetime -ne $gate.creation_filetime -or $approval.window -ne $window.window -or $approval.run_id -cne $gate.run_id){throw 'Separate own root control gate required'}
 if($approval.source_pins_sha256 -cne (FileHash $pinPath)){throw 'Own source pins changed'}
 if($approval.start_sha256 -cne (FileHash (Join-Path $hostDir 'start.json')) -or $approval.window_sha256 -cne (FileHash (Join-Path $hostDir 'window.json'))){throw 'Immutable complete start/window hash changed'}
 if($Turn -ge 2 -and $approval.review_T1 -ne $true){throw 'Pause beforeT2: root T1 review required'}
 if($Turn -ge 27 -and $approval.review_T26 -ne $true){throw 'Pause beforeT27: root T26 review required'}
 $t0=Join-Path $armDir 'T0.json'
 if($approval.accepted_T0_sha256 -cne (FileHash $t0)){throw 'Accepted own T0 anchor changed'}
 foreach($pin in (Get-Content $pinPath -Raw|ConvertFrom-Json).sources){if((FileHash (Join-Path $workspace $pin.path)) -cne $pin.sha256){throw 'Own source changed'}}
}
''' +s[b:]
s=s.replace('AFRONDING-T','TURN-T').replace('$started.n_consumed -ne 84','$started.n_consumed -ne 0')
a=s.index('if($Turn -eq 85){');b=s.index('}else{',a)
s=s[:a]+'''if($Turn -eq 1){
 if((FileHash $previousPath) -cne $approval.accepted_T0_sha256){throw 'Exact accepted T0 anchor required'}
''' +s[b:]
s=s.replace('$approval.accepted_T0_sha256','((Get-Content (Join-Path $completionFolder \'ROOT-CONTROL.json\') -Raw|ConvertFrom-Json).accepted_T0_sha256)',1 if False else 0) if False else s
# Function-local $approval is read afresh for the T1 anchor below.
s=s.replace("if((FileHash $previousPath) -cne $approval.accepted_T0_sha256)","if((FileHash $previousPath) -cne ((Get-Content (Join-Path $completionFolder 'ROOT-CONTROL.json') -Raw|ConvertFrom-Json).accepted_T0_sha256))")
a=s.index('$immediateHash=$null');b=s.index('\nBudget;OwnState;CompletionAuthorization',a)
s=s[:a]+s[b:]
s=s.replace("previous_completion_pass_sha256=$previousOwnPassHash;previous_completion_token_sha256=$previousOwnTokenHash;immediate85_recheck_sha256=$immediateHash;helper_sha256=(FileHash $PSCommandPath);legacy84_start_sha256='f9b6099e7ef664581a25dcf1682c01657586b7c7bd1b2b2f815dcc49be1b0aa8'", "previous_completion_pass_sha256=$previousOwnPassHash;previous_completion_token_sha256=$previousOwnTokenHash;helper_sha256=(FileHash $PSCommandPath);start_sha256=(FileHash (Join-Path $hostDir 'start.json'));accepted_T0_sha256=(FileHash (Join-Path $armDir 'T0.json'))")
s=s.replace("operation='completion_after_two_proven_preinput_stops';legacy_n_consumed=84;plain_100_token_protocol=$false", "operation='own_immutable_turn';start_sha256=(FileHash (Join-Path $hostDir 'start.json'));previous_pass_sha256=$previousOwnPassHash;previous_token_sha256=$previousOwnTokenHash;plain_100_token_protocol=$true")
# Persist accepted snapshots exclusively as well; never overwrite a turn file.
s=s.replace("Copy-Item -LiteralPath $output -Destination (Join-Path $armDir ('T'+$Turn+'.json'));$accepted=$true;break", "$target=[IO.File]::Open((Join-Path $armDir ('T'+$Turn+'.json')),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None);try{$raw=[IO.File]::ReadAllBytes($output);$target.Write($raw,0,$raw.Length);$target.Flush()}finally{$target.Dispose()};$accepted=$true;break")
s=s.replace("# Completion tokens alone register input; legacy host/start.json is read-only.","# Own tokens alone register input; complete host/start.json stays read-only/n0.")
s=s.replace("$previousOwnPassHash=FileHash $priorPassPath;$previousOwnTokenHash=FileHash $priorTokenPath", "if($priorToken.start_sha256 -cne (FileHash (Join-Path $hostDir 'start.json')) -or $priorPass.start_sha256 -cne $priorToken.start_sha256){throw 'Prior immutable start mismatch'}\n $previousOwnPassHash=FileHash $priorPassPath;$previousOwnTokenHash=FileHash $priorTokenPath")
# Media check is read-only, ordinary app media only.
s=s.replace("function OwnState {", "function OwnState {\n if(@(Get-CimInstance Win32_CDROMDrive|Where-Object {$_.Drive -eq 'E:' -and $_.MediaLoaded -eq $true -and $_.VolumeName -eq 'CCTP'}).Count -ne 1){throw 'Ordinary CD media unavailable'}")
clone('Pass-Duur.ps1',old,s)
print('Reader/scope/runtime adapter prepared; no live main called')
