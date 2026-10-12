# H1-I/T0 herhaling — uitsluitend voorbereid

11 oktober 2026, 16:12 Europe/Amsterdam. **PREPARED_ONLY_NOT_AUTHORIZED_NOT_EXECUTED**. Uitvoerder stopt voor rootreview en een nieuwe specifieke gebruikersmachtiging. De eenmalige proef van 10 oktober is afgehandeld; die geeft geen toestemming voor deze nieuwe Start.

Oorzaak: de vorige eenmalige uitvoering stopte vóór laden/A/n/B door verouderde budgetmetadata. Een verse accountreset is door root bevestigd. Deze voorbereiding gebruikt het reeds gereviewde protocol en bouwt geen nieuwe observer, controller of testframework. De huidige map is nieuw aangemaakt; oude scripts/resultaten blijven intact.

Bevroren voorstel ONTWERP/H3-T0-HERVATTING.md, SHA256 21fcf7cadf2c459f99ed45047f612aba11fe98a0234d1d898c496d3e2f64ecec, blijft ongewijzigd. De datum/run-/outputnamen uit het oude protocol zijn uitsluitend voor deze eventuele H1-I-herhaling geïsoleerd volgens onderstaande tabel. Geen H3-arm vrijgegeven.

| Onderdeel | Nieuwe concrete waarde |
| --- | --- |
| Eigen arm | PROEVEN/activatie-h3-runtime/2026-10-11/20261011T161002/H1-I |
| Arm/variant | H1-I |
| Run-ID | h1-20261011-161002 |
| Snapshot A | C:\GIT\ctp\PROEVEN\ai-uitlezen\activatie-h3-runtime-20261011-161002-h1-A.json |
| Snapshot B | C:\GIT\ctp\PROEVEN\ai-uitlezen\activatie-h3-runtime-20261011-161002-h1-B.json |
| B --before | Exact het bovenstaande eigen A-bronbestand in ai-uitlezen |
| Archiefkopieën | Eigen arm/A.json en B.json; bestaande bytekopie-/instancechecks behouden |
| Passlabel / turns | T0-to-T1; A turn0 en B turn1 na extern bewezen enige normale pass |

De bestaande vier-output-afwezigheidsgate blijft behouden. Naast beide H1-namen reserveert zij activatie-h3-runtime-20261011-161002-h3-A.json en -h3-B.json uitsluitend als afwezigheidspins; hier staan geen H3-scripts of uitvoering. Alle vier namen zijn bij voorbereiding afwezig. De exacte parent PROEVEN/ai-uitlezen, prefix activatie-h3- en .json blijven bij de bestaande reader passen. Deze voorbereiding heeft daar geen output aangemaakt.

Vier scripts rechtstreeks uit PROEVEN/activatie-h3-runtime/2026-10-10/20261010T130836622/H1-I gekopieerd. source-copies/ bewaart de oorspronkelijke bytes, inclusief eigen close-mainwindow/Finish. preparation-manifest.json bevat bronpad, oude hash, kopiehash, nieuwe hash, omvang en bytegelijkheid. Wijzigingen uitsluitend:

- Start: vier concrete observeroutputnamen krijgen de nieuwe datum/tijdlabel.
- Read: twee concrete outputpaden en de ene run-ID krijgen dezelfde nieuwe isolatie.
- Guard en Finish: bytegelijk aan hun gereviewde bronnen. PSScriptRoot en Split-Path binden vanzelf de nieuwe eigen map.

De inverse naamvervanging geeft ieder script exact de oude bronbytes terug. scripts.diff is volledig gelezen. Historische originele-menu-/cleanupverwijzingen zijn bewust niet naar nieuwe niet-bestaande bewijsbestanden veranderd. Alle overige bytes behouden: 480s livegrens, 470s reserve, exacte PID/CreationDate/Process.StartTime/exe/HWND/eigenaar/focusbinding, budgetstop met één unknown-hercheck, 15pins en profiel-/compatpoort, geladen-bytechecks, eigen A/B-/archive-instancebinding en normale exit/count0 vóór herstel. Geen logica of guard afgezwakt.

De twee gewijzigde scripts alleen met PowerShell Parser.ParseFile gecontroleerd: nul syntaxfouten, vastgelegd in syntax-checks.json. Geen script aangeroepen. De eerdere ongewijzigde Guard/Finish-tests zijn niet herhaald. Opnieuw gelezen huidige15pins matchen hun bestaande bron; C0-tool, reader en observerpakket matchen de bestaande hashes. Huidige profielhash is uitsluitend gelezen en in manifest opgenomen; geen profielbackup/rollback of werk-DLL-backup gemaakt. Live proces-/focus-/compatbudgetpoorten zijn niet uitgevoerd als spelproef; die moeten vlak vóór een eventueel specifiek toegestane Start opnieuw slagen.

Reviewpins:

| Bestand | SHA256 |
| --- | --- |
| Start-H1-T0.ps1 | d8c2dd20dc1a4808e473dfc3b4c8b4d75efb6eeba22a466833d165a4d9503c71 |
| Guard-H1-T0.ps1 | 250c38402d22b54c872c4aed6c77a6b51f583d593b39b7d7f6731617c3886bdc |
| Read-H1-Snapshot.ps1 | 84db77245d41952c70d8662b265032fe120ae8d1bac8abfc9efe6a7ca808d5fc |
| close-mainwindow/Finish-H1-T0.ps1 | 31d0d33a5c7f58b5386c40735e9c1f582f098151d2c3274ed394acb27d921728 |
| preparation-manifest.json | 4f9d4c7b726fae23b34cfaef8d2c8231fd3a1d2800e168644649ad7adf6d00b6 |
| scripts.diff | 6be34fd3fa30ce88f55dcd398562ada6bfd8ca824a97493aad0fc23cb92d3d62 |

Geen tijdelijke DLL geïnstalleerd, werk-DLL-backup gemaakt, Start, GUI, load, reader, pass, close of herstel uitgevoerd. Geen B2/B4/B5/H3-wijziging meegeleverd. Geen activatie-/gameplayacceptatie geclaimd. Voor toekomstige uitvoering gelden hetzelfde vaste QUOTA-START-T0, slechts één n, normale sluiting en originele DLLherstel na bewezen exit/count0; uitvoering vereist eerst nieuwe specifieke toestemming via root, geen automatische reviewafwijzing omzeilen.

Laatste verse budget16:11:47: bron17.3s oud, week96/vijf72, stateok. Werk stopt nu; rootreview van hashes/diff en nieuwe gebruikersmachtiging zijn de volgende poorten. Pc blijft aan.
