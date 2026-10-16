"""Prepare the one accepted type predicate repair; no install/native/process/UI."""
from pathlib import Path
import hashlib,json,difflib,datetime,ast
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
OLD=ROOT/'PROEVEN/u30-foutcodes/20261015T145000'
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(name,text):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,'utf-8')
files=['build_candidate.py','check_candidate.py','native.py','policy.py','integration_base.py','input-pins.py','bind_scheduler.py','preparation-manifest.json','release-v1.robotcom.backup.dll']
assert sha((OLD/'U30-40.prepared.dll').read_bytes())=='8610db83d4e424006f6c8ee3912bac11fd432dd2bb6264c7c9ed5b94fe67dc17'
sourcepins=[]
for name in files:
 data=(OLD/name).read_bytes();(OUT/name).write_bytes(data)
 sourcepins.append(dict(path=(OLD/name).relative_to(ROOT).as_posix(),sha256=sha(data),size=len(data)))
old="iface(r,P['udb'],['edi'],0xdc);r.test('eax','eax');r.j('jz','type_bad')"
new="iface(r,P['udb'],['edi'],0x1c);r.test('eax',0x80000000);r.j('jz','type_bad')"
s=(OUT/'native.py').read_text('utf-8');assert s.count(old)==1;write('native.py',s.replace(old,new))
s=(OUT/'input-pins.py').read_text('utf-8');assert 'SLOTS={0xc:' in s
s=s.replace('SLOTS={0xc:','SLOTS={0x1c:0x131940,0xc:').replace('ENGINE_BODIES={0x660f0:','ENGINE_BODIES={0x131940:0x1e,0x660f0:');write('input-pins.py',s)
prep=json.loads((OUT/'preparation-manifest.json').read_text('utf-8'))
for path in ['ANALYSE/U30-TYPE10.md','ONTWERP/U30-TYPE10.md']:
 prep['proposals'].append(dict(path=path,sha256=sha((ROOT/path).read_bytes())))
prep['source_pins']+=sourcepins
prep['stage']='TYPE10_PREPARATION_ONLY_NO_INSTALL_NATIVE_OR_GAME'
write('preparation-manifest.json',json.dumps(prep,indent=2)+'\n')
s=(OUT/'build_candidate.py').read_text('utf-8').replace("proposal_sha256=prep['proposals'][1]['sha256']","proposal_sha256=prep['proposals'][-1]['sha256']").replace('C1_SOURCE_CANDIDATE_ONLY_NOT_INSTALLED_NOT_NATIVE_NOT_GAMEPLAY','TYPE10_SOURCE_CANDIDATE_ONLY_NOT_INSTALLED_NOT_NATIVE_NOT_GAMEPLAY')
write('build_candidate.py',s)
reader='reader/Lees-Uitbreiding.py';s=(OLD/'r44-2/Lees-Uitbreiding.py').read_text('utf-8')
s=s.replace('[(0x543b0,0x41),','[(0x131940,0x1e),(0x3450b4,4),(0x542e0,0x30),(0x543b0,0x41),')
s=s.replace('scope=36,remaining=56,','scope=36,raw_t=44,raw_types=48,raw_d8=120,remaining=56,')
s=s.replace('        return shared\n','''        shared['raw_type_values_certified']=False
        shared['raw_type_values_note']='UNCERTIFIED intermediate values; zero may be initialization, not evidence of a completed resolver write'
        shared['raw_record']='UNKNOWN_NOT_BOUNDED_OR_INITIALIZED'
        if any(initialized.values()):
            raw_db=u32(eb+0x67dd18);raw_count=i32(raw_db)
            if 2<=raw_count<=4097 and 0<=shared['raw_t']<raw_count-1:
                raw_records=u32(raw_db+8);record=checked(raw_records,0x2c8*shared['raw_t'])
                raw30=u32(checked(record,0x30));raw34=u32(checked(record,0x34))
                shared['raw_record']=dict(certified=False,record30=raw30,record34=raw34,land_bit=bool(raw30&0x80000000),space_lander_bit=bool(raw34&0x20),space_launcher_bit=bool(raw34&0x10),note='UNCERTIFIED later bounded database read; does not prove resolver write or pass-time values')
        return shared
''')
write(reader,s)
for n in ['original_core.py','participants.json']:(OUT/'reader'/n).write_bytes((OLD/'r44-2'/n).read_bytes())
for name in ['native.py','input-pins.py','build_candidate.py','preparation-manifest.json']:
 write('diffs/'+name+'.diff',''.join(difflib.unified_diff((OLD/name).read_text('utf-8').splitlines(True),(OUT/name).read_text('utf-8').splitlines(True),fromfile='frozen-foutcodes/'+name,tofile='type10/'+name)))
write('diffs/Lees-Uitbreiding.py.diff',''.join(difflib.unified_diff((OLD/'r44-2/Lees-Uitbreiding.py').read_text('utf-8').splitlines(True),(OUT/reader).read_text('utf-8').splitlines(True),fromfile='frozen-r44-2/Lees-Uitbreiding.py',tofile='type10/reader/Lees-Uitbreiding.py')))
for p in OUT.rglob('*.py'):ast.parse(p.read_text('utf-8'),filename=str(p))
write('provenance.json',json.dumps(dict(created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),basis_candidate_sha256=sha((OLD/'U30-40.prepared.dll').read_bytes()),historical_package_unchanged=True,science_C2_integrated=False,source_pins=sourcepins,stage='SOURCE_ONLY'),indent=2)+'\n')
print('Prepared exact predicate, additive slot/body pins and optional bounded raw reader. No native calls.')
