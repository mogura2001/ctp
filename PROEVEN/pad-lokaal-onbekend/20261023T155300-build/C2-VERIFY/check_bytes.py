"""Saved-image Capstone/PE/recipe review only; no compose or native calls."""
from pathlib import Path
import datetime,difflib,hashlib,json,struct,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;PACK=OUT.parent;ROOT=PACK.parents[2]
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
sha=lambda b:hashlib.sha256(b).hexdigest()

def main():
    saved=(PACK/'candidate-manifest.json').read_bytes();m=json.loads(saved)
    parent=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500'
    old=json.loads((parent/'candidate-manifest.json').read_text('utf-8'))
    data=(PACK/'U30-40.prepared.dll').read_bytes();payload=(PACK/'U30-40.payload.bin').read_bytes()
    original=(parent/'release-v1.robotcom.backup.dll').read_bytes()
    p=pefile.PE(data=data);base=pefile.PE(data=original);pp=pefile.PE(str(parent/'U30-40.prepared.dll'))
    assert sha(data)==m['candidate_sha256']=='acfeec096ea39e1ff38435214769f4d24074e640b856e08d1c82cc09ea7a4984'
    assert sha(saved)=='0a10a7c7f1af1ecd0d71e549296a4e31ea850f100812515d519fa4055e497d4d'
    d=json.loads((OUT/'DETERMINISM.json').read_text('utf-8'))
    normalized=(PACK/'candidate-manifest.json').read_text('utf-8').encode()
    assert d['checks']['candidate'] and d['checks']['payload'] and d['manifest_sha256']==sha(normalized)
    representation=dict(original_checks=d['checks'],second_compose_LF_sha256=d['manifest_sha256'],saved_universal_newlines_sha256=sha(normalized),raw_saved_sha256=sha(saved),CRLF=saved.count(b'\r\n'),raw_LF=saved.count(b'\n'),tuple_example='historical compose execute_slot_HIGHLOW tuple becomes saved JSON list',second_compose_calls=1,third_compose=False,normalized_manifest_equal=True)
    (OUT/'MANIFEST-REPRESENTATION.json').write_text(json.dumps(representation,indent=2)+'\n','utf-8')
    labels=m['labels'];rows=m['recipe'];ext=int(m['components']['extension_rva'],16);rx=int(m['components']['internal_H3_rva'],16);rw=int(m['components']['state_rva'],16)
    def region(a,b):return [r for r in rows if labels[a]<=r['offset']<labels[b]]
    def asm(a,b):return [r['asm'] for r in region(a,b)]
    def rows_between(mm,begin,end):
        rr=mm['recipe'];aa=next(i for i,r in enumerate(rr) if r['offset']==mm['labels'][begin]);bb=next(i for i,r in enumerate(rr) if r['offset']==mm['labels'][end]);return rr[aa:bb]
    assert rw==0xef000 and rw%4096==0 and ext+labels['pass_state']==rw and ext+labels['generation']==rw+0x79800
    assert m['components']['state_size']==0x79904 and p.get_data(rw,0x79904)==bytes(0x79904)
    assert p.sections[-1].VirtualAddress==rw and p.sections[-1].Misc_VirtualSize==0x79904
    assert p.sections[-1].SizeOfRawData==(0x79904+511)//512*512
    assert p.OPTIONAL_HEADER.SizeOfImage==(rw+0x79904+4095)//4096*4096
    assert (p.sections[-2].Characteristics,p.sections[-1].Characteristics)==(0x60000020,0xc0000040)
    assert p.generate_checksum()==p.OPTIONAL_HEADER.CheckSum
    reloc=lambda pe:[(e.rva,e.type) for block in pe.DIRECTORY_ENTRY_BASERELOC for e in block.entries]
    assert reloc(p)==reloc(base)==reloc(pp) and reloc(p).count((0x8a598,3))==1
    assert data[len(original):len(original)+len(payload)]==payload
    assert not any(data[len(original)+len(payload):])
    assert p.get_data(0xd4000,rx-0xd4000)==pp.get_data(0xd4000,rx-0xd4000)
    assert p.get_data(rx,ext-rx)==pp.get_data(rx,ext-rx) and m['components']['internal_H3_sha256']==old['components']['internal_H3_sha256']
    # Every original byte difference must fall inside one disjoint named patch.
    mask=bytearray(len(original))
    for r in m['allowed_changes']:
        at=r['offset'];n=r['length'];assert not any(mask[at:at+n]);mask[at:at+n]=b'\1'*n
        assert original[at:at+n].hex()==r['before'] and data[at:at+n].hex()==r['after']
    changed=[i for i in range(len(original)) if original[i]!=data[i]]
    assert len(changed)==m['original_changed_byte_count']==82 and all(mask[i] for i in changed)
    actual=[];i=0
    while i<len(original):
        if original[i]==data[i]:i+=1;continue
        start=i
        while i<len(original) and original[i]!=data[i]:i+=1
        actual.append(dict(offset=start,length=i-start,before=original[start:i].hex(),after=data[start:i].hex()))
    actual.append(dict(offset=len(original),length=len(data)-len(original),before='',after=data[len(original):].hex(),kind='all appended bytes including exact zero fill'))
    assert actual==m['full_diff'] and m['unexplained_byte_count']==0
    cs=Cs(CS_ARCH_X86,CS_MODE_32);cs.detail=True;direct=0;decoded=0
    for r in rows:
        raw=bytes.fromhex(r['bytes']);at=ext+r['offset'];assert p.get_data(at,len(raw))==raw
        if not r['asm'].startswith(('constant','prepared')):
            ins=list(cs.disasm(raw,0x20000000+at));assert sum(x.size for x in ins)==len(raw),r;decoded+=len(ins)
        parts=r['asm'].split(' ',1)
        if len(parts)==2 and parts[1] in labels and (parts[0].startswith('j') or parts[0]=='call'):
            ins=list(cs.disasm(raw,0x20000000+at));assert len(ins)==1 and ins[0].operands[0].imm==0x20000000+ext+labels[parts[1]],r;direct+=1
    # Entire instruction stream outside the three intended functions is equal.
    def unchanged(manifest):
        ls=manifest['labels'];return [r for r in manifest['recipe'] if not (ls['direct_path']<=r['offset']<ls['capture_heap'] or ls['cached_path']<=r['offset']<ls['settler_name'])]
    a=unchanged(old);b=unchanged(m)
    assert [r['asm'] for r in a]==[r['asm'] for r in b],list(difflib.unified_diff([r['asm'] for r in a],[r['asm'] for r in b]))[:20]
    oldext=int(old['components']['extension_rva'],16);relocated=0
    for x,y in zip(a,b):
        if x['bytes']==y['bytes']:continue
        op=y['asm'].split(' ')[0]
        if op.startswith('j') or op=='call':relocated+=1;continue
        ar=bytes.fromhex(x['bytes']);br=bytes.fromhex(y['bytes']);assert ar[:-4]==br[:-4],(x,y)
        av=int.from_bytes(ar[-4:],'little');bv=int.from_bytes(br[-4:],'little')
        assert any(oldext+old['labels'][name]==av and ext+labels[name]==bv for name in old['labels'].keys()&labels.keys()),(x,y)
        relocated+=1
    # Real call edges and state/global address materialization, not historical RVAs.
    calls={}
    for pair,target in [('finalize_selection','select_direct_plans'),('selection_cached','cached_path'),('cached_direct','direct_path')]:
        c=m['path_diagnostic']['calls'][pair];raw=p.get_data(c['call_rva'],5)
        assert raw[0]==0xe8 and c['return_rva']==c['call_rva']+5 and c['call_rva']+5+struct.unpack('<i',raw[1:])[0]==ext+labels[target];calls[pair]=c
    for name,rva in m['effective_local4_labels_rva'].items():assert rva==ext+labels[name]
    materialized={}
    for name in ('pass_state','generation','pd_cache_return','pd_direct_return'):
        hits=[r for r in rows if r['asm'].startswith(('lea ','mov ','sub ')) and len(bytes.fromhex(r['bytes']))>=5 and int.from_bytes(bytes.fromhex(r['bytes'])[-4:],'little')==ext+labels[name]]
        assert hits,name;materialized[name]=len(hits)
    # All16 hard landings remain; edge4 has native-non0/1 plus3 dirty-zero guards.
    landings=[]
    for edge in range(1,17):
        entry=next(r for r in m['path_diagnostic']['branches'] if r['id']==edge)
        incoming=[r for r in rows if r['asm'].endswith(' pd_failure_'+str(edge))]
        assert len(incoming)==(4 if edge==4 else 1),(edge,len(incoming))
        assert entry['landing_rva']==ext+labels['pd_failure_'+str(edge)]
        assert 'historical_parent_edge_rva' in entry and 'parent_rva' not in entry
        landings.append(dict(id=edge,incoming=len(incoming),landing_rva=entry['landing_rva']))
    directbody=asm('direct_path','capture_heap')
    # The whole successful-native1 endpoint/safety loop is unchanged. Only
    # its already-verified branch/PIC addresses move with the inserted guards.
    def positive_body(mm,end):
        rr=rows_between(mm,'direct_path',end)
        first=next(i for i,r in enumerate(rr) if r['asm']=="mov esi,('ebp', -20)")
        return [r['asm'] for r in rr[first:]]
    assert positive_body(m,'path_local_candidate')==positive_body(old,'path_next')
    assert sum(x=='pairguard pushad' for x in directbody)==2 and sum(x=='pair inputs pushad' for x in directbody)==2
    local=asm('path_local_candidate','path_next')
    assert local[:6]==["cmp ('ebp', -16),0",'jne pd_failure_4',"cmp ('ebp', -24),0",'jne pd_failure_4',"cmp ('ebp', -20),0",'jne pd_failure_4']
    assert local[-2:]==["mov ('ebp', -36),4",'jmp path_free'] and not any(x.startswith("mov ('ebx',") for x in local)
    assert "cmp ('ebp', -36),0" in directbody and 'je path_local_candidate' in directbody
    for off,val in ((-40,0x3456ab89),(-44,0x4567bc90)):assert f"cmp ('ebp', {off}),{val}" in directbody
    assert "mov ecx,('edx', 7146388)" in directbody
    # Arguments and the enginefree route must remain identical instruction bytes.
    assert [r['bytes'] for r in rows_between(m,'path_free','path_done')]==[r['bytes'] for r in rows_between(old,'path_free','path_done')]
    free=asm('path_free','path_done');assert free.count("call eax")==1 and free.count("mov ('ebp', -20),0")==1
    def args(mm):
        rr=rows_between(mm,'direct_path','path_local_candidate') if 'path_local_candidate' in mm['labels'] else rows_between(mm,'direct_path','path_free')
        first=next(i for i,r in enumerate(rr) if r['asm']=='push 1' and rr[i+1]['asm']=='push 0' and rr[i+2]['asm']=='push 1')
        last=next(i for i in range(first,len(rr)) if rr[i]['asm']=="mov ('ebp', -36),eax")
        return rr[first:last+1]
    assert [r['bytes'] for r in args(m)]==[r['bytes'] for r in args(old)]
    assert sum(r['asm'].startswith('push ') for r in args(m))==20
    assert sum(r['asm']=="inc ('ebx', 84)" for r in region('direct_path','capture_heap'))==1
    dispatch=asm('source_post_done','source_choose')
    assert dispatch[:8]==['cmp eax,3','je select_ok','cmp eax,2','je source_next','cmp eax,4','je source_next','cmp eax,1','jne select_bad']
    cache=asm('cached_path','select_direct_plans')
    resultguard=['cmp eax,1','jb cached_unknown','cmp eax,4','ja cached_unknown']
    assert sum(cache[i:i+4]==resultguard for i in range(len(cache)))==2
    select=region('select_direct_plans','settler_name')
    assert any(r['asm']=='sub esp,320' for r in select[:7]),select[:8]
    for off in range(-240,-301,-4):
        assert any(r['asm']==f"mov ('ebp', {off}),eax" for r in select)
        assert any(r['asm']==f"mov eax,('ebp', {off})" for r in select)
    assert labels['select_add']<labels['selection_credit_pass_pc']<labels['selection_credit_done']
    assert all(r['offset']>=labels['selection_credit_done'] for r in region('select_add','select_next') if r['asm']=="mov ('edi', 24),eax")
    assert any(r['bytes']=='c20c00' for r in region('path_done','pd_failure_1'))
    assert any(r['bytes']=='c20c00' for r in region('cached_path','select_direct_plans'))
    assert any(r['bytes']=='c20400' for r in select)
    # Own guard families save all GPR and balance their scratch at both exits.
    assert sum(r['asm']=='pairguard pushad' for r in rows)==11
    assert sum(r['asm']=='pair inputs pushad' for r in rows)==7
    assert sum(r['asm']=='pairguard popad' for r in rows)==11 and sum(r['asm']=='pairguard failed popad' for r in rows)==11
    assert sum(r['asm']=='pair inputs popad' for r in rows)==7 and sum(r['asm']=='pair inputs failed popad' for r in rows)==7
    guardnames=['direct_pre_pass','direct_post_pass','cache_pre_pass','cache_post_pass','source_pre_pass','source_post_pass','selection_credit_pass','selection_pre','selection_sources','selection_best','selection_finish']
    for name in guardnames:
        body=asm(name+'_pc',name+'_done')
        for off,value in ((36,1),(40,0),(212,1),(268,0),(0,2),(4,0)):
            assert f"cmp ('ebx', {off}),{value}" in body,(name,off)
        for off in (0x78800,0x78804):assert f"cmp eax,('ebx', {off})" in body,(name,off)
        assert "cmp eax,('edx', 32)" in body and 'cmp eax,1' in body and 'cmp eax,31' in body
    # The same masks are emitted in logger landings/publication, not merely
    # declared in the manifest. No new record size or reached bits are used.
    for edge in range(1,17):
        end='pd_failure_'+str(edge+1) if edge<16 else 'capture_heap'
        body=asm('pd_failure_'+str(edge),end)
        assert body[-1]=='jmp path_unknown'
        expected=m['path_diagnostic']['branches'][edge-1]['required_reachedmask']&~(7<<17)
        assert f"cmp ('edi', {0x79804+16}),{expected}" in body
    assert m['path_diagnostic']['local4_returnmask']==sum(1<<i for i in (0,1,2,3,4,5,6,17,18,19))
    selectedasm=[r['asm'] for r in select]
    assert f"cmp ('edi', {0x79804+16}),{m['path_diagnostic']['local4_returnmask']&~(1<<19)}" in selectedasm
    for off in (204,208):assert f"cmp ('edi', {0x79804+off}),4" in selectedasm
    assert m['path_diagnostic']['local4_propagation']==[4,4,1] and m['path_diagnostic']['record_is_policy_input'] is False
    for role,filename in [('native','native.py'),('policy','policy.py'),('path_diagnostic','path_diagnostic.py'),('path_diagnostic_layout','path_diagnostic_layout.py')]:
        entry=m['effective_modules'][role];assert entry['path']==f'PROEVEN/pad-lokaal-onbekend/20261022T180000/{filename}' and sha((ROOT/entry['path']).read_bytes())==entry['sha256']
    report=dict(stage='C2B_STATIC_BYTES_COMPLETE_PENDING_ROOT_REVIEW',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate_sha256=sha(data),manifest_sha256=sha(saved),payload_sha256=sha(payload),determinism=representation,PE_checksum=True,RX_RW_and_zero_state=True,relocations_exact=True,all_original_byte_changes=82,unexplained_bytes=0,full_diff_exact=True,B2_H3_and_padding_exact=True,recipe_rows=len(rows),extension_instructions_decoded=decoded,direct_targets_checked=direct,unchanged_instruction_rows=len(a),unchanged_relocated_rows_explained=relocated,calls=calls,materialized_RVAs=materialized,landings=landings,twenty_args_and_cleanup_bytes_exact=True,strict_dispatch_and_bestsnapshot=True,guard_families=dict(pass_compare=11,pair_compare=7),state_rva=rw,state_size=0x79904,local4_returnmask=m['path_diagnostic']['local4_returnmask'],compose_calls_in_bytecheck=0,native=False,RPM=False,game=False,install=False,gameplay_proven=False,remaining=['independent root C2b review','separate native source/fixture gate and ABI/runtime verification'])
    (OUT/'BYTE-REVIEW.json').write_text(json.dumps(report,indent=2)+'\n','utf-8')
    print(json.dumps({k:report[k] for k in ('stage','recipe_rows','extension_instructions_decoded','direct_targets_checked','unchanged_instruction_rows','unexplained_bytes','native')}))

if __name__=='__main__':main()
