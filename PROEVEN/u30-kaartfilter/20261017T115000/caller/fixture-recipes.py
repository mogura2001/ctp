"""Four own caller-control stubs. SOURCE ONLY until separate root native gate.

Uses the existing B4 finite emitter/recipe fixup form, not an engine loader.
"""
from pathlib import Path
import json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'PROEVEN/production-h3'))
from x86 import X86,mem as m

def begin():
 r=X86();r.prologue(0);r.emit('own fixture inputstate, never candidate','bb00000000')
 return r,[dict(at=len(r.code)-4,context_offset=0)]
def end(name,r,fix,pop):
 r.epilogue(0,pop);folder=OUT/'helper';folder.mkdir(exist_ok=True)
 (folder/(name+'.bin')).write_bytes(r.finish())
 (folder/(name+'.recipe.json')).write_text(json.dumps(dict(recipe=r.rows,fixups=fix,labels=r.labels),indent=2)+'\n','utf-8')
def pointer_index(r,arg,bad):
 r.mov('eax',m('ebp',arg));r.alu('cmp','eax',m('ebx',8));r.j('jb',bad);r.alu('cmp','eax',m('ebx',12));r.j('jae',bad);r.alu('sub','eax',m('ebx',8));r.test('eax',7);r.j('jnz',bad);r.shift('shr','eax',3)

def main():
 # state: plan0/world4/captureStart8/captureEnd12/badKeyIndex20,
 # keyCalls32/gateCalls36/abiErrors40/h3Calls44/h3Status48/h3Reason52,
 # scoreSkipBelow56; gate return table begins0x1000 (4096DWORDs).
 r,f=begin();r.unary('inc',m('ebx',32));pointer_index(r,12,'key_bad')
 r.alu('cmp','eax',m('ebx',20));r.j('je','key_bad');r.mov('ecx',m('ebp',12));r.mov('edx',m('ebp',16))
 for off in (0,4):r.mov('eax',m('ecx',off));r.mov(m('edx',off),'eax')
 r.mov('eax',1);r.j('jmp','key_done');r.label('key_bad');r.mov('eax',0);r.label('key_done');r.mov('ecx',0x11112222);r.mov('edx',0x33334444);end('key',r,f,12)
 r,f=begin();r.unary('inc',m('ebx',36));r.mov('eax',m('ebp',8));r.alu('cmp','eax',m('ebx',4));r.j('jne','gate_bad');pointer_index(r,12,'gate_bad');r.shift('shl','eax',2);r.alu('add','eax','ebx');r.mov('eax',m('eax',0x1000));r.j('jmp','gate_done');r.label('gate_bad');r.unary('inc',m('ebx',40));r.mov('eax',0);r.label('gate_done');r.mov('ecx',0x55556666);r.mov('edx',0x77778888);end('gate',r,f,8)
 r,f=begin();r.mov('eax',m('ebp',8));r.alu('cmp','eax',m('ebx',4));r.j('jne','score_bad');r.mov('eax',m('ebp',12));r.alu('cmp','eax',m('ebx',56));r.j('jl','score_zero');r.mov('eax',1);r.j('jmp','score_done');r.label('score_bad');r.unary('inc',m('ebx',40));r.label('score_zero');r.mov('eax',0);r.label('score_done');end('score',r,f,16)
 r,f=begin();r.unary('inc',m('ebx',44));r.mov('edi',m('ebp',20));r.zero('edi',1024);r.mov('edi',m('ebp',20));r.mov('eax',m('ebx',48));r.mov(m('edi'),'eax');r.mov('edx',m('ebx',52));r.mov(m('edi',4),'edx');r.mov(m('edi',8),1);end('h3',r,f,16)

if __name__=='__main__':main()
