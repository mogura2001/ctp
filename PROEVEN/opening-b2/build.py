"""Frozen B2a-only five-hook candidate builder. Never installs or runs a game.

Reuse the existing finite H1/H3 x86 emitter and local PE/Capstone library.
Both N values are technical fixture artifacts, neither is production policy.
"""
from pathlib import Path
import sys,json,struct,hashlib
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'PROEVEN/production-h3'))
from x86 import X86,mem as m
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
INPUT=json.loads((OUT/'build-inputs.json').read_text())
BASE=0xd4000
sha=lambda b:hashlib.sha256(b).hexdigest()
align=lambda n,a:(n+a-1)//a*a
MARKER=bytes.fromhex(INPUT['record']['marker_hex'])
assert len(MARKER)==16

def pc(r,name):
 r.j('call',name);r.label(name);r.pop('esi');r.rva('sub esi,RVA('+name+')','81ee',name)
def ptr(r,reg,label):
 r.rva('lea '+reg+',module+'+label,{'eax':'8d86','edx':'8d96','ecx':'8d8e'}[reg],label)
def call(r,name):r.j('call',name)
def start(r,name):
 r.label(name);r.push('ebp');r.mov('ebp','esp');r.alu('sub','esp',1024);r.mov(m('ebp',-4),'ecx')
def end(r,pop):
 r.mov('esp','ebp');r.pop('ebp');r.op('ret '+str(pop),b'\xc2'+struct.pack('<H',pop))
def snapshot(r):
 r.op('pushfd',b'\x9c');r.op('pushad',b'\x60');r.lea('eax',m('ebp',-768));r.alu('and','eax',-16);r.mov(m('ebp',-12),'eax');r.fp('fxsave','0fae',0,m('eax'));r.op('fninit',b'\xdb\xe3');r.mov('eax',m('esp',28)) # expose original EAX to load/reload callers
def restore(r):
 r.mov('eax',m('ebp',-12));r.fp('fxrstor','0fae',1,m('eax'));r.op('popad',b'\x61');r.op('popfd',b'\x9d')
def failure(r,label):r.test('eax','eax');r.j('jz',label)
def frameout(r):r.lea('eax',m('ebp',-40));r.push('eax')
def find(r,ai):frameout(r);r.push(ai);call(r,'symbols')
def readbit(r):r.push(m('ebp',-40));call(r,'bit');r.alu('cmp','eax',1)
def writepair(r,ai,bit):r.push(bit);r.push(ai);call(r,'write_pair')

def registration(r):
 start(r,'registration')
 for off in (24,20,16,12,8):r.push(m('ebp',off))
 call(r,'AddSymbol');snapshot(r);pc(r,'registration_pc')
 for name,value in [('completed_name',0),('required_name',0x3ff00000)]:
  r.push(0);r.push(value);r.push(0);r.push(0);ptr(r,'eax',name);r.push('eax');r.mov('ecx',m('ebp',-4));call(r,'AddSymbol')
  ptr(r,'eax',name);r.push('eax');r.mov('ecx',m('ebp',-4));call(r,'GetSymbol');failure(r,'trap');r.push(2);r.mov('ecx','eax');call(r,'RegisterInit')
 restore(r);end(r,20)

def begin(r,N):
 start(r,'beginturn');snapshot(r);r.mov(m('ebp',-16),'esi');find(r,m('ebp',-16));failure(r,'trap');readbit(r);r.j('ja','trap');r.mov(m('ebp',-20),'eax');r.test('eax','eax');r.j('jnz','begin_write')
 r.mov('edi',m('ebp',-16));r.mov('eax',m('edi',0x8c));r.test('eax','eax');r.j('jz','trap');r.alu('cmp',m('eax'),N);r.j('jl','begin_write')
 r.mov('edx',m('edi',0x2c));r.test('edx','edx');r.j('jz','trap');r.mov('eax',m('edx'));r.test('eax','eax');r.j('jz','trap');r.push('edx');r.unary('call',m('eax',0x150));r.alu('cmp','eax',3);r.j('jne','begin_write');r.mov(m('ebp',-20),1)
 r.label('begin_write');writepair(r,m('ebp',-16),m('ebp',-20));failure(r,'trap');restore(r)
 r.push(m('ebp',8));r.mov('ecx',m('ebp',-4));call(r,'FireRules');end(r,4)

def save(r,N):
 start(r,'save');snapshot(r);call(r,'production_host');r.mov(m('ebp',-16),'eax');failure(r,'unknown_trap')
 r.push(1);r.push(m('ebp',8));r.push(m('ebp',-16));call(r,'archive');failure(r,'save_fatal')
 find(r,m('ebp',-4));failure(r,'save_fatal');readbit(r);r.j('ja','save_fatal');r.mov(m('ebp',-20),'eax');restore(r)
 r.push(m('ebp',8));r.mov('ecx',m('ebp',-4));call(r,'AiMain_Save');snapshot(r)
 # Original Save may grow the archive: revalidate and use current vtable only.
 r.push(1);r.push(m('ebp',8));r.push(m('ebp',-16));call(r,'archive');failure(r,'save_fatal')
 for off in range(0,16,4):r.mov(m('ebp',-80+off),struct.unpack_from('<I',MARKER,off)[0])
 for off,val in [(16,1),(20,36),(32,N)]:r.mov(m('ebp',-80+off),val)
 r.mov('eax',m('ebp',-4));r.mov('eax',m('eax',0x20));r.mov(m('ebp',-56),'eax');r.mov('eax',m('ebp',-20));r.mov(m('ebp',-52),'eax')
 r.mov('edx',m('ebp',8));r.mov('eax',m('edx'));r.push(36);r.lea('ecx',m('ebp',-80));r.push('ecx');r.push('edx');r.unary('call',m('eax',12));restore(r);end(r,4)
 r.label('save_fatal');r.push(m('ebp',-16));call(r,'fatal_save');r.op('ud2 no success continuation',b'\x0f\x0b')

def load(r,N):
 start(r,'load');r.push(m('ebp',12));r.push(m('ebp',8));r.mov('ecx',m('ebp',-4));call(r,'AiMain_Load');snapshot(r);r.mov(m('ebp',-16),'eax');r.test('eax','eax');r.j('jz','load_bad')
 call(r,'production_host');failure(r,'load_bad');r.push(0);r.push(m('ebp',12));r.push('eax');call(r,'archive');failure(r,'load_bad')
 r.push(N);r.mov('eax',m('ebp',-4));r.push(m('eax',0x20));r.push(m('ebp',12));call(r,'peek');r.alu('cmp','eax',-1);r.j('je','load_bad');r.mov(m('ebp',-20),'eax')
 # Verify both current symbols before any record consumption.
 find(r,m('ebp',-4));failure(r,'load_bad')
 r.alu('cmp',m('ebp',-20),2);r.j('jae','load_record');r.j('jmp','load_write')
 r.label('load_record');r.mov('edx',m('ebp',12));r.mov('eax',m('edx'));r.push(36);r.lea('ecx',m('ebp',-80));r.push('ecx');r.push('edx');r.unary('call',m('eax',16));r.alu('sub',m('ebp',-20),2)
 r.label('load_write');writepair(r,m('ebp',-4),m('ebp',-20));failure(r,'load_bad');r.j('jmp','load_done')
 r.label('load_bad');r.mov(m('ebp',-16),0)
 r.label('load_done');restore(r);r.mov('eax',m('ebp',-16));end(r,8)

def reload(r):
 start(r,'reload');snapshot(r);find(r,m('ebp',-4));failure(r,'trap');readbit(r);r.j('ja','trap');r.mov(m('ebp',-16),'eax');restore(r)
 r.push(m('ebp',8));r.mov('ecx',m('ebp',-4));call(r,'reload_trampoline');snapshot(r);r.mov(m('ebp',-20),'eax');failure(r,'trap');writepair(r,m('ebp',-4),m('ebp',-16));failure(r,'trap');restore(r);r.mov('eax',m('ebp',-20));end(r,4)
 r.label('reload_trampoline');r.op('exact displaced prologue',bytes.fromhex('558bec5356'));r.j('jmp','reload_rest')

def symbols(r):
 r.label('symbols');r.prologue(16);pc(r,'symbols_pc');r.mov('edi',m('ebp',8));r.test('edi','edi');r.j('jz','symbols_bad');r.mov('ebx',m('edi',0xc4));r.test('ebx','ebx');r.j('jz','symbols_bad')
 for idx,name in enumerate(('completed_name','required_name')):
  ptr(r,'eax',name);r.push('eax');r.mov('ecx','ebx');call(r,'GetSymbol');failure(r,'symbols_bad');r.mov('edx',m('ebp',12));r.mov(m('edx',idx*4),'eax')
  r.alu('cmp',m('eax'),0);r.j('jne','symbols_bad');r.load('ecx',m('eax',0x6a),'sx8');r.test('ecx',1);r.j('jnz','symbols_bad')
  r.load('ecx',m('eax',0xc2),'zx16');r.test('ecx',4);r.j('jz','symbols_bad');r.load('ecx',m('eax',0x68),'zx16');r.test('ecx',4);r.j('jnz','symbols_bad')
 r.mov('eax',1);r.j('jmp','symbols_done');r.label('symbols_bad');r.mov('eax',0);r.label('symbols_done');r.epilogue(16,8)
 r.label('bit');r.mov('edx',m('esp',4));r.alu('cmp',m('edx',8),0);r.j('jne','bit_bad');r.mov('eax',m('edx',12));r.test('eax','eax');r.j('jz','bit_done');r.alu('cmp','eax',0x3ff00000);r.j('jne','bit_bad');r.mov('eax',1);r.j('jmp','bit_done');r.label('bit_bad');r.mov('eax',-1);r.label('bit_done');r.op('ret4',b'\xc2\x04\x00')
 r.label('write_pair');r.prologue(32);find(r,m('ebp',8));failure(r,'write_bad');r.mov('edi',m('ebp',12));r.alu('cmp','edi',1);r.j('ja','write_bad')
 for off,complement in [(-40,False),(-36,True)]:
  r.mov('eax','edi')
  if complement:r.alu('xor','eax',1)
  r.imul('eax','eax',0x3ff00000);r.push('eax');r.push(0);r.mov('ecx',m('ebp',off));call(r,'SetValue')
 r.mov('eax',1);r.j('jmp','write_done');r.label('write_bad');r.mov('eax',0);r.label('write_done');r.epilogue(32,8)

def host(r):
 # Read only our process's mapped main-image pointer, no game-process handle.
 r.label('production_host');r.op('mov eax,fs:[30h] PEB',b'\x64\xa1\x30\x00\x00\x00');r.mov('eax',m('eax',8));r.alu('cmp','eax',0x400000);r.j('jne','production_unknown');r.push('eax');call(r,'host_check');r.op('ret',b'\xc3');r.label('production_unknown');r.mov('eax',0);r.op('ret',b'\xc3')
 r.label('host_check');r.prologue(0);r.mov('esi',m('ebp',8));r.test('esi','esi');r.j('jz','host_bad')
 # PEB ensures main image is mapped; only confirmed PE bounds permit fingerprints.
 r.load('eax',m('esi'),'zx16');r.alu('cmp','eax',0x5a4d);r.j('jne','host_bad');r.mov('edx',m('esi',0x3c));r.alu('cmp','edx',0x40);r.j('jb','host_bad');r.alu('cmp','edx',0x400);r.j('ja','host_bad');r.alu('add','edx','esi')
 for off,size,val in [(0,4,0x4550),(4,2,0x14c),(8,4,0x37d6f702),(24,2,0x10b),(52,4,0x400000),(160,4,0),(164,4,0)]:
  if size==2:r.load('eax',m('edx',off),'zx16');r.alu('cmp','eax',val)
  else:r.alu('cmp',m('edx',off),val)
  r.j('jne','host_bad')
 r.alu('cmp',m('edx',80),0x3462c0);r.j('jb','host_bad');r.load('eax',m('edx',94),'zx16');r.test('eax',0x40);r.j('jnz','host_bad')
 for name,desc in INPUT['fingerprints'].items():
  raw=bytes.fromhex(desc['bytes']);at=int(desc['rva'],16)
  for off in range(0,len(raw)//4*4,4):r.alu('cmp',m('esi',at+off),struct.unpack_from('<I',raw,off)[0]);r.j('jne','host_bad')
  for off in range(len(raw)//4*4,len(raw)):
   r.load('eax',m('esi',at+off),'sx8');r.alu('and','eax',255);r.alu('cmp','eax',raw[off]);r.j('jne','host_bad')
 for slot,rva in [(12,0x186930),(16,0x1869f0),(20,0x186c70)]:r.lea('eax',m('esi',rva));r.alu('cmp',m('esi',0x3462a8+slot),'eax');r.j('jne','host_bad')
 r.mov('eax','esi');r.j('jmp','host_done');r.label('host_bad');r.mov('eax',0);r.label('host_done');r.epilogue(0,4)
 r.label('fatal_save');r.mov('edx',m('esp',4));r.test('edx','edx');r.j('jz','unknown_trap');pc(r,'fatal_pc');ptr(r,'eax','fatal_format');r.push('eax');ptr(r,'eax','fatal_title');r.push('eax');r.lea('eax',m('edx',0x1560));r.unary('call','eax');r.op('ud2 unexpected fatal handler return',b'\x0f\x0b')

def archive(r):
 # stdcall(confirmed host,archive,expected mode). Does not read foreign layout.
 r.label('archive');r.prologue(0);r.mov('esi',m('ebp',8));r.test('esi','esi');r.j('jz','archive_bad');r.mov('edi',m('ebp',12));r.test('edi','edi');r.j('jz','archive_bad');r.lea('eax',m('esi',0x3462a8));r.alu('cmp',m('edi'),'eax');r.j('jne','archive_bad')
 for off,rva in [(12,0x186930),(16,0x1869f0),(20,0x186c70)]:r.lea('eax',m('esi',rva));r.alu('cmp',m('esi',0x3462a8+off),'eax');r.j('jne','archive_bad')
 r.load('eax',m('edi',8),'sx8');r.alu('cmp','eax',m('ebp',16));r.j('jne','archive_bad');r.mov('ebx',m('edi',12));r.mov('ecx',m('edi',16));r.alu('cmp','ecx','ebx');r.j('ja','archive_bad');r.mov('edx',m('edi',20));r.test('edx','edx');r.j('jz','archive_bad');r.mov('eax','edx');r.alu('add','eax','ebx');r.j('jb','archive_bad');r.mov('eax',m('edi',24));r.alu('cmp','eax','edx');r.j('jb','archive_bad');r.alu('sub','eax','edx');r.alu('cmp','eax','ecx');r.j('ja','archive_bad');r.mov('eax',1);r.j('jmp','archive_done');r.label('archive_bad');r.mov('eax',0);r.label('archive_done');r.epilogue(0,12)

def peek(r):
 # Called only after host/archive guard: stdcall(archive,civ,N), -1 error,
 # 0 legacy, 2 valid record0,3 valid record1. No cursor mutation or Load call.
 r.label('peek');r.prologue(0);r.mov('edi',m('ebp',8));r.mov('esi',m('edi',24));r.mov('ecx','esi');r.alu('sub','ecx',m('edi',20));r.mov('ebx',m('edi',16));r.alu('sub','ebx','ecx');r.test('ebx','ebx');r.j('jz','peek_legacy')
 for off,byte in enumerate(MARKER):
  r.alu('cmp','ebx',off);r.j('jbe','peek_bad');r.load('eax',m('esi',off),'sx8');r.alu('and','eax',255);r.alu('cmp','eax',byte);r.j('jne','peek_legacy')
 r.alu('cmp','ebx',36);r.j('jb','peek_bad')
 for off,val in [(16,1),(20,36)]:r.alu('cmp',m('esi',off),val);r.j('jne','peek_bad')
 for off,arg in [(24,12),(32,16)]:r.mov('eax',m('ebp',arg));r.alu('cmp',m('esi',off),'eax');r.j('jne','peek_bad')
 r.mov('eax',m('esi',28));r.alu('cmp','eax',1);r.j('ja','peek_bad');r.alu('add','eax',2);r.j('jmp','peek_done');r.label('peek_legacy');r.mov('eax',0);r.j('jmp','peek_done');r.label('peek_bad');r.mov('eax',-1);r.label('peek_done');r.epilogue(0,12)

def payload(N):
 r=X86()
 for name,rva in [('AddSymbol',0x38bf0),('GetSymbol',0x389e0),('RegisterInit',0x3bf50),('SetValue',0x3b790),('FireRules',0x38ff0),('AiMain_Save',0x27c0),('AiMain_Load',0x2c50),('reload_rest',0x61f5)]:r.labels[name]=rva-BASE
 registration(r);begin(r,N);save(r,N);load(r,N);reload(r);symbols(r);host(r);archive(r);peek(r)
 r.label('trap');r.label('unknown_trap');r.op('ud2 candidate contract failed without host handler',b'\x0f\x0b');code_end=len(r.code)
 for name,data in [('completed_name',b'opening_completed\0'),('required_name',b'opening_required\0'),('fatal_title',b'CTP I B2\0'),('fatal_format',b'B2 save rejected: invalid opening state or archive contract.\0')]:r.label(name);r.op('constant '+name,data)
 return r.finish(),r,code_end

def build(N):
 assert N in (25,30);assert sha((ROOT/'ONTWERP/GEZAMENLIJKE-OPENING-B2.md').read_bytes())==INPUT['design_sha256']
 blob=(OUT/'backup/robotcom.original.dll').read_bytes();assert sha(blob)==INPUT['original_dll_sha256'];p=pefile.PE(data=blob);code,r,code_end=payload(N);data=bytearray(blob);changes=[]
 def change(at,b,why):
  before=bytes(data[at:at+len(b)]);data[at:at+len(b)]=b;changes.append({'offset':hex(at),'before':before.hex(),'after':b.hex(),'reason':why})
 for name,site in INPUT['sites'].items():
  rva=int(site['rva'],16);at=p.get_offset_from_rva(rva);assert blob[at:at+5].hex()==site['preimage'];label='reload' if name=='reload_entry' else name
  change(at,(b'\xe9' if name=='reload_entry' else b'\xe8')+struct.pack('<i',BASE+r.labels[label]-rva-5),name+' adapter')
 assert not any(blob[0x250:0x278]);raw=align(len(code),512)
 change(0x250,struct.pack('<8sIIIIIIHHI',b'.b2a',len(code),BASE,raw,len(blob),0,0,0,0,0x60000020),'new RX section')
 for obj,field,value,fmt in [(p.FILE_HEADER,'NumberOfSections',5,'H'),(p.OPTIONAL_HEADER,'SizeOfImage',align(BASE+len(code),4096),'I'),(p.OPTIONAL_HEADER,'SizeOfCode',p.OPTIONAL_HEADER.SizeOfCode+raw,'I')]:change(obj.get_field_absolute_offset(field),struct.pack('<'+fmt,value),field)
 data.extend(code+bytes(raw-len(code)));change(p.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum'),struct.pack('<I',pefile.PE(data=data).generate_checksum()),'checksum')
 manifest={'variant':'B2a-N'+str(N)+'-TECHNICAL','N':N,'production_N_chosen':False,'status':'BUILT; not yet checked or installed','design_sha256':INPUT['design_sha256'],'original_sha256':sha(blob),'candidate_sha256':sha(data),'payload_sha256':sha(code),'payload_rva':BASE,'payload_size':len(code),'code_size':code_end,'labels':r.labels,'changes':changes,'recipe':r.rows,'record':INPUT['record'],'layout_correction':{'external_pointer_actual':0,'checkpoint_old_field':4,'evidence':'constructor2003b6a2 mov[ebx],esi; SetValue2003b7b3 mov eax,[ecx]'},'host_binding':'PEB own main ImageBase, supported fixed non-ASLR400000, PE and archive/fatal/caller fingerprints, vtable+slots; no unknown-host enginehandler/layout access','scope':'B2a candidate only; no B2b/c, H3, installation or gameplay'}
 return bytes(data),code,manifest

if __name__=='__main__':
 for N in (25,30):
  data,code,manifest=build(N);assert(data,code,manifest)==build(N);name=manifest['variant'];dest=OUT/'candidates'/name;dest.mkdir(parents=True,exist_ok=True);(dest/'robotcom.dll').write_bytes(data);(OUT/(name+'.payload.bin')).write_bytes(code);(OUT/(name+'.manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
  rows=list(Cs(CS_ARCH_X86,CS_MODE_32).disasm(code[:manifest['code_size']],BASE));assert sum(i.size for i in rows)==manifest['code_size'];(OUT/(name+'.disassembly.txt')).write_text('\n'.join(f'{i.address:08x} {i.bytes.hex():24} {i.mnemonic} {i.op_str}' for i in rows)+'\n');print(json.dumps({'built':name,'bytes':len(code),'instructions':len(rows),'candidate_sha256':manifest['candidate_sha256']}))
