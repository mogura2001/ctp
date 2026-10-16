"""Finite C4 copy/deltas only; alias is NOT created in the game path here."""
from pathlib import Path
import json,hashlib,shutil,difflib,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;OLD=OUT.parent/'c3';ROOT=OUT.parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()
assert not (OUT/'manifest.json').exists(),'Preserve existing preparation'
for folder in ['backups','candidate','protected-backups']:shutil.copytree(OLD/folder,OUT/folder)
for filename in ['original_core.py','participants.json']:shutil.copyfile(OLD/filename,OUT/filename)
m=json.loads((OLD/'manifest.json').read_text('utf-8'));m['state']='C4_SOURCE_ONLY_NO_ALIAS_INSTALL_START_RPM'
alias='CTP-proef/ctp_program/ctp/save/games/Julius/000-U30-40-START-T0'
assert not (ROOT/alias).exists()
m['T0_alias']=dict(path=alias,source='CTP-proef/ctp_program/ctp/save/games/Julius/QUOTA-START-T0',sha256=m['T0_sha256'],existed_before=False,ownership='C4_UI_LOAD_ALIAS_ONLY',create='Only after future root release and fresh successful count0, record own preimage before copy',remove='Only own original-hash alias after exit/count0/archival/release restore; otherwise preserve')
m['input_manifests'].append(dict(path='ONTWERP/UI-LAADROUTE-U30-40.md',sha256=sha((ROOT/'ONTWERP/UI-LAADROUTE-U30-40.md').read_bytes())))
(OUT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n','utf-8')
s=(OLD/'Uitbreiding.ps1').read_text('utf-8').replace('C3-ROOT-VRIJGAVE','C4-ROOT-VRIJGAVE').replace('C3 source','C4 source').replace('First C3','First C4').replace('C3 root','C4 root').replace('UITBREIDING-20261013-C3','UITBREIDING-20261013-C4').replace('uitbreiding-20261013-c3','uitbreiding-20261013-c4')
s=s.replace(' public delegate bool Callback',' [DllImport("user32.dll")]public static extern bool SetProcessDPIAware();\n public delegate bool Callback',1)
s=s.replace("'@\nfunction Elapsed", "'@\n[ExpansionWindow]::SetProcessDPIAware() | Out-Null\nfunction Elapsed",1)
s=s.replace('$limit=if($ForClose){470}else{465}','$limit=if($ForClose){470}else{420}')
alias_code=(OUT/'alias-functions.ps1.fragment').read_text('utf-8')
s=s.replace('function RestoreOwnInstallation {',alias_code+'\nfunction RestoreOwnInstallation {')
s=s.replace("JsonFile @{at=(Get-Date).ToString('o');install_attempted=$true;arm=$Arm} 'execution.json'", "JsonFile @{at=(Get-Date).ToString('o');install_attempted=$true;arm=$Arm} 'execution.json'\n CreateOwnT0Alias")
s=s.replace("throw 'Profile changed; preserve current bytes for review.'}\n", "throw 'Profile changed; preserve current bytes for review.'}\n RemoveOwnT0Alias\n",1)
s=s.replace("  Copy-Item -LiteralPath (Join-Path $workspace 'PROEVEN\\automatisering\\ctp-window.png') -Destination (Join-Path $armDir ($Label+'.png'))", "  $imagePath=Join-Path $armDir ($Label+'.png')\n  Copy-Item -LiteralPath (Join-Path $workspace 'PROEVEN\\automatisering\\ctp-window.png') -Destination $imagePath\n  $physicalState=OwnState $started -BindWindow\n  Add-Type -AssemblyName System.Drawing\n  $picture=[Drawing.Image]::FromFile($imagePath)\n  try{JsonFile @{image=$imagePath;pixel_width=$picture.Width;pixel_height=$picture.Height;physical_window=$physicalState;coordinate_system='SetProcessDPIAware physical pixels; inspect original image or explicitly rescale';at=(Get-Date).ToString('o')} ($Label+'-physical-bounds.json')}finally{$picture.Dispose()}")
(OUT/'Uitbreiding.ps1').write_text(s,'utf-8')
r=(OLD/'Lees-Uitbreiding.py').read_text('utf-8').replace('C3-ROOT-VRIJGAVE','C4-ROOT-VRIJGAVE').replace('C3 source','C4 source').replace('First C3','First C4')
(OUT/'Lees-Uitbreiding.py').write_text(r,'utf-8')
for name,new in [('Uitbreiding.ps1',s),('Lees-Uitbreiding.py',r),('manifest.json',(OUT/'manifest.json').read_text('utf-8'))]:
 (OUT/(name+'.diff')).write_text(''.join(difflib.unified_diff((OLD/name).read_text('utf-8').splitlines(True),new.splitlines(True),fromfile='preserved C3/'+name,tofile='owned C4/'+name)),'utf-8')
(OUT/'C4-ROOT-VRIJGAVE.json').write_text(json.dumps(dict(allowed=False,baseline_allowed=False,candidate_sha256='f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810',sources=[],state='SOURCE_ONLY_NO_ALIAS_CREATE_OR_LIVE'),indent=2)+'\n','utf-8')
print(json.dumps(dict(stage=m['state'],alias_on_game_path_exists=False,game_file_mutations=0)))
