"""C2 byte/own-saved-decoder checks; no native/engine/process/GUI access."""
from pathlib import Path
import ast,copy,difflib,hashlib,importlib.util,json,re,struct,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent.parent;ROOT=OUT.parents[2]
PARENT=ROOT/'PROEVEN/science-bezet-centrum/20261020T184100'
sys.path[:0]=[str(OUT),str(OUT/'reader'),str(ROOT/'PROEVEN/hulpmiddelen/python')]
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from path_diagnostic_layout import FIELDS,PAIRS,BRANCHES,STATE_SIZE,required_mask
from path_failure_decoder import decode_path,stable_record
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):(OUT/'c2'/name).write_text(json.dumps(value,indent=2)+'\n','utf-8')
def main():
 assert sha(OUT/'SOURCE-PINS.json')=='75244d1e104095f12204c3b67c03ad42ecf329c088fc795391b6880cf7394c37'
 for pin in json.loads((OUT/'SOURCE-PINS.json').read_text('utf-8'))['sources']:assert sha(ROOT/pin['path'])==pin['sha256'],pin['path']
 manifest=json.loads((OUT/'candidate-manifest.json').read_text('utf-8'));old=json.loads((PARENT/'candidate-manifest.json').read_text('utf-8'));rows=manifest['recipe'];oldrows=old['recipe'];labels=manifest['labels'];oldlabels=old['labels'];ext=int(manifest['components']['extension_rva'],16);oldext=int(old['components']['extension_rva'],16);rw=int(manifest['components']['state_rva'],16)
 p=pefile.PE(str(OUT/'U30-40.prepared.dll'));parent=pefile.PE(str(PARENT/'U30-40.prepared.dll'));base=pefile.PE(str(OUT/'release-v1.robotcom.backup.dll'))
 assert sha(OUT/'U30-40.prepared.dll')==manifest['candidate_sha256'] and manifest['unexplained_byte_count']==0
 assert rw%4096==0 and labels['generation']-labels['pass_state']==0x79800 and manifest['components']['state_size']==STATE_SIZE==0x79904
 assert p.sections[-1].VirtualAddress==rw and p.sections[-1].Misc_VirtualSize==STATE_SIZE and p.sections[-1].SizeOfRawData==(STATE_SIZE+511)//512*512 and p.OPTIONAL_HEADER.SizeOfImage==(rw+STATE_SIZE+4095)//4096*4096
 assert p.get_data(rw,STATE_SIZE)==bytes(STATE_SIZE) and p.generate_checksum()==p.OPTIONAL_HEADER.CheckSum
 assert (p.sections[-2].Characteristics,p.sections[-1].Characteristics)==(0x60000020,0xc0000040)
 reloc=lambda pe:[(e.rva,e.type) for block in pe.DIRECTORY_ENTRY_BASERELOC for e in block.entries]
 assert reloc(p)==reloc(base)==reloc(parent) and reloc(p).count((0x8a598,3))==1
 assert p.get_data(0xd4000,0x5000)==parent.get_data(0xd4000,0x5000),'B2/H3 and intercomponent padding'
 assert manifest['components']['internal_H3_sha256']==old['components']['internal_H3_sha256']
 cs=Cs(CS_ARCH_X86,CS_MODE_32);cs.detail=True;direct=0
 for row in rows:
  raw=bytes.fromhex(row['bytes']);at=ext+row['offset'];assert p.get_data(at,len(raw))==raw
  if not row['asm'].startswith(('constant','prepared')):assert sum(i.size for i in cs.disasm(raw,0x20000000+at))==len(raw),row
  parts=row['asm'].split(' ',1)
  if len(parts)==2 and parts[1] in labels and (parts[0].startswith('j') or parts[0]=='call'):
   ins=list(cs.disasm(raw,0x20000000+at));assert len(ins)==1 and ins[0].operands[0].imm==0x20000000+ext+labels[parts[1]],row;direct+=1
 # Strip only explicitly delimited new logger blocks and their16 landings.
 # What remains must be the entire historical policy/model instruction stream,
 # except equivalent single-read postcontext and retargeted unknown edges.
 stripped=[];logger_blocks=[];active=None
 for row in rows:
  if row['asm']=='pathdiag pushfd':assert active is None;active=[]
  if active is not None:
   active.append(row)
   if row['asm']=='pathdiag popfd':
    assert active[0]['bytes']=='9c' and active[1]['bytes']=='60' and active[-2]['bytes']=='61' and active[-1]['bytes']=='9d';logger_blocks.append(active);active=None
   continue
  if labels['pd_failure_1']<=row['offset']<labels['capture_heap']:assert row['asm']=='jmp path_unknown';continue
  item=dict(row);item['asm']=re.sub(r'pd_failure_\d+$','path_unknown',item['asm']);stripped.append(item)
 assert active is None
 pattern=['push ecx',"mov ecx,('edx', 7146388)",'cmp ecx,0','pop ecx']
 context_groups=0;normalized=[];i=0
 while i<len(stripped):
  if [r['asm'] for r in stripped[i:i+4]]==pattern:
   item=dict(stripped[i+2]);item['asm']="cmp ('edx', 7146388),0";item['context_read_equivalent']=True;normalized.append(item);i+=4;context_groups+=1
  else:normalized.append(stripped[i]);i+=1
 assert context_groups==1
 assert [r['asm'] for r in oldrows]==[r['asm'] for r in normalized],list(difflib.unified_diff([r['asm']+'\n' for r in oldrows],[r['asm']+'\n' for r in normalized]))[:60]
 relocated=[]
 for a,b in zip(oldrows,normalized):
  if a['bytes']==b['bytes']:continue
  if b.get('context_read_equivalent'):continue
  op=b['asm'].split(' ')[0]
  if op.startswith('j') or op=='call':kind='verified direct rel32'
  else:
   ar=bytes.fromhex(a['bytes']);br=bytes.fromhex(b['bytes']);assert ar[:-4]==br[:-4],(a,b)
   av=struct.unpack('<I',ar[-4:])[0];bv=struct.unpack('<I',br[-4:])[0]
   matches=[name for name in oldlabels.keys()&labels.keys() if oldext+oldlabels[name]==av and ext+labels[name]==bv]
   assert matches,('unexplained equal-asm bytes',a,b);kind='same named PIC/RVA target '+','.join(matches)
  relocated.append(dict(old=a,new=b,explanation=kind))
 # Every failure has one direct predicate edge and a unique own landing.
 edges=[]
 for edge,parent_rva,name in BRANCHES:
  entry=next(x for x in manifest['path_diagnostic']['branches'] if x['id']==edge);landing=entry['landing_rva'];assert landing==ext+labels['pd_failure_'+str(edge)] and entry['required_reachedmask']==required_mask(edge)
  incoming=[r for r in rows if r['asm'].endswith(' pd_failure_'+str(edge))];assert len(incoming)==1
  block=next(b for b in logger_blocks if b[0]['offset']==landing-ext)
  assert any(r['asm']=="cmp ('edi', 497684),"+str(required_mask(edge,False)) for r in block)
  assert any(r['asm']=="mov ('edi', 497680),eax" for r in block)
  assert not any(r['asm'].startswith(('f','call (')) for r in block)
  edges.append(dict(id=edge,parent_rva=hex(parent_rva),edge_rva=hex(ext+incoming[0]['offset']),landing_rva=hex(landing),name=name))
 for pair,target in [('finalize_selection','select_direct_plans'),('selection_cached','cached_path'),('cached_direct','direct_path')]:
  call=manifest['path_diagnostic']['calls'][pair];raw=p.get_data(call['call_rva'],5);assert call['return_rva']==call['call_rva']+5 and raw[0]==0xe8 and call['call_rva']+5+struct.unpack('<i',raw[1:])[0]==ext+labels[target]
 # Integer logger bodies may only access registers, stack and validated own
 # Plan/arrays; no x87 or native indirect calls are introduced by any block.
 for block in logger_blocks:assert not any(r['asm'].startswith(('f','call (')) for r in block)
 # Record the exact emitted EAX-source/store and reachedbit sequence for
 # independent review, including operands captured before original reuse.
 captures=[];stored=set()
 byoff={off:name for name,off in FIELDS.items()}
 for block in logger_blocks:
  values=[]
  for index,row in enumerate(block):
   match=re.fullmatch(r"mov \('edi', (\d+)\),(eax|edx|edi|\d+)",row['asm'])
   if match:
    relative=int(match.group(1))-0x79804
    if relative in byoff:stored.add(byoff[relative])
    values.append(dict(record_offset=relative,field=byoff.get(relative,'pair_high_DWORD'),source=block[index-1]['asm'] if index and match.group(2)=='eax' else match.group(2)))
  captures.append(dict(start_rva=hex(ext+block[0]['offset']),stores=values,reached_stores=[r for r in block if r['asm'].startswith("or ('edi', 497684),")]))
 assert set(FIELDS)<=stored,set(FIELDS)-stored
 assert any(r['asm']=="mov ('edi', 497668),1" for r in rows),'valid last publication'
 assert any(r['asm']=="mov eax,('esp', 32)" for b in logger_blocks for r in b),'overflow original EFLAGS snapshot operand'
 # Existing source pins plus normalized entire recipe prove unchanged SCI,
 # policy criteria, argument order, free path and both strict consumers.
 fixture=(OUT/'fixture/logger.bin').read_bytes();fm=json.loads((OUT/'fixture/logger.recipe.json').read_text('utf-8'))
 assert len(fixture)<0x40000-16 and (len(fixture)+4095)//4096*4096<=0x40000-4096
 assert fm['state_size']==STATE_SIZE and fm['allocation_size']==0x40000+STATE_SIZE+16
 assert sum(i.size for i in cs.disasm(fixture,0))==len(fixture)
 for row in fm['recipe']:assert fixture[row['offset']:row['offset']+len(bytes.fromhex(row['bytes']))].hex()==row['bytes']
 # New decoder: two positive guard types, padding distinction, bounded
 # negative binding/reach/operand/reserved cases, and complete read stability.
 plan=0x30000000+rw;ab=0x30000000;owner=123;shared=dict(status=5,reason=25,owner=0,civ=8,generation=7,scope=0,guard=0,raw_t=5,departures=1,slots=1,path_queries=1,context=1,context_error=0,classified=8,prefix_count=8)
 state=bytearray(STATE_SIZE)
 def put(off,n):struct.pack_into('<I',state,off,n)
 for field,off in dict(status=0,reason=4,owner=8,civ=12,generation=32,scope=36,guard=40,raw_t=44,departures=76,slots=80,path_queries=84,context=212,classified=220,prefix_count=224).items():put(off,shared[field])
 put(0x78800,owner);put(0x78804,7);put(0x79800,7);put(0x18200,42);put(0x18204,1);put(0x40600+72,2)
 def read(off,size):assert 0<=off<off+size<=STATE_SIZE and size<=2048;return bytes(state[off:off+size])
 def make(edge):
  raw=bytearray(256);f=dict(valid=1,schema=1,size=256,edge=edge,reached=required_mask(edge),owner=owner,generation=7,civ=8,plan_identity=plan,invocation=1,query=1,slot=0,prefix=0,role=2,departure=0,rawID=42,kind=1,type=5,native_EAX=0 if edge==4 else 1,postcontext=0,canary1=0x3456ab89,canary2=0x4567bc90,capacity=1,count=1,pointer=0x12340000,pointer_end=0x12340008,bounds=0,first_entry=0x12340000,first_conversion=1,source_conversion=1)
  for pair,prefix in [('finalize_selection','select'),('selection_cached','cache'),('cached_direct','direct')]:f[prefix+'_call']=manifest['path_diagnostic']['calls'][pair]['call_rva'];f[prefix+'_return_site']=manifest['path_diagnostic']['calls'][pair]['return_rva']
  for name,value in f.items():struct.pack_into('<I',raw,FIELDS[name],value)
  if edge==11:struct.pack_into('<I',raw,FIELDS['first_actual'],1)
  return raw
 cases=[]
 for name,edge,field,value,accept in [('native0',4,None,None,True),('endpoint11',11,None,None,True),('stalegeneration',4,'generation',8,False),('wrongcallpair',4,'cache_return_site',1,False),('missingreached',4,'reached',required_mask(4)&~4,False),('badsourceID',4,'rawID',43,False),('wrongpredicate',4,'native_EAX',1,False),('incompletepropagation',4,'direct_return',1,False),('reserved',4,None,None,False)]:
  raw=make(edge)
  if field:struct.pack_into('<I',raw,FIELDS[field],value)
  if name=='reserved':raw[216]=1
  result=decode_path(bytes(raw),shared,read(0x78800,8),read,plan,ab,manifest,sha(OUT/'candidate-manifest.json'));assert result['usable_diagnostic_evidence']==accept,(name,result)
  cases.append(dict(name=name,accepted=accept))
 zero=decode_path(bytes(256),shared,read(0x78800,8),read,plan,ab,manifest,'own-fixture')
 assert zero['observed']['source']=='ONBEREIKT' and zero['observed']['query']=='ONBEREIKT' and not zero['usable_diagnostic_evidence']
 cases.append(dict(name='unreached_initialized_bytes',accepted=False))
 raw=make(12);struct.pack_into('<H',raw,FIELDS['first_actual']+6,0xaabb)
 result=decode_path(bytes(raw),shared,read(0x78800,8),read,plan,ab,manifest,'own-fixture');assert result['usable_diagnostic_evidence'] and result['observed']['first_actual']['xyz']==[0,0,0] and result['observed']['first_actual']['padding_u16']==0xaabb
 cases.append(dict(name='DWORD4_padding_mismatch_is_separate',accepted=True))
 state[0x79804:0x79904]=make(4);raw,snap=stable_record(read,shared);assert raw==make(4)
 count=0
 def changing(off,size):
  nonlocal count
  value=bytearray(read(off,size))
  if off==0x79804 and size==256:
   count+=1
   if count==2:value[112]^=1
  return bytes(value)
 try:stable_record(changing,shared)
 except ValueError:pass
 else:raise AssertionError('same valid marker hid changed full record')
 cases.extend([dict(name='complete_stable_twice',accepted=True),dict(name='same_valid_changed_payload',accepted=False)])
 # Saved real SCI0 and scope17 remain separate from synthetic decoder tests.
 from partial_diagnostic import science_result,scope_header
 actual_path=ROOT/'PROEVEN/science-bezet-centrum-host/20261020/host1/variant/T1.json'
 actual=json.loads(actual_path.read_text('utf-8-sig'))['state']['shared_last_pass']['unselected_partial_pass_diagnostic']
 raw0=bytes.fromhex(next(o['rawhex'] for o in actual['objects'] if o['kind']=='ScienceResult' and o['index']==0));scenario=science_result.decode(raw0)['computed_current'];assert [x['margin_x2_i64'] for x in scenario['steps']]==[35,30,25]
 scopes=[x for x in actual['scope_excluded_centers'] if x['prefix_index']==3];assert len(scopes)==1 and scopes[0]['food'] is None and scopes[0]['consistent']
 spec=importlib.util.spec_from_file_location('SELECT25_bound_reader',OUT/'reader/Lees-Uitbreiding.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader);binding=reader.trusted_binding('U30-40');assert binding['shared_plan_rva']==rw and binding['shared_plan_size']==STATE_SIZE
 write('recipe-preservation.json',dict(entire_historical_recipe_preserved_after_named_logger_removal=True,old_rows=len(oldrows),new_rows=len(rows),logger_blocks=len(logger_blocks),equivalent_postcontext_read_groups=context_groups,verified_relocations=relocated,edges=edges,record_capture_operands=captures))
 result=dict(stage='C2_BYTES_OWN_DECODER_NOT_NATIVE_NOT_HOST',candidate_sha256=manifest['candidate_sha256'],manifest_sha256=sha(OUT/'candidate-manifest.json'),state_rva=hex(rw),state_size=STATE_SIZE,Plan_and_generation_offset=0x79800,PE_checksum=True,PE_RX_RW=True,RW_zero=True,relocations_unchanged=True,B2_H3_padding_unchanged=True,entire_policy_SCI_development_recipe_preserved=True,direct_rel32_targets_checked=direct,logger_blocks=len(logger_blocks),edge_landings=len(edges),callpairs=manifest['path_diagnostic']['calls'],fixture_bytes=len(fixture),fixture_RX_page_end=hex((len(fixture)+4095)//4096*4096),fixture_Plan_minus16=hex(0x40000-16),fixture_fully_decoded=True,decoder_cases=cases,real_saved_SCI0_margins=[35,30,25],real_saved_scope17_food=None,actual_saved_T1_sha256=sha(actual_path),offline_bound_reader=True,native_compiled=False,native_run=False,installed=False,gameplay_proven=False)
 write('candidate-static-checks.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('callpairs','decoder_cases')}))
if __name__=='__main__':main()
