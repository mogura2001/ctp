"""Own goal3 reader; RPM only, no callbacks, writes, game starts or GUI input."""
from original_core import *
import time

N30_HASH='eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'
MANIFEST_HASH='34562e21a9539cccae059a4746ed246039266b6ac8238ff4968c591307fe96ef'
original_binding=trusted_binding
original_verify=verify_loaded

def trusted_binding(variant):
    binding=original_binding('original')
    if variant not in ('original','B2a-N30-TECHNICAL'):
        raise ValueError('Only original and exact N30 are allowed')
    import pefile
    binding['variant']=variant
    original=pefile.PE(data=(ROOT/'CTP-og/ctp_program/ctp/dll/ai/robotcom.dll').read_bytes())
    engine=pefile.PE(data=(ROOT/'CTP-og/ctp_program/ctp/civctp.exe').read_bytes())
    # These are exact small instruction windows at already analysed scalar routes.
    for rva in (0x74b60,0xc2180,0x128f20,0xc2ee3,0xb8660,0xb8a3d):
        raw=engine.get_data(rva,32)
        binding['ranges'].append(dict(module='engine',rva=rva,length=len(raw),expected_hex=raw.hex(),kind='scalar-route-window'))
    mp=ROOT/'PROEVEN/opening-b2/B2a-N30-TECHNICAL.manifest.json'
    if hashlib.sha256(mp.read_bytes()).hexdigest()!=MANIFEST_HASH:
        raise ValueError('N30 manifest changed')
    manifest=json.loads(mp.read_text())
    if manifest['N']!=30 or manifest['candidate_sha256']!=N30_HASH or manifest['payload_rva']!=0xd4000 or manifest['payload_size']!=4348:
        raise ValueError('Not the approved N30 manifest')
    if variant=='B2a-N30-TECHNICAL':
        candidate=(ROOT/'PROEVEN/opening-b2/candidates/B2a-N30-TECHNICAL/robotcom.dll').read_bytes()
        if hashlib.sha256(candidate).hexdigest()!=N30_HASH:raise ValueError('N30 disk identity changed')
        cp=pefile.PE(data=candidate)
        binding['ai'].update(sha256=N30_HASH,size=cp.OPTIONAL_HEADER.SizeOfImage,header=candidate[:cp.OPTIONAL_HEADER.SizeOfHeaders].hex(),sections=[(s.VirtualAddress,s.Misc_VirtualSize,s.SizeOfRawData,s.Characteristics) for s in cp.sections])
        # This single reused original observer window overlaps the approved load hook.
        # Substitute its exact candidate bytes; every other original range must match.
        for r in binding['ranges']:
            if r['module']=='ai':
                current=cp.get_data(r['rva'],r['length'])
                if current!=bytes.fromhex(r['expected_hex']):
                    if r['rva']!=0xfe40 or r['length']!=0x20:
                        raise ValueError('Unexpected changed original observer range')
                    r['expected_hex']=current.hex()
        payload=cp.get_data(0xd4000,4348)
        if hashlib.sha256(payload).hexdigest()!=manifest['payload_sha256']:raise ValueError('N30 payload changed')
        binding['ranges'].append(dict(module='ai',rva=0xd4000,length=4348,expected_hex=payload.hex(),kind='PIC-payload'))
    else:cp=original
    # Five exact instruction windows; no permissive/unverified variant acceptance.
    for rva in (0x413da,0x3625b,0xfe2d,0xfe51,0x61f0):
        binding['sites'].append(dict(rva=rva,expected_hex=cp.get_data(rva,5).hex()))
    binding['manifest_sha256']=MANIFEST_HASH if variant!='original' else None
    return binding

def verify_loaded(*args):
    result=original_verify(*args)
    result.update(all_five_B2_or_original_hookwindows=True,N30_bound=args[1]['variant']=='B2a-N30-TECHNICAL')
    return result

def stable_sample(sample):
    first=sample();time.sleep(0.2);second=sample()
    if first!=second:raise ValueError('Unstable complete snapshot; no turn acceptance')
    return second

def scalar_state(read,player,actor,names):
    read=bounded(read)
    u32=lambda p:struct.unpack('<I',read(checked(p),4))[0]
    i32=lambda p:struct.unpack('<i',read(checked(p),4))[0]
    indexes={}
    for name in ('Religion','Theocracy'):
        matches=[i for i,n in enumerate(names) if n==name]
        if len(matches)!=1:raise ValueError('Advance name absent/ambiguous: '+name)
        indexes[name]=matches[0]
    science=u32(checked(player,0x12ec));known=u32(checked(science,0x1c))
    learned={name:dict(index=index,raw_byte=read(checked(known,index),1)[0]) for name,index in indexes.items()}
    for item in learned.values():item['known']=item['raw_byte']!=0
    return dict(known=learned,active_government=i32(checked(player,0x94)),government_requested=i32(checked(player,0x11d8)),government_deadline=i32(checked(player,0x11dc)),processed_round=i32(checked(player,0x11ac)),round_flag=i32(checked(player,0x11e0)),city_count=i32(u32(checked(actor,0x8c))))

def observe_goal3(read,eb,ab,participants):
    state=observe(read,eb,ab)
    rows={c['civ_id']:c for c in state['civilizations'] if c['civ_id']!=0}
    # Missing participants stay a failed observation, never disappear from the denominator.
    if sorted(rows)!=participants['civ_ids']:raise ValueError('Missing/unexpected fixed-T0 AI participant: '+repr(sorted(rows)))
    u32=lambda p:struct.unpack('<I',read(checked(p),4))[0]
    players=u32(eb+0x67dd80)
    for cid,row in rows.items():
        row['civ_name']=participants['names'].get(str(cid),'UNKNOWN')
        row.update(scalar_state(read,u32(players+4*cid),int(row['ai_actor'],16),state['advance_names']))
    state['civilizations']=list(rows.values())
    state.pop('advance_names')
    return state


class ModuleInfo(C.Structure):
    _fields_ = [('base', C.c_void_p), ('size', W.DWORD), ('entry', C.c_void_p)]

def main():
    parser=argparse.ArgumentParser(description='Read-only fixed-T0 goal3 snapshots; no game starts/writes/callbacks')
    parser.add_argument('--pid',type=int,required=True)
    parser.add_argument('--variant',choices=('original','B2a-N30-TECHNICAL'),required=True)
    parser.add_argument('--run-id',required=True);parser.add_argument('--snapshot-label',required=True)
    parser.add_argument('--turn',type=int,required=True);parser.add_argument('--pass-label',required=True)
    parser.add_argument('--manifest',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    output=args.output.resolve()
    if not output.is_relative_to(FOLDER) or output.suffix!='.json' or output.exists():raise ValueError('Output outside own package or already exists')
    participants=json.loads(args.manifest.read_text(encoding='utf-8-sig'))
    if participants['civ_ids']!=list(range(2,9)):raise ValueError('Unexpected fixed-T0 participants')
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
        state=observe_goal3(read,eb,ab,participants)
        return {'instance':{'pid':args.pid,'creationtime_filetime':(times[0].dwHighDateTime<<32)|times[0].dwLowDateTime,'executable':str(EXE.resolve()),'ai_module':str(DLL.resolve()),'engine_base':eb,'ai_base':ab},'loaded_checks':checks,'state':state}
    try:
        result=stable_sample(sample)
        result.update(run_id=args.run_id,snapshot_label=args.snapshot_label,turn=args.turn,pass_label=args.pass_label,variant=args.variant,binding={'engine_sha256':binding['engine']['sha256'],'ai_sha256':binding['ai']['sha256'],'manifest_sha256':binding['manifest_sha256'],'package_sha256':binding['package_sha256']},stable_twice=True,save_identity_proven=False,atomic_snapshot_proven=False)
        output.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
    except Exception as error:
        output.write_text(json.dumps({'status':'rejected','error':str(error),'variant':args.variant,'run_id':args.run_id,'snapshot_label':args.snapshot_label,'comparison_accepted':False},indent=2)+'\n')
        raise
    finally:k.CloseHandle(handle)


if __name__=='__main__':main()
