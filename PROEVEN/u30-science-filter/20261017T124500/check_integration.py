"""Actual emitted integration checks only. No native or process access."""
from pathlib import Path
import hashlib,json,re,sys
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
m=json.loads((OUT/'candidate-manifest.json').read_text());p=pefile.PE(data=(OUT/'U30-40.prepared.dll').read_bytes());base=0x20000000+int(m['components']['extension_rva'],16);labels={k:base+v for k,v in m['labels'].items()};d=Cs(CS_ARCH_X86,CS_MODE_32)
ins=[]
for row in m['recipe']:
 if not row['asm'].startswith('constant'):ins+=list(d.disasm(bytes.fromhex(row['bytes']),base+row['offset']))
def body(a,b):return [(i.mnemonic,i.op_str) for i in ins if labels[a]<=i.address<labels[b]]
roles=body('location_roles','choose_alternative');prefix=body('canonical_prefix','finalize_pass');typ=body('resolve_type','owner_gate')
assert ('call','dword ptr [edx + 0x1c]') in typ and ('test','eax, 0x80000000') in typ
assert ('call','dword ptr [edx + 0x28]') in prefix
for off in (0xe0,0xe4,0xe8,0xec):assert ('mov',f'dword ptr [ebx + {hex(off)}], 0') in prefix
assert ('cmp','eax, dword ptr [ebx + 0xe0]') in roles
assert ('cmp','dword ptr [ebx + 0xd0], 0') not in roles
assert ('cmp','dword ptr [ebx + 0x110], 0') in roles
assert ('mov','dword ptr [ebx + 0x110], 0') in roles
budgets=[k for k in labels if re.fullmatch(r'c2_count_\d+_budget',k)]
for name in budgets:
 stem=name[:-7];budget=body(name,stem+'_fail');context=body(stem+'_context',name)
 assert ('mov','dword ptr [ebx + 0xd0], 1') in budget and ('mov','dword ptr [ebx + 0x110], 1') in budget
 assert ('mov','dword ptr [ebx + 0x10c], 1') in context
 assert labels[stem+'_context']<labels[name]
assert sum(i.mnemonic=='mov' and i.op_str=='dword ptr [ebx + 0x110], 1' for i in ins)==len(budgets)
for offset,limit in [(240,64),(244,1280),(248,1280),(252,3840),(256,1344),(260,1280),(264,2624)]:assert any(i.mnemonic=='cmp' and i.op_str==f'dword ptr [ebx + {hex(offset)}], {hex(limit)}' for i in ins),(offset,limit)
assert labels['roles_postscience_context']<labels['roles_final_context']<labels['roles_bad']
assert ('cmp','dword ptr [ebx + 0x10c], 0') in roles
assert m['components']['state_size']==0x79804 and labels['generation']==labels['pass_state']+0x79800
assert m['components']['internal_H3_sha256']=='5a0c008f3e660e30cc9011146d029dd01c514c46f0840c8c20876848e4f25c57'
for row in m['sources']+m['source_dependency_pins']+m['release_pins']:assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
result=dict(stage='ACTUAL_EMITTED_STATIC_ONLY',candidate_sha256=m['candidate_sha256'],type1c_and_80000000=True,actual_prefix_world28_and_header_retained=True,consumer_prefix_loop=True,prefixcutoff_not_budgetstop=True,science_marker_only_actual_counterbudget=len(budgets),all_seven_new_counter_offsets_and_limits_present=True,context_failure_before_budget=True,postscience_and_final_context_guards_present=True,Plan_and_generation_79800_79804=True,H3_preserved=True,all_dependencies_match=True,native_positive_reader_game_cases='ONGETEST')
(OUT/'integration-static-checks.json').write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps(result))
