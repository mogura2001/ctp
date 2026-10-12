# Hoststart als voorwaarde voor activatie

Gerichte fase A, 9 oktober 2026, 21:19:23 Europe/Amsterdam. Ownership uitsluitend dit bestand en VOORTGANG-ANALIST-HOSTSTART.md. Geen spelstart, GUI, procesgeheugen, dump/debugger, installatie of wijziging van gamebestanden/register/compatinstellingen uitgevoerd. Brede M1-analyse blijft afgesloten.

## Opdracht en conclusie

Tussendoel: **wijzigingen daadwerkelijk actief**. De H1-I/H3-activatieproef wordt geblokkeerd door een crash van de proefhost vóór T0. Ontbrekende ontwerpkennis: wat bestaande metadata bewijst, of bestaande H1-I-startbindings een oorzaak aantonen, en welke minimale volgende controle startomgeving en kandidaatinvloed onderscheidt.

**A1–A3 zijn voldoende beantwoord voor B.** De crash is gekoppeld aan exact PID23468/proefexe. H1-I-causaliteit is onbewezen. Een begrensde normale menucontrole met de al herstelde originele DLL is uitvoerbaar via de bestaande proeftool; zij vereist geen volledige crashdiagnose. WER-inhoud is door OS-toegang niet leesbaar en is geen voorwaarde voor deze overdracht. Deze analyse levert geen hostfix of gameplayverbetering op.

## Dekkingsmatrix per beslisketen

| Vraag / schakel | Gedekt bewijs en huidige werking | Open grens | Route / noodzakelijke voorwaarden |
| --- | --- | --- | --- |
| A1: starttool → host | Bedien-CTP.ps1 Start bepaalt absolute proefexe, weigert een bestaande civctp en vraagt Start-Process met WorkingDirectory gelijk aan de exemap, WindowStyle Normal, PassThru, zonder opgegeven argumenten. Start meldt PID23468. | Alleen de aangevraagde werkdirectory bewezen; geen runtime-CWD of vastgelegde volledige geërfde omgeving. PIDuitvoer bewijst geen menu of geslaagde initialisatie. | Behoud dezelfde tool, exe, werkdirectory en normale zichtbare startroute. Leg actuele inputs vóór een C-start vast. |
| A1: host → crash / exit | Event1000 21:09:17.613 koppelt exact PID0x5BAC=23468 aan CTP-proef/civctp.exe en ntdll.dll10.0.26100.9444, c0000005, offset6f7aa. Latere succesvolle CIM21:09:33 vindt nul civctp-processen. | Geen procesexitcode/stack, foutende instructieanalyse, rootcause of welk stadium vóór T0 bereikt is. ntdll als faultmodule wijst geen veroorzakende DLL aan. | Correlatie van nieuw PID/starttijd/exactpath/events; crash of verdwijnend proces betekent stoppen, geen blinde retry. |
| A1: schijf → geladen modules | H1-I was tijdelijk op schijf gehasht; eindhashes bevestigen originele DLLherstel en15pins. | Geen geladenmodulelijst, geladen robotcom-basispad, loadedbytes, World/AI-init of scorecallbackbewijs. | Schijfhash blijft een inputcheck. Menuacceptatie apart houden van DLL/adapter/T0acceptatie. |
| A1: compat / profiel → host | Exacte huidige Layerswaarden buiten sandbox alleen-lezen gecontroleerd; huidige proefprofielhash gelijk aan bewaarde after-startsnapshot. | Geen precrashprofielinhoud; huidige registerwaarden bewijzen niet de feitelijk toegepaste crashproces-shims. | Voor baseline verse snapshot/hash van bestaand profiel en bekende startinputs; compat/CD/gebruikersstate behouden. |
| A2: bestaande H1-I → startup | Manifest/source wijzigen drie scorecalls plus afgebakende PEheaders/nieuwe RXpayload; entrypoint/imports/exports/initializers/relocdirectories blijven bestaand. Gewone loader en rebase in eigen helper eerder geslaagd. | Niet gemeten of game-loader, init of enige gewijzigde call vóór de crash bereikt is. Helperacceptatie bewijst geen echte gamecontext. | Geen aangetoonde H1-I-startupoorzaak. Eerst originele-DLL-hostmenucontrole, geen nieuwe hook of brede initreconstructie. |
| A3: originele host → eerste onderscheid | Originele DLL is reeds hersteld; dezelfde gewone Start/Status/Capture-route is aanwezig en eerder voor een menu gebruikt. | Huidige originele proefhost is nog niet gemeten. Eerdere werkende D:\\CTP-instantie is een andere path/omgeving en ongemeten referentie. | Eén poging tot menu met exactoriginalpins, voorafstate en foutcriteria. B maakt de begrensde C-overdracht; A start niets. |

## A1 — exact bewijs en beperkingen

Primaire lokale bewijsbestanden: [poging2-resultaten](../PROEVEN/activatie-h3-runtime/2026-10-09/avond/poging2/RESULTATEN.md), [event1000](../PROEVEN/activatie-h3-runtime/2026-10-09/avond/poging2/application-events.json), [preflight](../PROEVEN/activatie-h3-runtime/2026-10-09/avond/poging2/preflight.json), [eindhashes](../PROEVEN/activatie-h3-runtime/2026-10-09/avond/poging2/eindhashes.json), [profielrecord](../PROEVEN/activatie-h3-runtime/2026-10-09/avond/poging2/userprofile-record.json). Start-/focusregels: [Bedien-CTP.ps1](../PROEVEN/Bedien-CTP.ps1), [AUTOMATISERING.md](../PROEVEN/AUTOMATISERING.md).

De feitelijke crashpath is `C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe`, versie1.2.0.0, timestamp37d6f702. De gebonden engine-SHA is `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, imagebase400000. Event1000 geeft faultmodulepath `C:\WINDOWS\SYSTEM32\ntdll.dll`, timestamp427cc5bd en ReportID `c1ddc58d-a761-43ef-8391-0bf8eeb72998`. Exception c0000005 is de gerapporteerde exception; de toegangssoort, het geraakte geheugenadres en de veroorzakende caller zijn niet vastgelegd in dit event. Offset6f7aa zonder stack of passende ntdllanalyse verklaart de oorzaak niet.

Root vond aanvullend event1001 met hetzelfde ReportID en de archiefverwijzing:

`\\?\C:\ProgramData\Microsoft\Windows\WER\ReportArchive\AppCrash_civctp.exe_ad2626fb3072ed90851deaf96f6f15924247be_e13efadf_b0153637-0335-4078-b0f9-a55314216ffe`.

Deze analist controleerde uitsluitend die exacte directory zonder prefix via Test-Path; de containercheck was positief. Get-ChildItem/Report.wer-toegang gaf Access denied binnen sandbox; een toegelaten require_escalated alleen-lezen poging faalde opnieuw op directorytoegang. Er is geen Report.wer-inhoud of bestandslijst verkregen. Dit is een OS-toegangsgrens, geen automatische approvalrejection. Geen ACLwijziging, eigendomsovername, dump of andere appdata onderzocht. Daardoor blijft WERbewijs over modules/CWD/exitcontext **onbeschikbaar**, niet negatief. Rootmelding over1001 wordt als overgedragen eventbevinding onderscheiden van het zelf gelezen1000bewijs.

Een eerste sandbox-registerlezing gaf misleidend beperkte zichtbaarheid. De afzonderlijke succesvolle lezing buiten sandbox op **21:16:30.815 +02:00** vond voor uitsluitend de exacte proefexe:

| Actuele sleutel | Exacte waarde |
| --- | --- |
| HKCU\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers | `DWM8And16BitMitigation` |
| HKLM\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers | `$ DWM8And16BitMitigation` |
| HKLM\Software\WOW6432Node\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers | Sleutel aanwezig, exacte exewaarde afwezig |

`__COMPAT_LAYER` was null in het toenmalige uitvoerende PowerShellproces. Dit is huidige read-onlymetadata, geen volledige effectieve compatconfiguratie van PID23468 en geen historischbewijs dat de waarden gelijk waren. De ontwerper hoeft deze waarden niet te wijzigen. Geen onderzoek naar andere apps/registerpaden nodig.

Op **21:16:44** opnieuw alleen-lezen gehasht: huidige proefexe bovengenoemde engine-SHA, proefrobotcom origineel `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, kandidaat H1-I `59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0`; alle gelijk aan bestaande bindings. Huidig userprofile.txt1595bytes, SHA `72a99e860698508c876750d944a75d93111c56789117ee6c9480d7e341d4d1fd`, gelijk aan [after-startsnapshot](../PROEVEN/activatie-h3-runtime/2026-10-09/avond/poging2/userprofile.after-start.txt). Geen exact inhoudsdelta tegenover vóór21:09 te reconstrueren. Deze huidige snapshot is bruikbaar als **nieuwe voorafstate**, niet als oorspronkelijke precrashstate.

Profieltekst bevat onder meer RequireCD=No, UseRedbookAudio=No, TryWindowsResolution=No, ScreenResWidth=1920, ScreenResHeight=1080, DebugSlic=Yes en mappluginpaden. Dat zijn bestandsfeiten; de crash bewijst niet of en hoe de engine ze gebruikte. Eerdere CD-dialoog/editorbevindingen uit AUTOMATISERING zijn een mogelijke afhankelijkheid, geen diagnose voor deze crash. Behoud de bestaande CD-/displayomgeving; geen CD-, scherm- of compatwijziging als vermeende fix.

## A2 — wat H1-I aantoonbaar verandert

Hergebruik: [H1-analyse](INGREEP-LOCATIESCORE-H1.md), [bestaande PE/ABIbinding](BINAIR/score-hook-h1-pe-abi.txt), [H1-manifest](../PROEVEN/score-h1/H1-I.manifest.json), [builder](../PROEVEN/score-h1/build.py), [verifier](../PROEVEN/score-h1/verify.py), [payload](../PROEVEN/score-h1/H1-I.disassembly.txt), [technische resultaten](../PROEVEN/score-h1/RESULTATEN.md). Geen tests herhaald of nieuwe disassembler gemaakt.

Originele robotcom.dll: timestamp37b894e7, imagebase20000000; passende Robotcom.mapbinding. Civctp.map is niet gebruikt. De drie gewijzigde RVA's **784bb/78517/7aa35** zijn comparator-/doelcreatiescorecalls; oorspronkelijke bytes `ff9168010000` worden E8rel32 naar **d4000** plus NOP. H1-Ipayload87bytes bewaart nonvolatile registers/stack, haalt oorspronkelijke signed16positieargumenten op, roept oorspronkelijke **World+168** en retourneert signextended AX via ret10h. Zij leest geen extra terrein/AiMain/globalcontext; dat uitgebreidere pad hoort bij H1-M.

De aparte `.h1` RXsectie is RVA d4000/raw a1400; bestaande image d4000 wordt d5000. Manifest verklaart sectioncount/codegrootte/imagegrootte/checksum/nieuwe header plus de drie sites. Het beperkt toegestane diffbewijs en identieke bestaande datadirectories onderbouwen behoud van entrypoint/imports/exports/TLS-/initializerroutes/relocaties; geen nieuwe startupcallback toegevoegd. Dit sluit een game-specifiek laadprobleem of runtimecontextfout niet uit. De eerder geslaagde gewone LoadLibrary/FreeLibrary en rebase zijn echte native helpermetingen, geen hoststartbewijs.

**Conclusie:** geen aangetoonde relatie tussen een gewijzigde H1-I-instructie en de crash vóór T0. Er is ook geen bewijs dat de adapter onbereikbaar was vóór het menu of dat robotcom nog niet geladen was. Machinecode van de scorehook bepaalt haar functie; haar historische reachability blijft onbekend. Kandidateninvloed, oorspronkelijke host en startomgeving blijven open verklaringen. Geen nieuwe gameplaystrategie of startupfix onderbouwd.

## A3 — eerste minimale controle voor ontwerp

Technisch aannemelijke route: **één gewone originele-DLL-hoststart tot het hoofdmenu, stoppen vóór save-load of nieuwe partij**. De reeds herstelde DLL maakt extra installatie voor die eerste controle overbodig. Dit is een overdraagbare B-route, geen uitgevoerde proef of toestemming om in A te starten.

Voor een concreet B/C-protocol zijn voldoende voorwaarden bekend:

1. Controleer budget verse hoofdthreadbron; week<=10 of vijfuur<=5 stopt alle projectwerk, pc blijft aan. Procescontrole moet buiten sandbox met foutafhandeling aantonen dat geen civctp draait. Bij bestaande instantie of mislukte query stoppen; D:\CTP nooit bedienen/sluiten.
2. Leg vóór de enige start in een eigen unieke resultaatmap vast: toolhash/commando, exact exe-/werkdirectorypad, oorspronkelijke DLLhash, alle15bestaande pins/B1/T0, huidige profielkopie/hash/mtime en actuele exacte compatwaarden/knowninputs. De huidige after-startsnapshot is vergelijkingsbasis; C maakt een verse voorafkopie. Behoud profiel, CD, compat, display en gebruikersstate; geen instelling wisselen om de start te helpen. Beschikbaarheid van alle15pins opnieuw controleren, geen nieuwe beschermdeinventaris nodig.
3. Gebruik bestaande `Bedien-CTP.ps1 -Action Start` met dezelfde normale route. Maximaal **één** startpoging; B kan een observatiegrens van maximaal60seconden en korte tussentijdse Statuschecks vastleggen. Bewaar startuitvoer/PID/starttijd en controleer exactpath via succesvolle procesquery. Geen Restart, automatische retries, nieuwe kaart, T0-load, AI-orders of reader.
4. Gebruik bestaande Status en Capture alleen indien de exacte proefinstantie leeft. Capture eist werkelijk hoofdvenster/focus/bounds; een weigering is geen menupass. Omdat de tool naar PROEVEN/automatisering/ctp-window.png schrijft, moet B/C bestaand bewijs vooraf behouden en de nieuwe capture direct onder een uniek resultaatpad bewaren. Screenshot moet herkenbaar hoofdmenu tonen; alleen proces aanwezig/Responding/exit0 van het toolcommando volstaat niet.
5. Noteer crash/verdwenen proces/CD- of andere dialoog/time-out/focusprobleem afzonderlijk. Bij crash: alleen relevante nieuwe Application1000/1001-events aan exact PID/starttijd/path koppelen; exitcode uitsluitend rapporteren indien daadwerkelijk verkregen. Geen WERtoegangsworkaround, dump/debugger, compatfix of tweede start toevoegen.
6. Na observatie: profiel/hash en pins opnieuw vastleggen. Behoud door normale start gewijzigde gebruikersstate met voor/na-evidence; niet stilzwijgend terugkopiëren. Succesvolle menucontrole moet B een normale menu-exit/afwikkelroute en laatste exactprocescontrole geven voordat ander C-werk mag beginnen. Zonder menu/focus geen blinde toetsafwikkeling. DLL blijft origineel; bij onverwachte mismatch stoppen.

| Uitkomst van de ene originele-DLL-controle | Wel onderscheiden | Volgende B-uitkomst |
| --- | --- | --- |
| Dezelfde originele host crasht/faalt vóór menu | H1-I is niet nodig om de huidige startfout op te laten treden. | Geen H1-I/H3-installatie; gericht voorstel over de nieuwe originelehostfout, op basis van eigen event/dialoog. Geen conclusie dat eerdere H1-I-crash geheel verklaard is. |
| Originele host bereikt aantoonbaar menu en blijft binnen venster bruikbaar | Huidige oorspronkelijke start werkt onder vastgelegde inputs. | B kan een afzonderlijke begrensde H1-I-menuvergelijking ontwerpen met verse profilesnapshot, gelijke inputs en herstel. Eén historische H1-Icrash tegenover één nieuwe originalepass bewijst nog geen causaliteit. |
| Alleen proces/status of onleesbaar screenshot, focus/dialoog/time-out | Menuacceptatie niet aangetoond. | Als NOT_OBSERVABLE/blockedhostpoort rapporteren met concrete reden; geen causaliteit of H3activatie claimen. |

Een menupass bewijst **geen** geladen H1-I/H3-bytes, T0, AI-pass, nieuwe goals, Q/B, scorecall/heapordening of overhead. Het bestaande H3-activatievoorstel blijft voor die afzonderlijke vervolgstap gelden. Geen B2/B4-compositie in deze controle.

## Overdracht, acceptatie en backlog

Tussendoel **wijzigingen daadwerkelijk actief**: nieuwe delta is voldoende gerichte analyse van de hoststartpoort en ontwerpbare baselinecontrole. Analysescope A1–A3 afgerond; B kan nu een concreet begrensd voorstel opleveren. Gameplayacceptatie blijft open, huidige hostruntime geblokkeerd. Tussendoel **goede locaties kiezen/H3**: geen gameplaydelta; bestaande offlineacceptatie blijft geldig.

Niet-blokkerende open punten: onleesbare WERmodule-/CWD-/stackmetadata; exacte historische effectieve compatomgeving; precrashprofielinhoud; H1-I-reachability vóórcrash; volledige oorzaak. Alleen terug naar A wanneer nieuwe baselinebewijs een concrete eerstvolgende ingreep blokkeert. Geen volledige engine/init/callgraphreconstructie als extra oplevervoorwaarde.

Deze analist stopt na overdracht. Geen eigen game/helper gestart; geen C-werk loopt door deze agent. Root beheert PROJECTSTATUS/VERSIES en de volgende B/C-rol. Laatste budgetcontrole21:19:23, geldige bron21:18:26 (57.5s oud): vijfuur40/week13/warn, geen stopreden. Geen afsluithelper/commando/planning; pc aan.
