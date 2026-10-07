# Onderhoud, lonen en Deity-inkomsten

5 oktober2026, fase A. Vervolg op [RIJKSBUDGET-EN-WETENSCHAP.md](RIJKSBUDGET-EN-WETENSCHAP.md) en [DIRECTE-WETENSCHAP-EN-SCIENCEGEBOUWEN.md](DIRECTE-WETENSCHAP-EN-SCIENCEGEBOUWEN.md). Alleen-lezen onderzoek; geen spelstart, gameplaywijziging of binarypatch. B: oorspronkelijke machinecode met adressen; E: oorspronkelijke instructies uitgevoerd op synthetische objecten; T: configuratietekst. Enginehash `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, imagebase400000/timestamp37d6f702; afwijkende engine-map niet gebruikt.

## 1. Gebouwonderhoud gebruikt werkelijke records

**B:** token506 IMPROVEMENT_UPKEEP bereikt45e80b–45e81a en schrijft via522330 een integer naar BuildingRecord+3c. De voorafgaande productioncost gaat naar+38. Zie [token](BINAIR/economy-expense-parser-tokens.txt), [geldige recordparser45e7d0](BINAIR/economy-expense-upkeep-pop-and-setters.txt).

BuildingDB45cc70 loopt langs aanwezige gebouwbits en telt Record+3c alleen wanneer de upkeep **strikt groter** is dan een meegegeven vrijstellingsgrens. De volledige upkeep wordt geteld, niet alleen het verschil boven de grens. Stadsroute497810 haalt die grens uit wondercallback473450. De specifieke wonderflag van die callback is hier nog niet gebonden. Zie [gebouwsom](BINAIR/economy-expense-formula-candidates.txt), [stadsroute](BINAIR/economy-expense-building-removal.txt).

Bij meer onderhoud dan de beschikbare kas zoekt45cd00 het aanwezige betaalde gebouw met de laagste upkeep boven de vrijstellingsgrens. De stad roept49b9a0 aan, trekt de upkeep van dat record van de lokale som af en kan herhalen.49b9a0 heeft een echte gebouwbit-/cachemutatieroute; netwerk/eventgevolgen zijn niet volledig onderzocht. De uiteindelijke lokale som wordt via4a7200 als gebouwlast in ledger+1c geregistreerd;4a7070 haalt maximaal de beschikbare kas af. Zie [selectie/bitmutaties](BINAIR/economy-expense-building-removal.txt), [ledgerfuncties](BINAIR/economy-expense-city-upkeep-and-wages.txt).

Daarmee is een gebouwbonus zonder kasdekking geen gegarandeerde blijvende opbrengst. De gehele verwijderingslus is statisch gevolgd, maar niet offline uitgevoerd of in een gespeelde stad waargenomen.

## 2. Lonen worden per betreffende inwoner betaald

**B:** WGF-setter4cb920 berekent `BASE_WAGES + stand * UNIT_WAGES`, bewaart de double op+10 en de stand op+4c. Const-parser452a3d/452a5a bindt velden+140/+148 aan tokens523/526. [Setter](BINAIR/economy-expense-parser-and-getters.txt), [Const-parser](BINAIR/economy-city-const-ration-parser.txt), [tokens](BINAIR/economy-expense-parser-tokens.txt). **T:** [Const.txt](../CTP-og/ctp_data/default/gamedata/Const.txt) geeft1 en4; stand−2/0/+2 levert2/4/6 goud per betreffende inwoner, vóór latere integerverwerking.

De Player-update converteert de wage-double naar integer. City497a50 telt die integer per inwoner waarvoor Population4cc940 nul retourneert.4cc940 leest PopulationRecord+64 bit8; op6 oktober is die bit gebonden aan **IS_UNPAID**, token262→4622ac, afzonderlijk van IS_SLAVE/token267/bit20. Zie [geluk/WGF en flagbinding](GELUK-WGF-EN-STADSOMVANG.md). City+e8 kan één betaling vrijstellen, als het totaal daarvoor groot genoeg is; de precieze naam van die stadsflag blijft open. Zie [Player-volgorde](BINAIR/economy-science-player-turn.txt), [wagefunctie497a50](BINAIR/economy-expense-formula-candidates.txt), [popfilter](BINAIR/economy-expense-upkeep-pop-and-setters.txt).

De stad bewaart het totaal op+418. Bij voldoende kas verlaagt4a7070 de kas en registreert4a7220 het **positieve betaalde** totaal in ledger+18. Bij onvoldoende kas zet de stadsfunctie+9c op1 en retourneert0 zonder deze lokale betaling. De Player-route kan dan de wagesstand verlagen en het opnieuw proberen. De volledige herhaalde stadsbetaling en gelukreactie zijn niet offline uitgevoerd.

Voor vier betreffende inwoners en wage4 is dit16 goud; met twee uitgesloten inwoners8, met de eenmalige stadsflagvrijstelling12. Deze fixtures stellen geen algemene regeringseis of volledige kosten van een vier-inwonersproductiestad vast.

## 3. Deity heeft al een rijksinkomstencorrectie

**B:** na de normale stadsupdate-/inkomstenlus herberekent4a71e0 ledger+8 uit+10,+c,+4. Bij Player-type1 in de gewone singleplayercontext volgt4b7a2d–4b7ac4. Die vergelijkt het bestaande bedrag met `trunc(bedrag * DiffRecord[era].AI_GOLD_ADJUSTMENT)` en voegt het verschil toe of trekt het af; daarna herberekent hij+8. De multiplayerpredicate kan deze tak overslaan. Zie [volledige Player-update](BINAIR/economy-science-player-turn.txt).

AI_GOLD_ADJUSTMENT is token312. Diff-parser45851a controleert312 en vult vanafRecord+1a0 vijf doublewaarden. De bestaande difficultyrecord-loadingbinding wordt hergebruikt. Zie [exact token](BINAIR/economy-expense-ai-adjust-token.txt), [parser458541](BINAIR/economy-expense-parsers-full.txt), [databaseopbouw](BINAIR/economy-growth-difficulty-record-loading.txt).

**T:** de Deity-definitie in [DiffDB.txt](../CTP-og/ctp_data/default/gamedata/DiffDB.txt) geeft `1.0 1.0 1.1 1.2 1.2`. De selector leest een globale era-index; de volledige technologie→era-overgang is hier nog open. Dit zijn bestaande enginebonussen, geen projectwijzigingen. Deze correctie wordt niet rechtstreeks op de eerder berekende directe scientistwetenschap toegepast.

**Afrondingsgrens:** binary64-waarde1.2 ligt net onder exact6/5. Met een x87-significand van64 bits blijft100*1.2 vóór truncatie onder120 en geeft deze fixture119; met53 bits wordt het product120. Beide modes zijn gecontroleerd. De werkelijk ingestelde controlword tijdens een gespeelde game is niet vastgelegd; rapporteer119/120 daarom niet als gegarandeerd runtimeverschil. Factor1 en0.5 hebben dit grensprobleem niet.

## 4. Verificatie en gevolgen voor vervolg

[Controleer-Onderhoud-En-Lonen.py](../PROEVEN/Controleer-Onderhoud-En-Lonen.py) controleert de originele hash en levert [19/19 geslaagde controles](BINAIR/economy-expense-upkeep-wages-checks.json): vijf gebouwsommen inclusief bit33/vrijstellingsgrens, zes stadsbetalingen inclusief kasgrens/uitzonderingsflag, drie wagesettergevallen en vijf income-adjustment/context/precisiegevallen. Gebouwsom en wagesetter lopen zonder callbacks; betalingscases mocken popfilter/kasgetter, income-adjustment mockt difficulty-index met synthetische era/networkglobals. De geïmporteerde ftol-stub behoudt de caller-mode.

De eerste kostentest had verkeerd ledger+1c met negatieve wages verwacht. Inspectie van4a7220 toont werkelijk positieve registratie op+18; de fixture is daarop gecorrigeerd. Dit is een correctie van de testverwachting, geen wijziging van de engine.

Gebouwonderhoud, loonbetalingen en de rijksinkomstencorrectie mogen nu afzonderlijk in het economisch model worden opgenomen. De militaire productieondersteuning, PW, gelukcomponenten, individuele research-/productiekostcorrecties, het volledige scheduler-/beurtverloop en de twee uitzonderingsflags blijven open. Volgende rootstap is deze context; de analist onderzoekt improvementconstructie/stadsgebied. Brede fase A blijft open.
