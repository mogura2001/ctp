"""Offline-only reader package preparation; never imports/runs the live reader."""
from pathlib import Path
import ast, difflib, hashlib, json, shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'PROEVEN/u30-type10/20261015T194300'
HOST=HERE/'host1'
HOST.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def copy(src,dst):
    if dst.exists():raise ValueError('Existing package file: '+str(dst))
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
for name in ('candidate-manifest.json','preparation-manifest.json'):
    copy(SOURCE/name,HERE/name)
for name in ('original_core.py','participants.json'):
    copy(SOURCE/'host1'/name,HOST/name)
copy(ROOT/'PROEVEN/production-h3/layout.py',HOST/'h3_layout.py')
for arm in ('baseline','variant'):
    rel=Path('candidate')/arm/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll'
    copy(SOURCE/'host1'/rel,HOST/rel)
old=(SOURCE/'host1/Lees-Uitbreiding.py').read_text('utf-8')
assert sha(SOURCE/'host1/Lees-Uitbreiding.py')=='366d16d43d3df71da84d9e45db79efebbbb529282de0eb8c699c6ab8652fe1cc'
new=old.replace('import time\n','import time\nfrom h3_layout import HEADER, RESULT_SIZE, H2_RESULT_OFFSET, H2_ENTRY_OFFSET, H2_ENTRY_STRIDE, MAX_ENTRIES\n',1)
needle="        binding['shared_plan_rva']=int(manifest['components']['state_rva'],16)"
replacement=needle+"\n        state_size=manifest['components']['state_size']\n        if binding['shared_plan_rva']!=0xdd000 or state_size!=0x54804:raise ValueError('Exact reason23 own-state layout changed')\n        if not 0x40600+1152<=state_size or binding['shared_plan_rva']+state_size>binding['ai']['size']:raise ValueError('Own slot outside bound AI state/module')\n        state_sections=[s for s in cp.sections if s.VirtualAddress==binding['shared_plan_rva'] and s.Misc_VirtualSize==state_size]\n        if len(state_sections)!=1:raise ValueError('Exact own state section missing')\n        binding['shared_plan_size']=state_size"
assert new.count(needle)==1;new=new.replace(needle,replacement)
new=new.replace('classified=220)','classified=220,candidates=68,slots=80,h3calls=128)',1)
needle="        shared={key:i32(ptr+off) for key,off in fields.items()}"
replacement=needle+"\n        if binding['shared_plan_rva']!=0xdd000 or binding['shared_plan_size']!=0x54804 or 0x40600+1152>binding['shared_plan_size'] or binding['shared_plan_rva']+0x40600+1152>binding['ai']['size']:raise ValueError('Own slot read outside exact bound state/module')\n        slot=read(checked(ptr,0x40600),1152)\n        shared['slot0']=decode_slot0(slot,shared)"
assert new.count(needle)==1;new=new.replace(needle,replacement)
# Preserve one shared_state() call per snapshot after native observation as before.
# The pre-existing intermediate call supplies type identity; it must not add a second slot read.
new=new.replace('    t=None;shared=shared_state()','    t=None;shared=shared_state()',1)
new=new.replace('    return result,shared_state()','    return result,shared',1)
decoder='''
def decode_slot0(slot,shared):
    """Decode only own bytes using the existing H3 layout; never follow pointers."""
    if len(slot)!=1152 or RESULT_SIZE!=1024:raise ValueError('Exact slot/H3 extent required')
    h3=slot[128:1152]
    formats={4:'<i',8:'<q'}
    raw={key:(h3[off:off+size].hex() if key=='canonical_center' else struct.unpack_from('<d' if key=='actual_rations_double' else formats[size],h3,off)[0]) for key,(off,size) in HEADER.items()}
    # Preserve double bits as rawhex too; invalid/nonfinite values never affect JSON equality.
    raw['actual_rations_double']=h3[24:32].hex()
    h2=dict(zip(('status','reason','count','mountains'),struct.unpack_from('<4i',h3,H2_RESULT_OFFSET)))
    tied=shared['reason']==23 and shared['classified']==1 and shared['h3calls']==1 and shared['slots']==0
    unknown='UNKNOWN_NOT_REACHED_OR_INCOMPLETE'
    observed={key:unknown for key in raw}
    observed.update(status=raw['status'],reason=raw['reason'])
    current=raw['model_id']==1 and not (raw['status']==0 and raw['reason']==14)
    h2_reached=current and (h2['status'] in (1,2) or 1<=h2['reason']<=7)
    if current:observed['model_id']=1
    if h2_reached:observed.update(h2_status=raw['h2_status'],open_count=raw['open_count'])
    if current and (raw['status'] in (1,2) or raw['reason'] in (12,13)) and h2['status']==2:
        for key in ('actual_stand','actual_rations_double','demand_i64'):observed[key]=raw[key]
    if current and raw['center_conditions']==1:
        for key in ('canonical_center','center_conditions','center_food_i64','city_bonus_i64'):observed[key]=raw[key]
    if current and raw['reason']==13:observed['unsupported_entry_mask']=raw['unsupported_entry_mask']
    indices=[raw[key] for key in ('mountain1_index','mountain2_index','mountain3_index','food_index')]
    count=raw['open_count'];valid_count=0<=count<=MAX_ENTRIES and h2['count']==count
    valid_indices=raw['status']==2 and valid_count and len(set(indices))==4 and all(0<=i<count for i in indices)
    entries=unknown
    if current and h2['status'] in (1,2) and 0<=h2['count']<=MAX_ENTRIES:
        entries=[dict(index=i,position_hex=h3[H2_RESULT_OFFSET+H2_ENTRY_OFFSET+i*H2_ENTRY_STRIDE:H2_RESULT_OFFSET+H2_ENTRY_OFFSET+i*H2_ENTRY_STRIDE+8].hex(),terrain=struct.unpack_from('<i',h3,H2_RESULT_OFFSET+H2_ENTRY_OFFSET+i*H2_ENTRY_STRIDE+8)[0]) for i in range(h2['count'])]
    if raw['status']==2 and current:
        for key in raw:observed[key]=raw[key]
    if not tied:
        attribution='UNKNOWN_FIRSTCALL_PASS_PATTERN'
    elif raw['status']==0 and raw['reason']==14:attribution='H3_HOST_FAILED_BEFORE_CURRENT_MODEL_LEAF_UNKNOWN'
    elif raw['status']==0 and raw['reason'] in (10,11,12,13):attribution={10:'CAPACITY_CHAIN_LEAF_MAY_REMAIN_UNKNOWN',11:'WGF_PARTIAL_WRITES_ONLY',12:'CENTERFOOD_OR_ARITHMETIC_LEAF_UNKNOWN',13:'UNSUPPORTED_ENTRIES_LEAF_UNKNOWN'}[raw['reason']]
    elif raw['status']==2 and current and valid_indices:attribution='SUPPORTED_RESULT_KEY_INVARIANT_QUESTION_REMAINS'
    else:attribution='INCONSISTENT_OBSERVATION_NO_CERTIFICATE'
    if not tied:
        observed={key:unknown for key in raw};entries=unknown;valid_indices=False
    return dict(rawhex=slot.hex(),h3_raw=raw,h2_raw=h2,h3_observed=observed,h2_observed=h2 if tied and h2_reached else unknown,h2_entries=entries,indices_valid=valid_indices,firstcall_attribution=attribution,firstcall_pattern=tied,only_last_shared_pass=True,other_civs_certified=False,raw_zero_is_not_measurement=True)

'''
new=new.replace('def native_expansion_state(',decoder+'def native_expansion_state(',1)
copyreader=HOST/'Lees-Uitbreiding.py';copyreader.write_text(new,encoding='utf-8')
(HERE/'reader.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='type10/host1/Lees-Uitbreiding.py',tofile='reason23/host1/Lees-Uitbreiding.py')),encoding='utf-8')
pins=[dict(path=p.name,sha256=sha(p)) for p in (copyreader,HOST/'original_core.py',HOST/'participants.json',HOST/'h3_layout.py')]
gate=dict(allowed=False,baseline_allowed=False,candidate_sha256='b6f272d2503edf5f1cf03f927ebd40ff5dd82b1a2c9d9c948beb4e7215baed62',state='PREPARED_OFFLINE_ONLY_UNUSED_GATE',scope='Root review required before any live action; one fixed T0/n/T1 arm only',sources=pins)
(HOST/'C10-ROOT-VRIJGAVE.json').write_text(json.dumps(gate,indent=2)+'\n',encoding='utf-8')
manifest=json.loads((HERE/'candidate-manifest.json').read_text())
assert manifest['components']['state_rva']=='0xdd000' and manifest['components']['state_size']==0x54804
assert sha(HERE/'candidate-manifest.json')=='fa5392c650bc2647d072a9e828256b2a07c43d40d7893dee1efd2276ef431e27'
assert sha(HOST/'candidate/variant/CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll')==gate['candidate_sha256']
provenance=dict(source_package=str(SOURCE.relative_to(ROOT)),source_reader_sha256=sha(SOURCE/'host1/Lees-Uitbreiding.py'),copied_layout_sha256=sha(HOST/'h3_layout.py'),candidate_unchanged=True,manifest_unchanged=True,no_build=True,no_live_read=True,no_install=True,no_game=True)
(HERE/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(reader_sha256=sha(copyreader),state_size=hex(manifest['components']['state_size']),slot_rva=hex(0xdd000+0x40600),gate_allowed=False)))
