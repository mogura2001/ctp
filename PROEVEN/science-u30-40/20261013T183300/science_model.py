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

def top3(r,kind,selected_base,selected_offset,food_offset,required):
 # Emit two separate deterministic ranks; future never replaces current keys.
 for i in range(3):r.mov(m(selected_base,selected_offset+4*i),-1)
 r.mov(m('ebp',-220),0)
 r.label(kind+'_sort_loop');r.mov('eax',m('ebp',-220));r.alu('cmp','eax',m('edi',16));r.j('jge',kind+'_sort_done');ptr(r,'eax');r.mov('eax',m('esi',20));r.alu('and','eax',required);r.alu('cmp','eax',required);r.j('jne',kind+'_sort_next')
 for index in range(3):
  off=selected_offset+4*index;label=kind+'_insert_'+str(index);skip=kind+'_insert_skip_'+str(index)
  r.mov('eax',m(selected_base,off));r.alu('cmp','eax',-1);r.j('je',label);ptr(r,'eax','edx');r.mov('eax',m('esi',food_offset));r.alu('cmp','eax',m('edx',food_offset));r.j('jg',label);r.j('jl',skip)
  r.push('edx');r.push('esi');r.j('call','H3PosCompare');r.test('eax','eax');r.j('jge',skip);r.label(label)
  for target in range(2,index,-1):r.mov('eax',m(selected_base,selected_offset+4*(target-1)));r.mov(m(selected_base,selected_offset+4*target),'eax')
  r.mov('eax',m('ebp',-220));r.mov(m(selected_base,off),'eax');r.j('jmp',kind+'_sort_next');r.label(skip)
 r.label(kind+'_sort_next');r.unary('inc',m('ebp',-220));r.j('jmp',kind+'_sort_loop');r.label(kind+'_sort_done')

def scenarios(r,kind,selected_base,selected_offset,food_offset,publish_current):
 # All n1/2/3 are calculated even if an earlier margin fails. S3/margin3 stay
 # true current diagnostics. Future scenario is stack-only, never current out.
 r.mov(m('ebp',-540),1);r.mov('eax',m('edi',72));r.mov('edx',m('edi',76));r.mov(m('ebp',-240),'eax');r.mov(m('ebp',-236),'edx')
 for n in range(1,4):
  ptr(r,m(selected_base,selected_offset+4*(n-1)),'ecx');r.mov('eax',m('ecx',food_offset));r.alu('add',m('ebp',-240),'eax');r.alu('adc',m('ebp',-236),0);r.j('jo','science_bad')
  r.mov('eax',m('ebp',-240));r.mov('edx',m('ebp',-236));r.alu('add','eax','eax');r.alu('adc','edx','edx');r.j('jo','science_bad');r.mov(m('ebp',-248),'eax');r.mov(m('ebp',-244),'edx')
  r.mov('eax',m('edi',56));r.mov('ecx',5*n);r.ins('imul signed64 halfconsumption','f7',5,'ecx');r.alu('add','eax',20*n);r.alu('adc','edx',0);r.j('jo','science_bad')
  r.mov('ecx',m('ebp',-248));r.mov('esi',m('ebp',-244));r.alu('sub','ecx','eax');r.alu('sbb','esi','edx');r.j('jo','science_bad');r.test('esi','esi');r.j('js',kind+'_nonpositive_'+str(n));r.j('jnz',kind+'_positive_'+str(n));r.test('ecx','ecx');r.j('jnz',kind+'_positive_'+str(n))
  r.label(kind+'_nonpositive_'+str(n));r.mov(m('ebp',-540),0);r.label(kind+'_positive_'+str(n))
  if n==3 and publish_current:
   for src,dst in [(-240,80),(-236,84),(-248,104),(-244,108)]:r.mov('eax',m('ebp',src));r.mov(m('edi',dst),'eax')
   for dst in (88,96):r.mov(m('edi',dst),'ecx');r.mov(m('edi',dst+4),'esi')
 # Nonnegative center and sorted nonnegative food imply min(cmax1..3)=cmax3.

def development_summary(r):
 # UNKNOWN dominates PENDING, which dominates known READY/PRESENT. A mix of
 # READY/PRESENT is explicit; all PRESENT never reports a building readiness.
 r.mov(m('ebp',-544),0)
 for index in range(3):
  ptr(r,m('edi',28+4*index),'esi');r.mov('eax',m('esi',32));r.test('eax','eax');r.j('jz','science_summary_unknown');r.alu('cmp','eax',4);r.j('jg','science_summary_unknown')
  r.alu('cmp','eax',4);r.j('je','science_summary_present_'+str(index));r.alu('cmp','eax',3);r.j('je','science_summary_ready_'+str(index));r.alu('or',m('ebp',-544),4);r.j('jmp','science_summary_next_'+str(index))
  r.label('science_summary_present_'+str(index));r.alu('or',m('ebp',-544),2);r.j('jmp','science_summary_next_'+str(index));r.label('science_summary_ready_'+str(index));r.alu('or',m('ebp',-544),1);r.label('science_summary_next_'+str(index))
 r.test(m('ebp',-544),4);r.j('jnz','science_summary_pending');r.mov('eax',m('ebp',-544));r.alu('cmp','eax',2);r.j('je','science_summary_all_present');r.alu('cmp','eax',1);r.j('je','science_summary_all_ready');r.mov(m('edi',60),DEV_SUMMARY_MIXED_PRESENT_READY);r.j('jmp','science_summary_done')
 for label,state in [('unknown',DEV_SUMMARY_UNKNOWN),('pending',DEV_SUMMARY_PENDING),('all_present',DEV_SUMMARY_ALREADY_PRESENT),('all_ready',DEV_SUMMARY_READY_NOT_BUILT)]:
  r.label('science_summary_'+label);r.mov(m('edi',60),state);r.j('jmp','science_summary_done')
 r.label('science_summary_done')

def model(r,pins):
 r.label('science_model');r.prologue(KERNEL_FRAME_SIZE)
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
 r.mov('esi',m('ebx'));r.mov('eax',m('ebp',12));r.mov('ecx',m('eax'));r.lea('edx',m('esi',0x3452e0));r.alu('cmp','ecx','edx');r.j('jne','science_bad')
 r.lea('edx',m('esi',0x133620));r.alu('cmp',m('ecx',0x34),'edx');r.j('jne','science_bad')
 r.mov('eax',m('ebx',4));r.lea('edx',m('esi',0x344170));r.alu('cmp',m('eax'),'edx');r.j('jne','science_bad')
 # Shared context failures must not masquerade as locally unsupported food.
 r.mov('edx',m('eax',0x1c));r.test('edx','edx');r.j('jz','science_bad');r.mov('edx',m('edx'));r.test('edx','edx');r.j('jz','science_bad')
 for off in (0x67df20,0x67df22):r.load('eax',m('esi',off),'zx16');r.test('eax','eax');r.j('jz','science_bad')
 r.mov('eax',m('ebx',8));r.alu('cmp',m('eax'),0);r.j('jle','science_bad');r.mov('eax',m('eax',8));r.test('eax','eax');r.j('jz','science_bad')
 r.mov('eax',m('ebp',8));r.mov('eax',m('eax',0x50));r.test('eax','eax');r.j('jz','science_bad');r.mov('ecx',m('eax'));r.lea('edx',m('esi',0x3445b8));r.alu('cmp','ecx','edx');r.j('jne','science_bad')
 for slot,target in ((0x10,0x126a40),(0x20,0x126ad0),(0x48,0x126d50)):
  r.lea('edx',m('esi',target));r.alu('cmp',m('ecx',slot),'edx');r.j('jne','science_bad')
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
 r.label('science_h2_ok');r.mov('eax',m('ebp',-472));r.alu('cmp','eax',MAX_TILES);r.j('ja','science_bad');r.mov(m('edi',16),'eax')
 # Exact actual R=1+stand/4, positive finite, original supported stand>=-3.
 r.mov(m('edi',4),11)
 # Preserve all normal precision modes. PC24 is exact for -3..2^24-4:
 # stand and stand+4 each fit24 significant bits, quarter is power-of-two.
 # PC53/64 represent every int32 stand and stand+4 exactly. Reserved PC01 or
 # unmasked exceptions are unsupported, not permission to alter caller CW.
 r.load('eax',m('ebp',-144),'zx16');r.mov('ecx','eax');r.alu('and','ecx',0x3f);r.alu('cmp','ecx',0x3f);r.j('jne','science_bad');r.alu('and','eax',0x300);r.alu('cmp','eax',0x100);r.j('je','science_bad')
 r.mov('esi',m('ebx',16));r.mov('eax',m('esi',72));r.mov(m('edi',56),'eax');r.alu('cmp','eax',-3);r.j('jl','science_bad')
 r.load('ecx',m('ebp',-144),'zx16');r.alu('and','ecx',0x300);r.test('ecx','ecx');r.j('jnz','science_cw_ok');r.alu('cmp','eax',2**24-4);r.j('jg','science_bad');r.label('science_cw_ok')
 for src,dst in [(8,64),(12,68)]:r.mov('eax',m('esi',src));r.mov(m('edi',dst),'eax')
 r.test('eax',0x80000000);r.j('jnz','science_bad');r.alu('and','eax',0x7ff00000);r.alu('cmp','eax',0x7ff00000);r.j('je','science_bad')
 r.mov(m('ebp',-24),0);r.mov(m('ebp',-20),0x3fd00000)
 r.fp('fild stand','db',0,m('edi',56));r.fp('fmul quarter','dc',1,m('ebp',-24));r.op('fld1',b'\xd9\xe8');r.op('faddp',b'\xde\xc1');r.fp('fld actual R','dd',0,m('edi',64));r.op('fcompp',b'\xde\xd9');r.op('fnstsw ax',b'\xdf\xe0');r.alu('and','eax',0x4500);r.alu('cmp','eax',0x4000);r.j('jne','science_bad')
 # Center getterfood+real citybonus once; center is outside worker enum.
 r.push(1);r.lea('eax',m('ebp',-184));r.push('eax');r.push('ebx');r.push(m('ebp',16));r.push(m('ebp',12));r.j('call','H3FoodReader');r.test('eax','eax');r.j('jz','science_bad')
 r.mov('eax',m('ebp',-160));r.mov('edx',m('ebp',-156));r.alu('add','eax',m('ebp',-180));r.alu('adc','edx',0);r.j('jo','science_bad')
 # Explicit nonnegative center makes the cmax3 minimum proof valid, even if
 # loaded CITY_BONUS itself is negative. H3FoodReader also checks this sum.
 r.test('edx','edx');r.j('js','science_bad');r.mov(m('edi',72),'eax');r.mov(m('edi',76),'edx')
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
 r.lea('edx',m('edi',116));r.push('edx');r.push('esi');r.j('call','H3PosCompare');r.test('eax','eax');r.j('jz','science_duplicate')
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
 # Only trusted status/conditions authorize using future_food. UNKNOWN can
 # contain an intermediate NaN/fractional/overflow delta and is never used.
 r.test('eax','eax');r.j('jz','science_dev_invalid');r.alu('cmp','eax',4);r.j('jg','science_dev_invalid')
 r.alu('cmp',m('esi',36),0);r.j('jne','science_dev_invalid');r.mov('ecx',m('esi',88));r.alu('cmp','ecx',m('ebp',-512));r.j('jne','science_dev_invalid')
 r.alu('cmp',m('esi',68),-1);r.j('jl','science_dev_invalid');r.alu('cmp','eax',4);r.j('je','science_dev_present')
 r.test(m('esi',92),8);r.j('jz','science_dev_invalid');r.alu('cmp',m('esi',56),0);r.j('jne','science_dev_invalid')
 r.mov('ecx',m('esi',80));r.alu('sub','ecx',m('esi',84));r.j('jo','science_dev_invalid');r.alu('cmp','ecx',m('esi',16));r.j('jne','science_dev_invalid');r.j('jmp','science_dev_future_ok')
 r.label('science_dev_present');r.alu('cmp',m('esi',56),1);r.j('jne','science_dev_invalid');r.test(m('esi',92),4);r.j('jz','science_dev_invalid');r.test(m('esi',20),STRUCT_CURRENT_LEVEL_PRESENT);r.j('jz','science_dev_invalid')
 r.mov('ecx',m('esi',80));r.alu('cmp','ecx',m('esi',16));r.j('jne','science_dev_invalid');r.alu('cmp',m('esi',84),0);r.j('jne','science_dev_invalid')
 r.label('science_dev_future_ok');r.alu('cmp',m('esi',80),0);r.j('jl','science_dev_invalid');r.alu('or',m('esi',20),STRUCT_FUTURE_VALID);r.j('jmp','science_next')
 r.label('science_dev_invalid');r.mov(m('esi',32),0);r.mov(m('esi',36),22);bit(r,52);r.j('jmp','science_next')
 r.label('science_current_unknown');bit(r,40);r.mov(m('esi',28),2);r.j('jmp','science_next')
 r.label('science_duplicate');r.mov(m('esi',28),3);r.j('jmp','science_next')
 r.label('science_structural_absent');r.mov(m('esi',28),4)
 r.label('science_next');r.unary('inc',m('ebp',-220));r.j('jmp','science_tiles')
 r.label('science_choose');r.mov(m('edi',112),1);r.mov(m('edi',4),0);r.mov(m('edi'),STATUS_NO_NOW)
 top3(r,'science_current','edi',28,16,STRUCT_CERTIFIABLE)
 r.alu('cmp',m('edi',36),-1);r.j('je','science_insufficient')
 development_summary(r)
 scenarios(r,'science_current','edi',28,16,True)
 r.alu('cmp',m('ebp',-540),0);r.j('je','science_no_growth');r.mov(m('edi'),STATUS_NOW);r.j('jmp','science_done')
 r.label('science_no_growth');r.mov(m('edi',4),14);r.j('jmp','science_future')
 r.label('science_insufficient');r.alu('cmp',m('edi',40),0);r.j('jne','science_local_unknown');r.alu('cmp',m('edi',20),3);r.j('jl','science_done');r.mov(m('edi'),STATUS_STRUCTURAL_POTENTIAL);r.j('jmp','science_done')
 r.label('science_local_unknown');r.mov(m('edi'),STATUS_UNKNOWN);r.mov(m('edi',4),15);r.j('jmp','science_done')
 # Only trustworthy structural tiles and genuine validated development data.
 # Only the current FOOD-MARGIN failure reaches here. Spacefalse keeps its
 # original STRUCTURAL/SPATIAL_PENDING state; futurefood cannot bypass that.
 r.label('science_future');top3(r,'science_future','ebp',-560,80,STRUCT_CANONICAL_CURRENT_VALID|STRUCT_MAIN_IRR2|STRUCT_EFFECTIVE_POSITIVE_IRR2|STRUCT_CERTIFIABLE|STRUCT_FUTURE_VALID)
 r.alu('cmp',m('ebp',-552),-1);r.j('je','science_done')
 scenarios(r,'science_future','ebp',-560,80,False)
 r.alu('cmp',m('ebp',-540),0);r.j('je','science_done');r.mov(m('edi'),STATUS_PENDING_GROWTH);r.mov(m('edi',4),16);r.j('jmp','science_done')
 r.label('science_bad');r.mov(m('edi'),STATUS_UNKNOWN);r.mov(m('edi',24),0);r.mov(m('edi',112),0)
 r.label('science_done');r.mov('eax',m('edi'));r.fp('frstor','dd',4,m('ebp',-144));r.epilogue(KERNEL_FRAME_SIZE,20)
