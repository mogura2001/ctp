"""Voer originele DLL-onderzoekskeuze offline uit met synthetische interfaces.

Geen game-/binarywijzigingen. De parser, fuzzy inferentie, kostenberekening en
engine callbacks zijn geen onderdeel van deze controle: COM-resultaten zijn stubs.
"""
from pathlib import Path
import hashlib
import json
import struct
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_ESP, UC_X86_REG_EIP

DLL = ROOT / 'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll'
HASH = '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
assert hashlib.sha256(DLL.read_bytes()).hexdigest() == HASH
PE = pefile.PE(str(DLL))
BASE = PE.OPTIONAL_HEADER.ImageBase
MEM = 0x30000000
AIP, AI, LIST, ITEMS, SCIENCE, TABLE, GOLD, AGENT = [MEM+i for i in
    (0x1000, 0x3000, 0x5000, 0x5100, 0x6000, 0x6100, 0x7000, 0x8000)]
STOP = MEM + 0xff000


def w(uc, address, value=None):
    if value is None:
        return struct.unpack('<I', uc.mem_read(address, 4))[0]
    uc.mem_write(address, struct.pack('<I', value & 0xffffffff))


def check(label, advances, expected, known=(), depth=None, costs=None,
          science=1, limit=100., route=False):
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(BASE, (PE.OPTIONAL_HEADER.SizeOfImage+4095) & ~4095)
    uc.mem_write(BASE, PE.get_memory_mapped_image())
    uc.mem_map(MEM, 0x100000)
    w(uc, AIP+0x800, AI)
    w(uc, AIP+0x7fc, LIST if advances is not None else 0)
    w(uc, LIST, ITEMS)
    w(uc, LIST+4, len(advances or []))
    for i, value in enumerate(advances or []):
        w(uc, ITEMS+i*4, value)
    w(uc, AI+0x44, SCIENCE)
    w(uc, SCIENCE, TABLE)
    w(uc, AI+0xc8, GOLD)
    w(uc, GOLD+0x18, science)
    w(uc, AI+0x94, AIP-0x20)
    w(uc, AGENT+0xb8, 1)
    w(uc, AGENT+0xbc, 99)
    uc.mem_write(0x200c5d48, struct.pack('<d', limit))
    sent = []
    addresses = {STOP+0x100+i*0x10: slot for i, slot in enumerate((0x20,0x3c,0x40,0x24))}
    for address, slot in addresses.items():
        w(uc, TABLE+slot, address)
        uc.mem_write(address, b'\xc2\x08\x00')

    def hook(machine, address, size, data):
        if address not in addresses:
            return
        slot = addresses[address]
        tech = w(machine, machine.reg_read(UC_X86_REG_ESP)+8)
        if slot == 0x24:
            sent.append(tech)
            result = 0
        elif slot == 0x20:
            result = int(tech in known)
        elif slot == 0x3c:
            result = (depth or {}).get(tech, 1)
        else:
            result = (costs or {}).get(tech, 20)
        machine.reg_write(UC_X86_REG_EAX, result)

    uc.hook_add(UC_HOOK_CODE, hook)
    stack = MEM+0xe0000
    w(uc, stack, STOP)
    if route:
        w(uc, stack+4, AI)
    uc.reg_write(UC_X86_REG_ESP, stack)
    uc.reg_write(UC_X86_REG_ECX, AGENT if route else AIP)
    uc.emu_start(0x20025d80 if route else 0x20066ba0, STOP, count=10000)
    assert uc.reg_read(UC_X86_REG_EIP) == STOP
    got = w(uc, AGENT+0xbc) if route else uc.reg_read(UC_X86_REG_EAX)
    if got >= 0x80000000:
        got -= 0x100000000
    passed = got == expected
    if route:
        passed &= sent == ([] if expected < 0 else [expected]) and w(uc,AGENT+0xb8) == 0
    return dict(label=label, got=got, expected=expected, engine_requests=sent, passed=bool(passed))


checks = [
    check('null_list', None, -1),
    check('empty_list', [], -1),
    check('all_known', [1,2], -1, known=(1,2)),
    check('known_first_skipped', [1,2], 2, known=(1,)),
    check('missing_prerequisites_skipped', [1,2], 2, depth={1:2}),
    check('all_unavailable', [1,2], -1, depth={1:2,2:3}),
    check('first_fast_candidate', [1,2], 1, costs={1:65,2:20}),
    check('slow_first_fast_second', [1,2], 2, costs={1:150,2:20}),
    check('threshold_equality_skipped', [1,2], 2, costs={1:100,2:20}),
    check('all_slow_first_fallback', [1,2], 1, costs={1:150,2:120}),
    check('zero_science_clamped_to_one', [1,2], 2, science=0, costs={1:150,2:20}),
    check('science_reverses_time_filter', [1,2], 1, science=10, costs={1:150,2:20}),
    check('research_route_sends_choice', [1,2], 2, known=(1,), route=True),
    check('research_route_no_choice_clears_flag', [], -1, route=True),
]
print(json.dumps(dict(dll_sha256=HASH, checks=checks,
                     passed=sum(x['passed'] for x in checks), total=len(checks)), indent=2))
raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
