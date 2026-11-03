"""Finite source/import/disk-binding checks; no reader main, RPM or gameplay."""
from pathlib import Path
from types import SimpleNamespace
import ast,copy,difflib,hashlib,importlib.util,json,struct,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
OLD=ROOT/'PROEVEN/uitbreiding-lang/20261022T122400'
LEGACY=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500'
C1=ROOT/'PROEVEN/pad-lokaal-onbekend/20261022T180000'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n','utf-8')
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def main():
 for p in HERE.glob('*.py'):compile(p.read_text('utf-8'),str(p),'exec')
 reader=load('host_reader_offline',HERE/'Lees-Duur.py');scope=load('host_scope_offline',HERE/'scope.py')
 assert Path(reader.decode_path.__code__.co_filename).resolve()==C1/'reader/path_failure_decoder.py'
 assert Path(sys.modules['path_diagnostic_layout'].__file__).resolve()==C1/'path_diagnostic_layout.py'
 # All actually imported project/vendor Python files, plus exact disk inputs.
 paths={Path(m.__file__).resolve() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and Path(m.__file__).is_file() and Path(m.__file__).resolve().is_relative_to(ROOT)}
 paths.update(HERE.glob('*.py'));paths.update(HERE.glob('*.ps1'));paths.update(HERE.glob('*.md'))
 runtime=json.loads((HERE/'runtime-pins.json').read_text('utf-8'))
 paths.update([HERE/'runtime-pins.json',ROOT/runtime['candidate_path'],ROOT/runtime['manifest_path'],LEGACY/'science-spatial-pins.json',ROOT/'CTP-og/ctp_program/ctp/civctp.exe',ROOT/'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll',LEGACY/'reader/participants.json',ROOT/'PROEVEN/Bedien-CTP.ps1',ROOT/'PROEVEN/Controleer-Weekbudget.py',ROOT/'ONTWERP/PAD-SPELPROEF-2026-10-23.md'])
 # pefile/capstone are used by original_core.trusted_binding: import without native/game calls.
 sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
 import pefile,capstone
 paths.update(Path(m.__file__).resolve() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and Path(m.__file__).is_file() and Path(m.__file__).resolve().is_relative_to(ROOT))
 rows=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in sorted(paths)]
 save('SOURCE-PINS.json',dict(stage='C4_SOURCE_ONLY_NO_RUNTIME',sources=rows))
 binding=reader.trusted_binding('local4')
 assert binding['shared_plan_rva']==0xef000 and binding['shared_plan_size']==497924
 assert binding['ai']['sha256']==runtime['candidate_sha256'] and binding['manifest_sha256']==runtime['manifest_sha256']
 # Scalar, selected, food, nativeDesired/Actual functions/classes remain AST-equal;
 # only the existing arm predicate changes in native_expansion_state.
 before=ast.parse((OLD/'Lees-Duur.py').read_text('utf-8'));after=ast.parse((HERE/'Lees-Duur.py').read_text('utf-8'))
 def funcs(tree):return {n.name:ast.dump(n) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 b,a=funcs(before),funcs(after)
 changed=[]
 for name in a:
  if name in ('main','verify_loaded','native_expansion_state'):continue
  assert a[name]==b[name],name
  changed.append(name)
 oldnative=next(n for n in before.body if isinstance(n,ast.FunctionDef) and n.name=='native_expansion_state')
 for n in ast.walk(oldnative):
  if isinstance(n,ast.Constant) and n.value=='U30-40':n.value='local4'
 assert ast.dump(oldnative)==a['native_expansion_state']
 gate=dict(allowed=True,variant='local4',pid=123,creation_filetime=123456789,run_id='offline-only',ai_sha256=scope.CANDIDATE,manifest_sha256=scope.MANIFEST,turn_min=0,turn_max=100,output_directory=str(HERE/'local4'))
 args=SimpleNamespace(variant='local4',pid=123,creation_filetime=123456789,run_id='offline-only',turn=0,snapshot_label='offline',manifest=LEGACY/'reader/participants.json')
 cases=[]
 for label,turn,delta,ag,output,expected in [('T0',0,{}, {},HERE/'local4/offline.json',True),('T100',100,{}, {},HERE/'local4/offline.json',True),('negative',-1,{}, {},HERE/'local4/offline.json',False),('101',101,{}, {},HERE/'local4/offline.json',False),('wronghash',0,{'ai_sha256':'0'*64},{},HERE/'local4/offline.json',False),('wrongmanifest',0,{'manifest_sha256':'0'*64},{},HERE/'local4/offline.json',False),('wrongarm',0,{}, {'variant':'U30-40'},HERE/'local4/offline.json',False),('wrongPID',0,{}, {'pid':124},HERE/'local4/offline.json',False),('wrongcreation',0,{}, {'creation_filetime':123456790},HERE/'local4/offline.json',False),('wrongrun',0,{}, {'run_id':'other'},HERE/'local4/offline.json',False),('wrongoutput',0,{}, {},HERE/'offline.json',False),('closed',0,{'allowed':False},{},HERE/'local4/offline.json',False)]:
  test=copy.copy(args);test.turn=turn
  for k,v in ag.items():setattr(test,k,v)
  try:scope.admit(test,output.resolve(),dict(gate,**delta));ok=True
  except ValueError:ok=False
  assert ok==expected,label
  cases.append(dict(case=label,accepted=ok))
 # Historical reference frozen separately; never relabel or rewrite old files.
 reference=[]
 for t in range(101):
  p=OLD/'U30-40'/f'T{t}.json';d=json.loads(p.read_text('utf-8-sig'))
  assert d['stable_twice'] and d['binding']['ai_sha256']=='df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e'
  civs=sorted(d['state']['civilizations'],key=lambda c:c['civ_id'])
  assert [c['civ_id'] for c in civs]==list(range(2,9)) and all(c['processed_round']==t-1 for c in civs)
  reference.append(dict(turn=t,path=p.relative_to(ROOT).as_posix(),sha256=sha(p),cities=[c['city_count'] for c in civs]))
 save('REFERENCE-PINS.json',dict(arm='historical-df3',unchanged_T0_T100=reference,old_decoder_sha256=sha(LEGACY/'reader/path_failure_decoder.py')))
 # Replay saved raw diagnostic bytes through the pinned old and C1 decoders.
 # Only the already stored binding fields are rebuilt into tiny own-byte stubs;
 # this is a decoder contract check, not a replayed gameplay/native observation.
 olddecoder=load('historical_path_decoder_offline',LEGACY/'reader/path_failure_decoder.py')
 manifest=json.loads((LEGACY/'candidate-manifest.json').read_text('utf-8'))
 tests=[]
 for t in (70,71,81,84,85,86):
  d=json.loads((OLD/'U30-40'/f'T{t}.json').read_text('utf-8-sig'));shared=d['state']['shared_last_pass'];raw=bytes.fromhex(shared['path_failure_diagnostic']['rawhex'])
  f={k:(raw[o:o+8] if k in sys.modules['path_diagnostic_layout'].PAIRS else struct.unpack_from('<I',raw,o)[0]) for k,o in sys.modules['path_diagnostic_layout'].FIELDS.items()}
  slot=bytearray(1152);struct.pack_into('<II',slot,72,f['role'],f['prefix']);slot[:8]=f['destination']
  dep=struct.pack('<II',f['rawID'],f['kind'])+f['source']+bytes(16)
  def read(off,size):
   if off==0x40600+f['slot']*1152:return bytes(slot)
   if off==0x18200+f['departure']*32:return dep
   if off==0x526a0:return struct.pack('<'+'I'*shared['slots'],*range(shared['slots']))
   raise ValueError('Unexpected decoder own stub request')
  snapshot=struct.pack('<II',f['owner'],f['generation']);base=d['instance']['ai_base'];plan=f['plan_identity']
  old=olddecoder.decode_path(raw,shared,snapshot,read,plan,base,manifest,d['binding']['manifest_sha256'])
  new=reader.decode_path(raw,shared,snapshot,read,plan,base,manifest,d['binding']['manifest_sha256'])
  assert old==new and old['usable_diagnostic_evidence'],t
  tests.append(dict(turn=t,hard0_equal=True))
  if t==71:
   newmanifest=json.loads((ROOT/runtime['manifest_path']).read_text('utf-8'));local=bytearray(raw);state=copy.deepcopy(shared);state.update(status=5,reason=0)
   fields=sys.modules['path_diagnostic_layout'].FIELDS
   for key,value in dict(plan_identity=base+0xef000,direct_return=4,cache_return=4,selection_return=1,native_EAX=0,capacity=0,count=0,pointer=0,postcontext=0,canary1=0x3456ab89,canary2=0x4567bc90).items():struct.pack_into('<I',local,fields[key],value)
   for pair,prefix in [('finalize_selection','select'),('selection_cached','cache'),('cached_direct','direct')]:
    call=newmanifest['path_diagnostic']['calls'][pair]
    for key,value in [(prefix+'_call',call['call_rva']),(prefix+'_return_site',call['return_rva'])]:struct.pack_into('<I',local,fields[key],value)
   good=reader.decode_path(bytes(local),state,snapshot,read,base+0xef000,base,newmanifest,scope.MANIFEST)
   assert good['status']=='LOCAL_UNKNOWN_PAIR' and not good['certified']
   for field,value in [('native_EAX',1),('capacity',1),('cache_return',0),('selection_return',0),('postcontext',1)]:
    bad=bytearray(local);struct.pack_into('<I',bad,fields[field],value)
    result=reader.decode_path(bytes(bad),state,snapshot,read,base+0xef000,base,newmanifest,scope.MANIFEST)
    assert result['status']!='LOCAL_UNKNOWN_PAIR' and not result['usable_diagnostic_evidence'],field
 # Fresh diffs against exact historical source, including post-clone root fixes.
 for name,old in [('Lees-Duur.py',OLD/'Lees-Duur.py'),('scope.py',OLD/'scope.py'),('Pass-Duur.ps1',ROOT/'PROEVEN/uitbreiding-lang/20261022T171500-afronding/Afronding-85-100.ps1')]:
  (HERE/(name+'.diff')).write_text(''.join(difflib.unified_diff(old.read_text('utf-8').splitlines(True),(HERE/name).read_text('utf-8').splitlines(True),fromfile=old.relative_to(ROOT).as_posix(),tofile=(HERE/name).relative_to(ROOT).as_posix())),'utf-8')
 save('OFFLINE-CHECKS.json',dict(stage='C4_SOURCE_ONLY',syntax=True,import_without_main=True,live_memory=False,game=False,native_execution=False,build=False,binding=dict(candidate=binding['ai']['sha256'],manifest=binding['manifest_sha256'],state_rva=binding['shared_plan_rva'],state_size=binding['shared_plan_size']),unchanged_functions=changed,scope_cases=cases,old_reference_snapshots=101,hard0_decoder_contract=tests,synthetic_local4_contract=True,source_count=len(rows),source_pins_sha256=sha(HERE/'SOURCE-PINS.json')))
 print('C4 finite checks passed; no live reader main called')
if __name__=='__main__':main()
