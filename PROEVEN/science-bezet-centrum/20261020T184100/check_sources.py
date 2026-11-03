"""C1 AST/source/layout/pins only. Never import an emitter or run native."""
from pathlib import Path
import ast,datetime,difflib,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
PARENT=ROOT/'PROEVEN/science-foodreader-diagnostiek/20261019T194200'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tree=lambda p:ast.parse(p.read_text('utf-8'))
def literal(path,name):
 for n in tree(path).body:
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets):return ast.literal_eval(n.value)
 raise ValueError(name)
def body(path,name):
 return ast.dump(next(n for n in tree(path).body if isinstance(n,ast.FunctionDef) and n.name==name),include_attributes=False)
def pin(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),size=p.stat().st_size)
def main():
 parsed=[]
 for p in sorted(OUT.rglob('*.py')):tree(p);compile(p.read_text('utf-8'),str(p),'exec');parsed.append(p.relative_to(OUT).as_posix())
 spec=importlib.util.spec_from_file_location('own_layout_only',OUT/'food_diagnostic_layout.py');layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(layout)
 assert layout.validate_layout()
 assert layout.RETURN_SPILL==-348 and layout.FRAME_SIZE==352
 assert set(range(-348,-344)).isdisjoint(range(-336,-100))
 assert literal(OUT/'science_layout.py','KERNEL_FRAME_SIZE')==548
 assert literal(OUT/'science_layout.py','REASON_OCCUPIED_CENTER_SCOPE')==17
 # The original current/future sorting, signed64 margins and host query code
 # stay unchanged apart from the explicit three consumer/handler fragments.
 for name in ('ptr','bit','top3','scenarios','development_summary'):
  assert body(OUT/'science_model.py',name)==body(PARENT/'science_model.py',name),name
 changed={'build_candidate.py','food_diagnostic.py','food_diagnostic_layout.py','science_model.py','science_layout.py','science_result.py','reader/partial_diagnostic.py','reader/food_failure_decoder.py'}
 unchanged=[]
 provenance=json.loads((OUT/'INPUT-PROVENANCE.json').read_text('utf-8'))
 for row in provenance['inputs']:
  assert sha(ROOT/row['path'])==row['sha256'],row['path']
  if row['own_path'] not in changed:assert sha(OUT/row['own_path'])==row['sha256'];unchanged.append(row['own_path'])
 # Parse exact two call continuation contracts, no emitter is invoked.
 code=(OUT/'science_model.py').read_text('utf-8')
 assert code.count("r.j('call','H3FoodReader')")==2
 assert "r.alu('cmp','eax',2);r.j('je','science_center_occupied')\n r.alu('cmp','eax',1);r.j('jne','science_bad')" in code
 assert "r.alu('cmp','eax',1);r.j('jne','science_current_unknown')" in code
 handler=code[code.index("r.label('science_center_occupied')"):code.index("r.label('science_bad')")]
 assert "r.j('jmp','science_done')" in handler and 'H3FoodReader' not in handler
 # New reason has no previous ScienceResult reason assignment collision.
 assert 'REASON_OCCUPIED_CENTER_SCOPE' not in (PARENT/'science_layout.py').read_text('utf-8')
 assert "m('edi',4),17" not in (PARENT/'science_model.py').read_text('utf-8')
 diagnostic=(OUT/'food_diagnostic.py').read_text('utf-8')
 method=next(n for n in tree(OUT/'food_diagnostic.py').body if isinstance(n,ast.ClassDef)).body
 occupied=next(n for n in method if isinstance(n,ast.FunctionDef) and n.name=='occupied_return')
 assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and (n.func.attr=='fp' or (n.func.attr=='unary' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value=='call')) for n in ast.walk(occupied))
 assert 'RECORD_OFFSET' not in ast.get_source_segment(diagnostic,occupied) # no historical latch read
 assert "r.label('food_bad');r.zero(m('ebp',20),40);d.occupied_return();r.mov('eax',m('ebp',RETURN_SPILL))" in diagnostic
 assert "r.mov(m('ebp',RETURN_SPILL),2)" in diagnostic
 assert "STAGING+88),0);r.j('jle','food_occupied_done')" in diagnostic
 publish=diagnostic[diagnostic.index("r.label('food_publish');"):]
 assert publish.index('own Plan before publish')<publish.index("m('edi',36)")
 assert publish.index("r.alu('cmp','edi',m('ebp',PLAN_SPILL))")<publish.index("m('edi',36)")
 fixtures=(OUT/'fixture_sources.py').read_text('utf-8')
 assert "m('ebp',-144),0x5aa55aa5" not in fixtures and "m('ebp',-348),0x5aa55aa5" not in fixtures
 assert 'range(1,38)' not in fixtures and 'range(1,38)' not in (OUT/'native/NativeFoodCaller.cs').read_text('utf-8')
 gate=json.loads((OUT/'ROOT-BRONREVIEW.json').read_text('utf-8'))
 assert not any(gate.get(k) for k in ('candidate_build_allowed','fixture_emit_allowed','native_allowed','host_allowed'))
 assert not (OUT/'U30-40.prepared.dll').exists() and not (OUT/'candidate-manifest.json').exists() and not (OUT/'fixture').exists()
 assert sha(PARENT/'U30-40.prepared.dll')==provenance['parent_candidate_sha256']
 assert sha(PARENT/'candidate-manifest.json')==provenance['parent_manifest_sha256']
 folder=OUT/'diffs';folder.mkdir(exist_ok=True)
 for name in sorted(changed):
  a=PARENT/name;b=OUT/name
  (folder/(name.replace('/','__')+'.diff')).write_text(''.join(difflib.unified_diff(a.read_text('utf-8').splitlines(True),b.read_text('utf-8').splitlines(True),fromfile=str(a.relative_to(ROOT)),tofile=str(b.relative_to(ROOT)))),'utf-8')
 for name in ('fixture_sources.py','native/NativeFoodCaller.cs'):
  a=PARENT/name;b=OUT/name
  (folder/(name.replace('/','__')+'.diff')).write_text(''.join(difflib.unified_diff(a.read_text('utf-8').splitlines(True),b.read_text('utf-8').splitlines(True),fromfile=str(a.relative_to(ROOT)),tofile=str(b.relative_to(ROOT)))),'utf-8')
 paths=set(OUT.rglob('*.py'))|{OUT/'native/NativeFoodCaller.cs',OUT/'INPUT-PROVENANCE.json',OUT/'reader/participants.json',OUT/'preparation-manifest.json',OUT/'release-v1.robotcom.backup.dll',PARENT/'candidate-manifest.json',PARENT/'U30-40.prepared.dll'}
 paths.add(OUT/'BRONOVERDRACHT.md')
 for row in provenance['inputs']:paths.add(ROOT/row['path'])
 prep=json.loads((OUT/'preparation-manifest.json').read_text('utf-8'))
 for row in prep['release_pins']+prep['source_pins']+prep['proposals']:
  assert sha(ROOT/row['path'])==row['sha256'];paths.add(ROOT/row['path'])
 for name in ('shim5.bin','shim5.recipe.json','food.bin','food.recipe.json','convert.bin','convert.recipe.json'):paths.add(ROOT/'PROEVEN/production-h3/helper'/name)
 for p in (ROOT/'ONTWERP/SCIENCE-BEZET-CENTRUM.md',ROOT/'ANALYSE/SCIENCE-BEZET-CENTRUM.md',ROOT/'ANALYSE/REVIEW-SCIENCE-FOODREADER-DIAGNOSTIEK.md'):paths.add(p)
 (OUT/'SOURCE-PINS.json').write_text(json.dumps(dict(stage='C1_SOURCE_ONLY_NO_EMISSION',sources=[pin(p) for p in sorted(paths)]),indent=2)+'\n','utf-8')
 report=dict(stage='C1_SOURCE_AST_LAYOUT_ONLY',time_amsterdam=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).isoformat(),parsed=parsed,unchanged=unchanged,changed=sorted(changed),reason=17,private_returns=layout.PRIVATE_RETURNS,private_return_spill=-348,food_frame=352,model_frame=548,x87_range=[-144,-37],out40_range=[-184,-145],source_pins=len(paths),candidate_built=False,fixtures_emitted=False,native_compiled=False,native_run=False,live_read=False,gameplay_proven=False,open=['emitted bytes/full-diff/rel32/state-RVA','native ABI/flags/GPR/x87 and limited case results','reader own-byte negative cases with candidate bindings','actual fixed T0/n/T1 local scope and further classification'])
 (OUT/'SOURCE-CHECKS.json').write_text(json.dumps(report,indent=2)+'\n','utf-8')
 print(json.dumps(dict(stage=report['stage'],parsed=len(parsed),pins=len(paths),candidate=False,native=False)))
if __name__=='__main__':main()
