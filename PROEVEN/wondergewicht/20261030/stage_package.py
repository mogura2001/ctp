"""Stage the accepted single numeric difference; never touches CTP-proef."""
from pathlib import Path
import copy, datetime, difflib, hashlib, json, shutil
ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT/'VERSIES/wonders-2026-10-28'
NEW = ROOT/'VERSIES/wondergewicht-2026-10-30'
HERE = Path(__file__).resolve().parent
assert not NEW.exists(), 'Package already staged; do not overwrite'
NEW.mkdir(parents=True)
old = json.loads((OLD/'manifest.json').read_text('utf-8'))
manifest = copy.deepcopy(old)
manifest.update(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                package_path_base='VERSIES/wondergewicht-2026-10-30',
                parent_manifest_sha256=hashlib.sha256((OLD/'manifest.json').read_bytes()).hexdigest(),
                numerical_change={'from': 9100.0, 'to': 30000.0})
diffs = []
for item in manifest['files']:
    rel = item['candidate_package_rel']
    source = OLD/rel
    before = source.read_bytes()
    assert hashlib.sha256(before).hexdigest() == item['after_sha256']
    after = before
    if item['target_rel'].endswith('/opening_wonders.aip'):
        assert before.count(b'9100.0') == 1
        after = before.replace(b'9100.0', b'30000.0')
        item.update(after_sha256=hashlib.sha256(after).hexdigest(), after_size=len(after))
        diffs.extend(difflib.unified_diff(before.decode().splitlines(True), after.decode().splitlines(True),
                     fromfile='wonders-2026-10-28/'+rel, tofile='wondergewicht-2026-10-30/'+rel))
    dest = NEW/rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(after)
    if item['before_existed']:
        backup = OLD/item['backup_package_rel']
        assert hashlib.sha256(backup.read_bytes()).hexdigest() == item['before_sha256']
        dest = NEW/item['backup_package_rel']
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(backup, dest)
shutil.copyfile(OLD/'live-baseline.json', NEW/'live-baseline.json')
(NEW/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', 'utf-8')
(NEW/'wijzigingen.diff').write_text(''.join(diffs), 'utf-8')
for name in ('participants.json', 'binding-windows.json'):
    shutil.copyfile(ROOT/'PROEVEN/wonderbouw-kans/20261029'/name, HERE/name)
print('Staged 15 files; no live installation.')
