# Kwaliteit van vestigingslocaties: engineberekening gevonden

De kwaliteitsformule is een kernonderdeel van betere vestiging, naast packing en bereikbaarheid. Deze analyse volgt de echte executable via de bestaande AI-interface. Geen spel gestart of gameplay gewijzigd. Voedsel, productie, goud en goods zijn nu aan de terreinparser gekoppeld. De gereconstrueerde rekenformule is met 68 voorbeelden tegen de originele machinecode gecontroleerd. Scorepersistentie is inmiddels bevestigd; zie [SCORECACHE-EN-INGREEPPUNTEN.md](SCORECACHE-EN-INGREEPPUNTEN.md). De exacte betekenis van het centrumflag en de volledige herberekeningsroute blijven open.

## 1. Betrouwbare route ondanks de afwijkende engine-map

De GUID van IC3World wordt gelezen uit de overeenkomende robotcom.dll/map: 2037a9617ac8d11185a70060083a4082. Diezelfde GUID staat in civctp.exe op 00744eb8. De COM QueryInterface-routine vergelijkt deze GUID en geeft de World-interface terug. Zijn functietabel staat op 007452e0; de eerste drie functies hebben de verwachte QueryInterface/AddRef/Release-structuur.

De AI-DLL gebruikt offset 0x168 om de locatiewaarde op te vragen. In deze aangetoonde engine-functietabel wijst dat naar 00535500. Deze wrapper roept 005238d0 aan. Die leest een 16-bit waarde uit de kaarttabel op objectveld +0x248c, geïndexeerd met z/x/y.

Dit gebruikt **geen implementatieadressen uit civctp.map**. De oude map helpt slechts mogelijke namen herkennen; adressen en aanroepen zijn onafhankelijk in de aanwezige binary gevonden. Hulpmiddel: [Analyseer-Engine-Locaties.py](../PROEVEN/Analyseer-Engine-Locaties.py), optie --world. Bewijs: [interfacebinding](BINAIR/engine-world-binding.txt), [getter](BINAIR/engine-locatiewaarde-getter.txt).

## 2. Opbouw van de scoretabel

De routine op 005237d0 maakt een tijdelijke kaarttabel, vult die via 00522b20 en roept 005235e0 aan met het tijdelijke veld en de scoretabel. De laatste routine loopt de kaart af en roept voor iedere locatie de puntberekening op **00522e00** aan. De functies komen qua rol overeen met de oude symbolen RawStaticFP, StaticSettle, StaticSettlePoint en GetSettleValue, maar deze rolbeschrijving komt uit de gecontroleerde aanroepketen.

De tijdelijke tabel heeft vier bytes per vakje:

| Veld | Producerende routine | Huidige duiding |
|---|---|---|
| A, byte +0 | 00500290 | Productie/shields |
| B, byte +1 | 005003a0 | Goud |
| C, byte +2 | 00500110 | Voedsel |
| D, byte +3 | 004ffec0 | Lokaal good-slot, of −1 als geen bruikbaar slot |

De opbrengsthelpers lezen terreinrecords en conditionele extra opbrengsten, niet een fictieve uniforme tilewaarde. De binding is onafhankelijk van oude engine-adressen gecontroleerd via de echte tokenmetadata: ENV_FOOD = 1005, ENV_SHIELD = 1006, ENV_GOLD = 1015. De environmentparser schrijft deze op offsets 0, 4 en 0x3c. De terreinparser gebruikt voor ENV_BASE een environment op record+8; de helpers lezen daarmee voedsel op record+8, productie op record+0xc en goud op record+0x44. Voor dood terrein bestaan afzonderlijke offsets.

GOOD1-token 1018 leidt via de actuele parser-springtabel naar 004678b4. Daar wordt het eerste good-record op terreinrecord+0xa0 aangemaakt; andere good-slots volgen op +0xa4/+0xa8/+0xac. De aanwezigheidshelper selecteert zo'n slot met de celbits 0x1c0. D is dus een lokaal slot, niet automatisch de globale handelsidentiteit uit GOOD_INDEX. Voor D wordt −1 opgeslagen als de aanwezigheidscontrole faalt. De puntberekening gebruikt alleen D >= 0; zij vergelijkt geen good-identiteiten.

Bewijs van benoemde binding: [tokens](BINAIR/engine-token-binding.json), [environmentparser](BINAIR/engine-environment-parser.txt), [terreinparser](BINAIR/engine-terrain-parser-binding.txt), [good-recordregistratie](BINAIR/engine-goods-parser.txt) en de toewijzing op 00469805 in [engine-events](BINAIR/engine-score-events.txt).

Bron: [opbouw](BINAIR/engine-locatiewaarde-opbouw.txt), [tilehelpers](BINAIR/engine-locatiewaarde-tilehelpers.txt), [aanwezigheidscontrole](BINAIR/engine-locatiewaarde-gooddetectie.txt).

## 3. Welke vakjes worden beoordeeld?

De puntberekening verwerkt twintig omliggende vakjes en het centrum afzonderlijk. In interne coördinaten is de omgeving:

```text
  . X X X .
  X X X X X
  X X C X X
  X X X X X
  . X X X .
```

De eerste lus neemt x−1..x+1 met y−2 en y+2. De tweede neemt x−2..x+2 met y−1..y+1 en slaat het centrum over. De punten gaan door de wraphelper. Dit is de footprint van de berekening, geen afstandsverbod en nog geen definitieve koppeling aan zichtbare isometrische coördinaten.

De omgeving wordt in vier groepen ingedeeld op **C**: C ≤ 0, 0 < C ≤ 5, 5 < C ≤ 10, C > 10. Per groep worden aantallen en totalen van A en B bijgehouden. Dat is duidelijk meer dan alle ruwe opbrengsten zonder onderscheid optellen.

## 4. Aantoonbare numerieke hoofdstructuur

De eindberekening heeft onderstaande vorm. A = productie, B = goud, C = voedsel; een niet-negatieve D betekent hier een aanwezig good-slot.

```text
M = 1 + aantal omliggende vakjes met D >= 0
als B_centrum > 5: M += 1.1

S = (gewogen_A + 0.33 * gewogen_B) * M
    + (50 als centrumflag 0x40000000 gezet is, anders 0)
    - (35 als C_centrum < 5, anders 0)

als S <= 0: S = 1
S wordt naar een integer geconverteerd en als 16-bit waarde opgeslagen
```

Het centrum telt bij gewogen_A en gewogen_B mee. De groepen C > 5 worden rechtstreeks opgeteld; de lagere C-groepen worden via aantallen en een centrumafhankelijke budgetterm geschaald. De gereconstrueerde schaalbranches zijn:

```text
n0 = aantal omgevingstiles met C <= 0
n1 = aantal met 0 < C <= 5
n2 = aantal met 5 < C <= 10
budget = 3 * (C_centrum - 10) / 5

factor1 = max(0, min(n2, n1) + budget) / n1, als n1 > 0; anders 0
factor0 = max(0, n2 - min(n2, n1) + budget) / n0, als n0 > 0; anders 0

gewogen_A = A_centrum + factor0 * som_A_groep0
            + factor1 * som_A_groep1 + som_A_groep2 + som_A_groep3
gewogen_B wordt op dezelfde manier opgebouwd
```

De code bevat in deze branches geen expliciete bovengrens van 1 op de factoren. Dit model is inmiddels tegen de oorspronkelijke puntfunctie gecontroleerd, niet alleen tegen eigen pseudocode. Bij die controle is een eerdere fout gecorrigeerd: **centrumvoedsel wordt niet los bij de score opgeteld**. Het stuurt de schaalfactoren en de straf van 35. De eerdere formule met +C_centrum is achterhaald.

Het aanvullende centrumflag is nog niet definitief benoemd: de bonus van 50 mag niet zonder verdere binding als rivier-, kust- of stadsbonus worden uitgelegd. Hetzelfde bit wordt op 00534201 getoetst in een engine-interfacepredicate die een bewegingsmasker leest; dit is een nader aanknopingspunt, geen afgeronde semantische binding.

Bewijs: [puntberekening](BINAIR/engine-locatiewaarde-punt.txt), indeling op 00522f22–00523004 en de overeenkomstige tweede lus; budgetterm op 00523384–00523399; centrumvoorwaarden op 0052339c–005233c8; bonusflag en eindformule op 0052353e–005235ce. De coefficient is 0.33 zoals in de binary, niet exact 1/3. De integerhelper is nog niet zelf onderzocht.

## 5. Betekenis voor ons gewenste beleid

Het einddoel is expliciet de locatiebeoordeling aanpassen aan onze nieuwe vereisten. De concrete ontwerpvereisten en het onderscheid tussen toekomstige geschiktheid en vestigingsprioriteit staan in [LOCATIESELECTIE.md](../LOCATIESELECTIE.md#doel-locatiescore-aanpassen-aan-onze-vereisten). De technische route is nog niet gekozen; de oorspronkelijke formule begrijpen is de onderbouwing voor die keuze.

Een get_best_spot-instelling of hogere settle_value_coef verandert het gewicht van deze algemene locatiewaarde; het voegt geen eigen productie/science/monopoly-classificatie toe.

### Concrete rekenvoorbeelden

[Controleer-Locatiescore.py](../PROEVEN/Controleer-Locatiescore.py) voert uitsluitend gekopieerde engine-instructies in een lokale x86-emulator uit. Synthetische kaarttabellen vullen de input; de externe integerconversie wordt overgeslagen. Vergelijking betreft de double-score vóór die conversie, niet wettigheid van vestiging of een gespeelde stad. Alle 68 controles (acht gekozen voorbeelden en zestig deterministisch gevarieerde combinaties) komen overeen binnen floating-pointtolerantie. Bewijs: [score-formulecontrole.json](BINAIR/score-formulecontrole.json).

Onderstaande voorbeelden hebben hetzelfde graslandcentrum (productie 5, goud 0, voedsel 10), geen centrumflag en geen improvements. Basiswaarden komen uit de originele terrain.txt. Dit zijn scorevoorbeelden, geen gemeten economische opbrengsten van echte steden.

| Omgeving: twintig vakjes | Double-score |
|---|---:|
| Twintig graslandvakjes | 105 |
| Drie bergen + zeventien graslandvakjes | 458.05 |
| Drie bergen + zeventien plains-vakjes | 5 |
| Drie bergen + drie grasland + veertien plains | 50 |
| Twintig gelijke opbrengstvakjes, waarvan drie met hetzelfde good-slot | 420 |
| Dezelfde opbrengsten, drie verschillende good-slots | 420 |

De bergen hebben in deze voorbeelden productie 20, goud 5, voedsel 0. Grasland heeft 5/0/10; plains 10/0/5. De lage score van de derde locatie komt niet uit een expliciet bergverbod: de voedselgroepering maakt beide lage-voedselgroepen in dat voorbeeld waardeloos. Een locatie met goede toekomstige mijnen en één toekomstige sterke voedselvoorziening kan daardoor nu ongunstig worden gewaardeerd.

Een afzonderlijk grensgeval onderstreept dat deze formule geen toekomstplan voor verbeteringen is: drie bergen, drie voedsel-10-vakjes en veertien nulvakjes scoren 31.4618. Verhoog alleen die drie voedselwaarden naar 20 en de score daalt naar 20, omdat de tiles een andere groep ingaan. Dit is in machinecode bevestigd, maar geen bewijs dat een echte aangelegde farm onmiddellijk een gewijzigde AI-score veroorzaakt: daarvoor moet herberekening plaatsvinden.

### Gevolgen en resterende vragen

- Onze productiestaddefinitie is niet als expliciete regel aanwezig. De combinatie van ruwe voedselgroepen en productie bepaalt de score; toekomstige specialisatie wordt niet afzonderlijk doorgerekend.
- De tilehelpers lezen de huidige cel en aanwezige terreinmodificaties. In de gevolgde scoreberekening is geen voorspelling van nog aan te leggen mines/fisheries/advanced farms gevonden. Het precieze effect van iedere bestaande improvement moet nog apart worden gekoppeld.
- Een aanwezig good op een omgevingsvakje verhoogt de vermenigvuldiger met 1, ongeacht zijn identiteit. Onze monopolydefinitie en extra aanvoergoederen worden hiermee niet doorgerekend. De centrumgood wordt in deze telling niet apart gelezen; centrumgoud > 5 geeft wel de aanvullende verhoging van 1.1.
- Welk terrein-/celkenmerk geeft de centrumbonus van 50? Dat moeten we benoemen voordat we concrete locatievoorkeuren afleiden.

De scoreberekening neemt in deze route geen persoonlijkheids- of regeringargument. De AI voegt zulke aansturing later toe via haar profielen en doelprioriteiten. Twee directe aanroepen van de volledige scoreopbouw zijn gevonden: 0052d02e en 0056a531, bevestigd in de betreffende callers. De getter leest alleen de cache. Een rebuild iedere AI-beurt of na iedere improvement is hiermee niet aangetoond; inlined writes en indirecte aanroepen vergen apart onderzoek. Bron: [aanroepers](BINAIR/engine-score-directe-aanroepers.txt), [herberekening](BINAIR/engine-score-herberekening.txt).

## Volgende gerichte analyse

Vervolg uitgevoerd: [SCORECACHE-EN-INGREEPPUNTEN.md](SCORECACHE-EN-INGREEPPUNTEN.md). De scoretabel wordt opgeslagen en teruggelezen; twee synthetische archiefcontroles bevestigen exact herstel zonder scoreopbouw in die route. De nieuwe waardering moet ook vóór de kandidaatselectie meetellen. De bestaande World-interface kan de echte GOOD_INDEX leveren, hoewel de huidige kwaliteitsformule die niet gebruikt. Volledige herberekeningscondities blijven open.

Benoem centrumflag 0x40000000 en bind terrein-/improvementkenmerken en eigen good-tellingen. Werk daarmee de uitvoerbaarheid van een beoordeling per beschaving vóór de kandidaatordening uit. Een hogere algemene settle_value_coef herstelt ontbrekende monopoly- of toekomstwaardering niet. Nieuwe GUI-runs zijn hiervoor nog niet nodig.

Engine: civctp.exe SHA256 b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79, timestamp 37d6f702, imagebase 00400000. AI: robotcom.dll/map timestamp 37b894e7, imagebase 20000000. Er is geen binary gewijzigd en de engine-map blijft als adresbron afgewezen.
