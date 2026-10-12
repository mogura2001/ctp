# Begrensde C-afwikkeling van de oude proefinstantie

Afgerond op 10 oktober 2026, 12:02 Europe/Amsterdam. Uitvoerder gestopt; geen procesactie of achtergrondrun actief vanuit deze opdracht.

**Uitkomst: `TARGET_PID_ABSENT_NO_CLOSE_NEEDED`.** De succesvolle buiten-sandbox CIM-query voor uitsluitend `ProcessId=20536` vond geen proces op 12:00:48.8479954. Er is nul keer `CloseMainWindow()` aangeroepen. De oude PID is op dat meetmoment afwezig; historische exitcode, oorzaak en tijdstip zijn niet verkregen. Dit is geen bewijs van een normale historische afsluiting, crash, menu of gameplay.

Root droeg de afzonderlijke B-aanvulling in `ONTWERP/HOSTSTART-CONTROLE.md` over als volledig gereviewd/uitgelegd, SHA256 `84ee06f124911e3b70299626ca46e8e85d3c7ccaf3df1e0c79fbb77a0879c0d2`. Die hash is vóór en na gelijk. PROJECTSTATUS.md bevatte nog de eerdere budgetstop/niet-vrijgegeven toestand; de expliciete nieuwe roloverdracht begrensde deze uitvoering tot afwikkeling, zonder volgende start of installatie.

| Controle | Daadwerkelijk resultaat en bewijs |
| --- | --- |
| Budget vóór uitvoering | `ok`: week 99%, vijfuur 93%; bron 11:59:59.970, controle 12:00:27.921, leeftijd 28s; `budget-preflight.json` |
| Identiteitspins | Alle 15 pins gelijk aan `PROEVEN/activatie-h3-runtime/2026-10-09/avond/poging2/eindhashes.json`; `preflight.json` en `eindhashes.json` |
| Tool | Bedien-CTP SHA256 `3594e4f32b26265cfc3fa900fcd61f245656940929968b231b19315a734b5f1d` gelijk; tool niet bediend |
| Procesquery | `ErrorActionPreference=Stop`, buiten sandbox; uitsluitend `ProcessId=20536`; query gestart 12:00:47.881, succesvol voltooid 12:00:48.848, count 0; `process-initial.json` |
| Sluitaanvraag | Niet nodig/niet uitgevoerd, callcount 0; `close-request.json` |
| Identiteit/herbinding/modal | Door afwezigheid geen Process-object, StartTime, handle of owned-windowmetadata uitgelezen; nooit een andere PID getarget |
| Exit/eventobservatie | Geen aanvraag, dus geen +1/+5/+10s-observatievenster; geen HasExited/ExitCode verkregen en geen Application-events bevraagd; `process-checks.json` |
| Profiel | Voor-/nakopie bytegelijk; SHA256 `72a99e860698508c876750d944a75d93111c56789117ee6c9480d7e341d4d1fd`, mtime UTC `2026-10-09T21:19:10.1443179Z`; beide snapshots behouden, oorspronkelijke state behouden |
| Eindbudget | `ok`: week 99%, vijfuur 91%; bron 12:01:12.768, controle 12:01:28.573, leeftijd 15.8s; `budget-final.json` |

Alle tijden in de tabel zijn 10 oktober 2026 Europe/Amsterdam, behalve de expliciet als UTC gemarkeerde profielmtime. Nieuwe bewijsbestanden zijn uitsluitend in deze nieuwe submap geschreven; bestaande C-evidence, saves, binaries en gebruikerswijzigingen zijn behouden. Geen focusherstel, toets, klik, capture, Kill, Start, Restart, DLL-installatie, T0-proef, rollback of pc-afsluiting uitgevoerd.

De geconfigureerde normale AI-route en originele robotcom.dll zijn als bestaande pins gecontroleerd; geen proces aanwezig om geladen modules, laadgedrag of caches in deze instantie te controleren. De DLL-pin bleef `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`. Geen configuratiewijziging toegepast en geen gameplaymeting uitgevoerd.

Acceptatiestatus: de afwikkelblokkade voor de oude PID is door geslaagde afwezigheidsobservatie beoordeelbaar. `EXIT_CONFIRMED_NO_CRASH_OBSERVED` en `EXIT_CONFIRMED_CAUSE_UNKNOWN` worden niet gebruikt: er is geen nieuwe sluitaanvraag met verkregen exitcode. Er is geen query over alle civctp-processen uitgevoerd; count 0 geldt uitsluitend voor PID20536. Eerder menubewijs blijft `NOT_OBSERVABLE`; H1/H3-hostacceptatie en gameplay blijven open.

Volgende concrete handoff: root beoordeelt deze afwezigheid en eindpins, werkt PROJECTSTATUS/VERSIES bij en bepaalt de volgende afzonderlijke host/menu-stap. Een volgende C-installatie/start is vanuit deze opdracht niet vrijgegeven; daarvoor is opnieuw een actuele procespoort vereist. Geen zichtbaar sluitverzoek aan de gebruiker nodig voor een op het meetmoment afwezige PID. Onderzoek van de historische verdwijning valt buiten deze afwikkeling.
