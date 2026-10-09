"""Four bounded, self-owned x86 helper processes. No game process access."""
from pathlib import Path
import subprocess,json,time
OUT=Path(__file__).resolve().parent
HELPER=Path('C:/Windows/SysWOW64/WindowsPowerShell/v1.0/powershell.exe')
assert HELPER.is_file()
summary=[]
for variant in ('H1-I','H1-M'):
    for mode in ('fixture','loader'):
        cmd=[str(HELPER),'-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(OUT/'helper/native.ps1'),'-Variant',variant,'-Mode',mode]
        begin=time.monotonic()
        try:
            result=subprocess.run(cmd,capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
            output=result.stdout.decode('utf-8',errors='replace')+result.stderr.decode('utf-8',errors='replace')
            (OUT/f'{variant}.native-{mode}.log').write_text(output)
            record={'variant':variant,'mode':mode,'exit_code':result.returncode,'elapsed_seconds':round(time.monotonic()-begin,3),'timeout':False}
        except subprocess.TimeoutExpired as error:
            # subprocess.run kills and waits only for its own helper child.
            record={'variant':variant,'mode':mode,'timeout':True,'elapsed_seconds':round(time.monotonic()-begin,3)}
            (OUT/f'{variant}.native-{mode}.log').write_text(str(error))
        summary.append(record)
        print(json.dumps(record),flush=True)
(OUT/'native-processes.json').write_text(json.dumps({'helper_executable':str(HELPER),'per_process_timeout_seconds':45,'processes':summary},indent=2)+'\n')
if any(r.get('exit_code',-1)!=0 for r in summary):raise SystemExit(1)
