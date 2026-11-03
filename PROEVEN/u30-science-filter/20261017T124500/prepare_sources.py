"""Reproducible source-only composition. No emitter import/compose or runtime."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
FILTER=ROOT/'PROEVEN/u30-kaartfilter/20261017T115000';C2=ROOT/'PROEVEN/science-u30-40/20261015T152300-c2';C1=ROOT/'PROEVEN/science-u30-40/20261013T183300'
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p.read_bytes()),size=p.stat().st_size)
def write(n,s):p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,'utf-8')
def replace(n,a,b):
 s=(OUT/n).read_text('utf-8');assert s.count(a)==1,(n,a);write(n,s.replace(a,b))
def function(path,name):
 s=path.read_text('utf-8');n=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name==name);return ''.join(s.splitlines(True)[n.lineno-1:n.end_lineno])
def replace_function(n,name,value):
 s=(OUT/n).read_text('utf-8');old=function(OUT/n,name);assert s.count(old)==1;write(n,s.replace(old,value))
sources=[]
for folder,expected,mexpected in [(FILTER,'738be4098dadc6657b121519213e794ce3ec095025fdc940f6c30a5d89661d66','d48b63b2363f0bfce2fe4b7d44a83b90951a524ecf3f300bf9661b50080be2a9'),(C2,'18d8516bf915d137acbc679c695bf4163540d01007888d875da24183035b230d','265b5ee53bcc5adc4216f0df2471b45b95c41d2d3e5d8121cf8fb78eea888167')]:
 assert sha((folder/'U30-40.prepared.dll').read_bytes())==expected
 assert sha((folder/'candidate-manifest.json').read_bytes())==mexpected
 m=json.loads((folder/'candidate-manifest.json').read_text('utf-8'))
 for row in m['sources']+m['source_dependency_pins']:assert sha((ROOT/row['path']).read_bytes())==row['sha256'],row['path']
 sources += [pin(folder/'candidate-manifest.json'),pin(folder/'U30-40.prepared.dll')]
for folder,names in [(FILTER,['native.py','policy.py','integration_base.py','input-pins.py','input-pins.json','bind_scheduler.py','release-v1.robotcom.backup.dll']),(C2,['build_candidate.py','check_candidate.py','union.py','science_model.py','science_layout.py','science_result.py','science_development.py'])]:
 for name in names:(OUT/name).write_bytes((folder/name).read_bytes());sources.append(pin(folder/name))
for name in ['roles','conflicts','selection']:replace_function('native.py',name,function(C2/'native.py',name))
replace('native.py','PLAN_SIZE=0x54800','PLAN_SIZE=0x79800')
replace('policy.py',"invoke(r,'production_roles')","invoke(r,'location_roles')")

write('plan_layout.py','''"""Single own Plan-header contract; different from H3/ScienceResult bases."""
FILTER_FIELDS=dict(prefix_count=224,known_count=228,gate_queries=232,gate_false=236)
COUNTERS={'calls':(240,64),'tiles':(244,1280),'spatial':(248,1280),'improvement':(252,3840),'primary_food':(256,1344),'development_food':(260,1280),'total_food':(264,2624)}
CONTEXT_ERROR=268
SCIENCE_BUDGET_EXHAUSTED=272
PLAN_SIZE=0x79800
STATE_SIZE=0x79804
''')
s=(OUT/'union.py').read_text('utf-8');a=s.index('COUNTERS=');b=s.index('_serial=',a)
s=s[:a]+"from plan_layout import COUNTERS,CONTEXT_ERROR,SCIENCE_BUDGET_EXHAUSTED\n"+s[b:]
write('union.py',s)
replace('union.py',"r.label(p+'_budget');r.mov(m('ebx',n.P['cutoff']),1)","r.label(p+'_budget');r.mov(m('ebx',n.P['cutoff']),1);r.mov(m('ebx',SCIENCE_BUDGET_EXHAUSTED),1)")
replace('union.py'," r.mov(m('ebx',n.P['slots']),0);r.mov(m('ebp',-16),0)",""" r.mov(m('ebx',SCIENCE_BUDGET_EXHAUSTED),0)
 # Same current filter producer/consumer invariants, before any ORDER read.
 r.mov('eax',m('ebx',n.P['prefix_count']));r.test('eax','eax');r.j('js','roles_bad');r.alu('cmp','eax',64);r.j('ja','roles_bad');r.alu('cmp','eax',m('ebx',n.P['known_count']));r.j('jg','roles_bad')
 r.mov('eax',m('ebx',n.P['known_count']));r.alu('cmp','eax',m('ebx',n.P['candidates']));r.j('jg','roles_bad');r.mov('eax',m('ebx',n.P['candidates']));r.alu('cmp','eax',4096);r.j('jg','roles_bad')
 r.mov(m('ebx',n.P['slots']),0);r.mov(m('ebp',-16),0)""")
replace('union.py',"r.alu('cmp','eax',m('ebx',n.P['candidates']));r.j('jge','roles_ok');r.alu('cmp','eax',64);r.j('jae','roles_budget');", "r.alu('cmp','eax',m('ebx',n.P['prefix_count']));r.j('jge','roles_ok');")
replace('union.py',"r.mov('eax',m('edx'));r.shift('shl','eax',3);", "r.mov('eax',m('edx'));r.test('eax','eax');r.j('js','roles_bad');r.alu('cmp','eax',m('ebx',n.P['candidates']));r.j('jae','roles_bad');r.shift('shl','eax',3);")
replace('union.py',"r.alu('cmp',m('ebx',n.P['h3calls']),64);r.j('jae','roles_budget');", "r.alu('cmp',m('ebx',n.P['h3calls']),64);r.j('jae','roles_bad');")
replace('union.py',"r.alu('cmp',m('ebx',n.P['cutoff']),0);r.j('jne','roles_budget');", "r.alu('cmp',m('ebx',SCIENCE_BUDGET_EXHAUSTED),0);r.j('jne','roles_budget');")
# Final context-only guard and error retargets already present in current C2.
replace('build_candidate.py','C2_POSITIVE_UNION_CANDIDATE_ONLY_NOT_INSTALLED_NOT_NATIVE_NOT_GAMEPLAY','SCIENCE_FILTER_UNION_SOURCE_CANDIDATE_ONLY_NOT_INSTALLED_NOT_NATIVE_NOT_GAMEPLAY')
replace('build_candidate.py',"proposal_sha256=prep['proposals'][1]['sha256']", "proposal_sha256=prep['proposals'][-1]['sha256']")
replace('build_candidate.py',"'science_development.py']]", "'science_development.py','plan_layout.py']]")
replace('build_candidate.py'," paths += [SCIENCE_MANIFEST,C2_PROPOSAL]", " paths += [SCIENCE_MANIFEST,C2_PROPOSAL,OUT/'science-spatial-pins.json']\n paths += list((OUT/'reader').glob('*.py'))+list((OUT/'control-reader').glob('*.py'))")
cm=json.loads((C1/'candidate-manifest.json').read_text('utf-8'));assert sha((C1/'candidate-manifest.json').read_bytes())=='2d63697a79a69b63c844da6f1ee8d2130f9c8b64e6e03152b18ee1df490d0387'
write('science-spatial-pins.json',json.dumps(cm['spatial_pins'],indent=2)+'\n');sources.append(pin(C1/'candidate-manifest.json'))
for folder in ['reader','control-reader']:
 for name in ['Lees-Uitbreiding.py','original_core.py','h3_layout.py','participants.json']:
  p=OUT/folder/name;p.parent.mkdir(exist_ok=True);p.write_bytes((FILTER/'reader'/name).read_bytes());sources.append(pin(FILTER/'reader'/name))
write('reader/runtime-pins.json',json.dumps(dict(stage='SOURCE_ONLY_UNBUILT',candidate_sha256=None,manifest_sha256=None,state_rva=None,state_size=0x79804),indent=2)+'\n')
(OUT/'control-reader/runtime-pins.json').write_bytes((FILTER/'reader/runtime-pins.json').read_bytes())
s=(OUT/'reader/Lees-Uitbreiding.py').read_text('utf-8')
s=s.replace('0x54804','0x79804').replace("FOLDER/'KAARTFILTER-ROOT-VRIJGAVE.json'", "FOLDER/'SCIENCE-FILTER-ROOT-VRIJGAVE.json'")
s=s.replace("if args.turn not in (0,1)","if args.turn not in (0,1,5,10)")
s=s.replace('original_binding=trusted_binding',"sys.path.insert(0,str(FOLDER.parent))\nfrom plan_layout import COUNTERS,CONTEXT_ERROR,SCIENCE_BUDGET_EXHAUSTED\nfrom positive_reader import selected_evidence\noriginal_binding=trusted_binding")
s=s.replace("    for rva,length in [(0x11bc0", "    for row in json.loads((FOLDER.parent/'science-spatial-pins.json').read_text('utf-8')):\n        raw=ep.get_data(row['rva'],row['length'])\n        if raw.hex()!=row['bytes']:raise ValueError('Frozen SCI spatial pin mismatch')\n        binding['ranges'].append(dict(module='engine',rva=row['rva'],length=row['length'],expected_hex=raw.hex(),kind='SCI spatial/Improvement body'))\n    for rva,length in [(0x11bc0")
s=s.replace("        shared={key:i32(ptr+off) for key,off in fields.items()}", "        fields.update({'SCI_'+name:off for name,(off,limit) in COUNTERS.items()})\n        fields.update(context_error=CONTEXT_ERROR,science_budget_exhausted=SCIENCE_BUDGET_EXHAUSTED)\n        shared={key:i32(ptr+off) for key,off in fields.items()}")
s=s.replace("        shared['slot0']=decode_slot0(slot,shared)","        shared['slot0_historical_reason23_diagnostic']=decode_slot0(slot,shared)\n        shared['selected_evidence']=selected_evidence(lambda off,size:read(checked(ptr,off),size),shared,participants['civ_ids'])")
write('reader/Lees-Uitbreiding.py',s)
s=(OUT/'control-reader/Lees-Uitbreiding.py').read_text('utf-8')
s=s.replace("mp=FOLDER.parent/'candidate-manifest.json'", "mp=ROOT/'PROEVEN/u30-kaartfilter/20261017T115000/candidate-manifest.json'")
s=s.replace("FOLDER/'KAARTFILTER-ROOT-VRIJGAVE.json'", "FOLDER/'SCIENCE-FILTER-CONTROL-ROOT-VRIJGAVE.json'").replace('if args.turn not in (0,1)','if args.turn not in (0,1,5,10)')
s=s.replace("        return shared\n", "        shared['science']='NIET_VAN_TOEPASSING_CONTROL54804'\n        return shared\n")
write('control-reader/Lees-Uitbreiding.py',s)
prep=json.loads((FILTER/'preparation-manifest.json').read_text('utf-8'));prep['stage']='SCIENCE_FILTER_SOURCE_ONLY_NO_COMPOSE_BUILD_NATIVE_OR_GAME';prep['checked_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();prep['source_pins']+=sources
for name in ['ANALYSE/U30-SCIENCE-FILTER-INTEGRATIE.md','ONTWERP/U30-SCIENCE-FILTER-INTEGRATIE.md']:prep['proposals'].append(pin(ROOT/name))
write('preparation-manifest.json',json.dumps(prep,indent=2)+'\n')
write('ROOT-BRONREVIEW.json',json.dumps(dict(candidate_build_allowed=False,native_allowed=False,game_allowed=False,reason='Await separate current source review'),indent=2)+'\n')
write('provenance.json',json.dumps(dict(stage='SOURCE_ONLY_UNBUILT',basis_filter_candidate='738be4098dadc6657b121519213e794ce3ec095025fdc940f6c30a5d89661d66',positive_union_source_candidate='18d8516bf915d137acbc679c695bf4163540d01007888d875da24183035b230d',dll_sections_combined=False,source_pins=sources),indent=2)+'\n')
for folder,names in [(FILTER,['native.py','policy.py','integration_base.py','input-pins.py']),(C2,['union.py','build_candidate.py','science_model.py','science_layout.py','science_development.py','check_candidate.py'])]:
 for name in names:write('diffs/'+name+'.diff',''.join(difflib.unified_diff((folder/name).read_text('utf-8').splitlines(True),(OUT/name).read_text('utf-8').splitlines(True),fromfile=str(folder.relative_to(ROOT))+'/'+name,tofile='science-filter/'+name)))
for name in ['reader','control-reader']:write('diffs/'+name+'.diff',''.join(difflib.unified_diff((FILTER/'reader/Lees-Uitbreiding.py').read_text('utf-8').splitlines(True),(OUT/name/'Lees-Uitbreiding.py').read_text('utf-8').splitlines(True),fromfile='current-filter-reader',tofile=name+'/Lees-Uitbreiding.py')))
for p in OUT.rglob('*.py'):ast.parse(p.read_text('utf-8'),filename=str(p))
print('Sources only prepared; no emitter import, compose, build, native or process access.')
