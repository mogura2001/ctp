"""Bind actual completed offline results; never read installations again."""
from pathlib import Path
import sys,json,hashlib,struct,datetime
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
processes=load(OUT/'native-processes.json');assert len(processes)==10 and all(p['exit_code']==0 for p in processes)
pins=load(OUT/'input-pins.json');assert len(pins['bodies'])==15 and len(pins['slots'])==6
protected=load(OUT/'protected-check.json');assert protected['pass_'] and not protected['deltas'] and protected['installation_files']==3090 and protected['previous_package_files']==120
original=(ROOT/'PROEVEN/production-h3/backup/robotcom.original.dll').read_bytes();op=pefile.PE(data=original)
variants=[]
for n in (25,30):
 for enabled in (False,True):
  name=('B4' if enabled else 'BASELINE')+'-N'+str(n);manifest=load(OUT/(name+'.manifest.json'));data=(OUT/(name+'.prepared.dll')).read_bytes();code=(OUT/(name+'.payload.bin')).read_bytes();assert sha(data)==manifest['candidate_sha256'] and sha(code)==manifest['payload_sha256'];pe=pefile.PE(data=data)
  for rebase in (False,True):
   result=load(OUT/(name+'.native-loader'+('-rebase' if rebase else '')+'.json'));assert result['pass'] and result['candidate_sha256']==sha(data) and result['actual_rebase']==rebase
  if enabled:
   assert manifest['input_pins']==pins
   native=load(OUT/(name+'.native-producer.json'));assert native['pass'] and native['cases']==109 and native['candidate_sha256']==sha(data) and native['inputguard_actual_emitted_independent_cases']==22
   base=int(manifest['components']['B4']['rva'],16);wrappers={0x65a4c:base+manifest['labels']['quota_hook'],0x66b81:base+manifest['labels']['desired_hook']}
   # Actual and Choose bytes untouched; Desired and AIPUpdate differ solely
   # at the declared callsite, preserving native actual/priority construction.
   for start,length in ((0x655f0,0x2d0),(0x65900,0xa0),(0x659a0,0x320),(0x66b70,0x30)):
    before=bytearray(op.get_data(start,length))
    for site,target in wrappers.items():
     if start<=site<start+length:before[site-start:site-start+5]=b'\xe8'+struct.pack('<i',target-site-5)
    assert bytes(before)==pe.get_data(start,length)
   stage='COMPLETE OFFLINE FIXTURE/LOADER CHECKS; ROOT REVIEW PENDING'
  else:stage='OFFLINE COMPOSITION/LOADER CHECKS'
  variants.append(dict(name=name,sha256=sha(data),payload_sha256=sha(code),stage=stage,components=manifest['components']))
record=dict(reported_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),variants=variants,native_calls_per_N=109,independent_inputguard_cases_per_N=22,native_helpers_exit0=10,prepared=True,installed=False,offline_checked=True,root_accepted=False,real_host_accepted=False,gameplay_measured=False,performance_accepted=False,production_N_chosen=False,protected_snapshot=protected,scope='actual emitted producer/H3-current and fivewrapper chain with explicit controlled native inputs; standalone real15body6slot guard; original native Actual/Choose/Desired/AIPUpdate retained with intended hooks; ordinary loader/rebase; no engine/gameplay acceptance',pass_=True)
(OUT/'offline-results.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(dict(native_calls_per_N=109,independent_guard_cases=22,helpers=10,protected=3210,pass_=True)))
