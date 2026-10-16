"""Standalone science predicate emitter; not wired into quota/union/gameplay.

stdcall(AiMain*,World*,external center*,HostBinding*,ScienceResult*) ret20.
Calls real, serial World+34 query. No City/World object or scratch is invented.
Own Result and stack scratch only; inherited HostBinding is verified again.
"""
from x86 import mem as m
from science_layout import *

def ptr(r,index,reg='esi'):
 r.imul(reg,index,TILE_STRIDE);r.alu('add',reg,'edi');r.alu('add',reg,TILE_OFFSET)

def bit(r,offset):
 r.mov('ecx',m('ebp',-220));r.ins('bts own mask,index','0fab',1,m('edi',offset))

def model(r,pins):
 r.label('science_model');r.prologue(SCRATCH_SIZE+160)
 # x87 preserved, including controlword. Scratch is private to this invocation;
 # World native scratch remains owned by serial original query callbacks.
 r.fp('fnsave','dd',6,m('ebp',-144));r.fp('fldcw caller','d9',5,m('ebp',-144))
 r.zero(m('ebp',24),RESULT_SIZE);r.mov('edi',m('ebp',24));r.mov(m('edi',8),1)
 r.mov(m('edi',12),ZERO_NEW_CITY_MODIFIERS|CONDITIONAL_CRIME)
 for off in (28,32,36):r.mov(m('edi',off),-1)
 r.mov(m('edi',4),10);r.mov('ebx',m('ebp',20));r.test('ebx','ebx');r.j('jz','science_bad')
 # Original host validator fills actual six words; supplied binding must match.
 r.lea('eax',m('ebp',-208));r.push('eax');r.push(m('ebp',12));r.push(m('ebp',8));r.j('call','H3Host')
 r.test('eax','eax');r.j('jz','science_bad')
 for off in range(0,24,4):
  r.mov('eax',m('ebp',-208+off));r.alu('cmp','eax',m('ebx',off));r.j('jne','science_bad')
 r.mov('esi',m('ebx'));r.mov('eax',m('ebp',12));r.mov('ecx',m('eax'))
 r.lea('edx',m('esi',0x133620));r.alu('cmp',m('ecx',0x34),'edx');r.j('jne','science_bad')
 r.mov('eax',m('ebx',4));r.lea('edx',m('esi',0x344170));r.alu('cmp',m('eax'),'edx');r.j('jne','science_bad')
 # Full required slot/bodypreimages; address-valued bytes are fingerprints,
 # never copied into new World state or executed as synthetic callbacks.
 for row in pins:
  raw=bytes.fromhex(row['bytes']);base=row['rva']
  for offset in range(0,len(raw)//4*4,4):
   r.alu('cmp',m('esi',base+offset),int.from_bytes(raw[offset:offset+4],'little'));r.j('jne','science_bad')
  for offset in range(len(raw)//4*4,len(raw)):
   r.op('cmp byte original spatial pin',b'\x80'+r.rm(7,m('esi',base+offset))+raw[offset:offset+1]);r.j('jne','science_bad')
 # H2 enum accepts both valid status1 and2. No mountain-count gate.
 r.lea('eax',m('ebp',-480));r.push('eax');r.push(m('ebp',16));r.push(m('ebp',12));r.push(m('ebp',8));r.j('call','H3Capacity')
 r.mov(m('edi',124),'eax');r.alu('cmp','eax',1);r.j('je','science_h2_ok');r.alu('cmp','eax',2);r.j('jne','science_bad')
 r.label('science_h2_ok');r.mov('eax',m('ebp',-472));r.mov(m('edi',16),'eax')
 # Exact actual R=1+stand/4, positive finite, original supported stand>=-3.
 r.mov(m('edi',4),11);r.mov('esi',m('ebx',16));r.mov('eax',m('esi',72));r.mov(m('edi',56),'eax');r.alu('cmp','eax',-3);r.j('jl','science_bad')
 for src,dst in [(8,64),(12,68)]:r.mov('eax',m('esi',src));r.mov(m('edi',dst),'eax')
 r.test('eax',0x80000000);r.j('jnz','science_bad');r.alu('and','eax',0x7ff00000);r.alu('cmp','eax',0x7ff00000);r.j('je','science_bad')
 r.mov(m('ebp',-24),0);r.mov(m('ebp',-20),0x3fd00000)
 r.fp('fild stand','db',0,m('edi',56));r.fp('fmul quarter','dc',1,m('ebp',-24));r.op('fld1',b'\xd9\xe8');r.op('faddp',b'\xde\xc1');r.fp('fld actual R','dd',0,m('edi',64));r.op('fcompp',b'\xde\xd9');r.op('fnstsw ax',b'\xdf\xe0');r.alu('and','eax',0x4500);r.alu('cmp','eax',0x4000);r.j('jne','science_bad')
 # Center getterfood+real citybonus once; center is outside worker enum.
 r.push(1);r.lea('eax',m('ebp',-184));r.push('eax');r.push('ebx');r.push(m('ebp',16));r.push(m('ebp',12));r.j('call','H3FoodReader');r.test('eax','eax');r.j('jz','science_bad')
 r.mov('eax',m('ebp',-160));r.mov('edx',m('ebp',-156));r.alu('add','eax',m('ebp',-180));r.alu('adc','edx',0);r.j('jo','science_bad');r.mov(m('edi',72),'eax');r.mov(m('edi',76),'edx')
 r.push(m('ebp',16));r.lea('ecx',m('edi',116));r.unary('call',m('ebx',20))
 r.mov(m('edi',4),12);r.mov(m('ebp',-220),0)
 r.label('science_tiles');r.mov('eax',m('ebp',-220));r.alu('cmp','eax',m('edi',16));r.j('jge','science_choose')
 ptr(r,'eax');r.imul('ecx','eax',12);r.lea('edx',m('ebp',-464));r.alu('add','edx','ecx')
 r.mov('eax',m('edx',8));r.mov(m('ebp',-512),'eax')
 for src,dst in [(0,8),(4,12)]:r.mov('eax',m('edx',src));r.mov(m('esi',dst),'eax')
 r.lea('eax',m('esi',8));r.push('eax');r.mov('ecx','esi');r.unary('call',m('ebx',20))
 # food_reader independently bounds the internal coordinates/current model.
 r.push(0);r.lea('eax',m('ebp',-184));r.push('eax');r.push('ebx');r.lea('eax',m('esi',8));r.push('eax');r.push(m('ebp',12));r.j('call','H3FoodReader');r.test('eax','eax');r.j('jz','science_current_unknown')
 r.mov('eax',m('ebp',-180));r.mov(m('esi',16),'eax')
 r.mov('eax',m('ebp',-172));r.alu('cmp','eax',m('ebp',-512));r.j('jne','science_current_unknown')
 # Canonical duplicate cannot add a third unique workplace. Compare all
 # preceding valid keys; current flag bit16 marks a trustworthy canonicalkey.
 r.mov(m('ebp',-224),0)
 r.label('science_dedup');r.mov('eax',m('ebp',-224));r.alu('cmp','eax',m('ebp',-220));r.j('jge','science_unique');ptr(r,'eax','edx');r.test(m('edx',20),16);r.j('jz','science_dedup_next')
 r.push('edx');r.push('esi');r.j('call','H3PosCompare');r.test('eax','eax');r.j('jz','science_duplicate')
 r.label('science_dedup_next');r.unary('inc',m('ebp',-224));r.j('jmp','science_dedup')
 r.label('science_unique');r.mov(m('esi',20),16);r.mov('eax',m('ebp',-172))
 for terrain in (1,4,5,10,11):r.alu('cmp','eax',terrain);r.j('je','science_terrain_ok')
 r.j('jmp','science_current_unknown')
 r.label('science_terrain_ok');r.mov('edx',m('ebx',8));r.mov('edx',m('edx',8));r.imul('eax','eax',192);r.alu('add','edx','eax');r.alu('cmp',m('edx',0x6c),0);r.j('je','science_structural_absent');r.alu('or',m('esi',20),STRUCT_MAIN_IRR2)
 r.mov('edx',m('ebp',-152));r.mov('edx',m('edx',0x6c));r.test('edx','edx');r.j('jz','science_structural_absent');r.alu('cmp',m('edx'),0);r.j('jle','science_structural_absent');r.alu('or',m('esi',20),STRUCT_EFFECTIVE_POSITIVE_IRR2);r.unary('inc',m('edi',20))
 for source,target in [(0x20,-516),(0x24,-520),(0x44,-524)]:r.mov('eax',m('edx',source));r.mov(m('ebp',target),'eax')
 r.mov('eax',m('ebp',-176));r.shift('shr','eax',2);r.alu('and','eax',3);r.alu('cmp','eax',2);r.j('jl','science_spatial');r.alu('or',m('esi',20),STRUCT_CURRENT_LEVEL_PRESENT)
 r.label('science_spatial');r.lea('eax',m('esi',8));r.push('eax');r.push(m('ebp',12));r.mov('eax',m('ebp',12));r.mov('ecx',m('eax'));r.unary('call',m('ecx',0x34));r.mov(m('esi',24),'eax');r.alu('cmp','eax',1);r.j('je','science_certified');r.test('eax','eax');r.j('jz','science_spatial_pending')
 # Invalid return from a pinned shared host query invalidates whole context.
 bit(r,44);r.mov(m('esi',28),5);r.mov(m('edi',4),13);r.j('jmp','science_bad')
 r.label('science_certified');r.alu('or',m('esi',20),STRUCT_CERTIFIABLE);r.unary('inc',m('edi',24));r.j('jmp','science_development')
 r.label('science_spatial_pending');bit(r,48);r.mov(m('esi',28),1)
 r.label('science_development');r.push(2);r.push(1);r.lea('eax',m('esi',32));r.push('eax');r.push('ebx');r.lea('eax',m('esi',8));r.push('eax');r.push(m('ebp',12));r.push(m('ebp',8));r.j('call','H3DevelopmentTile')
 # Keep loaded target metadata even for PRESENT where shared routine returns
 # before querying a replacement improvement. Never apply any extra delta.
 for source,target in [(-516,60),(-520,64),(-524,68)]:r.mov('ecx',m('ebp',source));r.mov(m('esi',target),'ecx')
 r.test('eax','eax');r.j('jnz','science_next');bit(r,52);r.j('jmp','science_next')
 r.label('science_current_unknown');bit(r,40);r.mov(m('esi',28),2);r.j('jmp','science_next')
 r.label('science_duplicate');r.mov(m('esi',28),3);r.j('jmp','science_next')
 r.label('science_structural_absent');r.mov(m('esi',28),4)
 r.label('science_next');r.unary('inc',m('ebp',-220));r.j('jmp','science_tiles')
 r.label('science_choose');r.mov(m('edi',112),1);r.mov(m('edi',4),0);r.mov(m('edi'),1)
 r.alu('cmp',m('edi',24),3);r.j('jl','science_insufficient')
 # Deterministic top3 currentfood descending, then canonicalxyz ascending.
 r.mov(m('ebp',-220),0)
 r.label('science_sort_loop');r.mov('eax',m('ebp',-220));r.alu('cmp','eax',m('edi',16));r.j('jge','science_scenarios');ptr(r,'eax');r.test(m('esi',20),STRUCT_CERTIFIABLE);r.j('jz','science_sort_next')
 for index in range(3):
  off=28+4*index;label='science_insert_'+str(index);skip='science_insert_skip_'+str(index)
  r.mov('eax',m('edi',off));r.alu('cmp','eax',-1);r.j('je',label);ptr(r,'eax','edx');r.mov('eax',m('esi',16));r.alu('cmp','eax',m('edx',16));r.j('jg',label);r.j('jl',skip)
  r.push('edx');r.push('esi');r.j('call','H3PosCompare');r.test('eax','eax');r.j('jge',skip)
  r.label(label)
  for target in range(2,index,-1):r.mov('eax',m('edi',28+4*(target-1)));r.mov(m('edi',28+4*target),'eax')
  r.mov('eax',m('ebp',-220));r.mov(m('edi',off),'eax');r.j('jmp','science_sort_next');r.label(skip)
 r.label('science_sort_next');r.unary('inc',m('ebp',-220));r.j('jmp','science_sort_loop')
 r.label('science_scenarios');r.mov('eax',m('edi',72));r.mov('edx',m('edi',76));r.mov(m('ebp',-240),'eax');r.mov(m('ebp',-236),'edx')
 for n in range(1,4):
  ptr(r,m('edi',28+4*(n-1)),'ecx');r.mov('eax',m('ecx',16));r.alu('add',m('ebp',-240),'eax');r.alu('adc',m('ebp',-236),0);r.j('jo','science_bad')
  r.mov('eax',m('ebp',-240));r.mov('edx',m('ebp',-236));r.alu('add','eax','eax');r.alu('adc','edx','edx');r.j('jo','science_bad');r.mov(m('ebp',-248),'eax');r.mov(m('ebp',-244),'edx')
  # 2D_n=20n+5n*stand in signed64, never floor half-integer hunger.
  r.mov('eax',m('edi',56));r.mov('ecx',5*n);r.ins('imul signed64 demand','f7',5,'ecx');r.alu('add','eax',20*n);r.alu('adc','edx',0);r.j('jo','science_bad')
  r.mov('ecx',m('ebp',-248));r.mov('esi',m('ebp',-244));r.alu('sub','ecx','eax');r.alu('sbb','esi','edx');r.j('jo','science_bad');r.test('esi','esi');r.j('js','science_no_growth');r.j('jnz','science_positive_'+str(n));r.test('ecx','ecx');r.j('jz','science_no_growth');r.label('science_positive_'+str(n))
  if n==3:
   for src,dst in [(-240,80),(-236,84),(-248,104),(-244,108)]:r.mov('eax',m('ebp',src));r.mov(m('edi',dst),'eax')
   r.mov(m('edi',88),'ecx');r.mov(m('edi',92),'esi')
  # Food sorted nonincreasing, nonnegative center: S_n/n nonincreasing,
  # hence cmax3 is the minimum. Each earlier strict margin still checked.
 r.mov('eax',m('edi',88));r.mov(m('edi',96),'eax');r.mov('eax',m('edi',92));r.mov(m('edi',100),'eax');r.mov(m('edi'),STATUS_NOW)
 # Conservative summary separate from location: pending unless each selected
 # DEV_TILE is READY_NOT_BUILT or ALREADY_PRESENT; UNKNOWN kept independent.
 r.mov(m('edi',60),3)
 for index in range(3):
  ptr(r,m('edi',28+4*index),'esi');r.mov('eax',m('esi',32));r.test('eax','eax');r.j('jz','science_dev_unknown_'+str(index));r.alu('cmp','eax',3);r.j('jge','science_dev_continue_'+str(index));r.alu('cmp',m('edi',60),0);r.j('je','science_dev_continue_'+str(index));r.mov(m('edi',60),1);r.j('jmp','science_dev_continue_'+str(index))
  r.label('science_dev_unknown_'+str(index));r.mov(m('edi',60),0);r.label('science_dev_continue_'+str(index))
 r.j('jmp','science_done')
 # This C1 checkpoint does not claim future-positive growth before that
 # separately ranked pending calculation is implemented/reviewed.
 r.label('science_no_growth');r.mov(m('edi'),STATUS_NO_NOW);r.mov(m('edi',4),14);r.j('jmp','science_done')
 r.label('science_insufficient');r.alu('cmp',m('edi',40),0);r.j('jne','science_local_unknown');r.alu('cmp',m('edi',20),3);r.j('jl','science_done');r.mov(m('edi'),STATUS_STRUCTURAL_POTENTIAL);r.j('jmp','science_done')
 r.label('science_local_unknown');r.mov(m('edi'),STATUS_UNKNOWN);r.mov(m('edi',4),15);r.j('jmp','science_done')
 r.label('science_bad');r.mov(m('edi'),STATUS_UNKNOWN);r.mov(m('edi',24),0)
 r.label('science_done');r.mov('eax',m('edi'));r.fp('frstor','dd',4,m('ebp',-144));r.epilogue(SCRATCH_SIZE+160,20)
