"""Own runtime binding; disk bytes only until separately authorized reader main."""
from pathlib import Path
import json,hashlib
from original_core import trusted_binding as original_binding
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
FOLDER=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500/reader'
RUNTIME_PINS=json.loads((HERE/'runtime-pins.json').read_text('utf-8'))
NEW_HASH=RUNTIME_PINS['candidate_sha256'];MANIFEST_HASH=RUNTIME_PINS['manifest_sha256']

def trusted_binding(variant):
    pins=json.loads((HERE/'SOURCE-PINS.json').read_text('utf-8'))
    for pin in pins['sources']:
        if hashlib.sha256((ROOT/pin['path']).read_bytes()).hexdigest()!=pin['sha256']:raise ValueError('Pinned diagnostic/provenance source changed: '+pin['path'])
    if not NEW_HASH or not MANIFEST_HASH or RUNTIME_PINS['state_rva'] is None:raise ValueError('Source-only reader has no reviewed candidate pins')
    binding=original_binding('original')
    if variant!='local4':raise ValueError('Only own local4 arm')
    import pefile
    mp=ROOT/RUNTIME_PINS['manifest_path']
    if hashlib.sha256(mp.read_bytes()).hexdigest()!=MANIFEST_HASH:raise ValueError('C1 manifest changed')
    manifest=json.loads(mp.read_text('utf-8'))
    cpbytes=(ROOT/RUNTIME_PINS['candidate_path']).read_bytes()
    expected=NEW_HASH
    if hashlib.sha256(cpbytes).hexdigest()!=expected:raise ValueError('Exact staged AI changed')
    cp=pefile.PE(data=cpbytes);ep=pefile.PE(data=(ROOT/'CTP-og/ctp_program/ctp/civctp.exe').read_bytes())
    binding['variant']=variant
    binding['ai'].update(sha256=expected,size=cp.OPTIONAL_HEADER.SizeOfImage,header=cpbytes[:cp.OPTIONAL_HEADER.SizeOfHeaders].hex(),sections=[(s.VirtualAddress,s.Misc_VirtualSize,s.SizeOfRawData,s.Characteristics) for s in cp.sections])
    known=[(0xfe51,5)]
    windows=[]
    for row in manifest['allowed_changes']:
        if row['reason'].startswith('named new hook '):
            rva=cp.get_rva_from_offset(row['offset']);raw=bytes.fromhex(row['after'])
            if len(raw)!=row['length'] or cp.get_data(rva,len(raw))!=raw:raise ValueError('Own manifest sitebytes mismatch')
            windows.append(dict(name=row['reason'].split()[-1],rva=rva,raw=raw))
    if len(windows)!=9:raise ValueError('Exact own nine site windows required')
    known += [(r['rva'],len(r['raw'])) for r in windows]
    for r in binding['ranges']:
        if r['module']=='ai':
            current=cp.get_data(r['rva'],r['length']);old=bytes.fromhex(r['expected_hex'])
            for i,(x,y) in enumerate(zip(current,old)):
                if x!=y and not any(start<=r['rva']+i<start+size for start,size in known):raise ValueError('Unexpected changed decoder byte')
            r['expected_hex']=current.hex()
    for rva in (0x74b60,0xc2180,0x128f20,0xc2ee3,0xb8660,0xb8a3d):
        raw=ep.get_data(rva,32);binding['ranges'].append(dict(module='engine',rva=rva,length=32,expected_hex=raw.hex(),kind='scalar-route-window'))
    for rva,length in [(0x345308,4),(0x133580,0x25),(0xbbd50,0x1c),(0xebdf0,0x73),(0x131940,0x1e),(0x3450b4,4),(0x542e0,0x30),(0x543b0,0x41),(0x660f0,0xd4),(0x131a50,0x21),(0x131770,0xf),(0x131dc0,0x1c),(0x131de0,0x1c),(0x132020,0x1c),(0x132040,0x1c)]:
        raw=ep.get_data(rva,length);binding['ranges'].append(dict(module='engine',rva=rva,length=length,expected_hex=raw.hex(),kind='loaded type-read binding'))
    for row in json.loads((FOLDER.parent/'science-spatial-pins.json').read_text('utf-8')):
        raw=ep.get_data(row['rva'],row['length'])
        if raw.hex()!=row['bytes']:raise ValueError('Frozen SCI spatial pin mismatch')
        binding['ranges'].append(dict(module='engine',rva=row['rva'],length=row['length'],expected_hex=raw.hex(),kind='SCI spatial/Improvement body'))
    for rva,length in [(0x11bc0,0x20),(0x1a970,0x10),(0x1a980,0x20),(0x1cd50,0x20),(0x655f0,0x2d0)]:
        raw=cp.get_data(rva,length);binding['ranges'].append(dict(module='ai',rva=rva,length=length,expected_hex=raw.hex(),kind='native getter/Actual binding'))
    payload=cp.get_data(0xd4000,4348)
    if hashlib.sha256(payload).hexdigest()!=manifest['b2_preserved']['payload_sha256']:raise ValueError('N30 payload differs')
    binding['ranges'].append(dict(module='ai',rva=0xd4000,length=4348,expected_hex=payload.hex(),kind='PIC-payload'))
    for rva in (0x413da,0x3625b,0xfe2d,0xfe51,0x61f0):binding['sites'].append(dict(rva=rva,expected_hex=cp.get_data(rva,5).hex()))
    if variant=='local4':
        for row in windows:
            rva=row['rva'];raw=row['raw']
            if row['name']=='execute_slot':binding['ranges'].append(dict(module='ai',rva=rva,length=4,expected_hex=raw.hex(),kind='vtable'))
            else:binding['sites'].append(dict(rva=rva,expected_hex=raw.hex()))
        section=cp.sections[-2]
        raw=cp.get_data(section.VirtualAddress,section.Misc_VirtualSize)
        binding['ranges'].append(dict(module='ai',rva=section.VirtualAddress,length=len(raw),expected_hex=raw.hex(),kind='PIC-payload'))
        binding['shared_plan_rva']=int(manifest['components']['state_rva'],16)
        state_size=manifest['components']['state_size']
        if binding['shared_plan_rva']!=RUNTIME_PINS['state_rva'] or state_size!=RUNTIME_PINS['state_size'] or state_size!=0x79904:raise ValueError('Exact reason23 own-state layout changed')
        if not 0x40600+1152<=state_size or binding['shared_plan_rva']+state_size>binding['ai']['size']:raise ValueError('Own slot outside bound AI state/module')
        state_sections=[s for s in cp.sections if s.VirtualAddress==binding['shared_plan_rva'] and s.Misc_VirtualSize==state_size]
        if len(state_sections)!=1:raise ValueError('Exact own state section missing')
        binding['shared_plan_size']=state_size
        sections=[dict(name=s.Name.rstrip(b'\0').decode(),rva=s.VirtualAddress,virtual_size=s.Misc_VirtualSize,raw_offset=s.PointerToRawData,raw_size=s.SizeOfRawData,flags=s.Characteristics) for s in cp.sections]
        if sections!=manifest['sections']:raise ValueError('Own manifest sections mismatch')
        for name,call in manifest['path_diagnostic']['calls'].items():
            raw=cp.get_data(call['call_rva'],5)
            if raw[0]!=0xe8 or call['return_rva']!=call['call_rva']+5:raise ValueError('Own diagnostic actual call pair mismatch '+name)
        binding['path_manifest']=manifest
    binding['manifest_sha256']=MANIFEST_HASH;binding['package_sha256']=None
    return binding
