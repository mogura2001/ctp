"""Offline, read-only original-binary binding; never opens a process."""
from pathlib import Path
import hashlib
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

engine_path = ROOT / 'CTP-og/ctp_program/ctp/civctp.exe'
ai_path = ROOT / 'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll'
expected = {
    engine_path: 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79',
    ai_path: '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44',
}
for path, digest in expected.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit('Original identity mismatch: ' + str(path))
    print(path.name, actual)
engine = pefile.PE(str(engine_path))
ai = pefile.PE(str(ai_path))
base = engine.OPTIONAL_HEADER.ImageBase
md = Cs(CS_ARCH_X86, CS_MODE_32)

def dump(address, size):
    print(f'\nRANGE {address:08x}:{size:x}')
    for ins in md.disasm(engine.get_data(address-base, size), address):
        print(f'{ins.address:08x} {ins.bytes.hex():22} {ins.mnemonic:8} {ins.op_str}')

# Actual Science COM table; no mismatching engine linker-map symbols.
for slot in (0x0c, 0x24, 0x50):
    address = struct.unpack('<I', engine.get_data(0x744fe0-base+slot, 4))[0]
    print(f'\nSCIENCE slot {slot:02x} -> {address:08x}')
    dump(address, 0x100)

# AI's validated CLSID_IRobot is used to locate its actual engine consumers.
guid = ai.get_data(0x200896a8-ai.OPTIONAL_HEADER.ImageBase, 16)
print('\nCLSID_IRobot', guid.hex())
locations = []
offset = 0
while (offset := engine.__data__.find(guid, offset)) >= 0:
    locations.append(base + engine.get_rva_from_offset(offset))
    offset += 16
print('Engine GUID addresses:', [hex(value) for value in locations])
for section in engine.sections:
    if not section.Characteristics & 0x20000000:
        continue
    data = section.get_data()
    for address in locations:
        needle = struct.pack('<I', address)
        offset = 0
        while (offset := data.find(needle, offset)) >= 0:
            reference = base + section.VirtualAddress + offset
            print(f'GUID operand reference {reference:08x}; context boundary provisional')
            dump(reference-32, 0x70)
            offset += 4

print('\nDLL exports and engine string operands')
for symbol in ai.DIRECTORY_ENTRY_EXPORT.symbols:
    if not symbol.name or b'CoCreateInstanceRobotCom' not in symbol.name:
        continue
    print('Export', symbol.name.decode(), hex(ai.OPTIONAL_HEADER.ImageBase+symbol.address))
    for needle in (symbol.name, b'CoCreateInstanceRobotCom'):
        offset = 0
        while (offset := engine.__data__.find(needle+b'\0', offset)) >= 0:
            address = base+engine.get_rva_from_offset(offset)
            print('Engine creation-string', needle.decode(), hex(address))
            for section in engine.sections:
                if not section.Characteristics & 0x20000000:
                    continue
                data = section.get_data()
                operand = data.find(struct.pack('<I', address))
                if operand >= 0:
                    reference = base+section.VirtualAddress+operand
                    print(f'Creation-string reference {reference:08x}; boundary provisional')
                    dump(reference-32, 0x100)
            offset += len(needle)
