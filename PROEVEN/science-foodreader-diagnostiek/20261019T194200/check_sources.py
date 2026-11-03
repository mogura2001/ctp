"""AST/source/layout only. Never import an emitter, compose or run fixtures."""
from pathlib import Path
import ast,datetime,difflib,hashlib,importlib.util,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
PARENT=ROOT/'PROEVEN/u30-science-filter/20261017T124500'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def pin(path):return dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path),size=path.stat().st_size)
def tree(path):return ast.parse(path.read_text('utf-8'))
def function(path,name):return next(n for n in tree(path).body if isinstance(n,ast.FunctionDef) and n.name==name)
def body(path,name):return ast.dump(ast.Module(body=function(path,name).body,type_ignores=[]),include_attributes=False)
def diff(a,b,name):
 value=''.join(difflib.unified_diff(a.read_text('utf-8').splitlines(True),b.read_text('utf-8').splitlines(True),fromfile=str(a.relative_to(ROOT)),tofile=str(b.relative_to(ROOT))))
 folder=OUT/'diffs';folder.mkdir(exist_ok=True);(folder/name).write_text(value,'utf-8')
def main():
 parsed=[]
 for path in sorted(OUT.rglob('*.py')):tree(path);parsed.append(path.relative_to(OUT).as_posix())
 for path in sorted(OUT.rglob('*.py')):compile(path.read_text('utf-8'),str(path),'exec')
 spec=importlib.util.spec_from_file_location('only_food_layout',OUT/'food_diagnostic_layout.py');layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(layout)
 assert layout.validate_layout()
 factory=OUT/'food_components.py';original=ROOT/'PROEVEN/production-h3/components.py'
 default_source_equal=body(factory,'_original_reader')==body(original,'reader') and body(factory,'_original_environment_add')==body(original,'environment_add')
 assert default_source_equal
 unchanged=('native.py','policy.py','integration_base.py','input-pins.py','input-pins.json','bind_scheduler.py','union.py','science_model.py','science_layout.py','science_result.py','science_development.py','plan_layout.py','science-spatial-pins.json','preparation-manifest.json','release-v1.robotcom.backup.dll')
 for name in unchanged:assert sha(OUT/name)==sha(PARENT/name),name
 for name in ('original_core.py','h3_layout.py','positive_reader.py','participants.json'):
  assert sha(OUT/'reader'/name)==sha(PARENT/'diagnostic-reader'/name),name
 assert layout.FRAME_SIZE-80==272 and (layout.FRAME_SIZE-80)%16==0
 calls=[n for n in ast.walk(tree(OUT/'science_model.py')) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='j' and len(n.args)==2 and all(isinstance(v,ast.Constant) for v in n.args) and [v.value for v in n.args]==['call','H3FoodReader']]
 assert len(calls)==2
 diagnostic=tree(OUT/'food_diagnostic.py');ids=set()
 for n in ast.walk(diagnostic):
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute):
   if n.func.attr=='edge' and len(n.args)>1 and isinstance(n.args[1],ast.Constant):ids.add(n.args[1].value)
   if n.func.attr=='append' and isinstance(n.func.value,ast.Attribute) and n.func.value.attr=='ids' and isinstance(n.args[0],ast.Constant):ids.add(n.args[0].value)
  if isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and any(isinstance(t,ast.Name) and t.id=='branch' for t in n.target.elts):
   position=next(i for i,t in enumerate(n.target.elts) if isinstance(t,ast.Name) and t.id=='branch')
   try:ids.update(row[position] for row in ast.literal_eval(n.iter))
   except (ValueError,TypeError):pass
 assert ids==set(range(1,38)),ids
 assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='fp' for n in ast.walk(diagnostic))
 for name in ('stable_sample','decode_slot0','verify_loaded','observe_goal3','scalar_state'):
  assert body(OUT/'reader/Lees-Uitbreiding.py',name)==body(PARENT/'diagnostic-reader/Lees-Uitbreiding.py',name)
 provenance=json.loads((OUT/'INPUT-PROVENANCE.json').read_text('utf-8'))
 for row in provenance['inputs']:assert sha(ROOT/row['path'])==row['sha256'],row['path']
 for folder,name in ((PARENT,'BUILD-PINS.json'),(PARENT/'native-integration','NATIVE-PINS.json')):
  for row in json.loads((folder/name).read_text('utf-8'))['files']:assert sha(folder/row['path'])==row['sha256'],row['path']
 gate=json.loads((OUT/'ROOT-BRONREVIEW.json').read_text('utf-8'));assert not any(gate.get(k) for k in ('candidate_build_allowed','native_allowed','host_allowed','fixture_emit_allowed'))
 assert not (OUT/'U30-40.prepared.dll').exists() and not (OUT/'fixture').exists()
 diff(PARENT/'build_candidate.py',OUT/'build_candidate.py','builder.diff')
 diff(PARENT/'diagnostic-reader/Lees-Uitbreiding.py',OUT/'reader/Lees-Uitbreiding.py','reader.diff')
 diff(PARENT/'diagnostic-reader/partial_diagnostic.py',OUT/'reader/partial_diagnostic.py','bounded-reader.diff')
 diff(original,factory,'factory.diff')
 for name in ('food_diagnostic.py','food_diagnostic_layout.py','fixture_sources.py','reader/food_failure_decoder.py'):
  path=OUT/name
  (OUT/'diffs'/(path.name+'.new-source.diff')).write_text(''.join(difflib.unified_diff([],path.read_text('utf-8').splitlines(True),fromfile='/dev/null',tofile=path.relative_to(ROOT).as_posix())),'utf-8')
 paths=set(OUT.rglob('*.py'))
 paths.update(ROOT/row['path'] for row in provenance['inputs'])
 pm=json.loads((PARENT/'candidate-manifest.json').read_text('utf-8'))
 for row in pm['sources']+pm['source_dependency_pins']+pm['release_pins']:
  path=ROOT/row['path'];assert sha(path)==row['sha256'],row['path'];paths.add(path)
 paths.update((ROOT/'PROEVEN/production-h3/helper'/name) for name in ('Native.cs','shim5.bin','shim5.recipe.json','convert.bin','convert.recipe.json','food.bin','food.recipe.json'))
 sourcepins=dict(stage='SOURCE_ONLY_NO_EMISSION_NO_CANDIDATE',sources=[pin(p) for p in sorted(paths)])
 (OUT/'SOURCE-PINS.json').write_text(json.dumps(sourcepins,indent=2)+'\n','utf-8')
 result=dict(stage='AST_SOURCE_LAYOUT_CHECKED_ONLY',time_amsterdam=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).isoformat(),source_parse_count=len(parsed),parsed=parsed,default_reader_and_environment_source_bodies_equal=True,unchanged_copied_sources=list(unchanged),unchanged_shared_reader_sources=True,shared_H3_byte_preservation='NOT_EMITTED_NOT_YET_MEASURED',two_unchanged_SCI_source_calls=len(calls),declared_branch_ids=sorted(ids),emitted_branch_mapping='NOT_EMITTED_NOT_YET_MEASURED',record_offset=276,record_size=236,record_end_exclusive=512,state_size=497668,new_state_RVA='DERIVED_BY_FUTURE_COMPOSE_NOT_OLD_E1000',private_frame=352,frame_growth_multiple_of16=True,staging=[-336,-100],spills=[-340,-344],old_locals_unchanged=[-44,-16],instrumentation_fp_calls=0,parent_BUILD_pins_verified=62,parent_NATIVE_pins_verified=32,source_pins=len(sourcepins['sources']),candidate_built=False,fixtures_emitted=False,native_run=False,live_read=False,gameplay_acceptance=False,open_checks=['default factory emitted byte identity at same placement','whole shared H3 and development target preservation','two SCI-only rel32 and necessary state relocations','all37 emitted landing/guard mappings and foreign-load inventory','native ABI/flags/x87/bounds/out40 and37 injected log edges','representative original-vs-clone normal zero/positive/bonus/goodfallback and mismatch, latch/binding cases','bounded decoder own-byte negative cases after final candidate/readerdependencies pinned'])
 (OUT/'SOURCE-CHECKS.json').write_text(json.dumps(result,indent=2)+'\n','utf-8')
 print(json.dumps(dict(stage=result['stage'],parsed=len(parsed),declared_IDs=37,layout=236,pins=len(sourcepins['sources']),candidate=False,native=False)))
if __name__=='__main__':main()
