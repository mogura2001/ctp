"""Reproduce the reviewed source-only delta. No build/native/game/process access."""
from pathlib import Path
import ast, datetime, difflib, hashlib, json

OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
OLD=ROOT/'PROEVEN/u30-type10/20261015T194300'
READER=ROOT/'PROEVEN/u30-reason23/20261016T131100/host1'
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(name,s):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,'utf-8')
def pin(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p.read_bytes()),size=p.stat().st_size)
def replace(name,a,b):
 s=(OUT/name).read_text('utf-8');assert s.count(a)==1,(name,a);write(name,s.replace(a,b))

assert sha((OLD/'U30-40.prepared.dll').read_bytes())=='b6f272d2503edf5f1cf03f927ebd40ff5dd82b1a2c9d9c948beb4e7215baed62'
files=['build_candidate.py','check_candidate.py','native.py','policy.py','integration_base.py','input-pins.py','bind_scheduler.py','release-v1.robotcom.backup.dll']
sourcepins=[]
for name in files:
 (OUT/name).write_bytes((OLD/name).read_bytes());sourcepins.append(pin(OLD/name))
for name in ['Lees-Uitbreiding.py','original_core.py','h3_layout.py','participants.json']:
 p=OUT/'reader'/name;p.parent.mkdir(exist_ok=True);p.write_bytes((READER/name).read_bytes());sourcepins.append(pin(READER/name))

replace('native.py','source_overflow=216,classified=220)','source_overflow=216,classified=220,\n         prefix_count=224,known_count=228,gate_queries=232,gate_false=236)')
replace('native.py'," entry(r,'production_roles',96);r.mov(m('ebx',P['slots']),0);r.mov(m('ebp',-16),0)",""" entry(r,'production_roles',96);r.mov(m('ebx',P['slots']),0);r.mov(m('ebp',-16),0)
 # Validate the complete producer/consumer contract before ORDER access.
 r.mov('eax',m('ebx',P['prefix_count']));r.test('eax','eax');r.j('js','roles_bad');r.alu('cmp','eax',64);r.j('ja','roles_bad');r.alu('cmp','eax',m('ebx',P['known_count']));r.j('jg','roles_bad')
 r.mov('eax',m('ebx',P['known_count']));r.alu('cmp','eax',m('ebx',P['candidates']));r.j('jg','roles_bad');r.mov('eax',m('ebx',P['candidates']));r.alu('cmp','eax',4096);r.j('jg','roles_bad')""")
replace('native.py',"r.alu('cmp','eax',m('ebx',P['candidates']));r.j('jge','roles_ok');r.alu('cmp','eax',64);r.j('jae','roles_budget');", "r.alu('cmp','eax',m('ebx',P['prefix_count']));r.j('jge','roles_ok');")
replace('native.py',"r.mov('eax',m('edx'));r.shift('shl','eax',3);r.lea('edi',m('ebx',CAPTURE));", "r.mov('eax',m('edx'));r.test('eax','eax');r.j('js','roles_bad');r.alu('cmp','eax',m('ebx',P['candidates']));r.j('jae','roles_bad');r.shift('shl','eax',3);r.lea('edi',m('ebx',CAPTURE));")
replace('native.py',"r.j('jmp','roles_loop');r.j('jmp','roles_ok');r.label('roles_budget');r.mov(m('ebx',P['cutoff']),1);r.label('roles_ok');", "r.j('jmp','roles_loop');r.label('roles_ok');")

s=(OUT/'policy.py').read_text('utf-8');begin=s.index('def canonical_prefix(r):');end=s.index('\ndef finalize(r):',begin)
new="""def canonical_prefix(r):
 # Validate every copied key, but select only World+28-known centers.
 # VISITED is scratch only before DFS. CAPTURE retains original indices.
 n.entry(r,'canonical_prefix',64)
 for key in ('prefix_count','known_count','gate_queries','gate_false'):r.mov(m('ebx',n.P[key]),0)
 r.alu('cmp',m('ebx',n.P['nodes']),0);r.j('jne','prefix_bad');r.mov('eax',m('ebx',n.P['candidates']));r.test('eax','eax');r.j('js','prefix_bad');r.alu('cmp','eax',4096);r.j('jg','prefix_bad');r.mov(m('ebp',-16),0)
 r.label('prefix_keys');r.mov('eax',m('ebp',-16));r.alu('cmp','eax',m('ebx',n.P['candidates']));r.j('jge','prefix_choose');r.imul('edi','eax',n.NODE_STRIDE);r.alu('add','edi','ebx');r.alu('add','edi',n.VISITED);r.shift('shl','eax',3);r.lea('edx',m('ebx',n.CAPTURE));r.alu('add','edx','eax');r.mov(m('ebp',-32),'edx');r.push('edi');r.push('edx');r.push('ebx');r.j('call','canonical_key');r.test('eax','eax');r.j('jz','prefix_bad')
 # EDI is callee-saved; the external pointer survives in a separate local.
 r.mov('eax',m('ebp',-16));r.mov(m('edi',8),'eax');r.unary('inc',m('ebx',n.P['gate_queries']));n.iface(r,n.P['world'],[m('ebp',-32)],0x28);r.test('eax','eax');r.j('jz','prefix_unknown');r.unary('inc',m('ebx',n.P['known_count']));r.j('jmp','prefix_key_next')
 r.label('prefix_unknown');r.mov(m('edi',8),-1);r.unary('inc',m('ebx',n.P['gate_false']));r.label('prefix_key_next');r.unary('inc',m('ebp',-16));r.j('jmp','prefix_keys')
 r.label('prefix_choose');r.alu('cmp',m('ebx',n.P['known_count']),64);r.j('jle','prefix_no_cutoff');r.mov(m('ebx',n.P['cutoff']),1);r.label('prefix_no_cutoff');r.mov(m('ebp',-20),0);r.label('prefix_outer');r.mov('eax',m('ebp',-20));r.alu('cmp','eax',64);r.j('jae','prefix_ok');r.alu('cmp','eax',m('ebx',n.P['known_count']));r.j('jae','prefix_ok');r.mov(m('ebp',-24),-1);r.mov(m('ebp',-28),0)
 r.label('prefix_scan');r.mov('eax',m('ebp',-28));r.alu('cmp','eax',m('ebx',n.P['candidates']));r.j('jae','prefix_store');r.imul('edi','eax',n.NODE_STRIDE);r.alu('add','edi','ebx');r.alu('add','edi',n.VISITED);r.alu('cmp',m('edi',8),-1);r.j('je','prefix_next');r.alu('cmp',m('ebp',-24),-1);r.j('je','prefix_best');r.imul('eax',m('ebp',-24),n.NODE_STRIDE);r.alu('add','eax','ebx');r.alu('add','eax',n.VISITED);r.push('eax');r.push('edi');r.j('call','H3PosCompare');r.test('eax','eax');r.j('jge','prefix_next');r.label('prefix_best');r.mov('eax',m('ebp',-28));r.mov(m('ebp',-24),'eax');r.label('prefix_next');r.unary('inc',m('ebp',-28));r.j('jmp','prefix_scan')
 r.label('prefix_store');r.mov('eax',m('ebp',-24));r.test('eax','eax');r.j('js','prefix_bad');r.imul('edi','eax',n.NODE_STRIDE);r.alu('add','edi','ebx');r.alu('add','edi',n.VISITED);r.mov('eax',m('edi',8));r.mov(m('edi',8),-1);r.mov('edx',m('ebp',-20));r.shift('shl','edx',2);r.alu('add','edx','ebx');r.mov(m('edx',n.ORDER),'eax');r.unary('inc',m('ebx',n.P['prefix_count']));r.unary('inc',m('ebp',-20));r.j('jmp','prefix_outer');r.label('prefix_ok');r.mov('eax',1);r.j('jmp','prefix_done');r.label('prefix_bad');n.unknown(r,41);n.result(r,'prefix_done',64)
"""
write('policy.py',s[:begin]+new+s[end:])
replace('integration_base.py',"((0x3452e0,0x54,0x133880)","((0x3452e0,0x28,0x133580),(0x3452e0,0x54,0x133880)")
replace('input-pins.py','ENGINE_BODIES={0x131940:', 'ENGINE_BODIES={0x133580:0x25,0xbbd50:0x1c,0xebdf0:0x73,0x131940:')
replace('input-pins.py','only frozen T/D analysed read-only bodies and UnitDB slots','frozen T/D plus A-bounded World28 wrapper/gate bodies; UnitDB slots unchanged')
replace('build_candidate.py','TYPE10_SOURCE_CANDIDATE_ONLY_NOT_INSTALLED_NOT_NATIVE_NOT_GAMEPLAY','KAARTFILTER_SOURCE_CANDIDATE_ONLY_NOT_INSTALLED_NOT_NATIVE_NOT_GAMEPLAY')
replace('build_candidate.py',"paths+=list((ROOT/'PROEVEN/production-h3').glob('*.py'))", "paths+=list((OUT/'reader').glob('*.py'))+[OUT/'input-pins.json']\n paths+=list((ROOT/'PROEVEN/production-h3').glob('*.py'))")

# Reader pins intentionally fail closed until a separately reviewed build.
write('reader/runtime-pins.json',json.dumps(dict(stage='SOURCE_ONLY_UNBUILT',candidate_sha256=None,manifest_sha256=None,state_rva=None,state_size=0x54804),indent=2)+'\n')
s=(OUT/'reader/Lees-Uitbreiding.py').read_text('utf-8')
a=s.index("NEW_HASH=");b=s.index('original_binding=',a)
s=s[:a]+"""RUNTIME_PINS=json.loads((FOLDER/'runtime-pins.json').read_text('utf-8'))
NEW_HASH=RUNTIME_PINS['candidate_sha256']
MANIFEST_HASH=RUNTIME_PINS['manifest_sha256']
"""+s[b:]
s=s.replace("    binding=original_binding('original')","    if not NEW_HASH or not MANIFEST_HASH or RUNTIME_PINS['state_rva'] is None:raise ValueError('Source-only reader has no reviewed candidate pins')\n    binding=original_binding('original')")
s=s.replace("[(0x131940,0x1e),", "[(0x345308,4),(0x133580,0x25),(0xbbd50,0x1c),(0xebdf0,0x73),(0x131940,0x1e),")
s=s.replace("binding['shared_plan_rva']!=0xdd000", "binding['shared_plan_rva']!=RUNTIME_PINS['state_rva']")
s=s.replace("state_size!=0x54804", "state_size!=RUNTIME_PINS['state_size'] or state_size!=0x54804")
s=s.replace("tied=shared['reason']==23 and shared['classified']==1 and shared['h3calls']==1 and shared['slots']==0", """# Score-B skips can precede the unique H3 call after the new filter.
    prefix_valid=(0<=shared['prefix_count']<=64 and shared['prefix_count']==min(64,shared['known_count']) and 0<=shared['known_count']<=shared['candidates']<=4096 and shared['gate_queries']==shared['candidates']==shared['known_count']+shared['gate_false'] and shared['gate_false']>=0)
    tied=(prefix_valid and shared['context']==1 and shared['reason']==23 and 1<=shared['classified']<=shared['prefix_count'] and shared['h3calls']==1 and shared['slots']==0)""")
s=s.replace("'UNKNOWN_FIRSTCALL_PASS_PATTERN'","'UNKNOWN_UNIQUE_H3_CALL_ATTRIBUTION'")
s=s.replace('firstcall_attribution=attribution,firstcall_pattern=tied,','unique_h3_call_attribution=attribution,unique_h3_call_pattern=tied,first_classification_required=False,')
s=s.replace('classified=220,candidates=68,','classified=220,prefix_count=224,known_count=228,gate_queries=232,gate_false=236,candidates=68,')
s=s.replace("FOLDER/'C10-ROOT-VRIJGAVE.json'", "FOLDER/'KAARTFILTER-ROOT-VRIJGAVE.json'")
write('reader/Lees-Uitbreiding.py',s)

prep=json.loads((OLD/'preparation-manifest.json').read_text('utf-8'))
prep['stage']='KAARTFILTER_SOURCE_PREPARATION_ONLY_NO_BUILD_NATIVE_OR_GAME'
prep['checked_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
prep['source_pins']+=sourcepins
prep['basis_candidate_sha256']='b6f272d2503edf5f1cf03f927ebd40ff5dd82b1a2c9d9c948beb4e7215baed62'
for name in ['ANALYSE/U30-H2-GATE28.md','ONTWERP/U30-KAARTKENNISFILTER.md']:
 prep['proposals'].append(pin(ROOT/name))
write('preparation-manifest.json',json.dumps(prep,indent=2)+'\n')
for name in ['native.py','policy.py','integration_base.py','input-pins.py','build_candidate.py','preparation-manifest.json']:
 write('diffs/'+name+'.diff',''.join(difflib.unified_diff((OLD/name).read_text('utf-8').splitlines(True),(OUT/name).read_text('utf-8').splitlines(True),fromfile='frozen-type10/'+name,tofile='kaartfilter/'+name)))
write('diffs/Lees-Uitbreiding.py.diff',''.join(difflib.unified_diff((READER/'Lees-Uitbreiding.py').read_text('utf-8').splitlines(True),s.splitlines(True),fromfile='frozen-reason23-host1/Lees-Uitbreiding.py',tofile='kaartfilter/reader/Lees-Uitbreiding.py')))
for p in OUT.rglob('*.py'):ast.parse(p.read_text('utf-8'),filename=str(p))
write('provenance.json',json.dumps(dict(stage='SOURCE_ONLY_UNBUILT_UNTESTED',created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),basis_candidate_sha256=prep['basis_candidate_sha256'],historical_package_unchanged=True,science_C2_integrated=False,source_pins=sourcepins),indent=2)+'\n')
print('Source delta prepared; no candidate built, native code compiled/called, RPM or game run.')
