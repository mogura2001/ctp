"""Execute original SupplyEntertainers with explicit Population recorder mocks.

Status/happiness and bard-effect inputs are synthetic; requests do not mutate an
engine population. This checks requested counts and local accounting only.
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
CITY,AI,POP,TABLE,POSITION,AVAILABLE,STACK=range(0x30010000,0x30080000,0x10000)
STOP,STATUS,CHANGE,PLACE=0x300f0000,0x300f1000,0x300f2000,0x300f3000
def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def word(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
checks=[]
for name,happy,effect,threshold,available,limit,cached,fails,expected in [
 ('happy_enough',75,1,75,4,4,0,False,0),('one_needed',74,1,75,4,4,0,False,1),
 ('three_needed',72,1,75,4,4,0,False,3),('available_limit',70,1,75,2,4,0,False,2),
 ('position_limit',70,1,75,4,1,0,False,1),('zero_effect',70,0,75,2,4,0,False,2),
 ('cached_bard',74,1,75,4,4,1,False,0),('failed_requests',74,1,75,4,4,0,True,1)]:
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x20000000,(len(img)+4095)&~4095);u.mem_write(0x20000000,img)
 u.mem_map(0x30000000,0x100000);u.reg_write(UC_X86_REG_FPCW,0x37f)
 for a,v in [(AI+0x40,POP),(POP,TABLE),(TABLE+0x40,STATUS),(TABLE+0x34,CHANGE),
             (TABLE+0x3c,PLACE),(CITY+0xbc,cached),(POSITION,0),(AVAILABLE,available),
             (STACK,STOP),(STACK+4,AI),(STACK+8,POSITION),(STACK+12,AVAILABLE),(STACK+16,limit)]:put(u,a,v)
 dbl(u,STACK+20,threshold);dbl(u,STACK+28,0)
 requests=[]
 def hook(uc,address,size,data):
  sp=uc.reg_read(UC_X86_REG_ESP)
  if address==STATUS:
   put(uc,word(uc,sp+12),0);dbl(uc,word(uc,sp+16),happy);dbl(uc,word(uc,sp+20),effect);cleanup=20
  elif address in (CHANGE,PLACE):
   requests.append(dict(action='change' if address==CHANGE else 'place',position=word(uc,sp+12),type=word(uc,sp+16)))
   put(uc,word(uc,sp+20),int(fails));cleanup=20
  else:return
  target=word(uc,sp);uc.reg_write(UC_X86_REG_ESP,sp+4+cleanup);uc.reg_write(UC_X86_REG_EAX,0);uc.reg_write(UC_X86_REG_EIP,target)
 u.hook_add(UC_HOOK_CODE,hook);u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,CITY)
 u.emu_start(0x20021710,STOP,count=10000)
 got=[word(u,POSITION),word(u,AVAILABLE),word(u,CITY+0xbc),len(requests)]
 want=[expected,available-expected,cached+expected,2*expected]
 passed=got==want and all(r['type']==1 for r in requests)
 checks.append(dict(name=name,got=got,expected=want,passed=passed,requests=requests,request_error=fails))
report=dict(ai_sha256=HASH,limitations=__doc__,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks))
out=ROOT/'ANALYSE/BINAIR/happiness-bards-controls.json';out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(passed=report['passed'],total=report['total'],failures=[c for c in checks if not c['passed']],output=str(out)),indent=2))
if report['passed']!=report['total']:raise SystemExit(1)
