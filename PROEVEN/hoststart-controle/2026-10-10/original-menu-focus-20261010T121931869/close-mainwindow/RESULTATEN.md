# Afzonderlijke normale afwikkeling na de menuproef

Afgerond:10 oktober2026,12:41 Europe/Amsterdam. **EXIT_CONFIRMED_NO_CRASH_OBSERVED.** Uitvoerder gestopt; geen vervolgbediening/installatie of achtergrondrun.

Root las en gaf de volledige voorbereide batch vrij, SHA256 `240119728ff2118262ec345e7cbed0518918260ac4ac9659b7d4454c25213481`, parser0fouten. Afzonderlijk B-voorstelSHA `7bee59f2849ff7ded3bc599b637ab1f1286b928760220cb19fd279814c353931` was gereviewd en uitgelegd. Batchexactheid vóór de enige uitvoering opnieuw gecontroleerd; `rootreview-execution.json` en `batch-stdout.txt`. Oude C1-evidence, inclusief de oorspronkelijke nul-aanvraag/tijdguard, behouden.

| Controle | Gemeten resultaat / bewijs |
| --- | --- |
| Budget12:40:56.503 | Week91/vijfuur43, stateok, bron12:40:40.636/leeftijd15.9s; `budget-preflight.json` |
| Preflight | Alle15 pins en nieuwe toolhash gelijk, C1-no-callcount0 bevestigd, profielvoorafbytekopie gelijk; `preflight.json` |
| Eigen identiteit | PID14288/CIM CreationUtcMs1791628012889/exact `C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe`; Process.Path/StartTime gelijk; HWND984984/eigenaar14288; alle-civctpcount1 |
| Modalguard/rebinding | Twee succesvolle bindings; uitsluitend eigen CivCTP-hoofdvenster zichtbaar, twee eigen IME-vensters onzichtbaar; geen bekende modal waargenomen. Laatste guard12:40:57.115503; `process-checks.json` |
| Enige sluitaanvraag12:40:57.118064 | Eén `CloseMainWindow()`, retourtrue/exceptionnull, retour na3.154ms; `close-request.json` |
| Exitquery12:40:58.273553 | Succesvolle oorspronkelijke-PIDcount0 én alle-civctpcount0; bewaard Process-object HasExitedtrue/ExitCode0; eigen observatie1165.363ms, geen late OS-terugkeer. Overige5/9.9s-meetmomenten vervielen bij bewezen exit. |
| Application1000/1001 | Query geslaagd,0 passende events in uitsluitend aanvraag/observatievenster12:40:57.118064–58.290498; `application-events.json` |
| Postflight | Alle15 pins/tool gelijk; profielvoorna bytegelijk SHA `72a99e860698508c876750d944a75d93111c56789117ee6c9480d7e341d4d1fd`, gewone mtime bijgewerkt naar UTC10:40:57.167440 en state behouden; `eindhashes.json`/beide profielsnapshots |
| Eindbudget12:41:15.827 | Week91/vijfuur43 stateok; bron12:40:40.636/leeftijd35.2s; `budget-final.json` |

Tijden zijn10 oktober2026 Europe/Amsterdam behalve expliciet UTC. Aanvraag en maximaal10s-observatie liepen in dezelfde vooraf gereviewde batch zonder model-/toolpauze. Geen blokkerende WaitForExit, tweede aanvraag, focus, Capture, toetsen/klik, andere-appbediening, Kill/Start/Restart, reader/T0, DLL-/config-/profielwijziging of pcshutdown uitgevoerd. Normale gebruikersstate behouden; geen rollback.

Acceptatie: eigen instantie afgewikkeld en alle civctp op het geslaagde meetmoment afwezig. Code0 en afwezige passende crashevents ondersteunen de genoemde uitkomst; volledige interne normale shutdown is niet afzonderlijk bewezen. Eerder C1-MENU_PASS blijft het aparte menubewijs. Geen H1/H3/AI-/cache-/gameplayacceptatie uit deze sluitstap.

Volgende concrete handoff: root beoordeelt exit/count0/pins, werkt PROJECTSTATUS/VERSIES bij en bepaalt het afzonderlijke H1-I-vervolg. Deze agent stopt na afwikkeling; geen volgende start/installatie zonder nieuwe opdracht en verse procespoort.
