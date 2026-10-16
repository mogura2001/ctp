"""Finite C6->C7 source/staging copy only; no game/process/controller calls."""
from pathlib import Path
import json,hashlib,shutil,sys
sys.dont_write_bytecode=True
from delta import apply
OUT=Path(__file__).resolve().parent;OLD=OUT.parent/'c6';ROOT=OUT.parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()
PROPOSAL='46bb147baf46782b998927db9b2f0dd321d657cdafc48448a7b3537c08430978'
assert sha((ROOT/'ONTWERP/UI-TIJDRESERVE-U30-40-C7.md').read_bytes())==PROPOSAL
assert not (OUT/'manifest.json').exists(),'Preserve existing preparation'
old_sources=json.loads((OLD/'source-manifest.json').read_text('utf-8'))
for pin in old_sources['sources']:assert sha((OLD/pin['path']).read_bytes())==pin['sha256']
for folder in ['backups','candidate','protected-backups']:shutil.copytree(OLD/folder,OUT/folder)
for name in ['original_core.py','participants.json']:shutil.copyfile(OLD/name,OUT/name)
(OUT/'Uitbreiding.ps1').write_text(apply((OLD/'Uitbreiding.ps1').read_text('utf-8')),'utf-8')
for name in ['Lees-Uitbreiding.py','alias-functions.ps1.fragment']:
 (OUT/name).write_text((OLD/name).read_text('utf-8').replace('C6','C7'),'utf-8')
m=json.loads((OLD/'manifest.json').read_text('utf-8'))
m.update(state='C7_SOURCE_ONLY_NO_ALIAS_INSTALL_START_RPM',input_mode='HUMAN_ONE_N',c7_proposal_sha256=PROPOSAL)
m['T0_alias']['ownership']='C7_UI_LOAD_ALIAS_ONLY'
m['input_manifests'].append(dict(path='ONTWERP/UI-TIJDRESERVE-U30-40-C7.md',sha256=PROPOSAL))
assert not (ROOT/m['T0_alias']['path']).exists()
(OUT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n','utf-8')
(OUT/'C7-ROOT-VRIJGAVE.json').write_text(json.dumps(dict(allowed=False,baseline_allowed=False,input_mode='HUMAN_ONE_N',candidate_sha256='f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810',proposal_sha256=PROPOSAL,sources=[],state='SOURCE_ONLY_NO_ALIAS_CREATE_OR_LIVE',previous_arm='C6_CLOSED_CONSUMED_NO_REUSE'),indent=2)+'\n','utf-8')
print(json.dumps(dict(stage=m['state'],game_file_mutations=0)))
