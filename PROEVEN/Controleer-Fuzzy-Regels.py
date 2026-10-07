"""Original FLI shape, section initialization and rule-to-output instructions.

Synthetic parsed records/bytecode; not a text parser or full civilization turn.
Only function-index lookup, clock and logging are callbacks. Output procedures,
stacks, forms, centroid, counters and linked-value writes execute real code.
Preallocated output arrays avoid allocator branches; original instructions on
disk are never changed. FTOL is a fixture-only CRT substitute.
"""
from pathlib import Path
import hashlib,json,math,struct,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
from ctp_x87 import ftol_stub
P=ROOT/'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll'
HASH='3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
assert hashlib.sha256(P.read_bytes()).hexdigest()==HASH
img=pefile.PE(str(P)).get_memory_mapped_image()
F1,F2,F3,S1,S2,S3,ARRAY,PROCS,RULE,CODE,LIST,NODE,VALUE,STACK=[0x30010000+i*0x4000 for i in range(14)]
STOP,OUT,CLOCK=0x300f0000,0x300f1000,0x300f2000
def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def word(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
def getdbl(u,a):return struct.unpack('<d',u.mem_read(a,8))[0]
def ret(u,v,n):
 sp=u.reg_read(UC_X86_REG_ESP);target=word(u,sp)
 u.reg_write(UC_X86_REG_EAX,v);u.reg_write(UC_X86_REG_ESP,sp+4+n);u.reg_write(UC_X86_REG_EIP,target)
def fixture():
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x20000000,(len(img)+4095)&~4095);u.mem_write(0x20000000,img)
 u.mem_map(0x30000000,0x100000);u.mem_map(0,0x1000);u.reg_write(UC_X86_REG_FPCW,0x37f)
 u.mem_write(0x20085dc0,ftol_stub());put(u,0x2008900c,CLOCK);u.mem_write(0x200a4640,b'\x01')
 for f,s,value in [(F1,S1,.25),(F2,S2,.75),(F3,S3,7)]:
  dbl(u,f,1);dbl(u,f+8,1);put(u,f+0x1c,s);u.mem_write(f+0x14,b'\0')
  dbl(u,s+8,value);u.mem_write(s+0xc2,b'\x04\0')
 dbl(u,F3,8);u.mem_write(F3+0x14,b'\x02');dbl(u,F3+0x20,7);dbl(u,F3+0x28,9)
 dbl(u,S3+0x70,6);dbl(u,S3+0x78,10);u.mem_write(S3+0x6a,b'\x01')
 put(u,S3+0xc4,ARRAY);put(u,ARRAY+4,16);put(u,ARRAY+0xc,PROCS)
 put(u,RULE+8,2);put(u,RULE+0x10,LIST);put(u,LIST,NODE);put(u,NODE,S3)
 u.mem_write(S3+0x84,b'\x01\0')
 def hook(uc,a,size,data):
  sp=uc.reg_read(UC_X86_REG_ESP)
  if a==0x20038c60:ret(uc,{1:F1,2:F2,3:F3}.get(word(uc,sp+4),0),4)
  elif a in (CLOCK,0x2003a860,0x20039320):ret(uc,0,0)
 u.hook_add(UC_HOOK_CODE,hook);return u
def call(u,fn,this,args,store=False,count=200000):
 put(u,STACK,STOP)
 for i,a in enumerate(args):put(u,STACK+4+4*i,a)
 if store:u.mem_write(STOP,b'\xdd\x1d'+struct.pack('<I',OUT))
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,this)
 u.emu_start(fn,STOP+6 if store else STOP,count=count)
checks=[]
def equal(got,expected):
 if isinstance(expected,list):return len(got)==len(expected) and all(equal(a,b) for a,b in zip(got,expected))
 if isinstance(expected,float):return math.isclose(got,expected,rel_tol=0,abs_tol=1e-12)
 return got==expected
def check(name,got,expected):checks.append(dict(name=name,got=got,expected=expected,passed=equal(got,expected)))
def dwords(x):return struct.unpack('<II',struct.pack('<d',x))
for kind,x,expected in [(0,3,0),(0,4,.5),(0,5,1),(1,5,1),(1,6,.5),(1,7,0),
                         (2,4,.5),(2,5,1),(2,7,0),(3,4.5,0),(3,4.75,1),(3,5,1),(4,5,0)]:
 u=fixture();dbl(u,F1,5);dbl(u,F1+8,2);u.mem_write(F1+0x14,bytes([kind]))
 call(u,0x2003b270,F1,[*dwords(x),*dwords(1),OUT+8,OUT+12],True)
 check('shape_'+str((kind,x)),getdbl(u,OUT),expected)
for linked,registered,expected in [(False,True,3),(True,True,3),(False,False,7),(True,False,7)]:
 u=fixture();put(u,ARRAY+8,2);dbl(u,S3+0x20,3)
 if linked:put(u,S3,VALUE);dbl(u,VALUE,7)
 if registered:u.mem_write(S3+0x68,b'\x04\0')
 call(u,0x2003b850,S3,[2])
 check('section_'+str((linked,registered)),[getdbl(u,VALUE if linked else S3+8),word(u,ARRAY+8)],[expected,0])
def term(n):return b'\x01'+struct.pack('<I',n)
for name,antecedent,expected in [
 ('single',term(1),.25),('and',term(1)+term(2)+b'\x02',.25),
 ('or',term(1)+term(2)+b'\x03',.75),('not',term(1)+b'\x04',.75),
 # Antecedent Kinda is FSQRT; consequent code6 uses a different polynomial.
 ('very',term(1)+b'\x05',.0625),('kinda',term(1)+b'\x06',.5),
 ('zero',term(1),0)]:
 u=fixture()
 if name=='zero':dbl(u,S1+8,0)
 # Dispatch table2003b07c: opcode12 freezes antecedent scalar,11 adds output.
 code=antecedent+b'\x0c\x0b'+struct.pack('<I',3)+b'\x0d'
 u.mem_write(CODE,code);put(u,RULE,CODE);put(u,RULE+4,len(code))
 call(u,0x2003abf0,RULE,[0,2])
 check('rule_'+name,[getdbl(u,PROCS),getdbl(u,S3+8),word(u,ARRAY+8)],
       [expected,8.0 if expected>0 else 7.0,1 if expected>0 else 0])
# A single symmetric yes-output remains near its center even at weak activation.
# Default zero is a reset value, not an additional fuzzy consequent.
for strength,expected in [(1/3,1.0),(0,0.0)]:
 u=fixture();dbl(u,S1+8,strength);dbl(u,S3+8,0)
 dbl(u,F3,1);dbl(u,F3+8,.5);dbl(u,F3+0x20,.5);dbl(u,F3+0x28,1.5)
 dbl(u,S3+0x70,0);dbl(u,S3+0x78,2)
 code=term(1)+b'\x0c\x0b'+struct.pack('<I',3)+b'\x0d'
 u.mem_write(CODE,code);put(u,RULE,CODE);put(u,RULE+4,len(code))
 call(u,0x2003abf0,RULE,[0,2])
 check('yes_output_'+str(strength),getdbl(u,S3+8),expected)
report=dict(ai_sha256=HASH,limitations=__doc__,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks))
out=ROOT/'ANALYSE/BINAIR/fuzzy-policy-rule-controls.json';out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(passed=report['passed'],total=report['total'],failures=[c for c in checks if not c['passed']],output=str(out)),indent=2))
if report['passed']!=report['total']:raise SystemExit(1)
