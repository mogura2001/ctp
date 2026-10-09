"""H3 physical/current-food score candidate, from original H1-I route only.

Candidate artifacts only; no installation/game access. Development is separate.
"""
from pathlib import Path
import json,struct,sys,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'PROEVEN/score-h1'))
import build as h1
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from x86 import X86,mem as m
from components import h2,reader,poscmp
from model import model,chooseplan
from development import tile,development,public_development
from layout import RESULT_SIZE
sha=lambda b:hashlib.sha256(b).hexdigest()
DESIGN='be16e3844ca7ae0396bd31ac28478855ff906c4091b529605e0bd91a41a71248'
assert sha((ROOT/'ONTWERP/PRODUCTIELOCATIES-H3.md').read_bytes())==DESIGN

def adapter(r):
 r.label('adapter');r.prologue(RESULT_SIZE+96);r.mov('ebx',m('ebp',8))
 for source,local,packed in [(12,-20,-40),(16,-24,-38),(20,-28,-36)]:
  r.load('eax',m('ebp',source),'sx16');r.mov(m('ebp',local),'eax');r.word(m('ebp',packed),'eax')
 r.mov(m('ebp',-34),0) # padding and scratch; words z/padding set below
 r.load('eax',m('ebp',20),'sx16');r.word(m('ebp',-36),'eax')
 for off in (-28,-24,-20):r.push(m('ebp',off))
 r.push('ebx');r.mov('ecx',m('ebx'));r.unary('call',m('ecx',0x168));r.op('movsx eax,ax',b'\x0f\xbf\xc0');r.mov(m('ebp',-16),'eax');r.test('eax','eax');r.j('jle','adapter_done')
 r.j('call','adapter_pc');r.label('adapter_pc');r.pop('esi');r.rva('sub esi,RVA(adapter_pc)','81ee','adapter_pc')
 r.mov('edi',m('esi',0xc6fb4));r.test('edi','edi');r.j('jz','adapter_done');r.alu('cmp',m('edi',0x30),'ebx');r.j('jne','adapter_done');r.alu('cmp',m('ebp',-28),0);r.j('jne','adapter_done');r.load('eax',m('esi',0xc6fb0),'sx16');r.test('eax','eax');r.j('jnz','adapter_done')
 r.lea('eax',m('ebp',-(RESULT_SIZE+80)));r.push('eax');r.lea('eax',m('ebp',-40));r.push('eax');r.push('ebx');r.push('edi');r.j('call','classifier')
 r.alu('cmp','eax',2);r.j('jne','adapter_done');r.mov('eax',m('ebp',-(RESULT_SIZE+80)+68));r.test('eax','eax');r.j('jl','adapter_done');r.j('jg','adapter_bonus');r.alu('cmp',m('ebp',-(RESULT_SIZE+80)+64),0);r.j('je','adapter_done')
 r.label('adapter_bonus');r.alu('cmp',m('ebp',-16),32767);r.j('jge','adapter_done');r.unary('inc',m('ebp',-16))
 r.label('adapter_done');r.mov('eax',m('ebp',-16));r.epilogue(RESULT_SIZE+96,16)

def classifier(r):
 r.label('classifier');r.prologue(32);r.zero(m('ebp',20),RESULT_SIZE);r.mov('edi',m('ebp',20));r.mov(m('edi',8),1);r.mov(m('edi',4),14)
 r.lea('eax',m('ebp',-40));r.push('eax');r.push(m('ebp',12));r.push(m('ebp',8));r.j('call','host_validator');r.test('eax','eax');r.j('jz','classifier_done')
 r.lea('eax',m('ebp',-40));r.push('eax');r.push(m('ebp',20));r.push(m('ebp',16));r.push(m('ebp',12));r.push(m('ebp',8));r.j('call','current_model')
 r.label('classifier_done');r.mov('eax',m('edi'));r.epilogue(32,16)

def payload():
 r=X86();adapter(r);classifier(r);h2(r);reader(r);poscmp(r);model(r);chooseplan(r);tile(r);development(r);public_development(r)
 r.label('host_validator');validator=(OUT/'host/validator.prepared.bin').read_bytes();r.op('prepared production-only HostBinding validator',validator)
 return r.finish(),r

def build():
 blob=(OUT/'backup/robotcom.original.dll').read_bytes();assert sha(blob)==h1.HASH
 p=pefile.PE(data=blob);assert p.OPTIONAL_HEADER.ImageBase==0x20000000 and p.FILE_HEADER.TimeDateStamp==0x37b894e7
 assert len(blob)==0xa1400 and not any(blob[0x250:0x278])
 code,r=payload();raw=h1.align(len(code),0x200);data=bytearray(blob);changes=[]
 def change(at,b,why):
  before=bytes(data[at:at+len(b)]);data[at:at+len(b)]=b;changes.append({'offset':hex(at),'before':before.hex(),'after':b.hex(),'reason':why})
 for site in (0x784bb,0x78517,0x7aa35):
  at=p.get_offset_from_rva(site);assert blob[at:at+6].hex()=='ff9168010000';change(at,b'\xe8'+struct.pack('<i',0xd4000-site-5)+b'\x90','same H3 adapter on all H1 sites')
 change(0x250,struct.pack('<8sIIIIIIHHI',b'.h3',len(code),0xd4000,raw,0xa1400,0,0,0,0,0x60000020),'new RX section')
 change(p.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),struct.pack('<H',5),'section count')
 change(p.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfImage'),struct.pack('<I',h1.align(0xd4000+len(code),0x1000)),'image size')
 change(p.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfCode'),struct.pack('<I',p.OPTIONAL_HEADER.SizeOfCode+raw),'code size');data.extend(code+bytes(raw-len(code)))
 change(p.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum'),struct.pack('<I',pefile.PE(data=data).generate_checksum()),'PE checksum')
 manifest={'variant':'H3-SCORE_CURRENT','stage':'BUILT CURRENT + SEPARATE DEVELOPMENT; requires checks for this exact hash','original_sha256':h1.HASH,'design_sha256':DESIGN,'candidate_sha256':sha(data),'payload_sha256':sha(code),'payload_size':len(code),'payload_rva':'0xd4000','payload_raw':'0xa1400','changes':changes,'labels':r.labels,'recipe':r.rows,'appended_bytes':raw,'result_size':RESULT_SIZE,'development_result_size':2048,'scope':'candidate only; no installation; gameplay unmeasured'}
 return bytes(data),code,manifest

if __name__=='__main__':
 data,code,manifest=build();assert(data,code,manifest)==build()
 out=OUT/'candidates/H3-SCORE_CURRENT';out.mkdir(parents=True,exist_ok=True);(out/'robotcom.dll').write_bytes(data)
 (OUT/'H3-SCORE_CURRENT.payload.bin').write_bytes(code);(OUT/'H3-SCORE_CURRENT.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 rows=list(Cs(CS_ARCH_X86,CS_MODE_32).disasm(code,0xd4000));assert sum(i.size for i in rows)==len(code)
 (OUT/'H3-SCORE_CURRENT.disassembly.txt').write_text('\n'.join(f'{i.address:08x} {i.bytes.hex():24} {i.mnemonic} {i.op_str}' for i in rows)+'\n')
 print(json.dumps({'built':manifest['variant'],'payload_size':len(code),'instructions':len(rows),'candidate_sha256':manifest['candidate_sha256'],'stage':manifest['stage']}))
