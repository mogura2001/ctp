# Locatiekeuze en volgorde van vestigen

Dit document legt de gewenste strategie van de gebruiker vast. De genoemde spelmechanieken zijn hier uitgangspunten uit diens spelervaring; technische herkenning, exacte opbrengsten en aansturing door de AI moeten nog worden onderzocht. Er zijn geen spelbestanden aangepast.

## Vastgelegde uitgangspunten

**Timing van voedsel-improvements:** bouw normaal geen eerste generatie voedsel-improvements. Begin op water pas met de voedselverbetering beschikbaar via Ocean Faring, en op land met advanced farms via Agricultural Revolution. Een productiestad die Labyrinth moet bouwen mag hiervan afwijken wanneer een eerdere voedsel-improvement de gewenste ontwikkeling en productie ondersteunt. Tot die technologieën beoordelen we locaties op hun onverbeterde voedselvoorziening. De benaming van de water-improvement moet aan de interface worden getoetst; de technologie is leidend.

**Goede locaties gaan altijd vóór maximalisatie van oppervlakte.** Eén vakje tussen steden is geen verplicht raster: wijk daarvan af wanneer dat een monopoly-stad of een betere production- of science-stad mogelijk maakt. Forceer geen minderwaardige locatie om een vaste afstand of gelijkmatige gebiedsdekking te behouden. Afstand wordt beoordeeld op concrete gevolgen, zoals reistijd en bruikbare middelen; zij mag locatiekwaliteit niet automatisch overrulen.

1. Steden kunnen volgens de gebruiker één vakje van elkaar worden gesticht. Een locatie is waardevol zolang de stad uiteindelijk een production- of science-functie kan vervullen. Een algemene afstands- of overlapstraf mag zulke locaties niet automatisch uitsluiten. De precieze afstandsmaat en terreinbenutting worden technisch gecontroleerd.
2. Een goede late-game-locatie hoeft geen goede vroege uitbreidingslocatie te zijn. Bij weinig beschikbare productie kan later vestigen beter zijn. Houd de locatie als toekomstige mogelijkheid in beeld.
3. Zoek, indien beschikbaar, zo snel mogelijk een geschikte wonderproductiestad, bijvoorbeeld voor Labyrinth. Bergen hebben een sterke voorkeur; bos of jungle met rivier zijn alternatieven. Plaats de stad naast geschikte bergen, overeenkomstig het projectdoel voor berggebruik. Deze stad kan van settlers worden vrijgesteld.
4. Een monopoly-stad is volgens de gebruiker bijna altijd rendabel. De locatie wordt extra belangrijk wanneer dezelfde good al elders in het AI-territorium beschikbaar is.
5. De gewenste handelsopzet is een monopoly-stad plus vier extra exemplaren van dezelfde good, passend bij maximaal vier handelsroutes. Als een natuurlijke monopoly-stad ontbreekt, verzamel dan vijf exemplaren van dezelfde good en stuur ze naar één plek. De exacte import/exportrichting, telling van lokale exemplaren en monopolyformule moeten worden gecontroleerd voordat dit in code wordt vertaald.

## Beslismodel voor de AI

De afspraak om eerste generatie voedsel-improvements normaal over te slaan is voorlopig. Eerst brengen we de AI op het spelniveau van de gebruiker met diens strategie. Onderzoek mag later aantonen dat vroege voedselverbeteringen in specifieke gevallen rendabel zijn; zulke inzichten worden afzonderlijk onderbouwd en besproken voordat ze onderdeel van de AI-strategie worden.

### Definitie en vestigingsregels voor een productiestad

- Een productiestad heeft ten minste drie bergtiles in haar stadsgebied. Drie bergen vormen het criterium; meer bergen blijven waardevol.
- Bij voorkeur ligt de stad aan water, zodat zij zowel landeenheden als schepen kan bouwen. De precieze voorwaarden voor scheepsbouw worden technisch gecontroleerd.
- Plan steden rond een bergketen zo dat uiteindelijk alle beschikbare bergen kunnen worden bewerkt. Beoordeel daarvoor de combinatie van stadslocaties, niet uitsluitend de beste individuele locatie.
- Vestig bij voorkeur naast bergen. Vestigen op een berg is alleen toegestaan als bepaalde benodigde bergen anders echt niet bereikbaar zijn vanuit geschikte stadslocaties en hun productie nodig is.
- De voorkeur voor water mag het doel om benodigde bergen te benutten niet automatisch blokkeren. De afweging tussen locaties volgt de regel dat locatiekwaliteit vóór maximale gebiedsdekking gaat.

Deze definitie vervangt het eerdere algemenere gebruik van 'productiestad'. Bos/jungle met rivier blijft een alternatief voor een geschikte wonderproductielocatie, maar voldoet zonder drie bergtiles niet aan de vastgelegde definitie van een productiestad.

### Ontwikkeling en bevolkingsinzet van een productiestad

- De gewenste omvang is vier inwoners. Groei tot vier ondersteunt de ontwikkeling; vanaf vier is verdere groei geen doel en krijgt productie de prioriteit.
- Bij vier inwoners werken drie laborers op drie bergtiles. Bouw daar mijnen of de beschikbare verbeterde productie-improvements.
- De vierde inwoner werkt op één verbeterd voedselvakje, zoals een farm of fishery, dat voldoende voedsel levert voor het onderhoud van de stad.
- Beoordeel de combinatie van drie bergen en een geschikt voedselvakje bij locatiekeuze en ontwikkelplanning. Controleer technisch hoeveel voedsel nodig is onder de gekozen regering en rations-instellingen, en welke improvement daarvoor beschikbaar moet zijn.
- Houd voedselonderhoud in stand; de productiedoelstelling mag niet tot verhongering leiden. Wanneer één voedselvakje nog onvoldoende levert, is de gewenste eindinzet nog niet haalbaar en moet de ontwikkeling daarop worden afgestemd.
- Het streven om alle bergen van een bergketen te benutten geldt voor het gezamenlijke stadsplan. Deze standaardstad werkt op grootte vier drie bergen; overige bergen moeten via passende aanvullende stadslocaties worden benut.

Beoordeel een kandidaatlocatie op twee afzonderlijke vragen:

- Welke functie en economische waarde kan deze stad uiteindelijk hebben?
- Wat levert vestigen op deze plek nu op, vergeleken met de andere beschikbare locaties?

Een lage vroege productie verlaagt dus vooral de urgentie van een toekomstige science-stad. De stad mag daardoor niet permanent als waardeloos worden behandeld.

Production en science blijven de twee hoofdtypen. Wonderproductie is een taak voor een geschikte productiestad. Monopoly is een aanvullende handelsfunctie; de relatie met de hoofdtypen en bouwvolgordes werken we verder uit.

| Aspect | Te beoordelen kenmerken | Gewenste invloed |
| --- | --- | --- |
| Vroege uitbreiding | Beschikbaar voedsel en productie, tijd tot een volgende settler, reistijd | Geef tijdens de uitbreidingsfase voorrang aan locaties die verdere uitbreiding versnellen |
| Productiestad | Bruikbare bergen; bos/jungle met rivier; voedsel om terrein te benutten | Herken productiepotentieel en benodigde ontwikkeling |
| Wonderproductie | Sterke productie, ontwikkeltijd, al aanwezige geschikte wonderstad | Geef vroeg extra prioriteit aan een geschikte locatie; bergen hebben sterke voorkeur |
| Science-stad | Mogelijke bevolking en effectieve laborers-inzet; kosten om de stad te ontwikkelen | Waardeer toekomstige wetenschap, maar stel productiearme locaties zo nodig uit |
| Monopoly | Meerdere gelijke lokale goods, dezelfde goods elders in eigen gebied, haalbare handelsverbindingen | Geef hoge prioriteit aan het completeren van een bruikbare handelsopzet |
| Dichte vestiging | Uiteindelijke functie en werkelijk bruikbare middelen | Sta korte stadsafstand toe; beoordeel overlap op gevolgen, niet uitsluitend op afstand |
| Uitvoerbaarheid | Veiligheid, bereikbaarheid en wettelijke vestigingsvoorwaarden | Voorkom dat een aantrekkelijke score een onbruikbare bestemming oplevert |

Gebruik voorlopig geen verzonnen numerieke gewichten. Eerst moeten we weten welke kenmerken de engine beschikbaar stelt en hoe de huidige score werkt. Daarna kunnen we waarderingen kalibreren met de benchmark.

## Definitie en ontwikkeling van een science-stad

- Een science-stad heeft groeipotentieel en ten minste drie vakjes waarop voedsel-improvements kunnen worden gebouwd: farms, fisheries of hun verbeterde varianten.
- Ontwikkel deze voedselvakjes om de bevolking te onderhouden en groei mogelijk te maken. Beoordeel bij locatiekeuze ook de haalbare voedselopbrengst en ontwikkeltijd.
- Zodra de stad een academy, publishing house of university heeft gebouwd, kunnen laborers die niet op de voedsel-improvements werken in het labor-scherm naar scientists worden omgezet. De exacte unlockvoorwaarden en werking van deze gebouwen worden aan de spelbestanden getoetst; dit is nog geen vastgelegde volledige bouwvolgorde en vereist niet automatisch alle drie gebouwen.
- Bij verdere bevolkingsgroei weegt de AI de resterende spelduur, groeisnelheid en opbrengst van een extra scientist af tegen inzet van een extra voedselwerker.
- De voorlopige vuistregel is drie voedselwerkers, bij grootte acht een vierde en bij grootte tien een vijfde. Dit zijn startregels voor onderzoek en optimalisatie, geen harde grenzen.
- Controleer voor extra voedselwerkers of geschikte voedselvakjes beschikbaar zijn of ontwikkeld kunnen worden. De definitie van drie mogelijke voedselvakjes is een minimum, geen maximum.
- Waar groei nog loont, kan tijdelijk meer voedselinzet beter zijn; waar de opbrengst van extra bevolking te laat komt, kan directe wetenschap beter zijn. Onderbouw deze keuze met de spelregels en benchmarkresultaten voordat numerieke drempels worden aangepast.

## Dynamische prioriteit

- Tijdens de race naar 25–30 steden is verdere uitbreiding een hoofdcriterium.
- Vroege wonderproductie en sterke monopoly-kansen kunnen voorrang krijgen op een gewone uitbreidingslocatie. Hun onderlinge rangorde is nog niet numeriek bepaald.
- Een al geschikte wonderstad vermindert de noodzaak om een tweede locatie speciaal daarvoor vroeg te vestigen.
- De waarde van een good hangt mede af van de voorraad in het hele rijk en de geplande bestemming. Beoordeel locaties dus niet uitsluitend afzonderlijk.
- Houd rekening met kolonisten die al onderweg zijn naar een locatie of good, zodat meerdere plannen niet onbedoeld dezelfde behoefte proberen te vervullen, indien technisch mogelijk.
- Na de uitbreidingsfase komen uitgestelde, waardevolle science- en productielocaties opnieuw aan bod. Of dit uitbreiding voorbij 30 steden rechtvaardigt, blijft een open strategische keuze.

## Technisch onderzoek

1. Zoek bestaande settlerwaarderingen voor terrein, voedsel, productie, goods, afstand en gevaar.
2. Bepaal of meerdere gelijke goods en de voorraad in andere steden zichtbaar zijn voor de beslisregels.
3. Onderzoek hoe berg-, bos-, jungle- en rivieropbrengsten worden toegepast en wanneer een stad ze kan benutten.
4. Controleer de handelsroutegrens en de precieze werking van verzamelen, importeren, exporteren en monopoly-opbrengst.
5. Onderzoek afzonderlijke stadstaken, uitgestelde locaties en toewijzing van kolonisten. Maak onderscheid tussen beschikbare instellingen en gewenste nieuwe logica.

## Benchmark

Voeg kandidaatlocaties toe die de afwegingen zichtbaar maken: dichte maar nuttige vestiging, productiearme toekomstige science-locatie, berglocatie voor wonderproductie, rivierbos/jungle als alternatief, en goods die een bestaande verzameling aanvullen.

Registreer per gestichte stad de beurt, locatie, beschikbare middelen, verwachte functie en daadwerkelijke productie/wetenschap/handel. Meet ook wanneer een geschikte wonderstad beschikbaar is, hoeveel dezelfde goods zijn aangesloten en welke uitgestelde locaties later worden gekozen. Hoge stadsaantallen alleen bewijzen geen goede locatiekeuze.
