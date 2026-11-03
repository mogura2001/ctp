"""Offline review of the two completed T0..26 traces; no game access."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

helper = sha(HERE / 'Pass-Duur.ps1')
traces = {}
for arm in ('release-v1', 'U30-40'):
    folder = HERE / arm
    start = read(folder / 'host/start.json')
    start_hash = sha(folder / 'host/start.json')
    snapshots = []
    for turn in range(27):
        path = folder / f'T{turn}.json'
        snap = read(path)
        assert snap['stable_twice'] is True
        assert snap['turn'] == turn and snap['variant'] == arm
        assert snap['run_id'] == start['run_id']
        assert snap['instance']['pid'] == start['pid']
        assert snap['instance']['creationtime_filetime'] == start['creation_filetime']
        civs = snap['state']['civilizations']
        assert sorted(row['civ_id'] for row in civs) == list(range(2, 9))
        assert all(row['processed_round'] == turn - 1 for row in civs)
        for name, value in snap['loaded_checks'].items():
            expected = arm == 'U30-40' if name == 'new_payload_and_all_nine_windows_bound' else True
            assert value is expected, (arm, turn, name)
        if turn:
            token_path = folder / f'TURN-T{turn}-consumed.json'
            pass_path = folder / f'TURN-T{turn}-pass.json'
            token, passed = read(token_path), read(pass_path)
            assert passed['success'] is True and passed['one_n'] is True
            assert passed['native_all_round_plus_one'] is True
            assert passed['immutable_turn_protocol'] is True
            for record in (token, passed):
                assert record['turn'] == turn and record['pid'] == start['pid']
                assert record['creation_filetime'] == start['creation_filetime']
                assert record['run_id'] == start['run_id']
                assert record['helper_sha256'] == helper
                assert record['start_sha256'] == start_hash
            assert passed['accepted_snapshot_sha256'] == sha(path)
            assert passed['token_sha256'] == sha(token_path)
            assert token['previous_snapshot_sha256'] == sha(folder / f'T{turn-1}.json')
            prev_pass = sha(folder / f'TURN-T{turn-1}-pass.json') if turn > 1 else None
            prev_token = sha(folder / f'TURN-T{turn-1}-consumed.json') if turn > 1 else None
            assert token['previous_completion_pass_sha256'] == passed['previous_pass_sha256'] == prev_pass
            assert token['previous_completion_token_sha256'] == passed['previous_token_sha256'] == prev_token
        snapshots.append(snap)
    traces[arm] = snapshots

for base, candidate in zip(traces['release-v1'][0]['state']['civilizations'], traces['U30-40'][0]['state']['civilizations']):
    assert {k:v for k,v in base.items() if k not in ('ai_actor','effective_aip')} == {k:v for k,v in candidate.items() if k not in ('ai_actor','effective_aip')}

rows = []
for civ_id in range(2, 9):
    row = {'civ_id': civ_id}
    for arm, snapshots in traces.items():
        history = [next(c for c in snap['state']['civilizations'] if c['civ_id'] == civ_id) for snap in snapshots]
        final = history[-1]
        row['name'] = final['civ_name']
        armies = final['current_settler_armies']
        row[arm] = {
            'cities': final['city_count'],
            'active_government': final['active_government'],
            'religion_known': final['known']['Religion']['known'],
            'theocracy_known': final['known']['Theocracy']['known'],
            'settler_armies': len(armies) if isinstance(armies, list) else armies,
            'first_active_theocracy': next((t for t,c in enumerate(history) if c['active_government'] == 3), None),
            'first_30_plus_theocracy': next((t for t,c in enumerate(history) if c['active_government'] == 3 and c['city_count'] >= 30), None),
            'native_desired': final['native_desired'],
            'native_actual': final['native_actual'],
            'native_deficit': final['native_supplemental_deficit'],
        }
    row['city_delta'] = row['U30-40']['cities'] - row['release-v1']['cities']
    rows.append(row)

before = read(HERE / 'U30-40/host/before.json')
restore = read(HERE / 'U30-40/host/restore.json')
assert all(sha(ROOT / entry['path']) == entry['sha256'] for entry in before['files'])
for archive in restore['double_archives'] + [restore['packagecopy']]:
    assert sha(ROOT / archive) == restore['autosave_sha256']
actual_saves = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'CTP-proef/ctp_program/ctp/save').rglob('*') if p.is_file()}
assert actual_saves == set(before['save_paths']) | set(restore['double_archives'])
assert not (HERE / 'U30-40/TURN-T27-consumed.json').exists()
for path in (HERE/'U30-40/ROOT-READER.json', HERE/'U30-40/ROOT-CONTROL.json', HERE.parent/'20261027-prep/U30-40/ROOT-HOST.json'):
    gate = read(path)
    assert all(gate[key] is False for key in ('allowed','control_allowed','install_allowed','start_allowed','close_allowed','restore_allowed') if key in gate)

totals = {arm: sum(row[arm]['cities'] for row in rows) for arm in traces}
result = {'at_utc': datetime.now(timezone.utc).isoformat(), 'accepted_trace_and_restore': True,
          'snapshot_count_per_arm': 27, 'verified_turns_per_arm': 26, 'common_T0_fields_equal': True,
          'totals': totals, 'delta': totals['U30-40']-totals['release-v1'],
          'percent_change': 100*(totals['U30-40']/totals['release-v1']-1), 'per_civ': rows,
          'all_before_files_exact': len(before['files']), 'save_inventory_exact': len(actual_saves),
          'candidate_T27_not_sent': True, 'T100_comparison_complete': False,
          'goal1_complete': False, 'goal1a_complete': False, 'goal5_complete': False}
out = HERE / 'ROOT-T26-COMPARISON.json'
assert not out.exists(), 'Do not overwrite a review'
out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'totals':totals, 'delta':result['delta'], 'percent_change':result['percent_change'],
                  'per_civ':[{k:v for k,v in row.items() if k not in ('release-v1','U30-40')} |
                    {arm:{key:row[arm][key] for key in ('cities','settler_armies','active_government','first_active_theocracy')} for arm in traces} for row in rows],
                  'before_files_exact':len(before['files']), 'saves_exact':len(actual_saves)}, indent=2))
