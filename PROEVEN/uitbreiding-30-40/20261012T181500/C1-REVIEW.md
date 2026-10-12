# C1 basis- en ABI-reviewcheckpoint

12 oktober2026,18:23:27 Europe/Amsterdam. **Basisbindings gereed; implementatie gestopt vóór nieuw emitterwerk.** Eerst stale budgetmetadata na één retry; root bevestigt daarna verse harde stopvijfuur5%/week54%,bron18:23:22/leeftijd5.1s. Alleen ownfiles geschreven. De basis DLLbackup is de geteste releasev1, geen nieuwe candidate. Prepare.py is uitsluitend offline/read-only voor bestaand werk en schrijft binnen deze map.

Controlebewijs: preparation-manifest.json bevat19 actuelevariantsha's, A/Bsha's, exacte9preimages+offsets,5B2hooks, B2payloadsha/size en sectionlayout. Alleasserties geslaagd bij uitvoeringprepare.py. DLL SHA eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890; engine SHA b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79,base400000/timestamp37d6f702. AIbase20000000/timestamp37b894e7. Nieuwe sections mogen pas na actueleSizeOfImage d6000; B2 blijft opd4000.

## Werkelijk aanwezige ABI en resultbinding

Execute_Task200443c0: thiscallECXgoal,argsAiMain/Plan,ret8. Entrywrapper moet oorspronkelijke functie exacteenmaal roepen bij toegelaten/nietbeheerde policy,denial0.

FollowPath20044bf0: thiscallECXgoal, AiMain[ebp+8],Army[ebp+c],OtherArmy[ebp+10],subtask[ebp+14],fifthoutarg[ebp+18]. De arrivalbranch20044d03–11 pusht subtask,OtherArmy,Army,AiMain enECXgoal, vtable+90. Adapterret10h past dus. Het oorspronkelijke20044d17movEAX1 moet vervallen; FollowPath20044d22ret14h blijft. Originele markering ligt200487f3–f7,ActionSettle200487fd,arrivalret10h20048817. Native falsepath blijftEAX0 op20044d53.

GotoTaskSolution20044a70: ECXgoal→ESI;AiMain[ebp+8]→EDI; subtask[ebp+20]. Switchtable20044ba4 slot0/3→20044ab8;slot1→20044b48;slot2→20044b39. Call20044b21vtable+8c ontvangt AiMain,Army,OtherArmy,subtask enoutarg,ret14h; normalisatieplaats20044b27 heeft nog oorspronkelijke callerEBP enESI/EDI. Ownnormalisatie moet dus zonder nieuw frame of met expliciete inheritedframebinding caller[ebp+20] lezen. Sentinel−1 alleen type5/exactGoalSettle/subtask0→0; anders exacte9bytesneg/sbb/neg/add2→2/3. Nativefalse0 blijft2. Normalisatie20044b5e blijft origineel. GotoTaskSolutionret1ch blijft20044b36.

Schedulertabel20073958 is nog niet apart in dit checkpoint vastgelegd; de aanwezige body20073727→2007375c→200754b0bindt het bestaande detachpad. Voor sourcecandidate de tabel en Execute_Taskresultdoorgifte nog gericht verifiëren; geen nieuwe harness voor deze gewone bodybinding. Geen eigen detach inarrivaladapter.

## Resterende exact afgebakende implementatie

Hergebruik bestaande N30/B4/H3-emitterbronnen read-only; gewijzigde emitters in eigenmap. H3classifier/host/poscmp intern, geen3scorehooks. B2payload/fivehooks/36record exact. OwnRW SELECTEDcap40, ORDERstart minstensSELECTED+160 met afgescheidenPATHCACHE/PLAN_SIZE. Gcert is positieve volledig bewezen prefix met klassificatie/source/querybudgets plus4096totaalpadpunten; cutoff/incompletecontext onderscheid houden, geenfakeG0.

Finalize: actuelegov3/C/completionpolicy; Dorig over alle geselecteerde settlersklassen berekenen met nativeceilregels; D=min(R,max(Dorig,Gcert)),R0vóórcapturefallback. Zonder minimale type/klasse/context nativepass; cap blijft actuele uitvoerpoort. Completion1+anderegov nativequota/nativearrival. NativeDesiredentry/prioriteit viaChoose,Actualéénmaal. Capentry/arrival moetverseenginePlayer+12c0container+8 lezen met eigenaars-/hostvalidatie;arrivaldenialvóórmarkering,ownsentinel−1en44b27adapter.

Ownbuilder mag uitsluitend9aangegevenwindows, toegestanePEheadervelden, nieuweRX/RWsectionheaders en appendedbytes wijzigen. HIGHLOW opRVA8a598 behouden; pointernaarownExecute wrapper aanpassen. Audit ieder verschil volledig tegenpolicy en preserve B2bytes/hookbytes/originele overige bytes. Geen installatievoorreview; huidigereleaseblijft geïnstalleerd. Latere native/budgetcases en gameplay wachten oprootC2vrijgave.
