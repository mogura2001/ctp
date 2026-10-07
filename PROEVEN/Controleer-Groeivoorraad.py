"""Offline execution of original EatFood positive-growth instructions.

Synthetic ordinary cities, no slaves/difficulty/high-happiness modifiers. Database
lookups and population creation are mocked; imported ftol is replaced by x87
truncate conversion. Checks growth-food retention, not a complete game turn.
Never starts the game or writes its binaries.
"""
from pathlib import Path
import hashlib, json, struct, sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from ctp_x87 import ftol_stub
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EBP, UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_ESI, UC_X86_REG_FPCW

PATH = ROOT / 'CTP-og/ctp_program/ctp/civctp.exe'
SHA = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
if hashlib.sha256(PATH.read_bytes()).hexdigest() != SHA:
    raise SystemExit('Engine changed: revalidate addresses first')
pe = pefile.PE(str(PATH))
image = pe.get_memory_mapped_image()

def emulate(population, stored, surplus, silo, *, player_type=1, difficulty_bonus=0.0,
            happiness=75, network_active=False, network_remote=False):
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(0x400000, (len(image)+4095)&~4095)
    uc.mem_write(0x400000, image)
    uc.mem_map(0x20000000, 0x100000)
    city, const, unit, poprecord, player = [0x20010000+i*0x1000 for i in range(5)]
    frame = 0x200ef000
    def put32(a,v): uc.mem_write(a, struct.pack('<I',v & 0xffffffff))
    def get32(a): return struct.unpack('<i',uc.mem_read(a,4))[0]
    put32(city+0xc,stored)
    put32(city+0x58c,population)
    put32(city+0x590,0x20018000)
    uc.mem_write(city+0x58,struct.pack('<d',surplus))
    uc.mem_write(const+0x328,struct.pack('<d',175.0))
    uc.mem_write(unit+0x2a0,struct.pack('<d',1.0))
    put32(0xa7dd48,const)
    put32(0xa7dd80,0x20019000)
    put32(0x20019000,player)
    # Explicit context; the default retains the original ordinary-AI fixture.
    put32(player+4,player_type)
    put32(0xa44c9c,int(network_active));put32(0xa44c98,int(network_active))
    difficulty_table, setting, happy_object = 0x20020000,0x20025000,0x20026000
    put32(0xa7dd54,difficulty_table);put32(0xa7a6a4,setting);put32(setting,5)
    uc.mem_write(difficulty_table+5*0x200+0x1d8,struct.pack('<d',difficulty_bonus))
    put32(city+0x5cc,happy_object);put32(const+0x16c,85)
    uc.mem_write(happy_object,struct.pack('<d',happiness))
    put32(frame-0x1c,int(silo))
    put32(frame-0x20,50 if silo else 0)
    uc.reg_write(UC_X86_REG_EBP,frame)
    uc.reg_write(UC_X86_REG_ESP,frame-0x80)
    uc.reg_write(UC_X86_REG_ESI,city)
    uc.reg_write(UC_X86_REG_FPCW,0x37f)
    # _ftol import substitute: x87 integer conversion truncating toward zero.
    stub = 0x200f0000
    uc.mem_write(stub,ftol_stub())
    put32(0x743330,stub)
    growth_calls = []
    def return_mock(value,args):
        esp = uc.reg_read(UC_X86_REG_ESP)
        target = struct.unpack('<I',uc.mem_read(esp,4))[0]
        uc.reg_write(UC_X86_REG_EAX,value)
        uc.reg_write(UC_X86_REG_ESP,esp+4+args)
        uc.reg_write(UC_X86_REG_EIP,target)
    def hook(machine,address,size,data):
        if address == 0x4cc980: return_mock(0,0) # citizen type
        elif address == 0x456b70: return_mock(poprecord,4) # non-slave
        elif address == 0x4da870: return_mock(unit,0) # city unit record
        elif address == 0x579f60: return_mock(int(network_remote),4) # explicit network predicate
        elif address == 0x4da9a0: return_mock(0,4) # position output irrelevant here
        elif address == 0x496440:
            growth_calls.append(get32(city+0xc))
            put32(city+0x58c,get32(city+0x58c)+1)
            return_mock(1,12)
    uc.hook_add(UC_HOOK_CODE,hook)
    uc.emu_start(0x494fde,0x49522c,count=10000)
    return {'population':get32(city+0x58c), 'growth_food':get32(city+0xc),
            'food_buffer':get32(city+8), 'growth_calls':len(growth_calls)}

def checks():
    cases = []
    for n in (1,2,4):
        for silo in (False,True):
            for extra in (-1,0,23,175*(n+2)):
                stored = 175*n-10+extra
                actual = emulate(n,stored,10,silo)
                grows = stored+10 >= 175*n
                expected = {'population':n+int(grows),
                    'growth_food': (175*(n+1)//2 if silo else stored+10-175*n) if grows else stored+10,
                    'food_buffer':10 if silo else 0, 'growth_calls':int(grows)}
                cases.append({'initial_population':n,'silo':silo,'initial_growth_food':stored,
                              'surplus':10,'expected':expected,'actual':actual,'pass':actual==expected})
    result = {'binary_sha256':SHA,'original_range':'494fde..49522c','checks':len(cases),
              'failures':sum(not c['pass'] for c in cases),'cases':cases}
    print(json.dumps(result,indent=2))
    return bool(result['failures'])

if __name__ == '__main__': sys.exit(checks())
