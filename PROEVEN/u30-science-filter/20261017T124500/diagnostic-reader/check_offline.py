"""Only changed diagnostic own-byte cases; no native/host/RPM operations."""
from pathlib import Path
import ast, copy, difflib, hashlib, importlib.util, json, struct, sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;PACK=HERE.parent;ROOT=PACK.parents[2]
sys.path.insert(0,str(HERE))
import partial_diagnostic as d
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def pin(path):return dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path),size=path.stat().st_size)
def function(path,name):
 s=path.read_text('utf-8');n=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name==name)
 return ast.dump(n,include_attributes=False)
preserved={name:function(HERE/'Lees-Uitbreiding.py',name)==function(PACK/'reader/Lees-Uitbreiding.py',name) for name in ('stable_sample','decode_slot0','verify_loaded','observe_goal3','scalar_state')}
preserved.update({name:sha(HERE/name)==sha(PACK/'reader'/name) for name in ('positive_reader.py','original_core.py','h3_layout.py','participants.json','runtime-pins.json')})
assert all(preserved.values()),preserved
parent_counts=[];sources=set(HERE.glob('*.py'))
for folder,file in ((PACK,'BUILD-PINS.json'),(PACK/'native-integration','NATIVE-PINS.json')):
 manifest=json.loads((folder/file).read_text('utf-8'))
 for row in manifest['files']:assert sha(folder/row['path'])==row['sha256'],row['path']
 parent_counts.append(len(manifest['files']));sources.add(folder/file)
sources.update(PACK/name for name in ('candidate-manifest.json','preparation-manifest.json','science-spatial-pins.json','plan_layout.py','science_layout.py','science_result.py','science_development.py','U30-40.prepared.dll','release-v1.robotcom.backup.dll'))
sources.update(PACK/'reader'/name for name in ('Lees-Uitbreiding.py','original_core.py','positive_reader.py','h3_layout.py','participants.json','runtime-pins.json'))
sources.update(HERE/name for name in ('participants.json','runtime-pins.json'))
sources.update((d.C1/'development.py',PACK.parents[1]/'science-u30-40/20261015T152300-c2/science_development.py'))
sources.update(PACK/'reader/candidate'/variant/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll' for variant in ('variant','baseline'))
sources.update(ROOT/'PROEVEN/doel3/20261012-release-v1'/name for name in ('source-pins.json','manifest.json','release-final.json'))
pins=dict(stage='SOURCE_OFFLINE_ONLY_NO_HOST_RELEASE',state_rva=0xe1000,state_size=d.STATE_SIZE,parent_pin_counts=parent_counts,sources=[pin(p) for p in sorted(sources)])
(HERE/'DIAGNOSTIC-PINS.json').write_text(json.dumps(pins,indent=2)+'\n','utf-8')
spec=importlib.util.spec_from_file_location('own_diagnostic_reader',HERE/'Lees-Uitbreiding.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
binding=reader.trusted_binding('U30-40')
assert binding['shared_plan_rva']==0xe1000 and binding['shared_plan_size']==497668
assert binding['ai']['sha256']=='0ebafb11e08bc7dca74291dd8a8e9ea94441af09602ae2d94710217f19eabad9'
historical=json.loads((PACK/'reader/host1/variant/T1.json').read_text('utf-8'))['state']['shared_last_pass']
real_slot=bytes.fromhex(historical['slot0_historical_reason23_diagnostic']['rawhex'])
def fixture():
 raw=bytearray(d.STATE_SIZE);shared=copy.deepcopy(historical)
 def put(off,fmt,*values):struct.pack_into(fmt,raw,off,*values)
 raw[0x40600:0x40a80]=real_slot
 put(0x78800,'<II',shared['owner'] or 0x1234,shared['generation'])
 for n in range(8):put(0x526a0+4*n,'<I',n)
 raw[0x200:0x208]=real_slot[:8]
 base=0x54800
 for off,value in ((0,2),(4,0),(8,1),(12,3),(16,3),(28,0),(32,1),(36,2),(56,0),(112,1)):put(base+off,'<i',value)
 put(base+64,'<d',1.0);put(base+72,'<q',20)
 for off,value in ((80,50),(88,40),(96,40),(104,100)):put(base+off,'<q',value)
 raw[base+116:base+124]=real_slot[8:16]
 for n in range(3):
  tile=base+128+n*96;raw[tile:tile+8]=real_slot[40+n*8:48+n*8]
  for off,value in ((16,10),(20,24),(24,1)):put(tile+off,'<i',value)
 base=0x56000
 for off,value in ((4,12),(8,1),(28,-1),(32,-1),(36,-1)):put(base+off,'<i',value)
 return raw,shared
cases=[]
def run(name,mutate=None,module_size=None,state_rva=0xe1000):
 raw,shared=fixture()
 if mutate:mutate(raw,shared)
 reads=[]
 def own(off,size):
  assert 0<=off and 1<=size<=2048 and off+size<=497668
  reads.append([off,size]);return bytes(raw[off:off+size])
 result=d.diagnose(own,shared,bytes(raw[0x40600:0x40a80]),list(range(2,9)),module_size or binding['ai']['size'],state_rva,reader.decode_slot0)
 json.dumps(result,allow_nan=False)
 cases.append(dict(name=name,attribution=result['attribution_status'],prepared=result.get('earlier_science_example',{}).get('status'),reads=reads))
 return result,reads
r,reads=run('REAL_HISTORICAL_SLOT0_PLUS_SYNTHETIC_COMPLETE_CURRENT_SCI')
assert r['earlier_science_example']['status']=='CONSISTENT_PREPARED_CONDITIONAL_SCIENCE_NOW_EXAMPLE'
assert r['original_indices_reproduced'] and not r['selected'] and not r['certified']
assert [x for x in reads if x[1]==2048]==[[0x54800,2048],[0x56000,2048]]
assert r['last_SCI_guard']['header']['coverage']==0 and r['last_SCI_guard']['header']['reason']==12
assert r['last_SCI_guard']['possible_native_coverage_guard'] and not r['last_SCI_guard']['getter_cause_proven']
def word(off,value,fmt='<i'):return lambda raw,shared:struct.pack_into(fmt,raw,off,value)
r,_=run('COVERAGE0_PRESERVES_RAW_REASON_AND_FORBIDS_CURRENT_ACCEPTANCE',word(0x54800+112,0));assert r['earlier_science_example']['status']=='INCONSISTENT_OR_INCOMPLETE'
r,_=run('INVALID_SELECTED_INDEX_PRESERVES_HEADER_AND_ALL_BOUNDED_TILES',word(0x54800+28,20));obj=next(o for o in r['objects'] if o['kind']=='ScienceResult');assert len(obj['decode']['tiles'])==3 and obj['decode']['existing_decoder_status']=='ERROR'
r,reads=run('INVALID_ORDER_HAS_NO_CAPTURE_READ',word(0x526a0+4*4,4096,'<I'));assert r['next_ORDER_guard']['status']=='INVALID_ORDER_BEFORE_NEXT_CLASSIFICATION' and [0x8200,8] not in reads
def maxslots(raw,shared):
 shared.update(slots=64,prefix_count=64,known_count=64,gate_false=shared['candidates']-64)
 for n in range(64):struct.pack_into('<I',raw,0x526a0+4*n,n)
r,reads=run('SLOTS64_HAS_NO_WORKPLACE64',maxslots);assert r['work_slot']['status']=='NOT_AVAILABLE' and not any(size==1152 for off,size in reads)
r,reads=run('INVALID_EARLIER_PREFIX_REFUSED_BEFORE_SCI_READ',word(0x40600+76,64));assert r['attribution_status']=='INSUFFICIENT_EVIDENCE' and not any(size==2048 for off,size in reads)
r,reads=run('MODULE_BOUNDARY_REFUSED_BEFORE_READ',module_size=0xe1000+0x78807);assert not reads and r['attribution_status']=='INSUFFICIENT_EVIDENCE'
r,reads=run('WRONG_STATE_RVA_REFUSED_BEFORE_READ',state_rva=0xe1001);assert not reads
r,_=run('NONFINITE_DOUBLE_RAWBITS_JSON_SAFE',word(0x54800+64,float('nan'),'<d'));assert r['earlier_science_example']['status']=='INCONSISTENT_OR_INCOMPLETE';obj=next(o for o in r['objects'] if o['kind']=='ScienceResult');assert obj['decode']['header']['actual_R']['invalid']=='NONFINITE'
r,reads=run('T0_GENERATION0_NOT_INITIALIZED',lambda raw,s:s.update(generation=0));assert r['attribution_status']=='NOT_INITIALIZED' and not reads
# Changed complete sample equality includes diagnosis; no native sample invoked.
a,_=run('DETERMINISTIC_COMPLETE_DIAGNOSIS_A');b,_=run('DETERMINISTIC_COMPLETE_DIAGNOSIS_B');assert reader.stable_sample(lambda:copy.deepcopy(a))==b
intervals=[(0x54800,2048),(0x56000,2048),(0x40f00,1152),(0x526a0,32),(0x74b00,256),(0x78800,8),(0x54800+63*2048,2048),(0x40600+63*1152,1152),(0x74800+63*256,256),(0x200+4095*8,8)]
assert all(0<=off and 1<=size<=2048 and off+size<=497668 for off,size in intervals)
delta=''.join(difflib.unified_diff((PACK/'reader/Lees-Uitbreiding.py').read_text('utf-8').splitlines(True),(HERE/'Lees-Uitbreiding.py').read_text('utf-8').splitlines(True),fromfile='immutable reader/Lees-Uitbreiding.py',tofile='diagnostic-reader/Lees-Uitbreiding.py'))
(HERE/'reader.diff').write_text(delta,'utf-8')
result=dict(scope='OFFLINE_OWN_BYTES_ONLY_NO_NATIVE_RPM_HOST',passed=True,case_count=len(cases),cases=cases,preserved=preserved,parent_pins_verified=parent_counts,exact_state_size=497668,state_rva=0xe1000,planned_intervals=intervals,binding_range_count=len(binding['ranges']),schema_import_adapter='Existing DEV_TILE literal, current/C2/C1 equality; unchanged existing science_result/scenario, no emitter imports',diagnostic_provenance=d.PROVENANCE,host_release=False,gameplay_improvement_proven=False)
(HERE/'synthetic-example.json').write_text(json.dumps(a,indent=2,allow_nan=False)+'\n','utf-8')
(HERE/'offline-checks.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n','utf-8')
print(json.dumps(dict(passed=True,cases=len(cases),parent_pins=parent_counts,source_pins=len(pins['sources']),binding=True,no_host=True)))
