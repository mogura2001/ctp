"""Bind only this owned offline B2a package. No installation or game action."""
from pathlib import Path
import json,hashlib
OUT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
results=json.loads((OUT/'offline-results.json').read_text());assert results['pass']
files={}
for p in sorted(OUT.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p.name!='package-manifest.json':files[p.relative_to(OUT).as_posix()]={'size':p.stat().st_size,'sha256':sha(p.read_bytes())}
manifest={'status':'B2a offline candidate package checked; not installed or measured in gameplay','production_N_chosen':False,'variants':results['variants'],'protected_files_unchanged':results['protected_files_unchanged'],'previous_package_files_unchanged':results['previous_package_files_unchanged'],'files':files}
(OUT/'package-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({'artifact_files':len(files),'checked':True,'gameplay_measured':False,'installed':False}))
