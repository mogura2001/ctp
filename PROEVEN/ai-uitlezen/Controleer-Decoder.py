"""Small synthetic-memory decoder checks; never opens a game process."""
from pathlib import Path
import json
import runpy
import struct
import sys
import copy
import hashlib
import ast
sys.dont_write_bytecode=True

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

# Focused H3 extension of the existing fixture; no new framework or process API.
api=runpy.run_path(str(folder/'Lees-Onderzoeksactivatie.py'))
decode,compare,stable=api['decode_h3'],api['compare_snapshots'],api['stable_sample']
for address,value in ((0x1c0a28,0x1a0000),(0x1c0a2c,0x2e0000),(0x2e0000,4),(0x1c0a30,1),(0x1c0a38,2),(0x1c0a4c,2),(0x1c0a54,2),(0x1c0a48,0x2f0000),(0x1c0a50,0x300000),(0x2f0000,0x310000),(0x300000,3),(0x310000,ai_base+0x8a558),(0x310008,3),(0x31000c,5),(0x310028,0),(0x310054,0x330000),(0x1a0080,0x3a0000),(0x1a0030,0x3b0000),(0xb7dd70,0x350000),(0x10248c,0x360000),(0x360000,0x370000),(0x370004,0x380000)):
    put(address,value)
put(0x350014,struct.pack('<hhh',3,4,1));put(0x330000,struct.pack('<hhh',1,2,0));put(0x310048,struct.pack('<d',8));put(0x380004,struct.pack('<h',8))
sa=decode(read,engine_base,ai_base)
assert sa['civilizations'][0]['settlement']['goals'][0]['B']==8
assert [v['name'] for v in sa['civilizations'][0]['research_list']]==['ADVANCE_RELIGION','ADVANCE_THEOCRACY']
extra=['research-preserved-plus-external-cache-shape']
for address,value in ((0x110000,0x180000),(0x110004,0),(0x10220c,0x190000),(0x102210,0),(0x1a0020,0),(0x1b000c,0)):put(address,value)
assert decode(read,engine_base,ai_base)['civilizations']==[]
extra.append('civ0-only-excluded-from-H3decode')
for address,value in ((0x110000,0),(0x110004,0x180000),(0x10220c,0),(0x102210,0x190000),(0x1a0020,1),(0x1b000c,1)):put(address,value)
assert decode(read,engine_base,ai_base)['civilizations'][0]['civ_id']==1
for address,bad,good in ((0x1c0a28,0,0x1a0000),(0x2e0000,-1,4),(0x1c0a30,4097,1),(0x1c0a4c,0,2),(0x310008,2,3),(0x31000c,7,5),(0x310054,0,0x330000)):
    put(address,bad)
    try:decode(read,engine_base,ai_base)
    except ValueError:pass
    else:raise AssertionError('H3 invalid layout accepted '+hex(address))
    put(address,good);extra.append('layout-rejected-'+hex(address))
for bad in (float('nan'),0,32768,8.5):
    put(0x310048,struct.pack('<d',bad))
    try:decode(read,engine_base,ai_base)
    except ValueError:pass
    else:raise AssertionError('bad Q accepted')
    extra.append('invalid-Q-'+str(bad))
put(0x310048,struct.pack('<d',8));put(0x330000,struct.pack('<hhh',3,2,0))
try:decode(read,engine_base,ai_base)
except ValueError:extra.append('external-bound-rejection')
else:raise AssertionError('outsidecache accepted')
put(0x330000,struct.pack('<hhh',1,2,0));put(0x350014,struct.pack('<hhh',0,4,1))
assert decode(read,engine_base,ai_base)['civilizations'][0]['settlement']['goals'][0]['B'] is None
extra.append('unbound-dimensions-no-B');put(0x350014,struct.pack('<hhh',3,4,1))
meta={'run_id':'own-fixture','pass_label':'one-pass','instance':{'pid':123,'creation':456},'variant':'H3-SCORE_CURRENT','binding':{'fixture':True},'stable_twice':True}
a={**copy.deepcopy(meta),'snapshot_label':'A','state':sa}
put(0x1c0a30,2);put(0x2e0000,5);put(0x2f0004,0x320000);put(0x300004,4)
for o,v in ((0,ai_base+0x8a558),(8,4),(12,5),(0x28,0x20),(0x54,0x330000)):put(0x320000+o,v)
put(0x320048,struct.pack('<d',9));b={**copy.deepcopy(meta),'snapshot_label':'B','state':decode(read,engine_base,ai_base)}
r=compare(a,b);assert r['status']=='new-registered-goal-state-observable' and r['new_goal_settle'][0]['Q_minus_current_B']==1 and r['new_goal_settle'][0]['pending_deletion'] and not r['unconditional_bonus_proven'];extra.append('new-id-Q-minus-current-B-only-pendingdeletion')
barba,barbb=copy.deepcopy(a),copy.deepcopy(b)
for snapshot in (barba,barbb):
    snapshot['state']['civilizations'][0]['civ_id']=0
    snapshot['state']['civilizations'][0]['settlement']['civ_id']=0
assert compare(barba,barbb)['status']=='not-observable-at-this-moment' and compare(barba,barbb)['new_goal_settle']==[]
extra.append('civ0-new-QplusB-never-normalstate-acceptance')
for key in ('run_id','instance','variant','pass_label','binding'):
    broken=copy.deepcopy(b);broken[key]='changed'
    try:compare(a,broken)
    except ValueError:pass
    else:raise AssertionError('changed context accepted')
    extra.append('pair-rejected-'+key)
for key,value in (('scheduler','0xchanged'),('next_id',3),('all_goal_ids',[3,4])):
    broken=copy.deepcopy(b)
    if key=='all_goal_ids':
        old=copy.deepcopy(a);old['state']['civilizations'][0]['settlement'][key]=value
        assert compare(old,broken)['status']=='not-observable-at-this-moment';extra.append('old-ID-never-new');continue
    broken['state']['civilizations'][0]['settlement'][key]=value
    try:compare(a,broken)
    except ValueError:pass
    else:raise AssertionError('Scheduler context accepted')
    extra.append('scheduler-rejected-'+key)
empty=copy.deepcopy(b);empty['state']['civilizations'][0]['settlement'].update(goals=[],all_goal_ids=[],count=0)
assert compare(a,empty)['status']=='not-observable-at-this-moment';extra.append('empty-not-observable')
put(0x1c0a30,0);assert decode(read,engine_base,ai_base)['civilizations'][0]['settlement']['goals']==[];extra.append('zero-count-decoder-no-arraydump');put(0x1c0a30,2)
put(0x300004,3)
try:decode(read,engine_base,ai_base)
except ValueError:extra.append('duplicate-ID-rejected')
else:raise AssertionError('duplicate IDs accepted')
put(0x300004,4);put(0x1c0a50,0xfffffffc)
try:decode(read,engine_base,ai_base)
except ValueError:extra.append('array-address-overflow-rejected')
else:raise AssertionError('arrayread overflow accepted')
put(0x1c0a50,0x300000)
assert stable(lambda:copy.deepcopy(sa))==sa
samples=iter((sa,b['state']))
try:stable(lambda:next(samples))
except ValueError:extra.append('unstable-doubledecode-rejected')
else:raise AssertionError('unstable snapshot accepted')
try:api['bounded'](lambda p,n:b'xx')(0x10000,4)
except ValueError:extra.append('partial-read-rejected')
else:raise AssertionError('short read accepted')
before=(folder/'activatie-h3-observer.before.bin').read_bytes()
assert hashlib.sha256(before).hexdigest()=='b4270deecf27ac3dbcd6e1a2c08988e474c6d950a0de7f0ce961979852f71b2d'
old_ast=ast.parse(before.decode());new_ast=ast.parse((folder/'Lees-Onderzoeksactivatie.py').read_text())
getobserve=lambda tree:ast.dump(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='observe'),include_attributes=False)
assert getobserve(old_ast)==getobserve(new_ast);extra.append('original-researchdecoder-AST-identical')
bindings={}
for variant in api['VARIANTS']:
    binding=api['trusted_binding'](variant);bindings[variant]=binding
    loaded={}
    def fill(address,blob):loaded.update({address+i:byte for i,byte in enumerate(blob)})
    eb,ab=0x400000,0x21000000
    for kind,base in [('engine',eb),('ai',ab)]:fill(base,bytes.fromhex(binding[kind]['header']))
    for item in binding['ranges']:
        raw=bytearray.fromhex(item['expected_hex']);base=ab if item['module']=='ai' else eb
        if item['module']=='ai' and item['kind']!='PIC-payload':
            for reloc in binding['original_HIGHLOW']:
                if item['rva']<=reloc<item['rva']+len(raw):
                    off=reloc-item['rva'];struct.pack_into('<I',raw,off,(struct.unpack_from('<I',raw,off)[0]+ab-0x20000000)&0xffffffff)
        fill(base+item['rva'],raw)
    for site in binding['sites']:fill(ab+site['rva'],bytes.fromhex(site['expected_hex']))
    def loaded_read(p,n):return bytes(loaded[p+i] for i in range(n))
    sizes={k:binding[k]['size'] for k in ('engine','ai')}
    assert api['verify_loaded'](loaded_read,binding,eb,ab,sizes)['all_three_scorecalls'];extra.append(variant+'-exact-rebase-binding')
    address=ab+0x784bb;loaded[address]^=1
    try:api['verify_loaded'](loaded_read,binding,eb,ab,sizes)
    except ValueError:extra.append(variant+'-loadedsite-mismatch-rejected')
    else:raise AssertionError('loaded-site mismatch accepted')
    loaded[address]^=1
    loaded[ab]^=1
    try:api['verify_loaded'](loaded_read,binding,eb,ab,sizes)
    except ValueError:extra.append(variant+'-loadedheader-mismatch-rejected')
    else:raise AssertionError('loadedheader mismatch accepted')
    loaded[ab]^=1
    if variant!='original':
        address=ab+0xd4000+binding['ranges'][-1]['length']-1;loaded[address]^=1
        try:api['verify_loaded'](loaded_read,binding,eb,ab,sizes)
        except ValueError:extra.append(variant+'-lastpayload-byte-rejected')
        else:raise AssertionError('payload mismatch accepted')
for bad in ('H1-M','B2a-N25-TECHNICAL','unknown'):
    try:api['trusted_binding'](bad)
    except ValueError:extra.append('untrusted-variant-'+bad)
    else:raise AssertionError('untrusted variant accepted')
(folder/'activatie-h3-binding.json').write_text(json.dumps(bindings,indent=2)+'\n')
result={'passed':len(checks)+len(extra),'research_checks':checks,'H3_checks':extra,'scope':'offline owned synthetic-memory fixtures and pinned diskbytes only','liveprocessread':False,'actual_goal_activation':False,'heap_ordering_proven':False,'real_AI_overhead_proven':False,'review_rejection_resolved_by_normal_code_only_reassessment':True}
(folder/'activatie-h3-decoder-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
