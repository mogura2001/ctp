"""Original local pollution formula and AI repair action, synthetic fixtures.

No gameplay/binary writes. City calculation stops at the pollution field write,
before AI pact adjustments. Wonder/cleaner/history inputs are explicit mocks.
AI World/random/improvement actions are recorders, not real cleanup projects.
"""
from pathlib import Path
import sys,struct,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from ctp_x87 import ftol_stub
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
paths=['CTP-og/ctp_program/ctp/civctp.exe','CTP-og/ctp_program/ctp/dll/ai/robotcom.dll']
hashes=['b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79','3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44']
pes=[]
for p,h in zip(paths,hashes):
 p=ROOT/p;assert hashlib.sha256(p.read_bytes()).hexdigest()==h;pes.append(pefile.PE(str(p)))
CITY,CONST,PROFILE,PLAYERS,PLAYER,SCIENCE,KNOWN,ADB,ADVANCES,BDB,BUILDINGS,LIST,GOV,AIMAIN,REPAIR,NODE,TIME,WORLD,WV,IMP,IV,RNG,RV,PV,STACK=[0x30001000+i*0x3000 for i in range(25)]
STOP,CRT=0x300f0000,0x300f2000
def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def get(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
def ret(u,v,argc=0):
 sp=u.reg_read(UC_X86_REG_ESP);target=get(u,sp);u.reg_write(UC_X86_REG_EAX,v&0xffffffff)
 u.reg_write(UC_X86_REG_ESP,sp+4+argc);u.reg_write(UC_X86_REG_EIP,target)
def fixture():
 u=Uc(UC_ARCH_X86,UC_MODE_32)
 for p in pes:
  im=p.get_memory_mapped_image();base=p.OPTIONAL_HEADER.ImageBase;u.mem_map(base,(len(im)+4095)&~4095);u.mem_write(base,im)
 u.mem_map(0,4096);u.mem_map(0x30000000,0x100000);u.reg_write(UC_X86_REG_FPCW,0x37f)
 u.mem_write(CRT,ftol_stub());put(u,0x743330,CRT)
 for a,v in [(0xa7a6a4,PROFILE),(PROFILE+0x18,1),(0xa7dd48,CONST),(CONST+0x3a8,8),(CONST+0x3ac,300),
 (0xa7dd80,PLAYERS),(PLAYERS,PLAYER),(CITY+4,0),(PLAYER+0x12ec,SCIENCE),(SCIENCE+4,2),(SCIENCE+0x1c,KNOWN),
 (0xa7dd00,ADB),(ADB+8,ADVANCES),(0xa7dd1c,BDB),(BDB+8,BUILDINGS),(BDB+0x50,1),(BDB+0x118,LIST),(LIST,0),
 (0xa7dd34,GOV),(GOV,1),(GOV+8,GOV+0x100),(CITY+0x48,1)]:put(u,a,v)
 dbl(u,CONST+0x110,.5);dbl(u,CONST+0x118,.01);dbl(u,GOV+0x100+0x68,1)
 return u
def setup_run(u,start,this,args=()):
 put(u,STACK,STOP)
 for i,a in enumerate(args):put(u,STACK+4+i*4,a)
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,this)
def run(u,start,this,args=()):
 setup_run(u,start,this,args);u.emu_start(start,STOP,count=20000);return u.reg_read(UC_X86_REG_EAX)
checks=[]
def check(name,got,expected,**extra):checks.append(dict(name=name,got=got,expected=expected,passed=got==expected,**extra))
cases=[('size4',4,300,0,0,0,1,0),('size8',8,300,0,0,0,1,0),('size10',10,300,0,0,0,1,1),
 ('production400',4,400,0,0,0,1,1),('both',10,400,0,0,0,1,2),
 ('factory',10,400,1,0,0,1,4),('recycler_clamp',10,400,-2,0,0,1,0),
 ('tech_modifiers',10,400,0,1,1,1,4),('government3',10,400,0,0,0,3,6),
 ('additional_food',4,300,0,0,0,1,7)]
for name,pop,production,bonus,sm,pm,gov,expected in cases:
 u=fixture();put(u,CITY+0x58c,pop);put(u,CITY+0x3c,production);dbl(u,BUILDINGS+0xa0,bonus)
 u.mem_write(KNOWN,b'\x01\x00');put(u,ADVANCES+0x5c,sm);put(u,ADVANCES+0x60,pm);dbl(u,GOV+0x100+0x68,gov)
 if name=='additional_food':put(u,CITY+0x8c,7)
 def hook(uc,address,size,data):
  if address==0x7257c0:
   v=(uc.reg_read(UC_X86_REG_EAX)|(uc.reg_read(UC_X86_REG_EDX)<<32))<<(uc.reg_read(UC_X86_REG_ECX)&255)
   uc.reg_write(UC_X86_REG_EDX,(v>>32)&0xffffffff);ret(uc,v)
  elif address==0x4c1f70:uc.reg_write(UC_X86_REG_EDX,0);ret(uc,0)
  elif address in [0x472c10,0x472d00,0x472df0,0x4bbe30]:ret(uc,0,8 if address in [0x472c10,0x472d00,0x472df0] else 0)
  elif address==0x45d7b0:
   # explicit zero cleaner input; bonus sum remains original
   sp=uc.reg_read(UC_X86_REG_ESP);uc.mem_write(0x300f3000,bytes.fromhex('d9eec20800'));uc.reg_write(UC_X86_REG_EIP,0x300f3000)
 u.hook_add(UC_HOOK_CODE,hook);setup_run(u,0x4939e0,CITY);u.emu_start(0x4939e0,0x493c43,count=20000)
 check('city_'+name,get(u,CITY+0x80),expected,mocks='wonder/history/cleaner; real buildingbonus/techsum/government/formula; before AI pact')
for name,threshold,budget,rand,can,state,build,expected in [
 ('success',0,2300,99,1,0,1,[1,0,0,9]),('reserve_short',0,2299,99,1,0,1,[0,1,1,None]),
 ('dirty_threshold',1,5000,99,1,0,1,[0,1,1,None]),('request_fails',0,5000,99,1,0,0,[1,1,1,9]),
 ('legal_state_blocks',0,5000,99,1,1,1,[0,1,1,None]),('random_parameter4',0,5000,0,1,0,1,[1,0,0,4])]:
 u=fixture();calls=[]
 for a,v in [(REPAIR+4,1),(REPAIR+8,1),(REPAIR+0xc,NODE),(REPAIR+0x10,NODE),(NODE+8,10),(NODE+0xc,10),
 (AIMAIN+0x84,TIME),(AIMAIN+0x2c,PLAYER),(PLAYER,PV),(PV+0x94,0x300e0100),
 (AIMAIN+0x30,WORLD),(WORLD,WV),(WV+0x34,0x300e0110),(WV+0x64,0x300e0120),
 (AIMAIN+0x50,IMP),(IMP,IV),(IV+0x1c,0x300e0130),(IV+0x20,0x300e0140),(IV+0x18,0x300e0150),
 (AIMAIN+0x58,RNG),(RNG,RV),(RV+0xc,0x300e0160),(AIMAIN+0xa0,0)]:put(u,a,v)
 dbl(u,TIME,10);dbl(u,0x200c6900,threshold)
 def ai_hook(uc,address,size,data):
  if address==0x20085dc0:uc.reg_write(UC_X86_REG_EIP,CRT)
  elif address==0x300e0100:ret(uc,budget,4)
  elif address==0x300e0110:ret(uc,0,8)
  elif address==0x300e0120:ret(uc,0,8)
  elif address==0x300e0130:ret(uc,300,16)
  elif address==0x300e0140:
   sp=uc.reg_read(UC_X86_REG_ESP);put(uc,get(uc,sp+20),state);ret(uc,can,20)
  elif address==0x300e0150:
   sp=uc.reg_read(UC_X86_REG_ESP);calls.append(get(uc,sp+12));ret(uc,build,16)
  elif address==0x300e0160:ret(uc,rand,8)
  elif address==0x20026b80:ret(uc,0)
 u.hook_add(UC_HOOK_CODE,ai_hook);run(u,0x20057ae0,REPAIR,[AIMAIN])
 check('AI_'+name,[len(calls),get(u,REPAIR+4),get(u,REPAIR+8),calls[0] if calls else None],expected,mocks='Playerbudget/Worldowner/random/Improvementcost/legalstate/action/delete')
result=dict(hashes=hashes,checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks),limits='local pollution field only before AI pacts; synthetics and explicit inputs/actions; no completed cleanup or world catastrophe',x87='PC64 nearest/CW-preserving FTOL')
(ROOT/'ANALYSE/BINAIR/pollution-late-controls.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2));sys.exit(0 if result['passed']==len(checks) else 1)
