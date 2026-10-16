"""Own fixture correction audit; no native process/game access."""
from pathlib import Path
import json,hashlib,difflib,datetime,sys
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
audit={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':'prepared_not_executed','candidate_unchanged':False,'scope':'controlled callbacks and synthetic engine pin context only','files':[]}
for name in ('prepare_native_fixtures.py','fixture-large-center-reader.bin','native-fixture-input-pins.json','native-fixtures.cs','native-main.cs','native-fixtures.exe'):
 before=(root/(name+'.before-attempt8')).read_bytes();after=(root/name).read_bytes()
 audit['files'].append({'file':name,'before_sha256':sha(before),'after_sha256':sha(after),'unchanged':before==after})
 if name.endswith(('.py','.cs')):
  diff=''.join(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),fromfile=name+'.before-attempt8',tofile=name))
  (root/(name+'.attempt8.diff.txt')).write_text(diff,encoding='utf-8')
old=(root/'fixture-large-center-reader.bin.before-attempt8').read_bytes();new=(root/'fixture-large-center-reader.bin').read_bytes()
insertion=b'\x8b\xbd\x14\x00\x00\x00'
offset=new.index(insertion,new.index(b'\xf3\xab')+2)
assert new[:offset]+new[offset+len(insertion):]==old
audit['large_center_exact_change']={'offset':offset,'inserted_hex':insertion.hex(),'meaning':'MOV EDI,[EBP+20] reload output base after REP STOSD advances EDI','old_length':len(old),'new_length':len(new),'all_other_bytes_equal':True}
oldpins=json.loads((root/'native-fixture-input-pins.json.before-attempt8').read_text());newpins=json.loads((root/'native-fixture-input-pins.json').read_text())
audit['other_fixture_pins_unchanged']=all(a==b for a,b in zip(oldpins,newpins) if a['name']!='large-center-reader')
assert audit['other_fixture_pins_unchanged']
audit['candidate_sha256']=sha((root/'SCIENCE-C1-CREDIT-OFF.prepared.dll').read_bytes())
audit['candidate_unchanged']=audit['candidate_sha256']=='622cdd87c7b9480e9740ca5baaf37190ed632852358db0f80f6b6b936b13d6ba'
assert audit['candidate_unchanged']
input=json.loads((root/'native-input.json').read_text());blocks=sorted({0,0x130000,0x670000}|{v&0xffff0000 for v in input['pin_rvas']})
assert blocks==[0,0x90000,0x110000,0x120000,0x130000,0x340000,0x670000]
audit['early_fixed_own_blocks']=['0x%08x'%(0x400000+v) for v in blocks]
audit['finite_setup_change']='Reserve exact seven own 64KiB blocks before serializer/loader/image allocation; validate same set in Run; no ASLR retry/unmap/host patch/SCI guard bypass.'
audit['compiled_wrapper_sha256']=sha((root/'native-fixtures.attempt8.exe').read_bytes())
audit['byte_pins']={p.name:sha(p.read_bytes()) for p in root.glob('fixture-*.bin')}
audit['attempts_1_through_7_pins']={p.name:sha(p.read_bytes()) for p in root.glob('native-attempt[1-7]*')}
(root/'native-attempt8-preparation-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:audit[k] for k in ('candidate_unchanged','other_fixture_pins_unchanged','large_center_exact_change','early_fixed_own_blocks','compiled_wrapper_sha256')},indent=2))
