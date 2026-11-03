# C1: actueel bezet sciencecentrum

20 oktober2026. Uitsluitend bronvoorbereiding op geaccepteerde A/B. Alle build-/fixture-/native-/hostgates FALSE. **Geen kandidaat uitgezonden, geen nativecompile/-run, geen RPM/GUI/installatie/game.** CTP-og, CTP-proef, parentpakketten, release en saves zijn niet gewijzigd.

Parent `PROEVEN/science-foodreader-diagnostiek/20261019T194200`: kandidaat068ff459a19125fdd08db060450110210ad992698d27b920894f4502ac4aae4f, manifestbeebdb07abeb5bf111869e53f1c15dbb6466ece17808022276241d6ee4e28e44. `INPUT-PROVENANCE.json` bindt de gekopieerde bron-/baseinputs; parent wordt niet overschreven. Geen bestaande aangepaste spelbestanden gekopieerd als nieuwe release.

## Exacte broningreep

| Bestand | Wijziging |
|---|---|
|food_diagnostic.py|Elke invocatie initialiseert private returnspill0; na oorspronkelijke failure-out40wipe volgen verse eigenbindingchecks; alleen huidige branch10/cityhandle0/signedcount>0/SCI_CENTER geeft2. Succes1 blijft oorspronkelijke route. Andere failures0. Historische publicatie krijgt tevens PIC-Plan/spillvergelijking vóór eerste dereference; latchbeleid blijft gelijk en is geen spelbeleid.|
|food_diagnostic_layout.py|Vrije stackspill-348..-345, private contractversie2/returns0,1,2. Recordschema1/236bytes blijft ongewijzigd.|
|science_model.py|Centrumcall behandelt2 apart vóórstrict1-foodconsumer; tilecaller accepteert uitsluitend1. HandlerNO_NOW1/reason17/coverage1/certifiable0/indices-1 → oorspronkelijke science_done/frstor. Nulbytelabels begrenzen de twee consumers en de bestaande tileUNKNOWN-exit voor gerichte own-imagefixtures.|
|science_layout.py|Uniek ScienceResult-reason17 OCCUPIED_CENTER_SCOPE, private contractdeclaratie. Geen layout-/buffer-/budgetwijziging.|
|science_result.py|Reason17 geeft expliciete scope-uitkomst en nooit food-/margeberekening; geïnitialiseerde food/keyvelden worden alsNone uitgegeven, niet als gemeten nul. Andere scienceberekeningen blijven gelijk.|
|reader/partial_diagnostic.py|Bounded max64 eigen128-byteheaders om eerdere scope-uitkomsten te vinden na verdere classificatie. SCI0 wordt apart als volledig2048-byteobject behouden. Scopefood/key/margesNone; raw geïnitialiseerde bytes apart gelabeld. Oude original_indices_reproduced blijft alleen informatief, geen afwijzingspoort.|
|reader/food_failure_decoder.py|Eerste historische centerfailure mag nu een eerder geclassificeerd prefix hebben. Binding owner/gen/ordinal/ORDER/CAPTURE blijft vereist. Latch is nooit bewijs van huidige typedreturn; scopeheader op hetzelfde prefix apart vermeld.|
|build_candidate.py|Parenthashcontrole en nieuw private-contract/reason/coverage-manifestveld. Toekomstige compose leidt eigenstate-RVA af; geen oudeRVA hergebruiken.|

`union.py`, native/policy/FLI-aansturing, developmentreader, score/H3-bronnen en huidige/future top3-/margefuncties zijn ongewijzigd. Geen andere UNKNOWN-skip, unitrecordread, callback of budgetverhoging. De gedeelde FoodReader blijft0/1; er is geen caller naar de clone toegevoegd.

## Layout, ABI en returnpad

FoodReader-proloog: savedEBX/ESI/EDI op-12..-1;352private bytes totEBP-364. Staging[-336,-101], ACTIVE[-340,-337], PLAN_SPILL[-344,-341], nieuwe RETURN_SPILL[-348,-345]. [-364,-349] blijft vrij. Oude locals[-44,-16] blijven intact. De oude fixturecanary-348 zou nu fout zijn en wordt niet overgenomen.

SCI-model heeft548private bytes plus12savedbytes tot-560. x87[-144,-37], out40[-184,-145], host[-208,-185]; bronfixture gebruikt exact dit frame, FNSAVE/FLDCW/FRSTOR en geen canary op-144. Alle rest van de originele modelstack blijft gelijk.

Vlak na out40wipe en vóór `mov EAX,[returnspill]` controleert `occupied_return`: eigen ACTIVE/staging/schema/huidige branch10/centerkind/isCenter1/city0/count>0/native_called0/reachedbits; PIC-afgeleid Planadres gelijk aan eigen spill; scope1/guard1; owner/generation gelijk aan huidig Plan én snapshot en niet0; classified1..64/SCI_calls/classified≤prefix≤64/stagingprefix=classified−1; huidig primaryordinal1..1344 gelijk aan staging; exact SCI_CENTER-returnadres; alle World/HostBinding/outpointerargs tegenover Plan/staging/callerframe; bounded ORDER/CAPTURE en actuele externe xyz tegenover invocatiestaging. Vierde16bitwoord is padding en geenkey. Geen enkele historische-recordload.

Checks gebruiken PUSHFD/PUSHAD → POPAD/POPFD, alleen eigen locals/Plan en reeds gelezen count/city. Daardoor blijft de toestand na de oorspronkelijke wipe gelijk behalve bedoelde EAX2. Succes gebruikt EAX1, alle andere failures EAX0; stdcall20/ret20 blijft staan. De oorspronkelijke epiloog bepaalt zijn eigen EFLAGS zoals voorheen. x87 wordt niet door de clone aangeraakt; de modelhandler gebruikt originele science_done/frstor.

## Callerinventaris

1. `science_model` centrum-H3FoodReader is via buildernamespace aan SCIclone gebonden:2→lokale uitsluiting;1→foodconsumer; alle andere→science_bad/UNKNOWN.
2. `science_model` tile-H3FoodReader is dezelfde clone:uitsluitend1→foodconsumer;0/2/onverwacht→science_current_unknown. De clone zelf mag op tilecontext geen2 produceren.
3. Gedeelde H3-productieclassifier/scoreadapter en developmentroutine blijven aan oorspronkelijke gedeelde reader gebonden;0/1. `food_components.py` default factory is bytegelijke parentbron; uitgezonden bytegelijkheid volgt pas C2.
4. Geen andere clonealias/oproep toegevoegd. De twee echte SCIreturnlabels blijven de twee ingangen voor verse callsitebinding.

## Gerichte vervolgcontrolebron

`fixture_sources.py` hergebruikt X86/shim5/food/convert/finiteown-image. Slechts vier eigen wrappers: normale reader met echtSCIframe/x87; converter die één expliciet eigen Plan/frameadres na geldige entry verandert; kleine probe naar de echte gewijzigde modelcontinuations; observer die uitsluitend foodconsumer-bereik in eigencontext markeert. Geen37-edge-emissie of oude69suite.

`native/NativeFoodCaller.cs` is een beperkte source-only afgeleide van de bewezen finite caller. Gepland:35readerinvocaties +8geïnjecteerde daadwerkelijke modelcontinuations (=43; exactaantal bijC2 verifiëren). Twee actuele bezette centra met behouden firstlatch, daarna echte anderefailure; tile/count<0/count0/city/andereguard/shared0-1; wrongcallsite;12Plan- en12stagingmutaties na geldigeentry. Center/tilecontinuations krijgen0/1/2/3; alleen1 bereikt foodconsumer; exacte2-handler en oorspronkelijke frstor worden geraakt. Deze probes zijn expliciet GEEN volledigeSCI-executie of natuurlijke wereldtoestanden. Enginecallbacks tellen mee; nul bij vroege occupiedfailures. Eigenimage beschermt alleen RX-code; Plan blijftRW. Tijdelijke routes zijn uitsluitend eigenimagepatches over bekende complete6-byte CMP/load of volledige5-byte JMP, met teruggezette originele continuationwindows. Originele candidateopdisk blijft intact.

Canaries bewaken eigenPlan en externe out40; shim5 meet ret20/ESP, nonvolatile en exacte x87. EFLAGS/volatile-GPRbehoud van nieuwe validator is nu alleen bronmatig PUSHFD/PUSHAD-gecontroleerd; C2-bytecontrole en eventueel kleine gerichte observer moeten dit vóór nativeacceptatie afmaken. Dit is een expliciet open controlepunt, geen nativePASSclaim. Niet alle37oude guards worden opnieuw getest.

## Uitgevoerde controles en overdracht

`check_sources.py` doet uitsluitend AST/compile-to-codeobject zonder uitvoering, layout-only-import, oorspronkelijke bronidentiteit, tweecall-/strictreturn-/handlercontrole, reasoncollisioncheck, parent/proposal/release/dependencyhashes en diffs. Geen emitterimport/compose. `SOURCE-CHECKS.json`, `SOURCE-PINS.json`, `diffs/` zijn het bewijs. De twee eerdere voorbereidingsscripts kopieerden alleen source/baseinputs; finale bewerkte bron en pins zijn autoritatief.

Rootreview moet uitgezonden bytes/whole-diff/state-RVA/rel32/default-H3-/developmentbehoud, readernegatievecases, limitednative/ABI en echteT0/n/T1 nog apart vrijgeven. Nieuwe compilednative-/hostgate bestaat niet; root beheert aparte hostmap/29backups/vieroudeautosaves. Geen onuitvoerbare wijziging aangetoond, geen strategie vervangen. Oorspronkelijke Doel1/1a/5 blijvenOPEN; Doel3-release behouden. Na C1-overdracht stopt deze rol tot afzonderlijke opdracht. Pc blijft aan.
