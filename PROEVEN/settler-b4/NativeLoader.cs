// Loader-only own-process check: no game window or engine query executes.
using System;using System.IO;using System.Runtime.InteropServices;
public static class B4Loader {
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern IntPtr LoadLibraryW(string file);
 [DllImport("kernel32.dll")] static extern bool FreeLibrary(IntPtr module);
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr VirtualAlloc(IntPtr address,UIntPtr size,uint type,uint protect);
 [DllImport("kernel32.dll")] static extern bool VirtualFree(IntPtr address,UIntPtr size,uint type);
 [DllImport("kernel32.dll")] static extern uint SetErrorMode(uint mode);
 static void Check(bool v,string w){if(!v)throw new Exception(w);}
 public static string Run(string file,string payload,int size,int[] sites,int[] targets,bool forceRebase){SetErrorMode(0x8003);Check(IntPtr.Size==4,"x86 helper");IntPtr reserved=IntPtr.Zero,module=IntPtr.Zero;try{
  if(forceRebase){reserved=VirtualAlloc(new IntPtr(0x20000000),(UIntPtr)size,0x2000,1);Check(reserved==new IntPtr(0x20000000),"preferredbase reservation");}
  module=LoadLibraryW(file);Check(module!=IntPtr.Zero,"ordinary imports/DllMain loader error "+Marshal.GetLastWin32Error());if(forceRebase)Check(module.ToInt32()!=0x20000000,"actual rebase");
  byte[] bytes=File.ReadAllBytes(payload),mapped=new byte[bytes.Length];Marshal.Copy(new IntPtr(module.ToInt32()+0xd4000),mapped,0,mapped.Length);for(int i=0;i<bytes.Length;i++)Check(bytes[i]==mapped[i],"unchanged PICpayload byte "+i);
  for(int i=0;i<sites.Length;i++){int at=sites[i];Check(Marshal.ReadByte(module,at)==0xe8&&at+5+Marshal.ReadInt32(module,at+1)==targets[i],"mapped hooktarget "+at.ToString("x"));}
  return String.Format("0x{0:x8}",module.ToInt32());
 }finally{if(module!=IntPtr.Zero)Check(FreeLibrary(module),"ordinary FreeLibrary");if(reserved!=IntPtr.Zero)VirtualFree(reserved,UIntPtr.Zero,0x8000);}}
}
