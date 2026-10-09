"""Independent bounded PE/bytes/CFG/ABI/evidence/inventory checks. Read-only game."""
from pathlib import Path
import sys,json,struct,hashlib,runpy
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
sha=lambda b:hashlib.sha256(b).hexdigest()
inputs=json.loads((OUT/'build-inputs.json').read_text());original=(OUT/'backup/robotcom.original.dll').read_bytes();op=pefile.PE(data=original)
assert sha(original)==inputs['original_dll_sha256'];assert sha((ROOT/'ONTWERP/GEZAMENLIJKE-OPENING-B2.md').read_bytes())==inputs['design_sha256'];assert sha((ROOT/'CTP-proef/ctp_program/ctp/civctp.exe').read_bytes())==inputs['engine_sha256']
assert inputs['symbol_fields']['external_pointer']==0
md=Cs(CS_ARCH_X86,CS_MODE_32);variants=[]
builder=runpy.run_path(str(OUT/'build.py'))
for N in (25,30):
 name=f'B2a-N{N}-TECHNICAL';manifest=json.loads((OUT/(name+'.manifest.json')).read_text());data=(OUT/'candidates'/name/'robotcom.dll').read_bytes();payload=(OUT/(name+'.payload.bin')).read_bytes();p=pefile.PE(data=data)
 assert sha(data)==manifest['candidate_sha256'] and sha(payload)==manifest['payload_sha256']
 regenerated,regen_payload,regen_manifest=builder['build'](N);assert(data,payload,manifest)==(regenerated,regen_payload,regen_manifest)
 # Independently apply only documented writes; their preimages must still be
 # exactoriginal; no appended-code window is excused inside original sections.
 expected=bytearray(original);allowed=set()
 for delta in manifest['changes']:
  at=int(delta['offset'],16);before=bytes.fromhex(delta['before']);after=bytes.fromhex(delta['after']);assert len(before)==len(after);assert original[at:at+len(before)]==before;assert not allowed.intersection(range(at,at+len(after)));allowed.update(range(at,at+len(after)));expected[at:at+len(after)]=after
 assert data[:len(original)]==expected;assert data[len(original):len(original)+len(payload)]==payload;assert not any(data[len(original)+len(payload):])
 assert p.FILE_HEADER.NumberOfSections==5 and p.sections[-1].Name.rstrip(b'\0')==b'.b2a' and p.sections[-1].Characteristics==0x60000020
 assert p.sections[-1].VirtualAddress==0xd4000 and p.sections[-1].PointerToRawData==len(original) and p.sections[-1].Misc_VirtualSize==len(payload)
 assert p.OPTIONAL_HEADER.SizeOfImage%4096==0 and len(data)%512==0 and p.OPTIONAL_HEADER.CheckSum==p.generate_checksum()
 # Original relocation/import data stays exact. All new code/data addresses
 # are PIC/base+RVA; there are no new absolute-memory operands to relocate.
 assert [d.__dict__.get('VirtualAddress') for d in p.OPTIONAL_HEADER.DATA_DIRECTORY]==[d.__dict__.get('VirtualAddress') for d in op.OPTIONAL_HEADER.DATA_DIRECTORY]
 assert [(s.VirtualAddress,s.PointerToRawData,s.SizeOfRawData,s.Characteristics) for s in p.sections[:4]]==[(s.VirtualAddress,s.PointerToRawData,s.SizeOfRawData,s.Characteristics) for s in op.sections]
 rows=list(md.disasm(payload[:manifest['code_size']],0xd4000));assert sum(i.size for i in rows)==manifest['code_size'];boundaries={i.address for i in rows};labels=manifest['labels']
 original_targets={0x38bf0,0x389e0,0x3bf50,0x3b790,0x38ff0,0x27c0,0x2c50,0x61f5}
 for i in rows:
  if i.mnemonic.startswith('j') or i.mnemonic=='call':
   if i.op_str.startswith('0x'):assert int(i.op_str,16) in boundaries|original_targets,(i.address,i.op_str)
  assert not ('ptr [0x' in i.op_str),(hex(i.address),i.op_str)
 for site_name,site in inputs['sites'].items():
  rva=int(site['rva'],16);at=p.get_offset_from_rva(rva);raw=data[at:at+5];assert raw[0]==(0xe9 if site_name=='reload_entry' else 0xe8);label='reload' if site_name=='reload_entry' else site_name;assert rva+5+struct.unpack('<i',raw[1:])[0]==0xd4000+labels[label]
 assert payload[labels['reload_trampoline']:labels['reload_trampoline']+5]==bytes.fromhex(inputs['sites']['reload_entry']['preimage'])
 # The body after each wrapper's original call ends with MOV ESP/POP EBP/RET,
 # not a flag-changing epilogue. Correct thiscall stack cleanup is explicit.
 for label,pop,next_label in [('registration',20,'beginturn'),('beginturn',4,'save'),('load',8,'reload'),('reload',4,'reload_trampoline')]:
  part=payload[labels[label]:labels[next_label]];assert bytes.fromhex('8be55dc2')+struct.pack('<H',pop) in part
 assert b'\x8b\x84\x24\x1c\x00\x00\x00' in payload # snapshot exposes original EAX at pushad+28
 assert payload[labels['trap']:labels['trap']+2]==b'\x0f\x0b'
 fatalrows=[i for i in rows if 0xd4000+labels['fatal_save']<=i.address<0xd4000+labels['archive']];assert fatalrows[-1].mnemonic=='ud2' and any(i.mnemonic=='lea' and '0x1560' in i.op_str for i in fatalrows)
 peekrows=[i for i in rows if 0xd4000+labels['peek']<=i.address<0xd4000+labels['trap']];assert not any(i.mnemonic=='call' for i in peekrows) # no consuming peek/cursor rewind
 for mode in ('fixture','loader'):
  native=json.loads((OUT/(name+'.native-'+mode+'.json')).read_text(encoding='utf-8-sig'));assert native['pass'] and native['candidate_sha256']==sha(data) and native['bitness']==32
  if mode=='fixture':assert native['actual_rebase'] and native['mapped_candidate_unchanged'] and native['cases']>=88
 variants.append({'variant':name,'N_fixture':N,'candidate_sha256':sha(data),'payload_bytes':len(payload),'decoded_instructions':len(rows),'native_cases':native.get('cases',json.loads((OUT/(name+'.native-fixture.json')).read_text(encoding='utf-8-sig'))['cases']),'deterministic':True,'PE_diff_CFG_ABI':True})
# Check the concrete original engine zero branch independently of fixture code.
branch=(OUT/'host/load_manager_zero_branch.original.bin').read_bytes();br=list(md.disasm(branch,0x52dec8));assert [(i.mnemonic,i.op_str) for i in br[:2]]==[('test','eax, eax'),('jne','0x52dede')];assert any(i.mnemonic=='call' and i.op_str=='0x401560' for i in br);assert br[-1].mnemonic=='add' and br[-1].op_str=='esp, 8'
# Finite stub recipes also decode completely; all helper pointers are explicit
# owned fixups, absent from production candidates.
for path in (OUT/'helper').glob('*.bin'):
 b=path.read_bytes();assert sum(i.size for i in md.disasm(b,0))==len(b),path
inventory=json.loads((OUT/'protected-before.json').read_text());after={path:{'size':(ROOT/path).stat().st_size,'sha256':sha((ROOT/path).read_bytes())} for path in inventory};assert after==inventory
actual=set()
for tree in ('CTP-og','CTP-AAIP','CTP-proef','PROEVEN/settlerquota/vaste-start'):
 actual.update(p.relative_to(ROOT).as_posix() for p in (ROOT/tree).rglob('*') if p.is_file())
assert actual==set(inventory)
old=json.loads((OUT/'previous-packages-before.json').read_text());assert all({'size':(ROOT/path).stat().st_size,'sha256':sha((ROOT/path).read_bytes())}==desc for path,desc in old.items())
(OUT/'protected-after-native.json').write_text(json.dumps(after,indent=2)+'\n')
result={'status':'OFFLINE CHECKED; candidate only, not installed or gameplay measured','variants':variants,'protected_files_unchanged':len(after),'previous_package_files_unchanged':len(old),'five_hook_preimages_and_targets':True,'concrete_Load0_parent_fatal_branch':True,'save_cdecl_fatal_no_success_return':True,'legacy_cursor_native_fixtures':True,'original_T0_unchanged':True,'actual_engine_T0_load_or_active_Theocracy_binding_measured':False,'production_N_chosen':False,'pass':True}
(OUT/'offline-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
