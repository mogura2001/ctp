"""Own reader factory; default body is an exact parent source copy."""
from x86 import mem as m

def _original_reader(r):
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


def _original_environment_add(r,label):
 r.test('ecx','ecx');r.j('jz',label+'_skip');r.mov('eax',m('ecx'));r.op('cdq',b'\x99');r.alu('add',m('ebp',-40),'eax');r.alu('adc',m('ebp',-36),'edx');r.j('jo','food_bad');r.label(label+'_skip')


class FoodLabels:
 def __init__(self,r,namespace):self.r=r;self.namespace=namespace
 def __getattr__(self,name):return getattr(self.r,name)
 def name(self,label):return self.namespace+label[4:] if label.startswith('food_') else label
 def label(self,label):return self.r.label(self.name(label))
 def j(self,kind,label):return self.r.j(kind,self.name(label))

def reader(r,namespace='food',diagnostic=None):
 if diagnostic is None:
  return _original_reader(r if namespace=='food' else FoodLabels(r,namespace))
 from food_diagnostic import emit_reader
 return emit_reader(FoodLabels(r,namespace),diagnostic)

def environment_add(r,label,namespace='food',diagnostic=None):
 if diagnostic is not None:raise ValueError('diagnostic environment additions belong to emit_reader staging')
 return _original_environment_add(r if namespace=='food' else FoodLabels(r,namespace),label)
