"""Original AI science request, engine government cap and city gold conversion.

Synthetic objects. Request action/research and government lookup are mocked.
City gold conversion executes without callbacks. No turn, upkeep, direct
specialist science, difficulty or total research-cost simulation is performed.
"""
from pathlib import Path
import hashlib, json, math, struct, sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import *
SPECS = {
 'engine': ('CTP-og/ctp_program/ctp/civctp.exe','b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79',0x400000),
 'ai': ('CTP-og/ctp_program/ctp/dll/ai/robotcom.dll','3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44',0x20000000),
}
IMAGES={}
for key,(relative,sha,base) in SPECS.items():
 p=ROOT/relative
 if hashlib.sha256(p.read_bytes()).hexdigest()!=sha: raise SystemExit('Revalidate '+key)
 IMAGES[key]=pefile.PE(str(p)).get_memory_mapped_image()
def machine(key):
 u=Uc(UC_ARCH_X86,UC_MODE_32);base=SPECS[key][2];data=IMAGES[key]
 u.mem_map(base,(len(data)+4095)&~4095);u.mem_write(base,data)
 u.mem_map(0x30000000,0x100000);return u
def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def get(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
def read_double(u,a):return struct.unpack('<d',u.mem_read(a,8))[0]
def mock_return(u,value,args):
 sp=u.reg_read(UC_X86_REG_ESP);target=get(u,sp)
 u.reg_write(UC_X86_REG_EAX,value);u.reg_write(UC_X86_REG_ESP,sp+4+args);u.reg_write(UC_X86_REG_EIP,target)

def request(total,known,pending=0):
 u=machine('ai');ai,science,player,vt,stack=[0x30010000+i*0x10000 for i in range(5)]
 put(u,ai+0x120,science);put(u,ai+0x2c,player);put(u,science+0xb0,total);put(u,science+0x64,known);put(u,science+0xb8,pending)
 put(u,player,vt);put(u,vt+0x144,0x300f0000)
 put(u,stack,0x300f1000);put(u,stack+4,ai);put(u,stack+8,0);put(u,stack+12,0)
 u.reg_write(UC_X86_REG_ESP,stack);state={'research_calls':0,'requested':None}
 def hook(_u,address,size,data):
  if address==0x20025d80:state['research_calls']+=1;mock_return(u,0,4)
  elif address==0x300f0000:
   sp=u.reg_read(UC_X86_REG_ESP);state['requested']=read_double(u,sp+8);mock_return(u,0,12)
 u.hook_add(UC_HOOK_CODE,hook);u.emu_start(0x200376d0,0x300f1000,count=1000)
 return state

def capped(requested,cap,old=.2):
 u=machine('engine');player,arr,gov,science,frame=[0x30010000+i*0x10000 for i in range(5)]
 put(u,0xa7dd80,arr);put(u,arr,player);dbl(u,gov+0x168,cap);dbl(u,science,old)
 dbl(u,frame+8,requested);put(u,frame+0x10,0)
 u.reg_write(UC_X86_REG_EAX,gov);u.reg_write(UC_X86_REG_ESI,science);u.reg_write(UC_X86_REG_EBX,0)
 u.reg_write(UC_X86_REG_EBP,frame);u.reg_write(UC_X86_REG_ESP,frame-0x100)
 def hook(_u,address,size,data):
  if address==0x455750:mock_return(u,gov,4)
 u.hook_add(UC_HOOK_CODE,hook);u.emu_start(0x4d302d,0x4d3085,count=1000)
 return read_double(u,science)

def conversion(gold,ratio,fraction,knowledge):
 u=machine('engine');city,player,arr,science,output,stack=[0x30010000+i*0x10000 for i in range(6)]
 put(u,0xa7dd80,arr);put(u,arr,player);put(u,player+0x12e4,science)
 put(u,city+0x1c,gold);dbl(u,city+0x3e0,knowledge);dbl(u,science,fraction)
 put(u,stack,0x300f1000);dbl(u,stack+4,ratio);put(u,stack+12,output);put(u,stack+16,output+8)
 u.reg_write(UC_X86_REG_ESP,stack);u.reg_write(UC_X86_REG_ECX,city)
 u.emu_start(0x49e200,0x300f1000,count=1000)
 return [read_double(u,output),read_double(u,output+8)]

checks=[]
for total,known,pending in [(100,0,0),(100,99,0),(100,100,0),(100,101,0),(100,50,1)]:
 got=request(total,known,pending);expected={'research_calls':int(bool(pending)),'requested':float(total>known)}
 checks.append(dict(kind='ai_request',inputs=[total,known,pending],got=got,expected=expected,passed=got==expected))
for requested,cap in [(1,.5),(1,.6),(1,0),(.3,.6),(.6,.6),(0,.6)]:
 got=capped(requested,cap);expected=min(requested,cap)
 checks.append(dict(kind='engine_cap',inputs=[requested,cap],got=got,expected=expected,passed=math.isclose(got,expected,abs_tol=1e-12)))
for gold,ratio,fraction,knowledge in [(150,1,.5,0),(150,1,.6,.5),(150,.8,.5,.5),(150,1,.5,1),(150,0,.5,.5),(150,1,0,.5)]:
 got=conversion(gold,ratio,fraction,knowledge);cost=gold*ratio*fraction;expected=[cost*(1+knowledge),cost]
 checks.append(dict(kind='city_conversion',inputs=[gold,ratio,fraction,knowledge],got=got,expected=expected,passed=all(math.isclose(a,b,abs_tol=1e-9) for a,b in zip(got,expected))))
print(json.dumps(dict(hashes={k:v[1] for k,v in SPECS.items()},limitations=__doc__,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks)),indent=2))
if not all(c['passed'] for c in checks):raise SystemExit(1)
