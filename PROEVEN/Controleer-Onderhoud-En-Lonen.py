"""Read-only original engine checks of upkeep sums, wages and ledger effects.

Synthetic records. Wages population exclusion uses an explicit record-flag
mock (0x4cc940); cash lookup is mocked. No complete turn or unpaid-wage loop.
"""
from pathlib import Path
import hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from ctp_x87 import ftol_stub
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
ENGINE=ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
HASH='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
assert hashlib.sha256(ENGINE.read_bytes()).hexdigest()==HASH
img=pefile.PE(str(ENGINE)).get_memory_mapped_image()
CITY,PLAYER,PLAYERS,POPS,DB,RECORDS,LEDGER,WGF,CONST,STACK=[0x30010000+i*0x8000 for i in range(10)]
STOP=0x300f0000
def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def word(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def signed(u,a):return struct.unpack('<i',u.mem_read(a,4))[0]
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
def fixture():
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(img)+4095)&~4095)
 u.mem_write(0x400000,img);u.mem_map(0x30000000,0x100000)
 u.reg_write(UC_X86_REG_FPCW,0x37f)
 u.mem_write(0x300f2000,ftol_stub());put(u,0x743330,0x300f2000)
 for a,v in [(0xa7dd80,PLAYERS),(PLAYERS,PLAYER),(PLAYER+0x12dc,LEDGER),
             (0xa7dd48,CONST),(DB+8,RECORDS),(CITY+0x590,POPS)]:put(u,a,v)
 return u
def run(u,address,obj,args=()):
 put(u,STACK,STOP)
 for i,v in enumerate(args):put(u,STACK+4+i*4,v)
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,obj)
 u.emu_start(address,STOP,count=10000)
 return u.reg_read(UC_X86_REG_EAX)
checks=[]
for name,records,owned,threshold,expected in [
 ('empty',[],0,0,0),('academy_library',[(0,4),(1,6)],3,0,10),
 ('strict_free_threshold',[(0,4),(1,6)],3,4,6),
 ('high_bit',[(0,4),(33,12)],(1<<33)|1,0,16),
 ('unowned',[(0,4),(1,6)],1,0,4),
]:
 u=fixture();put(u,DB,34)
 for index,cost in records:put(u,RECORDS+index*0x108+0x3c,cost)
 got=run(u,0x45cc70,DB,(owned&0xffffffff,owned>>32,threshold))
 checks.append(dict(name=name,got=got,expected=expected,passed=got==expected,mocks=[]))
for name,flags,wage,free,cash,expected in [
 ('four_paid',[0]*4,4,False,100,[16,0,84,16]),
 ('excluded_two',[0,8,0,8],4,False,100,[8,0,92,8]),
 ('free_one',[0]*4,4,True,100,[12,0,88,12]),
 ('all_excluded',[8]*4,4,False,100,[0,0,100,0]),
 ('insufficient_cash',[0]*4,4,False,10,[16,1,10,0]),
 ('exact_cash',[0]*4,4,False,16,[16,0,0,16]),
]:
 u=fixture();put(u,CITY+0x58c,len(flags));put(u,CITY+0xe8,int(free));put(u,LEDGER,cash)
 def hook(uc,address,size,data):
  if address not in (0x4cc940,0x4c2340):return
  value=flags[(uc.reg_read(UC_X86_REG_ECX)-POPS)//4] if address==0x4cc940 else word(uc,LEDGER)
  sp=uc.reg_read(UC_X86_REG_ESP);target=word(uc,sp)
  uc.reg_write(UC_X86_REG_EAX,value);uc.reg_write(UC_X86_REG_ESP,sp+4);uc.reg_write(UC_X86_REG_EIP,target)
 u.hook_add(UC_HOOK_CODE,hook);run(u,0x497a50,CITY,(wage,))
 got=[word(u,CITY+0x418),word(u,CITY+0x9c),word(u,LEDGER),signed(u,LEDGER+0x18)]
 checks.append(dict(name=name,got=got,expected=expected,passed=got==expected,
                    mocks=['population record flag8','cash getter']))
for stand in [-2,0,2]:
 u=fixture();dbl(u,CONST+0x140,1);dbl(u,CONST+0x148,4)
 run(u,0x4cb920,WGF,(stand,));got=struct.unpack('<d',u.mem_read(WGF+0x10,8))[0]
 checks.append(dict(name='wage_slider_'+str(stand),got=got,expected=4+stand,passed=got==4+stand,mocks=[]))
for kind,factor,cw,expected in [(1,1,0x37f,[100,100]),(1,1.2,0x37f,[119,119]),
                              (1,1.2,0x27f,[120,120]),(1,.5,0x37f,[50,50]),(0,1.2,0x37f,[100,100])]:
 u=fixture();put(u,PLAYER+4,kind);put(u,LEDGER,100);put(u,LEDGER+4,100);put(u,LEDGER+8,100)
 u.reg_write(UC_X86_REG_FPCW,cw)
 put(u,0xa7dd54,DB);put(u,0xa7a6a4,CONST);put(u,CONST,0);dbl(u,DB+0x1a0,factor)
 # This follows a city income of100 with no other ledger components.
 def difficulty(uc,address,size,data):
  if address!=0x44eee0:return
  sp=uc.reg_read(UC_X86_REG_ESP);target=word(uc,sp)
  uc.reg_write(UC_X86_REG_EAX,0);uc.reg_write(UC_X86_REG_ESP,sp+8);uc.reg_write(UC_X86_REG_EIP,target)
 u.hook_add(UC_HOOK_CODE,difficulty)
 u.reg_write(UC_X86_REG_ESI,PLAYER);u.reg_write(UC_X86_REG_EBP,STACK+0x400)
 u.reg_write(UC_X86_REG_ESP,STACK);u.emu_start(0x4b7a2d,0x4b7ac4,count=1000)
 got=[word(u,LEDGER),word(u,LEDGER+8)]
 checks.append(dict(name='income_adjust_'+str(kind)+'_'+str(factor)+'_'+hex(cw),got=got,expected=expected,passed=got==expected,
                    precision_note='binary64 1.2 lies below exact6/5; 64-bit significand retains product below120, 53-bit rounds to120',
                    mocks=['difficulty record index0','network globals0','era index0']))
report=dict(engine_sha256=HASH,limitations=__doc__,checks=checks,
            passed=sum(c['passed'] for c in checks),total=len(checks))
print(json.dumps(report,indent=2))
if report['passed']!=report['total']:raise SystemExit(1)
