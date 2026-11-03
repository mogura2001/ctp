"""Bounded own Plan bytes only; positive union evidence is not first-H3diagnosis."""
import math,struct
from plan_layout import COUNTERS,CONTEXT_ERROR,SCIENCE_BUDGET_EXHAUSTED,STATE_SIZE

def selected_evidence(read,shared,civ_ids):
 def own(off,size):
  if not 0<=off or not 1<=size<=8192 or off+size>STATE_SIZE:raise ValueError('own-state range')
  raw=read(off,size)
  if len(raw)!=size:raise ValueError('incomplete own-state read')
  return raw
 def i(raw,off):return struct.unpack_from('<i',raw,off)[0]
 def q(raw,off):return struct.unpack_from('<q',raw,off)[0]
 def key(raw,off):
  x,y,z,padding=struct.unpack_from('<hhhH',raw,off)
  if min(x,y)<0 or z!=0:raise ValueError('invalid canonical key')
  return (x,y,z)
 result=dict(status='UNKNOWN',only_last_bound_civ_pass=True,other_civs_certified=False,selected=[],gameplay_improvement_proven=False)
 try:
  if not (shared['civ'] in civ_ids and shared['generation']>0 and shared['context']==1 and shared['reason']==0 and shared['status'] in (4,5) and shared['context_error']==0):raise ValueError('last-pass context not certified')
  owner,generation=struct.unpack('<2I',own(0x78800,8))
  if not owner or generation!=shared['generation'] or shared['owner'] not in (0,owner):raise ValueError('owner/generation snapshot mismatch')
  if not (0<=shared['prefix_count']<=64 and shared['prefix_count']==min(64,shared['known_count']) and 0<=shared['known_count']<=shared['candidates']<=4096 and shared['gate_queries']==shared['candidates']==shared['known_count']+shared['gate_false'] and shared['gate_false']>=0):raise ValueError('prefix invariants')
  if not (shared['science_budget_exhausted'] in (0,1) and 0<=shared['Gcert']<=40 and 0<=shared['slots']<=shared['prefix_count']):raise ValueError('selected/slot budget')
  for name,(off,limit) in COUNTERS.items():
   if not 0<=shared['SCI_'+name]<=limit:raise ValueError('query counter '+name)
  if shared['Gcert']>shared['slots']:raise ValueError('Gcert exceeds slots')
  selected=[struct.unpack('<I',own(0x52600+4*n,4))[0] for n in range(shared['Gcert'])]
  if len(set(selected))!=len(selected) or any(n>=shared['slots'] for n in selected):raise ValueError('selected index outside slots')
  used=set()
  for index in selected:
   slot=own(0x40600+index*1152,1152);role=i(slot,72);count=i(slot,28);prefix=i(slot,76)
   if (role,count) not in ((1,5),(2,4)) or not 0<=prefix<shared['prefix_count']:raise ValueError('role/count/prefix index')
   if i(slot,80)!=role-1:raise ValueError('alternative index is not role minus one')
   keys=[key(slot,32+8*n) for n in range(count)]
   if keys[0]!=key(slot,8) or len(set(keys))!=count or used&set(keys):raise ValueError('mandatory keys inconsistent or conflicting')
   used.update(keys)
   row=dict(slot_index=index,role=role,mandatory_count=count,keys=keys,prefix_result_index=prefix,alternative_index=i(slot,80),source_id=i(slot,20),source_index=i(slot,24),slot_rawhex=slot.hex())
   if role==2:
    raw=own(0x54800+prefix*2048,2048);open_count=i(raw,16);indices=[i(raw,28+4*n) for n in range(3)]
    if not (i(raw,0)==2 and i(raw,4)==0 and i(raw,8)==1 and i(raw,12)==3 and i(raw,112)==1 and 0<=open_count<=20):raise ValueError('SCI NOW/model/conditions/coverage')
    if not (len(set(indices))==3 and all(0<=n<open_count for n in indices)):raise ValueError('SCI selected index')
    if key(raw,116)!=keys[0]:raise ValueError('SCI center mismatch')
    foods=[];tiles=[]
    for n,expected in zip(indices,keys[1:]):
     off=128+n*96;flags=i(raw,off+20);spatial=i(raw,off+24);food=i(raw,off+16)
     if key(raw,off)!=expected or flags&(16|8)!=(16|8) or spatial!=1 or food<0:raise ValueError('SCI current foodkey/rawspatial mismatch')
     foods.append(food);tiles.append(dict(index=n,key=expected,current_food=food,raw_spatial=spatial,structure_flags=flags))
    stand=i(raw,56);actual_r=struct.unpack_from('<d',raw,64)[0];total=q(raw,72);steps=[]
    if stand < -3 or not math.isfinite(actual_r) or actual_r!=1+stand/4 or not 0<=total<=0x7fffffff:raise ValueError('SCI current ration/center contract')
    for n,food in enumerate(foods,1):
     total+=food;denominator=2*total;demand=20*n+5*n*stand;margin=denominator-demand
     if not all(-2**63<=v<2**63 for v in (total,denominator,demand,margin)) or margin<=0 or denominator<=0:raise ValueError('SCI current n1/2/3 margins')
     steps.append(dict(n=n,S=total,demand_x2=demand,margin_x2=margin,crime_denominator=denominator))
    if (q(raw,80),q(raw,88),q(raw,96),q(raw,104))!=(total,steps[-1]['margin_x2'],steps[-1]['margin_x2'],steps[-1]['crime_denominator']):raise ValueError('SCI raw current summary mismatch')
    row['science']=dict(location='NOW',coverage=1,center=keys[0],tiles=tiles,current_steps=steps,result_rawhex=raw.hex(),future_food_credit=False,conditional_new_city_model=True)
   result['selected'].append(row)
  result.update(status='CONSISTENT_LAST_PASS_SELECTION',civ=shared['civ'],generation=shared['generation'],Gcert=shared['Gcert'],science_selected=sum(r['role']==2 for r in result['selected']),production_selected=sum(r['role']==1 for r in result['selected']),science_budget_exhausted=shared['science_budget_exhausted'])
 except ValueError as error:
  result['reason']=str(error)
 return result
