"""Finite source/actual-candidate verification and integer cases, never native."""
from pathlib import Path
import sys,hashlib,json,importlib.util,ast,difflib
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];OLD=ROOT/'PROEVEN/u30-foutcodes/20261015T145000'
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
sha=lambda b:hashlib.sha256(b).hexdigest()
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def write(n,s):(OUT/n).write_text(s,'utf-8')
old="iface(r,P['udb'],['edi'],0xdc);r.test('eax','eax');r.j('jz','type_bad')"
new="iface(r,P['udb'],['edi'],0x1c);r.test('eax',0x80000000);r.j('jz','type_bad')"
assert (OUT/'native.py').read_text()==(OLD/'native.py').read_text().replace(old,new)
for name in ['policy.py','integration_base.py','bind_scheduler.py']:
 assert (OUT/name).read_bytes()==(OLD/name).read_bytes()
oldpins=module(OLD/'input-pins.py','old_pins').pins();newpins=module(OUT/'input-pins.py','new_pins').pins()
assert newpins['slots']==[dict(slot=0x1c,rva=0x131940)]+oldpins['slots']
body=bytes.fromhex('558bec8b450c8b0d18dda70050e88e29f2ff8b403025000000ff5dc20800')
assert len(body)==30
assert newpins['bodies'][1:]==oldpins['bodies']
assert newpins['bodies'][0]==dict(kind='engine',rva=0x131940,length=30,bytes=body.hex(),relocations=[])
write('input-pins.json',json.dumps(newpins,indent=2)+'\n')
manifest=json.loads((OUT/'candidate-manifest.json').read_text());candidate=(OUT/'U30-40.prepared.dll').read_bytes();cp=pefile.PE(data=candidate)
assert sha(candidate)==manifest['candidate_sha256']
base=int(manifest['components']['extension_rva'],16);labels=manifest['labels']
start=base+labels['resolve_type'];end=base+labels['owner_gate'];raw=cp.get_data(start,end-start)
dis=Cs(CS_ARCH_X86,CS_MODE_32);ins=list(dis.disasm(raw,0x20000000+start))
tests=[i for i,x in enumerate(ins) if x.mnemonic=='test' and x.op_str=='eax, 0x80000000'];assert len(tests)==1
i=tests[0];assert ins[i-1].mnemonic=='call' and ins[i-1].op_str=='dword ptr [edx + 0x1c]'
assert ins[i+1].mnemonic=='je' and int(ins[i+1].op_str,16)==0x20000000+base+labels['type_bad']
assert ins[i-2].mnemonic=='mov' and ins[i-2].op_str=='edx, dword ptr [eax]'
assert ins[i-3].mnemonic=='push' and ins[i-3].op_str=='eax'
assert ins[i-5].mnemonic=='push' and ins[i-5].op_str=='edi'
assert ins[-1].mnemonic=='ret' and ins[-1].op_str=='4'
assert any(x.mnemonic=='call' and x.op_str=='dword ptr [edx + 0xd8]' for x in ins)
assert not any(x.mnemonic=='call' and x.op_str=='dword ptr [edx + 0xdc]' for x in ins)
write('resolve-type-disassembly.txt','\n'.join(f'{x.address:08x} {x.bytes.hex():24} {x.mnemonic:8} {x.op_str}' for x in ins)+'\n')
ep=pefile.PE(str(ROOT/'CTP-og/ctp_program/ctp/civctp.exe'))
assert ep.OPTIONAL_HEADER.ImageBase==0x400000 and ep.FILE_HEADER.TimeDateStamp==0x37d6f702
assert ep.get_data(0x131940,30)==body and ep.get_data(0x3450b4,4)==bytes.fromhex('40195300')
engineins=list(dis.disasm(body,0x531940));assert engineins[-1].mnemonic=='ret' and engineins[-1].op_str=='8'
assert any(x.mnemonic=='call' and x.op_str=='0x4542e0' for x in engineins)
write('531940-disassembly.txt','\n'.join(f'{x.address:08x} {x.bytes.hex():24} {x.mnemonic:8} {x.op_str}' for x in engineins)+'\n')
cases=[]
for movement,flags,want in [(0x80000000,5,True),(0x90000000,5,True),(0,5,False),(0x10000000,5,False),(0,0x25,False),(0x80000000,0x25,True)]:
 result=bool((movement&0xff000000)&0x80000000);assert result==want
 cases.append(dict(record30=hex(movement),record34=hex(flags),predicate_result=result,expected=want,kind='INDEPENDENT_INTEGER_ONLY_NOT_MACHINECODE_NOT_ABI'))
write('integer-mask-cases.json',json.dumps(cases,indent=2)+'\n')
reader=OUT/'reader/Lees-Uitbreiding.py';s=reader.read_text();s=s.replace("NEW_HASH='8610db83d4e424006f6c8ee3912bac11fd432dd2bb6264c7c9ed5b94fe67dc17'","NEW_HASH='"+sha(candidate)+"'")
s=s.replace("MANIFEST_HASH='6bf3d57db8aa1f9c36ae5407292cfd597175420c22e16996a5d593737f8f3437'","MANIFEST_HASH='"+sha((OUT/'candidate-manifest.json').read_bytes())+"'");reader.write_text(s,'utf-8')
ast.parse(s)
assert '(0x131940,0x1e),(0x3450b4,4)' in s
assert '(0x542e0,0x30)' in s
write('diffs/Lees-Uitbreiding.py.diff',''.join(difflib.unified_diff((OLD/'r44-2/Lees-Uitbreiding.py').read_text().splitlines(True),s.splitlines(True),fromfile='frozen-r44-2/Lees-Uitbreiding.py',tofile='type10/reader/Lees-Uitbreiding.py')))
for p in OUT.rglob('*.py'):ast.parse(p.read_text('utf-8'))
summary=dict(stage='TYPE10_OFFLINE_STATIC_AND_INTEGER_ONLY',candidate_sha256=sha(candidate),manifest_sha256=sha((OUT/'candidate-manifest.json').read_bytes()),only_resolver_predicate_source_delta=True,policy_integration_and_faultcode_preservation_byte_identical=True,slot_and_full30byte_body_additive=True,reader_full30byte_and_real_slotpointer_binding=True,resolver_call_slot='0x1c',test_mask='0x80000000',same_type_bad_target=hex(0x20000000+base+labels['type_bad']),resolver_ret4=True,engine_body_ret8=True,integer_cases=len(cases),native_real_body_cases='NOT_EXECUTED_EXISTING_FIXTURE_NO_FIXED_GLOBAL_OR_REAL_GETTER_BINDING',native_abi='NOT_EXECUTED_STATIC_CALL_ARGUMENTS_AND_EPILOGUE_ONLY',native_calls=0,installations=0,game_starts=0,RPM_reads=0,gameplay_acceptance=False)
write('type10-checks.json',json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
