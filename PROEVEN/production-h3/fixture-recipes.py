"""Existing H1 own-process fixture method, extended with exact H3 ABIs.
These bytes never enter the production DLL and bind only own allocations.
"""
from pathlib import Path
import json,struct
from x86 import X86,mem as m
OUT=Path(__file__).resolve().parent/'helper';OUT.mkdir(exist_ok=True)
def save(name,r,fix=None):
 (OUT/(name+'.bin')).write_bytes(r.finish());(OUT/(name+'.recipe.json')).write_text(json.dumps({'labels':r.labels,'recipe':r.rows,'fixups':fix or []},indent=2)+'\n')

for argc in (3,4,5,6,7):
 r=X86();fix=[]
 def ptr(asm,op,offset):r.emit(asm,op+'00000000');fix.append({'at':len(r.code)-4,'context_offset':offset})
 for a in ('ebp','ebx','esi','edi'):r.push(a)
 ptr('fxsave original','0fae05',0x100);r.op('fninit',b'\xdb\xe3');r.op('fld1',b'\xd9\xe8');r.op('fldpi',b'\xd9\xeb');ptr('fxsave before','0fae05',0x300);ptr('before ESP','8925',40)
 for a,value in [('ebx',0x13579bdf),('esi',0x2468ace0),('edi',0x76543210),('ebp',0x55aa33cc)]:r.mov(a,value)
 for i in reversed(range(argc)):ptr('push arg'+str(i),'ff35',0x700+4*i)
 ptr('call target','ff15',112)
 for off,asm,op in [(36,'eax','a3'),(44,'esp','8925'),(48,'ebx','891d'),(52,'esi','8935'),(56,'edi','893d'),(60,'ebp','892d')]:ptr('store '+asm,op,off)
 ptr('fxsave after','0fae05',0x500);ptr('fxrstor original','0fae0d',0x100)
 for a in ('edi','esi','ebx','ebp'):r.pop(a)
 r.op('ret',b'\xc3');save('shim'+str(argc),r,fix)

def state(r,slot):
 r.mov('ecx',m('esp',4));r.mov('ecx',m('ecx',4));r.unary('inc',m('ecx',20));r.unary('inc',m('ecx',0x30+slot*4))
r=X86();state(r,0);r.mov('eax',m('ecx'));r.op('ret10h',b'\xc2\x10\x00');save('score',r)
r=X86();state(r,1);r.mov('eax',m('ecx',8));r.op('ret8',b'\xc2\x08\x00');save('gate',r)
r=X86();r.prologue(0);r.mov('esi',m('ebp',8));r.mov('esi',m('esi',4));r.unary('inc',m('esi',20));r.unary('inc',m('esi',0x38));r.mov('eax',m('esi',4));r.mov('edx',m('ebp',20));r.mov(m('edx'),'eax')
# Always copy full160 bytes to exercise raw-array guards, even invalid count.
r.mov('edi',m('ebp',24));r.alu('add','esi',0x200);r.mov('ecx',40);r.op('cld',b'\xfc');r.op('rep movsd',b'\xf3\xa5');r.mov('eax',0x7fffffff);r.epilogue(0,20);save('open',r)
for name,slot,data,status in [('terrain',3,0x400,12),('food',4,0x500,16)]:
 r=X86();state(r,slot);r.mov('edx',m('esp',8));r.load('eax',m('edx'),'zx16');r.shift('shl','eax',2);r.alu('add','eax','ecx');r.mov('eax',m('eax',data));r.mov('edx',m('esp',12));r.mov(m('edx'),'eax');r.mov('eax',m('ecx',status));r.op('ret0ch',b'\xc2\x0c\x00');save(name,r)
r=X86();r.mov('edx',m('esp',4));r.mov('eax',m('edx'));r.mov(m('ecx'),'eax');r.mov('eax',m('edx',4));r.mov(m('ecx',4),'eax');r.op('ret4',b'\xc2\x04\x00');save('convert',r)
# Improvement callbacks bind ONLY fixture's own state. Real delta ABI is ST0.
r=X86();r.mov('ecx',m('esp',4));r.mov('ecx',m('ecx',4));r.unary('inc',m('ecx',0x60));r.mov('eax',m('ecx',0x70));r.op('ret8',b'\xc2\x08\x00');save('available',r)
r=X86();r.mov('ecx',m('esp',4));r.mov('ecx',m('ecx',4));r.unary('inc',m('ecx',0x64));r.mov('edx',m('esp',20));r.mov('eax',m('ecx',0x78));r.mov(m('edx'),'eax');r.mov('eax',m('ecx',0x74));r.op('ret14h',b'\xc2\x14\x00');save('position',r)
r=X86();r.mov('ecx',m('esp',4));r.mov('ecx',m('ecx',4));r.unary('inc',m('ecx',0x68));r.mov('eax',m('esp',8));r.imul('eax','eax',8);r.alu('add','eax','ecx');r.fp('fld actual fixture delta','dd',0,m('eax',0x100));r.op('ret0ch',b'\xc2\x0c\x00');save('delta',r)
# Explicit own-allocation classifier trampoline for adapter fixtures only.
# Fixed host/model pointers supplied by own helper patchlist, never production.
r=X86();fix=[];r.prologue(0);r.emit('push explicit FixtureHostBinding','6800000000');fix.append({'at':len(r.code)-4,'kind':'host'})
for off in (20,16,12,8):r.push(m('ebp',off))
r.emit('mov eax,own modelentry','b800000000');fix.append({'at':len(r.code)-4,'kind':'model'});r.unary('call','eax');r.epilogue(0,16);save('fixture-classifier',r,fix)
print(json.dumps({'fixture_only':True,'files':len(list(OUT.glob('*.bin')))}))
