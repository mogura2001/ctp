"""Reuse pinned U30 emitter and C10 reader. No installation or process access."""
from pathlib import Path
import hashlib,json,difflib,datetime
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
OLD=ROOT/'PROEVEN/uitbreiding-30-40/20261012T181500'
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(name,data):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
def text(name,s):write(name,s.encode('utf-8'))
def pin(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p.read_bytes()),size=p.stat().st_size)
names=['build_candidate.py','check_candidate.py','native.py','policy.py','integration_base.py','input-pins.py','bind_scheduler.py','preparation-manifest.json','release-v1.robotcom.backup.dll']
old=json.loads((OLD/'candidate-manifest.json').read_text('utf-8'))
assert old['candidate_sha256']=='f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810'
assert sha((OLD/'U30-40.prepared.dll').read_bytes())==old['candidate_sha256']
for row in old['sources']+old['source_dependency_pins']+old['release_pins']:
 assert sha((ROOT/row['path']).read_bytes())==row['sha256'],row['path']
for name in names:write(name,(OLD/name).read_bytes())
s=(OUT/'policy.py').read_text('utf-8')
a="invoke(r,'bind_host');r.test('eax','eax');r.j('jz','final_bad')";b=a.replace('final_bad','final_done')
assert s.count(a)==1;s=s.replace(a,b)
a="  invoke(r,helper);r.test('eax','eax');r.j('jz','final_bad')";assert s.count(a)==1;s=s.replace(a,a.replace('final_bad','final_done'))
text('policy.py',s)
s=(OUT/'integration_base.py').read_text('utf-8');a="invoke(r,'bind_inputs');r.test('eax','eax');r.j('jz','bind_bad')";assert s.count(a)==1
text('integration_base.py',s.replace(a,a.replace('bind_bad','bind_done')))
# Reader remains at c10 depth so all original workspace/path guards remain valid.
for name in ['Lees-Uitbreiding.py','original_core.py','participants.json']:write('c10/'+name,(OLD/'c10'/name).read_bytes())
write('provenance/old-candidate-manifest.json',(OLD/'candidate-manifest.json').read_bytes())
text('provenance.json',json.dumps(dict(created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),old_candidate_sha256=old['candidate_sha256'],old_sources=old['sources'],old_manifest=pin(OLD/'candidate-manifest.json'),copied_inputs=[pin(OLD/n) for n in names],proposal=pin(ROOT/'ONTWERP/U30-FOUTCODES.md'),analysis=pin(ROOT/'ANALYSE/U30-REASON44.md')),indent=2)+'\n')
for name in ['policy.py','integration_base.py']:
 text(name+'.u30-source-diff.txt',''.join(difflib.unified_diff((OLD/name).read_text('utf-8').splitlines(True),(OUT/name).read_text('utf-8').splitlines(True),fromfile='tested-U30/'+name,tofile='owned-foutcodes/'+name)))
text('c10/C10-ROOT-VRIJGAVE.json',json.dumps(dict(allowed=False,baseline_allowed=False,candidate_sha256=None,sources=[],state='PREPARATION_ONLY_ROOT_REVIEW_REQUIRED'),indent=2)+'\n')
print('Prepared exact two source retargets; old pins verified; reader gate FALSE.')
