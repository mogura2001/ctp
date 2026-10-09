"""Finite static checks of PREPARED emission; does not assert native acceptance."""
from pathlib import Path
import sys,json,hashlib,struct,runpy
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
builder=runpy.run_path(str(OUT/'build.py'))
compose=builder['compose'];ORIGINAL=builder['ORIGINAL'];SITES=builder['SITES'];ORIGINAL_CALLS=builder['ORIGINAL_CALLS']
sha=lambda b:hashlib.sha256(b).hexdigest()
original=(ROOT/'PROEVEN/production-h3/backup/robotcom.original.dll').read_bytes();op=pefile.PE(data=original);assert sha(original)==ORIGINAL
md=Cs(CS_ARCH_X86,CS_MODE_32);results=[]
for N in (25,30):
 for enabled in (False,True):
  name=('B4' if enabled else 'BASELINE')+'-N'+str(N);data=(OUT/(name+'.prepared.dll')).read_bytes();code=(OUT/(name+'.payload.bin')).read_bytes();manifest=json.loads((OUT/(name+'.manifest.json')).read_text());p=pefile.PE(data=data)
  regen,rc,rm=compose(N,enabled);assert (data,code,manifest)==(regen,rc,rm)
  expected=bytearray(original);used=set()
  for delta in manifest['changes']:
   at=int(delta['offset'],16);before=bytes.fromhex(delta['before']);after=bytes.fromhex(delta['after']);assert len(before)==len(after);assert original[at:at+len(before)]==before;assert not used.intersection(range(at,at+len(before)));used.update(range(at,at+len(before)));expected[at:at+len(after)]=after
  assert data[:len(original)]==expected;assert data[len(original):len(original)+len(code)]==code;assert not any(data[len(original)+len(code):])
  assert p.FILE_HEADER.NumberOfSections==(6 if enabled else 5)
  assert [(s.VirtualAddress,s.PointerToRawData,s.SizeOfRawData,s.Characteristics) for s in p.sections[:4]]==[(s.VirtualAddress,s.PointerToRawData,s.SizeOfRawData,s.Characteristics) for s in op.sections]
  assert [(d.VirtualAddress,d.Size) for d in p.OPTIONAL_HEADER.DATA_DIRECTORY]==[(d.VirtualAddress,d.Size) for d in op.OPTIONAL_HEADER.DATA_DIRECTORY]
  assert p.sections[4].VirtualAddress==0xd4000 and p.sections[4].Characteristics==0x60000020
  assert p.OPTIONAL_HEADER.CheckSum==p.generate_checksum() and p.OPTIONAL_HEADER.SizeOfImage%4096==0 and len(data)%512==0
  decoded=0
  if enabled:
   assert p.sections[5].Characteristics==0xc0000040
   base=int(manifest['components']['B4']['rva'],16);rows=[];boundaries=set()
   for recipe in manifest['recipe']:
    if recipe['asm'].startswith('constant '):continue
    b=bytes.fromhex(recipe['bytes']);instructions=list(md.disasm(b,base+recipe['offset']));assert sum(i.size for i in instructions)==len(b),recipe;rows.extend(instructions);boundaries.update(i.address for i in instructions)
   external=set(ORIGINAL_CALLS.values())
   # Declared H3/B2 helper labels are linked at their real component RVAs.
   external.update(base+manifest['labels'][k] for k in ('H3Classifier','H3Host','H3PosCompare','B2Host','B2Symbols','B2Bit'))
   for i in rows:
    if (i.mnemonic.startswith('j') or i.mnemonic=='call') and i.op_str.startswith('0x'):assert int(i.op_str,16) in boundaries|external,(hex(i.address),i.op_str)
    assert 'ptr [0x' not in i.op_str,(hex(i.address),i.op_str)
   for hook,site,preimage in SITES:
    at=p.get_offset_from_rva(site);b=data[at:at+5];assert b[0]==0xe8;assert site+5+struct.unpack('<i',b[1:])[0]==base+manifest['labels'][hook]
   decoded=len(rows)
  results.append(dict(name=name,sha256=sha(data),deterministic=True,declared_PE_diff_CFG=True,B4_decoded_instructions=decoded))
result=dict(stage='STATIC CHECKED PREPARED; native integration acceptance pending',variants=results,native_acceptance=False,installed=False,gameplay_measured=False,production_N_chosen=False)
(OUT/'prepared-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
