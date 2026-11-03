# Review SCI-only FoodReader-diagnostiek

19 oktober 2026. Root heeft A en B volledig gelezen en het voorstel vóór C aan de gebruiker uitgelegd. Alleen een diagnose is beoogd; geen gewijzigde voedselregels, UNKNOWN-afhandeling, locatieacceptatie of settlervraag. Doel1/1a/5 blijven open. Doel3-release blijft de herstelversie.

## Bronreview in uitvoering

Root las `food_components.py`, `food_diagnostic.py`, `food_diagnostic_layout.py`, de gewijzigde buildersecties en `reader/food_failure_decoder.py` in `PROEVEN/science-foodreader-diagnostiek/20261019T194200`. Nog geen definitieve bouw- of hostvrijgave: uitvoerder moet bronoverdracht/pins en beperkte controlebron afronden.

De oorspronkelijke reader is als default factory gekopieerd; de historische gedeelde H3-bron blijft gebruikt voor het hele H3-payload. Alleen twee oproepen uit de ongewijzigde science-modelbron worden naar de aparte clone geleid. De development-reader blijft origineel. De nieuwe state-RVA volgt uit compositie; de reader gebruikt die gebonden manifestwaarde.

De 236-byte recordlayout vult uitsluitend Plan276..511. Private staging -336..-101 en spills -340/-344 overlappen oude locals niet binnen frame352. Framegroei272 is een veelvoud van16. Fragmenten gebruiken PUSHFD/PUSHAD en POPAD/POPFD; de opgeslagen registeroffsets passen bij die volgorde. Logging leest registers/eigen locals; oorspronkelijke memoryvergelijkingen die een operand moeten bewaren worden eenmaal geladen met registerherstel. Geen extra enginecallback of x87-instructie toegevoegd. Branchpredicaten, ADD/ADC-overloopvlaggen en native EAX worden door de bronroute behouden; uitgezonden bytes/ABI moeten nog worden gecontroleerd.

37 unieke failurelandingen bewaren vlaggen vóór de oorspronkelijke out40-wipe/EAX0/ret20. Publicatie vereist PIC-gebonden eigen Plan, scope/guard, owner/generation-snapshot, prefix/counter/callsite/argumentbinding. Valid wordt als laatste gezet. De eerste centrumfailure heeft voor dezelfde owner/generation voorrang boven eerdere tilefailures. De decoder houdt rawbytes en ONBEREIKT apart, controleert vereiste operandbits en koppelt centrum aan ORDER/CAPTURE. Geen geselecteerde credit uit deze diagnose.

## Hostvoorbereiding, nog niet vrijgegeven

Root beheert afzonderlijk `PROEVEN/science-foodreader-host/20261019/host1`.29verse beschermde backups en drie bestaande autosavearchieven zijn exact gecontroleerd. Gate FALSE; geen installatie/start/invoer. De bewezen eindige intro-monitor is overgenomen met nieuwe gate-/candidatebinding; scripts zijn door de PowerShell-parser gecontroleerd. Alleen normale sluiting van exact eigen proces; herstel weigert onverwachte gebruikerswijzigingen en vereist count0. Nieuwe autosave wordt vóór herstel dubbel bewaard. Pc blijft aan.

## Definitieve bronoverdracht 19:57

BRONOVERDRACHT.md, check_sources.py en de laatste beperkte wijzigingen zijn beoordeeld. De finale wijzigingen voegen alleen nulbyte-restored-exitlabels toe voor een observer op de volledige vijfbyte-JMP; required_bits vereist de werkelijk gelezen Cell al bij branch8; decoder controleert ook de oorspronkelijke Jcc-vlagvoorwaarde. Fixtureprestates zijn expliciet synthetisch en logisch consistent. Geen willekeurige vijfbytepatch over food_bad; de fixtureobserver gebruikt uitsluitend een eigen image. De nog niet aangesloten finite nativecaller is als open uitvoeringswerk beschreven.

Root controleerde alle149 SOURCE-pins exact; pinmanifestSHA256 `2bc87cc76916226f9096ffa014dded128ce259ff513a29fb9a7ba1a96b42bec9`. Finale food_diagnosticSHA `6fc67fdfaf4d84c0188303d51d59d76afe324452b96c6f636975c43bc63bab0b`, layoutSHA `00a67ec1c1a21cb9443ae566401179d1e966fc2d5f8249e58735ed44e82ecf2b`.24ASTbronnen/37gedeclareerdeIDs zijn bronbewijs; uitgezonden behoud/ABI nog open. Gate verleend uitsluitend voor kandidaatbouw, beperkte fixture-emissie en bytecontrole. Native/host blijven FALSE. Budget vers vijf51/week80; pc aan.

## C2 en native geaccepteerd 20:12

Root las volledige bytechecker/resultaten, C2-overdracht, NativeFoodCaller.cs en compile-/runnerscripts. Finale beperkte C#delta betreft uitsluitend stdout-call-/cleanupmarkeringen; die regels zijn herlezen. Fixturecanaries staan nu direct naast lokale out40.107BUILDpins(SHA21a5fe75...) en206nativebronpins(SHA3b9e3567...) zijn onafhankelijk exact geverifieerd. Kandidaat068ff459.../manifestbeebdb07.../state0xe3000/497668; defaultreader1196bytes en gedeeldeH3+padding exact,20oude rijdelta's=18stateadressen+2SCIcalls,37edges/restoreJMPs,556readinventaris en13decodergevallen beoordeeld.

Eerste compileerpoging draaide geen bron wegens Windows-scriptbeleid; bewijs behouden. Tweede start gebruikte uitsluitend processcope-scriptinstelling, compile exit0. AssemblySHAfcbab5745a11fb134243bca028ed6d4cfae010752c53f2c952c62bdf8641f4cf. Eigen nativehelperPID21776 exit0,69calls en cleanup=True. Alle37synthetischelogpaden, kleine echte clone/originele stubreads, ABI/register-/flags-/x87-/canary-/out40-/callback-/binding-/latchchecks geslaagd. Geen natuurlijke bereikbaarheid van37wereldtoestanden of gameplay bewezen. Nativegate verbruikt/FALSE; runtimebewijs gepind in native/NATIVE-RUNTIME-PINS.json.

Afzonderlijke root-hostvrijgave voor exact dezelfdeT0/max1n/T0-T1, nieuw kandidaat-/reader-/bronbinding,29versebackups/driearchieven exact. Eindige intro-monitor, normale sluiting/herstel volgens B. Geen ruimere benchmark, UNKNOWNskip of spelbeleidwijziging vrijgegeven. Budget vers vijf28/week77; pc aan.

## Spelbewijs en vervolgoverdracht 20:26

De ene hostproef heeft de exacte fout aangetoond: branch10, SCI_CENTER, count2, cityhandle0, native_called0. Eerder positief sciencevoorbeeld/marges behouden; pass nog23/Gcert0/desired5. Zie PROEVEN/science-foodreader-host/20261019/host1/HOST-PROOF.json en RESULTAAT.md voor timingcorrectie, herstel en grenzen. Geen nieuw oorspronkelijk gameplaydoel afgerond.

Root heeft ANALYSE/SCIENCE-BEZET-CENTRUM.md en ONTWERP/SCIENCE-BEZET-CENTRUM.md volledig gelezen en geaccepteerd voor de eerstvolgende bronvoorbereiding. De private typedreturn2 is vers per invocatie; de historische failurelatch wordt geen beleidscode. Alleen actueel geldig SCI_CENTER/branch10/cityhandle0/signedcount>0 wordt tijdelijk NO_NOW/OCCUPIED_CENTER_SCOPE/coverage1. Geen foodcredit, geen algemeen UNKNOWNskip. Shared/development/workerpad blijven0/1 en de union behoudt zijn positieve selectievoorwaarden.

Uitvoeringsvoorwaarde bij C1: voedselconsumptie vereist expliciet return1 na de afzonderlijke2-handler; onverwachte returnwaarden zijn UNKNOWN, ook bij de tilecaller. Reserveer een aantoonbaar vrije private returnspill en valideer actuele identiteit/ordinal/positie vóór2. Nieuw reasonnummer en readerfasestatus moeten onderscheid maken tussen scope-uitsluiting en voltooide voedselanalyse. Handler gaat door science_done met bestaande x87restore. Nieuwe kleine nativefixtures moeten de echte modelframe-/x87-layout respecteren; oude out40canary op-144 overlapt de echte SCI-x87save en mag daarin niet worden overgenomen. Deze review start geen nieuwe C-code, bouw, native of game. Afzonderlijke review/vrijgave volgt op de bronoverdracht.
