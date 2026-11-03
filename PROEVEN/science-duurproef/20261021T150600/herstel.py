"""Minimal command-contract repair checks/pins only; never execute controller."""
from pathlib import Path
import difflib,hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OLD=HERE.parent/'20261021T145100'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=(OLD/'Pass-Duur.ps1').read_text('utf-8');own=(HERE/'Pass-Duur.ps1').read_text('utf-8')
expected=source.replace('science-duur-host/20261021/host1','science-duur-host/20261021/host2').replace(' -ExpectedProcessId $gate.pid -ExpectedCreationUtcMs $started.creation_utc_ms -ExpectedWindowHandle $window.window','')
assert own==expected
key=next(line for line in own.splitlines() if '$inputResult=& $tool' in line)
assert key=='$inputResult=& $tool -Action Key -Keys n'
contract=(ROOT/'PROEVEN/Bedien-CTP.ps1').read_text('utf-8')
assert "if ($Action -ne 'Capture')" in contract and "} elseif ($Action -eq 'Key')" in contract and '[Windows.Forms.SendKeys]::SendWait($Keys)' in contract
for name in ('Lees-Duur.py','scope.py'):assert sha(HERE/name)==sha(OLD/name)
(HERE/'controller.diff').write_text(''.join(difflib.unified_diff(source.splitlines(True),own.splitlines(True),fromfile='immutable failed host1 controller',tofile='own host2 controller')),'utf-8')
paths={ROOT/row['path'] for row in json.loads((OLD/'SOURCE-PINS.json').read_text('utf-8'))['sources']}
paths|={OLD/'SOURCE-PINS.json',OLD/'OFFLINE-CHECKS.json'}
paths|={HERE/name for name in ['Lees-Duur.py','scope.py','Pass-Duur.ps1','herstel.py','controller.diff','POWERSHELL-PARSE.json','C1-OVERDRACHT.md']}
for row in json.loads((OLD/'SOURCE-PINS.json').read_text('utf-8'))['sources']:assert sha(ROOT/row['path'])==row['sha256']
pins=dict(stage='SOURCE_ONLY_COMMAND_CONTRACT_REPAIR_NO_LIVE',sources=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in sorted(paths)])
(HERE/'SOURCE-PINS.json').write_text(json.dumps(pins,indent=2)+'\n','utf-8')
gate=json.loads((OLD/'ROOT-READER.json').read_text('utf-8-sig'));gate.update(allowed=False,control_allowed=False,pid=None,creation_filetime=None,run_id='science-duur-20261021-host2',output_directory=str(HERE/'variant'),source_pins_sha256=sha(HERE/'SOURCE-PINS.json'))
(HERE/'ROOT-READER.json').write_text(json.dumps(gate,indent=2)+'\n','utf-8')
print(json.dumps(dict(pins=len(pins['sources']),sha256=sha(HERE/'SOURCE-PINS.json'),reader_scope_unchanged=True,only_controller_contract_and_host_changed=True,live=False)))
