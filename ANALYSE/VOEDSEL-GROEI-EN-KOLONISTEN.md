# Voedsel, groeivoorraad en kolonisten

Vervolg5 oktober16:44: de normale stadsbrede food/productiesom, centrumtelling, Government.PRODUCTION_COEF, floor-afgerond crime-foodverlies en inline Hunger/rantsoenconsumptie vóór groei zijn nu onderbouwd in [RANTSOENEN-EN-STADSOPBRENGSTEN.md](RANTSOENEN-EN-STADSOPBRENGSTEN.md). Tien extra enginecontroles volgen de som en echte updatebranch tot vóór494cf0; zij gebruiken expliciete externe inputmocks. Daardoor is de eerdere consumptievraag gedeeltelijk gesloten. Deity-groeicorrectie, gelukscontext en volledige ronde blijven open; eerdere oorspronkelijke secties hieronder zijn de historische basis.

Onderzoek fase A, 4 oktober 2026, aangevuld om 18:38. Verklaart groeivoorraad, granarywerking, recordmodifiers en singleplayer-settlerkosten, met bindings van de AI-getters aan de echte engine. Volledige consumptie, modifier-/beurtvolgorde en netwerkuitzonderingen blijven open. Geen spelstarts of gameplay-/binarywijzigingen.

**Belangrijk voor AI-strategie:** de onderzochte gewone singleplayerroute laat spelertype1 bij bevolking1 een settler voltooien. Met AIPopCheat=Yes slaat deze type1-route groeivoorraad-aftrek en bevolkingsverwijdering over. OG, AAIP en CTP-proef hebben alle drie deze bestaande profielinstelling. Dit is een aangetoond enginepad met synthetische branchecontroles en tekstconfiguratie, nog geen nieuwe benchmarkwaarneming. De menselijke settler-/granarycyclus mag dus niet zonder meer als AI-kostenmodel worden gebruikt; zie de laatste sectie.

## Wat nu onderbouwd is

Vervolg5 oktober16:52: de eerdere moeilijkheidsbranch is nu gebonden aan **HUMAN_FOOD_BONUS**, token317. [Token](BINAIR/economy-growth-human-food-token.txt), [parser en toepassing](BINAIR/economy-growth-difficulty-binding.txt). Recordparser457f70 schrijft op4585fc.. via ReadFloat naar+1d8. De zes records van512bytes worden op4586ea geparsed en met+200 doorgelopen; dezelfde tabelglobal a7dd54 wordt op407294 gezet. [Tabelinitialisatie](BINAIR/economy-growth-difficulty-table-initialization.txt), [recordladen](BINAIR/economy-growth-difficulty-record-loading.txt). De niet-passende engine-map is niet gebruikt.

De toepassing4950af..49511c vergelijkt de integer Player+4 na omzetting naar double met1.0. In de eerder gebonden gewone singleplayer-AI-context type1, met netwerkglobals nul, wordt de correctie overgeslagen. Andere typen krijgen `basis + trunc(basis * HUMAN_FOOD_BONUS)`; type1 kan via de expliciete netwerkpredicate ook in de correctietak komen. De volledige betekenis van die netwerkpredicate is hier niet benoemd. [Typebinding](BINAIR/food-growth-player-type-engine.txt) en de reeds bewezen AI/type1-context in de settlersectie blijven leidend.

[DiffDB.txt](../CTP-og/ctp_data/default/gamedata/DiffDB.txt) geeft HUMAN_FOOD_BONUS−0.4/−0.1/0/0/0/0 voor Chieftain..Deity. Deity heeft dus0, en de gewone singleplayer-AI gebruikt deze correctie sowieso niet. Hoog geluk wordt daarna afzonderlijk toegepast en verlaagt de drempel nog steeds. De vroegere generieke term 'moeilijkheidsbonus voor AI-groei' was te ruim.

[Controleer-Groeicontext.py](../PROEVEN/Controleer-Groeicontext.py) geeft [24/24 nieuwe controles](BINAIR/economy-growth-context-checks.json): telkens net onder/op de drempel, type0/1/2, synthetische bonus, netwerkpredicate en geluk/silo. De bestaande fixture is expliciet uitbreidbaar gemaakt; de originele geluksvergelijking4ac370 draait nu werkelijk met Const.VERY_HAPPY_THRESHOLD85. Poprecordopzoeken/-aanmaak en netwerkpredicate blijven mocks; de geïmporteerde ftol heeft een truncate-stub. De24 eerdere voorraadgevallen zijn na deze helperwijziging opnieuw gecontroleerd en blijven slagen. Geen netwerkspel, Deity-start of volledig gespeelde beurt getest.

Voor vier gewone inwoners, factor1 en175 basiscoëfficiënt: normale drempel700; bij geluk≥85 zonder silo350, met silo525. Na groei met silo blijft de opslag437 (trunc(5*175/2)), onafhankelijk van de lagere geluksdrempel. De oorspronkelijke AI-basisgetter levert700; hij voorspelt de geluksversnelling niet. Dit is nu onderbouwde context voor groei/scientistafwegingen, geen nieuw AI-beleid.

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
3. HUMAN_FOOD_BONUS conditioneel toepassen (4950af–49511c), zoals hierboven gebonden: gewone singleplayer-type1 slaat dit over; Deitywaarde0. Netwerkpredicate/-gevolgen zijn niet volledig benoemd.
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

Oorspronkelijk waren settlerkosten en bevolkingsverlies uitsluitend configuratiebewijs: Units.txt geeft 540 productie en BUILDING_REMOVES_A_POP. De vervolganalyse hieronder bindt nu de echte vlag en singleplayerkosten/-vrijstelling. Productie-/groeivolgorde en volledige overige effecten blijven open. Verwar het settlerquota niet met deze afzonderlijke bouwvoorwaarden.

Eerstvolgende onderzoekstap: het stadsunitrecordfactorveld en modifiers binden, daarna settler-voltooiing/bevolkingsverlies en de consumptie-/rationsformule. Gebruik deze engineketen voor analyse; nog geen nieuwe GUI-run nodig.

### Gevonden productie-/voltooiingsbranch (13:59)

De unitbranch in de queue begint op 48f7eb: ze vergelijkt de benodigde productie met de aangeleverde productievoorraad. Daarna bindt 48f8d2 het unitrecord van het queuehoofd. Bit **0x4000 van UnitRecord+0x40** leidt bij populatie kleiner dan 2 naar een extra contextcontrole (48f8df–48f948). Die controle kan Queue+0x130 zetten en de voltooiing verlaten; Player+4, een aanroepargument en netwerktoestand beïnvloeden de uitzonderingen. De betekenis van Player+4 en dit argument is nog niet gebonden: 'elke AI heeft altijd minimaal 2 nodig' zou dus te stellig zijn.

Bij toegestane voltooiing maakt 48f97a via 4b4ef0 een eenheid. Een volgende branch test opnieuw bit 0x4000, nu van het gemaakte unitrecord via 4da870. Als de eerdere context-/speciale globale checks niet overslaan, roept 48fa3e de routine 49f740 aan met integer(CITY_GROWTH_COEFFICIENT), gevolgd door 48fa47 → 496a50 met argument 1. **49f740 trekt die waarde van CityData+0xc af en begrenst het resultaat op nul**; het raakt CityData+8 niet in zijn eigen body. Bij originele coëfficiënt 175 is dit dus voorraad `max(0, voorraad − 175)`, zonder populatievermenigvuldiging of stadsunitfactor in deze aftrek. 496a50 kiest via 496750 een bevolkingsindex en geeft het bijbehorende record door aan 4cc6b0. De verwijderings-/geluks-/kaartgevolgen van die laatste routine zijn nog niet volledig gevolgd.

Bij de eerste analyse was de overeenkomst met BUILDING_REMOVES_A_POP een interpretatie. De vervolganalyse van 18:29 hieronder bindt de token nu daadwerkelijk aan bit0x4000. De contextuitzonderingen en volledige verwijderingsgevolgen blijven open. De populatiecontrole bij voltooiing is machinecodebewijs en verklaart waarom geen populatiecheck in de enqueue-route zichtbaar hoefde te zijn.

Bewijs: [unitrecord-aanroepers](BINAIR/food-growth-unit-record-callers.txt) (ruwe kandidaten), [queue-unitbranch](BINAIR/food-growth-queue-build-start.txt), [voorraadaftrek en selectieaanroep](BINAIR/food-growth-settler-pop-loss.txt), [bevolkingsselectie](BINAIR/food-growth-remove-pop-implementation.txt). Concrete hervatting: flagparser → Player+4/aanroepargument → echte verwijderingsroutine, daarna beurtvolgorde en productieoverschot. Geen nieuwe spelstart nodig.

### Parserbinding settlervlag en stadsunitfactor (18:29)

De werkelijke unitdatabase-initialisatie schrijft de constructoruitkomst 455300 naar global a7dd18 op 407192 en roept op 4071a3 parser46d9d0 aan. Deze laat via 454020 de recordarray aanmaken en leest via 46d390 de records. Recordparser46d390 roept op 46d902 de flagparser46b7f0 aan met het record als tweede argument. Dit pad komt uit de echte executable; adressen uit civctp.map zijn niet gebruikt.

De flagparser trekt10 van de geleverde token af en gebruikt eerst een byteselectietabel op46d108, daarna een adressentabel op46ce28. De exacte tokenstring BUILDING_REMOVES_A_POP heeft token235; de tabellen sturen deze naar case168, adres46c8f5. Daar zet `or ah,0x40` de vlag0x4000 in UnitRecord+40. Hiermee is de koppeling aan de eerder gevonden voltooiingsbranch **bewezen**. De oorspronkelijke settlerdefinitie heeft deze flag; haar bevolking-/voedselbranch is dus niet langer alleen een naaminterpretatie.

CITY_GROWTH_MODIFIER heeft token244 en gaat via case177 naar46ca1e. Daar schrijft de float-lezer5221f0 naar UnitRecord+2a0. De standaard is ook gebonden: arrayallocatie454020 geeft recordconstructor46dc20 door aan vectorconstructor725720 (454096–4540a7); deze zet op46df45/46df4b de double+2a0 op1.0. De originele UNIT_CITY heeft geen modifier en gebruikt dus1.0; SPACE_CITY en OCEAN_CITY geven expliciet0.5. Dit bevestigt de factorbinding in de echte groeidrempel; het maakt niet alle difficulty-/geluks-/slavenbranches of AI-schattingen gelijk.

Bewijs: [initialisatie](BINAIR/food-growth-unitdb-initialization.txt), [databaseparser](BINAIR/food-growth-unitdb-parser-route.txt), [recordparser](BINAIR/food-growth-unitdb-record-parser.txt), [flagaanroep](BINAIR/food-growth-unit-record-flags-call.txt), [switch](BINAIR/food-growth-unit-flag-switch.txt), [tabelwaarden](BINAIR/food-growth-unit-flag-table.json), [cases](BINAIR/food-growth-unit-flag-cases.txt), [tokens](BINAIR/food-growth-unit-flag-tokens.txt), [arrayconstructie](BINAIR/food-growth-unit-record-allocation.txt), [recordconstructor](BINAIR/food-growth-unit-record-constructor.txt). Dit is parser-/constructorbewijs, geen nieuwe spelproef of volledige geëmuleerde tekstparser.

Actueel vervolg: Player+4 en het queue-aanroepargument binden voor de bevolking<2-uitzonderingen; echte populationverwijdering volgen; difficulty-/consumptie-/beurtvolgorde vervolgen. De twee parsergaten hierboven zijn opgelost en hoeven niet opnieuw onderzocht te worden.

### Singleplayer: AI-settlers en bestaande AIPopCheat (18:38)

Player+4 is het spelertype: de passende DLL-functie Foreigner::GetPlayerType2000ce40 roept Player-slot270 aan, de gebonden tabel744660 wijst naar52b740, en die retourneert exact Player+4 als double. De naastgelegen slot274 op52b770 retourneert1 bij type1. Ook de echte SLIC-registratie van **IsHumanPlayer** is gevolgd: stringa22db8 → registratie53ec93 → object-vtable745630 → method552a40. De singleplayerbranch552ae5–552b1b geeft voor een bestaande speler false bij type1 en true bij andere typen. Dit onderbouwt de normale type1-AI-route; netwerktypen zijn hiermee niet volledig geclassificeerd.

De normale queuecalls497ef6 en498121 geven het laatste argument0 door aan BuildFront48f790. De aparte aanroep49eca1 geeft1. In de bevolking<2-controle bypasses dit argument1 de beperking. Bij argument0 en normale singleplayercontext mag type1 eveneens door, terwijl andere typen bij grootte1 Queue+130=1 krijgen en voltooiing verlaten. Grootte2 mag door. Dit is een voltooiingscontrole, geen harde enqueuebeperking.

Na eenheidcreatie leest de kostenbranch48f9be–48fa4c opnieuw het spelertype. Voor type1 in singleplayer gaat zij naar de aparte profielcheck. Global a7ddc8 is via408095–4080ad aan constructor4628f0 en profielinitialisatie463e50 gebonden. In deze objectregistratie koppelt463bc5–463bd5 exact sleutel912e40 **AIPopCheat** aan veld+854. Bij niet-nul slaat de AI de groeivoorraad-aftrek en bevolkingsverwijdering over. Bij uitgeschakelde AIPopCheat volgt de AI wel de kostenbranch; andere spelertypen volgen haar ook bij ingeschakelde cheat. OG, AAIP en proef bevatten op userprofile.txt:77 `AIPopCheat=Yes`. Er is geen nieuwe bonus ingesteld.

De daadwerkelijk gevolgde verwijderingsketen496a50 → 4cc6b0 → 4cc6d0 → 4dd0b0 → 4e5530 → 496c20 zoekt het gekozen pop-handle in de stadslijst en verlaagt op496caf CityData+58c met1. 4cc6d0 wist daarnaast waar van toepassing de kaartreferentie, roept4963f0 aan en verwijdert het poolrecord. De betekenis van die herberekeningsroutine en volledige geluk-/eventvolgorde blijven open. De geteste voorraadaftrek49f740 raakt +c, niet de afzonderlijke +8-buffer.

[Controleer-Settlerbevolking.py](../PROEVEN/Controleer-Settlerbevolking.py) voert de originele gate- en kostenbranches uit: **14/14 geslaagd**, [uitkomsten](BINAIR/food-growth-settler-pop-checks.json). Acht gevallen kruisen type0/1, grootte1/2 en argument0/1. Zes kostengevallen controleren AIPopCheat aan/uit, gewone versus type1-speler, lage voorraad en een unit zonder pop-lossflag. Type1 met cheat behoudt voorraad350 en doet geen verwijderingsaanvraag; zonder cheat wordt350→175 met één aanvraag. Andere typen doen die aanvraag ook met cheat. Voedselbuffer50 blijft in alle geteste branches50; voorraad10 wordt bij kosten0. Lookup en populationverwijdering zijn gemockt; de echte voorraadaftrek draait. De ftol-conversie krijgt een RAM-stub. Geen volledig unit-/turn-/netwerkexperiment of runtimeprofielmeting.

Bewijs: [AI-typegetter](BINAIR/food-growth-player-type-ai.txt), [engine-typegetters](BINAIR/food-growth-player-type-engine.txt), [IsHuman-registratie en kostenbranch](BINAIR/food-growth-human-registration-ai-exemption.txt), [IsHuman-body](BINAIR/food-growth-human-type-check.txt), [profielinitialisatie](BINAIR/food-growth-profile-initialization.txt), [profielconstructor](BINAIR/food-growth-profile-constructor.txt), [AIPopCheat-veld](BINAIR/food-growth-ai-pop-cheat-binding.txt), [queuecallers](BINAIR/food-growth-queue-build-callers.txt), [normale call](BINAIR/food-growth-queue-call-context.txt), [overige calls en CityData-removal](BINAIR/food-growth-completion-pop-city.txt), [populationwrapper](BINAIR/food-growth-pop-removal-wrapper.txt), [citywrapper](BINAIR/food-growth-pop-city-wrapper.txt).

**Vervolgimpact:** AI-expansie kan qua populatie veel goedkoper zijn dan menselijke expansie. Toch blijven productie, quota, geschikte vestigingsdoelen, bereikbaarheid en transport bepalend. Granary-/voedseltiming moet bij de AI worden beoordeeld vanuit groei/specialisatie, zonder onbewezen settler-popverlies in te rekenen. Voor fase C controleren dat de benchmark daadwerkelijk deze profiel-/spelertoestand gebruikt. Eerst nog de normale beurtvolgorde, consumptie, Deity-modifiers en resterende specialisatieketens volgen.
