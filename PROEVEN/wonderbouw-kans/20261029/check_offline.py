"""Only finite scalar fixtures; no engine model, process, or game."""
from pathlib import Path
import importlib.util,json,sys,datetime
sys.dont_write_bytecode=True
p=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('_wonderbouw_fixture',p/'Lees-Wonderbouw.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.pins()
checks=[]
def run(name,raw,keys,cost,threshold,limit,field,expected):
    result=m.predicates(raw,keys,cost,threshold,limit)
    assert result[field]==expected,(name,result)
    checks.append(name)
c=dict(production=40,stock=0,key=10,incumbent=-1,flag=0)
run('within buildtime limit',c,[1,10],1999,0.4,50,'build_rounds_pass',True)
run('above buildtime limit',c,[1,10],2080,0.4,50,'build_rounds_pass',False)
run('tie crosses threshold',c,[10,10],1000,0.4,50,'rank_threshold_pass','UNKNOWN_TIE_AT_THRESHOLD')
run('tie entirely below threshold',c,[10,10],1000,0.8,50,'rank_threshold_pass',False)
run('stock exception bypasses tie',dict(c,stock=500),[10,10],1000,0.4,50,'production_rank_buildtime_possible_after_normal_queue',True)
run('stock ratio below five',dict(c,stock=500,production=101),[10,10],1000,0.4,50,'stored_production_exception',False)
run('production below thirty',dict(c,stock=500,production=29),[10,10],1000,0.4,50,'stored_production_exception',False)
run('busy incumbent blocks now',dict(c,incumbent=2),[1,10],1000,0.4,50,'ai_predicates_now',False)
run('busy incumbent leaves later production possibility',dict(c,incumbent=2),[1,10],1000,0.4,50,'production_rank_buildtime_possible_after_normal_queue',True)
run('nonzero cache flag blocks now',dict(c,flag=1),[1,10],1000,0.4,50,'ai_predicates_now',False)
run('production below one uses cost only',dict(c,production=0,stock=500),[1,10],40,0.4,50,'ai_build_rounds',40)
result=dict(stage='C0_OFFLINE_ONLY_NO_PROCESS',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=checks,
            runtime_chance='NOT_MEASURED',new_queue='NOT_MEASURED',admission='UNKNOWN')
if '--output' in sys.argv:
    out=p/'offline-result.json'
    if out.exists(): raise ValueError('Preserve previous output')
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
