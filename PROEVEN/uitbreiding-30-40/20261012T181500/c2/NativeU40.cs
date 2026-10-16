// Native execution of actual B4 composition in a separate owned fixture copy.
// Changed dependency addresses provide controlled inputs; B4/H3 model intact.
using System;using System.IO;using System.Runtime.InteropServices;using System.Collections.Generic;using System.Text.RegularExpressions;
public static class U40Producer {
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


 static IntPtr Aip(){return A(planner,0x20);}
 static IntPtr DesiredArray(){return new IntPtr(R(new IntPtr(R(Aip(),0x7c0)),0));}
 static IntPtr ActualArray(){return new IntPtr(R(new IntPtr(R(Aip(),0x7c8)),0));}
 static IntPtr Priority(int t){return new IntPtr(R(new IntPtr(R(new IntPtr(R(Aip(),0x7c4)),0)),t*4));}

 static void ResetPlan(){Clear(plan,0x54800);W(plan,0,2);W(plan,8,ai.ToInt32());W(plan,12,2);W(plan,16,R(ai,0x80));W(plan,20,planner.ToInt32());W(plan,24,A(planner,0x20).ToInt32());W(plan,28,scheduler.ToInt32());W(plan,32,1);W(plan,36,1);W(plan,44,1);W(plan,48,3);W(plan,100,engine.ToInt32());W(plan,104,udb.ToInt32());W(plan,108,player.ToInt32());W(plan,112,world.ToInt32());W(plan,116,path.ToInt32());W(plan,144,engine.ToInt32());}
 static int fixtureN;
 static IntPtr policyOut,nativePlayer,cityContainer,completeSymbol,goal,otherGoal;
 static void PolicyInputs(){
  nativePlayer=new IntPtr(R(player,8));W(player,12,2);IntPtr players=Mem(32*4);W(players,8,nativePlayer.ToInt32());W(engine,0x67dd80,players.ToInt32());cityContainer=Mem(16);W(nativePlayer,0x12c0,cityContainer.ToInt32());policyOut=Mem(24);completeSymbol=new IntPtr(R(new IntPtr(R(ai,0xc4)),0));
  W(state,608,cityContainer.ToInt32());W(state,612,Entry("normalize_dispatch").ToInt32());Dependency("ExecuteOriginal","execute");
  goal=Mem(0x100);W(goal,0,A(image,0x8a558).ToInt32());W(goal,12,5);Jump(A(image,0x487e0),Code("arrival"));otherGoal=Mem(0x100);IntPtr otherVT=Mem(0x100);W(otherVT,0x90,Code("arrival").ToInt32());W(otherGoal,0,otherVT.ToInt32());W(otherGoal,12,4);
  labels["normalize_caller"]=Code("normalize_caller").ToInt32()-image.ToInt32();
  // Set original stock to2 from first selected settler class, zero later
  // settlerclasses; retain nonsettler2 contribution. Original native Choose,
  // Actual and Desired still execute actual mapped candidate bodies.
  IntPtr classes=new IntPtr(R(new IntPtr(R(Aip(),0x7bc)),0));for(int i=0;i<4;i++){IntPtr entry=new IntPtr(R(new IntPtr(R(classes,16*i+12)),0));D(entry,0,i==1?2:i==0?-2:0);}
  foreach(int off in new int[]{0x654c0,0x65cc0,0x668e0})Jump(A(image,off),Code("noop"));
  PolicyState(1,0,0);
 }
 static void PolicyState(int count,int government,int completed){W(cityContainer,8,count);W(nativePlayer,0x94,government);D(completeSymbol,8,completed);W(state,404,count);}
 static void Pipeline(int candidates,bool capture){Clear(plan,0x54800);Capture(candidates);Call("start_hook",scheduler.ToInt32(),true);if(capture)Call("capture_hook",R(ai,0x80),true,ai.ToInt32());Call("scope_hook",Aip().ToInt32(),false);}
 static double Wanted(){return BitConverter.ToDouble(Read(A(DesiredArray(),8),8),0);}
 static void ChangedCases(){
  int[,] table={{29,0,0,1,1},{30,0,0,1,0},{30,3,0,1,10},{39,3,1,1,1},{40,3,1,1,0},{29,3,0,1,1},{28,3,1,1,12},{40,4,1,0,0},{41,4,1,0,0}};
  for(int i=0;i<table.GetLength(0);i++){PolicyState(table[i,0],table[i,1],table[i,2]);int got=Call("read_policy",0,true,ai.ToInt32(),policyOut.ToInt32());Test("fresh policy C/gov/completion "+table[i,0]+"/"+table[i,1]+"/"+table[i,2],got==1&&R(policyOut,0)==table[i,3]&&R(policyOut,4)==table[i,4]&&R(policyOut,8)==table[i,0]);}
  PolicyState(1,0,0);W(city,0x1f0,1);Pipeline(6,true);Test("new native coherent Dorig2 Gcert6 Actual2 desired6 priority6 deficit4",R(plan,184)==2&&R(plan,188)==6&&Wanted()==6&&R(Priority(1),0)==6&&R(ActualArray(),4)==2&&R(plan,64)==6);
  Test("nonsettler original desired2 entries2",BitConverter.ToDouble(Read(A(DesiredArray(),16),8),0)==2&&R(Priority(2),0)==2);
  Pipeline(0,true);Test("production Gcert0 incomplete union keeps Dorig2",R(plan,188)==0&&Wanted()==2&&R(Priority(1),0)==2);
  Pipeline(6,false);Test("missing capture retains Dorig2 within current R",Wanted()==2&&R(plan,188)==0&&R(plan,4)!=0);
  PolicyState(40,3,1);Pipeline(6,false);Test("Theo40 R0 precedes missingcapture fallback completion",Wanted()==0&&R(Priority(1),0)==0&&R(plan,56)==0);
  PolicyState(30,0,0);Pipeline(6,false);Test("C30 nonTheo incomplete R0",Wanted()==0);
  PolicyState(41,4,1);Pipeline(6,false);Test("completion1 later otherGov41 preserves native stock2",Wanted()==2&&R(plan,64)==0&&R(plan,192)==0);
  PolicyState(1,0,0);ResetPlan();Capture(6);Call("capture_heap",0,true,plan.ToInt32());W(plan,84,127);int frees=R(state,108);Call("finalize_pass",0,false,plan.ToInt32());Test("query cutoff retains fully certified positiveprefix1 Dorig2",R(plan,188)==1&&R(plan,60)==2&&R(plan,208)==1&&R(state,108)==frees+1);
  ResetPlan();Capture(6);Call("capture_heap",0,true,plan.ToInt32());W(state,316,16);W(state,320,-2);Call("finalize_pass",0,false,plan.ToInt32());Test("malformed owner after positive slot discards certificate preserves Dorig",R(plan,188)==0&&R(plan,60)==2&&R(plan,4)!=0);W(state,316,-1);
  ResetPlan();Capture(6);Call("capture_heap",0,true,plan.ToInt32());W(plan,204,4094);frees=R(state,108);Call("finalize_pass",0,false,plan.ToInt32());Test("4096 total point bound retains prefix and frees cutoffbuffer once",R(plan,188)==1&&R(plan,204)==4096&&R(plan,208)==1&&R(state,108)==frees+2);
  ResetPlan();IntPtr dest=Mem(8);S(dest,0,8);W(state,100,4097);frees=R(state,108);Test("path entries4097 budget suffix freeonce",Call("direct_path",0,false,plan.ToInt32(),center.ToInt32(),dest.ToInt32())==3&&R(state,108)==frees+1&&R(plan,204)==0);W(state,100,2);
  // Endpoint sources and directland model are controlled fixture inputs.
  //40 actual conflict-free certificates exercise lastSELECTEDindex39; ORDER
  // is surrounded by observed guard values after it has been populated.
  ResetPlan();W(plan,56,40);W(plan,76,1);W(plan,80,40);IntPtr source=A(plan,0x18200);W(source,0,20);W(source,4,2);W(source,8,0);W(source,12,0);W(source,16,-1);
  for(int i=0;i<40;i++){IntPtr slot=A(plan,0x40600+i*1152);S(slot,0,(i+1)*5);for(int j=0;j<5;j++){W(slot,32+8*j,1000+i*10+j);W(slot,36+8*j,0);}W(plan,0x526a0+i*4,i);}
  W(plan,0x527a0,0x11223344);Call("select_direct_plans",0,false,plan.ToInt32());Test("actual SELECTED40 and ORDER nonoverlap",R(plan,60)==40&&R(plan,0x52600+39*4)==39&&R(plan,0x526a0)==0&&R(plan,0x526a0+39*4)==39&&R(plan,0x527a0)==0x11223344);
  PolicyState(40,3,1);int starts=R(state,600);Test("entry C40 returns0 no native execute",Call("execute_gate",goal.ToInt32(),true,ai.ToInt32(),0)==0&&R(state,600)==starts);
  PolicyState(39,3,1);Test("entry C39 calls original exactlyonce",Call("execute_gate",goal.ToInt32(),true,ai.ToInt32(),0)==7&&R(state,600)==starts+1);
  // Host callback simulates synchronous city registration. This proves gate
  // reread and no marking ondenial, never actual enginecitycreation.
  W(goal,0x1c,0);int arrivals=R(state,604);Test("arrival39 allowed callback registers40",Call("arrival_dispatch",goal.ToInt32(),true,ai.ToInt32(),0,0,0)==1&&R(cityContainer,8)==40&&R(state,604)==arrivals+1&&R(goal,0x1c)==1);W(goal,0x1c,0);
  Test("second serialarrival40 denied before marker",Call("arrival_dispatch",goal.ToInt32(),true,ai.ToInt32(),0,0,0)==-1&&R(cityContainer,8)==40&&R(state,604)==arrivals+1&&R(goal,0x1c)==0);
  Test("denial sentinel normalizes0 inherited EBP+[20]",Call("normalize_caller",0,true,-1,goal.ToInt32(),ai.ToInt32(),0)==0);
  Test("native false0 stays transport2",Call("normalize_caller",0,true,0,goal.ToInt32(),ai.ToInt32(),0)==2);
  Test("native true1 stays3",Call("normalize_caller",0,true,1,goal.ToInt32(),ai.ToInt32(),0)==3);
  foreach(int subtask in new int[]{1,2}){Test("other subtask sentinel uses native bool3 "+subtask,Call("normalize_caller",0,true,-1,goal.ToInt32(),ai.ToInt32(),subtask)==3);int before=R(state,604);Test("other subtask originalarrival once "+subtask,Call("arrival_dispatch",goal.ToInt32(),true,ai.ToInt32(),0,0,subtask)==1&&R(state,604)==before+1);}
  Test("nonsettle sentinel preserves native bool3",Call("normalize_caller",0,true,-1,otherGoal.ToInt32(),ai.ToInt32(),0)==3);int old=R(state,604);Test("nonsettle native arrival unchanged",Call("arrival_dispatch",otherGoal.ToInt32(),true,ai.ToInt32(),0,0,0)==1&&R(state,604)==old+1);
  foreach(int c in new int[]{40,41}){PolicyState(c,4,1);old=R(state,600);Test("completion1 otherGov native execute C"+c,Call("execute_gate",goal.ToInt32(),true,ai.ToInt32(),0)==7&&R(state,600)==old+1);old=R(state,604);Test("completion1 otherGov native arrival C"+c,Call("arrival_dispatch",goal.ToInt32(),true,ai.ToInt32(),0,0,0)==1&&R(state,604)==old+1);}
  PolicyState(39,3,1);Call("execute_gate",goal.ToInt32(),true,ai.ToInt32(),0);PolicyState(40,3,1);W(goal,0x1c,0);Test("freshcount changed betweenentry/arrival denies",Call("arrival_dispatch",goal.ToInt32(),true,ai.ToInt32(),0,0,0)==-1&&R(goal,0x1c)==0);
  PolicyState(39,3,1);Call("execute_gate",goal.ToInt32(),true,ai.ToInt32(),0);PolicyState(41,4,1);Test("freshgovernment changes entry/arrival permits native",Call("arrival_dispatch",goal.ToInt32(),true,ai.ToInt32(),0,0,0)==1);
  // One finite integrated real GotoTaskSolution -> FollowPathToTask -> own
  // arrivaldispatch -> own normalizer path. Only FindPath/WithinRange/Army
  // inCity/transport predicates are controlled callbacks. Native Execute
  // aggregate and complete Scheduler frame are NOT executed by this case.
  IntegratedChain();
 }
 static void IntegratedChain(){
  W(state,616,A(image,0x44a70).ToInt32());W(state,620,ai.ToInt32());W(state,624,army.ToInt32());W(state,628,center.ToInt32());
  labels["goto_caller"]=Code("goto_caller").ToInt32()-image.ToInt32();Jump(A(image,0x11f10),Code("false8"));Jump(A(image,0x76940),Code("true4"));Patch(A(image,0x8a558+0x84),8);W(image,0x8a558+0x84,Code("true24").ToInt32());W(image,0x8a558+0x88,Code("true12").ToInt32());W(goal,0x34,Mem(0x80).ToInt32());
  PolicyState(40,3,1);W(goal,0x1c,0);int old=R(state,604);Test("actual Goto Follow arrivaldenial normalizer chain returns0 beforemark",Call("goto_caller",goal.ToInt32(),true)==0&&R(goal,0x1c)==0&&R(state,604)==old);
 }

 public static Dictionary<string,object> Run(string project,string package,string file,int[] offsets,string[] names,int size,bool expectSafetyBug){
  root=project;pack=package;fixtureN=file.Contains("N30")?30:25;labels=new Dictionary<string,int>();for(int i=0;i<names.Length;i++)labels[names[i]]=offsets[i];imageSize=size;cases=0;passed.Clear();Check(IntPtr.Size==4,"32-bit helper");SetErrorMode(0x8003);IntPtr mapped=IntPtr.Zero;try{
   mapped=LoadLibraryW(file);Check(mapped!=IntPtr.Zero,"ordinary DLL loader "+Marshal.GetLastWin32Error());byte[] b=Read(mapped,imageSize);image=Mem(imageSize);Marshal.Copy(b,0,image,imageSize);
   // Apply exact PE base relocations to the self-owned complete mapped copy.
   int nt=R(image,0x3c),rel=R(image,nt+0xa0),length=R(image,nt+0xa4),end=rel+length;
   for(int at=rel;at<end;){int page=R(image,at),block=R(image,at+4);Check(block>=8&&at+block<=end,"reloc block");for(int k=at+8;k<at+block;k+=2){int e=(ushort)Marshal.ReadInt16(image,k);if((e>>12)==3){int dst=page+(e&4095);W(image,dst,R(image,dst)+image.ToInt32()-mapped.ToInt32());}else Check((e>>12)==0,"reloc type");}at+=block;}
   int loadedExecute=R(mapped,0x8a598),copiedExecute=R(image,0x8a598);
   Test("actual mapped HIGHLOWslot execute bound",loadedExecute==A(mapped,labels["execute_gate"]).ToInt32());
   Test("own full mappedcopy relocated HIGHLOWslot execute bound",copiedExecute==Entry("execute_gate").ToInt32()&&image!=mapped);
   byte[] disk=File.ReadAllBytes(file);int b2size=File.ReadAllBytes(Path.Combine(root,"PROEVEN","opening-b2","B2a-N30-TECHNICAL.payload.bin")).Length;
   byte[] b2expected=File.ReadAllBytes(Path.Combine(root,"PROEVEN","opening-b2","B2a-N30-TECHNICAL.payload.bin"));
   Test("actual loader B2payload byteexact",Same(b2expected,Read(A(mapped,0xd4000),b2size))&&Same(b2expected,Read(A(image,0xd4000),b2size)));
   foreach(int rva in new int[]{0x413da,0x3625b,0xfe2d,0xfe51,0x61f0}){byte[] expected=new byte[5];Array.Copy(disk,rva-0xc00,expected,0,5);Test("actual loader B2hook exact "+rva.ToString("x"),Same(expected,Read(A(mapped,rva),5))&&Same(expected,Read(A(image,rva),5)));}
   Setup();ProducerInputs();PolicyInputs();RX(image,labels["pass_state"]);Dependency("bind_inputs","true4");
   byte[] ownBefore=Read(Entry("read_policy"),labels["settler_name"]-labels["read_policy"]+13);
   IntegratedChain();
   Test("all actual changed emitted functions byte-intact",Same(ownBefore,Read(Entry("read_policy"),ownBefore.Length)));
   return new Dictionary<string,object>{{"native_calls",cases},{"checks",passed.ToArray()},{"mapped_base",mapped.ToInt32()},{"own_copy_base",image.ToInt32()},{"mapped_execute_slot",loadedExecute},{"copy_execute_slot",copiedExecute},{"normal_LoadLibrary_and_fullcopy_HIGHLOW_rebase",true},{"fixture_only",true},{"controlled_callbacks_not_engine",true},{"old109cases_executed",false},{"actual_changed_source_byte_intact",true},{"gameplay_measured",false},{"pass",true}};
  }finally{foreach(IntPtr p in owned)VirtualFree(p,UIntPtr.Zero,0x8000);owned.Clear();if(mapped!=IntPtr.Zero)FreeLibrary(mapped);}
 }
}
