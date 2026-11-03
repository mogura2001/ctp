"""Read-only verification of this run's saved evidence; no process access."""
from pathlib import Path
import hashlib, json
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = ROOT / 'PROEVEN/uitbreiding-lang/20261022T122400/U30-40'
read = lambda p: json.loads(p.read_text('utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
new, old, diffs, attrs, extras, local = [], [], [], Counter(), [], []
start_sha = sha(HERE / 'host/start.json')
helper_sha = sha(HERE / 'Pass-Duur.ps1')
for t in range(101):
    path = HERE / f'local4/T{t}.json'
    a, b = read(path), read(OLD / f'T{t}.json')
    assert a['stable_twice'] and all(a['loaded_checks'].values())
    assert sorted(r['civ_id'] for r in a['state']['civilizations']) == list(range(2, 9))
    assert all(r['processed_round'] == t - 1 for r in a['state']['civilizations'])
    assert a['instance']['pid'] == 18384
    assert a['instance']['creationtime_filetime'] == 134375148131610341
    assert a['variant'] == 'local4' and a['run_id'] == 'pad-local4-20261026c-host'
    assert a['turn'] == t
    assert a['binding']['ai_sha256'] == 'acfeec096ea39e1ff38435214769f4d24074e640b856e08d1c82cc09ea7a4984'
    assert a['binding']['manifest_sha256'] == '0a10a7c7f1af1ecd0d71e549296a4e31ea850f100812515d519fa4055e497d4d'
    new.append(a); old.append(b)
    ca = [r['city_count'] for r in a['state']['civilizations']]
    cb = [r['city_count'] for r in b['state']['civilizations']]
    if ca != cb: diffs.append(dict(turn=t, new=ca, old=cb))
    s = a['state']['shared_last_pass']
    d = s['path_failure_diagnostic']
    attrs[d['attribution_status']] += 1
    if d['attribution_status'] == 'LOCAL_UNKNOWN_PAIR': local.append(t)
    if isinstance(s.get('Gcert'), int) and isinstance(s.get('Dorig'), int) and s['Gcert'] > s['Dorig']:
        extras.append(dict(turn=t, civ=s['civ'], Gcert=s['Gcert'], Dorig=s['Dorig']))
    if not t: continue
    tokenpath, passpath = HERE / f'TURN-T{t}-consumed.json', HERE / f'TURN-T{t}-pass.json'
    token, passed = read(tokenpath), read(passpath)
    assert passed['success'] and passed['one_n'] and passed['native_all_round_plus_one']
    assert passed['accepted_snapshot_sha256'] == sha(path)
    assert passed['token_sha256'] == sha(tokenpath)
    assert token['start_sha256'] == passed['start_sha256'] == start_sha
    assert token['helper_sha256'] == passed['helper_sha256'] == helper_sha
    assert token['previous_snapshot_sha256'] == sha(HERE / f'local4/T{t-1}.json')
    if t > 1:
        assert passed['previous_pass_sha256'] == token['previous_completion_pass_sha256'] == sha(HERE / f'TURN-T{t-1}-pass.json')
        assert passed['previous_token_sha256'] == token['previous_completion_token_sha256'] == sha(HERE / f'TURN-T{t-1}-consumed.json')

rows = []
for cid in range(2, 9):
    get = lambda series, t: next(r for r in series[t]['state']['civilizations'] if r['civ_id'] == cid)
    first = lambda pred: next((t for t in range(101) if pred(get(new, t))), None)
    rows.append(dict(civ_id=cid, old_T100=get(old, 100)['city_count'], new_T100=get(new, 100)['city_count'],
                     first_25=first(lambda r:r['city_count'] >= 25), first_30=first(lambda r:r['city_count'] >= 30),
                     first_40=first(lambda r:r['city_count'] >= 40),
                     first_Theocracy=first(lambda r:r['active_government'] == 3),
                     Theocracy_T100=get(new, 100)['active_government'] == 3))
out = dict(verified_snapshots=101, verified_natural_steps=100, rows=rows,
           city_trajectory_differences=diffs, local_unknown_pair_turns=local,
           diagnostic_attributions=dict(attrs), last_pass_Gcert_above_Dorig=extras,
           only_last_civ_diagnostic=True, native_faultcases_tested=False,
           T100_sha256=sha(HERE / 'local4/T100.json'), start_sha256=start_sha)
(HERE / 'host/ROOT-END-REVIEW.json').write_text(json.dumps(out, indent=2), 'utf-8')
print(json.dumps(out, indent=2))
