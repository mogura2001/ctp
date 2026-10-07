"""Original FliEngine centroid with mocked membership samples.

This does not parse FLI rules. Centroid tests mock membership samples. Four
separate consequent tests execute real output transforms with mocked set-function
membership. Linked-value getter/setter execute real code.
"""
from pathlib import Path
import hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
P=ROOT/'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll'
HASH='3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
assert hashlib.sha256(P.read_bytes()).hexdigest()==HASH
img=pefile.PE(str(P)).get_memory_mapped_image()
SYM,VALUE,STACK,STOP,SCRATCH,RET4,RET24=0x30010000,0x30020000,0x30030000,0x300f0000,0x300f1000,0x300f2000,0x300f3000
def put(u,a,v):u.mem_write(a,struct.pack('<I',v))
def word(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
def getdbl(u,a):return struct.unpack('<d',u.mem_read(a,8))[0]
checks=[]
for name,expected in [('empty',7),('constant',5),('only2',2),('only10',10)]:
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x20000000,(len(img)+4095)&~4095);u.mem_write(0x20000000,img)
 u.mem_map(0x30000000,0x100000);u.reg_write(UC_X86_REG_FPCW,0x37f)
 put(u,SYM,VALUE);dbl(u,VALUE,7);dbl(u,SYM+0x70,0);dbl(u,SYM+0x78,10)
 for off,val in [(0,STOP),(4,0),(8,SYM)]:put(u,STACK+off,val)
 dbl(u,STACK+12,10)
 for a,n in [(RET4,4),(RET24,24)]:u.mem_write(a,b'\xdd\x05'+struct.pack('<I',SCRATCH)+b'\xc2'+struct.pack('<H',n))
 samples=[]
 def hook(uc,address,size,data):
  sp=uc.reg_read(UC_X86_REG_ESP)
  if address in (0x2003b770,0x2003a860,0x2003bac0):
   cleanup=4 if address==0x2003bac0 else 0
   target=word(uc,sp);uc.reg_write(UC_X86_REG_EAX,0);uc.reg_write(UC_X86_REG_ESP,sp+4+cleanup);uc.reg_write(UC_X86_REG_EIP,target)
  elif address==0x2003be70:dbl(uc,SCRATCH,1);uc.reg_write(UC_X86_REG_EIP,RET4)
  elif address==0x2003bc40:
   x=getdbl(uc,word(uc,sp+8));samples.append(x)
   membership=0 if name=='empty' else 1 if name=='constant' else int(x==(2 if name=='only2' else 10))
   dbl(uc,SCRATCH,membership);uc.reg_write(UC_X86_REG_EIP,RET24)
 u.hook_add(UC_HOOK_CODE,hook);u.reg_write(UC_X86_REG_ESP,STACK)
 u.emu_start(0x200391e0,STOP,count=10000)
 got=getdbl(u,VALUE);checks.append(dict(name=name,got=got,expected=expected,passed=got==expected,samples=samples))
for hedge,coef,expected in [(0,2,.5),(4,1,.75),(5,1,.0625),(6,1,.4375)]:
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x20000000,(len(img)+4095)&~4095);u.mem_write(0x20000000,img)
 u.mem_map(0x30000000,0x100000);u.reg_write(UC_X86_REG_FPCW,0x37f)
 dbl(u,SYM,coef);u.mem_write(SYM+0xc,bytes([int(hedge!=0),hedge]));put(u,STACK,STOP)
 dbl(u,SCRATCH,.25);u.mem_write(RET24,b'\xdd\x05'+struct.pack('<I',SCRATCH)+b'\xc2\x18\x00')
 u.mem_write(STOP,b'\xdd\x1d'+struct.pack('<I',VALUE))
 def consequent_hook(uc,address,size,data):
  if address==0x2003b270:uc.reg_write(UC_X86_REG_EIP,RET24)
 u.hook_add(UC_HOOK_CODE,consequent_hook);u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,SYM)
 u.emu_start(0x2003a980,STOP+6,count=10000)
 got=getdbl(u,VALUE);checks.append(dict(name='consequent_'+str((hedge,coef)),got=got,expected=expected,passed=got==expected))
report=dict(ai_sha256=HASH,limitations=__doc__,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks))
out=ROOT/'ANALYSE/BINAIR/fuzzy-policy-defuzzification-controls.json';out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(passed=report['passed'],total=report['total'],failures=[c for c in checks if not c['passed']],output=str(out)),indent=2))
if report['passed']!=report['total']:raise SystemExit(1)
