"""Decode only 236 caller-owned bytes. Raw is retained even when untrusted."""
from pathlib import Path
import hashlib,struct,sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from food_diagnostic_layout import FIELDS,BRANCHES,RECORD_OFFSET,RECORD_SIZE,required_bits
def decode_failure(raw,shared,plan_address,manifest_sha256,partial=None):
 if len(raw)!=RECORD_SIZE:raise ValueError('exact 236-byte own record required')
 decoded={name:struct.unpack_from('<'+fmt,raw,off)[0] for name,(off,fmt,bit) in FIELDS.items()}
 bits=decoded['reached_lo']|(decoded['reached_hi']<<32)
 serial={name:(value.hex() if isinstance(value,bytes) else value) for name,value in decoded.items()}
 result=dict(status='UNSELECTED_FOODREADER_FAILURE_DIAGNOSTIC',selected=False,certified=False,gameplay_improvement_proven=False,offset=RECORD_OFFSET,length=RECORD_SIZE,rawhex=raw.hex(),raw_fields=serial,decode_status='RAW_DECODED',attribution_status='UNVALIDATED',usable_diagnostic_evidence=False,manifest_sha256=manifest_sha256,decoder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),layout_sha256=hashlib.sha256((Path(__file__).resolve().parent.parent/'food_diagnostic_layout.py').read_bytes()).hexdigest(),observed={name:(serial[name] if bit is not None and bits&(1<<bit) else 'ONBEREIKT') for name,(off,fmt,bit) in FIELDS.items()})
 try:
  if shared['generation']==0:result['attribution_status']='NOT_INITIALIZED';return result
  if decoded['valid']!=1:
   result['attribution_status']='NO_FAILURE_PUBLISHED' if not any(raw) else 'INVALID_OR_PARTIAL_RAW_RECORD';return result
  if decoded['schema']!=1 or not 1<=decoded['branch_id']<=37 or decoded['callkind'] not in (1,2) or bits>>44:raise ValueError('schema/id/callkind/reserved reachedbits')
  branch=decoded['branch_id'];missing=required_bits(branch)-{i for i in range(44) if bits&(1<<i)}
  result['missing_required_reachedbits']=sorted(missing)
  if missing:raise ValueError('required guard operands ONBEREIKT')
  if not (decoded['owner'] and decoded['generation']==shared['generation']>0 and shared['owner'] in (0,decoded['owner']) and shared['context']==1 and shared['context_error']==0 and 0<=decoded['prefix']<shared['prefix_count']<=64 and decoded['prefix']<shared['classified'] and 1<=decoded['ordinal']<=shared['SCI_primary_food']<=1344):raise ValueError('last-pass owner/generation/prefix/ordinal context')
  if not partial or not partial.get('usable_diagnostic_evidence'):raise ValueError('separate complete bounded last-pass binding missing')
  snapshots=[o for o in partial['objects'] if o['kind']=='owner_generation_snapshot']
  if len(snapshots)!=1 or (snapshots[0]['owner'],snapshots[0]['generation'])!=(decoded['owner'],decoded['generation']):raise ValueError('owner/generation scratch mismatch')
  if decoded['bindingpointer']!=plan_address+144 or decoded['world']<0x10000 or decoded['outpointer']<0x10000:raise ValueError('native reader argument binding')
  external=struct.unpack('<hhhH',decoded['external']);internal=struct.unpack('<hhhH',decoded['internal'])
  if decoded['callkind']==1:
   if decoded['prefix']!=shared['classified']-1 or shared['SCI_calls']!=shared['classified']:raise ValueError('center failure last SCI attribution')
   centers=[o for o in partial.get('order_attribution',[]) if o['prefix_index']==decoded['prefix'] and o['valid']]
   if len(centers)!=1 or tuple(centers[0]['external_center'])!=external[:3]:raise ValueError('center external ORDER/CAPTURE mismatch')
  a=decoded['guard_a'];b=decoded['guard_b'];signed=lambda n:n if n<0x80000000 else n-0x100000000
  predicates={1:a!=0,2:a>=b,3:a>=b,9:a!=0,10:a!=0,11:a>23,12:a==13,13:a==18,14:a==23,22:a==0,23:a>=b,24:a==0,25:a>4,31:b!=0,32:signed(a)<0,33:a==0,34:a!=b,36:b!=0,37:signed(a)<0}
  for i,value in ((15,10),(16,11),(17,12),(18,14),(19,15),(20,16),(21,17)):predicates[i]=a==value and decoded['callkind']==1
  for i in range(4,9):predicates[i]=a==0 and decoded['pointer_value']==0
  for i in (26,27,28,29,30,35):predicates[i]=bool(decoded['failure_eflags']&0x800)
  if not predicates[branch]:raise ValueError('stored operands do not satisfy original guard')
  flags=decoded['failure_eflags'];zf=bool(flags&0x40);sf=bool(flags&0x80);cf=bool(flags&1);of=bool(flags&0x800)
  flag_predicates={1:not zf,2:not cf,3:not cf,9:not zf,10:not zf,11:not cf and not zf,22:zf,23:not cf,24:zf,25:not cf and not zf,31:not zf,32:sf,33:zf,34:not zf,36:not zf,37:sf}
  for i in list(range(4,9))+list(range(12,22)):flag_predicates[i]=zf
  for i in (26,27,28,29,30,35):flag_predicates[i]=of
  if not flag_predicates[branch]:raise ValueError('preserved failure EFLAGS do not take original branch')
  if branch==1 and signed(a)!=internal[2]:raise ValueError('z guard operand mismatch')
  if branch in (2,3) and (signed(a),b)!=(internal[branch-2],decoded['width' if branch==2 else 'height']):raise ValueError('dimension guard operand mismatch')
  if branch==9 and a!=decoded['cityhandle']:raise ValueError('cityhandle operand mismatch')
  if branch==10 and signed(a)!=decoded['unitcount']:raise ValueError('unitcount operand mismatch')
  if 11<=branch<=21 and signed(a)!=decoded['terrain']:raise ValueError('terrain operand mismatch')
  if branch==23 and (signed(a),signed(b))!=(decoded['terrain'],decoded['terrain_count']):raise ValueError('terrain range operand mismatch')
  if (branch==25 and a!=decoded['rawgood']) or (bits&(1<<18) and decoded['rawgood']!=((decoded['cellflags']>>6)&7)):raise ValueError('raw goodcode mismatch')
  if branch in (26,27,28,29,30,35):
   expected=branch-25 if branch<=30 else 6
   if decoded['addend_stage']!=expected:raise ValueError('overflow stage mismatch')
  if branch>=33 and (decoded['native_called']!=1 or decoded['output_before']!=-1):raise ValueError('native call/sentinel contract')
  if (branch==33 and decoded['native_return']!=0) or (branch==34 and (signed(a),signed(b))!=(decoded['output_after'],decoded['sum_after'])):raise ValueError('native guard operand mismatch')
  _,parent,name=BRANCHES[branch-1]
  result.update(attribution_status='BOUND_COMPLETE_GUARD_OPERANDS',usable_diagnostic_evidence=True,branch_name=name,parent_va_provenance=hex(0x200d0000+parent),external=external,internal=internal,callkind_name='SCI_CENTER' if decoded['callkind']==1 else 'SCI_PRIMARY_TILE',conditional_reader_scope_only=True,exact_native_guard_identified=True,gameplay_fix_proven=False)
  if bits&(1<<17):
   flags=decoded['cellflags'];result['decoded_flags']=dict(road_level=flags&3,irrigation_level=(flags>>2)&3,mine_level=(flags>>4)&3,river_present=bool(flags&0x800),canal_present=bool(flags&0x200),raw_goodcode=(flags>>6)&7)
 except Exception as error:result.update(attribution_status='INSUFFICIENT_EVIDENCE',error=type(error).__name__+': '+str(error))
 return result
