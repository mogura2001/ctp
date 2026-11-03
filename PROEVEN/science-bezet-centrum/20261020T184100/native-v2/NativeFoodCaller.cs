// SOURCE ONLY. Existing finite H3/B4 own-image, shim5 and data-stub method.
// No LoadLibrary, engine process, RPM, installation, game or GUI API.
using System;using System.IO;using System.Text;using System.Text.RegularExpressions;
using System.Collections.Generic;using System.Runtime.InteropServices;using System.Security.Cryptography;
public static class NativeFoodCaller {
 [DllImport("kernel32.dll",SetLastError=true)]static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint t,uint f);
 [DllImport("kernel32.dll")]static extern bool VirtualFree(IntPtr p,UIntPtr n,uint t);
 [DllImport("kernel32.dll")]static extern bool VirtualProtect(IntPtr p,UIntPtr n,uint f,out uint old);
 [DllImport("kernel32.dll")]static extern bool FlushInstructionCache(IntPtr process,IntPtr address,UIntPtr size);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)]delegate void Shim();
 static readonly List<IntPtr> owned=new List<IntPtr>();static readonly List<string> passes=new List<string>();
 static Dictionary<string,int> labels;static string root,pack;static IntPtr image,plan,ctx,shimctx,stage,world,stubstate,engine,grid,zarray,xarray,yarray,cell,db,records,good,bonus,output,normal,army,modelOutput,modelProbe,consumerObserver;
 static byte[] centerContinuation,tileContinuation;
 static byte[] originalRX;static bool restoredImage;
 static int validator2,validator0;
 static int extension,stateRva,stateSize,imageSize,imageRX,imageRXSize,normalContinuation,cases;static Shim shim;
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
 static void JumpSix(IntPtr at,IntPtr target){Check((Marshal.ReadByte(at)==0x81&&Marshal.ReadByte(at,1)==0xf8)||(Marshal.ReadByte(at)==0x8b&&Marshal.ReadByte(at,1)==0x85),"whole known six-byte cmp/load boundary");Jump(at,target);Marshal.WriteByte(at,5,0x90);}
 static byte[] HexBytes(string text,string field){Match m=Regex.Match(text,"\""+field+"\"\\s*:\\s*\"([0-9a-f]+)\"");Check(m.Success,"bound observer hex "+field);string s=m.Groups[1].Value;byte[] b=new byte[s.Length/2];for(int i=0;i<b.Length;i++)b[i]=Convert.ToByte(s.Substring(i*2,2),16);return b;}
 static void ValidatorObservers(){
  string binding=File.ReadAllText(Path.Combine(pack,"fixture","validator-observer-binding.json"));
  IntPtr begin=A(image,Number(binding,"validator_entry_rva")),end=A(image,Number(binding,"validator_exit_rva"));
  int before=Number(binding,"entry_overwrite_size"),after=Number(binding,"exit_overwrite_size");Check(before==12&&after==6,"whole validator overwrite extents");
  Check(Same(Read(begin,before),HexBytes(binding,"entry_original_hex"))&&Same(Read(end,after),HexBytes(binding,"exit_original_hex")),"exact untouched validator preimages");
  W(ctx,0xa88,A(image,Number(binding,"entry_continue_rva")).ToInt32());W(ctx,0xa8c,A(image,Number(binding,"exit_continue_rva")).ToInt32());
  Jump(begin,FixtureCode("validator_entry"));for(int i=5;i<before;i++)Marshal.WriteByte(begin,i,0x90);
  Jump(end,FixtureCode("validator_exit"));Marshal.WriteByte(end,5,0x90);
 }
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
  Check(found,"own code mapped");imageRX=rx;imageRXSize=rxSize;originalRX=Read(A(image,rx),rxSize);plan=A(image,stateRva);labels=new Dictionary<string,int>();Match table=Regex.Match(manifest,"\"labels\"\\s*:\\s*\\{([^}]+)\\}");Check(table.Success,"label table");
  foreach(Match m in Regex.Matches(table.Groups[1].Value,"\"([^\"]+)\"\\s*:\\s*(-?\\d+)"))labels[m.Groups[1].Value]=Int32.Parse(m.Groups[2].Value);
  Check(Entry("pass_state")==plan&&Entry("generation")==A(plan,0x79800),"PIC own Plan, not external scratch");
  // Independent allocations: shim5 owns its ABI/x87 context; fixture wrappers
  // own ctx0..32 and observer0x800. Neither can overwrite the other's slots.
  ctx=Mem(0x1000);shimctx=Mem(0x1000);stage=Mem(236);army=Mem(64);modelOutput=Mem(2048);world=Mem(16);stubstate=Mem(4096);engine=Mem(0x680000);grid=Mem(32);zarray=Mem(4);xarray=Mem(4);yarray=Mem(4);cell=Mem(32);db=Mem(12);records=Mem(24*192);good=Mem(192);bonus=Mem(80);IntPtr guarded=Mem(48);output=A(guarded,4);W(guarded,0,Canary);W(output,40,Canary);
  W(ctx,0,plan.ToInt32());W(ctx,4,stage.ToInt32());W(ctx,12,Entry("sci_food_diag_bad").ToInt32());
  normal=FixtureCode("normal");modelProbe=FixtureCode("model_probe");consumerObserver=FixtureCode("consumer_observer");
  string normalRecipe=File.ReadAllText(Path.Combine(pack,"fixture","normal.recipe.json"));normalContinuation=Number(normalRecipe,"continuation");
  // Save whole continuation windows before private-image-only routing.
  centerContinuation=Read(Entry("sci_food_diag_center_return"),16);tileContinuation=Read(Entry("sci_food_diag_primary_return"),16);
  JumpSix(Entry("sci_food_diag_center_return"),A(normal,normalContinuation));JumpSix(Entry("sci_food_diag_primary_return"),A(normal,normalContinuation));
  string old=Path.Combine(root,"PROEVEN","production-h3","helper");IntPtr vt=Mem(0x200);W(world,0,vt.ToInt32());W(world,4,stubstate.ToInt32());W(vt,0xb8,Code(File.ReadAllBytes(Path.Combine(old,"food.bin"))).ToInt32());
  W(plan,144+20,FixtureCode("convert_mutation").ToInt32());
  ValidatorObservers();
  Check(rx+rxSize<=stateRva-16,"prestate padding");for(int i=0;i<16;i+=4){W(plan,-16+i,Canary);W(plan,stateSize+i,Canary);}shim=MakeShim();
 }
 static void Reset(bool record){
  if(record)Clear(A(plan,276),236);Clear(stubstate,4096);Clear(cell,32);Clear(records,24*192);Clear(good,192);Clear(bonus,80);Clear(output,40);Clear(army,64);W(ctx,0x90c,0);
  W(plan,8,123);W(plan,32,7);W(plan,36,1);W(plan,40,1);W(plan,112,world.ToInt32());W(plan,68,1);W(plan,220,4);W(plan,224,4);W(plan,240,4);W(plan,256,64);W(plan,0x78800,123);W(plan,0x78804,7);W(plan,0x526a0+3*4,0);
  // Keep the converter pointer created once in Load; HostBinding uses Plan144.
  W(plan,144,engine.ToInt32());W(plan,148,grid.ToInt32());W(plan,152,db.ToInt32());H(engine,0x67df20,1);H(engine,0x67df22,1);W(grid,0x1c,zarray.ToInt32());W(zarray,0,xarray.ToInt32());W(xarray,0,yarray.ToInt32());W(yarray,0,cell.ToInt32());
  H(plan,0x200,0);H(plan,0x202,0);H(plan,0x204,0);H(plan,0x206,0xaabb);int sci=0x54800+3*2048;W(plan,sci+16,1);for(int i=0;i<8;i++)Marshal.WriteByte(plan,sci+136+i,Marshal.ReadByte(plan,0x200+i));
  Marshal.WriteByte(cell,13,1);W(db,0,24);W(db,8,records.ToInt32());W(records,192+8,5);W(stubstate,0x500,5);W(stubstate,16,1);W(ctx,0x830,0);W(ctx,0x834,0);
 }
 static byte[] Normal(bool clone,int kind,int returnKind=0){
  if(returnKind==0)returnKind=kind;
  W(ctx,32,Entry(returnKind==1?"sci_food_diag_center_return":"sci_food_diag_primary_return").ToInt32());W(ctx,36,Entry(clone?"sci_food_diag_reader":"food_reader").ToInt32());Clear(output,40);
  Clear(A(ctx,0xa00),0x88);W(ctx,0xa90,-1);
  int result=Invoke(normal,kind==1?A(plan,0x200):A(plan,0x54800+3*2048+136),kind==1?1:0);
  if(clone&&result!=1){Check(R(ctx,0xa80)==1&&R(ctx,0xa84)==1,"one entry/exit of actual occupied validator");Check(Same(Read(A(ctx,0xa00),36),Read(A(ctx,0xa40),36)),"all volatile/nonvolatile GPR/ESP/EBP and complete PUSHFD flags preserved by validator");Check(R(ctx,0xa90)==result,"typed spill matches observed validator result");if(result==2)validator2++;else if(result==0)validator0++;else Check(false,"unexpected private return");}
  else Check(R(ctx,0xa80)==0&&R(ctx,0xa84)==0,"success/shared skips private failure validator");
  byte[] value=new byte[48];Array.Copy(BitConverter.GetBytes(result),0,value,0,4);Array.Copy(Read(output,40),0,value,4,40);Array.Copy(BitConverter.GetBytes(R(stubstate,20)),0,value,44,4);return value;
 }
 static void Occupied(int count){W(cell,16,army.ToInt32());W(army,48,count);}
 static void Result(byte[] result,int expected,int callbacks,string why){
  Check(BitConverter.ToInt32(result,0)==expected,"typed return "+why);
  if(expected!=1){byte[] food=new byte[40];Array.Copy(result,4,food,0,40);Check(Same(food,new byte[40]),"out40 wiped "+why);}
  Check(BitConverter.ToInt32(result,44)==callbacks,"callback count "+why);Test(why,true);
 }
 static void ReaderCases(){
  Reset(true);Occupied(2);Result(Normal(true,1),2,0,"bound center positive2");
  // Same owner/gen, different prefix and ordinal; first latch remains prefix3.
  Reset(false);W(plan,220,5);W(plan,224,5);W(plan,240,5);W(plan,256,65);W(plan,0x526a0+4*4,0);Occupied(1);Result(Normal(true,1),2,0,"second occupied current invocation independent of first latch");Check(R(plan,276+24)==3,"first historical latch retained");
  Reset(false);W(plan,220,6);W(plan,224,6);W(plan,240,6);W(plan,256,66);W(plan,0x526a0+5*4,0);W(cell,20,7);Result(Normal(true,1),0,0,"subsequent city failure remains unknown despite first branch10 latch");
  Reset(true);Occupied(2);Result(Normal(true,2),0,0,"occupied tile remains unknown");
  Reset(true);Occupied(2);Result(Normal(true,1,2),0,0,"wrong center callsite remains unknown");
  Reset(true);Occupied(-1);Result(Normal(true,1),0,0,"negative count remains unknown");
  Reset(true);Occupied(0);Result(Normal(true,1),1,1,"zero count ordinary success");
  Reset(true);W(cell,20,7);Result(Normal(true,1),0,0,"city branch9 unchanged");
  Reset(true);W(records,192+8,-1);Result(Normal(true,1),0,0,"other guard pregetter unchanged");
  Reset(true);Result(Normal(false,1),1,1,"shared normal return1 unchanged");
  Reset(true);Occupied(2);Result(Normal(false,1),0,0,"shared occupied return0 unchanged");
  foreach(int offset in new int[]{8,32,36,40,220,224,240,256,0x78800,0x78804,68,0x526a0+12}){
   Reset(true);Occupied(2);W(ctx,0x900,A(plan,offset).ToInt32());W(ctx,0x904,offset==68?4097:offset==0x526a0+12?1:0);W(ctx,0x90c,1);
   Result(Normal(true,1),0,0,"fresh Plan mutation rejected offset"+offset);
  }
  // Mutations occur AFTER valid entry, in the converter, before failure.
  foreach(int offset in new int[]{-340,-344,-336,-336+12,-336+16,-336+20,-336+24,-336+28,-336+40,-336+60,-336+220,-336+224}){
   Reset(true);Occupied(2);W(ctx,0x900,offset);W(ctx,0x904,offset==-336+12?2:999);W(ctx,0x90c,2);
   Result(Normal(true,1),0,0,"fresh invocation staging mutation rejected offset"+offset);
  }
 }
 // Own image protection changes are finite, bound to mapped candidate bytes.
 static void Writable(bool write){uint old;Check(VirtualProtect(A(image,imageRX),(UIntPtr)imageRXSize,write?4u:0x20u,out old),"own fixture RX protection; Plan remains RW");if(!write)Check(FlushInstructionCache(new IntPtr(-1),A(image,imageRX),(UIntPtr)imageRXSize),"own fixture instruction cache");}
 static void RestoreImage(){if(originalRX==null||restoredImage)return;Writable(true);Marshal.Copy(originalRX,0,A(image,imageRX),originalRX.Length);Check(Same(Read(A(image,imageRX),imageRXSize),originalRX),"all original own-image RX windows restored exactly");Writable(false);restoredImage=true;}
 static void ModelCases(){
  Writable(true);Marshal.Copy(centerContinuation,0,Entry("sci_food_diag_center_return"),16);Marshal.Copy(tileContinuation,0,Entry("sci_food_diag_primary_return"),16);
  JumpSix(Entry("science_center_food_consumer"),consumerObserver);JumpSix(Entry("science_tile_food_consumer"),consumerObserver);
  // This label is a complete five-byte JMP after actual tile UNKNOWN marking.
  Check(Marshal.ReadByte(Entry("science_current_unknown_exit"))==0xe9,"whole unknown-exit JMP");Jump(Entry("science_current_unknown_exit"),Entry("science_done"));
  W(ctx,0x94c,Entry("science_done").ToInt32());Writable(false);
  foreach(int kind in new int[]{1,2})foreach(int returned in new int[]{0,1,2,3}){
   Clear(modelOutput,2048);W(ctx,0x948,0);W(ctx,0x944,returned);W(ctx,0x940,Entry(kind==1?"sci_food_diag_center_return":"sci_food_diag_primary_return").ToInt32());
   W(shimctx,112,modelProbe.ToInt32());W(shimctx,0x700,0);W(shimctx,0x704,0);W(shimctx,0x708,0);W(shimctx,0x70c,0);W(shimctx,0x710,modelOutput.ToInt32());shim();cases++;
   Check(R(shimctx,40)==R(shimctx,44),"model ret20/ESP");Check(Same(Read(A(shimctx,0x300),160),Read(A(shimctx,0x500),160)),"real model frstor/x87");
   Check(R(shimctx,48)==0x13579bdf&&R(shimctx,52)==0x2468ace0&&R(shimctx,56)==0x76543210&&R(shimctx,60)==0x55aa33cc,"model nonvolatile ABI");
   Check((R(ctx,0x948)==1)==(returned==1),"food consumers accept only1");
   if(kind==1&&returned==2){Check(R(modelOutput,0)==1&&R(modelOutput,4)==17&&R(modelOutput,112)==1&&R(modelOutput,24)==0,"actual occupied handler state/reason/coverage/no credit");for(int i=28;i<=36;i+=4)Check(R(modelOutput,i)==-1,"no selected indices");Check(Same(Read(A(modelOutput,72),40),new byte[40]),"food/margins untouched initialization");}
   if(kind==2&&returned!=1)Check(R(modelOutput,40)==1&&R(modelOutput,128+28)==2,"actual tile UNKNOWN flag/reason");
   if(kind==1&&returned!=1&&returned!=2)Check(R(modelOutput,0)==0&&R(modelOutput,112)==0,"other center returns UNKNOWN");
   Test("injected actual model continuation kind"+kind+" return"+returned,true);
  }
 }
 public static Dictionary<string,object> Run(string repository,string package,string candidateHash,string manifestHash){
  Check(IntPtr.Size==4,"x86 only");root=repository;pack=package;string gate=File.ReadAllText(Path.Combine(pack,"native-v2","NATIVE-ROOT-REVIEW.json"));
  Check(Regex.IsMatch(gate,"\"native_allowed\"\\s*:\\s*true")&&gate.Contains(candidateHash)&&gate.Contains(manifestHash),"new separate reviewed native release required");
  owned.Clear();passes.Clear();cases=0;validator2=0;validator0=0;originalRX=null;restoredImage=false;
  try{
   Load(candidateHash,manifestHash);
   Writable(false);ReaderCases();ModelCases();RestoreImage();
   Check(cases==43&&validator2==2&&validator0==30,"finite43 calls and actual validator healthy2/failed0 observer coverage");
   Check(Hash(File.ReadAllBytes(Path.Combine(pack,"U30-40.prepared.dll")))==candidateHash,"candidate disk unchanged");
   return new Dictionary<string,object>{{"scope","OWN_FIXTURE_ONLY_NOT_ENGINE_OR_GAMEPLAY"},{"calls",cases},{"validator_return2_observed",validator2},{"validator_return0_observed",validator0},{"own_image_all_windows_restored",restoredImage},{"passed",passes.ToArray()},{"synthetic_log_edges",0},{"natural_all37_guard_reachability_proven",false},{"gameplay_proven",false}};
  }finally{
   RestoreImage();bool all=true;for(int i=owned.Count-1;i>=0;i--)all=VirtualFree(owned[i],UIntPtr.Zero,0x8000)&&all;owned.Clear();Console.WriteLine("cleanup="+all);Console.Out.Flush();Check(all,"all own allocations released");
  }
 }
}
