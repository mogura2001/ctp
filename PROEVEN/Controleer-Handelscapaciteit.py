"""Original CTP I free-route predicate and capacity accounting; synthetic fixtures.

No game/binary writes. Route-pool and UI/action callbacks are explicit mocks.
Wonder record/obsolete/known lookup and capacity formula execute real code.
The CRT shift and FTOL substitutes preserve their calling conventions/x87 CW.
"""
from pathlib import Path
import hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from ctp_x87 import ftol_stub
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
P=ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
HASH='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
assert hashlib.sha256(P.read_bytes()).hexdigest()==HASH
pe=pefile.PE(str(P));image=pe.get_memory_mapped_image()
PLAYER,DB,RECORDS,LIST,PLAYERS,FOREIGN,SCIENCE,KNOWN,ROUTE,HANDLE,OUT,STACK=[0x30010000+i*0x4000 for i in range(12)]
STOP=0x300f0000
def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def get(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def ret(u,v,argc=0):
 sp=u.reg_read(UC_X86_REG_ESP);target=get(u,sp)
 u.reg_write(UC_X86_REG_EAX,v&0xffffffff);u.reg_write(UC_X86_REG_ESP,sp+4+argc);u.reg_write(UC_X86_REG_EIP,target)
def fixture(total=1,used=0,own=True,obsolete=True,known=False):
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(image)+4095)&~4095);u.mem_write(0x400000,image)
 u.mem_map(0,4096);u.mem_map(0x30000000,0x100000);u.reg_write(UC_X86_REG_FPCW,0x37f)
 for a,v in [(PLAYER,0),(PLAYER+0x98,total),(PLAYER+0x9c,used),(PLAYER+0x1170,4 if own else 0),
 (0xa7dd5c,DB),(DB,3),(DB+8,RECORDS),(DB+0x94,1),(DB+0x26c,LIST),(LIST,2),
 (RECORDS+2*0xd0+0x2c,1 if obsolete else 0),(RECORDS+2*0xd0+0xc,7),
 (0xa7dd80,PLAYERS),(PLAYERS,PLAYER),(PLAYERS+4,FOREIGN),(FOREIGN+0x12ec,SCIENCE),(SCIENCE+0x1c,KNOWN),
 (HANDLE,123),(ROUTE+0x24,0),(ROUTE+0xc4,1),(0xa44c9c,0),(0xa44c98,0)]:put(u,a,v)
 u.mem_write(KNOWN+7,bytes([known]));u.mem_write(0x300f2000,ftol_stub());put(u,0x743330,0x300f2000)
 calls=[]
 def hook(uc,address,size,data):
  if address==0x7257c0:
   v=(uc.reg_read(UC_X86_REG_EAX)|(uc.reg_read(UC_X86_REG_EDX)<<32)) << (uc.reg_read(UC_X86_REG_ECX)&255)
   uc.reg_write(UC_X86_REG_EDX,(v>>32)&0xffffffff);ret(uc,v)
  elif address in [0x4b23c0,0x4b2380]:ret(uc,ROUTE,4)
  elif address==0x6af2f4:ret(uc,0)
  elif address==0x4d5440:calls.append('capacity_notification');ret(uc,0,4)
  elif address==0x4d6eb0:calls.append('rollback_delete');ret(uc,0,4)
 u.hook_add(UC_HOOK_CODE,hook)
 return u,calls
def run(u,start,this,args=()):
 put(u,STACK,STOP)
 for i,a in enumerate(args):put(u,STACK+4+i*4,a)
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,this)
 u.emu_start(start,STOP,count=20000)
 v=u.reg_read(UC_X86_REG_EAX);return v if v<0x80000000 else v-0x100000000
checks=[]
def check(name,got,expected,**extra):checks.append(dict(name=name,got=got,expected=expected,passed=got==expected,**extra))
u,c=fixture()
def token(uc,address,size,data):
 if address==0x521b90:ret(uc,487)
u.hook_add(UC_HOOK_CODE,token)
check('free_flag_parser487',[run(u,0x4705c0,RECORDS,[HANDLE,OUT]),get(u,RECORDS+0x30),get(u,RECORDS+0x34)],[1,0,1],mocks='token487 and CRT64shift')
u,c=fixture();put(u,RECORDS+0x34,2);u.reg_write(UC_X86_REG_EBX,RECORDS)
u.emu_start(0x46bb01,0x46bb0a,count=10)
check('trader_parser103_case36',get(u,RECORDS+0x34),0x102)
for total,used in [(0,0),(1,0),(1,1),(1,3),(10,4)]:
 u,c=fixture(total,used);check('unused_%s_%s'%(total,used),run(u,0x4b9c70,PLAYER),total-used)
for name,own,obsolete,known,expected in [('no_wonder',False,True,False,0),('active',True,True,False,1),('foreign_obsoletes',True,True,True,0),('no_obsolete',True,False,True,1)]:
 u,c=fixture(own=own,obsolete=obsolete,known=known)
 check('free_'+name,run(u,0x473280,DB,[4 if own else 0,0]),expected,mocks='CRT64shift only; record/known getters original')
for name,total,used,own,known,active,result,counter,deleted in [
 ('last_ordinary',1,0,False,False,True,123,1,False),
 ('ordinary_overflow',1,1,False,False,True,0,1,True),
 ('free_overflow',1,1,True,False,True,123,2,False),
 ('free_without_caravan',0,0,True,False,True,123,1,False),
 ('foreign_obsolete_blocks',0,0,True,True,True,0,0,True),
 ('inactive_route',2,0,True,False,False,0,0,True)]:
 u,c=fixture(total,used,own=own,known=known);put(u,ROUTE+0xc4,int(active))
 run(u,0x4b9fb0,PLAYER,[OUT,HANDLE])
 check('charge_'+name,[get(u,OUT),get(u,PLAYER+0x9c),'rollback_delete' in c],[result,counter,deleted],mocks='route-pool/UI/notification/delete; original free predicate and routecost')
for name,payer,guard,expected in [('matching',0,0,2),('other_payer',1,0,3),('guarded',0,1,3)]:
 u,c=fixture(total=1,used=3);put(u,ROUTE+0x24,payer);put(u,ROUTE+0x140,guard)
 run(u,0x4ba360,PLAYER,[123]);check('release_'+name,[get(u,PLAYER+0x9c),get(u,PLAYER+0x98)],[expected,1],mocks='route-pool/UI only; original routecost')
for value,expected in [(1.,1),(2.,2),(0.,0)]:
 u,c=fixture(total=0);u.mem_write(RECORDS+0xa0,struct.pack('<d',value))
 def lookup(uc,address,size,data):
  if address==0x4542e0:ret(uc,RECORDS,4)
 u.hook_add(UC_HOOK_CODE,lookup)
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_EDI,PLAYER);u.reg_write(UC_X86_REG_EBX,0)
 u.emu_start(0x4b53b6,0x4b53d2,count=100)
 check('trader_capacity_'+str(value),get(u,PLAYER+0x98),expected,mocks='recordlookup; executes actual post-trader-segment only, not full createunit')
result=dict(engine_sha256=HASH,checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks),runtime_limit='synthetic objects; no scheduler/game turns/network/cityroute eligibility',x87='PC64 nearest; CW-preserving FTOL; integer routecost1')
(ROOT/'ANALYSE/BINAIR/trade-capacity-labyrinth-controls.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2));sys.exit(0 if result['passed']==len(checks) else 1)
