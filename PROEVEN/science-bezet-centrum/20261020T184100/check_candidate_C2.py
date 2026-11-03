"""Changed byte/reader checks only; never native execution or engine access."""
from pathlib import Path
import copy,difflib,hashlib,importlib.util,json,re,struct,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
PARENT=ROOT/'PROEVEN/science-foodreader-diagnostiek/20261019T194200'
sys.path[:0]=[str(OUT),str(OUT/'reader'),str(ROOT/'PROEVEN/production-h3'),str(ROOT/'PROEVEN/hulpmiddelen/python')]
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
import build_candidate as build,food_components
from food_failure_decoder import decode_failure
from partial_diagnostic import science,scope_header,science_result
from food_diagnostic_layout import FIELDS,required_bits
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def write(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n','utf-8')
def main():
 manifest=json.loads((OUT/'candidate-manifest.json').read_text('utf-8'));old=json.loads((PARENT/'candidate-manifest.json').read_text('utf-8'))
 p=pefile.PE(str(OUT/'U30-40.prepared.dll'));parent=pefile.PE(str(PARENT/'U30-40.prepared.dll'))
 assert sha(OUT/'U30-40.prepared.dll')==manifest['candidate_sha256']
 ext=int(manifest['components']['extension_rva'],16);labels=manifest['labels'];rows=manifest['recipe'];oldrows=old['recipe'];rw=int(manifest['components']['state_rva'],16)
 assert rw%4096==0 and manifest['components']['state_size']==497668 and p.OPTIONAL_HEADER.SizeOfImage>=rw+497668
 assert p.get_data(rw,497668)==bytes(497668)
 assert p.generate_checksum()==p.OPTIONAL_HEADER.CheckSum
 assert p.sections[-2].Characteristics==0x60000020 and p.sections[-1].Characteristics==0xc0000040
 base=pefile.PE(str(OUT/'release-v1.robotcom.backup.dll'))
 reloc=lambda pe:[(e.rva,e.type) for block in pe.DIRECTORY_ENTRY_BASERELOC for e in block.entries]
 assert reloc(p)==reloc(base) and reloc(p).count((0x8a598,3))==1
 assert p.get_data(0xd6000,0x3000)==parent.get_data(0xd6000,0x3000)
 assert manifest['components']['internal_H3_sha256']==old['components']['internal_H3_sha256']
 original=module('c2_default_original',ROOT/'PROEVEN/production-h3/components.py')
 products=[]
 for emitter in (original.reader,food_components.reader):
  r=build.Located(0xd64f5);emitter(r);products.append(r.finish())
 assert products[0]==products[1]==parent.get_data(0xd64f5,len(products[0]))
 # Prefix before SCI unchanged. Development body has identical instructions;
 # only relative destinations may move when the preceding SCI body grows.
 def region(recipe,start,end):return [r for r in recipe if start<=r['offset']<end]
 before=region(oldrows,0,old['labels']['science_model']);after=region(rows,0,labels['science_model']);assert before==after
 a=region(oldrows,old['labels']['development_tile'],old['labels']['sci_food_diag_reader']);b=region(rows,labels['development_tile'],labels['sci_food_diag_reader'])
 assert [r['asm'] for r in a]==[r['asm'] for r in b]
 relocated=[]
 for x,y in zip(a,b):
  if x['bytes']==y['bytes']:continue
  if x['asm']=='sub esi,modulepc':
   assert bytes.fromhex(x['bytes'])[:2]==bytes.fromhex(y['bytes'])[:2] and struct.unpack('<I',bytes.fromhex(y['bytes'])[2:])[0]-struct.unpack('<I',bytes.fromhex(x['bytes'])[2:])[0]==y['offset']-x['offset']
  else:assert x['asm'].startswith(('call ','j')) or ('own ' in x['asm'] and bytes.fromhex(x['bytes'])[:2]==bytes.fromhex(y['bytes'])[:2]),(x,y)
  relocated.append(dict(before=x,after=y))
 devcalls=[r for r in b if r['asm']=='call food_reader'];assert len(devcalls)==1
 for r in devcalls:assert ext+r['offset']+5+struct.unpack('<i',bytes.fromhex(r['bytes'])[1:])[0]==0xd64f5
 # Every recipe row equals bytes in the actual PE and disassembles completely.
 cs=Cs(CS_ARCH_X86,CS_MODE_32);cs.detail=True;direct=0
 for row in rows:
  raw=bytes.fromhex(row['bytes']);at=ext+row['offset'];assert p.get_data(at,len(raw))==raw
  if not row['asm'].startswith(('constant','prepared')):assert sum(i.size for i in cs.disasm(raw,0x20000000+at))==len(raw),row
  parts=row['asm'].split(' ',1)
  if len(parts)==2 and parts[1] in labels and (parts[0].startswith('j') or parts[0]=='call'):
   ins=list(cs.disasm(raw,0x20000000+at));assert len(ins)==1 and ins[0].operands[0].imm==0x20000000+ext+labels[parts[1]],row;direct+=1
 for call in manifest['diagnostic']['callers']:
  raw=p.get_data(call['call_rva'],5);assert raw[0]==0xe8 and call['call_rva']+5+struct.unpack('<i',raw[1:])[0]==manifest['diagnostic']['clone_rva']
 assert labels['food_reader']==old['labels']['food_reader']
 # Explain every recipe edit versus068f; byte shifts/relative fixups are
 # separately verified above. No old69/37 native suite is invoked.
 sm=difflib.SequenceMatcher(a=[r['asm'] for r in oldrows],b=[r['asm'] for r in rows],autojunk=False)
 edits=[]
 equal_relocations=0
 for tag,i,j,k,l in sm.get_opcodes():
  if tag!='equal':edits.append(dict(kind=tag,old=oldrows[i:j],new=rows[k:l]))
  else:
   for x,y in zip(oldrows[i:j],rows[k:l]):
    if x['bytes']==y['bytes']:continue
    op=x['asm'].split(' ')[0]
    if op.startswith('j') or op=='call':pass # all new direct targets checked above
    elif x['asm'] in ('sub esi,modulepc','sub esi,own diagnostic PC'):
     assert bytes.fromhex(x['bytes'])[:2]==bytes.fromhex(y['bytes'])[:2] and struct.unpack('<I',bytes.fromhex(y['bytes'])[-4:])[0]-struct.unpack('<I',bytes.fromhex(x['bytes'])[-4:])[0]==y['offset']-x['offset']
    elif x['asm']=='lea ebx,SCI primary return':assert struct.unpack('<I',bytes.fromhex(y['bytes'])[-4:])[0]==ext+labels['sci_food_diag_primary_return']
    else:raise AssertionError(('unexplained same-asm byte delta',x,y))
    equal_relocations+=1
 assert [[r['asm'] for r in e['old']] for e in edits]==[['test eax,eax','jz science_bad'],['test eax,eax','jz science_current_unknown'],[],[],['mov eax,0'],["mov edi,('ebp', -344)"]]
 allowed_new=('cmp eax,2','je science_center_occupied','cmp eax,1','jne science_bad','jne science_current_unknown',"mov ('edi', 0),1","mov ('edi', 4),17","mov ('edi', 112),1","mov ('edi', 24),0","mov ('edi', 28),-1","mov ('edi', 32),-1","mov ('edi', 36),-1",'jmp science_done')
 for edit in edits:
  for row in edit['new']:
   assert row['asm'] in allowed_new or row['offset']>=labels['sci_food_diag_reader'],row
 # Typed return consumes no food: two strict gates and exact scope handler.
 center=region(rows,labels['sci_food_diag_center_return'],labels['science_center_food_consumer'])
 assert [r['asm'] for r in center]==['cmp eax,2','je science_center_occupied','cmp eax,1','jne science_bad']
 tile=region(rows,labels['sci_food_diag_primary_return'],labels['science_tile_food_consumer'])
 assert [r['asm'] for r in tile]==['cmp eax,1','jne science_current_unknown']
 handler=region(rows,labels['science_center_occupied'],labels['science_bad'])
 assert [r['asm'] for r in handler]==["mov ('edi', 0),1","mov ('edi', 4),17","mov ('edi', 112),1","mov ('edi', 24),0","mov ('edi', 28),-1","mov ('edi', 32),-1","mov ('edi', 36),-1",'jmp science_done']
 done=region(rows,labels['science_done'],labels['development_tile']);assert any(r['asm'].startswith('frstor ') for r in done)
 observer=json.loads((OUT/'fixture/validator-observer-binding.json').read_text('utf-8'))
 for side in ('entry','exit'):
  at=observer['validator_'+side+'_rva'];n=observer[side+'_overwrite_size'];assert p.get_data(at,n).hex()==observer[side+'_original_hex']
 assert p.get_data(observer['validator_exit_rva']-2,2)==b'\x61\x9d'
 # New validator memory reads: only local stack or PIC Plan/validated own pos.
 start=observer['validator_entry_rva']-ext;end=observer['validator_exit_rva']-ext
 validator=region(rows,start,end);assert not any(r['asm'].startswith(('f','call (')) for r in validator)
 assert validator[0]['bytes']=='9c' and validator[1]['bytes']=='60' and validator[-2]['bytes']=='61' and validator[-1]['bytes']=='9d'
 # Fixtures are fully decoded, not executed. Two snapshots/replay observers
 # cover actual validator entry and restored exit on both return2 and0.
 fixture_names=[]
 for path in sorted((OUT/'fixture').glob('*.bin')):
  raw=path.read_bytes();decoded=list(cs.disasm(raw,0x10000000));assert sum(i.size for i in decoded)==len(raw);fixture_names.append(path.name)
  if path.stem.startswith('validator_'):assert not any(i.mnemonic.startswith(('f','wait')) for i in decoded)
 # Actual previously saved SCI0 arithmetic is unchanged with new decoder.
 actual_path=ROOT/'PROEVEN/science-foodreader-host/20261019/host1/variant/T1.json'
 actual=json.loads(actual_path.read_text('utf-8-sig'))['state']['shared_last_pass']['unselected_partial_pass_diagnostic']
 raw0=bytes.fromhex(next(o['rawhex'] for o in actual['objects'] if o['kind']=='ScienceResult' and o['index']==0))
 decoded=science_result.decode(raw0);scenario=decoded['computed_current'];assert [x['margin_x2_i64'] for x in scenario['steps']]==[35,30,25]
 # Small new scope-positive/negative cases; no fake current food interpretation.
 scope=bytearray(2048)
 for off,val in ((0,1),(4,17),(8,1),(12,3),(16,20),(24,0),(28,-1),(32,-1),(36,-1),(112,1)):struct.pack_into('<i',scope,off,val)
 cases=[]
 for name,off,val,accept in [('valid scope',None,None,True),('scope with NOW',0,2,False),('scope coverage0',112,0,False),('scope credit1',24,1,False),('scope selected0',28,0,False)]:
  raw=bytearray(scope)
  if off is not None:struct.pack_into('<i',raw,off,val)
  finding=scope_header(raw);assert finding['consistent']==accept
  if accept:
   value=science(raw);assert value['header']['center_food_i64'] is None and value['existing_decoder']['computed_current'] is None and not value['coverage_positive_calculation_allowed']
  else:
   try:science_result.decode(raw)
   except ValueError:pass
   else:raise AssertionError(name+' accepted')
  cases.append(dict(name=name,accepted=accept))
 # A historical branch10 is diagnostic evidence for its own earlier prefix,
 # not the last/current policy input after classification has progressed.
 guard=bytearray(236)
 values=dict(schema=1,valid=1,branch_id=10,callkind=1,owner=123,generation=7,prefix=3,ordinal=64,external=bytes(8),internal=bytes(8),width=1,height=1,world=0x12340000,cell=0x12340010,cityhandle=0,armyarray=0x12340080,unitcount=2,native_called=0,failure_eflags=0x202,outpointer=0x22220000,bindingpointer=0x30000000+144,guard_a=2,guard_b=0)
 mask=sum(1<<i for i in required_bits(10));values.update(reached_lo=mask&0xffffffff,reached_hi=mask>>32)
 for name,value in values.items():off,fmt,_=FIELDS[name];struct.pack_into('<'+fmt,guard,off,value)
 shared=dict(generation=7,owner=0,context=1,context_error=0,prefix_count=8,classified=6,SCI_primary_food=130,SCI_calls=6)
 partial=dict(usable_diagnostic_evidence=True,objects=[dict(kind='owner_generation_snapshot',owner=123,generation=7)],order_attribution=[dict(prefix_index=3,valid=True,external_center=(0,0,0))],scope_excluded_centers=[dict(prefix_index=3,**scope_header(scope))])
 for name,field,value,accept in [('historical occupied prefix3 while class6',None,None,True),('stale generation','generation',8,False),('unstarted prefix6','prefix',6,False),('wrong unit operand','unitcount',3,False)]:
  raw=bytearray(guard)
  if field:off,fmt,_=FIELDS[field];struct.pack_into('<'+fmt,raw,off,value)
  outcome=decode_failure(raw,shared,0x30000000,sha(OUT/'candidate-manifest.json'),partial)
  assert outcome['usable_diagnostic_evidence']==accept,(name,outcome)
  if accept:assert not outcome['typed_return2_proven_from_latch'] and not outcome['record_is_current_policy_input']
  cases.append(dict(name=name,accepted=accept))
 reader=module('c2_bound_reader',OUT/'reader/Lees-Uitbreiding.py');binding=reader.trusted_binding('U30-40')
 assert binding['shared_plan_rva']==rw and binding['shared_plan_size']==497668
 write('recipe-edits-C2.json',dict(edits=edits,equal_asm_byte_deltas_only_verified_rel32_PIC=equal_relocations,PE_checksum_valid=True,PE_RX_RW_permissions_valid=True,relocations_equal_release=True))
 write('candidate-static-checks-C2.json',dict(stage='C2_BYTES_AND_OWN_SAVED_DECODER_ONLY',candidate_sha256=manifest['candidate_sha256'],manifest_sha256=sha(OUT/'candidate-manifest.json'),whole_diff_explained=manifest['unexplained_byte_count']==0,original_changed_bytes=manifest['original_changed_byte_count'],appended_bytes=manifest['appended_byte_count'],shared_H3_and_padding_equal=True,default_factory_equal=True,default_factory_bytes=len(products[0]),prefix_before_SCI_equal=True,development_asm_equal=True,development_relocated_rows=len(relocated),original_development_reader_target=hex(0xd64f5),direct_rel32_checked=direct,state_rva=hex(rw),state_size=497668,RW_zero=True,recipe_edit_groups=len(edits),strict_center_tile_contract=True,handler_frstor_exit=True,validator_pushad_pushfd_balanced_bytes=True,validator_observer_binding=observer,fixtures=fixture_names,decoder_cases=cases,actual_saved_SCI0_margins=[35,30,25],actual_saved_SCI0_sha256=sha(actual_path),offline_reader_binding=True,native_compiled=False,native_run=False,installed=False,gameplay_proven=False))
 print(json.dumps(dict(candidate=manifest['candidate_sha256'],state=hex(rw),direct_rel32=direct,editgroups=len(edits),decoder_cases=len(cases),fixtures=len(fixture_names),native=False)))
if __name__=='__main__':main()
