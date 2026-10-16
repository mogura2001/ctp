"""Offline source syntax/binding/staging audit only. No reader main/RPM."""
from pathlib import Path
import sys,json,hashlib,ast,importlib.util,datetime,difflib
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()
for path in OUT.glob('*.py'):ast.parse(path.read_text('utf-8'),filename=str(path))
sys.path.insert(0,str(OUT));spec=importlib.util.spec_from_file_location('c3_reader_source',OUT/'Lees-Uitbreiding.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
bindings=[]
for variant in ['release-v1','U30-40']:
 binding=reader.trusted_binding(variant)
 bindings.append(dict(variant=variant,ai_sha256=binding['ai']['sha256'],sites=len(binding['sites']),ranges=len(binding['ranges']),module_size=binding['ai']['size'],new_shared_plan_rva=binding.get('shared_plan_rva'),engine_sha256=binding['engine']['sha256']))
manifest=json.loads((OUT/'manifest.json').read_text('utf-8'))
for row in manifest['files']:
 assert sha((ROOT/row['path']).read_bytes())==row['before_sha256']
 assert sha((OUT/'backups'/row['path']).read_bytes())==row['before_sha256']
 for arm in ['baseline','variant']:assert sha((OUT/'candidate'/arm/row['path']).read_bytes())==row[arm+'_sha256']
for row in manifest['preserved_saves_before']+[manifest['profile_before']]:
 assert sha((ROOT/row['path']).read_bytes())==row['sha256']
 assert sha((OUT/'protected-backups'/row['path']).read_bytes())==row['sha256']
for row in manifest['protected']+manifest['input_manifests']:assert sha((ROOT/row['path']).read_bytes())==row['sha256']
gate=json.loads((OUT/'C3-ROOT-VRIJGAVE.json').read_text('utf-8'));assert gate['allowed'] is False
old=ROOT/'PROEVEN/doel3/20261012T165300-baseline2/Doel3.ps1'
(OUT/'Doel3.ps1.diff').write_text(''.join(difflib.unified_diff(old.read_text('utf-8').splitlines(True),(OUT/'Uitbreiding.ps1').read_text('utf-8').splitlines(True),fromfile='readonly baseline2 controller',tofile='owned C3 controller')),'utf-8')
sources=[dict(path=path.relative_to(OUT).as_posix(),size=path.stat().st_size,sha256=sha(path.read_bytes())) for path in sorted(OUT.iterdir()) if path.suffix in ['.py','.ps1','.json'] and path.name not in ['source-manifest.json','source-checks.json','C3-ROOT-VRIJGAVE.json']]
report=dict(stage='C3_SOURCE_ONLY_NO_INSTALL_START_RPM',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reader_static_disk_binding=bindings,all_python_AST=True,controller_execute_count=0,process_queries=0,RPM_calls=0,read_handles_opened=0,installations=0,starts=0,release_staged_and_backed_up=19,protected_saves_backed_up=9,profile_backed_up=True,root_gate_disabled=True,sources=sources)
(OUT/'source-manifest.json').write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in report.items() if k!='sources'}))
