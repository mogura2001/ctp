# Science C1 bron- en interfacecontract

14 oktober 2026. C1 is een ongekoppelde kernel met sciencecredit UIT. Er is
**geen actieve caller in de game**: de nieuwe `.sci1` heeft geen hook/export/union
en verandert geen bestaande aansturing. De actieve U30 Plan blijft `0x54800`.
Dit document beschrijft het reviewbare contract voor een latere toegestane call,
niet een reeds waargenomen hostquery of gameplayresultaat.

## Caller, ABI en lifetime

`stdcall science_model(AiMain*, WorldInterface*, externalCenter8*,
HostBinding24*, callerResult2048*)`, vijf DWORD-argumenten, `ret 20`, EAX is
location_state. Caller levert bestaande leesbare objecten en een exclusieve
schrijfbare resultbuffer van exact 2048 bytes, die niet met inputs overlapt.
Geen fabricated World/city/worker of uit eerdere pass bewaarde hostpointer.
AiMain+30 moet dezelfde World zijn; huidige HostBinding wordt opnieuw uit de
gepinde H3-validator gelezen en alle zes woorden worden vergeleken.

EBX/ESI/EDI/EBP en ESP worden behouden. EAX/ECX/EDX zijn volatile, zoals de
bestaande helpers; arithmetic flags en DF zijn niet preserved (DF eindigt
clear). Eigen x87 `FNSAVE108`/`FRSTOR108` omvat controlword, status, diepte en
registers; tussentijds wordt het caller-controlword geladen. Geen nieuw
roundingmodebeleid. Gemaskerde zes x87-exceptions zijn vereist; reserved
precision PC01 of unmasked exceptions is UNKNOWN vóór rekenwerk/deltaqueries.
PC24 blijft toegestaan voor stand -3..16777212 (2^24-4): zowel stand als
stand+4 passen in24 significante bits, vermenigvuldiging met quarter verandert
alleen de exponent. Daarom blijft `1+stand/4=(stand+4)/4` exact bij iedere
roundingmode. Dit omvat de normale WGFstanden zonder DirectX-PC24 af te wijzen.
PC53/64 staat iedere ondersteunde int32-stand≥-3 toe. CW blijft ongewijzigd. Private
frame is548 bytes plus drie nonvolatile-pushes, dus laagste local EBP-560.
Er is geen onnodige >page stackreservering zonder probe; toekomstig
Plan-scratch4096 blijft alleen schema en wordt niet op C1-stack gereserveerd;
concrete gebruikte offsets staan in `science_layout.STACK`. H2-buffer
`[-480,-224)` wordt pas na alle tilekopieën hergebruikt voor de scenario-
rekenruimte `[-248,-224)`. Future-indices `[-560,-548)` overlappen deze niet.

Caller doet hoogstens één sciencecall tegelijk in dezelfde ononderbroken
AI/Scheduler-context, op de bestaande seriële thread. Geen re-entry vanuit
Worldcallbacks, parallelle science/productionquery, of worldmutatie tijdens
de call. Dat is een **callerpreconditie**, geen in C1 geïmplementeerde mutex.
World+34 gebruikt de echte native World+388/+38c-scratch en originele scan9,
wrap/callback/installationroute. De kernel maakt daarvan geen eigen kopie.
Result wordt bij iedere call geheel nul gemaakt; selected-currentindices gaan
naar -1. Eigen stack verdwijnt bij return. Geen heapallocatie/free, cache,
serialized state, GameActor-write of permanente sciencerol in C1. Caller mag
resultbytes bewaren als uitleg, maar moet owner/civ/generation extern binden;
result alleen geeft geen cividentiteit. Hergebruik als latere credit vereist
een nieuwe geldige call in dezelfde geselecteerde pass.

## Exact resultaatschema

`science_layout.HEADER` geeft elk byte-offset/formaat van header128;
`TILE` geeft tile96. `schema.json` bevat de mechanisch geëxporteerde mappings.
2048 = 128 + 20×96. De eerste open_count (0..20) rows zijn betekenisvol.
Canonical keys en external MapPoint zijn 3 signed16 + padding16; padding
is geen onderdeel van keyidentiteit. Per tile is +32..95 de oorspronkelijke
DEV_TILE64: status/reason/selector/raw+10/raw+20/rawstate/present/materials/
time/advance/double-delta/futurefood/intdelta/terrain/conditions. Voor PRESENT
worden materials/time/advance uit loaded IRR2-doelmetadata aangevuld; actual
IRR3 blijft huidige food en krijgt delta0, geen downgrade.

Structuurflags: 1 hoofd-IRR2 aanwezig, 2 effectief positief IRR2, 4 huidig
IRR2/3, 8 ruimtelijk/current certificeerbaar, 16 canoniek/current geldig,
32 futurefood geldig. Flag32 komt alleen na succesvolle gepinde
development_tile-status1..4/reason0, passende terrain/currentfood en geldige
conditions; UNKNOWN bevat soms intermediate NaN/delta/food en telt nooit.
Status1..3 impliceert door de gedeelde functie eindige exact-int32 delta,
overflowvrije current+delta en niet-negatieve futurefood. PRESENT gebruikt
geverifieerde currentfood zonder extra delta. Metadata/ontwikkelfout trekt
alleen flag32 in: een zelfstandig bewezen NOW blijft geldig.

Location: 0 UNKNOWN, 1 geen huidig NOW-scenario, 2 NOW, 3 structural/spatial
pending, 4 PENDING_GROWTH. Reason10 host/context, 11 rantsoenen, 12 centrum/
tilefase, 13 ongeldige spatialreturn, 14 currentgroeimarge onvoldoende,
15 lokale unknown bij onvoldoende bewezen currenttiles, 16 futuregroei
positief. Spatialreason per tile: 1 false/pending, 2 current unsupported,
3 duplicate, 4 ontbrekende structure, 5 ongeldige shared spatialreturn.
Coverage1 betekent uitsluitend voltooide lokale enum; geen complete wereld,
COMPLETE_G0, readiness of Gcert. Shared fault zet coverage0 en certcount0.
Lokale unsupported tiles blijven apart in current_unknownmask. Alleen
exact0/1-return is geldig; verkeerd vtable/body/World/DB/grid/dimensie/ration-
context trekt hele locatie in. Development-UNKNOWN zit in een eigen mask.

Development-summary is uitsluitend voor de drie geselecteerde CURRENT
indices: 0 UNKNOWN (ook geen complete currentselectie), 1 PENDING (tile1/2),
3 alle READY_NOT_BUILT, 4 alle ALREADY_PRESENT, 5 mix READY/PRESENT.
UNKNOWN domineert PENDING; alle PRESENT is nooit een bouw-PASS. Per-tile
status2 blijft PLACE_UNKNOWN, niet summary-state2. Decoder bewaart raw velden.

## Current en future blijven apart

Current rangt alleen flag8-tiles op currentfood aflopend, canonical xyz
oplopend. Geen bergen- of World+168/B>0-gate. NOW eist drie unieke fysieke
IRR2-tiles, World+34 exacttrue, en alle n1/2/3-marges strikt positief. +10/
+20false blokkeert deze vroege route niet. Centrumfood is current getter plus
echte citybonus eenmaal en expliciet signed64-nonnegative: uitsluitend het
high-DWORD-signbit beslist, low-DWORD-MSB1 is geen negatief64-getal. Positieve
centrumwaarden boven2^31 blijven toegestaan; ieder tilefood nonnegative.
Daarom heeft de aflopende top3 `min(cmax1,cmax2,cmax3)=cmax3`. Consumptie is
exact signed64 `2D_n=20n+5n×stand`; n3/stand1 is 75 halve-foodeenheden,
niet 74. S3_current/margin3/crimebreuk blijven current, ook bij groeitekort.
Geen volledige currentselectie laat die velden nul: betekent niet berekend.

Future rangt **apart** flag32 + structure1/2/8/16 op futurefood/xyz en bewaart
top3 alleen op private stack. Dezelfde n1/2/3-rekening bepaalt native
PENDING_GROWTH uitsluitend bij currentfoodmargefalen met minstens drie
ruimtelijk/current certificeerbare tiles en positieve futuregroei.
Spatialfalse/<3current behoudt STRUCTURAL_POTENTIAL/SPATIAL_PENDING of UNKNOWN,
ongeacht geladen toekomstige food. De per-tile futuredata blijft zichtbaar,
maar verandert die native basestate niet. Er is geen futurefood in current rank/som/marge,
geen tilebonus in centrum, geen scientistconsumptie weggelaten. Geen forecast
van enabling/aanleg/PW/crime/happiness/tijd of extra scientists.

Omdat result2048 exact vol is, worden future-indices/S/marges niet afzonderlijk
in header opgeslagen. `science_result.decode` geeft `computed_future` met
eigen indices, stappen/breuk/readiness en voorwaarden afgeleid
uit opgeslagen tiles. Het voert geen native code uit. `native_pending_parity`
vergelijkt deze afleiding met opgeslagen state, zonder die te vervangen.
Bij coverage0 is parity `None` met status NOT_APPLICABLE_UNTRUSTED_COVERAGE,
geen ongemeten MATCH/PASS; bij coverage1 is de status MATCH of MISMATCH.
Current-summary/velden blijven ongewijzigd; future-summary staat apart in
computed_future. Decoderarithmetic is geen runtime- of gameplaybewijs.

## Querygrenzen en toekomstige C2-sites

C1 per call: H2 max20 open tiles, max20 nieuwe World+34, max20 development,
max60 directe Improvement-calls (+10/+20/+48), max21 primaire foodreaders en
max20 development-herlezingen, dus max41 sciencefoodreaders. PRESENT doet
minder Improvement-calls. Eén World+34 bevat max9 lokale bezoeken, dus max180
voor deze afzonderlijke ruimtetoetsen. Native nested queries van +20/food/H2
zijn extra werk en geen beweerde constante query-/walltimekost.

Passplafonds (64 calls/1280 tiles/spatial/3840 Improvement/2624 foodreaders)
staan als schema in QUERY_BUDGETS; **C1 heeft geen actieve passcounter**.
De latere C2-caller moet vóór iedere call/query/write budget en actuele
owner/generation/scope/fingerprint controleren, counters bij echte callsites
verhogen, prefix-cutoff onderscheiden van malformedcontext en bestaande
runtimegrens behouden. C1 wordt daarvoor niet alvast gekoppeld.

Concrete C2-sites in gepinde U30-bron: `native.PLAN_SIZE`; builder.compose
`generation=rw+PLAN_SIZE`, RW raw/virtual/SizeOfImage en zero-fill;
`integration_base.wrappers:start_hook` zero(PlanSize)/generation/owner en
scope-hook end status5/scope0/owner0; `policy.finalize` rolopbouw;
`native.production_roles/plan_conflict/select_direct_plans` voor alternatieven,
werkelijke keycount en gedeelde bronclaims. Toekomstschema Result[64]
0x54800..0x74800, Alternatives[64×2×128] tot0x78800, Scratch4096 tot0x79800.
De huidige generation-DWORD direct na0x54800 mag dus niet overlappen: bij C2
moet die met het nieuwe planeinde meegaan. Geen engine-allocator voor Plan:
het is module-owned RW; pathallocator/freecontract blijft bestaand. Bij
scope-end worden eigen sciencebevoegdheid/status/counters ongeldig gemaakt;
geen science-H3-resultaat/ORDER/VISITED/scratchoverlay. Al deze C2-sites
zijn nu **ongewijzigd en nog niet geïmplementeerd/gecontroleerd**.
