"""Read-only execution of original terrain selectors, tile yields and upgrade deltas.

Synthetic world/record data; no parser, city modifiers, allocation or game session.
All tested engine instructions and their internal callees execute without mocks.
"""
from pathlib import Path
import hashlib
import json
import struct
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_ESP, UC_X86_REG_EIP

PATH = ROOT / 'CTP-og/ctp_program/ctp/civctp.exe'
HASH = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
assert hashlib.sha256(PATH.read_bytes()).hexdigest() == HASH
PE = pefile.PE(str(PATH))
BASE = PE.OPTIONAL_HEADER.ImageBase
MEM = 0x30000000
WORLD, LAYERS, COLUMNS, ROWS, DB, RECORDS, ENVS, CELL, POINT = [MEM+x for x in
    (0x1000, 0x1100, 0x1200, 0x1300, 0x2000, 0x3000, 0x5000, 0x7000, 0x8000)]
STOP, STACK = MEM+0xff000, MEM+0xe0000


def word(uc, address, value=None):
    if value is None:
        return struct.unpack('<I', uc.mem_read(address, 4))[0]
    uc.mem_write(address, struct.pack('<I', value & 0xffffffff))


def fixture(flags=0, terrain=4, missing=(), city=False, good=False):
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(BASE, (PE.OPTIONAL_HEADER.SizeOfImage+4095) & ~4095)
    uc.mem_write(BASE, PE.get_memory_mapped_image())
    uc.mem_map(MEM, 0x100000)
    word(uc, 0xa7dd3c, DB)
    word(uc, DB, 24)
    word(uc, DB+8, RECORDS)
    word(uc, 0xa7dd70, WORLD)
    word(uc, WORLD+0x1c, LAYERS)
    word(uc, LAYERS, COLUMNS)
    word(uc, COLUMNS, ROWS)
    word(uc, ROWS, CELL)
    uc.mem_write(0xa7df20, struct.pack('<hh', 16, 16))
    uc.mem_write(CELL+0xd, bytes([terrain]))
    word(uc, CELL, flags | (0x40 if good else 0))
    record = RECORDS+terrain*0xc0
    base = (0,20,5) if terrain in (8,20,22) else (10,5,0)
    for offset,value in zip((8,12,0x44),base): word(uc,record+offset,value)
    for i,(offset,food,prod,gold) in enumerate([
        (0x68,5,0,0),(0x6c,15,0,0),(0x70,25,0,0),
        (0x5c,0,2,1),(0x60,0,4,2),(0x64,0,6,3),
        (0x74,0,15,5),(0x78,0,30,10),(0x7c,0,45,15),
        (0x58,5,5,5),(0x54,3,3,3),(0x50,10,5,0),
    ]):
        env=ENVS+i*0x80
        if offset not in missing:
            word(uc,record+offset,env)
        word(uc,env,food)
        word(uc,env+4,prod)
        word(uc,env+0x3c,gold)
    if city: word(uc,CELL+0x14,1)
    if good:
        replacement=ENVS+0x800
        word(uc,record+0xa0,replacement)
        word(uc,replacement+8,18)
        word(uc,replacement+0xc,12)
        word(uc,replacement+0x44,7)
    return uc


checks=[]


def run(label, address, args, expected, *, receiver=DB, out=None, **setup):
    uc=fixture(**setup)
    word(uc,STACK,STOP)
    for i,arg in enumerate(args): word(uc,STACK+4+i*4,arg)
    uc.reg_write(UC_X86_REG_ESP,STACK)
    uc.reg_write(UC_X86_REG_ECX,receiver)
    uc.emu_start(address,STOP,count=10000)
    assert uc.reg_read(UC_X86_REG_EIP)==STOP
    got=word(uc,out) if out is not None else uc.reg_read(UC_X86_REG_EAX)
    if got>=0x80000000: got-=0x100000000
    checks.append(dict(label=label,engine_entry=hex(address),got=got,
                       expected=expected,passed=got==expected))


for kind,address,values in [
    ('food',0x468aa0,[5,15,25,0,0,0,0,0,0,3,10]),
    ('production',0x468a00,[0,0,0,2,4,6,15,30,45,3,5]),
]:
    for index,expected in enumerate(values):
        run(f'{kind}_absolute_selector_{index}',address,[index,4],expected)
    run(f'{kind}_missing_level_returns_zero',address,[1,4],0,missing=(0x6c,))

run('food_upgrade_subtracts_previous_farm',0x468b40,[POINT,1,0],10,flags=4)
run('food_level3_subtracts_previous_level2',0x468b40,[POINT,2,0],10,flags=8)
run('new_farm_delta',0x468b40,[POINT,0,0],5)
run('mine_food_delta_does_not_subtract_other_family_farm',0x468b40,[POINT,6,0],0,flags=4)
run('same_farm_has_no_food_increment',0x468b40,[POINT,0,0],0,flags=4)
run('production_upgrade_subtracts_previous_mine',0x468840,[POINT,7,0],15,flags=16)
run('farm_production_delta_does_not_subtract_other_family_mine',0x468840,[POINT,0,0],0,flags=16)
run('mine_delta_on_tile_with_farm',0x468840,[POINT,6,0],15,flags=4)
run('same_mine_has_no_production_increment',0x468840,[POINT,6,0],0,flags=16)

run('raw_grassland_food',0x500110,[],10,receiver=CELL)
run('farm2_additive_food',0x500110,[],25,receiver=CELL,flags=8)
run('river_additive_food',0x500110,[],15,receiver=CELL,flags=0x800)
run('canal_tunnel_additive_food',0x500110,[],13,receiver=CELL,flags=0x200)
run('road1_additive_production',0x500290,[],7,receiver=CELL,flags=1)
run('city_bonus_additive_food',0x500110,[],20,receiver=CELL,city=True)
run('mountain_mine1_production',0x500290,[],35,receiver=CELL,terrain=8,flags=16)
run('mountain_mine1_gold',0x5003a0,[],10,receiver=CELL,terrain=8,flags=16)
run('good_record_overrides_base_food',0x500110,[],18,receiver=CELL,good=True)
run('terrain_world_wrapper_uses_canonical_type20',0x5342e0,[MEM+0x9000,POINT,MEM+0x9100],20,
    terrain=20,out=MEM+0x9100)

print(json.dumps(dict(engine_sha256=HASH,
    limitations=['Synthetic record/world fixture; no engine parser.',
                 'No external callbacks stubbed in tested yield/delta routines.',
                 'No full city economy, technology legality, pop allocation or gameplay.'],
    checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks)),indent=2))
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
