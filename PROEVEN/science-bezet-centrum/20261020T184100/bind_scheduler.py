"""Finite RO caller/result binding; no host execution."""
import sys, struct
from pathlib import Path
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parents[2]/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
p=pefile.PE(data=(OUT/'release-v1.robotcom.backup.dll').read_bytes())
d=Cs(CS_ARCH_X86,CS_MODE_32)
rows=[]
for rva,size in [(0x4442d,0x1c8),(0x73506,0x280),(0x73714,0x244),(0x754b0,0x90),(0x659a0,0x160)]:
 rows.append(f'RVA {rva:x} size {size:x}')
 rows.extend(f'{i.address:08x} {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}' for i in d.disasm(p.get_data(rva,size),0x20000000+rva))
table=struct.unpack('<5I',p.get_data(0x73958,20))
rows.append('RESULT TABLE 20073958: '+', '.join(f'{i} -> {v:08x}' for i,v in enumerate(table)))
assert table[0]==0x20073727
ceil=[(dll.dll.decode(),imp.name.decode()) for dll in p.DIRECTORY_ENTRY_IMPORT for imp in dll.imports if imp.address==0x20089038]
assert len(ceil)==1 and ceil[0][1]=='ceil',ceil
rows.append('Desired shared IAT20089038: '+repr(ceil))
for rva in (0x8b4e0,0x8b4f8,0x8b500):
 raw=p.get_data(rva,8);rows.append(f'Desired qword200{rva:05x}: {raw.hex()} double={struct.unpack("<d",raw)[0]!r}')
(OUT/'scheduler-result-binding.txt').write_text('\n'.join(rows)+'\n','utf-8')
print(rows[-1])
