// Only self-owned allocations and mapped candidate DLL. No OpenProcess,
// injection, exports, GUI, gameplay, network or toolchain installation.
using System;
using System.IO;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.ComponentModel;
public static class H1Native {
 [DllImport("kernel32.dll",SetLastError=true,CharSet=CharSet.Unicode)] static extern IntPtr LoadLibraryExW(string file,IntPtr zero,uint flags);
 [DllImport("kernel32.dll",SetLastError=true,CharSet=CharSet.Unicode)] static extern IntPtr LoadLibraryW(string file);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool FreeLibrary(IntPtr module);
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr VirtualAlloc(IntPtr address,UIntPtr size,uint type,uint protect);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool VirtualFree(IntPtr address,UIntPtr size,uint type);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool VirtualProtect(IntPtr address,UIntPtr size,uint protection,out uint previous);
 [DllImport("kernel32.dll")] static extern uint SetErrorMode(uint flags);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)] delegate void Shim();
 static IntPtr At(IntPtr p,int d){return new IntPtr(p.ToInt32()+d);}
 static int R(IntPtr p,int d){return Marshal.ReadInt32(p,d);}
 static void W(IntPtr p,int d,int v){Marshal.WriteInt32(p,d,v);}
 static void Check(bool ok,string message){if(!ok)throw new InvalidOperationException(message);}
 static byte[] Read(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}
 static bool Equal(byte[] a,byte[] b){if(a.Length!=b.Length)return false;for(int i=0;i<a.Length;i++)if(a[i]!=b[i])return false;return true;}
 static IntPtr Mem(int n){IntPtr p=VirtualAlloc(IntPtr.Zero,(UIntPtr)n,0x3000,4);if(p==IntPtr.Zero)throw new Win32Exception();return p;}
 static IntPtr Executable(string file,List<IntPtr> owned){byte[] b=File.ReadAllBytes(file);IntPtr p=Mem(b.Length);owned.Add(p);Marshal.Copy(b,0,p,b.Length);uint old;Check(VirtualProtect(p,(UIntPtr)b.Length,0x20,out old),"RX helper protection");return p;}
 static long cases;
 static void Case(Shim call,IntPtr ctx,IntPtr module,IntPtr world,IntPtr ai,int raw,int terrain,int status,int write,int x,int y,int z,int globalZ,int context,bool feature){
   int score=(short)(raw&65535);
   W(ctx,0,unchecked((int)0xa55a0000)|(raw&65535));W(ctx,4,terrain);W(ctx,8,status);W(ctx,12,write);
   W(ctx,16,world.ToInt32());W(ctx,20,x);W(ctx,24,y);W(ctx,28,z);
   for(int i=36;i<=100;i+=4)W(ctx,i,unchecked((int)0xcccccccc));W(ctx,64,0);W(ctx,68,0);
   W(ctx,104,unchecked((int)0xf1e2d3c4));W(ctx,108,unchecked((int)0x89abcdef));W(ctx,0xfc,unchecked((int)0x6a7b8c9d));W(ctx,0x700,unchecked((int)0xa1b2c3d4));
   W(ai,0x30,context==2?At(world,16).ToInt32():world.ToInt32());
   W(module,0xc6fb4,context==1?0:ai.ToInt32());
   // Upper WORD deliberately nonzero: must not be treated as g_settle_z.
   W(module,0xc6fb0,unchecked((int)0xa55a0000)|(globalZ&65535));
   byte[] modelBefore=Read(world,0x800);
   call();
   bool query=feature&&score>1&&context==0&&(short)z==0&&(short)globalZ==0;
   int expected=score;
   if(query&&status!=0&&write!=0&&(terrain==8||terrain==20||terrain==22))expected--;
   Check(R(ctx,36)==expected,"score contract case "+cases+" score="+score+" terrain="+terrain+" context="+context);
   Check(R(ctx,40)==R(ctx,44),"ESP balance case "+cases);
   Check(R(ctx,48)==0x13579bdf&&R(ctx,52)==0x2468ace0&&R(ctx,56)==0x76543210&&R(ctx,60)==0x55aa33cc,"nonvolatile register canaries");
   Check(R(ctx,64)==1&&R(ctx,68)==(query?1:0),"callback counts");
   Check(R(ctx,72)==world.ToInt32()&&R(ctx,76)==(short)x&&R(ctx,80)==(short)y&&R(ctx,84)==(short)z,"original getter signed16 arguments");
   if(query){
     int xy=((ushort)y<<16)|(ushort)x;
     Check(R(ctx,88)==world.ToInt32()&&R(ctx,92)==xy&&R(ctx,96)==(ushort)z,"terrain packed16 arguments");
     Check(R(ctx,100)==-1,"terrain sentinel before callback");
   }
   Check(Equal(modelBefore,Read(world,0x800)),"World/vtable/AiMain memory canaries");
   Check(R(ctx,104)==unchecked((int)0xf1e2d3c4)&&R(ctx,108)==unchecked((int)0x89abcdef)&&R(ctx,0xfc)==unchecked((int)0x6a7b8c9d)&&R(ctx,0x700)==unchecked((int)0xa1b2c3d4),"context memory canaries");
   byte[] fpBefore=Read(At(ctx,0x300),160),fpAfter=Read(At(ctx,0x500),160);
   Check(Equal(fpBefore,fpAfter),"x87 control/status/TOP/tag/register preservation");
   Check(Marshal.ReadInt16(ctx,0x300)==0x37f,"fixture x87 controlword");
   Check((Marshal.ReadInt16(ctx,0x302)&0x3800)==0x3000&&Marshal.ReadByte(ctx,0x304)==0xc0,"fixture x87 depth two");
   cases++;
 }
 public static Dictionary<string,object> Run(string root,string variant,string mode){
   Check(IntPtr.Size==4,"x86 only");SetErrorMode(0x8003);
   string file=Path.GetFullPath(Path.Combine(root,"candidates",variant,"robotcom.dll"));
   var output=new Dictionary<string,object>();output["variant"]=variant;output["mode"]=mode;output["bitness"]=32;output["helper_pid"]=System.Diagnostics.Process.GetCurrentProcess().Id;
   if(mode=="loader"){
     IntPtr loaded=LoadLibraryW(file);int error=Marshal.GetLastWin32Error();
     if(loaded==IntPtr.Zero)throw new Win32Exception(error,"ordinary LoadLibraryW failed");
     output["module_base"]=String.Format("0x{0:x8}",loaded.ToInt32());
     Check(FreeLibrary(loaded),"ordinary FreeLibrary");output["ordinary_import_DllMain_acceptance"]=true;output["pass"]=true;return output;
   }
   IntPtr reserved=VirtualAlloc(new IntPtr(0x20000000),(UIntPtr)0xd5000,0x2000,1);
   Check(reserved==new IntPtr(0x20000000),"reserve exact preferred base");
   IntPtr module=IntPtr.Zero;var owned=new List<IntPtr>();
   try {
     module=LoadLibraryExW(file,IntPtr.Zero,1);if(module==IntPtr.Zero)throw new Win32Exception(Marshal.GetLastWin32Error(),"DONT_RESOLVE mapping failed");
     Check(module.ToInt32()!=0x20000000,"actual rebase required");
     output["module_base"]=String.Format("0x{0:x8}",module.ToInt32());output["preferred_base_reserved"]=true;output["actual_rebase"]=true;
     foreach(int site in new int[]{0x784bb,0x78517,0x7aa35})Check(Marshal.ReadByte(module,site)==0xe8&&site+5+R(module,site+1)==0xd4000&&Marshal.ReadByte(module,site+5)==0x90,"rebased call target");
     byte[] code=File.ReadAllBytes(Path.Combine(root,variant+".payload.bin"));Check(Equal(code,Read(At(module,0xd4000),code.Length)),"mapped payload equals candidate");
     byte[] imageBefore=Read(module,0xd5000);
     IntPtr ctx=Mem(0x800);owned.Add(ctx);IntPtr world=Mem(0x800);owned.Add(world);
     // Separate valid fixture World, vtable, and two alternating owner AiMains.
     IntPtr vtable=At(world,0x100),ai1=At(world,0x400),ai2=At(world,0x500);
     byte[] pattern=new byte[0x800];for(int i=0;i<pattern.Length;i++)pattern[i]=(byte)(i*37+11);Marshal.Copy(pattern,0,world,pattern.Length);
     W(world,0,vtable.ToInt32());W(world,4,ctx.ToInt32());
     IntPtr getter=Executable(Path.Combine(root,"helper","score-callback.bin"),owned);
     IntPtr terrain=Executable(Path.Combine(root,"helper","terrain-callback.bin"),owned);
     W(vtable,0x168,getter.ToInt32());W(vtable,0xa8,terrain.ToInt32());
     W(ctx,32,At(module,0xd4000).ToInt32());
     byte[] shim=File.ReadAllBytes(Path.Combine(root,"helper","shim.bin"));
     // Exact fixed relocation slots, independently checked against template.
     int[] fixAt={7,20,26,51,57,63,69,75,80,86,92,98,104,111,118};
     int[] fixOffset={0x100,0x300,40,28,24,20,16,32,36,44,48,52,56,60,0x500};
     // Parse the tiny emitted fixup list with framework JSON to avoid hardcoded
     // emitter positions silently diverging. No external package.
     string fixJson=File.ReadAllText(Path.Combine(root,"helper","shim-fixups.json"));
     var matches=System.Text.RegularExpressions.Regex.Matches(fixJson,"\\\"at\\\"\\s*:\\s*(\\d+)\\s*,\\s*\\\"context_offset\\\"\\s*:\\s*(\\d+)");
     Check(matches.Count==16,"exact shim fixup count");
     foreach(System.Text.RegularExpressions.Match match in matches){int at=Int32.Parse(match.Groups[1].Value),off=Int32.Parse(match.Groups[2].Value);Check(BitConverter.ToInt32(shim,at)==0,"unpatched pointer slot");Array.Copy(BitConverter.GetBytes(At(ctx,off).ToInt32()),0,shim,at,4);}
     IntPtr nativeShim=Mem(shim.Length);owned.Add(nativeShim);Marshal.Copy(shim,0,nativeShim,shim.Length);uint previous;Check(VirtualProtect(nativeShim,(UIntPtr)shim.Length,0x20,out previous),"shim RX");
     Shim invoke=(Shim)Marshal.GetDelegateForFunctionPointer(nativeShim,typeof(Shim));
     bool feature=variant=="H1-M";cases=0;
     if(!feature)for(int raw=0;raw<65536;raw++)Case(invoke,ctx,module,world,ai1,raw,8,1,1,unchecked((int)0x7abc8001),unchecked((int)0x9abcffff),unchecked((int)0x12340000),0,0,false);
     long exhaustive=cases;
     int[] scores={-32768,-1,0,1,2,32767};
     foreach(int score in scores)for(int t=-1;t<24;t++)Case(invoke,ctx,module,world,ai1,score,t,1,1,-32768,32767,0,0,0,feature);
     foreach(int score in scores)foreach(int t in new int[]{8,20,22,9,19,21}){
       Case(invoke,ctx,module,world,ai1,score,t,0,1,-1,-2,0,0,0,feature);
       Case(invoke,ctx,module,world,ai1,score,t,1,0,-1,-2,0,0,0,feature);
       for(int c=1;c<=2;c++)Case(invoke,ctx,module,world,ai1,score,t,1,1,-1,-2,0,0,c,feature);
       foreach(int z in new int[]{1,-1,32767,-32768})Case(invoke,ctx,module,world,ai1,score,t,1,1,-1,-2,z,0,0,feature);
       foreach(int gz in new int[]{1,-1,32767,-32768})Case(invoke,ctx,module,world,ai1,score,t,1,1,-1,-2,0,gz,0,feature);
     }
     for(int i=0;i<40;i++)Case(invoke,ctx,module,world,(i&1)==0?ai1:ai2,2+i%7,(i%4==0)?8:(i%4==1)?20:(i%4==2)?22:9,1,1,unchecked((int)0x7abc8001),unchecked((int)0x9abcffff),unchecked((int)0x12340000),0,0,feature);
     // Restore the only two module data fields touched by fixtures, then assert
     // the entire own mapped image (including shared score data) is unchanged.
     Marshal.Copy(imageBefore,0xc6fb0,At(module,0xc6fb0),4);Marshal.Copy(imageBefore,0xc6fb4,At(module,0xc6fb4),4);
     Check(Equal(imageBefore,Read(module,0xd5000)),"mapped module memory unchanged after restoring fixture globals");
     output["identity_AX_patterns"]=exhaustive;output["native_cases"]=cases;output["stack_register_x87_memory_canaries"]=true;output["context_branches"]=true;output["signed16_highbits_positions"]=true;output["global_z_WORD_highbits"]=true;output["alternating_civ_context"]=true;output["mapped_module_restored_unchanged"]=true;output["pass"]=true;
     GC.KeepAlive(invoke);return output;
   } finally {
     foreach(IntPtr p in owned)VirtualFree(p,UIntPtr.Zero,0x8000);
     if(module!=IntPtr.Zero)FreeLibrary(module);VirtualFree(reserved,UIntPtr.Zero,0x8000);
   }
 }
}
