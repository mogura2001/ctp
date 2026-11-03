"""Limited duration adapter offline checks only; no main/OS/RPM/game call."""
from pathlib import Path
from types import SimpleNamespace
from zoneinfo import ZoneInfo
import ast,datetime,difflib,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OLD=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500';BASE=ROOT/'PROEVEN/doel3/20261012T122000'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def main():
 for path in HERE.glob('*.py'):ast.parse(path.read_text('utf-8'))
 old=(OLD/'reader/Lees-Uitbreiding.py').read_text('utf-8');new=(HERE/'Lees-Duur.py').read_text('utf-8')
 oldtree=ast.parse(old);newtree=ast.parse(new)
 oldfunctions={n.name:ast.dump(n) for n in oldtree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};newfunctions={n.name:ast.dump(n) for n in newtree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 assert oldfunctions.keys()==newfunctions.keys() and all(v==newfunctions[k] for k,v in oldfunctions.items() if k!='main'),'getter/decoder drift'
 (HERE/'reader.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='immutable SELECT25/reader/Lees-Uitbreiding.py',tofile='own/Lees-Duur.py')),'utf-8')
 reader=load('duration_offline_entry',HERE/'Lees-Duur.py');scope=load('duration_offline_scope',HERE/'scope.py')
 candidate=reader.trusted_binding('U30-40');baseline=reader.trusted_binding('release-v1')
 assert candidate['ai']['sha256']==scope.CANDIDATE and candidate['shared_plan_rva']==0xeb000 and candidate['shared_plan_size']==497924
 assert baseline['ai']['sha256']=='eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890' and 'shared_plan_rva' not in baseline
 gate=dict(allowed=True,variant='U30-40',pid=123,creation_filetime=134370595768758551,run_id='offline-only',candidate_sha256=scope.CANDIDATE,manifest_sha256=scope.MANIFEST,turn_min=0,turn_max=26,output_directory=str(HERE/'variant'))
 args=SimpleNamespace(variant='U30-40',pid=123,creation_filetime=gate['creation_filetime'],run_id='offline-only',turn=0,snapshot_label='offline-T0',manifest=OLD/'reader/participants.json')
 cases=[]
 for name,turn,variant,accept in [('T0',0,'U30-40',True),('T26',26,'U30-40',True),('negative',-1,'U30-40',False),('beyond',27,'U30-40',False),('releasearm',0,'release-v1',False)]:
  args.turn=turn;args.variant=variant
  try:scope.admit(args,HERE/'variant/offline-T0.json',gate);ok=True
  except ValueError:ok=False
  assert ok==accept,(name,ok);cases.append(dict(name=name,accepted=ok))
 args.variant='U30-40';args.turn=0
 args.creation_filetime+=1
 try:scope.admit(args,HERE/'variant/offline-T0.json',gate)
 except ValueError:pass
 else:raise AssertionError('wrong creation accepted')
 cases.append(dict(name='wrongcreation',accepted=False))
 saved=[]
 for t in (0,1):
  path=ROOT/'PROEVEN/selectie-pad-host/20261021/host1/variant'/('T'+str(t)+'.json');data=json.loads(path.read_text('utf-8-sig'))
  assert data['stable_twice'] and all(data['loaded_checks'].values()) and data['binding']['ai_sha256']==scope.CANDIDATE
  assert sorted(c['civ_id'] for c in data['state']['civilizations'])==list(range(2,9)) and all(c['processed_round']==t-1 for c in data['state']['civilizations']);saved.append(path)
 manifest=json.loads((BASE/'manifest.json').read_text('utf-8'));before=json.loads((ROOT/'PROEVEN/science-duur-host/20261021/host1/before.json').read_text('utf-8'))
 named={r['path'] for r in manifest['files']};assert len(named)==19 and len(manifest['protected'])==118
 protected={Path(r['path']).resolve():r for r in before['protected']}
 for row in manifest['files']:
  path=ROOT/row['path'];assert sha(path)==row['variant_sha256'] and protected[path.resolve()]['sha256']==row['variant_sha256']
 for row in manifest['protected']:
  if row['path'] not in named:assert sha(ROOT/row['path'])==row['sha256'],row['path']
 instance=None
 for t in range(27):
  path=BASE/'variant'/('T'+str(t)+'.json');data=json.loads(path.read_text('utf-8-sig'));saved.append(path)
  assert data['stable_twice'] and all(data['loaded_checks'].values()) and data['binding']['ai_sha256']==baseline['ai']['sha256'] and data['turn']==t
  civs=sorted(data['state']['civilizations'],key=lambda c:c['civ_id']);assert [c['civ_id'] for c in civs]==list(range(2,9)) and all(c['processed_round']==t-1 for c in civs)
  for c in civs:
   for field in ('city_count','active_government','government_requested','government_deadline','research_list','known'):assert field in c,field
  if instance is None:instance=data['instance']
  else:assert data['instance']==instance
  if t:
   path=BASE/'variant'/('T'+str(t)+'-pass.json');passed=json.loads(path.read_text('utf-8-sig'));saved.append(path);assert passed['turn']==t and passed['one_n'] is True and passed['native_all_round_plus_one'] is True
 assert sum(c['city_count'] for c in civs)==20 and all(c['active_government']==3 for c in civs)
 result=dict(stage='C1_SOURCE_ONLY_OFFLINE_CHECKED_NOT_LIVE',at_amsterdam=datetime.datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat(),unchanged_getter_decoder_functions=len(oldfunctions)-1,offline_candidate_release_binding=True,scope_cases=cases,saved_candidate_T0_T1=True,historical_files=19,historical_protected=118,historical_snapshots=27,historical_passes=26,historical_T26_city_counts=[c['city_count'] for c in civs],live_RPM=False,game=False,native=False,build=False)
 (HERE/'OFFLINE-CHECKS.json').write_text(json.dumps(result,indent=2)+'\n','utf-8')
 paths=set(HERE.glob('*.py'))|{HERE/'Pass-Duur.ps1',HERE/'reader.diff',HERE/'OFFLINE-CHECKS.json',HERE/'C1-OVERDRACHT.md',HERE/'POWERSHELL-PARSE.json'}|set(saved)
 paths|={ROOT/p['path'] for p in json.loads((OLD/'reader/READER-PINS.json').read_text('utf-8'))['sources']}
 paths|={OLD/'reader/READER-PINS.json',OLD/'reader/Lees-Uitbreiding.py',ROOT/'PROEVEN/Bedien-CTP.ps1',ROOT/'PROEVEN/Controleer-Weekbudget.py',ROOT/'PROEVEN/doel3/20261012-release-v1/Doel3.ps1',BASE/'manifest.json',BASE/'participants.json',BASE/'ROOT-VARIANT-TRACE.json',ROOT/'ONTWERP/SCIENCE-DUURPROEF.md'}
 pins=dict(stage=result['stage'],sources=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in sorted(paths)])
 (HERE/'SOURCE-PINS.json').write_text(json.dumps(pins,indent=2)+'\n','utf-8')
 (HERE/'ROOT-READER.json').write_text(json.dumps(dict(allowed=False,control_allowed=False,variant='U30-40',pid=None,creation_filetime=None,run_id='science-duur-20261021-host1',turn_min=0,turn_max=26,output_directory=str(HERE/'variant'),candidate_sha256=scope.CANDIDATE,manifest_sha256=scope.MANIFEST,source_pins_sha256=sha(HERE/'SOURCE-PINS.json')),indent=2)+'\n','utf-8')
 print(json.dumps(dict(stage=result['stage'],pins=len(pins['sources']),pins_sha256=sha(HERE/'SOURCE-PINS.json'),scope_cases=len(cases),getters_unchanged=result['unchanged_getter_decoder_functions'],baseline='19+118/27snapshots/26passes',live=False)))
if __name__=='__main__':main()
