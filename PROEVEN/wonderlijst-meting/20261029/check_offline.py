"""Finite decoding fixtures only; no process handle, native call, or game model."""
from pathlib import Path
import ast
import ctypes
import difflib
import importlib.util
import json
import struct
import sys
import types
from datetime import datetime, timezone

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('_wonder_fixture_wrapper', HERE/'Lees-Wonderlijst.py')
wrapper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wrapper)
wrapper.verify_pins()
sentinel = types.ModuleType('unrelated_observer_sentinel')
sys.modules['original_core'] = sentinel
sys.modules['doel3original_core'] = sentinel
reader, projected_source = wrapper.load_reader()
assert sys.modules['original_core'] is sentinel and sys.modules['doel3original_core'] is sentinel
original_source = (wrapper.RELEASE/'Lees-Doel3.py').read_text('utf-8')
original_ast, projected_ast = ast.parse(original_source), ast.parse(projected_source)
unchanged = []
for name in ('trusted_binding', 'verify_loaded', 'stable_sample', 'observe_goal3', 'scalar_state'):
    a = next(x for x in original_ast.body if isinstance(x, ast.FunctionDef) and x.name == name)
    b = next(x for x in projected_ast.body if isinstance(x, ast.FunctionDef) and x.name == name)
    assert ast.dump(a) == ast.dump(b)
    unchanged.append(name)
assert 'handle=k.OpenProcess(0x410,False,args.pid)' in projected_source
assert reader.original_binding is sys.modules[wrapper.CORE_NAME].trusted_binding
assert reader.original_verify is sys.modules[wrapper.CORE_NAME].verify_loaded
binding = reader.trusted_binding('B2a-N30-TECHNICAL')
assert binding['ai']['sha256'] == reader.N30_HASH
assert [x['length'] for x in binding['ranges'] if x['kind'] == 'PIC-payload'] == [4348]
assert wrapper.text_expectations('control')['aidata_files'] == 118
assert (HERE/'participants.json').read_bytes() == (wrapper.ROOT/'PROEVEN/landbenchmark/20261027/participants.json').read_bytes()


def fixture():
    mem = {}
    def put(addr, blob):
        for i, value in enumerate(blob):
            mem[addr+i] = value
    def p32(addr, value):
        put(addr, struct.pack('<I', value))
    def read(addr, size):
        return bytes(mem[addr+i] for i in range(size))
    actor, planner, container, records = 0x20000, 0x21000, 0x23000, 0x24000
    p32(actor+0x94, planner)
    p32(planner+0x20+0x800, actor)
    p32(planner+0x20+0x7d0, container)
    p32(container, records)
    p32(container+4, 1)
    record = bytearray(32)
    struct.pack_into('<d', record, 0, 9100.0)
    struct.pack_into('<i', record, 8, 17)  # Arbitrary fixture index, never a token mapping.
    struct.pack_into('<i', record, 0x18, -1)
    put(records, record)
    p32(actor+0xc4, 0x25000)
    p32(0x25000, 0x26000)
    p32(0x26004, 0x27000)
    p32(0x26008, 1)
    p32(0x27000, 0x28000)
    for node, nameptr, symbol, nextnode, name, value in (
            (0x28000, 0x29000, 0x2a000, 0x28100, b'opening_required', 1.0),
            (0x28100, 0x29100, 0x2a200, 0, b'opening_completed', 0.0)):
        put(node, struct.pack('<III', nameptr, symbol, nextnode))
        put(nameptr, name+b'\0')
        p32(symbol, 0)
        put(symbol+8, struct.pack('<d', value))
        put(symbol+0xc2, struct.pack('<H', 4))
        put(symbol+0x68, b'\0\0\0')
    return read, put, p32, actor


passed = []
read, put, p32, actor = fixture()
state = wrapper.wonder_state(read, actor, reader)
assert state['effective_wonder_list']['records'] == [dict(weight=9100.0, native_index=17, category=-1)]
assert state['opening_symbols'] == dict(opening_required=1.0, opening_completed=0.0)
passed.append('valid bounded list and exact opening symbols')
for name, change, expected in (
        ('null list', lambda p, u: u(0x217f0, 0), 'NULL'),
        ('empty list', lambda p, u: u(0x23004, 0), 'EMPTY')):
    read, put, p32, actor = fixture()
    change(put, p32)
    assert wrapper.wonder_state(read, actor, reader)['effective_wonder_list']['status'] == expected
    passed.append(name)
for name, change in (
        ('count 201', lambda p, u: u(0x23004, 201)),
        ('negative count', lambda p, u: u(0x23004, 0xffffffff)),
        ('null storage for nonempty list', lambda p, u: u(0x23000, 0)),
        ('wrong AIP owner', lambda p, u: u(0x21820, 0x30000)),
        ('cyclic symbol chain', lambda p, u: u(0x28108, 0x28000)),
        ('invalid bucket count', lambda p, u: u(0x26008, 4097)),
        ('duplicate exact symbol name', lambda p, u: u(0x28100, 0x29000)),
        ('external symbol pointer', lambda p, u: u(0x2a000, 0x30000)),
        ('missing inputmask', lambda p, u: p(0x2a0c2, b'\0\0')),
        ('invalid symbol flag', lambda p, u: p(0x2a068, b'\x04\0')),
        ('special symbol flag', lambda p, u: p(0x2a06a, b'\x01')),
        ('fractional opening value', lambda p, u: p(0x2a008, struct.pack('<d', 0.5))),
        ('noncomplementary values', lambda p, u: p(0x2a208, struct.pack('<d', 1.0))),
        ('wrong wonder category', lambda p, u: u(0x24018, 0)),
        ('negative native index', lambda p, u: u(0x24008, 0xffffffff)),
        ('nonfinite weight', lambda p, u: p(0x24000, struct.pack('<d', float('nan'))))):
    read, put, p32, actor = fixture()
    change(put, p32)
    try:
        wrapper.wonder_state(read, actor, reader)
    except ValueError:
        passed.append('reject '+name)
    else:
        raise AssertionError(name+' was accepted')
times = [types.SimpleNamespace(dwHighDateTime=2, dwLowDateTime=3)]
wrapper.creationtime_exact(times, (2 << 32) | 3)
try:
    wrapper.creationtime_exact(times, (2 << 32) | 4)
except ValueError:
    passed.append('reject mismatched explicit creation FILETIME')
else:
    raise AssertionError('creationtime mismatch accepted')
try:
    reader.stable_sample(iter([1, 2]).__next__)
except ValueError:
    passed.append('reject unstable original complete sample')
else:
    raise AssertionError('unstable snapshot accepted')
result = dict(stage='C0_OFFLINE_ONLY_NO_PROCESS', at_utc=datetime.now(timezone.utc).isoformat(),
              checks=passed, unchanged_release_functions=unchanged,
              unique_imports=True, exact_N30_binding=True, text_control_118=True,
              native_token_binding='UNKNOWN', effective_runtime_list='NOT_MEASURED',
              queue_production='NOT_MEASURED', game_started=False, process_read=False)
if '--output' in sys.argv:
    target = HERE/'offline-result.json'
    if target.exists():
        raise ValueError('Existing offline result must be preserved')
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2))
