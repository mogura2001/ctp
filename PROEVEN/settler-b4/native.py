"""B4 owned native producer emission. Never opens a game or calls an engine.

Reuse the finite H3 X86 emitter. Functions receive a pass-owned Plan*, with
bounded owned buffers, and call only the frozen original native interfaces.
Those calls are executable only in a future accepted host or explicit owned
stub fixtures. No runtime engine export is called by this Python module.
"""
from x86 import X86, mem as m
import struct

# Own, nonserialized layout. Each array has separate storage and a fixed cap.
P = dict(status=0,reason=4,owner=8,civ=12,map=16,planner=20,aip=24,
         scheduler=28,generation=32,scope=36,guard=40,t=44,types=48,
         cities=52,remaining=56,desired=60,written=64,candidates=68,
         classes=72,departures=76,slots=80,path_queries=84,position_queries=88,
         nodes=92,hints=96,host=100,udb=104,player=108,world=112,path=116,
         d8=120,completion=124,h3calls=128,safetycalls=132)
CAPTURE=0x200; CAPTURE_CAP=4096
PREVIEW=0x8200; PREVIEW_CAP=4096; PREVIEW_STRIDE=16
DEPARTURES=0x18200; DEPARTURE_CAP=32; DEPARTURE_STRIDE=32
VISITED=0x18600; NODE_CAP=4096; NODE_STRIDE=12
STACK=0x24600; STACK_CAP=4096
HINTS=0x28600; HINT_CAP=4096; HINT_STRIDE=24
SLOTS=0x40600; SLOT_CAP=64; SLOT_STRIDE=1152
SELECTED=0x52600; SELECTED_CAP=30
ORDER=SELECTED+128
PATHCACHE=0x52800; PATHCACHE_CAP=128; PATHCACHE_STRIDE=24
PLAN_SIZE=0x54800
assert CAPTURE+CAPTURE_CAP*8==PREVIEW
assert PREVIEW+PREVIEW_CAP*PREVIEW_STRIDE==DEPARTURES
assert DEPARTURES+DEPARTURE_CAP*DEPARTURE_STRIDE==VISITED
assert VISITED+NODE_CAP*NODE_STRIDE==STACK
assert STACK+STACK_CAP*4==HINTS
assert HINTS+HINT_CAP*HINT_STRIDE==SLOTS
assert SLOTS+SLOT_CAP*SLOT_STRIDE==SELECTED
assert SELECTED+SELECTED_CAP*4<=PLAN_SIZE
assert ORDER+SLOT_CAP*4<=PATHCACHE
assert PATHCACHE+PATHCACHE_CAP*PATHCACHE_STRIDE<=PLAN_SIZE

def pc(r,label):
 r.j('call',label);r.label(label);r.pop('esi');r.rva('sub esi,modulepc','81ee',label)

def engine(r,reg,rva):
 r.mov(reg,m('ebx',P['host']));r.alu('add',reg,rva)

def original(r,name):r.j('call',name)

def iface(r,offset,args,slot):
 # All explicit interface calls are callee-cleanup, with interface as slot1.
 for arg in reversed(args):r.push(arg)
 r.mov('eax',m('ebx',offset));r.push('eax');r.mov('edx',m('eax'));r.unary('call',m('edx',slot))

def entry(r,name,size=128):
 r.label(name);r.prologue(size);r.mov('ebx',m('ebp',8))

def result(r,label,size,pop=4):
 r.label(label);r.epilogue(size,pop)

def unknown(r,reason):
 r.mov(m('ebx',P['status']),0);r.mov(m('ebx',P['reason']),reason);r.mov('eax',0)

def checked_type(r,reg,bad):
 r.test(reg,reg);r.j('js',bad);r.alu('cmp',reg,m('ebx',P['types']));r.j('jae',bad)

def resolve_type(r):
 entry(r,'resolve_type',64);pc(r,'resolve_type_pc')
 r.mov('edi',m('ebx',P['host']));r.mov('ecx',m('edi',0x67dcfc));r.test('ecx','ecx');r.j('jz','type_bad')
 r.mov(m('ebp',-16),-1);r.lea('eax',m('ebp',-16));r.push('eax');r.rva('lea eax,UNIT_SETTLER','8d86','settler_name');r.push('eax');engine(r,'eax',0x660f0);r.unary('call','eax');r.alu('cmp','eax',1);r.j('jne','type_bad');r.alu('cmp',m('ebp',-16),-1);r.j('je','type_bad')
 r.mov('ecx',m('edi',0x67dd18));r.test('ecx','ecx');r.j('jz','type_bad');r.mov('eax',m('ecx'));r.alu('cmp','eax',2);r.j('jl','type_bad');r.alu('cmp','eax',4097);r.j('jg','type_bad')
 r.mov(m('ebp',-20),'eax');r.mov('edx',m('ecx',8));r.test('edx','edx');r.j('jz','type_bad');r.imul('eax','eax',0x2c8);r.alu('add','eax','edx');r.j('jb','type_bad')
 r.mov(m('ebp',-24),-1);r.lea('eax',m('ebp',-24));r.push('eax');r.push(m('ebp',-16));engine(r,'eax',0x543b0);r.unary('call','eax');r.alu('cmp','eax',1);r.j('jne','type_bad')
 iface(r,P['udb'],[],0xc);r.mov(m('ebx',P['types']),'eax');r.unary('inc','eax');r.alu('cmp','eax',m('ebp',-20));r.j('jne','type_bad')
 r.mov('edi',m('ebp',-24));checked_type(r,'edi','type_bad');r.mov(m('ebx',P['t']),'edi')
 iface(r,P['udb'],['edi'],0x40);r.alu('cmp','eax',1);r.j('jne','type_bad')
 for slot in (0x44,0x48):iface(r,P['udb'],['edi'],slot);r.test('eax','eax');r.j('jnz','type_bad')
 iface(r,P['udb'],['edi'],0xdc);r.test('eax','eax');r.j('jz','type_bad')
 iface(r,P['udb'],['edi'],0xd8);r.test('eax','eax');r.mov('eax',0);r.j('jz','type_d8_done');r.mov('eax',1);r.label('type_d8_done');r.mov(m('ebx',P['d8']),'eax')
 r.mov('eax',1);r.j('jmp','type_done');r.label('type_bad');unknown(r,10);result(r,'type_done',64)

def owner_gate(r):
 # Standalone full-signed32 predicate: 1 allowed, 2 foreign, 0 unknown.
 r.label('owner_gate');r.mov('eax',m('esp',4));r.mov('edx',m('esp',8));r.alu('cmp','edx',1);r.j('jl','owner_unknown');r.alu('cmp','edx',31);r.j('jg','owner_unknown')
 r.alu('cmp','eax',-1);r.j('je','owner_allowed');r.alu('cmp','eax','edx');r.j('je','owner_allowed');r.test('eax','eax');r.j('js','owner_unknown');r.alu('cmp','eax',31);r.j('jg','owner_unknown');r.mov('eax',2);r.j('jmp','owner_done');r.label('owner_allowed');r.mov('eax',1);r.j('jmp','owner_done');r.label('owner_unknown');r.mov('eax',0);r.label('owner_done');r.op('ret8',b'\xc2\x08\x00')

def key(r):
 # Own canonical key is the bounded H3 terrain conversion. External inputs
 # remain unchanged; this key is never fed back into a World/Player query.
 entry(r,'canonical_key',32);r.mov('edi',m('ebp',16));r.zero('edi',8);r.mov('edi',m('ebp',16));r.push(m('ebp',12));r.mov('ecx','edi');engine(r,'eax',0x103f00);r.unary('call','eax')
 r.load('eax',m('edi',4),'sx16');r.test('eax','eax');r.j('jnz','key_bad');r.mov('edx',m('ebx',P['host']))
 for coord,dimension in ((0,0x67df20),(2,0x67df22)):
  r.load('eax',m('edi',coord),'sx16');r.test('eax','eax');r.j('js','key_bad');r.load('ecx',m('edx',dimension),'zx16');r.test('ecx','ecx');r.j('jz','key_bad');r.alu('cmp','eax','ecx');r.j('jae','key_bad')
 r.mov('eax',1);r.j('jmp','key_done');r.label('key_bad');r.mov('eax',0);result(r,'key_done',32,12)

def preview(r):
 entry(r,'preview_scope',64);r.mov('edi',m('ebx',P['aip']));r.mov('eax',m('edi',0x7b0));r.test('eax','eax');r.j('js','preview_bad');r.alu('cmp','eax',PREVIEW_CAP);r.j('jg','preview_bad');r.mov(m('ebx',P['classes']),'eax');r.mov(m('ebp',-16),0)
 r.mov('edx',m('edi',0x7bc));r.test('edx','edx');r.j('jz','preview_empty');r.mov('edx',m('edx'));r.test('edx','edx');r.j('jz','preview_bad');r.mov(m('ebp',-20),'edx')
 r.label('preview_loop');r.mov('eax',m('ebp',-16));r.alu('cmp','eax',m('ebx',P['classes']));r.j('jge','preview_ok');r.imul('eax','eax',16);r.mov('edx',m('ebp',-20));r.alu('add','edx','eax');r.mov('edx',m('edx',12));r.lea('esi',m('ebx',PREVIEW));r.alu('add','esi','eax');r.mov(m('esi'),'edx');r.mov(m('esi',4),-1);r.mov(m('esi',8),0);r.mov(m('esi',12),0);r.test('edx','edx');r.j('jz','preview_next')
 r.lea('eax',m('esi',4));r.push('eax');r.push('edx');r.mov('ecx','edi');original(r,'Choose');r.fp('fstp qword','dd',3,m('esi',8));r.mov('eax',m('esi',4));r.alu('cmp','eax',-1);r.j('je','preview_next');checked_type(r,'eax','preview_bad');r.mov(m('ebp',-24),'eax');iface(r,P['udb'],[m('ebp',-24)],0x40);r.alu('cmp','eax',1);r.j('ja','preview_bad');r.test('eax','eax');r.j('jz','preview_next');r.mov('eax',m('ebp',-24));r.alu('cmp','eax',m('ebx',P['t']));r.j('jne','preview_bad')
 r.label('preview_next');r.unary('inc',m('ebp',-16));r.j('jmp','preview_loop');r.label('preview_empty');r.alu('cmp',m('ebx',P['classes']),0);r.j('jne','preview_bad');r.label('preview_ok');r.mov('eax',1);r.j('jmp','preview_done');r.label('preview_bad');unknown(r,11);result(r,'preview_done',64)

def dfs(r):
 # stdcall(Plan*, Set*, kind). Shared set/nodes never written. Combined cap
 # applies to both sets, ID duplicates are tested within each namespace.
 entry(r,'read_set',80);r.mov('edi',m('ebp',12));r.test('edi','edi');r.j('jz','dfs_bad');r.mov('eax',m('edi',8));r.mov(m('ebp',-16),0);r.test('eax','eax');r.j('jz','dfs_ok');r.mov(m('ebx',STACK),'eax');r.mov(m('ebp',-16),1)
 r.label('dfs_loop');r.alu('cmp',m('ebp',-16),0);r.j('je','dfs_ok');r.unary('dec',m('ebp',-16));r.mov('eax',m('ebp',-16));r.shift('shl','eax',2);r.lea('edx',m('ebx',STACK));r.alu('add','edx','eax');r.mov('edi',m('edx'));r.mov('eax',m('ebx',P['nodes']));r.alu('cmp','eax',NODE_CAP);r.j('jae','dfs_bad');r.mov(m('ebp',-20),0)
 r.label('dfs_visited');r.mov('eax',m('ebp',-20));r.alu('cmp','eax',m('ebx',P['nodes']));r.j('jge','dfs_new');r.imul('eax','eax',NODE_STRIDE);r.lea('edx',m('ebx',VISITED));r.alu('add','edx','eax');r.alu('cmp',m('edx'),'edi');r.j('je','dfs_bad');r.mov('eax',m('ebp',16));r.alu('cmp',m('edx',8),'eax');r.j('jne','dfs_visited_next');r.mov('eax',m('edi'));r.alu('cmp',m('edx',4),'eax');r.j('je','dfs_bad');r.label('dfs_visited_next');r.unary('inc',m('ebp',-20));r.j('jmp','dfs_visited')
 r.label('dfs_new');r.mov('esi',m('edi',12));r.test('esi','esi');r.j('jz','dfs_bad');r.mov('eax',m('edi'));r.alu('cmp','eax',m('esi',12));r.j('jne','dfs_bad');r.mov('edx',m('ebp',16));r.alu('cmp','edx',m('esi',4));r.j('jne','dfs_bad');r.imul('ecx',m('ebx',P['nodes']),NODE_STRIDE);r.lea('edx',m('ebx',VISITED));r.alu('add','edx','ecx');r.mov(m('edx'),'edi');r.mov(m('edx',4),'eax');r.mov('eax',m('ebp',16));r.mov(m('edx',8),'eax');r.unary('inc',m('ebx',P['nodes']))
 r.push('esi');r.push(m('ebp',16));r.push('ebx');original(r,'read_departure');r.test('eax','eax');r.j('jz','dfs_bad')
 for offset in (4,8):
  r.mov('edx',m('edi',offset));r.test('edx','edx');r.j('jz','dfs_child_done_'+str(offset));r.mov('eax',m('ebp',-16));r.alu('cmp','eax',STACK_CAP);r.j('jae','dfs_bad');r.shift('shl','eax',2);r.lea('ecx',m('ebx',STACK));r.alu('add','ecx','eax');r.mov(m('ecx'),'edx');r.unary('inc',m('ebp',-16));r.label('dfs_child_done_'+str(offset))
 r.j('jmp','dfs_loop');r.label('dfs_ok');r.mov('eax',1);r.j('jmp','dfs_done');r.label('dfs_bad');unknown(r,12);result(r,'dfs_done',80,12)

def departures(r):
 # Entry builds real copied claims; unsupported valid armies are skipped and
 # remain in native Actual. City production and build origins share one ID.
 entry(r,'read_departure',160);r.mov('edi',m('ebp',16));r.alu('cmp',m('ebp',12),2);r.j('je','departure_city')
 r.mov('ecx','edi');original(r,'ArmyCount');r.test('eax','eax');r.j('js','departure_bad');r.alu('cmp','eax',1);r.j('jne','departure_skip');r.mov(m('ebp',-16),0);r.lea('eax',m('ebp',-16));r.push('eax');r.mov('ecx','edi');original(r,'ArmyType');checked_type(r,'eax','departure_bad');r.alu('cmp','eax',m('ebx',P['t']));r.j('jne','departure_skip');r.alu('cmp',m('edi',0x40),0);r.j('jne','departure_skip')
 r.mov('eax',m('edi',0x60));r.test('eax','eax');r.j('jz','departure_nocargo');r.load('eax',m('eax',8),'sx16');r.test('eax','eax');r.j('js','departure_bad');r.j('jnz','departure_skip');r.label('departure_nocargo');r.load('eax',m('edi',0x88),'sx8');r.test('eax',0x18);r.j('jnz','departure_skip')
 r.mov('eax',m('edi',0x74));r.alu('and','eax',0x7ff00000);r.alu('cmp','eax',0x7ff00000);r.j('je','departure_bad');r.fp('fld movement','dd',0,m('edi',0x70));r.mov(m('ebp',-24),0);r.mov(m('ebp',-20),0x40300000);r.fp('fcomp 16','dc',3,m('ebp',-24));r.op('fnstsw ax',b'\xdf\xe0');r.test('eax',0x0500);r.j('jnz','departure_skip');r.mov('ecx','edi');original(r,'IsWait');r.test('eax','eax');r.j('jnz','departure_skip')
 r.alu('cmp',m('ebx',P['departures']),DEPARTURE_CAP);r.j('jae','departure_bad');r.mov('eax',m('edi',0x64));r.test('eax','eax');r.j('jz','departure_bad');r.lea('eax',m('ebp',-40));r.push('eax');r.push(m('ebx',P['owner']));r.mov('ecx','edi');original(r,'ArmyPos');r.alu('cmp','eax',1);r.j('jne','departure_bad')
 r.mov(m('ebp',-44),-1);r.mov(m('ebp',-56),0);r.mov(m('ebp',-52),0);r.lea('eax',m('ebp',-56));r.push('eax');r.lea('eax',m('ebp',-44));r.push('eax');r.push(m('edi',12));r.mov('eax',m('ebx',P['player']));r.push('eax');r.mov('edx',m('eax'));r.unary('call',m('edx',0xc));r.unary('inc',m('ebx',P['position_queries']));r.alu('cmp','eax',1);r.j('jne','departure_bad');r.alu('cmp',m('ebp',-44),0);r.j('jne','departure_bad')
 for source,out in ((-40,-64),(-56,-72)):
  r.lea('eax',m('ebp',out));r.push('eax');r.lea('eax',m('ebp',source));r.push('eax');r.push('ebx');original(r,'canonical_key');r.test('eax','eax');r.j('jz','departure_bad')
 for off in (0,4):r.mov('eax',m('ebp',-64+off));r.alu('cmp','eax',m('ebp',-72+off));r.j('jne','departure_bad')
 r.mov(m('ebp',-76),1);r.j('jmp','departure_add')
 r.label('departure_city');r.unary('inc',m('ebx',P['cities']));r.mov('eax',m('edi',0x210));r.test('eax','eax');r.j('jz','departure_bad');r.lea('eax',m('ebp',-56));r.push('eax');r.mov('ecx','edi');original(r,'CityPos')
 r.lea('eax',m('ebp',-72));r.push('eax');r.lea('eax',m('ebp',-56));r.push('eax');r.push('ebx');original(r,'canonical_key');r.test('eax','eax');r.j('jz','departure_bad')
 r.push(m('ebx',P['owner']));r.mov('ecx','edi');original(r,'CityWhat');r.alu('cmp','eax',-1);r.j('je','departure_city_noqueue');checked_type(r,'eax','departure_bad');r.alu('cmp','eax',m('ebx',P['t']));r.j('jne','departure_city_noqueue');r.mov(m('ebp',-76),3);r.j('jmp','departure_city_build')
 r.label('departure_city_noqueue');r.mov(m('ebp',-76),2);r.label('departure_city_build');r.push(m('ebx',P['t']));r.push(m('ebx',P['owner']));r.mov('ecx','edi');original(r,'CanBuild');r.alu('cmp','eax',1);r.j('je','departure_add');r.test('eax','eax');r.j('jnz','departure_bad');r.alu('cmp',m('ebp',-76),3);r.j('jne','departure_skip');r.mov(m('ebp',-76),4)
 r.label('departure_add');r.mov('eax',m('ebx',P['departures']));r.alu('cmp','eax',DEPARTURE_CAP);r.j('jae','departure_bad');r.imul('eax','eax',DEPARTURE_STRIDE);r.lea('esi',m('ebx',DEPARTURES));r.alu('add','esi','eax');r.mov('eax',m('edi',12));r.mov(m('esi'),'eax');r.mov('eax',m('ebp',-76));r.mov(m('esi',4),'eax')
 for off in (0,4):r.mov('eax',m('ebp',-56+off));r.mov(m('esi',8+off),'eax')
 r.mov('eax',0);r.word(m('esi',14),'eax');r.mov(m('esi',16),-1);r.mov(m('esi',20),'edi');r.unary('inc',m('ebx',P['departures']))
 r.label('departure_skip');r.mov('eax',1);r.j('jmp','departure_done');r.label('departure_bad');unknown(r,13);result(r,'departure_done',160,12)

def safety(r):
 # stdcall(Plan*, externalpoint*). 1 current safe, 2 not certified safe,
 # 0 unknown whole pass. Owner, presence, legal land and converted threat
 # are all checked for every source/destination/path point.
 entry(r,'safe_point',160);r.mov('edi',m('ebp',12));r.lea('eax',m('ebp',-32));r.push('eax');r.push('edi');r.push('ebx');original(r,'canonical_key');r.test('eax','eax');r.j('jz','safe_unknown')
 r.mov(m('ebp',-36),-1);r.lea('eax',m('ebp',-36));iface(r,P['world'],['edi','eax'],0xa8);r.test('eax','eax');r.j('jz','safe_unknown');r.mov('eax',m('ebp',-36));r.alu('cmp','eax',23);r.j('ja','safe_unknown')
 for value in (10,11,12,13,14,15,16,17,18,23):r.alu('cmp','eax',value);r.j('je','safe_foreign')
 iface(r,P['player'],[m('ebx',P['t']),'edi'],0x2c);r.test('eax','eax');r.j('jz','safe_foreign')
 r.mov('ecx',m('ebx',P['owner']));r.mov('ecx',m('ecx',0xac));r.test('ecx','ecx');r.j('jz','safe_unknown');r.mov(m('ebp',-128),-1);r.mov(m('ebp',-132),-1);r.lea('eax',m('ebp',-132));r.push('eax');r.lea('eax',m('ebp',-128));r.push('eax');r.push('edi');r.push(m('ebx',P['owner']));original(r,'GetContinent');r.alu('cmp','eax',1);r.j('jne','safe_unknown');r.alu('cmp',m('ebp',-128),0);r.j('jl','safe_unknown');r.alu('cmp',m('ebp',-132),1);r.j('jne','safe_foreign')
 iface(r,P['world'],['edi'],0x54);r.push(m('ebx',P['civ']));r.push('eax');original(r,'owner_gate');r.alu('cmp','eax',1);r.j('je','safe_presence');r.alu('cmp','eax',2);r.j('je','safe_foreign');r.j('jmp','safe_unknown')
 r.label('safe_presence');r.lea('eax',m('ebp',-88));r.zero('eax',36);r.mov('edi',m('ebp',12));r.mov(m('ebp',-92),0x1abc2345);r.mov(m('ebp',-52),0x6bcd3456)
 # Same nine output slots/pushes as InsertBestSettleGoal, with own storage.
 for off in range(-56,-89,-4):r.lea('eax',m('ebp',off));r.push('eax')
 r.push('edi');r.mov('eax',m('ebx',P['world']));r.push('eax');r.mov('edx',m('eax'));r.unary('call',m('edx',0x78))
 for off,val in ((-92,0x1abc2345),(-52,0x6bcd3456)):r.alu('cmp',m('ebp',off),val);r.j('jne','safe_unknown')
 # Slot1 = raw owner, slot2/unitpresence, slot5/citypresence.
 r.mov('eax',m('ebp',-88));r.alu('cmp','eax',m('ebx',P['civ']));r.j('je','safe_threat')
 for off in (-84,-72):r.alu('cmp',m('ebp',off),0);r.j('jne','safe_foreign')
 r.label('safe_threat');r.lea('eax',m('ebp',-104));iface(r,P['player'],['edi','eax'],0x14)
 r.load('eax',m('ebp',-100),'sx16');r.test('eax','eax');r.j('jnz','safe_unknown');r.mov('edi',m('ebx',P['planner']));r.mov('edi',m('edi',0xa70));r.test('edi','edi');r.j('jz','safe_unknown');r.mov('ecx',m('edi'));r.test('ecx','ecx');r.j('jle','safe_unknown')
 pc(r,'safe_pc');r.mov('esi',m('esi',0xc6fdc));r.test('esi','esi');r.j('jz','safe_unknown');r.alu('cmp',m('esi'),0);r.j('je','safe_unknown')
 for pos,bound in ((-104,8),(-102,4)):
  r.load('eax',m('ebp',pos),'sx16');r.test('eax','eax');r.j('js','safe_unknown');r.op('cdq',b'\x99');r.op('idiv ecx',b'\xf7\xf9');r.alu('cmp',m('esi',bound),0);r.j('jle','safe_unknown');r.alu('cmp','eax',m('esi',bound));r.j('jae','safe_unknown')
 r.lea('eax',m('ebp',-104));r.push('eax');r.mov('ecx','edi');original(r,'GetThreat');r.fp('fstp threat','dd',3,m('ebp',-120));r.unary('inc',m('ebx',P['safetycalls']));r.mov('eax',m('ebp',-116));r.alu('and','eax',0x7ff00000);r.alu('cmp','eax',0x7ff00000);r.j('je','safe_unknown')
 r.mov('eax',m('ebp',-116));r.alu('and','eax',0x7fffffff);r.alu('or','eax',m('ebp',-120));r.j('jz','safe_ok');r.test(m('ebp',-116),0x80000000);r.j('jnz','safe_unknown')
 r.label('safe_foreign');r.mov('eax',2);r.j('jmp','safe_done');r.label('safe_unknown');unknown(r,20);r.j('jmp','safe_done');r.label('safe_ok');r.mov('eax',1);result(r,'safe_done',160,8)

def path(r):
 # stdcall(Plan*, source*, destination*), exactly twenty four-byte slots.
 # Every nonnull native returned pointer is freed once, including failures.
 entry(r,'direct_path',128);r.mov(m('ebp',-16),0);r.mov(m('ebp',-20),0);r.mov(m('ebp',-24),0);r.mov(m('ebp',-28),0);r.mov(m('ebp',-32),0);r.mov(m('ebp',-36),0);r.mov(m('ebp',-40),0x3456ab89);r.mov(m('ebp',-12-32),0x4567bc90)
 r.alu('cmp',m('ebx',P['path_queries']),128);r.j('jae','path_unknown');r.mov('edx',m('ebx',P['host']));r.alu('cmp',m('edx',0x6d0b94),0);r.j('jne','path_unknown');r.unary('inc',m('ebx',P['path_queries']))
 # Push20..1. Slot12 is the normalized frozen d8 queryresult.
 r.push(1);r.push(0);r.push(1);r.lea('eax',m('ebp',-32));r.push('eax');r.push(4096);r.push(0);r.push(0);r.push(1);r.push(m('ebx',P['d8']))
 for off in (-28,-24,-20,-16):r.lea('eax',m('ebp',off));r.push('eax')
 r.push(m('ebp',16));r.push(m('ebp',12));r.push(m('ebx',P['t']));r.push(1);r.push(0);r.push(0);r.mov('eax',m('ebx',P['path']));r.push('eax');r.mov('edx',m('eax'));r.unary('call',m('edx',12));r.mov(m('ebp',-36),'eax')
 r.mov('edx',m('ebx',P['host']));r.alu('cmp',m('edx',0x6d0b94),0);r.j('jne','path_unknown');r.alu('cmp',m('ebp',-40),0x3456ab89);r.j('jne','path_unknown');r.alu('cmp',m('ebp',-44),0x4567bc90);r.j('jne','path_unknown')
 r.alu('cmp',m('ebp',-36),1);r.j('jne','path_unknown');r.mov('esi',m('ebp',-20));r.test('esi','esi');r.j('jz','path_unknown');r.mov('eax',m('ebp',-24));r.alu('cmp','eax',1);r.j('jl','path_unknown');r.alu('cmp','eax',4096);r.j('jg','path_unknown');r.alu('cmp','eax',m('ebp',-16));r.j('jg','path_unknown');r.shift('shl','eax',3);r.alu('add','eax','esi');r.j('jb','path_unknown')
 for off,point in ((0,12),(-8,16)):
  if off==0:r.mov('edx','esi')
  else:r.lea('edx',m('eax',-8))
  r.lea('ecx',m('ebp',-64));r.push('ecx');r.push('edx');r.push('ebx');original(r,'canonical_key');r.test('eax','eax');r.j('jz','path_unknown');r.lea('ecx',m('ebp',-72));r.push('ecx');r.push(m('ebp',point));r.push('ebx');original(r,'canonical_key');r.test('eax','eax');r.j('jz','path_unknown')
  for part in (0,4):r.mov('eax',m('ebp',-64+part));r.alu('cmp','eax',m('ebp',-72+part));r.j('jne','path_unknown')
  r.mov('eax',m('ebp',-24));r.shift('shl','eax',3);r.alu('add','eax','esi')
 r.mov(m('ebp',-36),1);r.mov(m('ebp',-48),0)
 r.label('path_points');r.mov('eax',m('ebp',-48));r.alu('cmp','eax',m('ebp',-24));r.j('jge','path_free');r.shift('shl','eax',3);r.alu('add','eax','esi');r.push('eax');r.push('ebx');original(r,'safe_point');r.alu('cmp','eax',1);r.j('je','path_next');r.alu('cmp','eax',2);r.j('jne','path_unknown');r.mov(m('ebp',-36),2);r.j('jmp','path_free')
 r.label('path_next');r.unary('inc',m('ebp',-48));r.j('jmp','path_points');r.label('path_unknown');unknown(r,21);r.mov(m('ebp',-36),0)
 r.label('path_free');r.mov('eax',m('ebp',-20));r.test('eax','eax');r.j('jz','path_done');r.push('eax');engine(r,'eax',0x1866e0);r.unary('call','eax');r.alu('add','esp',4);r.mov(m('ebp',-20),0)
 r.label('path_done');r.mov('eax',m('ebp',-36));r.epilogue(128,12)

def capture(r):
 entry(r,'capture_heap',64);r.mov('edi',m('ebx',P['map']));r.mov('eax',m('edi',0x60));r.alu('cmp','eax',1);r.j('jl','capture_bad');r.alu('cmp','eax',32765);r.j('jae','capture_bad');r.alu('cmp','eax',m('edi',0x5c));r.j('jg','capture_bad');r.mov(m('ebp',-16),'eax');r.mov('esi',m('edi',0x64));r.test('esi','esi');r.j('jz','capture_bad');r.alu('cmp',m('esi'),0);r.j('jne','capture_bad');r.mov(m('ebp',-20),1);r.mov(m('ebx',P['candidates']),0)
 r.label('capture_loop');r.mov('eax',m('ebp',-20));r.alu('cmp','eax',m('ebp',-16));r.j('jge','capture_ok');r.shift('shl','eax',2);r.mov('edx','esi');r.alu('add','edx','eax');r.mov('edx',m('edx'));r.test('edx','edx');r.j('jz','capture_bad');r.mov('eax',m('edx'));r.mov(m('ebp',-32),'eax');r.mov(m('ebp',-28),0)
 r.lea('eax',m('ebp',-40));r.push('eax');r.lea('eax',m('ebp',-32));r.push('eax');r.push('ebx');original(r,'canonical_key');r.test('eax','eax');r.j('jz','capture_bad');r.mov(m('ebp',-24),0)
 r.label('capture_dedup');r.mov('eax',m('ebp',-24));r.alu('cmp','eax',m('ebx',P['candidates']));r.j('jge','capture_add');r.shift('shl','eax',3);r.lea('edi',m('ebx',CAPTURE));r.alu('add','edi','eax');r.lea('eax',m('ebp',-48));r.push('eax');r.push('edi');r.push('ebx');original(r,'canonical_key');r.test('eax','eax');r.j('jz','capture_bad');r.mov('eax',m('ebp',-40));r.alu('cmp','eax',m('ebp',-48));r.j('je','capture_next');r.unary('inc',m('ebp',-24));r.j('jmp','capture_dedup')
 r.label('capture_add');r.mov('eax',m('ebx',P['candidates']));r.alu('cmp','eax',CAPTURE_CAP);r.j('jae','capture_bad');r.shift('shl','eax',3);r.lea('edx',m('ebx',CAPTURE));r.alu('add','edx','eax');r.mov('eax',m('ebp',-32));r.mov(m('edx'),'eax');r.mov(m('edx',4),0);r.unary('inc',m('ebx',P['candidates']))
 r.label('capture_next');r.unary('inc',m('ebp',-20));r.j('jmp','capture_loop');r.label('capture_ok');r.mov(m('ebx',P['status']),2);r.mov('eax',1);r.j('jmp','capture_done');r.label('capture_bad');unknown(r,22);result(r,'capture_done',64)

def roles(r):
 entry(r,'production_roles',96);r.mov(m('ebx',P['slots']),0);r.mov(m('ebp',-16),0)
 r.label('roles_loop');r.mov('eax',m('ebp',-16));r.alu('cmp','eax',m('ebx',P['candidates']));r.j('jge','roles_ok');r.shift('shl','eax',3);r.lea('edi',m('ebx',CAPTURE));r.alu('add','edi','eax')
 for off in (4,2,0):r.load('eax',m('edi',off),'sx16');r.push('eax')
 r.mov('eax',m('ebx',P['world']));r.push('eax');r.mov('edx',m('eax'));r.unary('call',m('edx',0x168));r.op('movsx eax,ax',b'\x0f\xbf\xc0');r.test('eax','eax');r.j('jle','roles_next');r.mov(m('ebp',-20),'eax');r.alu('cmp',m('ebx',P['h3calls']),64);r.j('jae','roles_bad');r.unary('inc',m('ebx',P['h3calls']))
 r.imul('esi',m('ebx',P['slots']),SLOT_STRIDE);r.alu('add','esi','ebx');r.alu('add','esi',SLOTS);r.lea('eax',m('esi',128));r.push('eax');r.push('edi');r.push(m('ebx',P['world']));r.push(m('ebx',P['owner']));original(r,'H3Classifier');r.test('eax','eax');r.j('jz','roles_bad');r.alu('cmp','eax',2);r.j('jne','roles_next');r.alu('cmp',m('esi',136),1);r.j('jne','roles_bad')
 r.mov('eax',m('esi',196));r.test('eax','eax');r.j('js','roles_next');r.j('jnz','roles_now');r.alu('cmp',m('esi',192),0);r.j('je','roles_next');r.label('roles_now')
 for off in (0,4):r.mov('eax',m('edi',off));r.mov(m('esi',off),'eax')
 r.lea('eax',m('esi',8));r.push('eax');r.push('edi');r.push('ebx');original(r,'canonical_key');r.test('eax','eax');r.j('jz','roles_bad')
 r.mov('eax',m('ebp',-20));r.alu('cmp','eax',32767);r.j('je','roles_q');r.unary('inc','eax');r.label('roles_q');r.mov(m('esi',16),'eax');r.mov(m('esi',20),-1);r.mov(m('esi',24),-1);r.mov('eax',m('esi',8));r.mov(m('esi',32),'eax');r.mov('eax',m('esi',12));r.mov(m('esi',36),'eax')
 for i,idx in enumerate((100,104,108,112)):
  r.mov('eax',m('esi',128+idx));r.test('eax','eax');r.j('js','roles_bad');r.alu('cmp','eax',m('esi',224));r.j('jae','roles_bad');r.imul('eax','eax',12);r.alu('add','eax','esi');r.alu('add','eax',272);r.lea('edx',m('esi',40+8*i));r.push('edx');r.push('eax');r.push('ebx');original(r,'canonical_key');r.test('eax','eax');r.j('jz','roles_bad')
 r.unary('inc',m('ebx',P['slots']));r.label('roles_next');r.unary('inc',m('ebp',-16));r.j('jmp','roles_loop');r.label('roles_ok');r.mov('eax',1);r.j('jmp','roles_done');r.label('roles_bad');unknown(r,23);result(r,'roles_done',96)

def ordering(r):
 # Sort indices, never heap/source data or H3 comparator inputs. Maximum64.
 entry(r,'order_roles',48);r.mov('edi',0)
 r.label('order_init');r.alu('cmp','edi',m('ebx',P['slots']));r.j('jge','order_sort_begin');r.mov('eax','edi');r.shift('shl','eax',2);r.lea('edx',m('ebx',ORDER));r.alu('add','edx','eax');r.mov(m('edx'),'edi');r.unary('inc','edi');r.j('jmp','order_init')
 r.label('order_sort_begin');r.mov(m('ebp',-16),0);r.label('order_outer');r.mov('eax',m('ebp',-16));r.alu('cmp','eax',m('ebx',P['slots']));r.j('jge','order_done');r.mov(m('ebp',-20),0)
 r.label('order_inner');r.mov('eax',m('ebp',-20));r.unary('inc','eax');r.alu('cmp','eax',m('ebx',P['slots']));r.j('jge','order_outer_next');r.mov('eax',m('ebp',-20));r.shift('shl','eax',2);r.lea('edi',m('ebx',ORDER));r.alu('add','edi','eax');r.imul('esi',m('edi'),SLOT_STRIDE);r.alu('add','esi','ebx');r.alu('add','esi',SLOTS);r.imul('edx',m('edi',4),SLOT_STRIDE);r.alu('add','edx','ebx');r.alu('add','edx',SLOTS);r.mov('eax',m('esi',16));r.alu('cmp','eax',m('edx',16));r.j('jl','order_swap');r.j('jg','order_next');r.lea('eax',m('edx',8));r.push('eax');r.lea('eax',m('esi',8));r.push('eax');original(r,'H3PosCompare');r.test('eax','eax');r.j('jle','order_next')
 r.label('order_swap');r.mov('eax',m('edi'));r.mov('edx',m('edi',4));r.mov(m('edi'),'edx');r.mov(m('edi',4),'eax');r.label('order_next');r.unary('inc',m('ebp',-20));r.j('jmp','order_inner');r.label('order_outer_next');r.unary('inc',m('ebp',-16));r.j('jmp','order_outer');r.label('order_done');r.epilogue(48,4)

def conflicts(r):
 # stdcall(Plan*, candidateSlot*, selectedSlot*): 1 iff any centre or
 # mandatory worker key intersects; ordinary non-mandatory overlap allowed.
 r.label('plan_conflict');r.prologue(16);r.mov('esi',m('ebp',12));r.mov('edi',m('ebp',16));r.mov('ecx',0)
 r.label('conflict_outer');r.alu('cmp','ecx',5);r.j('jge','conflict_none');r.mov('edx',0);r.label('conflict_inner');r.alu('cmp','edx',5);r.j('jge','conflict_next_outer');r.mov('eax','ecx');r.shift('shl','eax',3);r.alu('add','eax','esi');r.mov('ebx','edx');r.shift('shl','ebx',3);r.alu('add','ebx','edi');r.mov('eax',m('eax',32));r.alu('cmp','eax',m('ebx',32));r.j('je','conflict_yes');r.unary('inc','edx');r.j('jmp','conflict_inner');r.label('conflict_next_outer');r.unary('inc','ecx');r.j('jmp','conflict_outer');r.label('conflict_none');r.mov('eax',0);r.j('jmp','conflict_done');r.label('conflict_yes');r.mov('eax',1);r.label('conflict_done');r.epilogue(16,12)

def path_cache(r):
 # type/source/destination identity, own result only, never native pointers.
 entry(r,'cached_path',64);r.lea('eax',m('ebp',-24));r.push('eax');r.push(m('ebp',12));r.push('ebx');original(r,'canonical_key');r.test('eax','eax');r.j('jz','cached_unknown');r.lea('eax',m('ebp',-32));r.push('eax');r.push(m('ebp',16));r.push('ebx');original(r,'canonical_key');r.test('eax','eax');r.j('jz','cached_unknown');r.mov('edi',0)
 r.label('cached_lookup');r.alu('cmp','edi',m('ebx',136));r.j('jge','cached_new');r.imul('esi','edi',PATHCACHE_STRIDE);r.alu('add','esi','ebx');r.alu('add','esi',PATHCACHE)
 for own,cached in ((-24,0),(-20,4),(-32,8),(-28,12)):
  r.mov('eax',m('ebp',own));r.alu('cmp','eax',m('esi',cached));r.j('jne','cached_next')
 r.mov('eax',m('ebx',P['t']));r.alu('cmp','eax',m('esi',16));r.j('jne','cached_next');r.mov('eax',m('esi',20));r.j('jmp','cached_done');r.label('cached_next');r.unary('inc','edi');r.j('jmp','cached_lookup')
 r.label('cached_new');r.alu('cmp','edi',PATHCACHE_CAP);r.j('jae','cached_unknown');r.push(m('ebp',16));r.push(m('ebp',12));r.push('ebx');original(r,'direct_path');r.test('eax','eax');r.j('jz','cached_done');r.mov(m('ebp',-36),'eax');r.imul('esi','edi',PATHCACHE_STRIDE);r.alu('add','esi','ebx');r.alu('add','esi',PATHCACHE)
 for own,cached in ((-24,0),(-20,4),(-32,8),(-28,12)):
  r.mov('eax',m('ebp',own));r.mov(m('esi',cached),'eax')
 r.mov('eax',m('ebx',P['t']));r.mov(m('esi',16),'eax');r.mov('eax',m('ebp',-36));r.mov(m('esi',20),'eax');r.unary('inc',m('ebx',136));r.j('jmp','cached_done');r.label('cached_unknown');unknown(r,24);result(r,'cached_done',64,12)

def selection(r):
 entry(r,'select_direct_plans',96);r.mov(m('ebx',P['desired']),0);r.mov(m('ebp',-16),0)
 r.label('select_loop');r.mov('eax',m('ebp',-16));r.alu('cmp','eax',m('ebx',P['slots']));r.j('jge','select_ok');r.mov('eax',m('ebx',P['desired']));r.alu('cmp','eax',m('ebx',P['remaining']));r.j('jge','select_ok');r.mov('eax',m('ebp',-16));r.shift('shl','eax',2);r.lea('edx',m('ebx',ORDER));r.alu('add','edx','eax');r.mov('eax',m('edx'));r.mov(m('ebp',-20),'eax');r.imul('edi','eax',SLOT_STRIDE);r.alu('add','edi','ebx');r.alu('add','edi',SLOTS);r.mov(m('ebp',-24),0)
 r.label('select_conflicts');r.mov('eax',m('ebp',-24));r.alu('cmp','eax',m('ebx',P['desired']));r.j('jge','select_endpoint');r.shift('shl','eax',2);r.lea('edx',m('ebx',SELECTED));r.alu('add','edx','eax');r.imul('eax',m('edx'),SLOT_STRIDE);r.alu('add','eax','ebx');r.alu('add','eax',SLOTS);r.push('eax');r.push('edi');r.push('ebx');original(r,'plan_conflict');r.test('eax','eax');r.j('jnz','select_next');r.unary('inc',m('ebp',-24));r.j('jmp','select_conflicts')
 r.label('select_endpoint');iface(r,P['player'],[m('ebx',P['t']),'edi'],0x34);r.test('eax','eax');r.j('jz','select_next');r.mov(m('ebp',-28),0);r.mov(m('ebp',-32),0)
 # Three stable priorities: ordinary existing, frontproduction, newbuild.
 # Within each priority choose lowest raw ID that certifies this destination.
 r.label('select_priority');r.alu('cmp',m('ebp',-28),3);r.j('jae','select_next');r.mov(m('ebp',-36),0);r.mov(m('ebp',-40),-1);r.mov(m('ebp',-44),-1)
 r.label('select_sources');r.mov('eax',m('ebp',-36));r.alu('cmp','eax',m('ebx',P['departures']));r.j('jge','select_best');r.imul('esi','eax',DEPARTURE_STRIDE);r.alu('add','esi','ebx');r.alu('add','esi',DEPARTURES);r.mov('eax',m('esi',4));r.alu('cmp',m('ebp',-28),0);r.j('je','source_existing');r.alu('cmp',m('ebp',-28),1);r.j('je','source_front');r.alu('cmp','eax',2);r.j('je','source_path');r.alu('cmp','eax',3);r.j('je','source_path');r.j('jmp','source_next')
 r.label('source_existing');r.alu('cmp','eax',1);r.j('jne','source_next');r.alu('cmp',m('esi',16),-1);r.j('jne','source_next');r.j('jmp','source_path')
 r.label('source_front');r.alu('cmp','eax',3);r.j('je','source_front_match');r.alu('cmp','eax',4);r.j('jne','source_next');r.label('source_front_match');r.alu('cmp',m('esi',16),-1);r.j('jne','source_next')
 r.label('source_path');r.lea('eax',m('esi',8));r.push('edi');r.push('eax');r.push('ebx');original(r,'cached_path');r.test('eax','eax');r.j('jz','select_bad');r.alu('cmp','eax',1);r.j('jne','source_next');r.mov('eax',m('esi'));r.alu('cmp',m('ebp',-44),-1);r.j('je','source_choose');r.alu('cmp','eax',m('ebp',-40));r.j('jae','source_next');r.label('source_choose');r.mov(m('ebp',-40),'eax');r.mov('eax',m('ebp',-36));r.mov(m('ebp',-44),'eax')
 r.label('source_next');r.unary('inc',m('ebp',-36));r.j('jmp','select_sources');r.label('select_best');r.alu('cmp',m('ebp',-44),-1);r.j('jne','select_add');r.unary('inc',m('ebp',-28));r.j('jmp','select_priority')
 r.label('select_add');r.mov('eax',m('ebp',-44));r.mov(m('edi',24),'eax');r.imul('esi','eax',DEPARTURE_STRIDE);r.alu('add','esi','ebx');r.alu('add','esi',DEPARTURES);r.mov('eax',m('esi'));r.mov(m('edi',20),'eax');r.alu('cmp',m('ebp',-28),2);r.j('je','select_buildorigin');r.mov('eax',m('ebp',-20));r.mov(m('esi',16),'eax');r.label('select_buildorigin');r.mov('eax',m('ebx',P['desired']));r.shift('shl','eax',2);r.lea('edx',m('ebx',SELECTED));r.alu('add','edx','eax');r.mov('eax',m('ebp',-20));r.mov(m('edx'),'eax');r.unary('inc',m('ebx',P['desired']))
 r.label('select_next');r.unary('inc',m('ebp',-16));r.j('jmp','select_loop');r.label('select_ok');r.mov('eax',1);r.j('jmp','select_done');r.label('select_bad');unknown(r,25);result(r,'select_done',96)
