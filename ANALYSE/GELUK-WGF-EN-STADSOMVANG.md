# Geluk, WGF en stadsomvang

6 oktober 2026, fase A. T = configuratie; B = oorspronkelijke machinecode; E = originele instructies in expliciete synthetische context. Geen spelstart, gameplaywijziging of volledig gesimuleerde geluks-/beurtcyclus.

## Betekenis voor de gezamenlijke opening

Snelle uitbreiding en Theocracy hangen ook via geluk samen. De gewone stadsantalberekening straft25 steden onder Tyranny met−7.5 en onder Monarchy met−2.5 geluk; Theocracy geeft bij25–30 steden nog0. Dit is een component per stad, naast alle andere componenten. Theocracy is hiermee onderbouwd als uitbreidingsvoorwaarde, maar haar40-grens is geen hard maximum op steden. De aparte AI-kandidaatfilter kan een overstap vanaf40 juist weigeren; zie [onderzoek/regering](ONDERZOEK-EN-REGERINGSKEUZE.md).

Grotere science-steden krijgen op Deity bovendien een grotere bevolkingsstraf. Een goedkope WGF-instelling kan die versterken, en de AI kan vervolgens inwoners aan entertainers besteden. Een model dat alleen voedsel en scientists telt mist deze concurrentie. De bestaande AI zoekt al combinaties van werkdag, loon en rantsoen: die route moet bij latere voorstellen worden benut.

## Basisgeluk en bevolkingsstraf

**T/B:** [DiffDB.txt](../CTP-og/ctp_data/default/gamedata/DiffDB.txt) heeft op Deity BASE_CONTENTMENT75, BIG_CITY_SCALE1 en BIG_CITY_OFFSET1. Player4c2830 leest basisgeluk uit [Player+12e8]+ac. Constructor4a13e0 kopieert DiffRecord+0/+8/+10 naar object+ac/+0/+8, met parsertokens268/270/271. Player4c2840/4c2850 lezen scale/offset. Zie [tokens](BINAIR/happiness-wgf-tokens.txt), [constructor/parser](BINAIR/deity-costs-handicap-copy-parser.txt) en [Player-getters](BINAIR/happiness-wgf-engine-base.txt).

De hoofdgeluksupdate4ab410, aangeroepen voor CityData+5cc, zet basisgeluk op object+0 en telt daarna componenten op. Zij telt bij4ab453–483 inwoners met PopulationRecord+64 bit4 in City+38. Token261 AFFECTS_CONTENTMENT_TOTAL→jumptabel4624bc, index2→4622a2 zet die bit. Gewone workers, entertainers en wisemen dragen de flag; de originele slave heeft haar niet. Zie [hoofdroute](BINAIR/economy-city-crime-full-update.txt), [popgetter](BINAIR/happiness-wgf-population-levels.txt), [Pop.txt](../CTP-og/ctp_data/default/gamedata/Pop.txt), [tokens](BINAIR/happiness-wgf-popflags-tokens.txt), [dispatchbinding](BINAIR/happiness-wgf-popflag-binding.json), [parser](BINAIR/happiness-wgf-pop-flags-parser.txt) en [recordroute](BINAIR/happiness-wgf-pop-record-route.txt).

**B/E:** de normale branch4ab54a–4ab666, zonder de aparte voorafgaande uitsluitingsflags en met gebouw-/wonderoffsets0, geeft:

`bevolkingscomponent = min(0, BIG_CITY_OFFSET − betrokken bevolking) × BIG_CITY_SCALE`

Bij1/4/8/10 betrokken inwoners is dat0/−3/−7/−9. Gebouw-/wondercallbacks45daf0/472fc0 kunnen deze branch wijzigen; hun volledige effectnamen/signs en de voorafgaande blissflags zijn hier niet opnieuw gebonden. Dit is daarom geen volledige gebouwafweging of exacte gelukvoorspelling voor een gespeelde stad.

## Straf voor teveel steden

**T/B/E:** parser45a9a7–45a9d1 bindt Government+140/+148 aan TOO_MANY_CITIES_THRESHOLD/token473 en TOO_MANY_CITIES_COEFFICIENT/token474. [govern.txt](../CTP-og/ctp_data/default/gamedata/govern.txt) gebruikt thresholds10/20/40 voor Tyranny/Monarchy/Theocracy en coefficient0.5. Zie [tokens](BINAIR/happiness-wgf-tokens.txt) en [parser](BINAIR/happiness-wgf-government-parser.txt).

Engine4aa5c0 loopt door Player+12c0, telt geldige stadhandles met opgevraagde omvang≥1 en neemt minstens1 als teller. Zij geeft0 bij teller≤threshold, anders:

`stedencomponent = −(getelde steden − threshold) × coefficient`

Opslag is happinessobject+a0 en geluksdetail15. De normale hoofdroute4ab66b roept deze herberekening aan; een andere callerbranch gebruikt de bestaande cache+a0. Geldige stad-/omvanggetters zijn in de controles gemockt. Zie [functie](BINAIR/happiness-wgf-government-and-difficulty.txt) en [caller](BINAIR/economy-city-crime-full-update.txt).

| Aantal getelde steden | Tyranny | Monarchy | Theocracy |
| --- | ---: | ---: | ---: |
| 10 |0 |0 |0 |
| 25 |−7.5 |−2.5 |0 |
| 30 |−10 |−5 |0 |
| 42 |−16 |−11 |−1 |

Die component maakt de25–30-opening onder Tyranny aantoonbaar zwaarder. Zij bewijst geen automatische revolte of val van een regering.

## Werkdag, loon en rantsoen in de engine

**B:** Player+1318 bevat de standen en economische factoren. Getters4c2520/4c2690/4c2800 lezen integerstand via4cb910/+960/+9b0 en geven die als double terug. Op object+50/+4c/+48 staan work/wage/ration. Regeringsgetters lezen coefficient/expectation op+30/+38, +40/+48, +50/+58. De parser bindt die aan tokens455/456,458/459,461/462. Zie [levelgetters](BINAIR/happiness-wgf-level-getters.txt), [levels](BINAIR/happiness-wgf-population-levels.txt), [regeringsgetters](BINAIR/happiness-wgf-government-and-difficulty.txt) en [parser](BINAIR/happiness-wgf-government-parser.txt).

**B/E:** enginefragment4ab7c9–4aba1e berekent voor gewone, betaalde stadscontext:

`dWork = (workStand − WORKDAY_EXPECTATION) × WORKDAY_COEF`

`dWage = (wageStand − WAGES_EXPECTATION) × WAGES_COEF`

`dRation = (rationStand − RATIONS_EXPECTATION) × RATIONS_COEF`

Bij City+9c (onbetaald loon) gebruikt de wagebranch de vaste stand−2; die branch is alleen statisch gevolgd. De som S van deze drie bijdragen wordt als volgt toegepast:

- S≤0: voeg `S × betrokken bevolking` aan het geluk toe.
- S>0: voeg precies2 toe, onafhankelijk van bevolkingsaantal en grootte van S.

Tyranny/Theocracy hebben hier coefficient1 en expectation−1. Alle standen−1 geven dus WGF-component0; work−2 met de andere standen−1 kost4 geluk bij4 inwoners en8 bij8 inwoners. Work0 met de andere standen−1 geeft+2. Tegengestelde bijdragen kunnen elkaar opheffen. De detailweergave gebruikt bij positieve S nog een eigen integerverdeling; die is niet hetzelfde als deze daadwerkelijke totaalsom. Bron: [hoofdcode](BINAIR/economy-city-crime-full-update.txt).

Economische standen lopen in dezelfde richting als eerder gebonden setters: work−2/−1/0 geeft productiefactor1.5/1.25/1; wage−1 geeft3 goud per betaald inwoner; ration−1 geeft0.75 van de voedselbehoefte. Zie [stadsopbrengsten](RANTSOENEN-EN-STADSOPBRENGSTEN.md) en [loonlasten](ONDERHOUD-LONEN-EN-DEITY-INKOMSTEN.md). Dit verklaart de kosten/geluksafweging, geen universeel optimale combinatie.

Het poploonfilter is nu nader benoemd:4cc940 leest Record+64 bit8, **IS_UNPAID**, token262→4622ac. IS_SLAVE is afzonderlijk token267→4623ec, bit20. De originele slave heeft beide, maar het zijn technisch verschillende flags. Zie [betaalgetter](BINAIR/happiness-wgf-paid-slave-fields.txt), [tokens/dispatch](BINAIR/happiness-wgf-popflag-binding.json) en [volledige flagparser](BINAIR/happiness-wgf-pop-flags-parser.txt). Alleen geldige decodegrenzen worden gebruikt; de losse misaligned range4623e7 is geen bewijs.

## Hoe kiest de bestaande AI haar WGF?

**B:** AllocWGF::SetRates20058400 vertaalt fuzzy work_min/max en food_min/max naar discrete grenzen met drempels±0.5/±1.5, begrenst met eigen beschikbare ranges en doorloopt kandidaatcombinaties van work/wages/food. Op200586cd roept zij CalcWGFUtility200598b0; een strikt hoger resultaat vervangt de beste combinatie. De gekozen combinatie wordt via Player-slot+d0 doorgegeven. Dat slot is5281d0; de engine-interface controleert iedere stand op−2..2 en roept achtereenvolgens de werkdag-, wage- en rantsoensetter aan. Dit is geen rechtstreekse uitvoering van iedere losse fuzzy wens. Bij een latere ongeldige parameter kan een eerdere setter al zijn uitgevoerd; de normale AI kiest binnen haar ranges.

CalcWGFUtility roept CalcHappy, CalcGold en CalcFood aan en combineert de geschatte opbrengsten met fuzzy wgf_prod/gold/food. Gewenste wage kan een positieve goldutility nog met wage_setting_bonus vermenigvuldigen. CalcHappy gebruikt regeringsverwachtingen/coefficienten, geschatte systeempopulatie, geluk-/crimegrenzen en een eigen piecewise model. De exacte overeenstemming van die aggregaatschatting met alle individuele citycomponenten is nog open. De optimizer is aanwezig; een nieuwe externe sliderplanner is niet zonder meer nodig.

Bewijs: [SetRates en selectie](BINAIR/economy-readiness-wgf-ai.txt), [utility en regeringsinitialisatie](BINAIR/happiness-wgf-ai-utility.txt), [slotwaarde](BINAIR/happiness-wgf-player-slot.json) en [volledige wrapper](BINAIR/happiness-wgf-player-setter-full.txt). System/cityinitialisatie, bijzondere fallback en fuzzy samenstelling zijn nog geen end-to-end controle.

## Grenzen, verificatie en volgende stap

Vervolg6 oktober16:49: [GELUKSGEBOUWEN-EN-GARNIZOEN](GELUKSGEBOUWEN-EN-GARNIZOEN.md) sluit de afzonderlijke martial-lawcap80 en vaste/regeringsgebonden gebouwsommen met17 controles. Die onderwerpen zijn dus niet meer geheel onbekend; finale reactie/overige componenten blijven open. Handelscapaciteit/Labyrinth23 is geaccepteerd, analist vervolgt pollution/latere stadstaken.

[Controleer-Geluk-WGF-En-Stadsgrens.py](../PROEVEN/Controleer-Geluk-WGF-En-Stadsgrens.py) geeft [19/19 controles](BINAIR/happiness-wgf-controls.json):7 stedenstraffen,4 normale sizecomponenten en8 WGF-gevallen. Governrecordlookup, stadvaliditeit/popoutputs, gebouw-/wonderoffsets0 en UI/details zijn mocks. Size/WGF zijn geldige interne ranges met expliciete callerregisters. De eerste WGF-fixture begon voor een FSTP uit de voorgaande callback en had bovendien de workrichting verkeerd aangenomen; de start is op4ab7c9 met correcte ECX gezet en de verwachtingen volgen nu de aangetoonde getters/formule. Er is geen volledige geluksupdate getest.

De voorheen onderbouwde criminaliteitsroute gebruikt dit uiteindelijke stadsgeluk; groei gebruikt VERY_HAPPY_THRESHOLD85. [const.txt](../CTP-og/ctp_data/default/gamedata/const.txt) noemt RIOT_LEVEL73. Exacte riotkans, revolte, bijzondere instantbliss, martial law, afstand, vervuiling, onbetaaldloon en wereldwonderlifecycle moeten van deze lokale componenten worden onderscheiden. De enkele subtotalen75+size+steden+WGF zijn geen voorspellingen voor het actuele scherm.

SHA/imagebase/timestamp en x87-mode volgen de eerdere enginechecks. Parser/writer/getterbindingen zijn onafhankelijk van de niet-passende civctp.map. Root vervolgt de resterende doelrelevante geluks-/defensiecomponenten en de fase-A-overdracht; de analist sluit zelfstandig handelscapaciteit/Labyrinth. Geen gewijzigde gameplay wordt met deze analyse geclaimd.
