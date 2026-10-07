"""Original ration setter and Player getter, synthetic constants/state.

No external callbacks, game start or binary writes. This verifies the scalar
factor, not total city consumption, slider legality or government application.
"""
from pathlib import Path
import hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_ESP
p=ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
sha='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
if hashlib.sha256(p.read_bytes()).hexdigest()!=sha:raise SystemExit('Revalidate engine')
data=pefile.PE(str(p)).get_memory_mapped_image()
checks=[]
for slider,unit,base in [(-2,.25,1),(-1,.25,1),(0,.25,1),(1,.25,1),(2,.25,1),(2,.5,2)]:
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(data)+4095)&~4095);u.mem_write(0x400000,data);u.mem_map(0x30000000,0x100000)
 state,const,player,stack,out=0x30010000,0x30020000,0x30030000,0x300ef000,0x300f2000
 put=lambda a,v:u.mem_write(a,struct.pack('<I',v&0xffffffff))
 dbl=lambda a,v:u.mem_write(a,struct.pack('<d',v))
 put(0xa7dd48,const);dbl(const+0x150,unit);dbl(const+0x158,base)
 put(stack,0x300f1000);put(stack+4,slider)
 u.reg_write(UC_X86_REG_ECX,state);u.reg_write(UC_X86_REG_ESP,stack)
 u.emu_start(0x4cb970,0x300f1000,count=100)
 put(player+0x1318,state);put(stack,0x300f1000)
 u.mem_write(0x300f1000,b'\xdd\x1d'+struct.pack('<I',out))
 u.reg_write(UC_X86_REG_ECX,player);u.reg_write(UC_X86_REG_ESP,stack)
 u.emu_start(0x4c27f0,0x300f1006,count=100)
 got=struct.unpack('<d',u.mem_read(out,8))[0];expected=base+slider*unit
 checks.append(dict(slider=slider,unit=unit,base=base,got=got,expected=expected,passed=got==expected))
print(json.dumps(dict(engine_sha256=sha,limitations=__doc__,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks)),indent=2))
if not all(c['passed'] for c in checks):raise SystemExit(1)
