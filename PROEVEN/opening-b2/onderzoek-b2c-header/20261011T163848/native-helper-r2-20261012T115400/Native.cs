// SOURCE ONLY until root C2 approval. Calls the unmodified original DLL in this own x86 subprocess.
// No game process, image copy, IAT patch, parser stub, native destructor, native free or DLL unload.
using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.ComponentModel;
using System.Security.Cryptography;
using System.Diagnostics;
public static class B2cParserNative {
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern IntPtr LoadLibraryW(string path);
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr VirtualAlloc(IntPtr p,UIntPtr n,uint type,uint protection);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool VirtualProtect(IntPtr p,UIntPtr n,uint protection,out uint old);
 [DllImport("kernel32.dll")] static extern uint SetErrorMode(uint flags);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)] delegate void Shim();
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate IntPtr PointerCallback(IntPtr self);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int CountCallback(IntPtr self);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int ScienceCallback(IntPtr self,IntPtr text);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate void ErrorCallback(IntPtr self,IntPtr text);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate void UnexpectedCallback(int slot);
 static List<Delegate> retained;
 static List<IntPtr> allocations;
 static IntPtr module,ctx,ai,game,units,science,diagnostic,path;
 static Shim[] shims;
 static Dictionary<string,int> indices;
 static List<string> names,errors;
 static List<object> calls,loaded;
 static string helper,trace;
 static int pathCalls,unitCalls,scienceCalls,diagnosticCalls;
 static bool unknownName;
 public static Dictionary<string,object> Evidence;
 const string Original="3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44";
 static IntPtr A(IntPtr p,int o){return new IntPtr(unchecked(p.ToInt32()+o));}
 static int R(IntPtr p,int o){return Marshal.ReadInt32(p,o);}
 static void W(IntPtr p,int o,int v){Marshal.WriteInt32(p,o,v);}
 static byte[] Read(IntPtr p,int n){if(p==IntPtr.Zero||n<0||n>0x100000)throw new InvalidOperationException("read bound");byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}
 static void Check(bool ok,string why){if(!ok)throw new InvalidOperationException(why);}
 static string Hash(byte[] b){using(var h=SHA256.Create())return BitConverter.ToString(h.ComputeHash(b)).Replace("-","").ToLowerInvariant();}
 static bool Equal(byte[] a,byte[] b){if(a.Length!=b.Length)return false;for(int i=0;i<a.Length;i++)if(a[i]!=b[i])return false;return true;}
 static void Note(string s){File.AppendAllText(trace,s+"\n",Encoding.UTF8);}
 static IntPtr Mem(int n){IntPtr p=VirtualAlloc(IntPtr.Zero,(UIntPtr)n,0x3000,4);if(p==IntPtr.Zero)throw new Win32Exception();allocations.Add(p);return p;}
 static IntPtr Bytes(byte[] bytes){IntPtr p=Mem(bytes.Length);Marshal.Copy(bytes,0,p,bytes.Length);return p;}
 static IntPtr Text(string s){return Bytes(Encoding.ASCII.GetBytes(s+"\0"));}
 static IntPtr Code(byte[] b){IntPtr p=Bytes(b);uint old;Check(VirtualProtect(p,(UIntPtr)b.Length,0x20,out old),"own code RX");return p;}
 static string Ansi(IntPtr p,int max){Check(p!=IntPtr.Zero,"null callback string");var b=new List<byte>();for(int i=0;i<max;i++){byte c=Marshal.ReadByte(p,i);if(c==0)return Encoding.ASCII.GetString(b.ToArray());Check(c<128,"non-ASCII callback string");b.Add(c);}throw new InvalidOperationException("unterminated bounded callback string");}
 static IntPtr Bind(Delegate d){retained.Add(d);return Marshal.GetFunctionPointerForDelegate(d);}
 static IntPtr Trap(int slot){
  UnexpectedCallback stop=delegate(int actual){Note("UNEXPECTED_INTERFACE_SLOT="+actual);Environment.Exit(2);};
  IntPtr target=Bind(stop);var b=new List<byte>();b.Add(0x68);b.AddRange(BitConverter.GetBytes(slot));b.Add(0xb8);b.AddRange(BitConverter.GetBytes(target.ToInt32()));b.AddRange(new byte[]{0xff,0xd0,0x0f,0x0b});return Code(b.ToArray());
 }
 static IntPtr Interface(int identity){IntPtr table=Mem(0x200),obj=Mem(4);for(int o=0;o<0x200;o+=4)W(table,o,Trap(identity*0x1000+o).ToInt32());W(obj,0,table.ToInt32());return obj;}
 static void Slot(IntPtr obj,int off,Delegate callback){W(new IntPtr(R(obj,0)),off,Bind(callback).ToInt32());}
 static void InstallCallbacks(string staging){
  game=Interface(1);units=Interface(2);science=Interface(3);diagnostic=Interface(4);path=Text(staging);
  Slot(game,0x54,new PointerCallback(delegate(IntPtr self){Check(self==game,"GameState self");pathCalls++;Note("PATH="+staging);return path;}));
  Slot(units,0x0c,new CountCallback(delegate(IntPtr self){Check(self==units,"UnitDB self");unitCalls++;return 1;}));
  Slot(science,0x50,new ScienceCallback(delegate(IntPtr self,IntPtr p){Check(self==science,"Science self");string n=Ansi(p,80);Check(names.Count<512,"science log bound");names.Add(n);scienceCalls++;int index;if(!indices.TryGetValue(n,out index)){unknownName=true;index=-1;}Note("SCIENCE="+n+":"+index);return index;}));
  Slot(game,0x58,new PointerCallback(delegate(IntPtr self){Check(self==game,"diagnostic GameState self");diagnosticCalls++;return diagnostic;}));
  Slot(diagnostic,0x10,new ErrorCallback(delegate(IntPtr self,IntPtr p){Check(self==diagnostic,"Diagnostic self");Check(errors.Count<32,"diagnostic bound");string s=Ansi(p,2048);errors.Add(s);Note("DIAGNOSTIC="+s);}));
  ai=Mem(0x100);W(ai,0x28,game.ToInt32());W(ai,0x38,units.ToInt32());W(ai,0x44,science.ToInt32());
 }
 static void PrepareShims(int[][] fixes1,int[][] fixes2){
  ctx=Mem(0x800);shims=new Shim[3];int[][][] fixsets={null,fixes1,fixes2};
  for(int argc=1;argc<=2;argc++){
   byte[] b=File.ReadAllBytes(Path.Combine(helper,"shim"+argc+".bin"));
   foreach(int[] fix in fixsets[argc])Array.Copy(BitConverter.GetBytes(A(ctx,fix[1]).ToInt32()),0,b,fix[0],4);
   shims[argc]=(Shim)Marshal.GetDelegateForFunctionPointer(Code(b),typeof(Shim));retained.Add(shims[argc]);
  }
 }
 static int Invoke(int rva,IntPtr self,params int[] args){
  Check(args.Length==1||args.Length==2,"bounded ABI argc");W(ctx,112,A(module,rva).ToInt32());W(ctx,116,self.ToInt32());W(ctx,120,ai.ToInt32());for(int i=0;i<args.Length;i++)W(ctx,0x700+4*i,args[i]);
  Note("CALL_BEGIN_RVA="+rva.ToString("x")+" SELF="+self.ToInt32()+" ARGC="+args.Length);
  shims[args.Length]();byte[] before=Read(A(ctx,0x300),160),after=Read(A(ctx,0x500),160);
  // Record full x87 state, compare ABI-preserved control, TOP/tag and 80-bit occupied registers.
  // FIP/FDP/opcode and exception flags may change after legitimate native floating point work.
  bool fp=before[0]==after[0]&&before[1]==after[1]&&before[4]==after[4]&&(before[3]&0x38)==(after[3]&0x38);
  int top=(before[3]>>3)&7;
  for(int i=32;i<160;i+=16)if((before[4]&(1<<((top+(i-32)/16)&7)))!=0)for(int j=0;j<10;j++)fp&=before[i+j]==after[i+j];
  bool esp=R(ctx,40)==R(ctx,44),nv=R(ctx,48)==0x13579bdf&&R(ctx,52)==ai.ToInt32()&&R(ctx,56)==0x76543210&&R(ctx,60)==0x55aa33cc;
  calls.Add(new Dictionary<string,object>{{"rva",rva},{"actual_entry",A(module,rva).ToInt32()},{"self",self.ToInt32()},{"args",args},{"return",R(ctx,36)},{"esp_before",R(ctx,40)},{"esp_after",R(ctx,44)},{"nonvolatile_pass",nv},{"x87_before",Convert.ToBase64String(before)},{"x87_after",Convert.ToBase64String(after)},{"x87_control_top_tag_values_pass",fp}});
  Note("CALL_END_RVA="+rva.ToString("x"));Check(esp,"ESP cleanup");Check(nv,"nonvolatile registers");Check(fp,"x87 control/TOP/tag/register values");return R(ctx,36);
 }
 static IntPtr NewAip(){IntPtr p=Mem(0xa08);int returned=Invoke(0x642a0,p,ai.ToInt32(),0);Check(returned==p.ToInt32()&&R(p,0x800)==ai.ToInt32()&&R(p,0x7b4)==0,"native ctor return/AiMain/bool0");Check(unitCalls>0,"native UnitDB ctor callback");return p;}
 static Dictionary<string,object> Inspect(IntPtr aip,bool rawEffective=false){
  int presence=R(aip,0x7ac),pointer=R(aip,0x7fc);int count=-1;int[] data=new int[0];
  if(rawEffective||(presence&0x4000)!=0){Check(pointer!=0,"present research pointer");IntPtr c=new IntPtr(pointer);count=R(c,4);Check(count>=0&&count<=200,"research count bound");data=new int[count];if(count>0){int entries=R(c,0);Check(entries!=0,"research data pointer");Marshal.Copy(new IntPtr(entries),data,0,count);}}
  return new Dictionary<string,object>{{"aip",aip.ToInt32()},{"presence",presence},{"research_pointer",pointer},{"research_count",count},{"indices",data},{"ownership_bits",R(aip,0x7cc)}};
 }
 static void Positive(IntPtr p,string[] expected,int start){
  var s=Inspect(p);Check(((int)s["presence"]&0x1fff0)==0x4000,"only research list presence");Check((int)s["research_count"]==98,"98 native entries");
  byte[] scalar=Read(A(p,0x740),0x6c);foreach(byte b in scalar)Check(b==0,"absent scalar presence");
  Check(names.Count-start==98,"98 actual name callbacks");int[] actual=(int[])s["indices"];
  for(int i=0;i<98;i++)Check(names[start+i]==expected[i]&&actual[i]==indices[expected[i]],"native names/order/indices "+i);
  Check(!unknownName&&errors.Count==0,"positive unknown-name/diagnostic rejection");loaded.Add(s);
 }
 static IntPtr Load(string filename,string[] expected,bool positive){
  Check(filename.Length<128&&filename.IndexOfAny(new char[]{'\\','/'})<0,"leaf filename bound");IntPtr p=NewAip();int start=names.Count;
  int returned=Invoke(0x628d0,p,Text(filename).ToInt32(),1);Check(returned==p.ToInt32()||(!positive&&returned==0),"actual Load_AIP_File return");
  if(positive)Positive(p,expected,start);else loaded.Add(Inspect(p));return p;
 }
 static int[] ListOffsets={0x7d0,0x7d4,0x7d8,0x7dc,0x7e0,0x7e4,0x7e8,0x7ec,0x7f0,0x7f4,0x7f8};
 static Dictionary<int,byte[]> Fixture(IntPtr p){
  var kept=new Dictionary<int,byte[]>();IntPtr unitTable=Mem(8),unitData=Mem(32);for(int i=0;i<8;i++)W(unitData,4*i,0x1100+i);W(unitTable,0,unitData.ToInt32());W(unitTable,4,2);W(p,0x7bc,unitTable.ToInt32());W(p,0x7b0,2);kept[unitTable.ToInt32()]=Read(unitTable,8);kept[unitData.ToInt32()]=Read(unitData,32);
  foreach(int off in ListOffsets){IntPtr c=Mem(8),d=Mem(8);W(d,0,off);W(d,4,off+1);W(c,0,d.ToInt32());W(c,4,2);W(p,off,c.ToInt32());kept[c.ToInt32()]=Read(c,8);kept[d.ToInt32()]=Read(d,8);}
  Marshal.Copy(BitConverter.GetBytes(321.25),0,A(p,8),8);Marshal.Copy(BitConverter.GetBytes(654.5),0,A(p,0x10),8);W(p,0x248,17);
  // Constructor ownership bits are left untouched. Absent source categories cannot invoke their frees.
  // Initial research is null; first native switch clears its own bit12, subsequent switches borrow.
  Check(R(p,0x7fc)==0,"effective initial research null");return kept;
 }
 static void Preserve(IntPtr p,byte[] scalar,Dictionary<int,byte[]> memory,int unitPointer,int[] pointers){
  byte[] current=Read(p,0x740);for(int i=0;i<scalar.Length;i++)if(!(i>=0x368&&i<0x370)&&!(i>=0x4e8&&i<0x4f0))Check(current[i]==scalar[i],"scalar baseline retention at "+i.ToString("x"));
  Check(BitConverter.ToDouble(Read(A(p,0x368),8),0)==-999999&&BitConverter.ToDouble(Read(A(p,0x4e8),8),0)==-999999,"native retreat sentinel exception");
  Check(R(p,0x7bc)==unitPointer&&R(p,0x7b0)==2,"unit fixture pointer/count preserved");for(int i=0;i<ListOffsets.Length;i++)Check(R(p,ListOffsets[i])==pointers[i],"other list pointer retained");
  foreach(var k in memory)Check(Equal(Read(new IntPtr(k.Key),k.Value.Length),k.Value),"other list fixture contents retained");
 }
 static void ModulesAndImports(){
  int nt=R(module,0x3c);Check(R(module,0)==0x00905a4d||Marshal.ReadInt16(module,0)==0x5a4d,"loaded MZ");Check(R(module,nt)==0x4550&&Marshal.ReadInt16(module,nt+4)==0x14c&&R(module,nt+8)==0x37b894e7,"loaded PE32/timestamp");
  var mods=new List<object>();foreach(ProcessModule m in Process.GetCurrentProcess().Modules){Check(mods.Count<256,"module bound");mods.Add(new Dictionary<string,object>{{"path",m.FileName},{"base",m.BaseAddress.ToInt32()},{"size",m.ModuleMemorySize},{"sha256",Hash(File.ReadAllBytes(m.FileName))}});}Evidence["modules"]=mods;
  int size=R(module,nt+0x50),desc=R(module,nt+0x80);var bindings=new List<object>();
  for(int i=0;i<128;i++){int off=desc+20*i;Check(off>=0&&off+20<size,"import descriptor range");int lookup=R(module,off),name=R(module,off+12),iat=R(module,off+16);if(lookup==0&&name==0&&iat==0)break;Check(name>0&&name<size&&iat>0&&iat<size,"import descriptor fields");if(lookup==0)throw new InvalidOperationException("unbound original thunk metadata");
   for(int j=0;j<1024;j++){Check(lookup+4*j+4<=size&&iat+4*j+4<=size,"import thunk range");int token=R(module,lookup+4*j);if(token==0)break;int target=R(module,iat+4*j);string symbol=(token<0)?"ordinal:"+(token&65535):Ansi(A(module,token+2),256);string owner="UNBOUND";foreach(ProcessModule m in Process.GetCurrentProcess().Modules){uint a=(uint)target,b=(uint)m.BaseAddress.ToInt32();if(a>=b&&a-b<(uint)m.ModuleMemorySize){owner=m.FileName;break;}}Check(owner!="UNBOUND","unbound actual IAT target");bindings.Add(new Dictionary<string,object>{{"library",Ansi(A(module,name),256)},{"symbol",symbol},{"iat_rva",iat+4*j},{"target",target},{"target_module",owner}});}
  }Evidence["actual_import_bindings"]=bindings;
 }
 public static Dictionary<string,object> Run(string helperRoot,string dll,string staging,string kind,string[] files,string[][] expected,string[] fixtureNames,int[][] f1,int[][] f2,int[] entryRvas,string[] entryHex,int[][] relocationOffsets,string tracePath){
  Check(IntPtr.Size==4,"x86 own helper required");helper=helperRoot;trace=tracePath;retained=new List<Delegate>();allocations=new List<IntPtr>();names=new List<string>();errors=new List<string>();calls=new List<object>();loaded=new List<object>();indices=new Dictionary<string,int>();pathCalls=unitCalls=scienceCalls=diagnosticCalls=0;unknownName=false;
  Evidence=new Dictionary<string,object>{{"pass",false},{"kind",kind},{"helper_pid",Process.GetCurrentProcess().Id},{"bitness",32},{"dll_path",dll},{"dll_sha256",Hash(File.ReadAllBytes(dll))},{"native_calls",calls},{"lists",loaded},{"science_names",names},{"diagnostics",errors},{"science_indices_are_fixtures",true},{"gameplay_measured",false}};
  Check((string)Evidence["dll_sha256"]==Original,"original DLL hash");for(int i=0;i<fixtureNames.Length;i++){Check(!indices.ContainsKey(fixtureNames[i]),"unique fixture mapping");indices.Add(fixtureNames[i],1000+i);}
  SetErrorMode(0x8003);module=LoadLibraryW(dll);if(module==IntPtr.Zero)throw new Win32Exception(Marshal.GetLastWin32Error());Evidence["actual_module_base"]=module.ToInt32();ModulesAndImports();
  Check(entryRvas.Length==3&&entryHex.Length==3,"three entry bindings");
  for(int i=0;i<3;i++){
   byte[] normalized=Read(A(module,entryRvas[i]),24);
   foreach(int offset in relocationOffsets[i]){Check(offset>=0&&offset+4<=24,"preimage relocation range");int original=unchecked(BitConverter.ToInt32(normalized,offset)-(module.ToInt32()-0x20000000));Array.Copy(BitConverter.GetBytes(original),0,normalized,offset,4);}
   Check(BitConverter.ToString(normalized).Replace("-","").ToLowerInvariant()==entryHex[i],"loaded original entry preimage "+entryRvas[i].ToString("x"));
  }
  InstallCallbacks(staging);PrepareShims(f1,f2);
  if(kind=="parse"){Load(files[0],expected[0],true);}
  else if(kind=="switch"){
   IntPtr restore=Load(files[0],expected[0],true),opening=Load(files[1],expected[1],true),effective=NewAip();var memory=Fixture(effective);byte[] scalar=Read(effective,0x740);int unit=R(effective,0x7bc),initialPresence=R(effective,0x7ac);int[] pointers=new int[ListOffsets.Length];for(int i=0;i<pointers.Length;i++)pointers[i]=R(effective,ListOffsets[i]);
   foreach(IntPtr source in new IntPtr[]{restore,opening,restore}){Invoke(0x63720,effective,source.ToInt32());Preserve(effective,scalar,memory,unit,pointers);var s=Inspect(source);var e=Inspect(effective,true);Check((int)e["presence"]==initialPresence,"effective presence remains native unchanged");Check((int)e["research_pointer"]==(int)s["research_pointer"]&&(int)e["research_count"]==98,"actual borrowed research replacement");int[] x=(int[])s["indices"],y=(int[])e["indices"];for(int i=0;i<98;i++)Check(x[i]==y[i],"all switched indices");Check((R(effective,0x7cc)&0x1000)==0,"native research borrowing bit");loaded.Add(e);}
  }else{
   IntPtr p=Load(files[0],expected[0],false);var s=Inspect(p);bool valid=((int)s["presence"]&0x4000)!=0&&(int)s["research_count"]==98;
   if(kind=="unknown-name"){Check(unknownName&&names.Contains("ADVANCE_B2C_FIXTURE_UNKNOWN"),"actual unknown-name callback");int[] data=(int[])s["indices"];bool found=false;foreach(int index in data)found|=index==-1;Check(found,"native negative index stored; not loader self-rejection");}
   else{Check(kind=="headerless"||kind=="missing-header","known negative kind");Check(!valid||errors.Count>0,"negative candidate must not silently pass");}
  }
  Check(pathCalls>0&&unitCalls>0,"actual path/constructor callbacks");Evidence["path_calls"]=pathCalls;Evidence["unit_count_fixture_calls"]=unitCalls;Evidence["science_calls"]=scienceCalls;Evidence["diagnostic_calls"]=diagnosticCalls;Evidence["unknown_name_seen"]=unknownName;Evidence["pass"]=true;
  // Retain module, native AIPs/borrowed lists, own allocations and delegates until OS reclaims this subprocess.
  // No destructorpass is claimed; no Marshal/free of native CRT buffers and no FreeLibrary.
  GC.KeepAlive(retained);GC.KeepAlive(allocations);return Evidence;
 }
}
