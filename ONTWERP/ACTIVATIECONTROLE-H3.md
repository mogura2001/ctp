# H3 — beperkte controle van nieuw bewaarde vestigingsdoelen

8 oktober 2026, fase B na geaccepteerde [activatieanalyse](../ANALYSE/ACTIVATIE-VESTIGING-H3.md). Alleen voorstel; geen code, observerbouw, tests, DLL-installatie, spelstart, GUI of livegeheugenactie. Dit document en VOORTGANG-ONTWERPER-H3-ACTIVATIE.md zijn de enige toegewezen bestanden. Root geeft uitleg vóór eventuele C-overdracht.

## Eerste kleine C-poort en doel

Breid uitsluitend [Lees-Onderzoeksactivatie.py](../PROEVEN/ai-uitlezen/Lees-Onderzoeksactivatie.py) uit met een strikt gebonden read-only Planner/GoalSettle/cachedecoder en twee vergelijkbare snapshots. **De eerste poort is controle van nieuwe nog geregistreerde goalstate:** exact vertrouwde geladen variant, juiste civ/eigenaar, nieuwe ID uit dezelfde Schedulerinstantie, positie, opgeslagen kwaliteit Q en actuele gedeelde World-score B. Het resultaat mag melden dat een nieuw doel waarneembaar is en hoe zijn opgeslagen Q zich tot de nu gelezen B verhoudt.

Dit dient [PROJECTDOELEN 1/7](../PROJECTDOELEN.md) en [LOCATIESELECTIE](../LOCATIESELECTIE.md): onderscheid tussen geladen oude goals, nieuwe vestigingsbeslissingen en H3-scoreactivatie. Oorzaak: GoalSettle bewaart Q/ID/positie bij creatie en herstelt die bij load; een huidige vtable of kwaliteitswaarde bewijst dus geen nieuwe H3-berekening. H3 verandert drie scorecalls, niet de gedeelde scorecache. De gewone observer accepteert momenteel uitsluitend originele robotcom en controleert geen geladen kandidaatpayload.

**Deze statepoort vervangt geen H3-eindpoort.** Echte nieuwe heap/comparator- én doelcalls met dezelfde score/ordening en echte totale AI-passtijd **≤1.10×H1-I** blijven onvoltooid. Observerlooptijd, nativefixtures, kandidaatbytes en nieuwe Q afzonderlijk bewijzen die poorten niet. Ook een gelukt nieuw goal bewijst geen gestichte/ontwikkelde stad of duurzaam voedselonderhoud.

## Exact vertrouwde varianten en geladen identiteit

Voeg één expliciete variantkeuze toe: `original`, `H1-I` of `H3-SCORE_CURRENT`. Geen willekeurige hashparameter, H1-M, B2-combinatie of permissieve hashacceptatie. Onbekende variant/manifest/hash/layout weigeren. De oorspronkelijke researchdecoder en eigenaarchecks blijven intact. Bestaande observerbron vóór C: SHA256 `b4270deecf27ac3dbcd6e1a2c08988e474c6d950a0de7f0ce961979852f71b2d`; C rapporteert zijn eigen gecontroleerde diff/hash na de uitbreiding.

Engine blijft exact SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp37d6f702, ondersteunde basis400000. Originele AI-DLL: SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, timestamp37b894e7, preferredbase20000000. Gebruik voor AI-adressen werkelijke modulebasis+RVA; de passende robotcom.map levert de decoderbinding, civctp.map geen engineadressen.

| Variant | Kandidaat-DLL SHA256 | Vertrouwd variantmanifest SHA256 |
| --- | --- | --- |
| original | 3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44 | Geen kandidaatmanifest; exacte originele backup/binary en originele decoderbewijsranges |
| H1-I | 59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0 | [H1-I.manifest.json](../PROEVEN/score-h1/H1-I.manifest.json): 77b1ad5b88343c18ecf7b67de6b2402900b0b39f7edcd0bbd53e1b2bbac7f49e |
| H3-SCORE_CURRENT | f93be3629decd38a94117ba774aac3673db2cd2b9e1a0d8a1dde42f7b8e4fd9c | [H3-SCORE_CURRENT.manifest.json](../PROEVEN/production-h3/H3-SCORE_CURRENT.manifest.json): a4eb2b27da3caf0b5d39fbaff71485a15ef7b829a50e08930feb40b13c2bc238 |

Manifestpins zijn alleen-lezen gemeten op8 oktober16:13. Controleer tevens bestaande pakketmanifesten: [H1](../PROEVEN/score-h1/package-manifest.json) SHA256 `cf334df116b5d22aa480f73fab4e715418a2a02da375c7196d65ed7006914a24`; [H3](../PROEVEN/production-h3/package-manifest.json) SHA256 `f781d4f361af9e8054f4d3ba5176dd6f4c86b2f27cbf4e0b1c533147bad4a665`. Een veranderd pakket krijgt rootreview en nieuwe expliciete binding, geen automatische acceptatie van de nieuwe hash.

Op het **daadwerkelijke readhandle**: exact CTP-proef executablepad/PID en beide modulepaden opnieuw bevestigen, PE32/timestamps/basis/SizeOfImage/sections binden aan de gekozen vertrouwde image, volledige RPM-reads eisen. Behoud QUERY_INFORMATION|VM_READ (0x410), nooit write/injection/callback/suspend/startrechten toevoegen. PIDhergebruik uitsluiten door creationtime en dezelfde processinstantie bij beide snapshots te bewaren; module-/owneridentiteit bij ieder snapshot opnieuw lezen.

Vóór objectdecode ook geladen bytes vergelijken, niet alleen diskhash/header:

- Drie zes-byte sites op AI-RVA784bb/78517/7aa35: original `ff9168010000`; H1-I/H3 respectievelijk `e840bb050090`, `e8e4ba050090`, `e8c695050090`. Alle drie moeten exact bij gekozen variant horen en naar RVA d4000 wijzen.
- Volledige geladen payload vergelijken met de gepinde payload: H1-I RVA d4000,87bytes,SHA256 `4300f151db39bb2061bf08d3ebd494df2c234ca8b4dd99dd60632f729d67060e`; H3 RVA d4000,8640bytes,SHA256 `21873cb38dcbcd39e5ca2f64a2473fe33d3daf11cae4d415c7831704afa65dbf`. H3 in begrensde chunks≤8192 lezen. Controleer sectielayout/SizeOfImage uit gepind manifest en vertrouwde PE, geen headeralleen-identiteit.
- Relevante oorspronkelijke decoderinstructies/vtables blijven exact gelijk: bestaande manager/RobotCOM/Science-ownerroute plus Planner-init/load/Add_Goal/Return_Goal_By_ID, Scheduler-IDinit/toekenning en GoalSettle/ArmyGoal-constructie/serialize en engine World+168/getter. C neemt hiervoor de volledige instructiegrensranges uit de reeds geleverde [goal-layout](../ANALYSE/BINAIR/settle-activation-h3-goal-layout.txt), [ID/lifetime](../ANALYSE/BINAIR/settle-activation-h3-id-lifetime.txt), [ID/save](../ANALYSE/BINAIR/settle-activation-h3-id-save.txt), [cachegetter](../ANALYSE/BINAIR/engine-locatiewaarde-getter.txt) en bestaande ownerdumps op in één kleine vaste bindingtabel; geen nieuwe disassembler/scanner. Verwachte bytes komen uitsluitend uit hashgebonden originele PE via RVA→rawmapping en worden onafhankelijk van kandidaatdata vastgesteld. Leg deze exacte ranges in C-resultaat vast vóór livegebruik.
- Pas bij AI-rebase uitsluitend de **reeds aanwezige gevalideerde PE-HIGHLOWrelocaties** in zulke ranges toe op verwachte bytes/vtablepointers; geen brede maskering van onbegrepen verschillen. Nieuwe payload/calls zijn volgens manifest relatief en krijgen geen willekeurige relocatiecorrectie. Engine is uitsluitend op400000 ondersteund. Onverklaarde geladen-byteafwijking→weigeren.

## Bounded object-/cachedecoder

Hergebruik manager uit engineglobal A7DDB8, Players uit A7DD80, de bestaande32-civ-loop en actorfilter. RobotCOM-vtable AI-RVA89728, RobotCOM+8→AiMain; AiMain+20 en Science-interface+0c moeten civ zijn, Science-interface+8 dezelfde Player, vtable engine744fe0. AIP=Planner+20 en AIP+800→AiMain blijven gecontroleerd. Pointers altijd opnieuw lezen; geen globale g_settle_ai en geen heapscan.

| Nieuwe read | Verplichte guard/uitvoer |
| --- | --- |
| AiMain+94→Planner; Planner+a28→AiMain | Exact eigen actor; AiMain+80/AiMap en +30/World alleen contextidentiteiten, geen heapdecode |
| Planner+a2c→Scheduler; Scheduler+0→nextID | Niet-null/volledig leesbaar; niet-negatieve signed32 teller; dezelfde Scheduler in A/B; daling/overflow/contextwissel verwerpt paar |
| Planner+a30 count; +a38 capaciteit; +a48 Goal*-array; +a4c capaciteit; +a50 ID-array; +a54 capaciteit | 0≤count≤alle drie capaciteiten; pointers geldig bij count>0; strikt oplopende IDs en ID↔pointerpaarcontrole |
| Alle geregistreerde goals: +8 ID | Dezelfde signed32 ID als ID-array; geen duplicaten. Alleen GoalSettle-layout nader lezen |
| Goal-vtable AI-RVA8a558, +0c=5 | Beide nodig voor GoalSettle; andere goaltypes als ID/typecontext opnemen zonder extra subklassedecode |
| Goal+28 flags, +48 double Q, +54 positiepointer | Flag20h=pending deletion, apart markeren; Q finite/positief/geheel1..32767; +54 eerste zes bytes signed16 x/y/z, nooit +58 substitueren |
| manager+248c→L; [L+4*z]→X; [X+4*x]→Y; signed16[Y+2*y]→B | Dezelfde externe scorecallpositie gebruiken, geen H3-terrainingridconversie; ondersteunde laag/daadwerkelijke kaartbounds en volledige pointerreads vereisen |

Eigen leeslimiet: maximaal4096 huidige geregistreerde goals per civ; dit is een veiligheidsgrens van de observer, **geen enginegoallimiet**. Grotere count→expliciet buiten observatiescope, niet trunceren. Alle checked32 pointer-/offsetberekeningen, reads1..8192bytes, arrays zo nodig in vaste chunks en precies countentries volgen. Capaciteiten zijn guards, nooit omvang voor een dump/allocation. count0 is geldige lege tabel, geen decodefout.

De eerste proef blijft grondlaag0. Cachebounds moeten uit de bestaande aangetoonde externe kaart-/scorecontext of het gecontroleerde T0-kaartmanifest gebonden zijn; interne H3-gridx/y niet stil als externe scoreindices gebruiken. Bij ongedekte bounds/context geen B lezen en geen Q/B-conclusie trekken. Dit is een gerichte C-guard op de bestaande cachebinding, geen nieuwe algemenekaart-/cache-eventanalyse.

Uitvoer per snapshot: gekozen variant/hashes/geladen-bytechecks, processcreationtime/PID/modulebases, procedure-runID/snapshotlabel/turn/passlabel, civ/Player/AiMain/Planner/Scheduleridentiteiten, count/capaciteiten/arrayidentiteiten, nextID, **alle huidige goalIDs**, en voor GoalSettle ID/pointer/type/flags/positie/Q/B/cachepointerpad/status. Researchvelden behouden. Geen H3CurrentResult-pointer volgen: dat resultaat is lokale adapterstackruimte en bestaat na call niet als bewezen persistent object.

Iedere snapshot twee complete identieke decodes, inclusief owners/teller/arraybinding/goals/B. Onrust/onvolledige read→geen vergelijking, hernemen op volgend toegestaan rustig moment. Geen onbeperkte busyretry. Twee gelijke reads bewijzen opgenomen-veldenstabiliteit over die twee reads, geen atomair enginebeeld of stabiliteit gedurende de voorafgaande selectiepass.

## Protocol, baseline en invoer

1. **Eerst klein offline C-pakket:** root kan na uitleg de bestaande observer laten uitbreiden/controleerbaar opleveren met uitsluitend bovenstaande guards/velden. Geen DLL-installatie of GUI/liveproef inbegrepen. C mag de bestaande decodercontrole gericht uitbreiden voor deze layout/afwijzingen; geen nieuw framework, heapobserver of trace-infrastructuur.
2. **Afzonderlijke runtimevrijgave nodig:** root stemt eerst af met B2a-uitvoerder die proefbestanden en H1/H3-pakketten bewaakt. Alleen expliciet vrijgegeven exacte variant installeren/starten; geen gecombineerd B2a-hash accepteren. Geen ander CTP-proces aanraken.
3. Controlepaar **H1-I versus H3-SCORE_CURRENT**, dezelfde engine, acht B1-AIPs, regels, rekentijdlimieten, passieve menselijke bediening en exacte [QUOTA-START-T0](../PROEVEN/settlerquota/vaste-start/STARTMANIFEST.md), SHA256 `8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26`, Deity/Gigantic/8spelers. Original is alleen decoder-/referentievariant; H1-M, packing, quota, onderzoek of andere features niet tegelijk wijzigen. Startsave-identiteit en laadhandeling komen uit proefmanifest/bedieningsbewijs, niet uit de observer.
4. Snapshot A rustig direct na die T0-load, vóór de te vergelijken echte AI-pass: alle huidige IDs en Nvoor=nextID vastleggen. Daarna uitsluitend toegelaten bestaande spelbediening voor één vastgelegde echte pass; invoersucces is geen passbewijs. Snapshot B op eerste toegestaan rustig moment na diezelfde pass **in dezelfde ononderbroken instantie**; Nna vastleggen. Geen reload tussen A en B. Eventuele volgende pass krijgt nieuw A/B-paar en apart passlabel, geen onbeperkte zoektocht naar bonus.
5. Nieuw nog geregistreerd goal vereist: ID niet in A, Nvoor≤ID<Nna, zelfde civ/Planner/Scheduler/instance en geldige layout. Flag20h apart: leesbare pending-deletionstate mag creatie zichtbaar maken, maar bewijst geen blijvende bruikbare opdracht. Tellerstijging betreft alle goaltypen en bewijst geen verdwenen GoalSettle. Variants vergelijken op civ/positie/vastgelegde pass/Q/B, nooit pointeradres of gelijke IDnummers over verschillende processen.

Minimale invoer voor latere C: expliciete vertrouwde variant, exact toegelaten CTP-proef-PID, runID/A-of-B-label, externe procedureturn/passlabel en A-resultaat voor B-vergelijking. De lezer start/beëindigt geen game, bedient niets, roept geen World/DLLfunctie aan en schrijft geen livegeheugen. Snapshots/resultaten worden alleen in toegewezen proefresultaatbestanden opgeslagen. Root kiest runtime/humaninput; dit document neemt geen nieuwe GUIvrijgave aan.

## Betekenis van Q/B en meetlat

**Q is creatiestate; B is snapshotstate.** De globale cache kan tussen doelcreatie en observerread veranderd zijn. Daarom is Q−B alleen de actuele gemeten vergelijking. Zelfs een nieuw Q=B+1 is zonder gebonden cache-/contextstabiliteit geen onvoorwaardelijke causale H3-bonusclaim. Bij betrouwbare gelijk gebleven B/context op creatietijd en snapshot is H1-I Q=B verwacht en is H3 Q=B+1 passend bij B>0/B<32767 en toegekende bonus; overige/fallback/saturatie geeft Q=B. Met alleen de rustige decoder blijft dit een door exacte kandidaatbytes onderbouwde **route-inferentie/hypothese**.

Als voor een vooraf benoemde kandidaat dezelfde B vóór/na gelezen wordt, rapporteer die endpointvergelijking apart. Zij sluit tussentijdse cachewijziging met terugkeer naar dezelfde waarde niet uit. Een sterke Q/B-deductie vereist een reeds gebonden stabiele score/context gedurende creatie óf een gerichte in-passwitness van dezelfde positie/ontvangen B/geretourneerde Q. Geen complete cache-eventanalyse of gefingeerde persistente classifierstate om het eerste statepakket sterker te laten lijken.

| Resultaat | Toegestane conclusie |
| --- | --- |
| Alle variant-/layoutguards en stabiele A/B; minstens één nieuw geregistreerd GoalSettle met geldige positie/Q/B | Eerste persistent-newgoal-statepoort geslaagd; exact huidig Q/B en nieuwheidsinterval waarneembaar |
| Nieuw Q=B+1 maar creatiecontext/cache niet bewezen stabiel | Actueel verschil waargenomen; H3-route-inferentie, geen onvoorwaardelijke bonus/classifieracceptatie |
| Nieuw Q=B | Consistent met H1-I én H3-no-bonus/fallback/saturatie; geen bewijs dat H3 niet actief is |
| Lege tabel, geen nieuwe GoalSettle of uitsluitend verdwenen voorbeelden | **Niet observeerbaar op dit meetmoment**; geen 'adapter niet actief' of geslaagde nieuwe heappoort |
| Nieuw ID maar Q/positie/layout/owner ongeldig | Decode/kandidaat/contextfout; geen stateacceptatie |
| Read-/teller-/processwissel/mismatch | Paar verwerpen; geen vergelijking met oude snapshot |

Een gelezen Q=B+1 bewijst geen correcte keuze van drie verschillende open bergen en aparte voedselplek, juiste rations/centrumfood/foodplan, werkelijke workerassignment of nettofood na crime/bonussen. De reader ziet alleen de opgeslagen score; H3 gebruikt een expliciet scenario en haar result is vluchtig. Correcte classifiercontext, echte stichtingskeuze/ontwikkeling/onderhoud en projectwinst vragen hun eigen bestaande H3-meetpoorten.

**Open na deze kleine poort:** tijdens echte selectiepass nieuwe comparatorcalls en nieuwe goalcall met zelfde civ/positie/B/Q en geldige ordening aantonen; totale echte AI-passtijd≤1.10×H1-I en≤43extra eigen directe World-calls per volledige classifiercall zoals [H3-ontwerp](PRODUCTIELOCATIES-H3.md). Niet observerdecode-, GUIwacht- of fixturetijd gebruiken. De kleine uitbreiding levert hiervoor geen teller/trace/timer in de game.

Als cleanup ieder relevante nieuwe goal vóór het rustige meetmoment verwijdert: stop deze vorm van activatieacceptatie na de afgesproken A/B-proef en meld bewijs van niet-observeerbaarheid. Kleinste vervolgvraag is **een begrensde echte in-passwaarneming vóór goalverwijdering voor een benoemde civ/positie/B/Q**, tevens bruikbaar voor de striktere scorecallpoort. Een exact veilig meetpunt/methode is hier niet bewezen; eerst gerichte analyse/nieuw proefvoorstel, geen tracevoorziening of heapscanner bijbouwen. Cleanup hoeft niet algemeen gereconstrueerd te worden.

## Herstel en overdracht

De observeruitbreiding wijzigt geen gameplaystate. Bij decodefout de readhandle sluiten, resultaat als geweigerd/instabiel bewaren, geen correcties in geheugen toepassen. Observerherstel: alleen haar eigen gecontroleerde diff terug naar de gepinde bron; researchdecoder/andere agents' edits behouden via baselinereconstructie. Geen H1/H3-build/pakketbestanden overschrijven.

Bij afzonderlijk vrijgegeven runtimevariant: vóór installatie exacte baselinebackup/hash en afstemming met B2a vastleggen. Na de proef uitsluitend de door root vrijgegeven DLLbasis terugzetten, hashes controleren en verse T0 voor controle gebruiken; variantgoal-/queue/save niet als baseline hergebruiken. Resultaatmanifest en A/B-snapshots bewaren. Deze ontwerprun doet geen installatie/herstelactie.

Reviewbare volgende stap: **zeer klein C-observerpakket voor vertrouwde byte/layoutchecks en nieuwe geregistreerde GoalSettle/Q/B-decode**, gevolgd door rootreview; livepass/variantinstallatie apart vrijgeven. Geen nieuwe gameplayfeature of full-H3-acceptatie. De directe heap/ordening/overheadpoorten blijven expliciet open. Hiermee is deze fase-B-opdracht afgerond.
