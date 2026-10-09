"""Separate native explanation only. Never called by SCORE_CURRENT adapter.

All returned delta scenarios remain conditional, queried not built. No IRR1.
The engine's integer environment-food delta is accepted only after exact double
roundtrip; no roundingmode changes or fractional truncation silently occur.
"""
from x86 import mem as m
from model import entryptr,foodptr
DEV_SIZE=2048
DEV_ENTRIES=128
DEV_STRIDE=64
DEV_MINES=1440
DEV_HEADER={'status':0,'reason':4,'model_id':8,'mode':12,'current_status':16,
 'pending_mountain1':32,'pending_mountain2':36,'pending_mountain3':40,'pending_food':44,
 'pending_S_i64':48,'pending_margin_i64':56,'pending_crime_numerator_i64':64,
 'pending_crime_denominator_i64':72,'mine_S_i64':80,'mine_margin_i64':88,
 'mine_crime_numerator_i64':96,'mine_crime_denominator_i64':104,
 'unsupported_mask':112,'pending_conditions':116,'mine_conditions':120}
DEV_TILE={'status':0,'reason':4,'selector':8,'availability_raw':12,'position_predicate_raw':16,
 'position_state_raw':20,'already_present':24,'target_materials':28,'target_time':32,
 'required_advance_id':36,'food_delta_double':40,'future_food_i32':48,'delta_i32':52,
 'terrain':56,'conditions':60}
# statuses0UNKNOWN;1AVAILABILITY_PENDING;2PLACE_UNKNOWN;3READY_NOT_BUILT;
#4ALREADY_PRESENT. conditions bits:1availabilityfalse,2predicatefalse,4already,
#8queried-not-built. No tech-only diagnosis or completion claims.

def tile(r):
 r.label('development_tile');r.prologue(192);r.fp('fnsave','dd',6,m('ebp',-128));r.fp('fldcw caller','d9',5,m('ebp',-128));r.zero(m('ebp',24),64);r.mov('edi',m('ebp',24));r.mov('eax',m('ebp',28));r.mov(m('edi',8),'eax');r.mov(m('edi',4),20)
 r.push(0);r.lea('eax',m('ebp',-172));r.push('eax');r.push(m('ebp',20));r.push(m('ebp',16));r.push(m('ebp',12));r.j('call','food_reader');r.test('eax','eax');r.j('jz','development_tile_done')
 r.mov('esi',m('ebp',-140));r.mov('eax',m('ebp',-160));r.mov(m('edi',56),'eax');r.mov('edx',m('ebp',-168));r.mov(m('edi',48),'edx')
 r.alu('cmp',m('ebp',28),1);r.j('jne','development_mine_target')
 # IRR2 only on already-bound1/4/5 and10/11 environments; other terrains
 # remain explicitly unknown pending, never inventing an enabling advance.
 for terrain in (1,4,5,10,11):r.alu('cmp','eax',terrain);r.j('je','development_irr2_target')
 r.mov(m('edi',4),21);r.j('jmp','development_tile_done')
 r.label('development_irr2_target');r.mov('eax',m('ebp',-164));r.shift('shr','eax',2);r.alu('and','eax',3);r.alu('cmp','eax',2);r.j('jge','development_already');r.mov('esi',m('esi',0x6c));r.j('jmp','development_target')
 r.label('development_mine_target');r.mov('eax',m('ebp',-152));r.alu('cmp','eax',3);r.j('jge','development_already');r.alu('cmp','eax',m('ebp',32));r.j('jge','development_already');r.mov('eax',m('ebp',32));r.unary('dec','eax');r.shift('shl','eax',2);r.alu('add','esi','eax');r.mov('esi',m('esi',0x74))
 r.label('development_target');r.test('esi','esi');r.j('jz','development_tile_done');r.mov('eax',m('esi',0x20));r.mov(m('edi',28),'eax');r.mov('eax',m('esi',0x24));r.mov(m('edi',32),'eax');r.mov('eax',m('esi',0x44));r.mov(m('edi',36),'eax');r.alu('cmp','eax',-1);r.j('jl','development_tile_done')
 r.mov('eax',m('ebp',8));r.mov('ebx',m('eax',0x50));r.test('ebx','ebx');r.j('jz','development_tile_done');r.mov('ecx',m('ebx'));r.test('ecx','ecx');r.j('jz','development_tile_done')
 r.push(m('ebp',28));r.push('ebx');r.unary('call',m('ecx',0x10));r.mov(m('edi',12),'eax')
 r.lea('eax',m('edi',20));r.push('eax');r.push(m('ebp',16));r.push(0);r.push(m('ebp',28));r.push('ebx');r.mov('ecx',m('ebx'));r.unary('call',m('ecx',0x20));r.mov(m('edi',16),'eax')
 r.push(m('ebp',16));r.push(m('ebp',28));r.push('ebx');r.mov('ecx',m('ebx'));r.unary('call',m('ecx',0x48));r.fp('fstp actual delta','dd',3,m('edi',40))
 # Reject nonfinite delta before integer roundtrip, and validate integerexact.
 r.mov('eax',m('edi',44));r.alu('and','eax',0x7ff00000);r.alu('cmp','eax',0x7ff00000);r.j('je','development_tile_done')
 r.fp('fld delta','dd',0,m('edi',40));r.fp('fistp exact-candidate','db',3,m('edi',52));r.fp('fild integer','db',0,m('edi',52));r.fp('fld delta','dd',0,m('edi',40));r.op('fcompp',b'\xde\xd9');r.op('fnstsw ax',b'\xdf\xe0');r.alu('and','eax',0x4500);r.alu('cmp','eax',0x4000);r.j('jne','development_tile_done')
 r.mov('eax',m('edi',48));r.alu('add','eax',m('edi',52));r.j('jo','development_tile_done');r.test('eax','eax');r.j('js','development_tile_done');r.mov(m('edi',48),'eax')
 r.mov(m('edi',4),0);r.mov(m('edi',60),8);r.mov(m('edi'),3);r.alu('cmp',m('edi',16),0);r.j('jne','development_available');r.mov(m('edi'),2);r.alu('or',m('edi',60),2)
 r.label('development_available');r.alu('cmp',m('edi',12),0);r.j('jne','development_tile_done');r.mov(m('edi'),1);r.alu('or',m('edi',60),1);r.j('jmp','development_tile_done')
 r.label('development_already');r.mov(m('edi'),4);r.mov(m('edi',4),0);r.mov(m('edi',24),1);r.mov(m('edi',60),4)
 r.label('development_tile_done');r.mov('eax',m('edi'));r.fp('frstor','dd',4,m('ebp',-128));r.epilogue(192,28)

def development(r):
 # Explicit internal fixtureable binding entry. Production public entry below
 # obtains its HostBinding from the same strict validator as classifier.
 r.label('development_model');r.prologue(1216);r.zero(m('ebp',24),DEV_SIZE);r.mov('ebx',m('ebp',24));r.mov(m('ebx',8),1);r.mov(m('ebx',12),1);r.mov(m('ebx',4),30)
 r.push(m('ebp',28));r.push(m('ebp',20));r.push(m('ebp',16));r.push(m('ebp',12));r.push(m('ebp',8));r.j('call','current_model');r.mov(m('ebx',16),'eax');r.mov('esi',m('ebp',20))
 r.alu('cmp',m('esi',92),2);r.j('jne','development_done');r.alu('cmp',m('esi',124),1);r.j('jne','development_done');r.alu('cmp','eax',0);r.j('jne','development_context_ok');r.alu('cmp',m('esi',4),13);r.j('jne','development_done')
 r.label('development_context_ok')
 # Own copy used solely for pending selection; original currentout is immutable.
 r.lea('edi',m('ebp',-1040));r.mov('ecx',256);r.op('cld',b'\xfc');r.op('rep movsd',b'\xf3\xa5');r.mov('edi',m('ebp',20));r.mov(m('ebp',-1044),0)
 r.label('development_loop');r.mov('eax',m('ebp',-1044));r.alu('cmp','eax',m('edi',96));r.j('jge','development_select');foodptr(r,'eax','ecx');r.alu('cmp',m('ecx'),1);r.j('jne','development_entry_unknown')
 r.imul('esi','eax',DEV_STRIDE);r.alu('add','esi','ebx');r.alu('add','esi',DEV_ENTRIES);r.push(2);r.push(1);r.push('esi');r.push(m('ebp',28));entryptr(r,m('ebp',-1044),'eax');r.push('eax');r.push(m('ebp',12));r.push(m('ebp',8));r.j('call','development_tile');r.test('eax','eax');r.j('jz','development_entry_unknown')
 # current mountains do not need IRR2 to be three valid present workers. Unknown
 # development leaves their current food untouched; unknown foodslots likewise
 # retain actual currentfood but the unknownmask is published separately.
 r.lea('edx',m('ebp',-1040));r.mov(m('ebp',-1048),'edi');r.mov('edi','edx');foodptr(r,m('ebp',-1044),'edx');r.mov('eax',m('esi',48));r.mov(m('edx',4),'eax');r.mov('edi',m('ebp',-1048));r.j('jmp','development_next')
 r.label('development_entry_unknown');r.mov('ecx',m('ebp',-1044));r.ins('bts unknown developmententry','0fab',1,m('ebx',112))
 r.label('development_next');r.unary('inc',m('ebp',-1044));r.j('jmp','development_loop')
 r.label('development_select');r.lea('eax',m('ebp',-1040));r.push('eax');r.j('call','plan_select');r.alu('cmp','eax',2);r.j('jne','development_done')
 r.mov(m('ebx'),2);r.mov(m('ebx',4),0)
 for source,target in [(100,32),(104,36),(108,40),(112,44),(56,48),(60,52),(64,56),(68,60),(72,64),(76,68),(80,72),(84,76)]:r.mov('eax',m('ebp',-1040+source));r.mov(m('ebx',target),'eax')
 r.mov('eax',m('ebx',44));r.imul('eax','eax',64);r.alu('add','eax','ebx');r.mov('eax',m('eax',128+60));r.mov(m('ebx',116),'eax')
 # Mines refer to this pending plan's three current mountains. Each next level
 # is queried independently; no identical existing mine's delta is applied.
 for i in range(3):
  r.mov('eax',m('ebx',32+i*4));r.mov(m('ebp',-1052),'eax');foodptr(r,'eax','ecx');r.mov('eax',m('ecx',20));r.unary('inc','eax');r.alu('cmp','eax',3);r.j('jle','mine_target_'+str(i));r.mov('eax',3);r.label('mine_target_'+str(i));r.mov(m('ebp',-1056),'eax');r.push('eax');r.alu('add','eax',5);r.push('eax');r.lea('esi',m('ebx',DEV_MINES+i*64));r.push('esi');r.push(m('ebp',28));entryptr(r,m('ebp',-1052),'eax');r.push('eax');r.push(m('ebp',12));r.push(m('ebp',8));r.j('call','development_tile')
 r.mov('eax',m('ebx',48));r.mov('edx',m('ebx',52));r.mov(m('ebx',80),'eax');r.mov(m('ebx',84),'edx')
 for i in range(3):
  r.lea('esi',m('ebx',DEV_MINES+i*64));r.alu('cmp',m('esi'),0);r.j('je','development_mine_unknown');r.mov('eax',m('esi',60));r.alu('or',m('ebx',120),'eax');r.mov('eax',m('esi',52));r.op('cdq',b'\x99');r.alu('add',m('ebx',80),'eax');r.alu('adc',m('ebx',84),'edx');r.j('jo','development_mine_unknown')
 r.mov('eax',m('ebx',80));r.mov('edx',m('ebx',84));r.mov(m('ebx',104),'eax');r.mov(m('ebx',108),'edx');r.alu('sub','eax',m('edi',32));r.alu('sbb','edx',m('edi',36));r.j('jo','development_mine_unknown')
 for low,high in ((88,92),(96,100)):r.mov(m('ebx',low),'eax');r.mov(m('ebx',high),'edx')
 r.j('jmp','development_done');r.label('development_mine_unknown');r.alu('or',m('ebx',120),0x80000000)
 for off in range(80,112,4):r.mov(m('ebx',off),0)
 r.label('development_done');r.mov('eax',m('ebx'));r.epilogue(1216,24)

def public_development(r):
 r.label('explain_development');r.prologue(32);r.zero(m('ebp',24),DEV_SIZE);r.mov('edi',m('ebp',24));r.mov(m('edi',8),1);r.mov(m('edi',12),1);r.mov(m('edi',4),14)
 r.lea('eax',m('ebp',-40));r.push('eax');r.push(m('ebp',12));r.push(m('ebp',8));r.j('call','host_validator');r.test('eax','eax');r.j('jz','explain_done')
 r.lea('eax',m('ebp',-40));r.push('eax');r.push(m('ebp',24));r.push(m('ebp',20));r.push(m('ebp',16));r.push(m('ebp',12));r.push(m('ebp',8));r.j('call','development_model')
 r.label('explain_done');r.mov('eax',m('edi'));r.epilogue(32,20)
