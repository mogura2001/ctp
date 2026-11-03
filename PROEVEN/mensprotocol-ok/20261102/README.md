# Mensprotocol OK: afgebakende C0

Alleen voorbereiding voor rootreview; Prepare/start/invoer zijn nog niet uitgevoerd. B: ONTWERP/MENSELIJKE-DEFENSIEPROTOCOL-2026-10-28.md, volledig gelezen. Geen nieuwe strategie of AI-wijziging. Ownership: deze map en PROEVEN/VOORTGANG-MENSPROTOCOL-C-02.md. PROJECTSTATUS/TUSSENDOELEN blijven van root.

Bron exact PROEVEN/land-stad-defensie/20261028/AUTOSAVE-after, 159906 bytes, SHA256 522b829d517b1d9e7d0f96f13632118aaeee59c70b31655ac54c8950bd819b9e. Eigen alias 000-MENSPROTOCOL-OK-20261102-T0; c6ba UITBREIDING-LAND-STAD-T0 blijft beschermd in de 38 saves. Arm uitsluitend control: geen kandidaatteksten, manifestinstallatie, DLL-wijziging, wereldingreep of instellingenwijziging. DLL eb6; executable b1b5256f volgens live-baseline. Helpers afgeleid van wondergewicht-host/20261030; exacte diffs hier. Geen nieuwe reader/geheugenvelden.

Prepare controleert bron/pins/count0, volledige aidata118/save38-inventaris en alle162baselinehashes; maakt alle162backups met hashcontrole en pas daarna before.json/alias. Herstel vereist count0, dezelfde inventaris (alleen eigen alias extra), alle backuphashes en uitsluitend verwachte gewijzigde AUTOSAVE-Julius/userprofile.txt. Archiveert die wijzigingen vóór herstel; onverwachte bestanden/waarden stoppen het herstel. Eigen alias is exact begrensd onder CTP-proef/save en wordt uitsluitend bij hashgelijkheid verwijderd; alle162hashes/full118/full38 eindcontrole. CTP-og en bestaande bronnen worden niet beschreven.

Na expliciete root-GO: verse budgetcheck, actuele computer-use-skill en PROEVEN/AUTOMATISERING.md lezen, cd E: ready/CCTP + PowerISO-imagepath controleren. Geen skyappapproval. Beheer-Proef.ps1 -Mode Prepare; daarna uitsluitend via PROEVEN/Bedien-CTP.ps1 -Action Start starten. Registreer direct eigen proces met dit bekende patroon, vóór enige Stap-invoer:

```powershell
$g=@(Get-Process civctp -ErrorAction Stop)
if($g.Count -ne 1){throw 'Expected own single instance'}
$g=$g[0]
$exe=Join-Path (Get-Location) 'CTP-proef/ctp_program/ctp/civctp.exe'
if($g.Path -cne $exe){throw 'Unexpected executable'}
$meta=Get-CimInstance Win32_Process -Filter "ProcessId=$($g.Id)"
[ordered]@{pid=$g.Id;creation_filetime=$g.StartTime.ToUniversalTime().ToFileTimeUtc();creation_utc_ms=([DateTimeOffset]$meta.CreationDate.ToUniversalTime()).ToUnixTimeMilliseconds();start_utc=$g.StartTime.ToUniversalTime().ToString('o');path=$g.Path;window=$g.MainWindowHandle.ToInt64()} | ConvertTo-Json | Set-Content PROEVEN/mensprotocol-ok/20261102/control/start.json -Encoding UTF8
```

Laadroute volgens bestaande 1N-host: zichtbaar hoofdmenu, Single Player, Load, Julius, eigen alias selecteren, Save-veld controleren, dan OK. Zwart intro/focus alleen bewijst geen menu. Stap-Proef gebruikt uitsluitend Bedien-CTP, bindt exact pad/PID/fullFILETIME/window, controleert vóór iedere input budget en foreground-capture, hercontroleert identiteit/window/deadline, bewaart actie/capturelogs. Vanaf780s geen input, vanaf900s geen capture; vóór900s normaal sluiten. Iedere stap unieke naam, nooit blinde herhaling. Capture is readonly. Key uitsluitend n/{ENTER}/f. n vereist visuele no-modalbevestiging en CreateNew N1-consumed vóór invoer; f vereist zichtbare Warrior-op-Rome en CreateNew F1. ResearchOK vereist zichtbare Stone Working-selectie gelijk aan CHANGE TO, CreateNew RESEARCH-OK-consumed, en klikt uitsluitend de zichtbare OK. Die operatorasserties zijn geen schermevidence; bewaar en inspecteer steeds de beelden.

Verwacht geladen3850BC/Warrior op Rome. Alleen zichtbare actieve Warrior: ENTER voor selectie indien nodig, type/positie bevestigen, eenmaal f; GUI-respons vastleggen. Rome-queue controleren: bij Warrior/nietleeg niets wijzigen, uitsluitend bij zichtbaar leeg normaal Warrior aanvullen volgens B (geen Rush). Voor n panels dicht/human1/geen modal. Maximaal1n. Na n verwacht3800BC, Domestication ontdekt en RESEARCH/Stone Working zichtbaar voorgeselecteerd plus CHANGE TO Stone Working. Geen entry kiezen. Alleen bij eenduidige overeenkomst eenmaal Action ResearchOK -ConfirmedResearchStoneWorking op de zichtbare OK. Controleer modalsluiting en actieve onderzoeksnaam; queue en fortify-UI alleen zover zichtbaar. Geen extra n, onderzoekslijstkeuze, wetenschap/regering, verplaatsing of andere productie. Onverwachte modal/resultaat stopt en gaat terug B. Maximaal2 informatiemeldingen per grens elk eenmaal volgens B; geen n terwijl modal open. Reader kan pauzeverwerking tonen: uitsluitend readonly resample na toegestane OK, nooit N opnieuw sturen.

Voor/nasample: bestaande ongewijzigde PROEVEN/wondergewicht/20261030/Lees-Wondergewicht.py. De zevenAI/participants.json en alle107C4pins zijn exact gepind. Alleen unieke mensprotocol-20261102-*.json in de bestaande C4map schrijven na GO, nooit oude output overschrijven. Commandopatroon met eigen start.json:

```powershell
$s=Get-Content PROEVEN/mensprotocol-ok/20261102/control/start.json -Raw|ConvertFrom-Json
# Before is label0, after label1; --turn is ONLY supplied metadata, not measured native round.
& 'C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe' PROEVEN/wondergewicht/20261030/Lees-Wondergewicht.py --pid $s.pid --creation-filetime $s.creation_filetime --wonder-arm control --variant B2a-N30-TECHNICAL --run-id MENSPROTOCOL-OK-20261102 --snapshot-label BEFORE --turn 0 --pass-label human-3850BC --manifest C:/GIT/ctp/PROEVEN/wondergewicht/20261030/participants.json --output C:/GIT/ctp/PROEVEN/wondergewicht/20261030/mensprotocol-20261102-before.json
# Repeat readonly with AFTER / --turn 1 / human-3800BC / unique mensprotocol-20261102-after[-resample].json.
```

Geen begin-native-round gokken. Vergelijk uitsluitend gemeten AI processed_round voor/na en stable_twice/instancebinding; UI3850→3800 is datummaat. Historische weight30000-expectation FAIL bij control is normale metadata; daadwerkelijke118baseline-teksten en bestaande control33-lijstverwachting zijn leidend. Geen gameplayverbetering/100beurtenoverleving afleiden.

Normaal CloseMainWindow eenmaal op exact eigen identiteit, maximaal korte waits en count0 bevestigen; geen forcekill. Daarna Beheer-Proef.ps1 -Mode Restore, bron/alias/162/full118/full38 rapporteren, pc aan. Stop bij budget five<=5/week<=10; stale/unknown eenmaal opnieuw checken, geen lang pakket starten met unknown. Afzonderlijke acceptatie voor queue, OK-afhandeling en fortifyopdracht. Nog niets in gameplay gemeten binnen deze opdracht.
