"""Read-only review of operational copies, no process/game access."""
from pathlib import Path
import difflib,hashlib,json
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'PROEVEN/pad-lokaal-onbekend'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for directory,sourcehash,delivery,deliveryhash in [
 ('20261026-host','2f9f3ec2b96160d075820b83ac4570f75969834915d4f6543f37ce52d00107fe','C4-PINS.json','bad63490b15829b9de567ab4454165a7db51e744f33f5dafa844d19adf87cd2a'),
 ('20261026-host-prep','e3885de1b2aeb6d18c8938778eb1834a33bf31fe2e59563c9e7bd9eee54978e8','C5-PINS.json','807fede259513509a4a7e51fe1933b905ace6104f9213a86f321e19b06474d93')]:
 folder=BASE/directory
 for name,wanted in [('SOURCE-PINS.json',sourcehash),(delivery,deliveryhash)]:
  assert sha(folder/name)==wanted,name
  for row in json.loads((folder/name).read_text('utf-8'))['sources']:assert sha(ROOT/row['path'])==row['sha256'],row['path']
for suffix,names in [('-host',['Lees-Duur.py','scope.py','runtime_adapter.py','runtime-pins.json','HOST-PLAN.json','Pass-Duur.ps1','check_sources.py']),('-host-prep',['Start-Monitored.ps1','Close-Normally.ps1','Restore.ps1'])]:
 old=BASE/('20261023'+suffix);new=BASE/('20261026'+suffix)
 for name in names:
  diff=''.join(difflib.unified_diff((old/name).read_text('utf-8').splitlines(True),(new/name).read_text('utf-8').splitlines(True),fromfile=(old/name).relative_to(ROOT).as_posix(),tofile=(new/name).relative_to(ROOT).as_posix()))
  assert diff==(new/(name+'.diff')).read_text('utf-8'),name
print('ROOT_OPERATIONAL_COPY_PINS_AND_DIFFS_EXACT; NO_RUNTIME')
