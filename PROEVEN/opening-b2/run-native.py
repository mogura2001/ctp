"""Reuse existing bounded own32-bit PowerShell/native ownallocation method."""
from pathlib import Path
import subprocess,json,time
OUT=Path(__file__).resolve().parent
HELPER=Path('C:/Windows/SysWOW64/WindowsPowerShell/v1.0/powershell.exe')
summary=[]
for n in (25,30):
 for mode in ('fixture','loader'):
  cmd=[str(HELPER),'-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(OUT/'helper/native.ps1'),'-N',str(n),'-Mode',mode];begin=time.monotonic()
  try:
   result=subprocess.run(cmd,capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
   output=result.stdout.decode('utf-8',errors='replace')+result.stderr.decode('utf-8',errors='replace');(OUT/f'B2a-N{n}-TECHNICAL.native-{mode}.log').write_text(output);rec={'N':n,'mode':mode,'exit_code':result.returncode,'elapsed_seconds':round(time.monotonic()-begin,3),'timeout':False}
  except subprocess.TimeoutExpired as e:
   rec={'N':n,'mode':mode,'timeout':True,'elapsed_seconds':round(time.monotonic()-begin,3)};(OUT/f'B2a-N{n}-TECHNICAL.native-{mode}.log').write_text(str(e))
  summary.append(rec);print(json.dumps(rec),flush=True)
(OUT/'native-processes.json').write_text(json.dumps({'helper_executable':str(HELPER),'per_process_timeout_seconds':45,'processes':summary},indent=2)+'\n')
if any(r.get('exit_code',-1)!=0 for r in summary):raise SystemExit(1)
