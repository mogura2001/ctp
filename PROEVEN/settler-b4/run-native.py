"""Bounded ordinary 32-bit native helpers, own memory only; no game process."""
from pathlib import Path
import subprocess,time,json
OUT=Path(__file__).resolve().parent
helper='C:/Windows/SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
summary=[]
for n in (25,30):
 tasks=[('producer',['-File',str(OUT/'native-producer.ps1'),'-N',str(n)])]
 for baseline in (False,True):
  for rebase in (False,True):
   tag=('BASELINE' if baseline else 'B4')+('-rebase' if rebase else '')
   args=['-File',str(OUT/'native-loader.ps1'),'-N',str(n)]
   if baseline:args+=['-Baseline']
   if rebase:args+=['-Rebase']
   tasks.append(('loader-'+tag,args))
 for mode,args in tasks:
  begin=time.monotonic()
  try:
   p=subprocess.run([helper,'-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass',*args],capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
   (OUT/f'N{n}.{mode}.log').write_text(p.stdout.decode('utf-8',errors='replace')+p.stderr.decode('utf-8',errors='replace'),encoding='utf-8')
   row=dict(N=n,mode=mode,exit_code=p.returncode,elapsed_seconds=round(time.monotonic()-begin,3))
  except subprocess.TimeoutExpired as exc:
   row=dict(N=n,mode=mode,timeout=True);(OUT/f'N{n}.{mode}.log').write_text(str(exc))
  summary.append(row);print(json.dumps(row),flush=True)
  if row.get('exit_code',-1)!=0:break
 if any(row.get('exit_code',-1)!=0 for row in summary):break
(OUT/'native-processes.json').write_text(json.dumps(summary,indent=2)+'\n')
if any(row.get('exit_code',-1)!=0 for row in summary):raise SystemExit(1)
