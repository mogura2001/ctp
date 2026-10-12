# Voortgang uitvoerder B2c-header

11 oktober 2026, 16:54 Europe/Amsterdam. **C1/C2 rootgeaccepteerd; C3 eerste geval vóór native uitvoering geblokkeerd, uitvoerder gestopt.**

Nieuw checkpoint: native-helper/Native.cs plus native.ps1/run-native.py/cases.json geschreven met normale LoadLibraryW, exacte drie callbacks plus diagnostiek, onbekende-slotstop, ctor/load/switchRVA en ABI-/98naam-/lijst-/switchasserties. Twee root-sourcecorrecties verwerkt: raw effective pointer lezen zonder fictief presencebit en fysieke FTW→logische ST viaTOP. Achttiengevallen-CLI heeft20s/4MiB privateownsubprocesslimiet en33inputpins; bronmanifest24bestanden. Alleen syntaxis/C#64-bit purecompile/Pythonast gecontroleerd; geen Run/LoadLibrary/nativecase. C2-VOORBEREIDING.md bindt reviewhashes en bewijsgrenzen. Geen concrete extra binding of brede analyse nodig.

Pakket PROEVEN/opening-b2/onderzoek-b2c-header/20261011T163848 bevat negentien kandidaten. Acht research-AIPs kregen exact 21-byte include+CRLF-prefix; oorspronkelijke 2866 bytes en alle 98 route-eigen namen behouden. Elf andere kandidaten bytegelijk, headerkopie onder staging/AIPs exact. Diff volledig gelezen; 168 bestaande bron-/pakketpins voor/na gelijk.

Bewijs: pakket RESULTATEN.md, manifest.json, candidate.diff, static-checks.json en protected-before/after.json. Geen installatie, native, helper, spel/procesbediening of C2 uitgevoerd. Bestaande D:\CTP-instatie bleef ongemoeid; pc blijft aan.

Acceptatie: C1/C2 rootgeaccepteerd. Exact eerste vrijgegeven C3case parse-opening_research eenmaal geprobeerd. Eigen x86 PID26432 exit1 na0.422s doordat scripts disabled native.ps1 vóór body blokkeerde (SecurityError/UnauthorizedAccess). Geen .json/.trace/nativecall; runner/stdout/stderr bewijzen FAIL vóór daadwerkelijke parser. Geen retry/policy/codewijziging. Zie C3-EERSTE-RESULTAAT.md. Native/FLI/host/gameplay blijven open; eerst concrete eigenhelper CLI-policyroute terug naar root/ontwerp. Laatste budget vóór/na16:53:58 week85/vijf7ok. Pc aan; werk gestopt.
