"""Audit saved T0..T26 and restored files; never access a live process."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PKG = ROOT / 'PROEVEN/science-duurproef/20261021T150600'
BASE = ROOT / 'PROEVEN/doel3/20261012T122000/variant'

def read(p):
    b = p.read_bytes()
    return json.loads(b.decode('utf-16' if b[:2] in (b'\xff\xfe', b'\xfe\xff') else 'utf-8-sig'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

rows = []
snaps = []
pins = {}
for t in range(27):
    file = PKG / 'variant' / f'T{t}.json'
    d = read(file)
    b = read(BASE / f'T{t}.json')
    assert d['stable_twice'] and b['stable_twice']
    assert d['loaded_checks'] and all(d['loaded_checks'].values()) and all(b['loaded_checks'].values())
    assert d['turn'] == b['turn'] == t
    assert d['binding']['ai_sha256'] == 'df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e'
    assert b['binding']['ai_sha256'] == 'eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'
    cs = sorted(d['state']['civilizations'], key=lambda c:c['civ_id'])
    bs = sorted(b['state']['civilizations'], key=lambda c:c['civ_id'])
    assert [c['civ_id'] for c in cs] == [c['civ_id'] for c in bs] == list(range(2,9))
    assert all(c['processed_round'] == t-1 for c in cs+bs)
    if snaps:
        assert d['instance'] == snaps[0]['instance']
    else:
        for old, new in zip(bs, cs):
            for k, v in old.items():
                if k not in ('ai_actor','effective_aip'):
                    assert new[k] == v, ('T0', old['civ_id'], k)
    if t:
        passed = read(PKG/'variant'/f'T{t}-pass.json')
        token = read(PKG/'variant'/f'T{t}-consumed.json')
        assert passed['turn']==t and passed['one_n'] and passed['native_all_round_plus_one']
        assert token['turn']==t and token['pid']==d['instance']['pid']
        assert token['previous_sha256']==sha(PKG/'variant'/f'T{t-1}.json')
        pins[f'T{t}-pass.json'] = sha(PKG/'variant'/f'T{t}-pass.json')
    rows.append(dict(turn=t,candidate=[c['city_count'] for c in cs],control=[c['city_count'] for c in bs],candidate_total=sum(c['city_count'] for c in cs),control_total=sum(c['city_count'] for c in bs)))
    pins[f'T{t}.json'] = sha(file)
    snaps.append(d)
before = read(HERE/'before.json')
close = read(HERE/'close.json')
restore = read(HERE/'restore.json')
assert close['close_requested'] and close['exited'] and close['all_civctp_count']==0 and close['n_consumed']==26
assert 0 < close['elapsed_seconds'] < 1500
assert restore['state']=='RESTORED' and restore['restored_hashes']==29 and restore['existing_archives_preserved']==6 and restore['alias_removed']
for r in before['protected']+before['extra_preserved_files']:
    assert sha(ROOT/r['path'])==r['sha256'] and sha(HERE/'backup'/r['path'])==r['sha256']
assert sha(HERE/'AUTOSAVE-after')==sha(ROOT/restore['autosave_archive'])==restore['autosave_after_sha256']
assert not read(HERE/'gate.json')['allowed']
assert not read(PKG/'ROOT-READER.json')['allowed'] and not read(PKG/'ROOT-READER.json')['control_allowed']
# T1's original marker denotes rejected foreground activation, not input.
# Its separate recovery is admitted only after a fresh unchanged native T0.
recheck = read(PKG/'variant/T0-focus-recheck.json')
assert recheck['instance']==snaps[0]['instance'] and recheck['stable_twice']
assert all(c['processed_round']==-1 for c in recheck['state']['civilizations'])
assert sha(PKG/'variant/T1-focus-recovery.json')==sha(PKG/'variant/T1.json')
recovery = read(HERE/'focus-recovery-T1-consumed.json')
assert recovery['before_sha256']==sha(PKG/'variant/T0-focus-recheck.json')
assert recovery['original_failed_token_sha256']==sha(PKG/'variant/T1-consumed.json')
assert 'Sent keys to probe game: n' in (HERE/'recovery-T1-n.log').read_text(encoding='utf-16')
for t in range(2,27):
    assert 'Sent keys to probe game: n' in (PKG/'variant'/f'T{t}-n.txt').read_text(encoding='utf-8-sig')
last = snaps[-1]['state']['civilizations']
theo = all(c['active_government']==3 and c['known']['Religion']['known'] and c['known']['Theocracy']['known'] for c in last)
signal = rows[-1]['candidate_total']>rows[-1]['control_total'] and all(x>=y for x,y in zip(rows[-1]['candidate'],rows[-1]['control'])) and theo
proof = dict(status='T0_T26_MEASUREMENT_COMPLETE_WITH_DOCUMENTED_INPUT_RECOVERY',snapshots=27,native_round_advances=26,successful_n_actions=26,consumption_markers=27,plain_26_token_protocol=False,recovery_token_preserved=True,rows=rows,Theocracy_retained_7of7=theo,positive_city_signal=signal,full_goal1_1a_complete=False,causal_replication_proven=False,close=close,restore=restore,files=pins,limitations=['One historical comparison; no universal/replicated causal claim.','No30/40-city or useful settler stop/resume acceptance.','First T1 activation rejected before input; separate recovery after fresh T0.','T2 paused before its token for stale budget; fresh valid measurement permitted continuation.','Autosave exact turn not independently proven.'])
(HERE/'HOST-PROOF.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status=proof['status'],last=rows[-1],Theocracy=theo,positive_city_signal=signal,proof_sha256=sha(HERE/'HOST-PROOF.json')),indent=2))
