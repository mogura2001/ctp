# Analyse van production- en science-steden

## Status en bronnen

Onderzocht: originele `terrain.txt`, `Improve.txt`, `Pop.txt`, `Advance.txt`, `Const.txt`, `govern.txt`, `DiffDB.txt`, `english/gamedata/gl_str.txt` en de AI-bestanden `outputs.fli` en `set_resource_desire.fli` in `CTP-og/ctp_data`.

Getallen hieronder zijn configuratiewaarden en expliciet aangeduide rekenmodellen. Netto stadsopbrengsten, centrumopbrengst, modifier-volgorde, afronding en groei moeten nog worden gecontroleerd in het spel. Er is geen speltest uitgevoerd en er zijn geen spelbestanden aangepast.

## Terrein en improvements

### Vastgelegde bouwregel na deze analyse

**Onderzoeksnotitie:** het overslaan van vroege voedsel-improvements is de huidige speelwijze die we eerst aan de AI willen leren, geen definitieve conclusie over optimale gameplay. Onderzoek later of specifieke vroege verbeteringen meer uitbreiding, productie of wetenschap opleveren dan hun investering kost. De gebruiker is ook geïnteresseerd in zulke verbeteringen voor zijn eigen spel. Leg eventuele afwijkende aanbevelingen apart vast met voorwaarden en bewijs; verander daarmee niet stilzwijgend het huidige implementatiedoel.

Normaal slaan we de eerste voedsel-improvements over. Waterverbeteringen starten bij Ocean Faring, advanced farms op land bij Agricultural Revolution. Alleen voor een productiestad die Labyrinth moet bouwen mag hiervan worden afgeweken. De onderstaande eerste-generatiewaarden blijven technische referentie en zijn geen standaard bouwadvies.

Dit corrigeert de voorlopige ontwikkelvolgordes hieronder: 'ontwikkel voedselvakjes' betekent pas bouwen zodra het toegestane niveau beschikbaar is, behalve bij de Labyrinth-uitzondering. Vóór die tijd telt natuurlijk voedsel. De vier-inwonersopzet met één voedselwerker en de science-groeiregels moeten dus ook op beschikbaarheid van technologie worden beoordeeld. We mogen de eerder genoemde kosten van drie mijnen plus een gewone voedsel-improvement niet als standaard stadsinvestering gebruiken.

Op het onderzochte shallow-water-terrein geeft het niveau via Ocean Faring 10 basisvoedsel + 15 extra = 25. Een advanced farm op grassland geeft eveneens 25; op grassland met rivier 30, en op plains 20. Dit zijn terreinwaarden vóór centrum en overige effecten. In `terrain.txt` betreft Ocean Faring ENV_IRR2; de spelbenaming 'fisheries' uit de gebruikersinstructie mag niet worden verward met het eerste niveau dat via Ship Building beschikbaar is. Technologie en improvementniveau zijn bepalend voor implementatie.

`terrain.txt` vermeldt dat de environmentwaarden na ENV_BASE additief zijn. Tabellen combineren een basis met één improvementniveau, niet meerdere niveaus boven elkaar. Technisch moet nog worden bevestigd hoe een upgrade een oudere improvement vervangt.

| Vakje | Basis | Eerste verbetering | Tweede verbetering | Derde verbetering |
| --- | ---: | ---: | ---: | ---: |
| Gewone berg, productie | 20 | 35 | 50 | 65 |
| Grassland, voedsel | 10 | 15 | 25 | 35 |
| Plains, voedsel | 5 | 10 | 20 | 30 |
| Shallow water, voedsel | 10 | 15 | 25 | 35 |

Rivier voegt bij de onderzochte landterreinen 5 voedsel en 5 productie toe. Daardoor geeft bijvoorbeeld grassland met rivier en een gewone farm 20 voedsel. Goods en andere modifiers zijn buiten deze voorbeelden gehouden. Andere berg- en watertypen moeten afzonderlijk worden gecontroleerd.

| Improvement, onderzocht terrein | Vereiste technologie | Materialen | ENV_TIME |
| --- | --- | ---: | ---: |
| Mountain mine 1 | Mining | 400 | 2 |
| Mountain mine 2 | Electricity | 1000 | 2 |
| Mountain mine 3 | Robotics | 2200 | 2 |
| Grassland/plains farm 1 | Agriculture | 200 | 2 |
| Grassland/plains farm 2 | Agricultural Revolution | 500 | 2 |
| Grassland/plains farm 3 | Intelligent Materials | 1400 | 2 |
| Shallow-water food improvement 1 | Ship Building | 200 | 2 |
| Shallow-water food improvement 2 | Ocean Faring | 500 | 2 |
| Shallow-water food improvement 3 | Robotics | 1400 | 2 |

Materiaalwaarden zijn per placement in het bestand. ENV_TIME is de ingestelde tijdparameter; planning, upgradeprijzen en daadwerkelijke activatie moeten worden geobserveerd. `tileimp.txt` bevat voornamelijk namen/iconen; de opbrengsten staan in `terrain.txt`.

## Productiestad: drie bergen en één voedselwerker

Onze definitie blijft: grootte vier, drie inwoners op verbeterde bergen en één op een voldoende sterk voedselvakje. Groei boven vier is geen doel.

Drie gewone bergen geven samen 60 basisproductie. Met drie gewone mijnen wordt dat 105; met niveau twee 150; met niveau drie 195. Dit sluit centrum, rivier, workday, regering, onderhoud, publieke werken en andere modifiers uit.

De eerste drie mijnen vragen samen 1200 aan ingestelde materialen. Drie mijnen plus een gewone farm of shallow-water voedselverbetering vragen samen 1400. Dat maakt tijdige publieke werken en beschikbare technologieën deel van het stadsplan.

### Voedsel: de cruciale haalbaarheidsvoorwaarde

Een worker en scientist hebben beide HUNGER 10 in `Pop.txt`. `Const.txt` bevat BASE_RATIONS 1 en UNIT_RATIONS 0.25. Als de rationsfactor wordt toegepast als `1 + 0.25*r`, levert dit het volgende voorlopige consumptiemodel voor vier gewone inwoners op:

| Rations-instelling r | Factor | Voedsel voor vier inwoners |
| --- | ---: | ---: |
| -2 | 0.5 | 20 |
| -1 | 0.75 | 30 |
| 0 | 1 | 40 |
| 1 | 1.25 | 50 |
| 2 | 1.5 | 60 |

Deze formule moet nog tegen het stadsvenster worden gecontroleerd. Slaven en andere bijzondere effecten zijn niet inbegrepen.

Een gewone farm of fishery levert volgens de onderzochte terreinwaarden niet zelfstandig 40 voedsel. Een river-grassland farm levert 20: dat sluit in dit eenvoudige model aan bij vier inwoners op r=-2, maar niet bij r=0. Eventuele automatisch meegetelde centrumopbrengst kan de uitkomst veranderen. `terrain.txt` bevat ENV_CITY_BONUS, maar de bestanden tonen niet volledig hoe de engine het centrum en tilewerk combineert; we tellen die daarom nog niet als bewezen extra inkomen mee.

Conclusie: de gekozen stadsopzet is een doel, maar kan niet op iedere locatie en bij iedere rationsstand zomaar worden aangenomen. Meet het netto voedsel van concrete steden. Kies een locatie met voldoende voedsel, ontwikkel de noodzakelijke improvement en voorkom verhongering tijdens de overgang naar drie bergwerkers. Theocracy heeft RATIONS_EXPECTATION 1; rations kunnen dus niet zonder gelukafweging worden verlaagd.

### Voorlopige ontwikkelvolgorde

1. Kies drie bruikbare bergen plus een voedselvoorziening die bij de landelijke instellingen haalbaar is; voorkeur voor water blijft gelden.
2. Groei naar vier. Stem de eerste mijnen en voedsel-improvement op deze ontwikkeling af; de exacte volgorde hangt van de huidige tekorten af.
3. Schakel naar drie bergwerkers en één voedselwerker zodra voedselonderhoud is gewaarborgd.
4. Bouw de toegewezen eenheden/schepen of het gewenste wonder; upgrade terrein wanneer de opbrengst de investering rechtvaardigt.

Een definitieve gebouwenqueue volgt nog niet uit deze terreinberekening. Een granary is niet automatisch noodzakelijk: onderzoek of de groei naar vier of eerdere kolonistenproductie de kosten rechtvaardigt. Verdere gebouwen moeten een concrete productiefunctie of noodzaak krijgen.

## Science-stad: groei versus scientists

Onze definitie blijft: groeipotentieel, minimaal drie mogelijke voedsel-improvementvakjes, later overige inwoners als scientists. Vuistregel: drie voedselwerkers, vier bij grootte acht en vijf bij grootte tien.

`POP_WISEMAN` heeft BONUS_SCIENCE 10, HUNGER 10 en IMPROVEMENT NULL. De bevolkingsdefinitie vraagt dus geen gebouw om deze specialist beschikbaar te maken. Dat bewijst nog niet dat iedere UI/enginevoorwaarde afwezig is. Onze keuze om na een science-gebouw scientists in te zetten is voorlopig een strategische timingregel, geen aangetoonde unlock.

| Gebouw | Interne naam | Technologie | Productiekosten | Upkeep | Science-flags |
| --- | --- | --- | ---: | ---: | --- |
| Academy | IMPROVE_ACADEMY | Philosophy | 540 | 4 | Knowledge +50%; SCIENCE_PER_POP 0.5 |
| Publishing House | IMPROVE_LIBRARY | Printing Press | 540 | 6 | Knowledge +25%; SCIENCE_PER_POP 0.5 |
| University | IMPROVE_UNIVERSITY | Classical Education | 1350 | 12 | Knowledge +50% |

De naam Publishing House is bevestigd in `english/gamedata/gl_str.txt`. De betekenis en toepassing van SCIENCE_PER_POP 0.5, inclusief samenloop tussen gebouwen, moet worden gecontroleerd. Ook stapeling van percentages en toepassing op specialists/regeringsbonussen staat niet volledig in de configuratie.

Academy is op de losse configuratiewaarden een aantrekkelijke eerste science-investering: dezelfde bouwkosten als Publishing House, lager onderhoud en een grotere knowledgebonus. Dat is nog geen bewijs dat zij altijd eerder moet komen; beschikbare technologie, lopende productie en horizon tellen mee. University kost 2.5 academy-bouwkosten en driemaal haar upkeep. Zij vraagt daarom een voldoende grote wetenschapsbasis en bruikbare resterende spelduur.

Philosophy vereist Jurisprudence en Religion; Jurisprudence vereist Writing, dat Agriculture vereist. Classical Education vereist Geometry en Philosophy; Geometry vereist Writing en Stone Working. Deze tak vraagt dus meer dan uitsluitend Religion/Theocracy. Houd de vroege uitbreidingsfase en latere science-ontwikkeling in de onderzoeksplanning uit elkaar.

### Bevolkingsinzet: voorlopige ruwe wetenschap

Als alle inwoners buiten voedselwerk scientists zijn, er geen andere taken nodig zijn en iedere scientist zijn ingestelde 10 oplevert vóór modifiers:

| Grootte | Voedselwerkers | Scientists | Ruwe specialist-science |
| --- | ---: | ---: | ---: |
| 4 | 3 | 1 | 10 |
| 6 | 3 | 3 | 30 |
| 8 | 4 | 4 | 40 |
| 10 | 5 | 5 | 50 |

Werkelijke wetenschap omvat ook terrein/goudconversie, gebouwen, regering en overige engine-effecten. Deze tabel is alleen een telling van de ingestelde specialistbonus.

Bij drie gewone grassland farms of shallow-water food improvements is de onderzochte voedselbasis 45. Drie river-grassland farms geven 60. Bij acht inwoners bedraagt consumptie in het bovenstaande model 40 op r=-2 en 80 op r=0. Dezelfde vuistregel kan dus op de ene locatie groei ondersteunen en op de andere zelfs onvoldoende onderhoud bieden. Controleer centrum en modifiers voordat hier harde conclusies uit volgen.

### Beslisregel voor extra groei

Vergelijk twee volledige alternatieven vanaf dezelfde stadstoestand:

- Behoud de extra scientist en bepaal huidige wetenschap en natuurlijke groei.
- Zet die inwoner op voedsel en bepaal wetenschap, versnelde groei en latere bevolkingsinzet.

De extra voedselwerker wint als de cumulatieve wetenschap binnen de resterende horizon hoger wordt, rekening houdend met iedere latere onderhoudsbehoefte. Gebruik bij voorkeur een beperkte simulatie per beurt met de gemeten groeiformule. Beide alternatieven kunnen groeien; vergelijk dus niet met een fictieve stilstaande tegenstander.

Illustratie, geen voorspelling: als extra voedselinzet 10 wetenschap per beurt kost gedurende zes beurten, is 60 wetenschap opgegeven. Als het groeipad vervolgens tien beurten eerder een duurzaam inzetbare extra scientist oplevert, kan het in die periode 100 terugwinnen. Als de extra inwoner nodig blijft voor voedsel of het andere pad snel dezelfde bevolking bereikt, vervalt dat voordeel. Gebouwbonussen en wetenschap van de vervangen tile moeten in de werkelijke vergelijking worden meegenomen.

### Voorlopige ontwikkelvolgorde

1. Ontwikkel minimaal drie voedselvakjes en groei op een tempo dat bij de huidige uitbreidingsfase past.
2. Bouw de eerste zinvolle beschikbare science-investering; academy is de eerste te toetsen kandidaat.
3. Zet inwoners boven de noodzakelijke voedselinzet om naar scientists wanneer dat gunstiger is dan tilewerk en benodigde gebouwproductie.
4. Gebruik grootte acht/vier voedselwerkers en grootte tien/vijf voedselwerkers als eerste benchmarkstrategie; optimaliseer daarna op netto voedsel en cumulatieve wetenschap.
5. Bouw extra science-gebouwen op basis van meeropbrengst, onderhoud, bouwtijd en horizon. Het voedselminimum en geluk blijven voorwaarden.

## Wat de huidige AI-interface al laat zien

`outputs.fli` bevat min_food_factor met no-growth/average/high waarden 1/1.5/2, prioriteiten voor pop_food_min/max en pop_science en farm-investering via inst_food. `set_resource_desire.fli` waardeert voedsel, productie, goud en wetenschap met gedeelde regels; de comments zeggen dat deze strategie voor alle stadsgroottes geldt.

Dit zijn aanknopingspunten voor beïnvloeding, maar nog geen aangetoonde mogelijkheid om per stad drie specifieke bergtiles of een exact aantal scientists te kiezen. Een wereldwijd hoger sciencegewicht kan productiesteden schaden; een wereldwijd voedseldoel kan science-steden en productiesteden verkeerd gelijk behandelen. Onderzoek per-stad-aansturing voordat we globale waarden wijzigen.

## Eerstvolgende technische en spelcontroles

1. Leg bij een grootte-vierstad met drie bergen het voedsel en de productie vast bij verschillende bevolkingsinzet en rations. Controleer centrumopbrengst.
2. Meet een science-stad vóór/na een scientist en vóór/na academy, publishing house en university, om bonuswerking en stapeling vast te stellen.
3. Meet voedselvoorraad en groeidrempels met/zonder granary en bij verschillende groottes; stel de echte groeiformule vast.
4. Controleer welke AI-inputs en outputs stadsspecifiek zijn, en of scripts het gewenste gedrag kunnen aansturen.
5. Maak pas daarna definitieve queues en numerieke microregels. Voldoende informatie voor een eerste experiment betekent niet dat de stadsmodellen al geïmplementeerd zijn.
