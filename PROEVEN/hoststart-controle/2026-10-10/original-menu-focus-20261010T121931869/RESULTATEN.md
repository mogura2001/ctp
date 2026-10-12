# C1: originele hostmenucontrole na introgelegenheid

Afgerond: 10 oktober 2026, 12:33 Europe/Amsterdam. **MENU_PASS zichtbaar bewezen; afwikkeling NOT_CONFIRMED.** Uitvoerder gestopt. Geen verdere livebediening of achtergrondrun vanuit deze opdracht.

Root accepteerde C0-toolSHA `d2dbbfcad3d9d8bec8e6a99a399d59561d8f9c4e9a48576a2aefc32e5997bc74` en gaf C1 afzonderlijk vrij onder het originele frozen voorstel SHA `baa078b80cbabd55db9de34d63e85bc0d9fafe2c0e58eeb93885f88a826333c1` en intro-addendum SHA `00293025b48f9c796bd5b7fe845c678cd5c6218d2ed5b675583b3e52fc8cad4d`. Gebruikerscorrectie over automatische foreground verving handfocus/beschikbaarheid. Geen toolpatch, input of intro-overslaan in C1.

| Meetpunt | Daadwerkelijk resultaat |
| --- | --- |
| Preflight12:26:27.888 | Succesvolle buiten-sandbox alle-civctp-query count0,15pins gelijk, originele herstelkopie gelijk, bekende compat/CD/display/profielinputs gelijk; `preflight.json` |
| Budget vóór Start12:26:51.186 | Week94/vijfuur61, stateok; bron12:26:44.254/leeftijd6.9s |
| Enige Start12:26:51.456 | Bestaande helperexit0, Startcount1; `start-stdout.txt`/`start-record.json` |
| Directe binding12:26:53.023 | PID14288, exact `C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe`, CreationUtcMs1791628012889 |
| Introgelegenheid | Tot+180s, alleen-lezen eigen venster/bindingssamples, geen Capture/input; `window-timeline.jsonl` |
| +90s budget12:28:22.013 | Week94/vijfuur60, stateok; bron12:28:11.630/leeftijd10.4s |
| Definitieve binding12:29:53.795 | +182.335s sample,2267ms dezelfde HWND984984/eigenaar/foreground/bounds0,0–1920,1080; `final-window-binding.json` |
| Budget vóór Capture12:29:53.866 | Week93/vijfuur58, stateok; bron12:29:46.656/leeftijd7.2s |
| Enige Capture12:29:54.530 | C0-opt-in, oorspronkelijke PID/Creation/HWND; Capturecount1, helperexit0; `capture-request.json`/`capture-result.json` |
| Capturechecks12:29:55.004–55.925 | Poll/350ms/bounds/voor-na-Copy dezelfde identiteit/eigenaar/foreground; Stopwatch920.938ms binnen30000ms; `capture-trace.txt` |
| Verse afbeelding12:29:55.974 bewaard | `menu-01.png`, SHA256 `b83200b1d878bd59f54e8232b4dee80c9d5b1c2c27299aa4986a4926594f85eb`; gewone leesbare Single Player/Multiplayer/Quit/Credits; uitvoerder en root bekeken werkelijk, MENU_PASS |
| Afwikkelguard12:30:51.009 | +239.561s, fout `Insufficient live time for close observation; no request`; CloseMainWindow-callcount0, geen retry; `close-error.json`/`close-request.json` |
| Livegrens12:30:51.456 | Geen verdere proces-/GUI-bediening; huidige processtatus onbekend, exit niet bewezen |
| Application1000/1001 | Postflight-query geslaagd voor start tot afwikkelguard,0 passende events; `application-events.json`. Dit bewijst geen exit of normale afsluiting. |
| Postflight/budget12:31:55.921 | Alle15 pins/tool/voorstel/addendum gelijk; profiel voorna bytegelijk en behouden. Week93/vijfuur56, stateok; bron12:31:26.632/leeftijd29.3s; `eindhashes.json`/`C1-budget-final.json` |

Alle genoemde tijden zijn 10 oktober 2026 Europe/Amsterdam. Voor-/naprofiel en vooraf aanwezige vaste screenshot zijn bytekopieën; oude C0- en afwikkelartefacten behouden. Binaries/saves/B1/configuratie onveranderd; geen herstelinstallatie of rollback. Geen T0-load, nieuwe partij, reader, H1/H3/B2/B4-installatie, focusforcering, Key/Click, Kill/Restart of pcshutdown uitgevoerd.

**Afwijkingen en bewijsgrens:** na directe startbinding werd de inline observatie pas rond+78s actief terwijl de uitvoerder haar aanroep voorbereidde; die vroege periode is niet iedere500ms gemeten. De latere samples en capturebindings zijn vastgelegd, maar geen ononderbroken observatie vanaf Start claimen. De afwikkeling was niet tijdig voorbereid na beeldbeoordeling; de guard voorkwam een sluitaanvraag zonder resterende10s. De volledige C1-afwikkelacceptatie is daarom niet gehaald, ondanks geldig en door root geaccepteerd menubewijs. Exacte introduur en eerder foregroundmoment zijn niet bepaald.

De originele DLL en B1 zijn als bestanden gepind. Dit menu bewijst geen geladen kandidaatbytes, scorecallback, AI-activatie, T0, heapordening, overhead of gameplayverbetering. HasExited/ExitCode en actuele alle-civctp count0 zijn niet verkregen. Afwezigheid van passende events is uitsluitend een eventwaarneming.

**Concrete handoff:** mogelijk nog open eigen proefinstantie PID14288/CreationUtcMs1791628012889/exact proefpad/HWND984984. Laatste geslaagde volledige eigen binding in Capturetrace op12:29:55.8236624, foreground984984; daarna geen afsluiten bewezen. Root krijgt verzoek uitsluitend deze eigen instantie zichtbaar normaal af te wikkelen of afzonderlijk een nieuwe begrensde afwikkelopdracht te reviewen. Geen nieuwe start/installatie zolang een verse procespoort afwikkeling niet bevestigt. Geen sluitcall alsnog buiten de240s uitgevoerd.

Root beheert PROJECTSTATUS/VERSIES en volgende opdracht. C1 eindigt hier: menu geaccepteerd, afwikkeling open; uitvoerder gestopt.
