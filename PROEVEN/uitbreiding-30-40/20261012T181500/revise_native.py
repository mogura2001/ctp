"""Reviewable one-time deltas to the owned B4 source copy."""
from pathlib import Path
p=Path(__file__).with_name('native.py')
s=p.read_text('utf-8')
assert 'SELECTED_CAP=30' in s
s=s.replace('SELECTED_CAP=30','SELECTED_CAP=40').replace('ORDER=SELECTED+128','ORDER=SELECTED+160')
s=s.replace('assert SELECTED+SELECTED_CAP*4<=PLAN_SIZE','assert SELECTED+SELECTED_CAP*4<=ORDER')
s=s.replace('d8=120,completion=124,h3calls=128,safetycalls=132)',
 '''d8=120,completion=124,h3calls=128,safetycalls=132,
         original=184,gcert=188,policy=192,government=196,engine_count=200,
         path_points=204,cutoff=208,context=212,source_overflow=216,classified=220)''')
# Preserve count of all cities while only first32 eligible endpoints are copied.
s=s.replace("r.j('jae','departure_bad')", "r.j('jae','departure_budget')")
s=s.replace("r.label('departure_skip');r.mov('eax',1)",
 "r.j('jmp','departure_skip');r.label('departure_budget');r.mov(m('ebx',P['source_overflow']),1);r.mov(m('ebx',P['cutoff']),1);r.label('departure_skip');r.mov('eax',1)")
# Query/point limits are louter suffixcutoff: return0 without invalidating prefix.
s=s.replace("r.j('jae','path_unknown');r.mov('edx',m('ebx',P['host']))", "r.j('jae','path_budget');r.mov('edx',m('ebx',P['host']))",1)
s=s.replace("r.alu('cmp','eax',4096);r.j('jg','path_unknown')", "r.alu('cmp','eax',4096);r.j('jg','path_budget')",1)
s=s.replace("r.mov(m('ebp',-36),1);r.mov(m('ebp',-48),0)",
 "r.mov('eax',m('ebx',P['path_points']));r.alu('add','eax',m('ebp',-24));r.j('jb','path_budget');r.alu('cmp','eax',4096);r.j('ja','path_budget');r.mov(m('ebp',-36),1);r.mov(m('ebp',-48),0)",1)
s=s.replace("r.label('path_next');r.unary('inc',m('ebp',-48))", "r.label('path_next');r.unary('inc',m('ebx',P['path_points']));r.unary('inc',m('ebp',-48))",1)
s=s.replace("r.label('path_free');", "r.j('jmp','path_free');r.label('path_budget');r.mov(m('ebx',P['cutoff']),1);r.mov(m('ebp',-36),0);r.label('path_free');",1)
# Canonical prefix is prepared in ORDER before production classification.
s=s.replace("r.j('jge','roles_ok');r.shift('shl','eax',3);r.lea('edi',m('ebx',CAPTURE));r.alu('add','edi','eax')",
 "r.j('jge','roles_ok');r.alu('cmp','eax',64);r.j('jae','roles_budget');r.shift('shl','eax',2);r.lea('edx',m('ebx',ORDER));r.alu('add','edx','eax');r.mov('eax',m('edx'));r.shift('shl','eax',3);r.lea('edi',m('ebx',CAPTURE));r.alu('add','edi','eax');r.unary('inc',m('ebx',P['classified']))",1)
s=s.replace("r.j('jge','roles_ok')", "r.j('jge','roles_ok')",1)
s=s.replace("r.label('roles_ok');r.mov('eax',1)", "r.j('jmp','roles_ok');r.label('roles_budget');r.mov(m('ebx',P['cutoff']),1);r.label('roles_ok');r.mov('eax',1)",1)
s=s.replace("r.j('jae','cached_unknown');r.push(m('ebp',16))", "r.j('jae','cached_budget');r.push(m('ebp',16))",1)
s=s.replace("r.label('cached_unknown');unknown(r,24)", "r.label('cached_budget');r.mov(m('ebx',P['cutoff']),1);r.mov('eax',0);r.j('jmp','cached_done');r.label('cached_unknown');unknown(r,24)",1)
s=s.replace("r.alu('cmp','eax',m('ebx',P['remaining']));r.j('jge','select_ok')",
 "r.alu('cmp','eax',m('ebx',P['remaining']));r.j('jge','select_ok');r.alu('cmp','eax',SELECTED_CAP);r.j('jae','select_ok')",1)
s=s.replace("r.j('jz','select_bad');r.alu('cmp','eax',1)", "r.j('jz','select_cutoff');r.alu('cmp','eax',1)",1)
s=s.replace("r.label('select_bad');unknown(r,25)", "r.label('select_cutoff');r.alu('cmp',m('ebx',P['cutoff']),1);r.j('je','select_ok');r.label('select_bad');unknown(r,25)",1)
p.write_text(s,'utf-8')
print('Applied bounded own native-source deltas')
