"""Independent read-only C4 file review; no game/process/memory access."""
from pathlib import Path
import ast, difflib, hashlib, json

ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'PROEVEN/pad-lokaal-onbekend/20261023-host'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={
 'SOURCE-PINS.json':'6b56fde8d93892e86665264851aae54b9880b525aaf3cd1b1d1fe30f773c4c27',
 'C4-PINS.json':'b0505f5d31c2b5313c8ce1a88adb24ce345771942eea1eef08980bcba95350eb',
}
counts={}
for name,pinsha in expected.items():
 assert sha(HERE/name)==pinsha,name
 rows=json.loads((HERE/name).read_text('utf-8'))['sources']
 for row in rows:
  p=ROOT/row['path']
  assert p.resolve().is_relative_to(ROOT) and sha(p)==row['sha256'],row['path']
 counts[name]=len(rows)
reference=json.loads((HERE/'REFERENCE-PINS.json').read_text('utf-8'))['unchanged_T0_T100']
assert [r['turn'] for r in reference]==list(range(101))
for row in reference:assert sha(ROOT/row['path'])==row['sha256'],row['path']
old=ROOT/'PROEVEN/uitbreiding-lang/20261022T122400'
for name,source in [('Lees-Duur.py',old/'Lees-Duur.py'),('scope.py',old/'scope.py'),('Pass-Duur.ps1',ROOT/'PROEVEN/uitbreiding-lang/20261022T171500-afronding/Afronding-85-100.ps1')]:
 diff=''.join(difflib.unified_diff(source.read_text('utf-8').splitlines(True),(HERE/name).read_text('utf-8').splitlines(True),fromfile=source.relative_to(ROOT).as_posix(),tofile=(HERE/name).relative_to(ROOT).as_posix()))
 assert diff==(HERE/(name+'.diff')).read_text('utf-8'),name
for p in HERE.glob('*.py'):ast.parse(p.read_text('utf-8'),filename=str(p))
for path in [HERE/'ROOT-CONTROL.json',HERE/'ROOT-HOST.json',HERE/'local4/ROOT-READER.json']:
 gate=json.loads(path.read_text('utf-8'))
 assert gate['allowed'] is False,path
 for key,value in gate.items():
  if key.endswith('_allowed') or key.startswith('review_T'):assert value in (False,None),key
print(json.dumps({'review':'ROOT_C4_FILES_ONLY','pins':counts,'reference_snapshots':len(reference),'diffs_exact':3,'python_syntax':True,'all_gates_false':True,'gameplay_tested':False},indent=2))

PREP=HERE.parent/'20261023-host-prep'
for name,wanted in [('SOURCE-PINS.json','561dfe56dbeaf9894fa975f3afea2271f7917f3b412aef2ce45479349b892719'),('C5-PINS.json','0886b510006d4be32b37ba7a7bac41fd80e3eecf207ef7afb684b7580e900129')]:
 assert sha(PREP/name)==wanted,name
 rows=json.loads((PREP/name).read_text('utf-8'))['sources']
 for row in rows:assert sha(ROOT/row['path'])==row['sha256'],row['path']
for name in ('Start-Monitored.ps1','Close-Normally.ps1','Restore.ps1'):
 source=ROOT/'PROEVEN/uitbreiding-lang-host/20261022/U30-40'/name
 diff=''.join(difflib.unified_diff(source.read_text('utf-8').splitlines(True),(PREP/name).read_text('utf-8').splitlines(True),fromfile=source.relative_to(ROOT).as_posix(),tofile=(PREP/name).relative_to(ROOT).as_posix()))
 assert diff==(PREP/(name+'.diff')).read_text('utf-8'),name
gate=json.loads((PREP/'ROOT-HOST.json').read_text('utf-8'))
assert all(gate[k] is False for k in ('allowed','install_allowed','start_allowed','close_allowed','restore_allowed'))
print(json.dumps({'review':'ROOT_C5_FILES_ONLY','source_pins':81,'delivery_pins':10,'diffs_exact':3,'all_gates_false':True,'helpers_executed':False},indent=2))
