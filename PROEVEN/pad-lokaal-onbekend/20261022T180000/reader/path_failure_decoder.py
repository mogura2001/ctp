"""Fixed own-state SELECT25 record. Never follows native path pointers."""
import struct
from path_diagnostic_layout import FIELDS,PAIRS,BRANCHES,REACHED,RECORD_OFFSET,RECORD_SIZE,STATE_SIZE,required_mask

def u(raw,off):return struct.unpack_from('<I',raw,off)[0]
def signed(n):return n if n<0x80000000 else n-0x100000000
def key(raw):
 x,y,z,padding=struct.unpack('<hhhH',raw)
 return dict(xyz=[x,y,z],padding_u16=padding,rawhex=raw.hex())

def stable_record(read,shared):
 """Two complete record reads, surrounded by complete binding samples.

 Stable twice is evidence of unchanged reads, never an atomic snapshot claim.
 read accepts only own Plan-relative offsets. Global generation is separate.
 """
 def binding():return (read(0,240),read(0x78800,8),read(0x79800,4))
 before=binding();valid_before=read(RECORD_OFFSET,4)
 first=read(RECORD_OFFSET,RECORD_SIZE);second=read(RECORD_OFFSET,RECORD_SIZE)
 valid_after=read(RECORD_OFFSET,4);after=binding()
 if any(len(x)!=n for sample in (before,after) for x,n in zip(sample,(240,8,4))):raise ValueError('incomplete path binding read')
 if len(first)!=256 or first!=second or valid_before!=valid_after or first[:4]!=valid_before or before!=after:raise ValueError('unstable complete path record/binding')
 for field,off in dict(status=0,reason=4,owner=8,civ=12,generation=32,scope=36,guard=40,raw_t=44,departures=76,slots=80,path_queries=84,context=212,classified=220,prefix_count=224).items():
  if signed(u(before[0],off))!=shared[field]:raise ValueError('record binding differs from shared '+field)
 if u(before[2],0)!=shared['generation']:raise ValueError('global generation mismatch')
 return first,before[1]

def decode_path(raw,shared,snapshot,read,plan_address,ai_base,manifest,manifest_sha256):
 if len(raw)!=256:raise ValueError('exact256-byte record required')
 fields={name:(raw[off:off+8] if name in PAIRS else u(raw,off)) for name,off in FIELDS.items()}
 f=fields;mask=f['reached'];seen=lambda name:bool(mask&(1<<REACHED[name]))
 result=dict(status='UNSELECTED_PATH_FAILURE_DIAGNOSTIC',selected=False,certified=False,gameplay_improvement_proven=False,rawhex=raw.hex(),raw_fields={k:v.hex() if isinstance(v,bytes) else v for k,v in f.items()},manifest_sha256=manifest_sha256,stable_complete_record_twice=True,atomic_snapshot_proven=False,usable_diagnostic_evidence=False,attribution_status='UNVALIDATED',external_path_xyz_read=False)
 field_bits=dict(native_EAX='native_return',capacity='native_return',count='native_return',pointer='native_return',postcontext='postcontext',canary1='canary1',canary2='canary2',pointer_end='overflow',bounds='overflow',first_entry='first_conversion',last_entry='last_conversion',first_actual='first_conversion',source_expected='source_conversion',last_actual='last_conversion',destination_expected='destination_conversion',first_conversion='first_conversion',source_conversion='source_conversion',last_conversion='last_conversion',destination_conversion='destination_conversion',direct_return='direct_return',cache_return='cache_return',selection_return='selection_return')
 field_bits.update({name:'callbinding' for name in ('owner','generation','civ','plan_identity','select_call','select_return_site','cache_call','cache_return_site','direct_call','direct_return_site','invocation')})
 field_bits.update({name:'source_destination' for name in ('slot','prefix','role','departure','rawID','kind','type','source','destination')})
 field_bits['query']='native_return'
 result['observed']={k:(key(v) if isinstance(v,bytes) else signed(v) if k in ('count','capacity') else v) if k not in field_bits or seen(field_bits[k]) else 'ONBEREIKT' for k,v in f.items()}
 try:
  if f['valid']!=1:
   result['attribution_status']=('NO_FAILURE_PUBLISHED' if not any(raw) else 'UNPUBLISHED_STAGING_RECORD') if f['valid']==0 else 'INVALID_VALID_MARKER';return result
  edge=f['edge']
  if f['schema']!=1 or f['size']!=256 or not 1<=edge<=16 or any(raw[216:]):raise ValueError('schema/size/edge/reserved')
  if mask!=required_mask(edge):raise ValueError('exact guard reached/propagation mask')
  if manifest['components']['state_size']!=STATE_SIZE or plan_address!=ai_base+int(manifest['components']['state_rva'],16):raise ValueError('manifest state/Plan binding')
  diag=manifest['path_diagnostic']
  if (diag['offset'],diag['size'],diag['schema'])!=(RECORD_OFFSET,256,1):raise ValueError('manifest diagnostic layout')
  owner,generation=struct.unpack('<2I',snapshot)
  if not (f['owner']==owner!=0 and f['generation']==generation==shared['generation']>0 and f['civ']==shared['civ'] and 1<=f['civ']<=31 and shared['owner'] in (0,owner) and f['plan_identity']==plan_address and f['invocation']>0):raise ValueError('owner/generation/civ/invocation/Plan')
  local=(f['direct_return'],f['cache_return'],f['selection_return'])==(4,4,1)
  if not (shared['status'] in ((4,5) if local else (0,5)) and shared['reason']==(0 if local else 25) and shared['scope']==0 and shared['guard']==0 and shared['context']==1 and shared['context_error']==0):raise ValueError('completed local/fallback pass context')
  for pair,field in [('finalize_selection','select'),('selection_cached','cache'),('cached_direct','direct')]:
   call=diag['calls'][pair]
   if (f[field+'_call'],f[field+'_return_site'])!=(call['call_rva'],call['return_rva']) or call['return_rva']!=call['call_rva']+5:raise ValueError('actual call/return pair '+pair)
  if not (1<=f['query']==shared['path_queries']<=128 and 0<=f['slot']<shared['slots']<=64 and 0<=f['departure']<shared['departures']<=32 and 0<=f['prefix']<shared['prefix_count']<=64 and f['prefix']<shared['classified'] and f['role'] in (1,2) and f['kind'] in (1,2,3,4) and f['type']==shared['raw_t']):raise ValueError('query/slot/source/role/prefix/type bounds')
  slot=read(0x40600+f['slot']*1152,1152);departure=read(0x18200+f['departure']*32,32)
  order=read(0x526a0,shared['slots']*4)
  if len(slot)!=1152 or len(departure)!=32 or len(order)!=shared['slots']*4:raise ValueError('incomplete bound own object')
  if sorted(struct.unpack('<'+'I'*shared['slots'],order))!=list(range(shared['slots'])):raise ValueError('post-order slot permutation')
  if (u(slot,76),u(slot,72),u(departure,0),u(departure,4),slot[:8],departure[8:16])!=(f['prefix'],f['role'],f['rawID'],f['kind'],f['destination'],f['source']):raise ValueError('current source/destination binding')
  if not local and (f['direct_return'],f['cache_return'],f['selection_return'])!=(0,0,0):raise ValueError('direct0/cache0/select25 propagation')
  if local and not (edge==4 and f['native_EAX']==f['capacity']==f['count']==f['pointer']==f['postcontext']==0 and f['canary1']==0x3456ab89 and f['canary2']==0x4567bc90):raise ValueError('clean local4 operands')
  predicates={1:f['postcontext']!=0,2:f['canary1']!=0x3456ab89,3:f['canary2']!=0x4567bc90,4:f['native_EAX']!=1,5:f['pointer']==0,6:signed(f['count'])<1,7:signed(f['count'])>signed(f['capacity']),8:f['pointer']+f['count']*8>0xffffffff,9:f['first_conversion']==0,10:f['source_conversion']==0,11:f['first_actual'][:4]!=f['source_expected'][:4],12:f['first_actual'][4:]!=f['source_expected'][4:],13:f['last_conversion']==0,14:f['destination_conversion']==0,15:f['last_actual'][:4]!=f['destination_expected'][:4],16:f['last_actual'][4:]!=f['destination_expected'][4:]}
  if not predicates[edge] or any(predicates[n] for n in range(1,edge)):raise ValueError('first failed original guard does not match stored operands')
  if edge>=7 and not 1<=f['count']<=4096:raise ValueError('precapacity querybudget bypass')
  if edge>=8 and (f['pointer_end']!=(f['pointer']+f['count']*8)&0xffffffff or f['bounds']!=int(predicates[8])):raise ValueError('pointer bounds operand')
  if edge>=9 and f['first_entry']!=f['pointer']:raise ValueError('first entry address')
  if edge>=13 and f['last_entry']!=(f['pointer_end']-8)&0xffffffff:raise ValueError('last entry address')
  for name,conversion in [('first_actual','first_conversion'),('source_expected','source_conversion'),('last_actual','last_conversion'),('destination_expected','destination_conversion')]:
   observed=result['observed'][name]
   if observed!='ONBEREIKT':
    if f[conversion] not in (0,1):raise ValueError('canonical conversion outside existing0/1 contract')
    observed['canonical_key_valid']=f[conversion]==1;observed['conversion_return']=f[conversion]
  result.update(attribution_status='BOUND_COMPLETE_GUARD_OPERANDS',usable_diagnostic_evidence=True,edge_id=edge,branch_name=BRANCHES[edge-1][2],parent_edge_rva=hex(BRANCHES[edge-1][1]),guard_attribution_proven=True,native_output_slots_are_observed_not_write_proof=True,order_phase='SLOT_ORDER_PLUS_UNATTRIBUTABLE_REMAINDER',prefix_CAPTURE_claims_allowed=False)
  if local:result.update(status='LOCAL_UNKNOWN_PAIR',attribution_status='LOCAL_UNKNOWN_PAIR',branch_name='clean_native0_local_unknown',selected=False,certified=False,no_route_proven=False)
 except Exception as error:result.update(attribution_status='INSUFFICIENT_EVIDENCE',error=type(error).__name__+': '+str(error))
 return result
