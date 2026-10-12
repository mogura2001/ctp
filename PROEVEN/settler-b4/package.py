"""Freeze exact own source/artifacts/evidence for independent root review."""
from pathlib import Path
import hashlib,json,datetime
OUT=Path(__file__).resolve().parent
files={}
for path in sorted(OUT.rglob('*')):
 if path.is_file() and path.name!='package-manifest.json' and '__pycache__' not in path.parts:
  raw=path.read_bytes();files[path.relative_to(OUT).as_posix()]=dict(size=len(raw),sha256=hashlib.sha256(raw).hexdigest())
manifest=dict(reported_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='B4 phase C complete offline artifact handoff; explicit controlled fixture/native guard scopes; rootreview pending; not installed',files=files)
(OUT/'package-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(dict(files=len(files),package_sha256=hashlib.sha256((OUT/'package-manifest.json').read_bytes()).hexdigest())))
