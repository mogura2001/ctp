# H1-I 11 oktober: gestopt vóór installatie en spelstart

11 oktober 2026, 16:32 Europe/Amsterdam. Uitvoering gestopt; geen agentwerk of spelproef meer actief. Nieuwe specifieke gebruikersmachtiging ontvangen voor deze ene H1-I-arm. De hoofdagent droeg uitsluitend deze arm over.

Start-H1-T0.ps1 eenmaal aangeroepen om 16:30:52.174. Dit is één scriptaanroep, **nul daadwerkelijke spelstarts**: de preflight stopte om 16:30:52.745 met `Preflight all-civctp gate not count0.` Installatie niet geprobeerd, geen werk-DLL-backup gemaakt, geen CreateProcess, geen nieuwe PID, Capture, save-load, A, n, B of Close uitgevoerd. Geen herstelactie nodig.

Read-only procescontrole om 16:31:09.534 bewijst één reeds bestaande instantie: PID 26784, executable `D:\CTP\ctp_program\ctp\civctp.exe`, ontstaan 15:55:24.441, parent PID 13864. Dit is een andere installatie dan CTP-proef. Deze instantie is niet bediend, gesloten of gewijzigd. Geen venster- of gameplaytoestand geclaimd op basis van uitsluitend deze procesquery.

De originele proef-DLL bleef SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`. Alle vijftien oorspronkelijke pins zijn na de stop opnieuw gehasht en gelijk; beide bedoelde A/B-bronoutputs ontbreken. Geen instellingen, saves of gebruikerswijzigingen teruggedraaid. Pc blijft aan.

Budgetpreflight: bron 16:30:50.527, gelezen 16:30:52.520, leeftijd 2.0s, week 90%, vijfuur 38%, state ok. De stop werd dus veroorzaakt door de bestaande spelinstantie, niet door de budgetgrens of automatische goedkeuringscontrole.

Bewijs: execution.json, startup-resultaat.json, budget-preflight.json, blocked-existing-processes.json en blocked-eindhashes.json. H1-I-activatie/A/B/nieuwe GoalSettle/gameplay blijven **niet gemeten**; NOT_OBSERVED zou een te sterke conclusie zijn omdat er geen geladen T0 en geen observerread waren.

Volgende poort: root/gebruiker informeren over de andere lopende installatie. Geen automatische herhaling of afsluiting; een eventuele nieuwe concrete uitvoering moet opnieuw worden vrijgegeven en krijgt eigen unieke arm/outputnamen. De gereviewde scripts en eerdere voorbereiding blijven ongewijzigd.
