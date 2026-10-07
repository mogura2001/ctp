# Pollution en latere stadstaken — fase A

**Aanvulling coördinator7 oktober19:29:** de ontbrekende normale constructorbinding is nu statisch gevolgd. Wrapper526bc0 geeft voor type10 de aangeleverde parameter ongewijzigd door aan Player4c0ae0 (526be9–526bfc). De geslaagde route4c0d43–4c0d61 geeft diezelfde parameter via projectpool4d3d10 door;4d3e29–4d3e44 draagt haar over als constructorargument+20. Constructor4d3450 kiest bij type10 branch4d34cb en schrijft dit argument op project+28 bij4d34d5. De eerder aangetoonde type10commit4d3689 geeft dat veld aan cellterrainwriter500d00. [Volledige gerichte binding](BINAIR/pollution-cleanup-project-terrain-binding.txt).

Dit sluit de onzekerheid over de herkomst van project+28: de normale aanvraag met parameter4/9 bereidt terrein Grassland/Hill voor. Er is in deze constructorroute geen omzetting naar het oorspronkelijke bergtype. **Als deze cleanup-aanvraag op een berg wordt toegelaten en het project via de onderzochte commit voltooit, wordt de berg dus naar het aangevraagde terrein omgezet.** Dat is B-bewijs voor de keten, geen gespeelde bergwaarneming of garantie dat iedere vervuilde berg zo wordt behandeld. Eligibility, eventselectie, timing en latere externe terreinveranderingen kunnen het voorkomen beïnvloeden. Het eerdere open punt over volledige projectinitialisatie geldt nu alleen nog voor overige velden/branches/lifecycle, niet voor deze normale type10-terreinkeuze. Bij ontwerpen voor blijvende bergproductie moet deze afhankelijkheid worden meegenomen. Geen nieuw emulatieresultaat; de oorspronkelijke16 controles blijven dezelfde.

6 oktober 2026. Afgebakende analyse van bestaande regels en AI-opruimverzoeken; geen ontwerp, spelstart of gameplay-/binarywijziging. Hergebruik van [terrein/upgrades](TERREIN-EN-IMPROVEMENTS.md), [constructie](IMPROVEMENTCONSTRUCTIE-EN-STADSGEBIED.md), [directe science](DIRECTE-WETENSCHAP-EN-SCIENCEGEBOUWEN.md), [groei](VOEDSEL-GROEI-EN-KOLONISTEN.md), [stadsopbrengsten](RANTSOENEN-EN-STADSOPBRENGSTEN.md) en [Deitykosten](DEITY-KOSTEN-EN-TECHNOLOGIEFASEN.md).

## 1. Waarom de vroege taak later opnieuw beoordeeld moet worden

De originele lokale vervuilingsfunctie gebruikt twee afzonderlijke bronnen: bevolking boven8 en productie boven300. Size4 voorkomt de eerste, maar voorkomt geen industriële vervuiling zodra voldoende productie beschikbaar is. Een groeiende sciencestad kan de bevolkingsbron bereiken, ook als veel inwoners scientists zijn. De populatieterm vraagt het totale aantal inwoners; hij telt geen afzonderlijke voedselwerkers/scientists.

Productieboostgebouwen verhogen bovendien de vermenigvuldigingsfactor voor vervuiling; hun percentageproductie is een andere regel. Recycling en latere technologie kunnen die factor of bron verkleinen. Dit beschrijft concrete afhankelijkheden, geen definitieve nieuwe bouwlijsten.

## 2. Records en AAIP

[Recordextract OG/AAIP](BINAIR/pollution-late-records.json) bevat alle actieve pollutionvelden van Advance/improve/govern/Terrain. Deze geselecteerde gameplayvelden zijn in beide versies gelijk. Het extract sluit commentaarregels uit: `#IMPROVEMENT_FLAG_POLLUTION_CLEANER −10` bij Recycling Plant is geen actieve flat-cleanerregel.

| Gebouw | Enabling advance | Pollution bonus | Upkeep |
|---|---|---:|---:|
| Factory | Industrial Revolution | +1 | 20 |
| Oil Refinery | Oil Refining | +2 | 20 |
| Airport | Aerodynamics | +1 | 20 |
| Nuclear Plant | Quantum Mechanics | −0.5 | 45 |
| Recycling Plant | Environmentalism | −2 | 5 |
| Robotic Plant | Robotics | +1 | 45 |
| Population Monitor | AI Surveillance | −1 | 10 |
| Zero Emission Vehicles | Fuel Cells | −2 | 15 |
| Fusion Plant | Fusion | −1 | 30 |

Voorbeelden van originele advancevelden: Oil Refining en Intelligent Materials geven size-/productionmodifier+1; Environmentalism en Nanoassembly−1. Mass Production bevat tekstwaarde0.5. De betreffende runtimegetters sommeren **integerrecordvelden**: de exacte parserbehandeling van deze fractionele advancewaarde is nog open. Behandel0.5 daarom niet als bewezen werkende halve modifier.

Theocracy heeft pollutioncoef1 en pollution-unhappycoef0. Communism heeft3/0.02, Ecotopia0.25/0.08. De eerste coefficient is hier aan de vervuilingsformule gebonden; de tweede en de volledige geluksketen vallen buiten dit pakket. Sciencegebouwpercentages en SCIENCE_PER_POP zijn reeds afzonderlijk geanalyseerd; uit het ontbreken van pollutionflags in die records volgt geen vrijstelling van hun bevolkingsbron.

De enabling advance blijft de gewone gebouwtoelatingsvoorwaarde uit het bouwrapport. Kosten en upkeep van later gespecialiseerde steden moeten de echte Deityqueuekosten en rijkslasten gebruiken, geen alleenstaande tekstbasis.

## 3. Normale engineberekening

De echte normale CityUpdate497f10 bereikt4939e0 bij4981d9, vóór de daaropvolgende opbrengstfuncties4940c0/494970 en groei494cf0. Vervuiling gebruikt dus de **op dat moment opgeslagen** City+3c-productiewaarde, niet een opnieuw in4939e0 berekende bergopbrengst. De precieze volledige cachegeschiedenis/ronde is niet geëmuleerd. [Aanroepvolgorde](BINAIR/pollution-late-city-update.txt), [volledige lokale functie](BINAIR/pollution-late-city-pollution.txt).

De gesloten gewone rekenbranch tot de eerste write493c3d geeft:

```text
sizeBron = max(0, bevolking−8) * 0.5 * (1 + sizeAdvanceSom)
prodBron = max(0, City+3c−300) * 0.01 * (1 + productionAdvanceSom)
gebouwFactor = max(0, 1 + gebouwBonusSom + stadsWonderBonus)
basis = max(0, (sizeBron + prodBron + City+8c) * gebouwFactor * regeringCoef)
City+80 = trunc(basis + gebouwCleanerSom + stadsWonderCleaner
                + contextConstTerm + eigenaarHistoryTerm)
```

De laatste hulpparameters zijn daadwerkelijk gelezen, maar hun volledige naam/levenscyclus is hier niet vastgesteld. ConstRecord+480 komt alleen bij City+a0≠0 erbij. De eindoptelling na de eerste clamp kan door negatieve cleanerinputs lager worden; dit rapport claimt geen algemene eindclamp die niet in die instructies staat.

Token514/515 binden Const+110/+118 aan0.5/0.01; tokens528/529 binden+3a8/+3ac aan8/300 via de eerder gevonden echte constparser451d40. Governmenttoken466 wordt door45a8e5 op Record+68 geschreven, dezelfde double die Player4c2970 ophaalt. [Canonieke tokens](BINAIR/pollution-late-tokens.txt), [constparser](BINAIR/economy-city-const-ration-parser.txt), [governmentparser](BINAIR/economy-budget-government-parser.txt), [exacte getters](BINAIR/pollution-late-getters-and-clean-request.txt).

Buildingflag470 komt via jumptable45f69c op45f430 en leest een real naar Record+a0. De echte som45d830 telt die doubles van aanwezige gebouwen op. De cleaner is de andere getter45d7b0/Record+a8. Advancegetters475900/475940 sommeren bekende records met stride8c, respectievelijk integer+5c/+60; Player4c2160/4c2170 leveren ze aan de formule. [Gebouwdispatch](BINAIR/pollution-late-building-dispatch.json), [parser/inputs](BINAIR/pollution-late-formula-inputs.txt), [techsommen](BINAIR/pollution-late-tech-modifiers.txt), [gebouwen/getters](BINAIR/pollution-late-getters-and-clean-request.txt).

Aan het begin kan de pollutionregelswitch of een afzonderlijke wonderpredicate voor enige speler City+80 direct op0 zetten. De wonderflag daarvan is hier niet semantisch gebonden. Na de eerste write volgt een afzonderlijke type1/netwerk-/pactbranch, daarna eigenaarbijschrijving4bfca0 en reset van City+84/+88. De controles stoppen vóór die pactbranch; de bovenstaande formule is daarom **niet** geclaimd als volledige finale Deityvervuiling inclusief verdragen.

## 4. AI-opruimketen en daadwerkelijke interfaceaanvraag

IC3RobotCom::RegisterPollution200102f0→AiMain20005a50→Opportunity_Action_Repair_Installation20057e90 voegt een node toe. Die bewaart de positie, huidige integerturn, type10 en nul in de aanvullende velden. Het object telt dirty tiles op+4 en queue-items op+8. De enginebron die het event uitstuurt en de volledige save-herbouw zijn niet opnieuw gevolgd. [Volledige AI-keten](BINAIR/pollution-late-ai-repair.txt).

Execute20057ae0 haalt eerst werkelijk beschikbare PW via Player+94 op. Een type10-node komt pas in aanmerking als de eventturn niet in de toekomst ligt en `dirtycount > fz_min_num_dirty_tiles`. Een gelijkstand stopt deze aanvraag. Daarna kiest de functie een extra parameter4 of9 via RNG0–99 en een World+34-predicate: bij true drempel70, anders30. De exacte semantiek van die predicate is nog open; deze parameters zijn geen bewezen improvementniveau of aantal schoonmaakbeurten.

Via Improvement+1c haalt hij de kosten op. Het verzoek vereist `PW≥kosten+2000`: ook een betaalbaar project kan dus op de vaste reserve stranden. World+64 moet als owner de AI of−1 teruggeven. Improvement+20 vult een state; alleen0/2 gaan door naar Improvement+18 met type10, parameter en positie. Bij succes vermindert dirtycount en het lokale budget; bij falen of uitstel kan de node worden teruggezet. De gevonden veldtest `<4` wordt niet als vier gegarandeerde retries uitgelegd: de volledige tellerlevenscyclus is niet gebonden.

De Improvement-interface is de bestaande echte vtable7445b8: +1c526c20, +20526ad0, +18526bc0. Kosten lopen naar4681f0; type10 kiest4682d1 en combineert terrainkostenvelden. Eligibility roept Player4bfd70 aan en de bestaande aanvraagcontrole; constructie526bc0 vraagt Player4c0ae0 om een echte PW-projecthandle. Dat is dezelfde engineprojectketen als eerder geanalyseerd. [Kosten/wrapper](BINAIR/pollution-late-city-calc-and-installation.txt), [kostenbranch](BINAIR/pollution-late-cleanup-project-branch.txt), [eligibility](BINAIR/pollution-late-clean-eligibility.txt), [echte actie](BINAIR/pollution-late-getters-and-clean-request.txt), [bestaande PW/projectvoorwaarden](IMPROVEMENTCONSTRUCTIE-EN-STADSGEBIED.md).

Bij projectcommit4d3580 kiest jumptable4d3920 voor type10 **4d3689**. Deze schrijft projectveld+28 naar cellterrain via500d00 en verwerkt terrein-/environmentbits. De echte writer500d00 schrijft cell+d. Parameters4/9 vallen samen met de eerder gebonden terrainindices Grassland/Hill. Volledige projectinitialisatie, timing en alle refreshgevolgen zijn hier niet gevolgd; dit is geen bewijs dat een vervuilde berg altijd als dezelfde berg terugkomt. [Dispatch](BINAIR/pollution-late-commit-dispatch.json), [commitbranch](BINAIR/pollution-late-clean-eligibility.txt), [terrainwriter](BINAIR/pollution-late-terrain-write.txt), [bestaande volledige commit](BINAIR/improvement-construction-project-actions.txt), [indexbinding](TERREIN-EN-IMPROVEMENTS.md).

## 5. FLI/AIP en AAIP-les

De gewone loader zet `green_me_test` bij een pollutionpact en geladen primaryprofiel, maar bevat hiervoor geen loadactie. Een aanwezige green_me.aip betekent dus geen effectief milieuprofiel. Dit was al aangestipt in [ARCHITECTUUR](ARCHITECTUUR.md). Zijn AIP bevat ook vervuilende productiegebouwen. AAIP verhoogt Recycling Plant9000→9900 en verlaagt onder meer Factory7990→3990 en Robotic Plant7990→2990; Fusion gaat10000→6000. De lijstvolgorde blijft dezelfde. [AAIP-diff](INVENTARIS/aaip-ai-diff.md), [OG loader](../CTP-og/ctp_data/default/aidata/aiploader.fli), [OG lijst](../CTP-og/ctp_data/default/aidata/AIPs/green_me.aip).

De al bewezen lijstselectie kiest eerst een geschikt item in volgorde; gewichten veranderen de concurrentie en sorteren die lijst niet automatisch opnieuw. Zonder effectieve loadbinding is dit geen aangetoond AAIP-effect op normale AI-pollutionbouw. Fuzzy oorsprong/default van min_num_dirty_tiles, pollutiongerelateerde diplomatietests en algemene gebouwutility blijven hier open.

## 6. Controles, gevolgen en grenzen

[Controleer-Pollution.py](../PROEVEN/Controleer-Pollution.py) controleert beide oorspronkelijke binaryhashes en voert **16/16** gerichte controles uit. Tien citygevallen tonen thresholds8/300, beide bronnen, gebouwfactor/clamp, bekende techsommen en governmentfactor. Zes echte AI-Executefuncties tonen reservegrens, dirtythreshold, legalstate, falen/queuebehoud en parameter4/9. [Uitkomsten en mocks](BINAIR/pollution-late-controls.json).

Citytests gebruiken echte gebouwbonus-, techsom-, government- en rekeninstructies, met expliciete zero-inputmocks voor wonders, history en cleaner. AItests vervangen World/random/kosten/eligibility/actie door callbacks. Ze bewijzen de requestvoorwaarden, geen voltooide schoonmaak of wereldcatastrofe. x87 gebruikt PC64/nearest en FTOL met bewaarde controlword. De synthetische bonus/techwaarden zijn geen claim over automatische parseruitkomsten van ieder tekstrecord.

Voor size4-bergensteden is industriële productie de relevante pollutionbron; later productiegebouwen en mijnupgrades kunnen de drempel bereiken. Voor sciencesteden telt verdere bevolkingsgroei mee, terwijl scientists geen afzonderlijke uitzondering krijgen. De terraingevonden commit maakt behoud van het bergplan bij pollutionherstel een concrete vervolgvraag. De normale groei blijft bij positief surplus actief; size4 is geen automatische engine-stop.

Open technische grenzen: fractionele advanceparser, volledige type1/pactcorrectie en finale Deitybijschrijving; engine-eventbron en dirtythresholdinitialisatie; volledige cleanup-projectinitialisatie/refresh en terreinkeuze; geluk door pollution en globale rampsomslag. De doelrelevante lokale bron-/requestketen is afgebakend geleverd; brede fase A blijft open.
