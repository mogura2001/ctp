"""Five focused pure checks; no Windows process APIs or game execution."""
from pathlib import Path
import importlib.util,json,struct
p=Path(__file__).parent
spec=importlib.util.spec_from_file_location('goal3',p/'Lees-Doel3.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
import sys
sys.path.insert(0,str(m.ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
checks=[]
for variant in ('original','B2a-N30-TECHNICAL'):
    b=m.trusted_binding(variant)
    ep=pefile.PE(str(m.ROOT/'CTP-og/ctp_program/ctp/civctp.exe'))
    ap=pefile.PE(str(m.ROOT/('CTP-og/ctp_program/ctp/dll/ai/robotcom.dll' if variant=='original' else 'PROEVEN/opening-b2/candidates/B2a-N30-TECHNICAL/robotcom.dll')))
    eb,ab=0x400000,0x21000000
    def read(address,size):
        pe,base=(ap,ab) if address>=ab else (ep,eb)
        raw=bytearray(pe.get_data(address-base,size))
        if pe is ap:
            for rva in b['original_HIGHLOW']:
                if address-base<=rva<address-base+size:
                    off=rva-(address-base)
                    if off+4>len(raw):raise ValueError('Fixture partial relocation')
                    struct.pack_into('<I',raw,off,(struct.unpack_from('<I',raw,off)[0]+0x1000000)&0xffffffff)
        return bytes(raw)
    m.verify_loaded(read,b,eb,ab,{'engine':b['engine']['size'],'ai':b['ai']['size']})
    checks.append(dict(case=variant+' relocated hooks/payload/ranges',passed=True))
    if variant!='original':
        def bad(address,size):
            raw=read(address,size)
            return bytes([raw[0]^1])+raw[1:] if address==ab+0xfe51 else raw
        try:m.verify_loaded(bad,b,eb,ab,{'engine':b['engine']['size'],'ai':b['ai']['size']})
        except ValueError:checks.append(dict(case='Changed fifth original/load hook is rejected',passed=True))
        else:raise AssertionError('Bad loaded hook accepted')
memory={}
def put(addr,value):
    for offset,b in enumerate(struct.pack('<i',value)):memory[addr+offset]=b
player,actor,science,known,cities=0x100000,0x200000,0x300000,0x400000,0x500000
for off,value in [(0x12ec,science),(0x94,3),(0x11d8,3),(0x11dc,8),(0x11ac,9),(0x11e0,1)]:put(player+off,value)
put(science+0x1c,known);put(actor+0x8c,cities);put(cities,17)
memory[known+1]=0;memory[known+2]=7
def scalar_read(addr,size):return bytes(memory[addr+i] for i in range(size))
v=m.scalar_state(scalar_read,player,actor,['Other','Theocracy','Religion'])
assert v['known']['Religion']['known'] and not v['known']['Theocracy']['known'] and v['active_government']==3 and v['processed_round']==9 and v['city_count']==17
checks.append(dict(case='Dynamic names, nonzero known byte, govt/deadline/round/cities',passed=True))
put(science+0x1c,0)
try:m.scalar_state(scalar_read,player,actor,['Other','Theocracy','Religion'])
except ValueError:checks.append(dict(case='Null known pointer is rejected',passed=True))
else:raise AssertionError('Null accepted')
(p/'reader-checks.json').write_text(json.dumps(dict(scope='PURE FIXTURES ONLY; no actual loaded process/gameplay',cases=checks),indent=2)+'\n')
print(json.dumps(checks))
