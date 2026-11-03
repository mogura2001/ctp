// SOURCE ONLY: direct canonical_prefix/production_roles; no compile/run yet.
// Reuses B4 Mem/RX/Code/Call shim mechanics. No LoadLibrary/fixed addresses.
using System;using System.IO;using System.Text;using System.Text.RegularExpressions;using System.Runtime.InteropServices;using System.Collections.Generic;using System.Security.Cryptography;
public static class KaartfilterCaller {
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr VirtualAlloc(IntPtr a,UIntPtr n,uint t,uint p);
 [DllImport("kernel32.dll")] static extern bool VirtualFree(IntPtr a,UIntPtr n,uint t);
 [DllImport("kernel32.dll")] static extern bool VirtualProtect(IntPtr a,UIntPtr n,uint p,out uint old);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)] delegate void Shim();
 static List<IntPtr> owned=new List<IntPtr>();static List<string> passed=new List<string>();
 static Dictionary<string,int> labels=new Dictionary<string,int>();static string root,pack;static IntPtr ctx,state,plan,allocation,image,world;static int cases;
 const int PlanSize=0x54800,Capture=0x200,Order=0x526a0;const int Canary=0x5aa55aa5;
 static IntPtr A(IntPtr p,int o){return new IntPtr(unchecked(p.ToInt32()+o));}static int R(IntPtr p,int o){return Marshal.ReadInt32(p,o);}static void W(IntPtr p,int o,int v){Marshal.WriteInt32(p,o,v);}static void S(IntPtr p,int o,int v){Marshal.WriteInt16(p,o,(short)v);}
 static void Check(bool v,string why){if(!v)throw new Exception("case "+cases+": "+why);}
 static IntPtr Mem(int n){IntPtr p=VirtualAlloc(IntPtr.Zero,(UIntPtr)n,0x3000,4);if(p==IntPtr.Zero)throw new Exception("allocation");owned.Add(p);return p;}
 static byte[] Read(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}static void Clear(IntPtr p,int n){Marshal.Copy(new byte[n],0,p,n);}
 static bool Same(byte[] a,byte[] b){if(a.Length!=b.Length)return false;for(int i=0;i<a.Length;i++)if(a[i]!=b[i])return false;return true;}
 static string Hash(byte[] b){using(SHA256 h=SHA256.Create())return BitConverter.ToString(h.ComputeHash(b)).Replace("-","").ToLowerInvariant();}
 static void RX(IntPtr p,int n){uint old;Check(VirtualProtect(p,(UIntPtr)n,0x20,out old),"RX own memory");}
 static IntPtr Code(string name){byte[] b=File.ReadAllBytes(Path.Combine(pack,"caller","helper",name+".bin"));string rec=File.ReadAllText(Path.Combine(pack,"caller","helper",name+".recipe.json"));foreach(Match f in Regex.Matches(rec,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)"))Array.Copy(BitConverter.GetBytes(A(state,Int32.Parse(f.Groups[2].Value)).ToInt32()),0,b,Int32.Parse(f.Groups[1].Value),4);IntPtr p=Mem(b.Length);Marshal.Copy(b,0,p,b.Length);RX(p,b.Length);return p;}
 static IntPtr Entry(string name){return A(image,labels[name]);}
 static void Jump(string label,IntPtr target){IntPtr p=Entry(label);Marshal.WriteByte(p,0xe9);W(p,1,unchecked(target.ToInt32()-p.ToInt32()-5));}
 static int Call(string label){
  Check(label=="canonical_prefix"||label=="production_roles","only approved direct helpers");Console.WriteLine("caller "+(cases+1)+" "+label);Console.Out.Flush();
  string h=Path.Combine(root,"PROEVEN","opening-b2","helper");byte[] b=File.ReadAllBytes(Path.Combine(h,"shim1.bin"));string rec=File.ReadAllText(Path.Combine(h,"shim1.recipe.json"));
  foreach(Match f in Regex.Matches(rec,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)"))Array.Copy(BitConverter.GetBytes(A(ctx,Int32.Parse(f.Groups[2].Value)).ToInt32()),0,b,Int32.Parse(f.Groups[1].Value),4);
  IntPtr code=Mem(b.Length);Marshal.Copy(b,0,code,b.Length);RX(code,b.Length);W(ctx,112,Entry(label).ToInt32());W(ctx,116,0);W(ctx,120,plan.ToInt32());W(ctx,0x700,plan.ToInt32());
  ((Shim)Marshal.GetDelegateForFunctionPointer(code,typeof(Shim)))();cases++;
  Check(R(ctx,40)==R(ctx,44),"stack cleanup "+label);Check(R(ctx,48)==0x13579bdf&&R(ctx,52)==plan.ToInt32()&&R(ctx,56)==0x76543210&&R(ctx,60)==0x55aa33cc,"nonvolatile ABI "+label);
  Check(Same(Read(A(ctx,0x300),160),Read(A(ctx,0x500),160)),"x87 exact "+label);Bounds();return R(ctx,36);
 }
 static void Bounds(){for(int i=0;i<16;i+=4){Check(R(allocation,i)==Canary&&R(allocation,16+PlanSize+i)==Canary,"outer Plan guard");}Check(R(plan,Order-4)==Canary&&R(plan,Order+64*4)==Canary,"ORDER guard");Check(R(state,40)==0,"stub World/external ABI");}
 static void Test(string s,bool v){Check(v,s);passed.Add(s);Console.WriteLine("PASS "+s);}
 static void Reset(int count){Clear(plan,PlanSize);Clear(state,0x5000);W(plan,0,2);W(plan,112,world.ToInt32());W(plan,68,count);W(state,0,plan.ToInt32());W(state,4,world.ToInt32());W(state,8,A(plan,Capture).ToInt32());W(state,12,A(plan,Capture+Math.Max(0,Math.Min(4096,count))*8).ToInt32());W(state,20,-1);W(state,48,1);W(state,56,-1);W(plan,Order-4,Canary);W(plan,Order+256,Canary);for(int i=0;i<64;i++)W(plan,Order+4*i,Canary);for(int i=0;i<16;i+=4){W(allocation,i,Canary);W(allocation,16+PlanSize+i,Canary);}}
 static void Point(int i,int x,int y,int gate){S(plan,Capture+8*i,x);S(plan,Capture+8*i+2,y);W(state,0x1000+4*i,gate);}
 static void Success(int known,int gatefalse){Test("prefix success",Call("canonical_prefix")==1&&R(plan,224)==Math.Min(64,known)&&R(plan,228)==known&&R(plan,232)==R(plan,68)&&R(plan,236)==gatefalse&&R(state,36)==R(plan,68));}
 static void Load(){
  byte[] b=File.ReadAllBytes(Path.Combine(pack,"U30-40.prepared.dll"));Check(Hash(b)=="738be4098dadc6657b121519213e794ce3ec095025fdc940f6c30a5d89661d66","reviewed candidate");string manifest=File.ReadAllText(Path.Combine(pack,"candidate-manifest.json"));Check(Hash(File.ReadAllBytes(Path.Combine(pack,"candidate-manifest.json")))=="d48b63b2363f0bfce2fe4b7d44a83b90951a524ecf3f300bf9661b50080be2a9","reviewed manifest");
  int pe=BitConverter.ToInt32(b,0x3c),optional=pe+24,size=BitConverter.ToInt32(b,optional+56),section=optional+BitConverter.ToInt16(b,pe+20),n=BitConverter.ToInt16(b,pe+6);image=Mem(size);bool found=false;int rx=0,rxsize=0;
  for(int i=0;i<n;i++){int p=section+40*i;if(Encoding.ASCII.GetString(b,p,8).TrimEnd('\0')!=".u40c")continue;Check(!found,"one code section");found=true;rx=BitConverter.ToInt32(b,p+12);rxsize=BitConverter.ToInt32(b,p+16);Marshal.Copy(b,BitConverter.ToInt32(b,p+20),A(image,rx),rxsize);}Check(found,"own code section");
  Match table=Regex.Match(manifest,"\"labels\"\\s*:\\s*\\{([^}]+)\\}");Check(table.Success,"labels");foreach(Match m in Regex.Matches(table.Groups[1].Value,"\"([^\"]+)\"\\s*:\\s*(-?\\d+)"))labels[m.Groups[1].Value]=0xd9000+Int32.Parse(m.Groups[2].Value);
  ctx=Mem(0x1000);state=Mem(0x5000);allocation=Mem(PlanSize+32);plan=A(allocation,16);world=Mem(16);IntPtr vt=Mem(0x200);W(world,0,vt.ToInt32());W(vt,0x28,Code("gate").ToInt32());W(vt,0x168,Code("score").ToInt32());Jump("canonical_key",Code("key"));Jump("H3Classifier",Code("h3"));RX(A(image,rx),rxsize);
 }
 static void Cases(){
  Reset(0);Success(0,0);Test("a empty no H3",Call("production_roles")==1&&R(plan,128)==0&&R(plan,80)==0);
  Reset(65);for(int i=0;i<65;i++)Point(i,i,0,i==64?7:0);Success(1,64);Test("b late index64",R(plan,Order)==64&&Call("production_roles")==1&&R(plan,220)==1&&R(plan,128)==1);
  Reset(130);List<int> expected=new List<int>();for(int i=0;i<130;i++){Point(i,(i*37)%113,0,i%3==0?0:1);if(i%3!=0)expected.Add(i);}expected.Sort(delegate(int a,int b){int c=((a*37)%113).CompareTo((b*37)%113);return c!=0?c:a.CompareTo(b);});byte[] capture=Read(A(plan,Capture),130*8);Success(expected.Count,130-expected.Count);bool ordered=true;for(int i=0;i<64;i++)ordered&=R(plan,Order+4*i)==expected[i];Test("c ordered true keys and source ties",ordered&&Same(capture,Read(A(plan,Capture),130*8)));
  Reset(65);for(int i=0;i<65;i++)Point(i,i,0,1);Success(65,0);Test("d 65known cutoff64",R(plan,208)==1&&Call("production_roles")==1&&R(plan,128)==64&&R(state,44)==64&&R(plan,80)==0);
  Reset(4096);for(int i=0;i<4096;i++)Point(i,i,0,0);Success(0,4096);Test("d 4096false no H3 or cutoff",Call("production_roles")==1&&R(plan,128)==0&&R(plan,208)==0&&R(plan,Order)==Canary);
  Reset(1);Point(0,0,0,0);W(state,20,0);Test("e invalid key before falsegate",Call("canonical_prefix")==0&&R(plan,4)==41&&R(state,36)==0);
  foreach(int count in new int[]{-1,4097}){Reset(count);Test("e bad candidate count "+count,Call("canonical_prefix")==0&&R(plan,4)==41&&R(state,32)==0);}Reset(1);W(plan,92,1);Test("e nodes guard",Call("canonical_prefix")==0&&R(plan,4)==41&&R(state,32)==0);
  int[,] invalid={{224,-1},{224,65},{228,-1},{68,-1},{224,2},{228,2},{68,4097},{Order,-1},{Order,1}};
  for(int i=0;i<invalid.GetLength(0);i++){Reset(1);Point(0,0,0,1);Success(1,0);W(plan,invalid[i,0],invalid[i,1]);Test("f consumer bounds "+i,Call("production_roles")==0&&R(plan,4)==23&&R(state,44)==0);}
  foreach(int reason in new int[]{11,10}){Reset(1);Point(0,0,0,1);Success(1,0);W(state,48,0);W(state,52,reason);Test("g H3UNKNOWN simulated reason "+reason,Call("production_roles")==0&&R(plan,4)==23&&R(plan,128)==1);}
  Reset(1);Point(0,0,0,1);Success(1,0);W(plan,128,64);Test("g separate H3budget",Call("production_roles")==0&&R(plan,4)==23&&R(state,44)==0);
  Reset(3);for(int i=0;i<3;i++)Point(i,i,0,1);Success(3,0);W(state,56,2);Test("h Bskips before unique H3",Call("production_roles")==1&&R(plan,220)==3&&R(plan,128)==1);
 }
 public static int Run(string repository,string package){root=repository;pack=package;try{Check(IntPtr.Size==4,"x86 only");Load();Cases();File.WriteAllLines(Path.Combine(pack,"caller","PASS.txt"),passed.ToArray());return cases;}finally{for(int i=owned.Count-1;i>=0;i--)VirtualFree(owned[i],UIntPtr.Zero,0x8000);owned.Clear();}}
}
