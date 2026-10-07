"""Run the original internal-route benefit fragment on synthetic objects.

No gameplay or binary writes. Position, database value, city-count getters and
remaining rounds are mocked. The original x87 arithmetic and filters execute.
This does not verify route creation or actual trade/economy outcomes.
"""
from pathlib import Path
import hashlib, json, math, struct, sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EBX, UC_X86_REG_ECX, UC_X86_REG_EDI, UC_X86_REG_ESI, UC_X86_REG_EBP, UC_X86_REG_ESP, UC_X86_REG_EIP

DLL = ROOT / 'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll'
SHA = '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
if hashlib.sha256(DLL.read_bytes()).hexdigest() != SHA:
    raise SystemExit('AI binary changed: revalidate addresses')
IMAGE = pefile.PE(str(DLL)).get_memory_mapped_image()

def execute(source, destination, value=10, conversion=1, rounds=20, layer=0, source_local=None, destination_local=None):
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(0x20000000, (len(IMAGE)+4095)&~4095)
    uc.mem_write(0x20000000, IMAGE)
    uc.mem_map(0x30000000, 0x100000)
    goal, ai, origin, dest, player, goods, pv, gv = [0x30010000+i*0x1000 for i in range(8)]
    frame, output = 0x300ef000, 0x30090000
    count_stub, value_stub = 0x30080000, 0x30080100
    def put(a,v): uc.mem_write(a,struct.pack('<I',v))
    def get(a): return struct.unpack('<I',uc.mem_read(a,4))[0]
    def double(a,v): uc.mem_write(a,struct.pack('<d',v))
    put(goal,0); put(goal+0x28,origin); put(origin+0xc,1); put(dest+0xc,2)
    put(ai+0x2c,player); put(ai+0x54,goods); put(ai+0x84,0x30070000)
    put(player,pv); put(pv+0xb8,count_stub); put(goods,gv); put(gv+0xc,value_stub)
    for offset,v in [(8,ai),(0xc,dest),(0x10,output),(0x14,output+8)]: put(frame+offset,v)
    double(0x200c5c08,conversion)
    # Return a synthetic double from the round-estimate callback, in RAM only.
    double(0x30071000,rounds)
    uc.mem_write(0x20008840,bytes.fromhex('dd0500100730c3'))
    for reg,v in [(UC_X86_REG_ESI,goal),(UC_X86_REG_EBX,dest),(UC_X86_REG_EBP,frame),(UC_X86_REG_ESP,frame-0x100)]:uc.reg_write(reg,v)
    state={'rejected':False,'counts_read':[]}
    def ret(v,args):
        sp=uc.reg_read(UC_X86_REG_ESP);addr=get(sp)
        uc.reg_write(UC_X86_REG_EAX,v);uc.reg_write(UC_X86_REG_ESP,sp+4+args)
        uc.reg_write(UC_X86_REG_EIP,addr)
    def hook(_uc,address,size,data):
        sp=uc.reg_read(UC_X86_REG_ESP)
        if address==0x2001c380:
            uc.mem_write(get(sp+4),struct.pack('<hhh',0,0,layer));ret(0,4)
        elif address==value_stub:ret(value,8)
        elif address==count_stub:
            city=get(sp+0xc);n=source if city==1 else destination
            local=source_local if city==1 else destination_local
            put(get(sp+8),0);put(get(sp+0x14),n if local is None else local);put(get(sp+0x18),n)
            state['counts_read'].append(city);ret(0,24)
        elif address in [0x20048418,0x2004834a]:
            state['rejected']=address==0x2004834a;uc.emu_stop()
    uc.hook_add(UC_HOOK_CODE,hook)
    uc.emu_start(0x200482cc,0,count=1000)
    state['benefit']=struct.unpack('<d',uc.mem_read(output,8))[0]
    return state

cases=[]
for source,dest in [(1,0),(1,1),(1,2),(1,4),(2,0),(2,1),(2,2),(3,1),(3,3),(5,5)]:
    got=execute(source,dest);expected=(dest+1-source)*10*20
    cases.append({'source':source,'destination':dest,'expected':expected,'got':got,'passed':not got['rejected'] and math.isclose(got['benefit'],expected,abs_tol=1e-9)})
for params in [dict(source=1,destination=4,value=12,conversion=2.5,rounds=7),dict(source=1,destination=2,rounds=0),dict(source=1,destination=4,source_local=3,destination_local=1)]:
    got=execute(**params);expected=(params['destination']+1-params['source'])*params.get('value',10)*params.get('conversion',1)*params.get('rounds',20)
    cases.append({'params':params,'expected':expected,'got':got,'passed':math.isclose(got['benefit'],expected,abs_tol=1e-9)})
for params in [dict(source=0,destination=4),dict(source=1,destination=4,layer=1)]:
    got=execute(**params);cases.append({'params':params,'got':got,'passed':got['rejected'] and got['benefit']<0})
ENGINE = ROOT / 'CTP-og/ctp_program/ctp/civctp.exe'
ENGINE_SHA = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
if hashlib.sha256(ENGINE.read_bytes()).hexdigest() != ENGINE_SHA:
    raise SystemExit('Engine changed: revalidate addresses')
engine_image = pefile.PE(str(ENGINE)).get_memory_mapped_image()

def engine_goods_sum(counts):
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(0x400000, (len(engine_image)+4095)&~4095)
    uc.mem_write(0x400000, engine_image)
    uc.mem_map(0x30000000,0x100000)
    city,db,array,record,stack = 0x30010000,0x30020000,0x30030000,0x30040000,0x300ef000
    def put(a,v):uc.mem_write(a,struct.pack('<I',v&0xffffffff))
    def get(a):return struct.unpack('<I',uc.mem_read(a,4))[0]
    put(0xa7ddd0,db);put(db,len(counts));put(city+0x5b8,array);put(record+0x30,10)
    for i,n in enumerate(counts):put(array+4*i,n)
    uc.reg_write(UC_X86_REG_ECX,city);uc.reg_write(UC_X86_REG_ESP,stack)
    state={}
    def hook(_uc,address,size,data):
        if address==0x456540:
            sp=uc.reg_read(UC_X86_REG_ESP);uc.reg_write(UC_X86_REG_EAX,record)
            uc.reg_write(UC_X86_REG_ESP,sp+8);uc.reg_write(UC_X86_REG_EIP,get(sp))
        elif address==0x49724a:
            state['gold']=get(uc.reg_read(UC_X86_REG_EBP)-4);uc.emu_stop()
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(0x4971f0,0,count=2000)
    return state['gold']

engine_cases=[]
for counts in [[0],[1],[2],[5],[1,1,1,1,1],[2,3],[0,4],[-1]]:
    expected=sum(max(0,n)*(max(0,n)+1)//2*10 for n in counts)
    got=engine_goods_sum(counts)
    engine_cases.append({'counts':counts,'expected_goods_component':expected,'got':got,'passed':got==expected})
report={'ai_sha256':SHA,'engine_sha256':ENGINE_SHA,'checks':len(cases)+len(engine_cases),'failures':sum(not c['passed'] for c in cases+engine_cases),'cases':cases,'engine_cases':engine_cases}
print(json.dumps(report,indent=2))
raise SystemExit(bool(report['failures']))
