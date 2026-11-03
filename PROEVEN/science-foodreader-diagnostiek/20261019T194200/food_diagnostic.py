"""SCI-only clone of the pinned reader; staging instrumentation is GPR/flags neutral.

No emitter is invoked by importing this file. No x87 instruction, foreign
logging load, callback, host allocation or policy change is introduced.
"""
from x86 import mem as m
from food_diagnostic_layout import FIELDS,BRANCHES,FRAME_SIZE,STAGING,ACTIVE,PLAN_SPILL,RECORD_OFFSET,RECORD_SIZE

class FoodStage:
 """Finite stores for this one record; source operands are regs/own locals."""
 SAVED={'edi':0,'esi':4,'ebp':8,'ebx':16,'edx':20,'ecx':24,'eax':28}
 def __init__(self,r,context):self.r=r;self.context=context;self.ids=[]
 def begin(self):self.r.op('diagnostic pushfd',b'\x9c');self.r.op('diagnostic pushad',b'\x60')
 def end(self):self.r.op('diagnostic popad',b'\x61');self.r.op('diagnostic popfd',b'\x9d')
 def source(self,value):
  if isinstance(value,str):self.r.mov('eax',m('esp',self.SAVED[value]))
  else:
   if isinstance(value,tuple):assert value[0]=='ebp','logging reads only own EBP locals'
   self.r.mov('eax',value)
 def bit(self,bit):self.r.alu('or',m('ebp',STAGING+32+(bit//32)*4),1<<(bit%32))
 def store(self,name,value,extra=0):
  off,fmt,bit=FIELDS[name];self.source(value)
  if fmt=='H':self.r.word(m('ebp',STAGING+off+extra),'eax')
  else:self.r.mov(m('ebp',STAGING+off+extra),'eax')
  if bit is not None:self.bit(bit)
 def capture(self,*values):
  self.begin()
  for row in values:self.store(*row)
  self.end()
 def pair(self,name,low=m('ebp',-40),high=m('ebp',-36)):
  return [(name,low,0),(name,high,4)]
 def edge(self,predicate,branch,a,b):
  assert branch not in self.ids and 1<=branch<=37;self.ids.append(branch)
  self.capture(('guard_a',a),('guard_b',b));self.r.j(predicate,'food_failure_'+str(branch))
 def pointer_before(self,parent,offset):self.capture(('pointer_parent',parent),('pointer_offset',offset))
 def pointer_after(self,value):self.capture(('pointer_value',value))
 def initialize(self):
  r=self.r;self.begin();r.mov(m('ebp',ACTIVE),0);r.mov(m('ebp',PLAN_SPILL),0)
  r.lea('edi',m('ebp',STAGING));r.zero('edi',RECORD_SIZE)
  r.j('call','food_binding_pc');r.label('food_binding_pc');r.pop('esi');r.rva('sub esi,own diagnostic PC','81ee',r.name('food_binding_pc'))
  r.rva('lea edi,own Plan','8dbe',self.context['plan'])
  r.alu('cmp',m('edi',36),1);r.j('jne','food_binding_done');r.alu('cmp',m('edi',40),1);r.j('jne','food_binding_done')
  r.mov('eax',m('edi',8));r.test('eax','eax');r.j('jz','food_binding_done');r.alu('cmp','eax',m('edi',0x78800));r.j('jne','food_binding_done')
  r.mov('edx',m('edi',32));r.test('edx','edx');r.j('jz','food_binding_done');r.alu('cmp','edx',m('edi',0x78804));r.j('jne','food_binding_done')
  r.mov('ecx',m('edi',220));r.alu('cmp','ecx',1);r.j('jb','food_binding_done');r.alu('cmp','ecx',64);r.j('ja','food_binding_done')
  r.alu('cmp','ecx',m('edi',240));r.j('jne','food_binding_done');r.mov('ebx',m('edi',224));r.alu('cmp','ebx',64);r.j('ja','food_binding_done');r.alu('cmp','ecx','ebx');r.j('ja','food_binding_done')
  r.unary('dec','ecx');r.mov(m('ebp',STAGING+24),'ecx')
  r.mov('ebx',m('edi',256));r.alu('cmp','ebx',1);r.j('jb','food_binding_done');r.alu('cmp','ebx',1344);r.j('ja','food_binding_done');r.mov(m('ebp',STAGING+28),'ebx')
  r.lea('ebx',m('edi',144));r.alu('cmp','ebx',m('ebp',16));r.j('jne','food_binding_done')
  r.mov('ebx',m('edi',112));r.alu('cmp','ebx',m('ebp',8));r.j('jne','food_binding_done')
  r.mov('ebx',m('ebp'));r.lea('ebx',m('ebx',-184));r.alu('cmp','ebx',m('ebp',20));r.j('jne','food_binding_done')
  r.alu('cmp',m('ebp',24),1);r.j('je','food_bind_center');r.alu('cmp',m('ebp',24),0);r.j('jne','food_binding_done')
  r.rva('lea ebx,SCI primary return','8d9e',self.context['tile_return']);r.alu('cmp','ebx',m('ebp',4));r.j('jne','food_binding_done')
  r.mov(m('ebp',STAGING+12),2)
  # The primary position must be one of this result's <=20 own tile positions.
  r.imul('ebx','ecx',2048);r.alu('add','ebx','edi');r.alu('add','ebx',0x54800)
  r.mov('eax',m('ebx',16));r.alu('cmp','eax',20);r.j('ja','food_binding_done')
  r.alu('add','ebx',136);r.mov('eax',m('ebp',12));r.alu('sub','eax','ebx');r.j('jb','food_binding_done')
  r.alu('cmp','eax',19*96);r.j('ja','food_binding_done');r.mov('edx',0);r.mov('ebx',96);r.ins('diagnostic own-index div','f7',6,'ebx');r.test('edx','edx');r.j('jnz','food_binding_done')
  r.imul('ebx','ecx',2048);r.alu('add','ebx','edi');r.alu('add','ebx',0x54800);r.alu('cmp','eax',m('ebx',16));r.j('jae','food_binding_done');r.j('jmp','food_bind_position')
  r.label('food_bind_center');r.rva('lea ebx,SCI center return','8d9e',self.context['center_return']);r.alu('cmp','ebx',m('ebp',4));r.j('jne','food_binding_done');r.mov(m('ebp',STAGING+12),1)
  r.imul('ebx','ecx',4);r.alu('add','ebx','edi');r.mov('ebx',m('ebx',0x526a0));r.alu('cmp',m('edi',68),4096);r.j('ja','food_binding_done');r.alu('cmp','ebx',m('edi',68));r.j('jae','food_binding_done')
  r.imul('ebx','ebx',8);r.alu('add','ebx','edi');r.alu('add','ebx',0x200);r.alu('cmp','ebx',m('ebp',12));r.j('jne','food_binding_done')
  r.label('food_bind_position')
  # Only the now-proven Plan-owned eight bytes are copied; never foreign pos.
  r.mov('ebx',m('ebp',12))
  for off in (0,4):r.mov('eax',m('ebx',off));r.mov(m('ebp',STAGING+40+off),'eax')
  r.mov('eax',m('edi',8));r.mov(m('ebp',STAGING+16),'eax');r.mov('eax',m('edi',32));r.mov(m('ebp',STAGING+20),'eax');r.mov(m('ebp',STAGING),1)
  r.mov(m('ebp',PLAN_SPILL),'edi');r.mov(m('ebp',ACTIVE),1)
  self.bit(0);self.bit(1)
  r.label('food_binding_done');self.end()
  self.capture(('world',m('ebp',8)),('outpointer',m('ebp',20)),('bindingpointer',m('ebp',16)),('native_called',0))
 def failures_and_publish(self):
  r=self.r
  assert sorted(self.ids)==list(range(1,38)),self.ids
  for branch,_,_ in BRANCHES:
   r.label('food_failure_'+str(branch));self.begin()
   r.mov('eax',m('esp',32));r.mov(m('ebp',STAGING+208),'eax');self.bit(37);r.mov(m('ebp',STAGING+8),branch)
   r.j('call','food_publish');self.end();r.label('food_failure_'+str(branch)+'_restored');r.j('jmp','food_bad')
  r.label('food_publish');r.alu('cmp',m('ebp',ACTIVE),1);r.j('jne','food_publish_done');r.mov('edi',m('ebp',PLAN_SPILL))
  r.alu('cmp',m('edi',36),1);r.j('jne','food_publish_done');r.alu('cmp',m('edi',40),1);r.j('jne','food_publish_done')
  for state,stage in ((8,16),(32,20),(0x78800,16),(0x78804,20)):
   r.mov('eax',m('ebp',STAGING+stage));r.alu('cmp','eax',m('edi',state));r.j('jne','food_publish_done')
  # Revalidate active prefix/call admission after the existing native query.
  r.mov('eax',m('ebp',STAGING+24));r.mov('ecx',m('edi',220));r.unary('dec','ecx');r.alu('cmp','eax','ecx');r.j('jne','food_publish_done');r.alu('cmp','eax',m('edi',224));r.j('jae','food_publish_done');r.alu('cmp',m('edi',224),64);r.j('ja','food_publish_done')
  r.mov('eax',m('edi',220));r.alu('cmp','eax',m('edi',240));r.j('jne','food_publish_done')
  r.lea('edi',m('edi',RECORD_OFFSET));r.alu('cmp',m('edi',4),1);r.j('jne','food_publish_write');r.alu('cmp',m('edi',12),1);r.j('jne','food_publish_write')
  for off in (16,20):
   r.mov('eax',m('ebp',STAGING+off));r.alu('cmp','eax',m('edi',off));r.j('jne','food_publish_write')
  r.j('jmp','food_publish_done') # first center failure is latched for owner/gen
  r.label('food_publish_write');r.mov(m('edi',4),0)
  for off in range(0,RECORD_SIZE,4):
   if off!=4:r.mov('eax',m('ebp',STAGING+off));r.mov(m('edi',off),'eax')
  r.mov(m('edi',4),1) # release marker LAST; no success path calls publish
  r.label('food_publish_done');r.op('diagnostic own publish ret',b'\xc3')

def emit_reader(r,context):
 d=FoodStage(r,context)
 r.label('food_reader');r.prologue(FRAME_SIZE);d.initialize();r.zero(m('ebp',20),40)
 r.mov('edi',m('ebp',20));r.mov('ebx',m('ebp',16));r.mov('esi',m('ebp',12))
 r.push('esi');r.lea('ecx',m('ebp',-28));r.unary('call',m('ebx',20))
 d.capture(('internal',m('ebp',-28),0),('internal',m('ebp',-24),4))
 r.load('eax',m('ebp',-24),'sx16');r.test('eax','eax');d.edge('jnz',1,'eax',0)
 r.mov('edx',m('ebx'));r.load('eax',m('ebp',-28),'sx16');r.load('ecx',m('edx',0x67df20),'zx16');d.capture(('width','ecx'));r.alu('cmp','eax','ecx');d.edge('jae',2,'eax','ecx')
 r.mov(m('ebp',-16),'eax');r.load('eax',m('ebp',-26),'sx16');r.load('ecx',m('edx',0x67df22),'zx16');d.capture(('height','ecx'));r.alu('cmp','eax','ecx');d.edge('jae',3,'eax','ecx');r.mov(m('ebp',-20),'eax')
 d.pointer_before('ebx',4);r.mov('eax',m('ebx',4));d.pointer_after('eax');r.test('eax','eax');d.edge('jz',4,'eax',0)
 d.pointer_before('eax',0x1c);r.mov('eax',m('eax',0x1c));d.pointer_after('eax');r.test('eax','eax');d.edge('jz',5,'eax',0)
 d.pointer_before('eax',0);r.mov('eax',m('eax'));d.pointer_after('eax');r.test('eax','eax');d.edge('jz',6,'eax',0)
 r.mov('edx',m('ebp',-16));r.shift('shl','edx',2);r.alu('add','eax','edx');d.pointer_before('eax',0);r.mov('eax',m('eax'));d.pointer_after('eax');r.test('eax','eax');d.edge('jz',7,'eax',0)
 r.mov('edx',m('ebp',-20));r.shift('shl','edx',2);r.alu('add','eax','edx');d.pointer_before('eax',0);r.mov('esi',m('eax'));d.pointer_after('esi');d.capture(('cell','esi'));r.test('esi','esi');d.edge('jz',8,'esi',0);r.mov(m('edi',36),'esi')
 # One original memory CMP becomes one LOAD+CMP, with ECX restored before Jcc.
 r.push('ecx');r.mov('ecx',m('esi',20));d.capture(('cityhandle','ecx'));r.alu('cmp','ecx',0);d.capture(('guard_a','ecx'),('guard_b',0));r.pop('ecx');r.j('jne','food_failure_9');d.ids.append(9)
 r.mov('eax',m('esi',16));d.capture(('armyarray','eax'));r.test('eax','eax');r.j('jz','food_no_armies')
 r.push('ecx');r.mov('ecx',m('eax',48));d.capture(('unitcount','ecx'));r.alu('cmp','ecx',0);d.capture(('guard_a','ecx'),('guard_b',0));r.pop('ecx');r.j('jne','food_failure_10');d.ids.append(10)
 r.label('food_no_armies');r.load('eax',m('esi',13),'sx8');d.capture(('terrain','eax'));r.alu('cmp','eax',23);d.edge('ja',11,'eax',23)
 for branch,value in ((12,13),(13,18),(14,23)):r.alu('cmp','eax',value);d.edge('je',branch,'eax',value)
 r.alu('cmp',m('ebp',24),0);r.j('je','food_terrain_ok')
 for branch,value in ((15,10),(16,11),(17,12),(18,14),(19,15),(20,16),(21,17)):r.alu('cmp','eax',value);d.edge('je',branch,'eax',value)
 r.label('food_terrain_ok');r.mov(m('edi',12),'eax');r.mov('edx',m('ebx',8));d.capture(('terrain_db','edx'));r.test('edx','edx');d.edge('jz',22,'edx',0)
 r.push('ecx');r.mov('ecx',m('edx'));d.capture(('terrain_count','ecx'));r.alu('cmp','eax','ecx');d.capture(('guard_a','eax'),('guard_b','ecx'));r.pop('ecx');r.j('jae','food_failure_23');d.ids.append(23)
 r.mov('edx',m('edx',8));d.capture(('recordarray','edx'));r.test('edx','edx');d.edge('jz',24,'edx',0);r.imul('eax','eax',192);r.alu('add','edx','eax');d.capture(('mainrecord','edx'))
 r.mov('eax',m('esi'));r.mov(m('edi',8),'eax');d.capture(('cellflags','eax'));r.shift('shr','eax',6);r.alu('and','eax',7);d.capture(('rawgood','eax'));r.alu('cmp','eax',4);d.edge('ja',25,'eax',4);r.mov(m('edi',16),'eax')
 r.label('food_good_loop');r.test('eax','eax');r.j('jz','food_good_done');r.unary('dec','eax');r.mov('ecx','eax');r.shift('shl','ecx',2);r.alu('add','ecx','edx');r.mov('ecx',m('ecx',0xa0));r.test('ecx','ecx');r.j('jz','food_good_loop');r.mov('edx','ecx');r.unary('inc','eax')
 r.label('food_good_done');r.mov(m('edi',16),'eax');r.mov(m('edi',32),'edx');d.capture(('chosengood','eax'),('chosenrecord','edx'));r.mov('eax',m('edi',8));r.shift('shr','eax',4);r.alu('and','eax',3);r.mov(m('edi',20),'eax')
 r.mov('eax',m('edx',8));r.op('cdq',b'\x99');r.mov(m('ebp',-40),'eax');r.mov(m('ebp',-36),'edx');d.capture(('basefood','eax'),('sum_before','eax',0),('sum_before','edx',4),('sum_after','eax',0),('sum_after','edx',4),('addend_stage',0));r.mov('esi',m('edi',32))
 for label,field,shift,base,stage,branch in (('road','road',0,0x58,1,26),('irr','irrigation',2,0x64,2,27),('mine','mine',4,0x70,3,28)):
  r.mov('eax',m('edi',8));r.shift('shr','eax',shift);r.alu('and','eax',3);d.capture((field,0));r.test('eax','eax');r.j('jz','food_'+label+'_end');r.shift('shl','eax',2);r.alu('add','eax','esi');r.mov('ecx',m('eax',base));emit_environment_add(r,d,'food_'+label,field,stage,branch);r.label('food_'+label+'_end')
 for label,mask,offset,stage,branch in (('river',0x800,0x58,4,29),('canal',0x200,0x54,5,30)):
  d.capture((label,0));r.test(m('edi',8),mask);r.j('jz','food_'+label+'_end');r.mov('ecx',m('esi',offset));emit_environment_add(r,d,'food_'+label,label,stage,branch);r.label('food_'+label+'_end')
 r.mov('eax',m('ebp',-40));r.mov('edx',m('ebp',-36));r.test('edx','edx');d.edge('jnz',31,'eax','edx');r.test('eax','eax');d.edge('js',32,'eax','edx');r.mov(m('edi',4),'eax')
 r.mov(m('ebp',-44),-1);d.capture(('output_before',m('ebp',-44)));r.lea('eax',m('ebp',-44));r.push('eax');r.push(m('ebp',12));r.push(m('ebp',8));r.mov('eax',m('ebp',8));r.mov('ecx',m('eax'));d.capture(('native_vtable','ecx'),('native_called',1));r.unary('call',m('ecx',0xb8));d.capture(('native_return','eax'),('output_after',m('ebp',-44)));r.test('eax','eax');d.edge('jz',33,'eax',0)
 r.mov('eax',m('ebp',-44));r.push('ecx');r.mov('ecx',m('edi',4));r.alu('cmp','eax','ecx');d.capture(('guard_a','eax'),('guard_b','ecx'));r.pop('ecx');r.j('jne','food_failure_34');d.ids.append(34)
 r.alu('cmp',m('ebp',24),0);r.j('je','food_success');r.mov('ecx',m('esi',0x50));d.capture(('bonuspointer','ecx'));r.test('ecx','ecx');r.j('jz','food_success')
 r.mov('eax',m('ecx'));r.op('cdq',b'\x99');r.mov(m('edi',24),'eax');r.mov(m('edi',28),'edx');d.capture(('bonus','eax'),*d.pair('center_before'),('addend_stage',6));r.alu('add',m('ebp',-40),'eax');r.alu('adc',m('ebp',-36),'edx');d.capture(*d.pair('center_after'));d.edge('jo',35,m('ebp',-40),m('ebp',-36))
 r.mov('eax',m('ebp',-40));r.alu('cmp',m('ebp',-36),0);d.edge('jne',36,'eax',m('ebp',-36));r.test('eax','eax');d.edge('js',37,'eax',m('ebp',-36))
 r.label('food_success');r.mov(m('edi'),1);r.mov('eax',1);r.j('jmp','food_done')
 r.label('food_bad');r.zero(m('ebp',20),40);r.mov('eax',0)
 r.label('food_done');r.epilogue(FRAME_SIZE,20)
 d.failures_and_publish()

def emit_environment_add(r,d,label,field,stage,branch):
 d.capture(('environment','ecx'));r.test('ecx','ecx');r.j('jz',label+'_skip');r.mov('eax',m('ecx'));r.op('cdq',b'\x99');d.capture((field,'eax'),*d.pair('sum_before'),('addend_stage',stage))
 r.alu('add',m('ebp',-40),'eax');r.alu('adc',m('ebp',-36),'edx');d.capture(*d.pair('sum_after'));d.edge('jo',branch,m('ebp',-40),m('ebp',-36));r.label(label+'_skip')
