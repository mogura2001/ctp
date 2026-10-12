from pathlib import Path
import datetime, difflib, hashlib, json, re

ROOT = Path(r'C:\GIT\ctp')
OUT = Path(__file__).resolve().parent
SRC = ROOT / 'CTP-proef/ctp_data/default/aidata'
B2B = ROOT / 'PROEVEN/opening-b2/regering-b2b/20261010T180801159'
DESIGN = 'ea5140b5505c11f457bdcdc3cf41fcc023e277bf247866228ad356919c9ef40e'
ROUTES = {'Cleric': 'cleric', 'Slaver': 'slaver', 'SciFew': 'scifew',
          'SciMany': 'scimany', 'WarFew': 'milfew', 'WarMany': 'milmany'}

def sha(data): return hashlib.sha256(data).hexdigest()
def emit(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

assert sha((ROOT / 'ONTWERP/GEZAMENLIJKE-OPENING-B2.md').read_bytes()) == DESIGN
pins_path = ROOT / 'PROEVEN/opening-b2/protected-before.json'
pins = json.loads(pins_path.read_text(encoding='utf-8-sig'))
selected = {p: v for p, v in pins.items() if p.startswith('CTP-proef/ctp_data/default/aidata/')}
assert len(selected) == 116
for p in ['CTP-proef/ctp_program/ctp/civctp.exe',
          'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll']:
    selected[p] = pins[p]
before = [{'path': p, 'sha256': sha((ROOT/p).read_bytes()), 'expected': v['sha256']}
          for p, v in selected.items()]
emit('source-before.json', before)
assert all(r['sha256'] == r['expected'] for r in before), 'Protected source differs.'
b2b_manifest = json.loads((B2B/'manifest.json').read_text(encoding='utf-8-sig'))
assert sha((B2B/'manifest.json').read_bytes()) == 'e1bacd6b0fbed849563fb167b2aae6f9b2cdf01878ddc03a3756698f97e2c5a1'
assert b2b_manifest['design_sha256'] == DESIGN
prepared, direct = {}, {}
for r in b2b_manifest['candidate_files']:
    data = (B2B/'candidate'/r['candidate']).read_bytes()
    assert len(data) == r['size'] and sha(data) == r['sha256']
    prepared[r['candidate']] = data
    direct[r['candidate']] = (B2B/'candidate'/r['candidate'], data)
assert len(prepared) == 10

candidate, backup = OUT/'candidate', OUT/'backup'
candidate.mkdir(); backup.mkdir()
for name, (path, data) in direct.items():
    (backup/name).write_bytes(data)

# Byte ranges are complete declaration-to-#END_DATA lines, including internal comments.
block_pattern = rb'(?m)^Advancement_Element Advancements_List\[MAX_ELEMENTS\];[^\r\n]*\r\n(?:(?!^#END_DATA)[\s\S])*?^#END_DATA[^\r\n]*\r\n'
source_blocks, block_records = {}, []
for profile in ['default', *ROUTES.values(), 'citywall_science']:
    relative = 'AIPs/' + profile + '.aip'
    data = (SRC/relative).read_bytes()
    hits = list(re.finditer(block_pattern, data))
    assert len(hits) == 1, profile
    block = hits[0].group()
    assert block.count(b'#DATA') == 1 and block.count(b'#END_DATA') == 1
    advances = re.findall(rb'"(ADVANCE_[A-Z0-9_]+)";', block)
    assert advances[:2] == [b'ADVANCE_RELIGION', b'ADVANCE_THEOCRACY']
    assert advances and b'...' not in block
    source_blocks[profile] = block
    (backup/'AIPs').mkdir(exist_ok=True)
    (backup/relative).write_bytes(data)
    direct[relative] = (SRC/relative, data)
    block_records.append({'source': str((SRC/relative).relative_to(ROOT)).replace('\\', '/'),
                          'source_sha256': sha(data), 'offset': hits[0].start(),
                          'length': len(block), 'block_sha256': sha(block),
                          'record_count': len(advances), 'ordered_advances': [a.decode() for a in advances]})
prepared['AIPs/opening_research.aip'] = source_blocks['default']
for profile in ['default', *ROUTES.values()]:
    prepared['AIPs/opening_restore_' + profile + '.aip'] = source_blocks[profile]
new_loader = 'load_opening_research.fli'
prepared[new_loader] = b'action load("opening_research.aip") when (opening_required > 0.5)\r\n'
loader_anchor = b'#include "aiploader.fli"\r\n'
for suffix, profile in ROUTES.items():
    name = 'beginturn' + suffix + '.fli'
    original = prepared[name]
    assert original.count(loader_anchor) == 1
    action = ('action load("opening_restore_' + profile + '.aip") when (opening_required < 0.5)\r\n').encode()
    replacement = action + loader_anchor + b'#include "load_opening_research.fli"\r\n'
    prepared[name] = original.replace(loader_anchor, replacement)
    assert prepared[name].replace(replacement, loader_anchor) == original
default_name = 'beginturn.fli'
default_anchor = b'#include "set_govern_opening.fli"\r\n'
assert prepared[default_name].count(default_anchor) == 1
default_addition = (b'action load("opening_restore_default.aip") when (opening_required < 0.5)\r\n'
                    b'#include "load_opening_research.fli"\r\n')
prepared[default_name] = prepared[default_name].replace(default_anchor, default_anchor + default_addition)
assert prepared[default_name].replace(default_anchor+default_addition, default_anchor) == direct[default_name][1]
assert len(prepared) == 19
for name, data in prepared.items():
    if name not in direct:
        assert not (SRC/name).exists(), 'Existing new target: ' + name
    assert not re.search(rb'(?<!\r)\n', data), 'CRLF required: ' + name
    target = candidate/name
    target.parent.mkdir(exist_ok=True)
    target.write_bytes(data)

# Only static textual include/action order. This is not a fuzzy or AIP parser.
include = re.compile(rb'^\s*#include\s+"([^"]+)"', re.M)
actions = re.compile(rb'^\s*action\s+load\s*\(\s*"([^"]+)"\s*\)\s+when\s*\(([^\r\n]+)\)', re.M)
def contents(name): return prepared[name] if name in prepared else (SRC/name).read_bytes()
def expand(name, stack=()):
    assert name not in stack, 'Include cycle'
    data = contents(name)
    return include.sub(lambda m: expand(m[1].decode(), stack+(name,)), data)
def reachable(name, seen=None):
    seen = set() if seen is None else seen
    if name in seen: return seen
    seen.add(name)
    for m in include.finditer(contents(name)): reachable(m[1].decode(), seen)
    return seen
routing = []
for suffix, profile in [*ROUTES.items(), ('Default', 'default'), ('Barbarians', 'barbarian')]:
    personality = 'personality' + suffix + '.fli'
    begin = 'beginturn.fli' if suffix == 'Default' else 'beginturn'+suffix+'.fli'
    reachable_files = sorted(reachable(personality))
    loads = [{'aip': m[1].decode(), 'condition': m[2].decode()} for m in actions.finditer(expand(begin))]
    if suffix == 'Barbarians':
        assert loads == [{'aip': 'barbarian.aip', 'condition': 'num_cities < 50.0'}]
        assert new_loader not in reachable_files
        assert not any(n.startswith('set_govern_') for n in reachable_files)
        assert 'set_govern.fli' in reachable_files
    else:
        assert loads[0] == {'aip': 'opening_restore_'+profile+'.aip', 'condition': 'opening_required < 0.5'}
        assert loads[-1] == {'aip': 'opening_research.aip', 'condition': 'opening_required > 0.5'}
        assert new_loader in reachable_files
        if suffix == 'Default':
            assert len(loads) == 2 and 'aiploader.fli' not in reachable_files
        else:
            old_loads = [{'aip': m[1].decode(), 'condition': m[2].decode()}
                         for m in actions.finditer(expand('aiploader.fli'))]
            assert loads[1:-1] == old_loads
            assert any(a['aip'] == 'citywall_science.aip' for a in loads[1:-1])
    routing.append({'route': suffix, 'active_include_reachability': reachable_files, 'begin_action_order': loads})

records, diffs = [], []
for name, data in prepared.items():
    previous = direct[name][1] if name in direct else b''
    mode = 'B2B_UNCHANGED' if data == previous else ('B2C_MODIFIED' if previous else 'B2C_NEW')
    records.append({'candidate': name, 'sha256': sha(data), 'size': len(data), 'mode': mode,
                    'direct_baseline': str(direct[name][0].relative_to(ROOT)).replace('\\','/') if previous else None,
                    'direct_baseline_sha256': sha(previous) if previous else None})
    if mode != 'B2B_UNCHANGED':
        diffs.extend(difflib.unified_diff(previous.decode('latin-1').splitlines(True), data.decode('latin-1').splitlines(True),
                                        fromfile='direct-b2b/'+name, tofile='candidate/'+name))
(OUT/'candidate.diff').write_bytes(''.join(diffs).encode('latin-1'))
backup_records = [{'path': name, 'source': str(path.relative_to(ROOT)).replace('\\','/'),
                   'sha256': sha(data), 'size': len(data), 'backup_matches': (backup/name).read_bytes() == data}
                  for name, (path, data) in direct.items()]
assert all(r['backup_matches'] for r in backup_records)
emit('backup-manifest.json', backup_records)
emit('category-blocks.json', block_records)
emit('routing.json', {'method': 'Static include expansion and textual action order; NOT native execution',
                       'routes': routing, 'ordinary_action_sequence_unchanged': True,
                       'barbarian_old_government_and_load_unchanged': True,
                       'default_template_remains_disabled': True})
after = [{'path': r['path'], 'sha256': sha((ROOT/r['path']).read_bytes()),
          'unchanged': sha((ROOT/r['path']).read_bytes()) == r['sha256']} for r in before]
after.extend({'path': str(path.relative_to(ROOT)).replace('\\','/'), 'sha256': sha(path.read_bytes()),
              'unchanged': path.read_bytes() == data} for path, data in direct.values() if B2B in path.parents)
emit('source-after.json', after)
assert all(r['unchanged'] for r in after)
emit('manifest.json', {'state': 'PREPARED_ONLY_NOT_INSTALLED', 'created_at': datetime.datetime.now().astimezone().isoformat(),
                       'design_sha256': DESIGN, 'direct_b2b_manifest': str((B2B/'manifest.json').relative_to(ROOT)).replace('\\','/'),
                       'direct_b2b_manifest_sha256': sha((B2B/'manifest.json').read_bytes()),
                       'existing_protected_manifest': str(pins_path.relative_to(ROOT)).replace('\\','/'),
                       'existing_protected_manifest_sha256': sha(pins_path.read_bytes()),
                       'checked_existing_sources': len(before), 'candidate_files': records,
                       'combined_candidate_count': len(records), 'b2c_changed_or_new_count': 16,
                       'byte_identical_carried_b2b_count': 3, 'direct_backup_count': len(backup_records),
                       'selected_N': None, 'workversion_changed': False, 'native_changed': False,
                       'native_parser': 'NOT_TESTED', 'native_action_pass': 'NOT_TESTED',
                       'research_selection': 'NOT_TESTED', 'real_game': 'NOT_TESTED'})
print(json.dumps({'state': 'PREPARED_ONLY_NOT_INSTALLED', 'directory': str(OUT), 'candidates': len(records),
                  'b2c_changed_or_new': 16, 'carried_b2b': 3, 'backup': len(backup_records),
                  'source_checks_after': len(after), 'routes': len(routing)}, indent=2))
