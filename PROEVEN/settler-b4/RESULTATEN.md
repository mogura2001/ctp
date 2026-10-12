# B4 beperkte directe productievariant — offline uitvoering

9 oktober 2026, uitvoerder fase C. **Echte emissie en de resterende offline producer/wrapper/compositiecontroles opgeleverd voor rootreview.** Geen installatie, procesuitlezing, spelstart, GUI of gameplaymeting uitgevoerd. Analysebasis en frozen voorstel blijven gelden; deze variant voltooit niet het volledige uitbreidingsbeleid.

## Delta en exacte versies

Beginstand: vier PREPARED-emissies met statische checks en elk32 native owner/conflict/ordergevallen; volledige produceracceptatie nog open. Die oude predicatechecks zijn niet als producerbewijs gebruikt of onnodig herhaald.

Twee routinecorrecties binnen frozen ontwerp `6e310ea5c15f7b3cc42ad75f586bab6bdf14bdee6e63a6639ac7c5f9b2717501`:

1. `native.py`, `safe_point`: na `zero(36)` EDI opnieuw uit het oorspronkelijke externalpointargument laden. REP STOSD verplaatste EDI naar de lokale outputbuffer. De oude echte N25-emissie gaf World+78 én Player+14 dezelfde foutieve stackpointer en eindigde UNKNOWN. [Oud native bewijs](B4-N25.native-producer-old-safety.json) en [oude exacte bron/emissies](checkpoint-pre-validatie/) bewaren de afgewezen versie.
2. `integration.py`, `bind_inputs`: vóór de T/D-inputcalls exact15 bestaande gedeclareerde read-only bodyranges en6 UnitDBslots controleren. [input-pins.json](input-pins.json) bindt de oorspronkelijke engine/DLL-hashes, ranges en zes AI-HIGHLOW-relocaties waar van toepassing. Geen nieuwe adresbinding, brede enginehashloop of strategie. Loaded engine blijft de ondersteunde vaste400000-host; AI-operandwaarden gebruiken loadedbase+RVA.

H3 blijft op RVA `d4000`, B2 op `d7000`, B4 op `d9000`. De toegevoegde guard vergroot RX; daarom ligt de eigen vluchtige RW-buffer nu op **`dd000`**. De oude `dc000` zou met de echte RX-emissie overlappen. Root heeft deze noodzakelijke routine-layoutcorrectie binnen de guardvrijgave geaccepteerd; pakketreview blijft apart. PLAN_SIZE blijft `54800`, plus4 generatiebytes. B2/H3semantiek en de oorspronkelijke actual/priorityopbouw blijven behouden. Geen opgeslagen producerstate of engineveld toegevoegd.

| Variant | Definitieve DLL SHA256 |
| --- | --- |
| H3+B2 controle N25 | `3b1a0ce1023ee041ea08c3ba6132e353e720a1d851ce841027ed8482b12f8519` |
| B4 N25 | `2528673643259ae7fd870834edda404407cd04f328c48fb424e003ba2faf1326` |
| H3+B2 controle N30 | `be2368421c9e4ee709e674b3e22eb5d5f548b41f67623d7ce53b927b44b867d3` |
| B4 N30 | `004dcad1f67a7594d83bb015e1f7c4ef8ff329b8815301ab4453f2c3b1855c23` |

De vier manifests binden payloads, oorspronkelijke preimages, hooks, section/headerwijzigingen, component-RVAs, recepten en inputpins. [Statische checks](prepared-checks.json) bevestigen deterministische reconstructie, exact verklaarde diff, PE/CFG,2453 B4-instructies en unchanged imports/relocatiedirectory. N25/N30 blijven technische fixtures, geen gekozen productiebeleid.

## Werkelijk native uitgevoerd

[Native resultaten N25](B4-N25.native-producer.json) en [N30](B4-N30.native-producer.json): **elk109 echte native calls**, exit0. [Tien helperprocessen](native-processes.json): twee producerhelpers, vier gewone loaders en vier loaders met werkelijk geforceerde rebase; alle exit0 zonder timeout. Dit zijn afzonderlijke32-bit helperprocessen met eigen geheugen; geen engine/gameproces is bevraagd. Reproduceerbaar met de absolute Python312 en `fixture-recipes.py`, `run-native.py`; bouw/check via `build.py`, `check-prepared.py`, `verify-results.py`.

De oorspronkelijke, geemitteerde `AIP::Update`, `Update_Actual_Units`, `Choose_Unit_From_List` en `Update_Desired_Units` draaien in de producerketen. Hun bytes blijven exact die van de echte geladen kandidaat, inclusief de twee bedoelde hooks; de onafhankelijke verifier vergelijkt ze ook met de originele DLL/preimages. H3classifier/currentmodel/rolcode blijven intact. Er is geen mocked G of vervangende producer.

Gecontroleerde native inputs leveren de wereld/database/path/hostantwoorden. De fixture vervangt de dependencies B2Host/H3Host, GetContinent/GetThreat/CanBuild/SchedulerUpdate/GroundBuild, GetSymbol/CityCount, converter/resolver/free en expliciete World/Player/UnitDB/pathcallbacks. De unrelated oorspronkelijke AIP-callees654c0/65cc0/668e0 zijn uitgesloten: geen nieuwe goals, queues of buildings vanuit deze fixtures. B2Symbol/Bit helpers, native agentgetters, Actual/Choose/Desired/AIPUpdate en de producer zelf voeren werkelijk uit.

De **echte `bind_inputs`-guard** is apart uitgevoerd:22 cases per N, één positieve originele-inputcase plus15 gewijzigde bodyranges en6 gewijzigde slots; alle mismatches geven UNKNOWN vóór gebruik. AI-relocaties zijn op de werkelijk herplaatste eigen fixturecopy gecontroleerd. Voor de overige pipelinecases vervangen gecontroleerde native callbacks noodzakelijkerwijs die enginebodybytes/slots; uitsluitend de `bind_inputs`-entry krijgt daar een expliciete vijfbytejump naar een fixtureantwoord. Alle overige B4bytes blijven intact. Deze uitzondering is vermeld in de resultaten; de guard en pipeline zijn afzonderlijke bewijzen. Geen fixturebranch of bypass zit in de kandidaat-DLL.

De freefixture registreert de exacte cdecl-call/pointer en callercleanup; de eigen allocation blijft voor fixturehergebruik bestaan tot helperafsluiting. 'Free eenmaal' in casenamen betekent dus **één nativefree-aanroep**, niet dat de echte engineallocator al is uitgevoerd of een enginepathallocation bewezen vrij is. Echte allocation/free blijft onderdeel van de afzonderlijke hostpoort.

## Resultaten tegenover meetlat

| Acceptatieonderdeel | Gemeten offline resultaat |
| --- | --- |
| Echt G en vijf wrappers samen | START→capture→native AIPUpdate/Actual→finalize→native Choose/Desired/quota→invalidate; G6, desired6, nativepriorityentries6, nativeActual2, rekenverschil4. Geen oorspronkelijke claimsaftrek vervangen of nogmaals toegepast. |
| Voorraad/latere klassen | Nietsettler tussenin behoudt oorspronkelijke vraag2/entries2; eerste settlerklasse draagt geheel D, latere settlerklassen0. NativeActual7 bij multiunitvoorraad behoudt desired6/entries6. De echte supplemental-goalcreatie is in fixtures uitgesloten; verschil4 is geen gemeten game-request. |
| D0 en fallback | Volledig scoped D0 geeft echt +0.0 en nulentries. TokenUNKNOWN, ontbrekende capture en UNKNOWN ná partialG1 behouden alle oorspronkelijke quota. Reentrant START en immutable previewmismatch veroorzaken daadwerkelijk UD2 op exact contract_erroradres; geen succesvolle fallback. |
| Type/current inputs | Exact token, ontbrekende lookup, trailing noninterface-index vóór traitcall, overige geselecteerde settlertypeUNKNOWN, volledige preview. Originele army/citygetters en current Player+c-query; movement16 accepteert,15.999/special/state/multiunits slaan over, NaN/∞/negativecount/cargo/ID/positiemismatch UNKNOWN. Cargo signed16zero met nietnul aangrenzend woord accepteert. |
| Read-only voorraad | Leeg, beide children, namespaceID/kind/cyclus/duplicateguards;4097 nodes geven UNKNOWN na4096 complete reads. Departure33 geeft UNKNOWN bij32 queries, geen gedeeltelijke voorraadacceptatie. Bronset-iteratorbytes ongewijzigd door eigen DFS. NativeActual gebruikt vervolgens haar eigen oorspronkelijke iterator. |
| Plannen/claims/steden | Canonical duplicatecentres eenmaal, echt H3NOW G6, echte mandatoryworkerconflicten geven G1, claims eenmaal en cityoriginhergebruik. N25 C23→D2/C25→D0; N30 C28→D2/C30→D0. H3querycutoff64 geeft hele-passUNKNOWN. Cached typed sourcepath wordt binnen dezelfde pass hergebruikt. |
| Paden/safety | Twintig slots, negen Worldoutputs, inputpointer/xyz, outputcanaries; eigen/exact−1 toegelaten, civ0/foreign niet gecertificeerd, invalidowner UNKNOWN op source/destination/midpoint. Freecallback bij failure/UNKNOWN/cutoff/malformedcount precies eenmaal met juiste pointer aangeroepen. Ordinaryarrival met één pathpoint en actuele armypositie accepteert. Threatpositive afwijzing en NaNUNKNOWN. |
| ABI/lifetime | ESP/nonvolatilechecks op alle109 calls; controlword/depth en op pure/start/capturecalls volledige x87state vergeleken. Doublequota werkelijk door native Desired geconsumeerd. Bij deliberate fatalUD2 audit herstelt alleen de helper naar zijn shim; x87 na exceptionrecovery is uitdrukkelijk geen behoudsclaim. AIPreturn maakt scope/status/owner ongeldig; START wist eigen vaste buffers; geen eigen pathpointer wordt na return gebruikt. |
| Loader/compositie | Alle vier DLLs laden met gewone imports/DllMain en na geforceerde rebase; volledige PICpayloads en gemeten H3/B4calltargets gelijk. B2/H3 componenthashes blijven aan oorspronkelijke emitters gebonden. |
| Beschermde bestanden | Definitieve snapshot21:08:00.883Europe/Amsterdam:3090 installatie/save/T0-paden plus120 eerdere H1/H3pakketbestanden exact gelijk, membership gelijk. [Bewijs](protected-check.json). Root daarna expliciet vrijgegeven voor een afzonderlijke H3-run; deze snapshot blijft het B4-eindmeetmoment. |

De fixtureharness kende tijdens ontwikkeling twee eigen fouten: de eerste ownimage had nog RW-executeprotectie en een malformedcountbranch kopieerde ten onrechte nog een endpoint. Die zijn gecorrigeerd vóór de finale succesvolle helperresultaten; zij zijn geen engine- of gameplayfouten. De safety-EDI-fout hierboven zat wel aantoonbaar in de kandidaat en is met oud/new nativebewijs hersteld.

## Acceptatie, herstel en volgende poort

[offline-results.json](offline-results.json) bindt de voltooide technische controles; [package-manifest.json](package-manifest.json) bindt alle eigen bron/emissie/resultaat/checkpointartefacten. Voorbereid en in eigen pakket toegepast: **ja**. Offline technisch gecontroleerd binnen de expliciete fixture/loader-scope: **ja, rootreview vereist**. In CTP-proef geïnstalleerd: **nee**. Echte hostcontext, engineallocation/padquery/loadedtypewereldbinding, T0/FLI-activatie en performance/gameplay gemeten: **nee**.

Herstel: geen installatie terug te draaien. De oorspronkelijke DLL en beide controlevarianten blijven beschikbaar; checkpoint-pre-validatie bewaart de foutversie, checkpoint-82 de correctie vóór de aanvullende guard. Iedere latere installatie hoort aan de complete verklaarde variant en originele T0 te worden gebonden; geen losse componentpatch of variantsave als baseline gebruiken. Eigen producer-RW is vluchtig; native pathbuffers zijn vóór invalidatie gesloten, geen savewijziging door deze taak.

Per betrokken tussendoel: **uitbreiding naar uitvoerbare behoefte/checkpoint2** ging van gedeeltelijke predicates naar volledige echte producer/wrapper/loaderfixtures, met één echte bugfix en noodzakelijke inputguard. **Goede locaties kiezen** krijgt offline bewijs voor H3NOW/mandatoryconflicts, geen nieuwe gameplayacceptatie. **Gezamenlijke opening** behoudt nativeActual/B2binding en beide Nfixtures; gekozen N/echte Theocracy/FLI blijven open. **Wijzigingen daadwerkelijk actief** en **gecombineerde versie bewezen** blijven open: geen gameplaydelta deze periode. Eerstvolgende concrete oplevering is rootreview van dit pakket en RWlayoutdelta; daarna de afzonderlijke echte host/querypoort, niet automatisch een B4-gameplayrun of volledige policyuitrol.

Uitvoerderwerk wordt na pakketafsluiting gestopt. Geen helperproces blijft actief; geen pc-afsluitcommando/helper/planning uitgevoerd.
