"""Small pure layout/AST check. Synthetic bytes are never actual game data."""
from pathlib import Path
import ast, hashlib, json, struct

HERE=Path(__file__).resolve().parent
HOST=HERE/'host1'
tree=ast.parse((HOST/'Lees-Uitbreiding.py').read_text('utf-8'))
layout={};exec(compile((HOST/'h3_layout.py').read_text('utf-8'),'copied existing H3 layout','exec'),layout)
env=dict(layout,struct=struct)
for name in ('decode_slot0','stable_sample'):
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    exec(compile(ast.Module(body=[node],type_ignores=[]),'pure AST function','exec'),env)
pattern=dict(reason=23,classified=1,h3calls=1,slots=0)
zero=env['decode_slot0'](bytes(1152),pattern)
assert zero['firstcall_attribution']=='INCONSISTENT_OBSERVATION_NO_CERTIFICATE'
reason14=bytearray(1152);struct.pack_into('<i',reason14,132,14)
r=env['decode_slot0'](bytes(reason14),pattern)
assert r['firstcall_attribution']=='H3_HOST_FAILED_BEFORE_CURRENT_MODEL_LEAF_UNKNOWN'
assert r['h2_observed']=='UNKNOWN_NOT_REACHED_OR_INCOMPLETE'
assert all(value=='UNKNOWN_NOT_REACHED_OR_INCOMPLETE' for key,value in r['h3_observed'].items() if key not in ('status','reason'))
assert len(bytes.fromhex(r['rawhex']))==1152 and len(bytes.fromhex(r['rawhex'])[128:])==1024
assert env['decode_slot0'](bytes(reason14),dict(pattern,h3calls=2))['firstcall_attribution']=='UNKNOWN_FIRSTCALL_PASS_PATTERN'
for rawslot in (bytes(1152),bytes(reason14)):
    offpattern=env['decode_slot0'](rawslot,dict(pattern,h3calls=0))
    assert all(value=='UNKNOWN_NOT_REACHED_OR_INCOMPLETE' for value in offpattern['h3_observed'].values())
    assert offpattern['h2_observed']==offpattern['h2_entries']=='UNKNOWN_NOT_REACHED_OR_INCOMPLETE'
    assert offpattern['indices_valid'] is False and bytes.fromhex(offpattern['rawhex'])==rawslot
supported=bytearray(1152)
for off,value in {0:2,8:1,92:2,96:4,100:0,104:1,108:2,112:3,128:2,136:4,140:3}.items():struct.pack_into('<i',supported,128+off,value)
assert env['decode_slot0'](bytes(supported),pattern)['indices_valid']
struct.pack_into('<i',supported,128+112,20)
assert env['decode_slot0'](bytes(supported),pattern)['firstcall_attribution']=='INCONSISTENT_OBSERVATION_NO_CERTIFICATE'
struct.pack_into('<i',supported,128+136,1000)
assert env['decode_slot0'](bytes(supported),pattern)['h2_entries']=='UNKNOWN_NOT_REACHED_OR_INCOMPLETE'
# Original stable_sample compares complete returned dicts, including every raw byte.
env['time']=type('NoWait',(),{'sleep':staticmethod(lambda _:None)})
assert env['stable_sample'](lambda:r)==r
for off in (0,127,128,1151):
    modified=bytearray(reason14);modified[off]^=1
    calls=iter((r,env['decode_slot0'](bytes(modified),pattern)))
    try:env['stable_sample'](lambda:next(calls))
    except ValueError:pass
    else:raise AssertionError('Changed own byte escaped stability equality')
shared=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='shared_state')
reads=[n for n in ast.walk(shared) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='read']
assert len(reads)==1 and ast.literal_eval(reads[0].args[1])==1152
original=ast.parse((HERE.parents[2]/'PROEVEN/u30-type10/20261015T194300/host1/Lees-Uitbreiding.py').read_text('utf-8'))
changed=[]
for node in original.body:
    if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
        current=next(n for n in tree.body if isinstance(n,type(node)) and n.name==node.name)
        if ast.dump(node)!=ast.dump(current):changed.append(node.name)
assert changed==['trusted_binding','native_expansion_state']
m=json.loads((HERE/'candidate-manifest.json').read_text())
pe=(HOST/'candidate/variant/CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll').read_bytes()
peoff=struct.unpack_from('<I',pe,0x3c)[0];assert pe[peoff:peoff+4]==b'PE\0\0'
sections=struct.unpack_from('<H',pe,peoff+6)[0];optsize=struct.unpack_from('<H',pe,peoff+20)[0]
image_size=struct.unpack_from('<I',pe,peoff+24+56)[0]
state_sections=[struct.unpack_from('<II',pe,peoff+24+optsize+i*40+8) for i in range(sections)]
state=m['components'];assert int(state['state_rva'],16)==0xdd000 and state['state_size']==0x54804
assert 0x40600+1152==0x40a80<=state['state_size']
assert 0xdd000+state['state_size']<=image_size
assert state_sections.count((0x54804,0xdd000))==1
gate=json.loads((HOST/'C10-ROOT-VRIJGAVE.json').read_text());assert gate['allowed'] is False
for row in gate['sources']:assert hashlib.sha256((HOST/row['path']).read_bytes()).hexdigest()==row['sha256']
result=dict(status='PASS_OFFLINE_ONLY',ast_changed_existing_functions=changed,slot_bytes=1152,h3_bytes=1024,slot_rva='0x11d600',slot_end_in_state='0x40a80',state_size='0x54804',copied_existing_layout=True,zero_and_reason14_unknown_labels=True,offpattern_all_interpretations_unknown=True,invalid_counts_indices_bounded=True,stability_includes_all_rawbytes=True,one_slot_read_per_snapshot=True,gate_allowed=False,synthetic_checks_are_not_actual_game_data=True,no_rpm_no_native_no_game=True)
(HERE/'offline-checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
