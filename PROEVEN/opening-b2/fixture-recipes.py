"""Own-allocation bounded native stubs/shims only. Never candidate bytes."""
import sys,json,struct
from pathlib import Path
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(OUT.parents[1]/'PROEVEN/production-h3'))
from x86 import X86,mem as m
HELP=OUT/'helper';HELP.mkdir(exist_ok=True)
def emit(name,r,fix=None):
 (HELP/(name+'.bin')).write_bytes(r.finish());(HELP/(name+'.recipe.json')).write_text(json.dumps({'labels':r.labels,'recipe':r.rows,'fixups':fix or []},indent=2)+'\n')
for argc in range(6):
 r=X86();fix=[]
 def p(asm,op,offset):r.emit(asm,op+'00000000');fix.append({'at':len(r.code)-4,'context_offset':offset})
 for a in ('ebp','ebx','esi','edi'):r.push(a)
 p('fxsave original','0fae05',0x100);r.op('fninit',b'\xdb\xe3');r.op('fld1',b'\xd9\xe8');r.op('fldpi',b'\xd9\xeb');p('fxsave before','0fae05',0x300);p('ESP before','8925',40)
 for a,val in [('ebx',0x13579bdf),('edi',0x76543210),('ebp',0x55aa33cc)]:r.mov(a,val)
 p('load ESI','8b35',120);p('load ECX','8b0d',116)
 for i in reversed(range(argc)):p('push arg'+str(i),'ff35',0x700+4*i)
 p('call candidate target','ff15',112);r.label('postcall')
 for off,asm,op in [(36,'eax','a3'),(44,'esp','8925'),(48,'ebx','891d'),(52,'esi','8935'),(56,'edi','893d'),(60,'ebp','892d')]:p('store '+asm,op,off)
 r.op('pushfd',b'\x9c');r.pop('eax');p('store postcall flags','a3',80)
 p('fxsave after','0fae05',0x500);p('fxrstor original','0fae0d',0x100)
 for a in ('edi','esi','ebx','ebp'):r.pop(a)
 r.op('ret',b'\xc3');emit('shim'+str(argc),r,fix)

r=X86();r.prologue(0);r.mov('ebx','ecx');r.unary('inc',m('ebx',16));r.mov('edx',m('ebp',8));r.load('eax',m('edx',1),'sx8');r.alu('cmp','eax',ord('p'));r.j('jne','old');r.load('eax',m('edx',8),'sx8');r.alu('cmp','eax',ord('c'));r.j('jne','required');r.mov('edi',m('ebx'));r.j('jmp','add');r.label('required');r.mov('edi',m('ebx',4));r.j('jmp','add');r.label('old');r.mov('edi',m('ebx',8));r.label('add')
r.mov('eax',m('ebp',12));r.mov(m('edi'),'eax');r.mov('eax',m('ebp',16));r.mov(m('edi',8),'eax');r.mov('eax',m('ebp',20));r.mov(m('edi',12),'eax');r.mov('eax',m('ebp',24));r.op('store type byte',b'\x88\x87\x6a\x00\x00\x00');r.mov(m('edi',0x68),0);r.mov(m('edi',0xc2),0);r.mov('eax',0x12345678)
for reg in ('edi','esi','ebx','ebp'):r.pop(reg)
r.alu('cmp','eax','eax');r.op('ret20',b'\xc2\x14\x00');emit('AddSymbol',r)
r=X86();r.mov('edx',m('esp',4));r.load('eax',m('edx',8),'sx8');r.alu('cmp','eax',ord('c'));r.j('jne','get_required');r.mov('eax',m('ecx'));r.j('jmp','get_done');r.label('get_required');r.mov('eax',m('ecx',4));r.label('get_done');r.op('ret4',b'\xc2\x04\x00');emit('GetSymbol',r)
r=X86();r.mov('edx',m('ecx',24));r.unary('inc',m('edx'));r.alu('cmp','eax','eax');r.op('ret4',b'\xc2\x04\x00');emit('FireRules',r)
r=X86();r.mov('edx',m('esp',4));r.mov('eax',m('edx',4));r.op('ret4',b'\xc2\x04\x00');emit('government',r)
for name,pop in [('AiMain_Save',4),('AiMain_Load',8)]:
 r=X86();r.mov('edx',m('ecx',0xe0));r.unary('inc',m('edx',0 if name.endswith('Save') else 4))
 if name.endswith('Load'):r.mov('eax',m('ecx',0xf0));r.mov(m('ecx',0xc4),'eax');r.mov('eax',m('edx',8))
 else:
  r.mov('eax',m('ecx',0xe4));r.test('eax','eax');r.j('jz','save_no_move');r.push('esi');r.push('edi');r.push('ebx');r.mov('ebx',m('esp',16));r.mov('esi',m('ebx',20));r.mov('edi','eax');r.mov('edx',m('ebx',24));r.alu('sub','edx','esi');r.mov(m('ebx',20),'eax');r.alu('add','eax','edx');r.mov(m('ebx',24),'eax');r.mov('ecx',m('ebx',16));r.op('cld',b'\xfc');r.op('rep movsb',b'\xf3\xa4')
  for reg in ('ebx','edi','esi'):r.pop(reg)
  r.label('save_no_move');r.mov('eax',0x13572468)
 r.alu('cmp','eax','eax');r.op('ret'+str(pop),b'\xc2'+struct.pack('<H',pop));emit(name,r)
r=X86();r.mov('edx',m('ecx',0xe0));r.unary('inc',m('edx',12));r.mov('eax',m('ecx',0xf0));r.mov(m('ecx',0xc4),'eax');r.mov('eax',1)
for reg in ('esi','ebx','ebp'):r.pop(reg)
r.alu('cmp','eax','eax');r.op('ret4',b'\xc2\x04\x00');emit('reload_rest',r)
for name,write in [('Store',True),('Load',False)]:
 r=X86();r.prologue(0);r.mov('ebx',m('ebp',8));r.mov('ecx',m('ebp',16));r.mov('edx',m('ebx',28));r.unary('inc',m('edx',16 if write else 20))
 if write:r.mov('esi',m('ebp',12));r.mov('edi',m('ebx',24))
 else:r.mov('esi',m('ebx',24));r.mov('edi',m('ebp',12))
 r.op('cld',b'\xfc');r.op('rep movsb',b'\xf3\xa4');r.mov('eax',m('ebp',16));r.alu('add',m('ebx',24),'eax')
 if write:r.alu('add',m('ebx',16),'eax')
 r.mov('eax',0);r.epilogue(0,12);emit(name,r)
# Save fatal recorder deliberately does not return: longjmps to own shim's
# postcall address, dropping the fatal stack. It records exact cdecl args and
# whether execution could have reached Store/success. No enginehandler executes.
r=X86();fix=[]
def ptr(reg,offset):r.emit('mov '+reg+',context','b8' if reg=='eax' else 'ba');r.code.extend(bytes(4));r.rows[-1]['bytes']+='00000000';fix.append({'at':len(r.code)-4,'context_offset':offset})
ptr('edx',0);r.unary('inc',m('edx',64));r.mov('eax',m('esp',4));r.mov(m('edx',68),'eax');r.mov('eax',m('esp',8));r.mov(m('edx',72),'eax');r.mov('esp',m('edx',40));r.mov('ebx',0x13579bdf);r.mov('esi',m('edx',120));r.mov('edi',0x76543210);r.mov('ebp',0x55aa33cc);r.mov('eax',-1);r.ins('jmp own shim postcall','ff',4,m('edx',124));r.op('ud2 no fixture fatal return',b'\x0f\x0b');emit('fatal',r,fix)
# Reproduce the concrete manager-zero instructions and ordering in own memory.
# Only the branch displacements/handlercall use own labels/handler; constants
# remain the exact engine operands and are recorded but never dereferenced.
r=X86();fix=[];r.prologue(0);r.push(m('ebp',12));r.push(m('ebp',8));r.emit('mov edx,own candidate load','ba00000000');fix.append({'at':len(r.code)-4,'context_offset':128});r.mov('edx',m('edx'));r.unary('call','edx')
r.test('eax','eax');r.j('jnz','manager_next');r.push(0xa20b8c);r.push(0xa20ba4);r.emit('mov edx,own fatal recorder','ba00000000');fix.append({'at':len(r.code)-4,'context_offset':132});r.mov('edx',m('edx'));r.unary('call','edx');r.alu('add','esp',8)
r.label('manager_next');r.emit('mov edx,own nextciv counter','ba00000000');fix.append({'at':len(r.code)-4,'context_offset':136});r.unary('inc',m('edx'));r.epilogue(0,8);emit('manager',r,fix)
print(json.dumps({'fixture_stubs':True,'helper_bins':len(list(HELP.glob('*.bin')))}))
