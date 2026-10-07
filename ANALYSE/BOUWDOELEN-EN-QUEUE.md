# Bestaande bouwdoelen en queueacceptatie

Fase A, 5 oktober 2026. Afgebakende analyse van de gewone CTP I-AI; geen wijzigingsvoorstel, spelstart of gameplaytest. Dit pakket verbindt effectieve AIP-lijsten met doelcreatie, bieding, uitvoering en het engineverzoek. De volledige militaire planning en alle legacygebouwutilities vallen buiten de bewezen subketen.

## 1. Hoofdbevinding

De AI gebruikt bouwlijsten al. Een lijst vormt geen vooraf ingeleverde complete bouwqueue: een geschikte stad krijgt per toepasselijke categorie een doel voor **het eerste geschikte lijstitem**. Die doelen concurreren met unitdoelen. Bij uitvoering wordt opnieuw gecontroleerd of de queue leeg is; daarna gaat één concrete aanvraag naar de engine.

Lijstvolgorde en lijstgewicht hebben verschillende functies. Volgorde kiest de kandidaat binnen een categorie; het gewicht beïnvloedt vervolgens de concurrentie met andere doelen. Een hoger Labyrinthgewicht laat de AI daarom niet automatisch een eerder geschikt Stonehenge-item overslaan. Gewicht nul betekent evenmin automatisch negeren: een positieve basisprioriteit blijft bestaan.

Bewijs: [AIP-doelcreatie en uitvoering](BINAIR/build-goals-queue-ai-core.txt), [parser en lijstvolgorde](BINAIR/build-goals-queue-ai-list-parser.txt), [33 offline controles](BINAIR/build-goals-queue-controls.json). De controles gebruiken synthetische toestand; toelating, allocation/planner en echte queueacties zijn waar nodig expliciet geregistreerde stubs.

## 2. Bewezen aanroepketen

`FSCompeteForAllMovement::Execute2002b030` werkt squads/planner bij en roept op **2002b0d8 AIP::Update20066b70** aan. Daarna volgt op **2002b0ea Scheduler::Allocate_Troops_And_Execute_Tasks2006f520**. Dat verbindt de AIP-vraag met de gezamenlijke planner; dit zijn geen afzonderlijke direct uitgevoerde productiequeues. Zie [movement/update-aanroep](BINAIR/build-goals-queue-ai-legacy-and-unit.txt).

De reeds bewezen unitroute telt bestaande en queued units, berekent de gewenste aantallen en maakt doelen voor positieve tekorten. Een vaste negatieve settlerquota is een gewenste gelijktijdige voorraad, geen verplicht productieblok vóór alle gebouwen. Na vestigen verdwijnt een settler uit de voorraad en kan opnieuw een tekort ontstaan. Zie [ruimte, quota en transports](RUIMTE-BUREN-TRANSPORT.md).

De gebouwroute is **Update_Building_Build_Lists200668e0 → Update_City_Distributions20065e40 → Update_City_Needs200660c0 → Add_Supplemental_Building_Build_Goal200664d0**. Zie [verdeling en categorieverzoeken](BINAIR/build-goals-queue-ai-distribution.txt), [selectie](BINAIR/build-goals-queue-ai-selection.txt).

De effectieve AIP staat op `AiMain+94 → Planner+20`. Ontbrekende onderdelen van een later geladen AIP blijven behouden; aanwezige gebouw-/wonderlijsten vervangen de betreffende hele categorie. Het huidige profielnaamveld bewijst dus niet welke complete lijstenset actief is. Zie [AIP-laadwerking](AIP-LAADWERKING.md).

## 3. Stadselectie en lijstkandidaat

De distributie maakt verschillende, oplopend gesorteerde stadarrays. De sorteersleutels komen uit CityAgent+2c, +4c, +54, +68 en +c0. De afzonderlijke arrayroutine **Add_Data20066e60** voert een vergelijking op de integerkey uit; dit is geen nieuw gewogen tilekwaliteitssysteem. `Update_City_Needs` gebruikt rang **i/N**: nul voor de eerste positie en maximaal `(N−1)/N`. Zie [distributie](BINAIR/build-goals-queue-ai-distribution.txt), [sortering en CityAgent-invoer](BINAIR/build-goals-queue-ai-scheduler-inputs.txt).

Wonder-/transport-/productie-/defensiecategorieën gebruiken de productiegerichte array en testen de rang tegen hun threshold. Science gebruikt de array met sleutel **CityAgent+68** en vergelijkt op **200662f4–20066321** dezelfde rang met `Science_List_Threshhold`, werkelijk gebonden aan AIP+280 door **200615c2**. Die science-input komt via Player+84→527d50 uit de stadswaarde +2c; dit is de bestaande stadswetenschap, geen inspectie van drie mogelijke voedselvakjes of een expliciete science-stadsrol. Zie [bindings](BINAIR/build-goals-queue-engine-tables.json), [engine-invoer](BINAIR/build-goals-queue-city-input-bindings-v3.txt), [thresholdparser](BINAIR/build-goals-queue-ai-priority-binding.txt).

De wonderthreshold is AIP+250, parser **20061319**. Op **20066103–20066127** moet `i/N ≥ threshold`, tenzij `HasLotOfStoredProduction` de uitzondering toestaat. Met de standaardthreshold0.8 kan een enkele stad met rang0 hierdoor niet via de gewone rankroute een wonderlijstdoel krijgen. De opslaguitzondering vereist tegelijk **stock≥500**, **productie≥30** en **integer(stock/productie)≥5**; zie **2001ca20–2001ca71** en de vijf echte predicatecontroles. Dit is een concrete uitzondering, geen algemene reservering van een vroege wonderstad.

Growth en happiness gebruiken anders gerichte rang-/behoeftevoorwaarden; gold en growth hebben bovendien categoriegebonden effect-/kostenlogica. De volledige semantiek van hun branchinputs is hier niet opnieuw gebonden. Zij mogen niet als identieke sciencefilters worden voorgesteld.

`Add_Supplemental_Building_Build_Goal` doet vervolgens:

1. **200664f9–20066500:** geen doel als GetQueueLen>0.
2. **20066513–20066545:** doorloop lijstrecords van32bytes in opgeslagen volgorde; geen sortering op hun doublegewicht.
3. Voor gewone gebouwen: **Can_Build_Building2001fa60**, daarna **Already_Has_One2001fa40**, op **200666b1/200666c4**.
4. Wonderitems hebben marker−1 en krijgen afzonderlijke WonderTable-/bouwtijdchecks; endgame−2 en capitalization−3 hebben eigen branches.
5. Voor de eerste geschikte kandidaat: doelconstructie **20048e00**, **Scheduler::Add_Single_Plan20071710** en **Planner::Add_Single_Plan_Goal2006ef20**, op **20066869/2006688f/200668a1**. Vervolgens stopt de volgende iteratie zodra de gevondenflag waar blijft.

De vijf oorspronkelijke lijstloopcontroles bewijzen: eerste geschikte item wint ondanks een later veel hoger gewicht; onbouwbaar of reeds aanwezig item wordt overgeslagen; geen geschikte kandidaat geeft geen doel; bezette queue geeft geen doel. Eligibility en planner zijn hier mocks, zodat dit geen volledige game-initialisatie bewijst.

## 4. Prioriteit en concurrentie

De parser schrijft `build_troops_priority` naar **AIP+8**, `build_buildings_priority` naar **AIP+10**, `fzwonder_priority_modifier` naar **AIP+1e0**. Door Planner+20 zijn de runtimevelden respectievelijk +28, +30 en +200. Die laatste koppeling is belangrijk om dezelfde schaal te vergelijken. Zie [parser, constructors en scheduler](BINAIR/build-goals-queue-ai-priority-binding.txt).

| Doel | Oorspronkelijke formule | Implementatie |
|---|---|---|
| Goal_Build_Supplemental | build_troops_priority + class/doelgewicht | 20049b30–20049b4e |
| Gewoon Goal_Build_List | build_buildings_priority + aangepast lijstgewicht | 200494c6–200494d0 |
| Wonder Goal_Build_List | fzwonder_priority_modifier + lijstgewicht | 2004946d–20049483 |
| Endgame / capitalization | eigen basis + lijstgewicht | 2004948d–200494c3 |
| Legacy GoalBuilding | fzbuild_priority_modifier × opgeslagen payoff | 20046260–20046281 |

Voor de standaardbasissen resulteert een unitgewicht10500 in **20010500**, een sciencegebouw7950 in **20007950**, een wonder10000 in **20007500**. Dit zijn gecontroleerde formulevoorbeelden met synthetische inputs, geen voorspelling dat iedere effectieve profielcombinatie dezelfde getallen heeft.

**Goal_Build_List::Compute_Matching_Value20049120** levert zijn rawprioriteit voor een squad met een stad; anders−1e9. Supplementalunitmatching **200497c0–20049950** zoekt een geschikte stadsagent en voert **PretestContructUnit2001da60** uit; ook hier volgt bij geschiktheid het opgeslagen doelgewicht als matchwaarde. Scheduler **20072721** vraagt die matchwaarde op; **20072740–20072757** gebruikt floor(matchwaarde) plus een kleine schedulerterm (`Scheduler+24 ×1e−5`) voor zijn plankey. De planpool en boom houden die keys bij. `Match_Resources_One_Pass20073970` haalt plannen uit die boom, controleert geldigheid/strength en roept **Execute_One_Task200733b0** aan op **20073ca0**. Zie [matching/sortkey](BINAIR/build-goals-queue-ai-priority-binding.txt), [resourcepass en uitvoering](BINAIR/build-goals-queue-ai-scheduler-inputs.txt).

Deze verbinding bewijst gezamenlijke concurrentie en de keyvorming. Alle boomsorteer-, tie-, herplan-, sterkte- en limietbranches zijn niet afzonderlijk geëmuleerd; een absoluut universeel 'hoogste getal bouwt altijd' is daarom te sterk.

## 5. Bouwtijd, sciencegebouwen en Labyrinth

Voor gewone lijstgebouwen is **PretestBuildingBuildTime2001d9f0** een **zachte gewichtstoets**. Zij schat een integer bouwtijd uit `(kosten+0.5−stock)/productie` bij positieve productie, anders uit kosten+0.5; succesvol wanneer strikt kleiner dan `max_build_building_rounds`. Als de toets faalt, wordt het item niet automatisch verwijderd. Op **200667d1–20066827** volgt bij verhouding `r=EstimateRoundsToBuildBuilding/max_build_building_rounds`: bij r<2 gewicht×0.5, anders gewicht/(r+8). Sciencecategorie heeft hier geen aparte gebouwbonus-/scientistberekening.

Voor units is het bouwtijdcriterium **hard**: **2001db20–2001db33** verlangt tijd<`max_build_unit_rounds`, daarna CanBuildUnit. Een groter settlertekort maakt een slechte producer daardoor niet vanzelf een geschikte settlerbouwer. Deze pretest is een afzonderlijke schakel naast voorraadquota en vestigingslocaties.

Voor wonders is de bouwtijdtoets eveneens **hard**, met tijd≤`max_build_wonder_rounds`: **2001db99–2001dbc8**. Cache+1f0 moet negatief en flag+1f8 nul zijn. De vijf controles bewijzen inclusie op de limiet, uitsluiting erboven, het effect van stock, blokkade door een incumbent en fallback bij nulproductie. De kostengetter en geïmporteerde CRT-truncatie zijn expliciete externe vervangers; de originele x87-berekening en vergelijking draaien werkelijk.

`CanInsertWonderGoalForCity2000f7a0` controleert ook wereldbeschikbaarheid, een via WonderDB+34 opgevraagde voortgangswaarde tegen0.3, de opslaguitzondering en lokale WonderBlg-beschikbaarheid/state. De exacte betekenis van die enginevoortgangsgetter en alle stateovergangen blijven open; noem0.3 daarom niet zonder verdere binding een bewezen 'rivaal30% klaar'-regel.

De originele defaultwaarden zijn15/20/50 voor building/unit/wonder. De precieze engine-tokennaam van Labyrinth is **WONDER_LABRYINTH_OF_THE_MINOTAUR**, inclusief bestaande spelling. Zie [default](../CTP-og/ctp_data/default/aidata/AIPs/default.aip), [scienceprofiel](../CTP-og/ctp_data/default/aidata/AIPs/scimany.aip).

OG scimany zet Stonehenge9000 vóór Sphinx4000 vóór Labyrinth10000. Wanneer een eerder item geschikt blijft, biedt deze lijst dat item aan. Een reeds zichtbaar wondergewicht10000 bewijst dus geen gewenste Labyrinthvoorrang. Evenmin bestaat in deze onderzochte route een expliciete uitzonderingsstad die tijdens de settlerfase voor Labyrinth wordt gereserveerd.

## 6. Uitvoering en echte enginequeue

`Goal_Build_List::Execute_Task20049220` controleert op **20049389–20049391** opnieuw QueueLen<1. Daarna roept de markerroute EnqueueBuildWonder/EnqueueBuildBuilding aan op **200493b0/20049418**. Supplementalunituitvoering **20049980** voert zijn pretest opnieuw uit en vraagt **EnqueueArmy2001c3d0** aan op **20049af2**. Een succesvolle doelkeuze is dus nog geen enqueuebewijs.

Alle drie gebruiken **Player+50 → echte vtable744660 →527850 →Player4c81d0**:

| Soort | Klasse | AI enqueue | Playerbranch | CityData enqueue |
|---|---:|---|---|---|
| Unit | 1 | 2001c3d0 | 4c8266 →4dc220 →4e22a0 | 498970 |
| Gebouw | 3 | 2001d260 | 4c8298 →4dc250 →4e22c0 | 498b00 |
| Wonder | 9 | 2001d2a0 | 4c827f →4dc280 →4e22e0 | 498c90 |

Werkelijke dispatchtabellen zijn apart uit dezelfde engine gelezen: [tabelwaarden](BINAIR/build-goals-queue-engine-tables.json), [verzoekroute](BINAIR/build-goals-queue-engine-request.txt), [CityData en queuetoelating](BINAIR/build-goals-queue-engine-admission.txt). Civctp.map is hierbij niet gebruikt.

Gebouwen worden opnieuw op **49d6a0** toegelaten; wonderenqueue controleert globale beschikbaarheid en WonderDB **4745a0**, plus record/contextbranches. Vervolgens wordt klasse/type/kosten aan **Queue491290** gegeven. De queuetoelating **4910c0** heeft eigen klasseswitch: units herhalen CanBuildUnit; gebouwen herhalen **4ddcc0** en zoeken duplicaten; wonders zoeken hetzelfde wonder in de bestaande nodes en blokkeren een nietlege queue. De volledige tech-/gov-/locatievoorwaarden van49d6a0 en4745a0 zijn niet in dit pakket semantisch benoemd.

De zes enqueueproeven registreren de daadwerkelijke AI-argumenten1/3/9 en testen acceptatie/failure afzonderlijk. CityAgent+1f0/+1f4 krijgt alleen bij een nietnul engineresultaat het nieuwe type/klasse. Bij wonder wordt **SetIamBuilding2000f8d0 echter vóór** het engineverzoek aangeroepen; de getoonde faalroute draait die flag niet terug. Latere resynchronisatie van die wonderflag blijft een open branch. De uitvoerder van een lijstgebouw slaat het doelID bovendien buiten de void enqueuefunctie op; dat is geen onafhankelijke bevestiging van engineacceptatie.

Unitvoltooiing, populatiekosten en AIPopCheat zijn reeds afzonderlijk bewezen in [voedsel, groei en kolonisten](VOEDSEL-GROEI-EN-KOLONISTEN.md). Een geaccepteerde queueaanvraag is geen bewijs van voltooide eenheid of gebouw.

## 7. Legacygebouwdoelen en AAIP-lessen

Naast lijstdoelen bestaat **CityAgent::InsertBuildingGoals2001d1c0 → BuildingAgent::CanConstructBuilding2001b0c0/CalcPayoff2001b100 →GoalBuilding20045f10**. Deze route is werkelijk verbonden met de gewone movementpass: Execute2002b0be roept FindAllGoalPos2002b110 aan; diens stadsloop roept op **2002b194** InsertBuildingGoals aan voor lege queues. Ook RegisterMyAddCity heeft een directe call op200047c4. De daarnaast aanwezige InsertCityBuildGoal2002b300 heeft geen directe xref in deze scan; die naam is niet nodig om bereikbaarheid te bewijzen. Zie [werkelijke entry](BINAIR/build-goals-queue-ai-legacy-entry.txt), [xrefcontrole](BINAIR/build-goals-queue-ai-legacy-xrefs.txt).

Cruciaal: InsertBuildingGoals doorloopt niet alle gebouwen. Zij gebruikt uitsluitend **CityAgent+214 plus8**, dus BuildingAgent-record1, en construeert het doel met gebouwtype1 op **2001d22a**. MemInit maakt8-byte records en zet hun type via2001b4a4; zie [recordopbouw](BINAIR/build-goals-queue-ai-building-records.txt). CalcPayoff levert101 wanneer BuildingDB+3c waar is, anders0 bij nietnul state en100−type bij state0. De exacte engine-tokenbinding van record1 en slot3c wordt hier niet als afgerond geclaimd. Het doel heeft een andere payoff×modifierformule en een aparte BuildTaskSolution, inclusief een gedeelde staatsflag voor de special-buildingbranch. Dit is geen algemene alternatieve sciencegebouwlijst. Zie [legacyfunctie](BINAIR/build-goals-queue-ai-legacy-and-unit.txt), [doelinsertion en tasksolution](BINAIR/build-goals-queue-ai-core.txt).

Het eerder gevonden **ActionBidBuildGoalBuilding20020540** vraagt effecten op maar roept zichtbaar alleen UtilityBlgCapitol en WeightTimeToBuild aan. Het bestaan van UtilityBlgSilo of een andere naam bewijst dus niet dat de gewone gebouwkeuze die utility gebruikt. Zie [bestaand bodbewijs](BINAIR/food-growth-building-bid.txt).

De AAIP-scimanylijst wijzigt Academy7950→8980 en plaatst Library8970 vóór University7950; OG zet University vóór Library en geeft beide7950. Dit betekent respectievelijk een sterker aangeboden sciencebod en een andere kandidaatvolgorde. Het is code-/configuratiebewijs van verschillende effecten, geen hier gemeten winst. Labyrinth10000 en de standaardbouwtijdwaarden blijven in de bekeken profielen gelijk. Zie [AAIP-scimany](../CTP-AAIP/ctp_data/default/aidata/AIPs/scimany.aip), [AAIP-default](../CTP-AAIP/ctp_data/default/aidata/AIPs/default.aip), [bredere AAIP-lessen](AAIP-LESSEN.md).

## 8. Verificatie en resterende essentiële vragen

Robotcom.dll SHA256 **3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44**, timestamp37b894e7, imagebase20000000; passend bij robotcom.map. Engine SHA256 **b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79**, timestamp37d6f702, base400000; engine-map past niet. De bewijsbestanden vermelden deze identiteit.

[Controleer-Bouwdoelen.py](../PROEVEN/Controleer-Bouwdoelen.py) voert **33/33** controles uit: zes rawformules zonder mocks, twaalf enqueueargument/cachechecks met expliciete externe callbacks, vijf lijstloopchecks met eligibility/goal/plannerstubs, vijf opslagpredicates zonder mocks, vijf wonderbouwtijdbranches met kosten-/CRT-vervangers. Geen echte queue, volledige scheduler, profielparse of spelbeurt wordt nagebootst.

Voor de volgende analyse zijn nog wezenlijk:

- Het volledige schedulerselectie-/tie-/limietgedrag en eventuele andere militaire buildtaskrequests, zodat priorityvoorbeelden niet te ruim worden uitgelegd.
- Alle enginevoorwaarden voor specifieke sciencegebouwen en Labyrinth, plus heropbouw/terugdraaien van wonderflags na geweigerde enqueue en na save/load.
- De engine-tokenbinding van legacyrecord1/BuildingDB+3c en zijn volledige matching/stateafhandeling; de normale bereikbaarheid en selectie van alleen record1 zijn wel bewezen. Geen alle-utilities-actiefaanname.
- De afzonderlijke vraag/transport-/veiligheidsketen die vestigen over zee of naast rivalen mogelijk maakt; een hogere settlervoorraad lost die ontbrekende contextbeslissing niet op.

De huidige subketen is voldoende onderbouwd om de bestaande bouwlijsten, quota, thresholds en verzoekroutes juist te begrijpen. De brede functionele fase A is hiermee niet afgerond.
