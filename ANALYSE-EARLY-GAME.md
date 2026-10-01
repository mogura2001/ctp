# Eerste analyse van de vroege strategie

De uitwerking van voedsel, bergproductie, science-gebouwen en bevolkingsinzet staat in [ANALYSE-STADSMODELLEN.md](ANALYSE-STADSMODELLEN.md).

Deze analyse gebruikt de originele bestanden in `CTP-og`. Doel: op Deity zo snel mogelijk 25–30 steden bereiken, daarna groei en specialisatie. Er zijn geen spelbestanden aangepast. Dit is een eerste onderbouwd strategieontwerp, geen gemeten prestatieresultaat.

## 1. Theocracy maakt de uitbreidingsstrategie haalbaarder

Bron: `ctp_data/default/gamedata/govern.txt`.

| Parameter | Tyranny | Monarchy | Theocracy |
| --- | ---: | ---: | ---: |
| TOO_MANY_CITIES_THRESHOLD | 10 | 20 | 40 |
| TOO_MANY_CITIES_COEFFICIENT | 1 | 1 | 0.5 |
| PRODUCTION_COEF | 1 | 1.25 | 1.25 |
| KNOWLEDGE_COEF | 1 | 1.25 | 1.25 |
| GOLD_COEF | 1 | 1 | 1.25 |
| CRIME_COEF | 1 | 1 | 0.5 |
| MAX_SCIENCE_RATE | 0.5 | 0.6 | 0.6 |
| MAX_MARTIAL_LAW_UNITS | 4 | 3 | 1 |
| RATIONS_EXPECTATION | -1 | 0 | 1 |

De ingestelde grens 40 past bij een rijk van 25–30 steden. Dat betekent niet dat alle gelukproblemen verdwijnen: afstand, bevolking, rantsoenen en andere factoren blijven relevant. De productie-, kennis- en goudcoëfficiënten ondersteunen Theocracy als vroege economische keuze. Deze coëfficiënten zijn geen garantie voor exact dezelfde procentuele stijging in netto stadsopbrengst; de engine combineert meerdere factoren.

Een tweede garnizoenseenheid levert onder Theocracy geen extra effect binnen de ingestelde martial-law-limiet van één. Extra verdediging moet daarom door militaire noodzaak worden gerechtvaardigd.

Bron: `Advance.txt`. Religion heeft geen vermelde vereiste en basiskosten 20. Theocracy vereist alleen Religion en heeft basiskosten 65. Het pad heeft dus 85 aan opgetelde basiskosten wanneer beide nog ontbreken. Dit is geen voorspelling van de werkelijke Deity-onderzoekskosten of benodigde beurten.

Bron: `set_govern.fli`. De originele regels vragen bij maximaal vijf steden Tyranny. In de normale voorkeuren van warriors, scientists en slavers is Theocracy niet opgenomen; clerics hebben haar wel. Dit is een concreet aanknopingspunt voor verbetering.

Voorstel: maak Theocracy de vroege voorkeur voor de gewone beschavingen, afgestemd met onderzoek. Meet de overgang en de tijdelijke kosten van regeringswisseling. `Const.txt` stelt MAX_GOVERNMENT_CHANGE_TURNS op 4; de werkelijke overgangsduur moet worden geobserveerd.

## 2. Uitbreiding wordt te vroeg aan andere prioriteiten overgelaten

Bron: `aidata/aiploader.fli`. De expliciete masssettle-keuze is beperkt tot bepaalde kaartgroottes, vrede en fuzzy categorieën voor één tot circa vijf steden. Daarna keert de AI terug naar persoonlijkheidsstrategieën. Die kunnen nog kolonisten bouwen, maar er is geen expliciete race naar ons doel van 25–30 steden in deze openingselectie.

Dezelfde loader kan bij nabijheid van de menselijke hoofdstad of bepaalde menselijke legerverhoudingen defensieve openingstrategieën laden. Verschillende oorlogsfases vragen bovendien `build_no_settlers`. Hierdoor kan uitbreiding worden verdrongen door verdediging en oorlog. Het zijn fuzzy regels: de categoriegrenzen zijn geen eenvoudige harde grenzen.

Voorstel: ontwerp een eigen uitbreidingsfase die blijft gelden tot de doelomvang, met gerichte uitzonderingen bij aantoonbaar gevaar, gebrek aan ruimte of onhoudbaar geluk. Controleer alle later geladen strategieën die de instellingen kunnen overschrijven. Alleen de settlerprioriteit verhogen is onvoldoende.

## 3. Kolonisten en granaries moeten samen worden gepland

Bron: `Units.txt`. UNIT_SETTLER heeft basiskosten 540, SHIELD_HUNGER 0, FOOD_HUNGER 0 en BUILDING_REMOVES_A_POP. Kolonistenproductie kost dus productie en een inwoner. Reisduur tot vestiging is een aanvullende vertraging.

Bron: `Improve.txt`. IMPROVE_SILO heeft basiskosten 540, onderhoud 1, vereist Agriculture en bevat IMPROVEMENT_FLAG_SILO 50. Een granary kost in basisproductie evenveel als één settler. De precieze toepassing van de 50-waarde bij groei, kolonistenbouw en de volgorde van gebeurtenissen moet nog in het spel worden vastgesteld; de configuratie alleen bewijst geen volledige formule.

Bron: `DiffDB.txt`, Deity-blok. GRANARY_COEF is 10. `Const.txt` bevat daarnaast CITY_GROWTH_COEFFICIENT 175. We mogen deze waarden niet zonder enginekennis tot één groeiformule combineren.

Als een stad constant netto P productie heeft en geen voorraad, aanpassingen of bevolkingseffecten optreden, is de productiecomponent van een settler ceil(540/P) beurten. Bij P=30 is dat 18 beurten; bij P=60 negen. De granary heeft dezelfde basisproductietijd. Een wonder van 2160 kost onder die aannames respectievelijk 72 of 36 beurten. Dit zijn rekenvoorbeelden, geen werkelijke AI-bouwtijden: Deity bevat afzonderlijke productieaanpassingen.

Voorstel: vergelijk per geschikte stad settler-direct met granary-dan-settlers. Meet de stichtingsbeurten van opvolgende steden en het herstel van de bevolking. Een granary is voor onze openingsdoelstelling pas effectief als de betere cyclus de aanvankelijke vertraging tijdig terugverdient. Meet ook wat er gebeurt wanneer granaryvoltooiing net vóór versus net ná groei valt.

## 4. Labyrinth is een handelsinvestering

Bron: `Wonder.txt`. Labyrinth heeft basiskosten 2160, vereist Ship Building, wordt obsolete door Age of Reason en heeft WONDER_FLAG_FREE_TRADE_ROUTES. De basisbouwkosten zijn gelijk aan vier settlers.

Bron: `Advance.txt`. Ship Building vereist Toolmaking; beide hebben basiskosten 20. Dit is een extra onderzoekstak naast Religion/Theocracy wanneer deze technologieën nog ontbreken. Trade vereist Writing, die Agriculture vereist. Beschikbaarheid van Labyrinth betekent dus niet automatisch dat de benodigde handelsontwikkeling al aanwezig is.

Voorstel: reserveer hoogstens één geschikte productiestad voor de vroege Labyrinth-poging, overeenkomstig het projectdoel. Beoordeel beschikbare handelsmogelijkheden, voltooiingskans en gemiste kolonisten. Vier settlers zijn een directe productie-equivalentie, geen exacte telling van gemiste steden: bevolking, reisduur en nieuwe steden die zelf settlers produceren veranderen de uitkomst.

De enginewerking van gratis routes, hun aanleg en opbrengst wordt apart gecontroleerd. We hebben nog niet bewezen hoeveel economische winst Labyrinth in onze benchmark geeft.

## 5. Legerlast en veiligheid

Bron: `Units.txt`. Een hoplite heeft basiskosten 135 en SHIELD_HUNGER 4.05. Andere eenheden hebben eigen waarden. Bron: `govern.txt`: peace/alert/war-readiness heeft coëfficiënten 0.1/0.5/1 en HP-waarden 0.5/0.75/1 bij de drie onderzochte regeringen.

Deze instellingen tonen waarom aantal én readiness moeten worden onderzocht. Zonder de volledige onderhoudsformule geven we nog geen exact netto onderhoudsbedrag. Ook de productie die naar bouw gaat vertraagt uitbreiding: vier hoplites kosten in basisproductie één settler.

Voorstel: onderscheid feitelijke dreiging van een standaardquotum voor iedere stad. Onderzoek of grenssteden verdedigers kunnen krijgen zonder het hele rijk dezelfde bezetting op te leggen. Een hogere readiness kan veiligheid bieden, maar heeft economische kosten; lagere readiness vermindert HP.

## 6. Voorgestelde vroege beslisregels

Aanvullende afspraak: bouw normaal geen eerste generatie voedsel-improvements. Begin op water bij Ocean Faring en op land bij Agricultural Revolution (advanced farms). Alleen de productiestad die Labyrinth moet bouwen mag eerder voedsel-improvements krijgen. Vroege vestiging en kolonistenproductie moeten tot die tijd op natuurlijk voedsel worden beoordeeld.

Aanvulling op basis van de spelervaring van de gebruiker: zie [LOCATIESELECTIE.md](LOCATIESELECTIE.md). Een geschikte toekomstige science- of productiestad mag dicht bij andere steden staan. Tijdens uitbreiding telt naast uiteindelijke waarde ook het moment waarop vestigen zinvol is. Zoek vroeg een wonderproductiestad, bij voorkeur naast bergen, en waardeer monopoly-kansen in samenhang met goods die het rijk al bezit.

1. Onderzoek ontbrekende Religion en vervolgens Theocracy met hoge vroege prioriteit.
2. Kies Theocracy zodra beschikbaar, rekening houdend met tijdelijke overgang en stadsgeluk.
3. Houd een uitbreidingsfase actief tot ongeveer 25–30 steden; tel onderweg zijnde kolonisten mee om onnodige overproductie te voorkomen, indien de AI-interface dat ondersteunt.
4. Laat geschikte steden kolonisten leveren. Gebruik granaries wanneer ze de herhaalbare kolonistenproductie binnen de relevante horizon versnellen.
5. Laat eventueel één sterke productiestad Labyrinth bouwen.
6. Bouw verdediging voor concrete risico's; voorkom dat algemene bouwquota de uitbreiding domineren.
7. Schakel bij doelomvang over op groei en production/science-specialisatie.

Dit zijn voorgestelde strategieën. De mogelijkheid om afzonderlijke steden rollen en dynamische bouwkeuzes te geven is nog niet vastgesteld.

## 7. Micro die het onderzoeken waard is

- Verschuif bevolkingsinzet wanneer dat een kolonist eerder oplevert zonder een schadelijke voedsel- of groeivertraging.
- Stem granaryvoltooiing af op de eerstvolgende groei; bepaal eerst de precieze gebeurtenisvolgorde.
- Vergelijk vestigingslocaties op totale tijd tot de volgende bruikbare producerende stad, inclusief reistijd.
- Vermijd overbodige extra productie boven een voltooiingsgrens alleen wanneer de engine die productie niet nuttig bewaart. Overflowgedrag moet eerst worden getest.
- Bescherm uitbreiding met zo weinig mogelijk nutteloze verplaatsingen en eenheden; onderzoek wat de engine hiervoor aanstuurbaar maakt.

## 8. Gerichte validatie

Science-steden hebben groeipotentieel en minimaal drie mogelijke voedsel-improvementvakjes. Na een academy/publishing house/university kunnen overige laborers scientists worden. Onderzoek de unlockvoorwaarden, netto wetenschap, voedseloverschot en tijd tot volgende groei. Gebruik voorlopig drie voedselwerkers, vier bij grootte acht en vijf bij grootte tien. Vergelijk de extra wetenschap die groei binnen de resterende spelduur oplevert met de wetenschap die tijdens die groei wordt opgegeven; dit vergt nog berekeningen en speltests.

Voor productiesteden is inmiddels grootte vier als doel vastgelegd: drie inwoners werken op verbeterde bergen en één op een voldoende sterk verbeterd voedselvakje. Onderzoek daarom vooral voedselhaalbaarheid, verbeteringen en bevolkingsinzet. Stagnatie op vier is op zichzelf geen fout; verdere groei is voor dit stadstype geen doel. Zie [LOCATIESELECTIE.md](LOCATIESELECTIE.md).

De eerste spelobservaties moeten groeivoorraad bij granary/settler, werkelijke Deity-bouwkosten, readiness-onderhoud, de overheidsovergang en activering van gewijzigde bestanden vanuit een save vaststellen.

Daarna vergelijken we een uitgangsversie en een experimentele uitbreidingsversie op turn 25/50/100 en op de stichtingsbeurt van stad 25/30. Noteer ook beschikbare ruimte, bedreigingen, bevolking, onderzoek, kolonisten onderweg en stadsverlies. We voorspellen nog geen haalbare beurt voor 25–30 steden zonder benchmark.
