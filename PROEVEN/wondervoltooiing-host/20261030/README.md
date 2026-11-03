# Labyrinthvoltooiing: C0 ter rootreview

2 november 2026. Alleen offline voorbereid en gecontroleerd; niet toegepast of in gameplay gemeten. Geen Prepare, installatie, spelstart, proceshandle of GUI in deze C0. Rootreview blijft de poort voor livewerk. Geaccepteerd voorstel: ONTWERP/WONDERVOLTOOIING-PROEF-2026-10-30.md. Pc blijft aan.

## Kleine aanvulling op C4

De C4-reader PROEVEN/wondergewicht/20261030/Lees-Wondergewicht.py blijft bytegelijk. Geen nieuwe reader, geheugenvelden, native calls of proceswrites. De lokale Beheer-Proef.ps1 behoudt de C4-herstelroute en gebruikt alleen de kandidaat30000/alias 000-WONDERCOMPLETE-CANDIDATE-T0, dezelfde 9280c97a-archiefsave, eb6 en deelnemers. Baseline: 162 pins, 118 aidata, 38 saves. Niets permanent installeren. Alle 107 oude C4-bronpinnen blijven behouden; eigen pins.json voegt de bestaande lokale helpers, hun offlinecheck, C4-reference-after-n1 en gedeelde bedien-/budgethelper toe. Alle bronhashes worden voor beheer/invoer en bij complete gecontroleerd.

Stap-Proef.ps1 is de minimale lokale N-runner; Stap-Origineel.ps1 blijft een bytegelijke referentiekopie van de oorspronkelijke een-N-helper in wondergewicht-host/20261030/Stap-Proef.ps1. Beide zijn gepind. De lokale runner accepteert alleen kandidaat30000, NIndex 1..21, exact 'n' en een expliciete BeforeSnapshot. guard.py heeft alleen zuivere bestands-/JSON-controles. Iedere consumed-marker ontstaat met CreateNew voor input. Een N wordt nooit opnieuw verzonden, ook niet na een onbekende uitkomst of een marker zonder completed-record.

De voormeting moet rechtstreeks in de C4-map staan met een unieke completion-*.json-naam. Zij bindt exact PID, volledige FILETIME en executable aan het eigen candidate/start.json; codechecks/binding/variant zijn gelijk aan de gepinde C4-reference. Stable_twice moet true zijn, AI IDs exact 2..8, native-ronden alle 25+NIndex-1. Vanaf N2 is de volledige weight30000-expectation 7/7 PASS vereist. Vanaf N2 is de voormeting exact het pad en de hash van de vorige nameting. Iedere consumed-marker bevat bovendien start-hash en hash van de vorige completed-marker; de hele eerdere keten wordt herlezen. JSON-dubbelkeys, beschadigde pins/binding, foutieve ronden, dubbele/incomplete markerreeksen en gewijzigde snapshots worden geweigerd.

Na iedere N roept de runner dezelfde C4-reader aan met exacte PID/full FILETIME en gepinde deelnemers. Nieuwe output staat direct in de C4-map als completion-<Name>-after-N<NN>.json; bestaande output wordt nooit overschreven. Alleen een volledige stabiele nameting met alle zeven native+1 en 30000 PASS maakt N<NN>-completed.json. N21 wordt afzonderlijk als native46 gevalideerd; N22 blijft verboden. Completed betekent uitsluitend geslaagde beurtmeting, geen wondervoltooiing.

## Liveprocedure na rootreview

Ruim vers bevestigd budget, media- en procescontrole en vaste omstandigheden zoals B/C4. Maximaal 21 n totaal, input uitsluitend binnen 780 seconden sinds processtart; host maximaal 900 seconden. Voor iedere n wordt de verse budgethelper gecontroleerd; unknown/stop weigert invoer. Een gebonden foreground-capture gaat aan consumptie vooraf, daarna worden exacte procesidentiteit en inputdeadline opnieuw gecontroleerd. Lees het scherm: passieve menselijke speler1, alle observatiepanels gesloten, geen onverwachte modal, geen defeat. Een invoercommando bewijst geen beurt.

Maak eerst met de ongewijzigde C4-reader een unieke completion-before-N01.json (run-id WONDERCOMPLETE-20261030, variant B2a-N30-TECHNICAL, wonder-arm candidate, bestaande deelnemers, native25); bewaar begin-Info/Wonders als visueel bewijs. De runner zelf start geen spel en laadt geen save. Roep voor een gecontroleerde beurt aan:

```powershell
./Stap-Proef.ps1 -Arm candidate -Name n01 -Action Key -Keys n -NIndex 1 -BeforeSnapshot C:/GIT/ctp/PROEVEN/wondergewicht/20261030/completion-before-N01.json
```

Gebruik bij N2..N21 exact de voorgaande geaccepteerde after-snapshot en een nieuwe Name. Automatisch doorgaan is niet ingebouwd: inspecteer iedere toestand/meetuitkomst. Bij n-fout of afgewezen nameting blijft consumed bestaan en stopt de runner. Niet opnieuw n sturen. Lees een eventuele melding eenmaal; echte Labyrinth+AI-leider-completion kan visueel doorslaggevend zijn terwijl de all7-marker pending blijft. Readerchecks worden nooit versoepeld of markers gefingeerd. Uitsluitend als de toestand normale verwerking toelaat, kan dezelfde verbruikte N met een nieuwe Name read-only worden nagemeten:

```powershell
./Stap-Proef.ps1 -Arm candidate -Name n01-resample -Action Complete -NIndex 1
```

Complete bevat geen toetsaanslag en is tot de hostdeadline toegestaan. Bij blijvende afwijking: bewaar pending N/status en wikkel af. Stop bij doorslaggevend bewijs, defeat, onverwachte modal, budget/deadline of native46. Queueverdwijning/global-built UNKNOWN bewijzen geen voltooiing. Vereist: Info/Wonders-eigenaar+stad tegenover ondubbelzinnige beginstatus, of bij verborgen beginstatus echte voltooiingsmelding met Labyrinth+AI-leider.

Normaal sluiten/count0, autosave archiveren, lokale Restore uitvoeren, daarna volledige 118-aidata-/38-save-inventaris plus 162 pins en alias/8 tijdelijke partials exact controleren zoals C4. Bestaande saves en gebruikerswijzigingen blijven behouden. Geen pc-afsluiting. Volledige Doel4 blijft OPEN, ook na eventueel voltooiingsbewijs.

## Offlinecontrole

check_c0.py gebruikt kleine tijdelijke JSON-fixtures en de bestaande C4-bewijs-/backupbestanden. Geen readeruitvoering of speltoegang. Het resultaat staat in C0-CHECK.json; omvat 21/22, duplicate/pending/volgorde, completed-hashketen, PID/full FILETIME/binding/code/ronden/deelnemers/gewicht en volledige bronpins plus exacte oude herstelbackups. Deze controles bewijzen alleen voorbereiding, geen gameplayverbetering of wondervoltooiing.

