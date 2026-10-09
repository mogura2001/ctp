"""Read-only protected inventory after native checks; package manifest."""
import json,hashlib
from pathlib import Path
import build
OUT=Path(__file__).resolve().parent
before=json.loads((OUT/'protected-before.json').read_text());after=build.inventory()
assert before==after,'protected installation/save mutation detected'
build.jwrite('protected-after-native.json',after)
for variant in ('H1-I','H1-M'):
    for mode in ('fixture','loader'):
        result=json.loads((OUT/f'{variant}.native-{mode}.json').read_text(encoding='utf-8-sig'))
        assert result['pass'] and result['bitness']==32
processes=json.loads((OUT/'native-processes.json').read_text())
assert all(p['exit_code']==0 and not p['timeout'] for p in processes['processes'])
b1names=('default','cleric','milmany','milfew','scimany','scifew','slaver','citywall_science')
casepaths={path.casefold():path for path in after}
b1={name:{'path':casepaths[f'CTP-proef/ctp_data/default/aidata/AIPs/{name}.aip'.casefold()],**after[casepaths[f'CTP-proef/ctp_data/default/aidata/AIPs/{name}.aip'.casefold()]]} for name in b1names}
start={name:value for name,value in after.items() if name.startswith('PROEVEN/settlerquota/vaste-start/')}
manifest={'scope':'candidates built and offline/native checked; not installed; no gameplay measurements','protected_files':len(after),'protected_before_after_identical':True,'design_sha256':build.DESIGN,'original_sha256':build.HASH,'B1_constant_proof_files':b1,'fixed_T0_inventory':start,'artifacts':{}}
for path in sorted(OUT.rglob('*')):
    if path.is_file() and path.name!='package-manifest.json' and '__pycache__' not in path.parts:
        data=path.read_bytes();manifest['artifacts'][path.relative_to(OUT).as_posix()]={'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(OUT/'package-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'protected_files':len(after),'identical':True,'B1_files':b1,'T0_inventory':start},indent=2))
