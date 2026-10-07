"""Original happiness components; synthetic cities, armies and building records.

Government/unitpool/record lookups, location/World army lookup and detail UI are
mocks. Military flag getter, government getters and complete garrison component
execute original code. Caller cap is a valid internal range with explicit caller
registers. Building functions execute original loops; wonder percentages and
64-bit shift are mocks. These are not full happiness updates or game turns.
"""
from pathlib import Path
import hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
from ctp_x87 import ftol_stub
ENGINE=ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
HASH='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
assert hashlib.sha256(ENGINE.read_bytes()).hexdigest()==HASH
img=pefile.PE(str(ENGINE)).get_memory_mapped_image()
HAPPY,PLAYER,GOV,CITY,ARMY,UDATA,URECORD,DB,BRECORD,LIST,SWITCH,STACK=[0x30010000+i*0x8000 for i in range(12)]
STOP,OUT=0x300f0000,0x300f1000
def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def word(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
def getdbl(u,a):return struct.unpack('<d',u.mem_read(a,8))[0]
def ret(u,value,cleanup):
 sp=u.reg_read(UC_X86_REG_ESP);target=word(u,sp)
 u.reg_write(UC_X86_REG_EAX,value);u.reg_write(UC_X86_REG_ESP,sp+4+cleanup);u.reg_write(UC_X86_REG_EIP,target)
def fixture(flags=(),maximum=1,effect=1,threshold=80,world=True,penalty=0,bonus=0):
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(img)+4095)&~4095)
 u.mem_write(0x400000,img);u.mem_map(0x30000000,0x100000)
 u.reg_write(UC_X86_REG_FPCW,0x37f);u.mem_write(0x7256c6,ftol_stub())
 put(u,GOV+0xa0,maximum);dbl(u,GOV+0xa8,effect);put(u,GOV+0xb0,threshold)
 put(u,ARMY+0x30,len(flags))
 for i,flag in enumerate(flags):
  put(u,ARMY+4+i*4,i);put(u,UDATA+i*0x100+0x30,i);put(u,URECORD+i*0x100+0x34,flag)
 for a,v in [(DB+8,BRECORD),(DB+0x2c,2),(DB+0x30,1),(DB+0xf4,LIST),
             (DB+0xf8,LIST+8),(LIST,0),(LIST+4,1),(LIST+8,2),
             (BRECORD+0x68,2),(BRECORD+264+0x68,1),
             (BRECORD+2*264+0x100,SWITCH),(SWITCH,3),(SWITCH+4,5),
             (0xa7dd80,LIST+0x100),(0xa7ab08,LIST+0x200)]:put(u,a,v)
 def hook(uc,address,size,data):
  sp=uc.reg_read(UC_X86_REG_ESP)
  if address==0x455750:ret(uc,GOV,4)
  elif address==0x4da9a0:ret(uc,0,4)
  elif address==0x518a50:ret(uc,ARMY if world else 0,4)
  elif address==0x4b23e0:ret(uc,UDATA+word(uc,sp+4)*0x100,4)
  elif address==0x4542e0:ret(uc,URECORD+word(uc,sp+4)*0x100,4)
  elif address==0x4ac8a0:ret(uc,0,12)
  elif address==0x473360:ret(uc,penalty,8)
  elif address==0x474320:ret(uc,bonus,8)
  elif address==0x7257c0:
   value=(uc.reg_read(UC_X86_REG_EDX)<<32)|uc.reg_read(UC_X86_REG_EAX)
   value=(value<<(uc.reg_read(UC_X86_REG_ECX)&63))&((1<<64)-1)
   uc.reg_write(UC_X86_REG_EDX,value>>32);ret(uc,value&0xffffffff,0)
 u.hook_add(UC_HOOK_CODE,hook);return u
checks=[]
def check(name,got,expected):checks.append(dict(name=name,got=got,expected=expected,passed=got==expected))
for name,flags,maximum,effect,expected in [
 ('empty',(),4,1,0),('one', (0x200,),4,1,1),('mixed',(0x200,0,0x200),4,1,2),
 ('theocracy_cap',(0x200,)*4,1,1,1),('tyranny_cap',(0x200,)*6,4,1,4),
 ('none_allowed',(0x200,),0,1,0),('fascism',(0x200,)*3,2,2,4)]:
 u=fixture(flags,maximum,effect);put(u,STACK,STOP);put(u,STACK+4,CITY);put(u,STACK+8,PLAYER)
 u.mem_write(STOP,b'\xdd\x1d'+struct.pack('<I',OUT))
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,HAPPY)
 u.emu_start(0x4aad10,STOP+6,count=10000)
 check('garrison_'+name,getdbl(u,OUT),expected)
for happiness,expected,out in [(74,75,1),(79.5,80,1),(80,80,0),(85,85,0)]:
 u=fixture((0x200,)*4);dbl(u,HAPPY,happiness)
 ebp=STACK+0x400;put(u,ebp+0x10,OUT)
 for reg,val in [(UC_X86_REG_ESP,STACK),(UC_X86_REG_EBP,ebp),
                 (UC_X86_REG_ESI,HAPPY),(UC_X86_REG_EBX,PLAYER),(UC_X86_REG_EDI,CITY)]:u.reg_write(reg,val)
 u.emu_start(0x4aba60,0x4abad8,count=10000)
 check('cap_'+str(happiness),[getdbl(u,HAPPY),word(u,OUT)],[expected,out])
for bits,gov,expected in [(0,0,0),(1,0,2),(3,0,3),(4,0,3),(4,1,5),(7,1,8)]:
 u=fixture();put(u,STACK,STOP);put(u,STACK+4,bits);put(u,STACK+8,0);put(u,STACK+12,OUT);put(u,STACK+16,0)
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,DB)
 u.emu_start(0x45d1c0,STOP,count=10000);base=word(u,OUT)
 for off,val in [(0,STOP),(4,bits),(8,0),(12,gov),(16,OUT),(20,0)]:put(u,STACK+off,val)
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,DB)
 u.emu_start(0x45d3b0,STOP,count=10000)
 check('buildings_'+str((bits,gov)),base+word(u,OUT),expected)
report=dict(engine_sha256=HASH,limitations=__doc__,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks))
target=ROOT/'ANALYSE/BINAIR/happiness-defense-controls.json'
target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(passed=report['passed'],total=report['total'],failures=[c for c in checks if not c['passed']],output=str(target)),indent=2))
if report['passed']!=report['total']:raise SystemExit(1)
