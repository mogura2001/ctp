"""Finite C4 to C5 source copy; no controller/main, process query or game writes."""
from pathlib import Path
import json, hashlib, shutil, difflib, sys
sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
OLD = OUT.parent / 'c4'
ROOT = OUT.parents[3]
sha = lambda b: hashlib.sha256(b).hexdigest()
assert not (OUT / 'manifest.json').exists(), 'Preserve existing preparation'
for folder in ['backups', 'candidate', 'protected-backups']:
    shutil.copytree(OLD / folder, OUT / folder)
for filename in ['original_core.py', 'participants.json']:
    shutil.copyfile(OLD / filename, OUT / filename)
fragment = (OLD / 'alias-functions.ps1.fragment').read_text('utf-8').replace('C4_UI_LOAD_ALIAS_ONLY', 'C5_UI_LOAD_ALIAS_ONLY')
(OUT / 'alias-functions.ps1.fragment').write_text(fragment, 'utf-8')
m = json.loads((OLD / 'manifest.json').read_text('utf-8'))
m['state'] = 'C5_SOURCE_ONLY_NO_ALIAS_INSTALL_START_RPM'
m['T0_alias']['ownership'] = 'C5_UI_LOAD_ALIAS_ONLY'
assert not (ROOT / m['T0_alias']['path']).exists()
m['input_manifests'].append(dict(path='ONTWERP/UI-FOCUS-CURSOR-U30-40.md', sha256=sha((ROOT / 'ONTWERP/UI-FOCUS-CURSOR-U30-40.md').read_bytes())))
(OUT / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n', 'utf-8')
s = (OLD / 'Uitbreiding.ps1').read_text('utf-8')
for old, new in [('C4-ROOT-VRIJGAVE', 'C5-ROOT-VRIJGAVE'), ('C4 source', 'C5 source'), ('C4 root', 'C5 root'), ('First C4', 'First C5'), ('UITBREIDING-20261013-C4', 'UITBREIDING-20261013-C5'), ('uitbreiding-20261013-c4', 'uitbreiding-20261013-c5'), ('C4_UI_LOAD_ALIAS_ONLY', 'C5_UI_LOAD_ALIAS_ONLY')]:
    s = s.replace(old, new)
old_guard = 'CheckInstalled\nOwnState $started -BindWindow -RequireFocus|Out-Null\nswitch($Action)'
new_guard = "CheckInstalled\nif($Action -eq 'Capture'){OwnState $started -BindWindow|Out-Null}else{OwnState $started -BindWindow -RequireFocus|Out-Null}\nswitch($Action)"
assert s.count(old_guard) == 1
s = s.replace(old_guard, new_guard)
old_capture = " 'Capture'{\n  $result=& powershell.exe"
new_capture = """ 'Capture'{
  $beforeCapture=OwnState $started -BindWindow
  if($beforeCapture.foreground_handle -ne $started.handle){
   $attemptPath=Join-Path $armDir 'focus-restore-attempt.json'
   if(Test-Path -LiteralPath $attemptPath){throw 'Second focus loss; no repeat focus attempt.'}
   JsonFile @{at=(Get-Date).ToString('o');attempt_count=1;action='UNCHANGED_BEDIEN_CTP_CAPTURE';own_state=$beforeCapture} 'focus-restore-attempt.json'
  }
  $result=& powershell.exe"""
assert s.count(old_capture) == 1
s = s.replace(old_capture, new_capture)
assert s.count('$physicalState=OwnState $started -BindWindow\n') == 1
s = s.replace('$physicalState=OwnState $started -BindWindow\n', '$physicalState=OwnState $started -BindWindow -RequireFocus\n')
old_picture = "  try{JsonFile @{image=$imagePath;pixel_width=$picture.Width"
new_picture = "  try{if($picture.Width -ne $physicalState.bounds.width -or $picture.Height -ne $physicalState.bounds.height){throw 'Captured physical PNG/window dimensions mismatch.'};JsonFile @{image=$imagePath;pixel_width=$picture.Width"
assert s.count(old_picture) == 1
s = s.replace(old_picture, new_picture)
(OUT / 'Uitbreiding.ps1').write_text(s, 'utf-8')
r = (OLD / 'Lees-Uitbreiding.py').read_text('utf-8').replace('C4-ROOT-VRIJGAVE', 'C5-ROOT-VRIJGAVE').replace('C4 source', 'C5 source').replace('First C4', 'First C5')
(OUT / 'Lees-Uitbreiding.py').write_text(r, 'utf-8')
for name in ['Uitbreiding.ps1', 'Lees-Uitbreiding.py', 'manifest.json', 'alias-functions.ps1.fragment', 'prepare.py', 'check_source.py']:
    if (OUT / name).exists():
        (OUT / (name + '.diff')).write_text(''.join(difflib.unified_diff((OLD / name).read_text('utf-8').splitlines(True), (OUT / name).read_text('utf-8').splitlines(True), fromfile='preserved C4/' + name, tofile='owned C5/' + name)), 'utf-8')
(OUT / 'C5-ROOT-VRIJGAVE.json').write_text(json.dumps(dict(allowed=False, baseline_allowed=False, candidate_sha256='f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810', sources=[], state='SOURCE_ONLY_NO_ALIAS_CREATE_OR_LIVE'), indent=2) + '\n', 'utf-8')
print(json.dumps(dict(stage=m['state'], game_file_mutations=0)))
