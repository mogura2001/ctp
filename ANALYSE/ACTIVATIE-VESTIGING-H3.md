# H3 — nieuwe vestigingsdoelen en activatiebewijs

8 oktober 2026, 16:05 Europe/Amsterdam. Gerichte fase A voor de H1-I/H3-proef; brede A blijft afgerond. Alleen bestaande bestanden en originele machinecode gelezen. Geen spelstart, GUI, livegeheugenactie, injection, binary-/gameplaywijziging of observerbouw.

## Antwoord en overdrachtsgrens

**De minimale read-only route is beschikbaar:** de bestaande gevalideerde civ/RobotCOM/AiMain-route kan worden uitgebreid met de eigen Planner-doeltabel, GoalSettle-vtable/ID, positiepointer en doublekwaliteit. Lees daarnaast de originele gedeelde World-score rechtstreeks uit de bestaande enginecache. Twee rustige snapshots vóór en na een werkelijk uitgevoerde AI-pass kunnen een *nog aanwezig* nieuw doel van opgeslagen doelen onderscheiden via de per-Scheduler volgende-IDwaarde.

**Deze uitbreiding bewijst geen transient heapcall of heapordening.** GoalSettle zet bij constructie veld +24 op nul; de aangetoonde Scheduler-cleanup kan juist zulke doelen verwijderen en vrijgeven. Daarom is aanwezigheid van een nieuw doel bij een gewone beurtgrens niet gegarandeerd. De kleinste echte runtimepoort is eerst vaststellen of op dezelfde T0 een nieuw doel vóór cleanup leesbaar blijft, met bekende civ/ID/positie/kwaliteit. Indien alle relevante doelen verdwijnen, is een begrensde waarneming binnen de echte selectiepass, vóór verwijdering, nodig. Een alleen na de beurt gedraaide observer kan dat gat niet oplossen. Er is hier geen al bewezen rustig heapmeetmoment, tracevoorziening of nieuwe observerhook bedacht.

Een ontwerper kan nu een kleine uitbreiding van [Lees-Onderzoeksactivatie.py](../PROEVEN/ai-uitlezen/Lees-Onderzoeksactivatie.py) specificeren. Zij volstaat voor blijvende doeltoestand en scoreonderscheid; de volledige vereiste nieuwe-heap/scorecall-activatie blijft een afzonderlijke runtimepoort. Performance **≤1,10 × H1-I** blijft eveneens afzonderlijk, met echte gelijke T0/B1-passes; fixture- of observerlooptijden vervangen dit niet.

Gameplaydoel: uitbreiding naar goede production-locaties volgens [PROJECTDOELEN](../PROJECTDOELEN.md) en [LOCATIESELECTIE](../LOCATIESELECTIE.md). Concrete wijzigingsvraag: H3-activatie en scoreconsistentie controleerbaar maken zonder oude goals of gedeelde cache als nieuwe adapteruitkomst te presenteren. Science, monopoly, nieuw beleid en algemene scheduler-/save-/heapreconstructie vallen buiten deze taak.

## Dekking per beslisschakel

| Schakel | Bestaand bewijs / huidige werking | Wat de minimale observatie oplevert | Grens |
| --- | --- | --- | --- |
| Civ/eigenaar | Observer bindt manager, RobotCOM-vtable, actor+20 en Science-wrapper aan dezelfde civ/Player | Gevalideerde AiMain per normale civ | Save-identiteit komt uit proefprocedure, niet uit observer |
| Eigen objecten | AiMain+94→Planner; +80→AiMap; +30→World | Civgebonden container, geen achtergebleven globale g_settle_ai als eigenaar | Pointers opnieuw lezen per snapshot |
| Doelcontainer | Planner+a30 count; +a48 Goal*-array; +a50 parallel gesorteerd ID-array | Alle huidige geregistreerde goals en ID-paarcontrole | Geen aantal vrije locaties/toewijsbare opdrachten |
| GoalSettle-identiteit | Vtable RVA 8a558; +0c=5; +08 signed32 ID | Concrete vestigingsdoelen zonder andere Goal-subklassen te decoderen | Zelfde identiteit/layout voor nieuwe en geladen doelen |
| Positie/kwaliteit | +54→MapPointData met signed16 x/y/z; +48 doublekwaliteit | Exact opgeslagen doelpositie en kwaliteit | +58 is tweede geconverteerde positie, niet de scorecallpositie |
| Nieuw versus opgeslagen | Nieuw ID begint -1; Scheduler+0 deelt een ID uit en verhoogt; laden herstelt bestaande ID/kwaliteit | Nieuwe surviving IDs in interval [Nvoor, Nna) in dezelfde ononderbroken instantie | Eén snapshot, andere heapadreswaarde of alleen nieuw ID in de tabel is onvoldoende |
| Originele World-score | manager+248c→laag→x-kolom→signed16[y] | B bij dezelfde x/y/z, zonder een callback aan te roepen | Cache is gedeeld en opgeslagen; B is geen H3-classifierresultaat |
| Adapter/constructor | Drie gepatchte sites; signed16-score positief→double→GoalSettle+48 | Nieuwe Q≠B kan gewijzigde kwaliteit zichtbaar maken | Q=B onderscheidt H1-I niet van H3-fallback/geen bonus/saturatie |
| Heap | Ground reset count, voegt positieobjecten in; score zit niet in AiCellPtr | Eventueel overgebleven locaties/heapindex | Geen generation/tijdstempel of persistente score; snapshot bewijst geen nieuwe comparatorcall |
| Levensduur | Doelen kunnen in cleanup uit Planner-IDtabel en via virtuele destructor verdwijnen | Aanwezige doelen zijn leesbaar; ontbrekende doelen blijven onbekend | Een rustige beurtgrens kan activatie-informatie al verloren hebben |

## Concrete machinecoderoute

Nieuwe bewijsextracten lezen originele DLL SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`; map en PE matchen timestamp `37b894e7`, imagebase `20000000`. Adressen hieronder zijn preferred VAs; gebruik geladen modulebasis plus RVA. Geen civctp.map-adres gebruikt.

### Eigenaar en Planner

Hergebruik [bestaande activatiebinding](ACTIVATIE-ONDERZOEKSLIJST.md) en de observer: engineglobal 00a7ddb8 geeft de manager; manager+220c+4*civ geeft RobotCOM; RobotCOM+8 geeft AiMain. Civbinding wordt reeds gecontroleerd.

AiMain+94 is Planner: de Init-store op **200021f3** en Load-store op **20003b6a** volgen hun echte Plannerconstructors. AiMain+80 is AiMap: stores **20001c1a / 20002d9e**. Bewijs: [init/load](BINAIR/masker-initialisatie-load-wrap.txt). Planner+a28 is eigen AiMain in de bekeken Store/Load-context; als aanvullende eigenaarsguard lezen. Geen directe civ-ID in ieder doel veronderstellen.

[Goal/containerbewijs](BINAIR/settle-activation-h3-goal-layout.txt):
- Add_Goal **2006ed8f–9c** bereikt Scheduler via Planner+a2c.
- **2006eda8–b4** leest Goal+8 en table count+a30.
- **2006eee6–2006ef04** schrijft dezelfde index naar IDs op +a50 en pointers op +a48 en verhoogt count.
- Return_Goal_By_ID **2006f0c0–2006f129** zoekt in die ID-array en retourneert bij gelijk ID de pointer op dezelfde index. Dit bewijst de parallelle tabelbinding.
- +a38 is gebruikte capaciteit; +a4c/+a54 de allocatiecapaciteiten van de twee arrays. Voor een bounded decoder geldt 0≤count≤capaciteiten, volledige reads, IDvolgorde en goal+8 gelijk aan zijn IDentry. Geen DLL-methoden vanuit de observer aanroepen.

### Goal-identiteit, positie en score

GoalSettleconstructie **20048633–52** bereikt ArmyGoal, zet vtable **2008a558**, +24=0, +0c=5 en +10=1. +10 is een klasseveld, geen extra civnummer.

ArmyGoal **20043194–a3** kopieert de aangeleverde double exact naar **+48/+4c**. **200431a9–c1** kopieert de drie positiehelften naar de allocatie op **+54**. Lees daarvan alleen de eerste zes bytes; interpreteer signed16 x/y/z. **200431c5–d0** vult de aparte +58-positie via Player+14; +54 correspondeert met de World/constructorpositie.

Nieuwe IDs: Init_Goal **2006835a** zet +8=-1. Scheduler::Add_New_Goal **20070ec1–cf** vervangt uitsluitend -1 door [Scheduler+0] en incrementeert die teller. Bewijs: [ID/lifetime](BINAIR/settle-activation-h3-id-lifetime.txt), [ID-init/save](BINAIR/settle-activation-h3-id-save.txt).

De gerichte directe constructorxref vindt precies **2007aa92** in InsertBestSettleGoal ([xref](BINAIR/settle-activation-h3-constructor-callers.txt)); dit sluit een indirecte call niet universeel uit. Die bekende route vraagt score op 2007aa35, eist signed BX>0, converteert BX naar double en geeft haar aan de constructor. Hergebruik [H1-callcontract](INGREEP-LOCATIESCORE-H1.md).

### Waarom opgeslagen doelen niet nieuw zijn

LoadMyGoals **2006dd12** gebruikt de archiveconstructor **20048700**. Die bereikt ArmyGoal::Serialize; **20043447–53** herstelt de double +48 en **2004346b–aa** de positie op +54. Goal::Serialize bewaart/leest de 28h bytes vanaf +8, inclusief ID. LoadMyGoals **2006e015–2006e17e** zet herstelde ID en pointer rechtstreeks in dezelfde Plannerarrays. Vtable en type zijn dus geen nieuwheidskenmerk.

Scheduler::Serialize **20070194–ab** bewaart/leest 1d0h bytes vanaf Scheduler+0, inclusief volgende-IDteller. Dit verklaart waarom geladen IDs in dezelfde tellercontext horen; het bewijst geen willekeurige volledige saveherstelcyclus. Het observerprotocol vergelijkt juist één ononderbroken geladen instantie; bij reload, nieuwe eigenaar/Scheduler, teruglopende teller of overflow vergelijking verwerpen.

### Originele gedeelde score

De echte World+168-wrapper **00535500–1b** neemt manager uit engineglobal **00a7ddb8** en roept **005238d0** aan. Getter **005238d7–eb** leest:
1. L = u32(manager+248c);
2. X = u32(L + 4*z);
3. Y = u32(X + 4*x);
4. B = signed16(Y + 2*y).

Bewijs: [wrapper](BINAIR/score-hook-h1-pe-abi.txt), [getter](BINAIR/engine-locatiewaarde-getter.txt), [cache/save](SCORECACHE-EN-INGREEPPUNTEN.md). Dit zijn exact de positie-indexen van de scorecall; niet stilzwijgend naar de canonical terrain/gridcoördinaten van H3 omzetten. Eerst dezelfde aangetoonde kaart-/laagbounds gebruiken. De bestaande observer heeft de manager al; geen World-callback, injectie of berekening in het spel nodig.

### Heap en vernietiging

GroundBuildSettleTree **2007a0a0–a9** selecteert heap vanaf AiMap+58 en wist count op **AiMap+60**; de pointerarray staat op +64. AiCellPtr is zes bytes x/y/heapindex, geen z of scoreveld; z komt tijdens vergelijken uit g_settle_z. Space bouwt dezelfde heap voor andere laag. De globale laag/eigenaar na een pass geeft geen betrouwbare historische context voor ieder achtergebleven entry. Een read-only goalsnapshot hoeft deze heap niet te decoderen.

[Cleanup](BINAIR/settle-activation-h3-cleanup.txt) **20070a4f–60** zet doelen met +24=0 en zonder deletebit op verwijdering. **200711a4–ac** zet Goal+28 bit20h; **20071232–39** voegt toe aan deletelijst. **20070d9a–a0 / 20070dec** verwijdert het ID uit de eigen Planner+a30-tabel; **20070df4–fa** roept de virtuele destructor met delete=1 aan. Dit bewijst mogelijke vernietiging vóór een latere snapshot, niet dat iedere GoalSettle altijd vóór iedere GUIgrens vernietigd wordt. Oude raw pointers daarna nooit opnieuw als huidige goals volgen.

## Kleine observeruitbreiding voor ontwerp

Behoud exacte proefpad/PID, VM_READ-only, modulebasis, volledigheid van bounded reads, dubbele identieke decode en reeds gebonden ownerguards. Geen researchdecoder vervangen door een permissieve heapscanner.

1. Expliciete vertrouwde variant kiezen: original, H1-I SHA `59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0`, of H3 SHA `f93be3629decd38a94117ba774aac3673db2cd2b9e1a0d8a1dde42f7b8e4fd9c`. Controleer het bekende bijbehorende manifest en exacte geladen drie callsites, payload en relevante originele decoderbytes rekening houdend met relocations. Alleen diskhash/headercheck bewijst geen geladen payloadidentiteit. Geen arbitraire --accept-any-hash.
2. Per gevalideerde civ Planner/Scheduler, volgende-ID, arrays/count/capaciteiten en huidige GoalSettle-entries lezen. Neem civ, pointer, ID, flags+28, positie, quality-double en B op. Flag20h is pending deletion, geen nuttige toewijsbare-opdrachttelling. Finite, positieve integerkwaliteit 1..32767 is het H1/H3-contract; afwijking als fout/ongevalideerd rapporteren.
3. Snapshot A direct na dezelfde T0-load vóór de te vergelijken nieuwe pass: bewaar alle IDs én volgende-ID Nvoor. Snapshot B na de gecontroleerde pass in dezelfde instantie: teller Nna. Alleen entries met ID∉A en Nvoor≤ID<Nna zijn nieuwe surviving goals. Nieuw pointeradres alleen is onvoldoende; raw pointers verschillen sowieso tussen H1-I- en H3-processen. Vergelijk varianten op civ/positie/kwaliteit en vastgelegde pass, niet op pointer of identieke IDnummers.
4. H1-I verwacht bij een werkelijk nieuw doel Q=B. H3 verwacht bij een ondersteund huidig plan met B>0 en B<32767 Q=B+1; bij overige/fallback/saturatiecontext Q=B. Een nieuw **Q=B+1** is het kleinste zichtbare onderscheid van de ongewijzigde globale cache. Q=B geeft uitsluitend consistentie met meer dan één route. De snapshot alleen bewijst geen juiste foodplanclassificatie; daarvoor de gebonden feitelijke context/planvoorwaarden lezen of een apart gekend kandidaatpaar gebruiken. H3CurrentResult is lokale adapterstackruimte volgens build-current.py, geen persistent resultaatobject om na afloop te volgen.
5. Bij geen nieuw zichtbaar GoalSettle: rapporteer **niet observeerbaar op dit meetmoment**, geen 'adapter niet actief'. Tellerstijging betreft alle Goaltypen; zij identificeert geen verdwenen GoalSettle.

Twee gelijke reads bewijzen alleen stabiliteit van de opgenomen velden over die reads. Ze zijn geen atomair stop-the-worldbeeld, geen bewijs van startsave, selectiephase, afgelopen calls, correcte stichtingsactie of werkelijke overhead.

## Echte runtimepoort en resterende vragen

De eerste latere C-proef houdt B1, exacte ongewijzigde T0 en host gelijk en start de gekozen DLL opnieuw. Zij moet een nog leesbaar nieuw GoalSettle met gevalideerde eigenaarscontext en Q/B vastleggen. Dat is de minimaal noodzakelijke persistent-statepoort. Het werkelijk bestaan/timing van zo'n venster is nog **runtime-onbekend**; cleanup maakt een garantie uit alleen bestandsbewijs onmogelijk.

Voor de strengere eis 'nieuw gebouwde heap/comparator en constructor gebruiken dezelfde score' is minimaal een waarneming tijdens de echte selectiepass nodig die dezelfde civ/positie en ontvangen/geretourneerde signed16-score bij comparator en doelcall verbindt. Exacte kandidaatbytes plus nieuwe Q geven een machinecodeonderbouwde route-inferentie, geen directe waarneming van heapordening of iedere callback. De bestaande rustige observeruitbreiding alleen volstaat daarvoor niet. Indien de opdrachtgever uitsluitend blijvend nieuw Q≠B als eerste activatiepoort kiest, is geen nieuw analysepakket nodig.

Backlog zonder blokkade voor de kleine decoder: volledige schedulercyclus, alle indirecte constructorcallers, save-/reloadinterleavings buiten dit protocol en verdwijnen van elk individueel doel. Geen uitbreiding naar andere gameplaydoelen.

Afgerond en overgedragen aan root/ctp_ontwerper. Hervat uitsluitend een concrete vraag uit het kleine observer-/runtimevoorstel; geen actieve achtergrondrun.
