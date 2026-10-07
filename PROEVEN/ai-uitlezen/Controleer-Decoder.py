"""Small synthetic-memory decoder checks; never opens a game process."""
from pathlib import Path
import json
import runpy
import struct

folder = Path(__file__).resolve().parent
observe = runpy.run_path(str(folder / 'Lees-Onderzoeksactivatie.py'))['observe']
memory = {}

def put(address, value):
    data = struct.pack('<I', value & 0xffffffff) if isinstance(value, int) else value
    memory.update({address+i: byte for i, byte in enumerate(data)})

def read(address, size):
    return bytes(memory.get(address+i, 0) for i in range(size))

engine_base, ai_base = 0x500000, 0x21000000
for address, value in ((0xb7ddb8, 0x100000), (0xb7dd80, 0x110000),
                       (0xb7dd00, 0x120000), (0xb7dcfc, 0x130000),
                       (0x120000, 2), (0x120008, 0x140000),
                       (0x130004, 0x150000)):
    put(address, value)
for i, name in enumerate((b'ADVANCE_RELIGION\0', b'ADVANCE_THEOCRACY\0')):
    put(0x140000+i*0x8c, 10+i)
    put(0x150000+4*(10+i), 0x160000+i*32)
    put(0x160008+i*32, 0x170000+i*64)
    put(0x170000+i*64, name)
for address, value in ((0x110004, 0x180000), (0x102210, 0x190000),
                       (0x190000, 0x21089728), (0x190008, 0x1a0000),
                       (0x1a0020, 1), (0x1a0044, 0x1b0000),
                       (0x1b0000, 0x844fe0), (0x1b0008, 0x180000),
                       (0x1b000c, 1), (0x1a0094, 0x1c0000),
                       (0x1a0120, 0x1d0000), (0x1c0820, 0x1a0000),
                       (0x1c081c, 0x1e0000), (0x1e0000, 0x1f0000),
                       (0x1e0004, 2), (0x1f0000, 0), (0x1f0004, 1),
                       (0x1d00b8, 1), (0x1d00bc, 1),
                       (0x1812ec, 0x200000), (0x200008, 0)):
    put(address, value)
result = observe(read, engine_base, ai_base)
civ = result['civilizations'][0]
assert len(result['civilizations']) == 1 and civ['civ_id'] == 1
assert [v['name'] for v in civ['research_list']] == ['ADVANCE_RELIGION', 'ADVANCE_THEOCRACY']
assert civ['last_ai_request']['index'] == 1 and civ['engine_current']['index'] == 0
checks = ['relocated-owner-and-name-chain', 'request-distinct-from-engine-current']
for address, bad, good, expected in (
    (0x1b000c, 2, 1, 'Civilization ownership mismatch'),
    (0x1c0820, 0, 0x1a0000, 'Effective AIP owner mismatch'),
    (0x1e0004, 1025, 2, 'Invalid effective research-list length'),
    (0x1f0004, 2, 1, 'Advance index outside engine database'),
):
    put(address, bad)
    try:
        observe(read, engine_base, ai_base)
    except ValueError as error:
        assert str(error) == expected
    else:
        raise AssertionError(expected)
    put(address, good)
    checks.append(expected)
print(json.dumps({'passed': len(checks), 'checks': checks,
                  'scope': 'synthetic decoder only; no process opened',
                  'live_validation': False}, indent=2))
