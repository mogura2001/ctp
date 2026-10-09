"""Independent readback of H3 PE/bytes/CFG/ABI and protected inventories.

Does not import the H3 emitter/model or run an emulator. pefile/Capstone are the
already present local libraries. All executed native evidence is separate.
"""
from pathlib import Path
import sys,json,struct,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from capstone.x86_const import X86_OP_MEM,X86_OP_IMM,X86_REG_EBP
sha=lambda b:hashlib.sha256(b).hexdigest()
original=(OUT/'backup/robotcom.original.dll').read_bytes();candidate=(OUT/'candidates/H3-SCORE_CURRENT/robotcom.dll').read_bytes()
manifest=json.loads((OUT/'H3-SCORE_CURRENT.manifest.json').read_text());p=pefile.PE(data=candidate);op=pefile.PE(data=original)
assert sha(original)==manifest['original_sha256']=='3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
assert sha(candidate)==manifest['candidate_sha256']
assert sha((ROOT/'ONTWERP/PRODUCTIELOCATIES-H3.md').read_bytes())==manifest['design_sha256']=='be16e3844ca7ae0396bd31ac28478855ff906c4091b529605e0bd91a41a71248'
assert p.FILE_HEADER.NumberOfSections==5 and p.FILE_HEADER.TimeDateStamp==0x37b894e7 and p.OPTIONAL_HEADER.ImageBase==0x20000000
section=p.sections[-1];assert(section.Name,section.VirtualAddress,section.PointerToRawData,section.Characteristics)==(b'.h3\0\0\0\0\0',0xd4000,0xa1400,0x60000020)
assert len(candidate)==0xa1400+section.SizeOfRawData
assert p.OPTIONAL_HEADER.SizeOfImage==(0xd4000+section.Misc_VirtualSize+0xfff)&~0xfff
assert p.OPTIONAL_HEADER.SizeOfCode==op.OPTIONAL_HEADER.SizeOfCode+section.SizeOfRawData
assert p.OPTIONAL_HEADER.CheckSum==p.generate_checksum()
assert candidate[0xa1400+section.Misc_VirtualSize:]==bytes(section.SizeOfRawData-section.Misc_VirtualSize)
for old,new in zip(op.sections,p.sections):assert old.__pack__()==new.__pack__()
assert [d.__pack__() for d in op.OPTIONAL_HEADER.DATA_DIRECTORY]==[d.__pack__() for d in p.OPTIONAL_HEADER.DATA_DIRECTORY]
allowed=set(range(0x250,0x278))
for obj,field,size in [(op.FILE_HEADER,'NumberOfSections',2),(op.OPTIONAL_HEADER,'SizeOfCode',4),(op.OPTIONAL_HEADER,'SizeOfImage',4),(op.OPTIONAL_HEADER,'CheckSum',4)]:
 at=obj.get_field_absolute_offset(field);allowed.update(range(at,at+size))
for site in (0x784bb,0x78517,0x7aa35):
 at=op.get_offset_from_rva(site);b=candidate[at:at+6];assert b[0]==0xe8 and b[5]==0x90 and site+5+struct.unpack('<i',b[1:5])[0]==0xd4000;allowed.update(range(at,at+6))
actual={i for i in range(len(original)) if original[i]!=candidate[i]};assert actual<=allowed
for change in manifest['changes']:
 at=int(change['offset'],16);before=bytes.fromhex(change['before']);after=bytes.fromhex(change['after']);assert original[at:at+len(before)]==before and candidate[at:at+len(after)]==after
code=p.get_data(0xd4000,section.Misc_VirtualSize);assert code==(OUT/'H3-SCORE_CURRENT.payload.bin').read_bytes() and sha(code)==manifest['payload_sha256']
md=Cs(CS_ARCH_X86,CS_MODE_32);md.detail=True;rows=list(md.disasm(code,0xd4000));assert sum(i.size for i in rows)==len(code);by={i.address:i for i in rows}
labels={n:0xd4000+v for n,v in manifest['labels'].items()}
functions=[('adapter',16,1120),('classifier',16,32),('capacity',16,224),('food_reader',20,80),('poscmp',8,0),('current_model',20,384),('plan_select',4,256),('development_tile',28,192),('development_model',24,1216),('explain_development',20,32),('host_validator',12,0)]
abis={labels[n]:pop for n,pop,_ in functions}
cfg=[]
for index,(name,pop,allocation) in enumerate(functions):
 start=labels[name];end=labels[functions[index+1][0]] if index+1<len(functions) else 0xd4000+len(code)
 seen=set();pending=[(start,0)];returns=[];calls=[];reached=set()
 while pending:
  addr,delta=pending.pop()
  if(addr,delta) in seen:continue
  assert start<=addr<end and addr in by,(name,hex(addr));seen.add((addr,delta));reached.add(addr);i=by[addr];nextaddr=addr+i.size;mn=i.mnemonic
  # Native pointer validity is a documented caller precondition. Every own EBP
  # scratch access nevertheless lies within allocated frame or arguments.
  for operand in i.operands:
   if operand.type==X86_OP_MEM:
    assert operand.mem.base or operand.mem.index,'production absolute pointer'
    if operand.mem.base==X86_REG_EBP and name not in ('poscmp','host_validator'):
     disp=operand.mem.disp;assert -allocation-12<=disp and disp+operand.size<=pop+8,(name,i.op_str)
  if mn=='push':delta-=4
  elif mn=='pop':delta+=4
  elif mn in ('sub','add') and i.op_str.startswith('esp, '):delta+=(1 if mn=='add' else -1)*i.operands[1].imm
  elif mn=='call':
   if i.operands[0].type==X86_OP_IMM:
    target=i.operands[0].imm
    if target==nextaddr:assert name=='adapter';delta-=4
    else:assert target in abis,(name,hex(target));delta+=abis[target];calls.append({'at':hex(addr),'callee':hex(target),'pop':abis[target]})
   else:
    o=i.operands[0]
    if o.type==X86_OP_MEM:
     slot=o.mem.disp
     expected={'adapter':{0x168:16},'capacity':{0x28:8,0xac:20,0xa8:12},'food_reader':{20:4,0xb8:12},'development_tile':{0x10:8,0x20:20,0x48:12}}
     assert slot in expected[name],(name,i.op_str);delta+=expected[name][slot];calls.append({'at':hex(addr),'slot':hex(slot),'pop':expected[name][slot]})
    else:raise AssertionError('unexpected production call')
  if mn=='ret':assert delta==0 and i.operands[0].imm==pop,(name,delta,pop);returns.append(hex(addr));continue
  if mn.startswith('j'):
   target=i.operands[0].imm;assert target in by;pending.append((target,delta))
   if mn=='jmp':continue
  assert nextaddr<end;pending.append((nextaddr,delta))
 assert returns and reached=={i.address for i in rows if start<=i.address<end},name
 cfg.append({'function':name,'bytes':end-start,'ret_pop':pop,'all_cfg_paths_stack_balanced':True,'reachable_instructions':len(reached),'returns':returns,'calls':calls})
# Dynamic-call hot path has no Improvement slots or developmententry. The sole
# production binding is exact original validator; no helper pointer/fallback.
adaptercalls=cfg[0]['calls'];assert [v.get('slot') for v in adaptercalls if 'slot' in v]==['0x168']
assert any(v.get('callee')==hex(labels['classifier']) for v in adaptercalls)
current_names={'adapter','classifier','capacity','food_reader','poscmp','current_model','plan_select','host_validator'}
for rec in cfg:
 if rec['function'] in current_names:
  assert not any(c.get('callee') in [hex(labels[n]) for n in ('development_tile','development_model','explain_development')] for c in rec['calls'])
validator=(OUT/'host/validator.prepared.bin').read_bytes();assert code[labels['host_validator']-0xd4000:]==validator
assert any(i.mnemonic=='cmp' and i.op_str=='esi, 0x400000' for i in rows if i.address>=labels['host_validator'])
assert any(i.mnemonic=='movsx' and i.op_str=='eax, ax' for i in rows if i.address<labels['classifier'])
assert any(i.mnemonic=='movsx' and i.op_str=='eax, word ptr [esi + 0xc6fb0]' for i in rows if i.address<labels['classifier'])
assert any(i.mnemonic=='fnsave' for i in rows) and any(i.mnemonic=='frstor' for i in rows)
helpers={}
expected={'shim3':0,'shim4':0,'shim5':0,'shim6':0,'shim7':0,'score':16,'gate':8,'open':20,'terrain':12,'food':12,'convert':4,'available':8,'position':20,'delta':12,'fixture-classifier':16}
for name,pop in expected.items():
 raw=(OUT/'helper'/f'{name}.bin').read_bytes();ins=list(md.disasm(raw,0));assert sum(i.size for i in ins)==len(raw);assert ins[-1].mnemonic=='ret' and (ins[-1].operands[0].imm if ins[-1].operands else 0)==pop
 (OUT/'helper'/f'{name}.disassembly.txt').write_text('\n'.join(f'{i.address:04x} {i.bytes.hex():24} {i.mnemonic} {i.op_str}' for i in ins)+'\n');helpers[name]={'sha256':sha(raw),'bytes':len(raw),'ret_pop':pop}
inventory={}
for tree in ('CTP-og','CTP-AAIP','CTP-proef','PROEVEN/settlerquota/vaste-start'):
 for path in sorted((ROOT/tree).rglob('*')):
  if path.is_file():inventory[path.relative_to(ROOT).as_posix()]={'size':path.stat().st_size,'sha256':sha(path.read_bytes())}
before=json.loads((OUT/'protected-before.json').read_text());assert inventory==before and len(inventory)==3090
(OUT/'protected-after-native.json').write_text(json.dumps(inventory,indent=2)+'\n')
h1=json.loads((ROOT/'PROEVEN/score-h1/package-manifest.json').read_text());b1=h1['B1_constant_proof_files']
for desc in b1.values():assert inventory[desc['path']]=={'size':desc['size'],'sha256':desc['sha256']}
for path,desc in h1['fixed_T0_inventory'].items():assert inventory[path]==desc
t0=[path for path,desc in inventory.items() if desc['sha256']=='8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26'];assert t0
control=ROOT/'PROEVEN/score-h1/candidates/H1-I/robotcom.dll';assert sha(control.read_bytes())=='59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0'
engine=ROOT/'CTP-proef/ctp_program/ctp/civctp.exe';assert sha(engine.read_bytes())=='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
native=json.loads((OUT/'H3-SCORE_CURRENT.native-fixture.json').read_text(encoding='utf-8-sig'));loader=json.loads((OUT/'H3-SCORE_CURRENT.native-loader.json').read_text(encoding='utf-8-sig'));assert native['pass'] and loader['pass']
for record in (native,loader):assert record['candidate_sha256']==sha(candidate) and record['payload_sha256']==sha(code)
assert native['measured_peak_extra_direct_world_calls']==43 and native['measured_peak_total_direct_world_calls']==44
result={'candidate_sha256':sha(candidate),'payload_sha256':sha(code),'payload_bytes':len(code),'instructions':len(rows),'changed_original_bytes':len(actual),'functions':cfg,'helpers':helpers,'full_decode':True,'PE_diff_relocations_checksum':True,'no_production_absolute_pointer_or_fixture_fallback':True,'protected_files':len(inventory),'protected_unchanged':True,'B1_constant':b1,'fixed_T0_paths':t0,'H1_I_constant':sha(control.read_bytes()),'native_cases':native['native_cases'],'ordinary_loader':loader['pass'],'real_engine_activation':False,'gameplay_measured':False,'AI_performance_accepted':False,'pass':True}
(OUT/'offline-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('candidate_sha256','payload_bytes','instructions','protected_files','native_cases','pass')}))
