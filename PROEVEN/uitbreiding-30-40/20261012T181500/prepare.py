"""C1 read-only binding and release audit; writes only this owned directory."""
from pathlib import Path
import sys, json, hashlib, importlib.util, datetime
sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
SHA = lambda b: hashlib.sha256(b).hexdigest()
BASE = 'eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'
ENGINE = 'b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79'
PROPOSALS = {'ANALYSE/UITBREIDING-30-40.md':'9144dfa2d2946ac566ae17be1649bfab378d5fe2d5d3e5a46020c8ce054f8497',
             'ONTWERP/UITBREIDING-30-40.md':'accf076e715b2aeed674b989fecd52fd608afa8a0cb739c2270265ec398bf12a'}
WINDOWS = {'start_hook':(0x2b079,'e882550400'), 'capture_hook':(0x7abac,'e8cff4ffff'),
           'desired_hook':(0x66b81,'e81aeeffff'), 'scope_hook':(0x2b0d8,'e893ba0300'),
           'quota_hook':(0x65a4c,'e8affeffff'), 'execute_slot':(0x8a598,'c0430420'),
           'arrival_call':(0x44d11,'ff9290000000'), 'arrival_result':(0x44d17,'b801000000'),
           'normalize':(0x44b27,'f7d81bc0f7d883c002')}

def module(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def prepare():
    release=ROOT/'PROEVEN/doel3/20261012-release-v1'
    manifest=json.loads((release/'manifest.json').read_text('utf-8'))
    pins=[]
    for row in manifest['files']:
        data=(ROOT/row['path']).read_bytes()
        actual=SHA(data); assert actual==row['variant_sha256'], row['path']
        pins.append(dict(path=row['path'],sha256=actual,size=len(data)))
    assert len(pins)==19
    proposals=[]
    for path, expected in PROPOSALS.items():
        actual=SHA((ROOT/path).read_bytes());assert actual==expected,path
        proposals.append(dict(path=path,sha256=actual))
    dll_path=ROOT/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll'
    dll=dll_path.read_bytes();assert SHA(dll)==BASE
    engine_path=ROOT/'CTP-proef/ctp_program/ctp/civctp.exe'
    engine=engine_path.read_bytes();assert SHA(engine)==ENGINE
    pe=pefile.PE(data=dll);ep=pefile.PE(data=engine)
    assert pe.OPTIONAL_HEADER.ImageBase==0x20000000
    assert pe.FILE_HEADER.TimeDateStamp==0x37b894e7
    assert ep.OPTIONAL_HEADER.ImageBase==0x400000 and ep.FILE_HEADER.TimeDateStamp==0x37d6f702
    windows=[]
    for name,(rva,expected) in WINDOWS.items():
        actual=pe.get_data(rva,len(bytes.fromhex(expected))).hex()
        assert actual==expected,(name,actual)
        windows.append(dict(name=name,rva=hex(rva),offset=hex(pe.get_offset_from_rva(rva)),preimage=actual))
    relocations=[dict(rva=hex(e.rva),type=e.type) for block in pe.DIRECTORY_ENTRY_BASERELOC for e in block.entries if e.rva==0x8a598]
    assert relocations==[dict(rva='0x8a598',type=3)]
    b2=module('c1_original_b2',ROOT/'PROEVEN/opening-b2/build.py')
    b2code,b2recipe,_=b2.payload(30)
    assert pe.get_data(0xd4000,len(b2code))==b2code
    b2hooks=[]
    for name,site in b2.INPUT['sites'].items():
        rva=int(site['rva'],16);length=len(bytes.fromhex(site['preimage']))
        data=pe.get_data(rva,length)
        target=rva+5+int.from_bytes(data[1:5],'little',signed=True)
        assert target==0xd4000+b2recipe.labels['reload' if name=='reload_entry' else name]
        b2hooks.append(dict(name=name,rva=hex(rva),bytes=data.hex(),target_rva=hex(target)))
    assert len(b2hooks)==5
    (OUT/'release-v1.robotcom.backup.dll').write_bytes(dll)
    ranges=[(0x443c0,0x70),(0x44a00,0x170),(0x44ba0,0x210),(0x487e0,0x40),(0x73710,0x70)]
    dis=Cs(CS_ARCH_X86,CS_MODE_32)
    text=[]
    for rva,length in ranges:
        text.append(f'\nRVA {rva:x} length {length:x}')
        text.extend(f'{i.address:08x} {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}' for i in dis.disasm(pe.get_data(rva,length),0x20000000+rva))
    (OUT/'caller-bindings.txt').write_text('\n'.join(text)+'\n','utf-8')
    sources=[]
    for path in ['PROEVEN/settler-b4/native.py','PROEVEN/settler-b4/integration.py','PROEVEN/settler-b4/input-pins.py','PROEVEN/production-h3/build-current.py','PROEVEN/opening-b2/build.py','PROEVEN/production-h3/x86.py']:
        sources.append(dict(path=path,sha256=SHA((ROOT/path).read_bytes())))
    report=dict(stage='C1_PREPARED_BASE_AND_PREIMAGES_VERIFIED_NOT_INSTALLED_NOT_RUNTIME',
        checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),release_pins=pins,
        proposals=proposals,base_sha256=BASE,engine_sha256=ENGINE,engine_timestamp=hex(ep.FILE_HEADER.TimeDateStamp),
        base_image_size=hex(pe.OPTIONAL_HEADER.SizeOfImage),base_sections=[dict(name=s.Name.rstrip(b'\0').decode(),rva=hex(s.VirtualAddress),size=hex(s.Misc_VirtualSize),raw=hex(s.PointerToRawData),raw_size=hex(s.SizeOfRawData)) for s in pe.sections],
        windows=windows,execute_slot_relocation=relocations,b2_payload=dict(rva='0xd4000',size=len(b2code),sha256=SHA(b2code),record_length=36,record_version=1,N=30),b2_hooks=b2hooks,source_pins=sources,
        recovery='No installation. Own backup is exact tested release-v1. Any future installation/restore requires current 19 pins, closed game, protected saves/profile and separate root authorization.',
        binary_diff_policy='Only these 9 windows, PE header count/size/checksum, newly declared RX/RW section headers and appended section bytes. Preserve all five B2 hooks and complete payload byte-for-byte, existing relocation directory and all unrelated original bytes. The slot40 HIGHLOW remains at original RVA with new wrapper pointer. No H3 score hooks, packing or FLI changes.')
    (OUT/'preparation-manifest.json').write_text(json.dumps(report,indent=2)+'\n','utf-8')
    print(json.dumps(dict(stage=report['stage'],pins=len(pins),preimages=len(windows),b2_hooks=len(b2hooks),relocation=relocations,image_size=report['base_image_size'])))
    return report

if __name__=='__main__':prepare()
