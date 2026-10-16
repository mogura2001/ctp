"""C3 source/staging only: own controller/reader copies and exact backups."""
from pathlib import Path
import sys,json,hashlib,difflib,datetime
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;PACK=OUT.parent;ROOT=PACK.parents[2]
OLD=ROOT/'PROEVEN/doel3/20261012T165300-baseline2';RELEASE=ROOT/'PROEVEN/doel3/20261012-release-v1'
sha=lambda b:hashlib.sha256(b).hexdigest()
BASE='eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890'
VARIANT='f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810'
def own_write(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists():assert path.read_bytes()==data,path
 else:path.write_bytes(data)
release=json.loads((RELEASE/'manifest.json').read_text('utf-8'))
manifest=dict(release);manifest['state']='C3_SOURCE_ONLY_NO_INSTALL_START_RPM';manifest['files']=[]
for row in release['files']:
 path=row['path'];raw=(ROOT/path).read_bytes();assert sha(raw)==row['variant_sha256'],path
 current=sha(raw);variant=(PACK/'U30-40.prepared.dll').read_bytes() if path.endswith('robotcom.dll') else raw
 own_write(OUT/'backups'/path,raw)
 for arm,data in [('baseline',raw),('variant',variant)]:own_write(OUT/'candidate'/arm/path,data)
 manifest['files'].append(dict(path=path,existed=True,before_sha256=current,baseline_sha256=current,variant_sha256=sha(variant)))
assert len(manifest['files'])==19
assert manifest['files'][-1]['variant_sha256']==VARIANT
manifest['protected']=[dict(path=r['path'],sha256=sha((ROOT/r['path']).read_bytes())) for r in release['protected']]
saves=sorted((ROOT/'CTP-proef/ctp_program/ctp/save').rglob('*'))
manifest['preserved_saves_before']=[]
for path in saves:
 if path.is_file():
  raw=path.read_bytes();relative=path.relative_to(ROOT).as_posix();own_write(OUT/'protected-backups'/relative,raw);manifest['preserved_saves_before'].append(dict(path=relative,sha256=sha(raw)))
assert len(manifest['preserved_saves_before'])==9
profile='CTP-proef/ctp_program/ctp/userprofile.txt';raw=(ROOT/profile).read_bytes();own_write(OUT/'protected-backups'/profile,raw)
manifest['profile_before']=dict(path=profile,sha256=sha(raw))
for path in manifest['T0_paths']:assert sha((ROOT/path).read_bytes())==manifest['T0_sha256']
manifest['proposal_sha256']='accf076e715b2aeed674b989fecd52fd608afa8a0cb739c2270265ec398bf12a'
manifest['input_manifests']=[dict(path='PROEVEN/uitbreiding-30-40/20261012T181500/candidate-manifest.json',sha256=sha((PACK/'candidate-manifest.json').read_bytes())),dict(path='PROEVEN/uitbreiding-30-40/20261012T181500/c2/C2-package.json',sha256=sha((PACK/'c2/C2-package.json').read_bytes()))]
manifest['baseline']='tested release-v1 B1+B2a-N30+B2b, never original'
manifest['variant']='release-v1 plus U30-40 candidate only'
manifest['max_arm_seconds']=480;manifest['reserve_seconds']=15
manifest['stage_limit']='variant only T0+oneT1 passive-human n, seven participants native+1; rootreview before moreturns/baseline'
manifest['created_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
if (OUT/'manifest.json').exists():manifest['created_at']=json.loads((OUT/'manifest.json').read_text('utf-8'))['created_at']
own_write(OUT/'manifest.json',(json.dumps(manifest,indent=2)+'\n').encode())
own_write(OUT/'participants.json',(OLD/'participants.json').read_bytes())
original=(OLD/'original_core.py').read_text('utf-8')
core=original.replace("ROOT = Path(__file__).resolve().parents[3]","ROOT = Path(__file__).resolve().parents[4]")
assert core!=original
own_write(OUT/'original_core.py',core.encode())
controller=(OLD/'Doel3.ps1').read_text('utf-8')
controller=controller.replace('Goal3Window','ExpansionWindow').replace('DOEL3-20261012T165300-baseline2','UITBREIDING-20261013-C3').replace('doel3-20261012T165300-baseline2','uitbreiding-20261013-c3')
controller=controller.replace("$variant=if($Arm -eq 'variant'){'B2a-N30-TECHNICAL'}else{'original'}","$variant=if($Arm -eq 'variant'){'U30-40'}else{'release-v1'}")
controller=controller.replace("$version=if($Arm -eq 'variant'){'N30'}else{'ORIGINAL'}","$version=if($Arm -eq 'variant'){'U30-40-N30'}else{'RELEASE-V1-N30'}")
controller=controller.replace("'3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44'","'"+BASE+"'")
# Archive source-version requirement needs variantcandidate, restorebasis BASE.
controller=controller.replace("required_dll_sha256=if($Arm -eq 'variant'){'"+BASE+"'}else{'"+BASE+"'}","required_dll_sha256=if($Arm -eq 'variant'){'"+VARIANT+"'}else{'"+BASE+"'}")
controller=controller.replace("'ONTWERP\\DOEL3-GAMEPLAYBEWIJS.md'","'ONTWERP\\UITBREIDING-30-40.md'")
controller=controller.replace('Lees-Doel3.py','Lees-Uitbreiding.py')
controller=controller.replace('$limit=if($ForClose){1790}else{1785}','$limit=if($ForClose){470}else{465}').replace('30min arm deadline','8min activation deadline').replace('-ge 1790','-ge 470')
# Controller can do nothing live until root creates exact-source authorization.
gate='''
$gatePath=Join-Path $package 'C3-ROOT-VRIJGAVE.json'
if(!(Test-Path -LiteralPath $gatePath)){throw 'C3 source only: no root activation release.'}
$gate=Get-Content -LiteralPath $gatePath -Raw -Encoding utf8|ConvertFrom-Json
if(!$gate.allowed -or $gate.candidate_sha256 -cne 'f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810'){throw 'C3 root release absent/disabled.'}
foreach($pin in $gate.sources){if((Get-FileHash -LiteralPath (Join-Path $package $pin.path) -Algorithm SHA256).Hash.ToLowerInvariant() -cne $pin.sha256){throw 'Released C3 source changed.'}}
if($Arm -eq 'baseline' -and !$gate.baseline_allowed){throw 'First activation is variant only; baseline needs later release.'}
if($Turn -notin @(0,1)){throw 'First C3 stage only T0/T1.'}
if($Action -eq 'Pass' -and $Turn -ne 1){throw 'Only the first native T1 pass is released.'}
'''
controller=controller.replace('$toolHash=',gate+'\n$toolHash=',1)
controller=controller.replace("Copy-Item -LiteralPath $source -Destination $target}","if((Hash $target) -ne $expected){Copy-Item -LiteralPath $source -Destination $target}}")
# Verify preserved named saves after autosave archival/default restore; never
# restore another user's named save or profile from preparation automatically.
after="""
 foreach($saved in $manifest.preserved_saves_before){if((Hash (Join-Path $workspace $saved.path)) -ne $saved.sha256){throw 'Protected named save changed; preserve for review.'}}
 if((Hash (Join-Path $workspace $manifest.profile_before.path)) -ne $manifest.profile_before.sha256){throw 'Profile changed; preserve current bytes for review.'}
"""
controller=controller.replace("if(@($checks|Where-Object{!$_.match}).Count){throw 'Restoration mismatch.'}","if(@($checks|Where-Object{!$_.match}).Count){throw 'Restoration mismatch.'}"+after)
controller=controller.replace(" foreach($pin in $manifest.protected){if((Hash (Join-Path $workspace $pin.path)) -ne $pin.sha256){throw 'Pre-run protected/current pin changed; no install.'}}", " foreach($pin in $manifest.protected){if((Hash (Join-Path $workspace $pin.path)) -ne $pin.sha256){throw 'Pre-run protected/current pin changed; no install.'}}\n foreach($saved in $manifest.preserved_saves_before){if((Hash (Join-Path $workspace $saved.path)) -ne $saved.sha256 -or (Hash (Join-Path (Join-Path $package 'protected-backups') $saved.path)) -ne $saved.sha256){throw 'Protected9saves/truebackup changed; no install.'}}\n if((Hash (Join-Path (Join-Path $package 'protected-backups') $manifest.profile_before.path)) -ne $manifest.profile_before.sha256){throw 'Protected profile truebackup changed; no install.'}")
own_write(OUT/'Uitbreiding.ps1',controller.encode())
for name,data in [('Doel3.ps1',controller),('original_core.py',core)]:
 before=(OLD/name).read_text('utf-8').splitlines(True);after=data.splitlines(True)
 own_write(OUT/(name+'.diff'),''.join(difflib.unified_diff(before,after,fromfile='readonly baseline2/'+name,tofile='owned C3/'+name)).encode())
own_write(OUT/'C3-ROOT-VRIJGAVE.json',(json.dumps(dict(allowed=False,baseline_allowed=False,candidate_sha256=VARIANT,sources=[],state='PREPARATION_ONLY_ROOT_RELEASE_REQUIRED'),indent=2)+'\n').encode())
print(json.dumps(dict(stage='SOURCE_STAGING_ONLY',release_files=19,preserved_saves=9,profile_backup=True,baseline=BASE,variant=VARIANT,live_actions=0)))
