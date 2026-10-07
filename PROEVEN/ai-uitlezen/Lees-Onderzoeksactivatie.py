"""Strictly read-only CTP-proef observation; no injection, hooks or process starts.

Use: python Lees-Onderzoeksactivatie.py --pid <CTP-proef PID>
This observer does NOT prove which save was loaded. Run at a quiet turn boundary.
"""
from pathlib import Path
import argparse
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import struct

ROOT = Path(__file__).resolve().parents[2]
EXE = ROOT / 'CTP-proef/ctp_program/ctp/civctp.exe'
DLL = EXE.parent / 'dll/ai/robotcom.dll'
HASH_EXE = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
HASH_DLL = '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'

def observe(read, engine_base, ai_base):
    """Decode only the original, instruction-bound object chain."""
    def u32(address):
        return struct.unpack('<I', read(address, 4))[0]
    def i32(address):
        return struct.unpack('<i', read(address, 4))[0]
    engine = lambda address: engine_base + address - 0x400000
    ai = lambda address: ai_base + address - 0x20000000
    manager = u32(engine(0xa7ddb8))
    players = u32(engine(0xa7dd80))
    database = u32(engine(0xa7dd00))
    strings = u32(engine(0xa7dcfc))
    count = i32(database)
    if not 0 < count <= 512:
        raise ValueError('Invalid advance count')
    records, names = u32(database+8), []
    for index in range(count):
        string_id = u32(records+0x8c*index)
        if string_id > 100000:
            raise ValueError('Invalid advance string ID')
        entry = u32(u32(strings+4)+4*string_id)
        name_pointer = u32(entry+8)
        name = bytearray()
        for offset in range(128):
            char = read(name_pointer+offset, 1)
            if char == b'\0':
                break
            name.extend(char)
        else:
            raise ValueError('Unterminated advance name')
        names.append(name.decode('ascii'))
    def name(index):
        if index == -1:
            return None
        if not 0 <= index < count:
            raise ValueError('Advance index outside engine database')
        return names[index]
    civs = []
    for civ in range(32):
        player, robot = u32(players+4*civ), u32(manager+0x220c+4*civ)
        if not player or not robot:
            continue
        if u32(player+0x1190):
            continue  # Same actor exclusion as the original manager Load loop.
        if u32(robot) != ai(0x20089728):
            raise ValueError('RobotCOM vtable mismatch')
        actor = u32(robot+8)
        wrapper = u32(actor+0x44)
        if u32(wrapper) != engine(0x744fe0):
            raise ValueError('Science interface vtable mismatch')
        if u32(wrapper+8) != player or i32(wrapper+0xc) != civ or i32(actor+0x20) != civ:
            raise ValueError('Civilization ownership mismatch')
        aip, science = u32(actor+0x94)+0x20, u32(actor+0x120)
        if u32(aip+0x800) != actor:
            raise ValueError('Effective AIP owner mismatch')
        container, indexes = u32(aip+0x7fc), []
        if container:
            length = i32(container+4)
            if not 0 <= length <= 1024:
                raise ValueError('Invalid effective research-list length')
            data = u32(container)
            indexes = [i32(data+4*index) for index in range(length)]
        requested, current = i32(science+0xbc), i32(u32(player+0x12ec)+8)
        rechoose = i32(science+0xb8)
        if rechoose not in (0, 1):
            raise ValueError('Unexpected rechoose flag')
        civs.append({'civ_id': civ, 'ai_actor': hex(actor), 'effective_aip': hex(aip),
                     'research_list': [{'index': index, 'name': name(index)} for index in indexes],
                     'rechoose': rechoose, 'last_ai_request': {'index': requested, 'name': name(requested)},
                     'engine_current': {'index': current, 'name': name(current)}})
    if not civs:
        raise ValueError('No validated live AI actors')
    return {'advance_count': count, 'civilizations': civs}

class ModuleInfo(C.Structure):
    _fields_ = [('base', C.c_void_p), ('size', W.DWORD), ('entry', C.c_void_p)]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pid', type=int, required=True)
    args = parser.parse_args()
    k, p = C.WinDLL('kernel32', use_last_error=True), C.WinDLL('psapi', use_last_error=True)
    k.OpenProcess.argtypes, k.OpenProcess.restype = [W.DWORD, W.BOOL, W.DWORD], W.HANDLE
    k.CloseHandle.argtypes = [W.HANDLE]
    k.QueryFullProcessImageNameW.argtypes = [W.HANDLE, W.DWORD, W.LPWSTR, C.POINTER(W.DWORD)]
    k.ReadProcessMemory.argtypes = [W.HANDLE, C.c_void_p, C.c_void_p, C.c_size_t, C.POINTER(C.c_size_t)]
    p.EnumProcessModulesEx.argtypes = [W.HANDLE, C.POINTER(W.HMODULE), W.DWORD, C.POINTER(W.DWORD), W.DWORD]
    p.GetModuleFileNameExW.argtypes = [W.HANDLE, W.HMODULE, W.LPWSTR, W.DWORD]
    p.GetModuleInformation.argtypes = [W.HANDLE, W.HMODULE, C.POINTER(ModuleInfo), W.DWORD]
    identity = k.OpenProcess(0x1000, False, args.pid)
    if not identity:
        raise OSError('Cannot query process identity')
    try:
        path, length = C.create_unicode_buffer(32768), W.DWORD(32768)
        if not k.QueryFullProcessImageNameW(identity, 0, path, C.byref(length)):
            raise OSError('Cannot query executable path')
        if Path(path.value).resolve() != EXE.resolve():
            raise ValueError('Refused: process executable is not the exact CTP-proef executable')
    finally:
        k.CloseHandle(identity)
    for file, digest in ((EXE, HASH_EXE), (DLL, HASH_DLL)):
        if hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            raise ValueError('Refused: on-disk original binary identity mismatch')
    handle = k.OpenProcess(0x410, False, args.pid)  # QUERY_INFORMATION | VM_READ only.
    if not handle:
        raise OSError('Cannot open controlled CTP-proef process for read access')
    try:
        # Recheck identity on the actual read handle, avoiding a PID reuse gap.
        length = W.DWORD(32768)
        if not k.QueryFullProcessImageNameW(handle, 0, path, C.byref(length)) or Path(path.value).resolve() != EXE.resolve():
            raise ValueError('Executable identity changed')
        modules, needed = (W.HMODULE*1024)(), W.DWORD()
        if not p.EnumProcessModulesEx(handle, modules, C.sizeof(modules), C.byref(needed), 3) or needed.value > C.sizeof(modules):
            raise OSError('Cannot enumerate complete module identities')
        found = {}
        for module in modules[:needed.value//C.sizeof(W.HMODULE)]:
            filename = C.create_unicode_buffer(32768)
            if not p.GetModuleFileNameExW(handle, module, filename, 32768):
                raise OSError('Cannot establish module path')
            module_path = Path(filename.value).resolve()
            if module_path in (EXE.resolve(), DLL.resolve()):
                info = ModuleInfo()
                if not p.GetModuleInformation(handle, module, C.byref(info), C.sizeof(info)):
                    raise OSError('Cannot read module identity')
                found[module_path] = info.base
        if set(found) != {EXE.resolve(), DLL.resolve()}:
            raise ValueError('Refused: exact CTP-proef engine and AI module paths are required')
        def read(address, size):
            if not 0x10000 <= address <= 0xffffffff or not 0 < size <= 8192 or address+size > 0x100000000:
                raise ValueError('Invalid bounded 32-bit memory read')
            data, actual = C.create_string_buffer(size), C.c_size_t()
            if not k.ReadProcessMemory(handle, address, data, size, C.byref(actual)) or actual.value != size:
                raise OSError('Unreadable or incomplete process memory')
            return data.raw
        for file in (EXE, DLL):
            image = file.read_bytes()
            header_offset = struct.unpack_from('<I', image, 0x3c)[0]
            module_base = found[file.resolve()]
            if read(module_base, 64) != image[:64] or read(module_base+header_offset, 24) != image[header_offset:header_offset+24]:
                raise ValueError('In-memory module header identity mismatch')
        first = observe(read, found[EXE.resolve()], found[DLL.resolve()])
        second = observe(read, found[EXE.resolve()], found[DLL.resolve()])
        if first != second:
            raise ValueError('AI state changed during observation; retry at a quiet turn boundary')
        print(json.dumps({'pid': args.pid, 'executable': str(EXE.resolve()),
                          'stable_twice': True, 'save_identity_proven': False, **second}, indent=2))
    finally:
        k.CloseHandle(handle)

if __name__ == '__main__':
    main()
