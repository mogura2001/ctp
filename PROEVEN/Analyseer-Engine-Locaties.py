"""Read-only engine inspection; never apply the mismatched civctp.map addresses.

--world / --archive identify COM interfaces by GUID from the matching AI DLL.
--refs lists raw 32-bit references (candidates, not decoded instructions).
--tokens reads the integer preceding exact, NUL-terminated token keywords.
Other arguments are VA:length (both hexadecimal), e.g. 5238d0:100.
"""
from pathlib import Path
import sys, struct, hashlib
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_MEM, X86_OP_IMM

path = ROOT / 'CTP-og/ctp_program/ctp/civctp.exe'
pe = pefile.PE(str(path)); base = pe.OPTIONAL_HEADER.ImageBase
md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True
print('Engine SHA256:', hashlib.sha256(path.read_bytes()).hexdigest())
print(f'Imagebase {base:08x}; timestamp {pe.FILE_HEADER.TimeDateStamp:08x}; no engine map addresses used')

def dump(address, length):
    print(f'\nRANGE {address:08x}:{length:x}')
    for ins in md.disasm(pe.get_data(address-base, length), address):
        notes = []
        for op in ins.operands:
            if op.type == X86_OP_MEM and not op.mem.base and not op.mem.index and ins.mnemonic.startswith('f') and op.size in (4,8):
                try:
                    notes.append('constant=' + str(struct.unpack('<f' if op.size==4 else '<d', pe.get_data(op.mem.disp-base,op.size))[0]))
                except Exception:
                    pass
        print(f'{ins.address:08x} {ins.bytes.hex():22} {ins.mnemonic:8} {ins.op_str}' + (' ; '+', '.join(notes) if notes else ''))

if '--refs' in sys.argv:
    for arg in sys.argv[2:]:
        target=int(arg,16); pattern=struct.pack('<I',target)
        for section in pe.sections:
            data=section.get_data(); pos=0
            while (pos := data.find(pattern,pos)) >= 0:
                print(f'RAW REF {base+section.VirtualAddress+pos:08x} -> {target:08x} in {section.Name.rstrip(bytes([0])).decode()}')
                pos+=1
elif '--tokens' in sys.argv:
    for arg in sys.argv[2:]:
        pattern=arg.encode('ascii')+bytes([0]); pos=0
        while (pos := pe.__data__.find(pattern,pos)) >= 0:
            print(f'TOKEN CANDIDATE {base+pe.get_rva_from_offset(pos):08x} {arg} preceding-int={struct.unpack_from("<I",pe.__data__,pos-4)[0]}')
            pos+=len(pattern)
elif '--calls' in sys.argv:
    # Candidate direct relative calls; inspect the caller to rule out data bytes.
    for arg in sys.argv[2:]:
        target=int(arg,16)
        for section in pe.sections:
            if not section.Characteristics & 0x20000000: continue
            data=section.get_data(); start=base+section.VirtualAddress
            for off in range(len(data)-5):
                if data[off]==0xe8 and start+off+5+struct.unpack_from('<i',data,off+1)[0]==target:
                    print(f'CALL CANDIDATE {start+off:08x} -> {target:08x}')
elif '--world' in sys.argv or '--archive' in sys.argv:
    ai = pefile.PE(str(ROOT / 'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll'))
    if ai.FILE_HEADER.TimeDateStamp != 0x37b894e7 or ai.OPTIONAL_HEADER.ImageBase != 0x20000000:
        raise SystemExit('AI binary changed; revalidate GUID symbol before using it')
    archive = '--archive' in sys.argv
    label = 'Archive' if archive else 'World'
    guid = ai.get_data(0x896e8 if archive else 0x896d8,16) # GUID symbols from matching robotcom.map
    print(label+' GUID:', guid.hex())
    guid_offsets = []; pos=0
    while (pos := pe.__data__.find(guid,pos)) >= 0:
        guid_offsets.append(base+pe.get_rva_from_offset(pos)); pos+=16
    print('GUID locations:', [hex(a) for a in guid_offsets])
    code_ranges = [(base+s.VirtualAddress,base+s.VirtualAddress+s.Misc_VirtualSize) for s in pe.sections if s.Characteristics & 0x20000000]
    seen=set()
    for section in pe.sections:
        if section.Name.rstrip(b'\0') != b'.rdata': continue
        data=section.get_data()
        for off in range(0,len(data)-0x16c,4):
            target=struct.unpack_from('<I',data,off)[0]
            if target in seen or not any(lo<=target<hi for lo,hi in code_ranges):continue
            seen.add(target)
            # QueryInterface must reference the exact World GUID; inspect candidate body.
            instructions=list(md.disasm(pe.get_data(target-base,112),target))
            if not any(op.type==X86_OP_IMM and op.imm in guid_offsets for ins in instructions for op in ins.operands):continue
            table=base+section.VirtualAddress+off
            print(f'Candidate {label} table {table:08x}, QueryInterface {target:08x}')
            for slot in ([0,4,8,0xc,0x10,0x14] if archive else [0,4,8,0x164,0x168]):
                ptr=struct.unpack_from('<I',data,off+slot)[0]
                print(f'SLOT {slot:03x} -> {ptr:08x}')
                dump(ptr,112 if slot==0 else 80 if archive else 32)
else:
    for arg in sys.argv[1:]:
        address,length=arg.split(':'); dump(int(address,16),int(length,16))
