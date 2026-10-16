"""C2 source-only positive NOW/production union, one slot and shared matching."""
import native as n
from x86 import mem as m
SCI=0x54800;ALT=0x74800;SCRATCH=0x78800
COUNTERS={'calls':(232,64),'tiles':(236,1280),'spatial':(240,1280),'improvement':(244,3840),'primary_food':(248,1344),'development_food':(252,1280),'total_food':(256,2624)}
CONTEXT_ERROR=260
_serial=0

def counter(r,names,fail):
 """At actual query sites, before arguments/writes. Preserve regs/flags/x87."""
 global _serial
 _serial+=1;p='c2_count_'+str(_serial)
 r.op('pushfd C2 budget',b'\x9c');r.op('pushad C2 budget',b'\x60');r.j('call',p+'_pc');r.label(p+'_pc');r.pop('esi');r.rva('sub esi,modulepc','81ee',p+'_pc');r.rva('lea ebx,own pass','8d9e','pass_state')
 for off,value in [(n.P['scope'],1),(n.P['guard'],1)]:r.alu('cmp',m('ebx',off),value);r.j('jne',p+'_context')
 for source,cached in [(n.P['owner'],SCRATCH),(n.P['generation'],SCRATCH+4)]:r.mov('eax',m('ebx',source));r.alu('cmp','eax',m('ebx',cached));r.j('jne',p+'_context')
 for name in names:
  off,limit=COUNTERS[name];r.alu('cmp',m('ebx',off),limit);r.j('jae',p+'_budget')
 for name in names:r.unary('inc',m('ebx',COUNTERS[name][0]))
 r.op('popad C2 budget',b'\x61');r.op('popfd C2 budget',b'\x9d');r.j('jmp',p+'_done')
 r.label(p+'_context');r.mov(m('ebx',CONTEXT_ERROR),1);r.j('jmp',p+'_fail');r.label(p+'_budget');r.mov(m('ebx',n.P['cutoff']),1)
 r.label(p+'_fail');r.op('popad C2 failed budget',b'\x61');r.op('popfd C2 failed budget',b'\x9d');r.j('jmp',fail);r.label(p+'_done')

def choose(r):
 n.entry(r,'choose_alternative',16);r.mov('edi',m('ebp',12));r.mov('esi',m('ebp',16))
 for src,dst in [(8,28),(4,72),(12,76),(56,88),(64,84)]:r.mov('eax',m('esi',src));r.mov(m('edi',dst),'eax')
 for off in range(0,40,4):r.mov('eax',m('esi',16+off));r.mov(m('edi',32+off),'eax')
 r.mov('eax',m('esi',4));r.unary('dec','eax');r.mov(m('edi',80),'eax');r.mov(m('edi',92),1);r.mov('eax',1);n.result(r,'choose_alternative_done',16,12)

def validate(r):
 n.entry(r,'validate_alternative',32);r.mov('esi',m('ebp',12));r.mov('eax',m('esi',8));r.alu('cmp','eax',4);r.j('jl','alt_bad');r.alu('cmp','eax',5);r.j('jg','alt_bad');r.mov('ecx',0)
 r.label('alt_outer');r.alu('cmp','ecx',m('esi',8));r.j('jge','alt_ok');r.mov('eax','ecx');r.shift('shl','eax',3);r.alu('add','eax','esi');r.load('edx',m('eax',20),'sx16');r.test('edx','edx');r.j('jnz','alt_bad');r.mov('edx',0)
 r.label('alt_inner');r.alu('cmp','edx','ecx');r.j('jge','alt_next');r.mov('edi','edx');r.shift('shl','edi',3);r.alu('add','edi','esi');r.mov('edi',m('edi',16));r.alu('cmp','edi',m('eax',16));r.j('je','alt_bad');r.unary('inc','edx');r.j('jmp','alt_inner')
 r.label('alt_next');r.unary('inc','ecx');r.j('jmp','alt_outer');r.label('alt_ok');r.mov('eax',1);r.j('jmp','alt_done');r.label('alt_bad');r.mov('eax',0);n.result(r,'alt_done',32,8)

def roles(r):
 n.entry(r,'location_roles',112);r.alu('cmp',m('ebx',n.P['scope']),1);r.j('jne','roles_bad');r.alu('cmp',m('ebx',n.P['guard']),0);r.j('jne','roles_bad');r.mov(m('ebx',n.P['guard']),1)
 for src,dst in [(n.P['owner'],SCRATCH),(n.P['generation'],SCRATCH+4)]:r.mov('eax',m('ebx',src));r.mov(m('ebx',dst),'eax')
 r.mov(m('ebx',n.P['slots']),0);r.mov(m('ebp',-16),0)
 r.label('roles_loop');r.mov('eax',m('ebp',-16));r.alu('cmp','eax',m('ebx',n.P['candidates']));r.j('jge','roles_ok');r.alu('cmp','eax',64);r.j('jae','roles_budget');r.shift('shl','eax',2);r.lea('edx',m('ebx',n.ORDER));r.alu('add','edx','eax');r.mov('eax',m('edx'));r.shift('shl','eax',3);r.lea('edi',m('ebx',n.CAPTURE));r.alu('add','edi','eax');r.mov(m('ebp',-24),'edi');r.unary('inc',m('ebx',n.P['classified']))
 r.imul('esi',m('ebx',n.P['slots']),n.SLOT_STRIDE);r.alu('add','esi','ebx');r.alu('add','esi',n.SLOTS);r.mov(m('ebp',-28),'esi')
 r.imul('eax',m('ebp',-16),256);r.alu('add','eax','ebx');r.alu('add','eax',ALT);r.mov(m('ebp',-32),'eax');r.alu('add','eax',128);r.mov(m('ebp',-36),'eax')
 r.imul('eax',m('ebp',-16),2048);r.alu('add','eax','ebx');r.alu('add','eax',SCI);r.mov(m('ebp',-40),'eax')
 r.zero(m('ebp',-28),n.SLOT_STRIDE);r.zero(m('ebp',-32),256);r.mov('edi',m('ebp',-24));r.mov('esi',m('ebp',-28))
 for off in (4,2,0):r.load('eax',m('edi',off),'sx16');r.push('eax')
 r.mov('eax',m('ebx',n.P['world']));r.push('eax');r.mov('edx',m('eax'));r.unary('call',m('edx',0x168));r.op('movsx eax,ax',b'\x0f\xbf\xc0');r.mov(m('ebp',-20),'eax');r.test('eax','eax');r.j('jle','roles_science')
 r.alu('cmp',m('ebx',n.P['h3calls']),64);r.j('jae','roles_budget');r.unary('inc',m('ebx',n.P['h3calls']));r.lea('eax',m('esi',128));r.push('eax');r.push('edi');r.push(m('ebx',n.P['world']));r.push(m('ebx',n.P['owner']));r.j('call','H3Classifier');r.test('eax','eax');r.j('jz','roles_bad');r.alu('cmp','eax',2);r.j('jne','roles_science');r.alu('cmp',m('esi',136),1);r.j('jne','roles_bad');r.mov('eax',m('esi',196));r.test('eax','eax');r.j('js','roles_science');r.j('jnz','roles_product');r.alu('cmp',m('esi',192),0);r.j('je','roles_science')
 r.label('roles_product');r.mov('edx',m('ebp',-32));r.mov(m('edx',4),1);r.mov(m('edx',8),5);r.mov('eax',m('ebp',-16));r.mov(m('edx',12),'eax');r.lea('eax',m('edx',16));r.push('eax');r.push('edi');r.push('ebx');r.j('call','canonical_key');r.test('eax','eax');r.j('jz','roles_bad')
 for i,idx in enumerate((100,104,108,112)):
  r.mov('eax',m('esi',128+idx));r.test('eax','eax');r.j('js','roles_bad');r.alu('cmp','eax',m('esi',224));r.j('jae','roles_bad');r.imul('eax','eax',12);r.alu('add','eax','esi');r.alu('add','eax',272);r.mov('edx',m('ebp',-32));r.lea('edx',m('edx',24+8*i));r.push('edx');r.push('eax');r.push('ebx');r.j('call','canonical_key');r.test('eax','eax');r.j('jz','roles_bad')
 r.push(m('ebp',-32));r.push('ebx');r.j('call','validate_alternative');r.test('eax','eax');r.j('jz','roles_bad');r.mov('eax',m('ebp',-32));r.mov(m('eax'),1)
 r.label('roles_science');counter(r,['calls'],'roles_budget');r.push(m('ebp',-40));r.lea('eax',m('ebx',144));r.push('eax');r.push(m('ebp',-24));r.push(m('ebx',n.P['world']));r.push(m('ebx',n.P['owner']));r.j('call','science_model')
 r.label('roles_postscience_context');counter(r,[],'roles_bad') # No query or counter increment.
 r.alu('cmp',m('ebx',CONTEXT_ERROR),0);r.j('jne','roles_bad');r.alu('cmp',m('ebx',n.P['cutoff']),0);r.j('jne','roles_budget');r.mov('esi',m('ebp',-40));r.alu('cmp',m('esi',112),1);r.j('jne','roles_bad');r.alu('cmp',m('esi'),2);r.j('jne','roles_commit')
 r.mov('edi',m('ebp',-36));r.mov(m('edi',4),2);r.mov(m('edi',8),4);r.mov('eax',m('esi',4));r.mov(m('edi',56),'eax');r.mov('eax',m('esi',12));r.mov(m('edi',64),'eax');r.mov('eax',m('ebp',-16));r.mov(m('edi',12),'eax')
 for off in (0,4):r.mov('eax',m('esi',116+off));r.mov(m('edi',16+off),'eax')
 for i in range(3):
  r.mov('eax',m('esi',28+4*i));r.test('eax','eax');r.j('js','roles_bad');r.alu('cmp','eax',m('esi',16));r.j('jae','roles_bad');r.imul('eax','eax',96);r.alu('add','eax','esi');r.alu('add','eax',128)
  for off in (0,4):r.mov('edx',m('eax',off));r.mov(m('edi',24+8*i+off),'edx')
 r.push('edi');r.push('ebx');r.j('call','validate_alternative');r.test('eax','eax');r.j('jz','roles_bad');r.mov('edi',m('ebp',-36));r.mov(m('edi'),1)
 r.label('roles_commit');r.mov('eax',m('ebp',-32));r.alu('cmp',m('eax'),1);r.j('je','roles_chosen');r.mov('eax',m('ebp',-36));r.alu('cmp',m('eax'),1);r.j('jne','roles_next')
 r.label('roles_chosen');r.push('eax');r.push(m('ebp',-28));r.push('ebx');r.j('call','choose_alternative');r.mov('esi',m('ebp',-28));r.mov('edi',m('ebp',-24))
 for off in (0,4):r.mov('eax',m('edi',off));r.mov(m('esi',off),'eax')
 r.lea('eax',m('esi',8));r.push('eax');r.push('edi');r.push('ebx');r.j('call','canonical_key');r.test('eax','eax');r.j('jz','roles_bad');r.mov('eax',m('ebp',-20));r.alu('cmp','eax',32767);r.j('je','roles_rank');r.unary('inc','eax');r.label('roles_rank');r.mov(m('esi',16),'eax');r.mov(m('esi',20),-1);r.mov(m('esi',24),-1);r.unary('inc',m('ebx',n.P['slots']))
 r.label('roles_next');r.unary('inc',m('ebp',-16));r.j('jmp','roles_loop');r.label('roles_budget');r.alu('cmp',m('ebx',CONTEXT_ERROR),0);r.j('jne','roles_bad');r.mov(m('ebx',n.P['cutoff']),1);r.label('roles_ok')
 r.label('roles_final_context');counter(r,[],'roles_bad') # Validate the prefix before guard teardown.
 r.mov(m('ebx',n.P['guard']),0);r.mov('eax',1);r.j('jmp','roles_done');r.label('roles_bad');r.mov(m('ebx',n.P['guard']),0);n.unknown(r,23);n.result(r,'roles_done',112)
 choose(r);validate(r)
