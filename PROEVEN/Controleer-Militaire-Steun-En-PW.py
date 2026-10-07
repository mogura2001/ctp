"""Read-only original x86 support/PW calculations with synthetic records.

Mocks: unit/record lookup, wonder percentage, gross city production and city
handle resolution. Whole-player checks bypass the shortage callback using the
existing Player+1194 flag; they do not prove shortage, disbanding or a full turn.
CRT ftol/ceil substitutes preserve x87 CW. No CTP binary is edited.
"""
from pathlib import Path
import hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from ctp_x87 import ftol_stub,ceil_stub
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
ENGINE=ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
HASH='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
assert hashlib.sha256(ENGINE.read_bytes()).hexdigest()==HASH
img=pefile.PE(str(ENGINE)).get_memory_mapped_image()
CITY,PLAYER,PLAYERS,UNIT,UNITDATA,RECORD,GOV,READY,ARRAY,HANDLES,PW,STACK=[0x30010000+i*0x8000 for i in range(12)]
STOP,OUT=0x300f0000,0x300f1000
def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def word(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def signed(u,a):return struct.unpack('<i',u.mem_read(a,4))[0]
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
def getdbl(u,a):return struct.unpack('<d',u.mem_read(a,8))[0]
def fixture():
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(img)+4095)&~4095)
 u.mem_write(0x400000,img);u.mem_map(0x30000000,0x100000);u.mem_map(0,0x1000)
 u.reg_write(UC_X86_REG_FPCW,0x37f)
 u.mem_write(0x300f2000,ftol_stub());put(u,0x743330,0x300f2000)
 u.mem_write(0x300f3000,ceil_stub());put(u,0x743344,0x300f3000)
 for a,v in [(0xa7dd80,PLAYERS),(PLAYERS,PLAYER),(PLAYER+0x1314,READY),
             (PLAYER+0x12c0,ARRAY),(ARRAY+0xc,HANDLES),(PLAYER+0x12f0,PW)]:put(u,a,v)
 return u
def ret(u,value,cleanup):
 sp=u.reg_read(UC_X86_REG_ESP);target=word(u,sp)
 u.reg_write(UC_X86_REG_EAX,value);u.reg_write(UC_X86_REG_ESP,sp+4+cleanup);u.reg_write(UC_X86_REG_EIP,target)
def run(u,address,obj,args=b'',floating=False):
 put(u,STACK,STOP);u.mem_write(STACK+4,args or b'\0')
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,obj)
 if floating:u.mem_write(STOP,b'\xdd\x1d'+struct.pack('<I',OUT))
 u.emu_start(address,STOP+6 if floating else STOP,count=20000)
 return getdbl(u,OUT) if floating else u.reg_read(UC_X86_REG_EAX)
checks=[]
def check(name,got,expected,mocks=()):
 checks.append(dict(name=name,got=got,expected=expected,passed=got==expected,mocks=list(mocks)))

for state,flag,exempt,instance,hunger,wonder,expected in [
 (0,0,0,0,10,0,1),(1,0,0,0,10,0,5),(2,0,0,0,10,0,10),
 (0,0x100,0,0,10,0,10),(2,0,0x1000,0,10,0,0),
 (2,0,0,0x100,10,0,0),(2,0,0,0,10,75,2.5),
 (2,0,0,0,0,0,0),(3,0,0,0,10,0,0)]:
 u=fixture();put(u,READY+0x20,state);put(u,RECORD+0x40,flag)
 put(u,RECORD+0x34,exempt);put(u,UNITDATA+0x44,instance);put(u,RECORD+0xbc,hunger)
 for offset,val in [(0x100,.1),(0x110,.5),(0x120,1)]:dbl(u,GOV+offset,val)
 def hook(uc,address,size,data):
  if address in (0x4b23e0,0x4542e0,0x455750,0x471fe0):
   value={0x4b23e0:UNITDATA,0x4542e0:RECORD,0x455750:GOV,0x471fe0:wonder}[address]
   ret(uc,value,8 if address==0x471fe0 else 4)
 u.hook_add(UC_HOOK_CODE,hook)
 got=run(u,0x4cf080,READY,struct.pack('<I',UNIT),True)
 check('unit_'+str((state,flag,exempt,instance,hunger,wonder)),got,expected,
       ['unit pool lookup','unit/government record lookup','wonder percentage'])

for production,ratio,tax,sflag,pflag,expected in [
 (100,.2,.2,1,1,[20,16,64]),(7,.2,.2,1,1,[2,1,4]),
 (100,.2,.2,0,1,[0,20,80]),(100,.2,.2,1,0,[20,0,80]),
 (0,.2,.2,1,1,[0,0,0]),(3,.5,1,1,1,[2,1,0])]:
 u=fixture();put(u,CITY+0x40,production);put(u,CITY+0x98,sflag);put(u,CITY+0x94,pflag)
 run(u,0x494870,CITY,struct.pack('<dIdI',ratio,OUT,tax,OUT+4))
 check('ordinary_city_'+str((production,ratio,tax,sflag,pflag)),
       [signed(u,OUT),signed(u,OUT+4),signed(u,CITY+0x40)],expected)

for production,residue,tax,expected in [(100,20,.2,[16,64]),(1,3,.2,[0,0]),
                                        (3,-1,.25,[1,3]),(7,2,.2,[1,4])]:
 u=fixture();put(u,CITY+0x40,production)
 run(u,0x494900,CITY,struct.pack('<IdI',residue&0xffffffff,tax,OUT))
 check('last_city_'+str((production,residue,tax)),[signed(u,OUT),signed(u,CITY+0x40)],expected)

for value,expected in [(0,0),(.257,.25),(.5,.5),(1,1),(-.1,.5),(1.1,.5)]:
 u=fixture();dbl(u,PLAYER+0x1160,.5)
 def hook(uc,address,size,data):
  if address==0x546ed0:ret(uc,0,4) # UI refresh only
 u.hook_add(UC_HOOK_CODE,hook)
 run(u,0x4bb380,PLAYER,struct.pack('<d',value))
 check('pw_tax_'+str(value),getdbl(u,PLAYER+0x1160),expected,['UI refresh','network globals zero'])

for productions,support,tax,expected in [
 ([100,100],40,.2,[128,32,[64,64]]),
 # Each ordinary city pays ceil(7*4/21)=2; last owes0 but still pays PW1.
 ([7,7,7],4,.2,[14,3,[4,4,6]]),
 ([1,1,1],1,0,[2,0,[0,0,2]]),
 ([100],20,.2,[64,16,[64]])]:
 u=fixture();put(u,ARRAY+8,len(productions));put(u,PLAYER+0x1194,1)
 dbl(u,READY+0x10,support);dbl(u,PLAYER+0x1160,tax)
 for i,p in enumerate(productions):
  c=CITY+i*0x1000;put(u,HANDLES+4*i,i);put(u,c+0x40,p);put(u,c+0x98,1);put(u,c+0x94,1)
 def hook(uc,address,size,data):
  if address not in (0x4dc900,0x4dc930,0x4dc970):return
  i=(uc.reg_read(UC_X86_REG_ECX)-HANDLES)//4;sp=uc.reg_read(UC_X86_REG_ESP)
  if address==0x4dc900:
   put(uc,word(uc,sp+4),1);put(uc,word(uc,sp+8),1);ret(uc,productions[i],8)
  else:
   uc.reg_write(UC_X86_REG_ECX,CITY+i*0x1000)
   uc.reg_write(UC_X86_REG_EIP,0x494870 if address==0x4dc930 else 0x494900)
 u.hook_add(UC_HOOK_CODE,hook);run(u,0x4b7dd0,PLAYER)
 remaining=[signed(u,CITY+i*0x1000+0x40) for i in range(len(productions))]
 check('player_allocation_'+str((productions,support,tax)),
       [sum(remaining),signed(u,PW),remaining],expected,
       ['gross city production/eligibility','city handle resolution','shortage callback bypass flag'])

report=dict(engine_sha256=HASH,limitations=__doc__,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks)
target=ROOT/'ANALYSE/BINAIR/economy-readiness-pw-checks.json'
target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(passed=report['passed'],total=report['total'],
                      failures=[c for c in checks if not c['passed']],output=str(target)),indent=2))
if report['passed']!=report['total']:raise SystemExit(1)
