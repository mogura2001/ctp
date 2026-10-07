"""Original gold-effect aggregation, income fragment and AI percentage utility.

Synthetic objects, no game starts or disk binary writes. Government lookup is
mocked; imported ftol uses an explicit x87 truncate stub. This does not test
the parser, fees, crime, upkeep, science allocation or full city turns.
"""
from pathlib import Path
import hashlib, json, math, struct, sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from ctp_x87 import ftol_stub
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import *

HASHES = {
    'engine': ('CTP-og/ctp_program/ctp/civctp.exe', 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79', 0x400000),
    'ai': ('CTP-og/ctp_program/ctp/dll/ai/robotcom.dll', '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44', 0x20000000),
}
IMAGES = {}
for key, (relative, sha, base) in HASHES.items():
    path = ROOT / relative
    if hashlib.sha256(path.read_bytes()).hexdigest() != sha:
        raise SystemExit('Binary changed: revalidate ' + key)
    IMAGES[key] = pefile.PE(str(path)).get_memory_mapped_image()

def machine(key):
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    base = HASHES[key][2]; data = IMAGES[key]
    uc.mem_map(base, (len(data)+4095)&~4095); uc.mem_write(base, data)
    uc.mem_map(0x30000000, 0x100000)
    uc.reg_write(UC_X86_REG_FPCW, 0x37f)
    return uc

def put(uc, a, v): uc.mem_write(a, struct.pack('<I', v & 0xffffffff))
def get(uc, a): return struct.unpack('<i', uc.mem_read(a, 4))[0]
def dbl(uc, a, v): uc.mem_write(a, struct.pack('<d', v))
def read_double(uc, a): return struct.unpack('<d', uc.mem_read(a, 8))[0]

def aggregate(records, owned):
    uc = machine('engine')
    db, array, recordbase, out, stack = [0x30010000+i*0x10000 for i in range(5)]
    put(uc, db+0x44, len(records)); put(uc, db+0x10c, array); put(uc, db+8, recordbase)
    for i, (index, kind, bonus) in enumerate(records):
        put(uc, array+i*4, index)
        put(uc, recordbase+index*0x108+0x90, kind)
        dbl(uc, recordbase+index*0x108+0x98, bonus)
    put(uc, stack, 0x300f1000); put(uc, stack+4, owned & 0xffffffff)
    put(uc, stack+8, owned >> 32); put(uc, stack+12, out)
    uc.reg_write(UC_X86_REG_ECX, db); uc.reg_write(UC_X86_REG_ESP, stack)
    uc.emu_start(0x45d730, 0x300f1000, count=10000)
    return [read_double(uc, out+i*8) for i in range(7)]

def gold_fragment(base_gold, modifier, government):
    uc = machine('engine')
    city, player, playerarray, govrecord, frame = [0x30010000+i*0x10000 for i in range(5)]
    put(uc, 0xa7dd80, playerarray); put(uc, playerarray, player)
    dbl(uc, city+0x3d8, modifier); dbl(uc, govrecord+0x130, government)
    uc.reg_write(UC_X86_REG_ESI, city); uc.reg_write(UC_X86_REG_EBX, base_gold)
    uc.reg_write(UC_X86_REG_EBP, frame); uc.reg_write(UC_X86_REG_ESP, frame-0x100)
    stub = 0x300f0000
    uc.mem_write(stub, ftol_stub()); put(uc, 0x743330, stub)
    def hook(_uc, address, size, data):
        if address == 0x455750:
            sp = uc.reg_read(UC_X86_REG_ESP)
            uc.reg_write(UC_X86_REG_EAX, govrecord)
            uc.reg_write(UC_X86_REG_ESP, sp+8)
            uc.reg_write(UC_X86_REG_EIP, get(uc, sp))
    uc.hook_add(UC_HOOK_CODE, hook)
    uc.emu_start(0x4975ba, 0x49760e, count=1000)
    return [get(uc, city+0x1c), get(uc, city+0x24)]

def utility(current_gold, bonus, conversion):
    uc = machine('ai')
    city, effects, stack, returned = [0x30010000+i*0x10000 for i in range(4)]
    put(uc, city+0x54, current_gold); dbl(uc, effects+0x78, bonus)
    dbl(uc, 0x200c5c08, conversion)
    sentinel = 0x300f1000
    uc.mem_write(sentinel, b'\xdd\x1d'+struct.pack('<I', returned))
    put(uc, stack, sentinel); put(uc, stack+4, 0); put(uc, stack+8, effects)
    uc.reg_write(UC_X86_REG_ECX, city); uc.reg_write(UC_X86_REG_ESP, stack)
    uc.emu_start(0x20020390, sentinel+6, count=1000)
    return read_double(uc, returned)

checks = []
for records, owned, expected in [
    ([], 0, [0]*7),
    ([(0,4,.5)], 1, [0,0,0,0,.5,0,0]),
    ([(0,4,.5),(1,4,.5)], 3, [0,0,0,0,1,0,0]),
    ([(0,4,.5),(1,4,.5)], 1, [0,0,0,0,.5,0,0]),
    ([(0,4,.5),(1,5,.25)], 3, [0,0,0,0,.5,.25,0]),
    ([(33,4,.5)], 1<<33, [0,0,0,0,.5,0,0]),
]:
    got = aggregate(records, owned)
    checks.append(dict(kind='aggregation', records=records, owned=owned, got=got,
                       expected=expected, passed=got==expected))
for base_gold, bonus, government in [(150,0,1),(150,.5,1),(150,1,1),(150,.5,1.25),(11,.5,1.25),(0,1,1.25)]:
    expected = math.trunc((base_gold+math.trunc(base_gold*bonus))*government)
    got = gold_fragment(base_gold, bonus, government)
    checks.append(dict(kind='income_fragment', base=base_gold, bonus=bonus,
                       government=government, got=got, expected=expected, passed=got==[expected,expected]))
for gold, bonus, conversion in [(150,.5,1),(300,.5,1),(100,.5,2),(150,0,1),(150,-.5,1)]:
    got = utility(gold, bonus, conversion)
    expected = max(0,bonus)*gold*conversion
    checks.append(dict(kind='ai_percent_utility', gold=gold, bonus=bonus, conversion=conversion,
                       got=got, expected=expected, passed=math.isclose(got,expected,abs_tol=1e-9)))
print(json.dumps(dict(hashes={k:v[1] for k,v in HASHES.items()},
    limitations=__doc__, checks=checks, passed=sum(c['passed'] for c in checks), total=len(checks)), indent=2))
if not all(c['passed'] for c in checks): raise SystemExit(1)
