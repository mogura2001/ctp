"""C1 AST/layout/source-pin checks ONLY. No production module import/emission."""
from pathlib import Path
from zoneinfo import ZoneInfo
import ast,datetime,difflib,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 parsed=[]
 for path in sorted(OUT.rglob('*.py')):
  ast.parse(path.read_text('utf-8'));compile(path.read_text('utf-8'),str(path),'exec');parsed.append(path.relative_to(OUT).as_posix())
 # The only executed project module is the side-effect-free integer layout.
 spec=importlib.util.spec_from_file_location('SELECT25_integer_layout_only',OUT/'path_diagnostic_layout.py');layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(layout)
 assert layout.validate() and (layout.PLAN_SIZE,layout.GENERATION_OFFSET,layout.RECORD_OFFSET,layout.STATE_SIZE)==(0x79800,0x79800,0x79804,0x79904)
 assert all(layout.required_mask(edge)&(7<<17)==7<<17 for edge in range(1,17))
 provenance=json.loads((OUT/'INPUT-PROVENANCE.json').read_text('utf-8'));changed=[];unchanged=[]
 folder=OUT/'diffs';folder.mkdir(exist_ok=True)
 for row in provenance['inputs']:
  parent=ROOT/row['path'];own=OUT/row['own_path'];assert sha(parent)==row['sha256'],row['path']
  if sha(own)==row['sha256']:unchanged.append(row['own_path']);continue
  changed.append(row['own_path'])
  (folder/(row['own_path'].replace('/','__')+'.diff')).write_text(''.join(difflib.unified_diff(parent.read_text('utf-8').splitlines(True),own.read_text('utf-8').splitlines(True),fromfile=parent.relative_to(ROOT).as_posix(),tofile=own.relative_to(ROOT).as_posix())),'utf-8')
 parent=ROOT/'PROEVEN/science-bezet-centrum/20261020T184100'
 for filename,key in [('U30-40.prepared.dll','parent_candidate_sha256'),('candidate-manifest.json','parent_manifest_sha256')]:assert sha(parent/filename)==provenance[key]
 native=(OUT/'native.py').read_text('utf-8');old=(parent/'native.py').read_text('utf-8')
 def segment(text,start,end):return text[text.index(start):text.index(end,text.index(start))]
 arguments_start=" r.push(1);r.push(0);r.push(1);r.lea('eax',m('ebp',-32))"
 arguments_end="r.mov(m('ebp',-36),'eax')"
 assert segment(native,arguments_start,arguments_end)==segment(old,arguments_start,arguments_end),'twenty native arguments/call'
 assert segment(native,"r.label('path_free')","r.label('path_done')")==segment(old,"r.label('path_free')","r.label('path_done')"),'nonnull free exactly once original route'
 assert "r.mov('ecx',m('edx',0x6d0b94));d.capture([('postcontext','ecx')],['postcontext']);r.alu('cmp','ecx',0);r.pop('ecx');d.edge('jne',1)" in native,'single existing postcontext read'
 assert "for off,point in ((0,12),(-8,16))" in native and 'base=9 if first else 13' in native
 for edge in range(1,9):assert 'd.edge('+repr('jne' if edge in (1,2,3,4) else 'jz' if edge==5 else 'jl' if edge==6 else 'jg' if edge==7 else 'jb')+','+str(edge)+')' in native
 for name in ('science_model.py','science_layout.py','science_result.py','science_development.py','union.py','food_components.py','food_diagnostic.py','reader/positive_reader.py'):
  assert name in unchanged,'unrelated source drift '+name
 for filename in ('plan_layout.py','food_diagnostic_layout.py'):
  tree=ast.parse((OUT/filename).read_text('utf-8'));values={node.targets[0].id:ast.literal_eval(node.value) for node in tree.body if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id=='STATE_SIZE'};assert values['STATE_SIZE']==layout.STATE_SIZE
 gate=json.loads((OUT/'ROOT-BRONREVIEW.json').read_text('utf-8'));assert not any(gate.values())
 live=json.loads((OUT/'reader/SCIENCE-FOODREADER-ROOT-VRIJGAVE.json').read_text('utf-8'));assert live['allowed'] is False
 runtime=json.loads((OUT/'reader/runtime-pins.json').read_text('utf-8'));assert runtime['state_size']==layout.STATE_SIZE and runtime['state_rva'] is None and runtime['candidate_sha256'] is None
 assert not (OUT/'U30-40.prepared.dll').exists() and not (OUT/'fixture').exists()
 assert not any(OUT.rglob('*.exe')) and not (OUT/'native/NativePathLoggerCaller.dll').exists()
 result=dict(stage='C1_SOURCE_COMPLETE_PENDING_ROOT_REVIEW_NO_BUILD_RELEASE',time_amsterdam=datetime.datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat(),AST_files=parsed,AST_count=len(parsed),changed_parent_sources=changed,unchanged_parent_sources=unchanged,layout=dict(Plan_size=layout.PLAN_SIZE,generation_offset=layout.GENERATION_OFFSET,record_offset=layout.RECORD_OFFSET,record_size=256,state_size=layout.STATE_SIZE,reserved='216..255 zero'),branches=layout.BRANCHES,native_twenty_arguments_and_free_route_source_identical=True,postcontext_existing_read_once=True,source_only=True,emitter_imported=False,compose=False,candidate=False,fixture_emitted=False,native_compiled_or_run=False,RPM=False,game=False,remaining=['independent complete root C1 review','separate C2 deterministic emission/byte/PE/callsite checks','separate limited logger native gate','separate one fixed T0/n/T1 host gate'],gameplay_goals_completed=0)
 (OUT/'SOURCE-REVIEW.json').write_text(json.dumps(result,indent=2)+'\n','utf-8')
 paths=set(OUT.rglob('*.py'))|set(OUT.rglob('*.cs'))|set(folder.glob('*.diff'))
 paths|={OUT/name for name in ['INPUT-PROVENANCE.json','preparation-manifest.json','input-pins.json','science-spatial-pins.json','release-v1.robotcom.backup.dll','SOURCE-REVIEW.json','BRONOVERDRACHT.md']}
 paths|={ROOT/name for name in ['ONTWERP/SCIENCE-SELECTIE-25-DIAGNOSE.md','ANALYSE/SCIENCE-SELECTIE-25.md','PROEVEN/production-h3/helper/shim5.bin','PROEVEN/production-h3/helper/shim5.recipe.json']}
 paths|={ROOT/row['path'] for row in json.loads((OUT/'preparation-manifest.json').read_text('utf-8'))['source_pins']}
 paths|={ROOT/row['path'] for row in provenance['inputs']}
 paths|={parent/'U30-40.prepared.dll',parent/'candidate-manifest.json'}
 pins=dict(stage=result['stage'],sources=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),size=p.stat().st_size) for p in sorted(paths)])
 (OUT/'SOURCE-PINS.json').write_text(json.dumps(pins,indent=2)+'\n','utf-8')
 print(json.dumps(dict(stage=result['stage'],AST=len(parsed),pins=len(pins['sources']),changed=changed,layout=256,emitter=False,native=False)))
if __name__=='__main__':main()
