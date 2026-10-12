# H1-I-hoofdmenucontrole: menu, exit en herstel gemeten

Afgerond:10 oktober2026,13:00 Europe/Amsterdam. **MENU_PASS; EXIT_CONFIRMED_NO_CRASH_OBSERVED; origineel hersteld en15pins gelijk.** Uitvoerder gestopt. Geen volgende start/installatie of gameplayproef.

Root gaf frozen B-voorstelSHA `8febdf78044f82d67023bfb84b07cb29bd79964546b6987aa9420b080a75f5e0` en volledige voorbereide controllerSHA `ef65d8446606710ef20329fd087717311a5c8ed9d0ad818b153dfd079dc34c28` vrij; parser0fouten. Exact één controlleruitvoering, alle code/typen/afwikkeling/herstel vooraf gereed. Geen model-/beeldpauze tijdenslive.

| Acceptatie / meetpunt | Werkelijk resultaat en bewijs |
| --- | --- |
| Preflight | Succesvolle alle-civctpcount0;15originele pins/tool/H1variantmanifest/pakketmanifest gelijk; profiel/compat/CD/display gelijk aan originele C1-eindstate. DLL/profiel/vaste screenshot bewaard; `preflight.json` |
| Enige tijdelijke wijziging | Alleen proef-robotcom.dll gekopieerd van origineleSHA `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44` naarH1-I SHA `59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0`; overige14pins gelijk; `temporary-install.json` |
| Eén Start12:56:25.683 | Helperexit0; nieuwe PID15464 direct gebonden12:56:26.225 aan exact proefexe/CreationUtcMs1791629786118; `start-record.json` |
| Intro180s | Eerste eigen bindingssample+639.696ms, aanvankelijk HWND0 toegestaan; directe polls vanaf startbinding, geen input/intro-overslaan; `window-timeline.jsonl` |
| Definitieve HWND12:59:28.298 | Handle6489958/eigenaar15464/foreground/bounds1920x1080,2478.809ms stabiliteit; `final-window-binding.json` |
| Eén Capture12:59:29.827 voltooid | +184.144s; trace896.582ms, poll/350ms/voor-na-copy dezelfde identiteit/eigenaar/foreground, geen fout/late return; `capture-trace.txt`/`capture-result.json` |
| Actuele afbeelding | `menu-01.png`, SHA `b83200b1d878bd59f54e8232b4dee80c9d5b1c2c27299aa4986a4926594f85eb`; uitvoerder en root werkelijk bekeken: herkenbaar gewoon menu Single Player/Multiplayer/Quit/Credits, MENU_PASS. Afbeelding bytegelijk aan originele C1-menuopname. |
| Eén normale aanvraag12:59:30.077 | Onmiddellijk na opnamebewaring, twee verse eigen modal-/identiteitsguards; alleen CivCTP zichtbaar. CloseMainWindowtrue/exceptionnull,4.922ms; `close-request.json`/`process-checks.json` |
| Exit12:59:31.135–31.141 | Succesvolle oorspronkelijkePIDcount0 én alle-civctpcount0, behouden Process.HasExitedtrue/ExitCode0,1067.904ms sluitobservatie; overige meetmomenten vervielen. Live185.466s binnen240s. |
| Application1000/1001 | Query geslaagd,0 passende events in start/observatievenster12:56:25.683–12:59:31.148; `application-events.json` |
| Origineel herstel12:59:31.851 | Nieuwe succesvolle alle-civctpcount0 direct vóór kopiëren; actueleH1-I en eigen originelebackuppin bevestigd; uitsluitend proef-DLL teruggekopieerd en exact3025070...35d44 geverifieerd; `restore.json` |
| Postflight |15originele pins en tool gelijk. Profielvoorna bytegelijk SHA `72a99e860698508c876750d944a75d93111c56789117ee6c9480d7e341d4d1fd`; gewone gewijzigde mtime UTC10:59:30.133835 behouden; `eindhashes.json` |
| Budget | Gates vóórinstallatie/Start, rond90s, vóórCapture en vóórherstel geslaagd. Eind13:00:11.001 week89/vijfuur27 stateok, bron12:59:47.782/leeftijd23.2s; `budget-final.json` |

Tijden zijn10 oktober2026 Europe/Amsterdam behalve expliciet UTC. Eén Start/Capture/Close; geen retry, andere-appbediening, focusforcering, toets/klik, Kill/Restart, reader/T0/nieuwe partij, H3/B2/B4, configuratiewijziging of shutdown. Bestaande saves/gebruikerswijzigingen en eerdere proefevidence behouden. Normale profielstate behouden; geen profielrollback.

Conclusie tegenover meetlat: de huidige H1-I-schijfvariant bereikt onder dezelfde bekende inputs een herkenbaar hoofdmenu, net als origineel. De eigen instantie is gemeten afgewikkeld en de originele DLL is aantoonbaar teruggezet. Code0 en afwezige passende crashevents ondersteunen de genoemde exituitkomst; volledige interne normale shutdown is niet afzonderlijk bewezen. De historische crashoorzaak9okt blijft onbekend. Menu/schijfhash bewijzen geen geladen H1-payload, scorecallback, AI-/cacheactivatie, H3-goals, overhead of gameplayverbetering. Geen nieuwe Deity-T0-meting.

Root heeft afbeelding en controller-/exit-/restore-/eindpinrecords gelezen en deze hostuitkomst aanvaard. Volgende concrete handoff: root legt versie/status vast en reviewt afzonderlijk het H3-T0-hervatvoorstel. Deze taak geeft geen vervolginstallatie/startmandaat; uitvoerder gestopt.
