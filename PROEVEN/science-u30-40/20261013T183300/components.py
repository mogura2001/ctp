"""Finite native H3 components. All buffers caller-owned; no game writes."""
from x86 import X86,mem as m

def context(r,ai,world,fail):
 r.test(ai,ai);r.j('jz',fail);r.test(world,world);r.j('jz',fail)
 r.alu('cmp',m(ai,0x30),world);r.j('jne',fail)
 r.mov('eax',m(world));r.test('eax','eax');r.j('jz',fail)

def h2(r):
 r.label('capacity');r.prologue(224)
 r.zero(m('ebp',20),256);r.mov('edi',m('ebp',20));r.mov('esi',m('ebp',8));r.mov('ebx',m('ebp',12))
 r.mov(m('edi',4),1);context(r,'esi','ebx','h2_bad')
 r.mov('eax',m('ebp',16));r.test('eax','eax');r.j('jz','h2_bad');r.load('ecx',m('eax',4),'sx16')
 r.mov(m('edi',4),2);r.test('ecx','ecx');r.j('jnz','h2_bad')
 r.push('eax');r.push('ebx');r.mov('ecx',m('ebx'));r.unary('call',m('ecx',0x28))
 r.mov(m('edi',4),3);r.test('eax','eax');r.j('jz','h2_bad')
 # raw scratch [ebp-204 .. -45] exactly160 bytes; preceding count at-208.
 r.lea('edi',m('ebp',-204));r.zero('edi',160);r.mov('edi',m('ebp',20));r.mov(m('ebp',-208),0)
 r.lea('eax',m('ebp',-204));r.push('eax');r.lea('eax',m('ebp',-208));r.push('eax');r.push(m('ebp',16));r.push(m('esi',0x20));r.push('ebx')
 r.mov('ecx',m('ebx'));r.unary('call',m('ecx',0xac))
 r.mov('eax',m('ebp',-208));r.mov(m('edi',4),4);r.alu('cmp','eax',20);r.j('ja','h2_bad')
 r.mov(m('ebp',-16),0);r.mov(m('edi',8),0);r.mov(m('edi',12),0)
 r.label('h2_loop');r.mov('eax',m('ebp',-16));r.alu('cmp','eax',m('ebp',-208));r.j('jge','h2_complete')
 r.shift('shl','eax',3);r.lea('esi',m('ebp',-204));r.alu('add','esi','eax')
 r.load('eax',m('esi',4),'sx16');r.mov(m('edi',4),5);r.test('eax','eax');r.j('jnz','h2_bad')
 r.mov('edx',m('ebp',16));r.mov('eax',m('esi'));r.alu('cmp','eax',m('edx'));r.j('jne','h2_dedup_begin')
 r.load('eax',m('esi',4),'zx16');r.load('ecx',m('edx',4),'zx16');r.alu('cmp','eax','ecx');r.j('je','h2_next')
 r.label('h2_dedup_begin');r.mov('edx',0)
 r.label('h2_dedup');r.alu('cmp','edx',m('edi',8));r.j('jge','h2_unique')
 r.imul('eax','edx',12);r.lea('ecx',m('edi',16));r.alu('add','ecx','eax')
 r.mov('eax',m('esi'));r.alu('cmp','eax',m('ecx'));r.j('jne','h2_dedup_next')
 r.load('eax',m('esi',4),'zx16');r.load('ecx',m('ecx',4),'zx16');r.alu('cmp','eax','ecx');r.j('je','h2_next')
 r.label('h2_dedup_next');r.unary('inc','edx');r.j('jmp','h2_dedup')
 r.label('h2_unique');r.mov(m('ebp',-20),-1);r.lea('eax',m('ebp',-20));r.push('eax');r.push('esi');r.push('ebx');r.mov('ecx',m('ebx'));r.unary('call',m('ecx',0xa8))
 r.mov(m('edi',4),6);r.test('eax','eax');r.j('jz','h2_bad');r.mov('eax',m('ebp',-20));r.mov(m('edi',4),7);r.alu('cmp','eax',23);r.j('ja','h2_bad')
 r.imul('ecx',m('edi',8),12);r.lea('edx',m('edi',16));r.alu('add','edx','ecx');r.mov(m('edx',8),'eax')
 r.mov('ecx',m('esi'));r.mov(m('edx'),'ecx');r.load('ecx',m('esi',4),'zx16');r.mov(m('edx',4),'ecx');r.unary('inc',m('edi',8))
 for value in (8,20,22):r.alu('cmp','eax',value);r.j('je','h2_mountain')
 r.j('jmp','h2_next');r.label('h2_mountain');r.unary('inc',m('edi',12))
 r.label('h2_next');r.unary('inc',m('ebp',-16));r.j('jmp','h2_loop')
 r.label('h2_complete');r.mov(m('edi',4),0);r.mov('eax',1);r.alu('cmp',m('edi',12),3);r.j('jl','h2_publish');r.mov('eax',2)
 r.label('h2_publish');r.mov(m('edi'),'eax');r.j('jmp','h2_done')
 r.label('h2_bad');r.mov('ebx',m('edi',4));r.zero(m('ebp',20),256);r.mov('edi',m('ebp',20));r.mov(m('edi',4),'ebx');r.mov(m('edi',8),-1);r.mov(m('edi',12),-1);r.mov('eax',0)
 r.label('h2_done');r.epilogue(224,16)

def reader(r):
 # stdcall(World,pos,HostBinding,out40,isCenter), output first24 matches FOOD_ENTRY.
 r.label('food_reader');r.prologue(80);r.zero(m('ebp',20),40)
 r.mov('edi',m('ebp',20));r.mov('ebx',m('ebp',16));r.mov('esi',m('ebp',12))
 r.push('esi');r.lea('ecx',m('ebp',-28));r.unary('call',m('ebx',20))
 # Internal z=0; x,y independently checked against actual loaded dimensions.
 r.load('eax',m('ebp',-24),'sx16');r.test('eax','eax');r.j('jnz','food_bad')
 r.mov('edx',m('ebx'));r.load('eax',m('ebp',-28),'sx16');r.load('ecx',m('edx',0x67df20),'zx16');r.alu('cmp','eax','ecx');r.j('jae','food_bad')
 r.mov(m('ebp',-16),'eax');r.load('eax',m('ebp',-26),'sx16');r.load('ecx',m('edx',0x67df22),'zx16');r.alu('cmp','eax','ecx');r.j('jae','food_bad');r.mov(m('ebp',-20),'eax')
 r.mov('eax',m('ebx',4));r.test('eax','eax');r.j('jz','food_bad');r.mov('eax',m('eax',0x1c));r.test('eax','eax');r.j('jz','food_bad')
 r.mov('eax',m('eax'));r.test('eax','eax');r.j('jz','food_bad');r.mov('edx',m('ebp',-16));r.shift('shl','edx',2);r.alu('add','eax','edx');r.mov('eax',m('eax'));r.test('eax','eax');r.j('jz','food_bad')
 r.mov('edx',m('ebp',-20));r.shift('shl','edx',2);r.alu('add','eax','edx');r.mov('esi',m('eax'));r.test('esi','esi');r.j('jz','food_bad');r.mov(m('edi',36),'esi')
 # This normal route deliberately excludes all existing-city and unitfood contexts.
 r.alu('cmp',m('esi',20),0);r.j('jne','food_bad');r.mov('eax',m('esi',16));r.test('eax','eax');r.j('jz','food_no_armies');r.alu('cmp',m('eax',48),0);r.j('jne','food_bad')
 r.label('food_no_armies');r.load('eax',m('esi',13),'sx8');r.alu('cmp','eax',23);r.j('ja','food_bad')
 for value in (13,18,23):r.alu('cmp','eax',value);r.j('je','food_bad')
 # Center must be actual normal land, not water/beach/special layer terrain.
 r.alu('cmp',m('ebp',24),0);r.j('je','food_terrain_ok')
 for value in (10,11,12,14,15,16,17):r.alu('cmp','eax',value);r.j('je','food_bad')
 r.label('food_terrain_ok');r.mov(m('edi',12),'eax');r.mov('edx',m('ebx',8));r.test('edx','edx');r.j('jz','food_bad');r.alu('cmp','eax',m('edx'));r.j('jae','food_bad');r.mov('edx',m('edx',8));r.test('edx','edx');r.j('jz','food_bad');r.imul('eax','eax',192);r.alu('add','edx','eax')
 r.mov('eax',m('esi'));r.mov(m('edi',8),'eax');r.shift('shr','eax',6);r.alu('and','eax',7);r.alu('cmp','eax',4);r.j('ja','food_bad');r.mov(m('edi',16),'eax')
 r.label('food_good_loop');r.test('eax','eax');r.j('jz','food_good_done');r.unary('dec','eax');r.mov('ecx','eax');r.shift('shl','ecx',2);r.alu('add','ecx','edx');r.mov('ecx',m('ecx',0xa0));r.test('ecx','ecx');r.j('jz','food_good_loop');r.mov('edx','ecx')
 r.unary('inc','eax')
 r.label('food_good_done');r.mov(m('edi',16),'eax');r.mov(m('edi',32),'edx');r.mov('eax',m('edi',8));r.shift('shr','eax',4);r.alu('and','eax',3);r.mov(m('edi',20),'eax')
 # Signed64 environment sum; each input is int32. At most six addends cannot
 # overflow signed64; JO checks each pair nevertheless. Clamp/int32 overflow
 # are unsupported, never hidden by a saturated comparison.
 r.mov('eax',m('edx',8));r.op('cdq',b'\x99');r.mov(m('ebp',-40),'eax');r.mov(m('ebp',-36),'edx');r.mov('esi',m('edi',32))
 for label,shift,base in [('road',0,0x58),('irr',2,0x64),('mine',4,0x70)]:
  r.mov('eax',m('edi',8));r.shift('shr','eax',shift);r.alu('and','eax',3);r.test('eax','eax');r.j('jz','food_'+label+'_end');r.shift('shl','eax',2);r.alu('add','eax','esi');r.mov('ecx',m('eax',base));environment_add(r,'food_'+label)
  r.label('food_'+label+'_end')
 for label,mask,offset in [('river',0x800,0x58),('canal',0x200,0x54)]:
  r.test(m('edi',8),mask);r.j('jz','food_'+label+'_end');r.mov('ecx',m('esi',offset));environment_add(r,'food_'+label);r.label('food_'+label+'_end')
 r.mov('eax',m('ebp',-40));r.mov('edx',m('ebp',-36));r.test('edx','edx');r.j('jnz','food_bad');r.test('eax','eax');r.j('js','food_bad');r.mov(m('edi',4),'eax')
 r.mov(m('ebp',-44),-1);r.lea('eax',m('ebp',-44));r.push('eax');r.push(m('ebp',12));r.push(m('ebp',8));r.mov('eax',m('ebp',8));r.mov('ecx',m('eax'));r.unary('call',m('ecx',0xb8));r.test('eax','eax');r.j('jz','food_bad');r.mov('eax',m('ebp',-44));r.alu('cmp','eax',m('edi',4));r.j('jne','food_bad')
 r.alu('cmp',m('ebp',24),0);r.j('je','food_success');r.mov('ecx',m('esi',0x50));r.test('ecx','ecx');r.j('jz','food_success')
 r.mov('eax',m('ecx'));r.op('cdq',b'\x99');r.mov(m('edi',24),'eax');r.mov(m('edi',28),'edx');r.alu('add',m('ebp',-40),'eax');r.alu('adc',m('ebp',-36),'edx');r.j('jo','food_bad');r.mov('eax',m('ebp',-40));r.alu('cmp',m('ebp',-36),0);r.j('jne','food_bad');r.test('eax','eax');r.j('js','food_bad')
 r.label('food_success');r.mov(m('edi'),1);r.mov('eax',1);r.j('jmp','food_done')
 r.label('food_bad');r.zero(m('ebp',20),40);r.mov('eax',0)
 r.label('food_done');r.epilogue(80,20)

def environment_add(r,label):
 r.test('ecx','ecx');r.j('jz',label+'_skip');r.mov('eax',m('ecx'));r.op('cdq',b'\x99');r.alu('add',m('ebp',-40),'eax');r.alu('adc',m('ebp',-36),'edx');r.j('jo','food_bad');r.label(label+'_skip')

def poscmp(r):
 r.label('poscmp');r.mov('ecx',m('esp',4));r.mov('edx',m('esp',8))
 for offset in (0,2,4):
  r.load('eax',m('ecx',offset),'sx16');r.push('ebx');r.load('ebx',m('edx',offset),'sx16');r.alu('cmp','eax','ebx');r.pop('ebx');r.j('jl','poscmp_lt');r.j('jg','poscmp_gt')
 r.mov('eax',0);r.op('ret8',b'\xc2\x08\x00');r.label('poscmp_lt');r.mov('eax',-1);r.op('ret8',b'\xc2\x08\x00');r.label('poscmp_gt');r.mov('eax',1);r.op('ret8',b'\xc2\x08\x00')
