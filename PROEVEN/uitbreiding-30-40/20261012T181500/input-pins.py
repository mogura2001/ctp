"""Frozen, already analysed T/D inputs only. No new disassembly or binding."""
from pathlib import Path
import hashlib,sys,struct,json
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
ENGINE_HASH='b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
AI_HASH='3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
SLOTS={0xc:0x131770,0x40:0x131a50,0x44:0x131dc0,0x48:0x131de0,0xd8:0x132020,0xdc:0x132040}
ENGINE_BODIES={0x660f0:0xd4,0x543b0:0x41,0x542e0:0x30,0x131770:0xf,0x131a50:0x21,0x131dc0:0x1c,0x131de0:0x1c,0x132020:0x1c,0x132040:0x1c}
AI_BODIES={0x11bc0:0x20,0x1a970:0x10,0x1a980:0x20,0x1c380:0x20,0x1cd50:0x20,0x129f0:0x40}
def pins():
 blobs={
 'engine':(ROOT/'CTP-og/ctp_program/ctp/civctp.exe').read_bytes(),
 'ai':(ROOT/'PROEVEN/production-h3/backup/robotcom.original.dll').read_bytes()}
 assert hashlib.sha256(blobs['engine']).hexdigest()==ENGINE_HASH
 assert hashlib.sha256(blobs['ai']).hexdigest()==AI_HASH
 result=[]
 for kind,ranges in (('engine',ENGINE_BODIES),('ai',AI_BODIES)):
  pe=pefile.PE(data=blobs[kind]);rel={e.rva for b in getattr(pe,'DIRECTORY_ENTRY_BASERELOC',[]) for e in b.entries if e.type==3}
  for at,length in ranges.items():
   raw=pe.get_data(at,length);assert len(raw)==length
   reloc=[r-at for r in rel if at<=r<at+length];assert all(r+4<=length for r in reloc)
   if kind=='engine':assert not reloc,'supported engine fixed no reloc'
   result.append(dict(kind=kind,rva=at,length=length,bytes=raw.hex(),relocations=sorted(reloc)))
 return dict(engine_sha256=ENGINE_HASH,ai_sha256=AI_HASH,scope='only frozen T/D analysed read-only bodies and UnitDB slots; engine fixed400000, AI declared HIGHLOWs',slots=[dict(slot=s,rva=r) for s,r in SLOTS.items()],bodies=result)
if __name__=='__main__':
 data=pins();(Path(__file__).resolve().parent/'input-pins.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(dict(bodies=len(data['bodies']),slots=len(data['slots']))))
