# C4 activatiepoging — normaal gestopt zonder T0

13 oktober 2026, 17:05 Europe/Amsterdam. Uitvoerder gestopt; geen spel- of helperproces draait. Pc blijft aan. Eén rootvrijgegeven activatie uitgevoerd; geen tweede start, bronwijziging of baseline.

De variant is tijdelijk toegepast en het menu is bereikt. De vaste save is **niet geladen**; geen RPM, T0-snapshot, T1-invoer of native ronde uitgevoerd. Geladen nieuwe payload en gameplayverbetering zijn daarom niet aangetoond. C1/C2 blijven de vooraf geaccepteerde technische onderbouwing.

## Feitelijke route en identiteit

- Verse prestartcontrole 16:57:47: succesvolle OS-query, alle civctp-processen count0. Budget 14:57:35UTC/leeftijd8.5s: week84/vijf95/stateok.
- InstallStart maakte uitsluitend de eigen alias `000-U30-40-START-T0`; bron en alias SHA256 `8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26`. Werkvariant DLL SHA256 `f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810`; overige 18 gepinde bestanden gelijk aan release.
- Eigen civctp PID8304, executable `C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe`, creation_utc_ms1791903488213, HWND918392. Na bekende intro stabiel hoofdmenu/focus gebonden; `start-record.json`, `final-window-binding.json`, `menu.png`.
- Hoofdmenu→Single Player→Load Game op scherm bevestigd. Alle klikopdrachten via ongewijzigde Bedien-CTP.ps1 na eigen Guard en vergelijking actuele bounds met de vorige opname. Originele afbeeldingen bekeken; menu1920×1080, Load Game2171×1080, beide matchen hun fysieke windowbounds.
- Klik naar1042,437 vanaf opgegeven1300,426 selecteerde **Alexan**; `julius.png` toont veld Game:Alexan en alleen AUTOSAVE-Alexan. De bestandsnaam van deze opname bewijst geen Julius-selectie. Zichtbare internecursor circa1034,426; kleine correctie naar1040,438 voorbereid.
- Deze correctie werd vóór invoer door de controller Guard geweigerd: `Own game not foreground; no input.` Buitenste command eindigde met `Guard failed`; geen klik/capture uitgevoerd, `julius-confirmed.png` ontbreekt. Waargenomen focusverlies is een concrete uitvoeringsblokkade in deze poging, geen bewijs dat de route technisch onmogelijk is. Geen focushelper, resetcursor, langdurig zoeken of CD-vraag toegevoegd.

## Normale afwikkeling en behoud

Finish één keer: CloseMainWindow op17:03:54.947 Amsterdam, bool_return=true/call_count1. HasExitedtrue op17:03:55.304; exit_code **null/onbekend**, geen exit0 claim. Afwikkeling startte circa347s na start, ruim vóór420s. Geen force/kill/shutdown.

Controller bevestigde count0 en herstelde alle19 true backups. `restore.json` en onafhankelijke eigen `postrestore-audit.json` op17:04:40 bevestigen19/19 werkelijke releasehashes,9/9 bestaande savehashes en profielhash gelijk. Geteste release DLL SHA256 `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890`; profiel `72a99e860698508c876750d944a75d93111c56789117ee6c9480d7e341d4d1fd`.

Default AUTOSAVE-Julius bleef ongewijzigd: `c5c222bbe06d91e8ddab236bb6053ea08b01bc2ea9ee95d2c67f6640490c46d6`. Geen nieuwe save of archief gemaakt. Eigen alias uitsluitend na releaseherstel/count0 en opnieuw gecontroleerde originele T0-hash verwijderd; `T0-alias-cleanup.json`. Acht rootvrijgegeven bronpins zijn nog bytegelijk. Oude C3-bronnen/resultaten ongemoeid; C4 executionrecord verbruikt, niet herstarten.

## Voortgang per tussendoel

| Tussendoel | Nieuwe oplevering / acceptatie | Open / volgende concrete oplevering |
| --- | --- | --- |
| Echte U30→40-activatie, Doel1/1a | Tijdelijke installatie, gebonden menu/laadvenster en normale cleanup bewezen; gameplay **open** | Rootreview van deze mislukte UI-poging; zo nodig terug naar ontwerper voor één beperkte uitvoeringscorrectie. T0 geladenbytes en7 native−1→0 ontbreken. |
| Doel3-behoud | Geteste release19/saves9/profiel na proef exact hersteld | B2-payload in combinatie nog niet live geobserveerd; behoud eerdere bewezen releaseacceptatie. |
| Nuttige uitbreiding30/40 | Geen nieuwe gameplayvoortgang | Benchmark, science/monopoly/transport, per-AI Gcert/Dorig/R en grotere gameplayvergelijking blijven open. Geen extrapolatie uit menu of offlinefixtures. |

Laatste eigen budget17:04:40, bron15:04:21UTC/leeftijd19.6s: week82/vijf88/stateok. Dit was een uitvoeringsstop na focusweigering, geen budgetstop of harde onuitvoerbaarheid. Volgende beslissing bij root/ontwerper; deze uitvoerder heeft geen nieuwe activatie gepland.
