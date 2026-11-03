"""Bounded own-state logger emitter SOURCE. Import does not emit anything.

No foreign read/query/callback or x87. Every block saves/restores flags+GPR.
Caller supplies only registers, existing own frame operands or own arrays.
"""
from contextlib import contextmanager
from x86 import mem as m
from path_diagnostic_layout import FIELDS as F,REACHED as B,RECORD_OFFSET as R,RECORD_SIZE,required_mask
class Trace:
 SAVED=dict(edi=0,esi=4,ebp=8,ebx=16,edx=20,ecx=24,eax=28)
 def __init__(self,r,phase):self.r=r;self.phase=phase;self.serial=0
 def label(self,name):return 'pd_'+self.phase+'_'+name
 def begin(self):self.r.op('pathdiag pushfd',b'\x9c');self.r.op('pathdiag pushad',b'\x60')
 def end(self):self.r.op('pathdiag popad',b'\x61');self.r.op('pathdiag popfd',b'\x9d')
 def val(self,v):
  if isinstance(v,tuple) and v[0]=='saved_flags':self.r.mov('eax',m('esp',32));self.r.alu('and','eax',v[1])
  elif isinstance(v,str):self.r.mov('eax',m('esp',self.SAVED[v]))
  else:self.r.mov('eax',v)
 def store(self,name,value,part=0):self.val(value);self.r.mov(m('edi',R+F[name]+part),'eax')
 def bit(self,bit):self.r.alu('or',m('edi',R+F['reached']),1<<(B[bit] if isinstance(bit,str) else bit))
 def rva(self,name,label):self.r.rva('mov eax,pathdiag '+label,'b8',label);self.r.mov(m('edi',R+F[name]),'eax')
 @contextmanager
 def block(self,initialize=False,propagate=False):
  r=self.r;self.serial+=1;pc=self.label('pc'+str(self.serial));done=self.label('done'+str(self.serial));self.begin()
  r.j('call',pc);r.label(pc);r.pop('esi');r.rva('sub esi,pathdiag PC','81ee',pc);r.rva('lea edi,independent pathdiag Plan','8dbe','pass_state')
  r.alu('cmp','edi',m('esp',self.SAVED['ebx']));r.j('jne',done)
  for off,value in ((36,1),(40,0)):r.alu('cmp',m('edi',off),value);r.j('jne',done)
  for off,snap in ((8,0x78800),(32,0x78804)):
   r.mov('eax',m('edi',off));r.test('eax','eax');r.j('jz',done);r.alu('cmp','eax',m('edi',snap));r.j('jne',done)
  r.alu('cmp',m('edi',12),1);r.j('jl',done);r.alu('cmp',m('edi',12),31);r.j('jg',done)
  ret={'selection':'pd_select_return','cache':'pd_cache_return','path':'pd_direct_return'}.get(self.phase)
  if ret:r.rva('lea ecx,actual pathdiag caller return','8d8e',ret);r.alu('cmp','ecx',m('ebp',4));r.j('jne',done)
  if not initialize:
   for field,value in [('schema',1),('size',256)]:r.alu('cmp',m('edi',R+F[field]),value);r.j('jne',done)
   for state,record in ((8,'owner'),(32,'generation'),(12,'civ')):
    r.mov('eax',m('edi',state));r.alu('cmp','eax',m('edi',R+F[record]));r.j('jne',done)
   r.alu('cmp','edi',m('edi',R+F['plan_identity']));r.j('jne',done);r.alu('cmp',m('edi',R),0);r.j('jne',done)
   r.alu('cmp',m('edi',R+F['invocation']),0);r.j('je',done)
   for field,label in [('select_call','pd_select_call'),('select_return_site','pd_select_return'),('cache_call','pd_cache_call'),('cache_return_site','pd_cache_return'),('direct_call','pd_direct_call'),('direct_return_site','pd_direct_return')]:
    r.rva('mov ecx,expected pathdiag callpair','b9',label);r.alu('cmp','ecx',m('edi',R+F[field]));r.j('jne',done)
   r.mov('eax',m('edi',R+F['query']));r.test('eax','eax');r.j('jz',self.label('no_query'+str(self.serial)));r.alu('cmp','eax',128);r.j('ja',done);r.alu('cmp','eax',m('edi',84));r.j('jne',done);r.label(self.label('no_query'+str(self.serial)))
   if not propagate:r.alu('cmp',m('edi',R+F['edge']),0);r.j('jne',done)
   if self.phase in ('cache','path'):
    parent=m('ebp',0);r.mov('edx',parent)
    parent_return='pd_select_return' if self.phase=='cache' else 'pd_cache_return'
    r.rva('lea ecx,actual parent pathdiag return','8d8e',parent_return);r.alu('cmp','ecx',m('edx',4));r.j('jne',done);r.alu('cmp','edi',m('edx',8));r.j('jne',done)
    if self.phase=='path':
     r.mov('edx',m('edx'));r.rva('lea ecx,actual grandparent selection return','8d8e','pd_select_return');r.alu('cmp','ecx',m('edx',4));r.j('jne',done);r.alu('cmp','edi',m('edx',8));r.j('jne',done)
    r.test(m('edi',R+F['reached']),1<<B['source_destination']);r.j('jz',done)
    for field,cap,count,base,stride,arg,extra in [('slot',64,80,0x40600,1152,16,0),('departure',32,76,0x18200,32,12,8)]:
     r.mov('ecx',m('edi',R+F[field]));r.alu('cmp','ecx',cap);r.j('jae',done);r.alu('cmp','ecx',m('edi',count));r.j('jae',done);r.imul('ecx','ecx',stride);r.alu('add','ecx','edi');r.alu('add','ecx',base+extra);r.alu('cmp','ecx',m('ebp',arg));r.j('jne',done)
     for part in (0,4):
      r.mov('eax',m('ecx',part));r.alu('cmp','eax',m('edi',R+F['destination' if field=='slot' else 'source']+part));r.j('jne',done)
     for record,off in ([('prefix',76),('role',72)] if field=='slot' else [('rawID',-8),('kind',-4)]):
      r.mov('eax',m('ecx',off));r.alu('cmp','eax',m('edi',R+F[record]));r.j('jne',done)
    r.mov('eax',m('edi',44));r.alu('cmp','eax',m('edi',R+F['type']));r.j('jne',done)
  yield done
  r.label(done);self.end()
 def reset(self):
  # Called by START inside the existing full ABI snapshot. No active scope
  # admission is possible there yet, so only independent PIC pointer binding.
  r=self.r;self.begin();pc=self.label('reset_pc');done=self.label('reset_done')
  r.j('call',pc);r.label(pc);r.pop('esi');r.rva('sub esi,pathdiag resetPC','81ee',pc);r.rva('lea edi,pathdiag resetPlan','8dbe','pass_state')
  r.alu('cmp','edi','ebx');r.j('jne',done);r.lea('eax',m('edi',R));r.zero('eax',RECORD_SIZE);r.label(done);self.end()
 def invocation(self):
  r=self.r
  with self.block(initialize=True):
   r.mov('edx',0)
   for state,record in ((8,'owner'),(32,'generation')):
    r.mov('eax',m('edi',state));r.alu('cmp','eax',m('edi',R+F[record]));r.j('jne',self.label('ordinal_increment'))
   r.mov('edx',m('edi',R+F['invocation']));r.label(self.label('ordinal_increment'));r.unary('inc','edx');r.j('jnz',self.label('ordinal_ok'));r.mov('edx',1);r.label(self.label('ordinal_ok'));r.push('edx')
   r.lea('eax',m('edi',R));r.zero('eax',RECORD_SIZE);r.pop('edx')
   # zero() clobbers EDI; recover independent Plan from EBX after comparison.
   r.mov('edi','ebx');r.mov(m('edi',R+F['invocation']),'edx');self.store('schema',1);self.store('size',256)
   # store(reg) reads saved pre-block regs: use own memory for identity.
   for state,record in ((8,'owner'),(32,'generation'),(12,'civ')):self.store(record,m('edi',state))
   r.mov(m('edi',R+F['plan_identity']),'edi')
   for field,label in [('select_call','pd_select_call'),('select_return_site','pd_select_return'),('cache_call','pd_cache_call'),('cache_return_site','pd_cache_return'),('direct_call','pd_direct_call'),('direct_return_site','pd_direct_return')]:self.rva(field,label)
   self.bit('callbinding')
 def source(self):
  r=self.r
  with self.block() as done:
   r.mov('ecx',m('ebp',-20));r.alu('cmp','ecx',64);r.j('jae',done);r.alu('cmp','ecx',m('edi',80));r.j('jae',done)
   r.imul('ecx','ecx',1152);r.alu('add','ecx','edi');r.alu('add','ecx',0x40600);r.alu('cmp','ecx',m('esp',self.SAVED['edi']));r.j('jne',done)
   r.mov('edx',m('ebp',-36));r.alu('cmp','edx',32);r.j('jae',done);r.alu('cmp','edx',m('edi',76));r.j('jae',done)
   r.imul('edx','edx',32);r.alu('add','edx','edi');r.alu('add','edx',0x18200);r.alu('cmp','edx',m('esp',self.SAVED['esi']));r.j('jne',done)
   for field,operand in [('slot',m('ebp',-20)),('prefix',m('ecx',76)),('role',m('ecx',72)),('departure',m('ebp',-36)),('rawID',m('edx')),('kind',m('edx',4)),('type',m('edi',44))]:self.store(field,operand)
   for part in (0,4):self.store('source',m('edx',8+part),part);self.store('destination',m('ecx',part),part)
   # New query staging clears old operands/reached bits, never a latched edge.
   r.mov(m('edi',R+F['query']),0)
   for off in range(112,216,4):r.mov(m('edi',R+off),0)
   r.mov(m('edi',R+F['reached']),3)
 def admission(self):
  r=self.r
  with self.block() as done:
   # Actual cached/direct arguments must be the same bounded own objects.
   for field,cap,base,stride,arg,extra in [('slot',64,0x40600,1152,16,0),('departure',32,0x18200,32,12,8)]:
    r.mov('ecx',m('edi',R+F[field]));r.alu('cmp','ecx',cap);r.j('jae',done);r.imul('ecx','ecx',stride);r.alu('add','ecx','edi');r.alu('add','ecx',base+extra);r.alu('cmp','ecx',m('ebp',arg));r.j('jne',done)
   self.bit('callbinding')
 def capture(self,values=(),bits=(),propagate=False):
  with self.block(propagate=propagate):
   for row in values:self.store(*row)
   for bit in bits:self.bit(bit)
 def edge(self,predicate,number):self.r.j(predicate,'pd_failure_'+str(number))
 def local_unknown(self):
  # Same fixed edge4 operand record, held unpublished until full 4/4/1
  # propagation. If any later query changes the one-record binding it stays
  # UNKNOWN; no diagnostic value participates in the executing guard.
  r=self.r
  with self.block() as done:
   r.alu('cmp',m('edi',R+F['reached']),required_mask(4,False));r.j('jne',done);self.store('edge',4)
 def publish_local(self):
  r=self.r
  with self.block(propagate=True) as done:
   r.alu('cmp',m('esp',self.SAVED['eax']),1);r.j('jne',done)
   r.alu('cmp',m('edi',R+F['edge']),4);r.j('jne',done)
   for field,value in [('native_EAX',0),('capacity',0),('count',0),('pointer',0),('postcontext',0),('canary1',0x3456ab89),('canary2',0x4567bc90),('direct_return',4),('cache_return',4)]:
    r.alu('cmp',m('edi',R+F[field]),value);r.j('jne',done)
   r.alu('cmp',m('edi',R+F['reached']),required_mask(4)&~(1<<B['selection_return']));r.j('jne',done)
   # Bind the recorded objects themselves. Current loop indices can already
   # be exhausted, so they cannot honestly describe the earlier pair.
   for field,cap,count,base,stride,extra in [('slot',64,80,0x40600,1152,0),('departure',32,76,0x18200,32,8)]:
    r.mov('ecx',m('edi',R+F[field]));r.alu('cmp','ecx',cap);r.j('jae',done);r.alu('cmp','ecx',m('edi',count));r.j('jae',done);r.imul('ecx','ecx',stride);r.alu('add','ecx','edi');r.alu('add','ecx',base+extra)
    for part in (0,4):
     r.mov('eax',m('ecx',part));r.alu('cmp','eax',m('edi',R+F['destination' if field=='slot' else 'source']+part));r.j('jne',done)
    for record,off in ([('prefix',76),('role',72)] if field=='slot' else [('rawID',-8),('kind',-4)]):
     r.mov('eax',m('ecx',off));r.alu('cmp','eax',m('edi',R+F[record]));r.j('jne',done)
   self.store('selection_return',1);self.bit('selection_return');r.mov(m('edi',R),1)
 def failures(self):
  r=self.r
  for number in range(1,17):
   r.label('pd_failure_'+str(number))
   with self.block() as done:
    r.alu('cmp',m('edi',R+F['reached']),required_mask(number,False));r.j('jne',done);self.store('edge',number)
   r.j('jmp','path_unknown')
 def publish(self):
  r=self.r
  with self.block(propagate=True) as done:
   r.alu('cmp',m('esp',self.SAVED['eax']),0);r.j('jne',done)
   for field,local,reg,base,stride,extra in [('slot',-20,'edi',0x40600,1152,0),('departure',-36,'esi',0x18200,32,8)]:
    r.mov('ecx',m('ebp',local));r.alu('cmp','ecx',m('edi',R+F[field]));r.j('jne',done);r.imul('ecx','ecx',stride);r.alu('add','ecx','edi');r.alu('add','ecx',base);r.alu('cmp','ecx',m('esp',self.SAVED[reg]));r.j('jne',done)
    for part in (0,4):
     r.mov('eax',m('ecx',extra+part));r.alu('cmp','eax',m('edi',R+F['destination' if field=='slot' else 'source']+part));r.j('jne',done)
   r.alu('cmp',m('edi',R+F['edge']),1);r.j('jb',done);r.alu('cmp',m('edi',R+F['edge']),16);r.j('ja',done)
   for field in ('direct_return','cache_return'):r.alu('cmp',m('edi',R+F[field]),0);r.j('jne',done)
   required=sum(1<<i for i in (0,1,17,18));r.mov('eax',m('edi',R+16));r.alu('and','eax',required);r.alu('cmp','eax',required);r.j('jne',done)
   r.alu('cmp',m('edi',4),25);r.j('jne',done);self.store('selection_return',0);self.bit('selection_return');r.mov(m('edi',R),1)
