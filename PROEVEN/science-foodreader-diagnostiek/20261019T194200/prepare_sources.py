"""One source-only copy; never imports emitters or builds/executes a candidate."""
from pathlib import Path
import ast,hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
PARENT=ROOT/'PROEVEN/u30-science-filter/20261017T124500'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),size=p.stat().st_size)
def copy(source,target):
 target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():raise ValueError('Refuse replace existing own source: '+str(target))
 target.write_bytes(source.read_bytes())
def extract(path,name):
 s=path.read_text('utf-8');n=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name==name)
 return ''.join(s.splitlines(True)[n.lineno-1:n.end_lineno])+'\n'
def main():
 assert sha(PARENT/'U30-40.prepared.dll')=='0ebafb11e08bc7dca74291dd8a8e9ea94441af09602ae2d94710217f19eabad9'
 assert sha(PARENT/'candidate-manifest.json')=='9b518945a76cd0369a781de5b8f63be5fc7df963050cb04567a3fa6f6afa58ad'
 pins=[pin(PARENT/'candidate-manifest.json'),pin(PARENT/'U30-40.prepared.dll')]
 for folder,name in ((PARENT,'BUILD-PINS.json'),(PARENT/'native-integration','NATIVE-PINS.json')):
  rows=json.loads((folder/name).read_text('utf-8'))['files']
  for row in rows:assert sha(folder/row['path'])==row['sha256'],row['path']
  pins.append(pin(folder/name))
 for name in ('build_candidate.py','native.py','policy.py','integration_base.py','input-pins.py','input-pins.json','bind_scheduler.py','union.py','science_model.py','science_layout.py','science_result.py','science_development.py','plan_layout.py','science-spatial-pins.json','preparation-manifest.json','release-v1.robotcom.backup.dll'):
  copy(PARENT/name,OUT/name);pins.append(pin(PARENT/name))
 for name in ('Lees-Uitbreiding.py','original_core.py','h3_layout.py','positive_reader.py','partial_diagnostic.py','participants.json'):
  source=PARENT/'diagnostic-reader'/name;copy(source,OUT/'reader'/name);pins.append(pin(source))
 components=ROOT/'PROEVEN/production-h3/components.py'
 text='"""Own reader factory; default body is an exact parent source copy."""\nfrom x86 import mem as m\n\n'
 text+=extract(components,'reader').replace('def reader(r):','def _original_reader(r):',1)+'\n'
 text+=extract(components,'environment_add').replace('def environment_add(r,label):','def _original_environment_add(r,label):',1)+'\n'
 text+='''class FoodLabels:
 def __init__(self,r,namespace):self.r=r;self.namespace=namespace
 def __getattr__(self,name):return getattr(self.r,name)
 def name(self,label):return self.namespace+label[4:] if label.startswith('food_') else label
 def label(self,label):return self.r.label(self.name(label))
 def j(self,kind,label):return self.r.j(kind,self.name(label))

def reader(r,namespace='food',diagnostic=None):
 if diagnostic is None:
  return _original_reader(r if namespace=='food' else FoodLabels(r,namespace))
 from food_diagnostic import emit_reader
 return emit_reader(FoodLabels(r,namespace),diagnostic)

def environment_add(r,label,namespace='food',diagnostic=None):
 if diagnostic is not None:raise ValueError('diagnostic environment additions belong to emit_reader staging')
 return _original_environment_add(r if namespace=='food' else FoodLabels(r,namespace),label)
'''
 (OUT/'food_components.py').write_text(text,'utf-8');pins.append(pin(components))
 gate=dict(candidate_build_allowed=False,native_allowed=False,host_allowed=False,state='SOURCE_ONLY_AWAITING_ROOT_REVIEW')
 (OUT/'ROOT-BRONREVIEW.json').write_text(json.dumps(gate,indent=2)+'\n','utf-8')
 (OUT/'reader/runtime-pins.json').write_text(json.dumps(dict(stage='SOURCE_ONLY_NO_CANDIDATE',candidate_sha256=None,manifest_sha256=None,state_rva=None,state_size=0x79804),indent=2)+'\n','utf-8')
 (OUT/'reader/SCIENCE-FOODREADER-ROOT-VRIJGAVE.json').write_text(json.dumps(dict(allowed=False,baseline_allowed=False,candidate_sha256=None,state='SOURCE_ONLY_NO_HOST_RELEASE',sources=[]),indent=2)+'\n','utf-8')
 for p in (ROOT/'CTP-og/ctp_program/ctp/civctp.exe',ROOT/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll',ROOT/'PROEVEN/doel3/20261012-release-v1/manifest.json',ROOT/'PROEVEN/doel3/20261012-release-v1/source-pins.json'):
  pins.append(pin(p))
 (OUT/'INPUT-PROVENANCE.json').write_text(json.dumps(dict(stage='SOURCE_COPY_ONLY_NO_EMISSION',parent_BUILD_count=62,parent_NATIVE_count=32,inputs=pins),indent=2)+'\n','utf-8')
 print('Exact source copies prepared; no emitter imported or candidate built')
if __name__=='__main__':main()
