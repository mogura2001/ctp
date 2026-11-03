"""Limited adapter checks from prior duration checker; no main/RPM/game/native call."""
from pathlib import Path
from types import SimpleNamespace
import ast,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OLD=ROOT/'PROEVEN/science-duurproef/20261022T114700'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def main():
 for path in HERE.glob('*.py'):ast.parse(path.read_text('utf-8'))
 before=ast.parse((OLD/'Lees-Duur.py').read_text('utf-8'));after=ast.parse((HERE/'Lees-Duur.py').read_text('utf-8'))
 previous={n.name:ast.dump(n) for n in before.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};current={n.name:ast.dump(n) for n in after.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 assert previous.keys()==current.keys() and all(v==current[k] for k,v in previous.items() if k!='main'),'getter/decoder/native helper drift'
 source=(HERE/'Lees-Duur.py').read_text('utf-8')
 assert "        if args.variant=='U30-40':\n            per_civ,shared=native_expansion_state(read,eb,ab,participants,binding)" in source
 reader=load('long_offline_entry',HERE/'Lees-Duur.py');scope=load('long_offline_scope',HERE/'scope.py')
 cases=[];saved=[];bindings={}
 for arm in ('release-v1','U30-40'):
  binding=reader.trusted_binding(arm);assert binding['ai']['sha256']==scope.ARMS[arm]
  assert ('shared_plan_rva' in binding)==(arm=='U30-40')
  bindings[arm]=dict(ai_sha256=binding['ai']['sha256'],manifest_sha256=binding['manifest_sha256'],shared_state=arm=='U30-40')
  gate=dict(allowed=True,variant=arm,pid=123,creation_filetime=134370595768758551,run_id='offline-only',ai_sha256=scope.ARMS[arm],manifest_sha256=scope.MANIFEST,turn_min=0,turn_max=100,output_directory=str(HERE/arm))
  args=SimpleNamespace(variant=arm,pid=123,creation_filetime=gate['creation_filetime'],run_id='offline-only',turn=0,snapshot_label='offline-T0',manifest=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500/reader/participants.json')
  for name,turn,change,accept in [('T0',0,{},True),('T100',100,{},True),('negative',-1,{},False),('beyond',101,{},False),('wronghash',0,{'ai_sha256':'0'*64},False),('wrongarm',0,{'variant':'release-v1' if arm=='U30-40' else 'U30-40'},False)]:
   args.turn=turn
   try:scope.admit(args,(HERE/arm/'offline-T0.json').resolve(),dict(gate,**change));ok=True
   except ValueError:ok=False
   assert ok==accept,(arm,name,ok);cases.append(dict(arm=arm,name=name,accepted=ok))
  args.turn=0
  try:scope.admit(args,(HERE/('U30-40' if arm=='release-v1' else 'release-v1')/'offline-T0.json').resolve(),gate)
  except ValueError:cases.append(dict(arm=arm,name='wrongpath',accepted=False))
  else:raise AssertionError('other arm output accepted')
  args.creation_filetime+=1
  try:scope.admit(args,(HERE/arm/'offline-T0.json').resolve(),gate)
  except ValueError:cases.append(dict(arm=arm,name='wrong100nscreation',accepted=False))
  else:raise AssertionError('other100ns accepted')
  folder=ROOT/('PROEVEN/doel3/20261012T122000/variant' if arm=='release-v1' else 'PROEVEN/science-duurproef/20261022T114700/variant')
  for t in (0,26):
   path=folder/('T'+str(t)+'.json');data=json.loads(path.read_text('utf-8-sig'));civs=data['state']['civilizations']
   assert data['stable_twice'] and all(data['loaded_checks'].values()) and data['binding']['ai_sha256']==scope.ARMS[arm]
   assert [c['civ_id'] for c in civs]==list(range(2,9)) and all(c['processed_round']==t-1 for c in civs)
   for c in civs:
    for field in ('city_count','active_government','government_requested','government_deadline','research_list','known'):assert field in c
   saved.append(dict(arm=arm,turn=t,path=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),scalar_binding=True))
 result=dict(stage='C1_SOURCE_ONLY_OFFLINE_NO_LIVE',unchanged_functions=len(previous)-1,import_without_main=True,bindings=bindings,scope_cases=cases,saved_T0_T26=saved,release_no_native_expansion_call=True,game=False,RPM=False,native=False,build=False)
 (HERE/'OFFLINE-CHECKS.json').write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps(result))
if __name__=='__main__':main()
