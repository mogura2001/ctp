"""C1 source/base copying only; no emitter/compose/candidate/native/host."""
from pathlib import Path
import json,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
PARENT=ROOT/'PROEVEN/science-bezet-centrum/20261020T184100'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert sha(PARENT/'U30-40.prepared.dll')=='e45313fde4d25a726fa2e8d26dec21c0142ac195ea5c0c40a9b380fd549b166f'
 assert sha(PARENT/'candidate-manifest.json')=='2077ac8a05d17f6ef7690ceb3a3a9e5555aa8d0f9a23e9e2d9db703288a5396b'
 names=['build_candidate.py','native.py','policy.py','integration_base.py','input-pins.py','input-pins.json','bind_scheduler.py','union.py','science_model.py','science_layout.py','science_result.py','science_development.py','plan_layout.py','food_components.py','food_diagnostic.py','food_diagnostic_layout.py','science-spatial-pins.json','preparation-manifest.json','release-v1.robotcom.backup.dll']
 names+=['reader/'+n for n in ['Lees-Uitbreiding.py','original_core.py','h3_layout.py','positive_reader.py','participants.json','partial_diagnostic.py','food_failure_decoder.py']]
 pins=[]
 for name in names:
  a=PARENT/name;b=OUT/name;assert not b.exists();b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(a.read_bytes());pins.append(dict(path=a.relative_to(ROOT).as_posix(),sha256=sha(a),own_path=name))
 (OUT/'INPUT-PROVENANCE.json').write_text(json.dumps(dict(parent_candidate_sha256=sha(PARENT/'U30-40.prepared.dll'),parent_manifest_sha256=sha(PARENT/'candidate-manifest.json'),inputs=pins),indent=2)+'\n','utf-8')
 (OUT/'ROOT-BRONREVIEW.json').write_text(json.dumps(dict(candidate_build_allowed=False,fixture_emit_allowed=False,native_allowed=False,host_allowed=False),indent=2)+'\n','utf-8')
 (OUT/'reader/runtime-pins.json').write_text(json.dumps(dict(candidate_sha256=None,manifest_sha256=None,state_rva=None,state_size=0x79904,stage='SOURCE_ONLY'),indent=2)+'\n','utf-8')
 (OUT/'reader/SCIENCE-FOODREADER-ROOT-VRIJGAVE.json').write_text(json.dumps(dict(allowed=False,stage='SOURCE_ONLY'),indent=2)+'\n','utf-8')
 print('Copied parent source/base only; all gates FALSE')
if __name__=='__main__':main()
