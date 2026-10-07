"""Original engine fragments: city-count penalty, normal size penalty, WGF.

Synthetic state; government lookup, valid-city/popcount and UI/detail callbacks
are mocks. Size cases mock wonder/building offsets0. WGF/size are valid internal
instruction ranges with explicit caller registers, not full happiness updates.
"""
from pathlib import Path
import hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
ENGINE=ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
HASH='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
assert hashlib.sha256(ENGINE.read_bytes()).hexdigest()==HASH
img=pefile.PE(str(ENGINE)).get_memory_mapped_image()
HAPPY,PLAYER,GOV,ARRAY,HANDLES,PROPS,CITY,WGF,STACK=[0x30010000+i*0x8000 for i in range(9)]
STOP,OUT=0x300f0000,0x300f1000
def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def word(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
def getdbl(u,a):return struct.unpack('<d',u.mem_read(a,8))[0]
def ret(u,value,cleanup):
 sp=u.reg_read(UC_X86_REG_ESP);target=word(u,sp)
 u.reg_write(UC_X86_REG_EAX,value);u.reg_write(UC_X86_REG_ESP,sp+4+cleanup);u.reg_write(UC_X86_REG_EIP,target)
def fixture(sizes=()):
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(img)+4095)&~4095)
 u.mem_write(0x400000,img);u.mem_map(0x30000000,0x100000);u.mem_map(0,0x1000)
 u.reg_write(UC_X86_REG_FPCW,0x37f)
 for a,v in [(PLAYER+0x12c0,ARRAY),(ARRAY+8,len(sizes)),(ARRAY+0xc,HANDLES),
             (PLAYER+0x12e8,PROPS),(PLAYER+0x1318,WGF)]:put(u,a,v)
 def hook(uc,address,size,data):
  sp=uc.reg_read(UC_X86_REG_ESP)
  if address==0x455750:ret(uc,GOV,4)
  elif address==0x4b2300:ret(uc,1,4)
  elif address==0x4dc570:
   i=(uc.reg_read(UC_X86_REG_ECX)-HANDLES)//4
   put(uc,word(uc,sp+4),sizes[i]);ret(uc,0,4)
  elif address==0x53ca30:ret(uc,0,12)
  elif address==0x55bcf0:ret(uc,0,0)
  elif address==0x4ac8a0:ret(uc,0,12)
  elif address in (0x472fc0,0x45daf0):ret(uc,0,8)
 u.hook_add(UC_HOOK_CODE,hook)
 return u
checks=[]
def check(name,got,expected,mocks):
 checks.append(dict(name=name,got=got,expected=expected,passed=got==expected,mocks=mocks))
for threshold,n,zero,expected in [(10,10,0,0),(10,25,0,-7.5),(20,25,0,-2.5),
                                (40,30,0,0),(40,42,0,-1),(10,12,2,0),(10,0,0,0)]:
 u=fixture([0]*zero+[1]*(n-zero));put(u,GOV+0x140,threshold);dbl(u,GOV+0x148,.5)
 put(u,STACK,STOP);put(u,STACK+4,PLAYER)
 u.mem_write(STOP,b'\xdd\x1d'+struct.pack('<I',OUT))
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,HAPPY)
 u.emu_start(0x4aa5c0,STOP+6,count=20000)
 check('city_count_'+str((threshold,n,zero)),getdbl(u,OUT),expected,
       ['government lookup','all handles valid','city size outputs','UI/detail callbacks'])
for population,expected in [(1,0),(4,-3),(8,-7),(10,-9)]:
 u=fixture();put(u,CITY+0x38,population);dbl(u,PROPS,1);dbl(u,PROPS+8,1);dbl(u,HAPPY,75)
 for reg,val in [(UC_X86_REG_EBP,STACK+0x400),(UC_X86_REG_ESP,STACK),
                 (UC_X86_REG_ESI,HAPPY),(UC_X86_REG_EBX,PLAYER),(UC_X86_REG_EDI,CITY)]:u.reg_write(reg,val)
 u.emu_start(0x4ab54a,0x4ab666,count=1000)
 check('size_penalty_'+str(population),[getdbl(u,HAPPY+0x18),getdbl(u,HAPPY)],
       [expected,75+expected],['wonder/building size offsets0','detail callback','caller registers'])
for pop,work,wage,ration,expected in [
 (4,-1,-1,-1,0),(4,-2,-1,-1,-4),(8,-2,-1,-1,-8),
 (4,-1,-2,-1,-4),(4,-1,-1,-2,-4),(4,0,-1,-1,2),
 (4,-2,0,-1,0),(4,0,0,0,2)]:
 u=fixture();put(u,CITY+0x38,pop);put(u,CITY+0x58c,pop)
 put(u,WGF+0x50,work);put(u,WGF+0x4c,wage);put(u,WGF+0x48,ration)
 for off,val in [(0x30,1),(0x38,-1),(0x40,1),(0x48,-1),(0x50,1),(0x58,-1)]:dbl(u,GOV+off,val)
 dbl(u,HAPPY,75)
 for reg,val in [(UC_X86_REG_EBP,STACK+0x400),(UC_X86_REG_ESP,STACK),
                 (UC_X86_REG_ESI,HAPPY),(UC_X86_REG_EBX,PLAYER),(UC_X86_REG_EDI,CITY)]:u.reg_write(reg,val)
 # Start after the preceding callback's FSTP at4ab7c7; ECX is its caller's Player.
 u.reg_write(UC_X86_REG_ECX,PLAYER)
 u.emu_start(0x4ab7c9,0x4aba1e,count=2000)
 check('wgf_'+str((pop,work,wage,ration)),getdbl(u,HAPPY),75+expected,
       ['government lookup','caller registers/contentment population','detail callbacks'])
report=dict(engine_sha256=HASH,limitations=__doc__,checks=checks,
            passed=sum(c['passed'] for c in checks),total=len(checks))
target=ROOT/'ANALYSE/BINAIR/happiness-wgf-controls.json'
target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(passed=report['passed'],total=report['total'],
                      failures=[c for c in checks if not c['passed']],output=str(target)),indent=2))
if report['passed']!=report['total']:raise SystemExit(1)
