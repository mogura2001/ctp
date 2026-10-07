# Bevolkingplaatsing en scientists — bestaande beslisketen

5 oktober 2026. Fase A, afgebakend vervolg op [terreinbinding](TERREIN-EN-IMPROVEMENTS.md) en [voedsel/groei](VOEDSEL-GROEI-EN-KOLONISTEN.md). Geen gameplaywijzigingen, spelstarts of ontwerp. Dit pakket volgt de bestaande FLI-gewichten via stadsplaatsing tot concrete Population-aanvragen. Netto rijksgoud/scienceallocatie wordt afzonderlijk onderzocht.

## 1. Belangrijkste uitkomst

Vervolg6 oktober: [BARDS-EN-GELUKSVOORWAARDEN](BARDS-EN-GELUKSVOORWAARDEN.md) bindt de eerder open entertainerhelper/geluksinvoer met8 controles. De AI telt bards aan onder de callergrens; status/cache/volledige riot blijven begrensde open vragen. [RANTSOENEN-EN-STADSOPBRENGSTEN](RANTSOENEN-EN-STADSOPBRENGSTEN.md) heeft inmiddels ook de hier historisch open foodfactor/getter aan echte rations gebonden.

De AI heeft al een volledige route om inwoners over vakjes en specialists te verdelen. Eerst behandelt zij minimumvoorwaarden en entertainers; daarna vergelijkt zij resterende gewone inwoners met beste vakjes en beschikbare specialists. Scientists ontbreken dus niet als mogelijkheid. De huidige route kent echter geen aangetoonde productie/science-stadsrol met de gebruikersregels van drie bergen, omvang vier of vaste aantallen voedselwerkers bij omvang acht/tien.

Drie concrete verschillen met aannames:

- `pop_production_min/max`, `pop_food_min/max` en `pop_science` zijn gewichten, geen gevraagde hoeveelheid productie/voedsel of aantal scientists.
- `SCIENCE_PER_POP` levert via een afzonderlijke engineketen een bijdrage op basis van totale stadsbevolking. Dit is niet het aantal of de basisscience van scientists.
- Het FLI-commentaar dat `min_food_factor=1.5` overal anderhalf maal onderhoud afdwingt volgt niet rechtstreeks uit de twee echte minimumfood-aanroepen: eerst multiplier 1, daarna conditioneel factor minus 1, met dezelfde reeds bijgewerkte foodteller.

Bewijslabels: **T** tekstbestand; **B** originele machinecode en gecontroleerde interface; **E** originele instructies uitgevoerd met synthetische gegevens. Geen nieuwe **R**untimegamewaarneming. De definitieve offlinecontrole heeft **27/27** geslaagde gevallen, met expliciet benoemde externe recorder-mocks bij tien plaatsingscontroles.

De bestaande binarybindings worden hergebruikt. robotcom.dll/map: timestamp37b894e7, imagebase20000000, SHA2563025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44. Engine: timestamp37d6f702, imagebase400000, SHA256b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79. civctp.map past niet; engine-adressen zijn rechtstreeks gevolgd. De helper controleert beide hashes.

## 2. Profielgewichten en herverdeling

**T:** [outputs.fli](../CTP-og/ctp_data/default/aidata/outputs.fli) definieert onder andere:

| Output | Originele declaratiestandaard | Betekenis in gevolgde code |
|---|---:|---|
| min_food_factor | 1.5 | Parameter voor een conditionele tweede minimumfoodfase |
| pop_food_max / min | 100 / 10 | Foodgewicht voor de twee stadslistgroepen |
| pop_production_min / max | 110 / 110 | Productiegewicht voor de twee stadslistgroepen |
| pop_gold | 150 | Goldgewicht |
| pop_science | 150 | Science-specialistgewicht |
| pop_happiness | 0 | Entertainmentgewicht na minimumvoorwaarden |

Deze declaraties zijn niet automatisch de effectieve fuzzy uitkomsten van iedere beurt. De actieve persoonlijkheidsbestanden includen [set_science_speed.fli](../CTP-og/ctp_data/default/aidata/set_science_speed.fli), [set_resource_desire.fli](../CTP-og/ctp_data/default/aidata/set_resource_desire.fli) en [set_food_or_prod.fli](../CTP-og/ctp_data/default/aidata/set_food_or_prod.fli). Opening, science-tempo, oorlog/unitfocus en goudcrisis kunnen dezelfde outputs beïnvloeden. De algemene beginturn.fli toont ook uitgecommentarieerde includes; het werkelijke profielpad blijft doorslaggevend. Dit sluit aan op de bewezen [AIP-laadwerking](AIP-LAADWERKING.md), maar deze outputs zijn FLI-gewichten en geen nieuwe AIP-velden.

**B:** FSAllocatePopulation::Execute (2002a820) kiest de argumenten voor PlaceAllPop:

1. Bij één stad en minder dan drie **gewone burgers**: food_max en production_min.
2. Bij één stad en ten minste drie gewone burgers: food_min en production_max.
3. Bij meerdere steden: twee delen van de bestaande CityList. De eerste gebruikt food_max/production_min; de tweede normaal food_min/production_max. In de tweede groep krijgt een stad met minder dan drie gewone burgers alsnog food_max/production_min.

De grens is drie gewone burgers via CityAgent::GetNumCitizens (20020800 → CityAgent+b0), geen bewezen grens van drie totale inwoners inclusief slaven. De precieze totstandkoming en ordening van de CityList-partitie blijven open. Bewijs: [allocatie-entry en caller](BINAIR/population-scientists-allocation-entry.txt), [burgergetter](BINAIR/population-scientists-num-citizens.txt).

Voor deze allocatie wordt `pop_science` nul gemaakt als ScienceAgent+b0 ≤ +64 (2002a834–2002a851). Hergebruik van ScienceAgent::Init bewijst +b0 als het totale advance-aantal, +64 als geteld bekende advances; LearnedScience verhoogt +64. Dit is beëindiging van scienceprioriteit na uitgeput onderzoek, geen academyvoorwaarde voor de early game. Bewijs: [bestaande science-init](BINAIR/research-government-budget-beginturn.txt), [learned-event](BINAIR/population-scientists-research-completion.txt), [allocatiecaller](BINAIR/population-scientists-allocation-entry.txt).

**B:** PopNeedsChanging (200209f0) vergelijkt gecachete food-, productie- en goldgewichten; controleert daarnaast AIP/cityflags en Population-statusslots +10..+28, en eindigt anders met een vijfbeurtenfasering (`turn % 5 == citylistindex % 5`, 20020b89–20020bb2). Niet ieder unchanged-geval herverdeelt dus iedere beurt. Science/happiness zijn niet onderdeel van de drie rechtstreekse gewichtsvergelijkingen. De semantiek van alle statusflags en de volledige save/load-werking van deze caches zijn nog niet ontleed.

## 3. Van PlaceAllPop naar concrete engineacties

PlaceAllPop (20020bd0) haalt totaalbevolking en het aparte aantal via Population+2c/+30 op. De tweede groep wordt verder onderscheiden via Population+38; gewone burgers en die aparte groep hebben afzonderlijke counters. Engine-best-specialistfilters herkennen de slaveflag; de volledige betekenis van alle totalen/filtercombinaties is niet tot uitsluitend enum-namen teruggebracht.

Vervolgens roept PlaceAllPop Player+24c/+11c aan, vraagt kandidaatvakjes via FindOpenTiles, werkt productiebonussen bij en voert SatisfyMinimumCityRequirements uit. Daarna volgt bij resterende bevolking MaximizeCityOutput. Aan het einde staat Player+250 (20020de3). De precieze reset/afrondingssemantiek van Player+24c/+11c/+250 blijft open; het is geen bewijs dat elke aanvraag altijd slaagt. Bewijs: [plaatsingshoofdroute](BINAIR/population-scientists-allocation-entry.txt).

De interfaces zijn echte COM-objecten uit de bestaande init. AiMain+2c is Player-vtable744660; AiMain+40 is Population-vtable744948. Die laatste komt via GameState+48 →526010 en constructor52c0d0. Hergebruik: [voedsel-interfaceconstructors](BINAIR/food-growth-interface-constructors.txt), [DLL-init](BINAIR/terrain-food-ai-interface-init.txt).

| Concrete aanvraag | Enginebinding | Verder gevolgde actie |
|---|---|---|
| Population+3c, type kiezen | 52c430 → 4c98e0 | Resolveert stad/inwoner, roept 4ccf60 voor het gekozen specialisttype aan |
| Population+60, vakje plaatsen | 52c6e0 → 4c9fe0 | Positie-/stad/inwonercontrole, World510d00 |
| Population+38 | 52c410 → 4c97f0 | Inwonerstatus die gewone/afzonderlijke plaatsingsloops onderscheidt |
| Player+27c, beste specialists | 52b820 → 49eab0 | Geeft cached types en bonusbedragen voor vier specialistcategorieën |
| Population+70, scientistwaarde | 52c780 → 4ca210 | Tijdelijk type2, sciencebonus lezen, type herstellen, knowledgebonus toepassen |

Bewijs: [slotwaarden](BINAIR/population-scientists-interface-slots.txt), [wrappers](BINAIR/population-scientists-engine-interface.txt), [engine-acties](BINAIR/population-scientists-engine-specialist-selection.txt), [Pop-type/Worldactie](BINAIR/population-scientists-parser-pop-actions.txt).

PutCitizenBestTile (20021ce0) vraagt Population+60 aan, controleert succes, telt World+bc/+b8 waarden bij de lokale bookkeeping en verwijdert het gebruikte kandidaatvakje uit de lijst. Bij mislukking zoekt hij verder. PutCitizenBestPosition (20021c00) kiest de tile als diens utility ten minste de specialistutility is, het specialisttype ongeldig is, of de gevolgde laagcheck z=1 geldt; anders vraagt hij Population+3c aan. Het specialistverzoek kan bij de foutoutput nogmaals plaatsvinden. De complete World510d00-interne plaatsingsketen en alle foutstatussen blijven open. Bewijs: [utility en acties](BINAIR/population-scientists-utility-actions.txt).

## 4. Minimumvoorwaarden: onderhoud, productie en entertainment

SatisfyMinimumCityRequirements (20020eb0) initialiseert de tallies met de centrumopbrengst: Population+44 →52c580 →4c9cb0 →CityData495250 voor food, +48 →52c5b0 →4c9d50 →495330 voor productie. Het centrum zit dus als afzonderlijke beginbijdrage in deze plaatsingsberekening. Dit bewijst nog niet de automatische centrumwerker-/bevolkingsregels van de gehele engine. Bewijs: [centrumwrappers](BINAIR/population-scientists-city-center-yields.txt), [echte CityData-calls](BINAIR/population-scientists-center-inputs.txt).

De gevolgde volgorde is entertainerfase, minimumfood met multiplier1, nogmaals entertainers, een conditionele extra-foodfase, minimumproductie, minimumgold en een laatste entertainerfase. Daardoor blijven beschikbare inwoners niet allemaal vrij voor de latere scientistvergelijking. Goldstrategie en rijksbudget zijn elders onderzocht; dit rapport legt alleen de plaats ervan vast.

PlacePopMinimumFood (200212d0) vraagt Population+58 →52c6c0 →4c9ae0 →CityData494ba0 om de behoefte. 494ba0 sommeert positieve hunger per inwoner (4ccaa0) maal de Player-factor uit 4c27f0. De exacte ration/governmentbinding van deze laatste factor is nog open. De wrapper rondt de behoefte af naar een integer; de DLL neemt vervolgens `ceil(behoefte × multiplier)` als target. Zolang de cumulatieve foodteller lager is en inwoners/kandidaten overblijven, kiest zij een food-georiënteerd vakje en vraagt PlaceACitizen aan. Bewijs: [minimumfoodloop](BINAIR/population-scientists-minimum-placement.txt), [behoeftewrapper](BINAIR/population-scientists-food-requirement-wrapper.txt), [stadopvraag](BINAIR/population-scientists-food-science-city-getters.txt), [honger/factor-som](BINAIR/population-scientists-food-demand.txt).

**Belangrijke B-beperking:** 20020fa9 geeft multiplier1. De tweede call20021063 krijgt `min_food_factor − 1` en dezelfde pointer naar de foodteller (&ebp−14). Die tweede call is ook afhankelijk van de branch20020fd5–20021021, met happiness/entertainers en Player+13c. Bij een standaardfactor1.5 is het tweede directe target dus `ceil(behoefte ×0.5)`, geen automatische aanvulling tot `ceil(behoefte ×1.5)`. De eerste call heeft de counter al aangevuld. Het FLI-commentaar en de eenvoudige strategische interpretatie ‘50% extra groei afdwingen’ zijn daarom niet als bewezen enginegedrag overgenomen. Geen fullturn- of benchmarkeffect gemeten.

PlacePopMinimumProduction (20021430) slaat plaatsing over wanneer de opgebouwde productie positief is. Anders zoekt hij een productiezwaar beste kandidaat en vraagt **hoogstens eenmaal** PlaceACitizen aan. Hij gebruikt niet een vereiste productiehoeveelheid110, geen drie-bergtest en geen permanente cap op bevolking4. **E:** vier controles bevestigen positieve-centrumskip, keuze voor het productierijkere vakje, maximaal één aanvraag en geen keuze wanneer er geen positieve kandidaat is. De externe PlaceACitizen-call is daarbij een recorder-mock; daadwerkelijke tileplaatsing is apart B gevolgd.

SupplyEntertainers (20021710) vraagt een Population-status/geluksopvraag, rekent met de musicianeffectwaarde en geeft waar nodig Population+34 en +3c met type1. Er zijn verschillende aanroepen met ruime tijdelijke grenzen en daarna de echte `min_happiness/max_crime` outputs. De volledige herberekening van happiness, crime en eventuele revolte is nog niet gereconstrueerd. Deze fase is dus een echte concurrent om inwoners, met nog open details.

## 5. Utility van een vakje en een scientist

De gewone tile-input food/productie/gold en het extra veld +20 zijn in het [terreinrapport](TERREIN-EN-IMPROVEMENTS.md) verbonden aan Player+120 →4c9e90. Food/productie kunnen CityData-modifiers bevatten; gebruik geen raw terreinwaarde als bewezen gelijke AI-invoer.

**B/E:** CalcTileUtility (20021ac0), eveneens inline in MaximizeCityOutput, schrijft voor iedere kandidaat:

`Utile = food × Wfood + productie × Wprod + gold × (1 + citybonus[type4]) × Wgold + extra`

Het extra veld heeft nog geen volledig gebonden semantische naam. GetProductionBonus (2001ff40) leest het aangevraagde type uit CityAgent+21c; een ontbrekende bonusarray geeft nul. Vier controles voeren zowel deze oorspronkelijke getter als de originele x87-tileberekening uit, zonder externe mock. Bewijs: [utilitycode](BINAIR/population-scientists-utility-actions.txt), [bonusgetter](BINAIR/population-scientists-production-bonus.txt), [controle-uitvoer](BINAIR/population-scientists-choice-checks.json).

MaximizeCityOutput (200217d0) sorteert de vakjes, handelt de aparte inwonergroep eerst op vakjes af, en haalt via Player+27c de beste beschikbare specialisttypes plus bonuswaarden op. Voor de scientistkandidaat staat in de actieve code200218e3–2002190a:

`Uscientist = beste_sciencebonus × (1 + citybonus[type5]) × Wscience`

Bij ontbrekend beschikbaar type staat een grote negatieve sentinel. Grunt, entertainer en merchant vormen afzonderlijke concurrerende candidates; hun onderlinge gelijkstandsregels zijn niet allemaal los gecontroleerd. Na die selectie vergelijkt PutCitizenBestPosition de gekozen specialist met de beste overgebleven tile. **E:** scientist hoger → specialistaanvraag; gelijk → tile; tile hoger → tile; ongeldig specialisttype → tile; laag1 → tile. Zonder kandidaatvakje kan de geteste helper alsnog een specialist aanvragen, maar de caller heeft eigen counters/20-slotgrenzen. Dit is geen bewijs van complete afhandeling van steden boven twintig plaatsbare tileposities.

CalcScientistUtility (20021bc0) biedt daarnaast Population+70 maal het gewicht. De actieve MaximizeCityOutput-route gebruikt rechtstreeks de best-specialistdata; dit rapport verwart het bestaan van die aparte utilityhelper niet met een bewezen directe call daarnaartoe.

## 6. Beschikbare scientisttypes en sciencegebouwen

**T:** [pop.txt](../CTP-og/ctp_data/default/gamedata/pop.txt) geeft POP_WISEMAN BONUS_SCIENCE10, HUNGER10 en IMPROVEMENT NULL. Andere specialists hebben onder andere theater/factory/bazaar/bank als vereiste gebouw. De wisemanrecord noemt geen academy als toelatingsvoorwaarde. De PopDB-volgorde en het abstracte Population-type2 zijn verschillende dingen; een abstracte aanvraag type2 wordt niet als tekstrecordindex2 behandeld.

**B:** CityData49e940 herbouwt de cache voor beste specialisttypen. Deze functie:

1. Sluit slaveflag20 uit en vereist eligibilitybit10. De naam CAN_WORK_CITY past bij de specialistrecords; de exacte PopDB-parserbinding van die bitnaam is in dit pakket nog open.
2. Controleert eventueel vereist improvement via CityData+48/+4c gebouwmasker.
3. Controleert eventuele min/max stadsomvang.
4. Controleert de governmentmaskerbit uit PopRecord+68.
5. Kiest per specialistcategorie de hoogste bonus; gelijke bonus behoudt de eerder gevonden recordindex.

De sciencecategorie gebruikt PopRecord+4c en CityData+3f8/+3fc. Player+27c geeft die cache door. **E:** negen oorspronkelijke writer/gettercontroles bevestigen hoogste bonus, gebouw afwezig/aanwezig, minimum/maximumomvang, governmentmasker, slave-/noncity-filter en gelijkstand. De volledige PopDB-parser/defaultgovernmentmaskers en alle cache-refresh-callers blijven open. Bewijs: [writer](BINAIR/population-scientists-best-type-writers.txt), [DB-getter](BINAIR/population-scientists-parser-pop-actions.txt), [cache-output](BINAIR/population-scientists-engine-specialist-selection.txt).

Academy/library/sciencegebouwen beïnvloeden daarom zowel opbrengstmodifiers als de afzonderlijke science-per-pop-bijdrage, zonder dat hun aanwezigheid in deze onderzochte wisemanregel de algemene scientistaanvraag blokkeert. Of de bestaande gewichten ze in een concreet beginstadje werkelijk aantrekkelijk maken is een numerieke keuze, geen bewijs dat de AI volgens onze gewenste stadsspecialisatie werkt.

## 7. SCIENCE_PER_POP is een afzonderlijke bijdrage

**T:** [improve.txt](../CTP-og/ctp_data/default/gamedata/improve.txt) bevat onder andere IMPROVE_LIBRARY knowledgepercent25 en science_per_pop0.5; academy knowledgepercent50 en science_per_pop0.5; university eveneens science_per_pop0.5. De meeste genoemde procentwaarden in de tekst zijn gehele percentages, terwijl de gebonden bonusarray fracties gebruikt.

**B:** exact token SCIENCE_PER_POP504 komt via de echte improvementparsertabel45f69c, index(token−456), bij case45f611. Die leest de float en schrijft ImprovementRecord+f0. Getter45e470 telt voor aanwezige gebouwen de doubles op dit veld op; recordstride108, tellijst BuildingDB+d8/+1a0. Zie [token](BINAIR/population-scientists-token-candidates.txt), [case](BINAIR/population-scientists-parser-pop-actions.txt), [getter](BINAIR/population-scientists-science-per-pop-application.txt).

De echte stadscode49e879–49e89d vraagt de som op met het gebouwmasker, vermenigvuldigt die met de bevolking en voegt de geconverteerde integerbijdrage toe aan de sciencebasis. De daaropvolgende code verwerkt onder andere CityData+3e0 knowledgepercent en verdere contextbonussen. De voorafgaande loop leest per inwoner basisscience via4ccc50. Deze bevolkingmaalgebouwbijdrage is dus onderscheiden van de extra basisscience die een scientist ten opzichte van een normale werker heeft. Bewijs: [echte toepassing](BINAIR/population-scientists-science-per-pop-application.txt).

**E:** gettercontroles tonen0.5 voor één aanwezig0.5-gebouw,1.0 voor twee, negeren een afwezig gebouw en leveren0 zonder aanwezige gebouwen. Dat bewijst optelling, niet een volledige nettoscienceformule voor een gespeelde stad. De knowledgepercent-binding naar type5/+3e0 wordt hergebruikt uit [percentparser](BINAIR/economy-gold-parser-final.txt), [effectarray](BINAIR/economy-gold-effect-array.txt) en [BuildingDB-output](BINAIR/food-growth-building-population.txt); root beheert deze gezamenlijke economiebronnen.

## 8. AAIP-lessen en projectbetekenis

**T:** AAIP laat pop.txt bytegelijk aan OG/proef (SHA25614bed4fddb6f4a3a7af0d58679b838f7ccd51dc08f7e417f4a959aca53634f51). In [AAIP outputs](../CTP-AAIP/ctp_data/default/aidata/outputs.fli) verandert de declaratiestandaard pop_food_min10→100, pop_science150→100 en de high_growth-membershipcenter2.0→1.7. De default min_food_factor blijft1.5. Profielregels kunnen deze outputs alsnog beïnvloeden; bovenstaande tekstverschillen zijn geen gemeten effect of bewijs van gewenste specialisatie. Hergebruik [AAIP-diff](INVENTARIS/aaip-ai-diff.md).

Voor onze productiesteden laat dit pakket zien dat de bestaande AI voedselonderhoud en productievakjes kan behandelen. De minimumproductiestap garandeert echter geen drie bergen en stopt geen groei bij vier inwoners. Voor sciencesteden bestaat de tile-versus-scientistvergelijking al en reageren de utilitywaarden op sciencegebouwbonussen. De regels van drie voedselvakjes, vierde voedselwerker bij omvang8 en vijfde bij10 komen niet als aangetoonde bestaande voorwaarden uit deze keten.

Een goede afweging tussen groei en een extra scientist vereist actuele foodoverschot/groeidrempel, citymodifiers, gebouwenbonus, nog beschikbare speeltijd en de effectieve weights. De bewezen afwijkende AI-settlerkosten uit het voedselrapport blijven relevant: de menselijke voedsel-/bevolkingscyclus is geen automatisch AI-model. Dit pakket bevat nog geen wijzigingsvoorstel.

## 9. Verificatie, grenzen en vervolgstap

[Controleer-Bevolkingskeuze.py](../PROEVEN/Controleer-Bevolkingskeuze.py) en [resultaat](BINAIR/population-scientists-choice-checks.json): **27/27**, bestaande engine/DLL-instructies met beide hashes gecontroleerd. Vier tileutility-, negen best-specialist- en vier science-per-pop-gettercontroles hebben geen externe callbacks vervangen. Vier minimumproductiecontroles gebruiken een PlaceACitizen-recorder; zes specialist/tile-keuzecontroles gebruiken Population+3c/+60 en World+b8/+bc-recorders. Dit bewijst aanroepkeuze en berekening, geen fysieke plaatsing, totale economie of gespeelde AI-beurt.

Essentiële open schakels:

1. CityData495250/495330/495460-modifiers en Player4c27f0-rationfactor tot een netto food/productie/sciencevoorbeeld; centrum-/automatische werkers en Deity-context expliciet meenemen.
2. Effectieve CityList-partitie/ordening en alle herverdelingsflags; sciencegewichtverandering en vijfbeurtenfasering kunnen op verschillende momenten doorwerken.
3. Volledige interne Population-/Worldplaatsing en PopDB-parser/defaults; specialistcache-refresh na gebouw/regering/bevolkingswisseling.
4. De dubbele minimumfood-aanroep, volledige happiness/crimebranches en de callergrenzen bij ontbrekende/volle tilelijst gezamenlijk controleren vóór een groeifactor als beleidsknop wordt behandeld.
5. Save/load van cached weights, counters, specialistcache en herverdelingsflags; er is in dit pakket geen runtime-saveproef uitgevoerd.

De afzonderlijke cash-to-scienceketen, rijksfractie en verdere government/wondercontext staan in [RIJKSBUDGET-EN-WETENSCHAP.md](RIJKSBUDGET-EN-WETENSCHAP.md). Deze rijksroute is onderscheiden van de directe scientistutility.

De volgende gerichte analyse is de gecombineerde citymodifier/consumptieketen met het afwijkende minimumfoodtarget, zodat productieomvang4 en groei-versus-scientist met echte cijfers kunnen worden beoordeeld. De brede fase A blijft open.
