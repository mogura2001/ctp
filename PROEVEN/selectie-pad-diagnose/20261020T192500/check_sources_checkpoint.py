"""Partial C1 AST/layout/diff checkpoint only; never emitter import or build."""
from pathlib import Path
import ast,datetime,difflib,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parsed=[]
 for p in sorted(OUT.rglob('*.py')):ast.parse(p.read_text('utf-8'));compile(p.read_text('utf-8'),str(p),'exec');parsed.append(p.relative_to(OUT).as_posix())
 spec=importlib.util.spec_from_file_location('only_new_record_layout',OUT/'path_diagnostic_layout.py');layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(layout);assert layout.validate()
 provenance=json.loads((OUT/'INPUT-PROVENANCE.json').read_text('utf-8'));changed=[];unchanged=[];folder=OUT/'diffs';folder.mkdir(exist_ok=True)
 for row in provenance['inputs']:
  parent=ROOT/row['path'];own=OUT/row['own_path'];assert sha(parent)==row['sha256'],row['path']
  if sha(own)!=row['sha256']:
   changed.append(row['own_path']);(folder/(row['own_path'].replace('/','__')+'.diff')).write_text(''.join(difflib.unified_diff(parent.read_text('utf-8').splitlines(True),own.read_text('utf-8').splitlines(True),fromfile=parent.relative_to(ROOT).as_posix(),tofile=own.relative_to(ROOT).as_posix())),'utf-8')
  else:unchanged.append(row['own_path'])
 gate=json.loads((OUT/'ROOT-BRONREVIEW.json').read_text('utf-8'));assert not any(gate.get(k) for k in ['candidate_build_allowed','fixture_emit_allowed','native_allowed','host_allowed'])
 assert not (OUT/'U30-40.prepared.dll').exists() and not (OUT/'fixture').exists()
 result=dict(stage='PARTIAL_C1_NOT_READY_FOR_BUILD',time_amsterdam=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).isoformat(),parsed=parsed,changed=changed,unchanged=unchanged,record_offset=layout.RECORD_OFFSET,record_size=256,state_size=layout.STATE_SIZE,Plan_size_unchanged=layout.PLAN_SIZE,generation_offset_unchanged=layout.GENERATION_OFFSET,declared_branchIDs=layout.BRANCHES,source_only=True,candidate=False,emitter_invoked=False,native=False,remaining=['review logger/wiring actual argument/ordinal/query/latch semantics','reader ORDER phase/record decoder and stable complete read integration','builder manifest state/layout metadata and exact current proposal provenance','small logger/ABI fixture source','final source pins and complete C1 rootreview'])
 (OUT/'SOURCE-CHECKPOINT.json').write_text(json.dumps(result,indent=2)+'\n','utf-8')
 paths=set(OUT.rglob('*.py'))|{OUT/'INPUT-PROVENANCE.json',OUT/'SOURCE-CHECKPOINT.json'}
 if (OUT/'CHECKPOINT.md').exists():paths.add(OUT/'CHECKPOINT.md')
 (OUT/'CHECKPOINT-PINS.json').write_text(json.dumps(dict(stage=result['stage'],files=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in sorted(paths)]),indent=2)+'\n','utf-8')
 print(json.dumps(dict(stage=result['stage'],AST=len(parsed),changed=changed,layout=256,candidate=False,native=False)))
if __name__=='__main__':main()
