// Existing H1 self-owned32-bit method. No live process access or game exports.
using System;
using System.IO;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.ComponentModel;
using System.Text.RegularExpressions;
using System.Security.Cryptography;
public static class H3Native {
 [DllImport("kernel32.dll",SetLastError=true,CharSet=CharSet.Unicode)] static extern IntPtr LoadLibraryExW(string file,IntPtr zero,uint flags);
 [DllImport("kernel32.dll",SetLastError=true,CharSet=CharSet.Unicode)] static extern IntPtr LoadLibraryW(string file);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool FreeLibrary(IntPtr module);
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr VirtualAlloc(IntPtr address,UIntPtr size,uint type,uint protect);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool VirtualFree(IntPtr address,UIntPtr size,uint type);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool VirtualProtect(IntPtr address,UIntPtr size,uint protection,out uint previous);
 [DllImport("kernel32.dll")] static extern uint SetErrorMode(uint flags);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)] delegate void Shim();
 static IntPtr A(IntPtr p,int off){return new IntPtr(p.ToInt32()+off);}
 static int R(IntPtr p,int off){return Marshal.ReadInt32(p,off);}
 static long L(IntPtr p,int off){return Marshal.ReadInt64(p,off);}
 static void W(IntPtr p,int off,int value){Marshal.WriteInt32(p,off,value);}
 static void S(IntPtr p,int off,int value){Marshal.WriteInt16(p,off,(short)value);}
 static void D(IntPtr p,int off,double value){Marshal.Copy(BitConverter.GetBytes(value),0,A(p,off),8);}
 static void Check(bool ok,string reason){if(!ok)throw new InvalidOperationException(reason);}
 static byte[] Read(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}
 static bool Equal(byte[] a,byte[] b){if(a.Length!=b.Length)return false;for(int i=0;i<a.Length;i++)if(a[i]!=b[i])return false;return true;}
 static List<IntPtr> owned;
 static IntPtr Mem(int n){IntPtr p=VirtualAlloc(IntPtr.Zero,(UIntPtr)n,0x3000,4);if(p==IntPtr.Zero)throw new Win32Exception();owned.Add(p);return p;}
 static IntPtr Code(byte[] b){IntPtr p=Mem(b.Length);Marshal.Copy(b,0,p,b.Length);uint old;Check(VirtualProtect(p,(UIntPtr)b.Length,0x20,out old),"RX own helper");return p;}
 static IntPtr Code(string root,string name){return Code(File.ReadAllBytes(Path.Combine(root,"helper",name+".bin")));}
 static Dictionary<string,int> Labels(string root){var o=new Dictionary<string,int>();string text=File.ReadAllText(Path.Combine(root,"H3-SCORE_CURRENT.manifest.json"));int start=text.IndexOf("\"labels\""),end=text.IndexOf("\"recipe\"",start);foreach(Match q in Regex.Matches(text.Substring(start,end-start),"\"([^\"]+)\"\\s*:\\s*(\\d+)"))o[q.Groups[1].Value]=Int32.Parse(q.Groups[2].Value);return o;}
 static int cases;
 static string Hash(byte[] bytes){using(var hash=SHA256.Create())return BitConverter.ToString(hash.ComputeHash(bytes)).Replace("-","").ToLowerInvariant();}
 static Shim MakeShim(string root,int argc,IntPtr ctx){byte[] b=File.ReadAllBytes(Path.Combine(root,"helper","shim"+argc+".bin"));string recipe=File.ReadAllText(Path.Combine(root,"helper","shim"+argc+".recipe.json"));foreach(Match q in Regex.Matches(recipe,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)")){int at=Int32.Parse(q.Groups[1].Value),off=Int32.Parse(q.Groups[2].Value);Check(BitConverter.ToInt32(b,at)==0,"unpatched shim slot");Array.Copy(BitConverter.GetBytes(A(ctx,off).ToInt32()),0,b,at,4);}return (Shim)Marshal.GetDelegateForFunctionPointer(Code(b),typeof(Shim));}
 static void Invoke(Shim shim,IntPtr ctx,IntPtr target,params IntPtr[] args){for(int i=0;i<args.Length;i++)W(ctx,0x700+4*i,args[i].ToInt32());W(ctx,112,target.ToInt32());shim();Check(R(ctx,40)==R(ctx,44),"ESP balance case"+cases);Check(R(ctx,48)==0x13579bdf&&R(ctx,52)==0x2468ace0&&R(ctx,56)==0x76543210&&R(ctx,60)==0x55aa33cc,"nonvolatile regs case"+cases);Check(Equal(Read(A(ctx,0x300),160),Read(A(ctx,0x500),160)),"x87 control/status/depth/registers case"+cases);cases++;}
 static IntPtr world,ai,state,host,wgf,db,records,center,result,module;
 static IntPtr[] cells,envs;
 static void Position(IntPtr p,int offset,int x,int y,int z,int padding){S(p,offset,x);S(p,offset+2,y);S(p,offset+4,z);S(p,offset+6,padding);}
 static void Reset(){
  Marshal.Copy(new byte[4096],0,state,4096);W(state,0,100);W(state,4,4);W(state,8,1);W(state,12,1);W(state,16,1);W(state,0x70,1);W(state,0x74,1);W(state,0x78,0x1234);D(state,0x108,15);D(state,0x130,0);D(state,0x138,0);D(state,0x140,0);
  Marshal.Copy(new byte[24*192],0,records,24*192);for(int i=0;i<24;i++)W(A(records,i*192),0xb0,i);
  for(int i=0;i<32;i++){Marshal.Copy(new byte[32],0,cells[i],32);Marshal.WriteByte(cells[i],13,1);W(state,0x400+4*i,1);W(state,0x500+4*i,0);}
  int[] types={1,8,20,22,4};int[] food={5,0,2,3,35};
  for(int i=0;i<types.Length;i++){Marshal.WriteByte(cells[i],13,(byte)types[i]);W(state,0x400+4*i,types[i]);W(state,0x500+4*i,food[i]);W(A(records,types[i]*192),8,food[i]);}
  W(A(records,192),0x50,envs[0].ToInt32());W(envs[0],0,7);
  for(int i=0;i<4;i++)Position(state,0x200+8*i,i+1,0,0,0xaabb);
  W(wgf,72,0);D(wgf,8,1);W(ai,0x20,2);W(ai,0x30,world.ToInt32());W(host,16,wgf.ToInt32());Position(center,0,0,0,0,0);Marshal.Copy(new byte[1024],0,result,1024);
  W(module,0xc6fb4,ai.ToInt32());W(module,0xc6fb0,unchecked((int)0xa55a0000));
 }
 static void Food(int position,int value){int terrain=Marshal.ReadByte(cells[position],13);W(A(records,terrain*192),8,value);for(int i=0;i<32;i++)if(Marshal.ReadByte(cells[i],13)==terrain)W(state,0x500+i*4,value);}
 static void Model(Shim sh,IntPtr ctx,IntPtr entry,int expectedStatus,long s,long d){Invoke(sh,ctx,entry,ai,world,center,result,host);Check(R(result,0)==expectedStatus,"model status case"+cases+" actual"+R(result,0)+" reason"+R(result,4));if(expectedStatus==2){Check(R(result,8)==1&&L(result,56)==s&&L(result,32)==d,"explicit scenario S/D case"+cases);Check(L(result,64)==s-d&&L(result,72)==s-d&&L(result,80)==s,"exact rational crime boundary case"+cases);var distinct=new HashSet<int>();for(int off=100;off<=112;off+=4)Check(distinct.Add(R(result,off)),"four distinct role entries");int f=R(result,112);Check(R(result,384+f*24+4)>0,"positive currentfood role");}Check(R(state,20)<=43,"extra directWorld call bound");}
 public static Dictionary<string,object> Run(string root,string mode){
  Check(IntPtr.Size==4,"x86 only");SetErrorMode(0x8003);var output=new Dictionary<string,object>();output["mode"]=mode;output["bitness"]=32;output["helper_pid"]=System.Diagnostics.Process.GetCurrentProcess().Id;
  string file=Path.Combine(root,"candidates","H3-SCORE_CURRENT","robotcom.dll");output["candidate_sha256"]=Hash(File.ReadAllBytes(file));output["payload_sha256"]=Hash(File.ReadAllBytes(Path.Combine(root,"H3-SCORE_CURRENT.payload.bin")));if(mode=="loader"){IntPtr p=LoadLibraryW(file);if(p==IntPtr.Zero)throw new Win32Exception(Marshal.GetLastWin32Error());output["ordinary_import_DllMain_acceptance"]=true;output["module_base"]=String.Format("0x{0:x8}",p.ToInt32());Check(FreeLibrary(p),"ordinary FreeLibrary");output["pass"]=true;return output;}
  owned=new List<IntPtr>();IntPtr reserved=VirtualAlloc(new IntPtr(0x20000000),(UIntPtr)0xe0000,0x2000,1);Check(reserved==new IntPtr(0x20000000),"reserve preferred DLLbase");module=IntPtr.Zero;
  try{
   module=LoadLibraryExW(file,IntPtr.Zero,1);if(module==IntPtr.Zero)throw new Win32Exception(Marshal.GetLastWin32Error());Check(module.ToInt32()!=0x20000000,"actual rebase");output["actual_rebase"]=true;output["module_base"]=String.Format("0x{0:x8}",module.ToInt32());
   var labels=Labels(root);byte[] payload=File.ReadAllBytes(Path.Combine(root,"H3-SCORE_CURRENT.payload.bin"));Check(Equal(payload,Read(A(module,0xd4000),payload.Length)),"mapped payload unchanged");foreach(int site in new int[]{0x784bb,0x78517,0x7aa35})Check(Marshal.ReadByte(module,site)==0xe8&&site+5+R(module,site+1)==0xd4000&&Marshal.ReadByte(module,site+5)==0x90,"same three hook targets afterrebase");
   int imageSize=R(module,R(module,0x3c)+0x50);byte[] imageBefore=Read(module,imageSize);
   IntPtr ctx=Mem(0x800);Shim sh3=MakeShim(root,3,ctx),sh4=MakeShim(root,4,ctx),sh5=MakeShim(root,5,ctx),sh6=MakeShim(root,6,ctx),sh7=MakeShim(root,7,ctx);
   world=Mem(0x400);ai=Mem(0x100);state=Mem(4096);host=Mem(24);wgf=Mem(0x50);db=Mem(12);records=Mem(24*192);center=Mem(8);IntPtr guarded=Mem(1100);result=A(guarded,32);
   IntPtr vt=A(world,0x100);W(world,0,vt.ToInt32());W(world,4,state.ToInt32());W(vt,0x168,Code(root,"score").ToInt32());W(vt,0x28,Code(root,"gate").ToInt32());W(vt,0xac,Code(root,"open").ToInt32());W(vt,0xa8,Code(root,"terrain").ToInt32());W(vt,0xb8,Code(root,"food").ToInt32());
   // Explicit fixture host, all addresses in owned VirtualAlloc blocks.
   IntPtr engineFixture=Mem(0x680000);S(engineFixture,0x67df20,32);S(engineFixture,0x67df22,1);IntPtr grid=Mem(0x20),zarray=Mem(4),xarray=Mem(32*4);W(grid,0x1c,zarray.ToInt32());W(zarray,0,xarray.ToInt32());cells=new IntPtr[32];envs=new IntPtr[8];for(int i=0;i<envs.Length;i++)envs[i]=Mem(0x50);
   for(int i=0;i<32;i++){cells[i]=Mem(32);IntPtr yy=Mem(4);W(yy,0,cells[i].ToInt32());W(xarray,i*4,yy.ToInt32());}
   W(db,0,24);W(db,8,records.ToInt32());W(host,0,engineFixture.ToInt32());W(host,4,grid.ToInt32());W(host,8,db.ToInt32());W(host,12,Mem(0x1320).ToInt32());W(host,16,wgf.ToInt32());W(host,20,Code(root,"convert").ToInt32());
   IntPtr improvement=Mem(0x100),impvt=A(improvement,0x20);W(improvement,0,impvt.ToInt32());W(improvement,4,state.ToInt32());W(impvt,0x10,Code(root,"available").ToInt32());W(impvt,0x20,Code(root,"position").ToInt32());W(impvt,0x48,Code(root,"delta").ToInt32());W(ai,0x50,improvement.ToInt32());
   IntPtr model=A(module,0xd4000+labels["current_model"]),capacity=A(module,0xd4000+labels["capacity"]),validator=A(module,0xd4000+labels["host_validator"]),adapter=A(module,0xd4000);
   // Patch ONLY a separate own RX allocation's classifiercall. Production
   // module/payload has no fixture branch, helper pointer or fallback.
   byte[] trampoline=File.ReadAllBytes(Path.Combine(root,"helper","fixture-classifier.bin"));string fixjson=File.ReadAllText(Path.Combine(root,"helper","fixture-classifier.recipe.json"));foreach(Match q in Regex.Matches(fixjson,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"kind\"\\s*:\\s*\"([^\"]+)\"")){int at=Int32.Parse(q.Groups[1].Value);Array.Copy(BitConverter.GetBytes(q.Groups[2].Value=="host"?host.ToInt32():model.ToInt32()),0,trampoline,at,4);}IntPtr fc=Code(trampoline);
   byte[] fixturePayload=(byte[])payload.Clone();int classifier=labels["classifier"];int fixtureCall=-1;for(int i=0;i<classifier-4;i++)if(fixturePayload[i]==0xe8&&i+5+BitConverter.ToInt32(fixturePayload,i+1)==classifier){Check(fixtureCall<0,"single adapter classifiercall");fixtureCall=i;}
   Check(fixtureCall>=0,"fixture classifier call found");IntPtr fixtureAdapter;uint old;
   // Copied adapter PIC expects module-relative globals; its base is different,
   // so provide two dedicated safe global data addresses in the copy by patching
   // only the fixture mov/load displacements to own allocation offsets. Better:
   // allocate complete module-sized fixture and retain original RVAs.
   IntPtr fixtureImage=Mem(imageSize);Marshal.Copy(imageBefore,0,fixtureImage,imageSize);Array.Copy(BitConverter.GetBytes(fc.ToInt32()-(fixtureImage.ToInt32()+0xd4000+fixtureCall+5)),0,fixturePayload,fixtureCall+1,4);Marshal.Copy(fixturePayload,0,A(fixtureImage,0xd4000),fixturePayload.Length);Check(VirtualProtect(A(fixtureImage,0xd4000),(UIntPtr)payload.Length,0x20,out old),"fixture image RXpayload");fixtureAdapter=A(fixtureImage,0xd4000);
   cases=0;Reset();Model(sh5,ctx,model,2,52,40);Check(R(result,96)==4&&R(result,92)==2,"H2 available mountains");
   byte[] noWritesWorld=Read(world,0x400),noWritesAi=Read(ai,0x100),noWritesHost=Read(host,24);W(guarded,0,0x12345678);W(guarded,1056,0x34567812);
   foreach(int stand in new int[]{-3,-2,-1,0,1,2,3,9}){Reset();W(wgf,72,stand);D(wgf,8,1+0.25*stand);Model(sh5,ctx,model,2,52,40+10*stand);}
   Reset();Food(4,20);Model(sh5,ctx,model,2,37,40);Reset();Food(4,23);Model(sh5,ctx,model,2,40,40);Reset();Food(4,0);Model(sh5,ctx,model,1,0,0);
   Reset();W(state,4,3);Food(1,80);Model(sh5,ctx,model,1,0,0); // precisely3 mountains cannot also fillfood role
   Reset();W(state,4,0);Model(sh5,ctx,model,1,0,0);Reset();W(state,4,2);Model(sh5,ctx,model,1,0,0);
   foreach(int count in new int[]{-1,21}){Reset();W(state,4,count);Model(sh5,ctx,model,0,0,0);Check(R(result,132)==4&&R(result,136)==-1,"invalidcount H2UNKNOWN");}
   Reset();W(state,8,0);Model(sh5,ctx,model,0,0,0);Check(R(result,132)==3,"gate rejected distinctfromzero");
   Reset();W(state,12,0);Model(sh5,ctx,model,0,0,0);Reset();W(state,0x400+4,-1);Model(sh5,ctx,model,0,0,0);Reset();W(state,0x400+4,24);Model(sh5,ctx,model,0,0,0);
   Reset();Position(state,0x200,1,0,1,0);Model(sh5,ctx,model,0,0,0);Reset();Position(center,0,0,0,1,0);Model(sh5,ctx,model,0,0,0);
   Reset();W(ai,0x30,0);Model(sh5,ctx,model,0,0,0);Reset();D(wgf,8,1.25);Model(sh5,ctx,model,0,0,0);Reset();D(wgf,8,Double.NaN);Model(sh5,ctx,model,0,0,0);Reset();W(wgf,72,-4);D(wgf,8,0);Model(sh5,ctx,model,0,0,0);
   Reset();W(state,16,0);Model(sh5,ctx,model,0,0,0);Reset();W(state,0x500,999);Model(sh5,ctx,model,0,0,0);Reset();Food(0,-5);Model(sh5,ctx,model,0,0,0);
   Reset();IntPtr army=Mem(0x34);W(army,48,1);W(cells[0],16,army.ToInt32());Model(sh5,ctx,model,0,0,0);Reset();W(cells[0],20,7);Model(sh5,ctx,model,0,0,0);Reset();W(cells[4],16,army.ToInt32());Model(sh5,ctx,model,0,0,0);
   Reset();W(state,4,6);Position(state,0x200+32,1,0,0,0x5555);Position(state,0x200+40,0,0,0,0x2222);Model(sh5,ctx,model,2,52,40);Check(R(result,96)==4,"centerremoved duplicatepadding ignored");
   Reset();W(cells[0],0,64);IntPtr good=Mem(192);W(good,8,9);W(good,0x50,envs[1].ToInt32());W(envs[1],0,11);W(A(records,192),0xa0,good.ToInt32());W(state,0x500,9);Model(sh5,ctx,model,2,60,40);Check(L(result,48)==11,"realgood centerbonus");
   Reset();W(cells[0],0,0x140);Model(sh5,ctx,model,0,0,0); // malformedgoodslot5
   Reset();W(cells[1],0,1|4|16|0x800|0x200);IntPtr rec=A(records,8*192);foreach(int off in new int[]{0x5c,0x68,0x74,0x58,0x54})W(rec,off,envs[2].ToInt32());W(envs[2],0,2);W(state,0x504,10);Model(sh5,ctx,model,2,62,40);Check(R(result,384+20)==1,"actualminelevel");
   Reset();W(A(records,192),8,Int32.MaxValue);W(state,0x500,Int32.MaxValue);Model(sh5,ctx,model,0,0,0); // futurecenter overflow
   Reset();S(engineFixture,0x67df20,0);Model(sh5,ctx,model,0,0,0);S(engineFixture,0x67df20,32);
   //20raw unique available places exhaust both queryloops:43extra directcalls.
   Reset();W(state,4,20);for(int i=0;i<20;i++)Position(state,0x200+i*8,i+1,0,0,0);Model(sh5,ctx,model,2,52,40);Check(R(state,20)==43,"measured maximum43extra directcalls");
   output["measured_peak_extra_direct_world_calls"]=R(state,20);W(state,20,0);W(fixtureImage,0xc6fb4,ai.ToInt32());W(fixtureImage,0xc6fb0,unchecked((int)0xa55a0000));Invoke(sh4,ctx,fixtureAdapter,world,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero);Check(R(ctx,36)==101&&R(state,20)==44,"measured total44calls includingoriginal on complete20place adapter");output["measured_peak_total_direct_world_calls"]=R(state,20);
   // Four mountains let richest mountain fillfoodrole only if3others exist.
   Reset();Marshal.WriteByte(cells[4],13,8);W(state,0x410,8);W(state,0x510,0);Food(1,40);Model(sh5,ctx,model,2,97,40);Check(R(result,112)==0,"lexicographic foodtie, triple distinct");
   // Separate development cannot replacecurrent food0 by future inSCORE_CURRENT.
   IntPtr development=A(module,0xd4000+labels["development_model"]),dev=Mem(2048);
   Reset();Food(4,0);W(A(records,4*192),0x6c,envs[3].ToInt32());W(envs[3],0x20,500);W(envs[3],0x24,7);W(envs[3],0x44,123);D(state,0x108,35);
   foreach(int t in new int[]{8,20,22}){W(A(records,t*192),0x74,envs[4].ToInt32());}W(envs[4],0x20,300);W(envs[4],0x24,3);W(envs[4],0x44,124);D(state,0x130,-1);
   Model(sh5,ctx,model,1,0,0);byte[] currentBefore=Read(result,1024);W(state,20,0);Invoke(sh6,ctx,development,ai,world,center,result,dev,host);
   Check(R(dev,0)==2&&R(dev,12)==1&&L(dev,48)==52&&L(dev,56)==12&&L(dev,64)==12&&L(dev,72)==52,"separate pendingfood exactscenario");Check(Equal(currentBefore,Read(result,1024)),"development preserves currentresult");Check(R(dev,128+3*64)==3&&R(dev,128+3*64+28)==500&&R(dev,128+3*64+32)==7&&R(dev,128+3*64+36)==123,"queried IRR2cost/time/advance notbuild");Check(L(dev,80)==0&&(R(dev,120)&unchecked((int)0x80000000))!=0,"negative finaltilefood unsupported");
   D(state,0x130,0);Invoke(sh6,ctx,development,ai,world,center,result,dev,host);Check(L(dev,80)==52&&L(dev,96)==12&&L(dev,104)==52,"separate three-minescenario exactratio");Check(R(state,0x68)>0,"actual x87 deltaqueries");
   W(state,0x70,0);Invoke(sh6,ctx,development,ai,world,center,result,dev,host);Check(R(dev,128+3*64)==1&&(R(dev,116)&1)!=0,"availabilitypending no tech-onlyclaim");W(state,0x70,1);W(state,0x74,0);Invoke(sh6,ctx,development,ai,world,center,result,dev,host);Check(R(dev,128+3*64)==2&&(R(dev,116)&2)!=0,"placeunknown rawstate preserved");Check(R(dev,128+3*64+20)==0x1234,"positionstate raw");
   W(state,0x74,1);D(state,0x108,Double.NaN);Invoke(sh6,ctx,development,ai,world,center,result,dev,host);Check(R(dev,128+3*64)==0,"nonfinite developmentdelta UNKNOWN");D(state,0x108,0.5);Invoke(sh6,ctx,development,ai,world,center,result,dev,host);Check(R(dev,128+3*64)==0,"fractional delta nottruncated");
   Food(1,2);Food(2,3);Food(3,4);D(state,0x108,35);D(state,0x130,-1);Invoke(sh6,ctx,development,ai,world,center,result,dev,host);Check(L(dev,48)==56&&L(dev,80)==53&&L(dev,88)==13&&L(dev,96)==13&&L(dev,104)==53,"negative mine delta with positive finalfood lowers real combined S/margin/crime");Check(R(dev,1440)==3&&R(dev,1440+48)==1&&R(dev,1440+52)==-1,"signed mine delta preserved");
   output["negative_mine_delta_valid_finalfood"]=new Dictionary<string,object>{{"pending_S",L(dev,48)},{"mine_S",L(dev,80)},{"mine_margin",L(dev,88)},{"crime_numerator",L(dev,96)},{"crime_denominator",L(dev,104)},{"delta",R(dev,1440+52)}};
   D(state,0x108,15);Invoke(sh6,ctx,development,ai,world,center,result,dev,host);Check(L(dev,48)==36&&L(dev,56)==-4&&L(dev,80)==33&&L(dev,88)==-7&&L(dev,96)==-7&&L(dev,104)==33,"genuinely insufficient pending+mine scenario preserves negative rationalmargin");
   output["insufficient_pending_mines"]=new Dictionary<string,object>{{"pending_S",L(dev,48)},{"mine_S",L(dev,80)},{"mine_margin",L(dev,88)},{"crime_numerator",L(dev,96)},{"crime_denominator",L(dev,104)}};
   Reset();W(cells[4],0,8);W(A(records,4*192),0x6c,envs[3].ToInt32());W(envs[3],0,15);W(state,0x510,50);Invoke(sh6,ctx,development,ai,world,center,result,dev,host);Check(R(dev,128+3*64)==4&&R(dev,128+3*64+24)==1&&R(dev,128+3*64+52)==0,"existingIRR2 no secondbonus");
   // Same formula for every originalscore, no new admission/rejection.
   foreach(int score in new int[]{-32768,-1,0,1,2,32766,32767})foreach(bool positive in new bool[]{true,false}){
    Reset();if(!positive)Food(4,20);W(state,0,unchecked((int)0xa55a0000)|(score&65535));W(fixtureImage,0xc6fb4,ai.ToInt32());W(fixtureImage,0xc6fb0,unchecked((int)0xa55a0000));Invoke(sh4,ctx,fixtureAdapter,world,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero);int expected=score;if(score>0&&positive&&score<32767)expected++;Check(R(ctx,36)==expected,"adapter +1/nonpositive/saturation case"+cases);Check(R(state,20)<=44,"includingoriginal directcallbound");
   }
   Reset();Invoke(sh4,ctx,adapter,world,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero);Check(R(ctx,36)==100&&R(state,20)==1,"production wronghost fallback");
   IntPtr bindOut=Mem(24);Reset();Invoke(sh3,ctx,validator,ai,world,bindOut);Check(R(ctx,36)==0&&Equal(Read(bindOut,24),new byte[24]),"productionvalidator wronghostzero binding");W(ai,0x30,0);Invoke(sh3,ctx,validator,ai,world,bindOut);Check(R(ctx,36)==0,"validator contextmismatch");W(ai,0x30,world.ToInt32());
   // Header/fingerprint rejection is tested on an OWN allocation at the single
   // supported base. No engine is loaded, no original wrapper is invoked.
   //400000 is occupied in this PowerShell helper. Test original base rejection
   // above, then vary ONLY that literal in a separate validatorallocation to
   // exercise original header/fingerprint/data logic on own arbitrary memory.
   IntPtr headerHost=Mem(0x680000);byte[] validatorCopy=new byte[payload.Length-labels["host_validator"]];Array.Copy(payload,labels["host_validator"],validatorCopy,0,validatorCopy.Length);int patchedBase=0;for(int i=0;i<validatorCopy.Length-5;i++)if(validatorCopy[i]==0x81&&validatorCopy[i+1]==0xfe&&BitConverter.ToInt32(validatorCopy,i+2)==0x400000){Array.Copy(BitConverter.GetBytes(headerHost.ToInt32()),0,validatorCopy,i+2,4);patchedBase++;}Check(patchedBase==1,"single explicit headerfixture baseguardliteral");IntPtr headerValidator=Code(validatorCopy);
   S(headerHost,0,0x5a4d);W(headerHost,0x3c,0x80);W(headerHost,0x80,0x4550);S(headerHost,0x84,0x14c);W(headerHost,0x88,0x37d6f702);S(headerHost,0x98,0x10b);W(headerHost,0xb4,0x400000);
   foreach(string name in new string[]{"terrain","food"}){byte[] wrapper=File.ReadAllBytes(Path.Combine(root,"host",name+"-wrapper.original.bin"));Marshal.Copy(wrapper,0,A(headerHost,name=="terrain"?0x1342e0:0x134340),wrapper.Length);}
   W(headerHost,0x67dd70,grid.ToInt32());W(headerHost,0x67dd3c,db.ToInt32());IntPtr playerInterface=Mem(12);W(playerInterface,8,R(host,12));W(new IntPtr(R(host,12)),0x1318,wgf.ToInt32());W(ai,0x2c,playerInterface.ToInt32());int oldTerrain=R(vt,0xa8),oldFood=R(vt,0xb8);W(vt,0xa8,A(headerHost,0x1342e0).ToInt32());W(vt,0xb8,A(headerHost,0x134340).ToInt32());
   Invoke(sh3,ctx,headerValidator,ai,world,bindOut);Check(R(ctx,36)==1&&R(bindOut,0)==headerHost.ToInt32()&&R(bindOut,4)==grid.ToInt32()&&R(bindOut,8)==db.ToInt32()&&R(bindOut,12)==R(host,12)&&R(bindOut,16)==wgf.ToInt32()&&R(bindOut,20)==A(headerHost,0x103f00).ToInt32(),"validator exact syntheticheader/data binding with explicitfixture baseguard");
   foreach(int off in new int[]{0,0x3c,0x80,0x88,0x98,0xb4,0x1342e0,0x134340,0x67dd70,0x67dd3c}){int oldValue=R(headerHost,off);W(headerHost,off,0);Invoke(sh3,ctx,headerValidator,ai,world,bindOut);Check(R(ctx,36)==0&&Equal(Read(bindOut,24),new byte[24]),"validator invalidheader/fingerprint/nullfield at"+off);W(headerHost,off,oldValue);}
   S(headerHost,0xde,0x40);Invoke(sh3,ctx,headerValidator,ai,world,bindOut);Check(R(ctx,36)==0,"validator DYNAMIC_BASE rejection");S(headerHost,0xde,0);W(headerHost,0x120,1);Invoke(sh3,ctx,headerValidator,ai,world,bindOut);Check(R(ctx,36)==0,"validator nonempty reloc rejection");W(headerHost,0x120,0);W(vt,0xa8,oldTerrain);W(vt,0xb8,oldFood);W(ai,0x2c,0);
   Check(Equal(noWritesWorld,Read(world,0x400))&&Equal(noWritesAi,Read(ai,0x100))&&Equal(noWritesHost,Read(host,24)),"read-only model context");Check(R(guarded,0)==0x12345678&&R(guarded,1056)==0x34567812,"resultguard canaries");
   Marshal.Copy(imageBefore,0xc6fb0,A(module,0xc6fb0),4);Marshal.Copy(imageBefore,0xc6fb4,A(module,0xc6fb4),4);Check(Equal(imageBefore,Read(module,imageSize)),"mapped candidateimage unchanged after ownfixture globalsrestore");
   output["native_cases"]=cases;output["stack_register_x87_result_canaries"]=true;output["direct_world_calls_max_allowed_extra"]=43;output["direct_world_calls_max_allowed_total"]=44;output["explicit_fixture_binding_only_own_allocations"]=true;output["production_wronghost_fallback"]=true;output["synthetic_header_fingerprint_checks_owncopy_baseguard_only"]=true;output["original_validator_acceptance_in_real_engine_unmeasured"]=true;output["development_pending_mines_queried_separately"]=true;output["candidate_pair_saturation_checks"]=true;output["mapped_candidate_restored_unchanged"]=true;output["gameplay_measured"]=false;output["runtime_performance_accepted"]=false;output["pass"]=true;
   GC.KeepAlive(sh3);GC.KeepAlive(sh4);GC.KeepAlive(sh5);GC.KeepAlive(sh6);GC.KeepAlive(sh7);return output;
  }finally{foreach(IntPtr p in owned)VirtualFree(p,UIntPtr.Zero,0x8000);if(module!=IntPtr.Zero)FreeLibrary(module);VirtualFree(reserved,UIntPtr.Zero,0x8000);}
 }
}
