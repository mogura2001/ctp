"""Minimal source-only attempt9 address/mapping delta; never starts helper."""
from pathlib import Path
import hashlib,json,difflib,datetime
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (P/'native-attempt9-preparation.json').exists()
frozen=[p for p in P.iterdir() if p.is_file() and p.name not in ('native-main.cs','native-fixtures.cs','prepare_attempt9.py')]
pins=[dict(path=p.name,sha256=sha(p),size=p.stat().st_size) for p in frozen]
for name in ['native-main.cs','native-fixtures.cs']:(P/(name+'.before-attempt9')).write_bytes((P/name).read_bytes())
s=(P/'native-main.cs').read_text('utf-8')
s=s.replace('   ScienceNative.ReserveEngineBlocks();','''   var process=System.Diagnostics.Process.GetCurrentProcess();var module=process.MainModule;
   Console.WriteLine("helper_mapping pid="+process.Id+" bitness="+(IntPtr.Size*8)+" path="+module.FileName+" base="+unchecked((uint)module.BaseAddress.ToInt32()).ToString("x8")+" size="+module.ModuleMemorySize.ToString("x"));Console.Out.Flush();
   ScienceNative.BindMainModule(module.BaseAddress,module.ModuleMemorySize);
   ScienceNative.ReserveEngineBlocks();''')
s=s.replace('   File.WriteAllText(output,serializer.Serialize(result));Console.WriteLine("PASS nativecalls "+result["native_calls"]);return 0;','   if(!ScienceNative.CleanupOk)throw new InvalidOperationException("owned cleanup failed; see stdout");\n   File.WriteAllText(output,serializer.Serialize(result));Console.WriteLine("PASS nativecalls "+result["native_calls"]);return 0;')
(P/'native-main.cs').write_text(s,'utf-8')
s=(P/'native-fixtures.cs').read_text('utf-8')
start=s.index(' public static void ReserveEngineBlocks(){');end=s.index(' static IntPtr A(',start)
s=s[:start]+''' [StructLayout(LayoutKind.Sequential)]
 struct MEMORY_BASIC_INFORMATION {
  public IntPtr BaseAddress,AllocationBase;public uint AllocationProtect;public UIntPtr RegionSize;public uint State,Protect,Type;
 }
 [DllImport("kernel32.dll",SetLastError=true)] static extern UIntPtr VirtualQuery(IntPtr address,out MEMORY_BASIC_INFORMATION info,UIntPtr length);
 static ulong mainBase,mainEnd;
 public static bool CleanupOk=true;
 static ulong Address(IntPtr p){return unchecked((uint)p.ToInt32());}
 static bool Overlaps(ulong a,ulong b,ulong c,ulong d){return a<d&&c<b;}
 public static void BindMainModule(IntPtr pointer,int size){
  Assert(IntPtr.Size==4&&size>0,"mainmodule x86 size");mainBase=Address(pointer);mainEnd=checked(mainBase+(ulong)size);Assert(mainEnd<=0x100000000UL,"mainmodule interval overflow");
 }
 static void QueryRange(IntPtr pointer,bool free){
  int mbiSize=Marshal.SizeOf(typeof(MEMORY_BASIC_INFORMATION));Assert(mbiSize==28,"x86 MEMORY_BASIC_INFORMATION size28");
  ulong start=Address(pointer),end=checked(start+0x10000UL),cursor=start;Assert(end<=0x100000000UL,"query interval overflow");
  while(cursor<end){
   MEMORY_BASIC_INFORMATION info;UIntPtr returned=VirtualQuery(new IntPtr(unchecked((int)(uint)cursor)),out info,(UIntPtr)mbiSize);int error=returned==UIntPtr.Zero?Marshal.GetLastWin32Error():0;
   Assert(returned.ToUInt64()==(ulong)mbiSize,"VirtualQuery bytes/error "+error);
   ulong rb=Address(info.BaseAddress),ab=Address(info.AllocationBase),length=info.RegionSize.ToUInt64(),next=checked(rb+length);
   Console.WriteLine("region phase="+(free?"before":"owned")+" interval="+start.ToString("x8")+" cursor="+cursor.ToString("x8")+" base="+rb.ToString("x8")+" allocation="+ab.ToString("x8")+" size="+length.ToString("x")+" state="+info.State.ToString("x")+" type="+info.Type.ToString("x")+" protect="+info.Protect.ToString("x")+" allocation_protect="+info.AllocationProtect.ToString("x"));Console.Out.Flush();
   Assert(length>0&&rb<=cursor&&next>cursor&&next<=0x100000000UL,"VirtualQuery nonprogress/overflow");
   if(free)Assert(info.State==0x10000,"fixture interval occupied "+start.ToString("x8")+" helper_overlap="+Overlaps(rb,next,mainBase,mainEnd)+" allocation_is_helper="+(ab==mainBase));
   else Assert(info.State==0x1000&&info.Type==0x20000&&ab==start&&info.Protect==4,"fixture interval not exact own committed private RW "+start.ToString("x8"));
   cursor=Math.Min(next,end);
  }
 }
 public static void ReserveEngineBlocks(){
  Assert(IntPtr.Size==4,"early x86 required");Assert(mainEnd>mainBase,"actual mainmodule bound");engine=new IntPtr(0x400000);
  try{
   foreach(int off in earlyBlocks){ulong start=0x400000UL+(ulong)off,end=start+0x10000UL;Assert(!Overlaps(start,end,mainBase,mainEnd),"actual helper mapping overlaps fixture block "+start.ToString("x8"));Assert(!Overlaps(start,end,0x20000000UL,0x20140000UL),"candidate reservation overlaps fixture block");QueryRange(A(engine,off),true);}
   foreach(int off in earlyBlocks){
    IntPtr wanted=A(engine,off),p=VirtualAlloc(wanted,(UIntPtr)0x10000,0x3000,4);int error=p==IntPtr.Zero?Marshal.GetLastWin32Error():0;
    if(p!=IntPtr.Zero)owned.Add(p);
    Console.WriteLine("allocation wanted="+Address(wanted).ToString("x8")+" returned="+Address(p).ToString("x8")+" error="+error+" registered="+(p!=IntPtr.Zero));Console.Out.Flush();
    Assert(p==wanted,"early synthetic fixed engine block "+Address(wanted).ToString("x8")+" error"+error);QueryRange(p,false);
   }
  }catch{ReleaseOwned();throw;}
 }
 public static void ReleaseOwned(){
  foreach(IntPtr p in owned){bool ok=VirtualFree(p,UIntPtr.Zero,0x8000);int error=ok?0:Marshal.GetLastWin32Error();if(!ok)CleanupOk=false;Console.WriteLine("cleanup own="+Address(p).ToString("x8")+" ok="+ok+" error="+error);}
  owned.Clear();Console.WriteLine("cleanup owned_complete="+CleanupOk);Console.Out.Flush();
 }
'''+s[end:]
old='  }finally{ReleaseOwned();if(module!=IntPtr.Zero)FreeLibrary(module);if(reserved!=IntPtr.Zero)VirtualFree(reserved,UIntPtr.Zero,0x8000);}'
new='''  }finally{ReleaseOwned();
   if(module!=IntPtr.Zero){bool ok=FreeLibrary(module);int error=ok?0:Marshal.GetLastWin32Error();if(!ok)CleanupOk=false;Console.WriteLine("cleanup own_module="+Address(module).ToString("x8")+" ok="+ok+" error="+error);}
   if(reserved!=IntPtr.Zero){bool ok=VirtualFree(reserved,UIntPtr.Zero,0x8000);int error=ok?0:Marshal.GetLastWin32Error();if(!ok)CleanupOk=false;Console.WriteLine("cleanup own_reservation="+Address(reserved).ToString("x8")+" ok="+ok+" error="+error);}Console.Out.Flush();
  }'''
assert old in s;s=s.replace(old,new)
(P/'native-fixtures.cs').write_text(s,'utf-8')
for name in ['native-main.cs','native-fixtures.cs']:
 (P/(name+'.attempt9.diff.txt')).write_text(''.join(difflib.unified_diff((P/(name+'.before-attempt9')).read_text().splitlines(True),(P/name).read_text().splitlines(True),fromfile=name+'.before-attempt9',tofile=name)),'utf-8')
assert all(sha(P/r['path'])==r['sha256'] for r in pins)
(P/'native-attempt9-preparation.json').write_text(json.dumps(dict(stage='SOURCE_PREPARED_NO_HELPERSTART',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),frozen_pins=pins,sources=[dict(path=n,sha256=sha(P/n)) for n in ['native-main.cs','native-fixtures.cs']]),indent=2)+'\n')
print('Two helper sources changed; all other preexisting files frozen and equal.')
