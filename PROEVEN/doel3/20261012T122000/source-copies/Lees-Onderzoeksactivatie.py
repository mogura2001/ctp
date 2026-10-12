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

ROOT = Path(__file__).resolve().parents[2]
EXE = ROOT / 'CTP-proef/ctp_program/ctp/civctp.exe'
DLL = EXE.parent / 'dll/ai/robotcom.dll'
HASH_EXE = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
HASH_DLL = '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
FOLDER = Path(__file__).resolve().parent
VARIANTS = {
 'original': {'sha256': HASH_DLL},
 'H1-I': {'sha256':'59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0','package':'score-h1','manifest_sha256':'77b1ad5b88343c18ecf7b67de6b2402900b0b39f7edcd0bbd53e1b2bbac7f49e','package_sha256':'cf334df116b5d22aa480f73fab4e715418a2a02da375c7196d65ed7006914a24','payload_size':87,'payload_sha256':'4300f151db39bb2061bf08d3ebd494df2c234ca8b4dd99dd60632f729d67060e'},
 'H3-SCORE_CURRENT': {'sha256':'f93be3629decd38a94117ba774aac3673db2cd2b9e1a0d8a1dde42f7b8e4fd9c','package':'production-h3','manifest_sha256':'a4eb2b27da3caf0b5d39fbaff71485a15ef7b829a50e08930feb40b13c2bc238','package_sha256':'f781d4f361af9e8054f4d3ba5176dd6f4c86b2f27cbf4e0b1c533147bad4a665','payload_size':8640,'payload_sha256':'21873cb38dcbcd39e5ca2f64a2473fe33d3daf11cae4d415c7831704afa65dbf'},
}

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

def goalstate(read, actor, civ, manager, engine_base, ai_base):
    """Registered goals only; capacity is a guard, never a dump length."""
    read = bounded(read)
    u32 = lambda a: struct.unpack('<I', read(a, 4))[0]
    i32 = lambda a: struct.unpack('<i', read(a, 4))[0]
    at = lambda p,o: checked(p,o)
    planner = u32(at(actor,0x94))
    if u32(at(planner,0xa28)) != actor:
        raise ValueError('Planner owner mismatch')
    scheduler = u32(at(planner,0xa2c)); next_id = i32(scheduler)
    if not 0 <= next_id < 0x7fffffff:
        raise ValueError('Scheduler ID negative/overflow')
    count = i32(at(planner,0xa30)); caps = [i32(at(planner,o)) for o in (0xa38,0xa4c,0xa54)]
    if not 0 <= count <= 4096 or any(cap < count for cap in caps):
        raise ValueError('Goal count/capacity outside observation scope')
    pointers, ids = u32(at(planner,0xa48)),u32(at(planner,0xa50))
    def array(pointer):
        out=[]
        for start in range(0,count,2048):
            n=min(2048,count-start);out.extend(struct.unpack('<'+'I'*n,read(at(pointer,4*start),4*n)))
        return out
    goalptrs, goalids = array(pointers),array(ids)
    if any(gid >= next_id for gid in goalids) or any(a >= b for a,b in zip(goalids,goalids[1:])):
        raise ValueError('Goal IDs not sorted/unique/in Scheduler range')
    world = u32(engine_base+0x67dd70)
    # Exact external scorecache allocation/serializer dimensions: World+14h,
    # not H3 terrain-grid globals67df20/22 or canonical gridcoordinates.
    dimensions = struct.unpack('<hhh',read(at(world,0x14),6))
    bounds_ok = all(0 < n <= 32767 for n in dimensions)
    context={'external_world':hex(world),'dimensions':list(dimensions),'bounds_source':'engine serializer52dd31..52ddaf World+14/16/18','ground_only':True,'cache_layers':hex(u32(at(manager,0x248c))) if bounds_ok else None}
    goals=[]
    for pointer,gid in zip(goalptrs,goalids):
        if i32(at(pointer,8)) != gid:
            raise ValueError('Goal ID/pointer pair mismatch')
        vt,kind=u32(pointer),i32(at(pointer,12))
        g={'id':gid,'pointer':hex(pointer),'vtable':hex(vt),'type':kind,'settle':False}
        if vt == ai_base+0x8a558 or kind == 5:
            if vt != ai_base+0x8a558 or kind != 5:
                raise ValueError('GoalSettle vtable/type mismatch')
            flags=u32(at(pointer,0x28));q=struct.unpack('<d',read(at(pointer,0x48),8))[0]
            if not math.isfinite(q) or not 1 <= q <= 32767 or q != int(q):
                raise ValueError('Invalid positive integer GoalSettle Q')
            position=u32(at(pointer,0x54));xyz=struct.unpack('<hhh',read(position,6));x,y,z=xyz
            if z != 0 or x < 0 or y < 0:
                raise ValueError('GoalSettle outside supported ground coordinates')
            g.update(settle=True,flags=flags,pending_deletion=bool(flags&0x20),position_pointer=hex(position),position=list(xyz),Q=int(q),B=None,Q_minus_current_B=None,cache_status='bounds-unavailable')
            if bounds_ok:
                if not x < dimensions[0] or not y < dimensions[1] or not z < dimensions[2]:
                    raise ValueError('GoalSettle outside external cache bounds')
                layer=u32(at(manager,0x248c));columns=u32(at(layer,4*z));row=u32(at(columns,4*x));b=struct.unpack('<h',read(at(row,2*y),2))[0]
                g.update(B=b,Q_minus_current_B=int(q)-b,cache_status='current-snapshot-only',cache_path=[hex(layer),hex(columns),hex(row)])
            goals.append(g)
        else:
            goals.append(g)
    return {'civ_id':civ,'ai_actor':hex(actor),'planner':hex(planner),'scheduler':hex(scheduler),'aimap':hex(u32(at(actor,0x80))),'world_interface':hex(u32(at(actor,0x30))),'next_id':next_id,'count':count,'capacities':caps,'goal_array':hex(pointers),'id_array':hex(ids),'all_goal_ids':goalids,'cache_context':context,'goals':goals}

def decode_h3(read, engine_base, ai_base):
    read=bounded(read);result=observe(read,engine_base,ai_base)
    # Preserve observe/research semantics; H3 measures normal AI only.
    result['civilizations']=[civ for civ in result['civilizations'] if 0 < civ['civ_id'] < 32]
    manager=struct.unpack('<I',read(engine_base+0x67ddb8,4))[0]
    for civ in result['civilizations']:
        actor=int(civ['ai_actor'],16)
        civ['settlement']=goalstate(read,actor,civ['civ_id'],manager,engine_base,ai_base)
        # Preserve canonical Player identity alongside unchanged research output.
        wrapper=struct.unpack('<I',read(actor+0x44,4))[0]
        civ['player']=hex(struct.unpack('<I',read(wrapper+8,4))[0])
    result['manager']=hex(manager)
    return result

def stable_sample(sample):
    first,second=sample(),sample()
    if first != second:
        raise ValueError('Unstable complete snapshot; pair not accepted')
    return second

def compare_snapshots(a,b):
    if a.get('snapshot_label')!='A' or b.get('snapshot_label')!='B' or not a.get('stable_twice') or not b.get('stable_twice'):
        raise ValueError('Invalid A/B snapshot labels/stability')
    for key in ('run_id','pass_label','instance','variant','binding'):
        if a.get(key)!=b.get(key):raise ValueError('Snapshot instance/context mismatch: '+key)
    ac={c['civ_id']:c for c in a['state']['civilizations'] if 0 < c['civ_id'] < 32};bc={c['civ_id']:c for c in b['state']['civilizations'] if 0 < c['civ_id'] < 32}
    if ac.keys()!=bc.keys():raise ValueError('Snapshot civilization context changed')
    new=[]
    for civ,after in bc.items():
        before=ac[civ];sa,sb=before['settlement'],after['settlement']
        for key in ('ai_actor','player'):
            if before[key]!=after[key]:raise ValueError('Snapshot owner changed')
        for key in ('planner','scheduler','aimap','world_interface','cache_context'):
            if sa[key]!=sb[key]:raise ValueError('Snapshot Planner/cache context changed')
        if sb['next_id'] < sa['next_id'] or sb['next_id'] >= 0x7fffffff:raise ValueError('Scheduler counter decreased/overflow')
        prior=set(sa['all_goal_ids'])
        for g in sb['goals']:
            if g['id'] not in prior:
                if not sa['next_id']<=g['id']<sb['next_id']:raise ValueError('New goal outside proven ID interval')
                if g['settle']:
                    new.append({'civ_id':civ,**g,'new_id_interval':[sa['next_id'],sb['next_id']],'meaning':'current Q/B only; creation-cache stability and bonus causality unproven'})
    visible=any(g['B'] is not None for g in new)
    return {'status':'new-registered-goal-state-observable' if visible else 'not-observable-at-this-moment','new_goal_settle':new,'unconditional_bonus_proven':False,'new_heap_ordering_proven':False,'real_AI_overhead_proven':False,'save_identity_proven':False}

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
    return {'advance_count': count, 'civilizations': civs}

class ModuleInfo(C.Structure):
    _fields_ = [('base', C.c_void_p), ('size', W.DWORD), ('entry', C.c_void_p)]

def main_h3():
    parser=argparse.ArgumentParser(description='Explicitly authorized read-only H3 snapshots; no game starts/writes/callbacks')
    parser.add_argument('--pid',type=int,required=True)
    parser.add_argument('--variant',choices=tuple(VARIANTS),required=True)
    parser.add_argument('--run-id',required=True);parser.add_argument('--snapshot-label',choices=('A','B'),required=True)
    parser.add_argument('--turn',type=int,required=True);parser.add_argument('--pass-label',required=True)
    parser.add_argument('--before',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    output=args.output.resolve()
    if output.parent!=FOLDER or not output.name.startswith('activatie-h3-') or output.suffix!='.json':raise ValueError('Output outside assigned activation results')
    if (args.snapshot_label=='B')!=(args.before is not None):raise ValueError('B requires A-result; A cannot take --before')
    binding=trusted_binding(args.variant)
    for file,key in ((EXE,'engine'),(DLL,'ai')):
        if hashlib.sha256(file.read_bytes()).hexdigest()!=binding[key]['sha256']:raise ValueError('Actual proof diskhash mismatch')
    k,p=C.WinDLL('kernel32',use_last_error=True),C.WinDLL('psapi',use_last_error=True)
    k.OpenProcess.argtypes,k.OpenProcess.restype=[W.DWORD,W.BOOL,W.DWORD],W.HANDLE
    k.CloseHandle.argtypes=[W.HANDLE]
    k.QueryFullProcessImageNameW.argtypes=[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)]
    k.ReadProcessMemory.argtypes=[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)]
    k.GetProcessTimes.argtypes=[W.HANDLE,C.POINTER(W.FILETIME),C.POINTER(W.FILETIME),C.POINTER(W.FILETIME),C.POINTER(W.FILETIME)]
    p.EnumProcessModulesEx.argtypes=[W.HANDLE,C.POINTER(W.HMODULE),W.DWORD,C.POINTER(W.DWORD),W.DWORD]
    p.GetModuleFileNameExW.argtypes=[W.HANDLE,W.HMODULE,W.LPWSTR,W.DWORD]
    p.GetModuleInformation.argtypes=[W.HANDLE,W.HMODULE,C.POINTER(ModuleInfo),W.DWORD]
    handle=k.OpenProcess(0x410,False,args.pid) # QUERY_INFORMATION|VM_READ only
    if not handle:raise OSError('Cannot open exact authorized proof process readhandle')
    def read(address,size):
        data,actual=C.create_string_buffer(size),C.c_size_t()
        if not k.ReadProcessMemory(handle,address,data,size,C.byref(actual)) or actual.value!=size:raise OSError('Incomplete RPM read')
        return data.raw
    read=bounded(read)
    def sample():
        for file,key in ((EXE,'engine'),(DLL,'ai')):
            if hashlib.sha256(file.read_bytes()).hexdigest()!=binding[key]['sha256']:raise ValueError('Actual proof diskhash changed')
        name,length=C.create_unicode_buffer(32768),W.DWORD(32768)
        if not k.QueryFullProcessImageNameW(handle,0,name,C.byref(length)) or Path(name.value).resolve()!=EXE.resolve():raise ValueError('Exact proof readhandle identity mismatch')
        times=[W.FILETIME() for _ in range(4)]
        if not k.GetProcessTimes(handle,*[C.byref(t) for t in times]):raise OSError('Cannot bind process creationtime')
        if times[1].dwLowDateTime or times[1].dwHighDateTime:raise ValueError('Process exited during snapshot')
        modules,needed=(W.HMODULE*1024)(),W.DWORD()
        if not p.EnumProcessModulesEx(handle,modules,C.sizeof(modules),C.byref(needed),3) or needed.value>C.sizeof(modules) or needed.value%C.sizeof(W.HMODULE):raise OSError('Incomplete module enumeration')
        found={}
        for module in modules[:needed.value//C.sizeof(W.HMODULE)]:
            filename=C.create_unicode_buffer(32768)
            if not p.GetModuleFileNameExW(handle,module,filename,32768):raise OSError('Cannot confirm module path')
            path=Path(filename.value).resolve()
            if path in (EXE.resolve(),DLL.resolve()):
                info=ModuleInfo()
                if path in found or not p.GetModuleInformation(handle,module,C.byref(info),C.sizeof(info)):raise ValueError('Ambiguous/unreadable trusted module')
                found[path]=(int(info.base),int(info.size))
        if set(found)!={EXE.resolve(),DLL.resolve()}:raise ValueError('Exact proof engine/AI modulepaths missing')
        eb,es=found[EXE.resolve()];ab,az=found[DLL.resolve()]
        checks=verify_loaded(read,binding,eb,ab,{'engine':es,'ai':az})
        state=decode_h3(read,eb,ab)
        return {'instance':{'pid':args.pid,'creationtime_filetime':(times[0].dwHighDateTime<<32)|times[0].dwLowDateTime,'executable':str(EXE.resolve()),'ai_module':str(DLL.resolve()),'engine_base':eb,'ai_base':ab},'loaded_checks':checks,'state':state}
    try:
        result=stable_sample(sample)
        result.update(run_id=args.run_id,snapshot_label=args.snapshot_label,turn=args.turn,pass_label=args.pass_label,variant=args.variant,binding={'engine_sha256':binding['engine']['sha256'],'ai_sha256':binding['ai']['sha256'],'manifest_sha256':binding['manifest_sha256'],'package_sha256':binding['package_sha256']},stable_twice=True,save_identity_proven=False,atomic_snapshot_proven=False)
        if args.before:result['comparison']=compare_snapshots(json.loads(args.before.read_text(encoding='utf-8-sig')),result)
        output.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
    except Exception as error:
        output.write_text(json.dumps({'status':'rejected','error':str(error),'variant':args.variant,'run_id':args.run_id,'snapshot_label':args.snapshot_label,'comparison_accepted':False},indent=2)+'\n')
        raise
    finally:k.CloseHandle(handle)

if __name__ == '__main__':
    main_h3()
