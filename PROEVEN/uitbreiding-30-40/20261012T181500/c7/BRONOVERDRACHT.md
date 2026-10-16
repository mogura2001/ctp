# C7 bronoverdracht — voorbereid/offline gecontroleerd, geen livevrijgave

14 oktober 2026 16:14 Europe/Amsterdam. Uitvoerder levert uitsluitend eigen c7-bronnen/staging op en stopt voor rootbronreview. Voorstel UI-TIJDRESERVE-U30-40-C7.md exact SHA256 `46bb147baf46782b998927db9b2f0dd321d657cdafc48448a7b3537c08430978` gelezen en door root voor sourceprep goedgekeurd. Geen controlleruitvoering, procesquery, aliasaanleg, installatie, game/GUI, RPM of nativehelper uitgevoerd. Gate initially allowed=false/baseline_allowed=false/input_mode=HUMAN_ONE_N; geen arm/start-/execution-/aliasowner-/closerecords gekopieerd. C6 blijft intact en consumed/disabled.

`source-manifest.json` SHA256 **`dd17b253b6446f189eb905b846640438261ef7b395d46a90eecc1a822c5bb7e4`** bindt10 bronbestanden en67 staging-/herstelpins. Controller SHA **`47b74fb9d519be51ccb75b01843df4cf26ab1a63674a2bb58518a0d6438cf31c`**; reader **`9ead24ce0b82d604a6bb6dab1ea2cfef677e5df7bf02c3a54fe0390fe2c01e8b`**; protocol **`87b943b365e5bbefacf3e290b7a93676be56cce7b1c370249b19e63a3cecd027`**. Gate bevat deze10 volledige sourcepins, voorstelpin en source-manifesthash. Laatste pins vervangen voorlopige manifests6cd41.../7c9fd...; protocol kreeg op rootverzoek uitsluitend de chatfocus/wachteninstructie erbij.

Bronroute: prepare.py kopieert uitsluitend eigen bewaarde C6 backups/candidate/protected-backups en bronbestanden. De oorspronkelijke C6-source-manifestc10ef408... en alle9 C6-bronhashes zijn werkelijk opnieuw gecontroleerd vóór kopie. delta.py bevat exact geankerde omzettingen; check_source.py toetst de volledige controller tegen deze beperkte C6→C7-transformatie. Alle10 volledige diffs naast de bestanden; nieuwe delta.py heeft een volledige new-filediff. Dit is geen claim dat een zelfvergelijking externe review vervangt: root leest de hele delta/controllerflow en10/67 pins vóór een afzonderlijke gate.

Concrete controllerdelta:

- Nieuwe C7-gatenaam, owner/run-id en zichtbaar autosaveversielabel; fysieke Julius-aliasnaam en bytes gelijk. Reader uitsluitend C6→C7 gate/teksten; decoder, CLI, observeerstappen en native/loadedbusinesssemantiek identiek. original_core.py/participants.json bytegelijk aan C6.
- Centrale monotone work600/close690/hard720; OwnState gebruikt Work/Close-grenzen. Finish hercontroleert690 na directe identityquery en720 vóór/ná live-/exit-/count0controles. Max10s normale exitwait, één CloseMainWindow; late/onzekere exit blijft failure zonder force. Count0-race behoudt afzonderlijke RestoreNoStart, geen tweede close/start. Cleanup na terminale exit heeft geen werk-/startreservetijdpoort.
- Budget Start vijf≥50/week>25 vóór SaveAutosaveBefore/install en direct vóór Start; Work vijf>15/week>10; Cleanup vijf>5/week>10. Beide vensters/≤120s/ok-warn vereist; oorspronkelijke exit0/25acceptatie en één unknownhercheck behouden. Cleanupguard vóór archivering/defaultrestore/releaseherstel/aliasremoval. Geen dispatchlus of pcactie.
- HUMAN_ONE_N Pass weigert vóór Add-Type/input; oude Key-ncall verwijderd, nul Key-command-ASTs. ReadT0 vaste labels/variant, zeven unieke deelnemers met native−1, bestaande strikte loadedchecks/readerhashes, exacte instance en gehashte eigen startrecord/HWND. Eigen T0-acceptance.json bindt snapshot/hash/start/instance. Geen T0-save-identiteitsclaim uit readerlabel; kaart/alias/T0 blijft afzonderlijke praktische poort.
- ReadT1 vereist exact eigen c7/variant/T0.json met eigen acceptancehash/startrecord/HWND/run/turn/binding/instance en native−1. Bestaande max30s poll zonderinput, unieke GUID/pollnamen, Work-/elapsedcontroles vóór/ná iedere read. Alleen originele unstabledatafout retry; overshoot>0/regressie fataal. T1.json pas na zeven−1→0; T1-pair.json hashes, zeven before/after, instance/loaded/binding/elapsed/controller_n_calls0, geen fictieve one_nclaim. Native+1 is rondebewijs en geen OS-keyeventteller.

Praktisch protocol: bekende intro/binding, eerste eigen leesbare Capture, rootlaadsein vóór430; gebruiker Julius→000-U30-40-START-T0, wacht; kaart/T0 zichtbaar/nativeRead vóór480; verse Guard/Work-budget/focus en rootsein voor precies éénn vóór525; gebruiker wacht; inputvrije ReadT1; Finish uiterlijk600/bij abort. Na chatmelding gebruiker CTP terug op voorgrond; bestaande max-één focusherstel unchanged. Geen controllermenuklikken/n/editor/T2/T60/baseline/science/saverewrite. Root communiceert menselijke seinen. Readstdout volledig in eigen bestanden bewaren, kleine resultaatmetadata in chat na terminale childexit.

Onveranderlijke pins:

| Object | SHA256 |
| --- | --- |
| U30-kandidaat | `f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810` |
| Release/herstel-DLL | `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890` |
| QUOTA-START-T0/toekomstige alias | `8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26` |
| Bedien-CTP.ps1 | `d2dbbfcad3d9d8bec8e6a99a399d59561d8f9c4e9a48576a2aefc32e5997bc74` |

Offlinechecks daadwerkelijk PASS: PythonAST alle eigen py; PowerShellparser0 fouten. `syntax-check.json` bevat één geldige synthetische metadatafixture en3 relevante rejectcases vanuit geïsoleerde werkelijke bron-AST: verkeerde run-id, nativeovershoot, staleT0hash. Eerste staleguardextractie selecteerde een bovenliggende if; exact-guardextractie gecorrigeerd zonder controllerwijziging en3/3 rejectPASS. Geen testframework/mirrorimplementatie/observer; geen controller uitgevoerd/RPM/gameinput. KeycommandASTcount0. Alle19 actuele releasefiles/eigen19 echte backups/beide19 stagedarmen,9 bestaande saves/profiel met echte backups, protected/input/T0pins en aliasafwezigheid werkelijk gecontroleerd. Statische bindings release8sites/52ranges, U30-40 16sites/54ranges; geen loadedmemory- of gameplaymeting daarvan afgeleid.

Volledige herstelroute vóór game aanwezig: eigen executionrecord/arm, verse Cleanupbudget/count0, currentbytes uitsluitend before/owncandidate en truebackups; eventuele autosave eerst beide versiearchieven plus vereiste DLLpin; defaultautosave herstellen,19 release terugplaatsen,9 oorspronkelijke saves/profiel controleren, eigen owner+origineleT0hashalias als laatste verwijderen. Onverwachte gebruikersbytes behouden. Geencount0/normaleexit/budget/termijnpoort betekent checkpoint met exacte identiteit/install/save/alias en rootmelden, geen herstelclaim.

Budget begin16:04:17 bron14:04:00UTC/leeftijd17,3s vijf76/week48. Laatste16:13:26 bron14:12:59UTC/leeftijd26,3s vijf63/week46/stateok. Eén tussentijdse stalelezing16:10:48 (140s oud) gevolgd door precies ene succesvolle hercheck16:10:54 (4,3s oud, vijf69/week46). Geen hardgrens bereikt. Root moet verse≥50/>25reserve opnieuw toetsen vóór eventueel install/start. Alle heavyhelpers volgens root terminal; deze uitvoerder startte geen helper.

| Tussendoel | Acceptatiestatus/opbrengst deze periode | Open / volgende oplevering |
| --- | --- | --- |
| Doel1/1a echte U30-activatie | C7 bron voorbereid en offline gecontroleerd; gate disabled | Root volledige bron/diff/pinreview, pas daarna één afzonderlijk vrijgegeven menselijke T0/T1-arm |
| Doel3 behoud | Actuele19 release/negen saves/profiel en eigen herstelbackups match | Werkelijk herladen/loadedbindings/combinatiebehoud nog niet in C7 gemeten |
| Uitbreiding30/40 | Geen nieuwe gameplayvoortgang/verbeteringsclaim | Zeven nativeactivatie/meting, latere nuttigeuitbreiding/vergelijking/science/transport blijven open |

Uitvoerder bronperiode afgerond en gestopt voor rootreview; geen actieve game/backgroundrun, timer, afsluithelper/commando/planning. PROJECTSTATUS.md uitsluitend door root. Geen nieuwe starteigendom door dit document; volgende concrete oplevering is rootvrijgave of gerichte reviewcorrectie.
