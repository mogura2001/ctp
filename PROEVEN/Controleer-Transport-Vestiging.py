"""Read-only original engine/DLL branch checks with explicit external mocks.

No game launch, actual army order, full pathfinding or scheduler execution.
"""
from pathlib import Path
import sys, struct, hashlib, json
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_ESP, UC_X86_REG_EIP
paths=[ROOT/'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll',ROOT/'CTP-og/ctp_program/ctp/civctp.exe']
hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]
assert hashes==['3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44','b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79']
pes=[pefile.PE(str(p)) for p in paths]
M=0x30000000
AI,ARM,PAX,PLAYER,PVT,DB,RECS,POS1,POS2,CARGO=[M+x for x in range(0x1000,0xb000,0x1000)]
STACK,STOP,OUT,HOOK=M+0xe0000,M+0xff000,M+0xf0000,M+0x20000
checks=[]
def integer(u,a,v=None):
 if v is None:return struct.unpack('<I',u.mem_read(a,4))[0]
 u.mem_write(a,struct.pack('<I',v&0xffffffff))
def short(u,a,v):u.mem_write(a,struct.pack('<h',v))
def real(u,a,v):u.mem_write(a,struct.pack('<d',v))
def ret(u,n,v=0):
 sp=u.reg_read(UC_X86_REG_ESP);u.reg_write(UC_X86_REG_EAX,v)
 u.reg_write(UC_X86_REG_EIP,integer(u,sp));u.reg_write(UC_X86_REG_ESP,sp+4+n)
def fixture():
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0,0x1000)
 for p in pes:
  base=p.OPTIONAL_HEADER.ImageBase;u.mem_map(base,(p.OPTIONAL_HEADER.SizeOfImage+4095)&~4095)
  u.mem_write(base,p.get_memory_mapped_image())
 u.mem_map(M,0x100000)
 integer(u,AI+0x2c,PLAYER);integer(u,PLAYER,PVT)
 integer(u,AI+0x38,DB);integer(u,DB,0x745098)
 integer(u,ARM+0xc,17);integer(u,PAX+0xc,23)
 integer(u,ARM+0x64,POS1);integer(u,PAX+0x64,POS2)
 short(u,ARM+0x48,1);short(u,ARM+0x4a,0)
 short(u,PAX+0x48,1);short(u,PAX+0x4a,1)
 integer(u,RECS+0x48,1);integer(u,RECS+0x4c,2)
 integer(u,RECS+0x300+0x30,0x80001000)
 def getter(uc,a,size,data):
  if a==0x4542e0:
   sp=uc.reg_read(UC_X86_REG_ESP);ret(uc,4,RECS+0x300*integer(uc,sp+4))
 u.hook_add(UC_HOOK_CODE,getter)
 return u
def run(u,a,args,receiver=ARM):
 integer(u,STACK,STOP)
 for i,v in enumerate(args):integer(u,STACK+4+4*i,v)
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,receiver)
 u.emu_start(a,STOP,count=100000)
 assert u.reg_read(UC_X86_REG_EIP)==STOP
 return u.reg_read(UC_X86_REG_EAX)
def record(name,got,expected,mocks):
 checks.append(dict(name=name,got=got,expected=expected,passed=got==expected,external_mocks=mocks))
for name,mask,size,expected in [('small_land',1,0x80001000,1),('no_carry_flag',0,0x80001000,0),('medium_land',1,0x80002000,0),('small_air',1,0x10001000,0)]:
 u=fixture();integer(u,RECS+0x48,mask);integer(u,RECS+0x330,size)
 record(name,run(u,0x46ea80,[0,1]),expected,['UnitDB record lookup'])
for cap in (0,2,5):
 u=fixture();integer(u,RECS+0x4c,cap)
 record('capacity_getter_'+str(cap),run(u,0x531fc0,[DB,0]),cap,['UnitDB record lookup'])
for name,count,cap,compatible,expected in [('one_fits',1,2,1,1),('two_fit',2,2,1,1),('three_do_not_fit',3,2,1,0),('wrong_cargo_type',1,2,0,0)]:
 u=fixture();integer(u,ARM+0x40,1);integer(u,PAX+0x40,3)
 short(u,PAX+0x48,count)
 for i in range(count):short(u,PAX+0x4a+2*i,1)
 integer(u,RECS+0x4c,cap)
 if not compatible:integer(u,RECS+0x330,0x10001000)
 record(name,run(u,0x20019440,[AI,PAX]),expected,['UnitDB record lookup'])
for name,state,types,loaded,expected in [('one_empty',3,[0],0,[1,0,2]),('one_loaded',3,[0],1,[1,1,1]),('two_carriers',3,[0,0],1,[1,1,3]),('represented_state_1',1,[0],0,[1,0,2]),('no_carrier',3,[1],0,[0,0,0]),('excluded_state_17',17,[0],0,[0,0,0])]:
 u=fixture();integer(u,ARM+0x40,state);short(u,ARM+0x48,len(types))
 for i,t in enumerate(types):short(u,ARM+0x4a+2*i,t)
 if loaded:integer(u,ARM+0x60,CARGO);integer(u,CARGO+8,loaded)
 integer(u,PVT+0x28c,HOOK);u.mem_write(HOOK,b'\xc3')
 def query(uc,a,size,data):
  if a==HOOK:
   sp=uc.reg_read(UC_X86_REG_ESP);integer(uc,integer(uc,sp+16),len(types))
   for i,t in enumerate(types):integer(uc,integer(uc,sp+20)+4*i,t)
   ret(uc,24,1)
 u.hook_add(UC_HOOK_CODE,query)
 got=run(u,0x20013420,[AI,OUT,OUT+4])
 record(name,[got,integer(u,OUT),integer(u,OUT+4)],expected,['UnitDB record lookup','Player army-type query'])
for name,movement,same,accepted,expected in [('cannot_move',15,True,1,[]),('same_tile_accepted',16,True,1,[[23,17]]),('same_tile_rejected',16,True,0,[[23,17]]),('different_tile',16,False,1,[])]:
 u=fixture();real(u,PAX+0x70,movement);integer(u,PAX+0x88,2)
 if not same:integer(u,POS2,1)
 integer(u,PVT+0xfc,HOOK);u.mem_write(HOOK,b'\xc3');requests=[]
 def board(uc,a,size,data):
  if a==HOOK:
   sp=uc.reg_read(UC_X86_REG_ESP);requests.append([integer(uc,sp+12),integer(uc,sp+16)])
   ret(uc,24,accepted)
 u.hook_add(UC_HOOK_CODE,board)
 run(u,0x200199a0,[AI,ARM],PAX)
 record(name,requests,expected,['Player boarding request'])
for accepted in (0,1):
 u=fixture();integer(u,PVT+0x24,HOOK);u.mem_write(HOOK,b'\xc3');requests=[]
 def settle(uc,a,size,data):
  if a==HOOK:
   sp=uc.reg_read(UC_X86_REG_ESP);requests.append(integer(uc,sp+8));ret(uc,12,accepted)
 u.hook_add(UC_HOOK_CODE,settle)
 got=run(u,0x20018980,[AI])
 record('settle_request_'+str(accepted),[requests,got],[[17],accepted],['Player settlement request'])
result=dict(binary_sha256=hashes,scope='Original engine/DLL instructions, synthetic records/state; external callbacks named; no actual orders/pathfinding/full scheduler',checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks))
(ROOT/'ANALYSE/BINAIR/transport-settle-actions-controls.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(f"{result['passed']}/{result['total']} controls passed")
assert result['passed']==result['total']
