"""C1 append-only standalone kernel build, science credit off, no native calls."""
from pathlib import Path
import sys,struct,json,hashlib,ast,difflib
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
sys.path.insert(0,str(OUT))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from x86 import X86
from science_model import model
import science_layout as layout
sha=lambda b:hashlib.sha256(b).hexdigest()
align=lambda n,a:(n+a-1)//a*a
BASE_HASH='f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810'
ENGINE_HASH='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
INPUTS={
 'ONTWERP/SCIENCELOCATIES-U30-40.md':'a66afdbf3fb74311092bfcde327783f444560c29948f15439eb372b6a7456cdb',
 'ANALYSE/SCIENCELOCATIES-INGREEP.md':'add49b19c83f70d1f1e452c37510cc53821d2932856afe1e1c5e2455f2a9e00a',
 'ANALYSE/SCIENCELOCATIES-FOODLEGALITEIT.md':'714eb177c658826f139831e7d8920778b655eb9664394b3895315bc4e3a777db',
 'PROEVEN/uitbreiding-30-40/20261012T181500/candidate-manifest.json':'9b2146579b7ccf3a8133850c360e7b0c934565998078fa7ae140a6b10f6e5341',
}
SPATIAL_RANGES=[('World_interface_slot34',0x345314,4),
 ('spatial_external_wrapper',0x133620,0x25),('spatial_internal',0x116c40,0x83),
 ('native_World_vtable_slot0',0x344170,4),('native_World_callback',0x1107b0,0x178),
 ('native_scan9',0x9fdd0,0x103),('native_wrap',0x9fb20,32),
 ('native_cellflag_predicate',0x114bc0,0x30),
 ('improvement_availability_slot',0x3445c8,4),
 ('improvement_place_slot',0x3445d8,4),
 ('improvement_delta_slot',0x344600,4),
 ('improvement_availability_body',0x126a40,0x8a),
 ('improvement_place_body',0x126ad0,0xbf),
 ('improvement_delta_body',0x126d50,0x4a)]
class Located(X86):
 def __init__(self,base):super().__init__();self.base=base
 def finish(self):
  for at,label,absolute in self.fix:
   assert label in self.labels,label
   value=self.base+self.labels[label] if absolute else self.labels[label]-at-4
   struct.pack_into('<I' if absolute else '<i',self.code,at,value)
  for row in self.rows:row['bytes']=self.code[row['offset']:row['offset']+len(bytes.fromhex(row['bytes']))].hex()
  return bytes(self.code)
def build():
 for path,expected in INPUTS.items():assert sha((ROOT/path).read_bytes())==expected,path
 shared=json.loads((OUT/'shared-copy-pins.json').read_text('utf-8-sig'))
 for row in shared:assert sha((OUT/row['path']).read_bytes())==row['sha256'],row['path']
 preservation=json.loads((OUT/'preservation-pins.json').read_text('utf-8-sig'))
 for row in preservation['dependencies']+preservation['protected_files']:
  assert sha((ROOT/row['path']).read_bytes())==row['sha256'],row['path']
 checkpoint=json.loads((OUT/'checkpoint-v1/archive-pins.json').read_text('utf-8-sig'))
 for row in checkpoint:assert sha((OUT/'checkpoint-v1'/row['name']).read_bytes())==row['sha256'],row['name']
 base=(OUT/'U30-40.control.backup.dll').read_bytes();assert sha(base)==BASE_HASH
 assert sha((ROOT/'PROEVEN/uitbreiding-30-40/20261012T181500/U30-40.prepared.dll').read_bytes())==BASE_HASH
 epbytes=(ROOT/'CTP-og/ctp_program/ctp/civctp.exe').read_bytes();assert sha(epbytes)==ENGINE_HASH
 assert (ROOT/'CTP-proef/ctp_program/ctp/civctp.exe').read_bytes()==epbytes
 ep=pefile.PE(data=epbytes);assert ep.OPTIONAL_HEADER.ImageBase==0x400000 and ep.FILE_HEADER.TimeDateStamp==0x37d6f702
 pins=[dict(name=name,rva=rva,length=size,bytes=ep.get_data(rva,size).hex()) for name,rva,size in SPATIAL_RANGES]
 assert pins[0]['bytes']==struct.pack('<I',0x533620).hex()
 assert pins[3]['bytes']==struct.pack('<I',0x5107b0).hex()
 for index,target in ((8,0x526a40),(9,0x526ad0),(10,0x526d50)):assert pins[index]['bytes']==struct.pack('<I',target).hex()
 p=pefile.PE(data=base);rx=align(p.OPTIONAL_HEADER.SizeOfImage,0x1000);r=Located(rx)
 cm=json.loads((ROOT/'PROEVEN/uitbreiding-30-40/20261012T181500/candidate-manifest.json').read_text('utf-8'))
 h3=int(cm['components']['internal_H3_rva'],16)
 for own,old in [('H3Host','host_validator'),('H3Capacity','capacity'),('H3FoodReader','food_reader'),('H3PosCompare','poscmp'),('H3DevelopmentTile','development_tile')]:r.labels[own]=h3+cm['h3_labels'][old]-rx
 model(r,pins);code=r.finish();dis=Cs(CS_ARCH_X86,CS_MODE_32);decoded=[]
 for row in r.rows:
  raw=bytes.fromhex(row['bytes']);rows=list(dis.disasm(raw,0x20000000+rx+row['offset']));assert sum(i.size for i in rows)==len(raw),(row,rows);decoded.extend(rows)
 data=bytearray(base);changes=[]
 def change(at,raw,why):
  before=bytes(data[at:at+len(raw)]);data[at:at+len(raw)]=raw;changes.append(dict(offset=at,length=len(raw),before=before.hex(),after=raw.hex(),reason=why))
 header=p.sections[-1].get_file_offset()+40;assert not any(base[header:header+40]);assert header+40<=p.OPTIONAL_HEADER.SizeOfHeaders
 rawsize=align(len(code),p.OPTIONAL_HEADER.FileAlignment);rawstart=len(base)
 change(header,struct.pack('<8sIIIIIIHHI',b'.sci1',len(code),rx,rawsize,rawstart,0,0,0,0,0x60000020),'new unreferenced RX standalone science kernel; credit off')
 change(p.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),struct.pack('<H',p.FILE_HEADER.NumberOfSections+1),'PE NumberOfSections')
 for field,value in [('SizeOfImage',align(rx+len(code),p.OPTIONAL_HEADER.SectionAlignment)),('SizeOfCode',p.OPTIONAL_HEADER.SizeOfCode+rawsize)]:change(p.OPTIONAL_HEADER.get_field_absolute_offset(field),struct.pack('<I',value),'PE '+field)
 data.extend(code+bytes(rawsize-len(code)));change(p.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum'),struct.pack('<I',pefile.PE(data=data).generate_checksum()),'PE CheckSum')
 cp=pefile.PE(data=data)
 # Entire existing code/data/relocations unchanged, except named PE metadata.
 allowed=set()
 for row in changes:
  extent=set(range(row['offset'],row['offset']+row['length']));assert not extent & allowed;allowed|=extent
 changed=[i for i in range(len(base)) if base[i]!=data[i]];assert all(i in allowed for i in changed)
 for section in p.sections:assert cp.get_data(section.VirtualAddress,section.Misc_VirtualSize)==p.get_data(section.VirtualAddress,section.Misc_VirtualSize)
 rel=lambda pe:[(e.rva,e.type) for block in pe.DIRECTORY_ENTRY_BASERELOC for e in block.entries]
 assert rel(cp)==rel(p)
 release=(OUT/'release-v1.control.backup.dll').read_bytes();assert sha(release)=='eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'
 rp=pefile.PE(data=release);b2size=cm['b2_preserved']['payload_size'];assert cp.get_data(0xd4000,b2size)==rp.get_data(0xd4000,b2size)
 prep=json.loads((ROOT/'PROEVEN/uitbreiding-30-40/20261012T181500/preparation-manifest.json').read_text('utf-8'))
 for row in prep['b2_hooks']:assert cp.get_data(int(row['rva'],16),5).hex()==row['bytes']
 for row in prep['windows']:assert cp.get_data(int(row['rva'],16),len(bytes.fromhex(row['preimage'])))==p.get_data(int(row['rva'],16),len(bytes.fromhex(row['preimage'])))
 installed=[]
 for row in prep['release_pins']:
  actual=sha((ROOT/row['path']).read_bytes());assert actual==row['sha256'],row['path'];installed.append(dict(path=row['path'],sha256=actual))
 own_sources=[]
 for path in sorted(OUT.glob('*.py')):
  ast.parse(path.read_text('utf-8'),filename=str(path));own_sources.append(dict(path=path.name,sha256=sha(path.read_bytes()),size=path.stat().st_size))
 manifest=dict(stage='C1_SOURCE_PREPARED_OFFLINE_BUILD_ONLY_NATIVE_NOT_ACCEPTED',base_sha256=BASE_HASH,candidate_sha256=sha(data),science_credit_enabled=False,union_enabled=False,engine_sha256=ENGINE_HASH,input_pins=INPUTS,spatial_pins=pins,sources=own_sources,recipe=r.rows,labels=r.labels,payload_rva=rx,payload_size=len(code),payload_sha256=sha(code),changes=changes,existing_changed_bytes=len(changed),unexplained_changed_bytes=0,appended_bytes=len(data)-len(base),existing_sections_byteidentical=True,current_hooks_and_caps_preserved=True,b2_record_bytes=36,b2_N=30,b2_five_hooks_preserved=True,relocations_preserved=True,instructions_decoded=len(decoded),installed_release_pins=installed,planned_layout=dict(result=2048,tile=96,scratch=4096,old_plan=0x54800,future_plan=0x79800),actual_active_plan_size=0x54800,append_plan_reset_allocation_deferred_to_C2=True,pending_work=['Root source review pending; native and C2 not accepted'])
 manifest.update(stage='C1_SOURCE_PREPARED_OFFLINE_BUILD_ONLY_NATIVE_NOT_ACCEPTED',
  future_growth_calculation_implemented=True,
  future_storage='private native stack; decoder arithmetic from saved tiles',
  development_summary='selected current indices: UNKNOWN/PENDING/READY/PRESENT/MIXED',
  per_call_limits=dict(open_tiles=20,spatial=20,development=20,improvement=60,primary_food=21,development_food=20,total_food=41),
  pass_query_counters_active=False,active_game_caller=False,
  shared_copy_pins=shared,protected_files_rechecked=preservation['protected_files'],
  dependency_pins_rechecked=preservation['dependencies'],checkpoint_pins=checkpoint,
  docs=[dict(path='SCHEMA-CONTRACT.md',sha256=sha((OUT/'SCHEMA-CONTRACT.md').read_bytes()))],
  pending_work=['Root review of C1 source/schema/candidate',
   'New kernel native ABI/semantic cases only after explicit root review',
   'Union/variable mandatory keys/allocation/reset/pass query counters only C2',
   'Actual engine activation and gameplay not measured'])
 return bytes(data),code,manifest,decoded
if __name__=='__main__':
 a=build();b=build();assert a[:3]==b[:3]
 data,code,manifest,decoded=a
 (OUT/'SCIENCE-C1-CREDIT-OFF.prepared.dll').write_bytes(data);(OUT/'science.payload.bin').write_bytes(code)
 (OUT/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n','utf-8')
 schema=dict(result_size=layout.RESULT_SIZE,header=layout.HEADER,tile_offset=layout.TILE_OFFSET,
  tile_stride=layout.TILE_STRIDE,max_tiles=layout.MAX_TILES,tile=layout.TILE,private_stack=layout.STACK,
  kernel_frame_size=layout.KERNEL_FRAME_SIZE,
  query_budgets=layout.QUERY_BUDGETS,active_plan=layout.CURRENT_PLAN_SIZE,
  future_plan=layout.PLAN_SIZE,future_fields_stored_in_header=False)
 (OUT/'schema.json').write_text(json.dumps(schema,indent=2)+'\n','utf-8')
 old=json.loads((OUT/'checkpoint-v1/candidate-manifest.json').read_text('utf-8'))
 (OUT/'checkpoint-v1/own-source-pins.json').write_text(json.dumps(old['sources'],indent=2)+'\n','utf-8')
 diffs=[]
 for name in ('science_model.py','science_layout.py','science_result.py','build_candidate.py'):
  diffs.extend(difflib.unified_diff((OUT/'checkpoint-v1'/name).read_text('utf-8').splitlines(True),
   (OUT/name).read_text('utf-8').splitlines(True),fromfile='checkpoint-v1/'+name,tofile='C1-v2/'+name))
 diffs.extend(difflib.unified_diff([], (OUT/'SCHEMA-CONTRACT.md').read_text('utf-8').splitlines(True),fromfile='/dev/null',tofile='C1-v2/SCHEMA-CONTRACT.md'))
 (OUT/'source-diffs.txt').write_text(''.join(diffs),'utf-8')
 (OUT/'science.disassembly.txt').write_text('\n'.join(f'{i.address:08x} {i.bytes.hex():24} {i.mnemonic} {i.op_str}' for i in decoded)+'\n','utf-8')
 print(json.dumps({key:manifest[key] for key in ['stage','candidate_sha256','science_credit_enabled','unexplained_changed_bytes','existing_changed_bytes','instructions_decoded','pending_work']}))
