"""SOURCE ONLY. Emits seven finite caller stubs after root source release.

No loader, engine, candidate rebuild or native execution. Reuses X86 and
the previous gate/score recipe. Stub SCI is synthetic input, not engine SCI.
"""
from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
sys.path.insert(0, str(ROOT / 'PROEVEN/production-h3'))
from x86 import X86, mem as m


def begin(size=0):
    r = X86(); r.prologue(size); r.emit('own input state', 'bb00000000')
    return r, [dict(at=len(r.code)-4, context_offset=0)]


def save(name, r, fix, pop):
    r.epilogue(0, pop)
    folder = OUT / 'helper'; folder.mkdir(exist_ok=True)
    (folder / (name+'.bin')).write_bytes(r.finish())
    (folder / (name+'.recipe.json')).write_text(json.dumps(
        dict(recipe=r.rows, fixups=fix, labels=r.labels), indent=2)+'\n')


def main():
    # state 0 Plan,4 World,8/12 capture bounds;20 invalidkeyindex (unused).
    # 32 keycalls,36 gatecalls,40 ABIerrors,44 H3calls,48 H3status,
    # 56 BskipBelow,60 SCIcalls,64 SCIcontextmutation,68 scorecontextmutation,
    # 72 endpointcalls,76 pathcalls,88 final_combine address.
    folder = OUT / 'helper'; folder.mkdir(exist_ok=True)
    old = ROOT/'PROEVEN/u30-kaartfilter/20261017T115000/caller/helper'
    for suffix in ('.bin', '.recipe.json'):
        (folder/('gate'+suffix)).write_bytes((old/('gate'+suffix)).read_bytes())
    r,f = begin(); r.unary('inc',m('ebx',32)); r.mov('ecx',m('ebp',12))
    r.alu('cmp','ecx',m('ebx',0)); r.j('jb','bad')
    r.mov('eax',m('ebx',0)); r.alu('add','eax',0x79800-8)
    r.alu('cmp','ecx','eax'); r.j('ja','bad')
    r.mov('edx',m('ebp',16))
    for off in (0,4):r.mov('eax',m('ecx',off));r.mov(m('edx',off),'eax')
    r.mov('eax',1);r.j('jmp','done');r.label('bad');r.mov('eax',0)
    r.label('done');save('key',r,f,12)

    r,f=begin();r.alu('cmp',m('ebx',68),0);r.j('je','score')
    r.mov('eax',m('ebx'));r.unary('inc',m('eax',8))
    r.label('score');r.mov('eax',1);save('score',r,f,16)

    r,f=begin();r.unary('inc',m('ebx',44));r.mov('edi',m('ebp',20))
    r.zero('edi',1024);r.mov('edi',m('ebp',20))
    r.mov('eax',m('ebx',48));r.mov(m('edi'),'eax');r.mov(m('edi',8),1)
    r.mov(m('edi',68),1);r.mov(m('edi',96),4)
    r.mov('esi',m('ebp',16));r.mov('edx',m('esi'))
    for i in range(4):
        r.mov(m('edi',100+4*i),i);r.mov('eax','edx')
        r.alu('add','eax',i+1);r.mov(m('edi',144+12*i),'eax')
    r.mov('eax',m('ebx',48));save('h3',r,f,16)

    r,f=begin();r.unary('inc',m('ebx',60));r.mov('edi',m('ebp',24))
    r.zero('edi',2048);r.mov('edi',m('ebp',24));r.mov(m('edi'),2)
    r.mov(m('edi',112),1);r.mov(m('edi',16),3)
    r.mov('esi',m('ebp',16));r.mov('edx',m('esi'))
    for off in (0,4):r.mov('eax',m('esi',off));r.mov(m('edi',116+off),'eax')
    for i in range(3):
        r.mov(m('edi',28+4*i),i);r.mov('eax','edx')
        r.alu('add','eax',11+i);r.mov(m('edi',128+96*i),'eax')
    r.alu('cmp',m('ebx',64),0);r.j('je','done')
    r.mov('eax',m('ebx'));r.unary('inc',m('eax',8))
    r.label('done');r.mov('eax',2);save('science',r,f,20)

    for name,pop,offset in [('endpoint',12,72),('path',12,76)]:
        r,f=begin();r.unary('inc',m('ebx',offset));r.mov('eax',1);save(name,r,f,pop)

    # Match finalize_pass's prologue exactly; native final_combine/final_done
    # execute unchanged. No policy/Actual simulation is substituted here.
    r,f=begin(112);r.mov('eax',m('ebx',88));r.mov('ebx',m('ebx'))
    r.op('jmp eax',b'\xff\xe0')
    (folder/'combine.bin').write_bytes(r.finish())
    (folder/'combine.recipe.json').write_text(json.dumps(
        dict(recipe=r.rows,fixups=f,labels=r.labels),indent=2)+'\n')


if __name__ == '__main__':main()
