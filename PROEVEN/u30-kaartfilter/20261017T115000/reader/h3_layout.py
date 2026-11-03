"""Own H3 caller-owned layout. No engine/save schema or model implementation."""
RESULT_SIZE=1024
MODEL_ZERO_NEW_CITY_MODIFIERS=1
MODE_SCORE_CURRENT=0
MODE_EXPLAIN_DEVELOPMENT=1
STATUS_UNKNOWN=0
STATUS_ASSESSED_NO_PLAN=1
STATUS_SUPPORTED_SCENARIO=2
HEADER={
 'status':(0,4),'reason':(4,4),'model_id':(8,4),'mode':(12,4),
 'actual_stand':(16,4),'actual_rations_double':(24,8),'demand_i64':(32,8),
 'center_food_i64':(40,8),'city_bonus_i64':(48,8),'S0_i64':(56,8),
 'margin0_i64':(64,8),'crime_numerator_i64':(72,8),'crime_denominator_i64':(80,8),
 'unsupported_entry_mask':(88,4),'h2_status':(92,4),'open_count':(96,4),
 'mountain1_index':(100,4),'mountain2_index':(104,4),'mountain3_index':(108,4),
 'food_index':(112,4),'canonical_center':(116,8),'center_conditions':(124,4),
}
H2_RESULT_OFFSET=128
H2_RESULT_SIZE=256
H2_ENTRY_OFFSET=16
H2_ENTRY_STRIDE=12
FOOD_ENTRY_OFFSET=384
FOOD_ENTRY_STRIDE=24
MAX_ENTRIES=20
FOOD_ENTRY={'status':(0,4),'current_food_i32':(4,4),'cellflags':(8,4),
 'terrain':(12,4),'selected_good_slot':(16,4),'current_minelevel':(20,4)}
DEVELOPMENT_OFFSET=864
DEVELOPMENT_SIZE=160
# A separate explanatory call fills this only after the current physical plan
# exists. No descriptor in this reserved range changes SCORE_CURRENT.
DEVELOPMENT={'status':(0,4),'reason':(4,4),'selector':(8,4),'availability_raw':(12,4),
 'position_predicate_raw':(16,4),'position_state_raw':(20,4),'target_present':(24,4),
 'food_delta_double':(32,8),'target_materials':(40,4),'target_time':(44,4),
 'pending_S_double':(48,8),'mine1_food_delta_double':(56,8),
 'mine2_food_delta_double':(64,8),'mine3_food_delta_double':(72,8),
 'pending_conditions':(80,4),'mine_conditions':(84,4)}
def disjoint(fields,limit):
    occupied=set()
    for offset,size in fields.values():
        extent=set(range(offset,offset+size));assert not occupied&extent
        assert 0<=offset and offset+size<=limit;occupied|=extent
disjoint(HEADER,128);disjoint(FOOD_ENTRY,FOOD_ENTRY_STRIDE);disjoint(DEVELOPMENT,DEVELOPMENT_SIZE)
assert H2_RESULT_OFFSET+H2_RESULT_SIZE==FOOD_ENTRY_OFFSET
assert FOOD_ENTRY_OFFSET+MAX_ENTRIES*FOOD_ENTRY_STRIDE==DEVELOPMENT_OFFSET
assert DEVELOPMENT_OFFSET+DEVELOPMENT_SIZE==RESULT_SIZE
assert H2_ENTRY_OFFSET+MAX_ENTRIES*H2_ENTRY_STRIDE==H2_RESULT_SIZE
