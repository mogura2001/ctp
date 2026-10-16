"""Current physical plan, exact scenario/ration arithmetic; native x86."""
from x86 import mem as m
from layout import *

class Scoped:
 def __init__(self,r,prefix):self.r=r;self.prefix=prefix
 def __getattr__(self,name):return getattr(self.r,name)
 def label(self,name):self.r.label(self.prefix+name)
 def j(self,kind,name):self.r.j(kind,name if name=='poscmp' else self.prefix+name)

def entryptr(r,index,dst):
 r.imul(dst,index,12);r.alu('add',dst,'edi');r.alu('add',dst,144)
def foodptr(r,index,dst):
 r.imul(dst,index,24);r.alu('add',dst,'edi');r.alu('add',dst,384)
def compare_indices(r,a,b):
 entryptr(r,b,'edx');r.push('edx');entryptr(r,a,'eax');r.push('eax');r.j('call','poscmp')

def model(r):
 r.label('current_model');r.prologue(384)
 # FSAVE/FRSTOR bracket private exact arithmetic and preserve caller x87
 # controlword/status/depth/registers. No integer rounding conversion is used.
 r.fp('fnsave','dd',6,m('ebp',-144));r.fp('fldcw caller controlword','d9',5,m('ebp',-144))
 r.zero(m('ebp',20),RESULT_SIZE);r.mov('edi',m('ebp',20));r.mov(m('edi',8),MODEL_ZERO_NEW_CITY_MODIFIERS);r.mov(m('edi',4),10)
 for off in (100,104,108,112):r.mov(m('edi',off),-1)
 r.mov('esi',m('ebp',16));r.test('esi','esi');r.j('jz','current_unknown');r.mov('eax',m('esi'));r.mov(m('edi',116),'eax');r.load('eax',m('esi',4),'zx16');r.mov(m('edi',120),'eax')
 r.lea('eax',m('edi',128));r.push('eax');r.push('esi');r.push(m('ebp',12));r.push(m('ebp',8));r.j('call','capacity');r.mov(m('edi',92),'eax');r.mov('ecx',m('edi',136));r.mov(m('edi',96),'ecx')
 r.test('eax','eax');r.j('jz','current_unknown');r.alu('cmp','eax',1);r.j('je','current_no_plan')
 # Read actual stand/factor from validated current Player's WGF object.
 r.mov('ebx',m('ebp',24));r.test('ebx','ebx');r.j('jz','current_unknown');r.mov('esi',m('ebx',16));r.test('esi','esi');r.j('jz','current_unknown');r.mov(m('edi',4),11)
 r.mov('eax',m('esi',72));r.mov(m('edi',16),'eax');r.alu('cmp','eax',-3);r.j('jl','current_unknown')
 r.mov('eax',m('esi',8));r.mov(m('edi',24),'eax');r.mov('eax',m('esi',12));r.mov(m('edi',28),'eax')
 r.test('eax',0x80000000);r.j('jnz','current_unknown');r.alu('and','eax',0x7ff00000);r.alu('cmp','eax',0x7ff00000);r.j('je','current_unknown')
 r.mov(m('ebp',-24),0);r.mov(m('ebp',-20),0x3fd00000) # exact0.25
 r.fp('fild stand','db',0,m('edi',16));r.fp('fmul quarter','dc',1,m('ebp',-24));r.op('fld1',b'\xd9\xe8');r.op('faddp',b'\xde\xc1');r.fp('fld actual R','dd',0,m('edi',24));r.op('fcompp',b'\xde\xd9');r.op('fnstsw ax',b'\xdf\xe0');r.alu('and','eax',0x4500);r.alu('cmp','eax',0x4000);r.j('jne','current_unknown')
 # D=40+10*stand as signed64. int32*10 cannot overflow64; JO checked.
 r.mov('eax',m('edi',16));r.mov('ecx',10);r.ins('imul ecx','f7',5,'ecx');r.alu('add','eax',40);r.alu('adc','edx',0);r.j('jo','current_unknown');r.mov(m('edi',32),'eax');r.mov(m('edi',36),'edx')
 # Center currentfood and real selected-record citybonus, no universal constant.
 r.push(1);r.lea('eax',m('ebp',-192));r.push('eax');r.push('ebx');r.push(m('ebp',16));r.push(m('ebp',12));r.j('call','food_reader');r.mov(m('edi',4),12);r.test('eax','eax');r.j('jz','current_unknown')
 r.mov('eax',m('ebp',-168));r.mov('edx',m('ebp',-164));r.mov(m('edi',48),'eax');r.mov(m('edi',52),'edx');r.alu('add','eax',m('ebp',-188));r.alu('adc','edx',0);r.j('jo','current_unknown');r.mov(m('edi',40),'eax');r.mov(m('edi',44),'edx');r.mov(m('edi',124),1)
 # All candidate places are read once; unsupported worker places remain UNKNOWN.
 r.mov(m('ebp',-196),0)
 r.label('current_read_loop');r.mov('eax',m('ebp',-196));r.alu('cmp','eax',m('edi',96));r.j('jge','current_top4_begin')
 entryptr(r,'eax','esi');r.push(0);r.lea('eax',m('ebp',-192));r.push('eax');r.push('ebx');r.push('esi');r.push(m('ebp',12));r.j('call','food_reader');r.test('eax','eax');r.j('jz','current_unsupported')
 r.mov('eax',m('ebp',-180));r.alu('cmp','eax',m('esi',8));r.j('jne','current_unsupported')
 foodptr(r,m('ebp',-196),'edx')
 for off in range(0,24,4):r.mov('eax',m('ebp',-192+off));r.mov(m('edx',off),'eax')
 r.j('jmp','current_read_next')
 r.label('current_unsupported');r.mov('ecx',m('ebp',-196));r.ins('bts unsupportedmask,ecx','0fab',1,m('edi',88))
 r.label('current_read_next');r.unary('inc',m('ebp',-196));r.j('jmp','current_read_loop')
 r.label('current_top4_begin');r.push('edi');r.j('call','plan_select');r.j('jmp','current_done')
 r.label('current_no_plan');r.mov(m('edi'),1);r.mov(m('edi',4),0);r.j('jmp','current_done')
 r.label('current_unknown');r.mov(m('edi'),0)
 r.label('current_done');r.mov('eax',m('edi'));r.fp('frstor','dd',4,m('ebp',-144));r.epilogue(384,20)

def chooseplan(r):
 r.label('plan_select');r=Scoped(r,'selection_');r.prologue(256);r.mov('edi',m('ebp',8))
 # Top4 distinct supported mountains, sorted currentfood descending, then xyz.
 # Once computed, any foodrole excludes itself from these4 to give optimum3.
 r.label('current_top4_begin')
 for off in (-212,-208,-204,-200):r.mov(m('ebp',off),-1)
 r.mov(m('ebp',-196),0)
 r.label('current_top4_loop');r.mov('eax',m('ebp',-196));r.alu('cmp','eax',m('edi',96));r.j('jge','current_plans_begin');foodptr(r,'eax','esi');r.alu('cmp',m('esi'),1);r.j('jne','current_top4_next');r.mov('eax',m('esi',12))
 for v in (8,20,22):r.alu('cmp','eax',v);r.j('je','current_top4_insert')
 r.j('jmp','current_top4_next');r.label('current_top4_insert')
 for slot in range(4):
  label='top4_slot_'+str(slot);off=-212+slot*4
  r.mov('edx',m('ebp',off));r.alu('cmp','edx',-1);r.j('je',label)
  foodptr(r,'edx','edx');r.mov('eax',m('esi',4));r.alu('cmp','eax',m('edx',4));r.j('jg',label);r.j('jl','top4_continue_'+str(slot))
  compare_indices(r,m('ebp',-196),m('ebp',off));r.test('eax','eax');r.j('jl',label);r.j('jmp','top4_continue_'+str(slot))
  r.label(label)
  for target in range(3,slot,-1):r.mov('eax',m('ebp',-212+(target-1)*4));r.mov(m('ebp',-212+target*4),'eax')
  r.mov('eax',m('ebp',-196));r.mov(m('ebp',off),'eax');r.j('jmp','current_top4_next');r.label('top4_continue_'+str(slot))
 r.label('current_top4_next');r.unary('inc',m('ebp',-196));r.j('jmp','current_top4_loop')
 r.label('current_plans_begin');r.mov(m('ebp',-216),0);r.mov(m('ebp',-196),0)
 r.label('current_plan_loop');r.mov('eax',m('ebp',-196));r.alu('cmp','eax',m('edi',96));r.j('jge','current_plans_end');foodptr(r,'eax','esi');r.alu('cmp',m('esi'),1);r.j('jne','current_plan_next');r.alu('cmp',m('esi',4),0);r.j('jle','current_plan_next')
 r.mov(m('ebp',-220),0)
 for slot in range(4):
  r.mov('eax',m('ebp',-212+slot*4));r.alu('cmp','eax',-1);r.j('je','current_plan_next');r.alu('cmp','eax',m('ebp',-196));r.j('je','plan_skip_'+str(slot))
  r.mov('edx',m('ebp',-220));r.shift('shl','edx',2);r.lea('ecx',m('ebp',-232));r.alu('add','edx','ecx');r.mov(m('edx'),'eax');r.unary('inc',m('ebp',-220));r.alu('cmp',m('ebp',-220),3);r.j('je','plan_triple');r.label('plan_skip_'+str(slot))
 r.j('jmp','current_plan_next');r.label('plan_triple')
 # Sort triple by xyz with three fixed compare-swaps for deterministic ties.
 for k,(a,b) in enumerate(((0,1),(1,2),(0,1))):
  compare_indices(r,m('ebp',-232+4*a),m('ebp',-232+4*b));r.test('eax','eax');r.j('jle','triple_sorted_'+str(k));r.mov('eax',m('ebp',-232+4*a));r.mov('edx',m('ebp',-232+4*b));r.mov(m('ebp',-232+4*a),'edx');r.mov(m('ebp',-232+4*b),'eax');r.label('triple_sorted_'+str(k))
 r.mov('eax',m('edi',40));r.mov('edx',m('edi',44));r.alu('add','eax',m('esi',4));r.alu('adc','edx',0);r.j('jo','current_unknown');r.mov(m('ebp',-240),'eax');r.mov(m('ebp',-236),'edx')
 for off in (-232,-228,-224):
  foodptr(r,m('ebp',off),'ecx');r.mov('eax',m('ecx',4));r.alu('add',m('ebp',-240),'eax');r.alu('adc',m('ebp',-236),0);r.j('jo','current_unknown')
 r.alu('cmp',m('ebp',-216),0);r.j('je','current_best')
 r.mov('eax',m('ebp',-236));r.alu('cmp','eax',m('edi',60));r.j('jg','current_best');r.j('jl','current_plan_next');r.mov('eax',m('ebp',-240));r.alu('cmp','eax',m('edi',56));r.j('ja','current_best');r.j('jb','current_plan_next')
 compare_indices(r,m('ebp',-196),m('edi',112));r.test('eax','eax');r.j('jl','current_best');r.j('jg','current_plan_next')
 for own,best in [(-232,100),(-228,104),(-224,108)]:
  compare_indices(r,m('ebp',own),m('edi',best));r.test('eax','eax');r.j('jl','current_best');r.j('jg','current_plan_next')
 r.j('jmp','current_plan_next');r.label('current_best');r.mov(m('ebp',-216),1)
 for own,target in [(-232,100),(-228,104),(-224,108),(-196,112),(-240,56),(-236,60)]:r.mov('eax',m('ebp',own));r.mov(m('edi',target),'eax')
 r.label('current_plan_next');r.unary('inc',m('ebp',-196));r.j('jmp','current_plan_loop')
 r.label('current_plans_end');r.alu('cmp',m('ebp',-216),0);r.j('jne','current_finish_scenario');r.alu('cmp',m('edi',88),0);r.j('je','current_no_plan');r.mov(m('edi',4),13);r.j('jmp','current_unknown')
 r.label('current_finish_scenario');r.mov('eax',m('edi',56));r.mov('edx',m('edi',60));r.mov(m('edi',80),'eax');r.mov(m('edi',84),'edx');r.alu('sub','eax',m('edi',32));r.alu('sbb','edx',m('edi',36));r.j('jo','current_unknown')
 for low,high in ((64,68),(72,76)):r.mov(m('edi',low),'eax');r.mov(m('edi',high),'edx')
 # Supported scenario may have zero/negative margin; adapter only rewards >0.
 r.mov(m('edi'),2);r.mov(m('edi',4),0);r.j('jmp','current_done')
 r.label('current_no_plan');r.mov(m('edi'),1);r.mov(m('edi',4),0);r.j('jmp','current_done')
 r.label('current_unknown');r.mov(m('edi'),0)
 r.label('current_done');r.mov('eax',m('edi'));r.epilogue(256,4)
