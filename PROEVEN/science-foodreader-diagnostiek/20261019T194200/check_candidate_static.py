"""Candidate bytes/PE/own-byte decoder only. No native process or game access."""
from pathlib import Path
import copy,hashlib,importlib.util,json,re,struct,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];PARENT=ROOT/'PROEVEN/u30-science-filter/20261017T124500'
sys.path[:0]=[str(OUT),str(OUT/'reader'),str(ROOT/'PROEVEN/production-h3'),str(ROOT/'PROEVEN/hulpmiddelen/python')]
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32,CS_AC_READ
from capstone.x86 import X86_OP_MEM
import build_candidate as build,food_components,fixture_sources
from food_diagnostic_layout import BRANCHES,FIELDS,required_bits
from food_failure_decoder import decode_failure
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
def main():
 m=json.loads((OUT/'candidate-manifest.json').read_text('utf-8'));old=json.loads((PARENT/'candidate-manifest.json').read_text('utf-8'))
 p=pefile.PE(str(OUT/'U30-40.prepared.dll'));parent=pefile.PE(str(PARENT/'U30-40.prepared.dll'))
 assert sha(OUT/'U30-40.prepared.dll')==m['candidate_sha256']
 assert m['components']['state_rva']=='0xe3000' and m['components']['state_size']==497668
 assert p.OPTIONAL_HEADER.SizeOfImage>=0xe3000+497668
 assert m['components']['internal_H3_sha256']==old['components']['internal_H3_sha256']
 assert p.get_data(0xd6000,0x3000)==parent.get_data(0xd6000,0x3000)
 original=module('static_original_components',ROOT/'PROEVEN/production-h3/components.py')
 recipes=[]
 for emitter in (original.reader,food_components.reader):
  r=build.Located(0xd64f5);emitter(r);recipes.append((r.finish(),r))
 assert recipes[0][0]==recipes[1][0]==parent.get_data(0xd64f5,len(recipes[0][0]))
 default=recipes[0][1];rows=m['recipe'];ext=int(m['components']['extension_rva'],16);labels=m['labels'];diag=m['diagnostic'];clone=labels['sci_food_diag_reader'];failure1=labels['sci_food_diag_failure_1']
 assert len(old['recipe'])<=len(rows)
 changes=[]
 for a,b in zip(old['recipe'],rows):
  if a==b:continue
  assert a['offset']==b['offset']
  if a['asm'] in ('lea ebx,own pass','lea edx,generation'):
   assert a['asm']==b['asm'] and a['bytes'][:4]==b['bytes'][:4]
   assert struct.unpack('<I',bytes.fromhex(b['bytes'])[-4:])[0]-struct.unpack('<I',bytes.fromhex(a['bytes'])[-4:])[0]==0x2000
   kind='necessary own-state/generation RVA immediate'
  else:
   assert a['asm']=='call H3FoodReader' and b['asm']=='call sci_food_diag_reader';kind='SCI-only call rel32'
  changes.append(dict(kind=kind,before=a,after=b))
 assert len(changes)==20 and sum(r['kind']=='SCI-only call rel32' for r in changes)==2
 assert labels['science_model']==old['labels']['science_model'] and labels['development_tile']==old['labels']['development_tile']
 assert labels['food_reader']==old['labels']['food_reader']==0xd64f5-ext
 development_calls=[r for r in rows if labels['development_tile']<=r['offset']<clone and r['asm']=='call food_reader']
 assert len(development_calls)==1
 for row in development_calls:
  at=ext+row['offset'];assert at+5+struct.unpack('<i',bytes.fromhex(row['bytes'])[1:])[0]==0xd64f5
 # Strip only emitted balanced diagnostic regions, then account for each
 # original memory-CMP's single-load ECX split. Every other original command
 # must remain in the same order with identical source operands/predicates.
 normalized=[];logging=False;categories={}
 for row in rows:
  if not clone<=row['offset']<failure1:continue
  if row['asm']=='diagnostic pushfd':assert not logging;logging=True
  categories[row['offset']]='added logging: own stack/PIC Plan/bounded own tile bytes' if logging else 'original reader path or declared single-load CMP split'
  if not logging:normalized.append(row['asm'].replace('sci_food_diag','food').replace('esp,352','esp,80'))
  if row['asm']=='diagnostic popfd':logging=False
 assert not logging
 splits={
  ('push ecx',"mov ecx,('esi', 20)",'cmp ecx,0','pop ecx'):"cmp ('esi', 20),0",
  ('push ecx',"mov ecx,('eax', 48)",'cmp ecx,0','pop ecx'):"cmp ('eax', 48),0",
  ('push ecx',"mov ecx,('edx', 0)",'cmp eax,ecx','pop ecx'):"cmp eax,('edx', 0)",
  ('push ecx',"mov ecx,('edi', 4)",'cmp eax,ecx','pop ecx'):"cmp eax,('edi', 4)"}
 reduced=[];i=0;used=[]
 while i<len(normalized):
  part=tuple(normalized[i:i+4])
  if part in splits:reduced.append(splits[part]);used.append(splits[part]);i+=4
  else:reduced.append(re.sub(r'food_failure_\d+','food_bad',normalized[i]));i+=1
 assert len(used)==4
 assert reduced==[r['asm'] for r in default.rows],next(((i,a,b) for i,(a,b) in enumerate(zip(reduced,[r['asm'] for r in default.rows])) if a!=b),None)
 cs=Cs(CS_ARCH_X86,CS_MODE_32);cs.detail=True
 inventory=[];edges={};fp=[];extra_indirect=[]
 for row in rows:
  off=row['offset']
  if off<clone:continue
  category=categories.get(off,'added failure/publication: own stack and PIC Plan only')
  for ins in cs.disasm(bytes.fromhex(row['bytes']),0x20000000+ext+off):
   if ins.mnemonic.startswith(('f','wait')):fp.append(ins.mnemonic)
   for operand in ins.operands:
    if operand.type!=X86_OP_MEM or not operand.access&CS_AC_READ or ins.mnemonic=='lea':continue
    base=ins.reg_name(operand.mem.base);entry=dict(va=hex(ins.address),bytes=ins.bytes.hex(),instruction=ins.mnemonic+' '+ins.op_str,base=base,index=ins.reg_name(operand.mem.index),displacement=operand.mem.disp,category=category)
    if category.startswith('added'):
     assert base in ('ebp','esp','edi','ebx'),entry
     if ins.mnemonic=='call':extra_indirect.append(entry)
    inventory.append(entry)
  match=re.fullmatch(r'(\w+) sci_food_diag_failure_(\d+)',row['asm'])
  if match:
   branch=int(match[2]);assert branch not in edges;edges[branch]=dict(predicate=match[1],guard_rva=ext+off,landing_rva=ext+labels['sci_food_diag_failure_'+str(branch)])
 assert not fp and not extra_indirect and set(edges)==set(range(1,38))
 for branch,tail,name in BRANCHES:
  info=next(b for b in diag['branches'] if b['id']==branch)
  assert info['parent_rva']==hex(0xd0000+tail) and info['parent_va']==hex(0x200d0000+tail)
  assert info['landing_rva']==edges[branch]['landing_rva']
  assert p.get_data(info['landing_rva'],2)==b'\x9c\x60'
  at=info['restored_exit_rva'];raw=p.get_data(at,5)
  assert p.get_data(at-2,2)==b'\x61\x9d' and raw[0]==0xe9 and at+5+struct.unpack('<i',raw[1:])[0]==ext+labels['sci_food_diag_bad']
 for call in diag['callers']:
  at=call['call_rva'];raw=p.get_data(at,5)
  assert raw[0]==0xe8 and at+5+struct.unpack('<i',raw[1:])[0]==diag['clone_rva'] and call['return_rva']==at+5
 # Complete finite fixtures decode, but are never executed here.
 for name in ('edge','observer','normal'):
  raw=(OUT/'fixture'/(name+'.bin')).read_bytes();decoded=list(cs.disasm(raw,0x10000000));assert sum(i.size for i in decoded)==len(raw)
  for ins in decoded:assert not ins.mnemonic.startswith(('f','wait'))
 # Small bounded changed own-byte decoder cases, explicitly synthetic.
 shared=dict(generation=7,owner=0,context=1,context_error=0,prefix_count=4,classified=4,SCI_primary_food=64,SCI_calls=4)
 partial=dict(usable_diagnostic_evidence=True,objects=[dict(kind='owner_generation_snapshot',owner=123,generation=7)],order_attribution=[dict(prefix_index=3,valid=True,external_center=(0,0,0))])
 cases=[]
 def decode_case(name,branch=9,mutate=None,accepted=False):
  raw=bytearray(fixture_sources.seed(branch))
  for field,value in (('valid',1),('branch_id',branch),('failure_eflags',fixture_sources.edge_flags(branch)),('outpointer',0x22220000),('bindingpointer',0x30000000+144)):
   off,fmt,_=FIELDS[field];struct.pack_into('<'+fmt,raw,off,value)
  off=FIELDS['reached_hi'][0];struct.pack_into('<I',raw,off,struct.unpack_from('<I',raw,off)[0]|(1<<(37-32)))
  if mutate:mutate(raw)
  value=decode_failure(bytes(raw),shared,0x30000000,sha(OUT/'candidate-manifest.json'),partial)
  assert value['usable_diagnostic_evidence']==accepted,(name,value)
  assert value['rawhex']==raw.hex() and not value['selected'] and not value['certified']
  cases.append(dict(name=name,accepted=accepted,attribution=value['attribution_status'],error=value.get('error')))
 def word(field,value):return lambda raw:struct.pack_into('<'+FIELDS[field][1],raw,FIELDS[field][0],value)
 decode_case('synthetic complete cityhandle9',accepted=True)
 decode_case('synthetic native return33',33,accepted=True)
 decode_case('synthetic getter mismatch34',34,accepted=True)
 decode_case('synthetic JO logedge26, no natural reachability',26,accepted=True)
 decode_case('missing required reached cityhandle8',mutate=lambda raw:struct.pack_into('<I',raw,32,struct.unpack_from('<I',raw,32)[0]&~(1<<8)))
 decode_case('partial valid0 raw retained',mutate=word('valid',0))
 decode_case('branch38 refused',mutate=word('branch_id',38))
 decode_case('invalid kind3 refused',mutate=word('callkind',3))
 decode_case('invalid prefix64 refused',mutate=word('prefix',64))
 decode_case('generation mismatch refused',mutate=word('generation',8))
 decode_case('reserved reached44 refused',mutate=lambda raw:struct.pack_into('<I',raw,36,struct.unpack_from('<I',raw,36)[0]|(1<<12)))
 decode_case('wrong taken branch flags refused',mutate=word('failure_eflags',0x242))
 decode_case('wrong HostBinding refused',mutate=word('bindingpointer',0x30000000))
 t0=decode_failure(bytes(236),dict(shared,generation=0),0x30000000,'synthetic',None);assert t0['attribution_status']=='NOT_INITIALIZED'
 try:decode_failure(bytes(237),shared,0x30000000,'synthetic',partial)
 except ValueError:pass
 else:raise AssertionError('237 bytes accepted')
 reader=module('static_own_food_reader',OUT/'reader/Lees-Uitbreiding.py');binding=reader.trusted_binding('U30-40')
 assert binding['shared_plan_rva']==0xe3000 and binding['shared_plan_size']==497668
 result=dict(stage='BUILT_OFFLINE_BYTE_STATIC_AND_OWNBYTE_DECODER_CHECKED_NOT_NATIVE',candidate_sha256=m['candidate_sha256'],manifest_sha256=sha(OUT/'candidate-manifest.json'),default_factory_byte_identity=True,default_factory_size=len(recipes[0][0]),whole_shared_H3_and_padding_byte_equal=True,original_recipe_changes=changes,normalized_original_reader_trace_equal=True,single_foreign_load_CMP_splits=used,foreign_read_inventory_entries=len(inventory),logging_adds_foreign_callbacks=False,added_logging_bases='own EBP/ESP, PIC Plan EDI, bounds-validated own table/position EBX',all37_unique_conditional_edges=edges,all37_landing_flag_GPR_restore_and_complete_JMPs=True,development_original_reader_calls=len(development_calls),state_rva='0xe3000',state_size=497668,fixture_emitted=True,decoder_synthetic_cases=cases,T0_NOT_INITIALIZED=True,invalid_size237_refused=True,offline_reader_binding=True,loaded_binding_ranges=len(binding['ranges']),native_compiled=False,native_executed=False,installed=False,gameplay_improvement_proven=False)
 (OUT/'foreign-read-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n','utf-8')
 (OUT/'candidate-static-checks.json').write_text(json.dumps(result,indent=2)+'\n','utf-8')
 print(json.dumps(dict(candidate=m['candidate_sha256'],default_and_H3_equal=True,changed_old_rows=20,edges=37,foreign_read_inventory=len(inventory),ownbyte_decoder_cases=len(cases),native=False)))
if __name__=='__main__':main()
