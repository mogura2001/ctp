"""Decode saved attempt8 bytes and bind finite native fixture evidence."""
from pathlib import Path
import json,hashlib,base64,datetime,sys,struct
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root))
from science_result import decode
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raw=json.loads((root/'native-attempt8.json').read_text(encoding='utf-8-sig'))
audit=json.loads((root/'native-attempt8-preparation-audit.json').read_text())
rows=[]
for row in raw['cases']:
 decoded=decode(base64.b64decode(row['raw_result_base64']))
 rows.append(dict(name=row['name'],native_ABI_pass=row['ABI_stack_regs_x87_canaries'],decoded=decoded))
pres=json.loads((root/'preservation-pins.json').read_text(encoding='utf-8-sig'))
protected=[]
for category in ('protected_files','dependencies'):
 for item in pres[category]:
  observed=sha(root.parents[2]/item['path'])
  protected.append(dict(category=category,path=item['path'],expected_sha256=item['sha256'],observed_sha256=observed,equal=observed==item['sha256']))
package=json.loads((root/'package-pins.json').read_text(encoding='utf-8-sig'))
packagecheck=[dict(path=item['path'],equal=sha(root/item['path'])==item['sha256']) for item in package['pins']]
oldchecks=[dict(path=name,equal=sha(root/name)==digest) for name,digest in audit['attempts_1_through_7_pins'].items()]
helper=(root/'native-fixtures.attempt8.exe').read_bytes();pe=struct.unpack_from('<I',helper,0x3c)[0];optional=pe+24
helper_imagebase=struct.unpack_from('<I',helper,optional+28)[0];helper_dllchars=struct.unpack_from('<H',helper,optional+70)[0]
prior=[]
for number in range(1,8):
 path=root/('native-attempt%d.json'%number)
 if path.exists():
  obj=json.loads(path.read_text(encoding='utf-8-sig'));cases=obj.get('cases',[])
  prior.append(dict(attempt=number,pass_reported=obj.get('pass'),saved_cases=len(cases),ABI_completed_cases=sum(row.get('ABI_stack_regs_x87_canaries') is True for row in cases),error=obj.get('error')))
full=bool(raw.get('pass')) and len(rows)==30 and all(row['native_ABI_pass'] for row in rows)
parity=all(row['decoded']['native_pending_parity'] in (True,None) for row in rows) if rows else None
coverage0=[row['name'] for row in rows if row['decoded']['header']['coverage']==0]
summary=dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 stage='CONTROLLED_NATIVE_FIXTURE_COMPLETED' if full else 'CONTROLLED_NATIVE_FIXTURE_FAILED',
 native_pass=full,decoder_parity_pass=parity,native_calls=len(rows),helper_pid=raw['helper_pid'],
 candidate_sha256=sha(root/'SCIENCE-C1-CREDIT-OFF.prepared.dll'),candidate_unchanged=sha(root/'SCIENCE-C1-CREDIT-OFF.prepared.dll')==audit['candidate_sha256'],
 coverage0_parity_none_cases=coverage0,preservation_checks=protected,package_checks=packagecheck,old_attempt_checks=oldchecks,
 helper_PE_imagebase_hex='0x%08x'%helper_imagebase,helper_PE_DLLCharacteristics_hex='0x%04x'%helper_dllchars,helper_PE_dynamicbase=bool(helper_dllchars&0x40),
 prior_attempts=prior,executions_this_period=1,native_calls_this_period=len(rows),native_complete_cases_this_period=len(rows) if full else 0,
 fixture_patches=raw['patches'],controlled_callbacks=True,synthetic_engine_pin_context=True,
 actual_engine_host_acceptance=False,original_engine_queries_executed=False,gameplay_measured=False,
 science_credit_enabled=False,union_enabled=False,active_plan_size=0x54800,game_writes=0,RPM_calls=0,GUI_calls=0,
 run_scope='one finite 30-case x86 run; no legacy suite; no allocation retry')
(root/'native-attempt8-decoded-results.json').write_text(json.dumps(rows,indent=2,allow_nan=True)+'\n',encoding='utf-8')
(root/'native-attempt8-final-checks.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
assert summary['candidate_unchanged'] and all(item['equal'] for item in protected+packagecheck+oldchecks)
if raw.get('pass'):assert full and parity
print(json.dumps({k:summary[k] for k in ('stage','native_pass','decoder_parity_pass','native_calls','helper_pid','candidate_unchanged','coverage0_parity_none_cases')},indent=2))
names=set()
for pattern in ('native-attempt8*','*.before-attempt8','*.attempt8.diff.txt'):
 names.update(p.name for p in root.glob(pattern) if p.is_file())
names.update(('native-fixtures.cs','native-main.cs','native-fixtures.attempt8.exe','prepare_native_fixtures.py','audit_attempt8.py','finalize_attempt8.py','native-fixture-input-pins.json','native-input.json','fixture-shim5-fixups.json','NATIVE-C1-OVERDRACHT.md','science_model.py','science_result.py','SCIENCE-C1-CREDIT-OFF.prepared.dll','science.payload.bin'))
names.update(p.name for p in root.glob('fixture-*.bin'))
names.discard('native-attempt8-package.json')
manifest=dict(stage=summary['stage'],native_pass=full,gameplay_measured=False,helper_running=False,pins=[dict(path=name,sha256=sha(root/name),size=(root/name).stat().st_size) for name in sorted(names) if (root/name).exists()])
(root/'native-attempt8-package.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
