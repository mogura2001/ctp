"""Original CTP I research cost, age selector and queue cost instructions.

Synthetic records, no game or binary writes. Research executes real age/known
getters; only optional wonder deduction uses an explicit mock. Queue admission,
city lookup/owner and heap allocation are mocks; formula and node writes are real.
FTOL substitutes the imported CRT and preserves x87 CW; PC=extended RC=nearest.
"""
from pathlib import Path
import hashlib,json,math,struct,sys
from fractions import Fraction
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from ctp_x87 import ftol_stub
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
P=ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
HASH='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
assert hashlib.sha256(P.read_bytes()).hexdigest()==HASH
pe=pefile.PE(str(P)); image=pe.get_memory_mapped_image()
PLAYERS,PLAYER,SCIENCE,KNOWN,DIFF,LEVEL,AGE,AGES,ADB,ADVANCES,PROPERTY,QUEUE,NODE,STACK=[0x30010000+i*0x8000 for i in range(14)]
STOP=0x300f0000
TECH=[-.1,-.2,-.3,-.4,-.6]; PROD=[-.05,-.15,-.3,-.4,-.5]
def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def get(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
def fixture(age=0,kind=1,count=3,base=65):
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(image)+4095)&~4095);u.mem_write(0x400000,image)
 u.mem_map(0x30000000,0x100000);u.reg_write(UC_X86_REG_FPCW,0x37f)
 for a,v in [(0xa7dd80,PLAYERS),(PLAYERS,PLAYER),(PLAYER+4,kind),(PLAYER+0x12ec,SCIENCE),
 (PLAYER+0x12e8,PROPERTY),(PROPERTY+0xc0,25),(SCIENCE,0),(SCIENCE+4,200),(SCIENCE+0x18,count),
 (SCIENCE+0x1c,KNOWN),(0xa7dd54,DIFF),(0xa7a6a4,LEVEL),(LEVEL,5),(0xa7dd4c,AGE),
 (AGE,5),(AGE+4,AGES),(0xa7dd00,ADB),(ADB+8,ADVANCES),(ADVANCES+0x58,base),
 (0xa7dd74,1)]:put(u,a,v)
 for i in range(5):
  put(u,AGES+i*0x34,1);put(u,AGES+i*0x34+4,i+10)
  u.mem_write(KNOWN+i+10,bytes([i<=age]));dbl(u,DIFF+5*512+0x150+8*i,TECH[i]);dbl(u,DIFF+5*512+0x178+8*i,PROD[i])
 dbl(u,DIFF+5*512+0x1d0,.25)
 u.mem_write(0x300f2000,ftol_stub());put(u,0x743330,0x300f2000)
 return u
def run(u,start,this,args=()):
 put(u,STACK,STOP)
 for i,a in enumerate(args):put(u,STACK+4+i*4,a)
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,this)
 u.emu_start(start,STOP,count=20000);v=u.reg_read(UC_X86_REG_EAX)
 return v if v<0x80000000 else v-0x100000000
def ret(u,v,argc=0):
 sp=u.reg_read(UC_X86_REG_ESP);target=get(u,sp);u.reg_write(UC_X86_REG_EAX,v&0xffffffff)
 u.reg_write(UC_X86_REG_ESP,sp+4+argc);u.reg_write(UC_X86_REG_EIP,target)
checks=[]
def check(name,got,expected,**context):
 checks.append(dict(name=name,got=got,expected=expected,passed=got==expected,**context))
def adjustment(raw,coefficient):
 # Exact stored IEEE double times integer. Small fixture products fit x87 PC64;
 # Python float multiplication would round them to 53 bits before truncation.
 return math.trunc(Fraction.from_float(coefficient)*raw)
for age in range(5):
 u=fixture(age);check('age_'+str(age),run(u,0x44eee0,AGE,[0]),age)
 for base,count in [(65,0),(65,3),(65,4),(20,3),(1,0)]:
  u=fixture(age,count=count,base=base);raw=base+25*count
  check('research_%s_%s_%s'%(age,base,count),run(u,0x475990,SCIENCE,[0]),raw+adjustment(raw,TECH[age]),age=age,base=base,known_count=count,rounded_double_model=raw+math.trunc(raw*TECH[age]))
 for category in [1,3,9]:
  u=fixture(age);cost=135
  def hook(uc,address,size,data):
   if address==0x4b2300:ret(uc,1,4)
   elif address in [0x4ddc90,0x4ddcc0]:ret(uc,1,4)
   elif address==0x4745a0:ret(uc,1,8)
   elif address==0x4da960:ret(uc,0)
   elif address==0x5866b0:ret(uc,NODE)
  u.hook_add(UC_HOOK_CODE,hook);run(u,0x490cf0,QUEUE,[category,0,cost])
  check('queue_%s_%s'%(age,category),[get(u,NODE),get(u,NODE+8),get(u,QUEUE)],
        [cost+adjustment(cost,PROD[age]),category,1],age=age,category=category,mocks='admission/city/owner/heap')
u=fixture(0);put(u,AGES+4*0x34,2);put(u,AGES+4*0x34+8,99);u.mem_write(KNOWN+14,b'\x01')
check('late_age_missing_second_prerequisite',run(u,0x44eee0,AGE,[0]),0)
u.mem_write(KNOWN+99,b'\x01');check('late_age_all_prerequisites_no_middle_required',run(u,0x44eee0,AGE,[0]),4)
u=fixture(0);u.mem_write(KNOWN+10,b'\x00');check('no_age_enabled_fallback',run(u,0x44eee0,AGE,[0]),0)
u=fixture(0,kind=0);check('human_research_other_factor',run(u,0x475990,SCIENCE,[0]),175)
u=fixture();put(u,ADVANCES+0x74,1)
def wonder(uc,address,size,data):
 if address==0x4c1f70:uc.reg_write(UC_X86_REG_EDX,0);ret(uc,0)
 elif address==0x472940:ret(uc,40,8)
u.hook_add(UC_HOOK_CODE,wonder);check('wonder_deduction_precedes_discount',run(u,0x475990,SCIENCE,[0]),90,mocks='wonder mask/deduction=40')
u=fixture();put(u,PLAYERS,0);check('missing_player_maxint',run(u,0x475990,SCIENCE,[0]),0x7fffffff)
u=fixture(count=8);check('religion_if_eight_known',run(u,0x475990,SCIENCE,[0]),239)
u=fixture(count=9);check('theocracy_if_nine_known',run(u,0x475990,SCIENCE,[0]),261)
for age in [0,4]:
 u=fixture(age);put(u,0xa7dd18,ADB);put(u,ADB,1);put(u,ADVANCES+0x50,135)
 check('unit_db_base_era_'+str(age),run(u,0x531960,PROPERTY,[0,0]),135)
 u=fixture(age);put(u,0xa7dd1c,ADB);put(u,ADB,1);put(u,ADVANCES+0x38,360)
 check('building_db_base_era_'+str(age),run(u,0x523a90,PROPERTY,[0,0]),360)
for category,start,nextstep,rejected in [(1,0x48f7eb,0x48f7f7,0x4906df),(3,0x48fac8,0x48fad4,0x4906df),(9,0x48fc3f,0x48fc4b,0x48fded)]:
 for stock in [128,129,130]:
  u=fixture();put(u,NODE,129);put(u,PROPERTY,stock)
  u.reg_write(UC_X86_REG_EAX,NODE);u.reg_write(UC_X86_REG_EDI,PROPERTY)
  reached=[]
  def boundary(uc,address,size,data):
   if address in [nextstep,rejected]:reached.append(address);uc.emu_stop()
  u.hook_add(UC_HOOK_CODE,boundary);u.emu_start(start,STOP,count=20)
  check('completion_threshold_%s_%s'%(category,stock),reached,[rejected if stock<129 else nextstep],category=category,stock=stock,mocks='none; comparison segment only')
result=dict(engine_sha256=HASH,limitations=__doc__,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks)
print(json.dumps(result,indent=2))
if not all(c['passed'] for c in checks):raise SystemExit(1)
