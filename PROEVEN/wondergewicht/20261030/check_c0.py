"""Finite package/composition/text-guard checks. No process access or live writes."""
from pathlib import Path
import copy, hashlib, importlib.util, json, shutil, sys, tempfile
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = ROOT/'VERSIES/wonders-2026-10-28'
NEW = ROOT/'VERSIES/wondergewicht-2026-10-30'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = json.loads((NEW/'manifest.json').read_text('utf-8'))
assert len(manifest['files']) == 15
same, changed = [], []
for item in manifest['files']:
    path = NEW/item['candidate_package_rel']
    assert len(path.read_bytes()) == item['after_size'] and sha(path) == item['after_sha256']
    old = (OLD/item['candidate_package_rel']).read_bytes()
    if old == path.read_bytes():
        same.append(item['target_rel'])
    else:
        assert item['target_rel'].endswith('/opening_wonders.aip')
        assert old.count(b'9100.0') == 1 and path.read_bytes() == old.replace(b'9100.0', b'30000.0')
        changed.append(item['target_rel'])
    if item['before_existed']:
        assert sha(NEW/item['backup_package_rel']) == item['before_sha256']
assert len(same) == 14 and len(changed) == 1
assert (NEW/'live-baseline.json').read_bytes() == (OLD/'live-baseline.json').read_bytes()
spec = importlib.util.spec_from_file_location('c4_offline', HERE/'Lees-Wondergewicht.py')
c4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c4)
c4.verify_pins()
c3 = c4.load_c3()
assert c3.HERE == HERE and c3.BASE == ROOT/'PROEVEN/wonderbewijs/20261029'
c2 = c3.load_base()
c1 = c2.load_base()
assert c1.WONDERS == NEW
for name in ('participants.json', 'binding-windows.json'):
    assert (HERE/name).read_bytes() == (ROOT/'PROEVEN/wonderbouw-kans/20261029'/name).read_bytes()
fixture = dict(opening_symbols={'opening_required': 1}, effective_wonder_list={
    'count': 1, 'records': [dict(weight=30000.0, native_index=2, category=-1)]})
assert c4.weight_expectation(fixture)['status'] == 'PASS'
bad = copy.deepcopy(fixture); bad['effective_wonder_list']['records'][0]['weight'] = 9100.0
assert c4.weight_expectation(bad)['status'] == 'FAIL'
bad = copy.deepcopy(fixture); bad['effective_wonder_list']['records'][0]['native_index'] = 3
assert c4.weight_expectation(bad)['status'] == 'FAIL'
with tempfile.TemporaryDirectory(prefix='c4-text-', dir=HERE) as temporary:
    temp = Path(temporary).resolve()
    assert temp.is_relative_to(HERE.resolve())
    data = temp/'CTP-proef/ctp_data/default/aidata'
    shutil.copytree(ROOT/'CTP-proef/ctp_data/default/aidata', data)
    for item in manifest['files']:
        target = temp/'CTP-proef'/item['target_rel']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(NEW/item['candidate_package_rel'], target)
    c1.ROOT = temp
    disk = c1.text_expectations('candidate')
    assert disk['aidata_files'] == 126
    target = data/'AIPs/opening_wonders.aip'
    target.write_bytes(target.read_bytes()+b'// unexpected text\r\n')
    try:
        c1.text_expectations('candidate')
    except ValueError as exc:
        assert 'disk text inventory mismatch' in str(exc)
    else:
        raise AssertionError('Unexpected effective text was accepted')
result = dict(pass_all=True, identical_candidate_files=14, numeric_change_files=1,
              complete_source_pins_verified=True, exact_restore_backups_verified=True,
              composition_paths=True, weighted_expectation_cases=3,
              exact_candidate_inventory_126=True, unexpected_text_rejected=True,
              live_writes=False, process_access=False, gui=False)
(HERE/'C0-result.json').write_text(json.dumps(result, indent=2)+'\n', 'utf-8')
print(json.dumps(result, indent=2))
