# Technische uitvoerbaarheid van onze AI-strategie

## Resultaat en bewijsniveau

De aanwezige FLI/AIP-bestanden bieden bruikbare aansturing voor uitbreiding, onderzoek, regering, legerquota en algemene economische prioriteiten. Exacte stadsspecialisatie, individuele bevolkingsinzet en onze eigen locatiewaardering zijn daarin nog niet aangetoond.

De installatie bevat bovendien `ctp_program/ctp/civctp.map` en `ctp_program/ctp/dll/ai/robotcom.map`. Dit zijn linker-symbolenlijsten, geen broncode. Ze tonen functienamen en aanknopingspunten, niet de implementatie of volledige scriptargumenten. Daardoor kunnen we verder onderzoeken dan alleen tekstinstellingen, zonder te doen alsof de gehele engine aanpasbaar is.

Onderzoek uitgevoerd op `CTP-og`; geen engine, scripts of spelregels gewijzigd en geen runtimeproef gedaan.

## Uitvoerbaarheid per doel

| Doel | Aanwezige aanknopingspunten | Wat nog moet worden vastgesteld |
| --- | --- | --- |
| Uitbreidingsfase tot 25–30 | `inputs.fli`: num_cities; `aiploader.fli`: strategieovergangen; settlerquota en priorities in AIPs; `no_settle.aip` schakelt settle goals uit | Exacte gekozen grens, onderweg zijnde settlers, interactie met oorlog/geluk en laadvolgorde |
| Vroeg Religion/Theocracy | Advancements_List in persoonlijkheids-AIPs en overrides zoals citywall_science.aip | Gedrag bij al bekende technologie, prioriteit van alle later geladen lijsten |
| Theocracy als regering | `set_govern.fli`, I_want_this_gov_THEOCRACY in `outputs.fli` | Selectie en overstaptiming in engine; conflicterende voorkeuren |
| Minder vroege units | AIP units_per_city en lijstprioriteiten; num_city_defenders; military readiness | Werkelijke veiligheid, enginebetekenis van quotas en afwijkende oorlogsmodes |
| Wonderselectie | Wonder_List en wonder-effectgewichten | Betrouwbaar uitsluiten versus alleen lager waarderen, concurrentie met andere lijsten |
| Eén Labyrinth-stad | SLIC-symbolen AddWonderToBuildList, ClearBuildQueue; interne city-build utilities | Scriptsyntax, selectie van die stad, AI die de queue weer verandert |
| Eigen queues per stadstype | SLIC-symbolen AddBuildingToBuildList, AddUnitToBuildList, KillBuildingFromBuildList, IsBuildingInBuildList; ClearBuildQueue wordt daadwerkelijk in tutorial gebruikt | Argumenten, AI-spelerondersteuning, events, behoud van voortgang en persistentie |
| Minimaal drie bergen herkennen | SLIC TerrainType wordt gebruikt in tutorial; stadlocatie is beschikbaar in scripts | Tiles in werkbaar stadsgebied enumereren, zichtbaarheid, stadsradius en overlap |
| Science-stad herkennen | Zelfde terreintoegang, gebouwcontrole via CityHasBuilding en city.population in testscripts | Voedsel-improvementgeschiktheid, technologie en groei per stad uitlezen |
| Locatiekeuze voor nieuwe steden | settler_packing, settle_value_coef, settle_patience, bid_settle_uscale; engine-symbolen InsertBestSettleGoal/InsertSettleGoals | Exacte interne score en mogelijkheid om kandidaatlocaties direct aan de AI te geven |
| Monopolywaardering | GoodCount in tutorial; symbolen GoodCountTotal/CityCollectingGood; interne handelsplanner | Local/imported telling, alle goods van rijk, routebestemmingen en koppeling aan vestigingsscore |
| Vier inwoners, drie bergwerkers | Algemene pop_food/pop_production-gewichten; CityAgent PlaceAllPop intern | Geen direct scriptcommando voor precieze tiletoewijzing gevonden |
| Scientists op vaste voorwaarden | pop_science, min_food_factor; CalcScientistUtility intern | Geen aangetoonde per-stad override van aantallen scientists |
| Voedsel-improvements uitstellen | inst_food/make_farm beïnvloeden wens; engine GetBestFarmType | Technologiekennis in FLI, blokkeren van niveau 1 zonder spelregels voor mens te wijzigen, uitzondering per Labyrinth-stad |

## Wat FLI/AIP wel en niet bewijst

FLI-inputs voor de gemeenschappelijke beurtregels zijn vooral rijkgegevens: stadsantal, oorlog, totale populatie, economie en kaart. Een nieuw verzonnen `input city_mountain_count` toevoegen betekent niet dat de engine die waarde levert.

De AIP-structuren bevatten lijstnamen, prioriteiten, aantallen eenheden per stad, gebouwprioriteiten en technologieën. Er is in `Aipdef.h` geen stad-ID of stadstypevoorwaarde in deze structuren. `units_per_city` is dus geen bewijs dat we individuele steden rollen kunnen geven.

De engine heeft wel per-stadberekeningen: CityAgent bouwutilities en CityAgentPop. Gedeelde gewichten kunnen daardoor verschillend uitpakken per stad. Dat is iets anders dan onze expliciete production/science-classificatie kunnen programmeren.

Het verlagen van settler_packing kan dichter vestigen bevorderen, maar voert niet automatisch de regel 'goede locatie vóór afstand' of monopolywaardering in. Terrein-ENV_SCORE is ook geen aangetoonde complete settler-score en mag niet blind als zo'n score worden gewijzigd.

## Scripts als mogelijke uitbreiding

Bewezen lokale voorbeelden:

- `tutorial_triggers.slc` gebruikt `ClearBuildQueue(city)`.
- Hetzelfde bestand gebruikt `TerrainType(location)` en `GoodCount(city, GoodType(...))`.
- `test.slc` noemt `city.population`, `city.location`, `city.building` en andere event/contextwaarden.

Symbolen tonen bovendien queuefuncties, CityHasBuilding, SetResearching, SetGovernment en goodsfuncties. De contextwaarden uit tutorial/tests zijn niet automatisch voor ieder moment of willekeurige stad beschikbaar. Functienamen alleen bewijzen evenmin argumenten of gedrag.

Een kleine scriptproef voor één AI-stad kan vaststellen of we een bestaande bouwqueue kunnen sturen en controleren. We moeten daarbij het natuurlijke bouwproces behouden: FinishBuilding, gratis technologie of gratis bevolking toevoegen zijn geen geschikte implementatie van slimmer spelen. ClearBuildQueue niet iedere beurt uitvoeren; dat kan lopende productie verstoren. Onderzoek eerst zachte aanpassing van queues en de 25%-bouwswitchpenalty in Const.txt.

## Bevolking en locatiekeuze: belangrijkste onzekerheden

`civctp.map` toont C3Population::SetCityPopInCity en SetCityPopType, en getters voor tile food/production. Dat zijn engine/AI-interfacefuncties, geen aangetoonde SLIC-functies. We kunnen ze niet zomaar vanuit een script aanroepen.

`robotcom.map` toont PlacePopMinimumFood, PlacePopMinimumProduction, PlaceAllPop en CalcScientistUtility. Dit bevestigt interne aansturing, maar de benodigde algoritmes staan in de DLL. Voor exacte eigen logica kan aanvullend interfaceonderzoek of een engine/AI-uitbreiding nodig zijn. Er is nog geen werkende vervangende DLL of compatibele broncode gevonden.

Hetzelfde geldt voor InsertBestSettleGoal en handelsfuncties zoals FindUnconnectedGoods, CollectCityBids en ConnectGoods. Monopolygedrag is daarom niet als 'onmogelijk' aangemerkt, maar ook nog niet als uitvoerbaar met tekstinstellingen.

## Opvallende bestaande details

- `inputs.fli` koppelt yes_diety aan chieftain_test in plaats van diety_test. Dit lijkt een fout, maar het runtime-effect en gebruik moeten eerst worden onderzocht. Nieuwe Deity-regels niet blind daarop bouwen.
- farm_count is een fuzzy set op input count, geen telling van gebouwde farms. De naam mag niet als betekenis worden aangenomen.
- De onderzoeksprioriteiten kunnen door citywall_science.aip worden vervangen. Een persoonlijkheidslijst aanpassen alleen is onvoldoende.
- `no_settle.aip` zet MAX_EVAL_SETTLE_GOALS en MAX_EXEC_SETTLE_GOALS op nul. Controleer opnieuw inschakelen en latere overrides bij faseovergangen.

## Aanbevolen vervolgstap

De afzonderlijke installatie `CTP-proef` en de eerste queueproef zijn inmiddels voorbereid. Zie [PROEVEN/QUEUE-PROEF.md](PROEVEN/QUEUE-PROEF.md) voor uitvoering en de nog open runtime-resultaten. De CTP-I-functieargumenten zijn gecontroleerd tegen de ontwikkelaarsdocumentatie; de proef is nog niet in het spel uitgevoerd.

Eerst een kleine proefomgeving met één AI-stad en een vroege save, in een afzonderlijke werkversie. Test:

1. Worden gewijzigde FLI/AIP-regels bij laden van de save actief?
2. Kan een SLIC-script een AI-stad identificeren, terrein/goods lezen en een normale bouwqueue wijzigen zonder gratis opbrengsten?
3. Blijft die queue bestaan na de normale AI-beurt?
4. Zijn population/tiletoewijzing en toekomstige settlerbestemmingen op enige manier scriptbaar?

De queueproef is de eerste concrete proef omdat ze bepaalt of onze twee stadstypen uitvoerbaar zijn zonder globale benadering. Onderzoek vóór schrijven de exacte lokale scriptdocumentatie of functieargumenten. Leg ontbrekende toegang expliciet vast; vul die niet in met CTP-II-API's, want dit project betreft CTP I.

Daarna kunnen we een eerste uitbreidingsversie maken met bevestigde FLI/AIP-aanpassingen en eventuele werkende stadsscripts. Die versie kan al een deel van de doelen realiseren, maar mag niet als volledige implementatie van onze stadsspecialisatie worden gepresenteerd zolang de kernmogelijkheden onbewezen zijn.
