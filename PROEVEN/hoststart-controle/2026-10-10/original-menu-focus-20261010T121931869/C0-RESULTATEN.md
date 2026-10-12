# C0: Capture-wachtoptie statisch gecontroleerd

Afgerond: 10 oktober 2026, 12:22 Europe/Amsterdam. Uitvoerder gestopt na C0. **Toegepast en statisch gecontroleerd; niet live uitgevoerd.** Rootreview van C0 resteert. Geen helperaanroep, proces-/GUI-proef, screenshotactie, gameplaymeting of C1 vanuit deze opdracht.

Root gaf het frozen voorstel `ONTWERP/FOCUS-CAPTURE-CONTROLE.md` afzonderlijk gereviewd en uitgelegd over, SHA256 `baa078b80cbabd55db9de34d63e85bc0d9fafe2c0e58eeb93885f88a826333c1`. Nieuwe foldernaam gebruikt de werkelijk gemeten C0-preflighttijd `2026-10-10T12:19:31.869+02:00`. Oude afwikkelbewijsmap behouden; PROJECTSTATUS/VERSIES blijven rootownership.

Gewijzigd bestand: `PROEVEN/Bedien-CTP.ps1`. Vijf nieuwe parameters: switch `CaptureWaitForForeground` standaard uit, int `CaptureWaitTimeoutMs` standaard30000/range1..30000, int `ExpectedProcessId`, long `ExpectedCreationUtcMs` en long `ExpectedWindowHandle`. Bij expliciete nieuwe parameters worden andere Actions, ontbrekende/uitgeschakelde switch of ontbrekende bindings vóór directory/API-/actieafhandeling geweigerd. Bij opt-in zijn positieve PID en niet-nul HWND vereist.

De nieuwe Capture-tak gebruikt één Stopwatch vanaf takingang, korte op resterende tijd gekapte polls, en dezelfde oorspronkelijke procesbinding. Iedere poll herleest CIM PID/UTCcreation/proefexe, ververst het oorspronkelijke Process-object en controleert diens PID/path/hoofdhandle en handle-eigenaar. Na gemeten foreground volgen350ms binnen dezelfde deadline, herbinding/foreground, positieve actuele bounds, voor-Copy-binding/foreground, onmiddellijke na-Copy-foreground en opnieuw identiteit/foreground. Afwijking of late OS-terugkeer wordt afgekeurd. Het bestaande PNG-pad wordt pas na deze checks geschreven; ook late Save-terugkeer wordt afgekeurd. De tak bevat geen SetForegroundWindow of invoer. Stdout krijgt compacte JSON-trace vanuit finally; een fout bij de voorafgaande selectie krijgt een afzonderlijke compacte fouttrace. Geen loggingframework of nieuwe Windows-API toegevoegd.

| C0-acceptatie | Daadwerkelijk bewijs |
| --- | --- |
| Herstelbare bytekopie | `Bedien-CTP.before.ps1`, exact oorspronkelijke SHA256 `3594e4f32b26265cfc3fa900fcd61f245656940929968b231b19315a734b5f1d`; vóór patch bevestigd |
| Nieuwe tool | SHA256 `d2dbbfcad3d9d8bec8e6a99a399d59561d8f9c4e9a48576a2aefc32e5997bc74` |
| PowerShell-parser | ParseFile zonder uitvoering:0 fouten; `parser.json` |
| Gerichte diffreview | `patch.diff` en `diff-review.json`: oude setup/Start/Restart, Status/DismissError en suffix met gewone Capture/Key/Click/Drag tekstgelijk behouden; alleen selectie omwikkeld met opt-in-fouttrace en rethrow |
| Encoding | Oorspronkelijk LF/UTF-8 zonder BOM, geen CRLF; deze vorm behouden |
| Scope | Geen C1, live helper, procesquery, focus, input, screenshot, reader, gameconfig/binary of pcshutdown uitgevoerd |
| Budget | Preflight en eindcontrole `ok`; eind12:22:05.230, bron12:21:39.297/leeftijd25.9s: week95/vijfuur67; `budget-preflight.json`/`budget-final.json` |

Deze statische controles bewijzen de ingreep en haar beschreven guards, geen werkende runtimeopname of host/gameplayverbetering. Sampling bewijst geen continue focus tussen reads. Een OS-query of CopyFromScreen/Save kan niet via Stopwatch worden afgebroken; late acceptatie is wel geweigerd. Actuele herkenbare menuafbeelding blijft vereist voor menupass.

Herstel: opt-in weglaten gebruikt de behouden oude route. Bij patchfout kan root na actuele hashcontrole de bytekopie terugzetten, uitsluitend als geen latere edits worden overschreven. Geen herstel uitgevoerd.

Volgende concrete handoff: root beoordeelt patch/parser/diff/toolmanifest en registreert de nieuwe toolversie. Gebruiker meldde tijdens C0 dat het spel vanzelf foreground wordt na mogelijk introvertraging; root past alleen de afzonderlijke C1-aanpak aan. Deze agent heeft de frozen C0-ingreep behouden. Alleen een nieuwe expliciete C1-opdracht na rootreview kan livebediening starten. Host/menu/H1/H3 en gameplay blijven open.
