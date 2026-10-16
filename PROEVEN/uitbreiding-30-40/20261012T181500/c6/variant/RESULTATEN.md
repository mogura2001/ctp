# C6: zichtbare aliasselectie, normaal gesloten vóór save-load

14 oktober 2026, 11:49 Europe/Amsterdam. Eén afzonderlijk vrijgegeven C6-variantarm uitgevoerd en gestopt. Hoofdmenu, Single Player, Load Game, Julius en eigen aliasselectie zijn werkelijk zichtbaar gecontroleerd. Geen OK, save-load, RPM, T0, n of T1 uitgevoerd. Nieuwe combinatie/produceractivatie en gameplayverbetering blijven onbewezen; geen tweede start.

Eigen preflightbudget11:39:48: bron09:39:38UTC/leeftijd9,8s, vijf26/week55/stateok. Succesvolle verse allcount0 op11:39:52 (`../prestart-process.json`). Eigen alias gemaakt11:40:05, bron en alias bytegelijk aan QUOTA-START-T0 SHA `8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26`. Tijdelijke U30-DLL `f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810`; sciencekandidaat niet gebruikt.

Proces PID28912/exact `C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe`, creation_utc_ms1791970807281 (11:40:07.281 Amsterdam), gebonden HWND329816. Bekende intro zonder invoer afgewacht; stabiele eigen window-/foregroundbinding. Alle captures hieronder hebben dezelfde PID/creation/HWND/foregroundbinding en passende oorspronkelijke PNG-/fysiekeboundsafmetingen.

| Eigen opname | Tijd Amsterdam / controllerelapsed | Daadwerkelijk zichtbaar resultaat |
| --- | --- | --- |
| menu.png | 11:43:20.746 /194,9997s | Hoofdmenu1920×1080, Single Player leesbaar. |
| singleplayer.png | 11:44:09.067 /243,3199s | Single Player1920×1080, Load Game leesbaar. |
| loadgame.png | 11:44:49.548 /283,8044s | Load Game2171×1080, Alexan en Julius zichtbaar. |
| julius.png | 11:45:37.989 /332,2321s | Game:Julius, unieke eigen000-U30-40-START-T0 bovenaan; geen scroll. |
| alias-selected.png | 11:46:27.177 /381,4366s | Game:Julius, Save:000-U30-40-START-T0, Julius Caesar/Romans en geselecteerde rij zichtbaar. |

Vier menuklikken via ongewijzigde Bedien-CTP.ps1 met ResetCursor na eigen Guard en actuele boundsmatch: Single Player1300,390; Load Game1300,426; Julius1040,437; alias1080,565. Na boundsverandering2171×1080 werden de getoonde2048×1019beelden expliciet teruggerekend naar oorspronkelijke pixels (x×2171/2048, y×1080/1019). Geen geschatte FromX/FromY, nieuwe helper of kaartinput. Eén vroege bestandsweergave liep vóór einde van het childcommando tegen ontbrekende singleplayer.png; na terminale childexit is de werkelijke capture geïnspecteerd vóór vervolginvoer. Geen focus-restore-attempt.json: focus matchte, dus de max-één herstelroute is nog niet daadwerkelijk beproefd.

Vers budget11:46:38: bron09:46:20UTC/leeftijd17,8s, vijf15/week54/stateok. Dit bereikte de door root opgelegde extra live-reservegrens≤15; onmiddellijk verder werk afgebroken en normale Finish ingezet. Aliasselectie bewijst geen laden van de save. Er is geen OK-klik/T0.json/T1.json/passrecord, geen OpenProcess/RPM, nieuwe loadedbytes of zeven-AI native−1→0. Geen per-AI Gcert/Dorig/R of uitbreidingsclaim.

## Normale afwikkeling en controleerbaar herstel

Eén CloseMainWindow11:46:58.712, call_count1/bool_returntrue: circa411,4s na procescreation en vóór werkgrens420s/sluitgrens470s. HasExited11:46:59.082 true, exit_code null/onbekend. Geen force/kill/tweedeclose/pcactie.

Onmiddellijke RestoreOwnInstallation weigerde zijn eerste CountZero met `All-civctp fresh gate not count0`, vóór herstelmutaties. Dit is een gemeten moment, geen bewezen crash of nog draaiende eigen instance. `postclose-process.json` bevestigt succesvolle verse OS-allcount0 op11:47:17.846. Alleen RestoreNoStart daarna uitgevoerd, zonder nieuwe start of sluiting; exit0. Release19 hersteld; eigen origineleT0hashalias verwijderd11:47:39.456 na echte releaseherstelling en count0 (`restore.json`, `T0-alias-cleanup.json`). Geen onverwachte bytes overschreven.

Default AUTOSAVE-Julius SHA `c5c222bbe06d91e8ddab236bb6053ea08b01bc2ea9ee95d2c67f6640490c46d6` bleef bytegelijk, statusUNCHANGED_DEFAULT; geen gegenereerde save of nieuw versiearchief. Profiel SHA `72a99e860698508c876750d944a75d93111c56789117ee6c9480d7e341d4d1fd` behouden.

`postrestore-process.json`: succesvolle verse OS-query11:48:12.009, count0. `postrestore-audit.json`:19/19actualreleasebestanden,9/9oudesaves,profiel,9/9rootvrijgegevenbron/protocolpins en source-manifestSHA `c10ef408483b1e03a995815ba4b21d025727195ebd4ba12ccf04ddc0739c3832` match; aliasafwezig. Herstel-DLL `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890`. C6-gate daarna consumed/allowedfalse/baselinefalse. Geen automatische nieuwe arm.

| Tussendoel | Werkperiodeopbrengst en huidige acceptatie | Open / volgende concrete oplevering |
| --- | --- | --- |
| Echteactivatie Doel1/1a | Tijdelijkeinstallatie/procesbinding, zichtbare menu→Julius→uniekealiasselectie en normaalherstel bewezen | Save-load/T0/éénT1/7AI/loadedbindings ontbreken door reserveafbreking. Rootreview van bewijs en budget-/werkdeadlineplanning; volgende eventuele arm afzonderlijk gereviewd/vrijgegeven. |
| Doel3behoud | Werkelijk19release/negen saves/profiel/bronpinsherstel behouden gecontroleerd | Combinatie-B2 nog nietlivegemeten; eerdere releaseacceptatie blijft gelden. |
| Uitbreiding30/40 | Geen nieuwe gameplayvoortgang | Nuttigeuitbreiding/vergelijking/science/monopoly/transport/volledige7AItelemetry blijvenopen; sciencekandidaat niet gecombineerd. |

Laatste eigen budget11:48:13: bron09:48:10UTC/leeftijd2,3s, vijf12/week53/stateok; gebruikershardgrens5vijf/10week niet bereikt. Livewerk al gestopt op rootreservegrens15; uitsluitend herstel/eindverslag daarna. Geen auto-review rejection of actieve achtergrondrun. Uitvoerder nu gestopt; root bewaakt projectstatus en eventuele budgetstop/expliciete eenmalige pc-afsluitopdracht. Deze uitvoerder deed geen afsluitactie.
