"""C1 source/candidate builder ONLY. Never installs or invokes native code."""
from pathlib import Path
import sys,struct,json,hashlib,importlib.util,difflib,datetime
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'PROEVEN/production-h3'))
from x86 import X86
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
sys.path.insert(0,str(OUT))
import native,policy
sha=lambda b:hashlib.sha256(b).hexdigest()
align=lambda n,a:(n+a-1)//a*a

def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

class Located(X86):
 def __init__(self,base):super().__init__();self.base=base
 def finish(self):
  for at,label,absolute in self.fix:
   assert label in self.labels,label
   value=self.base+self.labels[label] if absolute else self.labels[label]-at-4
   struct.pack_into('<I' if absolute else '<i',self.code,at,value)
  for row in self.rows:row['bytes']=self.code[row['offset']:row['offset']+len(bytes.fromhex(row['bytes']))].hex()
  return bytes(self.code)

def verify_base():
 prep=json.loads((OUT/'preparation-manifest.json').read_text('utf-8'))
 for row in prep['release_pins']+prep['proposals']+prep['source_pins']:
  assert sha((ROOT/row['path']).read_bytes())==row['sha256'],row['path']
 original=(OUT/'release-v1.robotcom.backup.dll').read_bytes();assert sha(original)==prep['base_sha256']
 assert sha((ROOT/'CTP-proef/ctp_program/ctp/civctp.exe').read_bytes())==prep['engine_sha256']
 return original,prep

def compose():
 original,prep=verify_base();p=pefile.PE(data=original);rx=p.OPTIONAL_HEADER.SizeOfImage;assert rx==0xd6000
 h3=module('extend_h3',ROOT/'PROEVEN/production-h3/build-current.py');h3.X86=lambda:Located(rx);hcode,hr=h3.payload()
 b2=module('extend_b2',ROOT/'PROEVEN/opening-b2/build.py');bcode,br,bend=b2.payload(30);assert p.get_data(0xd4000,len(bcode))==bcode
 base=module('extend_base_integration',OUT/'integration_base.py')
 extension=align(rx+len(hcode),0x1000);r=Located(extension)
 calls=dict(SchedulerUpdate=0x70600,GroundBuild=0x7a080,Desired=0x659a0,AIPUpdate=0x66b70,Choose=0x65900,ArmyCount=0x1a970,ArmyType=0x1a980,IsWait=0x129f0,ArmyPos=0x11bc0,CityPos=0x1c380,CityWhat=0x1cd50,CanBuild=0x1f330,GetThreat=0x83b10,GetContinent=0x7e030,ExecuteOriginal=0x443c0)
 for name,rva in calls.items():r.labels[name]=rva-extension
 for name,label in [('H3Classifier','classifier'),('H3Host','host_validator'),('H3PosCompare','poscmp')]:r.labels[name]=rx+hr.labels[label]-extension
 for name,label in [('B2Host','production_host'),('B2Symbols','symbols'),('B2Bit','bit')]:r.labels[name]=0xd4000+br.labels[label]-extension
 policy.emit(r,b2,base);rw=align(extension+len(r.code),0x1000);r.labels['pass_state']=rw-extension;r.labels['generation']=rw+native.PLAN_SIZE-extension
 ecode=r.finish();code=hcode+bytes(extension-rx-len(hcode))+ecode;rxraw=align(len(code),0x200);rwraw=align(native.PLAN_SIZE+4,0x200)
 data=bytearray(original);allowed=[]
 def change(at,value,why):
  before=bytes(data[at:at+len(value)]);data[at:at+len(value)]=value;allowed.append(dict(offset=at,length=len(value),before=before.hex(),after=value.hex(),reason=why))
 windows={row['name']:row for row in prep['windows']}
 targets={name:extension+r.labels[name] for name in ('start_hook','capture_hook','desired_hook','scope_hook','quota_hook')}
 targets.update(execute_slot=extension+r.labels['execute_gate'],arrival_call=extension+r.labels['arrival_dispatch'],normalize=extension+r.labels['normalize_dispatch'])
 for name,row in windows.items():
  site=int(row['rva'],16);at=int(row['offset'],16);pre=bytes.fromhex(row['preimage']);assert original[at:at+len(pre)]==pre
  if name=='execute_slot':value=struct.pack('<I',0x20000000+targets[name])
  elif name=='arrival_result':value=b'\x90'*5
  else:value=b'\xe8'+struct.pack('<i',targets[name]-site-5)+b'\x90'*(len(pre)-5)
  change(at,value,'named new hook '+name)
 assert p.sections[-1].get_file_offset()+40==0x278 and not any(original[0x278:0x2c8])
 section=lambda name,size,rva,raw,offset,flags:struct.pack('<8sIIIIIIHHI',name,size,rva,raw,offset,0,0,0,0,flags)
 change(0x278,section(b'.u40c',len(code),rx,rxraw,len(original),0x60000020),'new RX internal classifier/policy/adapters')
 change(0x2a0,section(b'.u40s',native.PLAN_SIZE+4,rw,rwraw,len(original)+rxraw,0xc0000040),'new RW nonserialized generation/pass')
 change(p.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),struct.pack('<H',7),'PE NumberOfSections')
 for field,value in [('SizeOfImage',align(rw+native.PLAN_SIZE+4,0x1000)),('SizeOfCode',p.OPTIONAL_HEADER.SizeOfCode+rxraw),('SizeOfInitializedData',p.OPTIONAL_HEADER.SizeOfInitializedData+rwraw)]:change(p.OPTIONAL_HEADER.get_field_absolute_offset(field),struct.pack('<I',value),'PE '+field)
 data.extend(code+bytes(rxraw-len(code))+bytes(rwraw));change(p.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum'),struct.pack('<I',pefile.PE(data=data).generate_checksum()),'PE CheckSum')
 cp=pefile.PE(data=data);assert cp.get_data(0xd4000,len(bcode))==bcode
 for row in prep['b2_hooks']:assert cp.get_data(int(row['rva'],16),5).hex()==row['bytes']
 # Independent whole-original-file byte classification, not just patch log.
 mask=bytearray(len(original))
 for row in allowed:
  assert not any(mask[row['offset']:row['offset']+row['length']]),'overlapping changes'
  mask[row['offset']:row['offset']+row['length']]=b'\x01'*row['length']
 changed=[i for i in range(len(original)) if original[i]!=data[i]]
 assert all(mask[i] for i in changed)
 full=[];i=0
 while i<len(original):
  if original[i]==data[i]:i+=1;continue
  start=i
  while i<len(original) and original[i]!=data[i]:i+=1
  full.append(dict(offset=start,length=i-start,before=original[start:i].hex(),after=bytes(data[start:i]).hex()))
 full.append(dict(offset=len(original),length=len(data)-len(original),before='',after=bytes(data[len(original):]).hex(),kind='all appended bytes including exact zero fill'))
 reloc_old=[(e.rva,e.type) for b in p.DIRECTORY_ENTRY_BASERELOC for e in b.entries]
 reloc_new=[(e.rva,e.type) for b in cp.DIRECTORY_ENTRY_BASERELOC for e in b.entries]
 assert reloc_old==reloc_new and reloc_new.count((0x8a598,3))==1
 # Every emitted recipe row independently decodes; no native call involved.
 dis=Cs(CS_ARCH_X86,CS_MODE_32);instructions=0
 for recipe,payload,start in [(hr,hcode,rx),(r,ecode,extension)]:
  for row in recipe.rows:
   raw=bytes.fromhex(row['bytes']);decoded=list(dis.disasm(raw,0x20000000+start+row['offset']))
   if row['asm'].startswith(('constant','prepared')):continue
   assert sum(i.size for i in decoded)==len(raw),(row,decoded)
   instructions+=len(decoded)
 deps=[]
 paths=[OUT/f for f in ['build_candidate.py','native.py','policy.py','integration_base.py','input-pins.py','bind_scheduler.py']]
 paths+=list((ROOT/'PROEVEN/production-h3').glob('*.py'))+[ROOT/'PROEVEN/score-h1/build.py',ROOT/'PROEVEN/opening-b2/build.py',ROOT/'PROEVEN/production-h3/host/validator.prepared.bin']
 for path in sorted(set(paths)):deps.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path.read_bytes()),size=path.stat().st_size))
 manifest=dict(stage='C1_SOURCE_CANDIDATE_ONLY_NOT_INSTALLED_NOT_NATIVE_NOT_GAMEPLAY',base_sha256=sha(original),candidate_sha256=sha(data),proposal_sha256=prep['proposals'][1]['sha256'],sources=deps,source_dependency_pins=prep['source_pins'],release_pins=prep['release_pins'],allowed_changes=allowed,full_diff=full,original_changed_byte_count=len(changed),appended_byte_count=len(data)-len(original),unexplained_byte_count=0,components=dict(internal_H3_rva=hex(rx),internal_H3_sha256=sha(hcode),extension_rva=hex(extension),extension_sha256=sha(ecode),state_rva=hex(rw),state_size=native.PLAN_SIZE+4),sections=[dict(name=s.Name.rstrip(b'\0').decode(),rva=s.VirtualAddress,virtual_size=s.Misc_VirtualSize,raw_offset=s.PointerToRawData,raw_size=s.SizeOfRawData,flags=s.Characteristics) for s in cp.sections],b2_preserved=dict(payload_rva='0xd4000',payload_size=len(bcode),payload_sha256=sha(bcode),all_five_hooks_unchanged=True,record_length=36,record_version=1,N=30),relocations_unchanged=True,execute_slot_HIGHLOW=(0x8a598,3),labels=r.labels,recipe=r.rows,h3_labels=hr.labels,instructions_decoded=instructions,policy='D=min(R,max(Dorig,Gcert)); incomplete union preserves native demand within managed R; completion1 other gov native; no native detachment duplication',buffers=dict(SELECTED=native.SELECTED,SELECTED_CAP=native.SELECTED_CAP,ORDER=native.ORDER,PATHCACHE=native.PATHCACHE,PLAN_SIZE=native.PLAN_SIZE),budgets=dict(candidate_copy=4096,canonical_prefix=64,departure_sources=32,path_queries=128,query_search=4096,path_entries=4096,total_path_points=4096,selected_slots=40))
 return bytes(data),code,manifest

def main():
 data,code,manifest=compose();data2,code2,manifest2=compose();assert (data,code,manifest)==(data2,code2,manifest2)
 (OUT/'U30-40.prepared.dll').write_bytes(data);(OUT/'U30-40.payload.bin').write_bytes(code);(OUT/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n','utf-8')
 for original,own in [('native.py','native.py'),('integration.py','integration_base.py'),('input-pins.py','input-pins.py')]:
  a=(ROOT/'PROEVEN/settler-b4'/original).read_text('utf-8').splitlines(True);b=(OUT/own).read_text('utf-8').splitlines(True)
  (OUT/(own+'.source-diff.txt')).write_text(''.join(difflib.unified_diff(a,b,fromfile='read-only B4/'+original,tofile='owned/'+own)),'utf-8')
 print(json.dumps(dict(stage=manifest['stage'],sha256=manifest['candidate_sha256'],original_changed_bytes=manifest['original_changed_byte_count'],appended_bytes=manifest['appended_byte_count'],unexplained_bytes=0,b2_unchanged=True,instructions_decoded=manifest['instructions_decoded'],components=manifest['components'])))

if __name__=='__main__':main()
