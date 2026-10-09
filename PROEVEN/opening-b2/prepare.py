"""Frozen B2a inputs/preimages only; not a candidate or completed B2a build.

The five integrated adapters and N25/N30 native fixtures remain separate work.
No installation or game/process/handler action. Existing packages read-only.
"""
from pathlib import Path
import sys,json,hashlib,struct
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
DESIGN='ea5140b5505c11f457bdcdc3cf41fcc023e277bf247866228ad356919c9ef40e'
DLL='3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
ENGINE='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(name,data):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():assert p.read_bytes()==data,'refuse different prepared artifact: '+str(p)
 else:p.write_bytes(data)
def dump(name,obj):save(name,(json.dumps(obj,indent=2)+'\n').encode())
assert sha((ROOT/'ONTWERP/GEZAMENLIJKE-OPENING-B2.md').read_bytes())==DESIGN
dllpath=ROOT/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll';enginepath=ROOT/'CTP-proef/ctp_program/ctp/civctp.exe'
dll=dllpath.read_bytes();engine=enginepath.read_bytes();assert sha(dll)==DLL and sha(engine)==ENGINE
dp=pefile.PE(data=dll);ep=pefile.PE(data=engine)
assert(dp.FILE_HEADER.Machine,dp.FILE_HEADER.TimeDateStamp,dp.OPTIONAL_HEADER.ImageBase)==(0x14c,0x37b894e7,0x20000000)
assert(ep.FILE_HEADER.Machine,ep.FILE_HEADER.TimeDateStamp,ep.OPTIONAL_HEADER.ImageBase)==(0x14c,0x37d6f702,0x400000)
assert not ep.OPTIONAL_HEADER.DllCharacteristics&0x40 and not ep.OPTIONAL_HEADER.DATA_DIRECTORY[5].VirtualAddress and not ep.OPTIONAL_HEADER.DATA_DIRECTORY[5].Size
save('backup/robotcom.original.dll',dll)
inventory={}
for tree in ('CTP-og','CTP-AAIP','CTP-proef','PROEVEN/settlerquota/vaste-start'):
 for p in sorted((ROOT/tree).rglob('*')):
  if p.is_file():inventory[p.relative_to(ROOT).as_posix()]={'size':p.stat().st_size,'sha256':sha(p.read_bytes())}
assert len(inventory)==3090;dump('protected-before.json',inventory)
oldpackages={}
for package in ('score-h1','production-h3'):
 for p in sorted((ROOT/'PROEVEN'/package).rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:oldpackages[p.relative_to(ROOT).as_posix()]={'size':p.stat().st_size,'sha256':sha(p.read_bytes())}
dump('previous-packages-before.json',oldpackages)
md=Cs(CS_ARCH_X86,CS_MODE_32)
sites={}
for name,rva,preimage,target in [('registration',0x413da,'e81178ffff',0x38bf0),('beginturn',0x3625b,'e8902d0000',0x38ff0),('save',0xfe2d,'e88e29ffff',0x27c0),('load',0xfe51,'e8fa2dffff',0x2c50),('reload_entry',0x61f0,'558bec5356',None)]:
 raw=dp.get_data(rva,5);assert raw.hex()==preimage;rows=list(md.disasm(raw,0x20000000+rva));assert sum(i.size for i in rows)==5
 if target is not None:assert rows[0].mnemonic=='call' and rva+5+struct.unpack('<i',raw[1:])[0]==target
 else:assert [(i.mnemonic,i.op_str) for i in rows]==[('push','ebp'),('mov','ebp, esp'),('push','ebx'),('push','esi')]
 sites[name]={'rva':hex(rva),'raw_offset':hex(dp.get_offset_from_rva(rva)),'preimage':raw.hex(),'original_target_rva':hex(target) if target else None,'return_rva':hex(rva+5),'disassembly':[f'{i.mnemonic} {i.op_str}' for i in rows]}
save('host/archive-vtable.original.bin',ep.get_data(0x3462a8,24))
vtable=struct.unpack('<6I',ep.get_data(0x3462a8,24));assert vtable[3:]==(0x586930,0x5869f0,0x586c70)
fingerprints={}
for name,rva,size in [('archive_store',0x186930,32),('archive_load',0x1869f0,32),('archive_mode',0x186c70,16),('fatal_handler',0x1560,0x47),('load_manager_zero_branch',0x12dec8,0x16)]:
 raw=ep.get_data(rva,size);save('host/'+name+'.original.bin',raw);fingerprints[name]={'rva':hex(rva),'size':len(raw),'bytes':raw.hex(),'sha256':sha(raw)}
dump('build-inputs.json',{'state':'PREPARED FROZEN INPUTS ONLY; integrated five-hook B2a candidate not built',
 'design_sha256':DESIGN,'original_dll_sha256':DLL,'engine_sha256':ENGINE,'sites':sites,'engine_base':'0x400000','engine_timestamp':'0x37d6f702','engine_relocations':False,
 'existing_PE':{'section_count':4,'file_alignment':dp.OPTIONAL_HEADER.FileAlignment,'section_alignment':dp.OPTIONAL_HEADER.SectionAlignment,'image_size':hex(dp.OPTIONAL_HEADER.SizeOfImage),'append_raw':hex(len(dll)),'append_rva':'0xd4000'},
 'functions':{'AddSymbol':'0x38bf0','GetSymbol':'0x389e0','RegisterInit':'0x3bf50','SetValue':'0x3b790','FireRules':'0x38ff0','AiMain_Save':'0x27c0','AiMain_Load':'0x2c50','ReloadFuzzyLogic':'0x61f0'},
 'AiMain_fields':{'civ':0x20,'PlayerInterface':0x2c,'cities_object':0x8c,'FliEngine':0xc4},
 'symbol_fields':{'double':8,'external_pointer':4,'section_init_mask':0x68,'section_input_mask':0xc2,'section_bit':4},
 'archive_contract':{'vtable_rva':'0x3462a8','Store_slot':12,'Load_slot':16,'IsStoring_slot':20,'mode_byte':8,'capacity_u32':12,'size_u32':16,'buffer_pointer':20,'cursor_pointer':24,'Store_rva':'0x186930','Load_rva':'0x1869f0','IsStoring_rva':'0x186c70','bounds':'checked unsigned32; size<=capacity; buffer interval no overflow; buffer<=cursor; offset<=size'},
 'record':{'marker_hex':'4354503142324f50454e535441544521','version':1,'length':36,'civ_offset':24,'completed_offset':28,'N_offset':32,'fixture_parameters':[25,30],'production_N_chosen':False},
 'fault_contract':{'Load':'EAX0, ret8; RobotCom preservesresult; manager zero branch calls401560 before next civ','Save':'void; verified host only cdecl title/format to401560, unexpectedreturn UD2; no success continuation','unknown_host':'no concrete enginememory or handlercall'},
 'fingerprints':fingerprints,'scope':'B2a only; no FLI/AIP consequents/actions, H3 combination, installation, GUI/livegame/export/real fatal handler',
 'remaining':'emit and integrate registration/beginturn/Save/Load/reloadtrampoline; archiveguard/boundedpeek/record/latch; exact native fixturesN25+N30 with explicit fatal stubs; independent PE/ABI/CFG/loader/rebase/inventory checks'})
after={path:{'size':(ROOT/path).stat().st_size,'sha256':sha((ROOT/path).read_bytes())} for path in inventory};assert after==inventory;dump('protected-after-preparation.json',after)
assert all(sha((ROOT/path).read_bytes())==desc['sha256'] for path,desc in oldpackages.items())
print(json.dumps({'prepared':True,'candidate_built':False,'protected_files':len(inventory),'previous_package_files_unchanged':len(oldpackages),'frozen_design':DESIGN,'five_preimages_verified':True}))
