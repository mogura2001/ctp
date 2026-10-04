"""Read-only COM binding by validated AI GUID; engine map is deliberately unused.

Usage: python Analyseer-Engine-Interfaces.py Player 0x78 0x130 0x134
Candidate tables require manual inspection of QueryInterface and callers.
"""
from pathlib import Path
import hashlib, re, struct, sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM

ai_path = ROOT / 'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll'
engine_path = ROOT / 'CTP-og/ctp_program/ctp/civctp.exe'
ai = pefile.PE(str(ai_path))
engine = pefile.PE(str(engine_path))
ai_base = ai.OPTIONAL_HEADER.ImageBase
base = engine.OPTIONAL_HEADER.ImageBase
maptext = ai_path.with_suffix('.map').read_text(errors='replace')
stamp = re.search(r'Timestamp is ([0-9a-f]+)', maptext, re.I)
preferred = re.search(r'Preferred load address is ([0-9a-f]+)', maptext, re.I)
if not stamp or not preferred or int(stamp[1],16) != ai.FILE_HEADER.TimeDateStamp or int(preferred[1],16) != ai_base:
    raise SystemExit('AI map/binary mismatch; no symbolic GUID binding performed')
label = sys.argv[1]
symbol = '_CLSID_IC3' + label
match = re.search(r'\s' + re.escape(symbol) + r'\s+([0-9a-f]{8})\s', maptext, re.I)
if not match:
    raise SystemExit('GUID symbol not found: ' + symbol)
guid = ai.get_data(int(match[1],16)-ai_base,16)
locations = []
pos = 0
while (pos := engine.__data__.find(guid,pos)) >= 0:
    locations.append(base + engine.get_rva_from_offset(pos))
    pos += 16
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True
slots = sorted(set([0,4,8] + [int(a,0) for a in sys.argv[2:]]))
print('AI SHA256:', hashlib.sha256(ai_path.read_bytes()).hexdigest())
print('Engine SHA256:', hashlib.sha256(engine_path.read_bytes()).hexdigest())
print(f'AI timestamp {ai.FILE_HEADER.TimeDateStamp:08x}; engine timestamp {engine.FILE_HEADER.TimeDateStamp:08x}')
print(symbol, guid.hex(), 'engine locations', [hex(a) for a in locations])
code_ranges = [(base+s.VirtualAddress,base+s.VirtualAddress+s.Misc_VirtualSize)
               for s in engine.sections if s.Characteristics & 0x20000000]
seen = set()
for section in engine.sections:
    if section.Name.rstrip(b'\0') != b'.rdata':
        continue
    data = section.get_data()
    for off in range(0,len(data)-max(slots)-4,4):
        target = struct.unpack_from('<I',data,off)[0]
        if target in seen or not any(lo <= target < hi for lo,hi in code_ranges):
            continue
        # Reject pointers before the real table that merely sit close to a GUID ref.
        trio = struct.unpack_from('<III',data,off)
        if not all(any(lo <= ptr < hi for lo,hi in code_ranges) for ptr in trio):
            continue
        seen.add(target)
        instructions = list(md.disasm(engine.get_data(target-base,128),target))
        if not any(op.type == X86_OP_IMM and op.imm in locations
                   for ins in instructions for op in ins.operands):
            continue
        print(f'Candidate {label} table {base+section.VirtualAddress+off:08x}; QueryInterface {target:08x}')
        for slot in slots:
            ptr = struct.unpack_from('<I',data,off+slot)[0]
            print(f'SLOT {slot:03x} -> {ptr:08x}')
            for ins in md.disasm(engine.get_data(ptr-base,128 if slot == 0 else 160),ptr):
                print(f'{ins.address:08x} {ins.bytes.hex():22} {ins.mnemonic:8} {ins.op_str}')
                if slot != 0 and ins.mnemonic == 'ret':
                    break
