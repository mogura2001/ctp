# B4: geladen settlertype en actuele vertrekclaims

9 oktober 2026, 14:57 Europe/Amsterdam. Gerichte fase A voor T en D1–D3 uit [de gebundelde C-terugvraag](../PROEVEN/settler-b4/BINDINGS-TERUGVRAAG.md). Gameplaydoel: dynamische settlervraag uitsluitend voor veilige, bruikbare directe landvestiging. Vraag: hoe identificeert de producer de echte geladen UNIT_SETTLER en leest hij actuele eigen bestaande/productie/nieuwe vertrekbronnen zonder native iteratie te wijzigen? De overige B4-hooks/H3/B2/owner/path/threatbindingen zijn overgenomen en niet opnieuw onderzocht.

**Alle vier inputs hebben nu een concrete uitvoeringsroute.** Gebruik twee read-only naamlookups en de native algemene settlerpredicate; lees own-BSetnodes met eigen bounded traversallogica; kopieer de concrete actuele agentvelden/getterresultaten binnen dezelfde pass; selecteer een kleine ondersteunde ordinarysingleunitbranch aan de hand van native bruikbaarheids-/cargo-/specialreadbewijs. Er is geen compleet nieuw producerprotocol of volledige reconstructie nodig. Deze overdracht beschrijft statisch bewezen reads en noodzakelijke voorwaarden, geen toegepaste producer of gemeten gameplay.

## Versie, ownership en bewijsgrenzen

- Engine SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp37d6f702, imagebase400000.
- AI SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, timestamp37b894e7, imagebase20000000. De bestaande DLL-disassembler controleert de passende robotcom.map. Symbolische namen worden steeds aan de getoonde body gekoppeld. Geen civctp.map-adres gebruikt.
- Bestaande scripts `Analyseer-AI-DLL.py`, `Analyseer-Engine-Locaties.py` en `Analyseer-Engine-Interfaces.py` hergebruikt. Geen eigen emulator, observer, test, framework, nativecall of game-/binarywijziging. Alleen dit rapport, eigen voortgang en de benoemde dumps geschreven.
- `Units.txt` bevestigt tekstueel dat de gewone UNIT_SETTLER land/mountainmovement en land/mountainsettling heeft. Dat is geen actueel geladen indexbewijs; de hieronder gebonden lookups leveren de actuele index.

## Dekkingsmatrix

| Input / beslisschakel | Concrete werking en binding | Uitvoeringscontract / noodzakelijke voorwaarden |
| --- | --- | --- |
| T: actuele naamidentiteit | StringDB `[A7DCFC]`,4660f0/ret8: exact casegevoelig token→StringID; UnitDB `[A7DD18]`,4543b0/ret8: StringID→loaded index | Beide bool1 vereisen; outputs vooraf−1; actuele DB-context/count/array controleren; geen vaste tekstindex |
| T: volledige geselecteerde settlercategorie | UnitDB745098+40→531a50; `Record+34 & F !=0`; native ArmyContainsSettlercaller132a3 gebruikt deze query | Iedere effectieve selectedtype eerst boundscheck; ander settlertype dan t zet hele pass uit; nietsettlerquota origineel |
| T: water/space | +48→531de0 leest bit2; Science waterworth246e0 gebruikt+48. +44→531dc0 leest bit8; spaceworth24710 gebruikt+44 | Deze bits benoemen water/space; gewone loaded t moet de bestaande beperkte landlegaliteit/movementvoorwaarden behouden; gewijzigde specialscope geen stilzwijgende toelating |
| D1: eigen containers | AiMain+90 ArmyBSet, +8c CityBSet; root+8; node+0ID/+4child/+8child/+cagent | Eigen bounded DFS/stack/visited-IDset; geen writes aan native BSet+10/+14/+18, geen Next/serialization/destructor/insertcall |
| D2: identiteit/soort | Agent+0c is raw32 BSetID; GetID10bd0 kopieert4bytes; GetType10bf0 leest Agent+4 | Node-ID==agent-ID; kind1army/kind2city; currentownset en civ/pass/generation binden; geen pointers uit vorige pass |
| D2: positie | Army11bc0 kopieert8bytes via+64, EAX1/ret8; City1c380 kopieert8bytes via+210, ret4 | AI-cachereads, geen eigen null/failurecheck; actuele huidige agent opnieuw zoeken en positie kopiëren, externe queryruimte behouden |
| D2: count/type | Army1a970 signedword+48→EAX;1a980 leest signedword+4a+2*i, ret4 | Voor ondersteunde singleclaim count==1, i=0; type==t/boundscheck; indexpointer werkelijk int32, geen valueargument |
| D2: huidige productie | City1cd50 leest+1f0type en+1f4category; type>=0 encategory1→type, anders−1;ret4 | Dezelfde actuele AI-frontteller als Actual6579f; één claim per huidige CityID/type, geen volledige enginequeueclaim |
| D3: ordinarysingleunit | State+40; count/type; cargo+60; native wait129f0; nativeusable759c3–759dc; specialflags+88 | Kleine ondersteunde state0branch, single t, cargo0, geen wait, finite movement>=16, geen fuel/paradrop; geen totale state-enum nodig |
| D2/D3: versheid | BeginTurn2a6b5→119e0;119e0 leest actuele movement en Player+c-positie, updatecache11cb0; productie-event10970→73f0→1c950 schrijftfrontcache | Alle positieve claims opnieuw uit huidige ownnodes/caches in huidige pass; oude hint alleen identityreferentie. Getterbool1 bewijst zelfstandig geen engine-refresh |

## T: exacte actuele resolver en failurecontract

**Read-only naamlookup:** `int32 __thiscall String_lookup(StringDB*, const char* token, int32* sid_out)` op4660f0. Push eerst `&sid`, dan pointer naar de exacte NUL-terminated string `UNIT_SETTLER`; ECX=`[A7DCFC]`. Return EAX1 bij exacte match;0 bij ontbreken. Native cleanup ret8. De routine hasht de token, leest StringDB+8-buckets en vergelijkt strings casegevoelig; zij schrijft uitsluitend de eigen output. De gelinkte zoekroute4662b0 doet hetzelfde in de bestaande bucketboom, ret0ch; bij ontbrekende node EAX0, zonder outputwrite. Geen toevoeging of StringDBmutatie.

**Read-only UnitDBlookup:** `int32 __thiscall Unit_index_from_sid(UnitDB*, int32 sid, int32* type_out)` op4543b0. Push `&type`, dan sid; ECX=`[A7DD18]`. Body4543b3 leest DBcount,4543bc recordarray+8 en4543c5 vergelijkt de echte naam-ID op Record+4. Zij doorloopt maximaal count records met stride2c8, schrijft bij match de arrayindex, EAX1/ret8; bij count<=0 of geen match EAX0, output onveranderd. Het veld is direct gebonden:4647f0 schrijft het parsernaam-ID naar Record+4. Er zijn geen DBwrites in4543b0.

**454200 mag niet worden gebruikt.** Dit eerdere parseraanknopingspunt is een insert: schrijft op4542cc een nieuwe index, verhoogt op4542d1–d2 DBcount en wijzigt op454295–c4 indexarrays. Zijn ret8/output lijken op een lookup, maar zijn body bewijst mutatie. Het is uitgesloten van deze read-only producer.

Failure/boundsvoorwaarden: geldige actuele StringDB/UnitDBpointers en recordarray, positieve redelijke geladen count/capacity, outputs vooraf−1, beide EAXbools exact1, resultaat in de ondersteunde UnitDBindexrange. UnitDB+0c→531770 geeft **DBcount−1** terug, zoals reeds de gewone AI-interface gebruikt. Voorkom de trailing niet-interface-entry: vereis `0<=t<UnitDB+0c-return` en tevens `<native DBcount`. De return van deze countquery is een aantal voor de AI-interface; `t==aantal` is geen geldig type. Geen lookupcall met onbekende stringpointer of DBcontext. De functies begrenzen hun eigen loop aan loaded count, maar bieden geen algemene bescherming tegen kapotte native pointers of willekeurig corrupte enorme counts; die input voldoet niet aan het gekozen passcontract.

Het index→record-pad4542e0 uit bestaand bewijs blijft nodig voor gecontroleerde recordreads. Die getter retourneertNULL buiten0..count−1; de UnitDBtraits derefereren het resultaat vervolgens zonder eigen nullcheck. **Controleer de typebounds vóór iedere traitcall.** De parser’s unchecked454310 is geen alternatief. Bind globals en interface aan de verwachte loaded engine; een onverwachte count/array/index/context geeft wholepassUNKNOWN/origineel vóór freeze.

**Volledige categorie:** UnitDB+40 neemt `(UnitDB_interface*, int32 type)` op de stack, ret8/EAXbool. Vtable745098+40 wijst naar531a50; deze haalt het actuele record via4542e0 op en reduceert `(Record+34 &0F)` naar0/1. UpdateArmyContainsSettler13294–132a8 loopt over echte unittypes en gebruikt juist+40; daarna herhaalt hij deze predicate voor cargo. Daarmee is dit een algemene native settlercategorie, geen `BUILDING_REMOVES_A_POP`-heuristiek.

Classpreview: selectedtype−1 betekent native geen geselecteerde entry; andere ongeldige codes zijn UNKNOWN. Voor iedere geldige selectedtype: categoriequery; categorie0 laat native quota ongemoeid; categorie1 en type!=t schakelt **hele pass** uit, ook voor upgrade/water/spacekeuzes of een andere klassebenaming. De geselecteerde t moet gewone landlegaliteit/movementbindings uit de geaccepteerde preflight hebben. Waterbit2/spacebit8 op t zijn concreet detecteerbaar via+48/+44; die specialscope valt buiten deze gekozen producer. De overige low-F-land/mountainbits hoeven niet volledig opnieuw als tokens te worden gedecompileerd om een ander settlertype veilig te herkennen.

## D1: bounded read-only eigen boomtraversal

De huidige eigen sets zijn aantoonbaar dezelfde die Actual655f0 verwerkt: AiMain+90 voor legers en+8c voor steden. De native First/Next-aanpak schrijft iteratorarrays/positie+10/+14/+18 en wordt **niet** als producerreadcall overgenomen.

Nodecontract is machinecodegebonden: Find1af50 leest root Set+8, vergelijkt het eerste rawID, volgt child+4/+8 en retourneert node+c. RawInsert8510 gebruikt dezelfde childstructuur. Cityrecurse84d0 behandelt node+0 als BSetID en node+c als CityAgent; city/armynodedestructors8080/80f0 gebruiken eveneens+4/+8/+c. RawBSetIDconstructor268c0 en kopie268e0 kopiëren precies4bytes, zonder encodingtransformatie.

Uitvoeringsroute: eigen lokale stack, bezoek root, lees node-ID/children/agent, kopieer gewenste waarden, voeg children aan eigen stack toe. Bound het aantal bezochte nodes en de stack aan een eigen vooraf gekozen cap; bewaak herhaalde nodeadressen, dubbele IDs, nullagent, kindmismatch en nodeID!=AgentID. Nullroot betekent lege complete set alleen binnen de geldige currentownercontext. Cap/cyclus/ongeldige structuur betekent INCOMPLETE/UNKNOWN, geen gecertificeerde lege of complete voorraad. De bestaande doelcap voor vertrekclaims van32 vervangt geen traversalcap of volledigheidscontrole van de bronset; overschrijding vóór freeze volgt de bestaande wholepassfallback.

**Geen native writes of calls naar muterende iterators.** Een eigen DFS hoeft nodeorder/balancing niet te reconstrueren; zij leest beide children eenmaal. IDs zijn de identiteiten; agentpointers zijn slechts pass-lokale bronnen. De gedumpte destructors/serializer/insert zijn layoutbewijs en mogen niet als query worden aangeroepen. Dit is een uitvoerbaar eigen bounded readpatroon, nog geen gebouwde/geteste traversal.

## D2: actuele agentreads, ABI en lifetime

Alle gettercalls zijn thiscall met ECX=currentagent. Ze zijn kleine directereads zonder eigen recordallocatie; hun pointergeldigheid moet vooraf uit het actuele ownset/lifetimecontract komen.

| Read | Stackargumenten en cleanup | Precieze interpretatie |
| --- | --- | --- |
| GetID10bd0 | verborgen `BSetID* result`; ret4; EAX=resultpointer | C++ objectreturn, geen EAXrawID; directe gecontroleerde32bitread op Agent+0c is gelijkwaardig voor deze producer |
| ArmyGetPos11bc0 | `(AiMain*, MapPointData* out)`; ret8, EAX1 | AiMainargument wordt niet gebruikt; kopieert+64→out8bytes zonder enginequery/failurecheck |
| CityGetPos1c380 | `(MapPointData* out)`; ret4; void | Kopieert+210→out8bytes; EAX is geen succescontract |
| ArmyCount1a970 | geen argumenten; ret | Signed16+48 uitgebreid naar volledige EAX |
| ArmyType1a980 | `(const int32* index)`; ret4 | Dereference index, signed16arrayread+4a+2*i; geen index/countguard in body |
| CityWhatArmy1cd50 | `(AiMain*)`; ret4; signed EAX | Actueel cachetype+1f0 alleen als>=0 encategory+1f4==1; anders exact−1 |

Kopieer externe x/y/z signed16 en normaliseer de eigen padding indien nodig; de getter kopieert ook de twee paddingbytes. Geen interne terrainy−x als bronpositie teruggeven. Agentkind uitGetType10bf0 is Agent+4; bestaande native usablecaller759aa–759b5 onderscheidt1army en2city.

**Versheid betekent huidige geregistreerde AI-objecttoestand in deze pass.** Actual6579f leest dezelfde WhatArmycache. Het buildfront-event10970→73f0 vindt de huidige CityID in eigen+8c en schrijft via1c950 exactcategory+1f4 entype+1f0. Het constructor/event/actualcontract maakt dit de gebruikte native actuele frontteller, geen telling van elke enginequeueentry. Stadsposities worden uit de opnieuw gebonden huidige CityAgent gelezen; verlies/recreatie wordt door huidige ownmembership/ID behandeld, geen historische pointer als bewijs.

ArmyBeginTurn119e0 haalt voor de gewone branch viaPlayer+c de huidige positie op en schrijft met11cb0 de cache; de bestaande caller2a6b5 in `research-government-budget-beginturn.txt` loopt de huidige ownarmies af. Binnen het geaccepteerde AIPUpdate/movementpasscontract worden unitcount/types/positie opnieuw uit de huidige node gelezen, na native actualrefresh. **Actualcountrefresh op zichzelf schrijft geen nieuwe Armypositie en GetPos’EAX1 bewijst geen enginequery.** Houd deze bewijsgrens in het implementatieverslag; geen onvoorwaardelijke engineversheidsclaim uit een cachedread.

Voor een expliciete verse nativeArmypositievalidatie is de minimale query nu eveneens concreet gebonden: Player744660+c→5273a0, `stdcall(Player*, uint32 armyID, int32* invalid_out, MapPointData* external_out)`, ret10h/EAXbool. De wrapper zet invalid_out=0, zoekt via4c7920 uitsluitend in de bij deze Player behorende huidige army-IDtree, geeft bij ontbrekende eigenID invalid1/EAX0, en converteert bij succes met503f70 naar de externe positie/EAX1. Dit verandert geen ArmyAgentcache. Zij is een beschikbare gerichte readroute voor ontwerp als hard nativepositie-revalidatie wordt geëist; extra calls/accounting moeten dan expliciet in B worden meegenomen. Geen UpdatePosition/BeginTurn als read-only helper aanroepen: die muteren de agent.

Lifetimecontract: capturehintvelden vóór cleanup alleen kopiëren. Finalize zoekt currentIDs opnieuw in dezelfde AiMainownsets; controleert civ/generation/owner/kind/ID, kopieert positie/count/type/fronttype en verwerkt alleen die huidige kopieën. Geen rawagent/node/positionpointer bewaren na de pass; geen reentrancy of andere civ tijdens een native query. Veranderde/ontbrekende/incomplete bron is geen positief claimbewijs. Dit hergebruikt de bestaande B4-passlifetime, zonder nieuwe save-/eventcycle.

## D3: kleinste ondersteunde ordinarysingleunitbranch

Een concrete conservatieve positieve branch is:

1. Current own ArmyAgent met rawID/nodeID gelijk en kind1; volledig ondersteund loaded t uit T.
2. Signedcount+48 precies1; verse index0type via1a980 preciest. Mixedarmies, pendingcity-armies en onbekende count/type krijgen geen gewone bestaande-unitclaim.
3. State+40 **exact0** als kleine ondersteunde gewone branch. Daarmee zijn o.a. native city-backedstates1/2 en de uit actual uitgesloten17/18 niet ongemerkt toegelaten. Er wordt geen volledige enumnaam of universele idlebetekenis voor alle statecodes aangenomen.
4. Geen cargo: Army+60NULL, of geldige cargocontainer met signedcount+8==0. GotCargo19970 bewijst precies de positievecountpredicate; een negatieve/ongeldige count is UNKNOWN, geen leegbewijs. De bestaande FindPath17fd3–17ffd neemt bij positieve cargocount een afzonderlijke branch181fb.
5. Native `IsWaitState129f0` EAX0; finite huidig doublemovement+70 **>=16**. Dit zijn exact de native bruikbaarheidsvoorwaarden vanStill_Can_Act759c3–759dc: minder16 of wait verlaagt zijn aantal bruikbare agents. Overnemen als positieve niet-wacht/kan-handelen-gate; niet claimen dat ieder niet-waitstate automatisch beschikbaar is. NaN/ongeldige movement wordt niet positief.
6. Geen fuel-/paradropbranch: Armyflagbyte+88 &18h==0. UpdateUsesFuel19fe0/1a023/1a042 bindt bit8 aan fuelgebruik; IsParatroop1a2e0 bindt bit10; migratingparatroop1a2f0 gebruikt bovendienbit20. Het geselecteerde normale type behoudt de reeds gebonden land-/endpoint-/mode1voorwaarden. Geen speciale beweging toelaten door alleen een positieve settlercachebit te lezen.

Dit is een **beperkte uitvoeringsscope**, geen volledige classificatie van iedere armytoestand. De positieve selectie is onderbouwd door bestaande native reads/bruikbaarheid en vermijdt cargo/specialbranches. Een strategie om aanvullende states mee te tellen is voor deze kleine producer niet vereist en wordt niet onderzocht. De ontwerper legt expliciet vast hoe niet-ondersteunde/ongeldige vertrekbronnen de bestaande UNKNOWN/wholepassregels volgen; Actual blijft origineel en wordt niet door deze subset herschreven.

Een bruikbare army is nog geen vrije schedulerassignment. Voor een historische assignedclaim blijven de reeds geaccepteerde reciprocal Goal/Squadchecks en currentID/type/positie/padrevalidatie verplicht; een onbekende mapping is UNKNOWNhint. Deze D3-gate mag geen leger dat een andere missie heeft stilzwijgend als gecertificeerd dezelfde settlementassignment presenteren. Die bestaande hintvoorwaarde is overgenomen, geen nieuw scheduleronderzoek.

## Bewijsbestanden en overdracht

De concrete ranges staan in [naam/category](BINAIR/b4-typeddepartures-name-and-category.txt), [UnitDBslots](BINAIR/b4-typeddepartures-unitdb-interface.txt), [water/spaceconsumers](BINAIR/b4-typeddepartures-settle-mask-consumers.txt), [agentgetters](BINAIR/b4-typeddepartures-agent-reads.txt), [categorie/BSet](BINAIR/b4-typeddepartures-category-and-bset.txt), [node/IDlayout](BINAIR/b4-typeddepartures-node-layout.txt), [productie/IDevent](BINAIR/b4-typeddepartures-production-and-id.txt), [positierefresh](BINAIR/b4-typeddepartures-position-refresh.txt), [PlayerGUID/positie](BINAIR/b4-typeddepartures-current-position-interface.txt), [currentpositiebody](BINAIR/b4-typeddepartures-position-current.txt), [eligibilityreads](BINAIR/b4-typeddepartures-eligibility-reads.txt), [nativeact/traversal](BINAIR/b4-typeddepartures-act-and-traversal.txt) en [fuelflag](BINAIR/b4-typeddepartures-fuel-flag.txt). De overige scoped dumps zijn ondersteunend onderzoeksmateriaal. `*.txt` bevat soms automatisch gedecodeerde padding/jumptablebytes na een return; die regels zijn geen uitgevoerd codebewijs. Gebruik de beschreven gevalideerde body-/callranges.

De [bestaande B4-terugvraag](../PROEVEN/settler-b4/TYPE-SCOPE-TERUGVRAAG.md) kan met T worden gesloten; D1–D3 worden tegelijk aan het uitvoeringscontract toegevoegd. Ontwerper moet de kleine ondersteunde eligibilityscope, cacheversheidsgrens en eventuele expliciete nativepositiequery in hetzelfde voorstel benoemen voordat C hervat. Geen native producer-/claim-/queryfixtureacceptatie of host/gameplaybewijs geclaimd. Alleen gerichte inputanalyse afgerond; geen vervolgpakket gestart.
