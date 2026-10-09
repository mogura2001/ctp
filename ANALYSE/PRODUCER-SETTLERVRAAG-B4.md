# B4-P — kandidaatcapture en minimale directe-landproducer

8 oktober 2026, 16:24 Europe/Amsterdam. Gerichte fase A na [B4-ontwerp](../ONTWERP/DYNAMISCHE-SETTLERVRAAG-B4.md), uitsluitend diens MinimaleGproducerterugvraag. Brede A en H3-activatie blijven afgerond. Geen producer/observer/emulator gebouwd, geen spelstart, GUI, livegeheugenactie of game-/binarywijziging.

## Uitkomst

**De integratieroute is concreet:** begin een eigen vluchtige planronde vóór de bestaande movementcleanup, kopieer de groundkandidaten direct na **2007abac**, en maak het getypeerde plan af **vóór 20066b81** nadat de oorspronkelijke actualtelling is vernieuwd. Houd het plan onveranderlijk tijdens Desired/Supplemental en ruim het na dezelfde AIPUpdate op. Er is geen machinecodeblokkade waardoor deze ene planronde geen eigen Gproducer kan krijgen.

Een bestaande complete Ginput is er in deze route niet. **Nieuwe logica is noodzakelijk** voor nuttigheid/gezamenlijke rolplannen, locatie- en claimdeduplicatie, typering, veilige directe paden en verdeling van bestaande/productie/nieuwe voorraad. Die logica kan op de bewezen capture-/refreshpunten worden ingevoegd; volledige reconstructie van scheduler, padzoeker of saves is daarvoor geen voorwaarde.

De minimale eerste variant ondersteunt alleen expliciet gevalideerde gewone landsettlers, eigen/bouwbare vertrekpunten en daadwerkelijk gevonden veilige landpaden. **Transport-backed slots blijven uit; transportstatus is UNKNOWN/NEEDS_TRANSPORT, nooit een positief Gslot zonder bewijs.** B4b moet later beschikbaar/pending carrier en techvragen uitwerken; het kleine-eilanddoel blijft onderdeel van de eindopdracht. Evenmin vervangt dit productie-onlykenmerk science-/monopolylocaties of B3/B5.

Voldoende voor een concreet direct-landontwerp. Geen verdere algemene analyse nodig; implementatie-, host-/ABI- en runtimechecks volgen pas na dat ontwerp.

## Huidige beslisketen en exact capturepunt

Machinecodebasis: robotcom SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, timestamp `37b894e7`, imagebase `20000000`; passende robotcom.map. Engine SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp `37d6f702`, base `400000`; civctp.map niet gebruikt. VAs hieronder moeten tegen echte modulebasis/fingerprint worden gebonden.

Movement **2002b030** doet vóór nieuwe locatievorming:
- **2002b079** Scheduler::Update_Squads;
- **2002b08a** Scheduler::Clean_Up;
- **2002b09b** Planning_Status_Reset;
- **2002b0a7** Planner::Update_Map: eigen rijk, threats, vijandelijk rijk, explored territory en power worden vernieuwd;
- **2002b0be** FindAllGoalPos;
- **2002b0ca** Planner::Update_Squads;
- **2002b0d8** AIP::Update;
- **2002b0ea** Allocate_Troops_And_Execute_Tasks.

Bewijs: [bestaande movementcode](BINAIR/build-goals-queue-ai-legacy-and-unit.txt), [gerichte pretests/refresh](BINAIR/settler-producer-b4-pass-pretests.txt).

**Belangrijk:** nieuwe matching/executie ligt ná AIPUpdate. Een snapshot vóór Desired kan daarom niet doen alsof de huidige nieuwe GoalSettle-lijst al volledige definitieve toewijzingen bevat. Oudere assignments kunnen al vóór FindAllGoalPos zijn losgemaakt of verwijderd; behoud ervan vraagt een vroeg kopiemoment en daarna verse validatie.

InsertSettleGoals zet eigen AiMain/grondlaag en kopieert het statische masker vóór GroundBuildSettleTree. **2007abac** roept de volledige groundopbouw aan; hervatten op **2007abb1** gebeurt vóór de beperkte doeliteratie **2007acb8–c5 / 2007acf3** en vóór heap-pops en tijdelijke radius1-maskerwijzigingen. Daarmee levert een calladapter die eerst de originele Groundfunctie uitvoert, en dan kopieert, precies de benodigde vóór-goallimietdekking. Niet InsertBestSettleGoal éénmaal tellen: die wordt alleen binnen de oude limiet aangeroepen.

Bewijs: [H1-callcontext](BINAIR/score-hook-h1-callcontext.txt), [selectiefilters](BINAIR/locatie-selectie-ingreeppunten.txt).

### Vier kleine technische adapters plus de reeds ontworpen quota-adapter

| Site / volledige preimage | Adapterverantwoordelijkheid | Oorspronkelijk ABI / eigenaar |
| --- | --- | --- |
| **2002b079**, `e882550400` | Begin generatie, invalideer vorig plan; kopieer nog bestaande gevalideerde assignmenthints vóór originele SchedulerUpdate/cleanup | thiscall ECX=Scheduler, geen stackargument, EAX-resultaat behouden; eigen AiMain via Scheduler+468 |
| **2007abac**, `e8cff4ffff` | Originele GroundBuildSettleTree uitvoeren, daarna volledige kandidaatkopie; geen pop/heap/maskerwrite | thiscall ECX=AiMap, AiMain op stack, ret4; check AiMain+80=AiMap en actuele planowner |
| **20066b81**, `e81aeeffff` | Na Update_Actual_Units het eigen plan valideren/finaliseren; daarna originele Desired uitvoeren | thiscall ECX=AIP, geen stackargument; AIP+800=owner, owner+94→Planner, AIP=Planner+20 |
| **2002b0d8**, `e893ba0300` | Originele AIPUpdate omgeven met passscope; na return eigen buffers/plan invalideren/vrijgeven | thiscall ECX=AIP, geen stackargument; Desiredadapter mag uitsluitend tijdens deze scope activeren |

[Preimages en buffer-ABI](BINAIR/settler-producer-b4-hook-abi.txt) bevestigt alle vijf bekeken callsites als één volledige vijf-byte call; de vijfde is de bestaande FindAllGoalPoscall2002b0be. Geen bytes toegepast. Alle adapters bewaren vereist register-/stack-/x87gedrag en roepen het originele doel eenmaal aan. Geen proloogpatch/trampoline nodig voor deze route.

Vier sites zijn een concrete minimale route met behoud van oude assignmenthints, prelimitdekking en actual-before-desired. Als ontwerp historische assignmenthints geheel als UNKNOWN uitsluit, kan de vroege hook worden verplaatst/vereenvoudigd, maar dan is 'bestaande assignments behouden' niet bewezen. Laat de ontwerper die keuze expliciet maken.

Nieuwe passopslag kan bounded eigen allocatie zijn met ownerpointer, civ, eigen generatie, statuses en gekopieerde waarden. Zij hoeft geen nieuw engineveld of saverecord te krijgen. Begin bij iedere echte movementpass; consumeer uitsluitend binnen dezelfde AIPUpdate, daarna ongeldig. Raw pointers alleen voor dezelfde gecontroleerde callscope. Bij gewijzigde owner, ontbrekende capture, unsupported scope of gedeeltelijke capture vóór Desired: volledige B4pass niet activeren, zoals B4-ontwerp vereist.

## Wat de groundkopie dekt en mist

AiMain+80→AiMap. Heapobject begint op **AiMap+58**: capacity+5c, count+60, pointerarray+64. Ground zet count eerst0 en voegt een nullsentinel toe; gewone entries staan **1..count−1**. Ieder AiCellPtr bevat signed16 x/y plus heapindex op+4; grondlaag is0. Kopieer xyz/identiteit en zo nodig score naar eigen entries; nooit AiCellPtrpointer of heapindex als duurzame reservering gebruiken.

Ground test het statische masker, zonder water-settle eventueel World+3c, en afstand tot eigen rijk tegen **AiMap+68**. Deze distancehorizon en de limiet rond **32765 enumeratiekandidaten** zijn al filtering vóór Gcapture. Ze worden door de nieuwe producer niet automatisch ongedaan gemaakt. Bij cap/truncatie of niet-volledige reads: INCOMPLETE/UNKNOWN, geen 'geen ruimte'. Een lege volledige groundheap betekent geen kandidaat binnen deze bestaande zoekscope, niet geen toekomstige ruimte elders.

De array is een heap, geen volledig gesorteerde lijst. Nieuwe logica moet gekopieerde kandidaten deterministisch ordenen volgens dezelfde geaccepteerde score/tievoorwaarden, of een eigen gespecificeerde volgorde gebruiken. Niet de array-index als bestaande globale prioriteitsrang presenteren. H1/H3-formule mag tijdens deze berekening niet door eigen reservations veranderen; sorteer eerst, selecteer conflictvrije plannen daarna.

Naast het statische masker missen groundentries nog de latere endpointchecks. InsertBest gebruikt **World+78 op2007a93b**, met World, positie plus negen afzonderlijke outputpointers, en **2007a93e–95b** wijst buitenlandse aanwezige eenheden/steden af. ABI-correctie bij ontwerp/rootreview8okt16:33: de bestaande dump2007a901–2007a93b pusht negen locals (-24,-28,-2c,-30,-14,-34,-38,-1c,-18), vervolgens positie en World; de eerdere tekst zeven was onjuist. Neem dit oorspronkelijke output-/ownercontract exact over; behandel de outputvelden niet als een zelfbedachte volledige dreigingsscore. **Continents::GetContinent2007e030** geeft ID en land/watercategorie; tel alleen grondland. De oude continentgoalquota en radius1-writes zijn uitvoeringstakken, geen Gdefinitie.

Geen new goal aanmaken, InsertBest callen, of de originele heap destructief leegtrekken om G te meten.

## Dekking per verplicht snapshotveld

| Verplicht veld | Bestaande concrete read / huidige werking | Minimale nieuwe producerlogica |
| --- | --- | --- |
| Owner/generatie/status | Scheduler+468, AiMain+20/+80/+94, AIP+800; één movementvolgorde | Eigen generation/state-machine: START→CAPTURED→VALIDATED→IMMUTABLE→INVALID; mismatches geen B4activatie |
| Unieke locatie | Gekopieerde signed16 x/y, z0; Player+14 voor tweede strategische coördinaten | Canonical inputidentiteit kiezen; gewrapte/verschillende alternatieven dedupliceren en coördinatenruimtes niet mengen |
| Juridische endpoint | Statisch masker, World+78/ownerchecks, Player+34 type-settlequery | Op gekopieerde entry opnieuw verse endpointtoelating doen; obsolete/bezette slots verwijderen |
| Nuttigheid/timing | H2/H3 levert beperkt fysiek productionplan; gewone Bscore is slechts ranking | B3/B5/rolpredicate levert expliciet NOW/LATER/UNKNOWN plus noodzakelijke werkplekken; geen score>0=nuttig |
| Gezamenlijk stadsplan | Native goalvorming verwijdert radius1; H3 reserveert geen bergen/food | Eigen conflictvrije subset en footprintclaims; één onmisbare tile niet tegelijk aan twee NOWplannen beloven |
| Typecompat/effective scope | AIP+7b0/+7bc, klasse+0c lijst; Choose_Unit_From_List20065900→UnitDB+14; Player+34 pertype/positie; CityAgent::CanBuildUnit2001f330 | Eén preview/vooruitpass van daadwerkelijke klasselijsten, zonder quota te muteren; expliciete ondersteunde ordinary-landtypes; laatste geschikte selectie behouden; iedere settlerklasse afgedekt of hele pass uit |
| Bestaande assignment | Goal+8/+30/+34 en Squad+5c/+60, reciprocal setter/detach bewezen | Vóór cleanup kopiëren als hint; na refresh op ID/owner/positie/type/path opnieuw valideren; verlopen claim geen reservation |
| Bestaande/in-productie units | AiMain+90 ArmyAgents, armyID+0c, actuele types via GetUnitCount2001a970/GetUnitTypeByNumber2001a980; Actual op AIP+7c8; What_Army_Am_I_Building2001cd50 | Eigen claimset per army/unit en per CityID/productieclaim; één claim op één bestemming; ambiguous/busy/cargo geen gecertificeerde matching; actual nooit tweede keer aftrekken |
| Veiligheid | Planner+a70→Strategic_Map; Update_Map ververst threats vóór capture; Get_Threat20083b10; World+54 eigenaar, World+78 bezetting | Eigen expliciete safetygate voor endpoint én alle padpunten, in juiste coördinatenruimte; ontbrekende/unknown beoordeling geen slot; bestaande threat0 is huidige waarnemingsmaat, geen absolute toekomstige veiligheid |
| Direct land | AiMain+34 queryslot+0c, native virtual-typepad met eigen buffers; hieronder gebonden | Per compatibel bestaand vertrekpunt of bouwbare eigen stad een echt pad zoeken; uitsluitend z0/landpaden zonder carrier/ruimteactie en met veilige punten crediteren |
| Beschikbaar transport | Planner+a74, CanTransport/capaciteit/utility zijn afzonderlijke gedeeltelijke bewijzen | Eerste variant geeft nul transport-backedslots. Geen a74, continentpretest of aanwezig schip als slotbewijs |
| Pending carrier/tech | Bestaande transportketen registreert soms tekort, enqueuet daar geen carrier | NEEDS_TRANSPORT/UNKNOWN apart rapporteren; concrete carrier/techplanning in B4b, geen fictieve beschikbaarheid |
| G/D_t | Geen bestaande volledige veldread | Eigen disjuncte destinatieslots/typekaart; D=min(Gdirect,N−C); original Actual en native deficit/priorityopbouw ongewijzigd |

Dat ontwerp predicates, deduplicatie en matching moet toevoegen is een uitvoerbare nieuwe-logicaroute, geen reden om eerst iedere enginefunctie te reconstrueren. Een niet-bestaande complete rolclassifier is wel een expliciete B3/B5-afhankelijkheid voor volledige gameplayactivatie. Een beperkte productionpredicate moet als beperkte proefscope worden benoemd; zij voltooit niet de overige stadsfuncties.

## Assignment, reservation en lifetime

[Setter/detachbewijs](BINAIR/settler-producer-b4-assignment.txt):
- Set_Goal20075476–8b schrijft **Squad+5c=Goal**, **Squad+60=GoalID**, **Goal+30=SquadID**, **Goal+34=Squad**.
- Detach_Squad200686a3–b9 wist Goal+34/+30; Detach_Goal200754b3–d7 wist Squad+5c/+60.
- De eerdere [H3-lifetimeanalyse](ACTIVATIE-VESTIGING-H3.md) bewijst cleanup/delete en de Planner-IDtabel. Neem daar geen oude pointers over naar een volgende pass.

Deze reads beschrijven een actuele reciprocal assignment, niet een globale locatiesreservering of exclusieve berg-/foodclaim. Een productiestad bezit bovendien geen bewezen bestaande bestemmingsID in What_Army_Am_I_Building: een productieclaim heeft pas een bestemming als de nieuwe producer die toekent.

Minimaal nieuw mechanisme: claims op stabiele kopieën van GoalID/locatie, army/unit-ID en CityID+actueelproductietype, met owner/generatie. Revalideer een historische claim tegen de huidige werkelijkheid. Bij onvolledig squad→individuele-settlerverband geen gedekte-opdrachtclaim verzinnen: label UNKNOWN en maak geen dubbele credit. Maak vervolgens eigen één-op-éénmatching over de gevalideerde bestaande en queued types/vertrekpunten; nog vrije slots krijgen de werkelijk geselecteerde bouwtypes. Dit zijn **producerclaims**, geen toegepaste Schedulerassignments. Zij mogen de native taken niet live wijzigen.

De oorspronkelijke Actual_t omvat ook units die voor deze nieuwe mapping onbruikbaar blijken. Het B4-ontwerp kiest conservatieve ondervraag in dat geval; de producer mag die oorspronkelijke teller niet wissen/verkleinen om alsnog vraag te forceren. D_t blijft voorraad inclusief doeldekking; Supplemental trekt actual eenmaal af.

## Gebonden directe-landpadquery zonder fake ArmyAgent

ArmyAgent::FindPath20017ef0 muteert onder meer **ArmyAgent+24/+28/+30/+2c/+88**, en kan UseOldPath/g_transcontext gebruiken. Haar blind voor ieder toekomstig slot uitvoeren zou de echte legerpadcache veranderen. Gebruik voor de nieuwe producer de onderliggende padinterface met eigen outputs.

[Bestaande AI-init](BINAIR/terrain-food-ai-interface-init.txt) **20001b41–44** bindt GameState+24 aan **AiMain+34**. [Echte enginebinding](BINAIR/settler-producer-b4-engine-reads.txt):
- GameState-vtable744420+24→**525fb0**, leest GameState+c.
- Constructor524c70 roept **582290 op524d21** aan en schrijft resultaat naar GameState+c op524d2f.
- [Padconstructor](BINAIR/settler-producer-b4-path-constructor.txt) zet uiteindelijk **vtable746220**, bewaart eigen enginePlayer op **+7c**.
- [Queryslot](BINAIR/settler-producer-b4-path-query.txt) **746220+0c→5826a0**, eindigt met **ret50h**, integer EAX. Mode1branch **58279c–f9** haalt het echte UnitRecord voor het gekozen type op en leest movementbits en movementwaarde. Mode0 vraagt een concreet leger; mode2 gebruikt andere invoer. Gebruik voor de minimale toekomstige ordinary-typecheck mode1.

De originele vertegenwoordigde-unitcaller **2001808b–d1** staat in [gerichte reads](BINAIR/settler-producer-b4-reads.txt). Zij geeft twintig vier-byte slots door. Op de stack na het retouradres:

| Argumentnummer | Betekenis uit caller/engine |
| --- | --- |
| 1..7 | Padinterface, callback, armyID, mode, type, sourceMapPointData*, destinationMapPointData* |
| 8..11 | Capaciteitref, pathpointerref, countref, eigen extra pathresultslot |
| 12..15 | Twee oorspronkelijke type/contextflags, callerflag, nulslot |
| 16..20 | Originele zoekgrens, eigen aanvullende outputref, callerflag, nul, één |

De oorspronkelijke caller geeft callback0 en mode1 door (**200180ce / 200180cb**) en een echt armyID. De mode1branch van5826a0 leest het type en de source; het armyID wordt alleen door mode0 gebruikt. De nieuwe producer kan in mode1 dus armyID0 aanbieden zonder een ArmyAgent te verzinnen. De overige flags worden uit de daadwerkelijk ondersteunde oorspronkelijke callerbranch overgenomen en afzonderlijk gefingerprint; geen gegokte nieuwe booleansemantiek. UnitDB+d8 levert haar bestaande typeflag. De gewone Goalcaller2004488e–a5 levert onder meer zoekgrens200000 en zijn eigen overige argumenten. Een nieuwe kleinere bounded zoekgrens is een ontwerpkeuze; afgesneden/timeoutsearch wordt UNKNOWN, niet bewezen geen route.

**Minimale outputvoorwaarden:**
- Geef alleen eigen initialisaties/capaciteit/pointer/count/resultslots; oorspronkelijke ArmyAgentvelden worden niet als outputstorage gebruikt.
- Start een fresh query met cap0/pointerNULL/count0. Engine **582926–995** alloceert zo nodig ruimte voor acht-byte entries; **582a23–6f** kopieert volledige MapPointDataentries en **582a73–77** zet de werkelijke count ook na padkopie. EAX1 plus volledige geldige bounds/endpoints is vereist; failure/reentrancy/cutoff houdt statusUNKNOWN/geen credit.
- Eigen padcopy/buffer eindigt via de echte engine-deallocator **5866e0** (cdecl, één pointer, callerpop4); [buffer-ABIbewijs](BINAIR/settler-producer-b4-hook-abi.txt) bindt die wrapper aan haar importcall. Geen allocator/free uit een willekeurige andere runtime mengen.
- Native query muteert haar **zoekworkspace** en globals, initialiseert helpers en verhoogt een searchcounter. **5826a6–bc** weigert een bestaande actieve context. Het is een padquery, geen letterlijk onveranderende geheugenfunctie. Voer uitsluitend synchroon buiten andere padcallbacks uit; geen recursieve classifier-/heapcalls. Geen gameorders/boarding/founding vanuit de producer.
- Controleer het geretourneerde pad: source/dest passend, bounded count, iedere z0-positie daadwerkelijk land, geen ruimte/sea-/transportsegment, relevante type-/endpointtoelating en safetygate. Een gelijk continent is alleen een goedkope voorfilter.
- Gebruik de eigen civ/Playerbinding van padinterface+7c en geldige originele host/layout. De flags/ABI voor andere types, mode2, bijzondere moves of cargo blijven uitgeschakeld. Native queryret/instructies zijn bewijs; daadwerkelijk hostaanroepen en gevonden veilige paden zijn nog geen runtimewaarneming.

Zo kan ontwerp een echte routecheck invoegen zonder opnieuw de complete A*implementatie of transportroute te reconstrueren. Het enginezoekwerk zelf blijft bestaand; de nieuwe producer interpreteert alleen zijn expliciet ondersteunde uitvoer.

## Minimale planlogica en acceptatiegrenzen

1. Begin pass; capture oude reciprocal assignments als hints, daarna originele refresh/cleanup laten werken.
2. Capture groundentries vóór limiet. Neem eigen kopieën; controleer volledige scope, originele maskers en eindpuntreads.
3. Na Update_Squads/Actual: preview effectieve klasseselecties en CityAgentbouwbaarheid, bepaal ondersteunde gewone landtypes en eigen vertrekpunten.
4. Vraag de gekozen B3/B5/rolpredicate om NOWplan plus noodzakelijke tiles; orden eerst, reserveer daarna een gezamenlijk bruikbare subset in eigen opslag. LATER/UNKNOWN blijft zichtbaar en krijgt geen uitvoerbaar slot.
5. Gebruik de gebonden virtual/concrete routequeries met eigen buffers, verse safetygate en typelegaliteit. Andere continenten, onbekende veiligheid en transport blijven apart zonder credit.
6. Dedup en match historical/current/queued claims eenmaal; verdeel ongedekte slots volgens B4klassevolgorde. Freeze D_t vóór native Desired. Original Actual blijft het enige aftrekpunt.
7. Na dezelfde AIPUpdate: plan/buffers ongeldig. Bij load/reload/civwisseling is de volgende echte pass de refreshroute; geen savepointer of passreservations bewaren.

Technische C moet naast quota/prioritycoherentie specifiek owner/generatie, sentinel/cap/truncatie, callback/niet-reentrant context, native pathbuffer-/allocatorABI, onbekende type/role/safety en dubbele claims controleren. Eigen fixturepaden blijven fixtures; geen producer-/pad-/gameplayacceptatie uit synthetische tijden. Na die controles volgt echte gelijke T0meting. Geen nieuwe vaste settlerquota of extra bonus als vervanging van G.

[AAIP-lessen](AAIP-LESSEN.md) veranderen dit bewijs niet: marinequota/packing zijn bestandslessen, geen gemeten producer-/directpadfunctie. [B4-vraagroute](DYNAMISCHE-SETTLERVRAAG-B4.md), [transportketen](TRANSPORT-EN-VESTIGINGSACTIES.md) en [H1](INGREEP-LOCATIESCORE-H1.md) blijven de onderbouwde basis.

Afgerond; overgedragen aan root/ctp_ontwerper voor een concreet kleine directe-landvariant. Geen actieve achtergrondrun. Niet-blokkerende backlog: alle indirecte callers, complete save-/scheduler-/pathflags voor bijzondere moves, optimale safety-/rolpolicy en volledig carrier-/pending-/landing-/techplan. Hervat alleen een concrete vraag uit dat ontwerp.
