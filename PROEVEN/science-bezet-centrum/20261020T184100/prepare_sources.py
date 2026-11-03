"""Copy only the reviewed source/base inputs. No emitter, candidate or host."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
PARENT=ROOT/'PROEVEN/science-foodreader-diagnostiek/20261019T194200'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 assert sha(PARENT/'U30-40.prepared.dll')=='068ff459a19125fdd08db060450110210ad992698d27b920894f4502ac4aae4f'
 assert sha(PARENT/'candidate-manifest.json')=='beebdb07abeb5bf111869e53f1c15dbb6466ece17808022276241d6ee4e28e44'
 names=['build_candidate.py','native.py','policy.py','integration_base.py','input-pins.py','input-pins.json','bind_scheduler.py','union.py','science_model.py','science_layout.py','science_result.py','science_development.py','plan_layout.py','food_components.py','food_diagnostic.py','food_diagnostic_layout.py','science-spatial-pins.json','preparation-manifest.json','release-v1.robotcom.backup.dll']
 names+=['reader/'+n for n in ['Lees-Uitbreiding.py','original_core.py','h3_layout.py','positive_reader.py','participants.json','partial_diagnostic.py','food_failure_decoder.py']]
 pins=[]
 for name in names:
  src=PARENT/name;dst=OUT/name
  assert not dst.exists(),str(dst)+' already exists'
  dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(src.read_bytes())
  pins.append(dict(path=src.relative_to(ROOT).as_posix(),sha256=sha(src),own_path=name))
 (OUT/'INPUT-PROVENANCE.json').write_text(json.dumps(dict(parent_candidate_sha256=sha(PARENT/'U30-40.prepared.dll'),parent_manifest_sha256=sha(PARENT/'candidate-manifest.json'),inputs=pins),indent=2)+'\n','utf-8')
 (OUT/'ROOT-BRONREVIEW.json').write_text(json.dumps(dict(stage='C1_SOURCE_PREPARATION_ONLY',candidate_build_allowed=False,fixture_emit_allowed=False,native_allowed=False,host_allowed=False),indent=2)+'\n','utf-8')
 (OUT/'reader/runtime-pins.json').write_text(json.dumps(dict(stage='SOURCE_ONLY_NO_CANDIDATE',candidate_sha256=None,manifest_sha256=None,state_rva=None,state_size=497668),indent=2)+'\n','utf-8')
 (OUT/'reader/SCIENCE-FOODREADER-ROOT-VRIJGAVE.json').write_text(json.dumps(dict(host_allowed=False,read_allowed=False,stage='SOURCE_ONLY'),indent=2)+'\n','utf-8')
 print('Copied reviewed source inputs only; all gates FALSE')
if __name__=='__main__':main()
