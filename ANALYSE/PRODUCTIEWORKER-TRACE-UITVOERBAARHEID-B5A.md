# B5a — uitvoerbaarheid van vier externe tracepins

Gerichte fase A, 11 oktober2026,16:22 Europe/Amsterdam. Ownership uitsluitend dit bestand en VOORTGANG-ANALIST-B5A-TRACE.md. Opdracht: drie eindige vragen onder ONTWERP/PRODUCTIEWORKER-TRACE-B5A.md. **A-overdracht gereed als exacte technische blokkade: geen lokaal gebonden bruikbare debuggerroute.** Wel nieuwe ABI-, read-only citymapping- en completed-storebindingen. Geen attach, spelstart, gameplay-/binarymutatie, nieuwe observer/framework/harness, installatie of test.

## 1. Feitelijk beschikbaar instrument: niet aangetoond

Lokale read-only checks16:16..16:21:

- Get-Command vond cdb.exe/windbg.exe/x32dbg.exe/ntsd.exe/DbgX.Shell.exe niet in PATH.
- Test-Path: geen cdb.exe of windbg.exe onder Windows Kits10/Debuggers/x86 ofx64; geen ProgramFiles/WinDbg, C:/Tools/x64dbg ofx32dbg; geen WinDbgX.exe/windbg.exe-appalias onder LocalAppData/Microsoft/WindowsApps.
- Get-AppxPackage '*WinDbg*' gaf geen pakketresultaat. WindowsApps-directory bestaat maar het lezen gaf access denied; daarom geen sluitend bewijs dat op de hele pc niets is geïnstalleerd.
- CIM-query naar genoemde debuggerprocessen gaf access denied: **geen processcount0/afwezigheidsbewijs**. Geen attach uitgevoerd en niet geëscaleerd om die niet-blokkerende procesinventaris te omzeilen.
- PROEVEN/hulpmiddelen bevat alleen directorypython. Gerichte bestands/codezoektocht in PROEVEN vond geen bestaande DebugActiveProcess/WaitForDebugEvent/(Wow64)GetThreadContext/DbgEng-debugloop. H3-reader Lees-Onderzoeksactivatie.py declareert alleen read-only OpenProcess(0x410=QUERY_INFORMATION|VM_READ), RPM en snapshots; geen debugregister/event-/thread-/detachroute.
- Huidige PowerShellproces en OS zijn64-bit; oorspronkelijke gameenginePE is32-bit. Aanwezigheid van64-bitPython/native offlinehelpers levert geen uitvoerbare WOW64-debugger.

**Exact blocker:** er is geen gevonden/gepinde tool met aantoonbaar vier executehardwarepins, begrensd log, alle huidige/nieuwe threads, juiste32/WOW64context, restore en pendingevent-detach. Toolpad/versie/bitness/hash kan daarom niet eerlijk worden geleverd. Dit is geen universele 'Windows kan dit niet'-uitspraak. B moet expliciet een werkelijk beschikbaar instrument aanwijzen of een andere observatieroute kiezen; niet automatisch een nieuw debuggerframework bouwen of installeren.

Microsoft [ba](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/ba--break-on-access-) documenteert processorbreakpoints met execute-toegang en commandstrings; dat bewijst geen aanwezige WinDbg/CDB-versie of betrouwbare lokale vierpin-/threadroute.

## 2. Vier pincontexts: bewezen machinecode en resterende toolgrens

Originele engineSHA256 b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79/base400000/timestamp37d6f702 en AI3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44/base20000000/timestamp37b894e7 rechtstreeks herbevestigd. Gerichte Capstone32-bit bodies; Robotcom bestaande binding, geen civctp.map. Alles hieronder statisch, nietlive.

### A20020fa9: echte AiMain op[ESP], niet op[EBP+8]

SatisfyMinimumCityRequirements-entry20020eb0 bindt CityAgent=ESI op20020eb8 `8bf1`;20020ebe `8b7d08` houdt origineleAiMain inEDI. Vervolgens wordt [EBP+8] door getters overschreven op20020ee0/efe/f28. Dat oude argumentslot is bij A dus **geen AiMain**.

Vlak vóór CALL:20020fa6 `57` pushtEDI,20020fa7 `8bce` zetECX=ESI,20020fa9 `e822030000`→minimumfood. Daardoor op de precallpin **AiMain=EDI=[ESP]**, CityAgent=ECX=ESI, cityID=[CityAgent+0c], civ=[AiMain+20]. Geen callee-return opESP; die wordt pas door de CALL gemaakt. De opgepakte17dwordargumenten beslaan[ESP,ESP+44h); laatste double1 ligt[ESP+3c..43]. AiMain niet uit geraden stackscan of callee-entryoffset halen. Playerinterface=[AiMain+2c]; native52b4f2 `8b4808` bevestigt PlayerInterface+8 als echtePlayerpointer. Extra vergelijking met [engineGlobalA7DD80][civ] mogelijk; geen nativefunctie remote oproepen.

### Read-only cityID ↔ handle ↔ CityData ↔ centrum

Een kleine bestaande inverse-arrayroute voorkomt een nieuwe remote tree-getter:

- Native4cb100 loopt Player+12c0-cityhandlesarray (count+8,data+0c), zoekt de exacte unitHandle en haalt dezelfde index uit Player+12c4-IDarray (4cb138 `8b89c4120000`;4cb13e `8b510c`;4cb141 `8b0482`). Read-only kan dezelfde parallelle koppeling omgekeerd worden gezocht op exactA-cityID; actuele counts/capaciteiten/buffers moeten matchen, uniek resultaat vereist.
- Arraylayoutcount+8/data+0c is native. Capaciteitsguard moet echte huidige header+4 (bestaande containerlayout) met checked count/bytebereik verifiëren; geen capacityblob dump of vast policy-aantal als echtecount. Zonder toolread/boundsbewijs blijft het resultaat UNKNOWN.
- NativeUnitPool4b2300 valideert nietnulhandle, `(handle&f0000000)==[Pool+4]` en bucket[Pool+0c+4*(handle&3ff)].4a68e0/4a68a0 zoeken unsigned exacte handle in node+0c, links+4 bij nodeID>handle, rechts+8 bij nodeID<handle. Equalnode is nativeUnitData; niet alleen bucketpointer als UnitData aannemen. Alleen boundedreadnodepad met cycle-/readfailureguard, geen gettercall of volledige pooldump.
- UnitData+58→CityData; City+5cc→Happy; City+4 en UnitData+18 moeten werkelijkeciv matchen. City+44c bevat eigen unitHandle en moet de gevondenhandle matchen. Native4da9a0 leest UnitData+4c/+50 als achtbytes interne centrumpositie (4da9b6 `8b504c`;4da9bb `8b4050`). Read-only dezelfde raw8bytes, geen externeCityAgent-positie als internecoördinaten presenteren.
- H/F kunnen dezelfde daadwerkelijke ownerPlayerarrays gebruiken om hun ECX/City aan een echt cityHandle/ID te koppelen; mismatch geeft UNKNOWN. Alleen herkenbare natuurlijkeAI-context, mens/barbaren niet op een gegokte Player+4-typewaarde wegfilteren. Actorbinding met A of bestaande bewezen speleridentiteit blijft nodig.

De maproute4cb060 is eveneens gelezen: Player+12c8-root+8, nodes+0key/+4links/+8rechts/+0cpayload, payloadindex→12c0.data. Zij is een remote-callverbod-neutrale nativebinding, geen toestemming de enginegetter aan te roepen. De parallelarrayroute hierboven volstaat als statische mappingbron.

### H/F-entry en S-completed-pair

H4ab410 preimage `55 8bec 83ec18`: ECX=Happy; entryESP bevatreturncaller,+4City,+8projection,+0cmartialoutputpointer,+10advance. Cityargument wordt later inH-frame overschreven: niet na proloog blijven lezen alsof het ongewijzigd is. F494970 preimage `55 8bec 83ec14`: ECX=City, entryESP returncaller/+4terrainbufferpointer. Beide zijn echte reeds gebonden entrylayouts; geen outputpointer/buffer derefereren voor deze ordermeting.

S4ab2f9 **is vóór de eerste store**, nietcompleted. ESI=Happy, ECX/EDX low/highwords. `4ab2f9 898ea8000000` schrijftlow;`4ab2ff 8996ac000000` schrijft high; **4ab305 `33db` is de mechanische na-beide-storesgrens**. Nativeprojection/advance-skipbranches4ab175/4ab17e gaan naar4ab307, niet305. De normale gevolgde durationroute bereikt305 lineair na beidewrites, voordat daaropvolgende instructieEBX wijzigt. B kan expliciet S vervangen door305 om met dezelfde vier hardwarepunten completed-pair te meten; dat is een ontwerpwijziging voor B, hier niet toegepast. Zonder na-grens blijft S-label STORE_BEGIN, nooit completed.

Cruciaal: in4ab0f0 worden oorspronkelijke **projection[EBP+10] én advance[EBP+14]** als scratch hergebruikt:4ab19b/2e4 `895d10`;4ab264/27d `897d14`;4ab282 `c7451400000000`. Die words zijn opS dus geen flags. EigenCity[EBP+8]/Player[EBP+0c] worden in gelezen completebody niet overschreven. Eigenreturn[EBP+4] moet4ab4c0 zijn; opgeslagenEBP verwijst dan direct naarH-frame. H-frameprojection+0c enadvance+14 worden vóór4ab4bb gelezen voor de helpercall; relevante code4ab4af `8b5514`,4ab4b2 `8b450c`,4ab4bb `e830fcffff`. Alleen direct gebonden H-frame/event mag flags leveren, nooit de overschrevenS-args. Happy==[City+5cc], owner==Player+0 en[Players[owner]] moeten overeenkomen; onbekende nesting/caller geeft UNKNOWN.

### Echte threadstackbounds blijven instrumentafhankelijk

[Microsoft !teb](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/-teb) toont StackBase/StackLimit van de geselecteerde actuele thread. Dit is algemene debuggerdocumentatie, geen werkelijk gelezen32-bitWOW64-TEB hier. De aanwezige snapshotreader heeft geen thread/TEB-/stackboundroute. Daarom **geen gevalideerde StackLimit/StackBase beschikbaar** en geen toestemming bovenstaande EBP-chain remote te lezen zonder die grens. Een latere concrete toolroute moet dezelfde thread,32-bitTEB/selectors en readablecommittedranges leveren; ESP/EBP zelf, FS-base van de lokale64-bitPowerShell of guessedstacksize volstaan niet.

## 3. Debuggingveiligheid: algemene voorwaarden, geen lokaal contract

Er is geen echte tool om rights/context/events/RF/herarm/restore/detach tegen te inspecteren. Daarom is dit antwoord **technisch ongebonde route blokkeert C**, niet zelfgeschreven APIlus met verzonnen constanten.

|Onderdeel|Primaire platformbasis|Exact lokaal open|
|---|---|---|
|Attachrechten|[DebugActiveProcess](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-debugactiveprocess) vereist passende volledige targettoegang; attach meldt bestaande threads/modules en initbreak.|Snapshot0x410 is geen debugtoegang; succesvolle rights/attach, juiste toolversie en onderscheid initbreak versus eigenhardwareevent niet aangetoond.|
|32/WOW64context|[Wow64GetThreadContext](https://learn.microsoft.com/en-us/windows/win32/api/wow64apiset/nf-wow64apiset-wow64getthreadcontext) vraagt THREAD_GET_CONTEXT/ContextFlags en geldige gestopte thread;[Wow64SetThreadContext](https://learn.microsoft.com/en-us/windows/win32/api/wow64apiset/nf-wow64apiset-wow64setthreadcontext) schrijft selectief en waarschuwt voor runningthreads.|Geen gevalideerde echte32-bitcontexttool, selectieveDR-/flagsbackup/restoreroute, RF/TF/DR6/DR7-eigenevent-/resume-/herarmcontract. Geen waarden of threadhacks ontwerpen.|
|Events/nieuwe threads|[debugmainloop](https://learn.microsoft.com/en-us/windows/win32/debug/writing-the-debugger-s-main-loop) beschrijft processtop bijevent, create-thread/moduleevents en continue.|Geen toolcontract dat vóór continue alle relevante huidige/nieuwe threads/modulebases gebonden zijn, logging begrensd is of events geen gaten hebben.|
|Pendingevent/exception|[ContinueDebugEvent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent) onderscheidt handled/nothandled en hoort bij betreffendePID/threadevent.|Geen actualpendingevent-/ownexceptionclassificatie, timeout/budgetrestore/hervatroute of bewijs dat ongekende engineexceptions niet worden opgeslokt.|
|Detach/uitval|[DebugActiveProcessStop](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-debugactiveprocessstop) heeft controleerbare successreturn;DebugActiveProcess-documentatie meldt targetexit bij debuggerexit tenzij kill-on-exitbeleid gewijzigd.|Geen gekozen instrumentpolicy voor targetnietkillen, exacte debugregisterrestore perthread, pendingeventafwikkeling vóórdetach, detachedbewijs of normaleclosebinnenreserve. APIbestaan is geen safe-detachbewijs.|

Geen softwareINT3/DLLinjectie of nieuwframework stil als alternatief genomen. Iedere latere gekozen route moet dit concrete contract leveren vóór Start; onder budget/timeout nu geen debugger besturen of sluiten omdat hier geen attach gedaan is.

## Handoff en stop

Drie schriftelijke antwoorden geleverd: (1) geen inspecteerbare aanwezige debuggerroute aangetoond met exact gezochte locaties/permissiongrenzen; (2) precallA, read-only citykoppeling, H/F, S-na-storegrens en clobberedflags gebonden; werkelijkethreadbounds nogtoolblocker; (3) Microsoftvoorwaarden gekoppeld aan exact ongebonde lokaleveiligheidsdelen. **Voldoende voor terugkeer naar B met expliciete instrument-/alternatiefkeuze.** Geen completefoodgate of trace-C-vrijgave. Geen verdere tool/engine/frameworkreconstructie als impliciet vervolg.

Analist stopt; alleen twee eigen analysebestanden geschreven. Pc aan, geen afsluitactie. Laatste eigenbudget16:19:30 week94/vijf60/stateok, bron6.7s oud; rootcheck later bepalend voor vervolg.
