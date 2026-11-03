"""Audit saved own snapshots and restore records; no process or game access."""
from pathlib import Path
import hashlib,json,datetime
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def read(p):
    b=p.read_bytes()
    return b.decode('utf-16' if b[:2] in (b'\xff\xfe',b'\xfe\xff') else 'utf-8-sig')
def js(p):return json.loads(read(p))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pkg=ROOT/'PROEVEN/science-bezet-centrum/20261020T184100'
previous=ROOT/'PROEVEN/science-foodreader-host/20261019/host1/HOST-PROOF.json'
old=js(previous); a=js(HERE/'variant/T0.json');b=js(HERE/'variant/T1.json')
assert a['instance']==b['instance'] and a['binding']==b['binding']
assert a['stable_twice'] and b['stable_twice']
assert all(a['loaded_checks'].values()) and all(b['loaded_checks'].values())
assert sorted(r['civ_id'] for r in a['state']['civilizations'])==list(range(2,9))
assert sorted(r['civ_id'] for r in b['state']['civilizations'])==list(range(2,9))
assert all(r['processed_round']==-1 for r in a['state']['civilizations'])
assert all(r['processed_round']==0 for r in b['state']['civilizations'])
start=js(HERE/'start.json');close=js(HERE/'close.json');restore=js(HERE/'restore.json')
assert start['n_consumed']==1 and close['n_consumed']==1 and js(HERE/'n1-token.json')['consumed']
assert close['exited'] and close['all_civctp_count']==0 and close['elapsed_seconds']<600
assert restore['state']=='RESTORED' and restore['restored_hashes']==29 and restore['existing_archives_preserved']==4 and restore['alias_removed']
assert not js(HERE/'gate.json')['allowed']
assert not js(pkg/'reader/SCIENCE-FOODREADER-ROOT-VRIJGAVE.json')['allowed']
s=b['state']['shared_last_pass'];q=s['unselected_partial_pass_diagnostic']
scope=[r for r in q['scope_excluded_centers'] if r['prefix_index']==3]
assert len(scope)==1 and scope[0]['consistent'] and scope[0]['reason']==17
assert scope[0]['food'] is None and scope[0]['margins'] is None
assert s['classified']==s['prefix_count']==s['SCI_calls']==8 and not s['context_error'] and not s['science_budget_exhausted']
earlier=q['earlier_science_example']
assert earlier['keys']==old['earlier_science_example']['keys']
assert [r['margin_x2_i64'] for r in earlier['current_scenario']['steps']]==[35,30,25]
native=js(pkg/'native-v2/native-caller-result.json')
assert native['calls']==43 and native['validator_return2_observed']==2 and native['validator_return0_observed']==30 and native['own_image_all_windows_restored']
before=js(HERE/'before.json')
for r in before['protected']+before['extra_preserved_files']:
    assert sha(ROOT/r['path'])==r['sha256'],r['path']
archive=ROOT/restore['autosave_archive']
assert sha(archive)==sha(HERE/'AUTOSAVE-after')==restore['autosave_after_sha256']
def snapshot(d,p):
    return dict(sha256=sha(p),stable_twice=d['stable_twice'],processed_rounds=[r['processed_round'] for r in d['state']['civilizations']],cities=[r['city_count'] for r in d['state']['civilizations']],all_loaded_checks=all(d['loaded_checks'].values()))
fields=['reason','civ','generation','context','Dorig','Gcert','desired','slots','classified','prefix_count','known_count','SCI_calls','SCI_tiles','SCI_primary_food','context_error','science_budget_exhausted']
proof=dict(stage='LOCAL_OCCUPIED_CENTER_FIX_PROVEN_NEXT_SELECTION_GUARD25_OPEN_RESTORED',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),instance=b['instance'],bindings=b['binding'],snapshots=dict(T0=snapshot(a,HERE/'variant/T0.json'),T1=snapshot(b,HERE/'variant/T1.json')),visible_menu_by_seconds=js(HERE/'intro-180.json')['actual_end_seconds'],visible_save='000-U30-40-START-T0, byte-equal QUOTA-START-T0',T0_sha256='8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26',n_consumed=1,shared_last_pass={k:s[k] for k in fields},comparison=dict(previous_proof_sha256=sha(previous),previous_classified=4,current_classified=8,previous_reason=23,current_reason=25,previous_slots=2,current_slots=3,local_occupied_center_scope_fix_proven=True,all_eight_prefix_centers_classified=True),occupied_scope=scope[0],earlier_science_example=earlier,native=dict(calls=43,validator_return2=2,validator_return0=30,own_RX_restored=True,scope='OWN_FIXTURE_ONLY'),normal_exit=close,restore=restore,limits=dict(gameplay_goal_completed=False,extra_settler_demand_proven=False,selected_certificate_proven=False,unit_owner_type_proven=False,occupied_center_food_measured=False,save_identity_proven=False,atomic_snapshot_proven=False,autosave_exact_turn_proven=False,only_last_bound_civ_pass_telemetry=True),operational_corrections=['Gate preparation read UTF16 process record with wrong encoding before any mutation; corrected encoding','First T0 reader gate expected release DLL after candidate installation; refused before OpenProcess; exact candidate pin substituted and same reader reused; no n before accepted T0'],pc_left_on=True)
(HERE/'HOST-PROOF.json').write_text(json.dumps(proof,indent=2)+'\n','utf-8')
print(json.dumps(dict(stage=proof['stage'],sha256=sha(HERE/'HOST-PROOF.json'),T1=proof['snapshots']['T1']['sha256'],classified=s['classified'],reason=s['reason'],restored=29)))
