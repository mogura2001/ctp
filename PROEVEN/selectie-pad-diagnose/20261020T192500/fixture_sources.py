"""Small existing X86/Trace/shim5 own-image fixtures; SOURCE ONLY.

 Isolated real logger, fabricated own frames/operands. This is not the path
 engine, not sixteen natural path scenarios and not a gameplay simulation.
 No production compose/import here. Root must separately permit emission.
 """
from pathlib import Path
import json,sys,struct
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]

def recipes():
 gate=json.loads((OUT/'ROOT-BRONREVIEW.json').read_text('utf-8'))
 if gate.get('fixture_emit_allowed') is not True:raise ValueError('Separate root fixture emission gate required')
 sys.path.insert(0,str(ROOT/'PROEVEN/production-h3'));sys.path.insert(0,str(OUT))
 from x86 import X86,mem as m
 from path_diagnostic import Trace
 from path_diagnostic_layout import STATE_SIZE
 class Located0(X86):
  # Parent Recipe.finish has a fixed d4000 base. Fixture code is mapped at
  # image+0, so use the existing Located finish algorithm with base0.
  def finish(self):
   for at,label,absolute in self.fix:
    assert label in self.labels,label
    value=self.labels[label] if absolute else self.labels[label]-at-4
    struct.pack_into('<I' if absolute else '<i',self.code,at,value)
   for row in self.rows:row['bytes']=self.code[row['offset']:row['offset']+len(bytes.fromhex(row['bytes']))].hex()
   return bytes(self.code)
 r=Located0();r.labels['pass_state']=0x40000
 def start(name,size):r.label(name);r.prologue(size);r.mov('ebx',m('ebp',8))
 def snap(off):
  r.op('fixture pushfd',b'\x9c');r.op('fixture pushad',b'\x60');r.mov('esi','esp');r.lea('edi',m('ebx',off));r.mov('ecx',9);r.op('fixture cld',b'\xfc');r.op('fixture rep movsd',b'\xf3\xa5');r.op('fixture popad',b'\x61');r.op('fixture popfd',b'\x9d')
 start('entry',32);r.push('ebx');r.label('pd_select_call');r.j('call','selection');r.label('pd_select_return');r.epilogue(32,20)
 start('reset_entry',32);Trace(r,'reset_fixture').reset();r.mov('eax',1);r.epilogue(32,20)
 start('selection',96);s=Trace(r,'selection');s.invocation();r.mov(m('ebp',-20),0);r.mov(m('ebp',-36),0);r.lea('edi',m('ebx',0x40600));r.lea('esi',m('ebx',0x18200));s.source()
 r.push('edi');r.lea('eax',m('esi',8));r.push('eax');r.push('ebx');r.label('pd_cache_call');r.j('call','cached');r.label('pd_cache_return');r.test('eax','eax');r.j('jnz','selection_done');r.mov(m('ebx',0),0);r.mov(m('ebx',4),25);s.publish();r.label('selection_done');r.epilogue(96,4)
 start('cached',64);r.push(m('ebp',16));r.push(m('ebp',12));r.push('ebx');r.label('pd_direct_call');r.j('call','direct');r.label('pd_direct_return');Trace(r,'cache').capture([('cache_return','eax')],['cache_return'],propagate=True);r.epilogue(64,12)
 start('direct',128);d=Trace(r,'path')
 # Wrong-argument case affects only fabricated own logger frames.
 r.alu('cmp',m('ebx',0x24680),5);r.j('jne','argument_ready');r.alu('add',m('ebp',12),8);r.label('argument_ready')
 r.unary('inc',m('ebx',84));r.mov('eax',0);r.alu('cmp',m('ebx',0x24680),2);r.j('je','endpoint');r.alu('cmp',m('ebx',0x24680),3);r.j('jne','native_ready');r.label('endpoint');r.mov('eax',1);r.label('native_ready')
 r.mov(m('ebp',-36),'eax');r.mov(m('ebp',-16),1);r.mov(m('ebp',-24),1);r.lea('edx',m('ebx',0x18600));r.mov(m('ebp',-20),'edx')
 r.alu('cmp','eax','eax');snap(0x24600)
 d.capture([('native_EAX','eax'),('capacity',m('ebp',-16)),('count',m('ebp',-24)),('pointer',m('ebp',-20)),('query',m('ebx',84))],['native_return'])
 snap(0x24630)
 d.capture([('postcontext',0)],['postcontext']);d.capture([('canary1',0x3456ab89)],['canary1']);d.capture([('canary2',0x4567bc90)],['canary2']);d.capture(bits=['raw_return_guard']);r.alu('cmp',m('ebp',-36),1);d.edge('jne',4)
 d.capture(bits=['pointer','count_min','capacity']);r.mov('eax',m('ebp',-20));r.alu('add','eax',8);d.capture([('pointer_end','eax'),('bounds',0)],['overflow'])
 d.capture([('first_entry',m('ebp',-20)),('first_conversion',1),('first_actual',1),('first_actual',0,4)],['first_conversion']);d.capture([('source_conversion',1),('source_expected',2),('source_expected',0,4)],['source_conversion'])
 r.alu('cmp',m('ebx',0x24680),3);r.j('je','normal');d.capture(bits=['first_compare']);r.mov('eax',1);r.alu('cmp','eax',2);d.edge('jne',11)
 r.label('normal');r.mov(m('ebp',-36),1);r.j('jmp','path_free')
 r.label('path_unknown');r.mov(m('ebp',-36),0)
 # A second logging attempt after edge latch must be ignored.
 d.capture([('native_EAX',99)])
 r.label('path_free');r.unary('inc',m('ebx',0x24684));r.mov(m('ebp',-20),0);r.mov('eax',m('ebp',-36));d.capture([('direct_return','eax')],['direct_return'],propagate=True);r.epilogue(128,12);d.failures()
 code=r.finish();assert len(code)<0x40000-16
 return dict(logger=dict(code=code,recipe=r.rows,labels=r.labels,state_size=STATE_SIZE,allocation_size=0x40000+STATE_SIZE+16,record_offset=0x79804,fixture_only=True,natural_path_or_engine=False))

def main():
 gate=json.loads((OUT/'ROOT-BRONREVIEW.json').read_text('utf-8'))
 if gate.get('fixture_emit_allowed') is not True:raise ValueError('Separate root fixture emission gate required')
 folder=OUT/'fixture';folder.mkdir(exist_ok=True)
 for name,data in recipes().items():
  (folder/(name+'.bin')).write_bytes(data['code']);(folder/(name+'.recipe.json')).write_text(json.dumps({k:v for k,v in data.items() if k!='code'},indent=2)+'\n','utf-8')
if __name__=='__main__':main()
