# Rantsoenfactor, criminaliteit en stadsopbrengsten

5 oktober2026, fase A; uitgebreid16:35 Europe/Amsterdam. Vervolg op [BEVOLKING-EN-SCIENTISTS.md](BEVOLKING-EN-SCIENTISTS.md). Rantsoenfactor, criminaliteitsmodifier en positionele opbrengstgetters zijn gebonden; de volledige stadsopbrengst-/consumptiecyclus is nog open. Geen spelstart of gameplay-/binarywijziging.

## Bewezen factorroute

De originale enginehash is `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp37d6f702/imagebase400000. Alle adressen zijn echte enginecode; de niet-passende civctp.map is niet gebruikt.

**B:** Player4c27f0 leest Player+1318 en springt naar4cb9a0. Die getter retourneert de double op object+8. Setter4cb970 berekent die als `Const+158 + integerArgument * Const+150` en bewaart tegelijk het argument op+48. Bewijs: [Player-route](BINAIR/economy-city-food-production-getters.txt), [objectgetters](BINAIR/economy-city-player-modifiers.txt), [setter](BINAIR/economy-city-hunger-ration.txt).

UNIT_RATIONS token524 (20c) en BASE_RATIONS token527 (20f) zijn [exact gevonden](BINAIR/economy-city-ration-token-candidates.txt). Const-parser451d40 schrijft op452a77… via token20c naar+150 en op452a94… via token20f naar+158. Zie [geldige volledige parserrange](BINAIR/economy-city-const-ration-parser.txt). [const.txt](../CTP-og/ctp_data/default/gamedata/const.txt) geeft respectievelijk0.25 en1.0. De gevolgde factor is dus:

```text
rantsoenfactor = 1 + 0.25 * rantsoenstand
```

**E:** [Controleer-Rantsoenfactor.py](../PROEVEN/Controleer-Rantsoenfactor.py) voert de oorspronkelijke setter en Player-getter uit zonder externe callbacks. [Zes controles](BINAIR/economy-city-ration-checks.json) slagen: standen−2..2 en één afwijkende constfixture. De controles bewijzen de rekenroute, niet de toegestane sliderstanden, AI-keuze of regeringstoepassing.

## Koppeling aan voedselbehoefte

De analist heeft CityData494ba0 gevolgd: positieve hunger per inwoner maal deze factor wordt opgeteld. De popgetter4ccaa0 resolveert de inwoner, leest het werkelijke PopDB-record en retourneert integer Record+30. Zie [hongergetter](BINAIR/economy-city-hunger-ration.txt) en de bestaande [som/aanroepers](BINAIR/population-scientists-food-demand.txt). De volledige PopDB-parser/defaults zijn niet opnieuw onderzocht.

Vier gewone inwoners met ieder hunger10 hebben in deze **behoefte-opvraag**:

| Stand | Factor | Behoefte |
| --- | ---: | ---: |
| −2 |0.5 |20 |
| −1 |0.75 |30 |
| 0 |1 |40 |
| 1 |1.25 |50 |
| 2 |1.5 |60 |

Dit bindt het eerdere voorlopige model uit [ANALYSE-STADSMODELLEN.md](../ANALYSE-STADSMODELLEN.md) aan de concrete opvraag voor AI-minimumfood. Het bewijst niet dat de volledige engine in alle groeibranches precies dezelfde behoefte afboekt, noch dat een gekozen stand qua geluk houdbaar is. Government.RATIONS_COEF is in deze setter/getter/hongersom niet rechtstreeks gelezen; de andere toepassingen van die regeringparameter moeten apart gevolgd worden.

## Criminaliteit: naam, formule en objectbinding

De aanvankelijk onbekende double([CityData+5cc]+b0) is nu aan criminaliteit gebonden. Government.CRIME_COEF/token486 en CRIME_OFFSET/token487 staan in [tokenbewijs](BINAIR/economy-city-crime-tokens.txt); de [werkelijke parser](BINAIR/economy-city-crime-parser-update.txt) schrijft op45aae6… respectievelijk Record+e8 en+f0. Player4c2b50/4c2b70 geven deze waarden terug via dezelfde GovernmentDB. De geldige functieproloog van de berekening is4aafe0, niet4ab020: zie [berekening](BINAIR/economy-city-crime-binding.txt) en [getters](BINAIR/economy-city-modifier-b0-entry.txt).

CityData492650 leest+5cc en roept4ab410 aan met dezelfde stad; aan het eind daarvan roept4abcc8 de criminaliteitsberekening aan. [City-objectbinding](BINAIR/economy-city-crime-city-object.txt), [volledige updater](BINAIR/economy-city-crime-full-update.txt). Het object+0 is de stadsgelukswaarde:4ac370 vergelijkt diezelfde waarde met de eerder gebonden VERY_HAPPY_THRESHOLD; de aparte updater4abce0 kan haar zetten en berekent vervolgens criminaliteit opnieuw. Dit identificeert het object; de samenstelling van alle gelukscomponenten is daarmee niet volledig verklaard.

City499840 haalt bestaande gebouwbits+48/+4c op en roept BuildingDB45d980 aan. Die begint bij1 en vermenigvuldigt Record+b8 voor ieder aanwezig gebouw uit de effectlijst (DB+80/+148). [Gebouwaggregatie](BINAIR/economy-city-crime-binding.txt). IMPROVEMENT_FLAG_LOWER_CRIME/token482 gaat via de bestaande parser-dispatch45f69c naar45f4ec en Record+b8: [effecttoken](BINAIR/economy-city-crime-effect-tokens.txt), [case](BINAIR/economy-city-crime-final-branches.txt). Courthouse en Police Station geven beide0.5 in [improve.txt](../CTP-og/ctp_data/default/gamedata/improve.txt): samen factor0.25, afzonderlijk0.5.

Wonder4721c0 telt integer Record+44 voor aanwezige, niet door de gevolgde obsolescencechecks uitgesloten wonders. De afzonderlijke token458=WONDER_FLAG_DEC_CRIME_PERCENT is [gevonden](BINAIR/economy-city-crime-wonder-token.txt); parser470792 trekt456 af en dispatcht via470e34, slot2 naar470808, dat op47081e Record+44 gebruikt. Zie [volledig parserbewijs](BINAIR/trade-goods-effect-flags-full.txt) en [wondergetter](BINAIR/economy-city-crime-parser-update.txt). Parthenon heeft100 in [wonder.txt](../CTP-og/ctp_data/default/gamedata/wonder.txt). De percentagebinding is bewezen; volledige wondertoekenning en actuele obsolescence in een spel zijn niet met dit pakket getest.

De berekening voor geluk onder de regeringsdrempel is:

```text
crime = clamp((CRIME_OFFSET - cityHappiness) * CRIME_COEF
              * product(aanwezige gebouw-crimefactoren)
              * (1 - wonderCrimePercent / 100) / 100, 0, 1)
```

Bij geluk≥CRIME_OFFSET wordt crime0. Opslag is object+b0/+b4;4ac8a0 schrijft tegelijk een geluksdetailveld voor component13. Voor Tyranny en Theocracy staan coefficient1 en offset85 in [govern.txt](../CTP-og/ctp_data/default/gamedata/govern.txt). Dus geluk75 betekent in deze keten10% verlies; één0.5-crimegebouw maakt dat5%. Dit is geen algemene aanbeveling dat zo'n gebouw zijn kosten altijd terugverdient.

## Positionele voedsel-/productieopbrengst en werkdag

CityData495250/495330 zijn vanuit geldige functiestarts gevolgd in [getterbewijs](BINAIR/economy-city-food-production-getters.txt) en [productie/controlegrenzen](BINAIR/economy-city-crime-test-boundaries.txt). Voor één opgevraagde positie:

```text
basisFood = WorldFood + terreingebonden stadsbonus + vlakke stadsbonus
food = basisFood * (1 + cityFoodPercent)
       * (1 + foodWonderPercent / 100) * (1 - crime)

basisProduction = WorldProduction + terreingebonden stadsbonus + vlakke stadsbonus
voorCrime = (basisProduction + trunc(basisProduction * cityProductionPercent))
            * workdayFactor
production = trunc(voorCrime - trunc(voorCrime * crime))
```

Voedsel blijft hier een double; productie gebruikt meerdere integerconversies. Daarom is productie niet algemeen gelijk aan één eindafronding van basis*(1+bonus)*werkdag*(1-crime). Bij basis35, werkdag1 en crime0.1 geeft deze getter32, terwijl trunc(35*0.9)=31. Dit is een positiegetter, geen bewijs van dezelfde afronding voor de volledige stadssom of uiteindelijke productievoorraad.

Player4c2500 leest object+1318 en geeft via4cb900 double+0 terug. Setter4cb8c0 schrijft `BASE_WORKDAY - stand*UNIT_WORKDAY`, met beide Constvelden+138/+130. [Setter/getter](BINAIR/economy-city-workday-happy.txt), [tokens522/525](BINAIR/economy-city-workday-tokens.txt), [unitparser](BINAIR/economy-city-workday-unit-parser.txt), [baseparser](BINAIR/economy-city-workday-parser.txt). Tekstwaarden1 en0.25 geven factor1−0.25*stand. Deze interne argumentrichting is geen bewijs van de richting/legale standen van de GUI-schuif of de optimale AI-stand. Een ontbrekend object geeft0 in de Player-getter.

Goud gebruikt dezelfde criminaliteitsdouble in de latere inhouding uit [GOUDGEBOUWEN-EN-STADSINKOMSTEN.md](GOUDGEBOUWEN-EN-STADSINKOMSTEN.md). De daar nog onbenoemde gedeelde modifier is hiermee geduid; andere inhoudingen blijven apart open.

## Verificatie en strategische betekenis

[Controleer-Stadsopbrengsten.py](../PROEVEN/Controleer-Stadsopbrengsten.py) voert oorspronkelijke enginecode uit op synthetische fixtures: [26/26 controles](BINAIR/economy-city-yield-crime-checks.json). Twaalf criminaliteitsgevallen gebruiken de originele callees zonder externe mocks, inclusief echte GovernmentDB, gebouwaggregatie, 64-bit bezitmasker en detailveldschrijver; twee extra wonderpercentgevallen vervangen alleen de percentagegetter. Zeven food/productiongevallen vervangen Worldopbrengst/type en food-wonderpercentage; de geïmporteerde ftol gebruikt een expliciete x87-truncate-stub. Vijf werkdaggevallen voeren setter plus Player-getter zonder externe mocks uit. Geen parser- of volledige spelcyclusclaim.

Gevolg voor de gebruikersstrategie: een stad van vier inwoners hoeft niet verder te groeien, maar haar geluk kan opbrengsten van bergen én het voedselvakje verminderen. De bestaande gebouw-crimereductie is multiplicatief; goudpercentages zijn daarentegen additief. Specialisatie kan daarom pas als netto model worden beoordeeld met werkdag, rantsoenen, geluk, centrumopbrengst en lasten erbij. Er is geen gameplaywijziging of nieuw gebouwenadvies toegepast.

## Stadsbrede som en feitelijk voedselonderhoud

Vervolg5 oktober16:44. [Stadsbrede routines](BINAIR/economy-city-total-yields.txt) laten zien waarom positiegetters niet zonder meer tot een netto stad mogen worden opgeteld. City494280 ververst gebouw-/terrein-/percentcaches, telt centrumproductie en de productiebijdrage van iedere inwoner. Terreinwerkers leveren Worldproductie plus terreinbonus; overige inwoners gebruiken hun afzonderlijke bijdragegetter. Daarna volgen vlakke bonus, gebouwpercentage, werkdag, wonderpercentage, regering, criminaliteit en eventueel een extra inhouding bij City+b0≥0. De naam van die laatste context is nog niet gebonden.

Government.PRODUCTION_COEF/token497 is [gevonden](BINAIR/economy-city-production-token.txt) en door [parser45ac25](BINAIR/economy-city-production-government-parser.txt) aan Record+138 gekoppeld. City4944f1 resolveert de actieve regering en gebruikt precies dit veld. Tyranny1 en Theocracy1.25 staan in [govern.txt](../CTP-og/ctp_data/default/gamedata/govern.txt). De positiegetter bevatte deze factor niet. Voor de normale som vóór de extra inhouding:

```text
P0 = centrum + som(terreinproductie/overige inwonersbijdragen) + vlakke bonus
P1 = P0 + trunc(P0 * gebouwpercentage)
P2 = trunc(P1 * werkdagfactor)
P3 = P2 + trunc(P2 * wonderpercentage / 100)
P4 = trunc(P3 * PRODUCTION_COEF)
Pnet = P4 - trunc(P4 * crime)
```

City494970 telt centrumvoedsel plus terreinwerkers/overige inwonersbijdragen; de centrumpositie komt eenmaal mee bovenop de bevolkingslijst. Vlakke/gebouwbonus en food-wonderpercentage volgen. Het resulterende bedrag wordt in+60 bewaard; criminaliteitsverlies is `floor(bedrag * crime)` in+70; het resterende voedsel komt in+68. Zie [volledige foodberekening](BINAIR/economy-city-food-sum-and-use.txt) en [echte importnamen](BINAIR/economy-city-rounding-imports.json):74335c is MSVCRT.floor, niet ceil of ftol. Een bijzondere City+448-tak omzeilt deze normale route; de betekenis daarvan blijft open.

De consumptie staat in de daadwerkelijk gevonden stadsupdate497f10 **inline**:498205..498295 doorloopt alle inwoners, telt alleen positieve Hunger maal de gebonden rantsoenfactor, schrijft totaal naar+78 en `voedselNaCrime - consumptie` naar+58. Daarna498298→494cf0, de eerder geanalyseerde voorraad-/groeiroute. [Updatevolgorde](BINAIR/economy-city-food-turn-order.txt). Daarmee is de eerdere vraag opgelost of de AI-behoefte-opvraag494ba0 dezelfde basisconsumptie rekent: de gevolgde update gebruikt dezelfde Hunger/rantsoenberekening. De losse494c30-routine doet hetzelfde, maar heeft in onze raw directe-callscan geen aanroeper; zij is daarom niet gebruikt als enig bewijs van de echte update.

In dezelfde onderzochte update wordt de bestaande queuevoltooiingsroutine48f790 op498121 eerder aangeroepen. Foodberekening494970 en goud4972c0 volgen op4981f6/498200, daarna consumptie en groei. Dit bindt de plaatselijke volgorde; volledige Player-/rondevolgorde, herverdeling na groei en alle kosten-/netwerkbranches zijn nog niet gesloten. Voor de bestaande AI-settleruitzondering blijft het afzonderlijke bewijs uit [VOEDSEL-GROEI-EN-KOLONISTEN.md](VOEDSEL-GROEI-EN-KOLONISTEN.md) leidend.

**Verificatie:** [Controleer-Stadssommen.py](../PROEVEN/Controleer-Stadssommen.py) geeft [10/10 controles](BINAIR/economy-city-total-sum-checks.json) van de oorspronkelijke food-/productiesom en de inline consumptie. Worldposities/terreinopbrengsten, pop-eigenschappen, gebouwcacheverversing en wonderopvragen zijn expliciet nagebootst. GovernmentDB, workday/ration-getters en de sominstructies zijn origineel; geïmporteerde ftol/floor hebben stubs met expliciete afronding. De uitvoering stopt vóór groei. Deze tests bewijzen de gecontroleerde somketen, geen daadwerkelijke bevolkingsplaatsing, update van gebouwen of volledig gespeelde beurt.

De gecontroleerde vier-inwonersfixture heeft centrumfood20/productie5, drie bergwerkers met ieder food0/productie35, één voedselwerker met food25/productie0, Hunger10 per inwoner, werkdag/ration1 en Theocracyproductiefactor1.25. Zonder gebouw-/wonderbonus en extra productie-inhouding:

| Invoer/situatie | Netto voedsel na onderhoud | Productie na crime/regering |
| --- | ---: | ---: |
| Crime0 |5 |137 |
| Crime0.1 |1 |124 |
| Centrumfood10, crime0 |−5 |137 |
| Centrumfood10, ration0.5, crime0 |15 |137 |
| Werkdag0.75, crime0.1 |1 |92 |

Dit is een **voorwaardelijk rekenvoorbeeld met expliciete invoer**. Het bewijst niet dat iedere werkelijke niet-bergcentrumlocatie20 food/5 productie oplevert of dat een lage rantsoenstand qua geluk houdbaar is. Het onderbouwt wel dat de functie van het centrum niet mag worden vergeten: drie mijnwerkers plus één voedselwerker zijn alleen duurzaam wanneer het totale voedsel ná crime het onderhoud dekt. Positief overschot blijft naar de groeiroute gaan; een productietaak met gewenste omvang4 beëindigt de automatische groei niet vanzelf.

## Nog open voor het volledige vier-inwonersmodel

Crime, positionele getters, normale centrum-/stadssom, Government.PRODUCTION_COEF en de consumptie vóór groei zijn nu gebonden. De Deity-groeicorrectie is om16:52 afzonderlijk gesloten in [VOEDSEL-GROEI](VOEDSEL-GROEI-EN-KOLONISTEN.md): HUMAN_FOOD_BONUS0 en gewone singleplayer-type1 slaat de correctie over; hoge gelukswaarde versnelt groei wel. Nog open: exacte centrum-/speciale-situatieopbrengsten op alle lagen, RATIONS_COEF in geluk/keuzes, science-eindketen, volledige PW/gebouw-/unitlasten, gelukscomponenten en volledige Player-/beurtvolgorde. Er is geen FOOD_COEF-token in het onderzochte govern.txt; de eerdere vermelding daarvan als te binden regeringparameter was een onbewezen aanname en is geschrapt. Losse getallen zijn nog geen volledige gespeelde stadssimulatie.

Volgende concrete stap: geluks-/lastencontext binden; normale basisconsumptie en Deity-groeicontext zijn gesloten. Behoud de gedeelde minimumfoodteller uit het bevolkingsrapport; een hoger min_food_factor is geen bewezen automatische surplusopdracht. Na de brede fase-A-overdracht kan de ontwerper deze getallen gebruiken voor haalbare productie-/sciencekeuzes.
