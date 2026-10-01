# Projectdoelen: Civilization: Call to Power AI

## Doel en uitgangspunten

Verbeter de gameplay van de computergestuurde beschavingen in het eerste Civilization: Call to Power op Deity. De AI moet een sterk rijk opbouwen door snelle uitbreiding, gerichte ontwikkeling en onderzoek, en dit effectief benutten in oorlogvoering en handel.

- We spelen altijd op Deity.
- `CTP-og` is de originele referentie en blijft ongewijzigd.
- `CTP-AAIP` is een leermodel: de wijzigingen en README's helpen begrijpen welke instellingen welk gedrag sturen. AAIP is niet automatisch onze basis.
- Grafische verschillen vallen voorlopig buiten het onderzoek.
- De spelervaring van de gebruiker bepaalt het gewenste gedrag. Analyse van de spelregels onderbouwt dit en kan aanvullende verbeteringen opleveren.
- Eerste prioriteit is de AI op het spelniveau van de gebruiker brengen door diens vastgelegde strategie te realiseren. Houd mogelijke verbeteringen van die strategie apart als onderzoekshypotheses. De gebruiker staat expliciet open voor onderbouwde inzichten die ook zijn eigen gameplay verbeteren; neem die niet automatisch als wijziging van de afgesproken AI-strategie over.
- Extra AI-bonussen zijn geen uitgangspunt. Verbeter eerst beslissingen en gebruik van bestaande mogelijkheden.
- De gewenste uitkomsten hieronder zijn projectdoelen; technische uitvoerbaarheid en effect moeten nog worden onderzocht.

## Gewenst gedrag

### Gezamenlijke opening voor alle persoonlijkheden

Alle normale AI-beschavingen volgen eerst dezelfde strategische basis: snelle uitbreiding naar 25–30 steden, Religion → Theocracy en een overstap naar Theocracy zodra beschikbaar en zinvol, beperkte noodzakelijke legerproductie en gebouwen die uitbreiding ondersteunen. Een geschikte productiestad kan voor Labyrinth worden vrijgesteld. De barbarenroute behandelen we afzonderlijk.

De bestaande persoonlijkheid blijft ingesteld, maar mag deze gezamenlijke opening niet verdringen. Na de opening krijgen wetenschappelijke, militaire en andere voorkeuren meer invloed. Goede locatiekeuze, stadsspecialisatie en het vermijden van nutteloze gebouwen blijven voor iedereen gelden.

De gewenste overgang wordt gekoppeld aan de toestand van het rijk: doelomvang bereikt en Theocracy actief, niet aan een vaste beurt. De exacte grens binnen 25–30 wordt nog gekozen. Concrete dreiging, gebrek aan vestigingsruimte of ernstige gelukproblemen kunnen tijdelijk afwijkend gedrag noodzakelijk maken. Dit is geen automatische vrijbrief om de opening definitief te verlaten.

Onderzoek een gedeeld openingsprofiel via bestaande FLI/AIP-aansturing. Laat tijdelijke defensie-, oorlogs- en onderzoeksprofielen ermee samenwerken, zodat ze de afgesproken opening niet onbedoeld vervangen. Technische uitvoering en effect zijn nog niet bewezen.

### 1. Snelle vroege uitbreiding

Bereik in de early game min of meer zo snel mogelijk 25–30 steden. Groei is tijdens deze fase ondersteunend aan kolonistenproductie; pas daarna krijgt bevolkingsgroei de hoofdprioriteit.

Een goede productiestad kan worden vrijgesteld van kolonistenproductie om bijvoorbeeld Labyrinth te bouwen. Onderzoek de afweging tussen wonderopbrengst en gemiste uitbreiding. De exacte omschakeling binnen de bandbreedte 25–30 en noodzakelijke uitzonderingen worden nog uitgewerkt.

### 2. Beperkte vroege legerlast

Voorkom overmatige vroege eenhedenproductie en de bijbehorende druk op economie en onderzoek. Houd voldoende eenheden voor noodzakelijke veiligheid en nuttige taken. Gewenste aantallen en uitzonderingen bij dreiging worden nog bepaald.

### 3. Gericht onderzoek en regering

Gebruik Religion → Theocracy als gewenste vroege strategische richting. Theocracy is volgens de ervaring van de gebruiker overwegend de beste vroege regering voor alle strategieën. Werk de vereisten, onderzoeksvolgorde en timing van de overstap uit aan de hand van de spelregels.

### 4. Gerichte wonderkeuze

Labyrinth is voorlopig het enige vroege wonder dat het bouwen waard wordt geacht. Stel een expliciete lijst op van gewenste wonders, voorwaarden waaronder ze gebouwd worden, en wonders die doorgaans genegeerd moeten worden.

### 5. Stadsspecialisatie en bouwvolgordes

Ontwikkel twee hoofdtypen: production-steden en science-steden. Leg voor beide een afzonderlijke bouwvolgorde vast. Andere gebouwen worden in principe niet gebruikt, tenzij een expliciet vastgelegde omstandigheid ze rechtvaardigt.

Onderzoek eerst of de AI afzonderlijke stadstypen en bouwvolgordes kan aansturen. De precieze gebouwen zijn nog niet vastgesteld.

Een productiestad heeft ten minste drie bergtiles in haar stadsgebied en ligt bij voorkeur aan water voor zowel landeenheden als schepen. Plan de steden gezamenlijk om alle beschikbare bergen in een bergketen te kunnen bewerken. Vestigen op een berg is uitsluitend een uitzondering wanneer benodigde bergen anders echt niet toegankelijk zijn; zie [LOCATIESELECTIE.md](LOCATIESELECTIE.md).

De gewenste omvang van een productiestad is vier inwoners: drie laborers werken op bergen met mijnen of verbeterde productie-improvements, de vierde op één verbeterd voedselvakje (farm/fishery) dat de stad kan onderhouden. Vanaf grootte vier is verdere groei geen doel; productie wel. Voedselhaalbaarheid is onderdeel van de locatiekeuze en ontwikkeling.

Een science-stad heeft groeipotentieel en minimaal drie vakjes voor farms/fisheries of verbeterde varianten. Na bouw van een academy, publishing house of university kunnen inwoners die niet op voedsel-improvements werken scientists worden. Weeg verdere groei af tegen directe wetenschap, op basis van resterende spelduur, groeisnelheid en de opbrengst van extra scientists. Voorlopige vuistregel: drie voedselwerkers, een vierde bij grootte acht en een vijfde bij grootte tien; deze inzet mag na analyse worden geoptimaliseerd.

### 6. Monopoly-steden en handel

Herken en benut locaties met meerdere gelijke goods om waardevollere handelsroutes te ontwikkelen. Gebruik goudverhogende gebouwen gericht waar ze voor monopoly-steden effectief zijn. De relatie met production/science-specialisatie wordt nog uitgewerkt; een aanvullende monopoly-aanduiding is voorlopig een ontwerpvoorstel.

### 7. Berggebruik

Vestig steden naast geschikte bergen in plaats van automatisch op bergen. Verbeter de ontwikkeling en bevolkingsinzet van deze steden. Onderzoek de observatie dat dergelijke AI-steden vaak rond vier inwoners blijven steken; dit is nog geen vastgestelde enginebeperking.

Aanvulling: grootte vier is voor de gewenste productiestad juist de doelomvang. Beoordeel het succes op de inzet van drie verbeterde bergen en voldoende voedselonderhoud, niet op verdere bevolkingsgroei.

### 8. Laborers en micromanagement

Verbeter het gebruik van laborers, vooral in science-steden. Analyseer de precieze spelwerking en effectieve verdeling van bevolking. Voeg micromanagement toe wanneer het aantoonbaar voordeel biedt en technisch uitvoerbaar is.

### 9. Groei en granaries

Bouw normaal pas voedsel-improvements vanaf Ocean Faring (water) en Agricultural Revolution (advanced farms op land). De eerste generatie wordt overgeslagen. Een productiestad die Labyrinth bouwt mag hiervan afwijken. Stem locatiekeuze en groeiplanning af op voedsel dat vóór deze technologieën zonder improvements beschikbaar is.

Onderzoeksnotitie: deze timing is een voorlopig strategisch uitgangspunt, geen bewezen optimum. Mogelijk blijkt vroeg verbeteren in sommige omstandigheden wel rendabel. Onderzoek en rapporteer die gevallen afzonderlijk; de eerste implementatie richt zich op de afgesproken speelwijze van de gebruiker.

Stem vroege stadsontwikkeling en groeimomenten af op het moment waarop de granary voltooid is. Tijdens de uitbreiding beoordelen we dit vooral op de bijdrage aan snelle, herhaalbare kolonistenproductie. Na uitbreiding beoordelen we het op bevolkingsgroei.

### 10. Effectieve marineoorlogvoering

Verbeter vlootbouw, transport en aanvallen over zee. Gebruik AAIP als voorbeeld om van eerdere marineaanpassingen te leren. Meer schepen alleen is geen succescriterium: ze moeten bruikbare militaire operaties mogelijk maken.

## Zelfstandige strategische analyse

De afspraken voor locatiekeuze, vestigingsvolgorde, vroege wonderproductie en verzameling van gelijke goods staan in [LOCATIESELECTIE.md](LOCATIESELECTIE.md). Deze vormen onderdeel van de doelen voor uitbreiding, specialisatie en handel.

Goede stadslocaties gaan altijd vóór maximalisatie van oppervlakte. Eén vakje tussen steden is geen verplicht patroon; wijk hiervan af voor een monopoly of een goede production- of science-stad.

Analyseer de aanwezige spelregels voordat concrete bouwvolgordes en wijzigingen worden vastgesteld:

- Gebouwkosten, onderhoud, opbrengsten, voorwaarden en terugverdientijd.
- Kolonistenproductie, voedsel, groei en granary-timing.
- Onderzoekspaden, regeringen en timing van Theocracy.
- Stadslocaties, stadsafstand, bergen, goods en monopoly-handel.
- Laborers en bevolkingsinzet voor voedsel, productie en wetenschap.
- Wonders en hun opbrengst tegenover gemiste uitbreiding.
- Legeronderhoud, samenstelling, transport en invasies.
- Mogelijke microvoordelen rond groei- en productieomslagpunten.

Maak onderscheid tussen regels die direct uit bestanden blijken, berekende verwachtingen, ervaringen van de gebruiker of modmakers, en waargenomen resultaten. We hebben toegang tot de aanwezige bestanden, maar niet tot alle interne enginecode.

## Benchmark en succescriteria

Maak een vaste vroege Deity-save die iedere versie vanaf dezelfde omstandigheden speelt. Leg kaart, beschavingen, instellingen, testprocedure en versie vast. Controleer of gewijzigde AI-bestanden bij laden actief worden en hoe reproduceerbaar het vervolg is. Voeg indien nodig aanvullende saves toe voor marine of andere specifieke situaties.

| Meetmoment | Beoordeling |
| --- | --- |
| Turn 25 | Uitbreidingstempo, steden en kolonisten in voorbereiding |
| Turn 50 | Voortgang naar 25–30 steden en oorzaken van vertraging |
| Turn 100 | Omzetting van uitbreiding naar groei, productie en wetenschap |
| Doorlopend | Beurt waarop stad 25 en stad 30 worden gesticht |

Meet daarnaast bevolking, wetenschap, technologieën, overgang naar Theocracy, legeronderhoud, stadsverlies, gebouwen en wonders, handelsopbrengst, bevolkingsinzet en daadwerkelijke militaire operaties.

Concrete streefwaarden per meetmoment worden na een uitgangsmeting en met de gebruiker vastgelegd. Beoordeel resultaten per ontwikkelfase: snelle uitbreiding weegt vroeg zwaarder dan groei. Controleer neveneffecten, zoals kwetsbaarheid of economisch onbruikbare steden. Herhaal metingen wanneer toeval de uitkomst kan verklaren.

## Stappenplan

1. Leg projectdoelen vast en werk open strategische keuzes met de gebruiker uit.
2. Analyseer zelfstandig de spelregels en bepaal effectieve strategieën en microkeuzes.
3. Koppel gewenste beslissingen aan AI-bestanden en onderzoek technische uitvoerbaarheid.
4. Relateer AAIP-README-uitspraken aan werkelijke wijzigingen en mogelijke effecten.
5. Maak de benchmarksave, testprocedure en meetlat; voer uitgangsmetingen uit.
6. Kies onderbouwd de basis voor onze versie en maak een afzonderlijke werkversie.
7. Verbeter eerst uitbreiding, legerlast, Religion/Theocracy en groei/granary-timing met gerichte experimenten.
8. Werk specialisatie, wonders, monopoly-handel, berggebruik, laborers en marine verder uit.
9. Vergelijk iedere versie met de uitgangsmeting; behoud, herzie of draai wijzigingen terug op basis van resultaten.
10. Test gecombineerde verbeteringen over meerdere spelstadia en documenteer installatie, wijzigingen en bevindingen.

## Nog vast te leggen

- Concrete bouwvolgordes voor production- en science-steden, inclusief uitzonderingen.
- Volledige wonderlijst en bouwvoorwaarden.
- Precieze onderzoeksvolgorde en overheidsovergang.
- Optimale granary-timing en kolonistencyclus.
- Minimumverdediging en reactie op dreiging.
- Keuze tussen 25 en 30 steden en omstandigheden om eerder of later te stoppen.
- Benchmarkinstellingen en numerieke streefwaarden.

Er zijn voor deze vastlegging geen spelbestanden aangepast.
