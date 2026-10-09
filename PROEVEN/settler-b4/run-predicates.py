"""Bounded 32-bit ownallocation checks; no game or engine calls."""
from pathlib import Path
import subprocess,json,time
OUT=Path(__file__).resolve().parent
summary=[]
for N in (25,30):
 begin=time.monotonic()
 result=subprocess.run(['C:/Windows/SysWOW64/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(OUT/'native-predicates.ps1'),'-N',str(N)],capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
 output=result.stdout.decode('utf-8',errors='replace')+result.stderr.decode('utf-8',errors='replace')
 (OUT/f'B4-N{N}.native-predicates.log').write_text(output,encoding='utf-8')
 row=dict(N_fixture=N,exit_code=result.returncode,elapsed_seconds=round(time.monotonic()-begin,3));summary.append(row);print(json.dumps(row),flush=True)
(OUT/'native-predicate-processes.json').write_text(json.dumps(summary,indent=2)+'\n')
if any(r['exit_code']!=0 for r in summary):raise SystemExit(1)
