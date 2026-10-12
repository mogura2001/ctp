"""Hash the existing protected B2 baseline paths; read-only installations."""
from pathlib import Path
import sys,json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
baseline=json.loads((ROOT/'PROEVEN/opening-b2/protected-after-native.json').read_text(encoding='utf-8-sig'))
previous=json.loads((ROOT/'PROEVEN/opening-b2/previous-packages-before.json').read_text(encoding='utf-8-sig'))
install_count=len(baseline);baseline.update(previous)
actual={};delta=[]
for name,row in baseline.items():
 path=ROOT/name
 if not path.is_file():delta.append(dict(path=name,reason='missing'));continue
 raw=path.read_bytes();current=dict(size=len(raw),sha256=hashlib.sha256(raw).hexdigest());actual[name]=current
 if current!=row:delta.append(dict(path=name,before=row,after=current))
members=set()
for tree in ('CTP-og','CTP-AAIP','CTP-proef','PROEVEN/settlerquota/vaste-start'):
 members.update(p.relative_to(ROOT).as_posix() for p in (ROOT/tree).rglob('*') if p.is_file())
expected=set(baseline)-set(previous)
if members!=expected:delta.append(dict(reason='installation membership difference',added=sorted(members-expected),missing=sorted(expected-members)))
record=dict(checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),baseline=['PROEVEN/opening-b2/protected-after-native.json','PROEVEN/opening-b2/previous-packages-before.json'],installation_files=install_count,previous_package_files=len(previous),files=len(baseline),deltas=delta,pass_=not delta,scope='existing protected installation/save/user changes and H1/H3 paths; exact installation membership; no modifications')
(OUT/'protected-after-native.json').write_text(json.dumps(actual,indent=2)+'\n')
(OUT/'protected-check.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
if delta:raise SystemExit(1)
