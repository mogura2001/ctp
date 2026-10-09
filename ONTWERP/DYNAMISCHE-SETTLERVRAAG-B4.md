# B4 — dynamische settlervraag met een uitvoerbare bestemming

8 oktober 2026, fase B. Afzonderlijk voorstel na rootacceptatie van [de gerichte A-overdracht](../ANALYSE/DYNAMISCHE-SETTLERVRAAG-B4.md), naast de geldige [brede overdracht](../ANALYSE/OVERDRACHT-A-NAAR-B.md). Geen implementatie, binarypatch, spelstart of gameplaymeting. Ownership: dit voorstel en VOORTGANG-ONTWERPER-B4.md. Root verzorgt uitleg aan de gebruiker, PROJECTSTATUS en eventuele C-overdracht.

## Beslissing en projectdoel

Vraag tijdens de gezamenlijke opening zoveel settlers aan als **unieke veilige nuttige locaties die nu uitvoerbaar zijn** en het resterende stadsdoel rechtvaardigen. Bestaande settlers en de oorspronkelijke CityAgent-productietelling dekken die voorraad mee af. Meer dan twee gelijktijdige settlers is daarmee mogelijk zonder permanent hoog quotum. Locaties waarvoor passend transport ontbreekt leveren eerst een transport-/techbehoefte, geen extra onbestemde settlers.

Dit dient [PROJECTDOELEN 1 en 1a](../PROJECTDOELEN.md): snelle nuttige uitbreiding richting 25–30, afremmen bij gedekte of ontbrekende opdrachten en hernemen bij nieuwe ruimte/veiligheid/transport. [LOCATIESELECTIE](../LOCATIESELECTIE.md) bepaalt nuttigheid; positieve oorspronkelijke score is daarvoor onvoldoende. Het voorstel ondersteunt doel 3 via de B2-fasekoppeling en de transportkant van doel 10. Het bouwt geen nieuwe marineoorlogsstrategie.

**Twee onderscheiden resultaten:** de quota-invoegroute en het getypeerde verdelingscontract zijn concreet genoeg voor review en een afzonderlijk, door root vrij te geven offline C-pakket. Volledige B4-gameplay blijft geblokkeerd door één gerichte binding: de per-civ locatie-/compatibiliteits-/reservationproducer. Een eigen resultstruct, interfacegetter of functienaam bewijst die binding niet. B4b carrierbouw/techaansturing is een volgende kleine wijziging, geen bijproduct van B4a.

## Huidige beslissing en aangetoonde oorzaak

De bestaande FLI-regels sturen packing, vestigingsstops en AIP-loads. `masssettle`, persoonlijkheids-, oorlogs- en marineprofielen kunnen het volledige unitklassenblok vervangen. AIP-lijsten kiezen een databasegeschikt type en vragen per klasse een voorraad: negatief q geeft `ceil(abs(q))`, niet-negatief q geeft `ceil(q×max(1,steden))`. Core/primary/overflowbijdragen tellen voor hetzelfde type op. Primary is geen ingebouwde voorkeur voor alle extra settlers.

`AIP::Update` telt eerst actual op 20066b7a, vervolgens desired op 20066b81, daarna tekorten op 20066b88. Actual omvat de bestaande armytelling en één door `CityAgent::What_Army_Am_I_Building` aangegeven unittype per stad. Niet bewezen: alle posities van willekeurig lange queues. Een stichting consumeert een settler, waardoor een vaste voorraad opnieuw vraag kan veroorzaken zonder toets op nuttige bestemming.

De bestaande T60-proef met hoge quota gaf 49→66 AI-steden, maar 3→71/78 losse settlers; Welsh ging van zeven naar drie steden en had geen schip in de hoge varianten. Dat toont waarom méér voorraad alleen onvoldoende is; het is geen causale meting van deze nieuwe policy. Bron: [VERBETERPLAN B4](VERBETERPLAN.md), [T60](../PROEVEN/settlerquota/reeks/VERGELIJKING-T60.md).

FLI bevat geen aangetoonde complete input voor unieke nuttige uitvoerbare bestemmingen. `land_continents_full_of_friends` is een bezettingsratio; de zoekheap is een gefilterde kandidaatvoorraad; de kleine goalcount is limietgebonden; `Planner+a74` is lokale bruikbare transportcapaciteit. Geen hiervan geeft zelfstandig het benodigde G. AAIP wijzigt marinequota en packing, maar bewijst geen dynamische doelgebonden settlervraag. Daarom blijven FLI/AIP-selectie, klassegewichten en stops intact en komt uitsluitend de ontbrekende vraagberekening aanvullend in de native AI-route. SLIC is hiervoor geen bewezen hook.

Bewijsbasis: [architectuur](../ANALYSE/ARCHITECTUUR.md), [AAIP-lessen](../ANALYSE/AAIP-LESSEN.md), [beslisketens](../ANALYSE/BESLISKETENS-OVERZICHT.md), [dekking](../ANALYSE/DEKKING.md), [quota/overrides](../ANALYSE/QUOTA-EN-OVERRIDES.md) en de nieuwere B4-machinecodeoverdracht. Historische onzekerheden over quotateken/volgorde worden door die overdracht vervangen.

## Gewenste beslissing en fasegrens

Noem C het actuele stadsantal, N de nog te kiezen openingsgrens, R=`max(0,N−C)` en G het aantal **gezamenlijk realiseerbare** nuttige veilige bestemmingen voor ondersteunde settlertypes, inclusief reeds toegewezen bestemmingen éénmaal. Het totale voorraadbudget is `D=min(G,R)`. De verdeling over types voldoet aan `sum(D_t)≤D`; ieder bestemmingsslot behoort tot precies één type. Onbruikbare/ontbrekende geselecteerde types kunnen het werkelijk gerealiseerde totaal verlagen.

N blijft parameter 25 of 30, dezelfde waarde als B2. Technische fixtures mogen beide toetsen; dat kiest geen productievariant. Zonder bevestigde N geen productieactivatie. B4 hergebruikt [B2 opening_completed/opening_required](GEZAMENLIJKE-OPENING-B2.md), geen eigen leeftijdsregel en geen tweede completionbit.

| Toestand | Deze B4-openingpolicy |
| --- | --- |
| opening_required=1, C<N, geldig actueel plan | Getypeerd D; extra vraag kan groter dan twee zijn |
| Tijdelijk geen bruikbare bestemmingen of alleen ontbrekend transport | Beheerde D_t=0; stop nieuwe tekorten, herbeoordeel volgende planronde |
| C≥N maar Theocracy nog niet actief | D_t=0 voor de beheerde openingvraag; B2 blijft true en regelt regering/onderzoek |
| opening_completed=1 | B4-openingadapter uit; oorspronkelijke returns/klassevraag herstellen |
| Barbaren, onbevestigde scope of ongeldige producer vóór de pass | B4 niet activeren; originele pass behouden, resultaat geen B4-acceptatie |

Herstel buiten opening is de begrenzing van dit wijzigingspakket, **geen keuze dat kolonisatie boven 30 gewenst is**. Het oorspronkelijke vervolg kan settlers blijven vragen. De gezamenlijke projectregels voor goede locaties blijven van kracht; een doelgebonden vervolgpolicy vereist een afzonderlijk voorstel en de open strategische keuze of/wanneer verder koloniseren. Dit ontwerp geeft geen C-vrijgave voor dat vervolgbeleid. Een stil N=30, permanent globaal D=0 of permanente dynamische opening na voltooiing zou die keuze vervangen en is niet toegestaan.

## Eén getypeerde voorraad, geen dubbele aftrek

De producer levert een disjunct bestemmingsplan en een typekaart, geen globale D die iedere lijst opnieuw mag gebruiken. Compatibele landtypes, techopvolgers, water- en spacesettlers zijn geen onafhankelijke claims op dezelfde grondlocatie. Eerste gameplayvariant ondersteunt uitsluitend de expliciet bewezen gewone landvestigingsscope; andere categorieën vragen eigen compatibiliteitsbewijs. Een ongedekte settlercategorie mag niet ongemerkt buiten de totaaltelling hetzelfde doel blijven aanvragen. Scopecontrole van alle effectieve geselecteerde settlerlijsten is dus een activatievoorwaarde voor de gehele pass.

Verdeling van bestemmingsslots, zonder numerieke gewichten:

1. Behoud geldige bestaande assignments/reservations op unieke bestemmingen. Een actuele settler, een productieclaim en een doelpointer zijn verschillende identiteiten; zij mogen dezelfde opdracht niet meerdere keren tellen.
2. Laat nog beschikbare compatibele bestaande/in-productie settlers eerst resterende bestemmingen dekken. Verreken oude en nieuwe uitwisselbare types zo in het gezamenlijke plan, voordat nieuwe voorraad aan het geselecteerde bouwtype wordt gegeven. Een oude settler voor een grondlocatie voorkomt een dubbele vraag naar de techopvolger voor dezelfde locatie.
3. Verdeel nog ongedekte bestemmingsslots over de bewezen effectieve geselecteerde types, in de oorspronkelijke klassepassvolgorde, met de bestaande kandidaatvolgorde als volgorde van bestemmingen. Elk slot krijgt één t. Geen nieuwe inhoudelijke prioriteitsgewichten; bestaande locatie-/taakprioriteit blijft uitgangspunt.
4. Publiceer alle D_t vóór de native quota-/priorityopbouw en houd de kaart gedurende die pass onveranderlijk. Voor beheerde types zonder slot is D_t expliciet 0. Types die deze pass niet daadwerkelijk geselecteerd worden leveren geen gefabriceerde unitvraag.

Dit is een contract voor de ontbrekende producer, geen claim dat huidige schedulerdata dit al aanbieden. Actual per type op `AIP+7c8` blijft het **enige** aftrekpunt: Supplemental berekent `max(0,D_t−Actual_t)`. D_t is voorraad inclusief gedekte bestemmingen, niet het tekort; trek bestaande/queued units niet al van D_t af. De planverdeling gebruikt aanwezigheid om slots tussen uitwisselbare types te kiezen, zonder een tweede productieaftrek.

Een native getelde settler die geen uitvoerbare opdracht heeft kan per type alsnog de native tekortvraag verlagen. B4 verandert actualfilters niet om die conservatieve ondervraag weg te poetsen. Producer/meetverslag moeten dat verschil zichtbaar maken; geen onbruikbare unit als gecertificeerde doeldekking tellen. Ongedekte matching betekent geen bewijs dat alle potentiële locaties nu uitvoerbaar zijn. Het opsporen en herplannen van zulke bestaande surplusunits is een latere afgebakende verbetering.

R begrenst de slots, ook wanneer er al meer settlers dan R zijn. Bestaande settlers worden niet verwijderd en lopende productie wordt niet blind geannuleerd. D_t<Actual_t geeft nul nieuwe tekorten. Het vervangen van al aanwezige goal-/queueopdrachten is niet bewezen door deze adapter; daarom kan eerder aangevraagde productie nog voltooid worden. Meet overshoot en bestaande requests afzonderlijk. Geen garantie van precies N gestichte steden door alleen nieuwe vraag af te remmen.

## Exacte technische ingreep en klasseprioriteit

Versiebinding: oorspronkelijke robotcom.dll SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, imagebase 20000000, timestamp 37b894e7; robotcom.map is passend. Enginecontext en eventuele B2/H3-kandidaten houden hun eigen fingerprints. Een gecombineerd pakket wordt uit verklaarde afzonderlijke diffs opgebouwd; geen originele hash claimen voor een reeds gewijzigde DLL.

Vervang uitsluitend de volledige vijf-byte call op **20065a4c**, oorspronkelijke bytes `e8 af fe ff ff`, door een call naar een eigen native returnadapter. Origineel doel: `AIP::Choose_Unit_From_List` op 20065900; hervatplaats 20065a51. De adapter roept eerst de originele selectie met dezelfde effectieve listpointer en type-outputpointer aan en vervangt alleen de quota-return voor expliciet beheerde types. De originele gekozen unit en outputpointer blijven intact.

**Expliciete klassekeuze:** de eerste oorspronkelijke klasse die type t selecteert draagt zijn volledige D_t en levert zijn oorspronkelijke klasseprioriteit voor alle bijbehorende entries. Latere core/primary/overflowklassen die hetzelfde t selecteren dragen nul. Dit kiest de kleinste bewezen route zonder een tweede klasseselector of nieuwe klassegewichten. Het garandeert geen primaryprioriteit: als core eerst selecteert, draagt core de voorraad. Dat lagere/hogere bestaande gewicht kan meer/minder queueconcurrentie geven en is een eigen meetuitkomst. Primary als drager forceren zou extra klassebinding/vooruitkijken vragen en wordt niet stil toegevoegd.

Lees W_t uit de al opgebouwde desireddouble op `AIP+7c0`; binnen de volledig beheerde types wordt iedere selectie onderschept, ook wanneer D_t=0. Invariant bij de eerste selectie: W_t=0; daarna W_t=D_t. Return voor beheerd t:

```text
bijdrage = max(0, D_t − W_t)
return bijdrage > 0 ? −double(bijdrage) : +0.0
```

De oorspronkelijke `Update_Desired_Units` bouwt zo zelf de totals **én quota-many priorityentries**. AIP+7c4 geeft per type de prioritycontainer, daar +0 entrycount en +18 data. Aan het einde moeten desired[t]=D_t en gebruikte entrycount[t]=D_t zijn. Actual blijft ongewijzigd. Ongeldig/negatief gekozen type of niet-beheerd niet-settlertype krijgt de oorspronkelijke return, inclusief bestaande fout-/skiproutes. Een beheerd type met D_t=0 krijgt werkelijk +0.0, geen achtergelaten positieve bijdrage.

**Niet toegestaan:** na desired alleen een grotere double schrijven. Supplemental leest op 20065d74–7a prioritydata met index `desired−actual−1`, zonder aangetoonde countcheck. Extra desired zonder extra native entries kan buiten de entries lezen. Geen gedeelde AIP-bronlijst tijdelijk wijzigen: pointers kunnen uit gedeelde managerdata komen en daarmee andere civs beïnvloeden.

ABI: thiscall, ECX=AIP; stackargumenten listpointer en signed32-type-outputpointer; oorspronkelijke functie ret8, double in x87 ST0. De adapter bewaart originele outputpointer/context en vereiste nonvolatile registers, houdt dezelfde stackbalans en retourneert precies één double in ST0. Consumeer/bewaar de originele double voordat extra queries x87 gebruiken. Behoud x87-depth/controlword, EFLAGS volgens het native callcontract en alle oorspronkelijke selection-/fallbacksemantiek. Alle D_t/W_t zijn finite gehele waarden binnen 0..N; geen onverwachte roundingmode of onbegrensde allocatie.

Eigen passplan staat in caller-/pass-owned opslag, niet in g_settle_ai. Owner is `AIP+800→AiMain`, met eigen Planner via AiMain+94; typegegevens via AiMain+38. Een ontbrekend/onvolledig plan kiest **vóór de hele desiredpass** origineel gedrag en maakt de B4-proef ongeldig. Niet halverwege naar originele quota terugvallen: dat mengt policies en kan D_t overschrijden. Een generatie-/ownerfout tijdens een eenmaal geactiveerde pass is een kandidaatfout: stop acceptatie en herstel de proef; geen geïmproviseerde nieuwe fatal-handler of gedeeltelijke tabellen als goed resultaat presenteren.

## Minimale G-producer en concrete integratiekeuze

Kies een **per-civ, per-planronde vluchtige snapshot tijdens de bestaande vestigingskandidaatpass**, vóór de kleine uitvoeringsgoallimiet en vóór heapcleanup. De gewone goalvorming blijft haar eigen prioriteit/filters houden. De snapshot moet dezelfde kandidaatcontext gebruiken en extra velden voor B4 leveren; een later los gelezen heapcount of een kopie van alleen de vijf bestaande goals is uitgesloten. Consumption gebeurt vóór de quota-opbouw van de daaropvolgende `AIP::Update`; de vraagadapter doet geen nieuw padzoekwerk per klassecall.

Dit is de gekozen integratierichting, **nog geen bewezen producerhookadres**. Movement roept FindAllGoalPos op 2002b0be, vervolgens Update_Squads op 2002b0ca en AIP::Update op 2002b0cf–d8. Goals ontstaan vóór de vraag, maar onder huidige filters/limieten. GroundBuildSettleTree op 2007a080, InsertBestSettleGoal op 2007a7c0 en cleanup op 2007af80 zijn de begrensde zoekregio. Alleen de bewezen quota-call krijgt in dit ontwerp exacte patchbytes.

| Verplichte snapshotinhoud | Contract / bewijsgrens |
| --- | --- |
| Owner, plan generation, status, scope | Actuele eigen AiMain/AIP/civ; geen andere civglobal; VALID/UNKNOWN expliciet, immutable tot pass-einde |
| Canonical locatie-identiteit | x/y/z en één stabiele identiteit binnen de pass; dezelfde locatie via verschillende heap-/goal-/typealternatieven telt éénmaal |
| Gezamenlijk bruikbaar stadsplan | Juridisch/maskerbruikbaar en nuttige huidige taak; geen gelijktijdige claims die dezelfde noodzakelijke berg/food/good onbewezen dubbel benutten |
| Nuttigheid en timing | Afzonderlijke inhoudelijke onderbouwing en nu/later-status volgens LOCATIESELECTIE; ruwe score>0 is alleen bestaande ordening |
| Typecompatibiliteit | Bewezen toegelaten categorie/types, tech/bouwbaarheid en effective-listdekking; oude/nieuwe types delen één bestemmingsslot |
| Assignment/reservation | Unieke goal/settler/productieclaim en eigenaar; reeds toegewezen bestemming omvatten, verlopen/verloren claim onderscheiden; geen pointertelling zonder lifetime |
| Veiligheid | Concrete gebonden huidige beoordeling; oorlogflag/burenratio op zichzelf geen volledige veiligheid; onbekend levert geen uitvoerbaar slot |
| Directe landroute | Gebonden uitvoerbare route voor de betreffende settler/categorie; continentnummer of PretestContinentReachable alleen bewijst dit niet |
| Beschikbaar transport | Compatibele concrete carrier, vrije capaciteit, locatie/ontmoetings-/landingsroute en exclusieve reservation; dezelfde cargoplek niet tegelijk aan verschillende doelen beloven |
| Eerst carrier/tech nodig | Locatie waardevol maar nu niet uitvoerbaar; ontbrekende capaciteit/tech en eigen/pending carrierclaim onderscheiden, geen G-slot zolang alleen toekomstig vervoer bestaat |
| Gescheiden tellingen | G/direct/transport-backed/pending/unknown en disjunct D_t; actuele native actual plus verklaarde matching/surplus, zonder tweede aftrek |

Deduplicatie betreft méér dan identieke centra: als twee alternatieven alleen op hetzelfde onmisbare ontwikkelplan kunnen bestaan, krijgen zij niet twee gelijktijdige vraagcredits. Geen radius1 als algemene nuttigheidsregel; dicht maar gezamenlijk bruikbaar vestigen blijft toegestaan. Een gedeelde berg buiten beide gekozen noodzakelijke plannen is geen automatische uitsluiting.

[H2/H3 fysieke capaciteit](PRODUCTIELOCATIES-H3.md) kan productiepotentie helpen onderbouwen: drie open bergen plus een aparte huidige voedselplek en benoemd onderhoudsscenario. Het is geen volledige netto-food-, veiligheids-, route- of stadsfunctiegarantie en reserveert geen werkplekken. H3 onbekend betekent niet alle science-/monopolylocaties waardeloos; de producer moet haar eigen beperkte nuttigheidsbewijs benoemen. B3/H3-kwaliteit en B4-uitvoerbaarheid blijven gescheiden meetfactoren.

**Eén gerichte terugvraag aan ctp_analist (B4-P):** bind in de bestaande FindAllGoalPos/GroundBuildSettleTree/InsertBestSettleGoal→Update_Squads→AIP::Update-regio het kleinste concrete capture-/refreshpunt en de bestaande gevalideerde reads/predicates waarmee bovenstaande snapshot voor gewone landvestiging vóór de klassepass gemaakt kan worden. Lever daarbij precies owner/lifetime, vóór-limit-kandidaatdekking, effective typecompatibiliteit, unieke assignment/reservation en direct/beschikbaar/pending-transportbinding met adressen/ABI/bewijsgrenzen. Als een noodzakelijk veld niet geleverd wordt, benoem de kleinste aanvullende producerlogica en het bewezen invoegpunt daarvoor; geen raw-scorecount als vervanging. **Kan één planronde deze gezamenlijke snapshot veilig leveren, of welke van haar verplichte velden maakt deze integratie aantoonbaar onmogelijk?**

Dit is één afgebakende producerlacune; geen opdracht voor volledige scheduler/pathfinder/transportdecompilatie, nieuwe tools, observer of runtimeproef. Stop zodra B4a uitvoerbaar gebonden is of een concrete blokkerende read/hook ontbreekt. Algemene late-game-compatibiliteit, lange queueboekhouding, volledige savecaches, cargo-invasies en optimalere matchalgoritmen blijven backlog tenzij deze gekozen route ze direct nodig maakt. Zonder deze binding geen volledige B4-C.

## Transport eerst, afzonderlijke B4b

B4a telt alleen direct of exclusief transport-backed bestemmingen in G. Op een klein eiland met nul landruimte en nul bruikbaar transport wordt dus D_t=0 voor nieuwe vraag; bestaande settlers verdwijnen niet. Een pending carrier in productie is een verklaarde oplossing in voorbereiding, nog geen beschikbare cargoplek. Zodra een compatibele carrier werkelijk toewijsbaar wordt, mogen zijn unieke bestemmingsslots meetellen. Bij carrierverlies vervallen die credits in de volgende verse pass.

B4b ontvangt de **gededupliceerde ontbrekende-operationele behoefte** uit dezelfde producer: bestemmingen, compatible carrier/cargo, vertrek/landingscontext, werkelijk aanwezige/pending capaciteit en zo nodig ontbrekende tech. Zij mag alleen het resterende capaciteitstekort aanvragen; dezelfde pending carrier niet ieder doel opnieuw laten aanvragen. Doel is passende kustproductie/tech vóór nieuwe transportloze settlers. De concrete carrierquota-/onderzoek-/queue-invoegroute is hier niet bewezen of vrijgegeven. B2 bezit research; een tijdelijke carriertechuitzondering moet met die categorie samenwerken en afzonderlijk onderbouwd zijn. Naval6000 versus settler10500 verklaart mogelijke concurrentie, geen universele queuevolgorde.

Daarom claimt B4a **remmen bij ontbrekend transport**, niet zelfstandig gerealiseerde schipbouw of overzeese stichting. De hele kleine-eilanddoelstelling slaagt pas als B4b operationele capaciteit werkelijk levert; dit aanvullende uitvoeringspunt wordt pas onderzocht als de producerbinding de concrete eerstvolgende transportwijziging bepaalt.

## Verwacht effect, risico's en alternatieven

Bij ruime veilige grondbestemmingen kan D>2 tegelijk ingezet worden en hoeft consumptie bij stichting geen nieuwe voorraad zonder bestemming te creëren. Bij gedekte vraag, tijdelijk gevaar, verdwenen bestemmingen of carrierverlies valt het nieuwe tekort terug. Verwacht minder onbestemde settlers en minder verdringing van noodzakelijke transportproductie. Snelheidswinst is een hypothese; queueconcurrentie, kleine actieve goallimieten en oorspronkelijke no_settling/stadsbouwchecks kunnen haar begrenzen.

Risico's: conservatieve onbekende routes/nuttigheid onderschatten G; teveel vermeend onafhankelijke footprints overschatten G; achterhaalde reservation geeft dubbelvraag; per-type native actual kan ongebruikte units als voorraad blijven aftrekken; eerste-classprioriteit kan extra vraag een ongunstig gewicht geven. Productie kan ondanks juiste vraag door bestaande gebouwen/defensie/stopregels winnen. Oude queued requests kunnen overshoot geven. Die neveneffecten worden gemeten en gericht teruggestuurd; geen uitbreiding van het pakket zonder concrete oorzaak.

Alternatieven:

- Alleen vaste−2/−20 of alleen per-cityquotum veranderen: nuttig als historische controlegroep, geen eindbeleid voor ruimte/transport.
- Alleen heapcount/goallimiet/continentvolheid gebruiken: mist nuttigheid, unieke resources of uitvoerbare route en kan groei door bestaande limieten blokkeren.
- Achteraf desired verhogen: aantoonbaar onveilig wegens priorityarray.
- Primary uitsluitend laten dragen: denkbaar vervolg als gemeten klasseconcurrentie dat vraagt; extra klassebinding nodig, niet vereist voor de eerste veilige route.
- Alle queues bij tijdelijke pauze wissen: verlies van productie en onnodige churn; stop eerst nieuwe requests, onderzoek bestaande surplus gericht.
- Carrierquota overal verhogen: mist compatible route en pending capaciteit; levert geen bewezen kleine-eilandoplossing.

## Kleine wijzigingen en volgorde

1. **B4a-0, uitsluitend offline mechaniek:** één quota-returnadapter met caller-owned gecontroleerde testplannen; gewone selectie, typed desired/actual/prioritycoherentie en klassevolgorde aantonen. Fixtureplannen heten expliciet FIXTURE, geen productieproducer of gameplaybewijs. Root kan dit afzonderlijk vrijgeven na review/uitleg; deze tekst is geen opdracht om te bouwen.
2. **B4-P gerichte analyse:** precies de producerbinding hierboven, zonder algemene nieuwe analyse. Kan voorafgaand aan een eventueel offline C-pakket afgerond worden; geen parallelle toepassing van dezelfde wijziging.
3. **B4a-1, producer + directe grondvraag:** alleen na acceptatie B4-P en bevestigde N, de verse typed planinvoer en adapter samen testen. Geen carrierquota/techpolicy veranderen. Bij onbekende scope geen productieactivatie.
4. **B4a-2, beschikbaar transport:** uitsluitend de bewezen transport-backed slots inschakelen boven dezelfde directe variant. Eigen gelijke transportsave en exclusieve capacityclaims toetsen. Geen reeds pending transport als beschikbaar tellen.
5. **B4b, ontbrekende capaciteit/tech:** pas na afzonderlijk concreet voorstel en aangetoonde request-/researchroute. Meet werkelijk carriercompletion, laad/reis/landing/stichting; meer schepen is geen einduitkomst.

B2-fase/N/lifecycle moet technisch bewezen beschikbaar zijn voor openingactivatie; alleen ontwerp of een half kandidaatbestand volstaat niet. H3 kan fysiek capaciteitbewijs leveren zodra haar echte enginecontext is geaccepteerd. Kleine bestaande goalgrenzen worden niet in B4a aangepast. Indien zij aantoonbaar het gebruik van correct gevraagde voorraad begrenzen, volgt één afzonderlijke limietproef; geen impliciet tweede gameplayfactor.

Eigen combinatieproeven: B4+B2 (zelfde N en faseovergang/Anarchy); B4+H3/B3 (nuttige kandidaten plus gezamenlijke footprint/reservation); B4b+B2research (carriertech kan Theocracy vertragen); B4+bestaande defensie/marine (veiligheid en productieconcurrentie); later B4+B5/wondervrijstelling. Losse positieve resultaten bewijzen hun combinatie niet.

## Meetbare succescriteria en gelijke start

Technische acceptatie is exact; numerieke gameplaystreefwaarden worden na uitgangsmeting met de gebruiker vastgesteld, niet uit dit voorstel verzonnen.

| Geval | Vereiste uitkomst |
| --- | --- |
| D=6, Actual=2, meerdere klassen kiezen hetzelfde t | Eén desired6, zes native priorityentries; tekort4; latere bijdragen0 |
| D=0, Actual=0 of >0 | Desired/entrycount0; geen nieuw Supplemental-tekort voor t |
| Twee uitwisselbare types delen vier bestemmingen | SomD_t≤4; oude compatible voorraad verhindert duplicaat voor opvolger; actual uitsluitend native eenmaal afgetrokken |
| G=9, N−C=3 | SomD_t≤3; aanwezige surplus blijft behouden en afzonderlijk gemeld |
| Drie bestemmingsalternatieven claimen dezelfde onmisbare berg/food/cargoplek | Alleen gezamenlijk uitvoerbare subset krijgt slots; geen driedubbele capaciteit |
| Zes nuttige veilige directe bestemmingen, R≥6 | D mag6 zijn, geen harde grens2; productie/assignment later apart aantonen |
| Nuttig doel alleen met ontbrekende carrier | Geen nieuw slot; pending capaciteit/tech apart, oorspronkelijke settlers niet verwijderen |
| Carrier beschikbaar/verloren of ruimte vrij/gevaar verdwenen | Slots nemen alleen op verse bewezen situatie toe/af; geen stale owner/generation |
| C=N zonder Theocracy; later completion1 | Eerst D0, daarna openingadapter uit en exacte oorspronkelijke returns; geen openingheractivatie |
| Baseline/offpolicy/niet-settlertype | Originele geselecteerde type/return/actual/klassegewichten en native ABI behouden |
| Save/load/reload of civwissel | Geen bewaarde producerpointer/reservationcache vertrouwen; verse pass reconstrueren vóór B4-request; B2-bit/N correct herstellen |

Na technische acceptatie dezelfde [T0](../PROEVEN/settlerquota/vaste-start/STARTMANIFEST.md), save SHA256 `8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26`, Deity/Gigantic/8 spelers, vaste passieve menselijke bediening en herstart per variant. Controle is dezelfde geaccepteerde B1/B2-basis zonder B4; H3 of H1-I staat per paar identiek. Noteer echte DLL/engine/aidata/regels/N/start/savehashes en actieve categorieën; geen historische OG→hoogquotumreeks als nieuwe controlegroep. Rekentijdlimieten en queueproefstatus blijven gelijk. Eerst aantonen dat variant en faseadapter na laden werkelijk actief zijn.

Gebruik voor beschikbaar/ontbrekend transport één **nog vast te leggen gezamenlijke transportsave**: zelfde eiland, settlervoorraad, compatible carriers/pendingproductie, technologie en dreiging. De technische proefsave is geen aangenomen vaste benchmark. Een scriptcommand of request bewijst geen scheepsbouw, loading, beweging of stichting; latere uitvoerder volgt AUTOMATISERING en verifieert scherm/beurt/actie.

Registreer per normale civ T25/T50/T100 en beurten stad25/stad30: C/G/D_t/Actual_t, native tekort en entrycount, unieke bestemming/functionele onderbouwing, assignment/reservation, nieuwe request/queueacceptatie/completion, bestaande/in-productie/onbestemde settlers, direct/transport/pending/unknown, carrierwachttijd en werkelijk gestichte nuttige steden. Daarnaast bevolking/science/research/Theocracy, gebouwen/wonders, defensie/stadsverlies en productieconcurrentie. Settler SHIELD_HUNGER0 is geen bewijs van kosteloze bouw; meet gemiste productie/tijd afzonderlijk.

Gameplayacceptatie vraagt sneller of minstens gelijkwaardig **nuttig** uitbreiden in ruime gevallen, minder nieuwe onbestemde voorraad bij gedekte/pending doelen, verklaarde herneming en geen gemaskeerde veiligheids-/economieachteruitgang. Hoge stadsaantallen, D>2, minder settlers of eerder requesten afzonderlijk volstaan niet. B4a mag transportremming bewijzen; B4b moet echte overzeese stichting bewijzen. Claim geen exacte snelheidswinst of N-overshootpreventie zonder meting.

## Activatie, herstel en formele vrijgave

Geen B4-bestanden in CTP-proef geïnstalleerd door deze ontwerprun. Alleen root geeft de gebruiker uitleg en doet B→C-overdracht. Routineklassekeuze hierboven past binnen het bestaande mandaat; N25/30 en vervolgkolonisatie blijven expliciete open gebruikerskeuzes voor afhankelijk productiebeleid.

Vóór iedere kandidaat: backup/hashes/preimages, ondersteunde hostbinding, verklaarde combinatie met B2/H3, reproductie van geselecteerde typen en complete scope. Bij mismatch niet patchen. Offline adapterchecks lopen eerst met productieproducer uit. Een fixture mag nooit als fallback in een geïnstalleerde variant blijven werken. Volledige gameplayactivatie vereist B4-P, geldige inhoudelijke nuttigheids/veiligheids/routecontracten, echte B2-fasecontext, bevestigde N en benchmarkmanifest; een interfacebeschrijving of datateller zonder bewezen hook voldoet niet.

Producerstate is vluchtig, niet nieuw geserialiseerd. Laat bestaande enginegoals/reservations eerst langs hun normale loadroute herstellen en maak de snapshot pas op het bewezen refreshpunt opnieuw. Nooit pointers uit een vorige civ/pass/save hergebruiken. Als B4-P aantoont dat normale loadstate daarvoor niet betrouwbaar is, benoemt de analist precies het benodigde refresh-/reconstructiepunt als deel van dezelfde producerbinding; geen algemene saveanalyse als voorwaarde.

Bij fout of ongunstig effect: stop de proef, bewaar variantresultaten en oorzaak, herstel uitsluitend B4-owned call/payload/config naar de vastgelegde geaccepteerde basis, verifieer hashes/diff en herstart vanuit dezelfde oorspronkelijke T0 of transportsave. B2/H3/andere agents' wijzigingen behouden via expliciete baselinereconstructie; geen blinde hele-DLL-og-restore boven anderen. Variantqueue-/requeststate niet als baseline laden. Geen settlers/queues live wissen om herstel cosmetisch te laten slagen.

**Vrijgegeven door dit document: niets toegepast. Reviewbaar:** veilige quota-calladapter, first-selected-classverdeling, typed totaal, fasegrens, producercontract en offline/gameplaymeetlat. **Eventueel beperkte C door root:** B4a-0 met expliciete fixturestatus. **Niet volledige C:** echte producer ontbreekt; Npending; transport-/techvraag en postopeningkolonisatie niet uitgewerkt tot uitvoeringsroute. Eerst B4-P beantwoorden; overige niet-blokkerende vragen op backlog. Hiermee is fase-B-ontwerp voor de toegewezen route afgerond zonder een ontbrekende hook te verzinnen.
