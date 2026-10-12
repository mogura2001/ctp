"""Own controlled native inputs, never emitted into a candidate or engine.

Fixture code records ABI arguments and supplies explicit own-memory outputs.
Producer and H3 current-model code remain the actual composed emitted bodies.
"""
from pathlib import Path
import sys,json,struct
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parents[1]/'PROEVEN/production-h3'))
from x86 import X86,mem as m
HELP=OUT/'helper';HELP.mkdir(exist_ok=True)

def save(name,r,fix):
 (HELP/(name+'.bin')).write_bytes(r.finish())
 (HELP/(name+'.recipe.json')).write_text(json.dumps(dict(recipe=r.rows,fixups=fix,labels=r.labels),indent=2)+'\n')
def begin():
 r=X86();fix=[];r.prologue(0)
 r.emit('own fixture inputstate, never candidate','bb00000000');fix.append(dict(at=len(r.code)-4,context_offset=0))
 return r,fix
def end(name,r,fix,pop):
 r.epilogue(0,pop);save(name,r,fix)
def count(r,slot):r.unary('inc',m('ebx',slot))

# Fields are fixture-owned ABI controls/observations, not engine layout.
# owner=0; presencepointer=4; threatpointer=8; presencexyz=12/16;
# terrain=20; unitpresence=24; citypresence=28; threat double=32;
# host=40; continent=44; land=48; count=52; settlertype=56;
# resolverok=60; categoryOther=64; trait=68; engineposition=72/76;
# invalidID=80; positionok=84; pathresult=88; pointptr=92; capacity=96;
# pointcount=100; cutoff=104; freecount=108; freeptr=112;
# pathargs=128..207; presence9pointers=208..243;
# H3binding=256..279; query counters=280+; selector state etc=400+
for name,pop,field in [('owner',8,0),('interfacecount',4,52),('trait',8,68)]:
 r,f=begin();r.mov('eax',m('ebx',field));end(name,r,f,pop)
for name,pop,value in [('true4',4,1),('true8',8,1),('true12',12,1),('false8',8,0)]:
 r,f=begin();r.mov('eax',value);end(name,r,f,pop)
r,f=begin();r.mov('eax',0);end('noop',r,f,0)
r,f=begin();r.mov('edx',m('ebp',16));r.mov('eax',m('ebx',20));r.mov(m('edx'),'eax');r.mov('eax',1);end('terrain',r,f,12)
r,f=begin();r.mov('eax',m('ebp',12));r.mov(m('ebx',4),'eax')
for off in (0,4):r.mov('edx',m('eax',off));r.mov(m('ebx',12+off),'edx')
for i in range(9):
 r.mov('edx',m('ebp',16+4*i));r.mov(m('ebx',208+4*i),'edx');r.mov(m('edx'),0)
for i,field in ((0,0),(1,24),(4,28)):
 r.mov('edx',m('ebp',16+4*i));r.mov('eax',m('ebx',field));r.mov(m('edx'),'eax')
count(r,280);r.mov('eax',1);end('presence',r,f,44)
r,f=begin();r.mov('eax',m('ebp',12));r.mov(m('ebx',8),'eax');r.mov('edx',m('ebp',16))
for off in (0,4):r.mov('eax',m('ebp',12));r.mov('eax',m('eax',off));r.mov(m('edx',off),'eax')
end('playerconvert',r,f,12)
r,f=begin();r.fp('fld controlled threat','dd',0,m('ebx',32));end('threat',r,f,4)
r,f=begin()
for arg,field in ((16,44),(20,48)):
 r.mov('edx',m('ebp',arg));r.mov('eax',m('ebx',field));r.mov(m('edx'),'eax')
r.mov('eax',1);end('continent',r,f,16)
r,f=begin();r.mov('edx',m('ebp',8))
for off in (0,4):r.mov('eax',m('edx',off));r.mov(m('ecx',off),'eax')
end('convert',r,f,4)
r,f=begin();r.mov('eax',m('ebx',40));end('host',r,f,0)
r,f=begin();r.mov('edi',m('ebp',16))
for off in range(0,24,4):r.mov('eax',m('ebx',256+off));r.mov(m('edi',off),'eax')
r.mov('eax',1);end('h3host',r,f,12)
r,f=begin();r.mov('edx',m('ebp',8));count(r,284)
for i,v in enumerate(b'UNIT_SETTLER\0'):
 r.load('eax',m('edx',i),'sx8');r.alu('cmp','eax',v);r.j('jne','bad')
r.alu('cmp',m('ebx',60),1);r.j('jne','bad');r.mov('edx',m('ebp',12));r.mov(m('edx'),123);r.mov('eax',1);r.j('jmp','done');r.label('bad');r.mov('eax',0);r.label('done');end('stringlookup',r,f,8)
r,f=begin();count(r,288);r.alu('cmp',m('ebp',8),123);r.j('jne','bad');r.mov('edx',m('ebp',12));r.mov('eax',m('ebx',56));r.mov(m('edx'),'eax');r.mov('eax',1);r.j('jmp','done');r.label('bad');r.mov('eax',0);r.label('done');end('typelookup',r,f,8)
r,f=begin();count(r,292);r.mov('eax',m('ebp',12));r.alu('cmp','eax',m('ebx',56));r.j('jne','other');r.mov('eax',1);r.j('jmp','done');r.label('other');r.mov('eax',m('ebx',64));r.label('done');end('category',r,f,8)
r,f=begin();count(r,296);r.mov('edx',m('ebp',16));r.mov('eax',m('ebx',80));r.mov(m('edx'),'eax');r.mov('edx',m('ebp',20))
for off in (0,4):r.mov('eax',m('ebx',72+off));r.mov(m('edx',off),'eax')
r.mov('eax',m('ebx',84));end('currentpos',r,f,16)
r,f=begin();count(r,300)
for i in range(20):r.mov('eax',m('ebp',8+4*i));r.mov(m('ebx',128+4*i),'eax')
for arg,field in ((36,96),(40,92),(44,100),(48,104),(72,104)):
 r.mov('edx',m('ebp',arg));r.mov('eax',m('ebx',field));r.mov(m('edx'),'eax')
r.mov('edi',m('ebx',92));r.test('edi','edi');r.j('jz','copydone');r.mov('eax',m('ebx',100));r.alu('cmp','eax',1);r.j('jl','copydone');r.alu('cmp','eax',3);r.j('jg','copydone');r.mov('esi',m('ebp',28))
for off in (0,4):r.mov('eax',m('esi',off));r.mov(m('edi',off),'eax')
r.mov('eax',m('ebx',100));r.unary('dec','eax');r.shift('shl','eax',3);r.alu('add','edi','eax');r.mov('esi',m('ebp',32))
for off in (0,4):r.mov('eax',m('esi',off));r.mov(m('edi',off),'eax')
r.label('copydone');r.alu('cmp',m('ebx',324),0);r.j('je','nocutoff');r.mov('edx',m('ebx',40));r.mov(m('edx',0x6d0b94),1);r.label('nocutoff')
r.mov('eax',m('ebx',88));end('path',r,f,80)
r,f=begin();count(r,108);r.mov('eax',m('ebp',8));r.mov(m('ebx',112),'eax');end('free',r,f,0)
r,f=begin();r.mov('eax',m('ebx',400));end('canbuild',r,f,8)
r,f=begin();r.mov('eax',m('ebx',404));end('citycount',r,f,0)
r,f=begin();count(r,408);r.mov('eax',0x12345678);end('scheduler',r,f,0)
r,f=begin();count(r,412);r.mov('eax',0x23456789);end('ground',r,f,4)
# Actual H3 model inputs: available places and terrain/current food are supplied
# from owned grid records, so G is computed by the emitted producer/model.
r,f=begin();r.mov('edx',m('ebp',20));r.mov(m('edx'),4);r.mov('edi',m('ebp',24));r.mov('esi',m('ebp',16))
for i in range(4):
 r.load('eax',m('esi'),'zx16');r.alu('cmp',m('ebx',332),0);r.j('je','usecenter'+str(i));r.mov('eax',m('ebx',332));r.label('usecenter'+str(i));r.alu('add','eax',i+1);r.mov(m('edi',8*i),'eax');r.mov(m('edi',8*i+4),0)
r.mov('eax',1);end('h3open',r,f,20)
for name,field in [('gridterrain',512),('gridfood',516)]:
 r,f=begin();r.mov('edx',m('ebp',12));r.load('eax',m('edx'),'zx16');r.shift('shl','eax',2);r.mov('edx',m('ebx',field));r.alu('add','edx','eax');r.mov('eax',m('edx'));r.mov('edx',m('ebp',16));r.mov(m('edx'),'eax');r.mov('eax',1);end(name,r,f,12)
r,f=begin();r.mov('eax',100);end('score',r,f,16)
# Owner controls can target one observed external x coordinate. Other points
# remain at the controlled default owner. This exposes endpoint/midpath gates.
r,f=begin();r.mov('edx',m('ebp',12));r.load('eax',m('edx'),'sx16');r.alu('cmp','eax',m('ebx',316));r.j('jne','default');r.mov('eax',m('ebx',320));r.j('jmp','done');r.label('default');r.mov('eax',m('ebx'));r.label('done');end('pointowner',r,f,8)
print(json.dumps(dict(helper_bins=len(list(HELP.glob('*.bin'))),controlled_inputs_only=True)))
