"""Read-only original-code checks; synthetic state, no game/order execution."""
from pathlib import Path
import sys, struct, json, hashlib
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import *
import pefile
from ctp_x87 import ftol_stub

binary = ROOT / 'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll'
digest = hashlib.sha256(binary.read_bytes()).hexdigest()
assert digest == '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
pe = pefile.PE(str(binary))
M = 0x30000000
OBJ, AI, PLAYER, VT, TABLE, OUT, POS, FRAME = [M + i * 0x1000 for i in range(1,9)]
STACK, STOP, HOOK = M + 0xe0000, M + 0xff000, M + 0x20000
checks = []
def integer(u,a,v=None):
    if v is None: return struct.unpack('<I',u.mem_read(a,4))[0]
    u.mem_write(a,struct.pack('<I',v & 0xffffffff))
def real(u,a,v=None):
    if v is None: return struct.unpack('<d',u.mem_read(a,8))[0]
    u.mem_write(a,struct.pack('<d',v))
def floating(u,a,v=None):
    if v is None: return struct.unpack('<f',u.mem_read(a,4))[0]
    u.mem_write(a,struct.pack('<f',v))
def ret(u,n,v=0):
    sp=u.reg_read(UC_X86_REG_ESP)
    u.reg_write(UC_X86_REG_EAX,v)
    u.reg_write(UC_X86_REG_EIP,integer(u,sp))
    u.reg_write(UC_X86_REG_ESP,sp+4+n)
def fixture():
    u=Uc(UC_ARCH_X86,UC_MODE_32)
    u.mem_map(0,0x1000)
    u.mem_map(0x20000000,(pe.OPTIONAL_HEADER.SizeOfImage+4095)&~4095)
    u.mem_write(0x20000000,pe.get_memory_mapped_image())
    u.mem_map(M,0x100000)
    u.mem_write(0x20085dc0,ftol_stub()) # In-memory CRT substitute only.
    u.reg_write(UC_X86_REG_FPCW,0x37f)
    integer(u,AI+0x84,OUT); real(u,OUT,60)
    integer(u,AI+0x2c,PLAYER);integer(u,PLAYER,VT)
    integer(u,AI+0xa8,TABLE)
    return u
def run(u,a,args=(),receiver=OBJ):
    integer(u,STACK,STOP)
    for i,v in enumerate(args): integer(u,STACK+4+4*i,v)
    u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,receiver)
    u.emu_start(a,STOP,count=100000)
    assert u.reg_read(UC_X86_REG_EIP)==STOP
    return u.reg_read(UC_X86_REG_EAX)
def fragment(u,a,end):
    u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_EBP,FRAME)
    u.emu_start(a,end,count=100000)
    assert u.reg_read(UC_X86_REG_EIP)==end
def record(name,got,want,mocks=()):
    checks.append(dict(name=name,got=got,expected=want,passed=got==want,external_mocks=list(mocks)))

# The three API arguments become diplomatic, unit and a shared bonus/cache pair.
u=fixture();run(u,0x2000cc60,[67,28,-9])
record('set_regard_fields',[real(u,OBJ+x) for x in (0x60,0x68,0x70,0x78)],[67,28,-9,-9])
for name,a,value,bonus,expected in [
    ('hot_attack',0x2000c750,80,25,[19,19,0,0,0]),
    ('hot_attack_low',0x2000c750,12,25,[12,12,0,0,0]),
    ('cease_broken',0x2000cc90,80,25,[15,15,0,25,0]),
    ('cease_exact20',0x2000cc90,20,25,[15,20,0,25,0]),
    ('alliance_broken',0x2000ccf0,80,25,[19,19,25,25,0]),
    ('alliance_low',0x2000ccf0,12,25,[12,12,25,25,0])]:
    u=fixture()
    for x in (0x60,0x68):real(u,OBJ+x,value)
    for x in (0x70,0x78):real(u,OBJ+x,bonus)
    integer(u,OBJ+0x204,1)
    if a==0x2000c750:run(u,a,[AI,*struct.unpack('<II',struct.pack('<d',1.0))])
    else:run(u,a)
    record(name,[real(u,OBJ+x) for x in (0x60,0x68,0x70,0x78)]+[integer(u,OBJ+0x204)],expected,
           ['CRT ftol preserving caller FPCW'] if a==0x2000c750 else [])

for name,foreign_id,exists,expected in [('other',2,True,3),('self',1,True,2),('missing',2,False,2)]:
    u=fixture();integer(u,AI+0x20,1);real(u,OBJ+0x1d8,2)
    if exists:integer(u,TABLE+4*foreign_id,OBJ)
    run(u,0x20034c30,[AI,foreign_id,7])
    record('broken_treaty_'+name,real(u,OBJ+0x1d8),expected)

# Actual update fragment, with an explicit valid register/frame entry.
for name,old,request,expected in [
    ('zero_preserves',80,0,80),('five_preserves',80,5,80),
    ('six_replaces',80,6,6),('35_replaces',80,35,35),
    ('over100_clamps',80,120,100),('negative_input_floor',-10,0,11)]:
    u=fixture();real(u,0x200c6a28,old);real(u,0x200c6ac0,request)
    u.reg_write(UC_X86_REG_ESI,OBJ)
    fragment(u,0x2002f94b,0x2002f9c4)
    record('unit_regard_'+name,[real(u,OBJ+0x68),real(u,0x200c6ac0)],[expected,0])

# Penalty-only suffix, not the complete callback/pathfinder. World owner is a mock.
for name,enabled,owner,foreigner_present,agreement,regard,expected in [
    ('active20',1,2,True,1,20,90),('active80',1,2,True,1,80,90),
    ('below20',1,2,True,1,19.99,10),('no_agreement',1,2,True,0,80,10),
    ('global_disabled',0,2,True,1,80,10),('owner_zero',1,0,True,1,80,10),
    ('owner32',1,32,True,1,80,10),('unknown_foreigner',1,2,False,1,80,10)]:
    u=fixture();integer(u,0x2009bf3c,AI);integer(u,AI+0x13c,enabled)
    integer(u,AI+0x30,PLAYER);integer(u,VT+0x54,HOOK)
    if foreigner_present:integer(u,TABLE+4*owner,OBJ)
    integer(u,OBJ+0x204,agreement);real(u,OBJ+0x68,regard)
    floating(u,0x2009bf20,80);floating(u,OUT,10)
    def owner_query(uc,a,size,data):
        if a==HOOK:ret(uc,8,owner)
    u.hook_add(UC_HOOK_CODE,owner_query)
    u.reg_write(UC_X86_REG_ESI,OUT);u.reg_write(UC_X86_REG_EDI,POS)
    fragment(u,0x200178a1,0x200178fc)
    record('transport_treaty_cost_'+name,floating(u,OUT),expected,['World tile-owner query'])

# Whole AI bombard attempt: query before action; no engine combat executed.
for name,eligible,accepted,want in [
    ('ineligible',0,1,[0,[]]),('accepted',1,1,[1,[[17,[3,4,0]]]]),
    ('engine_rejected',1,0,[0,[[17,[3,4,0]]]])]:
    u=fixture();integer(u,OBJ+0xc,17)
    integer(u,FRAME,FRAME+0x1000);integer(u,FRAME+0x1000+0x5c,HOOK+0x300)
    integer(u,VT+0x19c,HOOK+0x100);integer(u,VT+0x198,HOOK+0x200)
    requests=[]
    def bombard_callbacks(uc,a,size,data):
        sp=uc.reg_read(UC_X86_REG_ESP)
        if a==HOOK+0x300:
            uc.mem_write(integer(uc,sp+4),struct.pack('<hhh',3,4,0)+b'\0\0')
            ret(uc,4)
        elif a==HOOK+0x100:ret(uc,16,eligible)
        elif a==HOOK+0x200:
            p=integer(uc,sp+16)
            requests.append([integer(uc,sp+8),list(struct.unpack('<hhh',uc.mem_read(p,6)))])
            ret(uc,16,accepted)
    u.hook_add(UC_HOOK_CODE,bombard_callbacks)
    returned=run(u,0x200165b0,[AI,POS,FRAME])
    record('bombard_request_'+name,[returned,requests],want,
           ['Goal position getter','Player bombard target query +19c','Player bombard action +198'])

result=dict(binary_sha256=digest,scope='Original regard/treaty and bombard request functions and two explicitly bounded fragments; no full diplomacy pass/pathfinder/order/game',checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),fixtures='Synthetic Foreigner/AiMain/frame; in-memory ftol stub only where declared; FPCW 0x37f, actual game controlword unknown')
(ROOT/'ANALYSE/BINAIR/diplomacy-naval-controls.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(f"{result['passed']}/{result['total']} controls passed")
for c in checks:
    if not c['passed']:print(c)
assert result['passed']==result['total']
