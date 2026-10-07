"""Read-only offline control of the real engine government request/turn branch.

Original selection, availability getter and deadline instructions execute.
The RNG and the application helper (city/economy/UI effects) are explicit stubs.
The per-round test executes only the identified completion fragment, not a turn.
No binary or gameplay files are written.
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
from unicorn.x86_const import (
    UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EDI,
    UC_X86_REG_ESI, UC_X86_REG_ESP, UC_X86_REG_EIP,
)

PATH = ROOT / 'CTP-og/ctp_program/ctp/civctp.exe'
HASH = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
assert hashlib.sha256(PATH.read_bytes()).hexdigest() == HASH
PE = pefile.PE(str(PATH))
BASE = PE.OPTIONAL_HEADER.ImageBase
MEM = 0x30000000
PLAYER, DB, RECORDS, CONST, ROUND, SCIENCE, KNOWN = [MEM+x for x in
    (0x1000, 0x4000, 0x5000, 0x7000, 0x8000, 0x9000, 0xa000)]
STOP = MEM+0xff000
STACK = MEM+0xe0000


def word(uc, address, value=None):
    if value is None:
        return struct.unpack('<I', uc.mem_read(address, 4))[0]
    uc.mem_write(address, struct.pack('<I', value & 0xffffffff))


def fixture(active=1, desired=1, deadline=-1, completed=0, turn=20,
            random=0, knows=True):
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(BASE, (PE.OPTIONAL_HEADER.SizeOfImage+4095) & ~4095)
    uc.mem_write(BASE, PE.get_memory_mapped_image())
    uc.mem_map(MEM, 0x100000)
    uc.mem_map(0, 0x1000)  # FS:[0] exception chain for isolated execution.
    for address in (0xa44c9c, 0xa44c98, 0xa44c94):
        word(uc, address, 0)
    word(uc, 0xa7dd34, DB)
    word(uc, DB, 12)
    word(uc, DB+8, RECORDS)
    for index in range(12):
        word(uc, RECORDS+index*0x1c0+8, 17)
    word(uc, 0xa7dd48, CONST)
    word(uc, CONST+0x370, 4)
    word(uc, 0xa7ddc4, ROUND)
    word(uc, ROUND, turn)
    word(uc, PLAYER+0x94, active)
    word(uc, PLAYER+0x11d8, desired)
    word(uc, PLAYER+0x11dc, deadline)
    word(uc, PLAYER+0x11e0, completed)
    word(uc, PLAYER+0x12ec, SCIENCE)
    word(uc, SCIENCE+0x1c, KNOWN)
    uc.mem_write(KNOWN+17, bytes([int(knows)]))
    applied = []

    def hook(machine, address, size, data):
        if address not in (0x4fa370, 0x4c2f60):
            return
        esp = machine.reg_read(UC_X86_REG_ESP)
        if address == 0x4fa370:
            machine.reg_write(UC_X86_REG_EAX, random)
            cleanup = 4
        else:
            target = word(machine, esp+4)
            applied.append(target)
            word(machine, PLAYER+0x94, target)
            machine.reg_write(UC_X86_REG_EAX, 1)
            cleanup = 8
        machine.reg_write(UC_X86_REG_EIP, word(machine, esp))
        machine.reg_write(UC_X86_REG_ESP, esp+cleanup)

    uc.hook_add(UC_HOOK_CODE, hook)
    return uc, applied


def state(uc, applied):
    return dict(active=word(uc, PLAYER+0x94), desired=word(uc, PLAYER+0x11d8),
                deadline=word(uc, PLAYER+0x11dc), completed=word(uc, PLAYER+0x11e0),
                applied=applied.copy())


def request(uc, target):
    word(uc, STACK, STOP)
    word(uc, STACK+4, target)
    uc.reg_write(UC_X86_REG_ESP, STACK)
    uc.reg_write(UC_X86_REG_ECX, PLAYER)
    uc.emu_start(0x4c2d40, STOP, count=10000)
    assert uc.reg_read(UC_X86_REG_EIP) == STOP
    return uc.reg_read(UC_X86_REG_EAX)


def completion_fragment(uc, turn):
    word(uc, ROUND, turn)
    uc.reg_write(UC_X86_REG_ESI, PLAYER)
    uc.reg_write(UC_X86_REG_EDI, 0)
    uc.reg_write(UC_X86_REG_ESP, STACK)
    uc.emu_start(0x4b8a3d, 0x4b8a6d, count=100)
    assert uc.reg_read(UC_X86_REG_EIP) == 0x4b8a6d


checks = []


def record(label, uc, applied, expected, result=None):
    got = state(uc, applied)
    if result is not None:
        got['request_result'] = result
    checks.append(dict(label=label, got=got, expected=expected,
                       passed=all(got[key] == value for key, value in expected.items())))


for random in range(4):
    uc, applied = fixture(random=random)
    request(uc, 3)
    record(f'new_change_rng_remainder_{random}', uc, applied,
           dict(active=0, desired=3, deadline=21+random, completed=0, applied=[0]))

uc, applied = fixture(knows=False)
result = request(uc, 3)
record('unknown_enabling_advance_rejected', uc, applied,
       dict(active=1, desired=1, applied=[], request_result=0), result)

uc, applied = fixture()
result = request(uc, 1)
record('active_government_request_ignored', uc, applied,
       dict(active=1, applied=[], request_result=0), result)

uc, applied = fixture(random=3)
request(uc, 3)
request(uc, 3)
record('repeated_pending_request_keeps_deadline', uc, applied,
       dict(active=0, desired=3, deadline=24, applied=[0]))
completion_fragment(uc, 23)
record('before_deadline_not_completed', uc, applied,
       dict(active=0, deadline=24, completed=0, applied=[0]))
completion_fragment(uc, 24)
record('at_deadline_target_applied', uc, applied,
       dict(active=3, deadline=24, completed=1, applied=[0, 3]))
request(uc, 2)
record('same_round_after_completion_can_change_directly', uc, applied,
       dict(active=2, completed=1, deadline=24, applied=[0, 3, 2]))
completion_fragment(uc, 25)
record('following_round_clears_completion_flag', uc, applied,
       dict(active=2, completed=0, deadline=24, applied=[0, 3, 2]))

uc, applied = fixture(active=0, desired=2, deadline=24, turn=21)
request(uc, 3)
record('pending_target_can_change_without_timer_reset', uc, applied,
       dict(active=0, desired=3, deadline=24, applied=[]))

uc, applied = fixture(active=0, desired=3, deadline=24, turn=25)
request(uc, 3)
record('anarchy_request_after_deadline_applies_target', uc, applied,
       dict(active=3, deadline=24, applied=[3]))

print(json.dumps(dict(engine_sha256=HASH,
    limitations=['Synthetic player/database; engine availability instructions executed.',
                 'RNG result and government application helper are stubs.',
                 'Turn tests execute completion fragment only; no gameplay or full turn.'],
    checks=checks, passed=sum(x['passed'] for x in checks), total=len(checks)), indent=2))
raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
