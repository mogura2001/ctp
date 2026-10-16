"""C4 finite offline syntax/staging/source audit; never runs controller/main."""
from pathlib import Path
import sys,ast,json,hashlib,importlib.util,datetime
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()
for p in OUT.glob('*.py'):ast.parse(p.read_text('utf-8'),filename=str(p))
m=json.loads((OUT/'manifest.json').read_text('utf-8'));assert not (ROOT/m['T0_alias']['path']).exists()
assert m['T0_alias']['sha256']==m['T0_sha256'] and m['T0_alias']['existed_before'] is False
for row in m['files']:
 assert sha((ROOT/row['path']).read_bytes())==row['before_sha256']
 assert sha((OUT/'backups'/row['path']).read_bytes())==row['before_sha256']
 for arm in ['baseline','variant']:assert sha((OUT/'candidate'/arm/row['path']).read_bytes())==row[arm+'_sha256']
for row in m['preserved_saves_before']+[m['profile_before']]:
 assert sha((ROOT/row['path']).read_bytes())==row['sha256']
 assert sha((OUT/'protected-backups'/row['path']).read_bytes())==row['sha256']
for row in m['protected']+m['input_manifests']:assert sha((ROOT/row['path']).read_bytes())==row['sha256']
for path in m['T0_paths']:assert sha((ROOT/path).read_bytes())==m['T0_sha256']
sys.path.insert(0,str(OUT));spec=importlib.util.spec_from_file_location('c4_prepared_reader',OUT/'Lees-Uitbreiding.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
bindings=[]
for variant in ['release-v1','U30-40']:
 b=reader.trusted_binding(variant);bindings.append(dict(variant=variant,ai_sha256=b['ai']['sha256'],sites=len(b['sites']),ranges=len(b['ranges'])))
s=(OUT/'Uitbreiding.ps1').read_text('utf-8')
assert s.index('[ExpansionWindow]::SetProcessDPIAware()')<s.index('function OwnState')
assert 'pixel_width=$picture.Width' in s and 'physical_window=$physicalState' in s
assert 'CreateOwnT0Alias' in s and 'RemoveOwnT0Alias' in s
assert "Remove-Item -LiteralPath $paths.target" in s and '-Recurse' not in s
assert s.index('RemoveOwnT0Alias\n',s.index('function RestoreOwnInstallation'))>s.index("'restore.json'",s.index('function RestoreOwnInstallation'))
gate=json.loads((OUT/'C4-ROOT-VRIJGAVE.json').read_text('utf-8'));assert gate['allowed'] is False
sources=[dict(path=p.name,size=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(OUT.iterdir()) if p.suffix in ['.py','.ps1','.json','.fragment'] and p.name not in ['source-manifest.json','C4-ROOT-VRIJGAVE.json']]
report=dict(stage='C4_SOURCE_ONLY_ALIAS_NOT_CREATED_NO_INSTALL_START_RPM',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sources=sources,bindings=bindings,game_alias_absent=True,release_files_and_backups=19,existing_saves_and_backups=9,profile_match=True,controller_execute_count=0,RPM_calls=0,game_file_mutations=0,DPI_source_before_queries=True,physical_capture_metadata_source=True,alias_cleanup_exact_literal_after_restore=True,root_gate_disabled=True)
(OUT/'source-manifest.json').write_text(json.dumps(report,indent=2)+'\n','utf-8')
print(json.dumps(dict(stage=report['stage'],sources=len(sources),static_bindings=bindings,all_protected_match=True,alias_absent=True,source_manifest_sha256=sha((OUT/'source-manifest.json').read_bytes()))))
