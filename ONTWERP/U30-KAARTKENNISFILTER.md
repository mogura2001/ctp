# U30: lokale kaartkennis vóór de canonicalprefix

17 oktober 2026, 11:46 Europe/Amsterdam. Fase B voor Doel1/1a en LOCATIESELECTIE: nuttige uitbreiding naar30 steden en daarna tot40 onder actieve Theocracy. Basis: afgeronde, door root gelezen [A-overdracht met dekkingsmatrix](../ANALYSE/U30-H2-GATE28.md). Dit voorstel repareert één eigen selectiefout; het bewijst geen grotere settlervraag of extra stichting. B schrijft uitsluitend dit bestand en het eigen voortgangsbestand. Geen code, build, nativecall, spelbediening of binarywijziging uitgevoerd.

## Huidige en gewenste beslissing

World+28→00533580 leest via004bbd50→004ebdf0 een spelergebonden kaartbit8000h, met twee true-overrides. False is binnen het geldige object-/coördinatencontract normale ontbrekende kaartkennis, geen bewijs van fysieke ongeschiktheid. H2 geeft daarbij status0/reason3; H3 geeft0/reason10; onze `production_roles` maakt hiervan hele-pass reason23. De [gebonden hostmeting](../PROEVEN/u30-reason23/20261016T131100/host1/PAIR-PROOF.json) bevat precies dit patroon in de laatste pass: context1/classified1/h3calls1/slots0. Voedsel werd daar nog niet berekend.

Er is een tweede noodzakelijke schakel: [huidige policy.py, canonical_prefix](../PROEVEN/u30-type10/20261015T194300/policy.py) kiest de kleinste64 canonieke keys uit **alle** gekopieerde kandidaten. [native.py, production_roles](../PROEVEN/u30-type10/20261015T194300/native.py) bezoekt vervolgens hoogstens die64. Alleen `roles_next` bij onbekendheid voorkomt mogelijk reason23, maar laat64 onbekende vroege centra alle bekende latere centra verdringen. Daarom is de ingreep één samenhangende wijziging van filter, prefixlengte en consumergrens.

Gewenst: iedere gekopieerde kandidaat blijft eerst aan dezelfde key-/laag-/grenscontrole onderworpen. Alleen centra waarvan de echte kaartkennisquery true geeft doen mee aan de **extra productiecertificering** en de canonicalprefix64. False krijgt geen certificaat en verbruikt geen H3-call. Andere UNKNOWN-uitkomsten blijven de bestaande fallback geven. De gewone native vestigingsketen en oorspronkelijke AIP-vraag blijven actief; onbekende plaatsen worden niet permanent verwijderd of als ongeschikt opgeslagen.

## Bestaande aansturing eerst

[Architectuur](../ANALYSE/ARCHITECTUUR.md), [AAIP-lessen](../ANALYSE/AAIP-LESSEN.md), [beslisketens](../ANALYSE/BESLISKETENS-OVERZICHT.md) en [dekking](../ANALYSE/DEKKING.md) verbinden FLI/profielkeuze met AIP-settlerquota, goallimieten, locatiequeue en native toewijzing. Zij bevatten geen aangetoonde FLI/AIP-instelling die onze toegevoegde H3-UNKNOWNafhandeling of canonicalprefix repareert. Hogere quota wijzigen die fout niet. We behouden die bestaande aansturing voor oorspronkelijke settlervraag en uitvoering; alleen de aanvullende certificering krijgt de hieronder beschreven logica. Geen SLIC, nieuw profiel of nieuw scoregewicht. De enginequery is een concreet bewezen bestaande call binnen onze reeds aanwezige herstelbare adapter, geen algemene modding-hook.

## Exacte kleine broningreep

C maakt een nieuwe eigen pakketmap uit het geaccepteerde type10-pakket `PROEVEN/u30-type10/20261015T194300`, provenance kandidaat `b6f272d2503edf5f1cf03f927ebd40ff5dd82b1a2c9d9c948beb4e7215baed62`. Neem de latere geaccepteerde reason23-readerkopie mee voor observatie. Historische pakketten blijven intact; science-C2 wordt niet gecombineerd.

**1. Eigen header en prefixproducer.** Voeg in de eigen `native.P` vier DWORDs toe: `prefix_count=224`, `known_count=228`, `gate_queries=232`, `gate_false=236`. Huidige benoemde header eindigt bij `classified=220`; CAPTURE begint op0x200. De huidige H3HostBinding beslaat144..167 en de quota-index gebruikt168. Het gevonden `m('esi',224)` is relatief aan een H3-slot, niet Plan. Deze nieuwe velden overlappen daarmee niet. Behoud PLAN_SIZE, arrays, ORDER, strides en alle bestaande offsets. C bevestigt dit met de werkelijke samengestelde bronnen/checker/reader voordat bouwen wordt vrijgegeven. START wist reeds de volledige PLAN_SIZE; initialiseer deze vier velden tevens bij binnenkomst van `canonical_prefix`, zodat de producer zelfstandig eenduidig is. Controleer `nodes==0` vóór hergebruik van VISITED; anders bestaande prefix_bad/reason41.

Pas alleen `policy.canonical_prefix` aan. Houd de bestaande bronindexloop0..candidates−1, canonical_key en keyvergelijker. Controleer candidates binnen0..4096. De key blijft op VISITED[i].key staan; index blijft de oorspronkelijke CAPTURE-index. Geen compactering van CAPTURE en geen herschrijven van de native queue.

```text
prefix_count = known_count = gate_queries = gate_false = 0
for i in [0, candidates):
    external = &CAPTURE[i]              # dezelfde oorspronkelijke 8 bytes
    if canonical_key(Plan, external, &VISITED[i].key) == 0:
        prefix_bad(reason41)           # ook bij onbekend terrein behouden
    VISITED[i].index = i
    gate_queries += 1
    if World.slot28(World, external) == 0:
        VISITED[i].index = -1           # niet selecteerbaar, geen certificaat
        gate_false += 1
    else:
        known_count += 1
for k in [0, min(64, known_count)):
    best = bestaande minimumscan over VISITED[0:candidates]
           met index != -1, dezelfde H3PosCompare
    if geen best: prefix_bad(reason41)  # invariantfout, geen lokale skip
    ORDER[k] = VISITED[best].index
    VISITED[best].index = -1
    prefix_count += 1
if known_count > 64: cutoff = 1
return 1                               # ook bij known_count == 0
```

De query staat **na geslaagde canonical_key en vóór minimumselectie**, niet in H2 en niet alleen na positieveB. Gebruik de originele externe CAPTUREpositie; de omgezette key mag nooit World-input worden. Bewaar die pointer/index in de bestaande lokale stackruimte of herbereken hem na canonical_key; EAX/ECX/EDX zijn callclobbered. De huidige comparator/tievolgorde blijft gelijk. Alle bekende kandidaten houden dus dezelfde onderlinge volgorde; onbekende vullen geen prefixplaats. Nulbekende kandidaten mogen nooit `prefix_store` met best−1 bereiken.

**2. Prefixconsumer.** `native.production_roles` controleert bij entry `0 <= prefix_count <= 64` en `prefix_count <= known_count <= candidates <=4096`; schending houdt reason23. Vervang de loopgrens candidates/64 door prefix_count. Controleer iedere ORDERindex binnen0..candidates−1 vóór index*8; ongeldige index blijft reason23. De oude `roles_budget` op bronkandidaten mag geen cutoff meer zetten omdat onbekende kandidaten geen resterend classificatiewerk vormen; prefixproducer zet cutoff wanneer er werkelijk meer dan64 bekende zijn. Behoud de afzonderlijke `h3calls>=64 → roles_bad`-guard, scoreB-test, H3call, indices/model/foodchecks en slotopbouw exact.

`classified` blijft aantal door roles bezochte prefixkandidaten; gatefalse vóór prefix telt hier dus niet meer mee. `h3calls` telt uitsluitend werkelijk aangeroepen H3, na positieveB. Max64prefix/64slots/64H3 blijven gelden. Voeg geen tweede gatecall in roles toe: de interne H2- en World+ac-gates blijven juist ongewijzigd. Mocht die herhaalde gate onverwachtfalse worden, dan blijft H3UNKNOWN hele-pass reason23. Geen blanket UNKNOWNskip.

Bij lege prefix heeft roles slots0/h3calls0 en succesreturn1. De bestaande latere vertrek-/city-/contextcontroles blijven staan; zij mogen nog steeds falen. Bij verder geldige pass geeft lege selectie Gcert0, met dezelfde eindformule `desired=min(remaining,max(original,Gcert))`. Geen versnelde return die die controles omzeilt; geen claim dat allunknown altijd reason0 garandeert.

**3. Binding en reader, noodzakelijk voor dezelfde reparatie.** Behoud alle bestaande engine-/AI-/inputpins en H3Host/World-/playercontextguards. H3Host pint nu de terrain/foodwrappers en a8/b8, niet World+28; zijn succes alleen is dus geen binding van de nieuwe voorafgaande call. Vóór canonical_prefix moet `bind_host` naast de bestaande World-vtablebinding expliciet slot28 van engineRVA3452e0 vergelijken met enginebase+133580; verkeerde pointer neemt de bestaande bind_bad/reason30. Voeg de volledige37-byte wrapper op engineRVA133580 aan de bestaande ENGINE_BODIES/bind_inputs-lijst toe (einde `ret8`, bewijs [wrapper](../ANALYSE/BINAIR/production-candidate-h2-position-and-cell.txt)). Niet toevoegen aan de bestaande UnitDB-SLOTSdict: die gebruikt een andere vtable. Bodymismatch blijft bestaande inputs_bad/reason36. Neem ook de twee door A verklaarde gatebodies004bbd50 en004ebdf0 met de volledige door A begrensde bodies op in dezelfde bodypinroute; C legt bytes en exacte eindinstructies vast uit de gepinde engine, zonder nieuwe gedragsanalyse of verzonnen lengtes. De bestaande conversieroute503f00 blijft dezelfde. Alle dependencies en nieuwe bron-/reader-/kandidaathashes komen in manifest en loaded-rangecontrole; geen oude hash gebruiken voor de nieuwe kandidaat.

De expliciete interfacevorm is `push external; push World; call [World.vtable+28]`, callee ret8, geen caller-addESP. Dit kan via bestaande `iface(...P['world'],[external],0x28)`; caller gebruikt alleen EAX nul/nietnul. Bestaande proloog/epiloog bewaart EBX/ESI/EDI/EBP; geen x87-instructie toegevoegd. De wrapper gebruikt globale conversiescratch en haar bestaande calls; deze extra calls blijven serieel binnen dezelfde pass, geen thread/achtergrondquery.

Concrete aanvullende pinbron: [bestaande decode004bbd50](../ANALYSE/BINAIR/production-candidate-h2-center-gate-and-placement.txt) toont de volledige body van proloog004bbd50 tot en met `ret4` op004bbd69; aangrenzende NOPs of de volgende functie zijn geen body. Voor004ebdf0 gebruikt C het door de gate28-A afgebakende interval en legt de echte bytes/eindinstructie vast. Als de aangeleverde bytes of grens daarvoor niet eenduidig aansluiten, meldt C precies die pinlacune vóór bouwen; geen zelfgekozen bodylengte of stilzwijgend weglaten van de pin.

Readerkopie leest uitsluitend de vier nieuwe header-DWORDs binnen het reeds gebonden eigen Planbereik en neemt ze op in beide stable_samples. Geen onbekende pointers volgen. Prefixcount certificeert geen productiegeschiktheid: truegate is alleen de filtervoorwaarde. H3-slotdata blijven alleen conditioneel interpreteerbaar. CAPTURE/candidates houden hun oude betekenis. VISITED wordt later door DFS overschreven; reader mag daar achteraf geen bewaarde kaartkennislijst uit claimen. Geen nieuw observerframework.

## Meetlat, volgorde en gelijke start

Eerst uitsluitend bron-/pin-/layoutdiff en rootreview, zonder bouw/native; daarna afzonderlijke bouwvrijgave voor bouwen, disassembly/rel32/checksum/bestaande PE-checks; daarna beperkte callercontroles na vrijgave; pas na uitleg en technische review één echte hostarm. Filter/prefixconsumer vormen één factor en mogen niet afzonderlijk in de game worden geïnstalleerd. Reader verandert geen beslissing. Geen bouw/native/gamevrijgave louter omdat dit B-document bestaat.

Beperkte offlinegevallen met de bestaande finite emitterfixture in een eigen kopie, zonder nieuw fixed-addressframework: (a) nul kandidaten en allefalse geven prefix0/H3calls0; (b) de eerste64 keys false en key65 true selecteert index64; (c) gemengde ongeordende keys leveren exact de kleinste64 truekeys, met dezelfde tievolgorde; (d)65 bekende geven prefix64/cutoff1,4096false geven4096gatecalls/0H3, geen ORDERoverflow; (e) ongeldige canonical_key vóór een falsegate blijft reason41; (f) ongeldige prefix/ORDERindex houdt reason23; (g) andere H3UNKNOWN en een intern later gatefalse houden reason23; (h) nul/nonzero-gatecall en prefixsucces/failure behouden stack/callee-saved. Hergebruik bestaande `NativeU40`-allocaties/interface-stubs voor deze caller-controlflow; een conditionele ret8-stub mag de geselecteerde false/true-verdeling aanbieden. Dat bewijst het nieuwe consumeralgoritme, **niet de echte enginegate of haar bitbetekenis**. Geen hostguard verwijderen om de echte finale pass in de oude stubomgeving te laten slagen; rechtstreeks helper-entrypoints gebruiken. Indien deze beperkte fixture niet uitvoerbaar is: cases eerlijk ONGETEST, concrete reden aan root; geen fixtureherbouw of PASSclaim. Root beslist dan over passende statische plus hostdekking.

Statische technische criteria: alle beschreven grenzen/argumenten en mismatchfallbacks in werkelijke kandidaat zichtbaar; nieuwe header alleen in eigen vrij bereik; bestaande guards/H3/B2hooks/ongewijzigde native vraag en beleidsformule behouden; alle manifestpins consistent. Oude native-uitkomsten zijn geen test van de nieuwe delta. De nieuwe query kost maximaal4096 eenvoudige wrappercalls per pass, met hoogstens64 H3calls; de bestaande keyvergelijkingen blijven begrensd door64×4096. Deze bovengrens is geen gemeten tijdprestatie; werkelijke ronde-/afwikkeltijd registreren.

Hostcriterium: hergebruik dezelfde QUOTA-START-T0, SHA256 `8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26`, dezelfde zeven normale deelnemers/Deityinstellingen en bestaande T0/éénn/T1-procedure. Nieuwe eigen map, gate, verse29backups en pins; geen nieuwe kaart en geen hergebruik van verbruikte gate. Bestaande reason23-hostpaar is directe voorvergelijking voor deze ene factor; de bekende UI-/saveatomiciteitsgrens blijft vermeld. T0/T1 tweemaal stabiel, dezelfde PID/creationtime/geladen kandidaat en echte slot/body; alle zeven native rondes−1→0, één inputtoken/éénn, geen retry/T2.

Runtimeacceptatie van dit herstel vereist in de laatste gebonden pass gate_false>0, succesvolle prefixinvariant `prefix_count=min(64,known_count)`, `gate_queries=candidates=known_count+gate_false`, classified<=prefix_count en h3calls<=classified<=64, plus geen reason23 wegens die vooraf uitgefilterde centra. De oudeclassified1 hoeft niet terug te komen. Bekende latere locaties moeten in beperkte callercase(b) worden bereikt; in de echte start kan known_count0 zijn. Een andere resterende failure levert alleen gerichte vervolginformatie. Een H3slot/certificaat, verhoogde gewenste vraag en werkelijke stichting blijven drie afzonderlijke bewijzen. Deze korte ronde kan30/40steden niet accepteren.

Gebruik de bestaande bediening en tijdgrenzen uit [U30-TYPE10](U30-TYPE10.md), AUTOMATISERING en actuele rootproefprocedure: geen blokkerende wacht>60s, meting/afwikkeling meteen na T1/fout, uiterlijk bestaande600/690/720s-grenzen. Bij focus/CD/modal/binding/stabiliteitsfout stoppen zonder tweede start. Voor pakket/start/n en voortgang verse budgetcheck; week<=25 waarschuwen, week<=10 of vijfuur<=5 projectstop/checkpoint, pcaan.

## Onbekend terrein, risico's en alternatieven

De filter is tijdelijk per pass. CAPTURE en native queue blijven intact, de volgende pass queryt opnieuw en nieuw verkende centra kunnen dan certificeren. Bij uitsluitend onbekende vroege keys zoeken we binnen alle maximaal4096captured kandidaten naar bekende latere keys. Bij uitsluitend onbekende captured centra blijft oorspronkelijke AIP-vraag via dezelfde final_max behouden. Bestaande native GoalSettle/selectie/reis/stichting blijft het beschikbare uitvoeringspad; dit voorstel claimt geen bewezen volledige nieuwe productie-/sciencebeoordeling buiten kaartkennis.

Hiermee beperken we **dit certificaat** tot informatie die H2 al kan leveren. Het projectdoel blijft ook onbekende, later nuttige locaties omvatten. Als de host geen bruikbare bekende certificaten heeft, of die begrenzing de eerstvolgende nuttige uitbreiding daadwerkelijk blokkeert, is de ene eindige A-vraag: **welke al aanwezige native route levert voor een verder geldige captured onbekende centrumpositie de bruikbare werkplekken/terreingegevens zonder de World+28/World+ac-kennisgate, en welk bestaand AI-perceptiecontract geldt daar?** Lever concrete caller/query/ABI/bodybinding of een concrete blokkade. Eerst bestaande settlementketen volgen; geen algemene heranalyse, nieuwe fixture of GUIreeks. Deze vraag blokkeert de lokale reparatie niet; zij is vereist vóór een ungated certificaat voor onbekend terrein.

Verwacht effect: normale ontbrekende kaartkennis beëindigt de extra pass niet meer en onbekende keys verdringen bekende niet binnen64. Mogelijke neveneffecten: andere bekende centra worden nu bezocht; downstream H3-/bereikbaarheidsfouten worden zichtbaar;4096 extra lichte queries kunnen rondetijd verhogen. Geen verbetering in voedsel, veiligheid, transport of netto economie veronderstellen. De prefix blijft een eindige canonieke steekproef: meer dan64bekende en niet-positieveB's kunnen nog nuttige latere locaties missen; dat is de bestaande afzonderlijke budget-/volgordebeperking, geen claim van volledige locatiekwaliteit. Niet nu ongevraagd4096H3calls of nieuwe ranking toevoegen.

Alternatieven: alleen H3reason10/H2reason3 lokaal skippen verspilt H3budget en herstelt de prefix niet; alleen een gate vóór H3 herstelt de prefix evenmin. Alle UNKNOWNskip verbergt echte fouten. H2gate verwijderen volstaat niet omdat World+ac dezelfde gate herhaalt. Enginekaartbit/overrides zetten vervalst kennis en valt buiten de opdracht. Hogere AIPquota herstellen de eigen filterfout niet. Ungated classificatie vereist bovengenoemde A-vraag. Science-C2/nieuwe ranking/andere quotas krijgen na dit aparte herstel hun eigen combinatieproef; geen effecten daarvan aan deze filter toeschrijven.

## Herstel en overdracht

Archiveer bron, manifest, diff, kandidaat, offlinecases, beide hostmetingen/screens/logs en autosave. Sluit uitsluitend eigen game normaal, bevestig exit/verse count0, herstel daarna de gecontroleerde Doel3-release `PROEVEN/doel3/20261012-release-v1` (DLL `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890`), alle29beschermde bestanden/saves/profiel/default-autosave op vooraf gecontroleerde hashes. Nieuwe autosave dubbel bewaren, alleen eigen vooraf afwezige bytegelijke alias verwijderen, gate verbruiken. Bij sluitfout geen DLLherstel of forcekill: instance/checkpoint bewaren en herstel expliciet open. Geen pc-afsluiting. Bronterugkeer is de onveranderde type10-provenance; readerterugkeer de vooraf bewaarde kopie. Geen saveformatwijziging of persistent kaartkennisbit door deze reparatie.

Doel1/1a: analyse afgerond; voorstel inhoudelijk gereed voor rootreview en gebruikersuitleg; technisch/gegameplaytest open. Geen oorspronkelijk gameplaydoel afgerond. Eerstvolgende reviewbare C-oplevering: nieuwe eigen bronnen met exacte pin-/prefix-/consumerdiff, vervolgens geaccepteerde kandidaat en beperkte controles vóór de ene hostarm. Geen ontbrekende routinekeuze van gebruiker; een afwijkend perceptiebeleid wordt niet stilzwijgend gekozen. B stopt na overdracht; root beheert voortzetting en PROJECTSTATUS.md.
