"""Strictly read-only CTP-proef observation; no injection, hooks or process starts.

Future separately authorized runtime: explicit --pid, --variant, --run-id,
--snapshot-label A/B, --turn, --pass-label, --output; B also requires --before.
This observer does NOT prove which save was loaded. Quiet boundaries only.
"""
from pathlib import Path
import argparse
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import struct
import math
import sys
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[3]
EXE = ROOT / 'CTP-proef/ctp_program/ctp/civctp.exe'
DLL = EXE.parent / 'dll/ai/robotcom.dll'
HASH_EXE = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
HASH_DLL = '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
FOLDER = Path(__file__).resolve().parent
VARIANTS = {'original': {'sha256': HASH_DLL}}

def checked(address, offset=0):
    result = address + offset
    if not 0x10000 <= result <= 0xffffffff:
        raise ValueError('Invalid checked32 pointer/offset')
    return result

def bounded(read):
    def exact(address, size):
        checked(address)
        if not 1 <= size <= 8192 or address + size > 0x100000000:
            raise ValueError('Invalid bounded32 read')
        result = read(address, size)
        if len(result) != size:
            raise ValueError('Incomplete bounded read')
        return result
    return exact

def trusted_binding(variant):
    """Pinned disk and instruction/vtable expectations, no process opened."""
    if variant not in VARIANTS:raise ValueError('Untrusted AI variant')
    sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    digest=lambda b:hashlib.sha256(b).hexdigest()
    original_path=ROOT/'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll';engine_path=ROOT/'CTP-og/ctp_program/ctp/civctp.exe'
    original,engine=original_path.read_bytes(),engine_path.read_bytes()
    if digest(original)!=HASH_DLL or digest(engine)!=HASH_EXE:raise ValueError('Original reference identity mismatch')
    entry=VARIANTS[variant];manifest=None
    if variant=='original':candidate=original
    else:
        folder=ROOT/'PROEVEN'/entry['package'];mp=folder/(variant+'.manifest.json');pp=folder/'package-manifest.json'
        if digest(mp.read_bytes())!=entry['manifest_sha256'] or digest(pp.read_bytes())!=entry['package_sha256']:raise ValueError('Pinned variant/package manifest changed')
        manifest=json.loads(mp.read_text());candidate=(folder/'candidates'/variant/'robotcom.dll').read_bytes()
        if manifest['candidate_sha256']!=entry['sha256'] or manifest['original_sha256']!=HASH_DLL:raise ValueError('Manifest binary identity mismatch')
    if digest(candidate)!=entry['sha256']:raise ValueError('Trusted candidate diskhash mismatch')
    ep,op,cp=pefile.PE(data=engine),pefile.PE(data=original),pefile.PE(data=candidate)
    if ep.OPTIONAL_HEADER.ImageBase!=0x400000 or ep.FILE_HEADER.TimeDateStamp!=0x37d6f702 or ep.OPTIONAL_HEADER.DllCharacteristics&0x40:raise ValueError('Unsupported engine PE')
    if cp.OPTIONAL_HEADER.ImageBase!=0x20000000 or cp.FILE_HEADER.TimeDateStamp!=0x37b894e7:raise ValueError('Unsupported AI PE')
    ranges=[];md=Cs(CS_ARCH_X86,CS_MODE_32)
    # Existing full function-bound ranges. No new disassembler/scanner route.
    ai_ranges=[(0x21f3,0x21f9),(0x3b6a,0x3b70),(0x1c1a,0x1c20),(0x2d9e,0x2da4),(0xfcc0,0xfd30),(0xfe40,0xfe60),(0x66b80,0x66c80),(0x6d3d0,0x6d830),(0x6dbf0,0x6e240),(0x6ed80,0x6ef20),(0x6f0c0,0x6f140),(0x68310,0x683f0),(0x6f4c0,0x6f4e0),(0x70180,0x701e0),(0x70eb0,0x71030),(0x43100,0x43250),(0x43360,0x43500),(0x48600,0x48700),(0x48700,0x48770),(0x682d0,0x68310),(0x68580,0x68600)]
    engine_ranges=[(0x11c6ea,0x11c6f9),(0x12dc75,0x12dcd2),(0x1309b0,0x1309d8),(0x66320,0x66333),(0x1238d0,0x1238f3),(0x135500,0x13551e),(0x12dd31,0x12ddaf)]
    for module,pe,pairs in [('ai',op,ai_ranges),('engine',ep,engine_ranges)]:
        for start,end in pairs:
            raw=pe.get_data(start,end-start)
            if sum(i.size for i in md.disasm(raw,start))!=len(raw):raise ValueError('Binding range not complete instructions: '+hex(start))
            ranges.append({'module':module,'rva':start,'length':len(raw),'expected_hex':raw.hex(),'kind':'instructions'})
    for module,pe,start,length in [('ai',op,0x89728,0x20),('ai',op,0x8a558,0x20),('engine',ep,0x344fe0,0x54),('engine',ep,0x3452e0+0x168,4)]:ranges.append({'module':module,'rva':start,'length':length,'expected_hex':pe.get_data(start,length).hex(),'kind':'vtable'})
    relocs=[]
    for block in getattr(op,'DIRECTORY_ENTRY_BASERELOC',[]):
        for relocation in block.entries:
            if relocation.type==3:relocs.append(relocation.rva)
            elif relocation.type!=0:raise ValueError('Unsupported original PE relocation type')
    for r in ranges:
        if r['module']=='ai' and cp.get_data(r['rva'],r['length'])!=bytes.fromhex(r['expected_hex']):raise ValueError('Candidate decoder range changed')
    sites=[]
    for rva in (0x784bb,0x78517,0x7aa35):
        raw=cp.get_data(rva,6);expected=bytes.fromhex('ff9168010000') if variant=='original' else b'\xe8'+struct.pack('<i',0xd4000-rva-5)+b'\x90'
        if raw!=expected:raise ValueError('Trusted scorecall binding mismatch')
        sites.append({'rva':rva,'expected_hex':raw.hex()})
    if manifest:
        payload=cp.get_data(0xd4000,entry['payload_size'])
        if digest(payload)!=entry['payload_sha256'] or manifest['payload_size']!=len(payload) or manifest['payload_sha256']!=digest(payload):raise ValueError('Pinned payload mismatch')
        ranges.append({'module':'ai','rva':0xd4000,'length':len(payload),'expected_hex':payload.hex(),'kind':'PIC-payload'})
    def info(pe,data):return {'sha256':digest(data),'size':pe.OPTIONAL_HEADER.SizeOfImage,'header':data[:pe.OPTIONAL_HEADER.SizeOfHeaders].hex(),'sections':[(s.VirtualAddress,s.Misc_VirtualSize,s.SizeOfRawData,s.Characteristics) for s in pe.sections]}
    return {'variant':variant,'engine':info(ep,engine),'ai':info(cp,candidate),'sites':sites,'ranges':ranges,'original_HIGHLOW':relocs,'engine_base_required':0x400000,'ai_preferred_base':0x20000000,'manifest_sha256':entry.get('manifest_sha256'),'package_sha256':entry.get('package_sha256')}

def verify_loaded(read,binding,engine_base,ai_base,module_sizes):
    read=bounded(read)
    if engine_base!=0x400000:raise ValueError('Unsupported actual engine base')
    def same(base,rva,expected):
        for off in range(0,len(expected),8192):
            block=expected[off:off+8192]
            if read(checked(base,rva+off),len(block))!=block:raise ValueError('Loaded byte identity mismatch at '+hex(rva+off))
    for module,base in [('engine',engine_base),('ai',ai_base)]:
        if module_sizes[module]!=binding[module]['size']:raise ValueError('Loaded SizeOfImage mismatch')
        same(base,0,bytes.fromhex(binding[module]['header']))
    for site in binding['sites']:same(ai_base,site['rva'],bytes.fromhex(site['expected_hex']))
    delta=ai_base-0x20000000
    for item in binding['ranges']:
        expected=bytearray.fromhex(item['expected_hex'])
        if item['module']=='ai' and item['kind']!='PIC-payload':
            for rva in binding['original_HIGHLOW']:
                if item['rva']<=rva<item['rva']+len(expected):
                    off=rva-item['rva']
                    if off+4>len(expected):raise ValueError('Partial HIGHLOW boundary')
                    struct.pack_into('<I',expected,off,(struct.unpack_from('<I',expected,off)[0]+delta)&0xffffffff)
        same(ai_base if item['module']=='ai' else engine_base,item['rva'],expected)
    return {'headers_sections_sizes':True,'all_three_scorecalls':True,'payload_and_original_ranges':True,'only_original_HIGHLOW_relocation_adjustment':True}

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
    return {'advance_count': count, 'advance_names': names, 'civilizations': civs}

