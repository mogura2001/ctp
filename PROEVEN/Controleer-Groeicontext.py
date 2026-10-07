"""Original positive growth with explicit player/difficulty/happiness context.

Reuses synthetic ordinary-city fixture. Population/record lookup/creation and
network predicate are explicit mocks. Actual happy-threshold comparison and
growth arithmetic execute original instructions; no complete turn or gameplay.
"""
import importlib.util,json,math
from pathlib import Path
p=Path(__file__).with_name('Controleer-Groeivoorraad.py')
spec=importlib.util.spec_from_file_location('growth_stock',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
checks=[]
for kind,bonus,happy,silo,network,remote in [
    (1,0,75,False,False,False),(0,0,75,False,False,False),
    (0,-.4,75,False,False,False),(1,-.4,75,False,False,False),
    (0,.25,75,False,False,False),(2,.25,75,False,False,False),
    (1,-.4,75,False,True,True),(1,-.4,75,False,True,False),
    (1,0,85,False,False,False),(1,0,85,True,False,False),
    (0,.25,85,True,False,False),(0,-.4,85,False,False,False),
]:
    threshold=700
    adjusted=kind!=1 or (network and remote)
    if adjusted:threshold+=math.trunc(700*bonus)
    if happy>=85:threshold=threshold*3//4 if silo else threshold//2
    for available in (threshold-1,threshold):
        stored=available-10;grows=available>=threshold
        exp=dict(population=4+int(grows),growth_food=(875//2 if silo else available-threshold) if grows else available,
                 food_buffer=10 if silo else 0,growth_calls=int(grows))
        got=m.emulate(4,stored,10,silo,player_type=kind,difficulty_bonus=bonus,happiness=happy,
                      network_active=network,network_remote=remote)
        checks.append(dict(player_type=kind,difficulty_bonus=bonus,happiness=happy,silo=silo,
                           network_active=network,network_remote=remote,threshold=threshold,stored=stored,
                           got=got,expected=exp,passed=got==exp))
print(json.dumps(dict(engine_sha256=m.SHA,limitations=__doc__,checks=checks,
    passed=sum(c['passed'] for c in checks),total=len(checks)),indent=2))
if not all(c['passed'] for c in checks):raise SystemExit(1)
