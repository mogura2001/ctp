"""Execute original population gate/cost branches with synthetic SP state.

No game starts or binary writes. Unit lookup and population removal are mocked;
the actual growth-stock subtraction executes. Does not emulate a complete turn.
"""
from pathlib import Path
import hashlib, json, struct, sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import (
    UC_X86_REG_EAX, UC_X86_REG_EBX, UC_X86_REG_ECX, UC_X86_REG_EDI,
    UC_X86_REG_ESI, UC_X86_REG_EBP, UC_X86_REG_ESP, UC_X86_REG_EIP,
    UC_X86_REG_FPCW,
)

PATH = ROOT / 'CTP-og/ctp_program/ctp/civctp.exe'
SHA = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
if hashlib.sha256(PATH.read_bytes()).hexdigest() != SHA:
    raise SystemExit('Engine changed: revalidate addresses')
image = pefile.PE(str(PATH)).get_memory_mapped_image()

def execute(kind, player_type, population=1, forced=0, cheat=1, stored=350, flag=True):
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(0x400000, (len(image)+4095)&~4095)
    uc.mem_write(0x400000, image)
    uc.mem_map(0x20000000, 0x100000)
    city, queue, player, profile, unit, const = [0x20010000+i*0x2000 for i in range(6)]
    table, frame = 0x20030000, 0x200ef000
    def put(a,v): uc.mem_write(a,struct.pack('<I',v & 0xffffffff))
    def get(a): return struct.unpack('<i',uc.mem_read(a,4))[0]
    put(city+0x58c,population); put(city+0xc,stored); put(city+8,50)
    put(player+4,player_type); put(profile+0x854,cheat)
    put(unit+0x40,0x4000 if flag else 0)
    put(0xa7dd80,table); put(table,player)
    put(0xa7ddc8,profile); put(0xa7dd48,const)
    put(0xa44c9c,0); put(0xa44c98,0)
    uc.mem_write(const+0x328,struct.pack('<d',175.0))
    put(frame+0x1c,forced)
    for reg,value in [(UC_X86_REG_EBP,frame),(UC_X86_REG_ESP,frame-0x100),
                      (UC_X86_REG_EBX,city),(UC_X86_REG_ESI,queue),
                      (UC_X86_REG_EDI,0x3ff00000),
                      (UC_X86_REG_EAX,unit if kind=='gate' else 0)]:
        uc.reg_write(reg,value)
    uc.reg_write(UC_X86_REG_FPCW,0xf7f)
    # RAM-only ftol stand-in, truncating positive constant175 exactly.
    uc.mem_write(0x7256c6,bytes.fromhex('83ec08df3c24585ac3'))
    state={'blocked':False,'removal_requests':0}
    def mock_return(value,args):
        esp=uc.reg_read(UC_X86_REG_ESP)
        target=get(esp)
        uc.reg_write(UC_X86_REG_EAX,value)
        uc.reg_write(UC_X86_REG_ESP,esp+4+args)
        uc.reg_write(UC_X86_REG_EIP,target)
    def hook(machine,address,size,data):
        if address==0x4906df:
            state['blocked']=True; uc.emu_stop()
        elif address==0x4da870:
            mock_return(unit,0)
        elif address==0x496a50:
            state['removal_requests']+=1
            mock_return(0,4)
    uc.hook_add(UC_HOOK_CODE,hook)
    start,end=(0x48f8d7,0x48f94d) if kind=='gate' else (0x48f9be,0x48fa4c)
    uc.emu_start(start,end,count=10000)
    return {'blocked':state['blocked'],'queue_block_flag':get(queue+0x130),
            'growth_food':get(city+0xc),'food_buffer':get(city+8),
            'removal_requests':state['removal_requests']}

def main():
    cases=[]
    for typ in (0,1):
        for pop in (1,2):
            for forced in (0,1):
                blocked=typ!=1 and pop<2 and not forced
                expected={'blocked':bool(blocked),'queue_block_flag':int(blocked),
                          'growth_food':350,'food_buffer':50,'removal_requests':0}
                actual=execute('gate',typ,pop,forced)
                cases.append({'kind':'gate','type':typ,'population':pop,'forced':forced,
                              'actual':actual,'expected':expected,'pass':actual==expected})
    for typ,cheat,stored,flag in [(0,0,350,True),(0,1,350,True),
                                 (1,0,350,True),(1,1,350,True),
                                 (1,0,10,True),(0,1,350,False)]:
        loss=flag and not(typ==1 and cheat)
        expected={'blocked':False,'queue_block_flag':0,
                  'growth_food':max(0,stored-175) if loss else stored,
                  'food_buffer':50,'removal_requests':int(loss)}
        actual=execute('cost',typ,cheat=cheat,stored=stored,flag=flag)
        cases.append({'kind':'cost','type':typ,'cheat':cheat,'stored':stored,'flag':flag,
                      'actual':actual,'expected':expected,'pass':actual==expected})
    result={'engine_sha256':SHA,'checks':len(cases),
            'failures':sum(not c['pass'] for c in cases),'cases':cases}
    output=ROOT/'ANALYSE/BINAIR/food-growth-settler-pop-checks.json'
    output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'checks':result['checks'],'failures':result['failures'],
                      'result_file':str(output)}))
    return bool(result['failures'])

if __name__=='__main__': sys.exit(main())
