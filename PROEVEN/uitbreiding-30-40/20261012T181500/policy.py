"""Owned opening30/Theocracy40 source, no execution/installation."""
import native as n
from x86 import mem as m

def invoke(r,name):r.push('ebx');r.j('call',name)

def read_policy(r):
 # stdcall(AiMain*, output[6]). Fresh native count, no pass/global state.
 r.label('read_policy');r.prologue(112);r.mov('edi',m('ebp',8));r.test('edi','edi');r.j('jz','policy_bad')
 r.j('call','B2Host');r.test('eax','eax');r.j('jz','policy_bad');r.mov(m('ebp',-16),'eax')
 r.mov('edx',m('edi',0x20));r.alu('cmp','edx',1);r.j('jl','policy_bad');r.alu('cmp','edx',31);r.j('jg','policy_bad');r.mov(m('ebp',-20),'edx')
 r.mov('ebx',m('edi',0x2c));r.test('ebx','ebx');r.j('jz','policy_bad');r.lea('edx',m('eax',0x344660));r.alu('cmp',m('ebx'),'edx');r.j('jne','policy_bad')
 r.mov('edx',m('ebp',-20));r.alu('cmp',m('ebx',12),'edx');r.j('jne','policy_bad');r.mov('ebx',m('ebx',8));r.test('ebx','ebx');r.j('jz','policy_bad')
 r.mov('ecx',m('eax',0x67dd80));r.test('ecx','ecx');r.j('jz','policy_bad');r.shift('shl','edx',2);r.alu('add','ecx','edx');r.j('jb','policy_bad');r.alu('cmp',m('ecx'),'ebx');r.j('jne','policy_bad')
 r.lea('eax',m('ebp',-64));r.push('eax');r.push(m('edi',0x30));r.push('edi');r.j('call','H3Host');r.alu('cmp','eax',1);r.j('jne','policy_bad');r.alu('cmp',m('ebp',-52),'ebx');r.j('jne','policy_bad')
 r.mov('eax',m('ebx',0x12c0));r.test('eax','eax');r.j('jz','policy_bad');r.mov('ecx',m('eax',8));r.test('ecx','ecx');r.j('js','policy_bad');r.mov(m('ebp',-24),'ecx')
 r.mov('eax',m('ebx',0x94));r.test('eax','eax');r.j('js','policy_bad');r.mov(m('ebp',-28),'eax')
 r.lea('eax',m('ebp',-80));r.push('eax');r.push('edi');r.j('call','B2Symbols');r.test('eax','eax');r.j('jz','policy_bad');r.push(m('ebp',-80));r.j('call','B2Bit');r.alu('cmp','eax',1);r.j('ja','policy_bad');r.mov(m('ebp',-32),'eax')
 r.mov('edi',m('ebp',12));r.test('edi','edi');r.j('jz','policy_bad');r.mov(m('edi'),1);r.mov(m('edi',4),0)
 for local,out in [(-24,8),(-28,12),(-32,16)]:r.mov('eax',m('ebp',local));r.mov(m('edi',out),'eax')
 r.mov(m('edi',20),'ebx');r.alu('cmp',m('ebp',-32),0);r.j('jne','policy_after_opening');r.alu('cmp',m('ebp',-24),30);r.j('jl','policy_opening');r.label('policy_after_opening');r.alu('cmp',m('ebp',-28),3);r.j('je','policy_theocracy');r.alu('cmp',m('ebp',-32),1);r.j('je','policy_outside');r.label('policy_opening');r.mov('eax',30);r.j('jmp','policy_budget')
 r.label('policy_theocracy');r.mov('eax',40);r.label('policy_budget');r.alu('sub','eax',m('ebp',-24));r.j('jg','policy_store');r.mov('eax',0);r.label('policy_store');r.mov(m('edi',4),'eax');r.j('jmp','policy_ok')
 r.label('policy_outside');r.mov(m('edi'),0);r.label('policy_ok');r.mov('eax',1);r.j('jmp','policy_done');r.label('policy_bad');r.mov('eax',0);r.label('policy_done');r.epilogue(112,8)

def original_demand(r):
 # Full selected-class preview: exact native clamp/sign/city multiplier and
 # the same loaded ceil IAT as Desired. Own total is checked signed32.
 n.entry(r,'original_demand',64);n.pc(r,'original_demand_pc');r.mov(m('ebx',n.P['original']),0);r.mov(m('ebp',-16),0)
 r.mov('eax',m('ebx',n.P['engine_count']));r.test('eax','eax');r.j('jnz','orig_cities');r.mov('eax',1);r.label('orig_cities');r.mov(m('ebp',-20),'eax')
 r.label('orig_loop');r.mov('eax',m('ebp',-16));r.alu('cmp','eax',m('ebx',n.P['classes']));r.j('jge','orig_ok');r.imul('eax','eax',n.PREVIEW_STRIDE);r.lea('edi',m('ebx',n.PREVIEW));r.alu('add','edi','eax');r.mov('eax',m('ebx',n.P['t']));r.alu('cmp',m('edi',4),'eax');r.j('jne','orig_next')
 r.mov('eax',m('edi',12));r.alu('and','eax',0x7ff00000);r.alu('cmp','eax',0x7ff00000);r.j('je','orig_bad')
 r.fp('fld preview q','dd',0,m('edi',8));r.op('fld st0',b'\xd9\xc0');r.op('fabs',b'\xd9\xe1');r.fp('fcomp native clamp','dc',3,m('esi',0x8b4f8));r.op('fnstsw ax',b'\xdf\xe0');r.test('eax',0x4100);r.j('jnz','orig_clamped');r.op('fstp st0',b'\xdd\xd8');r.fp('fld native replacement','dd',0,m('esi',0x8b500));r.label('orig_clamped')
 r.fp('fcom native zero','dc',2,m('esi',0x8b4e0));r.op('fnstsw ax',b'\xdf\xe0');r.test('eax',0x100);r.j('jz','orig_ratio');r.op('fchs',b'\xd9\xe0');r.j('jmp','orig_amount');r.label('orig_ratio');r.fp('fimul city multiplier','da',1,m('ebp',-20));r.label('orig_amount')
 r.fp('fstp native amount','dd',3,m('ebp',-32));r.push(m('ebp',-28));r.push(m('ebp',-32));r.unary('call',m('esi',0x89038));r.alu('add','esp',8);r.fp('fistp ceil integer','db',3,m('ebp',-24));r.mov('eax',m('ebp',-24));r.test('eax','eax');r.j('js','orig_bad');r.alu('add','eax',m('ebx',n.P['original']));r.j('jo','orig_bad');r.mov(m('ebx',n.P['original']),'eax')
 r.label('orig_next');r.unary('inc',m('ebp',-16));r.j('jmp','orig_loop');r.label('orig_ok');r.mov('eax',1);r.j('jmp','orig_done');r.label('orig_bad');n.unknown(r,40);n.result(r,'orig_done',64)

def canonical_prefix(r):
 # Reuse VISITED only before DFS begins (nodes==0). Copy every canonical
 # key once, then pick minimum64 keys in64*4096 bounded comparisons.
 n.entry(r,'canonical_prefix',64);r.mov(m('ebp',-16),0)
 r.label('prefix_keys');r.mov('eax',m('ebp',-16));r.alu('cmp','eax',m('ebx',n.P['candidates']));r.j('jge','prefix_choose');r.imul('edi','eax',n.NODE_STRIDE);r.alu('add','edi','ebx');r.alu('add','edi',n.VISITED);r.mov(m('edi',8),'eax');r.shift('shl','eax',3);r.lea('edx',m('ebx',n.CAPTURE));r.alu('add','edx','eax');r.push('edi');r.push('edx');r.push('ebx');r.j('call','canonical_key');r.test('eax','eax');r.j('jz','prefix_bad');r.unary('inc',m('ebp',-16));r.j('jmp','prefix_keys')
 r.label('prefix_choose');r.mov(m('ebp',-20),0);r.label('prefix_outer');r.mov('eax',m('ebp',-20));r.alu('cmp','eax',64);r.j('jae','prefix_ok');r.alu('cmp','eax',m('ebx',n.P['candidates']));r.j('jae','prefix_ok');r.mov(m('ebp',-24),-1);r.mov(m('ebp',-28),0)
 r.label('prefix_scan');r.mov('eax',m('ebp',-28));r.alu('cmp','eax',m('ebx',n.P['candidates']));r.j('jae','prefix_store');r.imul('edi','eax',n.NODE_STRIDE);r.alu('add','edi','ebx');r.alu('add','edi',n.VISITED);r.alu('cmp',m('edi',8),-1);r.j('je','prefix_next');r.alu('cmp',m('ebp',-24),-1);r.j('je','prefix_best');r.imul('eax',m('ebp',-24),n.NODE_STRIDE);r.alu('add','eax','ebx');r.alu('add','eax',n.VISITED);r.push('eax');r.push('edi');r.j('call','H3PosCompare');r.test('eax','eax');r.j('jge','prefix_next');r.label('prefix_best');r.mov('eax',m('ebp',-28));r.mov(m('ebp',-24),'eax');r.label('prefix_next');r.unary('inc',m('ebp',-28));r.j('jmp','prefix_scan')
 r.label('prefix_store');r.mov('eax',m('ebp',-24));r.test('eax','eax');r.j('js','prefix_bad');r.imul('edi','eax',n.NODE_STRIDE);r.alu('add','edi','ebx');r.alu('add','edi',n.VISITED);r.mov('eax',m('edi',8));r.mov(m('edi',8),-1);r.mov('edx',m('ebp',-20));r.shift('shl','edx',2);r.alu('add','edx','ebx');r.mov(m('edx',n.ORDER),'eax');r.unary('inc',m('ebp',-20));r.j('jmp','prefix_outer');r.label('prefix_ok');r.mov('eax',1);r.j('jmp','prefix_done');r.label('prefix_bad');n.unknown(r,41);n.result(r,'prefix_done',64)

def finalize(r):
 n.entry(r,'finalize_pass',112);r.alu('cmp',m('ebx',n.P['scope']),1);r.j('jne','final_bad');r.lea('eax',m('ebp',-80));r.push('eax');r.push(m('ebx',n.P['owner']));r.j('call','read_policy');r.test('eax','eax');r.j('jz','final_bad')
 for local,key in [(-80,'policy'),(-76,'remaining'),(-72,'engine_count'),(-68,'government'),(-64,'completion')]:r.mov('eax',m('ebp',local));r.mov(m('ebx',n.P[key]),'eax')
 r.alu('cmp',m('ebx',n.P['policy']),0);r.j('je','final_outside');r.mov('eax',m('ebx',n.P['status']));r.mov(m('ebp',-16),'eax');invoke(r,'bind_host');r.test('eax','eax');r.j('jz','final_bad')
 for helper in ('resolve_type','preview_scope','original_demand'):
  invoke(r,helper);r.test('eax','eax');r.j('jz','final_bad')
 r.mov(m('ebx',n.P['context']),1);r.mov(m('ebx',n.P['gcert']),0);r.alu('cmp',m('ebx',n.P['remaining']),0);r.j('je','final_combine');r.alu('cmp',m('ebp',-16),2);r.j('jne','final_fallback')
 invoke(r,'canonical_prefix');r.test('eax','eax');r.j('jz','final_fallback');invoke(r,'production_roles');r.test('eax','eax');r.j('jz','final_fallback')
 for kind,offset in ((2,0x8c),(1,0x90)):
  r.mov('eax',m('ebx',n.P['owner']));r.push(kind);r.push(m('eax',offset));r.push('ebx');r.j('call','read_set');r.test('eax','eax');r.j('jz','final_fallback')
 r.mov('eax',m('ebx',n.P['cities']));r.alu('cmp','eax',m('ebx',n.P['engine_count']));r.j('jne','final_fallback');invoke(r,'order_roles');invoke(r,'select_direct_plans');r.test('eax','eax');r.j('jz','final_fallback');r.mov('eax',m('ebx',n.P['desired']));r.mov(m('ebx',n.P['gcert']),'eax');r.j('jmp','final_combine')
 r.label('final_fallback');r.mov(m('ebx',n.P['gcert']),0);r.alu('cmp',m('ebx',n.P['reason']),0);r.j('jne','final_combine');r.mov(m('ebx',n.P['reason']),42)
 r.label('final_combine');r.mov('eax',m('ebx',n.P['original']));r.alu('cmp','eax',m('ebx',n.P['gcert']));r.j('jge','final_max');r.mov('eax',m('ebx',n.P['gcert']));r.label('final_max');r.alu('cmp','eax',m('ebx',n.P['remaining']));r.j('jle','final_min');r.mov('eax',m('ebx',n.P['remaining']));r.label('final_min');r.mov(m('ebx',n.P['desired']),'eax');r.mov(m('ebx',n.P['status']),4);r.mov('eax',1);r.j('jmp','final_done')
 r.label('final_outside');r.mov(m('ebx',n.P['status']),6);r.mov(m('ebx',n.P['reason']),43);r.mov('eax',1);r.j('jmp','final_done');r.label('final_bad');n.unknown(r,44);n.result(r,'final_done',112)

def cap_adapters(r,b2):
 # Entry/arrival wrappers use existing full integer/flags/x87 snapshot ABI.
 b2.start(r,'execute_gate');b2.snapshot(r);r.lea('eax',m('ebp',-80));r.push('eax');r.push(m('ebp',8));r.j('call','read_policy');r.test('eax','eax');r.j('jz','contract_error');r.alu('cmp',m('ebp',-80),0);r.j('je','execute_native');r.alu('cmp',m('ebp',-76),0);r.j('jne','execute_native');b2.restore(r);r.mov('eax',0);b2.end(r,8)
 r.label('execute_native');b2.restore(r);r.push(m('ebp',12));r.push(m('ebp',8));r.mov('ecx',m('ebp',-4));r.j('call','ExecuteOriginal');b2.end(r,8)
 b2.start(r,'arrival_dispatch');b2.snapshot(r);r.alu('cmp',m('ebp',20),0);r.j('jne','arrival_native');r.mov('edi',m('ebp',-4));r.alu('cmp',m('edi',12),5);r.j('jne','arrival_native');n.pc(r,'arrival_pc');r.lea('eax',m('esi',0x8a558));r.alu('cmp',m('edi'),'eax');r.j('jne','arrival_native');r.lea('eax',m('ebp',-80));r.push('eax');r.push(m('ebp',8));r.j('call','read_policy');r.test('eax','eax');r.j('jz','contract_error');r.alu('cmp',m('ebp',-80),0);r.j('je','arrival_native');r.alu('cmp',m('ebp',-76),0);r.j('jne','arrival_native');b2.restore(r);r.mov('eax',-1);b2.end(r,16)
 r.label('arrival_native');b2.restore(r)
 for off in (20,16,12,8):r.push(m('ebp',off))
 r.mov('ecx',m('ebp',-4));r.mov('edx',m('ecx'));r.unary('call',m('edx',0x90));r.mov('eax',1);b2.end(r,16)
 # NO prologue: EBP is inherited caller GotoTaskSolution, subtask+[20].
 r.label('normalize_dispatch');r.push('edx');r.op('pushfd',b'\x9c');r.alu('cmp','eax',-1);r.j('jne','normalize_native');r.alu('cmp',m('ebp',0x20),0);r.j('jne','normalize_native');r.alu('cmp',m('esi',12),5);r.j('jne','normalize_native');r.j('call','normalize_pc');r.label('normalize_pc');r.pop('edx');r.rva('sub edx,modulepc','81ea','normalize_pc');r.lea('edx',m('edx',0x8a558));r.alu('cmp',m('esi'),'edx');r.j('jne','normalize_native');r.op('popfd',b'\x9d');r.pop('edx');r.mov('eax',0);r.op('ret',b'\xc3')
 r.label('normalize_native');r.op('popfd',b'\x9d');r.pop('edx');r.op('exact native bool 0->2/nonzero->3',bytes.fromhex('f7d81bc0f7d883c002'));r.op('ret',b'\xc3')

def emit(r,b2,base):
 base.host(r);base.input_guard(r);base.hints(r)
 read_policy(r);original_demand(r);canonical_prefix(r);finalize(r);base.wrappers(r,b2);cap_adapters(r,b2)
 for f in (n.resolve_type,n.owner_gate,n.key,n.preview,n.dfs,n.departures,n.safety,n.path,n.capture,n.roles,n.ordering,n.conflicts,n.path_cache,n.selection):f(r)
 r.label('settler_name');r.op('constant loaded token',b'UNIT_SETTLER\0')
