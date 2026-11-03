# Onbekend padpaar en behoud van selectieprefix

22 oktober 2026, 17:54 Europe/Amsterdam. Gerichte fase A voor Doel1/1a, drie beslisvragen. Alleen bestaande gepinde bronnen, oorspronkelijke DLLanalyse en opgeslagen T100-snapshots gelezen. Geen game/build/native/RPM, binary-/gameplaywijziging of nieuw hulpmiddel. Scope bereikt; overdracht naar B.

**Kleinste route is nu concreet:** onderscheid uitsluitend een schone oorspronkelijke nativequeryreturn0 als lokaal UNKNOWN-paar. Onderzoek daarna andere bronnen/bestemmingen binnen de bestaande budgets en behoud eerdere volledige positieve certificaten. Canary-, context-, malformed-output- en endpointfouten blijven hele-passfallback. Geen query0 als geenroute/geenruimte tellen; geen quota-, floor-, priority-, rol-, packing- of30/40wijziging.

## 1. Huidige nulbranches en daadwerkelijk opgeslagen reden

Basis: huidige kandidaat `df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e`, manifest `5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152`, pakket `PROEVEN/selectie-pad-diagnose/20261020T192500`. Relevante bronnen: native.py `path`, `path_cache`, `selection`, `safety`; policy.py `finalize`; path_diagnostic_layout.py/Trace en bestaande reader/path_failure_decoder.py. Geen oude B4 whole-budgetfallback als actuele policy lezen.

De huidige kleine returnruimte is:

| Return | direct_path/cached_path | selectie |
|---|---|---|
|1|Volledig bewezen direct veilig pad|Positieve bron voor dit slot; laagste rawID binnen bestaande prioriteit kiezen|
|2|Niet gecertificeerd veilig door bestaande safetycriteria|Bron overslaan; geen positieve credit, andere bron proberen|
|3|Technische query/cache/padpuntenbudgetgrens|select_ok: bestaande geselecteerde prefix behouden, lopend nog ongecommit slot niet toevoegen|
|0|UNKNOWN, context/integriteit en onvolledige native-uitkomst gebundeld|select_bad/reason25; final_fallback wist Gcert naar0|

`native.unknown(reason)` schrijft status0/reason/EAX0. direct_path gebruikt reason21, cached_path-keyfout reason24 en selectie overschrijft dit met reason25. Daardoor kan reason25 alleen de suboorzaak niet onderscheiden. De diagnosebuffer doet dat soms wel; hij is uitsluitend bewijs en geen beleidsinput.

### Zes echte reason25-passes: subbranch reeds bewezen

De zes bestaande bestanden `PROEVEN/uitbreiding-lang/20261022T122400/U30-40/T{70,71,81,84,85,86}.json` bevatten alle `path_failure_diagnostic.attribution_status=BOUND_COMPLETE_GUARD_OPERANDS`, usable=true en **edge4/native_EAX0**. Alle zes: postcontext0, canary1=3456ab89, canary2=4567bc90; cap/count/pointer0; direct/cache/selectionreturns0. Geen nieuwe reader of runtime nodig om dit vast te stellen.

| T | Generation | Query | Slot | Departure | Slots totaal | Padpunten pass |
|---|---|---|---|---|---|---|
|70|508|1|0|11|1|0|
|71|515|2|1|12|2|2|
|81|585|1|0|12|1|0|
|84|606|1|1|13|2|0|
|85|613|1|1|13|3|0|
|86|620|1|2|13|3|0|

Deze gebonden calls horen bij civ8, type4/kind1, bron externe(25,69,0), verschillende gebonden bestemmingen. Andere civs blijven onbekend. De readercontrole bindt huidige Plan/snapshot/generation, echte drie callparen, bron-/slotindices en bytes, native0→cache0→selection0 en exact het eerste falende guardpad. De cap/count/pointervelden zijn waargenomen eigen outputslots; nul bewijst niet dat de nativecall deze heeft geschreven. T71 heeft eerder twee padpunten verwerkt; dit bewijst op zichzelf geen eerder geselecteerd, conflictvrij certificaat. Een verloren positieve prefix op deze zes echte passes wordt daarom niet aangenomen.

T100 heeft reason0/classified0/slots0/pathqueries0. Dat is een andere keten en wordt niet aan reason25 toegeschreven. De zes gevallen verklaren evenmin de hele T100achterstand of garanderen30steden na een wijziging.

### Nulbranchmatrix uit huidige code

De zestien oorspronkelijke guards worden nu alle naar `path_unknown` gerouteerd; layout noemt historische parent-RVAs, het huidige manifest bindt de werkelijke emissie. Hieronder betekent “hard” uitsluitend dat deze kleine ingreep de hele pass blijft afwijzen; niet dat ieder geval een bewezen enginebug is.

| Branch / codepunt | Huidige betekenis | Kleinste veilige indeling |
|---|---|---|
|Vóór call: host+6d0b94!=0|Native padcontext al actief/reentrancy|Hard; geen query, geen prefixcredit|
|Edge1 postcontext_nonzero|Native context na call niet vrij|Hard; geen verdere calls|
|Edge2/3 canarymismatch|Eigen queryoutputframe/ABI niet betrouwbaar|Hard|
|Edge4 native_EAX_not1|Bundelt gewone0 en onverwachte andere codes|Alleen exacte0 met aanvullende schone contractvoorwaarden kan lokaal UNKNOWN worden; andere codes hard|
|Edge5 pointerNULL bij native1|Succes zonder bruikbaar padobject|Hard/onvolledige nativeoutput|
|Edge6 count<1 bij native1|Succes zonder volledig pad|Hard; negatieve count niet lokaal normaliseren|
|count>4096 of totaalpuntenlimiet/overflow|Technisch budget, return3|Bestaand prefixstopbeleid behouden|
|Edge7 count>capacity; edge8 pointerendoverflow|Onbetrouwbare nativebufferbounds|Hard; geen padentries lezen|
|Edge9/13 canonicalconversion0 nativeeerste/laatste padentry|Geen geldig huidig endpointkeybewijs|Hard in kleinste route; geen bewezen pair-local enginecontract|
|Edge10/14 conversion0 eigen source/dest|Eigen endpoint/wereldkey niet betrouwbaar|Hard|
|Edge11/12/15/16 eerste/laatste keymatchfout|Geretourneerd pad past niet bij gevraagde endpoints|Hard; geen “ander pad” gebruiken|
|safe_point0 onderweg|Bundelt ownerUNKNOWN, terrain/queryfout, canary, map/threat/coördinatenfout|Hard houden; deze opdracht splitst safety niet|
|cached_path canonical_key0|Eigen actuele pairkey niet geldig|Hard/reason24→25|
|select_alternate prefixindex>=64|Eigen rollen-/bufferrelatie ongeldig|Hard/reason25|

safe_point2 blijft de huidige conservatieve afwijzing bij ongeschikt land/type/foreign/presence/positieve threat e.d.; het is geen bewijs dat geen ander veilig pad bestaat. Daarvoor wordt al bron_next geprobeerd. Ook veilige nativequery0 kan geen eiland-/transport-/gevaar-/cutoffoorzaak onderscheiden.

De oorspronkelijke enginequery is daadwerkelijk int-return/ret50h op005826a0, vtable00746220+0c. [Bestaande dump](BINAIR/settler-producer-b4-path-query.txt) toont0returns bij actieve context005826b4, unsupported dispatch00582751 en na nativezoekuitkomst005828d2–e9 of lokaalflag005828ec–f9; de positieve route bouwt extern pad/output en retourneert1 op00582a7a. Dus native0 is een bestaande normale negatieve queryuitkomst, maar zijn specifieke interne reden is uit edge4 niet afleidbaar. Dat is voldoende voor **geen credit voor dit paar**, niet voor een negatieve wereldclaim. De bestaande wrapper heeft zijn beperkte mode1/type/flags reeds vooraf gebonden; onverwachte context/codes blijven hard.

## 2. Mag lokaal UNKNOWN worden overgeslagen en positieve prefix behouden?

**Ja, onder een expliciet gescheiden contract.** Een onbekend paar vormt geen logisch tegenbewijs tegen andere volledig bewezen onafhankelijke slots. De huidige return3-route bewaart zo'n prefix al bij budgetstop. Andere bronnen proberen bestaat al bij return2. De kleine uitbreiding combineert die bestaande principes voor één nauw begrensde normale native0-uitkomst.

Minimale voorwaarden voor lokaal UNKNOWN:

- Zelfde gebonden host/interfaces/type, Plan/AiMain/civ/generation en huidige finale selectie; scope1/guard0, owner/generation gelijk aan huidige scratchsnapshot. Loggerchecks alleen bewijzen dit voor de log en mogen niet als uitvoerende policyguard worden hergebruikt. Vóór nativecall en vóór verderzoeken/credit actuele context controleren in eigen beleidscode.
- Gebonden slot/departurerecords binnen huidige aantallen/caps, dezelfde type/source/destbytes en geldige externe/canonieke endpointidentiteit. Geen stale pointer/certificaat uit vorige generatie. Bronkind/state/claimscope blijft exact huidige departurescontract; geen nieuw busyveld of transportbron toelaten.
- Precontext0; oorspronkelijke twintig args en nativecallee/ret80bytes intact; postcontext0 en beide canaries intact; **nativeEAX exact0**, cap0/count0/pointerNULL. Dit is de aangetoonde smalle schone uitvoervorm. Native0 met nonnull pointer, negatieve/andere cap/count, onverwachte nativecode of andere contractfout blijft hard in deze eerste variant. Geen ontbrekende padbuffer lezen. Overige eigen nativeoutslots blijven outputs zonder positieve padcredit; onbekende waarden daarin niet als destinationbewijs gebruiken.
- De bestaande nonnull-enginebuffer wordt op alle routes precies eenmaal via engine005866e0/cdecl vrijgegeven vóór return; geen andere allocator of nieuw pointerbezit. De smalle lokale variant heeft pointerNULL. Iedere allocator-/ABI-/contextonzekerheid mag de lokale route niet bereiken.

Een lokaal onbekend paar krijgt geen slot en geen used-markering. Een eerder volledig geselecteerd slot blijft in SELECTED staan; zijn mandatorytileconflicten en eenmalige kind1/frontclaims blijven actief. Een reeds gekozen positieve bron binnen het nog lopende slot blijft kandidaat wanneer een andere bron lokaalUNKNOWN oplevert; alleen positieve paden bepalen de bestaande laagste-IDkeuze. Een onzekere bron mag niet als “onbereikbaar” worden opgeslagen.

De bestaande cache bewaart nonzero resultaten per(type,canonieke source,dest) binnen dezelfde finalisatie. Return2 wordt dus hergebruikt als **niet-gecertificeerd-veilig**, niet als nulruimte. Return3 stopt de huidige selectie. Voor lokaalUNKNOWN is een afzonderlijke eigen returnwaarde, bijvoorbeeld4, eenvoudiger controleerbaar dan de betekenis van2 wijzigen. Dan kan cache4 hetzelfde onbekende paar in dezelfde pass onthouden en herhaalde queries voorkomen; volgende START wist de Plan/cache zoals nu. Zonder cache4 zou hetzelfde paar via kind3front/newbuild of verschillende bronrecords herhaald mogen worden en sneller het budget verbruiken; daarom moet B deze beperkte cachesemantiek expliciet kiezen.

Hard failure blijft0 en trekt de hele Gcert-prefix in. Een local4route mag daarom `native.unknown` niet aanroepen: die zet status0 en vermengt passfalen met paironzekerheid. Geef lokale uitkomst/eigen reden terug zonder de vertrouwde passcontext ongeldig te maken. Een aparte partiële/dekkingsmarkering houdt zichtbaar dat de zoekscope onvolledig is; die geeft geen COMPLETE_G0. Niet de bestaande `context_error` wissen en geen globale fout achteraf “herstellen”.

Budgets blijven gelijk: capture4096/prefix64/departures32/selected40/R; nativequeries128, cache128, search/path4096 en totaal4096padpunten. Iedere echte query telt ook als deze0 retourneert; cachehit geen nieuwe query. Geen budgetverhoging, onbeperkte retry of nieuw persistent slotbeleid.

## 3. Kleinste uitvoerbare B-route en beperkte verificatie

1. **direct_path:** splits uitsluitend edge4 na reeds uitgevoerde postcontext/canarychecks. Exact native0 plus de genoemde schone output-/context-/bindingguards retourneert lokaleUNKNOWN4 via bestaande cleanup/returnroute. native!=0/1, native1 met kapotte output/endpoints en alle overige hardbranches houden0. Geen diagnosebuffer als beleidsinput lezen; predicates komen rechtstreeks uit huidige eigen querylocals en actuele Plan.
2. **cached_path:** huidige key/typecache uitbreiden met alleen de expliciete4semantiek; cap/pointerbuffers niet bewaren. 0 blijft niet-cachebare hardfailure. 1/2/3 behouden exacte betekenis. Cache volledig passlokaal.
3. **source_path:** behandel4 als “dit paar onbekend, source_next”; behoud eerdere geselecteerde prefix en een eventuele reeds gevonden positieve bron binnen deze prioriteit. Na uitgeputte bronnen volgt dezelfde existing→front→newbuildvolgorde en dezelfde overige bestemmingen.3 blijft stoppen met gecommitte prefix,0 blijft select_bad/helefallback,1 blijft enige positieve credit en2 blijft huidige afwijzing. Geen onbekende integercodes stil als4/2 accepteren.
4. **finalize:** succesvolle partiële selectie levert uitsluitend het werkelijk geselecteerde positieve aantal als ondergrensGcert. De bestaande formule `min(R,max(Dorig,Gcert))`, consolidatie van klasseprioriteiten, nativeActualaftrek en execute/arrival30/40gates blijven exact. LocalUNKNOWN zonder positieve selectie geeft Gcert0 en normale Dorigfallback binnenR, geen pauze/geenruimteclaim. Hard0 houdt final_fallback/Gcert0; bij onbetrouwbare type/context geldt het bestaande oorspronkelijke pad.

De relevante huidige manifestfuncties, RVA: direct_path0xdc307; safe_point0xdbf1b; cached_path0xe4a3e; source_path0xe52b5; select_bad0xe578c; path_unknown0xe0475; path_budget0xe049d; path_free0xe04b1. Runtimebasis herbaseren volgens huidig manifest. De zestien historische parentedge-RVA's in path_diagnostic_layout zijn geen nieuwe patchlijst; B/C moet de eigen emitterbranches kiezen en bestaande provenance behouden.

Voor B→C volstaat een kleine uitbreiding van bestaande integratie/nativegevallen, geen raamwerk:

- Schone native0 bronA, vervolgens volledig positieve bronB: B kan hetzelfde slot krijgen; A levert0credit en wordt niet gebruiktgemarkeerd. Zelfde paircachehit4 veroorzaakt geen tweede nativequery; andere source/dest wel.
- Eén positief gecommit conflictvrij slot, daarna lokaalUNKNOWN en later positief slot: prefix blijft, latere volledige credit groeit; mandatoryconflicten en eenmalige unit/frontclaims blijven gelden. Herbruikbare nieuwbouworigin blijft herbruikbaar. Geen claim dat dit exacte patroon al opT71 is gemeten.
- Native0 met postcontext!=0, kapotte canary, cap/count/pointermismatch, generation/bindingfout blijft hard en trekt eerdere prefix in. native1 met null/negatieve count/capacity/overflow/endpointfout evenzeer; safetyUNKNOWN niet verruimen. Onbekende returncode blijft hard.
- Budget3 na positieve prefix behoudt alleen bestaande geselecteerde slots; exact128queries/cachecap en4096punten blijven eindig. Geen fout in een later paar mag nativepathfree overslaan of verdubbelen; ret12/ret4/callee80/cdeclfree en registers/x87/canaries behouden.
- Dezelfde Dorig/Gcert/R-input moet dezelfde quota/priorityentries houden; Gcert>Dorig blijft noodzakelijke poort voor echte extra aanvraag. Meer onderzochte paren alléén is geen gameplayacceptatie. Vervolgens begrensde gelijkeT0-hostvergelijking van uitsluitend deze ingreep, met bestaande reader waar toereikend; geen automatische nieuwe observer of volledige causaliteitsproef.

**Noodzakelijke Bkeuze:** exacte lokale4contract inclusief schone native0outputs, expliciete passguards en passlokale cache4; alle andere UNKNOWN blijft hard. Deze keuze is nu onderbouwd uitvoerbaar. Niet eerst extra endpoint-/safety-/transport-/queuearchitectuur reconstrueren. Of extra bronnen werkelijk positieve slots leveren en Dorig5 overstijgen is een toekomstige meetuitkomst, geen beloofde30stedenwinst.

| Beslisketen | Huidig bewijs | A-status / lacune |
|---|---|---|
|Native0→reason25|Zes opgeslagen gebonden edge4/native0gevallen|Beantwoord; interne native0oorzaak en alternatief pad onbekend|
|0/1/2/3→cache/selection/finalize|Gepinde huidige emitters + bestaande originele querydump|Beantwoord; lokale4 is voorstelroute, nog niet toegepast|
|Lokaleunknown→verderzoeken/prefix|Bestaand source_next/return3/uniqueclaimscontract|Technisch onderbouwd; nieuwe native-/hostacceptatie vereist|
|Meer kansen→Doel1/1a|Bestaande T100121tegenover86, zes gemiste vervolgkansen mogelijk|Geen causaliteits-/30-/volledige rem-/transportclaim|

Alle drie vragen beantwoord en werk gestopt na overdracht. Geen eigen helper/run actief; pc blijft aan. Budgetstart17:51:18 verse vijfuur21/week39/stateok; root meldde17:52 vijf19/week39.
