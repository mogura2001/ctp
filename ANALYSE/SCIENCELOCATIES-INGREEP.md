# Gerichte A-overdracht: science-locaties naast productie

13 oktober 2026, 18:03 Europe/Amsterdam. Twee beslisvragen beantwoord voor fase B. Doel1/1a/5: science-potentieel zelfstandig herkennen en opnemen in de bestaande directe, veilige, bereikbare bestemmingsunion. Alleen analyse; geen gameplaywijziging, binarypatch, spelstart, livequery, helper of nieuwe fixture. Brede fase A blijft afgesloten. Ownership uitsluitend dit bestand en VOORTGANG-SCIENCELOCATIES.md.

Bewijslabels: **F** bestandsfeit, **M** gebonden machinecode, **C** gelezen bestaande kandidaatbron, **O** uitvoerbare ontwerpafleiding, **R** runtimewaarneming. Hieronder geen nieuw R-bewijs. H3/B4 en 30–40 zijn technisch gecontroleerd binnen hun eerdere scope; C5 leverde geen T0/T1-activatiebewijs. Doel3 is afzonderlijk reeds gameplaygeaccepteerd en blijft behouden.

## Antwoord en afbakening

**Vraag 1:** de bestaande World-footprint, loaded terrein/good/environments, huidige food/rations en Improvement-getters zijn voldoende voor een zelfstandige science-capaciteitspredicate met minstens drie unieke momenteel open voedselvakjes, expliciete readiness en een **conditioneel groeiscenario**. Een afwijzende beschikbaarheids-/plaatsingsquery bewijst geen toekomstig bruikbaar vakje en ook geen specifiek techtekort. Onbekende voorwaarden blijven UNKNOWN; toekomstige deltas zijn uitsluitend een afzonderlijk PENDING-scenario.

**Vraag 2:** voeg science als rolalternatief aan dezelfde canonieke bestemming toe vóór gezamenlijke conflictselectie en departurematching. Tel een bestemming eenmaal, ook als production én science passen. Gebruik dezelfde type-/owner-/endpoint-/safety-/padcertificering en voorraadroute. Breid de vaste vijf-key-conflicttest gericht uit naar het werkelijke aantal onmisbare tiles; draai geen tweede onafhankelijke matching met dezelfde units/frontclaims. De union blijft een ondergrens zolang monopoly, transport, masks/horizon en scanbudget niet volledig gedekt zijn.

Exact nettofood, gegarandeerde aanleg/groeibeurten en gerealiseerde scientists vóór stichting zijn niet aangetoond. Dat blokkeert een als zodanig benoemd fysiek/conditioneel locatiescenario niet. Een voorstel dat zulke garanties wél verlangt, heeft een concrete aanvullende blokkade (§ voorwaarden); daarvoor geen volledige economie reconstrueren.

## Dekkingsmatrix vraag 1: terrein → capaciteit → ontwikkeling → groei

| Beslisschakel | Concrete invoer/route | Gedekt bewijs en grens |
| --- | --- | --- |
| Eigen civ/World en centrum | AiMain+20 civ; +30 World; World+28→533580→4bbd50→4ebdf0 | M, H2: spelergebonden centrumgate, zonder city-ID. Gatefalse is niet hetzelfde als te weinig foodtiles |
| Werkbare footprint | World+ac→534510→502da0; civ, centrum, countpointer, 20×8-byte MapPointData | M/E bestaand H2: twintig buren zonder centrum; echte buur/wrapconversies gebruiken, count0..20, unieke canonieke xyz |
| Huidig open | 511030, argument1; Cell+18 pophandle; 5154e0/Cell+14 cityhandle; armyfilters | M/E: reeds bezette workerposities en centra vallen af. Onbezette overlap mag; geen afstandsraster toevoegen. Geen garantie van latere Population-plaatsing |
| Canoniek terrein | World+a8→5342e0→514b70, signed Cell+d; TerrainDB455b10, stridec0 | M: gewone ondersteunde foodrecords 1 plains,4 grassland,5 desert,10 shallow,11 deep. Dit is een begin-dekking, geen complete whitelist van alle bruikbare wereldterreinen |
| Loaded omgeving/good | enginebasis+RVA67DD70→World-grid+1c; +RVA67DD3C→TerrainDB count+0/array+8; geselecteerd record+a0 good-subrecord | M/C H3 food_reader: dezelfde lokale goodflagselectie als500110, geen GOOD_INDEX als lokaal slot gebruiken. Recordidentiteit volgt de geladen huidige toestand |
| Bestaand voedselniveau | Cell.flags bits2..3; record+68/+6c/+70 = IRR1/2/3; environment+0 food | M parserbinding: een bestaande IRR2/3 is reeds aangelegd; bestaand IRR1 blijft huidige opbrengst, maar toekomstige IRR1-aanleg is normaal uitgesloten |
| Mogelijke volgende verbetering | geselecteerd record+6c ENV_IRR2, environment+20 materials/+24 time/+44 required advance | M/F: gewone land-IRR2 Agricultural Revolution; shallow/deep IRR2 Ocean Faring. Ontbrekend doelenvironment levert geen verzonnen farm/fishery. Overige good-/watervarianten alleen tellen bij aantoonbaar ondersteunde binding |
| Typebeschikbaarheid | AiMain+50 Improvement; +10→526a40, ret8/EAX | M: enabling/obsoletecontrole, geen positionele toelating. False kan meer betekenen dan ontbrekende enabling tech |
| Positionele toelating | Improvement+20→526ad0→4bfd70; args Improvement,type,0,positie,&rawstate; ret14h | M: naast tech ook pending/request en World-checks via +28/4d43e0. False is geen bewijs dat de plek na stichting/tech legaal zal zijn; rawstate niet eigenmachtig hernoemen |
| Huidig food | World+b8→534340→510f70→Cell500110; ret0ch, EAX1, int32output | M: current environment/goods/niveaus. +bc is productie. H3 food_reader sluit city/unit-food, special/dead/negatieve preclamp/overflow uit en vergelijkt loaded som met getter |
| Future food | Improvement+48→526d50→468b40; ret0ch, doubleST0 | M/E: delta binnen foodfamilie t.o.v. werkelijk niveau/goodcontext. Future=current+delta, uitsluitend scenario; +38 is absolute environmentcomponent, geen complete futuretilefood |
| Hypothetisch centrum | huidig centrumfood + geselecteerd record+50 ENV_CITY_BONUS.food | M/C H3: ondersteund normaal landcentrum zonder city/unit-food; centrum slechts eenmaal, buiten workerlijst |
| Consumptie | echte Player via AiMain+2c-interface+8; Player+1318 WGF-object; double+8, stand+48 | M: R=werkelijke rantsoenfactor. POP_WORKER en POP_WISEMAN hebben F HUNGER10; n van deze inwoners verbruiken 10nR, geen regering-foodfactor verzinnen |
| Groei | bewezen brutofoodsom/consumptie, crime-inhouding en positieve EatFood-route494fde–49522c | M/E bestaande econanalyses: positief nettooverschot voedt groeivoorraad; drempel/happiness/silo verschillen. Een foodmarge is geen bewezen groeibeurt of aanlegtermijn |

Bronnen: [H2](PRODUCTIEKANDIDAAT-H2.md), [H3](KANDIDAATVOEDSEL-H3.md), [terrein](TERREIN-EN-IMPROVEMENTS.md), [stadsgebied/constructie](IMPROVEMENTCONSTRUCTIE-EN-STADSGEBIED.md), [rantsoenen](RANTSOENEN-EN-STADSOPBRENGSTEN.md), [groei](VOEDSEL-GROEI-EN-KOLONISTEN.md). Primaire bindingen: BINAIR/production-candidate-h2-position-and-cell.txt, production-candidate-h2-center-gate-and-placement.txt, terrain-food-v2-environment-field-binding.txt, terrain-food-engine-improvement-details.txt, terrain-food-v2-canonical-sort-and-legality.txt, terrain-food-v2-delta-final-tech.txt, candidate-food-h3-world-queries.txt. Geen nieuwe disassemblage nodig.

## Zelfstandige science-predicate en betekenis van NOW/PENDING/UNKNOWN

**C, noodzakelijk verschil met productie:** PROEVEN/production-h3/model.py, current_model, roept capacity aan en springt bij status1 (minder dan drie bergen) direct naar current_no_plan, **vóór** rations, centrumfood en workerfood. Het bestaande H3Classifier-status2 eisen sluit gewone science-locaties zonder bergen dus uit. Science deelt de enum/reader/HostBinding, maar krijgt een eigen predicate. De capacity-uitvoer met status1 bevat wel geldige open posities; gebruik succes!=UNKNOWN, niet alleen GE3bergen. Geen driebergenvoorwaarde of ontbrekende productiemarge aan science doorgeven.

Hergebruik PROEVEN/production-h3/components.py: capacity, food_reader, poscmp; model.py uitsluitend voor de bewezen rations-/scenariorekenroute, niet voor zijn productionplan_select. PROEVEN/production-h3/development.py: development_tile maakt al onderscheid tussen 0UNKNOWN,1AVAILABILITY_PENDING,2PLACE_UNKNOWN,3READY_NOT_BUILT,4ALREADY_PRESENT. Zijn IRR2-route ondersteunt expliciet de vijf hierboven gebonden terreinindices, leest loaded environment/kosten/tijd/advance, bewaart raw +10/+20/state en vraagt echte +48. Deze publieke development_model bevat eveneens het productionplan: deel de tilefunctie, niet die volledige modeluitkomst.

Voer per open tile de checks uit en houd twee vragen gescheiden: (a) past hier aantoonbaar een toegestane foodontwikkeling, (b) welk voedsel is nu daadwerkelijk aanwezig? Een al aanwezige tweede/derde generatie telt met de huidige getteropbrengst; voor nog aan te leggen IRR2 gelden loaded positief foodenvironment en echte type-/positionele checks. Meer dan drie geschikte tiles bewaren als mogelijkheden voor latere groei; claim voor het gekozen minimumplan alleen de werkelijk benodigde tiles.

| Uitkomst | Toelaatbare interpretatie | Gscience-credit |
| --- | --- | --- |
| NOW, conditioneel science-plan | Minstens drie unieke open tiles met bestaande toegestane foodontwikkeling of READY_NOT_BUILT-toelating, plus een positief **huidig** groeiscenario onder genoemde modifiers/crimevoorwaarden | Mogelijke toevoeging aan Gcert na alle overige B4-certificaten; READY_NOT_BUILT-delta blijft buiten currentfood |
| PENDING, ontwikkeling | Loaded ENV_IRR2 en scenario bekend, maar aanleg/availability ontbreekt; bestaande tilefunctie onderscheidt beschikbaarheidsfalse van plaatsingsunknown | Geen huidige credit alleen op grond van toekomstige food. Bij typefalse niet automatisch 'uitsluitend tech ontbreekt' claimen |
| UNKNOWN | Onvoldoende geldige tiles door onbekende toelating/omgeving, unsupported terrein/context, query-/fingerprintfout of onbekende groeivoorwaarde | Geen certificaat; geen bewezen ongeschikt/geen ruimte |
| Bekend onvoldoende binnen ondersteunde scope | Volledige geldige lijst heeft minder dan drie passende tiles, of gekozen brutofoodscenario heeft geen positieve marge | Geen science-certificaat voor dat scenario; production/monopoly/gewone uitbreiding blijven afzonderlijk mogelijk |

De NOW-route is een mogelijke **ontwerpskeuze van dezelfde bewijssterkte als het bestaande H3-scenario**; dit document kent geen exacte sciencebevolkingdrempel of scoregewicht toe. PENDING-techpotentieel blijft een toekomstige kans; beschikbaarheid/plaatsing vóór stichting kunnen wijzigen. Normaal geen IRR1-aanleg als oplossing. De afzonderlijke Labyrinth-uitzondering mag geen science-brede vrijstelling worden. Reeds aanwezige IRR1 telt wel in huidige rawfood. Bestaande IRR3 niet naar IRR2 downgraden of beide opbrengsten stapelen.

**Conditionele groei zonder forecast:** noem de gemodelleerde grootte n en het aantal foodwerkers k (minimaal drie foodmogelijkheden als locatiekenmerk). Voor een eerste minimumscenario met drie gewone foodwerkers is n=k=3; dit zegt alleen iets over groei vanuit die toestand. Voor n>k hebben overige gewone inwoners/scientists nog steeds HUNGER10; nul tilefood van een scientist is geen nulconsumptie. Grootte8/10 en het vierde/vijfde foodvakje zijn latere ontwerpkeuzes, geen huidige harde grenzen.

    S_now = gelezen hypothetisch centrumfood + som(currentfood van k gekozen tiles)
    D_n = 10 × n × R
    voorwaarden = ZERO_NEW_CITY_MODIFIERS en crime ≤ c, met 0 ≤ c < 1
    S_now × (1−c) > D_n  => voldoende conditionele positieve voedselmarge

De strikte > onderscheidt groei van enkel onderhoud. Voor S>0 is c < 1−D/S voldoende voor positieve marge; publiceer deze vereiste grens zonder actuele crime0 te claimen. In het expliciete nulmodifiersscenario kunnen beginpopulaties1/2/3 met beschikbare subsetfood apart worden beoordeeld om early-uitvoerbaarheid te bespreken; een positieve grootte3som bewijst niet automatisch dat de stad daar tijdig komt. Een n=4-scenario met drie foodwerkers en een vierde inwoner kan de extra onderhoudslast tonen, zonder scientists toe te wijzen of een sciencegebouw te bouwen. Geen nieuwe PW/happinessforecast nodig.

S_pending gebruikt afzonderlijk werkelijk opgevraagde fooddeltas en vermeldt vereiste tech/plaatsing/aanleg. Materials en ENV_TIME zijn doelkosten/projectparameter, geen bewezen totaalaantal beurten tot bruikbare science-stad of beschikbare PW. Pendinglegaliteit na stichting is niet bewezen door een loaded environment. Positieve brutofoodpotentie is evenmin toekomstige directe wetenschap. Gebouwen/workerallocator/scientistbeleid blijven buiten deze ingreep; [directe wetenschap](DIRECTE-WETENSCHAP-EN-SCIENCEGEBOUWEN.md) toont hun aparte keten.

## Dekkingsmatrix vraag 2: rolunion → slotcertificaat → voorraad

| Schakel | Bestaande huidige bron / codepunten | Gerichte aansluiting |
| --- | --- | --- |
| Pass en capture | movement2002b079; groundcapture2007abac vóór goallimiet; scope2002b0d8; actual→desired20066b81 | Zelfde owner/generatie en eigen transient buffers; science leest dezelfde immutable kandidaatkopie |
| Kandidaatruimte | AiMap+58 heap, count+60,array+64,sentinel; huidige masks, distancehorizon+68; canonieke prefix64 uit maximaal4096copieën | Geen science-specifieke tweede scanwereld; suffix/cutoff/horizon/maskuitsluiting is PARTIAL, geen COMPLETE_G0 |
| Rolherkenning | native.py roles/production_roles: World+168 ruwe B>0, H3Classifier=2, model1 en positieve marge; slot wordt productionplan | Eén zelfstandige sciencepredicate naast productie. B>0/GE3bergen mag geen science-definitie worden. Behoudt ontwerp zo'n filter als beperkte scope, meld die uitsluiting expliciet |
| Unieke bestemming/alternatief | canonical_key; slot+0 externe positie,+8 canonieke key,+16 rank; ORDER | Merge per centrumkey; production/science zijn alternatieven van één slot. Kies één uitvoerbaar rolplan met eigen mandatorykeys; tel geen twee slots |
| Onmisbare tiles | plan_conflict vergelijkt nu vaste vijf keys: centrum+vier productionworkers, slot+32..+64 | Science-minimum is centrum+driefoodkeys; werkelijke keycount gebruiken. Geen vierde fictieve worker/dubbele padkey als padding. Extra voor het gekozen groeiscenario noodzakelijke foodtile eveneens claimen |
| Rangorde en reservering | order_roles sorteert eigen indices; select_direct_plans kijkt conflicts vóór endpoint/source | Orden vóór gezamenlijke claims, deterministisch. Nieuwe science-urgentie/gewicht expliciet in B; geen futurefood als huidige score. Onnodige geometrische footprintoverlap blijft toegestaan |
| Endpoint/type/safety | Player+34; UNIT_SETTLER-preview; World+54/+78, Strategic_Map20083b10 en Player+14 coördinaten | Ongewijzigd per rolplan; mooie sciencecapaciteit is geen juridische of veilige bestemming |
| Direct pad | AiMain+34,vtable746220+0c→5826a0,ret50h; mode1 typequery; eigen buffer/free5866e0 | Bestaande directe-landcontract en elk veilig z0-padpunt behouden. Waterfood in landstad is geen transportpad; foodtiles hoeven geen settlerbestemmingen te worden |
| Vertrekvoorraad | read_set/read_departure, departures: existing gewone unit, frontproductie, bouwbare stad | Eén gedeelde bronlijst en één select_direct_plans. Iedere bestaande unit/frontclaim eenmaal, nieuwbouworigin mag meerdere toekomstige slots ondersteunen |
| Historische hints | Goal+30/+34↔Squad+5c/+60; copied stable IDs/keys vóór cleanup | Revalideren, geen pointers uit vorige pass en geen nieuwe scienceclaim op onbewezen squadmapping |
| D en cap | policy.py finalize, original_demand; P.original184/gcert188/remaining56/desired60; quota20065a4c→Choose20065900 | Gcert=cardinaliteit geselecteerde production/science-union. D=min(R,max(Dorig,Gcert)); native Actual eenmaal; cap/opening30/Theocracy40 ongewijzigd |
| Lifetime/save | scope-end status5,owner0; geen serialized producerstate | Nieuwe classifierdata even vluchtig. B2-N30record/Doel3payload blijven exact behouden; geen permanente sciencerol nodig voor locatiesnapshot |

Bronnen: [producer](PRODUCER-SETTLERVRAAG-B4.md), [type-/claims](TYPE-EN-VERTREKCLAIMS-B4.md), [30–40-analyse](UITBREIDING-30-40.md), [30–40-ontwerp](../ONTWERP/UITBREIDING-30-40.md), [rootreview](REVIEW-UITBREIDING-30-40.md). Gelezen concrete kandidaatbron: PROEVEN/uitbreiding-30-40/20261012T181500/native.py (roles,ordering,conflicts,selection), policy.py (canonical_prefix,finalize), integration_base.py (host,wrappers,quota). Deze bronnen zijn bouw-/offlinebewijs, geen geïnstalleerde sciencefunctie of echte hostacceptatie.

### Uitvoerbare aanpassingsroute voor fase B

1. Specificeer zelfstandige ScienceResult met open-foodtilekeys, readiness per tile, currentfood, pendingdelta/advance/materials/time, gekozen n/k/scenariovoorwaarden, marge/crimegrens en reason. Geen productievelden als scienceantwoord hernoemen.
2. Deel h2/food_reader/HostBinding en de IRR2-development_tile-route onder dezelfde fingerprints/ABI; omzeil uitsluitend de productie-GE3-voorwaarde in het nieuwe sciencemodel. Science blijft onafhankelijk van drie bergen.
3. Vervang uitsluitend de rolopbouw door per canoniek centrum production/science-alternatieven. Pas fixed-five mandatorykeyvergelijking aan naar echte keycount en kies één plan; gedeelde endpoint/type/pathcertificering en bronnen eenmaal uitvoeren. Herbereken bounded slotlayout/scratch en guards in C; het bestaande SLOT_STRIDE1152 is een huidig feit, geen garantie dat willekeurige sciencevelden er nog in passen.
4. Geef alleen volledig ondersteunde huidige scenario's positieve credit. Bij PENDING/UNKNOWN geen extra sciencecredit; volledig bewezen andere slots mogen volgens bestaande prefixregels blijven. Maak geen COMPLETE_G0 en laat Dorig/cap/Actualroute behouden.
5. Maak eerst het concrete B-voorstel met scenario-/urgentiebeleid en kleine gewijzigde meetlat. Geen nieuw framework, constructorforecast, observer of herhaling van ongewijzigde109B4gevallen. Pas fase C bouwt/controleert de gewijzigde science-/uniongevallen; echte activatie en gameplay blijven aparte poorten.

## Voorwaarden, blockers en begrensde backlog

**Geen resterende A-blocker voor een conditioneel science-locatievoorstel:** enum, loaded environment, tech-/positionqueries, food/rations en de gezamenlijke selectiepunten zijn concreet gebonden. De ontwerper moet het gekozen n/k-scenario, de vereiste crime-/modifiercondities en NOW-urgentie expliciet benoemen. Een conditionele marge niet als gegarandeerd netto verkopen.

**Alleen bij een sterkere claim ontstaat een echte blocker:** exact/garantied nettofood vóór stichting vereist nog de toekomstige stadstype/flat/percent/wondercache en happiness/crime; gegarandeerde IRR2-bouw na onbekende tech of huidige plaatsingsfalse vereist toekomstlegaliteit/aanlegbeleid. Er is geen algemene gebonden candidate-cityquery. Zulke claims niet door crime0, fictieve city-ID of PWstandaard oplossen. Conservative UNKNOWN houdt het beperkte ontwerp uitvoerbaar.

Fase C-afhankelijkheden voor deze concrete ingreep: echte versie/context/fingerprint, gebonden interface-ABI/x87/controlword, aangepast mandatorykey/slotlayout, bestaande bron-/type-/claimguards, beperkte gewijzigde offlinegevallen en daarna echte host/benchmark. De gewone installationutility vraagt een huidige werker van de stad; herkenning van drie foodmogelijkheden zorgt op zichzelf dus nog niet voor aanleg. FLI/AIP biedt rang-/food-/groeigewichten, geen aangetoonde complete per-locatie sciencepredicate. Daarom sluit aanvullende DLL-selectielogica aan op de bestaande route; geen SLIC of extra bonus.

Niet-blokkerende vervolgscope blijft expliciet bestaan: monopoly-identiteiten/rijksvoorraad/handelsbinding, volledig transport/carrier/techbeleid, packinguitzonderingen en ruimer zoekgebied, gebouwen/workerallocator/scientists, growthtime/granary/PWbeleid en latere rollen. Ook na science-uitbreiding is Gcert geen complete G en blijft anti-ophoping open zolang Dorigfallback nodig is. Deze opdracht vervangt of verkleint de volle projectdoelen niet.

AAIP-les (**F**, geen gemeten gameplay): hogere silo/aqueductprioriteiten en gewijzigde farm/popgewichten illustreren beïnvloedbare voorkeuren; zij leveren geen science-locatieclassifier of gegarandeerde ontwikkelroute. Terreinregels zijn in OG/AAIP/proef bytegelijk in het bestaande bewijs. Robotcom.map past bij oorspronkelijke DLL (timestamp37b894e7/base20000000); civctp.map past niet bij engine (timestamp37d6f702/base400000/SHA b1b5256f...). Loaded huidige kandidaatcode moet zijn eigen pinning blijven gebruiken; geen mapadresclaim voor engine.

Overdracht: beide vragen voldoende voor ctp_ontwerper. Volgende oplevering is één begrensd science-predicate/unionvoorstel, zonder gebouwen/laborers toe te passen. Analyse stopt bij deze overdracht; geen achtergrondrun of spelactiviteit achtergelaten.
