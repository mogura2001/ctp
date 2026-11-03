"""Finite AST/layout/provenance integration checks; no imports of emitters."""
from pathlib import Path
import ast,datetime,hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
FILTER=ROOT/'PROEVEN/u30-kaartfilter/20261017T115000';C2=ROOT/'PROEVEN/science-u30-40/20261015T152300-c2'
sha=lambda b:hashlib.sha256(b).hexdigest()
def tree(p):return ast.parse(p.read_text('utf-8'))
def funcs(p):return {n.name:ast.dump(n) for n in tree(p).body if isinstance(n,ast.FunctionDef)}
def value(p,name):return next(n.value for n in tree(p).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
for p in OUT.rglob('*.py'):tree(p)
f=funcs(FILTER/'native.py');n=funcs(OUT/'native.py');c=funcs(C2/'native.py')
for name in f:
 assert n[name]==(c[name] if name in ('roles','conflicts','selection') else f[name]),name
fpol=funcs(FILTER/'policy.py');npol=funcs(OUT/'policy.py')
for name in fpol:
 if name!='finalize':assert fpol[name]==npol[name],name
assert (OUT/'policy.py').read_text().replace("invoke(r,'location_roles')","invoke(r,'production_roles')")==(FILTER/'policy.py').read_text()
for name in ['integration_base.py','input-pins.py','input-pins.json','bind_scheduler.py']:assert (OUT/name).read_bytes()==(FILTER/name).read_bytes(),name
for name in ['science_model.py','science_development.py','science_layout.py','science_result.py','check_candidate.py']:assert (OUT/name).read_bytes()==(C2/name).read_bytes(),name
p={k.arg:ast.literal_eval(k.value) for k in value(OUT/'native.py','P').keywords};contract=OUT/'plan_layout.py'
counters=ast.literal_eval(value(contract,'COUNTERS'));filterfields={k.arg:ast.literal_eval(k.value) for k in value(contract,'FILTER_FIELDS').keywords}
assert {k:p[k] for k in filterfields}==filterfields
expected=dict(calls=(240,64),tiles=(244,1280),spatial=(248,1280),improvement=(252,3840),primary_food=(256,1344),development_food=(260,1280),total_food=(264,2624));assert counters==expected
fields=list(p.values())+[136,144,148,152,156,160,164,168]+[v[0] for v in counters.values()]+[268,272]
assert len(fields)==len(set(fields)) and max(fields)+4==276 and 276<=0x200
assert ast.literal_eval(value(OUT/'native.py','PLAN_SIZE'))==0x79800
assert 0x54800+64*2048==0x74800 and 0x74800+64*2*128==0x78800 and 0x78800+4096==0x79800
for name in ['CAPTURE','CAPTURE_CAP','PREVIEW','PREVIEW_CAP','PREVIEW_STRIDE','DEPARTURES','DEPARTURE_CAP','DEPARTURE_STRIDE','VISITED','NODE_CAP','NODE_STRIDE','STACK','STACK_CAP','HINTS','HINT_CAP','HINT_STRIDE','SLOTS','SLOT_CAP','SLOT_STRIDE','SELECTED','SELECTED_CAP','ORDER','PATHCACHE','PATHCACHE_CAP','PATHCACHE_STRIDE']:assert ast.dump(value(OUT/'native.py',name))==ast.dump(value(FILTER/'native.py',name)),name
u=(OUT/'union.py').read_text();assert "m('ebx',n.P['cutoff']),0" not in u
assert u.count('m(\'ebx\',SCIENCE_BUDGET_EXHAUSTED),1')==1
assert "n.P['h3calls']),64);r.j('jae','roles_bad')" in u
assert "r.label('roles_postscience_context');counter(r,[],'roles_bad')" in u and "r.label('roles_final_context');counter(r,[],'roles_bad')" in u
assert "m('ebx',n.P['prefix_count'])" in u and "r.j('jae','roles_bad');r.shift('shl','eax',3)" in u
assert funcs(OUT/'union.py')['choose']==funcs(C2/'union.py')['choose'] and funcs(OUT/'union.py')['validate']==funcs(C2/'union.py')['validate']
builder=(OUT/'build_candidate.py').read_text();assert 'union._serial=0' in builder and 'rw=align(extension+len(r.code),0x1000)' in builder
prep=json.loads((OUT/'preparation-manifest.json').read_text('utf-8'))
for row in prep['release_pins']+prep['proposals']+prep['source_pins']:assert sha((ROOT/row['path']).read_bytes())==row['sha256'],row['path']
assert json.loads((OUT/'reader/runtime-pins.json').read_text())['candidate_sha256'] is None
assert not (OUT/'candidate-manifest.json').exists() and not (OUT/'U30-40.prepared.dll').exists()
result=dict(stage='SOURCE_ONLY_AST_LAYOUT_PINS_NOT_EMITTED_OR_RUNTIME',checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),filter_type_prefix_all_other_native_functions_retained=True,c2_roles_conflicts_selection_retained=True,c2_kernel_development_schema_unchanged=True,filter_world_type_bodypins_unchanged=True,all_provenance_and_release_pins_match=True,header_disjoint_until=276,filter_fields=filterfields,science_counters=counters,context_error=268,science_budget_exhausted=272,PlanSize=0x79800,state_size=0x79804,prefix_cutoff_not_science_budgetstop=True,postscience_and_final_context_guards_retained=True,compile_build_native_rpm_game=0,changed_B4_B7_and_integration_cases='ONGETEST')
(OUT/'source-checks.json').write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps(result))
