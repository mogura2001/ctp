"""Reuse existing own-memory C# fixture and x86 inputs; only new branches."""
from pathlib import Path
import sys,json,hashlib
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;PACK=OUT.parent;ROOT=PACK.parents[2]
sys.path.insert(0,str(ROOT/'PROEVEN/production-h3'))
from x86 import X86,mem as m
OUT.mkdir(exist_ok=True)
(OUT/'helper').mkdir(exist_ok=True)
for path in (ROOT/'PROEVEN/settler-b4/helper').iterdir():
 if path.suffix in ('.bin','.json'):(OUT/'helper'/path.name).write_bytes(path.read_bytes())

def save(name,r,fix):
 (OUT/'helper'/(name+'.bin')).write_bytes(r.finish())
 (OUT/'helper'/(name+'.recipe.json')).write_text(json.dumps(dict(recipe=r.rows,fixups=fix,labels=r.labels),indent=2)+'\n','utf-8')
def begin():
 r=X86();r.prologue(0);r.emit('owned input state','bb00000000');return r,[dict(at=len(r.code)-4,context_offset=0)]
r,f=begin();r.unary('inc',m('ebx',600));r.mov('eax',7);r.epilogue(0,8);save('execute',r,f)
r,f=begin();r.unary('inc',m('ebx',604));r.mov('edi','ecx');r.mov(m('edi',0x1c),1);r.alu('cmp',m('ebp',20),0);r.j('jne','done');r.mov('edx',m('ebx',608));r.unary('inc',m('edx',8));r.label('done');r.mov('eax',55);r.epilogue(0,16);save('arrival',r,f)
# Fixture caller uses actual candidate normalizer with inherited artificial
# frame+[20h]. It supplies result/goal/AiMain/subtask; no mirrored normalizer.
r,f=begin();r.mov('esi',m('ebp',12));r.mov('edi',m('ebp',16));r.mov('eax',m('ebp',8));r.mov('edx',m('ebp',20));r.alu('sub','esp',64);r.alu('sub','ebp',64);r.mov(m('ebp',32),'edx');r.mov('edx',m('ebx',612));r.unary('call','edx');r.alu('add','ebp',64);r.alu('add','esp',64);r.epilogue(0,16);save('normalize_caller',r,f)
r,f=begin();r.mov('edi','ecx');r.push(0);r.push(m('ebx',628));r.push(0);r.push(0);r.push(m('ebx',624));r.push(0);r.push(m('ebx',620));r.mov('ecx','edi');r.unary('call',m('ebx',616));r.epilogue(0,0);save('goto_caller',r,f)
r,f=begin();r.mov('eax',1);r.epilogue(0,24);save('true24',r,f)

s=(ROOT/'PROEVEN/settler-b4/NativeProducer.cs').read_text('utf-8')
def remove_method(text,name):
 start=text.index(' static void '+name+'(');brace=text.index('{',start);depth=1;at=brace+1
 while depth:
  if text[at]=='{':depth+=1
  elif text[at]=='}':depth-=1
  at+=1
 return text[:start]+text[at:]
for name in ['RuntimeInputsGuard','TypesAndDepartures','PathsAndProducer','Wrappers']:s=remove_method(s,name)
s=s.replace('public static class B4Producer','public static class U40Producer')
s=s.replace('static int fixtureN;','static int fixtureN;\n'+(OUT/'ChangedCases.cs.fragment').read_text('utf-8'))
start=s.index('   int[] originalBodyStarts=')
end=s.index('\n  }finally{',start)
s=s[:start]+'''   int loadedExecute=R(mapped,0x8a598),copiedExecute=R(image,0x8a598);
   Test("actual mapped HIGHLOWslot execute bound",loadedExecute==A(mapped,labels["execute_gate"]).ToInt32());
   Test("own full mappedcopy relocated HIGHLOWslot execute bound",copiedExecute==Entry("execute_gate").ToInt32()&&image!=mapped);
   byte[] disk=File.ReadAllBytes(file);int b2size=File.ReadAllBytes(Path.Combine(root,"PROEVEN","opening-b2","B2a-N30-TECHNICAL.payload.bin")).Length;
   byte[] b2expected=File.ReadAllBytes(Path.Combine(root,"PROEVEN","opening-b2","B2a-N30-TECHNICAL.payload.bin"));
   Test("actual loader B2payload byteexact",Same(b2expected,Read(A(mapped,0xd4000),b2size))&&Same(b2expected,Read(A(image,0xd4000),b2size)));
   foreach(int rva in new int[]{0x413da,0x3625b,0xfe2d,0xfe51,0x61f0}){byte[] expected=new byte[5];Array.Copy(disk,rva-0xc00,expected,0,5);Test("actual loader B2hook exact "+rva.ToString("x"),Same(expected,Read(A(mapped,rva),5))&&Same(expected,Read(A(image,rva),5)));}
   Setup();ProducerInputs();PolicyInputs();RX(image,labels["pass_state"]);Dependency("bind_inputs","true4");
   byte[] ownBefore=Read(Entry("read_policy"),labels["settler_name"]-labels["read_policy"]+13);
   IntegratedChain();
   Test("all actual changed emitted functions byte-intact",Same(ownBefore,Read(Entry("read_policy"),ownBefore.Length)));
   return new Dictionary<string,object>{{"native_calls",cases},{"checks",passed.ToArray()},{"mapped_base",mapped.ToInt32()},{"own_copy_base",image.ToInt32()},{"mapped_execute_slot",loadedExecute},{"copy_execute_slot",copiedExecute},{"normal_LoadLibrary_and_fullcopy_HIGHLOW_rebase",true},{"fixture_only",true},{"controlled_callbacks_not_engine",true},{"old109cases_executed",false},{"actual_changed_source_byte_intact",true},{"gameplay_measured",false},{"pass",true}};'''+s[end:]
# own emitted bind_inputs is before read_policy; all other own functions remain
# byte-intact. Native unrelated mutations are substituted outside own source.
(OUT/'NativeU40.cs').write_text(s,'utf-8')
print(json.dumps(dict(prepared_only=True,own_helpers=len(list((OUT/'helper').glob('*.bin'))),old_case_methods_removed=4)))
