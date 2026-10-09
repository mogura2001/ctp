"""Bounded own32-bit PowerShell helper, reused from H1. No game access."""
from pathlib import Path
import subprocess,json,time
OUT=Path(__file__).resolve().parent
HELPER=Path('C:/Windows/SysWOW64/WindowsPowerShell/v1.0/powershell.exe')
summary=[]
for mode in ('fixture','loader'):
 cmd=[str(HELPER),'-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(OUT/'helper/native.ps1'),'-Mode',mode]
 begin=time.monotonic()
 try:
  result=subprocess.run(cmd,capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
  output=result.stdout.decode('utf-8',errors='replace')+result.stderr.decode('utf-8',errors='replace')
  (OUT/f'H3-SCORE_CURRENT.native-{mode}.log').write_text(output)
  record={'mode':mode,'exit_code':result.returncode,'elapsed_seconds':round(time.monotonic()-begin,3),'timeout':False}
 except subprocess.TimeoutExpired as error:
  record={'mode':mode,'timeout':True,'elapsed_seconds':round(time.monotonic()-begin,3)}
  (OUT/f'H3-SCORE_CURRENT.native-{mode}.log').write_text(str(error))
 summary.append(record);print(json.dumps(record),flush=True)
(OUT/'native-processes.json').write_text(json.dumps({'helper_executable':str(HELPER),'per_process_timeout_seconds':45,'processes':summary},indent=2)+'\n')
if any(r.get('exit_code',-1)!=0 for r in summary):raise SystemExit(1)
