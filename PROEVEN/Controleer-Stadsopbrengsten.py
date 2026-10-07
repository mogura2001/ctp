"""Execute original crime calculation and positional city yield getters.

Synthetic databases/city state. Crime with no wonder uses original callees
without mocks; nonzero wonder reduction uses one explicit percentage stub.
Yield getters mock World raw yield/type and food-wonder percentage, and use
an x87 truncate stub for the imported ftol. This does not verify real world
construction, happiness assembly, total consumption, full city turns or UI.
"""
from pathlib import Path
import hashlib, json, math, struct, sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from ctp_x87 import ftol_stub
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import *

PATH = ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
HASH = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
assert hashlib.sha256(PATH.read_bytes()).hexdigest() == HASH
PE = pefile.PE(str(PATH)); IMAGE = PE.get_memory_mapped_image()
CITY, PLAYER, HAPPY, GOVDB, GOV, BUILDS, RECORDS, INDICES, WONDERS, HISTORY, SLIDERS, ARRAY, POINT, CONST = [
    0x30010000+i*0x4000 for i in range(14)]
STACK, STOP, OUT = 0x300e0000, 0x300f0000, 0x300f1000

def put(u,a,v): u.mem_write(a,struct.pack('<I',v & 0xffffffff))
def dbl(u,a,v): u.mem_write(a,struct.pack('<d',v))
def number(u,a): return struct.unpack('<d',u.mem_read(a,8))[0]

def fixture():
    u=Uc(UC_ARCH_X86,UC_MODE_32)
    u.mem_map(0x400000,(len(IMAGE)+4095)&~4095);u.mem_write(0x400000,IMAGE)
    u.mem_map(0x30000000,0x100000);u.reg_write(UC_X86_REG_FPCW,0x37f)
    for addr, value in [(0xa7dd34,GOVDB),(0xa7dd1c,BUILDS),(0xa7dd5c,WONDERS),
                        (0xa7dd80,ARRAY),(0xa7dd48,CONST),(ARRAY,PLAYER),
                        (GOVDB,1),(GOVDB+8,GOV),(BUILDS+8,RECORDS),
                        (PLAYER+0x1318,SLIDERS),(CITY+0x5cc,HAPPY),(HAPPY+0xbc,HISTORY)]:
        put(u,addr,value)
    u.mem_write(STOP,b'\xdd\x1d'+struct.pack('<I',OUT))
    return u

def run(u,address,obj,args=()):
    put(u,STACK,STOP)
    for i,arg in enumerate(args):put(u,STACK+4+i*4,arg)
    u.reg_write(UC_X86_REG_ECX,obj);u.reg_write(UC_X86_REG_ESP,STACK)
    u.emu_start(address,STOP+6,count=30000)
    return number(u,OUT)

def return_int(u,value,argbytes):
    sp=u.reg_read(UC_X86_REG_ESP)
    dest=struct.unpack('<I',u.mem_read(sp,4))[0]
    u.reg_write(UC_X86_REG_EAX,value & 0xffffffff)
    u.reg_write(UC_X86_REG_ESP,sp+4+argbytes);u.reg_write(UC_X86_REG_EIP,dest)

def crime(happiness,coef=1,offset=85,records=(),owned=0,wonder=0):
    u=fixture();dbl(u,HAPPY,happiness);dbl(u,GOV+0xe8,coef);dbl(u,GOV+0xf0,offset)
    put(u,BUILDS+0x80,len(records));put(u,BUILDS+0x148,INDICES)
    put(u,CITY+0x48,owned);put(u,CITY+0x4c,owned>>32)
    for i,(index,multiplier) in enumerate(records):
        put(u,INDICES+i*4,index);dbl(u,RECORDS+index*0x108+0xb8,multiplier)
    if wonder:
        def hook(uc,address,size,data):
            if address==0x4721c0:return_int(uc,wonder,8)
        u.hook_add(UC_HOOK_CODE,hook)
    got=run(u,0x4aafe0,HAPPY,(CITY,PLAYER))
    return got,number(u,HAPPY+0xb0)

def yields(raw,terrainadd=0,flat=0,percent=0,work=1,loss=0,wonder=0):
    u=fixture();dbl(u,HAPPY+0xb0,loss);dbl(u,SLIDERS,work)
    for offset in (0x100+2*28,0x104+2*28):put(u,CITY+offset,terrainadd)
    for offset in (0x3a0,0x3a4):put(u,CITY+offset,flat)
    for offset in (0x3c0,0x3c8):dbl(u,CITY+offset,percent)
    stub=0x300f2000
    u.mem_write(stub,ftol_stub());put(u,0x743330,stub)
    def hook(uc,address,size,data):
        if address in (0x510f70,0x510fd0):return_int(uc,raw,4)
        elif address==0x516bc0:return_int(uc,2,8)
        elif address==0x473f40:return_int(uc,wonder,8)
    u.hook_add(UC_HOOK_CODE,hook)
    food=run(u,0x495250,CITY,(POINT,))
    production=run(u,0x495330,CITY,(POINT,))
    return food,production

checks=[]
for h,c,o,recs,owned,w in [
    (90,1,85,(),0,0),(85,1,85,(),0,0),(75,1,85,(),0,0),
    (60,1,85,(),0,0),(-30,1,85,(),0,0),(75,.5,85,(),0,0),
    (75,1.25,85,(),0,0),(75,1,80,(),0,0),
    (65,1,85,((0,.5),),1,0),(65,1,85,((0,.5),(1,.5)),3,0),
    (65,1,85,((0,.5),(1,.5)),1,0),(65,1,85,((33,.5),),1<<33,0),
    (65,1,85,(),0,50),(65,1,85,(),0,100),
]:
    reduction=math.prod(m for i,m in recs if owned & (1<<i))
    expected=max(0,min(1,(o-h)*c*reduction*(1-w/100)/100)) if h<o else 0
    got=crime(h,c,o,recs,owned,w)
    checks.append(dict(kind='crime',happiness=h,coefficient=c,offset=o,buildings=recs,
        owned=owned,wonder=w,got=got,expected=expected,
        passed=all(math.isclose(v,expected,abs_tol=1e-9) for v in got)))
for args in [(20,0,0,0,1,0,0),(20,5,3,.5,1,0,0),(11,0,0,.5,1,0,0),
             (35,0,0,0,1,.1,0),(35,0,0,0,.75,.1,0),(20,0,0,0,1,0,25),
             (35,0,0,0,1,1,0)]:
    raw,terrainadd,flat,pct,work,loss,wonder=args
    basis=raw+terrainadd+flat
    before=(basis+math.trunc(basis*pct))*work
    expected=(basis*(1+pct)*(1+wonder/100)*(1-loss),
              math.trunc(before-math.trunc(before*loss)))
    got=yields(*args)
    checks.append(dict(kind='yield_getters',arguments=args,got=got,expected=expected,
        passed=all(math.isclose(a,b,abs_tol=1e-9) for a,b in zip(got,expected))))
for slider in range(-2,3):
    u=fixture();dbl(u,CONST+0x130,.25);dbl(u,CONST+0x138,1)
    run(u,0x4cb8c0,SLIDERS,(slider,))
    got=run(u,0x4c2500,PLAYER);expected=1-.25*slider
    checks.append(dict(kind='workday',slider=slider,got=got,expected=expected,passed=got==expected))
report=dict(engine_sha256=HASH,limitations=__doc__,checks=checks,
            passed=sum(c['passed'] for c in checks),total=len(checks))
print(json.dumps(report,indent=2))
if not all(c['passed'] for c in checks):raise SystemExit(1)
