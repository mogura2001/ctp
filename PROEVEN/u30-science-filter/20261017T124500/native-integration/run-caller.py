"""One hidden, bounded own helper process; no engine process or installation."""
from pathlib import Path
import datetime, hashlib, json, subprocess, time
OUT=Path(__file__).resolve().parent;PACK=OUT.parent;ROOT=OUT.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2)+'\n','utf-8')
assert not (OUT/'caller-process.json').exists(), 'One run only; preserve attempts'
assert sha(OUT/'SOURCE-CHECKPOINT.json')=='165369aac4b1690b8fd8a2729becdde786ac19a3016684595a3e431edeca7147'
for x in json.loads((OUT/'SOURCE-CHECKPOINT.json').read_text())['files']:
    path=ROOT/x['repository_path'] if 'repository_path' in x else OUT/x['path']
    assert sha(path)==x['sha256'],str(path)
for x in json.loads((PACK/'BUILD-PINS.json').read_text())['files']:
    assert sha(PACK/x['path'])==x['sha256'],x['path']
files=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file():files.append(dict(path=p.relative_to(OUT).as_posix(),size=p.stat().st_size,sha256=sha(p)))
write('NATIVE-RUNTIME-CHECKPOINT.json',dict(
    stage='COMPILED_NOT_EXECUTED',checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    source_checkpoint_sha256=sha(OUT/'SOURCE-CHECKPOINT.json'),
    candidate_sha256=sha(PACK/'U30-40.prepared.dll'),
    manifest_sha256=sha(PACK/'candidate-manifest.json'),
    compiled_assembly_sha256=sha(OUT/'NativeCaller.dll'),
    helper_bins=len(list((OUT/'helper').glob('*.bin'))),files=files))
row=dict(stage='ONE_OWN_NATIVE_HELPER',started_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
         timeout_seconds=45,hidden=True,owned_process=True,
         runtime_checkpoint_sha256=sha(OUT/'NATIVE-RUNTIME-CHECKPOINT.json'))
start=time.monotonic()
p=subprocess.Popen(['C:/Windows/SysWOW64/WindowsPowerShell/v1.0/powershell.exe',
    '-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(OUT/'native-caller.ps1')],
    stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
row['pid']=p.pid
try:
    stdout,stderr=p.communicate(timeout=45);row['exit_code']=p.returncode
except subprocess.TimeoutExpired:
    row['timeout']=True;p.kill();stdout,stderr=p.communicate(timeout=10)
    row['exit_code_after_timeout']=p.returncode
row.update(ended_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
           elapsed_seconds=round(time.monotonic()-start,3),terminal_confirmed=p.poll() is not None,
           candidate_sha256=sha(PACK/'U30-40.prepared.dll'),
           candidate_unchanged=sha(PACK/'U30-40.prepared.dll')=='0ebafb11e08bc7dca74291dd8a8e9ea94441af09602ae2d94710217f19eabad9')
(OUT/'caller.stdout.log').write_bytes(stdout);(OUT/'caller.stderr.log').write_bytes(stderr)
lines=stdout.decode('utf-8-sig',errors='replace').splitlines()
row['cleanup_confirmed']='cleanup=True' in lines
row['pass_labels']=[s[5:] for s in lines if s.startswith('PASS ')]
row['native_calls_attempted']=len([s for s in lines if s.startswith('caller ')])
row['accepted']=row.get('exit_code')==0 and row['terminal_confirmed'] and row['cleanup_confirmed'] and row['candidate_unchanged'] and (OUT/'native-caller-result.json').exists()
row['engine_science_measured']=False;row['actual_deficit_measured']=False;row['gameplay_measured']=False
write('caller-process.json',row);print(json.dumps(row),flush=True)
if not row['accepted']:raise SystemExit(1)
