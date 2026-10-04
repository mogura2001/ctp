# Onderzoeksplan: packing en beschikbare vestigingslocaties

Doel: verklaren of geschikte, wettelijk toegestane nabijgelegen locaties door de AI worden uitgesloten, en bepalen of een packing-wijziging vanaf dezelfde benchmarksave eerlijk getest kan worden. Eerst alleen-lezen codeonderzoek; nog geen gameplaywijziging of nieuwe run.

## Besluit: eerst analyse, voorlopig geen nieuwe spelstarts

De gebruiker heeft bevestigd dat we eerst analyseren voordat opnieuw spellen worden gestart. We onderzoeken een contextafhankelijke opening: vrije ruimte, klein eiland en gedeeld land met buren. De hypothese voor Welsh is dat een hoge primary-settlervraag transportschepen verdringt. Dit is geen vastgestelde harde quota-verbodsregel; we moeten onderscheiden tussen bouwbaarheid, gewenste scheepsaantallen en verdringing door hogere prioriteit.

## 1. Bestaande beslisketen voor ruimte, buren en transport

Eerste analyse uitgevoerd: [RUIMTE-BUREN-TRANSPORT.md](RUIMTE-BUREN-TRANSPORT.md). De eenheidsquotaformule is vastgesteld; marine-omschakeling, continentoverlap en lokale defensie zijn gevolgd. Exacte enginebindings en actieve instellingen in de saves blijven deels onbekend. Stap 2 is inmiddels eveneens uitgevoerd; volgende analyse is het resterende deel van stap 3, zonder nieuwe spelstarts.

Onderzoek eerst ComputeLandContinentFull, continenttellingen, de naval/supernaval-aanvraag, de eenheidsvraag en Choose_Unit_From_List/Add_Supplemental_Unit_Build_Goals. Volg daarnaast beschikbare inputs voor gedeeld land, nabijheid, vrede/oorlog en dreiging naar de bestaande defensieprofielen. Bepaal welke signalen werkelijk aanwezig en bruikbaar zijn; verzin geen FLI-inputs.

Leg per situatie vast welk profiel en welke bouwvraag wordt aangevraagd, hoe settlers en transport concurreren, en welke voorwaarden kandidaten bereikbaar maken. Controleer of de AI op gebrek aan ruimte reageert voordat settlers zich ophopen, en of buren ook in vrede defensie activeren. Het resultaat is een onderbouwde beslisboom met drie situaties: vrije landuitbreiding, uitbreiding via transport en verdedigde uitbreiding op gedeeld land. Combinaties blijven mogelijk.

Gebruik Welsh als casus voor transportverdringing en de bestaande T60-resultaten als waarnemingen. Een afwezige Trireme bewijst niet dat bouwen verboden was. Onderzoek gewenste aantallen, bouwbaarheid/technologie, primary-concurrentie en marineloads afzonderlijk. Geen nieuwe run tijdens deze stap.

## 2. Levensduur van het locatiemasker

Uitgevoerd: [VESTIGINGSMASKER.md](VESTIGINGSMASKER.md). De statische land-/ruimtemaskers beginnen met enen, worden bij stadsregistratie gewist en worden volledig opgeslagen/teruggelezen. De planner gebruikt kopieën; een packing-wijziging herstelt daardoor niet vanzelf oude uitsluitingen. Buitenlandse stadsregistratie gebruikt vast radius 3; stadsvernietiging heropent vast radius 2. T60 is geen schone start voor een packing-vergelijking. De bestaande T0-save is een kandidaat, onder voorwaarde dat packing actief is vóór relevante stadsregistraties en de begintoestand wordt gecontroleerd.

Volg AiMap-constructors, Serialize, RegisterMyAddCity, FlattenStaticSettle en UnflattenSettle in de overeenkomende AI-DLL. Stel vast wanneer het statische masker wordt opgebouwd, of het in de save wordt bewaard en wanneer uitgesloten locaties terugkomen. Controleer ook stadsverlies en gewijzigde packing. Resultaat: aantoonbare keten voor verse start versus save laden, met adressen en onbekende branches expliciet benoemd.

## 3. Interne radius naar zichtbare vakjes

Nieuwe prioriteit van de gebruiker: eerst de kwaliteitsformule begrijpen. De echte engine-route is inmiddels gevonden via de World-GUID en functietabel, onafhankelijk van civctp.map. Zie [LOCATIEKWALITEIT.md](LOCATIEKWALITEIT.md): de score gebruikt twintig omgevingstiles plus centrum, voedselgroepen, productie/goud en een vermenigvuldigende goods-aanwezigheidsbonus. De velden zijn via de parser bevestigd en de gecorrigeerde formule is in 68 voorbeelden tegen machinecode gecontroleerd. Concrete voorbeelden tonen ontbrekende monopolywaardering en sterke afhankelijkheid van ruwe voedselgroepen. Herberekening en het aanvullende centrumflag blijven open. Dit onderzoek gaat nu vóór de verdere zichtbare-afstandsanalyse.

Het gesloten interne vierkant en de wrapbewerking zijn inmiddels vastgelegd in VESTIGINGSMASKER.md. De precieze omzetting naar zichtbare isometrische vakjes blijft te onderzoeken; een geïmporteerde __ftol-stub bewijst zelfstandig geen afronding van 3.7. Gebruik interne radii niet als wettelijke stadsafstand.

Vervolg op locatiekwaliteit uitgevoerd: [SCORECACHE-EN-INGREEPPUNTEN.md](SCORECACHE-EN-INGREEPPUNTEN.md). Scorewaarden worden in de save-archiefroute bewaard en teruggelezen; twee emulatorcontroles bevestigen exact herstel zonder herberekening in die route. De nieuwe beoordeling moet al bij de kandidaatordening worden gebruikt en daarna samenhangend in doelen en prioriteiten terugkomen. De World-interface kan echte good-identiteiten leveren; de volledige eigen voorraad-/reserveringstelling is nog niet gebonden.

Volgende gerichte analyse: terrein-/improvementkenmerken en eigen good-tellingen koppelen aan de bestaande interfaces. Werk daarmee uit welke ontwerpvereisten FLI/AIP kunnen sturen en welke aanvullende logica vóór kandidaatselectie vereisen. Volledige herberekeningscondities en centrumflag blijven open. Voor een latere scoreproef moet aantoonbaar zijn dat nieuwe waarden worden gebruikt; hergebruik van een save alleen bewijst dit niet.

Volg AiMap::Wrap en de gebruikte coördinatenconversies, integerconversie van packing en de grenzen van FlattenCanSettle. Maak op papier een klein raster met een bestaande stad en markeer welke coördinaten bij enkele packing-waarden worden gewist. Scheid de AI-uitsluiting van de wettelijke stichtingsregels. Gebruik geen onbevestigde engine-adressen uit civctp.map. Resultaat: concrete voorbeelden van toegestane en uitgesloten nabijgelegen locaties; geen handmatige stadstichting in de benchmark.

## 4. Verklaringen scheiden

Aanvullend beleidsdoel: de settlervoorraad moet aansluiten op de resterende uitvoerbare vestigingsbehoefte. Meer dan de standaard primary-vraag van twee bij ruimte, afremmen/pauzeren bij voldoende aanwezige en in productie zijnde settlers of gebrek aan bereikbare bestemmingen, en stoppen met extra openingsproductie bij de gekozen grens binnen 25–30 steden. Transportgebrek vraagt eerst om transport, niet om steeds meer settlers. Een tijdelijke pauze moet herbeoordeeld kunnen worden. Zoek aantoonbare bestaande signalen voor kandidaten, bereikbaarheid en toegewezen settlers; continentvolheid alleen bewijst geen gebrek aan bruikbare locaties. Geen quotaformule of nieuwe FLI-input verzinnen voordat de binding is onderzocht.

Beoordeel met de codebevindingen en bestaande T60-opnamen drie hypotheses apart: geen kandidaat door packing, kandidaat maar onbereikbaar zonder schip, en vestigingsdoelen uitgeschakeld. Gebruik Welsh/Cubans voor ophoping en Egyptians/Mongols als vergelijking. Een losse settler is niet automatisch een inactieve settler. Benoem welke runtimegegevens nog ontbreken voordat een oorzaak wordt toegewezen.

## 5. Pas na de analyse een gecontroleerde proef ontwerpen

Kies op basis van de bevindingen één afzonderlijke wijziging (bijvoorbeeld packing of transportaansturing); neem packing niet vooraf als oorzaak aan. Houd de overige factoren gelijk. Gebruik dezelfde oorspronkelijke T0-save en herstart per variant. Alleen als de maskeranalyse bewijst dat het masker correct wordt herberekend, is een latere bestaande save geschikt voor een korte diagnoseproef. Anders moet de locatiemaskerbeperking eerst worden opgelost; geen schijnvergelijking van nieuw beleid met een oud masker. Dit is een ontwerpstap voor later; voorlopig geen spelstarts of proefuitvoering.

Meet op dezelfde beurten (bijvoorbeeld T25/T60): steden, bevolking, bestaande settlers en transportschepen. Controleer voor de opgehoopte settlers hun positie en, voor zover uitleesbaar, opdracht en bereikbare kandidaatzones. Succes is extra bruikbare steden en minder ophoping, zonder dat goede locaties onnodig worden verdrongen. Transport blijft een afzonderlijk vervolgexperiment als packing de ophoping niet verklaart. De gebruiker kan de doorloop opnieuw uitvoeren om GUI- en tokenkosten te beperken.

## Vast te leggen uitkomst

Een radiusdiagram, een onderbouwde uitspraak over savecompatibiliteit en een concrete kleine proefconfiguratie. Geen automatische quota- of transportwijziging tijdens dit onderzoek. Volg de les over gerichte DLL-analyse uit AGENTS.md: eerst de betreffende implementatie begrijpen, daarna gericht gedrag meten.
