"""Read-only branch controls of original population/scientist instructions.

Synthetic records and cities. Tile/specialist action callbacks are recorded mocks;
no engine turn, real citizen placement, FLI evaluation or gameplay session.
"""
from pathlib import Path
import sys, struct, hashlib, json
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_ESP, UC_X86_REG_EIP
PE=[]
for name,digest in [
 ('CTP-og/ctp_program/ctp/civctp.exe','b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'),
 ('CTP-og/ctp_program/ctp/dll/ai/robotcom.dll','3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44')]:
 path=ROOT/name
 assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
 PE.append(pefile.PE(str(path)))
M=0x30000000
CITY,AIMAIN,POP,PV,WRLD,WV,POINT,TILES,TILE,BONUS,DB,RECORDS,PLAYER,PLAYERS,LIST,OUTPUT=[M+x for x in
 (0x1000,0x2000,0x3000,0x3100,0x4000,0x4100,0x5000,0x6000,0x7000,0x8000,0x9000,0xa000,0xb000,0xc000,0xd000,0xe000)]
STOP,STACK,HOOK=M+0xff000,M+0xe0000,M+0x20000
checks=[]

def integer(u,a,v=None):
 if v is None:return struct.unpack('<I',u.mem_read(a,4))[0]
 u.mem_write(a,struct.pack('<I',v&0xffffffff))

def real(u,a,v=None):
 if v is None:return struct.unpack('<d',u.mem_read(a,8))[0]
 u.mem_write(a,struct.pack('<d',v))

def fixture():
 u=Uc(UC_ARCH_X86,UC_MODE_32)
 for p in PE:
  base=p.OPTIONAL_HEADER.ImageBase
  u.mem_map(base,(p.OPTIONAL_HEADER.SizeOfImage+4095)&~4095)
  u.mem_write(base,p.get_memory_mapped_image())
 u.mem_map(M,0x100000)
 integer(u,CITY+0x210,POINT);integer(u,CITY+0x21c,BONUS)
 integer(u,AIMAIN+0x40,POP);integer(u,POP,PV)
 integer(u,AIMAIN+0x30,WRLD);integer(u,WRLD,WV)
 integer(u,TILES,TILE)
 return u

def execute(u,address,args,receiver=CITY,capture=False):
 integer(u,STACK,STOP)
 for i,a in enumerate(args):integer(u,STACK+4+i*4,a)
 u.reg_write(UC_X86_REG_ESP,STACK);u.reg_write(UC_X86_REG_ECX,receiver)
 end=STOP
 if capture:
  u.mem_write(STOP,b'\xdd\x1d'+struct.pack('<I',OUTPUT));end=STOP+6
 u.emu_start(address,end,count=100000)
 assert u.reg_read(UC_X86_REG_EIP)==end
 return real(u,OUTPUT) if capture else u.reg_read(UC_X86_REG_EAX)

def record(label,got,expected,mocks=()):
 checks.append(dict(label=label,got=got,expected=expected,passed=got==expected,external_mocks=list(mocks)))

# Actual original GetProductionBonus executes; no callback stub here.
for label,food,prod,gold,weight_f,weight_p,weight_g,bonus,extra in [
 ('tile_weighted_sum',10,20,5,2,3,4,0,7),
 ('tile_gold_bonus',10,20,5,2,3,4,.5,7),
 ('tile_food_zero_weight',30,10,0,0,2,1,0,0),
 ('tile_negative_extra',5,5,5,1,1,1,0,-20)]:
 u=fixture()
 for off,val in ((8,food),(16,prod),(24,gold),(32,extra)):real(u,TILE+off,val)
 real(u,BONUS+4*8,bonus)
 args=[TILES]
 for f in (weight_f,weight_p,weight_g):args.extend(struct.unpack('<II',struct.pack('<d',f)))
 execute(u,0x20021ac0,args)
 record(label,real(u,TILE),food*weight_f+prod*weight_p+gold*(1+bonus)*weight_g+extra)

# Original best-specialist writer and PopDB getter, including government mask.
for label,changes,expected in [
 ('best_science_selects_highest_bonus',{},1),
 ('required_building_absent',{('record',1,0x60):5},0),
 ('required_building_present',{('record',1,0x60):5,('city',0,0x48):32},1),
 ('minimum_size_blocks',{('record',1,0x58):5},0),
 ('maximum_size_blocks',{('record',1,0x5c):3},0),
 ('government_mask_blocks',{('record',1,0x68):2},0),
 ('slave_flag_blocks',{('record',1,0x64):0x30},0),
 ('not_city_specialist_blocks',{('record',1,0x64):0},0),
 ('equal_science_keeps_first',{('record',1,0x4c):10},0)]:
 u=fixture();integer(u,0xa7dd44,DB);integer(u,DB,2);integer(u,DB+8,RECORDS)
 integer(u,0xa7dd80,PLAYERS);integer(u,PLAYERS,PLAYER)
 integer(u,CITY+0x58c,4)
 for i in (0,1):
  r=RECORDS+i*0x88
  for off,v in ((0x58,-1),(0x5c,-1),(0x60,-1),(0x64,0x10),(0x68,1),(0x4c,10+10*i)):integer(u,r+off,v)
 for (kind,index,offset),v in changes.items():integer(u,(RECORDS+index*0x88 if kind=='record' else CITY)+offset,v)
 execute(u,0x49e940,[])
 record(label,integer(u,CITY+0x3f8),expected)

# Original SCIENCE_PER_POP aggregation; records and list are synthetic.
for label,mask,values,expected in [
 ('science_per_pop_one_building',1,[.5],.5),
 ('science_per_pop_two_buildings',3,[.5,.5],1),
 ('science_per_pop_ignores_absent',1,[.5,.5],.5),
 ('science_per_pop_no_buildings',0,[.5,.5],0)]:
 u=fixture();integer(u,DB+0xd8,len(values));integer(u,DB+0x1a0,LIST);integer(u,DB+8,RECORDS)
 for i,val in enumerate(values):integer(u,LIST+4*i,i);real(u,RECORDS+i*0x108+0xf0,val)
 result=execute(u,0x45e470,[mask,0],receiver=DB,capture=True)
 record(label,result,expected)

# Actual minimum-production selector; placement callback records chosen tile.
for label,current_prod,tile_data,expected in [
 ('minimum_production_skips_if_center_positive',5,[(10,0),(0,35)],'none'),
 ('minimum_production_selects_mountain',0,[(10,5),(0,35)],1),
 ('minimum_production_places_only_one',0,[(0,20),(0,35)],1),
 ('minimum_production_no_positive_candidate',0,[(0,0),(0,0)],'none')]:
 u=fixture();choices=[]
 for i,(f,p) in enumerate(tile_data):
  pos=TILE+0x80*i;integer(u,TILES+4*i,pos);real(u,pos+8,f);real(u,pos+16,p)
 pointers=[OUTPUT+4*i for i in range(4)]
 for pointer in pointers:integer(u,pointer,1)
 real(u,OUTPUT+0x100,current_prod)
 u.mem_write(0x20021500,b'\xc2\x20\x00')
 def minimum_callback(uc,address,size,data):
  if address==0x20021500:
   choices.append(integer(uc,uc.reg_read(UC_X86_REG_ESP)+8))
 u.hook_add(UC_HOOK_CODE,minimum_callback)
 execute(u,0x20021430,[AIMAIN,*pointers,4,TILES,OUTPUT+0x100])
 record(label,choices[0] if choices else 'none',expected,('PlaceACitizen recorder',))
 assert len(choices)<=1

# Actual DLL comparison/actions; callbacks only record chosen action.
for label,special,tile,type_id,z,has_tile,expected in [
 ('science_beats_tile',20,10,2,0,True,'specialist'),
 ('tie_keeps_tile',10,10,2,0,True,'tile'),
 ('tile_beats_science',5,10,2,0,True,'tile'),
 ('unavailable_specialist_keeps_tile',20,10,-1,0,True,'tile'),
 ('layer1_keeps_tile',20,10,2,1,True,'tile'),
 ('no_tile_selects_specialist',20,10,2,0,False,'specialist')]:
 u=fixture();actions=[]
 real(u,TILE,tile);u.mem_write(POINT+4,struct.pack('<h',z));integer(u,OUTPUT,0)
 if not has_tile:integer(u,TILES,0);integer(u,OUTPUT,20)
 for off,index,nargs in ((0x3c,0,5),(0x60,1,6)):
  integer(u,PV+off,HOOK+16*index);u.mem_write(HOOK+16*index,b'\xc2'+struct.pack('<H',nargs*4))
 for off,index in ((0xb8,2),(0xbc,3)):
  integer(u,WV+off,HOOK+16*index);u.mem_write(HOOK+16*index,b'\xc2\x0c\x00')
 def callback(uc,address,size,data):
  if address not in (HOOK,HOOK+16,HOOK+32,HOOK+48):return
  stack=uc.reg_read(UC_X86_REG_ESP)
  if address==HOOK:
   actions.append('specialist');integer(uc,integer(uc,stack+20),0)
  elif address==HOOK+16:
   actions.append('tile');integer(uc,integer(uc,stack+24),0);uc.reg_write(UC_X86_REG_EAX,1)
  else:integer(uc,integer(uc,stack+12),0)
 u.hook_add(UC_HOOK_CODE,callback)
 words=struct.unpack('<II',struct.pack('<d',special))
 execute(u,0x20021c00,[AIMAIN,0,*words,type_id,TILES,OUTPUT])
 record(label,actions[0] if actions else 'none',expected,('Population+3c/+60','World+b8/+bc'))

print(json.dumps(dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
 limitations=['Synthetic city/record inputs; no full parser, FLI, economy or game turn.',
              'Action callbacks record requests; they do not prove real engine placement.']),indent=2))
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
