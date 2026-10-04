# Voedsel, groeivoorraad en kolonisten

Onderzoek fase A, 4 oktober 2026. Dit eerste pakket verklaart de groeivoorraad en granarywerking en bindt de bestaande AI-getters aan de echte engine. De voedselconsumptieformule en alle gevolgen van settlerbouw zijn nog niet volledig gevolgd. Geen spelstarts of gameplay-/binarywijzigingen.

## Wat nu onderbouwd is

De granary heeft twee verschillende voorraden/effecten. De numerieke waarde `IMPROVEMENT_FLAG_SILO 50` begrenst een afzonderlijke buffer; zij is niet de formule 'bewaar 50% van het oude groeivoedsel'. Na bevolkingsgroei met een silo schrijft de engine juist de helft van de **nieuwe basisgroeidrempel** naar de groeivoorraad. Zonder silo trekt zij de gebruikte oude drempel van de voorraad af, zodat het overschot overblijft.

De gewone AI leest het voedseloverschot, opgebouwde groeivoedsel en een groeidrempel elke beurt uit. Die laatste getter geeft een eenvoudigere basisdrempel dan de uiteindelijke groeicontrole: hij verwerkt in de gevolgde route geen stadsunitfactor, moeilijkheidsaanpassing of bonus bij hoog stadsgeluk. Dit verschil moet worden meegenomen voordat een AI-groeischatting als exact aantal beurten wordt gebruikt.

24 offlinecontroles van de originele positieve groeicode slagen, met synthetische steden en nagebootste externe opzoek-/bevolkingsaanroepen. Dat bewijst de betreffende voorraadberekening, geen volledig gespeelde beurt of betere AI.

## Binding en bewijs

De AI-map past bij robotcom.dll: imagebase 20000000, timestamp 37b894e7, SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`.

De onderzochte executable heeft imagebase 400000, timestamp 37d6f702, SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`. civctp.map past niet en is niet gebruikt voor engineadressen. De route is gevolgd via de GUIDs uit de geldige AI-map, echte QueryInterface-code, vtables, getters en aanroepers.

[Analyseer-Engine-Interfaces.py](../PROEVEN/Analyseer-Engine-Interfaces.py) zoekt zulke COM-bindings alleen-lezen. Kandidaten moeten inhoudelijk worden gecontroleerd; een nabije verwijzing naar een GUID is op zichzelf onvoldoende. De eerste ruwe Player-scan bevatte ook een ongeldige voorafgaande tabelkandidaat op 744634. Alleen **744660** heeft de gecontroleerde Player-QueryInterface/AddRef/Release-keten; de helper filtert inmiddels kandidaten waarvan die drie pointers niet naar uitvoerbare code wijzen.

| Route | Gecontroleerde adressen |
| --- | --- |
| GameState-GUID | AI 200896b8 → engine 744ea8; QueryInterface 524bb0; vtable 744420 |
| Player-GUID | AI 200896c8 → engine 744f48; QueryInterface 5271c0; vtable 744660 |
| GameState → BuildingDB | slot 0x34 → 525ff0 → objectveld +0x1c; constructie 524d87 → 5239b0 schrijft vtable 744318 |
| GameState → Population | slot 0x48 → 526010 → +0x24; constructie 524db1 → 52c0d0 schrijft vtable 744948 |
| GameState → Government | slot 0x2c → 525fd0 → +0x2c; constructie 524e05 → 5261c0 schrijft vtable 7444f0 |

Bronnen: [AI-initialisatie](BINAIR/food-growth-ai-init.txt), [GameState-binding](BINAIR/food-growth-gamestate-binding.txt), [constructie](BINAIR/food-growth-gamestate-construct.txt), [interfaceconstructors](BINAIR/food-growth-interface-constructors.txt), [Player-binding](BINAIR/food-growth-player-binding.txt) en [volledige getterbranches](BINAIR/food-growth-player-getters.txt).

## Wat CityAgent iedere beurt ontvangt

`CityAgent::BeginTurn` (2001bfb0) leest via AiMain+0x2c de Player-interface:

| Player-slot | Engine | AI-veld | Betekenis in de gevolgde keten |
| --- | --- | --- | --- |
| 0x78 | 527b70 → 4c8690 → 4dda00 → 4e7470 | CityAgent+0x44 | CityData+0x58, een double die als integer wordt uitgelezen; net voedsel na consumptie |
| 0x130 | 527b90 | CityAgent+0x4c | CityData+0xc, opgebouwde groeivoorraad |
| 0x134 | 527c40 | CityAgent+0x50 | Basisdrempel: populatie minus burgers met PopDB-flag 0x20, maal integer(ConstRecord+0x328) |

De drie waarden worden door `GetFoodGrowth` (2001c310) weer als doubles aangeboden. `CityGrowth::EstimateGrowthTime` (2005ab30) controleert of de eerste positief is en geeft de drempel en het verschil drempel-minus-voorraad aan `InsertTime`. De constructor van GrowTime (2005a470) bewaart deze argumenten; hij deelt ze daar niet door het voedseloverschot. De verdere gebruiks-/normalisatieroute is nog open. Een functienaam met 'Time' is dus onvoldoende bewijs dat deze opgeslagen getallen al groeibeurten zijn.

Het field ConstRecord+0x328 is expliciet aan **CITY_GROWTH_COEFFICIENT** gekoppeld: token 604 (0x25c), parser 4533f8–453405 schrijft via ReadFloat naar +0x328. De originele configuratie geeft 175. Bewijs: [coëfficiëntvelden](BINAIR/food-growth-coefficient-fields.txt), [AI-beginturn](BINAIR/food-growth-city-beginturn.txt), [AI-groeifuncties](BINAIR/food-growth-ai.txt), [GrowTime](BINAIR/food-growth-ai-growtime.txt).

## Silo: bufferwaarde en aanwezigheid

Token **IMPROVEMENT_FLAG_SILO** is 455 (0x1c7). Parser 45ec3d–45ed30 koppelt hem aan het integer van ImprovementRecord+0x40. `GetSilo` (45cd80), aangeroepen door de gebonden BuildingDB-slot 0x50 op 523e1a en door de stadscode, neemt de gebouwbits en levert twee outputs: silo aanwezig en de hoogste silo-waarde onder de aanwezige gebouwen. Meerdere silo-effecten worden daar niet opgeteld.

In de positieve voedselroute telt 494ff2–495010 het integer voedseloverschot bij CityData+8 op en begrenst die buffer op de geleverde silo-waarde. De andere voorraad CityData+0xc krijgt hetzelfde overschot zonder die 50-cap. Code rond 496f19–496f7d controleert de silo en verbruikt de afzonderlijke buffer bij een voedselgerelateerde bevolkingscontrole. De volledige relatie met tekorten en de beurtvolgorde moet nog worden uitgeschreven; deze analyse claimt niet dat alle tekortregels al verklaard zijn.

Bewijs: [silo-parser](BINAIR/food-growth-silo-parser.txt), [veld](BINAIR/food-growth-silo-field.txt), [GetSilo](BINAIR/food-growth-get-silo.txt), [BuildingDB](BINAIR/food-growth-building-population.txt), [consumenten](BINAIR/food-growth-silo-consumers.txt).

## Positieve groei en voorraad na groei

De originele enginecode 494fde–49522c doet, voor een positief voedseloverschot:

1. Integer voedseloverschot toevoegen aan beide voorraden; de afzonderlijke buffer begrenzen op de silo-waarde.
2. Een basisdrempel berekenen uit de niet als slaaf gemarkeerde populatie en `integer(CITY_GROWTH_COEFFICIENT × factor uit het stadsunitrecord)` (495068–4950ac). De unitrecord-getter is via 4da870 gebonden; de semantische parserbinding van de factor +0x2a0 is nog niet voltooid.
3. Eventuele moeilijkheids-/spelcontextaanpassing toepassen (4950af–49511c). Die branch en de bijbehorende configuratiebinding zijn nog open.
4. Bij hoog stadsgeluk de drempel tot 3/4 verlagen met silo, of tot 1/2 zonder silo (49511e–495149). De voorwaarde 4ac370 levert waar wanneer de gelukswaarde ten minste ConstRecord+0x16c is. Parser 4533db–4533e8 bindt dit veld aan token 603, VERY_HAPPY_THRESHOLD; origineel 85. De eerdere benaming 'ongeluksvoorwaarde' was onjuist. Zie [parser en vergelijking](BINAIR/food-growth-happy-build-binding.txt) en [token](BINAIR/food-growth-happy-token.txt).
5. Bij voldoende groeivoorraad eenmaal de bevolkingsaanmaak aanroepen op 49516d. Deze route bevat geen loop om meerdere burgers met een groot overschot in dezelfde aanroep te maken.
6. Zonder silo de gebruikte drempel aftrekken (495224–495229). Met silo de populatie na groei opnieuw tellen, de nieuwe basisdrempel berekenen en de voorraad op de helft daarvan zetten (495187–495222). De moeilijkheidsaanpassing en bonus bij hoog geluk worden in die laatste berekening niet herhaald.

Voor de offline onderzochte gewone factor 1 en zonder modifiers geeft dit bijvoorbeeld:

| Situatie: bevolking 2, voorraad 340, overschot 10 | Zonder silo | Met silo |
| --- | --- | --- |
| Voorraad vóór groeicontrole | 350 | 350 |
| Bevolking na aanmaak | 3 | 3 |
| Groeivoorraad na groei | 0 | 262 (integer 525/2) |

Een bestaand overschot verandert de uitkomst met silo niet in 'oud overschot + halve drempel': deze branch schrijft de nieuwe halve basisdrempel rechtstreeks. Dit detail kan het nut van de bouwtiming beïnvloeden en hoort in de latere kosten-batenanalyse.

[Controleer-Groeivoorraad.py](../PROEVEN/Controleer-Groeivoorraad.py) voert de originele instructies uit met Unicorn. De 24 gevallen controleren drie begingroottes, wel/geen silo en een voorraad vlak onder/op/boven de drempel of voldoende voor meerdere groeistappen. Alle controles slagen; [resultaten](BINAIR/food-growth-checks.json). Externe databases, conditie voor hoog geluk (hier uitgeschakeld) en bevolkingsaanmaak worden nagebootst; de import _ftol krijgt een x87-conversie met afkappen. Het script claimt geen volledige engine-/populatie-emulatie, slaven-/modifiertest of gameplaywaarneming. De volledige gelezen code staat in [EatFood-bewijs](BINAIR/food-growth-eat-food.txt).

## Gevolg voor het project en vervolg

De granary moet worden beoordeeld op de volgende daadwerkelijke bevolkingsgroei, resterende bouwtijd, latere settlers en gewenste stadstaak. Een vaste algemene prioriteit alleen verklaart haar marginale nut niet. Dit is een analysevereiste, nog geen toegepast bouwbeleid of vervanging van de gebruikersstrategie.

`UtilityBlgSilo` (2001ffc0) bestaat, maar een directe xref-scan vindt geen aanroeper. De gevolgde `ActionBidBuild(GoalBuilding)` (20020540) haalt alle effecten op en roept `UtilityBlgCapitol` aan; het bestaan van alle benoemde utility-functies bewijst dus niet dat de gewone bouwketen ze gebruikt. Het werkelijke AIP-/gebouwselectiepad moet afzonderlijk gevolgd worden. Bewijs: [building-bid](BINAIR/food-growth-building-bid.txt), [xref](BINAIR/food-growth-ai-refs.txt).

### Toelating en enqueue van een eenheid

De gewone AI gebruikt twee afzonderlijke Player-slots: `CanBuildUnit` (2001f330) roept slot 0x238 → 52b360 aan; `EnqueueArmy` (2001c3d0) gebruikt slot 0x50 → 527850 met bouwklasse 1. De engine-toelatingsroute is 52b360 → 4ddc90 → 4e7650 → CityData 49d2b0. De enqueue-route is 527850 → 4c81d0 → 4dc220 → 4e22a0 → CityData 498970. Daar wordt 49d2b0 opnieuw gecontroleerd, vervolgens gaan klasse 1, type en UnitRecord+0x50 naar de queue op CityData+0x450 via 491290.

49d2b0 volgt tech-/recordflags, regeringsmasker en locatie-/eenheidvoorwaarden. In de volledig gelezen 49d2b0–49d69a is geen directe stadsbevolkingsvergelijking zichtbaar. De queue-toelating 4910c0 roept dezelfde CanBuildUnit-keten opnieuw aan; de afzonderlijke stringvergelijking in klasse 1 toont een melding en gaat daarna verder. Dit bewijst nog niet dat een settler bij bevolking 1 kan worden **voltooid**: de afhandeling tijdens productie en voltooiing is een ander pad. Ook de resterende AI-eigen checks in 2001f330 moeten worden geduid.

Bewijs: [AI-aanvragen](BINAIR/food-growth-unit-build-ai.txt), [Player-slots](BINAIR/food-growth-build-player.txt), [doorsturen](BINAIR/food-growth-build-unit-route.txt), [UnitData-binding](BINAIR/food-growth-happy-build-binding.txt), [CityData-toelating en enqueue](BINAIR/food-growth-city-build-eligibility.txt), [toelatingstaart en queue](BINAIR/food-growth-city-build-tail.txt), [queuecontrole](BINAIR/food-growth-queue-admission.txt).

Settlerkosten en bevolkingsverlies zijn vooralsnog configuratiebewijs: Units.txt geeft de settler 540 productie en BUILDING_REMOVES_A_POP. Nog te volgen: afhandeling van dit flag bij voltooiing, minimale stadsbevolking bij productie/voltooiing, terugslag op beide voedselvoorraden, productieoverschot en de volgorde ten opzichte van groei. Verwar het settlerquota niet met deze afzonderlijke bouwvoorwaarden.

Eerstvolgende onderzoekstap: het stadsunitrecordfactorveld en modifiers binden, daarna settler-voltooiing/bevolkingsverlies en de consumptie-/rationsformule. Gebruik deze engineketen voor analyse; nog geen nieuwe GUI-run nodig.

### Gevonden productie-/voltooiingsbranch (13:59)

De unitbranch in de queue begint op 48f7eb: ze vergelijkt de benodigde productie met de aangeleverde productievoorraad. Daarna bindt 48f8d2 het unitrecord van het queuehoofd. Bit **0x4000 van UnitRecord+0x40** leidt bij populatie kleiner dan 2 naar een extra contextcontrole (48f8df–48f948). Die controle kan Queue+0x130 zetten en de voltooiing verlaten; Player+4, een aanroepargument en netwerktoestand beïnvloeden de uitzonderingen. De betekenis van Player+4 en dit argument is nog niet gebonden: 'elke AI heeft altijd minimaal 2 nodig' zou dus te stellig zijn.

Bij toegestane voltooiing maakt 48f97a via 4b4ef0 een eenheid. Een volgende branch test opnieuw bit 0x4000, nu van het gemaakte unitrecord via 4da870. Als de eerdere context-/speciale globale checks niet overslaan, roept 48fa3e de routine 49f740 aan met integer(CITY_GROWTH_COEFFICIENT), gevolgd door 48fa47 → 496a50 met argument 1. **49f740 trekt die waarde van CityData+0xc af en begrenst het resultaat op nul**; het raakt CityData+8 niet in zijn eigen body. Bij originele coëfficiënt 175 is dit dus voorraad `max(0, voorraad − 175)`, zonder populatievermenigvuldiging of stadsunitfactor in deze aftrek. 496a50 kiest via 496750 een bevolkingsindex en geeft het bijbehorende record door aan 4cc6b0. De verwijderings-/geluks-/kaartgevolgen van die laatste routine zijn nog niet volledig gevolgd.

De overeenkomst met BUILDING_REMOVES_A_POP is een **interpretatie**, nog geen afgeronde parserbinding. Bind de flagtoken aan bit 0x4000 voordat deze conditionele branch als volledige settlerregel wordt gebruikt. De populatiecontrole bij voltooiing is wel machinecodebewijs en verklaart waarom geen populatiecheck in de enqueue-route zichtbaar hoefde te zijn.

Bewijs: [unitrecord-aanroepers](BINAIR/food-growth-unit-record-callers.txt) (ruwe kandidaten), [queue-unitbranch](BINAIR/food-growth-queue-build-start.txt), [voorraadaftrek en selectieaanroep](BINAIR/food-growth-settler-pop-loss.txt), [bevolkingsselectie](BINAIR/food-growth-remove-pop-implementation.txt). Concrete hervatting: flagparser → Player+4/aanroepargument → echte verwijderingsroutine, daarna beurtvolgorde en productieoverschot. Geen nieuwe spelstart nodig.
