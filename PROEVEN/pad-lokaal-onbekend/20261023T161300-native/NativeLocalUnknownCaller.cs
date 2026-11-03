// SOURCE ONLY. Actual candidate selection/cache/direct/safety/finalizer-tail.
// Raw owned PE copy; no loader/DllMain/import resolver/process/engine access.
using System;using System.IO;using System.Text;using System.Text.RegularExpressions;
using System.Collections.Generic;using System.Runtime.InteropServices;using System.Security.Cryptography;using System.Web.Script.Serialization;
public static class NativeLocalUnknownCaller {
 [DllImport("kernel32.dll",SetLastError=true)]static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint t,uint f);
 [DllImport("kernel32.dll")]static extern bool VirtualFree(IntPtr p,UIntPtr n,uint t);
 [DllImport("kernel32.dll")]static extern bool VirtualProtect(IntPtr p,UIntPtr n,uint f,out uint old);
 [DllImport("kernel32.dll")]static extern bool FlushInstructionCache(IntPtr process,IntPtr p,UIntPtr n);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]delegate void Shim();
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]delegate void FreeOwned(IntPtr p);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]delegate int Path20(IntPtr path,int a1,int a2,int a3,int type,IntPtr source,IntPtr destination,IntPtr capacity,IntPtr pointer,IntPtr count,IntPtr out1,int d8,int a12,int a13,int a14,int search,IntPtr out2,int a17,int a18,int a19);
 static readonly List<IntPtr> owned=new List<IntPtr>();static readonly List<Delegate> callbacks=new List<Delegate>();
 static readonly JavaScriptSerializer json=new JavaScriptSerializer(){MaxJsonLength=64000000};
 static string root,pack,mode;static IntPtr image,plan,active,engine,ai,planner,world,player,path,udb,state,context,driver,buffer,alternate;
 static Dictionary<string,object> manifest;static Dictionary<string,int> labels=new Dictionary<string,int>();
 static int queryCalls,freeCalls,caseCalls,totalQueries,totalNative,maxQueries,pointCount,failAt,expectedFreePointer;static bool preflight;static Shim shim;
 static readonly HashSet<int> freed=new HashSet<int>();static byte[] helperBefore;
 static IntPtr A(IntPtr p,int n){return new IntPtr(unchecked(p.ToInt32()+n));}static int R(IntPtr p,int n){return Marshal.ReadInt32(p,n);}static void W(IntPtr p,int n,int v){Marshal.WriteInt32(p,n,v);}static void S(IntPtr p,int n,int v){Marshal.WriteInt16(p,n,(short)v);}
 static void Check(bool ok,string why){if(!ok)throw new InvalidOperationException(why);}
 static byte[] Read(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}static void Clear(IntPtr p,int n){Marshal.Copy(new byte[n],0,p,n);}
 static string Hash(byte[] b){using(var h=SHA256.Create())return BitConverter.ToString(h.ComputeHash(b)).Replace("-","").ToLowerInvariant();}
 static bool Same(byte[] a,byte[] b){return Hash(a)==Hash(b)&&a.Length==b.Length;}
 static IntPtr Mem(int n){IntPtr p=VirtualAlloc(IntPtr.Zero,(UIntPtr)n,0x3000,4);Check(p!=IntPtr.Zero,"own allocation");owned.Add(p);return p;}
 static void RX(IntPtr p,int n){uint old;Check(VirtualProtect(p,(UIntPtr)n,0x20,out old),"own RX");Check(FlushInstructionCache(new IntPtr(-1),p,(UIntPtr)n),"flush own RX");}
 static Dictionary<string,object> Obj(object o){return (Dictionary<string,object>)o;}static int Num(object o){return Convert.ToInt32(o);}
 static Dictionary<string,object> Load(string p){return Obj(json.DeserializeObject(File.ReadAllText(p)));}
 static IntPtr Entry(string n){return A(image,labels[n]);}
 static IntPtr Existing(string n){
  string folder=Path.Combine(root,"PROEVEN","settler-b4","helper");byte[] b=File.ReadAllBytes(Path.Combine(folder,n+".bin"));string rec=File.ReadAllText(Path.Combine(folder,n+".recipe.json"));
  foreach(Match m in Regex.Matches(rec,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)"))Array.Copy(BitConverter.GetBytes(A(state,Int32.Parse(m.Groups[2].Value)).ToInt32()),0,b,Int32.Parse(m.Groups[1].Value),4);
  IntPtr p=Mem(b.Length);Marshal.Copy(b,0,p,b.Length);RX(p,b.Length);return p;
 }
 static void Jump(IntPtr at,IntPtr to){Marshal.WriteByte(at,0xe9);W(at,1,to.ToInt32()-at.ToInt32()-5);}
 static IntPtr Callback(Delegate d){callbacks.Add(d);return Marshal.GetFunctionPointerForDelegate(d);}
 static void Slot(int table,int off,string n){W(engine,table+off,Existing(n).ToInt32());}
 static void MapOwned(byte[] raw){
  int nt=BitConverter.ToInt32(raw,0x3c),count=BitConverter.ToUInt16(raw,nt+6),opt=nt+24,table=opt+BitConverter.ToUInt16(raw,nt+20),size=BitConverter.ToInt32(raw,opt+56),headers=BitConverter.ToInt32(raw,opt+60),baseAddress=BitConverter.ToInt32(raw,opt+28);
  image=Mem(size);Marshal.Copy(raw,0,image,headers);
  for(int i=0;i<count;i++){int s=table+40*i,n=BitConverter.ToInt32(raw,s+16),at=BitConverter.ToInt32(raw,s+20),rva=BitConverter.ToInt32(raw,s+12);Check(n>=0&&at+n<=raw.Length&&rva+n<=size,"owned PE section bounds");Marshal.Copy(raw,at,A(image,rva),n);}
  int reloc=R(image,opt+136),length=R(image,opt+140),end=reloc+length;
  for(int at=reloc;at<end;){int page=R(image,at),n=R(image,at+4);Check(n>=8&&at+n<=end,"reloc bounds");for(int k=at+8;k<at+n;k+=2){int e=(ushort)Marshal.ReadInt16(image,k);if((e>>12)==3){int dst=page+(e&4095);Check(dst>=0&&dst+4<=size,"reloc own image");W(image,dst,unchecked(R(image,dst)+image.ToInt32()-baseAddress));}else Check((e>>12)==0,"only HIGHLOW/ABS");}at+=n;}
  int ext=Convert.ToInt32((string)Obj(manifest["components"])["extension_rva"],16);
  foreach(var item in Obj(manifest["labels"]))labels[item.Key]=ext+Num(item.Value);
  plan=Entry("pass_state");alternate=Mem(0x79904);helperBefore=Read(A(image,ext),labels["pass_state"]-ext);
 }
 static byte[] Prologue(int n){var b=new List<byte>(new byte[]{0x55,0x8b,0xec,0x53,0x56,0x57,0x81,0xec});b.AddRange(BitConverter.GetBytes(n));b.AddRange(new byte[]{0x8b,0x9d,8,0,0,0});return b.ToArray();}
 static void Drivers(){
  // Inner owns the exact112-byte finalize frame and stdcall4 argument. It
  // enters the ORIGINAL pd_select_call; ORIGINAL continuation/fallback/combine
  // and finalize epilogue run unchanged. Outer adapts only shim5's ret20 ABI.
  IntPtr inner=Mem(64);var a=new List<byte>(Prologue(112));a.Add(0x53);a.Add(0xe9);a.AddRange(BitConverter.GetBytes(Entry("pd_select_call").ToInt32()-inner.ToInt32()-a.Count-4));Marshal.Copy(a.ToArray(),0,inner,a.Count);RX(inner,a.Count);
  driver=Mem(64);var b=new List<byte>(Prologue(0));b.Add(0x53);b.Add(0xe8);b.AddRange(BitConverter.GetBytes(inner.ToInt32()-driver.ToInt32()-b.Count-4));b.AddRange(new byte[]{0x81,0xc4,0,0,0,0,0x5f,0x5e,0x5b,0x5d,0xc2,20,0});Marshal.Copy(b.ToArray(),0,driver,b.Count);RX(driver,b.Count);
  context=Mem(0x1000);string folder=Path.Combine(root,"PROEVEN","production-h3","helper");byte[] sh=File.ReadAllBytes(Path.Combine(folder,"shim5.bin"));string rec=File.ReadAllText(Path.Combine(folder,"shim5.recipe.json"));
  foreach(Match m in Regex.Matches(rec,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)"))Array.Copy(BitConverter.GetBytes(A(context,Int32.Parse(m.Groups[2].Value)).ToInt32()),0,sh,Int32.Parse(m.Groups[1].Value),4);
  IntPtr code=Mem(sh.Length);Marshal.Copy(sh,0,code,sh.Length);RX(code,sh.Length);shim=(Shim)Marshal.GetDelegateForFunctionPointer(code,typeof(Shim));
 }
 static void Setup(){
  state=Mem(4096);engine=Mem(0x6e0000);ai=Mem(0x100);planner=Mem(0xb00);world=Mem(0x200);player=Mem(32);path=Mem(0x100);udb=Mem(16);buffer=Mem(128*32768);
  W(ai,0x20,2);foreach(int[] f in new int[][]{new int[]{0x94,planner.ToInt32()},new int[]{0x80,Mem(128).ToInt32()},new int[]{0x2c,player.ToInt32()},new int[]{0x30,world.ToInt32()},new int[]{0x34,path.ToInt32()},new int[]{0x38,udb.ToInt32()}})W(ai,f[0],f[1]);
  W(ai,0xac,Mem(32).ToInt32());W(world,0,A(engine,0x3452e0).ToInt32());W(player,0,A(engine,0x344660).ToInt32());W(path,0,A(engine,0x346220).ToInt32());W(udb,0,A(engine,0x345098).ToInt32());
  W(state,0,-1);W(state,20,1);W(state,44,0);W(state,48,1);W(state,40,engine.ToInt32());
  IntPtr strategic=Mem(32),grid=Mem(32);W(planner,0xa70,strategic.ToInt32());W(strategic,0,1);W(image,0xc6fdc,grid.ToInt32());W(grid,0,Mem(32).ToInt32());W(grid,4,1);W(grid,8,1024);S(engine,0x67df20,1024);S(engine,0x67df22,1);
  Jump(A(engine,0x103f00),Existing("convert"));RX(A(engine,0x103f00),5);
  Jump(Entry("GetContinent"),Existing("continent"));Jump(Entry("GetThreat"),Existing("threat"));
  Slot(0x3452e0,0xa8,"terrain");Slot(0x3452e0,0x54,"pointowner");Slot(0x3452e0,0x78,"presence");Slot(0x344660,0x14,"playerconvert");Slot(0x344660,0x2c,"true12");Slot(0x344660,0x34,"true12");
  W(engine,0x346220+12,Callback(new Path20(Query)).ToInt32());Jump(A(engine,0x1866e0),Callback(new FreeOwned(Free)));RX(A(engine,0x1866e0),5);
  RX(image,labels["pass_state"]);Drivers();
 }
 static int Query(IntPtr iface,int a1,int a2,int a3,int type,IntPtr src,IntPtr dst,IntPtr cap,IntPtr ptr,IntPtr count,IntPtr out1,int d8,int a12,int a13,int a14,int search,IntPtr out2,int a17,int a18,int a19){
  queryCalls++;totalQueries++;Check(queryCalls<=maxQueries&&totalQueries<=512,"finite query bound");
  Check(iface==path&&type==1&&d8==0&&a1==0&&a2==0&&a3==1&&a12==1&&a13==0&&a14==0&&search==4096&&a17==1&&a18==0&&a19==1,"real20argument ABI");
  int sx=(ushort)Marshal.ReadInt16(src),dx=(ushort)Marshal.ReadInt16(dst);bool failing=queryCalls==failAt;bool zero=mode=="all-zero"||(mode=="A-zero"&&sx==1)||(mode=="B-then-A"&&sx==2)||(mode=="middle-zero"&&dx==20);
  if(failing&&mode.StartsWith("hard-")){
   string x=mode.Substring(5);zero=true;
   if(x=="owner")W(plan,8,0);if(x=="civ")W(ai,0x20,3);if(x=="generation")W(plan,32,8);if(x=="snapshot")W(plan,0x78804,8);if(x=="global-generation")W(plan,0x79800,8);
   if(x=="type")W(plan,44,2);if(x=="d8")W(plan,120,1);if(x=="path")W(ai,0x34,world.ToInt32());if(x=="source-bytes")W(src,0,99);if(x=="destination-bytes")W(dst,0,99);if(x=="argument-pointer")W(cap,28,A(src,8).ToInt32());if(x=="claim")W(plan,0x18200+16,0);
   if(x=="canary1")W(cap,-24,0);if(x=="canary2")W(cap,-28,0);if(x=="postcontext")W(engine,0x6d0b94,1);
   if(x=="dirty-cap")W(cap,0,1);if(x=="dirty-count")W(count,0,1);
   if(x=="native2")return 2;if(x=="native-minus1")return -1;
   if(x=="dirty-pointer"){IntPtr own=A(buffer,(queryCalls-1)*32768);W(ptr,0,own.ToInt32());expectedFreePointer=own.ToInt32();return 0;}
   if(x.StartsWith("success-")||x=="safety-unknown")zero=false;
  }
  if(zero)return 0; // Never returns4: only the actual candidate can produce4.
  IntPtr points=A(buffer,(queryCalls-1)*32768);int n=pointCount;W(cap,0,n);W(count,0,n);W(ptr,0,points.ToInt32());expectedFreePointer=points.ToInt32();
  for(int i=0;i<n;i++){W(points,i*8,R(src,0));W(points,i*8+4,R(src,4));}W(points,(n-1)*8,R(dst,0));W(points,(n-1)*8+4,R(dst,4));
  if(failing){string x=mode.StartsWith("hard-")?mode.Substring(5):mode;if(x=="success-null")W(ptr,0,0);if(x=="success-count0")W(count,0,0);if(x=="success-negative")W(count,0,-1);if(x=="success-capacity")W(cap,0,1);if(x=="success-endpoint")W(points,0,999);if(x=="success-overflow"){W(ptr,0,unchecked((int)0xfffffff8));expectedFreePointer=unchecked((int)0xfffffff8);}if(x=="safety-unknown")W(state,0,-2);if(x=="safety2")W(state,0,3);}
  return 1;
 }
 static void Free(IntPtr p){freeCalls++;Check(p.ToInt32()==expectedFreePointer,"free exact observed native pointer");Check(freed.Add(p.ToInt32()),"nonnull free exactly once");}
 static void Reset(Dictionary<string,object> c){
  Clear(plan,0x79904);mode=(string)c["mode"];int slots=Num(c["slots"]),departures=Num(c["departures"]),kind=Num(c["kind"]);maxQueries=Num(c["query_max"]);pointCount=Num(c["points"]);failAt=Num(c["fail_at"]);queryCalls=freeCalls=0;freed.Clear();active=plan;
  W(ai,0x20,2);W(ai,0x34,path.ToInt32());W(state,0,-1);W(state,316,-1);W(state,320,-1);W(engine,0x6d0b94,0);
  foreach(int[] f in new int[][]{new int[]{0,2},new int[]{8,ai.ToInt32()},new int[]{12,2},new int[]{16,R(ai,0x80)},new int[]{20,planner.ToInt32()},new int[]{24,A(planner,0x20).ToInt32()},new int[]{28,Mem(16).ToInt32()},new int[]{32,7},new int[]{36,1},new int[]{44,1},new int[]{48,3},new int[]{56,40},new int[]{76,departures},new int[]{80,slots},new int[]{84,Num(c["start_queries"])},new int[]{100,engine.ToInt32()},new int[]{104,udb.ToInt32()},new int[]{108,player.ToInt32()},new int[]{112,world.ToInt32()},new int[]{116,path.ToInt32()},new int[]{184,Num(c["Dorig"])},new int[]{188,0},new int[]{212,1},new int[]{220,slots},new int[]{224,slots},new int[]{0x78800,ai.ToInt32()},new int[]{0x78804,7},new int[]{0x79800,7}})W(plan,f[0],f[1]);
  for(int i=0;i<slots;i++){int at=0x40600+i*1152;W(plan,at,(i+1)*10);W(plan,at+28,1);W(plan,at+32,(i+1)*10);W(plan,at+72,2);W(plan,at+76,i);W(plan,0x526a0+i*4,i);}
  for(int i=0;i<departures;i++){int at=0x18200+i*32;W(plan,at,10+i);W(plan,at+4,kind);W(plan,at+8,mode=="A-zero-cache"&&i<2?1:i+1);W(plan,at+16,-1);W(plan,at+20,ai.ToInt32());}
  if(mode=="A-zero-cache")mode="A-zero";
  if(mode=="conflict")W(plan,0x40600+1152+32,10);
  if(mode=="before-plan"){Marshal.Copy(Read(plan,0x79904),0,alternate,0x79904);active=alternate;}
  if(mode=="before-owner")W(plan,8,0);if(mode=="before-civ")W(plan,12,0);if(mode=="before-generation")W(plan,0x79800,8);if(mode=="before-precontext")W(engine,0x6d0b94,1);
 }
 static Dictionary<string,object> RunCase(Dictionary<string,object> c){
  Reset(c);W(context,112,driver.ToInt32());W(context,0x700,active.ToInt32());for(int i=4;i<20;i+=4)W(context,0x700+i,0);
  shim();caseCalls++;totalNative++;Check(totalNative<=64,"finite native driver calls");
  Check(R(context,40)==R(context,44),"shim/inner/actual-finalizer stack balance");Check(R(context,48)==0x13579bdf&&R(context,52)==0x2468ace0&&R(context,56)==0x76543210&&R(context,60)==0x55aa33cc,"nonvolatile GPR");Check(Same(Read(A(context,0x300),160),Read(A(context,0x500),160)),"x87/controlword/depth");
  Check(R(context,36)==1,"actual finalize tail returns1");Check(R(active,188)==Num(c["Gcert"])&&R(active,60)==Num(c["desired"])&&R(active,4)==Num(c["reason"]),"actual selection/fallback/combine expected");
  Check(queryCalls==Num(c["queries"])&&freeCalls==Num(c["frees"]),"exact nativequery/free counts");Check(R(active,208)==Num(c["cutoff"]),"budget cutoff");
  if((string)c["name"]=="positive-before-later4")Check(R(plan,0x40600+20)==10&&R(plan,0x18200+16)==0&&R(plan,0x18200+32+16)==-1,"restore_best chooses original positive only");
  if((string)c["name"]=="unit-claim-once")Check(R(plan,0x18200+16)==0,"single unit claimed once");
  if((string)c["name"]=="build-origin-reused")Check(R(plan,0x18200+16)==-1,"reusable build origin unconsumed");
  int ext=Convert.ToInt32((string)Obj(manifest["components"])["extension_rva"],16);Check(Same(helperBefore,Read(A(image,ext),helperBefore.Length)),"actual helper code untouched");
  return new Dictionary<string,object>{{"case",c["name"]},{"queries",queryCalls},{"free",freeCalls},{"Gcert",R(active,188)},{"desired",R(active,60)},{"reason",R(active,4)},{"native_abi_checked",true},{"full_native_priority_array_claim",false}};
 }
 public static int Run(string repository,string package){
  root=Path.GetFullPath(repository);pack=Path.GetFullPath(package);Check(IntPtr.Size==4,"owned32bit only");var gate=Load(Path.Combine(pack,"ROOT-VRIJGAVE.json"));Check((bool)gate["native_allowed"]&&(bool)gate["fixture_allowed"],"Separate reviewed native+fixture gate required");
  string pinsPath=Path.Combine(pack,"SOURCE-PINS.json"),casePath=Path.Combine(pack,"CASES.json"),build=Path.Combine(root,"PROEVEN","pad-lokaal-onbekend","20261023T155300-build");Check(Hash(File.ReadAllBytes(pinsPath))==(string)gate["reviewed_source_pins_sha256"],"reviewed sources");
  foreach(object x in (object[])Load(pinsPath)["sources"]){var r=Obj(x);Check(Hash(File.ReadAllBytes(Path.Combine(root,(string)r["path"])))==(string)r["sha256"],"source pin "+r["path"]);}
  byte[] candidate=File.ReadAllBytes(Path.Combine(build,"U30-40.prepared.dll"));string manifestPath=Path.Combine(build,"candidate-manifest.json");Check(Hash(candidate)==(string)gate["reviewed_candidate_sha256"]&&Hash(File.ReadAllBytes(manifestPath))==(string)gate["reviewed_manifest_sha256"]&&Hash(File.ReadAllBytes(casePath))==(string)gate["reviewed_cases_sha256"],"candidate/manifest/cases bound");
  manifest=Load(manifestPath);var cases=Load(casePath);Check(Num(cases["max_driver_calls"])<=64&&Num(cases["max_query_calls"])<=512,"finite approved case bounds");var results=new List<Dictionary<string,object>>();
  try{MapOwned(candidate);Setup();foreach(object x in (object[])cases["cases"])results.Add(RunCase(Obj(x)));Check(totalQueries<=Num(cases["max_query_calls"])&&caseCalls==Num(cases["max_driver_calls"]),"exact finite case count");File.WriteAllText(Path.Combine(pack,"NATIVE-RESULT.json"),json.Serialize(new Dictionary<string,object>{{"cases",results},{"calls",caseCalls},{"queries",totalQueries},{"gameplay",false},{"full_priority_runtime",false}}));return 0;}
  finally{for(int i=owned.Count-1;i>=0;i--)VirtualFree(owned[i],UIntPtr.Zero,0x8000);owned.Clear();GC.KeepAlive(callbacks);}
 }
}
