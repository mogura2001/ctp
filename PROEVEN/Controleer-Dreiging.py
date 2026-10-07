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

for value in (19.99,20.0,20.01,39.99,40.0,40.01):
 for name,address,limit in [('hot',0x2000c690,20),('cold',0x2000c6b0,40)]:
  u=fixture();real(u,OBJ+0x68,value);real(u,OBJ+0x70,0)
  record(name+'_'+str(value),run(u,address,[]),int(value<=limit))
# Same sum, different components.
u=fixture();real(u,OBJ+0x68,50);real(u,OBJ+0x70,-30)
record('hot_sum_components',run(u,0x2000c690,[]),1)
# Actual strategic map cell getter, including separate layer1 scalar.
for name,pos,expected in [('first_cell',(0,0,0),11),('second_cell',(2,0,0),22),('layer1',(2,0,1),77)]:
 u=fixture();integer(u,OBJ,2);integer(u,0x200c6fdc,LIST)
 integer(u,LIST,ITEMS);integer(u,LIST+4,1);integer(u,LIST+8,2)
 u.mem_write(ITEMS,struct.pack('<ff',11,22));u.mem_write(OBJ+0x6c,struct.pack('<f',77));point(u,POS,pos)
 integer(u,STACK,STOP);integer(u,STACK+4,POS)
 u.mem_write(STOP,b'\xdd\x1d'+struct.pack('<I',OUT))
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,OBJ)
 u.emu_start(0x20083b10,STOP+6,count=100000)
 record(name,real(u,OUT),expected)
result=dict(binary_sha256=hashes,scope='Original hot/cold predicates and map lookup, synthetic state, no external mocks or game turn',checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks))
(ROOT/'ANALYSE/BINAIR/threat-defense-controls.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(f"{result['passed']}/{result['total']} controls passed")
assert result['passed']==result['total']
