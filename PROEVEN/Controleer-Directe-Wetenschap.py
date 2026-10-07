"""Original CityData direct-science sum and Player extra-science accumulator.

Synthetic city/population/building/government records. Population science,
unit owner and three wonder percentages use explicit mocks; actual building
science-per-pop aggregation, Government getter and arithmetic execute original
instructions. Imported ftol uses x87 truncation. No full Player loop, parser,
placement, happiness or game turn is simulated.
"""
from pathlib import Path
import hashlib,json,math,struct,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from ctp_x87 import ftol_stub
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
p=ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
HASH='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
assert hashlib.sha256(p.read_bytes()).hexdigest()==HASH
pe=pefile.PE(str(p));image=pe.get_memory_mapped_image()
CITY,PLAYER,PLAYERS,POPS,GOVDB,GOV,BUILDDB,RECORDS,INDICES,STACK=[0x30010000+i*0x8000 for i in range(10)]
STOP=0x300f0000

def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
def word(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def fixture():
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(image)+4095)&~4095)
 u.mem_write(0x400000,image);u.mem_map(0x30000000,0x100000);u.reg_write(UC_X86_REG_FPCW,0x37f)
 for a,v in [(0xa7dd80,PLAYERS),(PLAYERS,PLAYER),(0xa7dd34,GOVDB),(GOVDB,1),(GOVDB+8,GOV),
              (0xa7dd1c,BUILDDB),(BUILDDB+8,RECORDS),(BUILDDB+0x1a0,INDICES),(CITY+0x590,POPS)]:put(u,a,v)
 u.mem_write(0x300f2000,ftol_stub());put(u,0x743330,0x300f2000)
 return u

def direct(bonuses,perpop=(),knowledge=0,government=1,flat=0,citywonder=0,popwonder=0,empirewonder=0):
 u=fixture();put(u,CITY+0x58c,len(bonuses));put(u,BUILDDB+0xd8,len(perpop));owned=0
 for i,(index,bonus) in enumerate(perpop):
  put(u,INDICES+i*4,index);dbl(u,RECORDS+index*0x108+0xf0,bonus);owned|=1<<index
 put(u,CITY+0x48,owned);put(u,CITY+0x4c,owned>>32);put(u,CITY+0x3b0,flat)
 dbl(u,CITY+0x3e0,knowledge);dbl(u,GOV+0x60,government)
 def ret(v,argbytes=0):
  sp=u.reg_read(UC_X86_REG_ESP);target=word(u,sp)
  u.reg_write(UC_X86_REG_EAX,v&0xffffffff);u.reg_write(UC_X86_REG_ESP,sp+4+argbytes);u.reg_write(UC_X86_REG_EIP,target)
 def hook(uc,address,size,data):
  if address==0x4ccc50:ret(bonuses[(uc.reg_read(UC_X86_REG_ECX)-POPS)//4])
  elif address==0x4da960:ret(0)
  elif address in (0x473c70,0x474230,0x4722b0):ret({0x473c70:citywonder,0x474230:popwonder,0x4722b0:empirewonder}[address],8)
 u.hook_add(UC_HOOK_CODE,hook)
 put(u,STACK,STOP);u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,CITY)
 u.emu_start(0x49e7b0,STOP,count=20000);value=u.reg_read(UC_X86_REG_EAX)
 # Execute the actual Player accumulator twice, to verify addition to existing state.
 put(u,PLAYER+0x11e4,7)
 for _ in range(2):
  put(u,STACK,STOP);put(u,STACK+4,value)
  u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,PLAYER)
  u.emu_start(0x4bb530,STOP,count=100)
 return value,word(u,PLAYER+0x11e4)

checks=[]
for name,bonuses,perpop,k,g,f,cw,pw,ew in [
 ('empty',[],(),0,1,0,0,0,0),('ordinary_no_buildings',[0]*8,(),0,1,0,0,0,0),
 ('scientists_no_buildings',[0,0]+[10]*6,(),0,1,0,0,0,0),
 ('academy_theocracy',[0,0]+[10]*6,((0,.5),),.5,1.25,0,0,0,0),
 ('academy_tyranny',[0,0]+[10]*6,((0,.5),),.5,1,0,0,0,0),
 ('library_record',[0,0]+[10]*6,((0,.5),),.25,1.25,0,0,0,0),
 ('university_only',[0,0]+[10]*6,(),.5,1.25,0,0,0,0),
 ('academy_university',[0,0]+[10]*6,((0,.5),),1,1.25,0,0,0,0),
 ('two_perpop_high_mask',[0,0]+[10]*6,((0,.5),(33,.5)),.75,1.25,0,0,0,0),
 ('fractional_perpop',[0,0,10],((0,.5),),.5,1.25,0,0,0,0),
 ('flat_science',[0,10],(),.5,1.25,3,0,0,0),
 ('empire_knowledge',[0,0]+[10]*6,((0,.5),),.5,1.25,0,0,0,10),
 ('citizen_and_specialist_percent',[0,0]+[10]*6,((0,.5),),.5,1.25,0,50,25,0),
]:
 base=sum(b+math.trunc(b*(cw+pw)/100) for b in bonuses)+math.trunc(len(bonuses)*sum(v for i,v in perpop))+f
 base+=math.trunc(base*k);base=math.trunc(base*g);expected=base+math.trunc(base*ew/100)
 got=direct(bonuses,perpop,k,g,f,cw,pw,ew)
 checks.append(dict(name=name,bonuses=bonuses,science_per_pop=perpop,knowledge=k,government=g,flat=f,
                    city_wonder=cw,pop_wonder=pw,empire_wonder=ew,got=got,expected=[expected,7+2*expected],passed=got==(expected,7+2*expected)))
print(json.dumps(dict(engine_sha256=HASH,limitations=__doc__,checks=checks,
                     passed=sum(c['passed'] for c in checks),total=len(checks)),indent=2))
if not all(c['passed'] for c in checks):raise SystemExit(1)
