# B4: dynamische settlervoorraad in de bestaande vraagketen

Gerichte fase-A-overdracht, 8 oktober2026,09:47 Europe/Amsterdam. Gameplaydoel: snelle nuttige uitbreiding richting25–30, meer dan vaste2 settlers waar uitvoerbaar, vraag afbouwen bij ontbrekende locaties en eerst bruikbaar transport op klein eiland. Geen permanente±20, geen complete strategieontwerp. N blijft parameter; B2/H3 niet heropend. Alleen-lezen DLL-/bestandsbewijs, geen spelstart, gameplay-/binarywijziging, build, liveprocesactie, observer of emulator.

## Uitkomst

**Een veilige technisch aannemelijke invoegroute is de bestaande quota-return binnen Update_Desired_Units**, call20065a4c naar Choose_Unit_From_List20065900. Laat de originele selectie het type bepalen en pas alleen voor expliciet beheerde settlertypes de geretourneerde quota aan. Daardoor bouwt de oorspronkelijke code zelf zowel de gewenste totals als voldoende bijpassende priorityentries; Actual blijft origineel.

**Alleen de desired-double na Update_Desired_Units verhogen is onveilig.** Supplemental gebruikt `desired−actual−1` rechtstreeks als index in een apart priorityarray, zonder zichtbare countcheck. Een higher desired met alleen twee bestaande priorityentries kan buiten die entries lezen. Dit is de concrete reden om de nieuwe voorraad via de oorspronkelijke quota-/priorityopbouw te sturen.

De invoegroute is voldoende voor ontwerp. Het volledig gewenste B4-beleid houdt één begrensde producerblokkade: **een actuele per-civ, per compatibele settlercategorie gededupliceerde telling van veilige nuttige/toewijsbare locaties met onderscheid direct land, werkelijk beschikbaar transport en ontbrekend transport, inclusief reeds toegewezen/reserveerde doelen eenmaal**. Geen aangetoonde scalar in de huidige analyse levert dit volledige G. De bestaande kleine plannerdoellimiet of raw positieve-scoretelling mag die producer niet vervangen.

## Dekking en volgorde

| Schakel | Huidige machinecode | B4-contract / bewijsgrens |
| --- | --- | --- |
| Plaats-/goalvorming | Movement2002b0be→FindAllGoalPos2002b110;2002b0ca→Planner::Update_Squads. | Nieuwe locatiegoals ontstaan vóór de unitvraag, maar al onder bestaande filters/goallimieten. |
| Eigen vraagobject |2002b0cf–d8 neemt AiMain+94→Planner en+20→AIP::Update20066b70. AIP+800 wijst terug naar eigen AiMain. | Gebruik actuele AIP/owner, geen overgebleven g_settle_ai van een andere civ. |
| Limieten | AIP::Update20066b73→Update_Max_Goals. | Dit is geen beschikbare-ruimtetelling. De voorafgaande locatiepass kan bovendien nog gecachte/eerder ingestelde limieten hebben gebruikt. |
| Actual |20066b7a→Update_Actual_Units200655f0. | Origineel behouden; bestaande units en door CityAgent aangegeven unit in productie worden opnieuw geteld. |
| Desired |20066b81→Update_Desired_Units200659a0. | Reset totals en prioriteitscounts, loopt alle aanwezige bouwklassen, selecteert type en bouwt quota-/prioritybijdragen. |
| Exacte ingreep |20065a45–4c pusht type-outputpointer en lijstpointer, ECX=AIP, callChoose_Unit_From_List20065900. | Native calladapter laat selectie intact en vervangt zo nodig quota-return. |
| Tekort |20066b88→Add_Supplemental_Unit_Build_Goals20065cc0. | Originele `max(0,desired−actual)` en bestaande no_settling-/stadspretests blijven werken. Trek actual niet al in quota af. |
| Overige bouw / uitvoering |20066b8f→Update_Building_Build_Lists;2002b0ea→Allocate_Troops_And_Execute_Tasks. | B4 vraagt units aan, garandeert geen queue-/transport-/stichtingsactie. |

Bewijs: [vraagentry en priorityopbouw](BINAIR/settler-demand-b4-demand-entry.txt), [movementvolgorde](BINAIR/build-goals-queue-ai-legacy-and-unit.txt), [bestaande aanvulling](RUIMTE-BUREN-TRANSPORT.md), [queueconcurrentie](BOUWDOELEN-EN-QUEUE.md).

## Velden, totals en prioriteiten

| AIP-veld | Concrete bestaande betekenis |
| --- | --- |
| +7b0 | Aantal bouwklassen. |
| +7bc | Klassencontainer; selected-listpointer uit klasse+0c in de loop20065a2e–4c. |
| +7c0 | Container met double desiredtotals; `[container] +8*t` voor unittype t. |
| +7c8 | Container met signed32 actualtelling; `[container] +4*t`. |
| +7c4 | Container met pointer per unittype naar prioritycontainer. Daar+0 is de gebruikte entrycount; +18 is de prioritydata die Supplemental leest. |
| +800 | Eigenaar AiMain; AiMain+38 is UnitDB en+94 Planner. |

Desired wist de doubles op200659d0/d4 en prioritycounts op200659e4. Ieder geselecteerd type krijgt de quotaformule: negatief→ceil(abs(q)), niet-negatief→ceil(q×max(1,steden)).20065ab6–c7 **telt bij het bestaande type-total op**. Core/primary/overflow zijn daarom geen drie onafhankelijke soorten settlers; meerdere klassen kunnen dezelfde typevoorraad vergroten. Daarna genereert20065b29–65c76 quota-many prioriteitsentries vanuit de betreffende klasseprioriteit; originele allocatie/sortering blijft verantwoordelijk.

Supplemental20065d0c–12 trekt actual af;20065d67 zet index optekort−1;20065d74–7a leest `[prioritycontainer+18][index]`. Daarom moeten quota, total en entrycount coherent ontstaan. Naar beneden begrenzen van een total kan binnen bestaande entries passen, maar lost veilige vergroting niet op en wordt niet de gekozen algemene route.

Actual wist zijn typecounts, telt legers via CountUnitTypes200656ab (bestaande state17/18-uitsluiting blijft behouden) en vraagt per CityAgent What_Army_Am_I_Building op2006579f. Als resultaat niet−1 is, verhoogt200657b4 de betreffende typecount met1. **Dit is de aangetoonde bestaande AI-productietelling**, geen nieuw bewijs dat alle posities van willekeurig langere enginequeues worden gesommeerd. De adapter blijft van deze telling, aanwezige settlers en queues af.

## Minimaal quota-/ABI-contract voor ontwerp

Kies voor iedere beheerde geselecteerde type t een eindvoorraad **D_t** als niet-negatieve begrensde integer. Die is een typevoorraad, niet de nieuwe tekortvraag. Gebruik de al opgebouwde desiredwaarde **W_t** uit+7c0. Voor iedere daarop volgende klasse die t selecteert:

    bijdrage_t = max(0, D_t - W_t)
    quota_return = bijdrage_t > 0 ? -double(bijdrage_t) : +0.0

De eerste geschikte klasse bouwt de resterende voorraad en priorityentries; latere core/primary/overflowklassen voor hetzelfde t leveren0. Daarmee resteert één D_t en geen stille dubbele bijdrage. Het klassegewicht van de oorspronkelijke eerste geselecteerde klasse blijft de bron voor de nieuwe entries. Welke klasse de voorraad hoort te dragen is een expliciete ontwerpkeuze; deze route geeft niet automatisch primaryvoorrang. Een andere verdeling kan binnen hetzelfde totaaldoel, maar moet vóór C concreet gemaakt worden.

**Een globaal settlertotaal D is niet hetzelfde als iedere D_t.** Als meerdere compatibele landsettlers, water-/spacesettlers of tech-upgrades geselecteerd worden, mag niet ieder type dezelfde D krijgen. De producer/ontwerper moet een disjuncte verdeling over types/categorieën geven met somD_t≤de gezamenlijke uitvoerbare behoefte. Bestaande actual pertype kan settlers niet automatisch tussen uitwisselbare types verrekenen. Waar categoriecompatibiliteit nog ontbreekt, niet doen alsof een typekaart reeds een correcte mondiale behoefte is.

Choose_Unit_From_List is thiscall: ECX=AIP; stackargumenten lijstpointer en pointer naar signed32 selectedtype; oorspronkelijke return is double in x87ST0; callee `ret8` op20065997. De volledige5-byte call20065a4c is `e8 af fe ff ff`; originele hervatplaats20065a51 gebruikt die ST0. De adapter moet dezelfde stackbalans behouden, eerst de originele functie aanroepen, de outputtypepointer en alle benodigde caller/nonvolatile registers bewaren en precies één double in ST0 teruggeven. Bewaar/pak de oorspronkelijke double correct als extra queries x87 gebruiken. Geen gekozen type vervangen of type-outputpointer overschrijven.

Bij null/ontbrekende classlist bereikt de oorspronkelijke loop deze call niet. Bij ongeldige/negatieve gekozen type of geen expliciet beheerde D_t retourneert de adapter de oorspronkelijke double, zodat originele skip-/fout-/fallbackroutes blijven gelden. Een ontbrekend bouwbaar type wordt niet gefabriceerd. Een geldige geselecteerde type met expliciete D_t=0 mag juist0 krijgen; een eerdere positieve klassebijdrage mag niet ongemoeid blijven als dat type werkelijk geheel onder B4 valt. Een ongeldig producerresultaat vraagt een vooraf ontworpen fallback, geen verzonnen positieve vraag.

D_t zelf moet actueel bij dezelfde eigenaar/planronde zijn, tijdens de klassepass stabiel blijven en vóór de native priorityopbouw beschikbaar zijn. Het oorspronkelijke q-foutpad bevat eigen magnitudechecks; voorkom niet-finite/overgrote outputs en blijf binnen de gekozen N/voorraadgrens. Geen AIP-bronlijst tijdelijk muteren: effectieve klasse-/lijstpointers kunnen uit de gedeelde bronmanager komen. De returnadapter vermijdt zulke alias-/restoreproblemen en nieuwe opgeslagen quota. AIP-overrides bepalen nog steeds de aanwezige lijsten en klassegewichten; off-policy/fase-einde geeft de originele return terug, volgende Update herbouwt de tabellen.

## Welke bestaande ruimtetellingen bruikbaar zijn

| Producerbron | Bewezen veld/plaats | Wat zij werkelijk vertelt |
| --- | --- | --- |
| Ruwe gekozen zoekheap | AiMain+80→AiMap; heap ingebed op AiMap+58;+60 is gebruikte heapcount met één sentinel, lokale code gebruiktcount−1. GroundBuildSettleTree2007a080 reset/herbouwt; zoekafstand AiMap+68. | Masker-/zoekafstandgefilterde kandidaatvoorraad vóór verdere acceptatie, **geen** deduplicatie van nuttige stadfootprints/veiligheid/daadwerkelijk transport. |
| Actuele lokaal gemaakte goals | InsertSettleGoals2007aaf0 lokale counters `[ebp-14]`/`[ebp-10]`, continentarrays lokaal toegewezen. InsertBestSettleGoal2007a7c0 krijgt deze via pointers en vergelijkt tevens doellimieten. | Aantal aan deze selectiepass aangeboden/geaccepteerde doelen onder limieten, niet alle vrije ruimte. Deze stackwaarden leven niet voort als G-input. |
| Tijdelijke uitsluiting | g_can_settle_ground/space worden uit eigen AiMap-maskers gekopieerd;2007aaa9 voegt GoalSettle toe;2007aabb→FlattenCanSettle wist radius1 rond gekozen punt in tijdelijk masker. | Locatiescheiding van deze pass; geen bewezen langdurige per-role/good-/foodreservationboekhouding. |
| Goal/locatie |2007aa92→GoalSettle20048600 met gekozen MapPointData en signed16kwaliteit;2007aaa9→eigen Planner::Add_Goal. | Geaccepteerde taaklocatie/kwaliteit, nog geen uitvoerbare of veilige stad. Goalcount is zelf limietgebonden. |
| Bestaand transport | Planner::GetUsableTransport2006f150 leest Planner+a74; Squadronberekening20077130; carriers gezocht inPlanner+a6c. | Lokale bruikbare vrije-capaciteittoets; niet bewezen als route-/type-/taskgebonden transportcapaciteit voor ieder vestigingsdoel. |

Bronnen: [selectiecode](BINAIR/vestigingsselectie.txt), [heaplevensduur](BINAIR/score-hook-h1-heap-callers.txt), [H1-ordering](INGREEP-LOCATIESCORE-H1.md), [transportketen](TRANSPORT-EN-VESTIGINGSACTIES.md). CleanSettleQueue2007af80 ruimt de tijdelijke heap op; een raw pointer/countsnapshot bij de later gelegen AIPUpdate mag daarom niet zonder bewezen lifetime worden gebruikt. g_settle_ai/g_can_settle zijn current-pass globals, geen betrouwbare bewaarde per-civ G.

InsertBestSettleGoal filtert bezetting, tijdelijk masker, land/watercategorie, continent en aanwezige legers; landcontinent zonder eigen landlegers krijgt niet onbeperkt goals. PretestContinentReachable20014a60 kan andere landcontinentnummers voorlopig toelaten via carrier-/kusttakken; dat is geen direct-landbereikbaarheid. TryTransport en ExecuteWithTransport kennen vervolgens beweging≥16, cargo, capaciteit, compatibiliteit en ontmoetingsroute. Een positievea74 of één Trireme belooft dus niet dat al die doelen vandaag transport hebben. Bezettingsratio land_continents_full/of_friends is evenmin G.

**Exact nog te leveren producerinput:** een eigenaar-/planronde-/locatiegebonden unieke lijst of telling van bruikbare doelen met categorie/toelaatbare settlertypes, actuele assignment/reservationstatus en routeklasse (direct / passend beschikbaar transport / eerst tech-carrier nodig), zodanig dat ieder locatie- en compatibiliteitsalternatief slechts eenmaal D oplevert. Alleen goals tellen begrenst groei door de oude5-doellimiet; alleen positieve heapitems tellen negeert overlappende footprints en transport. Een adapter aan de getoonde klassecall hoeft voor dit antwoord geen volledige scheduler of pathfinder te reconstrueren.

## Bewijs en overdracht

**B:** originele robotcom.dll SHA2563025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44, imagebase20000000, timestamp37b894e7; robotcom.map passend/gecontroleerd door het bestaande hulpmiddel. Eén gerichte nieuwe disassembly van Desired/Supplemental/Update; overige bronnen hergebruikt. **T:** aanwezige AIP-lijsten/klassegewichten. **Interpretatie/ontwerpcontract:** D_t-quotaadapter hierboven, nog niet gebouwd. **Runtime:** oude T60-voorraden zijn bestaande waarnemingen; geen nieuwe activatie-, snelheids- of transportwinst bewezen. AAIP marinequota zijn lessen uit bestanden, geen bewijs van dynamische nuttigheid.

Ontwerper krijgt een concrete invoegroute met intacte oorspronkelijke actual-/priorityopbouw en de precies ontbrekende G-/compatibiliteits-/reservationproducer. Daarmee is deze gerichte fase-A-taak afgerond. Volledig doelconforme B4-uitvoering vraagt die producerbinding vóór C; de route is geen vrijgave voor een willekeurige scorecount of nieuw vast voorraadgetal. Overige scheduler-/pad-/transport-/savevragen blijven backlog totdat een concrete ingreep ze nodig heeft.
