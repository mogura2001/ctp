"""Offline B4 composition builder. PREPARED artifacts require native checks.

Existing H3 bytes retain their original RVA. B2 and B4 are re-emitted using
the existing Recipe fixups at their declared RVAs. No accepted binaries are
copied over one another and no existing builder or installation is written.
"""
from pathlib import Path
import sys,struct,json,hashlib,importlib.util
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'PROEVEN/production-h3'))
from x86 import X86
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
import native,integration
pins_spec=importlib.util.spec_from_file_location('b4_frozen_input_pins',OUT/'input-pins.py');pins_mod=importlib.util.module_from_spec(pins_spec);pins_spec.loader.exec_module(pins_mod)
sha=lambda b:hashlib.sha256(b).hexdigest()
align=lambda n,a:(n+a-1)//a*a
DESIGN='6e310ea5c15f7b3cc42ad75f586bab6bdf14bdee6e63a6639ac7c5f9b2717501'
ORIGINAL='3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'

def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

class Located(X86):
 def __init__(self,base):super().__init__();self.base=base
 def finish(self):
  for at,label,absolute in self.fix:
   assert label in self.labels, label
   value=self.base+self.labels[label] if absolute else self.labels[label]-at-4
   struct.pack_into('<I' if absolute else '<i',self.code,at,value)
  for row in self.rows:row['bytes']=self.code[row['offset']:row['offset']+len(bytes.fromhex(row['bytes']))].hex()
  return bytes(self.code)

SITES=[('start_hook',0x2b079,'e882550400'),('capture_hook',0x7abac,'e8cff4ffff'),('desired_hook',0x66b81,'e81aeeffff'),('scope_hook',0x2b0d8,'e893ba0300'),('quota_hook',0x65a4c,'e8affeffff')]
ORIGINAL_CALLS=dict(SchedulerUpdate=0x70600,GroundBuild=0x7a080,Desired=0x659a0,AIPUpdate=0x66b70,Choose=0x65900,ArmyCount=0x1a970,ArmyType=0x1a980,IsWait=0x129f0,ArmyPos=0x11bc0,CityPos=0x1c380,CityWhat=0x1cd50,CanBuild=0x1f330,GetThreat=0x83b10,GetContinent=0x7e030)

def compose(N,enabled):
 assert N in (25,30)
 assert sha((ROOT/'ONTWERP/PRODUCER-SETTLERVRAAG-B4.md').read_bytes())==DESIGN
 original=(ROOT/'PROEVEN/production-h3/backup/robotcom.original.dll').read_bytes();assert sha(original)==ORIGINAL
 p=pefile.PE(data=original);assert len(original)==0xa1400 and p.FILE_HEADER.NumberOfSections==4
 h3=module('b4_existing_h3',ROOT/'PROEVEN/production-h3/build-current.py');hcode,hr=h3.payload();assert sha(hcode)==sha((ROOT/'PROEVEN/production-h3/H3-SCORE_CURRENT.payload.bin').read_bytes())
 b2=module('b4_existing_b2',ROOT/'PROEVEN/opening-b2/build.py');b2base=align(0xd4000+len(hcode),0x1000);b2.BASE=b2base;b2.X86=lambda:Located(b2base);bcode,br,bend=b2.payload(N)
 b4base=align(b2base+len(bcode),0x1000);r=Located(b4base)
 for name,rva in ORIGINAL_CALLS.items():r.labels[name]=rva-b4base
 for name,label in (('H3Classifier','classifier'),('H3Host','host_validator'),('H3PosCompare','poscmp')):r.labels[name]=0xd4000+hr.labels[label]-b4base
 for name,label in (('B2Host','production_host'),('B2Symbols','symbols'),('B2Bit','bit')):r.labels[name]=b2base+br.labels[label]-b4base
 if enabled:integration.emit(r,b2,N)
 # RW address depends on final RX extent; fixups are resolved only now.
 statebase=align(b4base+len(r.code),0x1000);r.labels['pass_state']=statebase-b4base;r.labels['generation']=statebase+native.PLAN_SIZE-b4base
 b4code=r.finish() if enabled else b''
 code=hcode+bytes(b2base-0xd4000-len(hcode))+bcode
 if enabled:code+=bytes(b4base-0xd4000-len(code))+b4code
 data=bytearray(original);changes=[]
 def change(at,value,why):
  before=bytes(data[at:at+len(value)]);data[at:at+len(value)]=value;changes.append(dict(offset=hex(at),before=before.hex(),after=value.hex(),reason=why))
 def callsite(site,target,preimage,why,jump=False):
  at=p.get_offset_from_rva(site);assert original[at:at+len(bytes.fromhex(preimage))].hex()==preimage
  patch=(b'\xe9' if jump else b'\xe8')+struct.pack('<i',target-site-5)
  if len(bytes.fromhex(preimage))==6:patch+=b'\x90'
  change(at,patch,why)
 for site in (0x784bb,0x78517,0x7aa35):callsite(site,0xd4000+hr.labels['adapter'],'ff9168010000','unchanged H3 score adapter')
 for name,site in b2.INPUT['sites'].items():
  label='reload' if name=='reload_entry' else name
  callsite(int(site['rva'],16),b2base+br.labels[label],site['preimage'],'relocated B2 '+name,name=='reload_entry')
 if enabled:
  for name,site,preimage in SITES:callsite(site,b4base+r.labels[name],preimage,'B4 '+name)
 assert not any(original[0x250:0x2a0]);raw=align(len(code),0x200);rwraw=0xa1400+raw;rwsize=align(native.PLAN_SIZE+4,0x200)
 def section(name,size,rva,rawsize,offset,flags):return struct.pack('<8sIIIIIIHHI',name,size,rva,rawsize,offset,0,0,0,0,flags)
 change(0x250,section(b'.b4c\0\0\0\0',len(code),0xd4000,raw,0xa1400,0x60000020),'RX declared component composition')
 if enabled:change(0x278,section(b'.b4s\0\0\0\0',native.PLAN_SIZE+4,statebase,rwsize,rwraw,0xc0000040),'RW own transient bounded pass')
 change(p.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),struct.pack('<H',6 if enabled else 5),'section count')
 imagesize=align(statebase+native.PLAN_SIZE+4,0x1000) if enabled else align(0xd4000+len(code),0x1000)
 change(p.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfImage'),struct.pack('<I',imagesize),'declared mapped extent')
 change(p.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfCode'),struct.pack('<I',p.OPTIONAL_HEADER.SizeOfCode+raw),'RX size')
 if enabled:change(p.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfInitializedData'),struct.pack('<I',p.OPTIONAL_HEADER.SizeOfInitializedData+rwsize),'RW size')
 data.extend(code);data.extend(bytes(raw-len(code)))
 if enabled:data.extend(bytes(rwsize))
 checksum=pefile.PE(data=data).generate_checksum();change(p.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum'),struct.pack('<I',checksum),'PE checksum')
 manifest=dict(stage='PREPARED EMISSION; see separate offline results/root review; not installed',variant=('B4-DIRECT-PRODUCTION-TECHNICAL' if enabled else 'H3-B2-COMPOSITION-BASELINE'),N=N,N_policy='pending; technical fixture only',original_sha256=ORIGINAL,design_sha256=DESIGN,candidate_sha256=sha(data),payload_sha256=sha(code),components=dict(H3=dict(rva=hex(0xd4000),sha256=sha(hcode)),B2=dict(rva=hex(b2base),sha256=sha(bcode)),B4=dict(rva=hex(b4base),sha256=sha(b4code)),state_rva=hex(statebase)),input_pins=pins_mod.pins() if enabled else None,changes=changes,labels=r.labels,recipe=r.rows,scope='production-only technical; gameplay/science/monopoly/transport unmeasured')
 return bytes(data),code,manifest

def main():
 for N in (25,30):
  for enabled in (False,True):
   data,code,manifest=compose(N,enabled);data2,code2,m2=compose(N,enabled);assert (data,code)==(data2,code2)
   name=('B4' if enabled else 'BASELINE')+'-N'+str(N)
   (OUT/(name+'.prepared.dll')).write_bytes(data);(OUT/(name+'.payload.bin')).write_bytes(code);(OUT/(name+'.manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
   print(json.dumps(dict(artifact=name,sha256=sha(data),stage=manifest['stage'])))

if __name__=='__main__':main()
