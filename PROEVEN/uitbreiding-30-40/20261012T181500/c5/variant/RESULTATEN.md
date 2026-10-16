# C5: twee zwarte opnames, normaal afgewikkeld zonder invoer

13 oktober 2026, 17:56 Europe/Amsterdam. Eén vrijgegeven variantarm uitgevoerd en gestopt. Geen input, T0-load, RPM, T1 of gameplaymeting. Pc blijft aan; geen tweede start gepland.

## Feitelijke uitvoering

Eigen vers budget17:50:28: bron15:50:11UTC/leeftijd16.7s, week79/vijf65/stateok. Succesvolle verse OS-allcount0 op17:50:31 (`prestart-process.json`). Controller maakte uitsluitend eigen bytegelijkeT0alias `000-U30-40-START-T0`; SHA256 `8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26` gelijk aan gepindeQUOTA-START-T0. Tijdelijke kandidaat `f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810`; overige18releasefiles bytegelijk.

Procesbinding: PID24236/exact `C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe`, creation_utc_ms1791906636604 (17:50:36.604 Amsterdam), HWND2951230. Bekende intro afgewacht zonder input. Controller start-record/final-window-binding bewijzen dezelfde unieke instance en stabiele HWND/foreground na180s; dit bewijst **geen zichtbaar hoofdmenu**.

Twee C5Capture-aanroepen via de bestaande ongewijzigde Bedien-CTP-tool, zonder voorafgaande externe RequireFocusGuard:

| Opname | Tijd Amsterdam / elapsed | Feitelijk resultaat |
| --- | --- | --- |
| menu.png | 17:53:52.230 /196.8307s | PNG1920×1080 volledig zwart bij originele visuele inspectie; actuele fysieke bounds1920×1080, HWNDforeground2951230. |
| menu-confirm.png | 17:54:16.037 /220.6352s | PNG1920×1080 opnieuw volledig zwart bij originele visuele inspectie; actuele fysieke bounds1920×1080, HWNDforeground2951230. |

Beide calls slaagden volgens technische capture/focus/dimensionvoorwaarden; bijbehorende physical-bounds.json bewaren de exacte meetmomenten. Geen `focus-restore-attempt.json`: OwnState foreground matchte vóór de toolaanroepen. De max-één herstelroute is daardoor **niet daadwerkelijk getest**. De oorzaak van de zwarte beelden is onbekend; deze bewijzen geen zwarte feitelijke game-UI of onuitvoerbare save-laadroute. Schermverificatie is in deze poging wel concreet geblokkeerd. Geen blinde Click/ResetCursor of andere helper/input gebruikt.

Geen Single Player, Load Game, Julius- of aliasselectie zichtbaar bevestigd; T0.json/T1.json en n-passrecords ontbreken. Exact geladen nieuwe RX/payload/negenwindows/vtableslot/B2/vijfhooks en native−1→0 zijn niet uitgelezen. Geen all7 Gcert/Dorig/R of nuttigeuitbreidingclaim.

## Normaal sluiten en werkelijk herstel

Eén Finish: CloseMainWindow17:54:43.933 Amsterdam/call_count1/bool_returntrue (circa247.3s na processtart, vóór420s). HasExitedtrue17:54:44.478, exit_code **null/onbekend**. Geen force/kill/retry/shutdown.

Controller `restore.json` en eigen `postrestore-audit.json` op17:55:33.506 bewijzen succesvolleallcount0,19/19actualreleasehashes,9/9bestaandesavehashes,profilematch en9/9rootvrijgegevenbron/protocolpins. Geteste release DLL `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890` hersteld. ProfielSHA `72a99e860698508c876750d944a75d93111c56789117ee6c9480d7e341d4d1fd` behouden.

DefaultAUTOSAVE-Julius bleef SHA `c5c222bbe06d91e8ddab236bb6053ea08b01bc2ea9ee95d2c67f6640490c46d6`; `autosave-archive.json` statusUNCHANGED_DEFAULT. Geen nieuwe save of versiearchief nodig/gemaakt. Eigen alias na releaseherstel/count0 en originalT0hashcontrole verwijderd op17:54:45.403 (`T0-alias-cleanup.json`); postauditaliasabsent. Geen onverwachte gebruikersbytes gewijzigd. C4-bronnen/resultaten/gate ongemoeid; C5executionrecord verbruikt, niet herstarten.

## Werkperiode per tussendoel

| Tussendoel | Nieuwe opbrengst / acceptatie | Open / volgende concrete oplevering |
| --- | --- | --- |
| Echteactivatie Doel1/1a | Tijdelijkeinstallatie, eigenprocesbinding, tweeexactgebondencaptures en normalecleanup bewezen; gameplay open | Rootreview/twee zwartePNG+bindings terug naarontwerper voor gerichte uitvoeringsvraag: waarom deze bestaande opname geen controleerbaar menu oplevert. Geen vervangende strategie door uitvoerder. T0/éénT1/7AI/loadedbindings blijven ontbreken. |
| Doel3behoud | Werkelijke19release/9saves/profiel ongewijzigdherstel bewezen | B2 in combinatie nognietlivegemeten; eerdere bewezen releaseacceptatie behouden. |
| Uitbreiding30/40 | Geen nieuwe gameplayvoortgang | Nuttigeuitbreiding/vergelijking/science/monopoly/transport/all7telemetry blijvenopen. C1/C2technischbewijs ongewijzigd. |

Laatste eigen budget17:55:35: bron15:55:06UTC/leeftijd29.1s, week78/vijf59/stateok. Geen budgetstop en geen auto-review rejection. Run en uitvoering gestopt; alleen verslag/checkpoint gemaakt. Nieuwe livearm vereist afzonderlijk gereviewde route/vrijgave, geen automatische tweede start.
