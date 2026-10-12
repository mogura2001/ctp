// Native execution of actual B4 composition in a separate owned fixture copy.
// Changed dependency addresses provide controlled inputs; B4/H3 model intact.
using System;using System.IO;using System.Runtime.InteropServices;using System.Collections.Generic;using System.Text.RegularExpressions;
public static class B4Producer {
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr VirtualAlloc(IntPtr a,UIntPtr n,uint t,uint p);
 [DllImport("kernel32.dll")] static extern bool VirtualFree(IntPtr a,UIntPtr n,uint t);
 [DllImport("kernel32.dll")] static extern bool VirtualProtect(IntPtr a,UIntPtr n,uint p,out uint old);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern IntPtr LoadLibraryW(string p);
 [DllImport("kernel32.dll")] static extern bool FreeLibrary(IntPtr p);
 [DllImport("kernel32.dll")] static extern uint SetErrorMode(uint p);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int ExceptionHandler(IntPtr info);
 [DllImport("kernel32.dll")] static extern IntPtr AddVectoredExceptionHandler(uint first,ExceptionHandler callback);
 [DllImport("kernel32.dll")] static extern uint RemoveVectoredExceptionHandler(IntPtr handle);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)] delegate void Shim();
 static List<IntPtr> owned=new List<IntPtr>();static Dictionary<string,int> labels;static string root,pack;static IntPtr ctx,plan,image,state,engine,ai,planner,world,player,path,udb,strategic,center,city,army,scheduler,hostbinding;static int cases,imageSize;static List<string> passed=new List<string>();
 static IntPtr A(IntPtr p,int o){return new IntPtr(p.ToInt32()+o);}static int R(IntPtr p,int o){return Marshal.ReadInt32(p,o);}static void W(IntPtr p,int o,int v){Marshal.WriteInt32(p,o,v);}static void S(IntPtr p,int o,int v){Marshal.WriteInt16(p,o,(short)v);}static void D(IntPtr p,int o,double v){Marshal.Copy(BitConverter.GetBytes(v),0,A(p,o),8);}
 static IntPtr Mem(int n){IntPtr p=VirtualAlloc(IntPtr.Zero,(UIntPtr)n,0x3000,4);if(p==IntPtr.Zero)throw new Exception("allocation");owned.Add(p);return p;}
 static void Check(bool v,string why){if(!v)throw new Exception("case "+cases+": "+why);}
 static byte[] Read(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}
 static bool Same(byte[] a,byte[] b){if(a.Length!=b.Length)return false;for(int i=0;i<a.Length;i++)if(a[i]!=b[i])return false;return true;}
 static void Clear(IntPtr p,int n){Marshal.Copy(new byte[n],0,p,n);}
 static void RX(IntPtr p,int n){uint o;Check(VirtualProtect(p,(UIntPtr)n,0x20,out o),"RX own memory");}
 static void Patch(IntPtr p,int n){uint o;Check(VirtualProtect(p,(UIntPtr)n,0x40,out o),"fixture patch protection");}
 static IntPtr Code(string name){byte[] b=File.ReadAllBytes(Path.Combine(pack,"helper",name+".bin"));string rec=File.ReadAllText(Path.Combine(pack,"helper",name+".recipe.json"));foreach(Match f in Regex.Matches(rec,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)"))Array.Copy(BitConverter.GetBytes(A(state,Int32.Parse(f.Groups[2].Value)).ToInt32()),0,b,Int32.Parse(f.Groups[1].Value),4);IntPtr code=Mem(b.Length);Marshal.Copy(b,0,code,b.Length);RX(code,b.Length);return code;}
 static void Jump(IntPtr target,IntPtr code){Patch(target,5);Marshal.WriteByte(target,0xe9);W(target,1,code.ToInt32()-target.ToInt32()-5);}
 static IntPtr Entry(string name){return A(image,labels[name]);}
 static void Dependency(string label,string stub){Jump(Entry(label),Code(stub));}
 static int Call(string label,int thisptr,bool exactFpu,params int[] args){
  Console.WriteLine("native case "+(cases+1)+" "+label);Console.Out.Flush();
  string h=Path.Combine(root,"PROEVEN","opening-b2","helper");byte[] b=File.ReadAllBytes(Path.Combine(h,"shim"+args.Length+".bin"));string rec=File.ReadAllText(Path.Combine(h,"shim"+args.Length+".recipe.json"));
  foreach(Match f in Regex.Matches(rec,"\"at\"\\s*:\\s*(\\d+)\\s*,\\s*\"context_offset\"\\s*:\\s*(\\d+)"))Array.Copy(BitConverter.GetBytes(A(ctx,Int32.Parse(f.Groups[2].Value)).ToInt32()),0,b,Int32.Parse(f.Groups[1].Value),4);
  IntPtr code=Mem(b.Length);Marshal.Copy(b,0,code,b.Length);RX(code,b.Length);Match post=Regex.Match(rec,"\"postcall\"\\s*:\\s*(\\d+)");Check(post.Success,"shim recoverylabel");W(ctx,124,A(code,Int32.Parse(post.Groups[1].Value)).ToInt32());W(ctx,112,Entry(label).ToInt32());W(ctx,116,thisptr);W(ctx,120,plan.ToInt32());for(int i=0;i<args.Length;i++)W(ctx,0x700+i*4,args[i]);
  int trapsBefore=R(state,336);((Shim)Marshal.GetDelegateForFunctionPointer(code,typeof(Shim)))();cases++;
  Check(R(ctx,40)==R(ctx,44),"stack cleanup "+label);Check(R(ctx,48)==0x13579bdf&&R(ctx,52)==plan.ToInt32()&&R(ctx,56)==0x76543210&&R(ctx,60)==0x55aa33cc,"nonvolatile ABI "+label);
  if(R(state,336)==trapsBefore){if(exactFpu)Check(Same(Read(A(ctx,0x300),160),Read(A(ctx,0x500),160)),"x87 preservation "+label);
  else Check((R(ctx,0x300)&65535)==(R(ctx,0x500)&65535)&&Marshal.ReadByte(ctx,0x304)==Marshal.ReadByte(ctx,0x504),"x87 controlword/depth "+label);}
  return R(ctx,36);
 }
 // Only deliberate UD2 at the exact emitted contract_error is caught. Its
 // actual exception address/code are recorded; the exception is rejected,
 // never treated as producer success or a fallback. Recovery skips to the
 // existing shim postcall so this bounded helper can report the rejection.
 static ExceptionHandler handler=ContractException;
 static int ContractException(IntPtr info){IntPtr record=new IntPtr(R(info,0)),context=new IntPtr(R(info,4));if(R(record,0)!=unchecked((int)0xc000001d)||R(record,12)!=Entry("contract_error").ToInt32())return 0;W(state,336,R(state,336)+1);W(state,340,R(record,0));W(state,344,R(record,12));W(context,184,R(ctx,124));W(context,196,R(ctx,40));W(context,164,0x13579bdf);W(context,160,plan.ToInt32());W(context,156,0x76543210);W(context,180,0x55aa33cc);W(context,176,-1);return -1;}
 static void Test(string name,bool v){Check(v,name);passed.Add(name);}
 static IntPtr Interface(int size,int vtrva){IntPtr p=Mem(size);W(p,0,A(engine,vtrva).ToInt32());return p;}
 static void Slot(int vtrva,int off,string code){W(engine,vtrva+off,Code(code).ToInt32());}
 static IntPtr Node(int kind,int id,IntPtr agent){IntPtr p=Mem(16);W(p,0,id);W(p,12,agent.ToInt32());W(agent,4,kind);W(agent,12,id);return p;}
 static IntPtr Set(IntPtr node){IntPtr p=Mem(32);W(p,0,node==IntPtr.Zero?0:1);W(p,8,node.ToInt32());W(p,16,Mem(4096*4).ToInt32());W(p,20,Mem(4096*4).ToInt32());W(p,24,-1);return p;}
 static void Setup(){
  ctx=Mem(0x800);state=Mem(4096);engine=Mem(0x6e0000);ai=Mem(0x100);planner=Mem(0xb00);scheduler=Mem(0x500);strategic=Mem(64);center=Mem(8);city=Mem(0x230);army=Mem(0x100);hostbinding=Mem(24);
  plan=A(image,labels["pass_state"]);world=Interface(0x200,0x3452e0);player=Interface(32,0x344660);path=Interface(0x100,0x346220);udb=Interface(16,0x345098);
  W(ai,0x20,2);W(ai,0x94,planner.ToInt32());W(ai,0x80,Mem(0x80).ToInt32());W(ai,0x2c,player.ToInt32());W(ai,0x30,world.ToInt32());W(ai,0x34,path.ToInt32());W(ai,0x38,udb.ToInt32());W(scheduler,0x468,ai.ToInt32());W(planner,0xa28,ai.ToInt32());W(planner,0xa2c,scheduler.ToInt32());W(planner,0xa70,strategic.ToInt32());W(strategic,0,1);
  W(planner,0x820,ai.ToInt32());W(ai,0xac,Mem(32).ToInt32());S(engine,0x67df20,256);S(engine,0x67df22,1);
  W(player,8,Mem(0x1320).ToInt32());W(path,0x7c,R(player,8));W(state,40,engine.ToInt32());W(state,256,engine.ToInt32());W(state,268,R(player,8));W(state,272,Mem(0x50).ToInt32());W(state,276,Code("convert").ToInt32());D(new IntPtr(R(state,272)),8,1);
  // Concrete ownership/call ABI targets are controlled fixture inputs.
  foreach(string x in new string[]{"B2Host","H3Host"})Dependency(x,x=="B2Host"?"host":"h3host");
  foreach(string x in new string[]{"GetContinent","GetThreat","CanBuild","SchedulerUpdate","GroundBuild"})Dependency(x,x=="GetContinent"?"continent":x=="GetThreat"?"threat":x=="CanBuild"?"canbuild":x=="SchedulerUpdate"?"scheduler":"ground");
  Jump(A(engine,0x103f00),Code("convert"));Jump(A(engine,0x660f0),Code("stringlookup"));Jump(A(engine,0x543b0),Code("typelookup"));Jump(A(engine,0x1866e0),Code("free"));
  foreach(int off in new int[]{0x2c,0x34})Slot(0x344660,off,"true12");Slot(0x344660,0x14,"playerconvert");Slot(0x344660,0xc,"currentpos");Slot(0x3452e0,0x54,"owner");Slot(0x3452e0,0x78,"presence");Slot(0x3452e0,0xa8,"terrain");Slot(0x346220,0xc,"path");
  Slot(0x345098,0xc,"interfacecount");Slot(0x345098,0x14,"true8");Slot(0x345098,0x40,"category");Slot(0x345098,0x44,"false8");Slot(0x345098,0x48,"false8");Slot(0x345098,0xdc,"true8");Slot(0x345098,0xd8,"trait");
  // bind_host pins these three slot target addresses; put controlled stubs at
  // its frozen target locations too, while retaining actual B4 guard checks.
  Jump(A(engine,0x133880),Code("owner"));W(engine,0x3452e0+0x54,A(engine,0x133880).ToInt32());Jump(A(engine,0x1273a0),Code("currentpos"));W(engine,0x344660+0xc,A(engine,0x1273a0).ToInt32());Jump(A(engine,0x1826a0),Code("path"));W(engine,0x346220+0xc,A(engine,0x1826a0).ToInt32());
  IntPtr nativeDB=Mem(16);W(nativeDB,0,4);W(nativeDB,8,Mem(4*0x2c8).ToInt32());W(engine,0x67dd18,nativeDB.ToInt32());W(engine,0x67dcfc,Mem(16).ToInt32());W(state,52,3);W(state,56,1);W(state,60,1);W(state,84,1);W(state,400,1);
  W(state,0,-1);W(state,20,1);W(state,44,0);W(state,48,1);W(image,0xc6fdc,Mem(16).ToInt32());IntPtr grid=new IntPtr(R(image,0xc6fdc));W(grid,0,Mem(32).ToInt32());W(grid,4,1);W(grid,8,256);
  ResetPlan();
 }
 static void ProducerInputs(){
  IntPtr grid=Mem(32),za=Mem(4),xa=Mem(256*4),terrainDB=Mem(12),records=Mem(24*192),bonus=Mem(8),types=Mem(256*4),food=Mem(256*4);
  W(state,260,grid.ToInt32());W(state,264,terrainDB.ToInt32());W(grid,0x1c,za.ToInt32());W(za,0,xa.ToInt32());W(terrainDB,0,24);W(terrainDB,8,records.ToInt32());W(bonus,0,7);W(A(records,192),0x50,bonus.ToInt32());W(state,512,types.ToInt32());W(state,516,food.ToInt32());
  for(int i=0;i<24;i++){W(A(records,i*192),0xb0,i);W(A(records,i*192),8,i==1?5:i==4?40:0);}
  for(int x=0;x<256;x++){int type=(x%8>=1&&x%8<=3)?8:x%8==4?4:1;IntPtr cell=Mem(32),yy=Mem(4);Marshal.WriteByte(cell,13,(byte)type);W(yy,0,cell.ToInt32());W(xa,4*x,yy.ToInt32());W(types,4*x,type);W(food,4*x,type==1?5:type==4?40:0);}
  Slot(0x3452e0,0x28,"true8");Slot(0x3452e0,0xac,"h3open");Slot(0x3452e0,0x168,"score");Slot(0x3452e0,0xa8,"gridterrain");Slot(0x3452e0,0xb8,"gridfood");
  Patch(A(engine,0x133880),5);Jump(A(engine,0x133880),Code("pointowner"));W(state,316,-1);
  // Current members; original native getter bodies remain intact.
  W(city,0x210,center.ToInt32());W(city,0x1f0,-1);W(city,0x1f4,1);IntPtr cityNode=Node(2,20,city),armyNode=Node(1,10,army);W(ai,0x8c,Set(cityNode).ToInt32());W(ai,0x90,Set(armyNode).ToInt32());S(army,0x48,1);S(army,0x4a,1);W(army,0x64,center.ToInt32());D(army,0x70,16);W(state,72,0);W(state,76,0);
  // B2 current symbol reads are real composed helpers; only GetSymbol provider
  // receives explicit fixture-owned FLI records.
  IntPtr fli=Mem(24),complete=Mem(0xe0),required=Mem(0xe0);W(fli,0,complete.ToInt32());W(fli,4,required.ToInt32());W(complete,0xc2,4);W(required,0xc2,4);W(ai,0xc4,fli.ToInt32());
  byte[] sym=File.ReadAllBytes(Path.Combine(root,"PROEVEN","opening-b2","helper","GetSymbol.bin"));IntPtr symbolCode=Mem(sym.Length);Marshal.Copy(sym,0,symbolCode,sym.Length);RX(symbolCode,sym.Length);Jump(A(image,0x389e0),symbolCode);
  // Real native Choose and Desired consume fixture lists and priorityarrays.
  labels["CityCount"]=0x81710;Dependency("CityCount","citycount");W(state,404,1);
  IntPtr classes=Mem(4*16),container=Mem(4);W(container,0,classes.ToInt32());W(planner,0x20+0x7b0,4);W(planner,0x20+0x7bc,container.ToInt32());
  for(int i=0;i<4;i++){IntPtr list=Mem(32),entry=Mem(16);W(list,0,entry.ToInt32());W(list,4,1);D(entry,0,i==1?2:-2);W(entry,8,i==1?2:1);W(classes,16*i+12,list.ToInt32());D(classes,16*i,100-i);}
  IntPtr desired=Mem(24),dp=Mem(4),priorities=Mem(12),pp=Mem(4),actual=Mem(12),ap=Mem(4);W(dp,0,desired.ToInt32());W(pp,0,priorities.ToInt32());W(ap,0,actual.ToInt32());W(planner,0x20+0x7c0,dp.ToInt32());W(planner,0x20+0x7c4,pp.ToInt32());W(planner,0x20+0x7c8,ap.ToInt32());
  for(int t=0;t<3;t++){IntPtr priority=Mem(40);W(priority,8,64);W(priority,24,Mem(64*8).ToInt32());W(priority,32,Mem(64*8).ToInt32());W(priorities,4*t,priority.ToInt32());}
  W(state,92,Mem(3*8).ToInt32());W(state,96,2);W(state,100,2);W(state,88,1);
 }
 static void Capture(int count){IntPtr map=new IntPtr(R(ai,0x80)),heap=Mem((count+1)*4);W(map,0x5c,count+1);W(map,0x60,count+1);W(map,0x64,heap.ToInt32());for(int i=0;i<count;i++){IntPtr p=Mem(8);S(p,0,(i+1)*8);W(heap,4*(i+1),p.ToInt32());}}
 static void TypesAndDepartures(){
  ResetPlan();Test("loaded exact token and actual interface count",Call("resolve_type",0,true,plan.ToInt32())==1&&R(plan,44)==1&&R(plan,48)==3);
  W(state,60,0);ResetPlan();Test("absent loaded token UNKNOWN",Call("resolve_type",0,true,plan.ToInt32())==0&&R(plan,0)==0);W(state,60,1);
  W(state,56,3);int before=R(state,292);ResetPlan();Test("trailing noninterface type rejected before trait",Call("resolve_type",0,true,plan.ToInt32())==0&&R(state,292)==before);W(state,56,1);
  ResetPlan();Test("full class preview incl nonsettler",Call("preview_scope",0,false,plan.ToInt32())==1&&R(plan,72)==4);
  W(state,64,1);ResetPlan();Test("other selected settlertype wholepass UNKNOWN",Call("preview_scope",0,false,plan.ToInt32())==0&&R(plan,0)==0);W(state,64,0);
  ResetPlan();IntPtr aset=new IntPtr(R(ai,0x90));byte[] saved=Read(aset,32);Test("ordinary movement16 departure using original getters",Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1)==1&&R(plan,76)==1&&R(plan,88)==1);Test("shared BSet iterator untouched",Same(saved,Read(aset,32)));
  foreach(int count in new int[]{0,2}){ResetPlan();S(army,0x48,count);Test("valid count outside ordinary "+count,Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1)==1&&R(plan,76)==0);}S(army,0x48,1);
  foreach(double movement in new double[]{15.999,Double.NaN,Double.PositiveInfinity}){ResetPlan();D(army,0x70,movement);int got=Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1);Test("movement branch "+movement,Double.IsNaN(movement)||Double.IsInfinity(movement)?got==0&&R(plan,0)==0:got==1&&R(plan,76)==0);}D(army,0x70,16);
  foreach(int flag in new int[]{8,16}){ResetPlan();Marshal.WriteByte(army,0x88,(byte)flag);Test("special movement skip "+flag,Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1)==1&&R(plan,76)==0);}Marshal.WriteByte(army,0x88,0);
  IntPtr cargo=Mem(16);W(army,0x60,cargo.ToInt32());W(cargo,8,unchecked((int)0x7fff0000));ResetPlan();Test("cargo signed16 zero accepted despite adjacentword",Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1)==1&&R(plan,76)==1);S(cargo,8,-1);ResetPlan();Test("negative cargo UNKNOWN",Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1)==0);W(army,0x60,0);
  W(state,72,1);ResetPlan();Test("engine position mismatch UNKNOWN",Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1)==0);W(state,72,0);W(state,80,1);ResetPlan();Test("engine currentID invalid UNKNOWN",Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1)==0);W(state,80,0);
  IntPtr node=new IntPtr(R(aset,8));W(node,4,node.ToInt32());ResetPlan();Test("cyclic DFS UNKNOWN",Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1)==0);W(node,4,0);
  W(army,12,11);ResetPlan();Test("fresh ID mismatch UNKNOWN",Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1)==0);W(army,12,10);
  W(city,0x1f0,1);ResetPlan();Test("cityfront production one copied claim",Call("read_set",0,false,plan.ToInt32(),R(ai,0x8c),2)==1&&R(plan,52)==1&&R(plan,76)==1&&R(plan,0x18204)==3);W(city,0x1f4,0);ResetPlan();Test("front nonarmy category no production claim",Call("read_set",0,false,plan.ToInt32(),R(ai,0x8c),2)==1&&R(plan,0x18204)==2);W(city,0x1f4,1);W(city,0x1f0,-1);
  ResetPlan();IntPtr empty=Set(IntPtr.Zero);Test("empty DFS complete",Call("read_set",0,true,plan.ToInt32(),empty.ToInt32(),1)==1&&R(plan,92)==0);
  IntPtr na=Mem(0x100),nb=Mem(0x100);S(na,0x48,0);S(nb,0x48,0);IntPtr left=Node(1,11,na),right=Node(1,12,nb);W(node,4,left.ToInt32());W(node,8,right.ToInt32());ResetPlan();Test("read-only DFS both children complete",Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1)==1&&R(plan,92)==3);W(nb,12,11);W(right,0,11);ResetPlan();Test("duplicate namespace ID UNKNOWN",Call("read_set",0,false,plan.ToInt32(),aset.ToInt32(),1)==0);W(node,4,0);W(node,8,0);
  W(army,4,2);ResetPlan();Test("kind mismatch UNKNOWN",Call("read_set",0,true,plan.ToInt32(),aset.ToInt32(),1)==0);W(army,4,1);S(army,0x48,-1);ResetPlan();Test("negative unitcount UNKNOWN",Call("read_set",0,true,plan.ToInt32(),aset.ToInt32(),1)==0);S(army,0x48,1);
  W(army,0x40,1);ResetPlan();Test("nonordinary state skip",Call("read_set",0,true,plan.ToInt32(),aset.ToInt32(),1)==1&&R(plan,76)==0);W(army,0x40,0);
  // Isolate the combined4096-node traversal bound with valid count0 armies,
  // so no earlier32-departure bound conceals it.
  IntPtr chain=IntPtr.Zero;for(int i=0;i<4097;i++){IntPtr aa=Mem(0x100),nn=Node(1,10000+i,aa);W(nn,8,chain.ToInt32());chain=nn;}IntPtr large=Set(chain);ResetPlan();Test("DFS4097 wholepassUNKNOWN after4096complete reads",Call("read_set",0,true,plan.ToInt32(),large.ToInt32(),1)==0&&R(plan,92)==4096&&R(plan,0)==0);
  chain=IntPtr.Zero;for(int i=0;i<33;i++){IntPtr aa=Mem(0x100);S(aa,0x48,1);S(aa,0x4a,1);W(aa,0x64,center.ToInt32());D(aa,0x70,16);IntPtr nn=Node(1,20000+i,aa);W(nn,8,chain.ToInt32());chain=nn;}ResetPlan();Test("departure33 UNKNOWN at32queries no partial stock",Call("read_set",0,false,plan.ToInt32(),Set(chain).ToInt32(),1)==0&&R(plan,88)==32&&R(plan,76)==32&&R(plan,0)==0);
 }
 static void PathsAndProducer(){
  ResetPlan();S(center,0,0);IntPtr destination=Mem(8);S(destination,0,8);W(state,108,0);
  Test("actual path20 positive with source/destination safety",Call("direct_path",0,false,plan.ToInt32(),center.ToInt32(),destination.ToInt32())==1&&R(state,108)==1&&R(state,112)==R(state,92));
  int[] constants={path.ToInt32(),0,0,1,1,center.ToInt32(),destination.ToInt32(),0,0,0,0,0,1,0,0,4096,0,1,0,1};
  for(int i=0;i<20;i++)if(i<7||i==11||i>=12&&i!=16)Check(R(state,128+4*i)==constants[i],"path ABI slot"+(i+1));
  Test("path20 exact constants and pointers",R(state,128+20)==center.ToInt32()&&R(state,128+24)==destination.ToInt32());
  foreach(int raw in new int[]{0,7,-2,255}){ResetPlan();W(state,316,8);W(state,320,raw);int frees=R(state,108);int got=Call("direct_path",0,false,plan.ToInt32(),center.ToInt32(),destination.ToInt32());Test("destination owner pathfree "+raw,got==(raw>=0&&raw<=31?2:0)&&R(state,108)==frees+1);}W(state,316,-1);
  ResetPlan();W(state,88,0);int f=R(state,108);Test("native pathfailure nonnull buffer freed once UNKNOWN",Call("direct_path",0,false,plan.ToInt32(),center.ToInt32(),destination.ToInt32())==0&&R(state,108)==f+1);W(state,88,1);
  ResetPlan();W(plan,84,128);f=R(state,108);Test("path budget wholepass UNKNOWN without query",Call("direct_path",0,false,plan.ToInt32(),center.ToInt32(),destination.ToInt32())==0&&R(state,108)==f);
  ResetPlan();Capture(6);Test("real capture six canonical candidates",Call("capture_heap",0,true,plan.ToInt32())==1&&R(plan,68)==6);
  int gotFinal=Call("finalize_pass",0,false,plan.ToInt32());Test("true emitted producer H3-current positive G6",gotFinal==1&&R(plan,0)==4&&R(plan,60)==6&&R(plan,80)==6&&R(plan,76)==2&&R(plan,52)==1&&R(plan,88)==1);
  Test("claims once and reused city newbuild origins",R(plan,0x18200+16)==-1&&R(plan,0x18200+32+16)==0);
  W(state,100,3);W(state,96,3);IntPtr middle=A(new IntPtr(R(state,92)),8);S(middle,0,4);W(state,316,4);W(state,320,-2);ResetPlan();f=R(state,108);Test("UNKNOWN midpath freeonce wholepass",Call("direct_path",0,false,plan.ToInt32(),center.ToInt32(),destination.ToInt32())==0&&R(plan,0)==0&&R(state,108)==f+1);W(state,316,-1);W(state,100,2);W(state,96,2);
  foreach(int malformed in new int[]{0,4097}){W(state,100,malformed);ResetPlan();f=R(state,108);Test("invalid pathcount UNKNOWN/free "+malformed,Call("direct_path",0,false,plan.ToInt32(),center.ToInt32(),destination.ToInt32())==0&&R(state,108)==f+1);}W(state,100,2);
  W(state,324,1);ResetPlan();f=R(state,108);Test("native global cutoff UNKNOWN/free",Call("direct_path",0,false,plan.ToInt32(),center.ToInt32(),destination.ToInt32())==0&&R(state,108)==f+1);W(state,324,0);W(engine,0x6d0b94,0);
  W(state,100,1);W(state,96,1);ResetPlan();Test("ordinary arrival onepoint path to same position",Call("direct_path",0,false,plan.ToInt32(),destination.ToInt32(),destination.ToInt32())==1);W(state,100,2);W(state,96,2);
  ResetPlan();S(center,0,8);W(state,72,8);Test("arrived ordinary army fresh currentposition claim",Call("read_departure",0,false,plan.ToInt32(),1,army.ToInt32())==1&&R(plan,76)==1&&R(plan,88)==1&&R(plan,0x18208)==8);S(center,0,0);W(state,72,0);
  // Canonical duplicates are copied once; cap never becomes partial G.
  ResetPlan();Capture(2);IntPtr map=new IntPtr(R(ai,0x80)),heap=new IntPtr(R(map,0x64));IntPtr second=new IntPtr(R(heap,8));S(second,0,8);Test("duplicate centers canonical capture once",Call("capture_heap",0,true,plan.ToInt32())==1&&R(plan,68)==1);
  ResetPlan();Capture(65);map=new IntPtr(R(ai,0x80));heap=new IntPtr(R(map,0x64));for(int i=0;i<65;i++)S(new IntPtr(R(heap,4*(i+1))),0,i);Call("capture_heap",0,true,plan.ToInt32());Test("H3query cutoff wholepass not partialD",Call("finalize_pass",0,false,plan.ToInt32())==0&&R(plan,0)==0&&R(plan,128)==64);
  // Fully traversed registered CityIDs are the actual C for min(G,N-C).
  IntPtr oldCities=new IntPtr(R(ai,0x8c));int n=fixtureN;
  foreach(int cityCount in new int[]{n-2,n}){IntPtr next=IntPtr.Zero;for(int i=0;i<cityCount;i++){IntPtr ca=Mem(0x230);W(ca,0x210,center.ToInt32());W(ca,0x1f0,-1);IntPtr cn=Node(2,100+i,ca);W(cn,8,next.ToInt32());next=cn;}W(ai,0x8c,Set(next).ToInt32());ResetPlan();Capture(6);Call("capture_heap",0,true,plan.ToInt32());Test("N-C exact registered cities "+cityCount,Call("finalize_pass",0,false,plan.ToInt32())==1&&R(plan,52)==cityCount&&R(plan,60)==n-cityCount);}W(ai,0x8c,oldCities.ToInt32());
 }
 static IntPtr Aip(){return A(planner,0x20);}
 static IntPtr DesiredArray(){return new IntPtr(R(new IntPtr(R(Aip(),0x7c0)),0));}
 static IntPtr ActualArray(){return new IntPtr(R(new IntPtr(R(Aip(),0x7c8)),0));}
 static IntPtr Priority(int t){return new IntPtr(R(new IntPtr(R(new IntPtr(R(Aip(),0x7c4)),0)),t*4));}
 static void Wrappers(){
  // Actual AIP::Update, Update_Actual_Units, Choose_Unit_From_List and
  // Update_Desired_Units bodies execute unchanged. The unrelated goal/queue/
  // building mutation callees are excluded at their dependency entries.
  foreach(int off in new int[]{0x654c0,0x65cc0,0x668e0})Jump(A(image,off),Code("noop"));
  labels["Actual"]=0x655f0;
  W(city,0x1f0,1);W(city,0x1f4,1);ResetPlan();Call("Actual",Aip().ToInt32(),false);
  Test("actual loadedtype counts army and current city production",R(ActualArray(),4)==2);
  Capture(6);Clear(plan,0x54800);int starts=R(state,408),grounds=R(state,412);
  Test("START calls original once preserves EAX and ABI",Call("start_hook",scheduler.ToInt32(),true)==0x12345678&&R(state,408)==starts+1&&R(plan,0)==1&&R(plan,36)==0);
  Test("capture original once return and ret4",Call("capture_hook",R(ai,0x80),true,ai.ToInt32())==0x23456789&&R(state,412)==grounds+1&&R(plan,0)==2&&R(plan,68)==6);
  Call("scope_hook",Aip().ToInt32(),false);
  Test("fivehook chain G6 real desired6 priority6 nativeActual2 deficit4",BitConverter.ToDouble(Read(A(DesiredArray(),8),8),0)==6&&R(Priority(1),0)==6&&R(ActualArray(),4)==2&&R(plan,60)==6&&R(plan,64)==6&&R(plan,168)==4);
  Test("nonsettler original quota remains2 entries2",BitConverter.ToDouble(Read(A(DesiredArray(),16),8),0)==2&&R(Priority(2),0)==2);
  Test("AIPreturn invalidates pass and owner",R(plan,0)==5&&R(plan,36)==0&&R(plan,8)==0);
  // Whole-pass UNKNOWN must leave all three original settler contributions.
  W(state,60,0);Clear(plan,0x54800);Call("start_hook",scheduler.ToInt32(),true);Call("capture_hook",R(ai,0x80),true,ai.ToInt32());Call("scope_hook",Aip().ToInt32(),false);
  Test("prefreeze UNKNOWN keeps all original selected settler quotas",BitConverter.ToDouble(Read(A(DesiredArray(),8),8),0)==6&&R(Priority(1),0)==6&&R(plan,64)==0&&R(plan,168)==0&&R(plan,4)!=0);W(state,60,1);
  // Scoped D0: original Desired invokes quota wrapper for first/later classes;
  // it must produce true +0.0 and no native priorityentries.
  Capture(0);Clear(plan,0x54800);Call("start_hook",scheduler.ToInt32(),true);Call("capture_hook",R(ai,0x80),true,ai.ToInt32());Call("scope_hook",Aip().ToInt32(),false);
  Test("D0 first/later classes positivezero no entries nativeActual unchanged",Marshal.ReadInt64(DesiredArray(),8)==0&&R(Priority(1),0)==0&&R(ActualArray(),4)==2&&R(plan,60)==0&&R(plan,168)==4);
  // NativeActual includes unsupported-for-ordinary multiunit armies and is
  // never replaced by the matched-claim count or subtracted a second time.
  S(army,0x48,6);for(int i=0;i<6;i++)S(army,0x4a+2*i,1);Capture(6);Clear(plan,0x54800);Call("start_hook",scheduler.ToInt32(),true);Call("capture_hook",R(ai,0x80),true,ai.ToInt32());Call("scope_hook",Aip().ToInt32(),false);Test("enough nativeActual7 retains desired6 andentries6 no claim doubleaftrek",R(ActualArray(),4)==7&&BitConverter.ToDouble(Read(A(DesiredArray(),8),8),0)==6&&R(Priority(1),0)==6&&R(plan,76)==1);S(army,0x48,1);
  W(state,316,16);W(state,320,-2);Capture(6);Clear(plan,0x54800);Call("start_hook",scheduler.ToInt32(),true);Call("capture_hook",R(ai,0x80),true,ai.ToInt32());Call("scope_hook",Aip().ToInt32(),false);Test("UNKNOWN after partial G1 leaks no managed quota",R(plan,60)==1&&R(plan,64)==0&&BitConverter.ToDouble(Read(A(DesiredArray(),8),8),0)==6&&R(Priority(1),0)==6);W(state,316,-1);
  Clear(plan,0x54800);Call("start_hook",scheduler.ToInt32(),true);Call("scope_hook",Aip().ToInt32(),false);Test("missing capture wholepass original",R(plan,64)==0&&BitConverter.ToDouble(Read(A(DesiredArray(),8),8),0)==6);
  ResetPlan();W(plan,36,0);Test("finalize outside AIPscope rejected",Call("finalize_pass",0,true,plan.ToInt32())==0&&R(plan,0)==0);
  IntPtr registration=AddVectoredExceptionHandler(1,handler);Check(registration!=IntPtr.Zero,"own exception audit");try{
   ResetPlan();int traps=R(state,336);Test("reentrant START actual UD2 candidate rejection",Call("start_hook",scheduler.ToInt32(),false)==-1&&R(state,336)==traps+1&&R(state,344)==Entry("contract_error").ToInt32());
   ResetPlan();W(plan,0,4);Call("preview_scope",0,false,plan.ToInt32());IntPtr list=new IntPtr(R(plan,0x8200)),selected=Mem(4);W(list,4,0);traps=R(state,336);Test("immutable previewmismatch actual UD2 rejection",Call("quota_hook",Aip().ToInt32(),false,list.ToInt32(),selected.ToInt32())==-1&&R(state,336)==traps+1);W(list,4,1);
  }finally{RemoveVectoredExceptionHandler(registration);GC.KeepAlive(handler);}
 }
 static void ResetPlan(){Clear(plan,0x54800);W(plan,0,2);W(plan,8,ai.ToInt32());W(plan,12,2);W(plan,16,R(ai,0x80));W(plan,20,planner.ToInt32());W(plan,24,A(planner,0x20).ToInt32());W(plan,28,scheduler.ToInt32());W(plan,32,1);W(plan,36,1);W(plan,44,1);W(plan,48,3);W(plan,100,engine.ToInt32());W(plan,104,udb.ToInt32());W(plan,108,player.ToInt32());W(plan,112,world.ToInt32());W(plan,116,path.ToInt32());W(plan,144,engine.ToInt32());}
 static int fixtureN;
 public static Dictionary<string,object> Run(string project,string package,string file,int[] offsets,string[] names,int size,bool expectSafetyBug){
  root=project;pack=package;fixtureN=file.Contains("N30")?30:25;labels=new Dictionary<string,int>();for(int i=0;i<names.Length;i++)labels[names[i]]=offsets[i];imageSize=size;cases=0;passed.Clear();Check(IntPtr.Size==4,"32-bit helper");SetErrorMode(0x8003);IntPtr mapped=IntPtr.Zero;try{
   mapped=LoadLibraryW(file);Check(mapped!=IntPtr.Zero,"ordinary DLL loader "+Marshal.GetLastWin32Error());byte[] b=Read(mapped,imageSize);image=Mem(imageSize);Marshal.Copy(b,0,image,imageSize);
   // Apply exact PE base relocations to the self-owned complete mapped copy.
   int nt=R(image,0x3c),rel=R(image,nt+0xa0),length=R(image,nt+0xa4),end=rel+length;
   for(int at=rel;at<end;){int page=R(image,at),block=R(image,at+4);Check(block>=8&&at+block<=end,"reloc block");for(int k=at+8;k<at+block;k+=2){int e=(ushort)Marshal.ReadInt16(image,k);if((e>>12)==3){int dst=page+(e&4095);W(image,dst,R(image,dst)+image.ToInt32()-mapped.ToInt32());}else Check((e>>12)==0,"reloc type");}at+=block;}
   int[] originalBodyStarts={0x655f0,0x65900,0x659a0,0x66b70},originalBodySizes={0x2d0,0xa0,0x320,0x30};byte[][] originalBodies=new byte[4][];for(int j=0;j<4;j++)originalBodies[j]=Read(A(image,originalBodyStarts[j]),originalBodySizes[j]);byte[] h3Core=Read(A(image,0xd4000),labels["H3Host"]-0xd4000);
   Setup();RX(image,labels["pass_state"]);byte[] b4Before=Read(Entry("bind_host"),labels["settler_name"]-labels["bind_host"]+13);
   int result=Call("safe_point",0,false,plan.ToInt32(),center.ToInt32());
   bool correct=R(state,4)==center.ToInt32()&&R(state,8)==center.ToInt32()&&R(state,12)==R(center,0)&&R(state,16)==R(center,4);
   if(expectSafetyBug){Test("old emission passes wrong position to World78 and Player14",!correct);return new Dictionary<string,object>{{"cases",cases},{"old_emission_rejected",true},{"expected_position",center.ToInt32()},{"World78_position",R(state,4)},{"Player14_position",R(state,8)},{"result",result},{"pass",true},{"gameplay_measured",false}};}
   Test("World78 and Player14 exact externalpointer and xyz",correct&&result==1);
   foreach(int raw in new int[]{2,-1,0,7,-2,255}){ResetPlan();W(state,0,raw);int got=Call("safe_point",0,false,plan.ToInt32(),center.ToInt32());Test("safe owner fullsigned "+raw,got==((raw==2||raw==-1)?1:(raw>=0&&raw<=31)?2:0));}
   W(state,0,-1);ResetPlan();D(state,32,1);Test("positive threat rejects",Call("safe_point",0,false,plan.ToInt32(),center.ToInt32())==2);D(state,32,Double.NaN);ResetPlan();Test("nonfinite threat wholepassUNKNOWN",Call("safe_point",0,false,plan.ToInt32(),center.ToInt32())==0&&R(plan,0)==0);D(state,32,0);
   // Controlled producer input construction retains real emitted H3 role and
   // B4 producer bodies. No scalar G provider or mocked producer is introduced.
   ProducerInputs();TypesAndDepartures();PathsAndProducer();Wrappers();
   Test("B4 actual emitted body unchanged in fixture",Same(b4Before,Read(Entry("bind_host"),b4Before.Length)));
   for(int j=0;j<4;j++)Test("original body retained from mapped candidate "+originalBodyStarts[j].ToString("x"),Same(originalBodies[j],Read(A(image,originalBodyStarts[j]),originalBodySizes[j])));Test("H3core classifier/currentmodel/roles intact",Same(h3Core,Read(A(image,0xd4000),h3Core.Length)));
   return new Dictionary<string,object>{{"cases",cases},{"checks",passed.ToArray()},{"fixture_only",true},{"B4_body_unchanged",true},{"full_producer_acceptance",false},{"gameplay_measured",false},{"pass",true}};
  }finally{foreach(IntPtr p in owned)VirtualFree(p,UIntPtr.Zero,0x8000);owned.Clear();if(mapped!=IntPtr.Zero)FreeLibrary(mapped);}
 }
}
