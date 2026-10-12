# Eén originele-DLL-hoofdmenucontrole

Checkpoint: 2026-10-09 21:27:59 +02:00, Europe/Amsterdam. Alleen één Start uitgevoerd; verdere bediening stopte onmiddellijk bij focusweigering vóór60s. Geen retry of vervolgcontrole/exitinvoer.

| Tussendoel/checkpoint | Aantoonbare delta | Huidige acceptatie | Volgende oplevering |
| --- | --- | --- | --- |
| Wijzigingen daadwerkelijk actief / originele hostpoort | Originele pins/knowninputs gelijk; StartPID20536; +5s exact proefproces en zichtbaar hoofdvenster/responding gemeten | Menu NOT_OBSERVABLE door Capture-focusweigering; exit NOT_CONFIRMED | Normale zichtbare afwikkeling van PID20536 door root/gebruiker, daarna rootreview over eventuele vervolgrichting |
| Goede locaties kiezen / H3 | Geen gameplaydelta; geen variantinstallatie/T0/AIorders/reader | Bestaande offlineacceptatie blijft; runtime/gameplay open | Afzonderlijke proeven pas na bevestigde exit; deze opdracht voltooit die poorten niet |

Vooraf: [preflight.json](preflight.json) bevat15pins, originalebackup/tool/designhash en compat/Profileinputs; alle overeenkomstig B. Resultaatmap vooraf afwezig; Capture-voorbeeld bytegelijk bewaard als capture.before.png met hash/mtime. Verse budgetbron21:25:41, hercontrole21:26:19:five32/week12/warn, age38.7s;geenstopredenen. Succesvolle unsandboxed CIMcount0 vóór Start. Geen compatibility/display/CD/profielwijziging verricht.

Enige Start: 2026-10-09T21:26:44.1076473+02:00; deadline 2026-10-09T21:27:44.1076473+02:00. [start.txt](start.txt) meldt PID20536; [start-record.json](start-record.json) bindt exacte executable en CreationDate. [process-01.json](process-01.json) legt eerste meetmoment vast. Status: CivCTP, mainwindowhandle330040, respondingtrue, visibletrue. Capture faalde: 'Unable to foreground the game window.' Deze fout wordt als [capture-error.txt](capture-error.txt) bewaard. Geen nieuwe capture/screenshot verkregen, dus geen menuherkenning mogelijk. De helper stopte vóór invoer/opname. Responding/windowtitle/toolstart zijn geen menubewijs. Latere +20/+40-bediening verviel wegens directe toolweigering; niet nogmaals geprobeerd.

Normale afwikkeling: geen herkenbaar menu/cursor/focus, daarom geen Exit/Quitklik of blinde toets. Geen Kill/Restart. [process-final.json](process-final.json) bevestigt op21:27:13.543 nog één exacte CTP-proefinstantie PID20536 met CreationDate1791574004358. Laatste bekende handle330040/titleCivCTP. Root heeft direct handoff ontvangen. Deze instantie blijft open; normale zichtbare afwikkeling vereist voordat een nieuwe installatie/start plaatsvindt. Er is geen crash/verdwenen PID gemeten; daarom geen crashdiagnose of Applicationeventquery.

Bestanden: [eindhashes.json](eindhashes.json) bevestigt alle15pins en tool gelijk; DLL bleef origineel3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44, geen herstelinstallatie. userprofile.before.txt en userprofile.after.txt bewaard; inhoud gelijk=True, beforemtime21:09:14.4199111, aftermtime=2026-10-09T21:26:45.0858998+02:00, huidigehash=72a99e860698508c876750d944a75d93111c56789117ee6c9480d7e341d4d1fd. Actuele gebruikersstate behouden; geen rollback. Oude screenshot niet als nieuwe menu-evidence gebruikt.

Begrenzing: geen H1/H3/B2/B4-installatie, load/newgame/T0/reader/AIpass/orders. Geen H1causaliteit/loadedbytes/score/heap/overhead/gameplayclaim. Eén hoofdvenster zonder opname is NOT_OBSERVABLE. Uitvoerder stopt na checkpoint; PID20536 blijft volgens laatstequery actief. Pc aan, geen shutdown/helper/timer.
