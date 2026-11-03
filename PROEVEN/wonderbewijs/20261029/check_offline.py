"""Small finite byte fixtures for token/owner/queue gates; no engine emulation."""
from pathlib import Path
import hashlib
import importlib.util
import json
import struct
import sys
from datetime import datetime, timezone

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('_wonderbewijs_fixture', HERE/'Lees-Wonderbewijs.py')
project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(project)
project.verify_pins()
base = project.load_base()
base_pin = base.verify_pins()
reader, source = project.compose_reader(base.load_reader)
binding = reader.trusted_binding('B2a-N30-TECHNICAL')
assert binding['ai']['sha256'] == reader.N30_HASH
extra = json.loads((HERE/'binding-windows.json').read_text('utf-8'))
assert binding['ranges'][-len(extra['ranges']):] == extra['ranges']
assert reader.verify_loaded is not None and reader.FOLDER == HERE
assert 'wonder_creationtime(times,args.creation_filetime)' in source
assert 'handle=k.OpenProcess(0x410,False,args.pid)' in source
assert (HERE/'participants.json').read_bytes() == (base.HERE/'participants.json').read_bytes()
import pefile
images = {}
for label, path, address in (
        ('engine', project.ROOT/'CTP-og/ctp_program/ctp/civctp.exe', 0x400000),
        ('ai', project.ROOT/'PROEVEN/opening-b2/candidates/B2a-N30-TECHNICAL/robotcom.dll', 0x20000000)):
    pe = pefile.PE(str(path))
    images[address] = pe.get_memory_mapped_image()
def image_read(address, size):
    for start, blob in images.items():
        if start <= address and address+size <= start+len(blob):
            return blob[address-start:address-start+size]
    raise ValueError('Offline loaded-image fixture read out of bounds')
reader.verify_loaded(image_read, binding, 0x400000, 0x20000000,
                     {k:binding[k]['size'] for k in ('engine', 'ai')})
assert project.token_hash(project.TOKEN) == (37859, 116)
passed = ['exact add-then-rol16 token hash including NUL', 'unchanged base pins and eb6 binding plus 18 exact loaded windows',
          'original verify_loaded on offline PE mapped bytes', 'original CLI creation/read-only/output guards retained']


def fixture():
    memory = {}
    def put(address, data):
        memory.update({address+i: b for i,b in enumerate(data)})
    def u(address, value):
        put(address, struct.pack('<I', value))
    def read(address, size):
        return bytes(memory[address+i] for i in range(size))
    eb, actor, player = 0x400000, 0x20000, 0x22000
    u(eb+0x67dcfc, 0x30000); u(0x30008, 0x31000)
    u(0x31000+4*116, 0x32000)
    u(0x32000, 42); u(0x32004, 0x33000)
    put(0x33000, project.TOKEN+b'\0')
    u(eb+0x67dd5c, 0x34000); u(0x34000, 3); u(0x34008, 0x35000)
    for i in range(3): u(0x35000+i*0xd0+4, 40+i)
    u(0x351a0+8, 5); u(0x351a0+0x2c, 1); u(0x351a0+0xc, 6)
    u(eb+0x67dd80, 0x36000)
    for civ in range(32): u(0x36000+4*civ, player if civ == 2 else 0)
    u(player+0x12ec, 0x37000); u(0x3701c, 0x38000)
    put(0x38005, b'\x01\0')
    u(eb+0x67a69c, 0x39000); u(0x39014, 0x3a000); u(0x3a008, 0xffffffff)
    u(actor+0x94, 0x24000); u(0x24820, actor); put(0x24270, struct.pack('<d', 0.8))
    u(actor+0x8c, 0x40000); u(0x40000, 1); u(0x40008, 0x41000)
    for off,val in ((0,7),(4,0),(8,0),(12,0x42000)): u(0x41000+off,val)
    u(0x42004, 2); u(0x4200c, 7)
    u(player+0x12c8, 0x43000); u(0x43008, 0x44000)
    for off,val in ((0,7),(4,0),(8,0),(12,0x45000)): u(0x44000+off,val)
    u(0x45000, 0)
    u(player+0x12c0, 0x46000); u(0x46008, 1); u(0x4600c, 0x47000)
    handle = 0x12340007  # Deliberately differs from AIcity-ID 7.
    u(0x47000, handle)
    u(eb+0x67dd74, 0x48000); u(0x4800c+4*(handle&1023), 0x49000)
    for off,val in ((4,0),(8,0),(12,handle),(0x18,2),(0x58,0x4a000)): u(0x49000+off,val)
    for off,val in ((0,0),(8,0),(12,0)): u(0x4a450+off,val)
    u(0x4a004, 2)
    view = project.View(read, reader)
    return read, put, u, view, eb, player, actor


read, put, u, view, eb, player, actor = fixture()
identity, record = project.native_identity(view, eb)
assert identity['unique_native_index'] == 2 and identity['string_sid'] == 42
u(0x32000,0xffffffff); u(0x351a4,0xffffffff)
assert project.native_identity(view,eb)[0]['string_sid'] == 0xffffffff
u(0x32000,42); u(0x351a4,42)
passed.append('opaque full-u32 StringId above 100000 accepted with exact unique binding')
cities = project.actor_cities(view, eb, player, actor, 2)
assert cities[0]['full_engine_handle'] == 0x12340007 and cities[0]['ai_city_id'] == 7
assert cities[0]['real_queue']['count'] == 0
passed.append('exact token SID uniquely index2 and AI-ID through slot to owned full handle/empty queue')
state = dict(advance_count=10, civilizations=[dict(civ_id=2, ai_actor=hex(actor))])
project.evidence(read, eb, state, reader)
assert state['civilizations'][0]['wonder_build_evidence']['prerequisite']['known']
assert state['wonder_global_evidence']['global_built_raw'] == 0xffffffff
assert state['wonder_global_evidence']['global_built'].startswith('UNKNOWN')
assert not state['wonder_global_evidence']['obsolete_at_any_existing_player']
put(0x38006, b'\x01')
project.evidence(read, eb, state, reader)
assert state['wonder_global_evidence']['obsolete_at_any_existing_player']
passed.append('prerequisite/obsolete bytes change interpretation while global-built stays raw UNKNOWN')
u(0x4a450, 1); u(0x4a458, 0x4b000); u(0x4a45c, 0x4b000)
u(0x4b004, 2); u(0x4b008, 9); u(0x4b010, 0)
assert project.real_queue(view, 0x4a000)['nodes'][0]['is_exact_labyrinth']
passed.append('one real queue node class9/type2 with consistent endpoints')
for name, mutate, call in (
    ('wrong exact token name', lambda p,u: p(0x33000,b'WONDER_Z\0') or u(0x3200c,0), 'identity'),
    ('StringDB search cycle', lambda p,u: p(0x33000,b'WONDER_Z\0') or u(0x3200c,0x32000), 'identity'),
    ('duplicate WonderDB SID', lambda p,u: u(0x35004,42), 'identity'),
    ('AIcity-ID identity mismatch', lambda p,u: u(0x4200c,8), 'city'),
    ('player slot map cycle', lambda p,u: u(0x44004,0x44000), 'city'),
    ('out-of-range player slot', lambda p,u: u(0x45000,1), 'city'),
    ('full handle mismatch', lambda p,u: u(0x4900c,7), 'city'),
    ('pool owner mismatch', lambda p,u: u(0x49018,3), 'city'),
    ('CityData owner mismatch', lambda p,u: u(0x4a004,3), 'city'),
    ('pool tree cycle', lambda p,u: u(0x49004,0x49000), 'city'),
    ('empty queue with nonnull head', lambda p,u: u(0x4a458,0x4b000), 'city'),
    ('queue count bounds', lambda p,u: u(0x4a450,4097), 'city')):
    read, put, u, view, eb, player, actor = fixture()
    mutate(put,u)
    try:
        project.native_identity(view,eb) if call=='identity' else project.actor_cities(view,eb,player,actor,2)
    except ValueError:
        passed.append('reject '+name)
    else:
        raise AssertionError(name+' accepted')
read, put, u, view, eb, player, actor = fixture()
u(0x4a450,2); u(0x4a458,0x4b000); u(0x4a45c,0x4b100)
u(0x4b004,2); u(0x4b008,9); u(0x4b010,0x4b000)
try:
    project.real_queue(view,0x4a000)
except ValueError:
    passed.append('reject real queue cycle')
else:
    raise AssertionError('cyclic queue accepted')
result=dict(stage='C0_OFFLINE_ONLY_NO_RPM_OR_GAME',at_utc=datetime.now(timezone.utc).isoformat(),
    checks=passed,base_pins_sha256=base_pin,extra_loaded_windows=18,
    native_token_runtime='OPEN_NOT_MEASURED',real_queue_runtime='OPEN_NOT_MEASURED',
    global_built_interpretation='UNKNOWN',city_rank_buildtime_admission='UNKNOWN')
if '--output' in sys.argv:
    output=HERE/'offline-result.json'
    if output.exists(): raise ValueError('Preserve existing offline result')
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
