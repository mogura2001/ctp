"""Bounded own Plan diagnosis, never selection/certification or engine pointers."""
from pathlib import Path
import ast, hashlib, importlib.util, json, math, struct, sys, types
sys.dont_write_bytecode = True
HERE=Path(__file__).resolve().parent
PACK=HERE.parent
C1=PACK.parents[1]/'science-u30-40/20261013T183300'
sys.path.insert(0,str(PACK))
import science_layout as layout
import positive_reader, plan_layout
def dev_schema(path):
 return ast.literal_eval(next(n.value for n in ast.parse(path.read_text('utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DEV_TILE' for t in n.targets)))
# science_result imports the generic name development. Bind only its existing
# literal schema explicitly: no emitter/model import, no alternate food model.
development=types.ModuleType('development');development.__file__=str(PACK/'science_development.py')
development.DEV_TILE=dev_schema(PACK/'science_development.py')
if development.DEV_TILE!=dev_schema(C1/'development.py') or development.DEV_TILE!=dev_schema(PACK.parents[1]/'science-u30-40/20261015T152300-c2/science_development.py'):raise ValueError('DEV_TILE schema drift')
previous=sys.modules.get('development')
try:
 sys.modules['development']=development
 spec=importlib.util.spec_from_file_location('diagnostic_pinned_science_result',PACK/'science_result.py')
 science_result=importlib.util.module_from_spec(spec);spec.loader.exec_module(science_result)
finally:
 if previous is None:sys.modules.pop('development',None)
 else:sys.modules['development']=previous
for module,path in ((layout,PACK/'science_layout.py'),(science_result,PACK/'science_result.py'),
                    (positive_reader,HERE/'positive_reader.py'),(plan_layout,PACK/'plan_layout.py')):
 if Path(module.__file__).resolve()!=path.resolve():raise ValueError('Diagnostic import drift: '+module.__name__)
STATE_SIZE=0x79804
assert STATE_SIZE==plan_layout.STATE_SIZE and layout.RESULT_SIZE==2048
PROVENANCE={str(Path(m.__file__).resolve().relative_to(PACK.parents[2])):hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest() for m in (layout,science_result,positive_reader,plan_layout,development)}
PROVENANCE.update({str(p.relative_to(PACK.parents[2])):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__).resolve(),HERE/'Lees-Uitbreiding.py',HERE/'h3_layout.py')})

def integer(raw,off):return struct.unpack_from('<i',raw,off)[0]
def key(raw,off):return struct.unpack_from('<hhhH',raw,off)[:3]
def canonical(value):return value[0]>=0 and value[1]>=0 and value[2]==0
def safe(value):
 if isinstance(value,float) and not math.isfinite(value):return dict(invalid='NONFINITE',rawbits_le=struct.pack('<d',value).hex())
 if isinstance(value,dict):return {k:safe(v) for k,v in value.items()}
 if isinstance(value,(list,tuple)):return [safe(v) for v in value]
 return value

def science(raw):
 """Raw schema decode survives invalid selection; existing decoder is separate."""
 header={name:(struct.unpack_from('<d',raw,off)[0] if name=='actual_R' else struct.unpack_from('<hhhH',raw,off) if name=='center_key' else struct.unpack_from('<q' if size==8 else '<i',raw,off)[0]) for name,(off,size) in layout.HEADER.items()}
 count=header['open_count'];rows=[]
 if 0<=count<=layout.MAX_TILES:
  for index in range(count):
   base=layout.TILE_OFFSET+index*layout.TILE_STRIDE
   dev={name:struct.unpack_from('<d' if name=='food_delta_double' else '<i',raw,base+32+off)[0] for name,off in development.DEV_TILE.items()}
   rows.append(dict(index=index,canonical_key=struct.unpack_from('<hhhH',raw,base),external_MapPoint=struct.unpack_from('<hhhH',raw,base+8),current_food_i32=integer(raw,base+16),structure_flags=integer(raw,base+20),raw_spatial=integer(raw,base+24),spatial_reason=integer(raw,base+28),development=dev))
 result=dict(header=safe(header),tiles=safe(rows),raw_header_decode_status='DECODED',bounded_tile_decode_status='DECODED' if 0<=count<=20 else 'INVALID_OPEN_COUNT',attribution_status='OWN_BYTES_NOT_PHASE_PROOF',coverage_positive_calculation_allowed=header['coverage']==1,actual_R_rawbits_le=raw[64:72].hex())
 try:result.update(existing_decoder_status='DECODED',existing_decoder=safe(science_result.decode(raw)))
 except Exception as error:result.update(existing_decoder_status='ERROR',existing_decoder_error=type(error).__name__+': '+str(error))
 return result

def prepared(slot,raw):
 """Same current-only invariants as pinned positive_reader, with no selection."""
 result=dict(status='INCONSISTENT_OR_INCOMPLETE',selected=False,certified=False,future_food_credit=False,conditional_new_city_model=True)
 try:
  h=science_result.decode(raw)['header'];count=h['open_count'];indices=[h['selected'+str(n)] for n in range(3)]
  if (integer(slot,72),integer(slot,28),integer(slot,80),integer(slot,84),integer(slot,88),integer(slot,92))!=(2,4,1,3,0,1):raise ValueError('slot role/count/alternative/conditions/reason/prepared')
  keys=[key(slot,32+8*n) for n in range(4)]
  if key(slot,8)!=keys[0] or len(set(keys))!=4 or not all(map(canonical,keys)):raise ValueError('slot mandatory canonical keys')
  if (h['location_state'],h['reason'],h['model'],h['conditions'],h['coverage'])!=(2,0,1,3,1) or not 0<=count<=20:raise ValueError('SCI NOW/reason/model/conditions/coverage')
  if len(set(indices))!=3 or not all(0<=n<count for n in indices):raise ValueError('SCI selected index')
  if key(raw,116)!=keys[0]:raise ValueError('SCI center mismatch')
  rows=science_result.decode(raw)['tiles'];selected=[rows[n] for n in indices]
  for row,expected in zip(selected,keys[1:]):
   if tuple(row['canonical_key'][:3])!=expected or row['structure_flags']&24!=24 or row['raw_spatial']!=1 or row['current_food_i32']<0:raise ValueError('SCI current foodkey/rawspatial/flags')
  if not 0<=h['center_food_i64']<=0x7fffffff:raise ValueError('current center food contract')
  scenario=science_result.scenario(h,selected,'current')
  if scenario is None or not scenario['strict_positive_n1_n2_n3']:raise ValueError('SCI current ration/int64/n1/n2/n3 margins')
  last=scenario['steps'][-1]
  if (h['S3_current_i64'],h['margin3_x2_i64'],h['crime_numerator_i64'],h['crime_denominator_i64'])!=(last['S_i64'],last['margin_x2_i64'],last['margin_x2_i64'],last['crime_denominator_i64']):raise ValueError('SCI stored current summary')
  h2count=integer(slot,128+128+8);mountains=integer(slot,128+128+12)
  result.update(status='CONSISTENT_PREPARED_CONDITIONAL_SCIENCE_NOW_EXAMPLE',keys=keys,current_scenario=scenario,H3_status=integer(slot,128),H3_model=integer(slot,136),H2_status=integer(slot,128+128),H2_count=h2count,H2_mountains=mountains,three_mountains_absent=True if integer(slot,128)==1 and integer(slot,136)==1 and integer(slot,128+128)==1 and 0<=h2count<=20 and 0<=mountains<3 else None)
 except Exception as error:result['error']=type(error).__name__+': '+str(error)
 return safe(result)

def slot_header(raw):
 fields={name:integer(raw,off) for name,off in dict(source_id=20,source_index=24,mandatory_count=28,role=72,prefix=76,alternative=80,conditions=84,SCIreason=88,prepared=92).items()}
 count=fields['mandatory_count']
 fields.update(external_center=key(raw,0),canonical_center=key(raw,8),keys=[key(raw,32+8*n) for n in range(count)] if 0<=count<=5 else 'INVALID_COUNT',phase_status='RAW_UNCOMMITTED_NOT_PHASE_PROOF')
 return fields

def diagnose(read,shared,slot0,civ_ids,module_size,state_rva,decode_h3):
 result=dict(status='UNSELECTED_PARTIAL_PASS_DIAGNOSTIC',selected=False,certified=False,only_last_bound_civ_pass=True,other_civs_certified=False,gameplay_improvement_proven=False,provenance=PROVENANCE,objects=[],attribution_status='NOT_VALIDATED',usable_diagnostic_evidence=False,original_indices_reproduced=False)
 def own(off,size,index=None,kind=None):
  if not (isinstance(off,int) and 0<=off and 1<=size<=2048 and off+size<=STATE_SIZE and state_rva==0xe1000 and state_rva+off+size<=module_size):raise ValueError('diagnostic own-state/module bounds')
  raw=read(off,size)
  if len(raw)!=size:raise ValueError('incomplete diagnostic read')
  obj=dict(kind=kind,index=index,offset=off,length=size,rawhex=raw.hex(),provenance=PROVENANCE,decode_status='RAW_PRESERVED',attribution_status='OWN_BYTES_NOT_PHASE_PROOF')
  result['objects'].append(obj)
  return raw,obj
 def table(base,stride,index,limit,size,kind):
  if not isinstance(index,int) or not 0<=index<limit:raise ValueError('invalid '+kind+' index')
  if not size<=stride or base+limit*stride>STATE_SIZE:raise ValueError('table extent')
  return own(base+stride*index,size,index,kind)
 try:
  if shared['generation']==0:
   result.update(attribution_status='NOT_INITIALIZED',main_questions=dict(earlier_current_food='NOT_INITIALIZED',failure_branch='NOT_INITIALIZED'));return result
  if not (shared['civ'] in civ_ids and shared['generation']>0 and shared['context']==1 and shared['context_error']==0):raise ValueError('last-pass binding/context invalid')
  snapshot,obj=own(0x78800,8,kind='owner_generation_snapshot');owner,generation=struct.unpack('<2I',snapshot)
  obj.update(decode_status='DECODED',owner=owner,generation=generation)
  if not owner or generation!=shared['generation'] or shared['owner'] not in (0,owner):raise ValueError('owner/generation snapshot mismatch')
  prefix=shared['prefix_count'];classified=shared['classified'];slots=shared['slots'];candidates=shared['candidates']
  if not (0<=prefix<=64 and prefix==min(64,shared['known_count']) and 0<=shared['known_count']<=candidates<=4096 and shared['gate_queries']==candidates==shared['known_count']+shared['gate_false'] and shared['gate_false']>=0 and 0<=classified<=prefix and 0<=slots<=64 and slots<=prefix):raise ValueError('prefix/classified/slot invariants')
  result.update(attribution_status='BOUND_LAST_CIV_GENERATION',usable_diagnostic_evidence=True,civ=shared['civ'],generation=shared['generation'],phase_claim='PARTIAL_PASS_RAW_FIELDS_DO_NOT_PROVE_EVERY_STAGE')
  earlier=integer(slot0,76) if slots>0 and integer(slot0,72)==2 and integer(slot0,92)==1 else None
  if earlier is not None and not 0<=earlier<prefix:raise ValueError('earlier prefix index invalid')
  last=classified-1 if 1<=classified<=prefix else None
  results={}
  for index in dict.fromkeys(i for i in (earlier,last) if i is not None):
   raw,obj=table(layout.SCIENCE_RESULTS,2048,index,64,2048,'ScienceResult');obj.update(decode_status='DECODED',decode=science(raw));results[index]=raw
  result['earlier_science_example']=prepared(slot0,results[earlier]) if earlier is not None else dict(status='NIET_OBSERVEERD')
  result['earlier_science_result_index']=earlier;result['last_started_science_result_index']=last
  result['slot0_reused']=dict(index=0,offset=0x40600,length=len(slot0),rawhex=slot0.hex(),provenance=PROVENANCE,decode_status='DECODED',attribution_status='EARLIER_COMMITTED_ROLE_HEADER' if slots>0 else 'NOT_PROVEN_COMMITTED',decode=slot_header(slot0))
  work=None
  if slots<64:
   raw,obj=table(0x40600,1152,slots,64,1152,'uncommitted_work_slot');work=slot_header(raw);obj.update(decode_status='DECODED',header=work,existing_H3=safe(decode_h3(raw,shared)))
  else:result['work_slot']=dict(status='NOT_AVAILABLE',reason='slots64 has no slot64; no read')
  order=[]
  if prefix:
   raw,obj=own(0x526a0,prefix*4,kind='ORDER');order=list(struct.unpack('<'+'I'*prefix,raw));obj.update(decode_status='DECODED',values=order)
  centers={}
  for position,index in enumerate(order):
   row=dict(prefix_index=position,capture_index=index,valid=0<=index<candidates)
   if row['valid']:
    raw,obj=table(0x200,8,index,4096,8,'CAPTURE_center');row['external_center']=key(raw,0);obj.update(decode_status='DECODED',external_center=row['external_center']);centers[position]=row['external_center']
   else:row['guard_finding']='INVALID_ORDER_NO_CAPTURE_READ'
   result.setdefault('order_attribution',[]).append(row)
  if last is not None:
   raw,obj=table(layout.ROLE_ALTERNATIVES,256,last,64,256,'last_ALT_pair');alts=[]
   for alternative in range(2):
    part=raw[alternative*128:(alternative+1)*128];count=integer(part,8);ready=integer(part,0)
    row=dict(alternative=alternative,ready=ready,role=integer(part,4),count=count,prefix=integer(part,12),SCIreason=integer(part,56),conditions=integer(part,64),phase_status='READY_DECLARED' if ready==1 else 'NOT_PROVEN_REACHED')
    if ready==1:
     keys=[key(part,16+n*8) for n in range(count)] if 4<=count<=5 else []
     row.update(keys=keys,structurally_consistent=count==len(keys) and len(set(keys))==count and all(map(canonical,keys)) and row['prefix']==last and row['role']==alternative+1 and count==(5 if alternative==0 else 4))
     if alternative==1:
      sci=results[last];open_count=integer(sci,16);indices=[integer(sci,28+4*n) for n in range(3)]
      valid=0<=open_count<=20 and len(set(indices))==3 and all(0<=n<open_count for n in indices)
      expected=[key(sci,116)]+[key(sci,128+n*96) for n in indices] if valid else None
      row.update(SCI_selected_indices_valid=valid,SCI_canonical_keys_match=keys==expected if valid else None,SCI_reason_conditions_match=(row['SCIreason'],row['conditions'])==(integer(sci,4),integer(sci,12)))
    alts.append(row)
   obj.update(decode_status='DECODED',alternatives=alts)
  result['original_indices_reproduced']=(earlier,last,slots)==(0,3,2)
  result['external_attribution']=dict(slot0_matches_CAPTURE=key(slot0,0)==centers[earlier] if earlier in centers else None,last_external_center=centers.get(last),work_external_matches_CAPTURE=tuple(work['external_center'])==centers[last] if work is not None and work['prepared']==1 and last in centers else None,work_external_phase_status='NOT_WRITTEN_UNTIL_CHOOSE_AND_CANONICAL_COMMIT',canonical_and_external_are_distinct_coordinate_systems=True)
  result['next_ORDER_guard']=dict(prefix_index=classified,status='NO_NEXT_PREFIX' if classified==prefix else 'VALID' if 0<=order[classified]<candidates else 'INVALID_ORDER_BEFORE_NEXT_CLASSIFICATION',branch_execution_proven=False)
  last_header=science(results[last])['header'] if last is not None else None
  result['last_SCI_guard']=dict(header=last_header,SCI_calls_match_classified=shared['SCI_calls']==classified,invocation_attribution_status='ALL_CLASSIFIED_CENTERS_ENTERED_SCI' if shared['SCI_calls']==classified and classified>0 else 'NOT_PROVEN_LAST_CENTER_ENTERED_SCI',possible_native_coverage_guard='200dcd0d..200dcd17' if last_header and last_header['coverage']!=1 and shared['SCI_calls']==classified else None,exact_failure_branch_proven=False,getter_cause_proven=False)
  result['main_questions']=dict(earlier_current_food=result['earlier_science_example']['status'],failure_branch='RAW_ATTRIBUTION_ONLY_EXACT_BRANCH_NOT_PROVEN')
 except Exception as error:result.update(attribution_status='INSUFFICIENT_EVIDENCE',error=type(error).__name__+': '+str(error),usable_diagnostic_evidence=False)
 return safe(result)
