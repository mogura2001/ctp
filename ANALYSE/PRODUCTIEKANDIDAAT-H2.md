# H2 — beschikbare bergwerkplekken vóór stichting

7 oktober 2026, 22:03 Europe/Amsterdam. Afgebakende analyse voor de eerstvolgende production-feature. Geen spelstart, liveproces, gameplay-/binarywijziging, classifierimplementatie of nieuwe emulatie. H1-M blijft een afzonderlijk uitvoeringspakket.

## Antwoord

**Zonder city-ID kan de AI minstens drie momenteel beschikbare bergwerkplekken herkennen.** Gebruik de bestaande **World+ac → 00534510** met de actuele civ en kandidaatcentrum, en vraag voor de teruggegeven unieke posities via **World+a8 → 005342e0** de terreinindex op. Tel indices **8,20,22**. World+ac verwijdert al bezette laborerposities en bestaande stadscentra; drie aanwezige bergen waarvan één momenteel door een andere stad wordt gewerkt voldoen dus niet aan deze beschikbare-werkplekkentest.

Dit levert een ontwerpbaar querypredicate voor **minstens drie verschillende, momenteel open bergvakjes in de bestaande stadsfootprint**. Het garandeert niet dat een later gestichte stad daar daadwerkelijk drie inwoners plaatst, dat de plekken vrij blijven of dat alle toekomstige bezettings-/herverdelingskeuzes optimaal zijn. Die grens is expliciet onderdeel van het contract; voedsel, aanleg en volledige productionclassificatie volgen afzonderlijk.

## Bewijs en dekking van de beslisketen

| Schakel | Concrete punten / aangetoond gedrag | Betekenis voor H2 |
| --- | --- | --- |
| Beschaving en centrum | AiMain+20=civ; AiMain+30=World. FindOpenTiles 20020e30 pusht CityAgent+210 als **positiepointer**, niet als city-ID | Kandidaatcentrum kan dezelfde positieinput leveren; geen CityAgent of fictieve cityhandle aanmaken |
| Toegankelijke centrumquery | 534579–534593 roept World+28 aan met World/centrum; false schrijft count=0 | Bij afgewezen/ongedekte centrumquery geen productiegeschiktheid claimen |
| Footprint | World+ac→534510→502da0 onderzoekt twintig omliggende posities zonder centrum, in bestaande buur-/wraplogica | Gebruik de interface; geen eigen vierkante-afstandsregel of schermcoördinaten |
| Huidige beschikbaarheid | 511030, argument1: Cell+18 populatiehandle blokkeert; 5154e0/Cell+14 cityhandle blokkeert; conditionele army-ownerchecks | Bezette bergen en bestaande bergstadscentra tellen niet als beschikbare werkplekken |
| Terreintype | World+a8→5342e0→514b70; canonical indices8/20/22 | Alle drie bergvarianten tellen, hills9/19/21 niet |
| Gelijktijdige capaciteit | Unieke coördinaten; ieder geteld vakje heeft geen bestaande laborer/city | Eén berg nooit tweemaal als werkplek tellen, ook niet op kleine gewrapte kaarten |
| Daadwerkelijke latere plaatsing | Population+60→52c6e0→4c9fe0→510d00→5005d0 vereist echte stad/inwoner | H2 is capaciteit op het meetmoment, geen vooraf geslaagde plaatsingsactie |

Hergebruikt: [IMPROVEMENTCONSTRUCTIE-EN-STADSGEBIED](IMPROVEMENTCONSTRUCTIE-EN-STADSGEBIED.md), [BEVOLKING-EN-SCIENTISTS](BEVOLKING-EN-SCIENTISTS.md), [TERREIN-EN-IMPROVEMENTS](TERREIN-EN-IMPROVEMENTS.md), [GOODS-EN-HANDELSROUTES](GOODS-EN-HANDELSROUTES.md). Goods worden pas bij daadwerkelijk bewerken lokale voorraad; H2 telt bergcapaciteit, geen reeds gerealiseerde opbrengst.

Binaire identiteit hergebruikt en in gerichte dumps gecontroleerd: robotcom.dll/map timestamp37b894e7, imagebase20000000, SHA2563025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44. Engine timestamp37d6f702, imagebase00400000, SHA256b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79. Civctp.map blijft afgewezen als adresbron. Geen nieuwe AAIP-gameplayclaim.

## Interfacecontract zonder city-ID

De bewezen caller [FindOpenTiles](BINAIR/terrain-food-v2-ai-tile-input.txt) pusht op 20020e23–36 achtereenvolgens outputarray, countpointer, centrumpositiepointer, civ en World; daarna `call [vtable+ac]`. Conceptueel:

`World_open_tiles(World*, int32 civ, MapPointData* center, int32* count, MapPointData* positions)`

Bij callee-entry zijn dit ESP+4,+8,+0c,+10,+14. De wrapper heeft `ret 14h`; caller ruimt de vijf argumenten niet op. Gebruik **count als resultaat**; EAX is geen bewezen bool-/aantalcontract voor de volledige enumerator. Reserveer twintig **8-byte** positieobjecten, dus160bytes. Elk bevat signed16 x/y/z op +0/+2/+4, met twee paddingbytes. De engine schrijft output op `array + count*8` (534604–534614 en overeenkomstige loops). Count wordt door de wrapper op0 gezet; de caller mag het vooraf eveneens op0 zetten. Alleen indices0..count−1 lezen; ongeldige count buiten0..20 als fout behandelen.

De positiequery vereist geen bestaande stad: 534510 leest de centrumpositie, de opgegeven civ en de actuele World-grid. Er is geen CityData-lookup in deze enumerator. De CityAgent-caller haalt later via **Player+120** opbrengsten op met zijn city-ID; die tweede aanvraag hoort niet bij H2 en wordt voor een hypothetisch centrum niet uitgevoerd.

De voorafgaande **World+28** is onafhankelijk gebonden aan **00533580** in [gericht bewijs](BINAIR/production-candidate-h2-position-and-cell.txt). Die zet het centrum via503f00 om en roept via World+0c de Player-route **4bbd50 → Player+1304 → 4ebdf0** aan; zie [centrumgate](BINAIR/production-candidate-h2-center-gate-and-placement.txt). Dit is een spelergebonden centrumgate, geen city-ID-vereiste. De exacte semantische naam van4ebdf0 wordt hier niet verder gereconstrueerd: de bestaande gate ongewijzigd gebruiken is genoeg. Een count0 bewijst dus niet uitsluitend gebrek aan bergen; de gate kan de gehele query afwijzen. Desgewenst eerst World+28 met hetzelfde centrum opvragen en **niet beoordeelbaar** onderscheiden van een geldige lijst met te weinig bergen.

World+a8 neemt World, positiepointer en int32-outputpointer; wrapper5342e0 eindigt met `ret 0ch`, schrijft de index en geeft1 terug. Deze ABI staat ook in [gericht bewijs](BINAIR/production-candidate-h2-position-and-cell.txt). Geen directe celladresberekening of globale enginepointer nodig in de latere feature.

## Footprint en coördinaten

[Bestaande enumerator](BINAIR/improvement-construction-neighbours-and-build.txt) en [bestaande controles](BINAIR/improvement-construction-controls.json) zijn voldoende: oorspronkelijke instructies gaven twintig unieke posities zonder centrum voor(20,40,0) en(21,41,0), met overlap tussen beide lijsten. De eligibilityantwoorden waren bij die geometriecontrole gemockt; drie aparte echte filtercontroles bewezen leeg/werker/cityhandle.

Voor het gecontroleerde centrum(20,40,0) kan de relatieve output zo worden gelezen:

| dy | dx in de teruggegeven MapPointData |
| --- | --- |
| −2 | −1,0,+1 |
| −1 | −2,−1,0,+1,+2 |
| 0 | −2,−1,+1,+2 |
| +1 | −2,−1,0,+1,+2 |
| +2 | −1,0,+1 |

Deze tabel is controlebewijs voor die gewone kaartpositie, geen zelfstandige algoritmevervanging aan polen/randen. De wrapper gebruikt echte buurfunctie502da0, kaartafmetingen/wrap en conversies. **503f00** normaliseert x en zet extern y om naar intern y−x; **503f70** zet intern y weer naar y+x met de kaartomvang. Daarom de input van H1 als MapPointData aan World+ac aanbieden en teruggegeven MapPointData direct aan World+a8 doorgeven; niet tussentijds handmatig y−x toepassen.

Gebruik voor een eerste H2-feature landlaag0. Andere lagen, poolgedrag en uiterst kleine kaarten zijn geen uitgebreid nieuw controlepakket in deze taak. Maak iedere teruggegeven positie uniek op x/y/z en sluit het genormaliseerde centrum defensief uit, zodat wrapduplicaten niet als verschillende bergen tellen. De enginequery bewaart haar interne scratch in globale velden; gebruik haar in dezelfde bestaande seriële AI-callcontext, geen nieuwe parallelle/reentrante scorequeries.

## Uitvoerbaar predicate en ontwerpgrens

Conceptuele specificatie voor de ontwerper; geen toegepaste featurecode:

```text
BeschikbareBergen(AiMain, centrum):
    eis passende World/civ-context en ondersteunde landlaag
    als World+28(centrum) afwijst: NIET_BEOORDEELBAAR
    World+ac(civ, centrum, &count, positions[20])
    als count buiten 0..20: NIET_BEOORDEELBAAR
    maak posities uniek op genormaliseerd x/y/z; verwijder centrum
    voor iedere overgebleven positie:
        vraag terrein via World+a8
        bij queryfout: NIET_BEOORDEELBAAR
        indien terrein in {8,20,22}: tel één bergwerkplek
    geef beschikbare_count en (beschikbare_count >= 3)
```

Beschikbaar betekent hier **momenteel open volgens dezelfde enginefilter als de normale AI**. Cell+18 sluit alle bestaande laborers uit, ook eigen arbeiders die later misschien verplaatst kunnen worden; Cell+14 sluit stadscentra uit. Het enkele overlappen met de footprint van een bestaande stad sluit een **onbezet** vakje niet uit. Een algemene afstandsstraf zou deze informatie verliezen en volgt niet uit het projectdoel.

De actuele armyfilter mag niet worden weggeoptimaliseerd:511030 controleert count/predicate/eigenaar en kan een vakje weigeren. De finale lokale Cell-route5005d0 weigert ook city/popbezetting en heeft een verwante armybranch met extra conditionele4c38a0-check. World+ac is hierdoor een bestaande, conservatieve open-werkplekkenroute; geen volledige vervanging van Population-actielegaliteit. De uiteindelijke Population-aanvraag heeft echte city-/inwonerhandles nodig. Zonder zulke handles vóór stichting kan niet een reeds geslaagde concrete plaatsing van drie inwoners worden bewezen.

**Volstaat voor het volgende ontwerp:** drie onderscheidbare, huidige open bergen tellen, en bergen van bestaande werkers/stadscentra weglaten. Geen technisch blocker voor dit querypredicate. **Nog geen belofte:** drie toekomstige werkers na stichting, herverdeling van bestaande werkers, reserveringen van andere settlerplannen, voedselonderhoud, mijnplaatsing of permanent exclusieve mountainrechten. Bij tijdelijke bevolkingsreset kan het huidige beeld veranderen; beoordeel in een consistente selectiepass en behandel een momentopname niet als permanente roltoekenning. Nieuwe lifecycle/events worden alleen onderzocht wanneer dat latere ontwerp die echt nodig heeft.

## Overdracht

H2 geeft de ontwerper voldoende concrete query-, ABI-, footprint- en bezettingskennis voor één volgende capacity-feature. Laat de meetlat onderscheiden: drie ruwe bergen maar één bezet→hoogstens2 beschikbaar; drie open unieke bergen→predicate waar; eigen/buitenlandse bezette werker→niet tellen; lege overlappende footprint→blijft kandidaat; duplicate wrappositie→eenmaal tellen. Dit zijn latere ontwerp-/testgevallen, geen nieuwe uitgevoerde tests.

Nieuwe bewijsstukken zijn alleen gerichte disassemblage van de nog ontbrekende gate-/conversie-/plaatsingscontext. De eerdere emulatorcontroles zijn hergebruikt, niet opnieuw uitgevoerd. Run stopt bij deze overdracht. Geen nieuwe gewichten, voedselonderzoek, volledige classifier of verdere finale plaatsingsreconstructie.
