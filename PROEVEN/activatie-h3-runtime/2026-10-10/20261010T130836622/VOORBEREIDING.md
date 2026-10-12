# H1-I T0-arm: voorbereiding, geen uitvoervrijgave

10 oktober 2026, 13:15 Europe/Amsterdam. Alleen H1-I / run-id `h1-20261010`. Frozen ontwerp H3-T0-HERVATTING.md SHA256 `21fcf7cadf2c459f99ed45047f612aba11fe98a0234d1d898c496d3e2f64ecec`. H3-arm niet voorbereid of vrijgegeven. Geen installatie, Start, GUI, live-reader of afwikkeling uitgevoerd.

Vier nieuwe scripts hergebruiken de eerder gereviewde H1-menu-/cleanupdelen. ParseFile zonder uitvoering: viermaal nul fouten, exacte hashes in parser.json. Start bevat preflight, vier afwezige outputs, vijftien pins, originele backup, tijdelijke H1-I, directe procesbinding, 180 seconden intro en één menu-Capture. Guard controleert budget, oorspronkelijke identiteit, enige civctp, gebonden HWND/eigenaar/focus en monotone livegrens met tien seconden reserve. Finish bevat de reeds bewezen modal-/herbindingspoort, één eigen CloseMainWindow, maximaal tien seconden observatie, events en herstel alleen na bewezen exit en verse succesvolle alle-processen-count0. Het bestaande C0-tool en de observer blijven ongewijzigd.

Voor rootreview, pas na afzonderlijke vrijgave gebruiken:

```powershell
$arm = 'C:\GIT\ctp\PROEVEN\activatie-h3-runtime\2026-10-10\20261010T130836622\H1-I'
& powershell.exe -NoProfile -File "$arm\Start-H1-T0.ps1"
& powershell.exe -NoProfile -File "$arm\Guard-H1-T0.ps1" -Purpose Gui
# Iedere volgende GUI-actie pas na werkelijk bekeken actuele Capture.
& powershell.exe -NoProfile -File "$arm\Read-H1-Snapshot.ps1" -SnapshotLabel A
& powershell.exe -NoProfile -File "$arm\Guard-H1-T0.ps1" -Purpose Pass
# Eén n uitsluitend na geldig A, rustige T0-kaart en actuele scherm-/focuscontrole.
& powershell.exe -NoProfile -File "$arm\Read-H1-Snapshot.ps1" -SnapshotLabel B
& powershell.exe -NoProfile -File "$arm\close-mainwindow\Finish-H1-T0.ps1"
```

De GUI-route wordt niet vooraf geklikt: herkenbaar menu, Single Player/load, Load Game, Julius/QUOTA-START-T0, zichtbare Load, rustige kaart 4000 BC. Voor iedere afzonderlijke actie een nieuwe schermwaarneming en guard; cursorcoördinaten uitsluitend uit die waarneming. Geen vaste historische coördinaten. Eén n pas na geldig A; datum/passbewijs naar 3950 BC vóór B. Rejected/instabiel A betekent geen n/B; geen tweede n. Labels hieronder bewijzen geen beurt. Bij onbekend scherm, identiteit of proces: handen af en eigen afwikkeling volgens poorten. Na B of fout direct de vooraf gereedstaande Finish; geen codevoorbereiding tijdens live. Geen nieuwe GUI/read/pass vanaf 470 seconden; totale livegrens 480 seconden inclusief maximaal tien seconden afwikkeling.

Concrete observerargumenten van de wrapper (toekomstige PID uit eigen start-record, geen oude PID):

```powershell
$py = 'C:\Users\Stephan\AppData\Local\Programs\Python\Python312\python.exe'
$reader = 'C:\GIT\ctp\PROEVEN\ai-uitlezen\Lees-Onderzoeksactivatie.py'
$boundPid = [string](Get-Content "$arm\start-record.json" -Raw -Encoding utf8 | ConvertFrom-Json).pid
$a = 'C:\GIT\ctp\PROEVEN\ai-uitlezen\activatie-h3-runtime-20261010-h1-A.json'
$b = 'C:\GIT\ctp\PROEVEN\ai-uitlezen\activatie-h3-runtime-20261010-h1-B.json'
$aArgs = @($reader,'--pid',$boundPid,'--variant','H1-I','--run-id','h1-20261010','--snapshot-label','A','--turn','0','--pass-label','T0-to-T1','--output',$a)
$bArgs = @($reader,'--pid',$boundPid,'--variant','H1-I','--run-id','h1-20261010','--snapshot-label','B','--turn','1','--pass-label','T0-to-T1','--output',$b,'--before',$a)
# Alleen illustratie: wrapper voert na zijn guard één van deze argumentarrays uit.
# & $py @aArgs
# & $py @bArgs
```

Argumentarrays vermijden Python -c en samengestelde shellquoting; pad/run/passlabels zijn ASCII. De observer schrijft JSON met ASCII-escaped tekst en leest before als UTF-8-sig. De wrapper bewaart concrete argv/stdout/exitstatus en kopieert geproduceerde bronoutput bytegelijk naar eigen A.json/B.json met beide hashes. B gebruikt uitsluitend de eigen A in ai-uitlezen. Vooraf waren alle vier 10-oktober H1/H3 A/B-bronoutputs afwezig; startup controleert dit opnieuw. Geen overwrite/retry.

Codehashes:

- Start-H1-T0.ps1: `add21943b503b72c96acf148292f41fc0d655772b816d4c6c19d63245e540677`
- Guard-H1-T0.ps1: `6439e4a3ae35b8c667b80b2c709852f8e8a2fd3df75bd9c5ce668999735d5987`
- Read-H1-Snapshot.ps1: `25acc89ee6117509d508a33db7c3846f14fa900695cf9b7e9657f3567bd244d1`
- close-mainwindow/Finish-H1-T0.ps1: `5037e5ef4155a07359a27cb0d63384802b8263003cadfde37ee308b5f446d51d`

Laatste eigen verse budgetcontrole 13:14:31: week86%, vijfuur10%, state ok. Rootreview van volledige code/CLI en afzonderlijke livevrijgave ontbreken. Uitvoerder stopt na deze voorbereidingsoplevering; pc blijft aan. Geen gameplay-, callback- of H3-conclusie.

## Routinecorrecties na budgetreset

10 oktober2026,18:02 Europe/Amsterdam. Hervatting uitsluitend drie rootreviewpunten; geen livevrijgave. Oude scripts/parser/verslag bytegelijk bewaard in routinecorrecties-before-20261010T180100 met manifest.json. Start-H1-T0.ps1 ongewijzigd (add21943...40677); oude parser.json blijft historisch. Actuele parser-routinecorrecties.json: drie gewijzigde scripts ParseFile nul fouten, geen uitvoering. routinecorrecties.diff toont uitsluitend deze delta.

Guard bindt na CIM ook echte Process.MainModule.FileName en StartTime aan exact start-record.exe/creation. Read controleert succesvolle JSON.instance.pid, creationtime_filetime via FromFileTimeUtc naar Unixmilliseconden en exact executable; mismatch werpt fout, archive blijft bytegelijk met instance_verified=false/procedure_accepted=false. Geen n na die fout; B-wrapper weigert onverifieerd eigen A-archive. Observer zelf ongewijzigd.

Finish checkt de470sgrens opnieuw na laatste binding en called_at, direct vóór callmarkering/Close. Voor en na iedere observatie-CIM en rond retainedProcess-exitstatus controleert dezelfde monotone480s- en10sgrens; late query wordt gemarkeerd en werpt fout vóór exitacceptatie. Verse herstelquery heeft bovendien vóór/na de480sgrens; bij late query geen herstelmutatie. OS-calls kunnen laat terugkeren: dat wordt geweigerd bewijs, geen uitgestelde normale-exitclaim.

Actuele SHA256:
- Guard-H1-T0.ps1:250c38402d22b54c872c4aed6c77a6b51f583d593b39b7d7f6731617c3886bdc
- Read-H1-Snapshot.ps1:dcb6ea8de597cef4d1c8fd10eabed7c233e06206a1ed89b026d3a4f8655cc242
- close-mainwindow/Finish-H1-T0.ps1:31d0d33a5c7f58b5386c40735e9c1f582f098151d2c3274ed394acb27d921728

Concrete CLI hierboven blijft gelijk. Laatste eigen verse budget18:01:51 week84/vijfuur98 stateok, gewijzigde reset1791665936 bevestigd. Geen installatie/Start/GUI/live-reader/close/pcactie uitgevoerd. Uitvoerder gestopt voor rootreview van deze delta; geen eigen liveactie.
