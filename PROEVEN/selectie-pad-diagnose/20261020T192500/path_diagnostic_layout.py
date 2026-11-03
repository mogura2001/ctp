"""SELECT25 own transient appendix; all offsets record-relative DWORDs."""
PLAN_SIZE=0x79800
GENERATION_OFFSET=0x79800
RECORD_OFFSET=0x79804
RECORD_SIZE=256
STATE_SIZE=0x79904
FIELDS=dict(valid=0,schema=4,size=8,edge=12,reached=16,owner=20,generation=24,civ=28,plan_identity=32,
 select_call=36,select_return_site=40,cache_call=44,cache_return_site=48,direct_call=52,direct_return_site=56,invocation=60,
 query=64,slot=68,prefix=72,role=76,departure=80,rawID=84,kind=88,type=92,source=96,destination=104,
 native_EAX=112,capacity=116,count=120,pointer=124,pointer_end=128,bounds=132,canary1=136,canary2=140,postcontext=144,
 first_entry=148,last_entry=152,first_actual=156,source_expected=164,last_actual=172,destination_expected=180,
 first_conversion=188,source_conversion=192,last_conversion=196,destination_conversion=200,direct_return=204,cache_return=208,selection_return=212)
PAIRS={'source','destination','first_actual','source_expected','last_actual','destination_expected'}
BRANCHES=[(1,0xdc3f8,'postcontext_nonzero'),(2,0xdc408,'canary1_mismatch'),(3,0xdc418,'canary2_mismatch'),(4,0xdc428,'native_EAX_not1'),(5,0xdc436,'pointer_null'),(6,0xdc448,'count_lt1'),(7,0xdc460,'count_gt_capacity'),(8,0xdc46b,'pointer_end_overflow'),(9,0xdc483,'first_conversion0'),(10,0xdc49e,'source_conversion0'),(11,0xdc4b0,'first_dword0_mismatch'),(12,0xdc4c2,'first_dword4_mismatch'),(13,0xdc4e9,'last_conversion0'),(14,0xdc504,'destination_conversion0'),(15,0xdc516,'last_dword0_mismatch'),(16,0xdc528,'last_dword4_mismatch')]
REACHED=dict(callbinding=0,source_destination=1,native_return=2,postcontext=3,canary1=4,canary2=5,raw_return_guard=6,pointer=7,count_min=8,capacity=9,overflow=10,first_conversion=11,source_conversion=12,last_conversion=13,destination_conversion=14,first_compare=15,last_compare=16,direct_return=17,cache_return=18,selection_return=19)
def required_mask(edge,propagation=True):
 """Exact sequential guard reach; shared compare bits cover both DWORDs."""
 if not 1<=edge<=16:raise ValueError('edge outside fixed sixteen landings')
 bits=set(range(4))
 for first,bit in ((2,4),(3,5),(4,6),(5,7),(6,8),(7,9),(8,10),(9,11),(10,12),(11,15),(13,13),(14,14),(15,16)):
  if edge>=first:bits.add(bit)
 if propagation:bits.update((17,18,19))
 return sum(1<<bit for bit in bits)
def validate():
 used=set()
 for name,off in FIELDS.items():
  span=set(range(off,off+(8 if name in PAIRS else 4)))
  assert not used&span and 0<=off and max(span)<216,name;used|=span
 assert used==set(range(216)) and RECORD_OFFSET==GENERATION_OFFSET+4 and RECORD_OFFSET+RECORD_SIZE==STATE_SIZE
 assert PLAN_SIZE==GENERATION_OFFSET and len(BRANCHES)==16 and [x[0] for x in BRANCHES]==list(range(1,17))
 return True
validate()
