"""Two small own-image observers for the newly emitted occupied validator.

No native execution. Original C1 sources/pins stay intact. Observers preserve
GPR/flags, replay complete overwritten instructions and jump back. No x87.
"""
from pathlib import Path
import json,struct,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'PROEVEN/production-h3'))
from x86 import X86,mem as m

def main():
 gate=json.loads((OUT/'ROOT-BRONREVIEW.json').read_text('utf-8'))
 assert gate['fixture_emit_allowed'] and not gate['native_allowed'] and not gate['host_allowed']
 manifest=json.loads((OUT/'candidate-manifest.json').read_text('utf-8'))
 rows=manifest['recipe'];labels=manifest['labels'];ext=int(manifest['components']['extension_rva'],16)
 bad=labels['sci_food_diag_bad'];done=labels['sci_food_diag_done']
 entry=next(i for i,row in enumerate(rows) if bad<row['offset']<done and row['asm']=='diagnostic pushfd')
 start=rows[entry]['offset'];first=rows[entry:entry+3]
 assert [r['asm'] for r in first]==['diagnostic pushfd','diagnostic pushad',"mov ('ebp', -348),0"]
 original_entry=b''.join(bytes.fromhex(r['bytes']) for r in first);assert len(original_entry)==12
 finish=next(r for r in rows if start<r['offset']<done and r['asm']=="mov eax,('ebp', -348)")
 original_exit=bytes.fromhex(finish['bytes']);assert len(original_exit)==6
 bound=dict(validator_entry_rva=ext+start,entry_overwrite_size=12,entry_original_hex=original_entry.hex(),entry_continue_rva=ext+start+12,validator_exit_rva=ext+finish['offset'],exit_overwrite_size=6,exit_original_hex=original_exit.hex(),exit_continue_rva=ext+finish['offset']+6)
 for name,off,replay,continuation,record,count in [('validator_entry',start,original_entry,0xa88,0xa00,0xa80),('validator_exit',finish['offset'],original_exit,0xa8c,0xa40,0xa84)]:
  r=X86();fixups=[]
  def fix(text,op,offset):
   r.emit(text,op+'00000000');fixups.append(dict(at=len(r.code)-4,context_offset=offset))
  r.op('observer pushfd',b'\x9c');r.op('observer pushad',b'\x60');r.mov('esi','esp');fix('own nineword GPR/flags snapshot','bf',record);r.mov('ecx',9);r.op('cld',b'\xfc');r.op('rep movsd',b'\xf3\xa5')
  fix('increment own observer count','ff05',count)
  if name=='validator_exit':r.mov('eax',m('ebp',-348));fix('observed private returnspill','a3',0xa90)
  r.op('observer popad',b'\x61');r.op('observer popfd',b'\x9d')
  # Replay each original instruction as an individual complete recipe row.
  for row in first if name=='validator_entry' else [finish]:r.op('replay '+row['asm'],bytes.fromhex(row['bytes']))
  fix('continue original validator/epilogue','ff25',continuation)
  raw=r.finish();(OUT/'fixture'/(name+'.bin')).write_bytes(raw)
  (OUT/'fixture'/(name+'.recipe.json')).write_text(json.dumps(dict(recipe=r.rows,fixups=fixups,labels=r.labels),indent=2)+'\n','utf-8')
 (OUT/'fixture/validator-observer-binding.json').write_text(json.dumps(bound,indent=2)+'\n','utf-8')
 print('Emitted two finite own-image observer wrappers; no native execution')
if __name__=='__main__':main()
