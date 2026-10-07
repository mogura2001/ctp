# Dreiging en stadsverdediging

Fase A, 5 oktober 2026. Klein alleen-lezen pakket; geen spelstarts/game-/binarywijzigingen. Hergebruik [lokale dreiging en gedeeld land](RUIMTE-BUREN-TRANSPORT.md), [bouwconcurrentie](BOUWDOELEN-EN-QUEUE.md) en [transportuitvoering](TRANSPORT-EN-VESTIGINGSACTIES.md). Marine-invasie en volledige militaire scheduler blijven buiten dit pakket.

## Kernresultaat

De AI kan al vóór formele oorlog op buitenlandse dreiging reageren. De helpers IsAtHotWar en IsAtColdWar lezen geen formele oorlogsenum: ze toetsen een som van regardvelden. Lokale CityAgent-dreiging gebruikt hot óf cold als filter. De strategische dreigingskaart betrekt ook overige buitenlanders met een houdingafhankelijke factor. Stadsdefensiebehoefte leest die kaart; de twee dreigingsroutes zijn dus niet hetzelfde.

Bewijs komt uit de originele robotcom.dll, SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, imagebase20000000, timestamp37b894e7, passende robotcom.map. Een symboolnaam alleen is niet gebruikt als bewijs voor formele oorlog. [Diplomatie/defensiedoelcode](BINAIR/threat-defense-goals-diplomacy.txt), [kaartcode](BINAIR/threat-defense-strategic-map.txt).

## 1. Regard en zichtbare buitenlandse legers

IsAtHotWar2000c690 geeft bij eindige waarden true wanneer Foreigner+68 plus+70 hoogstens20 is. IsAtColdWar2000c6b0 geeft true bij hoogstens40. GetFZRegard2000cc20 levert onder meer deze velden via zijn outputs. De complete opbouw van de regardcomponenten, treaty-/oorlogevents en diplomatieke feedback blijft apart onderzoek; deze grenspredicates bewijzen geen declaratie van oorlog. [Regardgetter en smoothing](BINAIR/threat-defense-regard-smoothing.txt), [exacte predicates](BINAIR/threat-defense-goals-diplomacy.txt).

FSUpdateThreat20037ea0 vraagt zichtbare buitenlanders op via AiMap::GetVisibleForeigners en werkt stadsdreiging bij. CityAgent::UpdateThreat2001cd70 slaat de lokale buitenlandse bijdragen over wanneer beide hot/coldpredicates false zijn. Voor de overgebleven legers gebruikt het positie, afstand en beweging; ForeignAgent::CalcThreat20022630 draagt de legerwaardering bij. Zichtbaarheid, cached ForeignAgent en actuele engine-eenheid zijn afzonderlijke schakels: volledige observatie-/geheugenverversing is hier niet gereconstrueerd. [Bestaande lokale callchain](BINAIR/ruimte-stadsdreiging.txt).

CityAgent houdt bovendien een huidige bijdrage+78 en gedempte waarde+80 bij. Bij een daling berekent2001cf59–2001cf78: decay maal huidige bijdrage plus(1−decay) maal vorige gedempte waarde. Bij een niet-dalende bijdrage wordt de huidige waarde direct overgenomen. fz_city_threat_decay beïnvloedt dus de afbouw, niet eenvoudig iedere stijging. [Lokale decaycode](BINAIR/ruimte-stadsdreiging.txt).

## 2. Strategische dreigingskaart

Update_Threats20081860 initialiseert de kaartpass en doorloopt buitenlandse city-/armyverzamelingen. Voor een hot-buitenlander is de factor1. Voor overige buitenlanders is de factor `(101−min(Foreigner+68,100))*0.01`; ook bij regard100 blijft deze factor0.01. Dit is geen hard hot-only-filter. Bijdragen van steden en legers worden op kaartcellen opgeteld, met afzonderlijke laag-/spacebranches. De volledige krachtformule van iedere ForeignCity/ForeignAgent is hier niet geëmuleerd. [Weging en invoerlussen](BINAIR/threat-defense-strategic-map.txt).

Relax_Threats20084e80 verspreidt kaartdreiging naar naburige cellen. Bronwaarden hoogstens25 slaan de gevolgde verspreidingsbranch over. Relax_Two_Cells20085520 verwerkt gewicht/afstand met de bestaande doelcel en zet te lage resultaten weer op0; dit vormt ruimtelijke invloed, geen bewezen tijdsdecay van dezelfde vorm als CityAgent. De volledige volgorde, iteratie en effectieve constanten blijven open. [Relaxpass](BINAIR/threat-defense-strategic-map.txt), [twee-celfunctie](BINAIR/threat-defense-regard-smoothing.txt).

Get_Threat20083b10 leest voor gewone lagen de kaartcel na integerdeling van x/y door de kaartgrofheid op Strategic_Map+0. Voor laag1 leest het de afzonderlijke scalar+6c. CityAgent::GetDefenseRequired2001d0f0 converteert zijn stadspositie en roept precies deze getter aan. De defensiebehoefte is dus niet simpelweg de lokale CityAgent+80-waarde. [Kaartlookup](BINAIR/threat-defense-strategic-map.txt), [stadsbehoefte](BINAIR/ruimte-defensie-bouwbaarheid.txt).

## 3. Van stadsbehoefte naar defensiedoel en toewijzing

Setup_Defense_Goal2001d6c0 maakt een GoalDefense en registreert het bij de planner, met een statuscheck tegen dupliceren. De complete gebeurtenis-/beginbeurtvoorwaarden voor iedere stad blijven open. GoalDefense::Compute_Needed_Troop_Flow2004ef50 vraagt GetDefenseRequired op, vermenigvuldigt dat met een via AddMinMaxRandomRange verkregen matchingfactor en schrijft de verdediging naar beide benodigde Squad_Strength-objecten. De minimumunitcount komt uit Planner+268 (ingebedde effectieve AIP+248) en wordt op minstens1 geklemd. [Doelopbouw](BINAIR/ruimte-defensie-bouwbaarheid.txt), [troop-flow](BINAIR/threat-defense-goals-diplomacy.txt).

De bestaande AIP-parser bindt num_city_defenders aan dit scalargedeelte; profieloverrides kunnen de effectieve waarde wijzigen. OG default heeft1, AAIP default2. min_defense_matching_force_ratio staat in beide op1.2; het is niet zelfstandig de volledige uiteindelijke forcefactor, want fuzzy minimum/maximum en randomrange worden ook gelezen. [Scalarbinding](BINAIR/aip-load-scalar-bindings.txt), [OG default](../CTP-og/ctp_data/default/aidata/AIPs/default.aip), [AAIP default](../CTP-AAIP/ctp_data/default/aidata/AIPs/default.aip), [samengestelde AIP-toestand](AIP-LAADWERKING.md).

Compute_Raw_Priority2004ed40 combineert de generieke legerdoelscore met bevolkingswaarde, nabije vijandafstand en een recent-captured bijdrage; de basis komt uit het effectieve profiel. ActionBidToDefend20013e50 geeft een legerbod op dit doel. De algemene planner/scheduler moet dit met andere doelen matchen. Dit pakket bewijst de gebruikte functies en troopbehoefte, niet de optimale keuze van elke unit of scheduler-gelijkstand. Wanneer een cityagent voor een legerdoel bouwt, bestaat de eerder gebonden generieke Find_Best_Utility_Agent_We_Can_Build→PretestContructUnit→EnqueueArmy-route; dit is te onderscheiden van vaste Defend_Troops-lijstquota. [Defensiebod en score](BINAIR/threat-defense-goals-diplomacy.txt), [bestaande leger-/bouwuitvoering](BINAIR/transport-settle-actions-execution-trigger.txt), [bouwacceptatie](BOUWDOELEN-EN-QUEUE.md).

ArrivedAtTask2004ee40 heeft een transport-subtask2; bij gewone aankomst behandelt het stadsaanwezigheid en kan ResetDefenseStrength2001d170 bijwerken. Het feitelijk slagen van alle verplaatsings-/groeporders is niet bewezen. De volledige terugkoppeling van stadsbezetting naar voldane defensiebehoefte en nieuwe bouwvraag blijft open. [Aankomst en behoefte](BINAIR/threat-defense-goals-diplomacy.txt).

## 4. Gedeeld continent en AAIP-les

LandContinentShared is al als overlapmaat aangetoond, maar geen algemene early-game-FLI-omschakeling bij een AI-buur is bewezen. Wel bestaan de regardfilters, strategische gewogen buitenlandse invloed, lokale nabijheid en defensiedoelen. De bestaande vroege citywall/survival-profielregels kijken bovendien naar nabijheid van de menselijke hoofdstad en krachtsverhoudingen zonder in die specifieke branch een formele-oorlogvoorwaarde. Dat mag niet worden veralgemeniseerd naar iedere AI-buur. [Eerder onderbouwde profiel- en burenvoorwaarden](RUIMTE-BUREN-TRANSPORT.md).

AAIP verhoogt in default num_city_defenders van1 naar2. Dat kan de minimumunitvraag binnen deze bestaande defensieketen verhogen; het bewijst geen nieuwe dreigingswaarneming of algemene escortestrategie. Omdat effectieve profielen samengesteld zijn, is de defaulttekst niet automatisch de waarde op elke beurt. Een grotere defensievraag concurreert tevens met uitbreiding en andere unitdoelen. [AAIP default](../CTP-AAIP/ctp_data/default/aidata/AIPs/default.aip), [lijstconcurrentie](BOUWDOELEN-EN-QUEUE.md).

## 5. Controle en technische grenzen

De helper heeft **16/16 geslaagde controles** op oorspronkelijke instructies, zonder externe callbacks: twaalf hot/cold-drempelchecks rondom20/40, één somcomponentcheck en drie kaartlookups met synthetische kaartdata. Geen formele treatycontext, volledige kaartupdate, scheduler of spelbeurt is geëmuleerd. [Helper](../PROEVEN/Controleer-Dreiging.py), [resultaten](BINAIR/threat-defense-controls.json).

Open blijven de volledige observatie-/geheugencyclus, regardopbouw en treatyreacties, volledige kracht-/relaxformule, alle defensiedoel-aanmaakvoorwaarden, concrete squad/unit-selectie en voldaan-/bouwterugkoppeling. Marine-invasie en escorte van settlers blijven afzonderlijke onderdelen. Dit rapport verklaart de huidige aansluitingen en het verschil tussen lokale en strategische dreiging; het sluit brede fase A niet af.
