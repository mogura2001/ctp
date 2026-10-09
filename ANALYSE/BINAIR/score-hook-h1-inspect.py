"""H1: read-only checks of three callsites, PE room, and real getter ABI.

No emulation, process access, PE edits, or gameplay changes.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

path = ROOT / 'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll'
blob = path.read_bytes()
pe = pefile.PE(data=blob)
maptext = path.with_suffix('.map').read_text(errors='replace')
stamp = int(re.search(r'Timestamp is ([0-9a-f]+)', maptext, re.I)[1], 16)
base = int(re.search(r'Preferred load address is ([0-9a-f]+)', maptext, re.I)[1], 16)
assert stamp == pe.FILE_HEADER.TimeDateStamp == 0x37b894e7
assert base == pe.OPTIONAL_HEADER.ImageBase == 0x20000000
assert hashlib.sha256(blob).hexdigest() == '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
md = Cs(CS_ARCH_X86, CS_MODE_32)
checks = []
for address in (0x200784bb, 0x20078517, 0x2007aa35):
    raw = pe.get_data(address-base, 6)
    assert raw.hex() == 'ff9168010000'
    ins = list(md.disasm(raw, address))
    assert len(ins) == 1 and ins[0].size == 6
    checks.append({'address': hex(address), 'bytes': raw.hex(),
                   'instruction': f'{ins[0].mnemonic} {ins[0].op_str}'})
table_end = pe.sections[-1].get_file_offset() + 40
first_raw = min(s.PointerToRawData for s in pe.sections if s.PointerToRawData)
new_header = blob[table_end:table_end+40]
assert table_end+40 <= min(first_raw, pe.OPTIONAL_HEADER.SizeOfHeaders)
assert not any(new_header)
align = lambda n, a: ((n+a-1)//a)*a
proposed_rva = align(max(s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData)
                         for s in pe.sections), pe.OPTIONAL_HEADER.SectionAlignment)
relocs = pe.OPTIONAL_HEADER.DATA_DIRECTORY[5]
security = pe.OPTIONAL_HEADER.DATA_DIRECTORY[4]
out = {
    'mode': 'read-only; no candidate binary produced',
    'dll_sha256': hashlib.sha256(blob).hexdigest(),
    'timestamp': hex(stamp), 'imagebase': hex(base),
    'machine': hex(pe.FILE_HEADER.Machine), 'pe_magic': hex(pe.OPTIONAL_HEADER.Magic),
    'callsite_checks': checks,
    'sections': [{'name': s.Name.rstrip(b'\0').decode(), 'rva': hex(s.VirtualAddress),
                  'virtual_size': hex(s.Misc_VirtualSize), 'raw_offset': hex(s.PointerToRawData),
                  'raw_size': hex(s.SizeOfRawData), 'flags': hex(s.Characteristics)}
                 for s in pe.sections],
    'new_header_offset': hex(table_end), 'header_zero_bytes_checked': 40,
    'first_section_raw': hex(first_raw), 'size_of_headers': hex(pe.OPTIONAL_HEADER.SizeOfHeaders),
    'file_alignment': hex(pe.OPTIONAL_HEADER.FileAlignment),
    'section_alignment': hex(pe.OPTIONAL_HEADER.SectionAlignment),
    'size_of_image': hex(pe.OPTIONAL_HEADER.SizeOfImage),
    'proposed_new_section_rva': hex(proposed_rva),
    'proposed_new_raw_offset': hex(align(len(blob), pe.OPTIONAL_HEADER.FileAlignment)),
    'reloc_directory': {'rva': hex(relocs.VirtualAddress), 'size': hex(relocs.Size)},
    'relocs_stripped': bool(pe.FILE_HEADER.Characteristics & 1),
    'security_directory': {'file_offset': hex(security.VirtualAddress), 'size': hex(security.Size)},
    'imports': [e.dll.decode() for e in getattr(pe, 'DIRECTORY_ENTRY_IMPORT', [])],
    'file_unchanged_after_reads': hashlib.sha256(path.read_bytes()).hexdigest() == hashlib.sha256(blob).hexdigest(),
}
print(json.dumps(out, indent=2))
enginepath = ROOT / 'CTP-og/ctp_program/ctp/civctp.exe'
engineblob = enginepath.read_bytes()
engine = pefile.PE(data=engineblob)
assert hashlib.sha256(engineblob).hexdigest() == 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
assert engine.OPTIONAL_HEADER.ImageBase == 0x400000
print('\nREAL ENGINE WRAPPER 00535500; no civctp.map addresses used')
for ins in md.disasm(engine.get_data(0x535500-0x400000, 0x40), 0x535500):
    print(f'{ins.address:08x} {ins.bytes.hex():22} {ins.mnemonic:8} {ins.op_str}')
    if ins.mnemonic == 'ret':
        assert ins.op_str == '0x10'
        break
else:
    raise AssertionError('No wrapper ret 0x10 at expected function boundary')
