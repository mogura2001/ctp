"""Finite comparison with tested U30 and binding-only C10 update; no RPM."""
from pathlib import Path
import sys,json,hashlib,struct,difflib,ast
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];OLD=ROOT/'PROEVEN/uitbreiding-30-40/20261012T181500'
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
sha=lambda b:hashlib.sha256(b).hexdigest()
old=json.loads((OLD/'candidate-manifest.json').read_text());new=json.loads((OUT/'candidate-manifest.json').read_text())
a=(OLD/'U30-40.prepared.dll').read_bytes();b=(OUT/'U30-40.prepared.dll').read_bytes();p=pefile.PE(data=b)
assert len(a)==len(b) and old['labels']==new['labels'] and old['sections']==new['sections']
rows=[]
for x,y in zip(old['recipe'],new['recipe']):
 if x['bytes']!=y['bytes']:
  assert x['bytes'].startswith('0f84') and y['bytes'].startswith('0f84') and len(x['bytes'])==len(y['bytes'])==12
  rva=int(new['components']['extension_rva'],16)+x['offset']
  target=lambda raw:rva+6+struct.unpack('<i',bytes.fromhex(raw)[2:])[0]
  expect='bind_done' if rva<0xda000 else 'final_done'
  assert target(y['bytes'])==int(new['components']['extension_rva'],16)+new['labels'][expect]
  rows.append(dict(rva=hex(rva),file_offset=hex(p.get_offset_from_rva(rva)),before=x['bytes'],after=y['bytes'],old_target_rva=hex(target(x['bytes'])),new_target_rva=hex(target(y['bytes'])),epilogue=expect))
assert len(rows)==5 and len(old['recipe'])==len(new['recipe'])
allowed=set(range(p.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum'),p.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum')+4))
for r in rows:allowed.update(range(int(r['file_offset'],16)+2,int(r['file_offset'],16)+6))
diff=[dict(offset=hex(i),before=x,after=y) for i,(x,y) in enumerate(zip(a,b)) if x!=y]
assert all(int(r['offset'],16) in allowed for r in diff)
assert old['b2_preserved']==new['b2_preserved'] and old['h3_labels']==new['h3_labels'] and old['components']['internal_H3_sha256']==new['components']['internal_H3_sha256']
report=dict(old_candidate_sha256=sha(a),candidate_sha256=sha(b),changed_byte_count=len(diff),exact_byte_diff=diff,five_rel32_retargets=rows,all_labels_and_section_layout_equal=True,all_other_recipe_bytes_equal=True,all_prologues_epilogues_and_hookwrappers_equal=True,only_rel32_operands_and_checksum_changed=True,b2_and_relocations_preserved=True,native_ABI='Existing C2 shim reused separately; flags/x87 hook snapshots byte-identical. No host validation implied.')
(OUT/'binary-diff.json').write_text(json.dumps(report,indent=2)+'\n')
reader=OUT/'c10/Lees-Uitbreiding.py';s=reader.read_text('utf-8');s=s.replace(old['candidate_sha256'],new['candidate_sha256']).replace('9b2146579b7ccf3a8133850c360e7b0c934565998078fa7ae140a6b10f6e5341',sha((OUT/'candidate-manifest.json').read_bytes()));reader.write_text(s,'utf-8')
for name in ['Lees-Uitbreiding.py','original_core.py','participants.json']:
 q=OUT/'c10'/name;ast.parse(q.read_text('utf-8')) if name.endswith('.py') else json.loads(q.read_text())
 (OUT/'c10'/(name+'.source-diff.txt')).write_text(''.join(difflib.unified_diff((OLD/'c10'/name).read_text('utf-8').splitlines(True),q.read_text('utf-8').splitlines(True),fromfile='tested-C10/'+name,tofile='own-C10/'+name)),'utf-8')
dest=OUT/'c10/candidate/variant/CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
gate=dict(allowed=False,baseline_allowed=False,candidate_sha256=sha(b),sources=[dict(path=name,sha256=sha((OUT/'c10'/name).read_bytes())) for name in ['Lees-Uitbreiding.py','original_core.py','participants.json']],state='ROOT_REVIEW_PENDING_NO_LIVE_READER')
(OUT/'c10/C10-ROOT-VRIJGAVE.json').write_text(json.dumps(gate,indent=2)+'\n')
print(json.dumps(dict(candidate=sha(b),changed_bytes=len(diff),retargets=rows,reader_logic_unchanged_except_two_hash_pins=True,gate=False)))
