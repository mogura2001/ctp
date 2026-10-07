# Transport en uitvoering van vestigingsdoelen

Fase A, 5 oktober 2026. Alleen-lezen onderzoek van de originele CTP I-bestanden. Dit pakket verbindt de eerder bewezen locatiekeuze met bereikbaarheid, transportselectie en concrete engine-aanvragen. Het reconstrueert geen volledige militaire scheduler en bewijst geen gespeelde uitbreiding over zee.

## 1. Resultaat en bewijsgrens

De bestaande AI heeft transportuitvoering binnen gewone legerdoelen, waaronder GoalSettle. Een afzonderlijk transportdoel is dus niet noodzakelijk voor iedere bootreis. De onderzochte uitvoering zoekt beschikbare carriers, toetst capaciteit en compatibiliteit, laat legers naar een ontmoetingspunt gaan en kan boarding, debarking en vestiging aanvragen. Een ontbrekend schip, verkeerde capaciteit of onbereikbaar ontmoetingspunt kan deze keten onderbreken terwijl settlers en vestigingsdoelen al bestaan.

De betekenis van `TRANSPORT_GOALS = 0` moet daarom beperkt blijven tot de betreffende doelcategorie; deze waarde bewijst geen verbod op schipbouw of transport binnen een vestigingsdoel. De volledige aanmaakroute van die afzonderlijke doelcategorie blijft buiten dit pakket. De eerdere Welsh-waarneming bewijst evenmin op zichzelf dat settlers de bouw van schepen onmogelijk maken. [Bestaande quota- en eilandanalyse](RUIMTE-BUREN-TRANSPORT.md), [bouwdoelconcurrentie](BOUWDOELEN-EN-QUEUE.md).

De DLL heeft SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, imagebase `20000000`, timestamp `37b894e7`; robotcom.map past hierbij. De engine heeft SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, imagebase `00400000`, timestamp `37d6f702`; de afwijkende engine-map is niet gebruikt. Alle concrete engineadressen hieronder zijn aan daadwerkelijke bytes/interfaces gekoppeld. [AI-disassemblage](BINAIR/transport-settle-actions-goal-planner.txt), [enginebewijs](BINAIR/transport-settle-actions-engine-carry-and-found.txt).

## 2. Van kandidaat naar uitvoerbaar legerdoel

De kwaliteitscore, packingmaskers en goallimieten bepalen eerst welke locaties GoalSettle worden. Dat onderzoek wordt hier hergebruikt. Daarna biedt `ArmyAgent::ActionBidToSettle`, `20012b60`, een leger of een vertegenwoordigde unit aan dit doel aan. De betrokken controles omvatten vestigingsgeschiktheid, continentbereikbaarheid, afstand en eventuele productie-/wachttijd. Een toegelaten kandidaat is nog geen uitgevoerde stad. [Vestigingsdoelen](VESTIGINGSDOELEN.md), [bod en continentcontrole](BINAIR/transport-settle-actions-goal-planner.txt).

`PretestSettleArmy`, `200130e0`, gebruikt voor state1/2 een unit-typecheck en voor andere betrokken states een check op het concrete leger. Bij aanwezige cargo bestaat tevens een route die vestigende cargo onderzoekt. De numerieke statenames worden hier niet als volledige state-enum geïnterpreteerd. De engine beslist mede of een unit/leger op het doel kan vestigen; locatiekwaliteit en deze toelating zijn afzonderlijke voorwaarden. [Pretests](BINAIR/transport-settle-actions-reach-safety.txt).

`PretestContinentReachable`, `20014a60`, accepteert dezelfde land/watercategorie en hetzelfde continent direct. Voor andere gevallen bestaan speciale beweging, ruimteverbinding en carrier-/kusttakken. In de laatste landtak kunnen verschillende continentnummers toch door de pretest komen: de uiteindelijke vergelijking betreft daar de land/watercategorie. Dit is voorlopige bereikbaarheid met vervolgwerk, geen bewijs dat een settler zonder schip zee kan oversteken. [Continentbranches](BINAIR/transport-settle-actions-goal-planner.txt).

GoalSettle-vtable `2008a558` bindt slot40 aan de generieke `ArmyGoal::Execute_Task`, `200443c0`; slot80 aan `GotoTaskSolution`, `20044a70`; slot9c aan `TryTransport`, `20045240`; slota0/a4 aan `FindTranportInSquad`/`LoadTransport`, `20045380`/`20045520`; slot90 aan `GoalSettle::ArrivedAtTask`, `200487e0`. De ontbrekende s in FindTranportInSquad staat ook zo in het originele symbool. Dit maakt de overgeërfde transportketen aantoonbaar voor het vestigingsdoel. [Vtable en resultaatstabel](BINAIR/transport-settle-actions-vtable-branches.json), [uitvoeringsfuncties](BINAIR/transport-settle-actions-execution-trigger.txt).

Wanneer de normale padoplossing geen bruikbare vervolgstap oplevert, kan GotoTaskSolution via slot9c naar TryTransport. Deze kan bestaand geladen transport behandelen, een carrier zoeken en een laadoplossing proberen. Bij ontbrekende oplossing voegt `20045305–2004531c` het verschil tussen legerunitcount en beschikbare transports toe aan de gevraagde transportsterkte en retourneert resultaat2. Dit is een geregistreerde behoefte; deze instructies enqueuen geen schip. [TryTransport en LoadTransport](BINAIR/transport-settle-actions-goal-planner.txt).

## 3. Scheduler: beschikbaar transport is een eigen voorwaarde

De normale scheduler behandelt taskresultaat2 via switchtarget `20073770`. Deze route probeert `ExecuteWithTransport`, `20073df0`, alleen wanneer de extra uitvoerargumentwaarde1 is en `Planner::GetUsableTransport` positief terugkomt. De getter, `2006f150`, leest Planner+a74. De quota voor bouwlijsten worden hier niet opnieuw geraadpleegd. [Schedulerroute](BINAIR/build-goals-queue-ai-scheduler-inputs.txt), [resultaatswitch](BINAIR/transport-settle-actions-vtable-branches.json).

`Squad::GetUsableTransport`, `20077130`, telt vrije capaciteit van toepasselijke legeragents op. Het slaat onder andere legers met minder dan16 bewegingspunten en wachtende legers over; `GetNumCargo` levert de vrije capaciteit. De plannerwaarde kan tijdens toewijzing worden bijgesteld (`2007355d–20073571`). De volledige initialisatie en boekhouding van Planner+a74 is hier niet gereconstrueerd; de lokale positieve toelatingsvoorwaarde en de squadberekening zijn wel verbonden. [Bruikbare capaciteit](BINAIR/transport-settle-actions-usable-count.txt), [plannerbijstelling](BINAIR/build-goals-queue-ai-scheduler-inputs.txt).

ExecuteWithTransport berekent een tekort uit squadunitcount, transportunitcount en reeds geregistreerde transportsterkte. Vervolgens doorloopt het kandidaten uit Planner+a6c. Het slaat onder andere de eigen squad, ongeschikte squadstates, cityagents, carriers met geladen cargo en carriers zonder vrije plaatsen over. Bij de resterende agents vergelijkt het transportutility; onvoldoende utility levert geen keuze op. Een gekozen carrier verhuist uit zijn oude squad naar de squad van het doel. Bij voldoende capaciteit probeert de scheduler de taak opnieuw; bij tekort stopt deze lokale poging. Er is in deze selectiefunctie geen schipbouw-enqueue. [Selectie, verplaatsing en heruitvoering](BINAIR/transport-settle-actions-goal-planner.txt), [utility en capaciteit](BINAIR/transport-settle-actions-carriers.txt).

Dit betekent concreet: een schip kan bestaan en toch niet voor deze poging beschikbaar zijn, bijvoorbeeld doordat het al cargo heeft of zijn beweging tekortschiet. Omgekeerd garandeert een positief bruikbare-capaciteitgetal niet dat er een passende carrier naar deze settler kan varen. EstimateTransportUtility, `20018ce0`, controleert CanTransport, beweging, kust/continentverbinding en de afstand-/bouwschatting. Het volledige optimum en alle wachttijdtermen zijn hier niet als model gevalideerd. [Utilityfunctie](BINAIR/transport-settle-actions-carriers.txt).

## 4. Echt record: capaciteit en soort cargo

AiMain+38 is de UnitDB-interface: de bewezen AI-init vraagt GameState+28 op; de echte GameState-wrapper `525fc0` leest zijn object+18; constructor `5316a0` zet vtable `745098`. De eerdere terrain-initbinding wordt hergebruikt. Een los GUID-zoekresultaat zonder UnitDB-symbolen levert hiervoor geen bewijs. [Bestaande AI-init](BINAIR/terrain-food-ai-interface-init.txt), [UnitDB-constructor](BINAIR/transport-settle-actions-unitdb-binding-v2.txt), [slots](BINAIR/transport-settle-actions-unitdb-slots.json).

| Interface/record | Aantoonbare betekenis |
|---|---|
| UnitDB+c8 →531fa0 →Record+48 | Carry-compatibiliteitsmasker |
| UnitDB+cc →531fc0 →Record+4c | Integer TRANSPORT_CAPACITY |
| UnitDB+e0 →532060 →46ea80 | Compatibiliteit carrier-type/cargo-type |
| Record+30, bit1000 | SIZE_SMALL |
| Record+30, bit80000000 | MOVEMENT_TYPE_LAND |
| Record+48, bit1 | CAN_CARRY_SMALL_LAND |

De echte UnitRecord-parser `46b7f0` gebruikt token66/77/93/96 voor respectievelijk landbeweging, kleine landcargo, kleine size en capaciteit. De overeenkomstige schrijftakken zijn `46b82b`, `46b941`, `46ba89` en `46b9ed`. De laatste leest de integer in Record+4c. `46ea80` combineert het carrymasker met grootte en beweging van de cargo; voldoende numerieke capaciteit alleen volstaat dus niet. [Tokenlookup](BINAIR/transport-settle-actions-unit-tokens.txt), [dispatch](BINAIR/transport-settle-actions-unit-parser-table.json), [schrijfvelden](BINAIR/transport-settle-actions-unit-parser-fields.txt), [compatibiliteitsfunctie](BINAIR/transport-settle-actions-engine-carry-and-found.txt).

De originele Settler is SIZE_SMALL met MOVEMENT_TYPE_LAND. Triremes dragen CAN_CARRY_SMALL_LAND en capaciteit2, maar hebben alleen MOVEMENT_TYPE_SHALLOW_WATER in deze definitie; ze worden beschikbaar bij Ship Building. Hiermee is de capaciteit/compatibiliteit van de vroege combinatie onderbouwd, zonder de volledige enginelegaliteit van iedere zeetegel te claimen. [Originele unitdefinities](../CTP-og/ctp_data/default/gamedata/Units.txt).

`CanTransport`, `20019440`, heeft afzonderlijke routes voor state1/2 en concrete legers. Bij een vertegenwoordigde carrier en concreet passagiersleger moet de capaciteit minstens de unitcount zijn en moet iedere cargo-typecheck slagen. Bij concrete legers vraagt de AI Player+f0 en accepteert alleen een engineantwoord≥1. De volledige engineberekening van dat antwoord, inclusief alle bijzondere armycondities, is niet uitgewerkt. [AI-capaciteitsfilter](BINAIR/transport-settle-actions-carriers.txt), [Player-interface](BINAIR/transport-settle-actions-player-interface.txt).

`GetNumCargo`, `20013420`, vraagt bij concrete carriers de actuele legerunittypes op, sommeert hun transportcapaciteit en trekt de gecachete cargo-count af. Een leger met geen carrymasker wordt geen carrier; state17 wordt uitgesloten. Voor state1/2 wordt capaciteit van het vertegenwoordigde eerste type gebruikt, met geladen count0. Inconsistente caches en de volledige cargo-eventcyclus blijven apart runtimeonderzoek. [Capaciteitsberekening](BINAIR/transport-settle-actions-carriers.txt).

## 5. Van ontmoeting naar engine-aanvraag

AiMain+2c gebruikt de echte Player-vtable `744660`.

| Actie | AI → Player-slot → echte engine |
|---|---|
| Vestiging | ActionSettle20018980 →+24 →527560 →4c7b00 →4b9a10 |
| Cargo mag doelvakje betreden | +2c →527610 →unit/world-controle |
| Concrete legers transportcompatibel | +f0 →5282d0 →4ca6b0 |
| Boarding aanvragen | TryToBoardTransport200199a0 →+fc →528340 →4cab90 |
| Debarking aanvragen | DebarkCargoOntoPath20019e60 →+100 →528370 →4cad10 |
| Actuele leger-/cargogegevens | +28c →52bac0 |

[Player-slotbinding](BINAIR/transport-settle-actions-player-interface.txt), [AI-actiecode](BINAIR/transport-settle-actions-engine-requests-ai.txt), [enginewrappers](BINAIR/transport-settle-actions-engine-wrappers.txt), [legaliteit en orders](BINAIR/transport-settle-actions-engine-legality.txt).

Boarding vereist in de AI minstens16 beweging en exact dezelfde MapPointData-positie van settler en carrier. Bij verschillende posities gaat er geen boardingrequest uit. In die branch wordt bovendien een lokaal returnslot gelezen zonder zichtbare initialisatie; daarom behandelen de controles uitsluitend het aantoonbare ontbreken van de actie, niet een betrouwbare false-return. Een algemeen gameplaydefect is hiermee niet bewezen. Bij dezelfde positie verstuurt de functie beide armyIDs via Player+fc. De engine voert eerst `4ca890` uit en bouwt bij toelating een ordertype3b; een uitgegeven verzoek is nog geen waargenomen inscheping. [Boardingbranches](BINAIR/transport-settle-actions-engine-requests-ai.txt), [engineordertoelating](BINAIR/transport-settle-actions-engine-legality.txt).

DebarkCargoOntoPath kiest een volgend padpunt en controleert of de cargotypes het vakje mogen betreden. Zo nodig onderzoekt het aangrenzende gewrapte vakjes. Vervolgens kan het Player+100 aanvragen. De engine zet via `4cad10` orders klaar. De volledige opvolging, unitverplaatsing en registratie zijn hier niet geëmuleerd. [Debarkroute](BINAIR/transport-settle-actions-engine-requests-ai.txt), [engineverzoek](BINAIR/transport-settle-actions-engine-legality.txt).

ArrivedAtTask gebruikt subtask2 voor TryToBoardTransport en subtask0 voor ActionSettle. ActionSettle zelf retourneert het Player-antwoord, maar ArrivedAtTask handelt dat antwoord in deze branch niet afzonderlijk af: het markeert via slot48 en vraagt vestiging aan. De engine heeft een echte stadstichtingsroute met verdere controles en cityregistratie. De bevestiging dat dit doel pas na succesvolle stadcreatie uit alle AI-lijsten verdwijnt, vereist aanvullend event-/doellevenscyclusonderzoek. [Aankomst](BINAIR/transport-settle-actions-goal-planner.txt), [actie en werkelijke engine-foundroute](BINAIR/transport-settle-actions-engine-carry-and-found.txt).

## 6. Eilandruimte, buren en veiligheid

De bestaande land_continents_full_of_friends-input, met naval bij>0.65 en supernaval bij>0.9, beschrijft bezetting van landmassaruimte door steden/settlers en conditionele buitenlandse steden. Dit is niet hetzelfde als het aantal bereikbare geschikte vestigingsplaatsen. LandContinentShared bestaat als diplomatieke overlapmaat; koppeling aan een afzonderlijke openingsstrategie is niet bewezen. Deze signalen blijven bruikbare bestaande interfaces voor later ontwerp, met deze beperkingen. [Bestaande signalen en profielloads](RUIMTE-BUREN-TRANSPORT.md), [persistentie van opeenvolgende loads](AIP-LAADWERKING.md).

De transportpadcallback `20017650` betrekt beweging, kustlanding/citycapturevoorwaarden, mapinformatie en buitenlandse eigenaren. World+90/+94 zijn hier aan mapbitchecks gebonden; dit zijn geen berekende militaire dreigingsscores. Bij een specifieke Foreigner+204/+68-combinatie kan betreden van buitenlands terrein extra padkosten krijgen. De precieze semantische naam van die velden blijft open. Dit pakket bewijst geen algemene escorte-eis of veiligheidswaarborg voor settlers. PretestAttack is aanwezig maar mag niet zonder callbinding als settlerbescherming worden geïnterpreteerd. [Pad- en aanvalpretests](BINAIR/transport-settle-actions-reach-safety.txt), [echte World-slots](BINAIR/transport-settle-actions-world-path-inputs.txt).

AAIP verandert de primaire naval Triremesquota van−2 naar0.4 en de Sea_Troops_Primary-gewichtwaarde van6000 naar6500. Het wijzigt ook de aanvullende Triremeslijst van0.75 naar0.4. Deze wijzigingen beïnvloeden vraag en concurrentie, via de eerder bewezen quota- en bouwketen. Ze bewijzen geen wijziging van de onderzochte enginecapaciteit of movementorders, en garanderen niet dat een concrete eilandsituatie oplost. [OG naval](../CTP-og/ctp_data/default/aidata/AIPs/naval.aip), [AAIP naval](../CTP-AAIP/ctp_data/default/aidata/AIPs/naval.aip), [quota-afleiding](RUIMTE-BUREN-TRANSPORT.md).

## 7. Controle en resterende gaten

De read-only helper voert **23/23 geslaagde controles** uit op originele instructies: vier carrycompatibiliteitsbranches, drie capaciteitgetters, vier AI-capaciteit/typebranches, zes cargotellingen, vier boarding-aanvraagbranches en twee vestigingsaanvragen. Synthese van records en states is expliciet; recordlookup, Player-legerquery en actionacceptatie zijn externe mocks. Er is geen CRT/ftol- of globale FPCW-vervanging nodig. Dit bewijst de lokale voorwaarden en requestargumenten, geen volledige spelbeurt, zeereis of scheduleroptimum. [Controlescript](../PROEVEN/Controleer-Transport-Vestiging.py), [resultaat en mocks](BINAIR/transport-settle-actions-controls.json).

De belangrijkste nog open schakels voor vervolg zijn:

1. Volledige Planner+a74-init en de eligibility/available-statelevenscyclus: waarom een aanwezige carrier in een concrete save wel of niet bruikbaar is.
2. Volledige ontmoetingspunt-/padkeuze en orderafhandeling tot cargo-events; lokale requests bewijzen geen voltooide reis.
3. Engineantwoord van CanTransport voor concrete legers, inclusief bijzondere stack-/ordercondities.
4. Semantische binding van specifieke diplomatievelden in de padcallback en samenhang met dreiging/escorte van settlers.
5. Terugkoppeling van gefaalde of geslaagde stadstichting naar GoalSettle-lijsten en stopvoorwaarden voor nieuwe settlers.

Deze gaten beperken conclusies over feitelijke eilandprestaties en veiligheid. De keten is wel voldoende afgebakend om quota/bouwvraag, voorlopige bereikbaarheid, beschikbare capaciteit en uitgegeven beweging-/vestigingsrequests afzonderlijk te beoordelen. Fase A als geheel is hiermee niet afgerond.
