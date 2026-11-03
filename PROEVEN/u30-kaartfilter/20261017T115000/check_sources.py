"""Finite AST/layout/frozen-pin checks only. Does not compose or invoke code."""
from pathlib import Path
import ast,datetime,hashlib,json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
OLD=ROOT/'PROEVEN/u30-type10/20261015T194300'
sha=lambda b:hashlib.sha256(b).hexdigest()
def parsed(p):return ast.parse(p.read_text('utf-8'))
def functions(p):return {n.name:ast.dump(n) for n in parsed(p).body if isinstance(n,ast.FunctionDef)}
def assigned(p,name):
 return next(n.value for n in parsed(p).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
def named_constants(p,name):return {k.arg:ast.literal_eval(k.value) for k in assigned(p,name).keywords}
for p in OUT.rglob('*.py'):parsed(p)
preserved={}
for name,changed in [('native.py',{'roles'}),('policy.py',{'canonical_prefix'}),('integration_base.py',{'host'})]:
 a=functions(OLD/name);b=functions(OUT/name);assert a.keys()==b.keys()
 assert all(a[k]==b[k] for k in a.keys()-changed)
 preserved[name]=sorted(a.keys()-changed)
oldp=named_constants(OLD/'native.py','P');newp=named_constants(OUT/'native.py','P')
assert all(newp[k]==v for k,v in oldp.items())
assert {k:v for k,v in newp.items() if k not in oldp}==dict(prefix_count=224,known_count=228,gate_queries=232,gate_false=236)
occupied=set()
for offset in newp.values():
 extent=set(range(offset,offset+4));assert not extent&occupied;occupied|=extent
assert not occupied&set(range(144,168)) and 239<0x200
arrays=['CAPTURE','CAPTURE_CAP','PREVIEW','PREVIEW_CAP','PREVIEW_STRIDE','DEPARTURES','DEPARTURE_CAP','DEPARTURE_STRIDE','VISITED','NODE_CAP','NODE_STRIDE','STACK','STACK_CAP','HINTS','HINT_CAP','HINT_STRIDE','SLOTS','SLOT_CAP','SLOT_STRIDE','SELECTED','SELECTED_CAP','ORDER','PATHCACHE','PATHCACHE_CAP','PATHCACHE_STRIDE','PLAN_SIZE']
for k in arrays:assert ast.dump(assigned(OLD/'native.py',k))==ast.dump(assigned(OUT/'native.py',k))
assert ast.dump(assigned(OLD/'input-pins.py','SLOTS'))==ast.dump(assigned(OUT/'input-pins.py','SLOTS'))
pins=json.loads((OUT/'input-pins.json').read_text('utf-8'));originalpins=json.loads((OLD/'input-pins.json').read_text('utf-8'))
for row in originalpins['bodies']:assert row in pins['bodies']
assert pins['slots']==originalpins['slots']
extra=[r for r in pins['bodies'] if r not in originalpins['bodies']]
assert {(r['rva'],r['length']) for r in extra}=={(0x133580,37),(0xbbd50,28),(0xebdf0,115)}
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
engine=(ROOT/'CTP-proef/ctp_program/ctp/civctp.exe').read_bytes();assert sha(engine)==pins['engine_sha256']
pe=pefile.PE(data=engine);assert pe.OPTIONAL_HEADER.ImageBase==0x400000 and pe.FILE_HEADER.TimeDateStamp==0x37d6f702
assert int.from_bytes(pe.get_data(0x345308,4),'little')==0x533580
decode=Cs(CS_ARCH_X86,CS_MODE_32);bodyrows=[]
for row in extra:
 raw=bytes.fromhex(row['bytes']);assert raw==pe.get_data(row['rva'],row['length'])
 ins=list(decode.disasm(raw,0x400000+row['rva']));assert sum(i.size for i in ins)==len(raw) and ins[-1].mnemonic=='ret'
 bodyrows.append(dict(**row,sha256=sha(raw),last_address=hex(ins[-1].address),last_instruction=ins[-1].mnemonic+' '+ins[-1].op_str,end_exclusive=hex(ins[-1].address+ins[-1].size),instructions=[f'{i.address:08x} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for i in ins]))
(OUT/'gate-body-pins.json').write_text(json.dumps(bodyrows,indent=2)+'\n','utf-8')
prep=json.loads((OUT/'preparation-manifest.json').read_text('utf-8'))
for row in prep['release_pins']+prep['proposals']+prep['source_pins']:assert sha((ROOT/row['path']).read_bytes())==row['sha256'],row['path']
assert not (OUT/'U30-40.prepared.dll').exists() and not (OUT/'candidate-manifest.json').exists()
rp=json.loads((OUT/'reader/runtime-pins.json').read_text('utf-8'));assert rp['candidate_sha256'] is None and rp['manifest_sha256'] is None and rp['state_rva'] is None
reader=(OUT/'reader/Lees-Uitbreiding.py').read_text('utf-8')
assert "shared['classified']==1" not in reader
assert all(f'{k}={v}' in reader for k,v in newp.items() if k not in oldp)
result=dict(stage='SOURCE_AST_LAYOUT_PIN_ONLY_NOT_CANDIDATE_OR_RUNTIME',checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),ast_valid=True,old_functions_ast_unchanged=preserved,old_header_offsets_and_arrays_unchanged=True,new_fields={k:v for k,v in newp.items() if k not in oldp},new_header_disjoint=True,new_engine_bodies=len(extra),all_old_body_and_unitdb_slot_pins_retained=True,all_preparation_pins_match=True,reader_runtime_pins_unset_fail_closed=True,builds=0,native_compiles=0,native_calls=0,rpm=0,installations=0,game_starts=0,gameplay_acceptance=False)
(OUT/'source-checks.json').write_text(json.dumps(result,indent=2)+'\n','utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='old_functions_ast_unchanged'}))
