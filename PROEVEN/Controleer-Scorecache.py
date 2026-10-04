"""Emulate the original score-table archive round trip with synthetic objects.

No game process, real save, executable or DLL is changed. Archive I/O is mocked;
the actual 0x52dbe0 instructions perform the iteration and memory assignments.
AI-player serialization is excluded by supplying 32 empty player slots.
"""
from pathlib import Path
import hashlib, json, struct, sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EIP, UC_X86_REG_ECX, UC_X86_REG_EAX

PATH = ROOT / 'CTP-og/ctp_program/ctp/civctp.exe'
SHA = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
if hashlib.sha256(PATH.read_bytes()).hexdigest() != SHA:
    raise SystemExit('Engine changed: revalidate archive routine addresses')
pe = pefile.PE(str(PATH))
IMAGE = pe.get_memory_mapped_image()

def check(dimensions):
    machine = Uc(UC_ARCH_X86, UC_MODE_32)
    machine.mem_map(0, 4096)  # Synthetic FS exception-chain head.
    machine.mem_map(0x400000, (len(IMAGE) + 4095) & ~4095)
    machine.mem_write(0x400000, IMAGE)
    machine.mem_map(0x20000000, 0x100000)
    next_address = 0x20010000
    def alloc(data):
        nonlocal next_address
        address = next_address
        next_address += (len(data) + 15) & ~15
        machine.mem_write(address, data)
        return address
    def u32(value): return struct.pack('<I', value)
    nx, ny, nz = dimensions
    world = alloc(bytes(64))
    machine.mem_write(world + 0x14, struct.pack('<hhh', nx, ny, nz))
    machine.mem_write(0xa7dd70, u32(world))
    machine.mem_write(0xa7dd80, u32(alloc(bytes(128))))
    machine.mem_write(0xa7ddfc, u32(0))
    robot = alloc(bytes(0x2500))
    rows, values, layers = [], [], []
    for z in range(nz):
        layer = []
        for x in range(nx):
            row_values = [(1 + len(values) * 997 + y * 197) % 65536 for y in range(ny)]
            # Include high-bit patterns to check exact 16-bit preservation.
            if z == nz - 1 and x == nx - 1: row_values[-1] = 65535
            values.extend(row_values)
            address = alloc(struct.pack('<' + 'H' * ny, *row_values))
            rows.append(address); layer.append(address)
        layers.append(alloc(b''.join(u32(a) for a in layer)))
    machine.mem_write(robot + 0x248c, u32(alloc(b''.join(u32(a) for a in layers))))
    archive_table = alloc(b''.join(u32(a) for a in [0, 0, 0, 0x200f0100, 0x200f0200, 0x200f0300]))
    archive = alloc(u32(archive_table))
    sentinel, stack = 0x200f0000, 0x200eff00
    stream = bytearray(); cursor = 0; storing = True; rebuilds = []
    def hook(uc, address, size, data):
        nonlocal cursor
        if address == 0x5237d0: rebuilds.append(address)
        if address not in (0x200f0100, 0x200f0200, 0x200f0300): return
        sp = uc.reg_read(UC_X86_REG_ESP)
        ret, this = struct.unpack('<II', uc.mem_read(sp, 8))
        if this != archive: raise RuntimeError('Unexpected archive object')
        argc = 1
        if address == 0x200f0300:
            uc.reg_write(UC_X86_REG_EAX, int(storing))
        else:
            pointer, count = struct.unpack('<II', uc.mem_read(sp + 8, 8)); argc = 3
            if address == 0x200f0100:
                if not storing: raise RuntimeError('Store called in load mode')
                stream.extend(uc.mem_read(pointer, count))
            else:
                if storing or cursor + count > len(stream): raise RuntimeError('Invalid read')
                uc.mem_write(pointer, bytes(stream[cursor:cursor + count])); cursor += count
        uc.reg_write(UC_X86_REG_ESP, sp + 4 + argc * 4)
        uc.reg_write(UC_X86_REG_EIP, ret)
    machine.hook_add(UC_HOOK_CODE, hook)
    def run():
        machine.mem_write(stack, struct.pack('<II', sentinel, archive))
        machine.reg_write(UC_X86_REG_ESP, stack)
        machine.reg_write(UC_X86_REG_ECX, robot)
        machine.emu_start(0x52dbe0, sentinel, count=100000)
        if machine.reg_read(UC_X86_REG_EIP) != sentinel:
            raise RuntimeError('Archive routine did not finish')
    run()
    expected = struct.pack('<' + 'H' * len(values), *values)
    stored_exactly = bytes(stream[-len(expected):]) == expected
    for address in rows: machine.mem_write(address, bytes(ny * 2))
    storing = False
    run()
    restored = b''.join(bytes(machine.mem_read(address, ny * 2)) for address in rows)
    result = {'dimensions': dimensions, 'scores': len(values), 'archive_bytes': len(stream),
              'stored_exactly': stored_exactly, 'restored_exactly': restored == expected,
              'read_all_bytes': cursor == len(stream), 'score_rebuild_calls': len(rebuilds)}
    if not all(result[k] for k in ['stored_exactly', 'restored_exactly', 'read_all_bytes']) or rebuilds:
        raise RuntimeError(result)
    return result

if __name__ == '__main__':
    print(json.dumps({'binary_sha256': SHA, 'cases': [check((2, 3, 2)), check((3, 5, 2))],
                      'scope': 'Synthetic archive and empty AI-player slots; no actual save loading'}, indent=2))
