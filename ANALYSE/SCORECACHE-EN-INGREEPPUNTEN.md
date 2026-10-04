# Locatiescore: savegedrag en punten voor nieuwe beoordeling

Alleen-lezen vervolg op [LOCATIEKWALITEIT.md](LOCATIEKWALITEIT.md). Geen spel gestart en geen executable, DLL of echte save gewijzigd. De gebruiker wil de beoordeling uiteindelijk aan de productie-, science- en monopolyvereisten aanpassen; zie [LOCATIESELECTIE.md](../LOCATIESELECTIE.md).

## 1. De scoretabel wordt opgeslagen en teruggelezen

De echte routine op **0052dbe0** gebruikt een archiefobject met een modusvraag en afzonderlijke schrijf-/leesaanroepen. In de schrijfbranch loopt zij z/x/y af en schrijft voor iedere locatie twee bytes uit objectveld +0x248c. In de leesbranch leest zij twee bytes uit het archief en schrijft die naar dezelfde tabel. Dit is het veld dat de aangetoonde GetSettleValue-route uitleest.

| Onderdeel | Aangetoonde code |
| --- | --- |
| Modus kiezen | 0052dc09–0052dc0e: archiefmethode +0x14, branch op resultaat |
| Scores schrijven | 0052dd61–0052dd90: +0x248c, 16-bit score, archiefmethode +0x0c met lengte 2 |
| Scores lezen | 0052df63–0052df98: archiefmethode +0x10 met lengte 2, daarna 16-bit toewijzing aan +0x248c |
| Tabel voor laden alloceren | 0052cdf0–0052ce7b: lagen, kolommen en rijen op basis van wereldafmetingen |
| Daarna de laadroute aanroepen | 0052ce8b: call 0052dbe0 |
| Andere directe archiefcaller | 0051c6f4: call 0052dbe0 met het globale RobotInterface-object |

Bewijs: [archiefroute](BINAIR/engine-score-cache-levensduur.txt), [allocatie en wrappers](BINAIR/engine-score-cache-en-masker.txt), [caller-detail](BINAIR/engine-cache-aanroepdetail.txt), [directe callkandidaten](BINAIR/engine-score-cache-callers.txt). Sommige expliciete disassemblagebereiken beginnen midden in een grotere functie; alleen gecontroleerde instructies/branches worden hierboven gebruikt. De afwijkende civctp.map levert geen implementatieadressen.

### Machinecodecontrole van bewaren en herstellen

[Controleer-Scorecache.py](../PROEVEN/Controleer-Scorecache.py) voert de originele instructies van 0052dbe0 uit in Unicorn met synthetische objecten. Archief-I/O is vervangen door een geheugenbuffer; de werkelijke code doet de iteratie en tabeltoewijzing. Er zijn geen AI-spelers in deze test, zodat hun afzonderlijke serialisatie buiten de controle blijft.

Twee tabellen van 2×3×2 en 3×5×2, respectievelijk 12 en 30 scores, zijn exact bewaard en hersteld. Ook een 16-bit patroon van 65535 blijft intact. Tussen bewaren en laden wordt de scoretabel gewist: herstel komt dus uit het archief. In beide uitvoeringen wordt 005237d0, de scoreopbouw, niet aangeroepen. Alle archiefbytes worden uitgelezen. Resultaten: [score-cache-controle.json](BINAIR/score-cache-controle.json).

Dit bevestigt de tabelserialisatie; het is geen proef met een echte spelstart, compressie, actieve AI-spelers of de volledige applicatielaadroute. Een eventuele herberekening elders na laden is hiermee niet uitgesloten.

**Gevolg voor ons experiment:** een nieuwe scoreformule alleen geeft geen garantie dat een oude save nieuwe waarden gebruikt. Voor een latere vergelijking moeten we aantonen dat de gewijzigde beoordeling bij laden wordt berekend of dat de oude cache expliciet wordt vernieuwd. Anders vergelijkt de proef mogelijk nog de oorspronkelijke tabel. Dit staat naast de afzonderlijke persistentie van het packing-masker.

## 2. Wanneer wordt de tabel opgebouwd?

De scoreopbouw op 005237d0 heeft twee gecontroleerde directe calls:

- **0052d02e**, aan het begin van 0052d020. Deze routine zet de RobotInterface-structuren op en start vervolgens AI-objecten voor spelers. De AI-startaanroep staat onder meer op 0052d21f; de caller van 0052d020 is 004f80c4.
- **0056a531**, in de dispatcher op 0056a200. De betreffende branch begint op 0056a41e en staat op index 2 van de springtabel 0056c720. Zij vervangt onder meer een kaart-/weergaveobject, roept de wereldroutine 00511170 aan en bouwt daarna de scores opnieuw op als het RobotInterface-object bestaat.

De dispatcher leest een typeveld uit een aangeboden bericht; de verwante routine op 0056a160 schrijft een bericht met beginbytes 49 49. Dit is geen bewijs van een gewone beginbeurt of een update na iedere verbetering. De precieze betekenis en aanroepcondities van berichttype 2 zijn nog open.

Ruwe referenties naar veld +0x248c zijn gevonden in allocatie, vrijgave, serialisatie en getters. Geen afzonderlijke incrementele score-update is hiermee aangetoond. Deze zoektocht sluit indirecte toegang via verkregen pointers, inlining of een andere applicatieroute niet uit. Bewijs: [ruwe referenties](BINAIR/engine-cache-ruwe-referenties.txt), [opbouwcallers](BINAIR/engine-score-cache-levensduur.txt) en [dispatcherbranch](BINAIR/engine-cache-aanroepdetail.txt).

## 3. Nieuwe waardering moet vóór de kandidaatselectie meetellen

Dezelfde kwaliteit wordt op meerdere plaatsen gebruikt:

1. **Kandidaten ordenen:** AiCellPtr-vergelijker 20078460 vraagt de score op via World-offset 0x168, op 200784bb en 20078517. Een uitgesloten maskerpositie krijgt in deze vergelijking waarde nul. De code vergelijkt de waarden als 16-bit getallen.
2. **Een vestigingsdoel maken:** InsertBestSettleGoal op 2007a7c0 haalt een kandidaat uit de priority queue, verwerkt selectievoorwaarden en vraagt op 2007aa35 opnieuw de score op. Bij een positieve waarde wordt op 2007aa92 een GoalSettle aangemaakt met die score als kwaliteit.
3. **Doelen laten concurreren:** GoalSettle::Compute_Raw_Priority op 20048820 combineert algemene planner-/ArmyGoal-prioriteit met kwaliteit × settle_value_coef en een typebonus. De vermenigvuldiging staat op 200488e3.

Bewijs: [kandidatenvergelijker](BINAIR/locatiewaardering-vergelijker.txt), [doelaanmaak](BINAIR/locatie-selectie-ingreeppunten.txt), [doelprioriteit](BINAIR/locatie-doelprioriteit.txt). Limieten, masker en bereikbaarheid zijn eerder afzonderlijk beschreven in [VESTIGINGSDOELEN.md](VESTIGINGSDOELEN.md) en [VESTIGINGSMASKER.md](VESTIGINGSMASKER.md).

**Ontwerpgevolg:** alleen een monopolybonus toevoegen aan de uiteindelijke doelprioriteit kan onvoldoende zijn. De locatie moet eerst door de kandidaatselectie komen, die al op de oude score ordent. Een nieuwe beoordeling moet daarom samenhangend in kandidaatordening, doelaanmaak en de latere prioriteit terechtkomen. Dit is een eis aan de implementatie, geen bewijs dat een tekstinstelling zulke logica kan invoegen.

Bij een aangepaste score moeten ook de 16-bit opslag/vergelijkingen, positieve-scorevoorwaarden en reeds opgeslagen doelkwaliteiten worden onderzocht. Kies geen willekeurig grote bonussen zonder te controleren wat die representatie en laadroute ermee doen.

## 4. Good-identiteit is via de bestaande interface beschikbaar

De globale kwaliteitsformule gebruikt alleen aanwezigheid van een lokaal good-slot. Er bestaat daarnaast een aparte engine-interface die de echte good-identiteit kan leveren:

- World-functietabel 007452e0, **offset 0xb4 → 00534310**.
- Deze wrapper zet de positie om en roept **00514f60** aan.
- Die controleert good-aanwezigheid via 004ffec0, leest het terreinrecord en selecteert het lokale good-record op terreinrecord+0xa0+slot×4.
- Op **00514fac–00514fb2** wordt good-recordveld **+0xa8** naar het meegegeven uitvoerveld gekopieerd.
- De actuele tokenmetadata geeft **GOOD_INDEX = 1028**. In de terreinparser 00467330 leidt index 1028−992 via de gecomprimeerde tabel naar case **00467a47**. Deze schrijft op **00467a86–00467a8f** de integer naar record+0xa8.

Deze keten koppelt de teruggegeven waarde aan GOOD_INDEX, onafhankelijk van de afwijkende engine-map. Bewijs: [interface en celroute](BINAIR/engine-locatie-kenmerken.txt), [tokenmetadata](BINAIR/engine-token-binding.json), [functietabel- en parserindices](BINAIR/engine-locatie-interface-binding.json), [GOOD_INDEX-toewijzing](BINAIR/engine-good-index-toewijzing.txt). World-offset 0xa8 geeft daarnaast de huidige terreinindex terug via 005342e0 → 00514b70; de koppeling van iedere index aan zijn terreinnaam moet apart worden gecontroleerd.

De bestaande handels-AI vraagt al per good-type stadsgegevens op: FindUnconnectedGoods op 20029360 gebruikt Player-interfaceoffset 0xb8, met een city-ID en een itererend good-type, op 20029457. De precieze betekenis van de twee teruggegeven tellingen is hier nog niet vastgesteld. Dit is een aanknopingspunt voor eigen voorraad, geen afgerond model van beschikbare of reeds gereserveerde monopoly-goederen. Bewijs: [handels-AI](BINAIR/goederen-identiteit-interface.txt).

**Gevolg:** een monopolybeoordeling hoeft niet uitsluitend op de onvolledige good-aanwezigheidsbonus te berusten; de engine kan good-identiteit via haar bestaande AI-interface aanbieden. Daarmee is nog geen FLI-input, ingebouwde monopolyselectie of uitvoerbare nieuwe mod bewezen.

## 5. Voorstel voor de technische opbouw

Onderzoek een beoordeling met twee samenwerkende onderdelen:

- **Terreinpotentieel:** bruikbare bergen, voedselvakjes, kust, huidige opbrengsten, verbeteringen en ontwikkeltijd; lokale goods per echte identiteit.
- **Prioriteit voor de huidige beschaving:** uitbreiding nu versus uitstel, een nog ontbrekende wonderstad, goederen elders in het eigen rijk, reeds geplande steden/settlers, beschikbare technologie en transport, en concrete dreiging.

Het eerste onderdeel kan waar zinvol worden gecachet. Het tweede moet veranderen wanneer de relevante toestand van het rijk verandert; het kan niet volledig worden weergegeven door één onveranderlijke wereldscore voor alle beschavingen. Dit is een ontwerpvoorstel. Een per-beschaving-beoordeling vóór de kandidaatordening verdient daarom gericht uitvoerbaarheidsonderzoek.

Bestaande FLI/AIP blijven bruikbaar voor packing, algemene prioriteiten, limieten, typebonussen en de invloed van kwaliteit tegenover andere doelen. De onderzochte set_settle_density.fli geeft voor settle_value_coef bijvoorbeeld voorkeuren rond 0.1, 6 en 10. Zij bevat geen afzonderlijke berekening voor drie bergen, toekomstig voedsel of gelijke goods. Gewichten aanpassen vult die ontbrekende beoordeling niet vanzelf in.

Volgende stap: bind de benodigde terrein-/improvementkenmerken en de eigen good-tellingen aan de bestaande interfaces. Maak daarna per ontwerpvereiste duidelijk wat via FLI/AIP kan, wat aanvullende logica vraagt en waar die vóór de kandidaatselectie kan werken. Centrumflag 0x40000000 en de volledige herberekeningscondities blijven open. Nog geen binarypatch, scriptoplossing of nieuwe spelproef kiezen voordat die route is onderbouwd.
