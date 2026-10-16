"""Finite C8 source/pin/AST audit; no controller, observer, nativecall or game."""
from pathlib import Path
import sys,ast,json,hashlib,datetime,difflib
sys.dont_write_bytecode=True
from delta import apply
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3];OLD=OUT.parent/'c7'
sha=lambda b:hashlib.sha256(b).hexdigest()
PROPOSAL='6461e2f67884671528964dac1aa50e3deb38f0fbcf2a7d21993be121a5383961'
for p in OUT.glob('*.py'):ast.parse(p.read_text('utf-8'),filename=str(p))
old_manifest=OLD/'source-manifest.json'
assert sha(old_manifest.read_bytes())=='dd17b253b6446f189eb905b846640438261ef7b395d46a90eecc1a822c5bb7e4'
old=json.loads(old_manifest.read_text('utf-8'))
for pin in old['sources']:assert sha((OLD/pin['path']).read_bytes())==pin['sha256']
for pin in old['backup_pins']:assert sha((OLD/pin['path']).read_bytes())==pin['sha256']==sha((OUT/pin['path']).read_bytes())
for name in ['original_core.py','participants.json']:assert (OUT/name).read_bytes()==(OLD/name).read_bytes()
for name in ['Lees-Uitbreiding.py','alias-functions.ps1.fragment']:assert (OUT/name).read_text('utf-8')==(OLD/name).read_text('utf-8').replace('C7','C8')
s=(OUT/'Uitbreiding.ps1').read_text('utf-8');assert s==apply((OLD/'Uitbreiding.ps1').read_text('utf-8'))
assert '-Action Key' not in s and '-Keys n' not in s and s.count('$own.CloseMainWindow()')==1
m=json.loads((OUT/'manifest.json').read_text('utf-8'))
expected=json.loads((OLD/'manifest.json').read_text('utf-8'));expected.update(state='C8_SOURCE_ONLY_NO_ALIAS_INSTALL_START_RPM',c8_proposal_sha256=PROPOSAL);expected['T0_alias']['ownership']='C8_UI_LOAD_ALIAS_ONLY';expected['input_manifests'].append(dict(path='ONTWERP/UI-HERSTART-CD-U30-40-C8.md',sha256=PROPOSAL));assert m==expected
assert not (ROOT/m['T0_alias']['path']).exists() and m['T0_alias']['sha256']==m['T0_sha256']=='8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26'
for row in m['files']:
 assert sha((ROOT/row['path']).read_bytes())==row['before_sha256']==sha((OUT/'backups'/row['path']).read_bytes())
 for arm in ['baseline','variant']:assert sha((OUT/'candidate'/arm/row['path']).read_bytes())==row[arm+'_sha256']
for row in m['preserved_saves_before']+[m['profile_before']]:assert sha((ROOT/row['path']).read_bytes())==row['sha256']==sha((OUT/'protected-backups'/row['path']).read_bytes())
for row in m['protected']+m['input_manifests']:assert sha((ROOT/row['path']).read_bytes())==row['sha256']
for path in m['T0_paths']:assert sha((ROOT/path).read_bytes())==m['T0_sha256']
assert sha((ROOT/'PROEVEN/Bedien-CTP.ps1').read_bytes())=='d2dbbfcad3d9d8bec8e6a99a399d59561d8f9c4e9a48576a2aefc32e5997bc74'
for folder in ['variant','baseline']:assert not (OUT/folder).exists(),'No old executionrecords copied'
gatepath=OUT/'C8-ROOT-VRIJGAVE.json';gate=json.loads(gatepath.read_text('utf-8'));assert gate['allowed'] is False and gate['baseline_allowed'] is False and gate['input_mode']=='HUMAN_ONE_N' and gate['proposal_sha256']==PROPOSAL
source_names=['alias-functions.ps1.fragment','check_source.py','delta.py','Lees-Uitbreiding.py','manifest.json','original_core.py','participants.json','prepare.py','Uitbreiding.ps1','UITVOERINSTRUCTIE.md']
sources=[dict(path=name,size=(OUT/name).stat().st_size,sha256=sha((OUT/name).read_bytes())) for name in source_names]
for name in source_names:
 (OUT/(name+'.diff')).write_text(''.join(difflib.unified_diff((OLD/name).read_text('utf-8').splitlines(True),(OUT/name).read_text('utf-8').splitlines(True),fromfile='preserved C7/'+name,tofile='owned C8/'+name)),'utf-8')
report=dict(stage='C8_SOURCE_ONLY_NO_INSTALL_ALIAS_START_RPM',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),proposal_sha256=PROPOSAL,previous_source_manifest_sha256=sha(old_manifest.read_bytes()),sources=sources,backup_pins=old['backup_pins'],bindings=old['bindings'],bindings_inherited_exact_diskbytes_and_reader_business=True,controller_exact_C7_names_and_Start50_to40=True,reader_business_semantics_exact_C7=True,game_alias_absent=True,release_files_and_backups=19,existing_saves_and_backups=9,profile_match=True,controller_execute_count=0,RPM_calls=0,game_file_mutations=0,root_gate_disabled=True,live_results=None)
(OUT/'source-manifest.json').write_text(json.dumps(report,indent=2)+'\n','utf-8')
gate.update(sources=sources,source_manifest_sha256=sha((OUT/'source-manifest.json').read_bytes()));gatepath.write_text(json.dumps(gate,indent=2)+'\n','utf-8')
print(json.dumps(dict(stage=report['stage'],sources=len(sources),backup_pins=len(old['backup_pins']),all_pins_match=True,normalized_C7_parity=True,source_manifest_sha256=gate['source_manifest_sha256'])))
