# Terrein, opbrengsten en verbeteringen — eerste interfaceketen

5 oktober 2026. Fase A, P0.2. Afgebakende analyse van de aanwezige CTP I-binaries en regels; geen wijzigingsvoorstel of spelproef. Dit pakket bindt terreinindices, opbrengstgetters, verbeteringfamilies, technologiecontrole en de bestaande AI-invoer voor stadsvakjes. De volledige werkerverdeling en netto stadseconomie blijven open.

## 1. Uitkomst en bewijsgrenzen

De AI kan het echte terreintype, huidige vakjesopbrengsten en het effect van een hogere verbetering opvragen. Dezelfde engine bevat controles op vereiste technologie en plaatsingsgeschiktheid. Daarvoor is dus niet uitsluitend tekstinterpretatie nodig. Het bestaan van die interfaces bewijst nog geen geschikte strategie, correcte bevolkingstoewijzing of goede vestigingsscore.

Belangrijk voor vervolganalyse: de volgorde van records in terrain.txt is **niet** de World-terreinindex. Bergen zijn 8, 20 en 22; heuvels 9, 19 en 21. Verder zijn Improvement-slots +38/+40 absolute food/productie op een positie, terwijl +48/+44 de verschillen met de bestaande verbetering opvragen. Deze functies mogen niet verwisseld worden.

Bewijslabels in dit rapport: **T** = aanwezige tekstregels, **B** = echte machinecode/interfacebinding, **E** = uitvoering van oorspronkelijke instructies met synthetische gegevens. Er is geen nieuwe **R**untimewaarneming in een gestart spel. De 43 offline controles voeren getters en hun interne callees uit, maar geen volledige parser, stadseconomie, plaatsingsactie of AI-beurt.

De robotcom.dll/map-binding wordt hergebruikt: timestamp 37b894e7, imagebase 20000000, SHA256 3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44. Engine-adressen komen rechtstreeks uit civctp.exe: timestamp 37d6f702, imagebase 00400000, SHA256 b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79. civctp.map past niet en wordt niet gebruikt. Zie de bestaande [interface-identificatie](BINAIR/terrain-food-engine-interface-binding.txt) en de headers van de nieuwe bewijsstukken.

## 2. Echte terreinindex en database

**B:** World-slot +a8, engine 5342e0, normaliseert de positie via 503f00 en vraagt 514b70 aan. Deze laatste functie leest de gesigneerde byte cell+d uit de echte World-cel. De databasegetter 455b10 controleert de index en gebruikt records met stride c0. Bewijs: [index/getter](BINAIR/terrain-food-v2-engine-getters.txt), [positieconversie](BINAIR/terrain-food-v2-position-worker-tech.txt) en [indexwrapper](BINAIR/terrain-food-v2-current-tile-and-level.txt).

De parser 467bf0 schrijft het vaste type in TerrainRecord+b0. Na alle records roept 4681ba de herschikking 469c20 aan: vergelijking met de gewenste index, zoeken naar het passende +b0-type, verwisselen van recordinhoud en bijwerken van lookupgegevens. De type-tokenbindingen en adressen staan in [24 parserbindings](BINAIR/terrain-food-v2-terrain-type-binding.json); de werkelijke herschikking in [sortering](BINAIR/terrain-food-v2-canonical-sort-and-legality.txt) en [staart/lookup](BINAIR/terrain-food-v2-worker-final-and-sort.txt). Dit is een machinecodebinding; de volledige parser/sortering is niet geëmuleerd.

| World-index | Terrein | World-index | Terrein |
|---:|---|---:|---|
| 0 | FOREST | 12 | WATER_VOLCANO |
| 1 | PLAINS | 13 | SPACE |
| 2 | TUNDRA | 14 | WATER_BEACH |
| 3 | GLACIER | 15 | WATER_SHELF |
| 4 | GRASSLAND | 16 | WATER_TRENCH |
| 5 | DESERT | 17 | WATER_RIFT |
| 6 | SWAMP | 18 | DEAD |
| 7 | JUNGLE | 19 | BROWN_HILL |
| 8 | MOUNTAIN | 20 | BROWN_MOUNTAIN |
| 9 | HILL | 21 | WHITE_HILL |
| 10 | WATER_SHALLOW | 22 | WHITE_MOUNTAIN |
| 11 | WATER_DEEP | 23 | DEAD_HILL |

**E:** World-wrapper 5342e0 schrijft bij een synthetische cel met type 20 daadwerkelijk 20 naar de output. **Let op:** het veld `index` in het eerder gemaakte [tekstextract](BINAIR/terrain-food-text-regels.json) beschrijft tekstrecordvolgorde; gebruik voor echte World-index de bovenstaande parserbinding. Het oude extract is behouden als bronmateriaal.

## 3. Improvement-interface: absolute opbrengst en verschil

**B:** AiMain::Init haalt via GameState-slot +38 de Improvement-interface op en bewaart deze op AiMain+50 (20001b83). De echte GameState-vtable 744420 wijst +38 naar 526000; objectconstructie koppelt Improvement-vtable 7445b8. Hergebruik: [DLL-init](BINAIR/terrain-food-ai-interface-init.txt), [engine-interface](BINAIR/terrain-food-engine-interface-binding.txt), [slotmetadata](BINAIR/terrain-food-interface-metadata.json).

| Slot | Engine | Aangetoonde betekenis |
|---|---|---|
| +0c | 526a20 | Aantal speciale installations plus elf normale selectors |
| +10 | 526a40 | Globale beschikbaarheid van type, inclusief enabling/obsolete advance |
| +1c | 526c20 | Materials-opvraag voor verbetering op positie |
| +20 | 526ad0 | Plaatsingscontrole met Player-route, bestaande aanvraag en World-check |
| +28 | 526c90 | Controle op bestaande/pending aanvraag voor die plaatsing |
| +34 | 526e20 → 468aa0 | Absolute food-component van gekozen environment, gegeven terrainindex |
| +38 | 526da0 → +34 | Dezelfde absolute food-component, gegeven positie |
| +3c | 526e60 → 468a00 | Absolute productiecomponent, gegeven terrainindex |
| +40 | 526de0 → +3c | Dezelfde absolute productiecomponent, gegeven positie |
| +44 | 526d00 → 468840 | Productieverschil met bestaande verbetering uit dezelfde familie |
| +48 | 526d50 → 468b40 | Foodverschil met bestaande verbetering uit dezelfde familie |

De positievarianten +38/+40 lezen eerst het terrein en roepen de absolute variant aan. De delta-varianten gebruiken de echte celtoestand en kunnen daarbij een good-specifiek record selecteren. Zij zijn dus niet zonder meer uitwisselbaar. Bewijs: [wrappers](BINAIR/terrain-food-engine-improvement.txt), [absolute selectors](BINAIR/terrain-food-v2-engine-getters.txt), [volledige fooddelta](BINAIR/terrain-food-v2-delta-final-tech.txt).

Een absolute component betekent hier de bijdrage van het gevraagde environment, **niet** de volledige toekomstige opbrengst van het vakje inclusief basis, rivier, centrum en stadsmodifiers. De onderzochte normale food/productie-getters geven bij ontbrekend environment nul. Voor speciale installationselectors vanaf 11 leveren de absolute wrappers geen normale terreinverbeteringsopbrengst op. Er is in deze slotreeks geen afzonderlijke toekomstige-goldgetter gebonden; actuele gold bereikt de AI wel via de stadsvakjesinterface (§6).

## 4. Families, niveau en bestaande celtoestand

De namen zijn rechtstreeks aan parsercases gekoppeld. **B:** tokeninteger → compressed switch → recordveld. Zie [tokenmetadata](BINAIR/terrain-food-v2-environment-tokens.txt), [roadtokens](BINAIR/terrain-food-v2-road-river-tokens.txt) en de volledige [naam/veld-binding](BINAIR/terrain-food-v2-environment-field-binding.txt).

| Normale selector | Environment | TerrainRecord-pointer | Bestaand niveau in cellflags |
|---|---|---|---|
| 0, 1, 2 | ENV_IRR1, 2, 3 | +68, +6c, +70 | `(flags >> 2 & 3) - 1` |
| 3, 4, 5 | ENV_ROAD1, 2, 3 | +5c, +60, +64 | `(flags & 3) - 1` |
| 6, 7, 8 | ENV_MINE1, 2, 3 | +74, +78, +7c | `(flags >> 4 & 3) - 1` |
| 9 | ENV_CANAL_TUNNEL | +54 | bit 200 |
| 10 | ENV_BASE | inline +8 | Geen verbeteringniveau |

ENV_RIV_CUR is een afzonderlijke pointer +58, toegevoegd bij cellflag 800. ENV_CITY_BONUS staat op +50 en wordt toegevoegd wanneer cell+14 niet nul is. De laagste twee bits zijn dus wegen, niet mijnen. Voor de namen is de echte parser doorslaggevend; een eigennaam van een helper of synthetische testgegevens mag die binding niet vervangen.

Binnen een familie telt de raw getter alleen het geselecteerde niveau. Een farm2 bevat in de gewone landregels +15 food; hij stapelt niet farm1 +5 en farm2 +15. De delta-getter trekt farm1 af: 15 − 5 = 10 extra food. Hetzelfde principe geldt voor mijnniveaus en hun productiecomponent. Bewijs: [niveauhelpers en delta](BINAIR/terrain-food-v2-level-and-legal-start.txt), [raw celgetters](BINAIR/engine-locatiewaarde-tilehelpers.txt), [delta-staart](BINAIR/terrain-food-v2-delta-final-tech.txt).

**E/B-beperking:** de deltafuncties trekken bij een gevraagde mijn niet de food van een bestaande farm af, en bij een farm niet de productie van een bestaande mijn. Ze vergelijken binnen de gekozen familie. Daarmee is niet bewezen dat plaatsing in een echte game beide families behoudt of juist één verwijdert: de finale constructie/bitwijziging is nog niet gevolgd. Ook is cell+14/ENV_CITY_BONUS niet gelijkgesteld aan de nog ongebonden scoreflag 40000000.

## 5. Regels, vereiste technologie en plaatsing

**T:** terrain.txt is bytegelijk in OG, AAIP en proef; SHA256 d1b8c038876d2a3a7abc963cc5e29c70ba29e449dfa6594709c452c0aa53b28f. De gelijkheid is vastgelegd in [veld/hashbewijs](BINAIR/terrain-food-v2-environment-field-binding.txt). Dit bewijst gelijke terreinregels, geen gelijke AI-aansturing. Bron: [originele terrain.txt](../CTP-og/ctp_data/default/gamedata/terrain.txt) en [tekstextract](BINAIR/terrain-food-text-regels.json).

| Vakje/verbetering | Niveau 1 | Niveau 2 | Niveau 3 |
|---|---|---|---|
| Plains/grassland/desert food | +5 / Agriculture / 200 materials | +15 / Agricultural Revolution / 500 | +25 / Intelligent Materials / 1400 |
| Shallow water food | +5 / Ship Building / 200 | +15 / Ocean Faring / 500 | +25 / Robotics / 1400 |
| Deep water food | +10 / Ship Building / 300 | +30 / Ocean Faring / 700 | +50 / Robotics / 1800 |
| Bergen productie | +15 / Mining / 400 | +30 / Electricity / 1000 | +45 / Robotics / 2200 |

De genoemde environments hebben ENV_TIME 2. Bergen hebben basisproductie 20 en basisgold 5; hun mijnen voegen respectievelijk gold 5, 10 en 15 toe. Shallow water heeft basisfood 10, deep water 5; die basis hoort niet nogmaals in de bovenstaande environmentbijdrage. Andere watertypes en good-specifieke subrecords kunnen andere cijfers hebben; deze tabel is geen universele waterformule. Op de gewone forest/jungle/mountain-records staan geen drie gewone IRR-niveaus zoals op plains; toekomstige transformatie of een good-subrecord vereist afzonderlijke inspectie.

**B:** ENV_ADVANCE, token 1014, parsercase 46707d, schrijft via naamresolver 466c10 naar Environment+44. De positiegettter 4685e0 selecteert het relevante environment en leest dat veld. Player-plaatsingsroute 4bfd70 vraagt de vereiste advance op bij 4bfeef; 4bff51–4bff64 controleert deze via de echte known-advancefunctie 474b60. Daarna volgt ook een obsolete-filter. Dit koppelt de tekstvoorwaarde aan echte engine-toelating; een aanwezige technologystring is niet het enige bewijs. Zie [parser](BINAIR/terrain-food-parser-fields.txt), [advance-resolver](BINAIR/terrain-food-v2-ai-city-yields-engine.txt), [techgetter](BINAIR/terrain-food-v2-delta-final-tech.txt) en [plaatsingsfilter](BINAIR/terrain-food-v2-canonical-sort-and-legality.txt).

Daarnaast voert +20 → 526ad0 → 4bfd70 verdere plaatsingschecks uit en vraagt de wrapper via +28 en 4d43e0 nog bestaande/pending toestand en World-geschiktheid op. De hele lijst met blokkaderedenen is niet semantisch ontleed. Globale typebeschikbaarheid (+10) is daarom niet voldoende om een vakje als bouwbaar te tellen. Bewijs: [plaatsingswrapper](BINAIR/terrain-food-engine-improvement-details.txt), [toelating begin](BINAIR/terrain-food-v2-level-and-legal-start.txt), [toelating einde](BINAIR/terrain-food-v2-parser-completion-and-eligibility.txt).

Materials-getter 4681f0 leest de waarde +20 van het doel-environment; tijdgetter 468470 leest +24. Deze opvraag bevat geen aangetoonde aftrek van het betaalde lagere niveau. Of de finale buildactie dezelfde volledige waarde als PW afboekt, en hoe duur/afronding verwerkt worden, blijft open. Bewijs: [kosten/tijd](BINAIR/terrain-food-v2-cost-build-readers.txt).

## 6. Huidige vakjesopbrengsten en werkers behoren tot bestaande AI

**B:** engine 500110/500290/5003a0 lezen actuele food/productie/gold. Zij selecteren basisrecord, bestaande niveaus, rivier en eventuele citybonus. Bij een geldige good-selectie wordt een genest good-record gekozen in plaats van het gewone basisrecord; dit kan de raw opbrengst wijzigen. Goods zijn dus niet uitsluitend een aparte handelsbonus. Speciale DEAD-terreinpaden en verdere celcontext staan in dezelfde helpers; deze analyse maakt geen universele somformule voor alle situaties. Bewijs: [raw getters](BINAIR/engine-locatiewaarde-tilehelpers.txt).

CityAgent::FindOpenTiles (20020e00) vraagt World+ac (534510) om kandidaatposities en gebruikt een lijst met twintig TileUtility-slots. De engine loopt via 502da0 en controleert via 511030; de volledige geometrie, overlap- en uitsluitingsregels hiervan zijn nog niet gebonden. Dit is een echte kandidaatinterface, maar niet automatisch dezelfde footprint als de eerder onderzochte vestigingsscore. Bewijs: [DLL-kandidaten](BINAIR/terrain-food-v2-ai-tile-input.txt), [engine-enumeratie](BINAIR/terrain-food-v2-terrain-index-context.txt) en [enumeratievervolg](BINAIR/terrain-food-v2-canonical-terrain-and-yield.txt).

Daarna vraagt FindOpenTiles via AiMain+2c (20020e96) de Player-interface om waarden: slot +120 (528760 → 4c9e90). In TileUtility staan food op +8, productie op +10 en gold op +18. Food/productie gaan via CityData 495250/495330; gold komt via 5003a0 of de contextvariant 495460. **Deze CityData-modifiers zijn nog niet ontleed**: de AI-invoer is daarom niet simpelweg gelijkgesteld aan raw terrain.txt. AiMain+40 is een andere interface, Population, en wordt niet voor dit Player-slot gebruikt. Bewijs: [DLL-caller](BINAIR/terrain-food-v2-ai-tile-input.txt), [Player-wrapper](BINAIR/terrain-food-v2-city-tile-values-and-advance-name.txt), [echte engine-vulling](BINAIR/terrain-food-v2-ai-city-yields-engine.txt).

AiMap::HasPopFromThisCity (200797a0) gebruikt World+a4 (5343f0). Dat controleert de eigenaar via 516c10/cell byte+e, leest een geplaatste populatiehandle uit cell+18, resolveert die via 4ccd10 en haalt de stadshandle op via 4cb100. De DLL vergelijkt die handle met de bedoelde cityID. De farmwaardering roept dit werkelijk aan: geen passende huidige werker → geen normale farmutility. Het is geen generieke test of het vakje ergens binnen eigen land ligt. Bewijs: [DLL-popcheck/utility](BINAIR/terrain-food-v2-work-area.txt), [engine-popcheck](BINAIR/terrain-food-v2-worker-final-and-sort.txt), [owner/city-handle](BINAIR/terrain-food-v2-ai-city-yields-engine.txt) en [farm/quarrywaardering](BINAIR/terrain-food-ai-improvement.txt).

Dit sluit aan op de afzonderlijk bewezen handelsketen: lokale goods worden uit centrum en daadwerkelijk geplaatste gewone werkers verzameld. Die afleiding wordt beheerd in [GOODS-EN-HANDELSROUTES.md](GOODS-EN-HANDELSROUTES.md); dit rapport herhaalt of wijzigt dat onderzoek niet. Exacte werkerplaatsing, scientist-keuze en de prioriteit tussen steden zijn nog een eigen beslisketen.

## 7. Offline controles en betekenis voor projectdoelen

[Controleer-Terrein-Opbrengsten.py](../PROEVEN/Controleer-Terrein-Opbrengsten.py) controleert de enginehash en voert de oorspronkelijke instructies uit met een synthetische World, cel en database. Er zijn geen externe callbacks gemockt in de geteste getter/delta-routes. [Resultaat](BINAIR/terrain-food-v2-yield-checks.json): **43/43** geslaagd. Controles omvatten alle elf absolute selectors voor food/productie, ontbrekende levels, farm-/mine-upgrades, verschil binnen een familie, het niet aftrekken van een andere familie, actuele farm/road/mine/canal/river/citybijdragen, good-recordselectie en World-typeoutput 20. Fixturewaarden dienen branchcontrole; ze bewijzen geen werkelijk stadsresultaat of universele spelwaarde.

De afsluitende parsercontrole heeft bovendien voorkomen dat de synthetische labels voor mijnen en wegen als bewijs gebruikt werden: +5c/+60/+64 zijn wegen; mijnen staan op +74/+78/+7c. Alle labels, fixturevelden en mineflags in de definitieve controle zijn daarop gecorrigeerd. De resultaten gelden voor de definitieve 43 controles.

Voor de projectdoelen is nu onderbouwd welke terrainindices als bergen tellen, waar de afzonderlijke food-/productieniveaus en enabling-tech te vinden zijn, hoe de AI bestaande werkers herkent en waar actuele food/productie/gold binnenkomen. De gebruikersvoorkeur voor advanced farms/fisheries is te relateren aan IRR2 en de genoemde advances. Er is geen nieuw beleid ingesteld.

De stelling dat drie gemijnde bergen en één voedselvakje een productiestad van vier inwoners onderhouden, vereist daarnaast werkelijke centrum-/populatieregels, rations, regering-/Deity-modifiers en consumptie. Raw basisproductie 20 plus mijn1 15 bewijst op zichzelf geen netto stadsproductie of voedselbalans. Ook bewijst drie geometrisch aanwezige voedselvakjes nog niet dat ze legaal, beschikbaar en tegelijk bewerkbaar zijn.

## 8. Concrete open schakels en vervolg

1. **CityData-opbrengstmodifiers en populatieutility:** volg 495250/495330/495460 naar consumptie, totale opbrengst en de AI-afweging werker/scientist. Nodig om vier inwoners/één voedselvakje en de sciencegroeiregels cijfermatig te beoordelen.
2. **Finale improvementconstructie:** daadwerkelijke PW-afboeking, duur, familybits en eventuele vervanging/coexistentie. De delta-getter is hiervoor geen volledige simulatie.
3. **Werkbare oppervlakte en overlap:** bind 534510 → 502da0/511030 en centrumbehandeling vóór regels over drie bergen of drie voedselvakjes als uitvoerbare gebiedstest gelden.
4. **Positiescore naar toekomstpotentieel:** interfacegegevens bestaan, maar de aanroepers voor vestigingsscore/specialisatie, future-techhorizon en de onbekende centrum-scoreflag zijn nog niet volledig verbonden. Hergebruik [LOCATIEKWALITEIT.md](LOCATIEKWALITEIT.md) en de bestaande cacheanalyse; herhaal de bewezen scoreberekening niet.

Dit rondt het eerste P0.2-interfacepakket af. De brede fase A blijft open; de bovenstaande gaten vereisen gerichte vervolgketens, geen nieuwe spelstarts tijdens deze analyse.
