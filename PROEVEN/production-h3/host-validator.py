"""Prepared production-only x86 HostBinding validator, not an H3 adapter.

stdcall(AiMain*, World*, HostBinding*) / ret0ch. Binding is24 bytes:
enginebase,grid,terrainDB,realPlayer,WGF,convert-function. There is no fixture
fallback in these bytes. No candidate is emitted until the food model exists.
"""
import json,struct,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'PROEVEN/score-h1'))
from build import Recipe
sys.path.insert(0,str(ROOT/'PROEVEN/hulpmiddelen/python'))
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
inputs=json.loads((OUT/'build-inputs.json').read_text())
r=Recipe()
def emit(asm,h):r.emit(asm,h)
def no():r.branch('jne unknown','0f85','unknown')
def null():r.branch('jz unknown','0f84','unknown')
for asm,h in [('push ebp','55'),('mov ebp,esp','8bec'),('push ebx','53'),('push esi','56'),('push edi','57'),
 ('mov edi,[ebp+10h]','8b7d10'),('xor eax,eax','33c0'),('mov ecx,6','b906000000'),('cld','fc'),('rep stosd','f3ab'),
 ('mov edi,[ebp+10h]','8b7d10'),('mov ebx,[ebp+0ch]','8b5d0c'),('test ebx,ebx','85db')]:emit(asm,h)
null();emit('mov edx,[ebp+8]','8b5508');emit('test edx,edx','85d2');null()
emit('cmp [edx+30h],ebx','395a30');no();emit('mov ecx,[ebx]','8b0b');emit('test ecx,ecx','85c9');null()
emit('mov esi,[ecx+b8h]','8bb1b8000000');emit('sub esi,134340h','81ee40431300');emit('cmp esi,400000h','81fe00004000');no()
emit('lea eax,[esi+1342e0h]','8d86e0421300');emit('cmp [ecx+a8h],eax','3981a8000000');no()
emit('cmp word [esi],MZ','66813e4d5a');no();emit('mov eax,[esi+3ch]','8b463c')
emit('cmp eax,40h','83f840');r.branch('jb unknown','0f82','unknown')
emit('cmp eax,400h','3d00040000');r.branch('ja unknown','0f87','unknown');emit('add eax,esi','03c6')
for asm,h in [('cmp [eax],PE','813850450000'),('cmp word [eax+4],14ch','668178044c01'),('cmp [eax+8],37d6f702h','81780802f7d637'),('cmp word [eax+18h],10bh','668178180b01'),('cmp [eax+34h],400000h','81783400004000')]:emit(asm,h);no()
emit('test word [eax+5eh],40h','66f7405e4000');r.branch('jnz unknown','0f85','unknown')
emit('cmp [eax+a0h],0','83b8a000000000');no();emit('cmp [eax+a4h],0','83b8a400000000');no()
for name,wrapper in inputs['strict_host']['wrappers'].items():
    raw=bytes.fromhex(wrapper['bytes']);base=int(wrapper['rva'],16)
    for offset in range(0,len(raw)//4*4,4):
        emit(f'cmp dword [esi+{base+offset:x}],original {name}','81be'+struct.pack('<I',base+offset).hex()+raw[offset:offset+4].hex());no()
    for offset in range(len(raw)//4*4,len(raw)):
        emit(f'cmp byte [esi+{base+offset:x}],original {name}','80be'+struct.pack('<I',base+offset).hex()+raw[offset:offset+1].hex());no()
for asm,h in [('mov [edi],esi','8937'),('mov eax,[esi+67dd70h]','8b8670dd6700'),('test eax,eax','85c0')]:emit(asm,h)
null();emit('mov [edi+4],eax','894704');emit('mov eax,[esi+67dd3ch]','8b863cdd6700');emit('test eax,eax','85c0');null();emit('mov [edi+8],eax','894708')
emit('mov eax,[edx+2ch]','8b422c');emit('test eax,eax','85c0');null();emit('mov eax,[eax+8]','8b4008');emit('test eax,eax','85c0');null();emit('mov [edi+0ch],eax','89470c')
emit('mov eax,[eax+1318h]','8b8018130000');emit('test eax,eax','85c0');null();emit('mov [edi+10h],eax','894710')
emit('lea eax,[esi+103f00h]','8d86003f1000');emit('mov [edi+14h],eax','894714');emit('mov eax,1','b801000000');r.branch('jmp done','e9','done')
r.label('unknown')
for asm,h in [('mov edi,[ebp+10h]','8b7d10'),('xor eax,eax','33c0'),('mov ecx,6','b906000000'),('cld','fc'),('rep stosd','f3ab')]:emit(asm,h)
r.label('done')
for asm,h in [('pop edi','5f'),('pop esi','5e'),('pop ebx','5b'),('pop ebp','5d'),('ret0ch','c20c00')]:emit(asm,h)
code=r.finish();rows=list(Cs(CS_ARCH_X86,CS_MODE_32).disasm(code,0));assert sum(i.size for i in rows)==len(code)
assert rows[-1].mnemonic=='ret' and rows[-1].op_str=='0xc'
# This component has no absolute memory operands: all production engine reads
# use the base obtained from the two exact World slots. Original wrapperbytes
# contain address-valued fingerprint data, not executed absolute operands.
(OUT/'host/validator.prepared.bin').write_bytes(code)
(OUT/'host/validator.prepared.recipe.json').write_text(json.dumps({'status':'PREPARED UNINTEGRATED; not native-tested','binding_size':24,'labels':r.labels,'recipe':r.rows},indent=2)+'\n')
(OUT/'host/validator.prepared.disassembly.txt').write_text('\n'.join(f'{i.address:04x} {i.bytes.hex():24} {i.mnemonic} {i.op_str}' for i in rows)+'\n')
print(json.dumps({'prepared_component':'production-only HostBinding validator','bytes':len(code),'instructions':len(rows),'candidate_built':False,'native_tested':False}))
