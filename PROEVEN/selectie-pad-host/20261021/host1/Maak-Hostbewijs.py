"""Validate saved proof bytes and restored files; no process/game access."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PKG = ROOT / 'PROEVEN/selectie-pad-diagnose/20261020T192500'

def read(path):
    data = path.read_bytes()
    return json.loads(data.decode('utf-16' if data[:2] in (b'\xff\xfe', b'\xfe\xff') else 'utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

t0, t1 = [read(HERE / 'variant' / name) for name in ('T0.json', 'T1.json')]
assert t0['stable_twice'] and t1['stable_twice']
assert t0['instance'] == t1['instance']
for snap, turn, native_round in ((t0, 0, -1), (t1, 1, 0)):
    assert snap['turn'] == turn and snap['variant'] == 'U30-40'
    assert all(snap['loaded_checks'].values())
    civs = snap['state']['civilizations']
    assert {c['civ_id'] for c in civs} == set(range(2, 9))
    assert all(c['processed_round'] == native_round for c in civs)
    assert sha(PKG / 'reader/host-20261021/variant' / f'T{turn}.json') == sha(HERE / 'variant' / f'T{turn}.json')
start, close, restore = [read(HERE / name) for name in ('start.json', 'close.json', 'restore.json')]
assert start['n_consumed'] == close['n_consumed'] == 1
assert read(HERE / 'n1-token.json')['consumed']
assert close['close_requested'] and close['exited'] and close['all_civctp_count'] == 0
assert 0 < close['elapsed_seconds'] < 720
assert restore['state'] == 'RESTORED' and restore['restored_hashes'] == 29
assert restore['existing_archives_preserved'] == 5 and restore['alias_removed']
assert not read(HERE / 'gate.json')['allowed']
assert not read(PKG / 'reader/SCIENCE-FOODREADER-ROOT-VRIJGAVE.json')['allowed']
assert not read(PKG / 'ROOT-BRONREVIEW.json')['native_allowed']
assert not read(PKG / 'native-v2/NATIVE-ROOT-REVIEW.json')['native_allowed']
before = read(HERE / 'before.json')
for row in before['protected'] + before['extra_preserved_files']:
    assert sha(ROOT / row['path']) == row['sha256']
    assert sha(HERE / 'backup' / row['path']) == row['sha256']
fixed = ROOT / 'CTP-proef/ctp_program/ctp/save/games/Julius/QUOTA-START-T0'
assert sha(fixed) == '8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26'
assert sha(HERE / 'AUTOSAVE-after') == sha(ROOT / restore['autosave_archive']) == restore['autosave_after_sha256']
assert sha(PKG / 'U30-40.prepared.dll') == t1['binding']['ai_sha256']
s = t1['state']['shared_last_pass']
assert (s['status'], s['reason'], s['generation'], s['civ'], s['context']) == (5, 0, 7, 8, 1)
assert (s['classified'], s['prefix_count'], s['slots'], s['Gcert'], s['path_queries'], s['path_points']) == (8, 8, 3, 1, 1, 2)
assert s['context_error'] == s['science_budget_exhausted'] == s['cutoff'] == 0
assert s['Dorig'] == s['desired'] == 5
selection = s['selected_evidence']
assert selection['status'] == 'CONSISTENT_LAST_PASS_SELECTION' and len(selection['selected']) == 1
selected = selection['selected'][0]
assert selected['role'] == 2 and selected['prefix_result_index'] == 0
science = selected['science']
assert science['location'] == 'NOW' and science['coverage'] == 1
assert [x['margin_x2'] for x in science['current_steps']] == [35, 30, 25]
diag = s['path_failure_diagnostic']
assert diag['attribution_status'] == 'UNPUBLISHED_STAGING_RECORD'
assert not diag['usable_diagnostic_evidence'] and diag['raw_fields']['valid'] == 0
proof = dict(
    status='ONE_FIXED_T0_N_T1_COMPLETE_RESTORED',
    instance=t1['instance'], candidate_sha256=t1['binding']['ai_sha256'],
    fixed_T0_sha256=sha(fixed), rounds_seven=[-1, 0], n_consumed=1,
    last_civ_pass={k:s[k] for k in ('status','reason','civ','generation','Dorig','Gcert','desired','classified','slots','path_queries','path_points')},
    selected_science=dict(slot=0, prefix=0, center=science['center'], margins_x2=[35,30,25], location='NOW'),
    diagnostic_status=diag['attribution_status'],
    failure_cause_proven=False, instrumentation_behavior_equivalence_runtime_proven=False,
    expansion_goal_complete=False, all_civs_location_certified=False,
    close=close, restore=restore,
    limitation='Outcome differs from previous parent: successful selection, no published failure; cause of difference needs scoped analysis. Dorig=desired=5, no extra settler demand or settlement proven.',
    incident='First T0 read reached output write but missing directory prevented saving; directory created, same unchanged reader repeated before sole n. No extra turn.',
    files={name:sha(HERE/name) for name in ('variant/T0.json','variant/T1.json','n1-token.json','close.json','restore.json','intro-180.png','loaded.png','T1-screen.png')},
    native_result=read(PKG/'native-v2/native-caller-result.json'))
(HERE/'HOST-PROOF.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':proof['status'],'proof_sha256':sha(HERE/'HOST-PROOF.json'),'selected_science':proof['selected_science'],'expansion_goal_complete':False},indent=2))
