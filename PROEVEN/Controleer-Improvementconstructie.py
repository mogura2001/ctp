"""Original-instruction checks with synthetic state and named external mocks."""
from pathlib import Path
import sys,struct,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EIP
paths=[ROOT/'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll',ROOT/'CTP-og/ctp_program/ctp/civctp.exe']
hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]
assert hashes==['3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44','b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79']
pes=[pefile.PE(str(p)) for p in paths];M=0x30000000
AI,OBJ,VT,GOAL,POS,OUT,LIST,COUNTS,ITEMS=[M+i*0x1000 for i in range(1,10)]
STACK,STOP,HOOK=M+0xe0000,M+0xff000,M+0x20000
checks=[]
def integer(u,a,v=None):
 if v is None:return struct.unpack('<I',u.mem_read(a,4))[0]
 u.mem_write(a,struct.pack('<I',v&0xffffffff))
def real(u,a,v=None):
 if v is None:return struct.unpack('<d',u.mem_read(a,8))[0]
 u.mem_write(a,struct.pack('<d',v))
def point(u,a,p=None):
 if p is None:return struct.unpack('<hhh',u.mem_read(a,6))
 u.mem_write(a,struct.pack('<hhh',*p)+b'\0\0')
def ret(u,n,v=0):
 sp=u.reg_read(UC_X86_REG_ESP);u.reg_write(UC_X86_REG_EAX,v);u.reg_write(UC_X86_REG_EIP,integer(u,sp));u.reg_write(UC_X86_REG_ESP,sp+4+n)
def fixture():
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0,0x1000)
 for p in pes:
  a=p.OPTIONAL_HEADER.ImageBase;u.mem_map(a,(p.OPTIONAL_HEADER.SizeOfImage+4095)&~4095);u.mem_write(a,p.get_memory_mapped_image())
 u.mem_map(M,0x100000);return u
def run(u,a,args,receiver=OBJ):
 integer(u,STACK,STOP)
 for i,v in enumerate(args):integer(u,STACK+4+4*i,v)
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,receiver);u.emu_start(a,STOP,count=100000)
 assert u.reg_read(UC_X86_REG_EIP)==STOP
 return u.reg_read(UC_X86_REG_EAX)
def record(name,got,expected,mocks=()):checks.append(dict(name=name,got=got,expected=expected,passed=got==expected,external_mocks=list(mocks)))
# Actual direction initializer, neighbour arithmetic and open-area enumerator.
areas=[]
for center in [(20,40,0),(21,41,0)]:
 u=fixture();integer(u,0xa7e328,7);integer(u,0xa7dd70,OBJ)
 point(u,0xa7df20,(100,100,2));run(u,0x502cc0,[])
 integer(u,OBJ,VT);integer(u,VT+0x28,HOOK);u.mem_write(HOOK,b'\xc3');point(u,POS,center)
 def legal(uc,a,size,data):
  if a==HOOK:ret(uc,8,1)
  elif a==0x511030:ret(uc,16,1)
 u.hook_add(UC_HOOK_CODE,legal)
 run(u,0x534510,[OBJ,1,POS,OUT,ITEMS]);n=integer(u,OUT)
 pts=[point(u,ITEMS+8*i) for i in range(n)];areas.append(pts)
 record('candidate_count_'+str(center),n,20,['World layer predicate','World tile eligibility: all allowed'])
 record('unique_positions_'+str(center),len(set(pts)),20,['World layer predicate','World tile eligibility: all allowed'])
 record('center_excluded_'+str(center),center in pts,False,['World layer predicate','World tile eligibility: all allowed'])
record('adjacent_areas_overlap',len(set(areas[0])&set(areas[1]))>0,True,['World layer predicate','World tile eligibility: all allowed'])
# Actual utility selection, including ties and consumed-goal marking.
for name,utilities,expected in [('highest',[1,9,3],1),('first_tie',[9,9,3],0),('nonpositive',[0,-1,-2],None)]:
 u=fixture();integer(u,LIST,3);integer(u,LIST+4,COUNTS);integer(u,LIST+8,ITEMS)
 for i,v in enumerate(utilities):
  g=GOAL+0x100*i;integer(u,ITEMS+4*i,g);integer(u,COUNTS+4*i,1);real(u,g+0x10,v)
 got=run(u,0x2005c410,[AI,OUT],LIST);selected=integer(u,OUT)
 record(name,[got,selected],[int(expected is not None),0 if expected is None else GOAL+0x100*expected])
 if expected is not None:record(name+'_consumed',real(u,selected+0x10)<0,True)
# Actual Construct budget gate and request. Engine acceptance is deliberately mocked.
for name,budget,cost,accept,expected in [('enough',500,200,1,[1,300]),('exact',200,200,1,[1,0]),('engine_rejects',500,200,0,[1,300]),('not_enough',100,200,1,[0,-100])]:
 u=fixture();integer(u,AI+0x50,OBJ);integer(u,OBJ,VT);integer(u,VT+0x18,HOOK);u.mem_write(HOOK,b'\xc3')
 integer(u,GOAL+8,1);integer(u,GOAL+0xc,0);integer(u,GOAL+0x18,cost);integer(u,GOAL+0x20,POS);integer(u,OUT,budget);requests=[]
 def construct(uc,a,size,data):
  if a==HOOK:
   sp=uc.reg_read(UC_X86_REG_ESP);requests.append([integer(uc,sp+8),integer(uc,sp+12),integer(uc,sp+16)]);ret(uc,16,accept)
 u.hook_add(UC_HOOK_CODE,construct);run(u,0x20050430,[AI,OUT],GOAL)
 remaining=struct.unpack('<i',u.mem_read(OUT,4))[0]
 record(name,[len(requests),remaining],expected,['Improvement construction request'])
# Actual World tile eligibility with a synthetic one-cell grid; no callbacks.
for name,worker,city,expected in [('unoccupied',0,0,1),('occupied_worker',1,0,0),('city_center',0,1,0)]:
 u=fixture();layer,column,cell=M+0x31000,M+0x32000,M+0x33000
 integer(u,OBJ+0x1c,VT);integer(u,VT,layer);integer(u,layer,column);integer(u,column,cell)
 integer(u,cell+0x18,worker);integer(u,cell+0x14,city);point(u,POS,(0,0,0))
 record(name,run(u,0x511030,[1,POS,1,OUT]),expected)
# Local final cell-bit writers preserve the other improvement family.
for family,addr,mask,shift in [('farm',0x4fffc0,12,2),('mine',0x500000,48,4)]:
 for level in (1,2,3):
  u=fixture();flags=0x25;integer(u,OBJ,flags)
  def refresh(uc,a,size,data):
   if a==0x501170:ret(uc,0)
  u.hook_add(UC_HOOK_CODE,refresh);run(u,addr,[level])
  record(family+'_level_'+str(level),integer(u,OBJ),(flags&~mask)|(level<<shift),['Cell yield/cache refresh'])
result=dict(binary_sha256=hashes,scope='Original local instructions; synthetic state, no game/PW mutation; eligibility/action mocks explicit',area_positions=areas,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks))
(ROOT/'ANALYSE/BINAIR/improvement-construction-controls.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(f"{result['passed']}/{result['total']} controls passed")
assert result['passed']==result['total']
