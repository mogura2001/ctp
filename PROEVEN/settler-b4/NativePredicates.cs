// Small ownallocation fixtures using the accepted B2 shim, not engine code.
using System;using System.IO;using System.Runtime.InteropServices;using System.Collections.Generic;using System.Text.RegularExpressions;
public static class B4Predicates {
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr VirtualAlloc(IntPtr a,UIntPtr n,uint t,uint p);
 [DllImport("kernel32.dll")] static extern bool VirtualFree(IntPtr a,UIntPtr n,uint t);
 [DllImport("kernel32.dll")] static extern bool VirtualProtect(IntPtr a,UIntPtr n,uint p,out uint old);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)] delegate void Shim();
 static List<IntPtr> owned=new List<IntPtr>();static IntPtr ctx,plan,image;static int cases;
 static IntPtr A(IntPtr p,int o){return new IntPtr(p.ToInt32()+o);}static int R(IntPtr p,int o){return Marshal.ReadInt32(p,o);}static void W(IntPtr p,int o,int v){Marshal.WriteInt32(p,o,v);}static void S(IntPtr p,int o,int v){Marshal.WriteInt16(p,o,(short)v);}
 static IntPtr Mem(int n){IntPtr p=VirtualAlloc(IntPtr.Zero,(UIntPtr)n,0x3000,4);if(p==IntPtr.Zero)throw new Exception("allocation");owned.Add(p);return p;}
 static void Check(bool v,string why){if(!v)throw new Exception("case "+cases+": "+why);}
 static byte[] Read(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}
 static bool Same(byte[] a,byte[] b){if(a.Length!=b.Length)return false;for(int i=0;i<a.Length;i++)if(a[i]!=b[i])return false;return true;}
 static int Call(string root,int count,int target,params int[] args){
  string h=Path.Combine(root,"PROEVEN","opening-b2","helper");byte[] b=File.ReadAllBytes(Path.Combine(h,"shim"+count+".bin"));string rec=File.ReadAllText(Path.Combine(h,"shim"+count+".recipe.json"));
  foreach(Match f in Regex.Matches(rec,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)"))Array.Copy(BitConverter.GetBytes(A(ctx,Int32.Parse(f.Groups[2].Value)).ToInt32()),0,b,Int32.Parse(f.Groups[1].Value),4);
  IntPtr code=Mem(b.Length);Marshal.Copy(b,0,code,b.Length);uint old;Check(VirtualProtect(code,(UIntPtr)b.Length,0x20,out old),"RX shim");
  W(ctx,112,target);W(ctx,116,0);W(ctx,120,plan.ToInt32());for(int i=0;i<args.Length;i++)W(ctx,0x700+i*4,args[i]);
  ((Shim)Marshal.GetDelegateForFunctionPointer(code,typeof(Shim)))();cases++;
  Check(R(ctx,40)==R(ctx,44),"stack cleanup");Check(R(ctx,48)==0x13579bdf&&R(ctx,52)==plan.ToInt32()&&R(ctx,56)==0x76543210&&R(ctx,60)==0x55aa33cc,"nonvolatile ABI");Check(Same(Read(A(ctx,0x300),160),Read(A(ctx,0x500),160)),"x87 preservation");return R(ctx,36);
 }
 public static int Run(string root,string payload,int owner,int conflict,int order){
  Check(IntPtr.Size==4,"32-bit");cases=0;owned.Clear();try {
   ctx=Mem(0x800);plan=Mem(0x54800);byte[] b=File.ReadAllBytes(payload);image=Mem(0xd4000+b.Length);Marshal.Copy(b,0,A(image,0xd4000),b.Length);uint old;Check(VirtualProtect(A(image,0xd4000),(UIntPtr)b.Length,0x20,out old),"own RX payload");
   foreach(int civ in new int[]{1,7,31})foreach(int raw in new int[]{-1,0,1,7,31,-2,32,255}) {
    int expected=(raw==-1||raw==civ)?1:(raw>=0&&raw<=31)?2:0;
    Check(Call(root,2,A(image,owner).ToInt32(),raw,civ)==expected,"full signed owner gate");
   }
   Check(Call(root,2,A(image,owner).ToInt32(),-1,0)==0,"invalid own civ");
   IntPtr a=A(plan,0x40600),c=A(a,1152);
   for(int i=0;i<5;i++){W(a,32+i*8,i+1);W(c,32+i*8,i+100);}
   Check(Call(root,3,A(image,conflict).ToInt32(),plan.ToInt32(),a.ToInt32(),c.ToInt32())==0,"independent footprints");
   for(int i=0;i<5;i++){int saved=R(c,32+i*8);W(c,32+i*8,3);Check(Call(root,3,A(image,conflict).ToInt32(),plan.ToInt32(),a.ToInt32(),c.ToInt32())==1,"centre/worker conflict");W(c,32+i*8,saved);}
   W(plan,80,3);for(int i=0;i<3;i++){IntPtr p=A(a,1152*i);W(p,16,i==0?2:4);S(p,8,i==1?5:1);S(p,10,2);}
   Call(root,1,A(image,order).ToInt32(),plan.ToInt32());Check(R(plan,0x52680)==2&&R(plan,0x52684)==1&&R(plan,0x52688)==0,"Q descending canonical xy order");
   Check(Same(b,Read(A(image,0xd4000),b.Length)),"fixture payload unchanged");return cases;
  }finally{foreach(IntPtr p in owned)VirtualFree(p,UIntPtr.Zero,0x8000);owned.Clear();}
 }
}
