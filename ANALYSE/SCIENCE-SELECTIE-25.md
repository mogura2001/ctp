# Science-selectie: wholepassreason 25

20 oktober 2026, 19:19 Europe/Amsterdam (klokcontrole 19:19:25+02:00). Gerichte fase A afgerond; geen actieve analyse na deze overdracht. Ownership uitsluitend dit rapport en VOORTGANG-ANALIST-SELECT25.md. Geen spelstart, RPM, native uitvoering, binary- of gameplaywijziging verricht.

Gameplaydoelen 1/1a/5: nuttige science-locaties laten meetellen in uitvoerbare vestigingsplannen. Concrete wijzigingsvraag: waarom keert de eerste selectie na de bezetcentrumreparatie terug met reason25, en wat is de kleinste onderbouwde vervolgingreep? Ontwerpblokker: de gecomprimeerde foutcode verbergt de specifieke padguard. De brede analyse blijft gesloten.

## Conclusie en dekkingsmatrix

De nieuwe reason25 komt uit `cached_path==0` na de **eerste native direct_path-query, vóór de padpuntenlus**. De alternatieve-indexroute is voor deze pass uitgesloten. Welke van de zestien resterende guards afwijst is niet uit T1 te reconstrueren; geen specifieke binding-, register-, ABI- of padfout is bewezen. De kleinste route naar B is één lokale eerstefoutdiagnose met de hieronder benoemde actuele operands, behoud van huidig beleid en dezelfde ene T0/n/T1-proef. Geen algemene padengineanalyse nodig.

| Beslisketen / vraag | Huidige werking en bewijs | Status / volgende stap |
| --- | --- | --- |
| 1. Alle reason25-routes | Exact twee uitgezonden edges naar select_bad; adressen en guards hieronder | AF |
| 2. T1-betekenis | Query1, punten0, cutoff0 en beginreset isoleren eerste direct_path0; ORDER wordt hergebruikt | AF; grenzen hieronder |
| 3. Code/binding/ABI | Eigen stdcallketen en native ret50h passen; geen concrete oorzaak aantoonbaar met bewaarde outputs | AF als begrensd negatief antwoord; specifieke guard is enige blokker |
| 4. Uitvoerbare route | Eén gebonden eerstefoutrecord, zestien landingen en minimale operands; geen beleid aanpassen | A→B gereed |

## Gebonden bronnen en controles

Pakket: `PROEVEN/science-bezet-centrum/20261020T184100/`. Kandidaat SHA256 `e45313fde4d25a726fa2e8d26dec21c0142ac195ea5c0c40a9b380fd549b166f`; manifest `2077ac8a05d17f6ef7690ceb3a3a9e5555aa8d0f9a23e9e2d9db703288a5396b`. Manifest extension-RVA d9000, eigen state-RVA e3000/497668bytes. Alle adressen hieronder zijn **RVA's van deze kandidaat**, tenzij expliciet engine-VA genoemd; geen civctp.map gebruikt.

De bestaande manifestrecipe is alleen-lezen met de bestaande PE-/Capstonebibliotheken tegen de kandidaatbytes gecontroleerd: selectie159, pad173 en cache91 recipe-rows exact. Ook de disassemblydoelen van de twee edges en de eigen calls kloppen. Dit is een offline bytecontrole, geen nieuwe native- of engine-uitvoering. Relevante bronhashes: native.py `191d67517274e3f83369be0018697999ef1e2dbd6da7e1b1b0dca6f47f2ead93`, policy.py `60a391cea559b37915c4a2b0d7d70c9e619878db198679e8c4531fa32998794e`, union.py `e16dbfbce044405acb05f66211681d5ff839cbcc4351548dc1fd11adc74ef3e8`.

Runtimebron, door root beheerd: [T1](../PROEVEN/science-bezet-centrum-host/20261020/host1/variant/T1.json), SHA256 `7675ffbfcdf7e1f19966ed94f88c37e5c704286b1269687cd09eda7305bfb67c`; [HOST-PROOF](../PROEVEN/science-bezet-centrum-host/20261020/host1/HOST-PROOF.json), SHA256 `a73375ec0f15c6465bdc178aa63a9454b17234e8667b5cff920e4cf153fcfaae`. Bestaande normale sluiting/herstel blijft rootbewijs. Geen claim van atomair snapshot of per-civ producertelemetrie voor alle zeven AI's.

## 1. Exacte select_bad-routes en caller

`native.py:selection`, entry `select_direct_plans` dd4dc; gemeenschappelijk `select_bad` dd817 schrijft Plan.status0/reason25/EAX0, `select_done` eindigt dd83a met ret4. Geen andere recipe-edge naar dit label.

| Edge | Guard en noodzakelijke voorgeschiedenis | Vervolg |
| --- | --- | --- |
| dd5cd `jae select_bad` | `select_alternate` dd5b1: een conflict met een al geselecteerd plan; candidateSlot+72==1 (production), daarna unsigned candidateSlot+76>=64 | Ongeldige prefixindex voor de sciencealternative; geen ALT-read buiten cap |
| dd731 `jz select_bad` | `source_path` dd715: geldige prioriteits-/vertrekclaim; call cached_path dd71e retourneert0. EAX3 gaat eerst naar select_ok; EAX2 gaat naar volgende bron; alleen1 kan positieve bron opleveren | Onderliggende fout24/cache of21/direct_path wordt overschreven door25 |

De alternatieve route gebruikt bij index<64 Plan+74880+index*256, vereist ready==1, en roept `choose_alternative` dcffb aan; anders slaat zij de locatie over. `union.py:roles/choose` produceert prefix uit de begrensde 0..prefix_count-1-lus en kopieert ALT+12 naar Slot+76. Bronmatig is er geen aangetoonde onbegrensde prefixproducer; corruptie is hiermee niet algemeen uitgesloten.

`policy.py:finalize`: na canonical_prefix, succesvolle volledige location_roles, read_set(city en army), citycount==engine_count en order_roles(dd1a4) pusht dac41 Plan/EBX; call dac42 → dd4dc; test dac47, zeroedge dac49 → final_fallback. Fallback zet Gcert0; reason25 blijft staan. final_combine kiest `min(R,max(Dorig,Gcert))`, dus de latere desired5 is **geen** vijf geselecteerde plannen. `integration_base.py:scope_hook` schrijft na AIPUpdate status5/scope0/owner0; dit is normale scopeafsluiting en wist reason/civ/generatie niet.

## 2. Wat bestaande T1 exact bewijst

Laatste gebonden pass civ8/gen7: status5/reason25, context1/context_error0, classified8/prefix8/SCIcalls8, slots3, path_queries1/path_points0/cutoff0, Gcert0, Dorig5/desired5, science_budget_exhausted0. De bezette prefix3 is actueel NO_NOW/reason17/coverage1/foodNone; SCI0 behoudt NOWkeys/marges35/30/25. Dat lokale resultaat is behouden, geen nieuwe geselecteerde scienceclaim.

**Afleiding uit runtimevelden plus exact uitgezonden code:** start_hook(dad0c) wist de gehele Plan per nieuwe generatie; select_direct_plans begint desired0. Een conflict/alternatieve-indexroute vereist eerst een geselecteerd plan. De eerste selectie vereist cached_path1; een nieuwe direct_path1 of2 verwerkt minimaal één punt (count>=1 en puntenlus). De cache is ook per generatie nul. Query3/budget zou cutoff1 zetten en selectie direct via select_ok verlaten. Met query1/punten0/cutoff0 kan er dus geen eerdere succesvolle selectie of bruikbare cachehit zijn geweest. De eerste native query is daadwerkelijk bereikt: de counterincrement staat na de precontextguard en onvoorwaardelijk vóór de call, zonder tussenliggende fouttak. Zij eindigt direct_path0 vóór de puntenlus, cached_path propageert0, dd731 veroorzaakt25. Hiermee zijn dd5cd, de twee cached canonical-inputfouten, een cachehit, de prequery-contextguard en de safety-puntenfout voor **deze pass** uitgesloten.

Niet bewezen: raw native EAX, sourceID/kind/index, gekozen bestemmingsslot, precieze outputcapaciteit/count/pointer, canarywaarden, canonical endpointvergelijkingen, bereikbaarheid of foutieve ABI. Die tijdelijke stackoutputs worden niet bewaard; een lege/ongeselecteerde readeruitkomst bevat ze evenmin. De native query kan zelf0 retourneren, of1 met een door onze wrapper afgewezen output. Engine0 blijft volgens bestaand B UNKNOWN en bewijst geen ontbrekende route/eilandruimte.

**ORDER-fasehergebruik:** canonical_prefix en location_roles lezen ORDER als CAPTURE-indices. `order_roles` herschrijft daarna alleen de eerste `slots` elementen naar gesorteerde **slotindices**. T1 heeft slots3 en ORDER `[0,1,2,1408,356,1444,1446,360]`: een gemengde restbuffer. `reader/partial_diagnostic.py` noemt alle entries nog prefix/CAPTURE; `slot0_matches_CAPTURE=false`, `original_indices_reproduced=false` en historische attributielabels bewijzen daarom geen verkeerde locatie of oude classificatiefase. Prefix voor een slot komt uit Slot+76 en SCI/ALT per-prefixgegevens; post-order locatie komt uit het slot zelf. De oorspronkelijke prefix→CAPTURElijst voor de eerste drie entries is uit deze T1 niet hersteld. Ook `slot0_historical_reason23_diagnostic` is een historische decodernaam, geen actuele passreason. De ware reason25-route bewijst juist dat roles en order_roles voltooid zijn. Scope0/owner0 na afloop is geen stale-passbewijs; snapshot bewaart eigenaar/generatie.

## 3. Caller-/calleecontract en overgebleven guards

| Binding | Contract in aanwezige bytes | Relevante registers |
| --- | --- | --- |
| select_direct_plans dd4dc | stdcall(Plan*), ret4 | Caller-EBX is Plan; EDI slot, ESI bron |
| cached_path dd342, call dd71e | stdcall(Plan*,externalSource*,destinationSlot*), ret12 op dd4d9; Slot begint met externe centrumpositie | EBX/ESI/EDI/EBP opgeslagen/hersteld door eigen pro-/epiloog; EAX return0/1/2/3, ECX/EDX volatile |
| direct_path dc2d4, call dd42e | Zelfde drie argumenten/ret12 op dc63a | Cache-EDI (index) en selectie-ESI/EDI blijven door deze callee bewaard; return EAX wordt vóór overige bewerkingen in eigen spill bewaard |
| canonical_key db6e7 | stdcall(Plan*,external*,outputKey*), ret12; roept engine-VA503f00 met ECX=output en push external aan | EAX wordt expliciet0/1; eigen nonvolatile-registers bewaard. direct_path berekent de endpointer opnieuw na eerste endpointcontrole, dus gebruikt daar niet blind volatile EAX na een call |
| Native pathcall dc3dc | push twintig slots; expliciete interface slot1, geen ECX-thiscall; engine-vtable746220+0c→VA5826a0; ret50h, EAX integer0/1 | Enginebody bewaart EBX/ESI/EDI/EBP; EAX/ECX/EDX volatile. Eigen caller voegt terecht geen extra pop80 toe |
| Native free dc618 | enginebase+1866e0 (VA5866e0), cdecl(pointer), callerpop4 | Iedere nonnull outputpointer wordt ook bij failure vrijgegeven; daarna lokale pointer0 |

Native argumenten volgens bestaande [B4-overdracht](PRODUCER-SETTLERVRAAG-B4.md) en [B-ontwerp](../ONTWERP/PRODUCER-SETTLERVRAAG-B4.md): interface; 0;0;mode1;type;source;destination;&capacity;&pointer;&count;&extra;d8;1;0;0;4096;&searchresult;1;0;1. Outputs eigen nulstorage; canaries op EBP-40/-44. De bestaande gevalideerde [querydump](BINAIR/settler-producer-b4-path-query.txt) toont integer0 op onder meer VA5828e1 en5828f1, succes1 op582a7a en ret50h. Dat rechtvaardigt geen specifieke enginefailureclaim uit reason25.

Geen concrete callerregisterfout gevonden binnen deze keten. De status-/returnpropagatie is bewust verlieslatend voor diagnostiek maar volgt bestaand beleid; een specifieke codefix gokken is niet onderbouwd.

Zestien nog mogelijke `path_unknown`-edges (landing dc5c1, writes reason21/localresult0, daarna free en return):

| Edge-RVA | Guard die afwijst / benodigde operand |
| --- | --- |
| dc3f8 | enginecontext na query !=0 |
| dc408 | canary EBP-40 !=3456ab89 |
| dc418 | canary EBP-44 !=4567bc90 |
| dc428 | raw native EAX, spill EBP-36, !=1 |
| dc436 | outputpointer EBP-20==NULL |
| dc448 | signed count EBP-24<1 |
| dc460 | count>capaciteit EBP-16 |
| dc46b | pointer+count*8 unsigned overflow |
| dc483 | canonical_key(first pathentry)==0 |
| dc49e | canonical_key(expected source)==0 |
| dc4b0 / dc4c2 | first actual versus expected key DWORD0 / DWORD4 ongelijk |
| dc4e9 | canonical_key(last pathentry)==0 |
| dc504 | canonical_key(expected destination)==0 |
| dc516 / dc528 | last actual versus expected key DWORD0 / DWORD4 ongelijk |

Prequery dc356 is uitgesloten door de eerste querycounter; safetyerror dc5a1 is uitgesloten door punten0. Count>4096/pointbudget gaan naar3/cutoff, niet naar25. Een mogelijke paddingvergelijking of native0 is slechts hypothese zolang operands ontbreken.

## 4. Kleine overdracht naar ontwerp

Ontwerper kan één **diagnostische** aanpassing uitwerken, geen gameplayreparatie. Gebruik nieuw pakket afgeleid van exact e45313fd/2077ac8a; historische pakketten intact. Behoud beide selectieregels, alle padcriteria, UNKNOWN/nativefallback, SCI0marges en scope-exclusion. Geen engine-interne instrumentatie nodig.

Het noodzakelijke record is een eigen, per owner/generatie/finalisatie gebonden eerstefoutrecord voor selectie/cached/direct_path, met unique edge-ID voor bovenstaande zestien landingen. Bewaar alleen wat de falende vergelijking verklaart, vóór destructieve spillreset/free: geselecteerd slotindex/prefix/role, vertrekindex/ID/kind, type, externe source/destinationxyz; queryordinal; raw native EAX, capacity/count, pointer-aanwezig/bounds, beide canaries en postquery-context. Bij endpointtak bovendien bereikte-bitmask en de actuele first/last entry en actual/expected canonical keys incl rawbytes, met padding apart. Lees nooit een ontbrekende of ongevalideerde native pointer voor diagnose; reeds door de beleidscode gelezen/omgezette operands volstaan. Markeer onbereikte velden expliciet; nulinitialisatie is geen meting. Latch geen fout uit een eerdere generatie. Bind record aan callsite/return en onafhankelijk eigen Plan zoals bestaande SCI-diagnose; dezelfde log mag de besturing niet beïnvloeden.

Header0..275 is bestaande state/counters,276..511 is bestaande fooddiagnose; daar geen overlap maken. B kiest en controleert de kleinste aparte eigen opslag en finale state-/readerbounds. Geen nieuw observatieraamwerk, geen herstel van de volledige prefixlijst nodig. De reader hoeft voor de huidige vraag alleen het nieuwe record plus bestaande tellers te lezen; noemt ORDER na order_roles expliciet slotvolgorde/mengrest, geen prefix/CAPTUREbewijs. Een pure readeruitbreiding zonder nieuw foutrecord kan vernietigde native stackoutputs niet terughalen.

Meetlat voor B/C: unieke eigen landingen en read-only logging zonder veranderde returns/flags/registers/x87/free; beperkte nieuwe fixturegevallen voor raw native0, postcallcontext, canary, pointer/count en endpointfout, geen oude volledige suite. Daarna precies één nieuwe vasteT0/n/T1 met bestaande afzonderlijke hostpoort, normaal sluiten en Doel3-herstel. Acceptatie is een actueel gebonden specifieke guard plus relevante operandwaarden, gelijke nativefallback en geen foutcredit. Gcert0 of raw native0 alléén is onvoldoende diagnose. Bij bewezen specifieke fout volgt een afzonderlijke concrete B-reparatie; blijft het native0 dan pas de daarbij werkelijk blokkerende engine-/invoervraag, geen algemene padreconstructie.

Tussendoel: SELECT25-A AF (4/4 beslisvragen beantwoord); diagnose-B volgende oplevering. Oorspronkelijke Doel1/1a/volledigeDoel5 OPEN, Doel3 behouden AF. Niet-blokkerende backlog: bredere padmogelijkheden/alternatieven, alle engine0-oorzaken, alle civpasses/performance en volledige gameplaybenchmark. Werk hier gestopt na overdracht, pc aan.
