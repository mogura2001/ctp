"""Own goal3 reader; RPM only, no callbacks, writes, game starts or GUI input."""
from original_core import *
import time

BASE_HASH='eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'
NEW_HASH='8610db83d4e424006f6c8ee3912bac11fd432dd2bb6264c7c9ed5b94fe67dc17'
MANIFEST_HASH='6bf3d57db8aa1f9c36ae5407292cfd597175420c22e16996a5d593737f8f3437'
original_binding=trusted_binding
original_verify=verify_loaded

def trusted_binding(variant):
    binding=original_binding('original')
    if variant not in ('release-v1','U30-40'):raise ValueError('Only exact tested release or reviewed U30-40')
    import pefile
    mp=FOLDER.parent/'candidate-manifest.json'
    if hashlib.sha256(mp.read_bytes()).hexdigest()!=MANIFEST_HASH:raise ValueError('C1 manifest changed')
    manifest=json.loads(mp.read_text('utf-8'))
    cpbytes=(FOLDER/'candidate'/('variant' if variant=='U30-40' else 'baseline')/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll').read_bytes()
    expected=NEW_HASH if variant=='U30-40' else BASE_HASH
    if hashlib.sha256(cpbytes).hexdigest()!=expected:raise ValueError('Exact staged AI changed')
    cp=pefile.PE(data=cpbytes);ep=pefile.PE(data=(ROOT/'CTP-og/ctp_program/ctp/civctp.exe').read_bytes())
    binding['variant']=variant
    binding['ai'].update(sha256=expected,size=cp.OPTIONAL_HEADER.SizeOfImage,header=cpbytes[:cp.OPTIONAL_HEADER.SizeOfHeaders].hex(),sections=[(s.VirtualAddress,s.Misc_VirtualSize,s.SizeOfRawData,s.Characteristics) for s in cp.sections])
    known=[(0xfe51,5)]
    if variant=='U30-40':known += [(int(r['rva'],16),len(bytes.fromhex(r['preimage']))) for r in json.loads((FOLDER.parent/'preparation-manifest.json').read_text())['windows']]
    for r in binding['ranges']:
        if r['module']=='ai':
            current=cp.get_data(r['rva'],r['length']);old=bytes.fromhex(r['expected_hex'])
            for i,(x,y) in enumerate(zip(current,old)):
                if x!=y and not any(start<=r['rva']+i<start+size for start,size in known):raise ValueError('Unexpected changed decoder byte')
            r['expected_hex']=current.hex()
    for rva in (0x74b60,0xc2180,0x128f20,0xc2ee3,0xb8660,0xb8a3d):
        raw=ep.get_data(rva,32);binding['ranges'].append(dict(module='engine',rva=rva,length=32,expected_hex=raw.hex(),kind='scalar-route-window'))
    for rva,length in [(0x543b0,0x41),(0x660f0,0xd4),(0x131a50,0x21),(0x131770,0xf),(0x131dc0,0x1c),(0x131de0,0x1c),(0x132020,0x1c),(0x132040,0x1c)]:
        raw=ep.get_data(rva,length);binding['ranges'].append(dict(module='engine',rva=rva,length=length,expected_hex=raw.hex(),kind='loaded type-read binding'))
    for rva,length in [(0x11bc0,0x20),(0x1a970,0x10),(0x1a980,0x20),(0x1cd50,0x20),(0x655f0,0x2d0)]:
        raw=cp.get_data(rva,length);binding['ranges'].append(dict(module='ai',rva=rva,length=length,expected_hex=raw.hex(),kind='native getter/Actual binding'))
    payload=cp.get_data(0xd4000,4348)
    if hashlib.sha256(payload).hexdigest()!=manifest['b2_preserved']['payload_sha256']:raise ValueError('N30 payload differs')
    binding['ranges'].append(dict(module='ai',rva=0xd4000,length=4348,expected_hex=payload.hex(),kind='PIC-payload'))
    for rva in (0x413da,0x3625b,0xfe2d,0xfe51,0x61f0):binding['sites'].append(dict(rva=rva,expected_hex=cp.get_data(rva,5).hex()))
    if variant=='U30-40':
        for row in json.loads((FOLDER.parent/'preparation-manifest.json').read_text())['windows']:
            rva=int(row['rva'],16);raw=cp.get_data(rva,len(bytes.fromhex(row['preimage'])))
            if row['name']=='execute_slot':binding['ranges'].append(dict(module='ai',rva=rva,length=4,expected_hex=raw.hex(),kind='vtable'))
            else:binding['sites'].append(dict(rva=rva,expected_hex=raw.hex()))
        section=cp.sections[-2]
        raw=cp.get_data(section.VirtualAddress,section.Misc_VirtualSize)
        binding['ranges'].append(dict(module='ai',rva=section.VirtualAddress,length=len(raw),expected_hex=raw.hex(),kind='PIC-payload'))
        binding['shared_plan_rva']=int(manifest['components']['state_rva'],16)
    binding['manifest_sha256']=MANIFEST_HASH;binding['package_sha256']=None
    return binding

def verify_loaded(*args):
    result=original_verify(*args)
    result.update(all_five_B2_hooks=True,N30_payload_bound=True,new_payload_and_all_nine_windows_bound=args[1]['variant']=='U30-40')
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



def native_expansion_state(read,eb,ab,participants,binding):
    read=bounded(read)
    u32=lambda p:struct.unpack('<I',read(checked(p),4))[0]
    i32=lambda p:struct.unpack('<i',read(checked(p),4))[0]
    def name(pointer):
        data=bytearray()
        for i in range(128):
            raw=read(checked(pointer,i),1)
            if raw==b'\0':return data.decode('ascii')
            data.extend(raw)
        raise ValueError('Unterminated bounded type token')
    players=u32(eb+0x67dd80);manager=u32(eb+0x67ddb8)
    initialized={civ:i32(u32(players+4*civ)+0x11ac)>=0 for civ in participants['civ_ids']}
    def uninitialized():return dict(loaded_settler_type='UNKNOWN_NOT_INITIALIZED',native_desired='UNKNOWN_NOT_INITIALIZED',native_actual='UNKNOWN_NOT_INITIALIZED',native_supplemental_deficit='UNKNOWN_NOT_INITIALIZED',current_front_cache='UNKNOWN_NOT_INITIALIZED',current_settler_armies='UNKNOWN_NOT_INITIALIZED',Gcert='UNKNOWN_PER_CIV_SHARED_BUFFER_OVERWRITTEN',Dorig='UNKNOWN_PER_CIV_SHARED_BUFFER_OVERWRITTEN',R='UNKNOWN_PER_CIV_SHARED_BUFFER_OVERWRITTEN',complete_queue_and_free_mission_status='UNKNOWN_NOT_DECODED')
    def shared_state():
        if binding['variant']!='U30-40':return None
        ptr=ab+binding['shared_plan_rva'];fields=dict(status=0,reason=4,owner=8,civ=12,generation=32,scope=36,remaining=56,desired=60,path_queries=84,Dorig=184,Gcert=188,policy=192,government=196,engine_count=200,path_points=204,cutoff=208,context=212,classified=220)
        shared={key:i32(ptr+off) for key,off in fields.items()}
        shared.update(only_last_pass_buffer=True,all_seven_telemetry_available=False,certificate_not_attributed_to_other_civs=True)
        return shared
    # Fixed T0 previously observed processed_round=-1. Native cache extras
    # are optional before any native AIpass; strict loaded/identity/tech/round
    # checks still run. After round>=0 nonzero malformed data reject normally.
    if not any(initialized.values()):return {civ:uninitialized() for civ in participants['civ_ids']},shared_state()
    db=u32(eb+0x67dd18);strings=u32(eb+0x67dcfc);count=i32(db)
    if not 2<=count<=4097:raise ValueError('Loaded UnitDB count invalid')
    records=u32(db+8);table=u32(strings+4);type_info=[]
    for index in range(count-1):
        sid=u32(records+0x2c8*index+4)
        if sid>100000:raise ValueError('Unit name SID out of bounded range')
        entry=u32(table+4*sid);mask=u32(records+0x2c8*index+0x34)
        type_info.append(dict(type_index=index,string_id=sid,display_name=name(u32(entry+8)),native_settler_category=bool(mask&15),native_water_or_space_bits=mask&10))
    # Display names are NOT exact identifier-token lookups. An actual new
    # pass context1 is written only after the loaded native UNIT_SETTLER
    # resolver/preview/original-demand checks. Its type is a global DB index;
    # only that identity can be shared, never per-civ Gcert/Dorig/R.
    t=None;shared=shared_state()
    if shared is not None and shared['context']==1:
        candidate_type=i32(ab+binding['shared_plan_rva']+44);pass_types=i32(ab+binding['shared_plan_rva']+48)
        if pass_types!=count-1 or not 0<=candidate_type<count-1:raise ValueError('Frozen global type/count mismatch')
        info=type_info[candidate_type]
        if not info['native_settler_category'] or info['native_water_or_space_bits']:raise ValueError('Certified ordinary type category mismatch')
        t=candidate_type
    def nodes(container,kind):
        todo=[u32(container+8)];seen=set();ids=set();rows=[]
        while todo:
            ptr=todo.pop()
            if not ptr:continue
            if ptr in seen or len(seen)>=4096:raise ValueError('Bounded own-set traversal malformed')
            seen.add(ptr);ident=u32(ptr);actor=u32(ptr+12)
            if ident in ids or u32(actor+12)!=ident or i32(actor+4)!=kind:raise ValueError('Current BSet identity mismatch')
            ids.add(ident);rows.append((ident,actor));todo.extend([u32(ptr+4),u32(ptr+8)])
        if len(rows)!=i32(container):raise ValueError('Current own-set count mismatch')
        return rows
    players=u32(eb+0x67dd80);manager=u32(eb+0x67ddb8);result={}
    for civ in participants['civ_ids']:
        if not initialized[civ]:result[civ]=uninitialized();continue
        robot=u32(manager+0x220c+4*civ);actor=u32(robot+8);aip=u32(actor+0x94)+0x20;player=u32(players+4*civ)
        desired=u32(u32(aip+0x7c0));actual=u32(u32(aip+0x7c8));stock=[]
        for info in type_info:
            index=info['type_index'];d=struct.unpack('<d',read(desired+8*index,8))[0];a=i32(actual+4*index)
            if not math.isfinite(d) or d<0 or d!=int(d) or a<0:raise ValueError('Native desired/Actual not a valid stock')
            stock.append(dict(info,native_desired=d,native_actual=a,native_supplemental_deficit=max(0,int(d)-a)))
        selected=stock[t] if t is not None else dict(native_desired='UNKNOWN_EXACT_TOKEN_TYPE',native_actual='UNKNOWN_EXACT_TOKEN_TYPE',native_supplemental_deficit='UNKNOWN_EXACT_TOKEN_TYPE')
        cities=[]
        for ident,city in nodes(u32(actor+0x8c),2):cities.append(dict(city_id=ident,front_type=i32(city+0x1f0),front_category=i32(city+0x1f4),front_is_settler=(i32(city+0x1f0)==t and i32(city+0x1f4)==1) if t is not None else 'UNKNOWN_EXACT_TOKEN_TYPE'))
        armies=[]
        for ident,army in nodes(u32(actor+0x90),1):
            amount=struct.unpack('<h',read(army+0x48,2))[0]
            if not 0<=amount<=4096:raise ValueError('Bounded cached army count invalid')
            types=list(struct.unpack('<'+'h'*amount,read(army+0x4a,amount*2))) if amount else []
            if any(x<0 or x>=count-1 for x in types):raise ValueError('Cached unit index outside loaded interface')
            if t in types or t is None and any(type_info[index]['native_settler_category'] for index in types):
                position=u32(army+0x64)
                armies.append(dict(army_id=ident,agent_state=i32(army+0x40),unit_count=amount,type_indexes=types,settler_count=types.count(t) if t is not None else 'UNKNOWN_EXACT_TOKEN_TYPE',native_Actual_state_excluded=i32(army+0x40) in (17,18),cache_position_hex=read(position,8).hex() if position else 'UNKNOWN_NATIVE_CACHE_POSITION'))
        result[civ]=dict(selected,loaded_settler_type=t if t is not None else 'UNKNOWN_EXACT_TOKEN_TYPE',type_identity_source='native_newpass_global_resolver_context' if t is not None else 'display_name_not_token_lookup',native_stock_by_type=stock,engine_city_count=i32(u32(player+0x12c0)+8),current_front_cache=cities,current_settler_armies=armies,Gcert='UNKNOWN_PER_CIV_SHARED_BUFFER_OVERWRITTEN',Dorig='UNKNOWN_PER_CIV_SHARED_BUFFER_OVERWRITTEN',R='UNKNOWN_PER_CIV_SHARED_BUFFER_OVERWRITTEN',complete_queue_and_free_mission_status='UNKNOWN_NOT_DECODED')
    return result,shared_state()

class ModuleInfo(C.Structure):
    _fields_ = [('base', C.c_void_p), ('size', W.DWORD), ('entry', C.c_void_p)]

def main():
    parser=argparse.ArgumentParser(description='Read-only fixed-T0 goal3 snapshots; no game starts/writes/callbacks')
    parser.add_argument('--pid',type=int,required=True)
    parser.add_argument('--variant',choices=('release-v1','U30-40'),required=True)
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
    gate=json.loads((FOLDER/'C10-ROOT-VRIJGAVE.json').read_text('utf-8-sig'))
    if not gate.get('allowed') or gate.get('candidate_sha256')!=NEW_HASH:raise ValueError('C10 source-only; no live reader release')
    if args.turn not in (0,1) or args.variant=='release-v1' and not gate.get('baseline_allowed'):raise ValueError('First C10 scope is variant T0/T1 only')
    for pin in gate.get('sources',[]):
        if hashlib.sha256((FOLDER/pin['path']).read_bytes()).hexdigest()!=pin['sha256']:raise ValueError('Released C10 source changed')
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
        per_civ,shared=native_expansion_state(read,eb,ab,participants,binding)
        for row in state['civilizations']:row.update(per_civ[row['civ_id']])
        state['shared_last_pass']=shared
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
