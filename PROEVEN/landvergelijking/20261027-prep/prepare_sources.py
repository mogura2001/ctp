"""Finite source preparation only. Never imports reader/main or starts a process."""
from pathlib import Path
import ast, difflib, hashlib, json
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[3]
C4=ROOT/'PROEVEN/landvergelijking/20261027'
C5=Path(__file__).resolve().parent
OLD=ROOT/'PROEVEN/uitbreiding-lang/20261022T122400'
RUN=ROOT/'PROEVEN/pad-lokaal-onbekend/20261026c-host'
PREP=ROOT/'PROEVEN/pad-lokaal-onbekend/20261026c-host-prep'
REL='eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'
CAND='df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e'
MAN='5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152'
PART='PROEVEN/landbenchmark/20261027/participants.json'
SAVE='PROEVEN/landbenchmark/20261027/UITBREIDING-LAND-T0.original'
VERSION='VERSIES/uitbreiding-2026-10-22-T100'
def read(p):return p.read_text('utf-8-sig')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
def clone(src,dst,fn=lambda s:s):
 old=read(src);new=fn(old);write(dst,new)
 write(dst.with_name(dst.name+'.diff'),''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(src.relative_to(ROOT)),tofile=str(dst.relative_to(ROOT)))))
C4.mkdir(parents=True,exist_ok=True)
clone(OLD/'scope.py',C4/'scope.py',lambda s:s.replace('PROEVEN/selectie-pad-diagnose/20261020T192500/reader/participants.json',PART))
def reader(s):
 old="        if args.variant=='U30-40':\n            per_civ,shared=native_expansion_state(read,eb,ab,participants,binding)\n            for row in state['civilizations']:row.update(per_civ[row['civ_id']])\n            state['shared_last_pass']=shared"
 new="        per_civ,shared=native_expansion_state(read,eb,ab,participants,binding)\n        for row in state['civilizations']:row.update(per_civ[row['civ_id']])\n        state['shared_last_pass']=shared"
 assert old in s
 return s.replace(old,new)
clone(OLD/'Lees-Duur.py',C4/'Lees-Duur.py',reader)
def runner(s):
 s=s.replace("ValidateSet('local4')","ValidateSet('release-v1','U30-40')")
 s=s.replace('$completionFolder=$PSScriptRoot;$package=$PSScriptRoot;$armDir=Join-Path $package $Arm','$package=$PSScriptRoot;$armDir=Join-Path $package $Arm;$completionFolder=$armDir')
 s=s.replace("$hostDir=Join-Path $package 'host'","$hostDir=Join-Path $armDir 'host'")
 s=s.replace("$expectedAI='acfeec096ea39e1ff38435214769f4d24074e640b856e08d1c82cc09ea7a4984'",f"$expectedAI=if($Arm -ceq 'U30-40'){{'{CAND}'}}else{{'{REL}'}}")
 s=s.replace('0a10a7c7f1af1ecd0d71e549296a4e31ea850f100812515d519fa4055e497d4d',MAN)
 s=s.replace("($Arm -ceq 'local4')","($Arm -ceq 'U30-40')").replace("$approval.arm -cne 'local4'","$approval.arm -cne $Arm")
 return s.replace('PROEVEN/selectie-pad-diagnose/20261020T192500/reader/participants.json',PART)
clone(RUN/'Pass-Duur.ps1',C4/'Pass-Duur.ps1',runner)
clone(RUN/'HOST-PLAN.json',C4/'HOST-PLAN.json')
def common(s):
 s="param([Parameter(Mandatory=$true)][ValidateSet('release-v1','U30-40')][string]$Arm)\n"+s
 s=s.replace("$c4=Join-Path $workspace 'PROEVEN/pad-lokaal-onbekend/20261026c-host';$hostDir=Join-Path $c4 'host'","$c4=Join-Path $workspace 'PROEVEN/landvergelijking/20261027';$armDir=Join-Path $c4 $Arm;$hostDir=Join-Path $armDir 'host'")
 s=s.replace("$package=$PSScriptRoot;$hostDir=Join-Path $workspace 'PROEVEN/pad-lokaal-onbekend/20261026c-host/host'","$package=$PSScriptRoot;$c4=Join-Path $workspace 'PROEVEN/landvergelijking/20261027';$armDir=Join-Path $c4 $Arm;$hostDir=Join-Path $armDir 'host'")
 s=s.replace("Join-Path $package 'ROOT-HOST.json'","Join-Path (Join-Path $package $Arm) 'ROOT-HOST.json'")
 s=s.replace("$gate.arm -cne 'local4'","$gate.arm -cne $Arm").replace("$gate.run_id -cne 'pad-local4-20261026c-host'","$gate.run_id -cne ('land-20261027-'+$Arm)")
 return s.replace('acfeec096ea39e1ff38435214769f4d24074e640b856e08d1c82cc09ea7a4984',CAND)
def start(s):
 s=common(s).replace("'050bb93ff333ef7cd1a76631ee98e167cedc4996074d9a2d4b40cd26e1665da6'","$gate.c4_source_pins_sha256")
 s=s.replace("$candidate=Join-Path $workspace 'PROEVEN/pad-lokaal-onbekend/20261023T155300-build/U30-40.prepared.dll'",f"$candidate=if($Arm -ceq 'U30-40'){{Join-Path $workspace '{VERSION}/files/CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll'}}else{{Join-Path $workspace 'PROEVEN/selectie-pad-diagnose/20261020T192500/reader/candidate/baseline/CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll'}}")
 s=s.replace(f"$candidateHash='{CAND}'",f"$candidateHash=if($Arm -ceq 'U30-40'){{'{CAND}'}}else{{'{REL}'}}")
 s=s.replace('PROEVEN/pad-lokaal-onbekend/20261023T155300-build/candidate-manifest.json',VERSION+'/manifest.json')
 s=s.replace("$plan=Get-Content (Join-Path $c4 'HOST-PLAN.json') -Raw|ConvertFrom-Json","$plan=Get-Content (Join-Path $c4 'HOST-PLAN.json') -Raw|ConvertFrom-Json\n$releasePins=$plan.config19\nif((Hash (Join-Path $workspace '"+VERSION+"/manifest.json')) -cne 'c665c92f19e37abe49d627a86070306b93519a7088399e90763a2a102a36e950' -or @($manifest.files).Count -ne 19){throw 'Exact tested package19 required'}\nforeach($row in $manifest.files){if((Hash (Join-Path $workspace ('"+VERSION+"/files/'+$row.path))) -cne $row.sha256){throw 'Package file mismatch'};if($row.path -cne 'CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll' -and (Hash (Join-Path $workspace $row.path)) -cne $row.sha256){throw 'Non-DLL package file differs'}}")
 s=s.replace('$manifest.release_pins','$releasePins')
 s=s.replace("$alias='CTP-proef/ctp_program/ctp/save/games/Julius/000-PAD-LOCAL4-20261026C-START-T0'","$alias=if($Arm -ceq 'U30-40'){'CTP-proef/ctp_program/ctp/save/games/Julius/000-LAND-R1-U30-T0'}else{'CTP-proef/ctp_program/ctp/save/games/Julius/000-LAND-R1-CONTROLE-T0'}")
 s=s.replace("$save='CTP-proef/ctp_program/ctp/save/games/Julius/QUOTA-START-T0'",f"$save='{SAVE}'")
 s=s.replace('8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26','a670867460bae5d8d9196856d5ca88163b0eff951e9a9db42a05b83ee38d2301')
 return s.replace('before180s and load/T0 before300s','before240s and load/T0 before360s')
clone(PREP/'Start-Monitored.ps1',C5/'Start-Monitored.ps1',start)
clone(PREP/'Close-Normally.ps1',C5/'Close-Normally.ps1',common)
def restore(s):
 s=common(s).replace("Join-Path $c4 'local4/ROOT-READER.json'","Join-Path $armDir 'ROOT-READER.json'").replace("Join-Path $c4 'ROOT-CONTROL.json'","Join-Path $armDir 'ROOT-CONTROL.json'")
 s=s.replace("$archiveA='CTP-proef/ctp_program/ctp/save/games/Julius/PAD-LOCAL4-20261026C-AUTOSAVE-A';$archiveB='CTP-proef/ctp_program/ctp/save/games/Julius/PAD-LOCAL4-20261026C-AUTOSAVE-B'","$archiveA='CTP-proef/ctp_program/ctp/save/games/Julius/LAND-R1-'+$Arm+'-AUTOSAVE-A';$archiveB='CTP-proef/ctp_program/ctp/save/games/Julius/LAND-R1-'+$Arm+'-AUTOSAVE-B'")
 return s
clone(PREP/'Restore.ps1',C5/'Restore.ps1',restore)
# Exact inherited provenance closure, plus actual reader imports and fixed package.
# Mutable root gates and installed/live files are deliberately outside source pins.
paths=set()
for manifest in (OLD/'SOURCE-PINS.json',ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500/reader/READER-PINS.json'):
 for row in json.loads(read(manifest))['sources']:
  p=row['path']
  if Path(p).name.startswith('ROOT-') or p.startswith('CTP-proef/'):continue
  paths.add(p)
paths.update([PART,SAVE,VERSION+'/manifest.json','ONTWERP/LANDVERGELIJKING-2026-10-27.md','PROEVEN/AUTOMATISERING.md'])
for row in json.loads(read(ROOT/(VERSION+'/manifest.json')))['files']:paths.add(VERSION+'/files/'+row['path'])
for p in (ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500').glob('*.py'):paths.add(p.relative_to(ROOT).as_posix())
for p in (ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500/reader').glob('*.py'):paths.add(p.relative_to(ROOT).as_posix())
for folder in (C4,C5):
 for p in folder.iterdir():
  if p.suffix in ('.py','.ps1','.diff') or p.name=='HOST-PLAN.json':paths.add(p.relative_to(ROOT).as_posix())
pins={'stage':'SOURCE_ONLY_ALL_RUNTIME_GATES_FALSE','historical_host_plan_is_backup':False,'sources':[{'path':p,'sha256':sha(ROOT/p)} for p in sorted(paths)]}
js(C4/'SOURCE-PINS.json',pins)
c4hash=sha(C4/'SOURCE-PINS.json')
paths.add((C4/'SOURCE-PINS.json').relative_to(ROOT).as_posix())
js(C5/'SOURCE-PINS.json',dict(pins,sources=[{'path':p,'sha256':sha(ROOT/p)} for p in sorted(paths)]))
for arm,digest in [('release-v1',REL),('U30-40',CAND)]:
 runid='land-20261027-'+arm
 js(C4/arm/'ROOT-READER.json',dict(allowed=False,control_allowed=False,variant=arm,pid=0,creation_filetime=0,run_id=runid,turn_min=0,turn_max=100,max_n=100,output_directory=str(C4/arm),ai_sha256=digest,manifest_sha256=MAN,source_pins_sha256=c4hash))
 control=json.loads(read(RUN/'ROOT-CONTROL.json'))
 for k in control:
  if k.startswith('review_'):control[k]=False if k in ('review_T1','review_T26') else None
 control.update(allowed=False,arm=arm,pid=0,creation_filetime=0,window=0,run_id=runid,source_pins_sha256=c4hash,start_sha256=None,window_sha256=None,accepted_T0_sha256=None)
 js(C4/arm/'ROOT-CONTROL.json',control)
 gate=json.loads(read(PREP/'ROOT-HOST.json'));gate.update(arm=arm,run_id=runid,source_pins_sha256=sha(C5/'SOURCE-PINS.json'),c4_source_pins_sha256=c4hash)
 js(C5/arm/'ROOT-HOST.json',gate)
write(ROOT/'ANALYSE/VOORTGANG-LANDBRON-27.md',datetime.now(ZoneInfo('Europe/Amsterdam')).isoformat()+' — Minimale C4/C5-bronnen voorbereid. Alle gates FALSE; geen game/native/UI/install. Statische syntax/scope/gettercontrole volgt; rootreview vóór hostvrijgave. Geen gameplayresultaat.\n')
