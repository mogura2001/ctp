# Controlehost3: reason 42 en besluit over de integratiearm

19 oktober 2026, 18:49 Europe/Amsterdam. Gerichte fase A voor Doel1/1a/5, vóór de afzonderlijke science-integratiearm. Vraag: verklaart controle-T10 een integratieblokkerende fout? Alleen bestaande bestanden en kandidaatbytes gelezen; geen helper, test, livegeheugenactie, spelstart of wijziging buiten dit rapport. Vier beslisvragen afgehandeld; analyse gestopt en overgedragen aan root.

## Besluit

**Reason 42 is de expliciete fail-closed terugval van onze producer, geen enginefout of aangetoonde science-integratiefout.** De oorspronkelijke vraag blijft binnen R behouden. De beschikbare snapshot bewijst de precieze genomen tak niet: de reader bewaart het oorspronkelijke statuswoord en de eigen getelde steden niet. Noem het daarom niet bewezen uitsluitend een ontbrekende capture.

De al ontworpen afzonderlijke integratiearm vanaf dezelfde T0 tot maximaal T10 blijft zinvol en technisch verdedigbaar na de bestaande root-/budget-/herstelpoorten. **Stop die arm bij de eerste waargenomen eigen reason42 of context/wholepassfailure**, conform B; reason42 wordt niet als onschadelijke succesvolle pass geaccepteerd. T1 had acht bekende geclassificeerde centra en kan de toegevoegde echte SCI-route bereiken. De vergelijking kan dus ook vóór dezelfde mogelijke terugval nieuwe SCI-evidence opleveren. Verwacht geen positief T10-certificaat op basis van de controle: T5 had alleen onbekende centra en T10 geen overgeleverde kandidaatvoorraad. Geen automatische verlenging als sciencecredit uitblijft. Deze conclusie autoriseert zelf geen hoststart of aanpassing van B.

Een aparte A/B-ingreep in capture is nu niet noodzakelijk om deze ene vergelijking uit te voeren. Mocht dezelfde ontbrekende producerinput de integratie ook blokkeren, is de volgende gerichte vraag de levensduur/voorwaarde van de bestaande groundcapture, niet een nieuwe SCI-formule of groter vast settlerquotum. Oude heapdata hergebruiken zonder generatievalidatie of de guard verwijderen is geen onderbouwde reparatie.

## 1. Exacte bron- en machinecodevoorwaarde

Gecontroleerde controle-DLL SHA256 `738be4098dadc6657b121519213e794ce3ec095025fdc940f6c30a5d89661d66`, PE-timestamp `37b894e7`, imagebase `20000000`. Manifest `d48b63b2363f0bfce2fe4b7d44a83b90951a524ecf3f300bf9661b50080be2a9`. Directe alleen-lezen disassemblage van de aanwezige kandidaat is gebruikt, niet alleen symbolen. Extension-RVA `d9000`; labels zijn relatief daaraan. De overeenkomstige finalize-bron en labels in de science-integratiekandidaat zijn gelijk, behalve de aangeroepen rollenfunctie.

Bron: `PROEVEN/u30-kaartfilter/20261017T115000/policy.py`, `finalize`, regels51–64. `final_fallback` doet achtereenvolgens:

1. `Gcert=0`.
2. Alleen als `reason==0`: `reason=42`.
3. Daarna `D=min(R,max(Dorig,Gcert))`; status4, succesreturn1.

| VA controle-DLL | Machinecode / betekenis |
| --- | --- |
| `200dab57`–`200dab5d` | Bewaart pre-finalize `Plan.status` op `[ebp-10h]`, vóór bind/type/preview/original. |
| `200dab9b` | Schrijft `context=1` nadat die helpers geslaagd zijn. |
| `200dabbf`–`200dabc9` | `cmp [ebp-10h],2`; `jne 200dac60`. Status2 betekent succesvolle kandidaatcapture. |
| `200dac29`–`200dac35` | Vergelijkt `Plan.cities` (+34h) met `engine_count` (+C8h); verschil springt eveneens naar `200dac60`. |
| `200dac60` | `c783bc00000000000000`: Gcert nul. |
| `200dac6a`–`200dac7a` | Test bestaande reason; bij nul `c783040000002a000000`: schrijft42. |
| `200dac84`–`200dacb4` | max(Dorig,Gcert), min met R, schrijft desired en status4. |

Andere fallback-ingangen zijn mislukte canonical_prefix, rollen, read_set of selectie. Die helpers zetten zelf respectievelijk reason41/23/12/25 (eventuele onderliggende fout blijft specifiek); zij verklaren geen onbeschreven reason42 bij normale uitvoering. De twee hierboven genoemde kale controles doen dat wel.

De afsluitende scopewrapper overschrijft later status met5 en wist scope/owner; de gemeten status5 verraadt het oude statuswoord dus niet. START wist de hele Plan en zet status1 (`200dad79`–`200dadac`). Capturehook accepteert alleen status1 (`200dae40`–`200dae4a`) en een passende owner/map. Succesvolle `native.capture` zet status2, een capturefout reason22; contextfout reason33. Dit maakt ontbrekende capture aannemelijk bij nul kandidaten/queries en reason42, maar de alternatieve stadstellingtak blijft ononderscheidbaar doordat beide nodige historische velden niet worden opgeslagen.

**Exact ontbrekend onderscheid:** (a) het pre-finalize statuswoord, oorspronkelijk `Plan+0` en door finalize gekopieerd naar zijn tijdelijke stacklocal `[ebp-10h]`; na return bestaat daarvan geen gepinde duurzame kopie en Plan+0 is door scope_end5 geworden; (b) de eigen getelde `Plan.cities` op `Plan+34h` (52), tegenover het wel opgeslagen `engine_count` op `Plan+C8h` (200). De reader leest losse benoemde header-DWORDs en uitsluitend slot0 als rawhex (`Plan+40600h`,1152bytes). Hij bewaart geen rauwe Planheader, dus deze informatie is ook niet uit bestaande rawhex te reconstrueren. Voor (b) zou een extra bestaande bounded headerread volstaan; (a) vraagt een apart ontworpen observatiemoment of duurzame diagnostiek. Geen van beide wordt hier gebouwd of als aanwezig verondersteld. Deze attributieleemte hoeft de ene aparte arm niet te blokkeren zolang42 een stop-/UNKNOWN-uitkomst blijft; zij verhindert wél een latere claim dat de precieze captureoorzaak bewezen is of een gerichte capturefix zonder verdere A.

Dit is conform de al vastgelegde B4-regel: geen certificaat gebruiken bij ontbrekende actuele capture; zie `ANALYSE/PRODUCER-SETTLERVRAAG-B4.md`, hoofdstuk capturepunt. Het bewijst nog niet dat de gekozen refreshplaats iedere gewenste toekomstige settlervraag kan dekken.

## 2. Wat T1, T5 en T10 werkelijk aantonen

Bron: `PROEVEN/u30-science-filter/20261017T124500/control-reader/host3/variant/T*.json`. Alle snapshots `stable_twice=true`, alle geladen-codechecks true, dezelfde PID27936/creationtijd en kandidaatbinding. Reader vermeldt terecht `save_identity_proven=false` en `atomic_snapshot_proven=false`; een stabiele bounded snapshot is geen atomaire wereldsnapshot.

**Onderstaande producerwaarden betreffen uitsluitend de laatste gedeelde pass, civ8.** Zij mogen niet aan de overige zes civs worden toegeschreven.

| Snapshot | generation | reason/context | engine_count | candidates / gatequeries / gatefalse | known/prefix/classified/H3 | Gcert / Dorig / desired / R |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | 7 | 0 / 1 | 0 | 3584 / 3584 / 3576 | 8 / 8 / 8 / 8 | 0 / 5 / 5 / 30 |
| T5 | 35 | 0 / 1 | 2 | 27 / 27 / 27 | 0 / 0 / 0 / 0 | 0 / 5 / 5 / 28 |
| T10 | 70 | 42 / 1 | 2 | 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 / 5 / 5 / 28 |

T5 is een **normale lege bekende prefix**, geen classifierfout: alle27 gekopieerde centra werden door World+28 uitgesloten. `canonical_prefix` retourneert succes bij known0; production_roles heeft vervolgens nul iteraties en retourneert succes. Selectie van nul slots levert Gcert0. Reason blijft0 en Dorig5 behouden. Geen conclusie dat er nergens goede locaties zijn, ook niet voor civ8: alleen deze huidige gekopieerde, kaartkennisgefilterde voorraad is leeg.

T10 heeft nul queries. Dat bewijst geen27 nieuwe false-antwoorden en ook geen voedsel-/terrein-/SCI-falen: classificatie is niet waargenomen. Context1 bewijst de eerdere binding/type/preview/original-checks, niet geslaagde kandidaatcapture of een compleet certificaat. De onbeschreven42-tak is een begrensde bewijsleemte, geen reden om hem als inputcorruptie of veilige positieve locatie te presenteren.

## 3. Native aantallen per civ

Dit zijn afzonderlijk gelezen native velden; Actual kan aanwezige eenheden en huidig productiefront omvatten en is geen telling van uitsluitend vrije settlers. Op alle drie momenten is native_desired voor alle zeven5. De native aanvullende tekorten zijn de door de reader gerapporteerde waarden, niet zelf als Gcert herberekend.

| Civ | T1 steden(engine) / Actual / tekort | T5 steden(engine) / Actual / tekort | T10 steden(engine) / Actual / tekort |
| --- | --- | --- | --- |
| 2 | 0 / 2 / 3 | 1 / 1 / 4 | 2 / 2 / 3 |
| 3 | 0 / 2 / 3 | 1 / 1 / 4 | 2 / 2 / 3 |
| 4 | 0 / 2 / 3 | 2 / 1 / 4 | 2 / 2 / 3 |
| 5 | 0 / 2 / 3 | 1 / 1 / 4 | 2 / 1 / 4 |
| 6 | 1 / 2 / 3 | 1 / 1 / 4 | 2 / 1 / 4 |
| 7 | 1 / 2 / 3 | 1 / 1 / 4 | 2 / 1 / 4 |
| 8 | 0 / 2 / 3 | 2 / 1 / 4 | 2 / 2 / 3 |

T1/T5/T10 processed_round is voor alle zeven respectievelijk0/4/9. T10 heeft geen current_settler_armies voor alle zeven; civs2/3/4/8 hebben twee settlerfronts, civs5/6/7 één. Dit ondersteunt dat native Actual geen nul hoefde te zijn zonder vrije settlers, maar bewijst niet waarom native de groundbuild wel/niet aanriep in de laatste pass. Deze taak reconstrueert die caller niet verder.

Snapshot-SHA256: T0 `1315a7e16ddcf759509fe78da97dc5c3124b98e3c434b2468f241a48673c6079`; T1 `51a33272384ba2c0a704d34111edc9a38b0abb4701addc60c5cd1a1791061999`; T5 `fcf5208d437616a0c57ab683bea798fe5cb91790a4b8af853068aaf05c4a859d`; T10 `ab690b2324f1c92999e9fd05ff76686b10b09cb4b6061bea7028df72888ce422`.

## Overdracht

Vier vragen afgehandeld: exacte reason42-semantiek met adressen; grens van T10-takattributie; normale T5-nulprefix; native aantallen en proefbesluit. Geen gameplaydoel afgerond door deze analyse. Root kan de bestaande aparte integratiearm beoordelen zonder deze fallback als technische fout te bestempelen. Een vervolg ter verbetering van capture vereist een apart begrensd A/B-antwoord als de daadwerkelijke vergelijking dezelfde lacune bevestigt. Budget18:46 vers vijf66/week95; geen stopgrens. Geen achtergrondwerk actief; pcaan.
