"""Alleen-lezen disassemblage van CTP I met de meegeleverde linker-map.

Dependencies lokaal: PROEVEN/hulpmiddelen/python (capstone 5.0.9, pefile).
Gebruik: python Analyseer-AI-DLL.py Update_Max_Goals InsertSettleGoals
Symbolen bepalen grenzen; assembly is bewijs, gereconstrueerde semantiek niet vanzelf.
"""
from pathlib import Path
import sys
import re
import struct

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "PROEVEN/hulpmiddelen/python"))
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

engine = '--engine' in sys.argv
if engine:
    sys.argv.remove('--engine')
base = ROOT / ("CTP-og/ctp_program/ctp" if engine else "CTP-og/ctp_program/ctp/dll/ai")
binary = 'civctp.exe' if engine else 'robotcom.dll'
mapfile = 'civctp.map' if engine else 'robotcom.map'
pe = pefile.PE(str(base / binary))
symbols = {}
maptext = (base / mapfile).read_text(errors="replace")
stamp = re.search(r'Timestamp is ([0-9a-f]+)',maptext,re.I)
preferred = re.search(r'Preferred load address is ([0-9a-f]+)',maptext,re.I)
if not stamp or int(stamp[1],16) != pe.FILE_HEADER.TimeDateStamp or not preferred or int(preferred[1],16) != pe.OPTIONAL_HEADER.ImageBase:
    raise SystemExit('Map en binary komen niet overeen: timestamp/imagebase. Geen symbolische analyse uitvoeren.')
for line in maptext.splitlines():
    m = re.match(r"\s+[0-9a-f]+:[0-9a-f]+\s+(\S+)\s+([0-9a-f]{8})\s", line, re.I)
    if m:
        symbols.setdefault(int(m[2], 16), []).append(m[1])
functions = sorted(a for a in symbols if any(sec.Characteristics & 0x20000000 and
                           sec.VirtualAddress <= a - pe.OPTIONAL_HEADER.ImageBase <
                           sec.VirtualAddress + sec.Misc_VirtualSize for sec in pe.sections))
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
print(f"{binary} SHA256: {__import__('hashlib').sha256((base/binary).read_bytes()).hexdigest()}")
print(f"PE imagebase: {pe.OPTIONAL_HEADER.ImageBase:08x}; timestamp {pe.FILE_HEADER.TimeDateStamp:08x}")
if '--vtable' in sys.argv:
    for query in sys.argv[2:]:
        term, offset = query.rsplit(':',1)
        for a,names in symbols.items():
            if any(term in s for s in names):
                ptr = struct.unpack('<I',pe.get_data(a+int(offset,0)-pe.OPTIONAL_HEADER.ImageBase,4))[0]
                print(f"VTABLE {'/'.join(names)} +{offset} -> {ptr:08x} {'/'.join(symbols.get(ptr,[]))}")
    sys.exit(0)
if '--xref' in sys.argv:
    from bisect import bisect_right
    wanted = {a for a, names in symbols.items() if any(t in s for t in sys.argv[2:] for s in names)}
    for i, start in enumerate(functions):
        end = functions[i+1] if i+1 < len(functions) else start+512
        # Reset per symbool om na ingebedde data opnieuw correct te decoderen.
        # Kandidaatrefs controleren in de afzonderlijke functie-disassemblage.
        for ins in md.disasm(pe.get_data(start-pe.OPTIONAL_HEADER.ImageBase, end-start), start):
            refs = [op.mem.disp & 0xffffffff for op in ins.operands
                    if op.type == X86_OP_MEM and not op.mem.base and not op.mem.index]
            refs += [op.imm for op in ins.operands if op.type == X86_OP_IMM]
            for a in wanted.intersection(refs):
                idx = bisect_right(functions, ins.address)-1
                owner = functions[idx] if idx >= 0 else 0
                print(f"XREF {ins.address:08x} {ins.mnemonic} {ins.op_str} -> {'/'.join(symbols[a])} IN {'/'.join(symbols.get(owner,[]))}")
    sys.exit(0)
for i, address in enumerate(functions):
    if not any(term in s for term in sys.argv[1:] for s in symbols[address]):
        continue
    end = functions[i+1] if i+1 < len(functions) else address+512
    print(f"\nFUNCTION {address:08x} {' / '.join(symbols[address])} END {end:08x}")
    data = pe.get_data(address - pe.OPTIONAL_HEADER.ImageBase, end-address)
    for ins in md.disasm(data, address):
        notes = []
        for op in ins.operands:
            if op.type == X86_OP_IMM and op.imm in symbols:
                notes.append(' / '.join(symbols[op.imm]))
            elif op.type == X86_OP_IMM and pe.OPTIONAL_HEADER.ImageBase <= op.imm < pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.SizeOfImage:
                raw = pe.get_data(op.imm-pe.OPTIONAL_HEADER.ImageBase, 100).split(b'\0', 1)[0]
                if 4 <= len(raw) < 100 and all(32 <= b < 127 for b in raw):
                    notes.append(repr(raw.decode('ascii')))
            if op.type == X86_OP_MEM and not op.mem.base and not op.mem.index:
                a = op.mem.disp & 0xffffffff
                if a in symbols:
                    notes.append(' / '.join(symbols[a]))
                elif ins.mnemonic.startswith('f') and op.size in (4, 8):
                    try:
                        raw = pe.get_data(a-pe.OPTIONAL_HEADER.ImageBase, op.size)
                        notes.append(f"constant={struct.unpack('<d' if op.size==8 else '<f',raw)[0]:g}")
                    except Exception:
                        pass
        print(f"{ins.address:08x} {ins.bytes.hex():22} {ins.mnemonic:8} {ins.op_str}" +
              (" ; " + " | ".join(notes) if notes else ""))
