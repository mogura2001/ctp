# C2 CLI-correctie: bronvoorbereiding voor rootreview

2026-10-12T11:54:38.588449+02:00 Europe/Amsterdam. **SOURCE_PREPARED_NOT_EXECUTED**. Routinecorrectie afgerond; uitvoerder stopt voor rootreview en afzonderlijke eerste-casevrijgave.

De vorige eerste case stopte v??r de scriptbody door PowerShell executionpolicy. Deze eigen kopie hergebruikt precies de private childargumenten van de bestaande opening-b2/run-native.py en production-h3/run-native.py: `-NoProfile -NonInteractive -ExecutionPolicy Bypass -File`. Geen systeem-/registrypolicy, parserbron, spelstrategie of gamebestand gewijzigd.

Alle 24 manifestgebonden oude bronnen/stagingbestanden zijn eerst bytegelijk gekopieerd naar deze eigen map en naar source-copies/. Alleen run-native.py en cases.json verschillen. De runner heeft ??n argumentlijstwijziging; inverse vervanging levert exact de oude bytes op. De caseplanwijziging is uitsluitend 36 absolute helperrootvervangingen: 18 case-stagingpaden en 18 eigen shim/staging-inputpinnen. Inverse vervanging levert het gehele oorspronkelijke cases.json bytegelijk op; alle 18 gevallen, 33 inputhashes, 98 namen/indices, callbacks, ctor/ABI/preimages en overige grenzen blijven behouden.

22 overige bronbestanden zijn bytegelijk, inclusief Native.cs, native.ps1, beide ABIshims/recipes en alle 14 stagingbestanden. source-syntax.json is expliciet historische bytegelijke syntaxevidence; geen nieuwe C# compile of x86-uitvoering geclaimd. Python ast.parse slaagt zonder runnerimport/main/nativeuitvoering. De oude 24 bronpinnen en 33 externe inputpinnen zijn na de kopie opnieuw gemeten en ongewijzigd. Geen oude results of vrijgaverecords gekopieerd of gewijzigd. Nieuwe C3-ROOT-VRIJGAVE.json heeft native_execution_approved=false en geen actuele vrijgave.

Behoud: ??n exacte gepinde case per subprocess; eigen Popen/handle, verborgen venster, 20s/4MiB-grenzen, volledige stdout/stderr, geen resultaatoverschrijving/herhaling, budgetcheck met ??n unknown-hercheck. Geen LoadLibrary, helpercase, native call, CTP-installatie, spelactie, GUI, debugger of procesattach uitgevoerd; results/ bestaat niet.

Beschermde inputpinnen omvatten uitsluitend de oorspronkelijke CTP-og robotcom.dll SHA3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44, het B-voorstel, bestaande B2c/C1-kandidaat/manifests/category/routering/header en eigen shim/stagingbestanden. **Geen CTP-proef robotcom.dll-pin in dit parsercaseplan**; H1 kan die dus afzonderlijk tijdelijk wijzigen zonder deze checks tegen te spreken. Er is geen native case uitgevoerd tijdens H1. Root moet eventuele latere helperuitvoering met H1 co?rdineren.

Reviewbare bestanden: source-manifest.json, minimal-source.diff, routine-checks.json, input-pins-before-after.json en source-copies/. ManifestSHA8f003cd0b7eb4a36a6a0038765e7641b9d6fd0ee0782f133f376c609f16aec56; planSHA67e3aeb8a059cfeb3e08b1152beb9cb35c97015bb803f1ab5006cd4a266a5deb; runnerSHA6c1fcdbb736b052c00495e5e84b3221f93963c70916945bb7990ea445f9bb75a; Native.cs blijft9c75d0464f3a9e46519128aae917fb7b6f31dfd03eb5571261d9a7ef3877cc8c.

Acceptatiestatus: CLI-/bronvoorbereiding gereed voor review; geen echte parser-, ABI-, FLI-, host- of gameplayacceptatie. Volgende concrete stap: rootreview van alleen deze routine-delta en nieuwe plan-/bronpinnen, dan afzonderlijke vrijgave uitsluitend parse-opening_research; resultaatreview v??r alle overige cases. De oude mislukte case blijft bewaard.

Budget v??r pakket12okt11:52:01: week84/vijf99, bron15.3s, stateok. Einde wordt door eigen voortgangsbestand en rootmelding bevestigd. Pc aan; alle afsluittoestemmingen ingetrokken.

Rootsteering12okt11:55: werk stopt op dit broncheckpoint; geen nativevrijgave of 18-casesvervolg aangenomen. Technische helperpass telt niet voor de nieuwe drie-sessiesmeetlat. Root bepaalt eerst bewijsroute voor echt gameplaydoel3 Religion?Theocracy/government. Eindbudget11:54:37 week83/vijf94, bron22.8s, stateok; geen budgetstop. Pc aan.
