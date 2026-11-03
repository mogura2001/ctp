"""Decode caller-owned saved ScienceResult bytes only; no RPM/GUI/process tools."""
import struct, math
from fractions import Fraction
from science_layout import HEADER, TILE, RESULT_SIZE, TILE_OFFSET, TILE_STRIDE, STRUCT_FUTURE_VALID
from development import DEV_TILE
LOCATION_NAMES={0:'UNKNOWN',1:'NO_CURRENT_NOW_SCENARIO',2:'NOW',
 3:'STRUCTURAL_POTENTIAL_SPATIAL_PENDING',4:'PENDING_GROWTH'}
DEVELOPMENT_NAMES={0:'UNKNOWN',1:'AVAILABILITY_PENDING',2:'PLACE_UNKNOWN',
 3:'READY_NOT_BUILT',4:'ALREADY_PRESENT'}
SUMMARY_NAMES={0:'UNKNOWN',1:'PENDING',3:'READY_NOT_BUILT',4:'ALREADY_PRESENT',
 5:'MIXED_PRESENT_READY'}

def development_summary(rows):
 if len(rows)!=3 or any(row['development']['status'] not in (1,2,3,4) for row in rows):return 0
 states={row['development']['status'] for row in rows}
 if states & {1,2}:return 1
 if states=={3}:return 3
 if states=={4}:return 4
 return 5

def valid_future(row):
 """Do not infer validity from an intermediate future_food/delta value."""
 dev=row['development'];flags=row['structure_flags'];state=dev['status']
 if flags & (16|1|2|STRUCT_FUTURE_VALID)!=(16|1|2|STRUCT_FUTURE_VALID):return False
 if state not in (1,2,3,4) or dev['reason']!=0 or dev['required_advance_id'] < -1:return False
 current=row['current_food_i32'];future=dev['future_food_i32'];delta=dev['delta_i32']
 if current<0 or future<0 or row['raw_spatial'] not in (0,1):return False
 if state==4:
  return bool(flags&4) and dev['already_present']==1 and bool(dev['conditions']&4) and future==current and delta==0 and dev['food_delta_double']==0
 if not dev['conditions']&8 or dev['already_present']!=0:return False
 value=dev['food_delta_double']
 return math.isfinite(value) and value==delta and -2**31<=current+delta<2**31 and future==current+delta

def scenario(header,rows,field):
 """Computed explanation from bytes; never a native/game execution claim."""
 if len(rows)!=3:return None
 total=header['center_food_i64'];stand=header['ration_stand'];steps=[]
 if total<0 or stand < -3 or not math.isfinite(header['actual_R']) or header['actual_R']!=1+stand/4:return None
 for n,row in enumerate(rows,1):
  food=row['current_food_i32'] if field=='current' else row['development']['future_food_i32']
  if food<0:return None
  total+=food;denominator=2*total;demand=20*n+5*n*stand;margin=denominator-demand
  if not all(-2**63<=value<2**63 for value in (total,denominator,demand,margin)):return None
  steps.append(dict(n=n,k=n,S_i64=total,demand_x2_i64=demand,margin_x2_i64=margin,crime_numerator_i64=margin,crime_denominator_i64=denominator))
 positive=all(step['margin_x2_i64']>0 and step['crime_denominator_i64']>0 for step in steps)
 minimum=min((Fraction(step['crime_numerator_i64'],step['crime_denominator_i64']) for step in steps if step['crime_denominator_i64']>0),default=None)
 return dict(selected_indices=[row['index'] for row in rows],steps=steps,strict_positive_n1_n2_n3=positive,
  minimum_crime_fraction=[minimum.numerator,minimum.denominator] if minimum is not None else None,
  development_state_name=SUMMARY_NAMES[development_summary(rows)],conditional_only=True)
def decode(raw):
 if len(raw)!=RESULT_SIZE:raise ValueError('ScienceResult must be exactly 2048 bytes')
 def i32(off):return struct.unpack_from('<i',raw,off)[0]
 header={name:(struct.unpack_from('<d',raw,off)[0] if name=='actual_R' else
  struct.unpack_from('<hhhH',raw,off) if name=='center_key' else
  struct.unpack_from('<q' if size==8 else '<i',raw,off)[0]) for name,(off,size) in HEADER.items()}
 count=header['open_count']
 if not 0<=count<=20:raise ValueError('Invalid bounded tile count')
 rows=[]
 for index in range(count):
  base=TILE_OFFSET+index*TILE_STRIDE
  development={name:(struct.unpack_from('<d',raw,base+32+off)[0] if name=='food_delta_double' else i32(base+32+off)) for name,off in DEV_TILE.items()}
  development['state_name']=DEVELOPMENT_NAMES.get(development['status'],'INVALID')
  rows.append(dict(index=index,canonical_key=struct.unpack_from('<hhhH',raw,base),external_MapPoint=struct.unpack_from('<hhhH',raw,base+8),current_food_i32=i32(base+16),structure_flags=i32(base+20),raw_spatial=i32(base+24),spatial_reason=i32(base+28),development=development))
 current_indices=[header['selected'+str(i)] for i in range(3)]
 if any(index < -1 or index >= count for index in current_indices):raise ValueError('Invalid current selection index')
 current_rows=[rows[index] for index in current_indices if index!=-1]
 if len({row['canonical_key'][:3] for row in current_rows})!=len(current_rows):raise ValueError('Duplicate current canonical selection')
 # Future rank is independent of current indices and preserves every raw field.
 future_rows=sorted((row for row in rows if row['structure_flags']&8 and valid_future(row)),key=lambda row:(-row['development']['future_food_i32'],row['canonical_key'][:3]))[:3]
 trusted=header['coverage']==1
 current=scenario(header,current_rows,'current') if trusted else None
 future=scenario(header,future_rows,'future') if trusted else None
 if future is not None:
  future['conditions']=['ZERO_NEW_CITY_MODIFIERS','CONDITIONAL_CRIME','ENABLING_AND_PLACEMENT_REVALIDATED','QUERIED_IMPROVEMENTS_BUILT','UNCHANGED_CURRENT_FOOD_CONTEXT']
  future['spatial_pending_indices']=[] # future scenario never substitutes for spatial certification
 parity=None if not trusted else (header['location_state']==4)==bool(header['location_state']!=2 and future and future['strict_positive_n1_n2_n3'])
 return dict(header=header,location_name=LOCATION_NAMES.get(header['location_state'],'INVALID'),
  development_name=SUMMARY_NAMES.get(header['development_state'],'INVALID'),
  computed_current=current,computed_future=future,tiles=rows,science_credit_enabled=False,
  conditional_only=True,future_growth_calculation_implemented=True,
  diagnostic_origin='arithmetic from caller-owned saved bytes; future indices were native-private stack data',
  summary_selection='selected CURRENT indices only',
  native_pending_parity=parity,
  native_pending_parity_status='NOT_APPLICABLE_UNTRUSTED_COVERAGE' if parity is None else 'MATCH' if parity else 'MISMATCH')
