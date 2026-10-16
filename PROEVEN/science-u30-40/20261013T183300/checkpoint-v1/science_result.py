"""Decode caller-owned saved ScienceResult bytes only; no RPM/GUI/process tools."""
import struct
from science_layout import HEADER, TILE, RESULT_SIZE, TILE_OFFSET, TILE_STRIDE
from development import DEV_TILE
LOCATION_NAMES={0:'UNKNOWN',1:'NO_CURRENT_NOW_SCENARIO',2:'NOW',
 3:'STRUCTURAL_POTENTIAL_SPATIAL_PENDING',4:'PENDING_GROWTH'}
DEVELOPMENT_NAMES={0:'UNKNOWN',1:'AVAILABILITY_PENDING',2:'PLACE_UNKNOWN',
 3:'READY_NOT_BUILT',4:'ALREADY_PRESENT'}
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
 return dict(header=header,location_name=LOCATION_NAMES.get(header['location_state'],'INVALID'),tiles=rows,science_credit_enabled=False,conditional_only=True,future_growth_calculation_implemented=False)
