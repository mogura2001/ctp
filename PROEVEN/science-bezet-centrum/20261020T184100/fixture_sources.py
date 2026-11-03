"""Limited changed-path own fixtures; source only until separate root gate.

Reuses shim5/convert/food and the parent's finite own-image mechanism. No
37-edge loop. No engine/RPM/process/GUI APIs. Real SCI frame548 and x87 save
-144..-37: NEVER place an out40 upper canary at -144 in these wrappers.
"""
from pathlib import Path
import json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'PROEVEN/production-h3'))
from x86 import X86,mem as m
from science_layout import KERNEL_FRAME_SIZE,RESULT_SIZE

def recipes():
 def start():return X86(),[]
 def fix(r,items,text,op,off):
  r.emit(text,op+'00000000');items.append(dict(at=len(r.code)-4,context_offset=off))
 def finish(r,items):return dict(code=r.finish(),recipe=r.rows,fixups=items,labels=r.labels)
 r,f=start();r.prologue(KERNEL_FRAME_SIZE)
 r.fp('fnsave real SCI x87 area','dd',6,m('ebp',-144));r.fp('fldcw caller','d9',5,m('ebp',-144))
 r.push(m('ebp',24));r.lea('eax',m('ebp',-184));r.push('eax');r.push(m('ebp',16));r.push(m('ebp',12));r.push(m('ebp',8))
 fix(r,f,'pinned SCI return site in own image','ff35',32);fix(r,f,'real clone or original reader','ff25',36)
 r.label('continuation');r.mov(m('ebp',-16),'eax')
 r.lea('esi',m('ebp',-184));r.mov('edi',m('ebp',20));r.mov('ecx',10);r.op('cld',b'\xfc');r.op('rep movsd',b'\xf3\xa5')
 r.mov('eax',m('ebp',-16));r.fp('frstor exact caller state','dd',4,m('ebp',-144));r.epilogue(KERNEL_FRAME_SIZE,20)
 normal=finish(r,f)
 # Converter first does its old eight-byte copy; optional mutation changes
 # only an explicitly owned Plan/frame address. This tests fresh validation
 # after valid entry admission. It does not model a naturally changing game.
 r,f=start();r.mov('edx',m('esp',4));r.mov('eax',m('edx'));r.mov(m('ecx'),'eax');r.mov('eax',m('edx',4));r.mov(m('ecx',4),'eax')
 r.op('pushfd',b'\x9c');r.op('pushad',b'\x60')
 fix(r,f,'own mutation mode','a1',0x90c);r.test('eax','eax');r.j('jz','mutation_done')
 fix(r,f,'owned absolute ptr or signed frame offset','8b15',0x900)
 r.alu('cmp','eax',2);r.j('jne','mutation_ptr_ready');r.alu('add','edx','ecx');r.alu('add','edx',28)
 r.label('mutation_ptr_ready');fix(r,f,'owned mutation value','a1',0x904);r.mov(m('edx'),'eax')
 r.label('mutation_done');r.op('popad',b'\x61');r.op('popfd',b'\x9d');r.op('ret4',b'\xc2\x04\x00')
 convert=finish(r,f)
 # Isolated real consumer-continuation probe, not a complete SCI execution.
 # The parent returnsite is patched only in the private mapped fixture image.
 r,f=start();r.prologue(KERNEL_FRAME_SIZE)
 r.fp('fnsave real SCI x87 area','dd',6,m('ebp',-144));r.fp('fldcw caller','d9',5,m('ebp',-144))
 r.zero(m('ebp',24),RESULT_SIZE);r.mov('edi',m('ebp',24));r.mov(m('edi',8),1);r.mov(m('edi',12),3);r.mov(m('edi',4),11);r.mov(m('edi',16),1)
 for off in (28,32,36):r.mov(m('edi',off),-1)
 r.mov(m('ebp',-220),0);r.lea('esi',m('edi',128))
 fix(r,f,'injected private return value','a1',0x944);fix(r,f,'actual center/tile continuation','ff25',0x940)
 model=finish(r,f)
 r,f=start();r.emit('record food-consumer reached in own context','c7050000000001000000');f.append(dict(at=len(r.code)-8,context_offset=0x948))
 fix(r,f,'actual science_done includes frstor and ret20','ff25',0x94c)
 consumer=finish(r,f)
 return dict(normal=normal,convert_mutation=convert,model_probe=model,consumer_observer=consumer)

def main():
 gate=json.loads((OUT/'ROOT-BRONREVIEW.json').read_text('utf-8'))
 if not gate.get('fixture_emit_allowed'):raise ValueError('Separate root fixture source release required')
 folder=OUT/'fixture';folder.mkdir(exist_ok=True)
 for name,data in recipes().items():
  (folder/(name+'.bin')).write_bytes(data['code'])
  (folder/(name+'.recipe.json')).write_text(json.dumps({k:v for k,v in data.items() if k!='code'},indent=2)+'\n','utf-8')
 print('Limited own fixture emission only; no native run')
if __name__=='__main__':main()
