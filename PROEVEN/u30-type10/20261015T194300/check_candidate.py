"""Independent finite PE/full-diff/branch checks, no native execution."""
from pathlib import Path
import sys,json,hashlib,struct
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((OUT/'candidate-manifest.json').read_text('utf-8'))
original=(OUT/'release-v1.robotcom.backup.dll').read_bytes();candidate=(OUT/'U30-40.prepared.dll').read_bytes()
assert sha(original)==manifest['base_sha256'] and sha(candidate)==manifest['candidate_sha256']
for row in manifest['sources']+manifest['source_dependency_pins']+manifest['release_pins']:
 assert sha((ROOT/row['path']).read_bytes())==row['sha256']
rebuilt=bytearray(original)
for row in manifest['full_diff']:
 at=row['offset'];before=bytes.fromhex(row['before']);after=bytes.fromhex(row['after'])
 assert original[at:at+len(before)]==before
 if at==len(original):rebuilt.extend(after)
 else:assert len(before)==len(after);rebuilt[at:at+len(after)]=after
assert bytes(rebuilt)==candidate
p=pefile.PE(data=original);cp=pefile.PE(data=candidate)
new=cp.sections[5:];assert len(new)==2
assert new[0].VirtualAddress==0xd6000 and new[1].VirtualAddress>=new[0].VirtualAddress+new[0].Misc_VirtualSize
assert new[0].Characteristics==0x60000020 and new[1].Characteristics==0xc0000040
assert not any(candidate[new[1].PointerToRawData:new[1].PointerToRawData+new[1].SizeOfRawData])
for i in range(5):assert p.sections[i].__pack__()==cp.sections[i].__pack__()
for section in p.sections:
 a=section.PointerToRawData;b=a+section.SizeOfRawData
 changed=[j for j in range(a,b) if original[j]!=candidate[j]]
 assert all(any(row['offset']<=j<row['offset']+row['length'] for row in manifest['allowed_changes'] if row['reason'].startswith('named new hook')) for j in changed)
assert cp.OPTIONAL_HEADER.CheckSum==cp.generate_checksum()
labels=manifest['labels'];base=int(manifest['components']['extension_rva'],16)
for name in ['start_hook','capture_hook','desired_hook','scope_hook','quota_hook','execute_gate','arrival_dispatch','normalize_dispatch']:
 assert 0<=labels[name]<new[0].Misc_VirtualSize
prep=json.loads((OUT/'preparation-manifest.json').read_text('utf-8'))
for row in prep['windows']:
 name=row['name'];rva=int(row['rva'],16);data=cp.get_data(rva,len(bytes.fromhex(row['preimage'])))
 if name=='execute_slot':assert struct.unpack('<I',data)[0]==0x20000000+base+labels['execute_gate']
 elif name=='arrival_result':assert data==b'\x90'*5
 else:
  target=struct.unpack('<i',data[1:5])[0]+rva+5
  assert target==base+labels[dict(arrival_call='arrival_dispatch',normalize='normalize_dispatch').get(name,name)]
  assert data[0]==0xe8 and data[5:]==b'\x90'*(len(data)-5)
for row in prep['b2_hooks']:assert cp.get_data(int(row['rva'],16),5).hex()==row['bytes']
bp=prep['b2_payload'];assert sha(cp.get_data(0xd4000,bp['size']))==bp['sha256']
dis=Cs(CS_ARCH_X86,CS_MODE_32);lines=[];branches=[]
allstarts=set()
for row in manifest['recipe']:
 raw=bytes.fromhex(row['bytes']);at=0x20000000+base+row['offset']
 if row['asm'].startswith('constant'):continue
 decoded=list(dis.disasm(raw,at));assert sum(x.size for x in decoded)==len(raw)
 for ins in decoded:
  allstarts.add(ins.address)
  lines.append(f'{ins.address:08x} {ins.bytes.hex():24} {ins.mnemonic:8} {ins.op_str}')
  if (ins.mnemonic=='call' or ins.mnemonic.startswith('j')) and ins.op_str.startswith('0x'):branches.append((ins.address,int(ins.op_str,16)))
for at,target in branches:
 targetrva=target-0x20000000
 if base<=targetrva<new[0].VirtualAddress+new[0].Misc_VirtualSize:assert target in allstarts,(hex(at),hex(target))
(OUT/'extension-disassembly.txt').write_text('\n'.join(lines)+'\n','utf-8')
source=(OUT/'native.py').read_text('utf-8')
assert 'SELECTED_CAP=40' in source and 'ORDER=SELECTED+160' in source
buffers=manifest['buffers'];assert buffers['SELECTED']+40*4<=buffers['ORDER'];assert buffers['ORDER']+64*4<=buffers['PATHCACHE']
assert 'manual' not in (OUT/'policy.py').read_text('utf-8').lower()
summary=dict(stage='C1_OFFLINE_STATIC_ONLY',candidate_sha256=sha(candidate),manifest_sha256=sha((OUT/'candidate-manifest.json').read_bytes()),full_diff_reconstructs_exact_candidate=True,all_original_changes_only_named_hooks_and_headers=True,original_sections_preserved=True,b2_payload_and_five_hooks_exact=True,existing_HIGHLOW_directory_unchanged=manifest['relocations_unchanged'],rx_rw_after_original_SizeOfImage=True,rw_initial_zero=True,checksum_valid=True,direct_own_branches_at_instruction_boundaries=True,buffers_nonoverlap=True,branch_count=len(branches),native_calls_executed=0,installations=0,game_starts=0,gameplay_acceptance=False)
(OUT/'candidate-static-checks.json').write_text(json.dumps(summary,indent=2)+'\n','utf-8')
print(json.dumps(summary))
