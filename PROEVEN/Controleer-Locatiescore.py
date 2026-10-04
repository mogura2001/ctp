"""Compare reconstructed settlement formula with original point-function emulation.

Runs only copied code in Unicorn, never starts or alters CTP. Synthetic tile
values exercise arithmetic, not game legality, database loading or AI behavior.
The imported float-to-int helper is intercepted; compare the double BEFORE it.
"""
from pathlib import Path
import sys, struct, math, hashlib, random, json
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EIP, UC_X86_REG_EBP, UC_X86_REG_EAX

PATH = ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
SHA = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
if hashlib.sha256(PATH.read_bytes()).hexdigest() != SHA:
    raise SystemExit('Engine changed: revalidate point-function addresses first')
pe = pefile.PE(str(PATH))
image = pe.get_memory_mapped_image()
OFFSETS = [(x,y) for x in range(-2,3) for y in range(-2,3)
           if (x,y)!=(0,0) and not (abs(x)==2 and abs(y)==2)]

def model(center, tiles, flag=False):
    # Tuple order: production, gold, food, presence/index.
    groups = [[],[],[],[]]
    for a,b,c,d in tiles:
        groups[0 if c<=0 else 1 if c<=5 else 2 if c<=10 else 3].append((a,b,c,d))
    n0,n1,n2 = [len(g) for g in groups[:3]]
    budget = 3*(center[2]-10)/5
    f1 = max(0,min(n2,n1)+budget)/n1 if n1 else 0
    f0 = max(0,n2-min(n2,n1)+budget)/n0 if n0 else 0
    weights = [f0,f1,1,1]
    a = center[0]+sum(w*sum(t[0] for t in g) for w,g in zip(weights,groups))
    b = center[1]+sum(w*sum(t[1] for t in g) for w,g in zip(weights,groups))
    m = 1+sum(t[3]>=0 for t in tiles)+(1.1 if center[1]>5 else 0)
    value = (a+0.33*b)*m+(50 if flag else 0)-(35 if center[2]<5 else 0)
    return value if value>0 else 1

def emulate(center, tiles, flag=False):
    uc=Uc(UC_ARCH_X86,UC_MODE_32)
    uc.mem_map(0x400000,(len(image)+4095)&~4095); uc.mem_write(0x400000,image)
    uc.mem_map(0x20000000,0x100000)
    next_address=0x20010000
    def alloc(data):
        nonlocal next_address
        address=next_address; next_address+=(len(data)+15)&~15
        uc.mem_write(address,data); return address
    def u32(value): return struct.pack('<I',value)
    # World layout: dimensions +0x14, cells +0x1c, flags at each cell +0.
    cell=alloc(u32(0x40000000 if flag else 0)+bytes(28))
    cellrow=alloc(u32(cell)*8); celllayer=alloc(u32(cellrow)*8)
    world=alloc(bytes(64)); uc.mem_write(world+0x14,struct.pack('<hhh',8,8,2))
    uc.mem_write(world+0x1c,u32(alloc(u32(celllayer)*2)))
    uc.mem_write(0xa7dd70,u32(world))
    grid={(4,4):center}; grid.update({(4+x,4+y):t for (x,y),t in zip(OFFSETS,tiles)})
    rows=[]
    for x in range(8):
        rows.append(alloc(b''.join(struct.pack('<bbbb',*grid.get((x,y),(0,0,0,-1))) for y in range(8))))
    working=alloc(u32(alloc(b''.join(u32(a) for a in rows)))*2)
    outrows=[alloc(bytes(16)) for _ in range(8)]
    output=alloc(u32(alloc(b''.join(u32(a) for a in outrows)))*2)
    pos=alloc(struct.pack('<hhh',4,4,0)); sentinel=0x200f0000
    stack=0x200eff00; uc.mem_write(stack,struct.pack('<IIII',sentinel,working,output,pos))
    uc.reg_write(UC_X86_REG_ESP,stack)
    result=[]
    def hook(machine,address,size,data):
        if address==0x5235bb:
            frame=machine.reg_read(UC_X86_REG_EBP)
            value=struct.unpack('<d',machine.mem_read(frame-8,8))[0]
            result.append(value)
            # Conversion is outside this arithmetic test; skip its call.
            machine.reg_write(UC_X86_REG_EAX,int(value)&0xffffffff)
            machine.reg_write(UC_X86_REG_EIP,0x5235c0)
    uc.hook_add(UC_HOOK_CODE,hook)
    uc.emu_start(0x522e00,sentinel,count=100000)
    if len(result)!=1: raise RuntimeError('Point routine did not complete as expected')
    return result[0]

def run_checks():
    rng=random.Random(20261002); failures=[]
    cases=[('uniform', (5,0,10,-1),[(5,0,10,-1)]*20,False),
           ('three_mountains', (5,0,10,-1),[(20,5,0,-1)]*3+[(5,0,10,-1)]*17,False),
           ('three_goods_same_index', (5,0,10,-1),[(5,0,10,0)]*3+[(5,0,10,-1)]*17,False),
           ('three_goods_different_indices', (5,0,10,-1),[(5,0,10,d) for d in [0,1,2]]+[(5,0,10,-1)]*17,False),
           ('three_mountains_only_five_food_surroundings', (5,0,10,-1),[(20,5,0,-1)]*3+[(10,0,5,-1)]*17,False),
           ('three_mountains_three_grass_fourteen_plains', (5,0,10,-1),[(20,5,0,-1)]*3+[(5,0,10,-1)]*3+[(10,0,5,-1)]*14,False),
           ('three_mountains_three_food10_rest_zero', (5,0,10,-1),[(20,5,0,-1)]*3+[(5,0,10,-1)]*3+[(0,0,0,-1)]*14,False),
           ('three_mountains_three_food20_rest_zero', (5,0,10,-1),[(20,5,0,-1)]*3+[(5,0,20,-1)]*3+[(0,0,0,-1)]*14,False)]
    for i in range(60):
        tile=lambda:(rng.randrange(0,41),rng.randrange(0,16),rng.choice([0,3,5,8,10,15,20]),rng.choice([-1,-1,0,1]))
        cases.append((f'random_{i}',tile(),[tile() for _ in range(20)],bool(i%2)))
    examples=[]
    for name,center,tiles,flag in cases:
        expected=model(center,tiles,flag); actual=emulate(center,tiles,flag)
        if not math.isclose(expected,actual,rel_tol=1e-10,abs_tol=1e-8):
            failures.append({'case':name,'model':expected,'machine':actual,'center':center,'tiles':tiles,'flag':flag})
        if not name.startswith('random'):examples.append({'case':name,'model':expected,'machine':actual})
    print(json.dumps({'binary_sha256':SHA,'checks':len(cases),'failures':failures,'examples':examples},indent=2))
    return bool(failures)

if __name__=='__main__':sys.exit(run_checks())
