"""Finite H1 byte recipe; candidates only. No installation or gameplay."""
from pathlib import Path
import hashlib, json, struct, sys
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'PROEVEN/hulpmiddelen/python'))
import pefile
HASH = '3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'
DESIGN = '02ac9a121906022314a3204f69a4700d5854b5b680722a352c693d31f3802668'
sha = lambda b: hashlib.sha256(b).hexdigest()
align = lambda n,a: (n+a-1)//a*a
def save(name, data):
    p=OUT/name; p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists(): assert p.read_bytes()==data, f'refuse overwrite different artifact: {p}'
    else:
        temp=p.with_suffix(p.suffix+'.tmp'); temp.write_bytes(data); temp.replace(p)
def jwrite(name, data): save(name, (json.dumps(data,indent=2)+'\n').encode())

class Recipe:
    def __init__(self): self.code=bytearray(); self.labels={}; self.fix=[]; self.rows=[]
    def emit(self, text, hexbytes):
        b=bytes.fromhex(hexbytes); self.rows.append({'offset':len(self.code),'asm':text,'bytes':b.hex()}); self.code.extend(b)
    def label(self,name):
        assert name not in self.labels; self.labels[name]=len(self.code)
    def branch(self,text,opcode,label):
        self.emit(text,opcode+'00000000'); self.fix.append((len(self.code)-4,label,False))
    def rva(self,text,opcode,label):
        self.emit(text,opcode+'00000000'); self.fix.append((len(self.code)-4,label,True))
    def finish(self):
        for at,label,absolute in self.fix:
            assert label in self.labels
            value=0xd4000+self.labels[label] if absolute else self.labels[label]-(at+4)
            struct.pack_into('<I' if absolute else '<i',self.code,at,value)
        for row in self.rows: row['bytes']=self.code[row['offset']:row['offset']+len(bytes.fromhex(row['bytes']))].hex()
        return bytes(self.code)

def payload(feature):
    r=Recipe()
    for asm,h in [('push ebp','55'),('mov ebp,esp','8bec'),('push ebx','53'),('push esi','56'),('push edi','57'),('sub esp,20h','83ec20'),('mov ebx,[ebp+8]','8b5d08')]:r.emit(asm,h)
    for src,local,packed in [(12,0xec,0xd8),(16,0xe8,0xda),(20,0xe4,0xdc)]:
        r.emit(f'movsx eax,word [ebp+{src:#x}]','0fbf45'+f'{src:02x}')
        r.emit(f'mov [ebp-{256-local:#x}],eax','8945'+f'{local:02x}')
        r.emit(f'mov [ebp-{256-packed:#x}],ax','668945'+f'{packed:02x}')
    for asm,h in [('push [ebp-1ch]','ff75e4'),('push [ebp-18h]','ff75e8'),('push [ebp-14h]','ff75ec'),('push ebx','53'),('mov ecx,[ebx]','8b0b'),('call [ecx+168h]','ff9168010000'),('movsx eax,ax','0fbfc0'),('mov [ebp-10h],eax','8945f0')]:r.emit(asm,h)
    if not feature:r.branch('jmp done','e9','done')
    else:
        r.emit('cmp eax,1','83f801');r.branch('jle done','0f8e','done')
        r.branch('call L','e8','L');r.label('L');r.emit('pop esi','5e');r.rva('sub esi,RVA(L)','81ee','L')
        r.emit('mov edi,[esi+c6fb4h]','8bbeb46f0c00');r.emit('test edi,edi','85ff');r.branch('jz done','0f84','done')
        r.emit('cmp [edi+30h],ebx','395f30');r.branch('jne done','0f85','done')
        r.emit('cmp dword [ebp-1ch],0','837de400');r.branch('jne done','0f85','done')
        r.emit('cmp word [esi+c6fb0h],0','6683beb06f0c0000');r.branch('jne done','0f85','done')
        for asm,h in [('mov [ebp-20h],-1','c745e0ffffffff'),('lea eax,[ebp-20h]','8d45e0'),('push eax','50'),('lea eax,[ebp-28h]','8d45d8'),('push eax','50'),('push ebx','53'),('mov ecx,[ebx]','8b0b'),('call [ecx+a8h]','ff91a8000000'),('test eax,eax','85c0')]:r.emit(asm,h)
        r.branch('jz done','0f84','done');r.emit('mov eax,[ebp-20h]','8b45e0')
        r.emit('cmp eax,8','83f808');r.branch('je mountain','0f84','mountain')
        r.emit('cmp eax,20','83f814');r.branch('je mountain','0f84','mountain')
        r.emit('cmp eax,22','83f816');r.branch('jne done','0f85','done')
        r.label('mountain');r.emit('dec [ebp-10h]','ff4df0')
    r.label('done')
    for asm,h in [('mov eax,[ebp-10h]','8b45f0'),('add esp,20h','83c420'),('pop edi','5f'),('pop esi','5e'),('pop ebx','5b'),('pop ebp','5d'),('ret10h','c21000')]:r.emit(asm,h)
    return r.finish(),r

def build(blob,feature):
    p=pefile.PE(data=blob); assert sha(blob)==HASH
    assert (p.FILE_HEADER.Machine,p.FILE_HEADER.NumberOfSections,p.FILE_HEADER.TimeDateStamp,p.OPTIONAL_HEADER.Magic,p.OPTIONAL_HEADER.ImageBase)==(0x14c,4,0x37b894e7,0x10b,0x20000000)
    assert (p.OPTIONAL_HEADER.FileAlignment,p.OPTIONAL_HEADER.SectionAlignment,p.OPTIONAL_HEADER.SizeOfHeaders)==(0x200,0x1000,0x400)
    assert p.sections[-1].get_file_offset()+40==0x250 and not any(blob[0x250:0x278])
    assert max(s.PointerToRawData+s.SizeOfRawData for s in p.sections)==len(blob)==0xa1400
    assert align(max(s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData) for s in p.sections),0x1000)==0xd4000
    assert not p.OPTIONAL_HEADER.DATA_DIRECTORY[4].VirtualAddress and not p.FILE_HEADER.Characteristics&1
    code,r=payload(feature); raw=align(len(code),0x200); data=bytearray(blob)
    changes=[]
    def change(at,b,why):
        before=bytes(data[at:at+len(b)]); data[at:at+len(b)]=b
        changes.append({'offset':hex(at),'before':before.hex(),'after':b.hex(),'reason':why})
    for site in (0x784bb,0x78517,0x7aa35):
        at=p.get_offset_from_rva(site);assert blob[at:at+6].hex()=='ff9168010000'
        change(at,b'\xe8'+struct.pack('<i',0xd4000-site-5)+b'\x90',f'call adapter RVA d4000 from {site:x}; NOP fallthrough')
    change(0x250,struct.pack('<8sIIIIIIHHI',b'.h1',len(code),0xd4000,raw,0xa1400,0,0,0,0,0x60000020),'new RX section')
    change(p.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),struct.pack('<H',5),'section count')
    change(p.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfImage'),struct.pack('<I',align(0xd4000+len(code),0x1000)),'image size')
    change(p.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfCode'),struct.pack('<I',p.OPTIONAL_HEADER.SizeOfCode+raw),'code size')
    data.extend(code+bytes(raw-len(code)))
    checksum=pefile.PE(data=data).generate_checksum()
    change(p.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum'),struct.pack('<I',checksum),'PE checksum')
    manifest={'variant':'H1-M' if feature else 'H1-I','original_sha256':HASH,'design_sha256':DESIGN,'candidate_sha256':sha(data),'payload_sha256':sha(code),'payload_size':len(code),'payload_rva':'0xd4000','payload_raw':'0xa1400','changes':changes,'labels':r.labels,'recipe':r.rows,'appended_bytes':raw,'checksum':hex(checksum),'scope':'candidate only; not installed; gameplay unmeasured'}
    return bytes(data),code,manifest

def inventory():
    # Full original/model/proof installations, including saves and users' edits.
    out={}
    for tree in ('CTP-og','CTP-AAIP','CTP-proef'):
        for p in sorted((ROOT/tree).rglob('*')):
            if p.is_file():out[p.relative_to(ROOT).as_posix()]={'size':p.stat().st_size,'sha256':sha(p.read_bytes())}
    t0=ROOT/'PROEVEN/settlerquota/vaste-start'
    for p in sorted(t0.rglob('*')):
        if p.is_file():out[p.relative_to(ROOT).as_posix()]={'size':p.stat().st_size,'sha256':sha(p.read_bytes())}
    return out

def helper_templates():
    # Helpers execute only in our own process; absolute pointers are patched
    # at allocation time, never inserted into either candidate DLL.
    r=Recipe(); fix=[]
    def ptr(asm,h,offset):
        r.emit(asm,h+'00000000');fix.append({'at':len(r.code)-4,'context_offset':offset})
    for asm,h in [('push ebp','55'),('push ebx','53'),('push esi','56'),('push edi','57')]:r.emit(asm,h)
    ptr('fxsave original','0fae05',0x100)
    r.emit('fninit','dbe3');r.emit('fld1','d9e8');r.emit('fldpi','d9eb')
    ptr('fxsave before','0fae05',0x300);ptr('mov [before],esp','8925',40)
    for asm,h in [('mov ebx,13579bdfh','bbdf9b5713'),('mov esi,2468ace0h','bee0ac6824'),('mov edi,76543210h','bf10325476'),('mov ebp,55aa33cch','bdcc33aa55')]:r.emit(asm,h)
    for offset,name in [(28,'z'),(24,'y'),(20,'x'),(16,'World')]:ptr('push '+name,'ff35',offset)
    ptr('call [target]','ff15',32)
    for offset,asm,h in [(36,'eax','a3'),(44,'esp','8925'),(48,'ebx','891d'),(52,'esi','8935'),(56,'edi','893d'),(60,'ebp','892d')]:ptr('store '+asm,h,offset)
    ptr('fxsave after','0fae05',0x500);ptr('fxrstor original','0fae0d',0x100)
    for asm,h in [('pop edi','5f'),('pop esi','5e'),('pop ebx','5b'),('pop ebp','5d'),('ret','c3')]:r.emit(asm,h)
    shim=r.finish();save('helper/shim.bin',shim);jwrite('helper/shim-fixups.json',fix)
    # Both callback ABIs are deliberately different (ret10h vs ret0ch).
    s=Recipe();s.emit('World -> context','8b4c24048b4904');s.emit('inc score calls','ff4140')
    for stack,local in [(4,72),(8,76),(12,80),(16,84)]:s.emit('capture score argument','8b4424'+f'{stack:02x}'+'8941'+f'{local:02x}')
    s.emit('mov eax,[ecx]','8b01');s.emit('ret10h','c21000');save('helper/score-callback.bin',s.finish())
    t=Recipe();t.emit('World -> context','8b4c24048b4904');t.emit('inc terrain calls','ff4144')
    t.emit('capture World','8b442404894158');t.emit('packed pointer','8b542408')
    t.emit('capture xy','8b0289415c');t.emit('capture z word','0fb74204894160')
    t.emit('output pointer','8b54240c');t.emit('capture initial sentinel','8b02894164')
    t.emit('cmp write,0','83790c00');t.branch('jz no_write','0f84','no_write')
    t.emit('write terrain','8b41048902');t.label('no_write');t.emit('status','8b4108');t.emit('ret0ch','c20c00')
    save('helper/terrain-callback.bin',t.finish())
    jwrite('helper/recipes.json',{'shim':r.rows,'score_callback':s.rows,'terrain_callback':t.rows})

if __name__=='__main__':
    assert sha((ROOT/'ONTWERP/SCORE-INVOEGROUTE-H1.md').read_bytes())==DESIGN
    before=inventory();jwrite('protected-before.json',before)
    source=ROOT/'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll';blob=source.read_bytes();assert sha(blob)==HASH
    save('backup/robotcom.original.dll',blob)
    for feature in (False,True):
        data,code,m=build(blob,feature);assert (data,code,m)==build(blob,feature)
        name=m['variant'];save(f'candidates/{name}/robotcom.dll',data);save(f'{name}.payload.bin',code);jwrite(f'{name}.manifest.json',m)
    helper_templates()
    after=inventory();assert before==after;jwrite('protected-after-build.json',after)
    print(json.dumps({'built':['H1-I','H1-M'],'protected_files':len(before),'source_unchanged':sha(source.read_bytes())==HASH,'deterministic_double_build':True}))
