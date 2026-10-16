"""Finite C5 to C6 source copy only; no controller/main/process query/game writes."""
from pathlib import Path
import json, hashlib, shutil, difflib, sys
sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
OLD = OUT.parent / 'c5'
ROOT = OUT.parents[3]
sha = lambda b: hashlib.sha256(b).hexdigest()
assert not (OUT / 'manifest.json').exists(), 'Preserve existing preparation'
for folder in ['backups', 'candidate', 'protected-backups']:
    shutil.copytree(OLD / folder, OUT / folder)
for filename in ['original_core.py', 'participants.json']:
    shutil.copyfile(OLD / filename, OUT / filename)
for name in ['Uitbreiding.ps1', 'Lees-Uitbreiding.py', 'alias-functions.ps1.fragment']:
    s = (OLD / name).read_text('utf-8')
    for old, new in [('C5', 'C6'), ('20261013-C6', '20261014-C6'), ('20261013-c5', '20261014-c6')]:
        s = s.replace(old, new)
    (OUT / name).write_text(s, 'utf-8')
m = json.loads((OLD / 'manifest.json').read_text('utf-8'))
m['state'] = 'C6_SOURCE_ONLY_NO_ALIAS_INSTALL_START_RPM'
m['T0_alias']['ownership'] = 'C6_UI_LOAD_ALIAS_ONLY'
assert not (ROOT / m['T0_alias']['path']).exists()
(OUT / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n', 'utf-8')
for name in ['Uitbreiding.ps1', 'Lees-Uitbreiding.py', 'manifest.json', 'alias-functions.ps1.fragment', 'prepare.py', 'check_source.py', 'UITVOERINSTRUCTIE.md']:
    if (OUT / name).exists():
        (OUT / (name + '.diff')).write_text(''.join(difflib.unified_diff((OLD / name).read_text('utf-8').splitlines(True), (OUT / name).read_text('utf-8').splitlines(True), fromfile='preserved C5/' + name, tofile='owned C6/' + name)), 'utf-8')
(OUT / 'C6-ROOT-VRIJGAVE.json').write_text(json.dumps(dict(allowed=False, baseline_allowed=False, candidate_sha256='f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810', sources=[], state='SOURCE_ONLY_NO_ALIAS_CREATE_OR_LIVE', previous_arm='C5_CLOSED_CONSUMED_NO_REUSE'), indent=2) + '\n', 'utf-8')
print(json.dumps(dict(stage=m['state'], game_file_mutations=0)))
