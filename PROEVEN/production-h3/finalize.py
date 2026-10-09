"""Package exact built/offline/native state for root; no installation."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((OUT/'H3-SCORE_CURRENT.manifest.json').read_text())
offline=json.loads((OUT/'offline-results.json').read_text())
native=json.loads((OUT/'H3-SCORE_CURRENT.native-fixture.json').read_text(encoding='utf-8-sig'))
loader=json.loads((OUT/'H3-SCORE_CURRENT.native-loader.json').read_text(encoding='utf-8-sig'))
assert offline['pass'] and native['pass'] and loader['pass']
assert offline['candidate_sha256']==native['candidate_sha256']==loader['candidate_sha256']==manifest['candidate_sha256']
assert offline['payload_sha256']==native['payload_sha256']==loader['payload_sha256']==manifest['payload_sha256']
assert native['measured_peak_extra_direct_world_calls']==43 and native['measured_peak_total_direct_world_calls']==44
baseline=json.loads((OUT/'protected-before.json').read_text());after=json.loads((OUT/'protected-after-native.json').read_text());assert baseline==after
artifacts={}
for p in sorted(OUT.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p.name!='package-manifest.json' and not p.name.endswith('.tmp'):
  artifacts[p.relative_to(OUT).as_posix()]={'size':p.stat().st_size,'sha256':sha(p.read_bytes())}
package={'scope':'Built and independent offline/own native checked; NOT INSTALLED; real engine acceptance and AI activation/performance/gameplay UNMEASURED',
 'design_sha256':manifest['design_sha256'],'original_sha256':manifest['original_sha256'],'candidate_sha256':manifest['candidate_sha256'],'payload_sha256':manifest['payload_sha256'],
 'candidate':'candidates/H3-SCORE_CURRENT/robotcom.dll','control_H1_I_sha256':offline['H1_I_constant'],'protected_files':len(after),'protected_before_after_identical':True,
 'B1_constant_proof_files':offline['B1_constant'],'fixed_T0_paths':offline['fixed_T0_paths'],'native_cases':native['native_cases'],
 'measured_extra_direct_world_calls':43,'measured_total_direct_world_calls':44,'top4_plan_comparison_upper_bound':376,
 'negative_mine_delta_valid_finalfood':native['negative_mine_delta_valid_finalfood'],'insufficient_pending_mines':native['insufficient_pending_mines'],
 'header_fixture_limit':'Original production wronghost/basis/context rejection tested; own headercopy changes only400000 baseguardliteral because400000 was occupied; no production fixture fallback',
 'representational_limit':'Development delta must be finite exact int32; negative delta supported when finalfood is nonnegative; fractional/overflow/negative finalfood UNKNOWN',
 'rollback':'No installation; preserve original backup and actual later chosen baseline, only restore that DLL in closed proof installation, unchangedB1/T0/users/saves',
 'artifacts':artifacts}
(OUT/'package-manifest.json').write_text(json.dumps(package,indent=2)+'\n')
print(json.dumps({'package_sha256':sha((OUT/'package-manifest.json').read_bytes()),'artifacts':len(artifacts),'candidate_sha256':manifest['candidate_sha256'],'native_cases':native['native_cases'],'installed':False}))
