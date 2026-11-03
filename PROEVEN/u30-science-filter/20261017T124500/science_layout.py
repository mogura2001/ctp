"""Transient ScienceResult schema only; no game/save schema or policy writes."""
SCIENCE_CREDIT_ENABLED = True
RESULT_SIZE = 2048
HEADER_SIZE = 128
TILE_OFFSET = 128
TILE_STRIDE = 96
MAX_TILES = 20
SCRATCH_SIZE = 4096
KERNEL_FRAME_SIZE = 548 # +12 saved-register bytes covers EBP-560 exactly
H2_SCRATCH = 0
RAWFOOD_SCRATCH = 256
HOST_SCRATCH = 296
SCENARIO_SCRATCH = 320
CURRENT_PLAN_SIZE = 0x54800
SCIENCE_RESULTS = 0x54800
ROLE_ALTERNATIVES = 0x74800
SCIENCE_SCRATCH = 0x78800
PLAN_SIZE = 0x79800
STATUS_UNKNOWN = 0
STATUS_NO_NOW = 1
STATUS_NOW = 2
STATUS_STRUCTURAL_POTENTIAL = 3
STATUS_PENDING_GROWTH = 4
ZERO_NEW_CITY_MODIFIERS = 1
CONDITIONAL_CRIME = 2
HEADER = {
 'location_state':(0,4), 'reason':(4,4), 'model':(8,4), 'conditions':(12,4),
 'open_count':(16,4), 'potential_count':(20,4), 'certifiable_count':(24,4),
 'selected0':(28,4), 'selected1':(32,4), 'selected2':(36,4),
 'current_unknownmask':(40,4), 'spatial_unknownmask':(44,4),
 'spatial_pendingmask':(48,4), 'development_unknownmask':(52,4),
 'ration_stand':(56,4), 'development_state':(60,4), 'actual_R':(64,8),
 'center_food_i64':(72,8), 'S3_current_i64':(80,8), 'margin3_x2_i64':(88,8),
 'crime_numerator_i64':(96,8), 'crime_denominator_i64':(104,8),
 'coverage':(112,4), 'center_key':(116,8), 'h2_status':(124,4),
}
TILE = {
 'canonical_key':(0,8), 'external_MapPoint':(8,8), 'current_food_i32':(16,4),
 'structure_flags':(20,4), 'raw_spatial':(24,4), 'spatial_reason':(28,4),
 'development':(32,64),
}
STRUCT_MAIN_IRR2 = 1
STRUCT_EFFECTIVE_POSITIVE_IRR2 = 2
STRUCT_CURRENT_LEVEL_PRESENT = 4
STRUCT_CERTIFIABLE = 8
STRUCT_CANONICAL_CURRENT_VALID = 16
STRUCT_FUTURE_VALID = 32
# Summary applies to selected CURRENT indices only. Per-tile states retain
# development_tile's enum; mixed/pending summaries are not building permits.
DEV_SUMMARY_UNKNOWN = 0
DEV_SUMMARY_PENDING = 1
DEV_SUMMARY_READY_NOT_BUILT = 3
DEV_SUMMARY_ALREADY_PRESENT = 4
DEV_SUMMARY_MIXED_PRESENT_READY = 5
# Private invocation scratch, not persisted in ScienceResult or active Plan.
STACK = dict(x87=(-144,108), rawfood=(-184,40), host=(-208,24),
 h2=(-480,256), loop=(-220,4), dedup=(-224,4), scenario=(-248,24),
 terrain=(-512,4), target=(-524,12), future_selected=(-560,12),
 summary_bits=(-544,4), scenario_positive=(-540,4))
QUERY_BUDGETS = dict(science_calls=64, tiles=1280, spatial_calls=1280,
 improvement_calls=3840, primary_food_readers=1344,
 development_food_readers=1280, total_food_readers=2624)
def disjoint(fields, limit):
 used=set()
 for offset,size in fields.values():
  extent=set(range(offset,offset+size))
  assert 0<=offset and offset+size<=limit and not used & extent
  used |= extent
disjoint(HEADER, HEADER_SIZE)
disjoint(TILE, TILE_STRIDE)
assert HEADER_SIZE+MAX_TILES*TILE_STRIDE == RESULT_SIZE
assert SCIENCE_RESULTS+64*RESULT_SIZE == ROLE_ALTERNATIVES
assert ROLE_ALTERNATIVES+64*2*128 == SCIENCE_SCRATCH
assert SCIENCE_SCRATCH+SCRATCH_SIZE == PLAN_SIZE
assert SCENARIO_SCRATCH+4*32 <= SCRATCH_SIZE
assert HOST_SCRATCH+24 <= SCENARIO_SCRATCH
# scenario reuses H2 storage only after enumeration is copied to tile rows.
assert all(-KERNEL_FRAME_SIZE-12 <= off and off+size <= -16 for off,size in STACK.values())
assert not set(range(-560,-548)) & set(range(-524,-512))
