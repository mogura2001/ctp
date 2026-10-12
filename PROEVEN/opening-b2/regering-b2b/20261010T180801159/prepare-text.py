from pathlib import Path
import datetime, difflib, hashlib, json, re, shutil

ROOT = Path(r'C:\GIT\ctp')
OUT = Path(__file__).resolve().parent
SRC = ROOT / 'CTP-proef/ctp_data/default/aidata'
DESIGN = 'ea5140b5505c11f457bdcdc3cf41fcc023e277bf247866228ad356919c9ef40e'
def sha(data): return hashlib.sha256(data).hexdigest()
def emit(name, value): (OUT / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

assert sha((ROOT/'ONTWERP/GEZAMENLIJKE-OPENING-B2.md').read_bytes()) == DESIGN
pins = json.loads((ROOT/'PROEVEN/opening-b2/protected-before.json').read_text(encoding='utf-8-sig'))
baseline = {k:v for k,v in pins.items() if k.startswith('CTP-proef/ctp_data/default/aidata/')}
assert len(baseline) == 116
before = []
for path, pin in baseline.items():
    data = (ROOT/path).read_bytes()
    before.append({'path':path, 'sha256':sha(data), 'expected':pin['sha256'], 'match':sha(data)==pin['sha256']})
emit('baseline-before.json', before)
assert all(r['match'] for r in before), 'Accepted aidata baseline changed; no candidate generation.'
backup, candidate = OUT/'backup', OUT/'candidate'
backup.mkdir(); candidate.mkdir()
for path in baseline:
    relative = (ROOT/path).relative_to(SRC)
    destination = backup/relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT/path, destination)

routes = ['beginturnCleric.fli','beginturnSlaver.fli','beginturnSciFew.fli',
          'beginturnSciMany.fli','beginturnWarFew.fli','beginturnWarMany.fli']
prepared = {}
inputs = (SRC/'inputs.fli').read_bytes()
assert b'opening_completed' not in inputs and b'opening_required' not in inputs
assert inputs.startswith(b'// inputs.fli\r\n\r\n')
prepared['inputs.fli'] = inputs[:len(b'// inputs.fli\r\n\r\n')] + (
    b'input opening_completed\r\ninput opening_required\r\n'
    b'\ttri yes_opening_required(opening_required, 1.0, 0.5)\r\n'
    b'\ttri no_opening_required(opening_required, 0.0, 0.5)\r\n\r\n'
) + inputs[len(b'// inputs.fli\r\n\r\n'):]
prepared['set_govern_opening.fli'] = (
    b'if (yes_opening_required)\r\n{\r\n\tgov_theocracy_1\r\n\tgov_tyranny_2\r\n}\r\n')
original = (SRC/'set_govern.fli').read_bytes()
conditions = list(re.finditer(rb'\bif\s*\(([^()]*)\)', original))
assert len(conditions) == 12
guarded, count = re.subn(rb'(\bif\s*)\(([^()]*)\)',
                       lambda m:m[1]+b'(('+m[2]+b') and no_opening_required)', original)
assert count == 12
prepared['set_govern_after_opening.fli'] = guarded
old = b'#include "set_govern.fli"'
replacement = b'#include "set_govern_opening.fli"\r\n#include "set_govern_after_opening.fli"'
for name in routes:
    data = (SRC/name).read_bytes()
    assert data.count(old) == 1
    prepared[name] = data.replace(old, replacement)
default = (SRC/'beginturn.fli').read_bytes()
anchor = b'#include "outputs.fli"\r\n'
assert default.count(anchor) == 1
prepared['beginturn.fli'] = default.replace(anchor, anchor+b'#include "set_govern_opening.fli"\r\n')
for name, data in prepared.items():
    if name.startswith('set_govern_'): assert not (SRC/name).exists(), 'Existing new include: no overwrite.'
    assert not re.search(rb'(?<!\r)\n', data), 'Preserve CRLF.'
    (candidate/name).write_bytes(data)

# Textual include reachability only; this is not a native FLI parser.
def includes(name):
    data = prepared.get(name, (SRC/name).read_bytes() if (SRC/name).exists() else None)
    assert data is not None, 'Missing include '+name
    return re.findall(r'^\s*#include\s+"([^"]+)"', data.decode('latin-1'), flags=re.M)
def reachable(name, seen=None):
    if seen is None: seen=set()
    if name in seen: return seen
    seen.add(name)
    for child in includes(name): reachable(child, seen)
    return seen
reach = {}
for suffix in ['Cleric','Slaver','SciFew','SciMany','WarFew','WarMany','Barbarians']:
    reach[suffix] = sorted(reachable('personality'+suffix+'.fli'))
reach['Default'] = sorted(reachable('personalityDefault.fli'))
assert all('set_govern_opening.fli' in reach[s] and 'set_govern_after_opening.fli' in reach[s] and 'set_govern.fli' not in reach[s] for s in ['Cleric','Slaver','SciFew','SciMany','WarFew','WarMany'])
assert 'set_govern_opening.fli' in reach['Default'] and 'set_govern_after_opening.fli' not in reach['Default']
assert 'set_govern.fli' in reach['Barbarians'] and not any(n.startswith('set_govern_') for n in reach['Barbarians'])
assert b'action load("barbarian.aip") when (num_cities < 50.0)' in (SRC/'beginturnBarbarians.fli').read_bytes()
assert guarded.count(b'and no_opening_required') == 12
restored = re.sub(rb'(\bif\s*)\(\(([^()]*)\) and no_opening_required\)', lambda m:m[1]+b'('+m[2]+b')', guarded)
assert restored == original, 'Every original condition/consequent/comment retained.'

diff, byte_changes, records = [], [], []
for name, data in prepared.items():
    source_name = 'set_govern.fli' if name == 'set_govern_after_opening.fli' else name
    previous = (SRC/source_name).read_bytes() if (SRC/source_name).exists() else b''
    diff.extend(difflib.unified_diff(previous.decode('latin-1').splitlines(True), data.decode('latin-1').splitlines(True), fromfile='baseline/'+source_name, tofile='candidate/'+name))
    for tag,a,b,c,d in difflib.SequenceMatcher(None, previous, data, autojunk=False).get_opcodes():
        if tag!='equal': byte_changes.append({'file':name,'baseline_file':source_name,'operation':tag,'old_offset':a,'old_length':b-a,'new_offset':c,'new_length':d-c,'old_hex':previous[a:b].hex(),'new_hex':data[c:d].hex()})
    records.append({'candidate':name,'sha256':sha(data),'size':len(data),'baseline_source':source_name if previous else None,'baseline_sha256':sha(previous) if previous else None,'encoding':'Original byte text; CRLF; inserted bytes ASCII'})
(OUT/'candidate.diff').write_bytes(''.join(diff).encode('latin-1'))
emit('byte-diff.json', byte_changes)
emit('routing.json', {'method':'Static active #include reachability, no FLI parse/native execution','personality_expansions':reach,'all_twelve_original_guards_retained':True,'barbarian_old_government_and_load_unchanged':True,'default_template_comments_preserved':True,'b2c_actions_or_overlays_added':False})
after = [{'path':r['path'],'sha256':sha((ROOT/r['path']).read_bytes()),'unchanged':sha((ROOT/r['path']).read_bytes())==r['sha256']} for r in before]
emit('baseline-after.json', after)
assert all(r['unchanged'] for r in after)
emit('manifest.json', {'state':'PREPARED_OFFLINE_TEXT_ONLY_NOT_INSTALLED','created_at':datetime.datetime.now().astimezone().isoformat(),'design_sha256':DESIGN,'baseline_manifest':'PROEVEN/opening-b2/protected-before.json','baseline_manifest_sha256':sha((ROOT/'PROEVEN/opening-b2/protected-before.json').read_bytes()),'baseline_file_count':len(baseline),'candidate_files':records,'selected_N':None,'native_changed':False,'workversion_changed':False,'parser_acceptance':'NOT_TESTED','native_effective_ranks':'NOT_TESTED','real_game':'NOT_TESTED'})
print(json.dumps({'state':'PREPARED','candidate_count':len(records),'guard_count':12,'unchanged_baseline_count':len(after),'directory':str(OUT)},indent=2))
