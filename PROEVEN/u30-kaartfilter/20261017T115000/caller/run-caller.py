"""One bounded hidden own x86 caller helper, using existing C2 launch pattern."""
from pathlib import Path
import datetime,hashlib,json,subprocess,time
OUT=Path(__file__).resolve().parent;PACK=OUT.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
m=json.loads((PACK/'candidate-manifest.json').read_text('utf-8'))
assert m['components']['extension_rva']=='0xd9000'
assert m['candidate_sha256']==sha((PACK/'U30-40.prepared.dll').read_bytes())=='738be4098dadc6657b121519213e794ce3ec095025fdc940f6c30a5d89661d66'
assert sha((PACK/'candidate-manifest.json').read_bytes())=='d48b63b2363f0bfce2fe4b7d44a83b90951a524ecf3f300bf9661b50080be2a9'
checkpoint=json.loads((PACK/'BUILD-PINS.json').read_text('utf-8'))
for r in checkpoint['files']:assert sha((PACK/r['path']).read_bytes())==r['sha256'],r['path']
assert not (OUT/'caller-process.json').exists(),'One finite run only; retain prior attempt'
start=time.monotonic()
proc=subprocess.Popen(['C:/Windows/SysWOW64/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(OUT/'native-caller.ps1')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
row=dict(stage='OWN_CALLER_ONLY',started_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),pid=proc.pid,owned_process=True,hidden=True,timeout_seconds=45)
try:
 stdout,stderr=proc.communicate(timeout=45);row['exit_code']=proc.returncode
except subprocess.TimeoutExpired:
 row['timeout']=True;proc.kill();stdout,stderr=proc.communicate(timeout=10);row['exit_code_after_kill']=proc.returncode
row.update(elapsed_seconds=round(time.monotonic()-start,3),terminal_confirmed=proc.poll() is not None,candidate_unchanged=sha((PACK/'U30-40.prepared.dll').read_bytes())==m['candidate_sha256'])
(OUT/'caller.stdout.log').write_bytes(stdout);(OUT/'caller.stderr.log').write_bytes(stderr)
row['accepted']=row.get('exit_code')==0 and row['terminal_confirmed'] and row['candidate_unchanged'] and (OUT/'native-caller-result.json').exists()
(OUT/'caller-process.json').write_text(json.dumps(row,indent=2)+'\n','utf-8');print(json.dumps(row),flush=True)
if not row['accepted']:raise SystemExit(1)
