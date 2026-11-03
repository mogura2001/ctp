// SOURCE ONLY. Existing finite own-image/shim5 method; no engine/game/RPM.
// Exercises the real Trace logger in fabricated own callframes. Adapter-free
// counter is not proof that the production engine allocator/free was called.
using System;using System.IO;using System.Text.RegularExpressions;
using System.Collections.Generic;using System.Runtime.InteropServices;using System.Security.Cryptography;
public static class NativePathLoggerCaller {
 [DllImport("kernel32.dll",SetLastError=true)]static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint t,uint f);
 [DllImport("kernel32.dll")]static extern bool VirtualFree(IntPtr p,UIntPtr n,uint t);
 [DllImport("kernel32.dll")]static extern bool VirtualProtect(IntPtr p,UIntPtr n,uint f,out uint old);
 [DllImport("kernel32.dll")]static extern bool FlushInstructionCache(IntPtr process,IntPtr address,UIntPtr size);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]delegate void Shim();
 static readonly List<IntPtr> owned=new List<IntPtr>();static readonly List<string> passes=new List<string>();
 static IntPtr image,plan,context;static Shim shim;static int stateSize=0x79904,cases;const int Canary=0x5aa55aa5;
 static IntPtr A(IntPtr p,int off){return new IntPtr(unchecked(p.ToInt32()+off));}
 static int R(IntPtr p,int off){return Marshal.ReadInt32(p,off);}static void W(IntPtr p,int off,int n){Marshal.WriteInt32(p,off,n);}
 static void Check(bool b,string s){if(!b)throw new InvalidOperationException(s);}
 static byte[] Read(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}
 static bool Same(byte[] a,byte[] b){if(a.Length!=b.Length)return false;for(int i=0;i<a.Length;i++)if(a[i]!=b[i])return false;return true;}
 static string Hash(byte[] b){using(var h=SHA256.Create())return BitConverter.ToString(h.ComputeHash(b)).Replace("-","").ToLowerInvariant();}
 static IntPtr Mem(int n){IntPtr p=VirtualAlloc(IntPtr.Zero,(UIntPtr)n,0x3000,4);Check(p!=IntPtr.Zero,"own allocation");owned.Add(p);return p;}
 static void RX(IntPtr p,int n){uint old;Check(VirtualProtect(p,(UIntPtr)n,0x20,out old),"own RX");Check(FlushInstructionCache(new IntPtr(-1),p,(UIntPtr)n),"flush exact own RX range");}
 static int Number(string s,string name){var m=Regex.Match(s,"\""+name+"\"\\s*:\\s*(\\d+)");Check(m.Success,"integer "+name);return Int32.Parse(m.Groups[1].Value);}
 static Dictionary<string,int> labels;
 static void Setup(int mode,bool stale){
  Marshal.Copy(new byte[stateSize],0,plan,stateSize);
  W(plan,8,123);W(plan,12,8);W(plan,32,7);W(plan,36,1);W(plan,44,5);W(plan,76,1);W(plan,80,1);W(plan,0x78800,123);W(plan,0x78804,stale?6:7);W(plan,0x79800,7);
  W(plan,0x18200,42);W(plan,0x18204,1);W(plan,0x18208,0x00020001);W(plan,0x40600,0x00040003);W(plan,0x40600+72,2);W(plan,0x24680,mode);
  for(int i=0;i<16;i+=4){W(plan,-16+i,Canary);W(plan,stateSize+i,Canary);}
 }
 static void Invoke(string entry){
  W(context,112,A(image,labels[entry]).ToInt32());W(context,0x700,plan.ToInt32());for(int i=4;i<20;i+=4)W(context,0x700+i,0);
  shim();cases++;
  Check(R(context,40)==R(context,44),"stdcall20 ESP");
  Check(R(context,48)==0x13579bdf&&R(context,52)==0x2468ace0&&R(context,56)==0x76543210&&R(context,60)==0x55aa33cc,"nonvolatile ABI");
  Check(Same(Read(A(context,0x300),160),Read(A(context,0x500),160)),"exact x87/controlword");
  for(int i=0;i<16;i+=4)Check(R(plan,-16+i)==Canary&&R(plan,stateSize+i)==Canary,"full0x79904 boundary canaries");
 }
 static void Pass(string s){passes.Add(s);}
 public static int Main(string[] args){
  int status=1;
  try {
   Check(IntPtr.Size==4&&args.Length==4,"x86 only; args root pack reviewed-bin-sha256 reviewed-recipe-sha256");
   string root=args[0],pack=args[1];Check(Regex.IsMatch(File.ReadAllText(Path.Combine(pack,"ROOT-BRONREVIEW.json")),"\"native_allowed\"\\s*:\\s*true"),"separate root native gate");byte[] b=File.ReadAllBytes(Path.Combine(pack,"fixture","logger.bin"));byte[] recipe=File.ReadAllBytes(Path.Combine(pack,"fixture","logger.recipe.json"));
   Check(Hash(b)==args[2]&&Hash(recipe)==args[3],"separately reviewed fixture hashes");string json=System.Text.Encoding.UTF8.GetString(recipe);
   Check(Number(json,"state_size")==stateSize&&Number(json,"record_offset")==0x79804,"exact layout");
   labels=new Dictionary<string,int>();var table=Regex.Match(json,"\"labels\"\\s*:\\s*\\{([^}]+)\\}");Check(table.Success,"label table");
   foreach(Match m in Regex.Matches(table.Groups[1].Value,"\"([^\"]+)\"\\s*:\\s*(\\d+)"))labels[m.Groups[1].Value]=Int32.Parse(m.Groups[2].Value);
   Check(labels["pass_state"]==0x40000&&b.Length<0x40000-16,"own PIC allocation");image=Mem(Number(json,"allocation_size"));Marshal.Copy(b,0,image,b.Length);RX(image,b.Length);plan=A(image,0x40000);context=Mem(0x1000);
   string helper=Path.Combine(root,"PROEVEN","production-h3","helper");byte[] shimbytes=File.ReadAllBytes(Path.Combine(helper,"shim5.bin"));string shimrecipe=File.ReadAllText(Path.Combine(helper,"shim5.recipe.json"));
   foreach(Match m in Regex.Matches(shimrecipe,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)"))Array.Copy(BitConverter.GetBytes(A(context,Int32.Parse(m.Groups[2].Value)).ToInt32()),0,shimbytes,Int32.Parse(m.Groups[1].Value),4);
   IntPtr code=Mem(shimbytes.Length);Marshal.Copy(shimbytes,0,code,shimbytes.Length);RX(code,shimbytes.Length);shim=(Shim)Marshal.GetDelegateForFunctionPointer(code,typeof(Shim));
   foreach(int mode in new int[]{1,2}){
    Setup(mode,false);Invoke("entry");int record=0x79804;
    Check(R(plan,record)==1&&R(plan,record+12)==(mode==1?4:11),"unique raw0 or endpoint edge");
    Check(R(plan,record+112)==(mode==1?0:1),"first failure latch resisted99 overwrite");
    Check(R(plan,record+204)==0&&R(plan,record+208)==0&&R(plan,record+212)==0&&R(plan,4)==25,"direct/cache/selection fallback");
    Check(R(plan,record+36)==labels["pd_select_call"]&&R(plan,record+40)==labels["pd_select_return"]&&R(plan,record+44)==labels["pd_cache_call"]&&R(plan,record+48)==labels["pd_cache_return"]&&R(plan,record+52)==labels["pd_direct_call"]&&R(plan,record+56)==labels["pd_direct_return"],"three actual own callpairs");
    Check(Same(Read(A(plan,0x24600),36),Read(A(plan,0x24630),36)),"logger all GPR/EBP/ESP/EFLAGS exactly preserved");
    Check(R(plan,0x24684)==1,"fixture adapter cleanup once (not enginefree proof)");
    Pass(mode==1?"native0 operands/latch/ABI":"endpoint11 operands/latch/ABI");
    Invoke("reset_entry");Check(Same(Read(A(plan,record),256),new byte[256])&&R(plan,0x79800)==7,"record reset only; generation retained");Pass("reset");
   }
   Setup(3,false);Invoke("entry");Check(R(context,36)==1&&R(plan,0x79804)==0,"normal no failure publication");Pass("normal");
   Setup(1,true);Invoke("entry");Check(R(plan,0x79804)==0&&R(context,36)==0,"stale generation suppresses logging only");Pass("stale binding");
   Setup(5,false);Invoke("entry");Check(R(plan,0x79804)==0&&R(context,36)==0,"wrong actual source argument suppresses logging only");Pass("actual argument binding");
   status=0;
  }catch(Exception e){Console.Error.WriteLine(e);status=1;}
  finally{
   bool cleanup=true;
   for(int i=owned.Count-1;i>=0;i--)cleanup=VirtualFree(owned[i],UIntPtr.Zero,0x8000)&&cleanup;
   owned.Clear();Console.WriteLine("cleanup="+cleanup);
   if(!cleanup)status=1;
  }
  if(status==0){foreach(string pass in passes)Console.WriteLine("PASS "+pass);Console.WriteLine("PASS calls="+cases+"; isolated logger only; no productionpath/gameplay claim");}
  return status;
 }
}
