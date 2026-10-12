# C3 eerste geval: PowerShell blokkeerde vóór native uitvoering

11 oktober 2026, 16:54 Europe/Amsterdam. **CASE_FAIL_BEFORE_HELPER_BODY_NOT_NATIVE_TESTED**. Uitsluitend `parse-opening_research` eenmaal via de gereviewde run-native.py CLI geprobeerd. Geen andere case, herhaling of code-/instellingswijziging. Uitvoerder gestopt voor rootreview.

Eigen x86 PowerShell-subprocess PID26432 keerde terug met exitcode1 na0.422s, binnen20s/4MiB. Geen timeout of forcebeëindiging. De fout ontstond vóór het script kon laden: `native.ps1 cannot be loaded because running scripts is disabled on this system`, SecurityError/UnauthorizedAccess. Dit is de aangetroffen runtimeblokkade; het exacte effectieve executionpolicy-niveau is niet aanvullend uitgelezen.

Bewijs in native-helper/results/: parse-opening_research.runner.json, .stderr (411bytes), .stdout (0bytes). Geen native .json of .trace aangemaakt. Dus geen LoadLibrary, ctor/load/switch, callbacknamen, presence/count, diagnostics of ABI uitgevoerd/gemeten. De bestaande tekst-/bronacceptatie blijft beperkt; een exit van het eigen subprocess bewijst geen parserpass.

Budget vóór eigen subprocess: 16:53:57.820, bron0.8s, week85/vijf7, stateok. Na exit: 16:53:58.319, bron1.3s, week85/vijf7, stateok. Runnerpassfalse/native_case_passfalse eerlijk vastgelegd. Geen budgetstopreden gebruikt als verklaring voor deze fout.

Bron/staging ongewijzigd; geen ExecutionPolicy, register, source, DLL, engine of game gewijzigd. Bestaande D:\CTP-instatie ongemoeid, pc aan. Er valt geen installatie te herstellen.

Volgende concrete vraag terug naar root/ontwerp: hoe mag de bestaande eigen x86 PowerShell-helper worden uitgevoerd onder de werkelijke scriptpolicy? Eerst die CLI-/policyroute concreet reviewen; geen stil bypassflag toevoegen of dezelfde case opnieuw proberen. Bij een nieuwe vrijgave ook outputisolatie/no-retryguards behouden. De resterende17cases en eerste echte partialparseracceptatie blijven open.
