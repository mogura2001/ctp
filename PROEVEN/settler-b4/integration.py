"""B4 five-hook state/producer integration, using existing B2 ABI wrappers.

This emits source; no engine, game process, installation or GUI is accessed.
The pass buffer belongs to the candidate's own RW section, is cleared at START
and invalidated on AIP return. It is not an engine allocation or save record.
"""
import struct
import native as n
from x86 import mem as m

def plan(r,name):
 n.pc(r,name);r.rva('lea ebx,own pass','8d9e','pass_state')

def invoke(r,name):r.push('ebx');r.j('call',name)

def host(r):
 n.entry(r,'bind_host',80);r.j('call','B2Host');r.test('eax','eax');r.j('jz','bind_bad');r.mov(m('ebx',n.P['host']),'eax')
 r.mov('edi',m('ebx',n.P['owner']));r.test('edi','edi');r.j('jz','bind_bad')
 for source,key in ((0x94,'planner'),(0x80,'map'),(0x38,'udb'),(0x2c,'player'),(0x30,'world'),(0x34,'path')):
  r.mov('eax',m('edi',source));r.test('eax','eax');r.j('jz','bind_bad');r.mov(m('ebx',n.P[key]),'eax')
 r.mov('eax',m('edi',0x20));r.alu('cmp','eax',1);r.j('jl','bind_bad');r.alu('cmp','eax',31);r.j('jg','bind_bad');r.mov(m('ebx',n.P['civ']),'eax')
 r.mov('eax',m('ebx',n.P['planner']));r.lea('edx',m('eax',0x20));r.mov(m('ebx',n.P['aip']),'edx');r.alu('cmp',m('edx',0x800),'edi');r.j('jne','bind_bad');r.alu('cmp',m('eax',0xa28),'edi');r.j('jne','bind_bad');r.mov('edx',m('ebx',n.P['scheduler']));r.alu('cmp',m('eax',0xa2c),'edx');r.j('jne','bind_bad')
 r.lea('eax',m('ebx',144));r.push('eax');r.push(m('ebx',n.P['world']));r.push('edi');r.j('call','H3Host');r.test('eax','eax');r.j('jz','bind_bad')
 for key,vtable in (('udb',0x345098),('player',0x344660),('world',0x3452e0),('path',0x346220)):
  r.mov('edx',m('ebx',n.P[key]));n.engine(r,'eax',vtable);r.alu('cmp',m('edx'),'eax');r.j('jne','bind_bad')
 r.mov('edx',m('ebx',n.P['player']));r.mov('eax',m('edx',8));r.alu('cmp','eax',m('ebx',156));r.j('jne','bind_bad');r.mov('edx',m('ebx',n.P['path']));r.alu('cmp',m('edx',0x7c),'eax');r.j('jne','bind_bad')
 for vtable,slot,target in ((0x3452e0,0x54,0x133880),(0x344660,0xc,0x1273a0),(0x346220,0xc,0x1826a0)):
  n.engine(r,'edx',vtable);n.engine(r,'eax',target);r.alu('cmp',m('edx',slot),'eax');r.j('jne','bind_bad')
 r.mov('eax',1);r.j('jmp','bind_done');r.label('bind_bad');n.unknown(r,30);n.result(r,'bind_done',80)

def hints(r):
 # Reciprocal identities are copied before cleanup. Squad->unit membership
 # has no accepted binding: these remain explicitly UNKNOWN hints, never
 # certified assignments and never dereferenced after SchedulerUpdate.
 n.entry(r,'copy_hints',64);r.mov('edi',m('ebx',n.P['planner']));r.mov('eax',m('edi',0xa30));r.test('eax','eax');r.j('js','hint_bad');r.alu('cmp','eax',4096);r.j('jg','hint_bad');r.mov(m('ebp',-16),'eax')
 for cap in (0xa38,0xa4c,0xa54):r.alu('cmp','eax',m('edi',cap));r.j('jg','hint_bad')
 r.mov('eax',m('edi',0xa48));r.mov(m('ebp',-20),'eax');r.mov('eax',m('edi',0xa50));r.mov(m('ebp',-24),'eax');r.mov(m('ebp',-28),0)
 r.label('hint_loop');r.mov('eax',m('ebp',-28));r.alu('cmp','eax',m('ebp',-16));r.j('jge','hint_ok');r.mov('edx',m('ebp',-20));r.test('edx','edx');r.j('jz','hint_bad');r.shift('shl','eax',2);r.alu('add','edx','eax');r.mov('edi',m('edx'));r.test('edi','edi');r.j('jz','hint_next');r.alu('cmp',m('edi',0xc),5);r.j('jne','hint_next');n.pc(r,'hint_pc');r.lea('eax',m('esi',0x8a558));r.alu('cmp',m('edi'),'eax');r.j('jne','hint_bad')
 r.mov('eax',m('ebp',-24));r.test('eax','eax');r.j('jz','hint_bad');r.mov('edx',m('ebp',-28));r.shift('shl','edx',2);r.alu('add','eax','edx');r.mov('eax',m('eax'));r.alu('cmp','eax',m('edi',8));r.j('jne','hint_bad')
 r.mov('edx',m('edi',0x34));r.test('edx','edx');r.j('jz','hint_next');r.alu('cmp',m('edx',0x5c),'edi');r.j('jne','hint_next');r.alu('cmp',m('edx',0x60),'eax');r.j('jne','hint_next');r.mov('ecx',m('edx'));r.alu('cmp','ecx',m('edi',0x30));r.j('jne','hint_next');r.mov('esi',m('edi',0x54));r.test('esi','esi');r.j('jz','hint_bad')
 r.imul('edi',m('ebx',n.P['hints']),n.HINT_STRIDE);r.alu('add','edi','ebx');r.alu('add','edi',n.HINTS);r.mov(m('edi'),'eax');r.mov(m('edi',4),'ecx')
 for part in (0,4):r.mov('eax',m('esi',part));r.mov(m('edi',8+part),'eax')
 r.mov(m('edi',16),0);r.mov(m('edi',20),0);r.unary('inc',m('ebx',n.P['hints']))
 r.label('hint_next');r.unary('inc',m('ebp',-28));r.j('jmp','hint_loop');r.label('hint_ok');r.mov('eax',1);r.j('jmp','hint_done');r.label('hint_bad');n.unknown(r,31);n.result(r,'hint_done',64)

def finalize(r,N):
 n.entry(r,'finalize_pass',64);r.alu('cmp',m('ebx',n.P['status']),2);r.j('jne','final_bad');r.alu('cmp',m('ebx',n.P['scope']),1);r.j('jne','final_bad');invoke(r,'bind_host');r.test('eax','eax');r.j('jz','final_bad')
 r.lea('eax',m('ebp',-24));r.push('eax');r.push(m('ebx',n.P['owner']));r.j('call','B2Symbols');r.test('eax','eax');r.j('jz','final_bad');r.push(m('ebp',-24));r.j('call','B2Bit');r.alu('cmp','eax',1);r.j('ja','final_bad');r.mov(m('ebx',n.P['completion']),'eax');r.test('eax','eax');r.j('jnz','final_bad')
 for helper in ('resolve_type','preview_scope'):
  invoke(r,helper);r.test('eax','eax');r.j('jz','final_bad')
 for kind,offset in ((2,0x8c),(1,0x90)):
  r.mov('eax',m('ebx',n.P['owner']));r.push(kind);r.push(m('eax',offset));r.push('ebx');r.j('call','read_set');r.test('eax','eax');r.j('jz','final_bad')
 r.mov('eax',N);r.alu('sub','eax',m('ebx',n.P['cities']));r.j('jg','final_remaining');r.mov('eax',0);r.label('final_remaining');r.mov(m('ebx',n.P['remaining']),'eax');r.test('eax','eax');r.j('jz','final_freeze')
 for helper in ('production_roles','order_roles','select_direct_plans'):
  invoke(r,helper)
  if helper!='order_roles':r.test('eax','eax');r.j('jz','final_bad')
 r.label('final_freeze');r.mov(m('ebx',n.P['status']),3);r.mov(m('ebx',n.P['status']),4);r.mov('eax',1);r.j('jmp','final_done');r.label('final_bad');n.unknown(r,32);n.result(r,'final_done',64)

def wrappers(r,b2):
 b2.start(r,'start_hook');b2.snapshot(r);plan(r,'start_pc');r.alu('cmp',m('ebx',n.P['scope']),0);r.j('jne','contract_error');r.rva('lea edx,generation','8d96','generation');r.unary('inc',m('edx'));r.mov('edx',m('edx'));r.mov(m('ebp',-16),'edx');r.zero('ebx',n.PLAN_SIZE);r.mov('eax',m('ebp',-16));r.mov(m('ebx',n.P['generation']),'eax');r.mov('edx',m('ebp',-4));r.mov(m('ebx',n.P['scheduler']),'edx');r.mov('eax',m('edx',0x468));r.mov(m('ebx',n.P['owner']),'eax');r.mov(m('ebx',n.P['status']),1);invoke(r,'bind_host');r.test('eax','eax');r.j('jz','start_original');invoke(r,'copy_hints');r.label('start_original');b2.restore(r);r.mov('ecx',m('ebp',-4));r.j('call','SchedulerUpdate');b2.end(r,0)
 b2.start(r,'capture_hook');r.push(m('ebp',8));r.mov('ecx',m('ebp',-4));r.j('call','GroundBuild');b2.snapshot(r);plan(r,'capture_pc');r.alu('cmp',m('ebx',n.P['status']),1);r.j('jne','capture_restore');r.mov('eax',m('ebp',8));r.alu('cmp','eax',m('ebx',n.P['owner']));r.j('jne','capture_context_bad');r.mov('eax',m('ebp',-4));r.alu('cmp','eax',m('ebx',n.P['map']));r.j('jne','capture_context_bad');invoke(r,'capture_heap');r.j('jmp','capture_restore');r.label('capture_context_bad');n.unknown(r,33);r.label('capture_restore');b2.restore(r);b2.end(r,4)
 b2.start(r,'scope_hook');b2.snapshot(r);plan(r,'scope_pc');r.alu('cmp',m('ebx',n.P['scope']),0);r.j('jne','contract_error');r.mov('eax',m('ebp',-4));r.alu('cmp','eax',m('ebx',n.P['aip']));r.j('jne','scope_bad');r.mov(m('ebx',n.P['scope']),1);r.j('jmp','scope_ready');r.label('scope_bad');n.unknown(r,34);r.label('scope_ready');b2.restore(r);r.mov('ecx',m('ebp',-4));r.j('call','AIPUpdate');b2.snapshot(r);plan(r,'scope_end_pc');r.mov(m('ebx',n.P['status']),5);r.mov(m('ebx',n.P['scope']),0);r.mov(m('ebx',n.P['owner']),0);b2.restore(r);b2.end(r,0)
 b2.start(r,'desired_hook');b2.snapshot(r);plan(r,'desired_pc');r.mov('eax',m('ebp',-4));r.alu('cmp','eax',m('ebx',n.P['aip']));r.j('jne','desired_bad');invoke(r,'finalize_pass');r.j('jmp','desired_ready');r.label('desired_bad');n.unknown(r,35);r.label('desired_ready');b2.restore(r);r.mov('ecx',m('ebp',-4));r.j('call','Desired');b2.end(r,0)
 quota(r,b2)
 r.label('contract_error');r.op('ud2 immutable or reentrant candidate contract failed',b'\x0f\x0b')

def quota(r,b2):
 b2.start(r,'quota_hook');r.push(m('ebp',12));r.push(m('ebp',8));r.mov('ecx',m('ebp',-4));r.j('call','Choose');r.fp('fstp original quota','dd',3,m('ebp',-40));b2.snapshot(r);plan(r,'quota_pc');r.alu('cmp',m('ebx',n.P['status']),4);r.j('jne','quota_restore');r.alu('cmp',m('ebx',n.P['scope']),1);r.j('jne','contract_error');r.mov('edi',m('ebp',-4));r.alu('cmp','edi',m('ebx',n.P['aip']));r.j('jne','contract_error');r.mov('edx',m('ebp',12));r.mov('eax',m('edx'));r.mov(m('ebp',-16),'eax')
 # Confirm the entire native list/type/double sequence, including nonsettlers.
 r.label('quota_preview');r.mov('eax',m('ebx',168));r.alu('cmp','eax',m('ebx',n.P['classes']));r.j('jae','contract_error');r.imul('eax','eax',n.PREVIEW_STRIDE);r.lea('esi',m('ebx',n.PREVIEW));r.alu('add','esi','eax');r.unary('inc',m('ebx',168));r.alu('cmp',m('esi'),0);r.j('je','quota_preview');r.mov('eax',m('ebp',8));r.alu('cmp','eax',m('esi'));r.j('jne','contract_error');r.mov('eax',m('ebp',-16));r.alu('cmp','eax',m('esi',4));r.j('jne','contract_error')
 for off in (0,4):r.mov('eax',m('ebp',-40+off));r.alu('cmp','eax',m('esi',8+off));r.j('jne','contract_error')
 r.mov('eax',m('ebp',-16));r.alu('cmp','eax',m('ebx',n.P['t']));r.j('jne','quota_restore')
 # Read W from the native current desired double, not the own claim count.
 r.mov('edx',m('edi',0x7c0));r.test('edx','edx');r.j('jz','contract_error');r.mov('edx',m('edx'));r.test('edx','edx');r.j('jz','contract_error');r.shift('shl','eax',3);r.alu('add','edx','eax');r.fp('fld native W','dd',0,m('edx'));r.fp('fistp W','db',3,m('ebp',-20));r.mov('eax',m('ebp',-20));r.alu('cmp','eax',m('ebx',n.P['written']));r.j('jne','contract_error');r.fp('fild W','db',0,m('ebp',-20));r.fp('fcomp native W','dc',3,m('edx'));r.op('fnstsw ax',b'\xdf\xe0');r.alu('and','eax',0x4500);r.alu('cmp','eax',0x4000);r.j('jne','contract_error')
 r.mov('eax',m('ebx',n.P['desired']));r.alu('sub','eax',m('ebx',n.P['written']));r.j('js','contract_error');r.mov(m('ebp',-24),'eax');r.test('eax','eax');r.j('jz','quota_zero');r.fp('fild contribution','db',0,m('ebp',-24));r.op('fchs negative native quantum',b'\xd9\xe0');r.j('jmp','quota_store');r.label('quota_zero');r.op('fldz positive zero',b'\xd9\xee');r.label('quota_store');r.fp('fstp managed quota','dd',3,m('ebp',-40));r.mov('eax',m('ebx',n.P['desired']));r.mov(m('ebx',n.P['written']),'eax')
 r.label('quota_restore');b2.restore(r);r.fp('fld one quota return','dd',0,m('ebp',-40));b2.end(r,8)

def emit(r,b2,N):
 for f in (host,hints):f(r)
 finalize(r,N);wrappers(r,b2)
 for f in (n.resolve_type,n.owner_gate,n.key,n.preview,n.dfs,n.departures,n.safety,n.path,n.capture,n.roles,n.ordering,n.conflicts,n.path_cache,n.selection):f(r)
 r.label('settler_name');r.op('constant exact loaded token',b'UNIT_SETTLER\0')
