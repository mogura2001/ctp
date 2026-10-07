"""Original DLL branch controls; synthetic state, explicit action recorders.

No game launch, real queue or complete scheduler execution.
"""
from pathlib import Path
import sys, struct, hashlib, json
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_ESP, UC_X86_REG_EIP
path=ROOT/'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll'
digest=hashlib.sha256(path.read_bytes()).hexdigest()
assert digest=='3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
pe=pefile.PE(str(path)); M=0x30000000
AI,PL,CITY,GOAL,PLAYER,VT,LIST,ITEMS,DB,DVT=[M+x for x in range(0x1000,0xb000,0x1000)]
STACK,STOP,OUT,HOOK=M+0xe0000,M+0xff000,M+0xf0000,M+0x20000
checks=[]
def integer(u,a,v=None):
 if v is None:return struct.unpack('<I',u.mem_read(a,4))[0]
 u.mem_write(a,struct.pack('<I',v&0xffffffff))
def real(u,a,v=None):
 if v is None:return struct.unpack('<d',u.mem_read(a,8))[0]
 u.mem_write(a,struct.pack('<d',v))
def fixture():
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0,0x1000)
 u.mem_map(pe.OPTIONAL_HEADER.ImageBase,(pe.OPTIONAL_HEADER.SizeOfImage+4095)&~4095)
 u.mem_write(pe.OPTIONAL_HEADER.ImageBase,pe.get_memory_mapped_image());u.mem_map(M,0x100000)
 integer(u,AI+0x94,PL);integer(u,AI+0x2c,PLAYER);integer(u,PLAYER,VT)
 integer(u,AI+0x3c,DB);integer(u,DB,DVT)
 return u
def run(u,addr,args,receiver=GOAL,capture=False):
 integer(u,STACK,STOP)
 for i,v in enumerate(args):integer(u,STACK+4+i*4,v)
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,receiver)
 end=STOP
 if capture:u.mem_write(STOP,b'\xdd\x1d'+struct.pack('<I',OUT));end+=6
 u.emu_start(addr,end,count=100000)
 assert u.reg_read(UC_X86_REG_EIP)==end
 return real(u,OUT) if capture else u.reg_read(UC_X86_REG_EAX)
def ret(u,n,v=0):
 sp=u.reg_read(UC_X86_REG_ESP);u.reg_write(UC_X86_REG_EAX,v)
 u.reg_write(UC_X86_REG_EIP,integer(u,sp));u.reg_write(UC_X86_REG_ESP,sp+4+n)
def record(name,got,expected,mocks=()):
 checks.append(dict(name=name,got=got,expected=expected,passed=got==expected,external_mocks=list(mocks)))

# Original raw priority, including category flags. No external callbacks.
for name,addr,flag,base,weight,expected in [
 ('unit_raw_add',0x20049b30,None,20000000,10500,20010500),
 ('building_raw_add',0x20049460,None,20000000,7950,20007950),
 ('wonder_raw_add',0x20049460,0x70,19997500,10000,20007500),
 ('wonder_zero_weight_still_positive',0x20049460,0x70,19997500,0,19997500),
 ('endgame_raw_add',0x20049460,0x74,123,50,173),
 ('capitalization_raw_add',0x20049460,0x78,321,50,371)]:
 u=fixture();real(u,GOAL+0x68,weight)
 field=0x28 if addr==0x20049b30 else {None:0x30,0x70:0x200,0x74:0x38,0x78:0x40}[flag]
 real(u,PL+field,base)
 if flag:integer(u,GOAL+flag,1)
 record(name,run(u,addr,[AI],capture=True),expected)

# Actual enqueue methods: Player callback records request and returns acceptance.
for kind,addr,category in [('unit',0x2001c3d0,1),('building',0x2001d260,3),('wonder',0x2001d2a0,9)]:
 for accepted in (0,1):
  u=fixture();requests=[];integer(u,CITY+0xc,77);integer(u,CITY+0x1f0,-1)
  integer(u,VT+0x50,HOOK);u.mem_write(HOOK,b'\xc3')
  def cb(uc,a,size,data):
   sp=uc.reg_read(UC_X86_REG_ESP)
   if a==HOOK:
    requests.append([integer(uc,sp+8),integer(uc,sp+16),integer(uc,sp+20)])
    ret(uc,20,accepted)
   elif a==0x2000f860:ret(uc,8,1)
   elif a==0x2000f8d0:ret(uc,4)
  u.hook_add(UC_HOOK_CODE,cb)
  run(u,addr,[AI,4,0,0],receiver=CITY)
  record(kind+'_request_'+str(accepted),requests,[[77,category,4]],('Player enqueue', 'wonder availability/mark' ) if kind=='wonder' else ('Player enqueue',))
  record(kind+'_cache_'+str(accepted),[integer(u,CITY+0x1f0),integer(u,CITY+0x1f4)],
         [4,category] if accepted else [0xffffffff,0],('Player enqueue',))

# Actual AIP list loop; external eligibility and allocation/planner are stubs.
for name,eligible,present,queue,expected in [
 ('list_first_eligible',[1,1,1],[0,0,0],0,[0]),
 ('list_skip_unbuildable',[0,1,1],[0,0,0],0,[1]),
 ('list_skip_owned',[1,1,1],[1,0,0],0,[1]),
 ('list_none',[0,0,0],[0,0,0],0,[]),
 ('list_busy_queue',[1,1,1],[0,0,0],1,[])]:
 u=fixture();aip=PL+0x20;integer(u,aip+0x800,AI)
 integer(u,LIST,ITEMS);integer(u,LIST+4,3);integer(u,DVT+0x14,HOOK)
 for i,weight in enumerate((1,99999,2)):
  real(u,ITEMS+32*i,weight);integer(u,ITEMS+32*i+8,i);integer(u,ITEMS+32*i+0x18,0)
 chosen=[]
 def select_cb(uc,a,size,data):
  sp=uc.reg_read(UC_X86_REG_ESP)
  if a==0x2001c330:ret(uc,0,queue)
  elif a==0x2001fa60:ret(uc,8,eligible[integer(uc,sp+8)])
  elif a==0x2001fa40:ret(uc,4,present[integer(uc,sp+4)])
  elif a==HOOK:ret(uc,8,100)
  elif a==0x2001d9f0:ret(uc,8,1)
  elif a==0x20026b50:ret(uc,0,GOAL)
  elif a==0x20048e00:
   chosen.append(integer(uc,sp+8));ret(uc,32,GOAL)
  elif a==0x20071710:ret(uc,8)
  elif a==0x2006ef20:ret(uc,4)
 u.hook_add(UC_HOOK_CODE,select_cb)
 run(u,0x200664d0,[CITY,LIST,0,0,4],receiver=aip)
 record(name,chosen,expected,('eligibility/cost/pretest', 'allocator/goal constructor/planner'))

# Stored-production exception is an actual instruction predicate, without mocks.
for stock,production,expected in [(499,100,0),(500,29,0),(500,30,1),(500,120,0),(600,120,1)]:
 u=fixture();integer(u,CITY+0x28,stock);integer(u,CITY+0x38,production)
 record(f'stored_production_{stock}_{production}',run(u,0x2001ca20,[],receiver=CITY),expected)

# Actual wonder build-time gate; only production-cost getter is an x87 stub.
for name,cost,production,stock,incumbent,max_turns,expected in [
 ('wonder_at_time_limit',1000,20,0,-1,50,1),
 ('wonder_over_time_limit',1020,20,0,-1,50,0),
 ('wonder_stock_makes_feasible',1500,20,500,-1,50,1),
 ('wonder_busy_cache_blocks',1000,20,0,3,50,0),
 ('wonder_zero_production_uses_cost',1000,0,0,-1,50,0)]:
 u=fixture();integer(u,CITY+0x38,production);integer(u,CITY+0x28,stock)
 integer(u,CITY+0x1f0,incumbent);integer(u,PL+0x754,max_turns)
 real(u,OUT+0x100,cost)
 u.mem_write(0x2000f840,b'\xdd\x05'+struct.pack('<I',OUT+0x100)+b'\xc2\x04\x00')
 # Imported CRT _ftol replacement: truncate x87 input, same integer boundary.
 u.mem_write(0x20085dc0,b'\xdb\x0d'+struct.pack('<I',OUT+0x108)+b'\xa1'+struct.pack('<I',OUT+0x108)+b'\xc3')
 record(name,run(u,0x2001db50,[AI,4],receiver=CITY),expected,('wonder production-cost getter','CRT float-to-int truncation replacement'))

result=dict(binary_sha256=digest,scope='Original DLL instructions, synthetic state; no actual engine queue or full scheduler',checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks))
out=ROOT/'ANALYSE/BINAIR/build-goals-queue-controls.json';out.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(f"{result['passed']}/{result['total']} controls passed")
assert result['passed']==result['total']
