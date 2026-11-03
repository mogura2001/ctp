"""One-shot C1 text wiring. Never imports an emitter or builds anything."""
from pathlib import Path
OUT=Path(__file__).resolve().parent
def change(name,fn):
 p=OUT/name;s=p.read_text('utf-8');p.write_text(fn(s),'utf-8')
def native(s):
 s=s.replace('import struct','import struct\nfrom path_diagnostic import Trace')
 s=s.replace("def original(r,name):r.j('call',name)","def original(r,name):\n label={'cached_path':'pd_cache','direct_path':'pd_direct'}.get(name)\n if label:r.label(label+'_call')\n r.j('call',name)\n if label:r.label(label+'_return')")
 a=s.index('def path(r):');b=s.index('\ndef capture(r):',a);part=s[a:b]
 part=part.replace(" entry(r,'direct_path',128);"," d=Trace(r,'path')\n entry(r,'direct_path',128);")
 marker="r.unary('call',m('edx',12));r.mov(m('ebp',-36),'eax')"
 part=part.replace(marker,marker+"\n d.capture([('native_EAX','eax'),('capacity',m('ebp',-16)),('count',m('ebp',-24)),('pointer',m('ebp',-20)),('query',m('ebx',P['path_queries']))],['native_return'])")
 old=" r.mov('edx',m('ebx',P['host']));r.alu('cmp',m('edx',0x6d0b94),0);r.j('jne','path_unknown');r.alu('cmp',m('ebp',-40),0x3456ab89);r.j('jne','path_unknown');r.alu('cmp',m('ebp',-44),0x4567bc90);r.j('jne','path_unknown')"
 new=" r.mov('edx',m('ebx',P['host']));r.push('ecx');r.mov('ecx',m('edx',0x6d0b94));d.capture([('postcontext','ecx')],['postcontext']);r.alu('cmp','ecx',0);r.pop('ecx');d.edge('jne',1)\n d.capture([('canary1',m('ebp',-40))],['canary1']);r.alu('cmp',m('ebp',-40),0x3456ab89);d.edge('jne',2);d.capture([('canary2',m('ebp',-44))],['canary2']);r.alu('cmp',m('ebp',-44),0x4567bc90);d.edge('jne',3)"
 assert old in part;part=part.replace(old,new)
 part=part.replace("r.alu('cmp',m('ebp',-36),1);r.j('jne','path_unknown')","d.capture(bits=['raw_return_guard']);r.alu('cmp',m('ebp',-36),1);d.edge('jne',4)")
 part=part.replace("r.test('esi','esi');r.j('jz','path_unknown')","d.capture(bits=['pointer']);r.test('esi','esi');d.edge('jz',5)")
 part=part.replace("r.alu('cmp','eax',1);r.j('jl','path_unknown')","d.capture(bits=['count_min']);r.alu('cmp','eax',1);d.edge('jl',6)")
 part=part.replace("r.alu('cmp','eax',m('ebp',-16));r.j('jg','path_unknown')","d.capture(bits=['capacity']);r.alu('cmp','eax',m('ebp',-16));d.edge('jg',7)")
 part=part.replace("r.alu('add','eax','esi');r.j('jb','path_unknown')","r.alu('add','eax','esi');d.capture([('pointer_end','eax')],['overflow']);d.edge('jb',8)")
 part=part.replace(" for off,point in ((0,12),(-8,16)):"," for off,point in ((0,12),(-8,16)):\n  first=off==0;base=9 if first else 13;actual='first_actual' if first else 'last_actual';expected='source_expected' if first else 'destination_expected';ar='first_conversion' if first else 'last_conversion';er='source_conversion' if first else 'destination_conversion'")
 part=part.replace("  r.lea('ecx',m('ebp',-64));", "  d.capture([('first_entry' if first else 'last_entry','edx')])\n  r.lea('ecx',m('ebp',-64));")
 old="original(r,'canonical_key');r.test('eax','eax');r.j('jz','path_unknown')"
 assert part.count(old)==2
 part=part.replace(old,"original(r,'canonical_key');d.capture([(ar,'eax'),(actual,m('ebp',-64)),(actual,m('ebp',-60),4)],[ar]);r.test('eax','eax');d.edge('jz',base)",1)
 part=part.replace(old,"original(r,'canonical_key');d.capture([(er,'eax'),(expected,m('ebp',-72)),(expected,m('ebp',-68),4)],[er]);r.test('eax','eax');d.edge('jz',base+1)",1)
 part=part.replace("for part in (0,4):r.mov('eax',m('ebp',-64+part));r.alu('cmp','eax',m('ebp',-72+part));r.j('jne','path_unknown')","for part in (0,4):d.capture(bits=['first_compare' if first else 'last_compare']);r.mov('eax',m('ebp',-64+part));r.alu('cmp','eax',m('ebp',-72+part));d.edge('jne',base+2+part//4)")
 part=part.replace("r.label('path_done');r.mov('eax',m('ebp',-36));r.epilogue(128,12)","r.label('path_done');r.mov('eax',m('ebp',-36));d.capture([('direct_return','eax')],['direct_return'],propagate=True);r.epilogue(128,12)\n d.failures()")
 s=s[:a]+part+s[b:]
 s=s.replace(" entry(r,'select_direct_plans',96);"," d=Trace(r,'selection')\n entry(r,'select_direct_plans',96);d.invocation();")
 s=s.replace(" r.label('source_path');r.lea", " r.label('source_path');d.source();r.lea")
 s=s.replace("r.label('select_bad');unknown(r,25);result", "r.label('select_bad');unknown(r,25);d.publish();result")
 s=s.replace("original(r,'direct_path');r.test('eax','eax')","original(r,'direct_path');Trace(r,'cache').capture([('cache_return','eax')],['cache_return'],propagate=True);r.test('eax','eax')")
 return s
def policy(s):
 s=s.replace("def invoke(r,name):r.push('ebx');r.j('call',name)","def invoke(r,name):\n r.push('ebx')\n if name=='select_direct_plans':r.label('pd_select_call')\n r.j('call',name)\n if name=='select_direct_plans':r.label('pd_select_return')")
 return s
def integration(s):return s.replace("r.zero('ebx',n.PLAN_SIZE);","r.zero('ebx',n.PLAN_SIZE);__import__('path_diagnostic').Trace(r,'start').reset();")
def main():
 change('native.py',native);change('policy.py',policy);change('integration_base.py',integration)
 # Only actual allocated state grows; Plan and generation address stay fixed.
 for name in ['plan_layout.py','food_diagnostic_layout.py','reader/partial_diagnostic.py','reader/Lees-Uitbreiding.py']:
  change(name,lambda s:s.replace('0x79804','0x79904').replace('497668','497924'))
 change('build_candidate.py',lambda s:s.replace('native.PLAN_SIZE+4','0x79904'))
 print('Source wiring only; no emission performed')
if __name__=='__main__':main()
