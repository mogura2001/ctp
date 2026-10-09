"""H3 build inputs only. Does not emit a classifier or candidate DLL.

Keep the H1-I control and all installations untouched. Preparation can be
resumed after the account window reset; no fallback/stub is installed.
"""
from pathlib import Path
import hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'PROEVEN/score-h1'))
import build as h1
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
DESIGN='be16e3844ca7ae0396bd31ac28478855ff906c4091b529605e0bd91a41a71248'
ENGINE='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
sha=lambda data:hashlib.sha256(data).hexdigest()
def save(name,data):
    path=OUT/name;path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():assert path.read_bytes()==data,'refuse overwriting a different prepared artifact'
    else:
        temp=path.with_suffix(path.suffix+'.tmp');temp.write_bytes(data);temp.replace(path)
def dump(name,obj):save(name,(json.dumps(obj,indent=2)+'\n').encode())
assert sha((ROOT/'ONTWERP/PRODUCTIELOCATIES-H3.md').read_bytes())==DESIGN
source=ROOT/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll'
enginepath=ROOT/'CTP-proef/ctp_program/ctp/civctp.exe'
dll=source.read_bytes();engine=enginepath.read_bytes()
assert sha(dll)==h1.HASH and sha(engine)==ENGINE
pe=pefile.PE(data=engine)
assert pe.OPTIONAL_HEADER.ImageBase==0x400000 and pe.FILE_HEADER.TimeDateStamp==0x37d6f702
assert pe.FILE_HEADER.Machine==0x14c and pe.OPTIONAL_HEADER.Magic==0x10b
assert not pe.OPTIONAL_HEADER.DllCharacteristics&0x40
assert pe.OPTIONAL_HEADER.DATA_DIRECTORY[5].VirtualAddress==0 and pe.OPTIONAL_HEADER.DATA_DIRECTORY[5].Size==0
inventory=h1.inventory()
save('backup/robotcom.original.dll',dll)
dump('protected-before.json',inventory)
# The strict host validator may compare these entire wrappers, because this
# exact engine has no relocations and only imagebase400000 is supported.
wrappers={}
for name,rva,size,tail in [('terrain',0x1342e0,47,'c20c00'),('food',0x134340,47,'c20c00')]:
    raw=pe.get_data(rva,size);assert raw.endswith(bytes.fromhex(tail))
    wrappers[name]={'rva':hex(rva),'bytes':raw.hex(),'sha256':sha(raw),'size':size}
    save(f'host/{name}-wrapper.original.bin',raw)
dump('build-inputs.json',{
 'state':'PREPARED ONLY; no H3 payload/candidate/native check yet',
 'design_sha256':DESIGN,'dll_sha256':h1.HASH,'engine_sha256':ENGINE,
 'control_variant':'H1-I','control_sha256':'59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0',
 'three_callsites':['0x784bb','0x78517','0x7aa35'],'section_rva':'0xd4000','raw_offset':'0xa1400',
 'strict_host':{'engine_base':'0x400000','timestamp':'0x37d6f702','wrappers':wrappers,
  'grid_pointer_rva':'0x67dd70','terrain_db_pointer_rva':'0x67dd3c',
  'width_word_rva':'0x67df20','height_word_rva':'0x67df22','convert_thiscall_rva':'0x103f00',
  'fixture_binding':'only an explicitly separate fixture entrypoint; never production fallback'},
 'query_ABIs':{'original_score':{'slot':'0x168','pop':16},'center_gate':{'slot':'0x28','pop':8},
  'open_tiles':{'slot':'0xac','pop':20,'raw_stride':8,'max_count':20},
  'terrain':{'slot':'0xa8','pop':12},'food':{'slot':'0xb8','pop':12},
  'improvement_available':{'slot':'0x10','pop':8},'improvement_position':{'slot':'0x20','pop':20},
  'improvement_fooddelta':{'slot':'0x48','pop':12,'result':'x87 ST0 consumed immediately'}},
 'cell_fields':{'flags':0,'terrain_signed_byte':13,'armylist':16,'cityhandle':20,'army_count':48},
 'record_fields':{'stride':192,'basefood':8,'city_environment':80,'canal_environment':84,'river_environment':88,
  'roads':[92,96,100],'irrigation':[104,108,112],'mines':[116,120,124],'goods_base':160},
 'flag_decode':{'good_local_slot':'(flags >> 6) & 7; only0..4; decrement before subrecord lookup and walk back',
  'road':'flags & 3','irrigation':'(flags >> 2) & 3','mine':'(flags >> 4) & 3','river_mask':'0x800','canal_mask':'0x200'},
 'rations':{'AiMain_PlayerInterface':44,'PlayerInterface_Player':8,'Player_WGF':4888,'WGF_double':8,'WGF_stand':72,
  'actual_factor_must_equal':'1 + 0.25*actual_stand','D_checked64':'40 + 10*actual_stand'},
 'current_contract':'four different workers; three mountains8/20/22 plus other supported Ffood>0; supported center; S0>D; +1 clamp32767; B<=0/UNKNOWN unchanged',
 'limits':{'direct_world_calls_extra':43,'direct_world_calls_including_original':44,'top3_tile_comparisons':400},
 'development':'separate mode; IRR2 and mine food deltas/costs/predicates; no future score bonus and no new IRR1 without proven wondertask',
 'protected_files':len(inventory),
 'remaining':'emit actual host-validator/modelreader/H2/top3/current-plan/development; integrate score adapter; independent offline plus native fixtures/loader/rebase; final inventory'
})
assert h1.inventory()==inventory
print(json.dumps({'prepared':True,'candidate_built':False,'protected_files':len(inventory),'design_sha256':DESIGN,'host_wrappers':wrappers},indent=2))
