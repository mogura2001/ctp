// SOURCE ONLY. Existing finite H3/B4 own-image, shim5 and data-stub method.
// No LoadLibrary, engine process, RPM, installation, game or GUI API.
using System;using System.IO;using System.Text;using System.Text.RegularExpressions;
using System.Collections.Generic;using System.Runtime.InteropServices;using System.Security.Cryptography;
public static class NativeFoodCaller {
 [DllImport("kernel32.dll",SetLastError=true)]static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint t,uint f);
 [DllImport("kernel32.dll")]static extern bool VirtualFree(IntPtr p,UIntPtr n,uint t);
 [DllImport("kernel32.dll")]static extern bool VirtualProtect(IntPtr p,UIntPtr n,uint f,out uint old);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]delegate void Shim();
 static readonly List<IntPtr> owned=new List<IntPtr>();static readonly List<string> passes=new List<string>();
 static Dictionary<string,int> labels;static string root,pack;static IntPtr image,plan,ctx,shimctx,stage,world,stubstate,engine,grid,zarray,xarray,yarray,cell,db,records,good,bonus,output,edge,observer,normal;
 static int extension,stateRva,stateSize,imageSize,normalContinuation,cases;static Shim shim;
 const int Canary=0x5aa55aa5;
 static IntPtr A(IntPtr p,int off){return new IntPtr(unchecked(p.ToInt32()+off));}
 static int R(IntPtr p,int off){return Marshal.ReadInt32(p,off);}static void W(IntPtr p,int off,int value){Marshal.WriteInt32(p,off,value);}
 static void H(IntPtr p,int off,int value){Marshal.WriteInt16(p,off,(short)value);}static void Clear(IntPtr p,int n){Marshal.Copy(new byte[n],0,p,n);}
 static byte[] Read(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}
 static bool Same(byte[] a,byte[] b){if(a.Length!=b.Length)return false;for(int i=0;i<a.Length;i++)if(a[i]!=b[i])return false;return true;}
 static void Check(bool ok,string why){if(!ok)throw new InvalidOperationException("case "+cases+": "+why);}
 static void Test(string why,bool ok){Check(ok,why);passes.Add(why);Console.WriteLine("PASS "+why);Console.Out.Flush();}
 static string Hash(byte[] bytes){using(var h=SHA256.Create())return BitConverter.ToString(h.ComputeHash(bytes)).Replace("-","").ToLowerInvariant();}
 static IntPtr Mem(int n){IntPtr p=VirtualAlloc(IntPtr.Zero,(UIntPtr)n,0x3000,4);Check(p!=IntPtr.Zero,"own allocation");owned.Add(p);return p;}
 static void RX(IntPtr p,int n){uint old;Check(VirtualProtect(p,(UIntPtr)n,0x20,out old),"RX own allocation");}
 static IntPtr Code(byte[] b){IntPtr p=Mem(b.Length);Marshal.Copy(b,0,p,b.Length);RX(p,b.Length);return p;}
 static IntPtr FixtureCode(string name){
  byte[] b=File.ReadAllBytes(Path.Combine(pack,"fixture",name+".bin"));string json=File.ReadAllText(Path.Combine(pack,"fixture",name+".recipe.json"));
  foreach(Match m in Regex.Matches(json,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)")){int at=Int32.Parse(m.Groups[1].Value),off=Int32.Parse(m.Groups[2].Value);Check(BitConverter.ToInt32(b,at)==0,"unpatched context slot");Array.Copy(BitConverter.GetBytes(A(ctx,off).ToInt32()),0,b,at,4);}
  return Code(b);
 }
 static int Number(string text,string name){Match m=Regex.Match(text,"\""+name+"\"\\s*:\\s*(\\d+)");Check(m.Success,"manifest integer "+name);return Int32.Parse(m.Groups[1].Value);}
 static int HexNumber(string text,string name){Match m=Regex.Match(text,"\""+name+"\"\\s*:\\s*\"0x([0-9a-f]+)\"");Check(m.Success,"manifest RVA "+name);return Convert.ToInt32(m.Groups[1].Value,16);}
 static IntPtr Entry(string name){return A(image,extension+labels[name]);}
 static void Jump(IntPtr at,IntPtr target){Marshal.WriteByte(at,0xe9);W(at,1,unchecked(target.ToInt32()-at.ToInt32()-5));}
 static Shim MakeShim(){
  string h=Path.Combine(root,"PROEVEN","production-h3","helper");byte[] b=File.ReadAllBytes(Path.Combine(h,"shim5.bin"));string json=File.ReadAllText(Path.Combine(h,"shim5.recipe.json"));
  foreach(Match m in Regex.Matches(json,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)"))Array.Copy(BitConverter.GetBytes(A(shimctx,Int32.Parse(m.Groups[2].Value)).ToInt32()),0,b,Int32.Parse(m.Groups[1].Value),4);
  return (Shim)Marshal.GetDelegateForFunctionPointer(Code(b),typeof(Shim));
 }
 static void Bounds(){
  for(int i=0;i<16;i+=4)Check(R(plan,-16+i)==Canary&&R(plan,stateSize+i)==Canary,"own Plan boundary canaries");
  Check(R(output,-4)==Canary&&R(output,40)==Canary,"out40 boundaries");
 }
 static int Invoke(IntPtr target,IntPtr position,int center){
  Console.WriteLine("caller "+(cases+1));Console.Out.Flush();
  W(shimctx,112,target.ToInt32());W(shimctx,0x700,world.ToInt32());W(shimctx,0x704,position.ToInt32());W(shimctx,0x708,A(plan,144).ToInt32());W(shimctx,0x70c,output.ToInt32());W(shimctx,0x710,center);
  shim();cases++;
  Check(R(shimctx,40)==R(shimctx,44),"stdcall20/ESP");
  Check(R(shimctx,48)==0x13579bdf&&R(shimctx,52)==0x2468ace0&&R(shimctx,56)==0x76543210&&R(shimctx,60)==0x55aa33cc,"nonvolatile ABI");
  Check(Same(Read(A(shimctx,0x300),160),Read(A(shimctx,0x500),160)),"exact x87/controlword state");Bounds();return R(shimctx,36);
 }
 static void Load(string expectedCandidate,string expectedManifest){
  byte[] bytes=File.ReadAllBytes(Path.Combine(pack,"U30-40.prepared.dll"));string manifest=File.ReadAllText(Path.Combine(pack,"candidate-manifest.json"));
  Check(Hash(bytes)==expectedCandidate&&Hash(File.ReadAllBytes(Path.Combine(pack,"candidate-manifest.json")))==expectedManifest,"reviewed candidate/manifest");
  int pe=BitConverter.ToInt32(bytes,0x3c),optional=pe+24,section=optional+BitConverter.ToInt16(bytes,pe+20),count=BitConverter.ToInt16(bytes,pe+6);
  imageSize=BitConverter.ToInt32(bytes,optional+56);image=Mem(imageSize+16);extension=HexNumber(manifest,"extension_rva");stateRva=HexNumber(manifest,"state_rva");stateSize=Number(manifest,"state_size");Check(stateSize==497668,"exact own state");
  int rx=0,rxSize=0;bool found=false;
  for(int i=0;i<count;i++){int at=section+40*i;if(Encoding.ASCII.GetString(bytes,at,8).TrimEnd('\0')!=".u40c")continue;Check(!found,"single own RX section");found=true;rx=BitConverter.ToInt32(bytes,at+12);rxSize=BitConverter.ToInt32(bytes,at+16);Marshal.Copy(bytes,BitConverter.ToInt32(bytes,at+20),A(image,rx),rxSize);}
  Check(found,"own code mapped");plan=A(image,stateRva);labels=new Dictionary<string,int>();Match table=Regex.Match(manifest,"\"labels\"\\s*:\\s*\\{([^}]+)\\}");Check(table.Success,"label table");
  foreach(Match m in Regex.Matches(table.Groups[1].Value,"\"([^\"]+)\"\\s*:\\s*(-?\\d+)"))labels[m.Groups[1].Value]=Int32.Parse(m.Groups[2].Value);
  Check(Entry("pass_state")==plan&&Entry("generation")==A(plan,0x79800),"PIC own Plan, not external scratch");
  // Independent allocations: shim5 owns its ABI/x87 context; fixture wrappers
  // own ctx0..32 and observer0x800. Neither can overwrite the other's slots.
  ctx=Mem(0x1000);shimctx=Mem(0x1000);stage=Mem(236);world=Mem(16);stubstate=Mem(4096);engine=Mem(0x680000);grid=Mem(32);zarray=Mem(4);xarray=Mem(4);yarray=Mem(4);cell=Mem(32);db=Mem(12);records=Mem(24*192);good=Mem(192);bonus=Mem(80);IntPtr guarded=Mem(48);output=A(guarded,4);W(guarded,0,Canary);W(output,40,Canary);
  W(ctx,0,plan.ToInt32());W(ctx,4,stage.ToInt32());W(ctx,12,Entry("sci_food_diag_bad").ToInt32());
  edge=FixtureCode("edge");observer=FixtureCode("observer");normal=FixtureCode("normal");
  string normalRecipe=File.ReadAllText(Path.Combine(pack,"fixture","normal.recipe.json"));normalContinuation=Number(normalRecipe,"continuation");
  // ONLY a private image: hook whole emitted JMPs after POPAD/POPFD; never
  // overwrite the variable-length first instruction of production food_bad.
  for(int i=1;i<=37;i++){
   IntPtr at=Entry("sci_food_diag_failure_"+i+"_restored");Check(Marshal.ReadByte(at)==0xe9&&Marshal.ReadByte(at,-2)==0x61&&Marshal.ReadByte(at,-1)==0x9d,"complete restored-exit JMP boundary");Jump(at,observer);
  }
  // Only the copied SCI return sites point to fixture continuation. The DLL
  // on disk and shared reader bytes are never altered.
  Jump(Entry("sci_food_diag_center_return"),A(normal,normalContinuation));Jump(Entry("sci_food_diag_primary_return"),A(normal,normalContinuation));
  string old=Path.Combine(root,"PROEVEN","production-h3","helper");IntPtr vt=Mem(0x200);W(world,0,vt.ToInt32());W(world,4,stubstate.ToInt32());W(vt,0xb8,Code(File.ReadAllBytes(Path.Combine(old,"food.bin"))).ToInt32());
  W(plan,144+20,Code(File.ReadAllBytes(Path.Combine(old,"convert.bin"))).ToInt32());
  Check(rx+rxSize<=stateRva-16,"prestate padding");for(int i=0;i<16;i+=4){W(plan,-16+i,Canary);W(plan,stateSize+i,Canary);}RX(A(image,rx),rxSize);shim=MakeShim();
 }
 static void Reset(bool record){
  if(record)Clear(A(plan,276),236);Clear(stubstate,4096);Clear(cell,32);Clear(records,24*192);Clear(good,192);Clear(bonus,80);Clear(output,40);
  W(plan,8,123);W(plan,32,7);W(plan,36,1);W(plan,40,1);W(plan,112,world.ToInt32());W(plan,68,1);W(plan,220,4);W(plan,224,4);W(plan,240,4);W(plan,256,64);W(plan,0x78800,123);W(plan,0x78804,7);W(plan,0x526a0+3*4,0);
  // Keep the converter pointer created once in Load; HostBinding uses Plan144.
  W(plan,144,engine.ToInt32());W(plan,148,grid.ToInt32());W(plan,152,db.ToInt32());H(engine,0x67df20,1);H(engine,0x67df22,1);W(grid,0x1c,zarray.ToInt32());W(zarray,0,xarray.ToInt32());W(xarray,0,yarray.ToInt32());W(yarray,0,cell.ToInt32());
  H(plan,0x200,0);H(plan,0x202,0);H(plan,0x204,0);H(plan,0x206,0xaabb);int sci=0x54800+3*2048;W(plan,sci+16,1);for(int i=0;i<8;i++)Marshal.WriteByte(plan,sci+136+i,Marshal.ReadByte(plan,0x200+i));
  Marshal.WriteByte(cell,13,1);W(db,0,24);W(db,8,records.ToInt32());W(records,192+8,5);W(stubstate,0x500,5);W(stubstate,16,1);W(ctx,0x830,0);W(ctx,0x834,0);
 }
 static int EdgeFlags(int id){int flags=0x202;if((id>=4&&id<=8)||(id>=12&&id<=22)||id==24||id==33)flags|=0x40;if(id==32||id==37)flags|=0x80;if((id>=26&&id<=30)||id==35)flags|=0x800;return flags;}
 static void Edge(int id,int kind,bool keep,int expectedLatched){
  Reset(!keep);byte[] pre=File.ReadAllBytes(Path.Combine(pack,"fixture","edge-"+id+".stage.bin"));Check(pre.Length==236,"exact prestate");Array.Copy(BitConverter.GetBytes(kind),0,pre,12,4);Marshal.Copy(pre,0,stage,236);
  W(ctx,8,Entry("sci_food_diag_failure_"+id).ToInt32());W(ctx,20,EdgeFlags(id));Clear(A(ctx,0x800),64);
  int result=Invoke(edge,A(plan,0x200),kind==1?1:0);
  Check(result==0&&Same(Read(output,40),new byte[40]),"original bad out40/EAX0");
  // Saved pushad order: EDI,ESI,EBP,ESP-before-pushad,EBX,EDX,ECX,EAX,flags.
  Check(R(ctx,0x800)==output.ToInt32()&&R(ctx,0x804)==0x56789abc&&R(ctx,0x808)==R(ctx,28)&&R(ctx,0x80c)+4==R(ctx,24),"instrument EDI/ESI/EBP/ESP");
  Check(R(ctx,0x810)==0x456789ab&&R(ctx,0x814)==0x3456789a&&R(ctx,0x818)==0x23456789&&R(ctx,0x81c)==0x12345678,"instrument EBX/EDX/ECX/EAX");
  Check((R(ctx,0x820)&0xcd5)==(EdgeFlags(id)&0xcd5),"instrument arithmetic+DF flags");
  Check(R(ctx,0x824)==Canary&&R(ctx,0x828)==Canary,"private frame staging guards");
  Check(R(plan,280)==1&&R(plan,284)==expectedLatched,"published failure/latch ID");
  if(expectedLatched==id){
   byte[] expected=(byte[])pre.Clone();Array.Copy(BitConverter.GetBytes(1),0,expected,4,4);Array.Copy(BitConverter.GetBytes(id),0,expected,8,4);Array.Copy(BitConverter.GetBytes(R(ctx,0x820)),0,expected,208,4);Array.Copy(BitConverter.GetBytes(BitConverter.ToInt32(pre,36)|(1<<5)),0,expected,36,4);Array.Copy(BitConverter.GetBytes(output.ToInt32()),0,expected,220,4);Array.Copy(BitConverter.GetBytes(A(plan,144).ToInt32()),0,expected,224,4);Array.Copy(BitConverter.GetBytes(world.ToInt32()),0,expected,60,4);
   Check(Same(expected,Read(A(plan,276),236)),"exact reached payload/operands including original EFLAGS");
  }
  Check(R(stubstate,20)==0,"injected log edge has no callbacks");Test("SYNTHETIC log edge "+id+" kind"+kind+" (not natural reachability)",true);
 }
 static byte[] Normal(bool clone,int kind){
  W(ctx,32,Entry(kind==1?"sci_food_diag_center_return":"sci_food_diag_primary_return").ToInt32());W(ctx,36,Entry(clone?"sci_food_diag_reader":"food_reader").ToInt32());Clear(output,40);
  int result=Invoke(normal,kind==1?A(plan,0x200):A(plan,0x54800+3*2048+136),kind==1?1:0);Check(R(ctx,0x830)==Canary&&R(ctx,0x834)==Canary,"SCI local out40 frame canaries");
  byte[] value=new byte[48];Array.Copy(BitConverter.GetBytes(result),0,value,0,4);Array.Copy(Read(output,40),0,value,4,40);Array.Copy(BitConverter.GetBytes(R(stubstate,20)),0,value,44,4);return value;
 }
 static void Setting(string name){
  if(name=="zero"){W(records,192+8,0);W(stubstate,0x500,0);}
  if(name=="bonus"){W(records,192+0x50,bonus.ToInt32());W(bonus,0,7);}
  if(name=="goodfallback"){W(cell,0,2<<6);W(records,192+0xa0,good.ToInt32());W(good,8,9);W(good,0x50,bonus.ToInt32());W(bonus,0,11);W(stubstate,0x500,9);}
  if(name=="pregetter"){W(records,192+8,-1);}
  if(name=="nativefalse")W(stubstate,16,0);if(name=="mismatch")W(stubstate,0x500,6);if(name=="city")W(cell,20,7);
  if(name=="scope0")W(plan,36,0);if(name=="owner0")W(plan,8,0);if(name=="generation_mismatch")W(plan,0x78804,8);if(name=="SCI_count_mismatch")W(plan,240,3);
 }
 static void Compare(string name,int kind,int expectedID){
  Reset(true);Setting(name);byte[] original=Normal(false,kind);Reset(true);Setting(name);byte[] clone=Normal(true,kind);
  Check(Same(original,clone),"same out40/EAX/native callback count "+name);
  if(expectedID==0)Check(R(plan,280)==0,"no success/invalid-binding publication "+name);else Check(R(plan,280)==1&&R(plan,284)==expectedID,"real taken reader guard "+name);
  Test("normal original/clone "+name+" kind"+kind,true);
 }
 public static Dictionary<string,object> Run(string repository,string package,string candidateHash,string manifestHash){
  Check(IntPtr.Size==4,"x86 only");root=repository;pack=package;string gate=File.ReadAllText(Path.Combine(pack,"native","NATIVE-ROOT-REVIEW.json"));
  Check(Regex.IsMatch(gate,"\"native_allowed\"\\s*:\\s*true")&&gate.Contains(candidateHash)&&gate.Contains(manifestHash),"new separate reviewed native release required");
  owned.Clear();passes.Clear();cases=0;
  try{
   Load(candidateHash,manifestHash);
   for(int i=1;i<=37;i++)Edge(i,1,false,i);
   Compare("zero",1,0);Compare("positive",1,0);Compare("bonus",1,0);Compare("goodfallback",1,0);Compare("pregetter",1,31);Compare("nativefalse",1,33);Compare("mismatch",1,34);Compare("city",1,9);Compare("positive",2,0);
   foreach(string name in new string[]{"scope0","owner0","generation_mismatch","SCI_count_mismatch"})Compare(name,1,0);
   Edge(9,2,false,9);Edge(10,2,true,10);Edge(33,1,true,33);Edge(9,2,true,33);Edge(34,1,true,33);
   byte[] latch=Read(A(plan,276),236);Reset(false);Normal(true,1);Check(Same(latch,Read(A(plan,276),236)),"success preserves center failure latch");Test("first center retained across tiles/centers/success; prior tiles replaceable",true);
   Check(Hash(File.ReadAllBytes(Path.Combine(pack,"U30-40.prepared.dll")))==candidateHash,"candidate disk unchanged");
   return new Dictionary<string,object>{{"scope","OWN_FIXTURE_ONLY_NOT_ENGINE_OR_GAMEPLAY"},{"calls",cases},{"passed",passes.ToArray()},{"synthetic_log_edges",37},{"natural_all37_guard_reachability_proven",false},{"gameplay_proven",false}};
  }finally{
   bool all=true;for(int i=owned.Count-1;i>=0;i--)all=VirtualFree(owned[i],UIntPtr.Zero,0x8000)&&all;owned.Clear();Console.WriteLine("cleanup="+all);Console.Out.Flush();Check(all,"all own allocations released");
  }
 }
}
