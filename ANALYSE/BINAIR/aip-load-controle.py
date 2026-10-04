"""Offline controle van originele AIP-switch/action-instructies; geen spelwijziging.

Synthetische AIP-objecten, geen parserproef. FireRules gebruikt lege fuzzy regels;
OS/log/init-callbacks zijn stubs. De originele action-, lookup- en switchcode loopt.
"""
from pathlib import Path
import hashlib
import json
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

DLL = ROOT / 'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll'
HASH = '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
assert hashlib.sha256(DLL.read_bytes()).hexdigest() == HASH
PE = pefile.PE(str(DLL))
BASE = PE.OPTIONAL_HEADER.ImageBase
MEM = 0x30000000
DEST = MEM + 0x1000
STOP = MEM + 0xff000


def pack(value):
    return struct.pack('<I', value)


def fresh():
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(BASE, (PE.OPTIONAL_HEADER.SizeOfImage + 4095) & ~4095)
    uc.mem_write(BASE, PE.get_memory_mapped_image())
    uc.mem_map(MEM, 0x100000)
    uc.mem_write(STOP, b'\xc3')
    return uc


def word(uc, address, value=None):
    if value is None:
        return struct.unpack('<I', uc.mem_read(address, 4))[0]
    uc.mem_write(address, pack(value))


def number(uc, address, value=None):
    if value is None:
        return struct.unpack('<d', uc.mem_read(address, 8))[0]
    uc.mem_write(address, struct.pack('<d', value))


def name(uc, address):
    return bytes(uc.mem_read(address, 128)).split(b'\0')[0].decode('ascii')


def source(uc, address, label, scalar=None, lists=None):
    uc.mem_write(address, b'\0' * 0xa08)
    uc.mem_write(address + 0x804, label.encode() + b'\0')
    if scalar is not None:
        word(uc, address + 0x740, 2)
        number(uc, address + 8, scalar)
    flags = 0
    for bit, offset, pointer in lists or []:
        flags |= 1 << bit
        word(uc, address + offset, pointer)
        if bit == 4:
            word(uc, address + 0x7b0, 3)
    word(uc, address + 0x7ac, flags)


def seed(uc):
    source(uc, DEST, 'initial.aip')
    number(uc, DEST + 8, 111.)
    number(uc, DEST + 0x10, 222.)
    for index, offset in enumerate([0x7bc, *range(0x7d0, 0x800, 4)]):
        word(uc, DEST + offset, MEM + 0x10000 + index * 0x100)
    word(uc, DEST + 0x7b0, 7)
    number(uc, DEST + 0x2d0, -80.)
    number(uc, DEST + 0x450, -5.)
    number(uc, DEST + 0x368, -999999.)
    number(uc, DEST + 0x4e8, -999999.)


def snapshot(uc):
    return {
        'troops': number(uc, DEST + 8),
        'buildings': number(uc, DEST + 0x10),
        'unit_classes': word(uc, DEST + 0x7bc),
        'unit_count': word(uc, DEST + 0x7b0),
        'wonder': word(uc, DEST + 0x7d0),
        'growth': word(uc, DEST + 0x7d8),
        'defense': word(uc, DEST + 0x7ec),
        'advances': word(uc, DEST + 0x7fc),
        'eval_settle': number(uc, DEST + 0x2d0),
        'exec_settle': number(uc, DEST + 0x450),
        'eval_retreat': number(uc, DEST + 0x368),
        'exec_retreat': number(uc, DEST + 0x4e8),
        'name': name(uc, DEST + 0x804),
    }


def run(uc, address, this, arguments):
    stack = MEM + 0x80000
    uc.mem_write(stack, pack(STOP) + b''.join(pack(a) for a in arguments))
    uc.reg_write(UC_X86_REG_ESP, stack)
    uc.reg_write(UC_X86_REG_ECX, this)
    uc.emu_start(address, STOP, count=200000)
    assert uc.reg_read(UC_X86_REG_EIP) == STOP


checks = []
cases = [
    ('absent_fields_retain', None, [], {}),
    ('scalar_overwrite', 444., [], {'troops': 444.}),
    ('unit_block_replaced', None, [(4, 0x7bc, MEM + 0x20000)],
     {'unit_classes': MEM + 0x20000, 'unit_count': 3}),
    ('growth_defense_independent', None,
     [(7, 0x7d8, MEM + 0x22000), (12, 0x7ec, MEM + 0x23000)],
     {'growth': MEM + 0x22000, 'defense': MEM + 0x23000}),
    ('research_list_replaced', None, [(14, 0x7fc, MEM + 0x24000)],
     {'advances': MEM + 0x24000}),
    ('explicit_empty_growth', None, [(7, 0x7d8, MEM + 0x25000)],
     {'growth': MEM + 0x25000}),
]
for label, scalar, lists, changed in cases:
    uc = fresh()
    seed(uc)
    before = snapshot(uc)
    src = MEM + 0x4000
    source(uc, src, label + '.aip', scalar, lists)
    expected = before | changed | {'name': label + '.aip'}
    run(uc, 0x20063720, DEST, [src])
    actual = snapshot(uc)
    checks.append({'case': label, 'expected': expected, 'actual': actual,
                   'ok': actual == expected})

for value, present in [(0., True), (-30., True), (-999999., True), (0., False)]:
    uc = fresh()
    seed(uc)
    source(uc, MEM + 0x4000, 'limits.aip')
    word(uc, MEM + 0x4000 + 0x751, int(present))
    word(uc, MEM + 0x4000 + 0x781, int(present))
    number(uc, MEM + 0x4000 + 0x2d0, value)
    number(uc, MEM + 0x4000 + 0x450, value)
    # Ook een ongemelde retreatlimiet wordt door de switch hard hersteld.
    number(uc, DEST + 0x368, 9.)
    number(uc, DEST + 0x4e8, 9.)
    run(uc, 0x20063720, DEST, [MEM + 0x4000])
    actual = snapshot(uc)
    expected_eval = value if present and value != -999999. else -80.
    expected_exec = value if present and value != -999999. else -5.
    checks.append({'case': 'goal_limit_exception', 'source': value, 'present': present,
                   'actual': actual, 'ok': actual['eval_settle'] == expected_eval
                   and actual['exec_settle'] == expected_exec
                   and actual['eval_retreat'] == -999999. and actual['exec_retreat'] == -999999.})

uc = fresh()
seed(uc)
source(uc, MEM + 0x4000, 'first.aip', 444., [(7, 0x7d8, MEM + 0x22000)])
source(uc, MEM + 0x6000, 'second.aip', 555., [(14, 0x7fc, MEM + 0x24000)])
run(uc, 0x20063720, DEST, [MEM + 0x4000])
run(uc, 0x20063720, DEST, [MEM + 0x6000])
actual = snapshot(uc)
checks.append({'case': 'last_present_writer_wins', 'actual': actual,
               'ok': actual['troops'] == 555. and actual['growth'] == MEM + 0x22000
               and actual['advances'] == MEM + 0x24000 and actual['buildings'] == 222.})

# FireRules: twee true loads, een false load. Lookup en switches blijven origineel.
uc = fresh()
seed(uc)
engine, ai, planner = MEM + 0x30000, MEM + 0x31000, DEST - 0x20
manager, array, entries = MEM + 0x33000, MEM + 0x34000, MEM + 0x35000
source(uc, MEM + 0x4000, 'first.aip', 444., [(7, 0x7d8, MEM + 0x22000)])
source(uc, MEM + 0x6000, 'second.aip', 555., [(14, 0x7fc, MEM + 0x24000)])
word(uc, 0x2009bee4, manager)
word(uc, manager, array)
word(uc, array, 2)
word(uc, array + 0x18, entries)
word(uc, entries, MEM + 0x4000)
word(uc, entries + 4, MEM + 0x6000)
word(uc, ai + 0x94, planner)
word(uc, engine + 0x1c, ai)
rulearray, actionarray, empty, actionlist = [MEM + x for x in (0x36000, 0x37000, 0x38000, 0x39000)]
word(uc, engine + 0xc, rulearray)
word(uc, rulearray + 8, empty)
word(uc, engine + 0x10, actionarray)
word(uc, actionarray + 8, actionlist)
for i, (label, value) in enumerate([('first.aip', 1.), ('second.aip', 0.), ('second.aip', 1.)]):
    action, node, arglist, argnode, string, symbol = [MEM + 0x40000 + i * 0x1000 + x for x in (0,0x100,0x200,0x300,0x400,0x500)]
    word(uc, action + 8, arglist)
    word(uc, arglist, argnode)
    word(uc, argnode, string)
    uc.mem_write(string, label.encode() + b'\0')
    word(uc, action + 0xc, symbol)
    word(uc, action + 0x10, 2)  # greater than threshold
    number(uc, symbol + 8, value)
    number(uc, action + 0x18, .5)
    word(uc, node, action)
    word(uc, node + 4, MEM + 0x40000 + (i + 1) * 0x1000 + 0x100 if i < 2 else 0)
    if i == 0:
        word(uc, actionlist, node)
tick = MEM + 0xe0000
word(uc, 0x2008900c, tick)
uc.mem_write(tick, b'\xc3')
events = []


def hook(uc, address, size, data):
    if address == 0x20067280:
        sp = uc.reg_read(UC_X86_REG_ESP)
        events.append(name(uc, word(uc, sp + 12)))
    if address in (0x2003a860, 0x2003a910, 0x2003c770, tick):
        sp = uc.reg_read(UC_X86_REG_ESP)
        return_to = word(uc, sp)
        uc.reg_write(UC_X86_REG_ESP, sp + 4 + (4 if address == 0x2003c770 else 0))
        uc.reg_write(UC_X86_REG_EAX, 0)
        uc.reg_write(UC_X86_REG_EIP, return_to)


uc.hook_add(UC_HOOK_CODE, hook)
run(uc, 0x20038ff0, engine, [2])
first = snapshot(uc)
checks.append({'case': 'actions_in_list_order_true_only', 'loads': events[:], 'actual': first,
               'ok': events == ['first.aip', 'second.aip'] and first['troops'] == 555.
               and first['growth'] == MEM + 0x22000 and first['advances'] == MEM + 0x24000})
# Volgende section-run: geen true action, geen reset van effectieve AIP.
for i in (0, 2):
    number(uc, MEM + 0x40000 + i * 0x1000 + 0x500 + 8, 0.)
events.clear()
run(uc, 0x20038ff0, engine, [2])
second = snapshot(uc)
checks.append({'case': 'next_section_no_load_retains', 'loads': events[:], 'actual': second,
               'ok': events == [] and second == first})
for label in ('unknown.aip', 'First.aip'):
    events.clear()
    uc.mem_write(MEM + 0x60000, label.encode() + b'\0')
    run(uc, 0x20067280, manager, [ai, DEST, MEM + 0x60000])
    actual = snapshot(uc)
    checks.append({'case': 'missing_or_case_mismatch_noop', 'request': label,
                   'actual': actual, 'ok': actual == second})

result = {'binary_sha256': HASH, 'checks': checks,
          'passed': sum(c['ok'] for c in checks), 'total': len(checks),
          'limitations': ['Synthetic pre-parsed objects, not real AIP parser/files.',
                          'No fuzzy rules in FireRules; fixed symbol values.',
                          'OS/log/init callbacks stubbed; destination list ownership bits zero.',
                          'No savegame/app/gameplay run; no unit list contents dereferenced.']}
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['passed'] == result['total'] else 1)
