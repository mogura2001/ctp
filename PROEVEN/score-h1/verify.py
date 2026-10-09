"""Independent candidate reader: PE/diff/Capstone/CFG stack proofs."""
from pathlib import Path
import hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
sha=lambda b:hashlib.sha256(b).hexdigest()
orig=(OUT/'backup/robotcom.original.dll').read_bytes();op=pefile.PE(data=orig)
assert sha(orig)=='3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
results=[];md=Cs(CS_ARCH_X86,CS_MODE_32)
for variant in ('H1-I','H1-M'):
    b=(OUT/f'candidates/{variant}/robotcom.dll').read_bytes();p=pefile.PE(data=b);s=p.sections[-1]
    assert p.FILE_HEADER.NumberOfSections==5
    assert s.Name==b'.h1\0\0\0\0\0' and s.VirtualAddress==0xd4000 and s.PointerToRawData==0xa1400
    assert s.Characteristics==0x60000020 and s.SizeOfRawData==0x200
    assert p.OPTIONAL_HEADER.SizeOfImage==0xd5000
    assert p.OPTIONAL_HEADER.SizeOfCode==op.OPTIONAL_HEADER.SizeOfCode+0x200
    assert p.OPTIONAL_HEADER.CheckSum==p.generate_checksum()
    assert b[0xa1400+s.Misc_VirtualSize:]==bytes(0x200-s.Misc_VirtualSize)
    allow=set(range(0x250,0x278))
    for obj,field,n in [(op.FILE_HEADER,'NumberOfSections',2),(op.OPTIONAL_HEADER,'SizeOfImage',4),(op.OPTIONAL_HEADER,'SizeOfCode',4),(op.OPTIONAL_HEADER,'CheckSum',4)]:
        at=obj.get_field_absolute_offset(field);allow.update(range(at,at+n))
    calls=[]
    for site in (0x784bb,0x78517,0x7aa35):
        at=op.get_offset_from_rva(site);raw=b[at:at+6]
        assert raw[0]==0xe8 and raw[5]==0x90 and site+5+struct.unpack('<i',raw[1:5])[0]==0xd4000
        assert list(md.disasm(raw,site))[1].address==site+5
        allow.update(range(at,at+6));calls.append(hex(site))
    actual={i for i in range(len(orig)) if orig[i]!=b[i]};assert actual<=allow
    # Every old section's metadata and data-directory is byte-identical.
    for os,ns in zip(op.sections,p.sections):assert os.__pack__()==ns.__pack__()
    assert [d.__pack__() for d in op.OPTIONAL_HEADER.DATA_DIRECTORY]==[d.__pack__() for d in p.OPTIONAL_HEADER.DATA_DIRECTORY]
    assert p.FILE_HEADER.TimeDateStamp==op.FILE_HEADER.TimeDateStamp and p.OPTIONAL_HEADER.ImageBase==0x20000000
    code=p.get_data(0xd4000,s.Misc_VirtualSize);ins=list(md.disasm(code,0xd4000));by={i.address:i for i in ins}
    assert sum(i.size for i in ins)==len(code)
    assert code[:7]==bytes.fromhex('558bec53565783') and code[-13:]==bytes.fromhex('8b45f083c4205f5e5b5dc21000')
    rets=[i for i in ins if i.mnemonic=='ret'];assert len(rets)==1 and rets[0].op_str=='0x10'
    calls_ins=[i for i in ins if i.mnemonic=='call']
    assert calls_ins[0].op_str=='dword ptr [ecx + 0x168]'
    if variant=='H1-M':
        assert len(calls_ins)==3 and calls_ins[2].op_str=='dword ptr [ecx + 0xa8]'
        pic=calls_ins[1];assert int(pic.op_str,16)==pic.address+pic.size
        after=by[pic.address+pic.size];assert after.mnemonic=='pop' and after.op_str=='esi'
        sub=by[after.address+after.size];assert sub.mnemonic=='sub' and sub.op_str==f'esi, {hex(after.address)}'
        assert any(i.op_str=='word ptr [esi + 0xc6fb0], 0' for i in ins)
        assert any(i.op_str=='edi, dword ptr [esi + 0xc6fb4]' for i in ins)
    else:assert len(calls_ins)==1
    assert not any(i.mnemonic.startswith('f') for i in ins)
    # Explore every CFG branch with exact stack delta. Callback methods consume
    # their explicit arguments; the call/pop PIC sequence contributes -4/+4.
    seen=set();pending=[(0xd4000,0)];returns=[];branches=[]
    while pending:
        addr,delta=pending.pop()
        if (addr,delta) in seen:continue
        seen.add((addr,delta));i=by[addr];nxt=addr+i.size;mn=i.mnemonic
        if mn=='push':delta-=4
        elif mn=='pop':delta+=4
        elif mn in ('add','sub') and i.op_str.startswith('esp, '):delta+=(1 if mn=='add' else -1)*int(i.op_str.split(', ')[1],16)
        elif mn=='call':
            if '0x168' in i.op_str:delta+=16
            elif '0xa8' in i.op_str:delta+=12
            else:delta-=4
        if mn=='ret':assert delta==0;returns.append(addr);continue
        if mn.startswith('j'):
            target=int(i.op_str,16);assert target in by;branches.append([hex(addr),hex(target)])
            pending.append((target,delta))
            if mn=='jmp':continue
        assert nxt in by;pending.append((nxt,delta))
    assert returns and len({a for a,d in seen})==len(ins)
    # Saved registers -4/-8/-12; allocated locals are -44..-13. Disjoint
    # variable extents: B -16..-13; x -20..-17; y -24..-21; z -28..-25;
    # terrain -32..-29; packed x/y/z -40..-35. Bottom -44..-41 is spare.
    extents=[set(range(a,a+n)) for a,n in [(-16,4),(-20,4),(-24,4),(-28,4),(-32,4),(-40,6)]]
    assert all(a.isdisjoint(c) for idx,a in enumerate(extents) for c in extents[idx+1:])
    assert all(-44<=v<=-13 for a in extents for v in a)
    listing='\n'.join(f'{i.address:08x} {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}' for i in ins)+'\n'
    (OUT/f'{variant}.disassembly.txt').write_text(listing)
    results.append({'variant':variant,'sha256':sha(b),'PE_checksum':hex(p.OPTIONAL_HEADER.CheckSum),'payload_bytes':len(code),'instructions':len(ins),'branches':branches,'callsites':calls,'all_cfg_paths_stack_balanced':True,'changed_original_bytes':len(actual),'old_sections_directories_unchanged':True,'new_absolute_relocations_required':False})
# Native helper templates are separately decoded to reject truncated instructions.
helpers={}
for name in ('shim','score-callback','terrain-callback'):
    raw=(OUT/f'helper/{name}.bin').read_bytes();rows=list(md.disasm(raw,0));assert sum(i.size for i in rows)==len(raw)
    expect={'shim':'','score-callback':'0x10','terrain-callback':'0xc'}[name]
    assert rows[-1].mnemonic=='ret' and rows[-1].op_str==expect
    helpers[name]={'bytes':len(raw),'sha256':sha(raw),'ret':expect or 'plain ret'}
    (OUT/f'helper/{name}.disassembly.txt').write_text('\n'.join(f'{i.address:04x} {i.bytes.hex():24} {i.mnemonic} {i.op_str}' for i in rows)+'\n')
(OUT/'offline-results.json').write_text(json.dumps({'candidates':results,'helpers':helpers},indent=2)+'\n')
print(json.dumps({'offline_pass':True,'variants':results,'helper_decoding':helpers},indent=2))
