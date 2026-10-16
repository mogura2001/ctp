// Minimal alternative launcher of the same existing32bit fixture body.
using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using System.Web.Script.Serialization;
public static class NativeMain {
 static int[] Ints(object value){var list=(object[])value;int[] result=new int[list.Length];for(int i=0;i<list.Length;i++)result[i]=Convert.ToInt32(list[i]);return result;}
 static string[] Strings(object value){var list=(object[])value;string[] result=new string[list.Length];for(int i=0;i<list.Length;i++)result[i]=(string)list[i];return result;}
 public static int Main(string[] args){
  if(args.Length!=2||!args[1].StartsWith("attempt"))return 2;
  string root=Path.GetFullPath(args[0]),output=Path.Combine(root,"native-"+args[1]+".json");if(File.Exists(output))return 3;
  JavaScriptSerializer serializer=null;
  Console.WriteLine("helper_pid "+System.Diagnostics.Process.GetCurrentProcess().Id);
  try{
   var process=System.Diagnostics.Process.GetCurrentProcess();var module=process.MainModule;
   Console.WriteLine("helper_mapping pid="+process.Id+" bitness="+(IntPtr.Size*8)+" path="+module.FileName+" base="+unchecked((uint)module.BaseAddress.ToInt32()).ToString("x8")+" size="+module.ModuleMemorySize.ToString("x"));Console.Out.Flush();
   ScienceNative.BindMainModule(module.BaseAddress,module.ModuleMemorySize);
   ScienceNative.ReserveEngineBlocks();
   serializer=new JavaScriptSerializer();serializer.MaxJsonLength=10000000;
   var input=(Dictionary<string,object>)serializer.DeserializeObject(File.ReadAllText(Path.Combine(root,"native-input.json")));
   var result=ScienceNative.Run(root,Ints(input["ranges"]),Ints(input["pin_rvas"]),Strings(input["pin_hex"]),Ints(input["fix_at"]),Ints(input["fix_off"]));
   if(!ScienceNative.CleanupOk)throw new InvalidOperationException("owned cleanup failed; see stdout");
   File.WriteAllText(output,serializer.Serialize(result));Console.WriteLine("PASS nativecalls "+result["native_calls"]);return 0;
  }catch(Exception ex){
   if(serializer==null){serializer=new JavaScriptSerializer();serializer.MaxJsonLength=10000000;}
   var result=new Dictionary<string,object>{{"pass",false},{"error",ex.ToString()},{"cases",ScienceNative.Results},{"patches",ScienceNative.Patches},{"helper_pid",System.Diagnostics.Process.GetCurrentProcess().Id},{"bitness",IntPtr.Size*8},{"gameplay_measured",false}};
   File.WriteAllText(output,serializer.Serialize(result));Console.Error.WriteLine(ex.ToString());return 1;
  }finally{ScienceNative.ReleaseOwned();}
 }
}
