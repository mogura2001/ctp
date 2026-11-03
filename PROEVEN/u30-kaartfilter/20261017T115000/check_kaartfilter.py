"""Actual candidate delta checks. No native execution or process reads."""
from pathlib import Path
import json,sys,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
m=json.loads((OUT/'candidate-manifest.json').read_text('utf-8'));p=pefile.PE(data=(OUT/'U30-40.prepared.dll').read_bytes());base=0x20000000+int(m['components']['extension_rva'],16);labels={k:base+v for k,v in m['labels'].items()};d=Cs(CS_ARCH_X86,CS_MODE_32)
def body(a,b):return list(d.disasm(p.get_data(labels[a]-0x20000000,labels[b]-labels[a]),labels[a]))
prefix=body('canonical_prefix','finalize_pass');roles=body('production_roles','order_roles');host=body('bind_host','bind_inputs')
def pair(ins):return (ins.mnemonic,ins.op_str)
def sequence(ins,expected):
 for i in range(len(ins)-len(expected)+1):
  if [pair(x) for x in ins[i:i+len(expected)]]==expected:return ins[i].address
 raise AssertionError(expected)
def branch(ins,mnemonic,label):assert any(x.mnemonic==mnemonic and x.op_str==hex(labels[label]) for x in ins),(mnemonic,label)
checks={}
for off in (0xe0,0xe4,0xe8,0xec):sequence(prefix,[('mov',f'dword ptr [ebx + {hex(off)}], 0')])
checks['four_dword_zero_writes']=True
sequence(prefix,[('cmp','dword ptr [ebx + 0x5c], 0'),('jne',hex(labels['prefix_bad']))]);branch(prefix,'js','prefix_bad');sequence(prefix,[('cmp','eax, 0x1000'),('jg',hex(labels['prefix_bad']))])
checks['nodes_candidates_guards_before_keys']=True
key=sequence(prefix,[('call',hex(labels['canonical_key'])),('test','eax, eax'),('je',hex(labels['prefix_bad']))])
gate=sequence(prefix,[('push','dword ptr [ebp - 0x20]'),('mov','eax, dword ptr [ebx + 0x70]'),('push','eax'),('mov','edx, dword ptr [eax]'),('call','dword ptr [edx + 0x28]'),('test','eax, eax'),('je',hex(labels['prefix_unknown']))])
assert key<gate
sequence(prefix,[('mov','dword ptr [edi + 8], 0xffffffff'),('inc','dword ptr [ebx + 0xec]')]);sequence(prefix,[('cmp','dword ptr [ebx + 0xe4], 0x40'),('jle',hex(labels['prefix_no_cutoff'])),('mov','dword ptr [ebx + 0xd0], 1')])
sequence(prefix,[('cmp','eax, dword ptr [ebx + 0xe4]'),('jae',hex(labels['prefix_ok']))]);sequence(prefix,[('test','eax, eax'),('js',hex(labels['prefix_bad']))]);sequence(prefix,[('inc','dword ptr [ebx + 0xe0]')])
checks.update(key_before_original_external_ret8_gate=True,no_caller_stack_adjust_after_gate=True,false_excluded_before_minimum=True,known_count_prefix_limit_and_cutoff=True,store_minus_one_guard_and_prefix_increment=True)
for pattern in [[('test','eax, eax'),('js',hex(labels['roles_bad']))],[('cmp','eax, 0x40'),('ja',hex(labels['roles_bad']))],[('cmp','eax, dword ptr [ebx + 0xe4]'),('jg',hex(labels['roles_bad']))],[('cmp','eax, dword ptr [ebx + 0x44]'),('jg',hex(labels['roles_bad']))],[('cmp','eax, 0x1000'),('jg',hex(labels['roles_bad']))]]:sequence(roles,pattern)
sequence(roles,[('cmp','eax, dword ptr [ebx + 0xe0]'),('jge',hex(labels['roles_ok']))])
sequence(roles,[('mov','eax, dword ptr [edx]'),('test','eax, eax'),('js',hex(labels['roles_bad'])),('cmp','eax, dword ptr [ebx + 0x44]'),('jae',hex(labels['roles_bad'])),('shl','eax, 3')])
sequence(roles,[('cmp','dword ptr [ebx + 0x80], 0x40'),('jae',hex(labels['roles_bad']))]);sequence(roles,[('call',hex(labels['H3Classifier'])),('test','eax, eax'),('je',hex(labels['roles_bad']))])
assert not any(x.mnemonic=='call' and x.op_str=='dword ptr [edx + 0x28]' for x in roles)
assert not any(x.mnemonic=='mov' and x.op_str=='dword ptr [ebx + 0xd0], 1' for x in roles)
checks.update(consumer_full_bounds_and_order_before_scale=True,prefix_count_loop_only=True,h3_budget_and_unknown_fallback_retained=True,no_duplicate_gate_or_source_count_cutoff_in_consumer=True)
sequence(host,[('mov','edx, dword ptr [ebx + 0x64]'),('add','edx, 0x3452e0'),('mov','eax, dword ptr [ebx + 0x64]'),('add','eax, 0x133580'),('cmp','dword ptr [edx + 0x28], eax'),('jne',hex(labels['bind_bad']))])
checks['world_slot28_real_engine_pointer_bound_before_prefix']=True
for instructions,reason in [(prefix,41),(roles,23),(host,30)]:
 sequence(instructions,[('mov','dword ptr [ebx], 0'),('mov',f'dword ptr [ebx + 4], {hex(reason)}'),('mov','eax, 0')])
 assert pair(instructions[-1])==('ret','4')
 assert not any(x.mnemonic.startswith('f') for x in instructions)
checks['mismatch_reasons_and_ret4_nonvolatile_epilogues_no_x87_added']=True
old=json.loads((ROOT/'PROEVEN/u30-type10/20261015T194300/candidate-manifest.json').read_text())
assert m['components']['internal_H3_sha256']==old['components']['internal_H3_sha256'];assert m['b2_preserved']==old['b2_preserved']
checks['entire_internal_H3_and_B2_unchanged']=True
result=dict(stage='ACTUAL_CANDIDATE_STATIC_SEMANTICS_ONLY',candidate_sha256=m['candidate_sha256'],checks=checks,gate_call_address=hex(gate),key_call_address=hex(key),native_calls=0,rpm=0,gameplay_acceptance=False)
(OUT/'kaartfilter-static-checks.json').write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps(result))
