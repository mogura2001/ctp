"""Finite after-native protected pins/results audit, no native calls."""
from pathlib import Path
import hashlib,json,datetime,difflib
OUT=Path(__file__).resolve().parent;PACK=OUT.parent;ROOT=PACK.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((PACK/'candidate-manifest.json').read_text('utf-8'))
assert manifest['candidate_sha256']=='f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810'
assert sha((PACK/'candidate-manifest.json').read_bytes())=='9b2146579b7ccf3a8133850c360e7b0c934565998078fa7ae140a6b10f6e5341'
assert sha((PACK/'U30-40.prepared.dll').read_bytes())==manifest['candidate_sha256']
for row in manifest['sources']+manifest['release_pins']+manifest['source_dependency_pins']:
 assert sha((ROOT/row['path']).read_bytes())==row['sha256'],row['path']
r1=json.loads((OUT/'native-policy-result.json').read_text('utf-8-sig'))
r3=json.loads((OUT/'native-policy-result-r3.json').read_text('utf-8-sig'))
p1=json.loads((OUT/'policy-process.json').read_text('utf-8'))
p2=json.loads((OUT/'policy-process-r2.json').read_text('utf-8'))
p3=json.loads((OUT/'policy-process-r3.json').read_text('utf-8'))
assert r1['pass'] and r1['native_calls']==52 and len(r1['checks'])==41
assert r3['pass'] and r3['native_calls']==1 and len(r3['checks'])==10
for process in (p1,p2,p3):assert process['terminal_confirmed'] and process['candidate_unchanged']
assert p1['exit_code']==p3['exit_code']==0 and p2['exit_code']==0xc0000005
sources=[]
for path in sorted(OUT.rglob('*')):
 if path.is_file() and path.suffix in ('.py','.cs','.ps1','.bin','.json','.fragment') and path.name!='C2-package.json':
  sources.append(dict(path=path.relative_to(ROOT).as_posix(),size=path.stat().st_size,sha256=sha(path.read_bytes())))
original=(ROOT/'PROEVEN/settler-b4/NativeProducer.cs').read_text('utf-8').splitlines(True)
own=(OUT/'NativeU40.cs').read_text('utf-8').splitlines(True)
(OUT/'NativeU40.source-diff.txt').write_text(''.join(difflib.unified_diff(original,own,fromfile='readonly existing NativeProducer.cs',tofile='owned C2 NativeU40.cs')),'utf-8')
report=dict(stage='C2_NATIVE_CHANGED_CASES_FIXTURE_ONLY_NO_GAMEPLAY',checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate_sha256=manifest['candidate_sha256'],candidate_source_and_19_release_pins_unchanged=True,successful_native_calls=53,successful_checks=51,failed_attempt=dict(pid=p2['pid'],exit_code=p2['exit_code'],terminal=True,reason='fixture Marshal.WriteInt32 into own RX vtable before extra Goto call; fixed owned VirtualProtect; no candidate change',old_outputs_preserved=True),processes=[p1,p2,p3],fixture_sources_and_artifacts=sources,scope=dict(native_original_Choose_Actual_Desired=True,new_policy_finalize_prefix_cap_adapters_executed=True,actual_Goto_Follow_arrival_normalizer_chain=True,normal_LoadLibrary=True,manual_full_owned_copy_HIGHLOW_rebase=True,forced_LoadLibrary_rebase=False,actual_engine_callbacks=False,actual_city_creation=False,full_native_Execute_aggregate=False,full_Scheduler_detach_runtime=False,whole_actual_game_host_allocator=False,gameplay=False),remaining=['Root review these actual branch results before any live activation','Execute/Scheduler result propagation and single detach have machinecode bindings, full corresponding native frames not executed','Actual host/path allocator/safety/query cost and useful request-to-city effect require separately authorized benchmark','Native LoadLibrary preferred base + manual owned full-copy rebase proven; forced OS-loader rebase not run','30/40 city creation and Doel3 retention/save-load in actual combination unmeasured'])
(OUT/'C2-package.json').write_text(json.dumps(report,indent=2)+'\n','utf-8')
print(json.dumps(dict(stage=report['stage'],calls=53,checks=51,protected_pins_unchanged=True,all_three_owned_helpers_terminal=True,failed_r2_preserved=True,package_sha256=sha((OUT/'C2-package.json').read_bytes()))))
