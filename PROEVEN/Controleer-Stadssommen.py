"""Original full food loop, inline turn consumption and production sum.

Synthetic city/players. World position/yield/type, population properties,
building-cache refresh and wonder queries are explicit mocks. Government,
workday/ration getters and arithmetic execute original instructions. Imported
ftol/floor are x87 stubs with explicit rounding modes. Stops before growth;
does not test real placement, database parsing, happiness, PW or a game turn.
"""
from pathlib import Path
import hashlib,json,math,struct,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from ctp_x87 import ftol_stub, floor_stub
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
HASH='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
p=ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
assert hashlib.sha256(p.read_bytes()).hexdigest()==HASH
pe=pefile.PE(str(p));data=pe.get_memory_mapped_image()
CITY,PLAYER,ARRAY,HAPPY,SLIDERS,GOVDB,GOV,POPS,STACK,FRAME,OUT1,OUT2 = [
    0x30010000+i*0x8000 for i in range(12)]
STOP=0x300f0000

def put(u,a,v):u.mem_write(a,struct.pack('<I',v&0xffffffff))
def dbl(u,a,v):u.mem_write(a,struct.pack('<d',v))
def word(u,a):return struct.unpack('<I',u.mem_read(a,4))[0]
def number(u,a):return struct.unpack('<d',u.mem_read(a,8))[0]

def evaluate(center,populations,loss=0,foodpct=0,prodpct=0,work=1,ration=1,govprod=1,foodwonder=0,prodwonder=0):
    u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(data)+4095)&~4095)
    u.mem_write(0x400000,data);u.mem_map(0x30000000,0x100000)
    u.reg_write(UC_X86_REG_FPCW,0x37f)
    for a,v in [(0xa7dd80,ARRAY),(ARRAY,PLAYER),(0xa7dd34,GOVDB),
                (GOVDB,1),(GOVDB+8,GOV),(CITY+0x5cc,HAPPY),
                (PLAYER+0x1318,SLIDERS),(CITY+0x58c,len(populations)),(CITY+0x590,POPS),
                (CITY+0xb0,-1)]:put(u,a,v)
    dbl(u,HAPPY+0xb0,loss);dbl(u,SLIDERS,work);dbl(u,SLIDERS+8,ration)
    dbl(u,GOV+0x138,govprod);dbl(u,CITY+0x3c0,prodpct);dbl(u,CITY+0x3c8,foodpct)
    # Imported truncation and floor, retaining the original caller's ABI.
    put(u,0x743330,0x300f2000);u.mem_write(0x300f2000,ftol_stub())
    u.mem_write(0x300f2100,floor_stub());put(u,0x74335c,0x300f2100)
    calls=[]
    def ret(value,argbytes=0):
        sp=u.reg_read(UC_X86_REG_ESP);dest=word(u,sp)
        u.reg_write(UC_X86_REG_EAX,value&0xffffffff)
        u.reg_write(UC_X86_REG_ESP,sp+4+argbytes);u.reg_write(UC_X86_REG_EIP,dest)
    def hook(uc,address,size,unused):
        sp=u.reg_read(UC_X86_REG_ESP);obj=u.reg_read(UC_X86_REG_ECX)
        if address==0x4da9a0:
            uc.mem_write(word(uc,sp+4),struct.pack('<hhh',0,0,0));ret(0,4)
        elif address==0x516bc0:ret(2,8)
        elif address in (0x510f70,0x510fd0):
            point=word(uc,sp+4);idx=struct.unpack('<h',uc.mem_read(point,2))[0]
            tile=center if idx==0 else populations[idx-1]['tile']
            ret(tile[0 if address==0x510f70 else 1],4)
        elif address in (0x4cca70,0x4ccb30,0x4ccbc0,0x4ccb60,0x4ccaa0):
            idx=(obj-POPS)//4;pop=populations[idx]
            if address==0x4cca70:ret(int(pop['tile'] is not None))
            elif address==0x4ccb30:
                uc.mem_write(word(uc,sp+4),struct.pack('<hhh',idx+1,0,0));ret(0,4)
            elif address==0x4ccaa0:ret(pop['hunger'])
            else:ret(pop.get('bonus_food' if address==0x4ccbc0 else 'bonus_prod',0))
        elif address in (0x473f40,0x473e50,0x474230,0x4721c0):
            ret(foodwonder if address==0x473f40 else prodwonder if address==0x473e50 else 0,8)
        elif address in (0x45d540,0x45d6b0,0x45d730):
            calls.append(hex(address));ret(0,12)
    u.hook_add(UC_HOOK_CODE,hook)
    def run(address,args):
        put(u,STACK,STOP)
        for i,v in enumerate(args):put(u,STACK+4+i*4,v)
        u.reg_write(UC_X86_REG_ECX,CITY);u.reg_write(UC_X86_REG_ESP,STACK)
        u.emu_start(address,STOP,count=30000)
    run(0x494280,(OUT1,OUT2,1));production=word(u,CITY+0x40)
    run(0x494970,(CITY+0xfc,))
    beforecrime=number(u,CITY+0x60);aftercrime=number(u,CITY+0x68);foodloss=number(u,CITY+0x70)
    # Inline consumption from actual turn routine; stop before growth call.
    u.reg_write(UC_X86_REG_ESI,CITY);u.reg_write(UC_X86_REG_EDI,0)
    u.reg_write(UC_X86_REG_EBP,FRAME);u.reg_write(UC_X86_REG_ESP,FRAME-0x100)
    u.emu_start(0x498205,0x498298,count=20000)
    return dict(production=production,food_before_crime=beforecrime,food_after_crime=aftercrime,
                crime_food_loss=foodloss,consumption=number(u,CITY+0x78),net_food=number(u,CITY+0x58),cache_refresh_calls=calls)

def expected(center,pops,loss,fp,pp,work,ration,gp,fw,pw):
    f=(center[0]+sum(p['tile'][0] if p['tile'] is not None else p.get('bonus_food',0) for p in pops))*(1+fp)
    f-=math.trunc(-fw*f/100)
    fl=math.floor(f*loss);after=f-fl;cons=sum(max(0,p['hunger'])*ration for p in pops)
    p=center[1]+sum(p['tile'][1] if p['tile'] is not None else p.get('bonus_prod',0) for p in pops)
    p+=math.trunc(p*pp);p=math.trunc(p*work);p+=math.trunc(p*pw/100);p=math.trunc(p*gp)
    p-=math.trunc(p*loss)
    return dict(production=p,food_before_crime=f,food_after_crime=after,
                crime_food_loss=fl,consumption=cons,net_food=after-cons)

base=[dict(tile=(0,35),hunger=10) for _ in range(3)]+[dict(tile=(25,0),hunger=10)]
special=base[:2]+[dict(tile=None,hunger=10,bonus_food=2,bonus_prod=3),base[3]]
checks=[]
for name,center,pops,loss,fp,pp,work,ration,gp,fw,pw in [
    ('four_pop_maintenance',(20,5),base,0,0,0,1,1,1.25,0,0),
    ('four_pop_crime',(20,5),base,.1,0,0,1,1,1.25,0,0),
    ('poor_center_deficit',(10,5),base,0,0,0,1,1,1.25,0,0),
    ('ration_half',(10,5),base,0,0,0,1,.5,1.25,0,0),
    ('short_workday',(20,5),base,.1,0,0,.75,1,1.25,0,0),
    ('building_percent',(20,5),base,.1,.5,.5,1,1,1.25,0,0),
    ('specialist',(20,5),special,0,0,0,1,1,1,0,0),
    ('wonders',(20,5),base,.1,0,0,1,1,1,25,25),
    ('empty_city',(20,5),[],0,0,0,1,1,1,0,0),
    ('nonpositive_hunger',(20,5),[dict(tile=(25,0),hunger=-1)],0,0,0,1,1,1,0,0),
]:
    args=(center,pops,loss,fp,pp,work,ration,gp,fw,pw)
    got=evaluate(*args);exp=expected(*args)
    checks.append(dict(name=name,inputs=dict(center=center,populations=pops,crime=loss,food_percent=fp,
        production_percent=pp,workday=work,ration=ration,government_production=gp,food_wonder=fw,prod_wonder=pw),
        got=got,expected=exp,passed=all(math.isclose(got[k],v,abs_tol=1e-9) for k,v in exp.items())))
print(json.dumps(dict(engine_sha256=HASH,limitations=__doc__,checks=checks,
                     passed=sum(c['passed'] for c in checks),total=len(checks)),indent=2))
if not all(c['passed'] for c in checks):raise SystemExit(1)
