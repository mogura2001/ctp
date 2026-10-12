"""SOURCE ONLY: finite 18-case own-x86-subprocess runner; no game access or installation."""
import argparse, hashlib, json, os, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PYTHON=Path('C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe')
WORKSPACE=Path('C:/GIT/ctp')
PS=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def budget():
 command=[str(PYTHON),str(WORKSPACE/'PROEVEN/Controleer-Weekbudget.py'),'--thread','01a0f7b4-4751-7513-b510-3835ce43f47d']
 result=None
 for attempt in range(2):
  result=subprocess.run(command,capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
  if result.returncode!=2:break
 if result.returncode not in (0,25):raise RuntimeError('Budget stop/unknown; checkpoint only: '+result.stdout)
 return json.loads(result.stdout)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--case',required=True)
 args=parser.parse_args();approval=ROOT/'C3-ROOT-VRIJGAVE.json'
 if not approval.is_file():raise RuntimeError('C2 source-only: missing root C3 execution approval')
 approved=read(approval);plan=read(ROOT/'cases.json')
 assert approved['native_execution_approved'] is True
 assert hashfile(ROOT/'cases.json')==approved['plan_sha256']
 for pin in approved['reviewed_source_pins']:assert hashfile(ROOT/pin['path'])==pin['sha256'],pin['path']
 cases=[c for c in plan['cases'] if c['id']==args.case];assert len(cases)==1,'one of 18 pinned cases required'
 case=cases[0];out=ROOT/'results';out.mkdir(exist_ok=True)
 record=out/(args.case+'.runner.json');assert not record.exists(),'no runner retry/overwrite'
 assert not any((out/(args.case+suffix)).exists() for suffix in ['.json','.trace','.stdout','.stderr'])
 state={'case':args.case,'pass':False,'own_subprocess_only':True,'timeout_seconds':20,'byte_limit_each_output':4194304,'budget_before':budget()}
 command=[str(PS),'-NoProfile','-File',str(ROOT/'native.ps1'),'-CaseId',args.case];state['command']=command
 started=time.monotonic()
 try:
  with (out/(args.case+'.stdout')).open('xb') as stdout,(out/(args.case+'.stderr')).open('xb') as stderr:
   proc=subprocess.Popen(command,stdout=stdout,stderr=stderr,cwd=ROOT,creationflags=subprocess.CREATE_NO_WINDOW)
   state['own_created_pid']=proc.pid
   while proc.poll() is None:
    exceeded=time.monotonic()-started>=20
    oversized=any(p.exists() and p.stat().st_size>4194304 for p in [out/(args.case+s) for s in ['.json','.trace','.stdout','.stderr']])
    if exceeded or oversized:
     # Only the process created by this Popen/retained Windows handle, never another PID or a game.
     proc.kill();state['own_subprocess_terminated_for_bound']=True
     state['failure_reason']='TIMEOUT' if exceeded else 'OUTPUT_BOUND'
     proc.wait(timeout=3);break
    time.sleep(0.1)
   state['exit_code']=proc.returncode
  result=out/(args.case+'.json')
  state['elapsed_seconds']=time.monotonic()-started
  state['native_case_pass']=state['exit_code']==0 and not state.get('own_subprocess_terminated_for_bound',False) and result.is_file() and read(result).get('pass') is True
  if result.exists():state['result_sha256']=hashfile(result)
  try:
   state['budget_after']=budget()
   state['pass']=state['native_case_pass']
  except Exception as exc:
   state['budget_after_error']=str(exc)
   state['checkpoint_state']='BUDGET_STOP_OR_UNKNOWN_NO_NEXT_CASE'
   state['pass']=False
 finally:
  record.write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(state,indent=2));return 0 if state['pass'] else 2
if __name__=='__main__':
 try:sys.exit(main())
 except Exception as exc:print(str(exc),file=sys.stderr);sys.exit(2)
