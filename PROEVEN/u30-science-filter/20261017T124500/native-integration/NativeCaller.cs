// SOURCE ONLY: bounded emitted integration entries; no compile/run yet.
// Reuses B4 Mem/RX/Code/Call shim mechanics. No LoadLibrary/fixed addresses.
using System;using System.IO;using System.Text;using System.Text.RegularExpressions;using System.Runtime.InteropServices;using System.Collections.Generic;using System.Security.Cryptography;
public static class ScienceFilterCaller {
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr VirtualAlloc(IntPtr a,UIntPtr n,uint t,uint p);
 [DllImport("kernel32.dll")] static extern bool VirtualFree(IntPtr a,UIntPtr n,uint t);
 [DllImport("kernel32.dll")] static extern bool VirtualProtect(IntPtr a,UIntPtr n,uint p,out uint old);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)] delegate void Shim();
 static List<IntPtr> owned=new List<IntPtr>();static List<string> passed=new List<string>();
 static Dictionary<string,int> labels=new Dictionary<string,int>();static string root,pack;static IntPtr ctx,state,plan,image,world,player,coupled;static int cases;
 const int PlanSize=0x79800,Capture=0x200,Order=0x526a0;const int Canary=0x5aa55aa5;
 static IntPtr A(IntPtr p,int o){return new IntPtr(unchecked(p.ToInt32()+o));}static int R(IntPtr p,int o){return Marshal.ReadInt32(p,o);}static void W(IntPtr p,int o,int v){Marshal.WriteInt32(p,o,v);}static void S(IntPtr p,int o,int v){Marshal.WriteInt16(p,o,(short)v);}
 static void Check(bool v,string why){if(!v)throw new Exception("case "+cases+": "+why);}
 static IntPtr Mem(int n){IntPtr p=VirtualAlloc(IntPtr.Zero,(UIntPtr)n,0x3000,4);if(p==IntPtr.Zero)throw new Exception("allocation");owned.Add(p);return p;}
 static byte[] Read(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}static void Clear(IntPtr p,int n){Marshal.Copy(new byte[n],0,p,n);}
 static bool Same(byte[] a,byte[] b){if(a.Length!=b.Length)return false;for(int i=0;i<a.Length;i++)if(a[i]!=b[i])return false;return true;}
 static string Hash(byte[] b){using(SHA256 h=SHA256.Create())return BitConverter.ToString(h.ComputeHash(b)).Replace("-","").ToLowerInvariant();}
 static void RX(IntPtr p,int n){uint old;Check(VirtualProtect(p,(UIntPtr)n,0x20,out old),"RX own memory");}
 static IntPtr Code(string name){byte[] b=File.ReadAllBytes(Path.Combine(pack,"native-integration","helper",name+".bin"));string rec=File.ReadAllText(Path.Combine(pack,"native-integration","helper",name+".recipe.json"));foreach(Match f in Regex.Matches(rec,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)"))Array.Copy(BitConverter.GetBytes(A(state,Int32.Parse(f.Groups[2].Value)).ToInt32()),0,b,Int32.Parse(f.Groups[1].Value),4);IntPtr p=Mem(b.Length);Marshal.Copy(b,0,p,b.Length);RX(p,b.Length);return p;}
 static IntPtr Entry(string name){return A(image,labels[name]);}
 static void Jump(string label,IntPtr target){IntPtr p=Entry(label);Marshal.WriteByte(p,0xe9);W(p,1,unchecked(target.ToInt32()-p.ToInt32()-5));}
 static int Call(string label,params int[] more){
  Check(label=="canonical_prefix"||label=="location_roles"||label=="order_roles"||label=="select_direct_plans"||label=="validate_alternative"||label=="plan_conflict"||label=="combine_adapter"||label=="coupled_counter","approved direct helper");
  Console.WriteLine("caller "+(cases+1)+" "+label);Console.Out.Flush();
  int argc=1+more.Length;Check(argc<=3,"bounded arguments");
  string h=Path.Combine(root,"PROEVEN","opening-b2","helper");byte[] b=File.ReadAllBytes(Path.Combine(h,"shim"+argc+".bin"));string rec=File.ReadAllText(Path.Combine(h,"shim"+argc+".recipe.json"));
  foreach(Match f in Regex.Matches(rec,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)"))Array.Copy(BitConverter.GetBytes(A(ctx,Int32.Parse(f.Groups[2].Value)).ToInt32()),0,b,Int32.Parse(f.Groups[1].Value),4);
  IntPtr code=Mem(b.Length);Marshal.Copy(b,0,code,b.Length);RX(code,b.Length);IntPtr target=label=="combine_adapter"?Code("combine"):(label=="coupled_counter"?coupled:Entry(label));W(ctx,112,target.ToInt32());W(ctx,116,0);W(ctx,120,plan.ToInt32());W(ctx,0x700,plan.ToInt32());for(int i=0;i<more.Length;i++)W(ctx,0x704+4*i,more[i]);
  ((Shim)Marshal.GetDelegateForFunctionPointer(code,typeof(Shim)))();cases++;
  Check(R(ctx,40)==R(ctx,44),"stack cleanup "+label);Check(R(ctx,48)==0x13579bdf&&R(ctx,52)==plan.ToInt32()&&R(ctx,56)==0x76543210&&R(ctx,60)==0x55aa33cc,"nonvolatile ABI "+label);
  Check(Same(Read(A(ctx,0x300),160),Read(A(ctx,0x500),160)),"x87 exact "+label);Bounds();return R(ctx,36);
 }
 // Exact candidate c2_count_4 fragment: primary_food + total_food. Only PIC
 // sub-immediate is relocated to this private block's PC; own Plan remains
 // image+pass_state. Original fail exit redirects to local return. Success
 // continuation counts a synthetic query/write, never an engine call.
 static IntPtr CoupledCounter(){
  int pc=labels["c2_count_4_pc"],start=pc-7,n=labels["c2_count_4_done"]-start;Check(n==181,"reviewed coupled fragment length");byte[] b=Read(A(image,start),n);Check(b[0]==0x9c&&b[1]==0x60&&b[n-5]==0xe9,"fragment boundaries");
  byte[] tail={0xff,0x05,0,0,0,0,0xb8,1,0,0,0,0xc2,4,0,0xb8,0,0,0,0,0xc2,4,0};IntPtr p=Mem(n+tail.Length);Marshal.Copy(b,0,p,n);Marshal.Copy(tail,0,A(p,n),tail.Length);W(p,pc-start+3,unchecked(A(p,pc-start).ToInt32()-image.ToInt32()));W(p,n-4,14);W(p,n+2,A(state,80).ToInt32());RX(p,n+tail.Length);return p;
 }
 static void Bounds(){for(int i=0;i<16;i+=4)Check(R(plan,-16+i)==Canary&&R(plan,PlanSize+i)==Canary,"PIC Plan red boundaries");Check(R(plan,Order-4)==Canary&&R(plan,Order+256)==Canary,"ORDER guard");Check(R(state,40)==0,"controlled stub argument ABI");}
 static void Test(string s,bool v){Check(v,s);passed.Add(s);Console.WriteLine("PASS "+s);}
 static void Reset(int count){Clear(plan,PlanSize);Clear(state,0x5000);W(plan,0,2);W(plan,8,123);W(plan,32,7);W(plan,36,1);W(plan,56,10);W(plan,112,world.ToInt32());W(plan,108,player.ToInt32());W(plan,68,count);W(state,0,plan.ToInt32());W(state,4,world.ToInt32());W(state,8,A(plan,Capture).ToInt32());W(state,12,A(plan,Capture+Math.Max(0,Math.Min(4096,count))*8).ToInt32());W(state,20,-1);W(state,48,2);W(state,56,0);W(state,88,Entry("final_combine").ToInt32());W(plan,Order-4,Canary);W(plan,Order+256,Canary);for(int i=0;i<16;i+=4){W(plan,PlanSize+i,Canary);}}
 static void Point(int i,int x,int y,int gate){S(plan,Capture+8*i,x);S(plan,Capture+8*i+2,y);W(state,0x1000+4*i,gate);}
 static void Success(int known,int gatefalse){Test("prefix success",Call("canonical_prefix")==1&&R(plan,224)==Math.Min(64,known)&&R(plan,228)==known&&R(plan,232)==R(plan,68)&&R(plan,236)==gatefalse&&R(state,36)==R(plan,68));}
 static void Load(){
  byte[] b=File.ReadAllBytes(Path.Combine(pack,"U30-40.prepared.dll"));Check(Hash(b)=="0ebafb11e08bc7dca74291dd8a8e9ea94441af09602ae2d94710217f19eabad9","reviewed candidate");string manifest=File.ReadAllText(Path.Combine(pack,"candidate-manifest.json"));Check(Hash(File.ReadAllBytes(Path.Combine(pack,"candidate-manifest.json")))=="9b518945a76cd0369a781de5b8f63be5fc7df963050cb04567a3fa6f6afa58ad","reviewed manifest");
  int pe=BitConverter.ToInt32(b,0x3c),optional=pe+24,size=BitConverter.ToInt32(b,optional+56),section=optional+BitConverter.ToInt16(b,pe+20),n=BitConverter.ToInt16(b,pe+6);image=Mem(size);bool found=false;int rx=0,rxsize=0;
  for(int i=0;i<n;i++){int p=section+40*i;if(Encoding.ASCII.GetString(b,p,8).TrimEnd('\0')!=".u40c")continue;Check(!found,"one code section");found=true;rx=BitConverter.ToInt32(b,p+12);rxsize=BitConverter.ToInt32(b,p+16);Marshal.Copy(b,BitConverter.ToInt32(b,p+20),A(image,rx),rxsize);}Check(found,"own code section");
  Match table=Regex.Match(manifest,"\"labels\"\\s*:\\s*\\{([^}]+)\\}");Check(table.Success,"labels");foreach(Match m in Regex.Matches(table.Groups[1].Value,"\"([^\"]+)\"\\s*:\\s*(-?\\d+)"))labels[m.Groups[1].Value]=0xd9000+Int32.Parse(m.Groups[2].Value);
  // Crucial PIC binding: Plan is the image's own emitted pass_state, never external allocation.
  Check(labels["pass_state"]==0xe1000,"reviewed pass_state RVA");plan=Entry("pass_state");Check(labels["generation"]==labels["pass_state"]+PlanSize,"Plan/generation separation");
  ctx=Mem(0x1000);state=Mem(0x5000);world=Mem(16);player=Mem(16);IntPtr vt=Mem(0x200),pv=Mem(0x100);W(world,0,vt.ToInt32());W(player,0,pv.ToInt32());W(vt,0x28,Code("gate").ToInt32());W(vt,0x168,Code("score").ToInt32());W(pv,0x34,Code("endpoint").ToInt32());Jump("canonical_key",Code("key"));Jump("H3Classifier",Code("h3"));Jump("science_model",Code("science"));Jump("cached_path",Code("path"));Check(rx+rxsize<=labels["pass_state"]-16,"prestate padding redzone");coupled=CoupledCounter();for(int i=0;i<16;i+=4)W(plan,-16+i,Canary);RX(A(image,rx),rxsize);

 }
 const int Slots=0x40600,Stride=1152,Alt=0x74800,Selected=0x52600,Depart=0x18200;
 static IntPtr Slot(int i){return A(plan,Slots+i*Stride);}static void Keys(IntPtr p,int off,int count,int first){for(int i=0;i<count;i++){W(p,off+8*i,first+i);W(p,off+8*i+4,0);}}
 static void PutSlot(int i,int role,int first){IntPtr p=Slot(i);W(p,0,first);W(p,8,first);W(p,16,100-i);W(p,20,-1);W(p,24,-1);W(p,28,role==1?5:4);Keys(p,32,role==1?5:4,first);W(p,72,role);W(p,76,i);W(p,80,role-1);W(p,92,1);W(plan,Order+4*i,i);}
 static void Source(int i,int kind){int d=Depart+32*i;W(plan,d,10+i);W(plan,d+4,kind);W(plan,d+8,1000+i);W(plan,d+16,-1);W(plan,76,i+1);}
 static void Prefix(int count,int falseCount){Reset(count);for(int i=0;i<count;i++)Point(i,100*i,0,i<falseCount?0:1);Success(count-falseCount,falseCount);}
 static void Cases(){
  Prefix(2,2);Test("B6 false gates no SCI",Call("location_roles")==1&&R(state,60)==0&&R(plan,240)==0&&R(plan,80)==0);
  Prefix(66,65);Test("B6 source index65 survives",R(plan,Order)==65&&Call("location_roles")==1&&R(state,60)==1&&R(plan,240)==1&&R(plan,80)==1);
  Prefix(0,0);Test("B6 zero prefix no SCI",Call("location_roles")==1&&R(plan,80)==0&&R(state,60)==0);
  Prefix(1,0);Test("B4 one center two roles one slot",Call("location_roles")==1&&R(plan,80)==1&&R(plan,Slots+72)==1&&R(plan,Alt)==1&&R(plan,Alt+128)==1&&R(plan,Slots+28)==5&&R(plan,Alt+128+8)==4);
  Prefix(65,0);Test("B7 prefix cutoff preserves all64 complete",R(plan,208)==1&&Call("location_roles")==1&&R(plan,80)==64&&R(plan,240)==64&&R(plan,272)==0&&R(state,60)==64&&R(plan,232)==65&&R(plan,236)==0);
  Prefix(2,0);W(plan,240,63);Test("B7 genuine SCIcall exhaustion after complete center",Call("location_roles")==1&&R(plan,80)==1&&R(state,60)==1&&R(plan,240)==64&&R(plan,272)==1&&R(plan,208)==1);
  foreach(int cutoff in new int[]{0,1}){Prefix(2,0);W(plan,208,cutoff);W(state,64,1);Test("B7 postcallback context mismatch cutoff"+cutoff,Call("location_roles")==0&&R(plan,268)==1&&R(plan,40)==0&&R(plan,4)==23);}
  Prefix(1,0);W(plan,240,64);W(state,68,1);Test("B7 scorecallback context mismatch before budget",Call("location_roles")==0&&R(plan,268)==1&&R(plan,272)==0&&R(state,60)==0&&R(plan,40)==0);
  // A coupled real query admission fragment: neither counter increments
  // and continuation query/write is unreachable when either member is full.
  foreach(int full in new int[]{256,264}){Reset(0);W(plan,40,1);W(plan,0x78800,123);W(plan,0x78804,7);W(plan,256,1343);W(plan,264,2623);W(plan,full,full==256?1344:2624);int primary=R(plan,256),total=R(plan,264);Test("B7 coupled limit "+full,Call("coupled_counter")==0&&R(plan,256)==primary&&R(plan,264)==total&&R(state,80)==0&&R(plan,272)==1);}
  Reset(0);W(plan,40,1);W(plan,0x78800,123);W(plan,0x78804,7);W(plan,232,17);W(plan,236,9);Test("B7 coupled success independent gate counters",Call("coupled_counter")==1&&R(plan,256)==1&&R(plan,264)==1&&R(state,80)==1&&R(plan,232)==17&&R(plan,236)==9);
  // Positive/negative physical mandatory-key intersection with complete 4/5 lists.
  Reset(0);PutSlot(0,1,10);PutSlot(1,2,20);Test("B4 disjoint5by4",Call("plan_conflict",Slot(0).ToInt32(),Slot(1).ToInt32())==0);W(Slot(1),32+3*8,14);Test("B4 fifth vs fourth physical key collision",Call("plan_conflict",Slot(0).ToInt32(),Slot(1).ToInt32())==1);W(Slot(1),32+3*8,23);W(Slot(0),100,20);Test("B4 footprint-only overlap permitted",Call("plan_conflict",Slot(0).ToInt32(),Slot(1).ToInt32())==0);
  IntPtr alt=A(plan,Alt);W(alt,8,4);Keys(alt,16,4,10);Test("B4 four unique alternate valid",Call("validate_alternative",alt.ToInt32())==1);W(alt,16+3*8,10);Test("B4 duplicated actual key rejected",Call("validate_alternative",alt.ToInt32())==0);
  foreach(bool valid in new bool[]{true,false}){Reset(0);PutSlot(0,1,10);PutSlot(1,1,30);W(Slot(1),32+4*8,14);W(plan,80,2);Source(0,1);Source(1,1);IntPtr a=A(plan,Alt+256+128);W(a,0,1);W(a,4,2);W(a,8,4);W(a,12,1);Keys(a,16,4,30);W(a,16+3*8,valid?33:14);Test("B4 alternate selection success="+valid,Call("select_direct_plans")==1&&R(plan,60)==(valid?2:1)&&R(Slot(1),72)==2&&R(plan,Depart+32+16)==(valid?1:-1));}
  foreach(int kind in new int[]{1,4,2}){Reset(0);PutSlot(0,1,10);PutSlot(1,2,30);W(plan,80,2);Source(0,kind);Test("B5 sharedsource kind"+kind,Call("select_direct_plans")==1&&R(plan,60)==(kind==2?2:1)&&R(plan,Depart+16)==(kind==2?-1:0));}
  Reset(0);for(int i=0;i<5;i++)PutSlot(i,i<2?1:2,100*i);W(plan,80,5);Source(0,2);Test("B5 combined production2 science3 unique selection",Call("select_direct_plans")==1&&R(plan,60)==5);W(plan,188,R(plan,60));W(plan,184,2);W(plan,56,10);Test("B5 real final_combine G5 D5",Call("combine_adapter")==1&&R(plan,188)==5&&R(plan,60)==5&&R(plan,0)==4);
 }
 public static int Run(string repository,string package){root=repository;pack=package;try{Check(IntPtr.Size==4,"x86 only");Load();Cases();File.WriteAllLines(Path.Combine(pack,"native-integration","PASS.txt"),passed.ToArray());return cases;}finally{bool ok=true;for(int i=owned.Count-1;i>=0;i--)ok=VirtualFree(owned[i],UIntPtr.Zero,0x8000)&&ok;owned.Clear();Console.WriteLine("cleanup="+ok);if(!ok)throw new Exception("cleanup failure");}}
}
