# Schone native padnul lokaal behandelen

22 oktober 2026,18:00 Europe/Amsterdam. Fase B voor Doel1/1a; A3/3 in [PAD-ONBEKEND-EN-SELECTIEPREFIX](../ANALYSE/PAD-ONBEKEND-EN-SELECTIEPREFIX-2026-10-22.md) overgedragen en door root geaccepteerd. Drie ontwerpvragen hieronder beantwoord. Alleen voorstel; geen broncode, bouw, nativefixture, RPM of spel bediend.

De bestaande kandidaat df3ac89d… gaf op dezelfdeT100-start121 tegenover86 steden, alle zeven hoger/Theocracy behouden; geen civ bereikte30. Op zes echte civ8-passes T70/71/81/84/85/86 is een schone nativequery0 met lege output, vrije postcontext en intacte canaries gebonden. Nu wordt daardoor de hele selectie teruggezet, vóór andere bronparen geprobeerd worden. Niet bewezen is dat deze passes een geselecteerde positieve prefix verloren of dat andere bronnen positief zouden zijn geweest. Interne zoekoorzaak blijft UNKNOWN; T100 zonder padqueries is een andere keten.

Voorstel: uitsluitend zo'n **aantoonbaar schoon onbeantwoord paar** retourneert eigen4. Het geeft geen credit, maar laat bestaande selectie verderzoeken en reeds volledig bewezen onafhankelijke certificaten behouden. Meer kansen is een verwachte mogelijkheid, geen30-garantie. Volledige ruimte-/transport-/queueafstemming blijft OPEN.

## 1. Uitvoerend contract: binding, lokale4 en cleanup

Basis is gepinde `PROEVEN/selectie-pad-diagnose/20261020T192500`, kandidaatSHA `df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e`, manifest `5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152`. `native.py:path`/`path_cache`/`selection` en `policy.py:finalize` zijn de uitvoerende ingreeppunten. FLI/AIP leveren de bestaande gezamenlijke vraag; zij onderscheiden deze nativequeryuitkomst niet. Extra FLI-quota of SLIC is daarom geen passende ingreep. Een diagnosebuffer is geen beleidsinput of modding-hook.

Voeg alleen de ontbrekende **vergelijkende uitvoeringsguard** toe, onafhankelijk van Trace. Controleer bij het huidige selectieslot vóór directcall, na nativecall vóór toelating4 en vóór cachehit/verderzoeken/credit:

- Planpointer exact de herbaseerde eigen `pass_state`; scope1, guard0, context1, context_error0. Owner nietnul en gelijk aan eigen actuele owner-snapshot opPlan+0x78800; generation>0 en gelijk aan eigen snapshot+0x78804 én huidige globale generation. Civ1..31 gelijk aan owner+0x20. Bij mismatch hard0, geen prefixcredit.
- Hergebruik de reeds uitgevoerde bind_host/bind_inputs-controle op AiMain/planner/scheduler/interfaces/civ/vtables/callee; geen tweede fingerprintlaag of herhaalde bind_host die velden overschrijft. De aanvullende vergelijking beperkt zich tot huidige owner/civ/generation, eigen Plan/scope en bewaarde callinputs: host/path/world/player/type/d8 onveranderd, owner+34 nog dezelfde pathinterface. De bestaande20args/callee blijven exact. Nieuwe guard vergelijkt en herschrijft geen identiteit om een mismatch weg te werken.
- Plan/type/d8 binnen bestaande resolvercontract; onveranderd tijdens call. Slotindex<slots<=64, vertrekindex<departures<=32, geldige prefix/rol en directe argumentpointers exact naar de huidige eigen slot-/departurebytes. Bewaar/vergelijk type, source/destbytes, bron-ID/kind/claim en canonieke source/destkeys rond call. Gebruik huidige canonical_key en departuresvoorwaarden; conversiefout of veranderde binding blijft hard. Geen Tracevelden hiervoor lezen.

Gebruik bestaande frame-/eigen locals voor dit kleine call-snapshot; geen nieuwe persistent engine-interface. Aanvullende mismatchcheck is uitvoerend, ook als logger niets publiceert. Onbekende/inconsistente eigen telling of status maakt de lokale route ontoelaatbaar.

In direct_path wordt alleen de huidige edge4 gesplitst **na** postcontext- en canarychecks: nativeEAX exact0, precontext0/postcontext0, canaries3456ab89/4567bc90, capacity0/count0/pointerNULL en bovengenoemde binding ongewijzigd → eigenreturn4. Cap/count/pointer komen rechtstreeks uit huidige querylocals−16/−24/−20, nativeEAX uit−36. De nulslots hoeven niet door native geschreven te zijn; ze bewijzen uitsluitend de schone lege uitvoervorm. Geen pathbuffer lezen, geen endpoint-/veiligheidsbewijs uit native0 afleiden.

Local4 roept **niet** native.unknown aan: status/reason/context_error blijven geldig; geen bestaande fout wissen. Zet alleen de lokale return op4 en ga door de bestaande path_free/epiloog. Nonnull buffers blijven op alle andere routes precies eenmaal engine005866e0/cdecl-vrijgegeven; lokale4 heeft pointerNULL. Originele twintig argumenten, callee-ret80, direct-ret12/cache-ret12 en registers/flags/x87 blijven volgens bestaande ABI. Cleanup-/ABI-onzekerheid blijft hard.

| Eigen return | Cache/selectie/finalisatie |
| --- | --- |
|1|Enige positieve padcredit; alle oorspronkelijke endpoint- en safetychecks blijven verplicht.|
|2|Bestaand niet-gecertificeerd-veilig; source_next, geen positieve credit.|
|3|Bestaande budgetstop; behoud uitsluitend gecommitte positieve prefix, geen lopend slot toevoegen.|
|4|Alleen schoon lokaalUNKNOWN; passlokale cache4 en source_next, geen used-markering of nulruimteclaim.|
|0 / onbekende code|Hardfailure; select_bad/final_fallback, gehele Gcert-prefix ingetrokken. Onbekende integers niet als2/4 behandelen.|

Cache blijft dezelfde begrensde(type,canonieke source,dest)→eigenresultaatarray; geen nativepointer opslaan. Laat alleen expliciet1/2/3/4 als geldige cachewaarden door. Herhaling van hetzelfde4-paar in dezelfde pass gebruikt geen nieuwe nativequery; een ander paar wel. START wist cache zoals nu; geen generatieoverschrijdende UNKNOWN-cache. Iedere echte nulquery telt mee.128query/cache,4096zoek-/padpunten,32vertrekken,64prefix en40selected/R blijven gelijk.

source_path: behandel4 expliciet als source_next. Bestaande selectedslots, mandatoryconflicten en gebruikte single-unit/frontclaims blijven staan; een eerder gevonden positieve bron voor het lopende slot blijft kandidaat wanneer een volgende bron4 geeft. Volg bestaande existing→front→newbuild en laagste-rawIDkeuze. Herbruikbare bouworigin blijft herbruikbaar. Alleen1 commit een slot; na uitgeputte bronnen gewone volgende prioriteit/bestemming.

Hard blijven: pre/postcontext, canaries, native!=0/1, native0 met nietlege of afwijkende outputs, native1 met malformedbuffer/capacity/overflow/endpoints, canonicalkeyfout en safetyUNKNOWN. Geen native0-intern onderzoek, transportclaim of safetyversoepeling. finalize gebruikt uitsluitend werkelijk positief geselecteerde Gcert; quotaformule `min(R,max(Dorig,Gcert))`, consolidatie/priorityentries, Actualaftrek en30/40gates blijven exact. Cache4 markeert zelf de lokale onvolledigheid; geen nieuw completenessveld nodig omdat Gcert altijd ondergrens blijft. Gcert0 bij lokale4 blijft normale Dorigfallback, nooit COMPLETE_G0/pauze.

## 2. Minimale bron- en decodercompatibiliteit

C1 krijgt eigen pakket/bronkopieën; historische kandidaat/bewijsbytes blijven intact. Alleen path/kleine compareguard/cache-/source_path-dispatch aanpassen. Finale formule en overige emitters inhoudelijk gelijk; bouwadressen worden later opnieuw uit eigen manifest gebonden, historische RVA's zijn geen patchlijst.

De bestaande edge4logger/reader heeft nu hard0/cache0/selectie0/fallback als contract. Behoud deze oude decodebranch. Voeg alleen noodzakelijke herkenning van **local4** toe aan dezelfde diagnosevorm: schone nuloperanden plus directe/cache4 en een geldige normale selectiereturn; label `LOCAL_UNKNOWN_PAIR`, nooit certified/selected/no-route. Alle bestaande manifest/call-/Plan-/generation-/object-/reachedmaskbindings blijven. Publiceer de lokale uitkomst pas met geldige propagatie; indien de bestaande ene recordruimte niet alle nieuwe propagatie kan representeren, rapporteer die combinatie UNKNOWN in plaats van Falsebewijs of nieuwe observer. Oude opgeslagen diagnose blijft leesbaar met zijn eigen manifest/schema; geen oude traces herschrijven.

Geen nieuwe per-civobserver, loggingraamwerk, enginehelper of beleidsinvoer uit diagnostiek. Geen rol/packing/prioriteit/klasse/floor/30/40aanpassing. De winst121vs86 blijft voor de bestaande combinatie gelden; deze ingreep krijgt eigen acceptatie.

## 3. Beperkte verificatie en afzonderlijke poorten

**Eerst C1 bronoverdracht:** compacte diff/pins, uitleg uitvoerende guards/returndispatch/cleanup en noodzakelijke oude/nieuwe decodercompatibiliteit; syntax/import zonder emissie, native of RPM. Rootreview vóór bouwpoort. C1 is geen toestemming om kandidaat te bouwen, nativecases te draaien of spel te starten.

Na aparte rootvrijgave volstaan uitbreiding van bestaande gerichte nativecases:

- Schone native0 bronA→4, daarna positiefB→slot; A geenclaim/credit. Cachehit4 geen extra query; ander paar wel. Positief reeds gekozenB blijft bij later4 in hetzelfde slot.
- Positief gecommitte slot→lokaal4→later positief slot behoudt alleen volledige conflictvrije credit; eenmalige claims/conflicten en herbruikbare bouworigin gelijk.
- Stale Plan/owner/civ/generation/argumentkeys, pre/postcontext/canary, native0 met cap/count/pointerafwijking, native2/−1 en native1 malformed/endpoints/safetyUNKNOWN blijven hard0 en trekken prefix in. Bewijs native1/safetyregels afzonderlijk ongewijzigd.
- Budget3 behoudt gecommitte prefix;128grenzen/4096punten eindig. Nonnullcleanup exacteenmaal en ABI/canaries behouden. Gelijke Dorig/Gcert/R/Actual houdt gelijke quota én priorityentries.

**Daarna eventuele begrensde hostpoort:** root bepaalt afzonderlijk run/horizon na nativeacceptatie; dit voorstel start of ontwerpt geen nieuweT100-proef. Gebruik dan dezelfde vasteT0, passieve mens/alle zeven, gelijk gehouden19config/effectieve118protected, bron-/module-/proces-/vensterpins, eenmalige tokens, volledige natuurlijke ronden, versebudgetchecks en bestaande normaleclose/archief/herstelprocedure. Vergelijk met de bewaarde huidige kandidaat als juiste ingreepreferentie; Doel3-release blijft herstelinstallatie. Geen ongelijke eindbeurten of onbekende referentietussenmetingen als gepaarde winst presenteren.

Meetlat voor zo'n vrijgegeven proef: gebonden local4 veroorzaakt geen helefallback, geen credit voor dat paar; waar werkelijk aanwezig volgt positieve andere bron/prefix. Meet echte steden/onderzoek/regering per civ en eventuele Gcert>Dorig/extra aanvraag uitsluitend bij geldige eigen passbinding. Lokale4 zonder gevonden alternatief is geen succes in uitbreiding; meer queries alleen evenmin. Stadswinst is pas gemeten bij echte gelijke start/horizon;30, nuttige40 en volledige rem blijven open tot aangetoond.

Risico: meer paren kunnen budget eerder vullen; bestaande3 stopt eindig. De nieuwe guard kan bij onduidelijke context conservatief vaker hardfallback geven. Verwacht voordeel is minder onnodig verloren vervolgkansen; omvang onbekend. Alternatieven (native0als2/geenroute, alle0overslaan, floor verwijderen, hogere caps) missen deze scheiding en zijn afgewezen. Bij regressie herstel exact oude df3ac89d-kandidaat voor de proefreferentie; normale installatie na procesexit terug naar getesteeb6f-release, allebeforebestanden/archieven controleren, gatesFalse, pcaan.

B3/3 gereed: exacte lokale4contract/guards, minimale brondelta en beperkte verificatie/latere meetpoort vastgelegd. Root presenteert uitleg vóór toepassing. Voorstelagent stopt na overdracht; geen actief achtergrondwerk of extra causaal onderzoek.
