# Science C1: helperadres en één attempt9

15 oktober 2026, 15:09 Europe/Amsterdam. Fase B gereed voor rootreview. Basis is de door root geaccepteerde [gerichte A-overdracht](../ANALYSE/SCIENCE-FIXTURE-ADRES.md). Alleen voorstel; geen bronwijziging, compilatie, nativecall of spelhandeling uitgevoerd.

Dit ondersteunt projectdoel1/5: science-locaties herkennen tijdens nuttige uitbreiding. De onmiddellijke blokkade is uitsluitend de ontbrekende centrum64/ABI-fixture. De bestaande29 cases blijven deelbewijs. FLI/AIP kan dit eigen helperadres niet bepalen: dit betreft de testlauncher van reeds ontworpen aanvullende science-logica, geen nieuwe gameplayaansturing of modding-hook. Engine-/sciencepolicy en gewichten blijven gelijk.

## Huidig en gewenst

Attempt8 vraagt vroeg zeven eigen64KiBblokken en faalt op00400000/error487, vóór alle callbacks. Zijn PE heeft preferredBase00400000; oudere helper preferredBase10000000. Dat bewijst een plausibele botsing, niet welke mapping destijds daadwerkelijk op00400000 zat. `owned.Contains` alleen bewijst geen OS-eigendom.

Gewenst: compileer de **actuele twee C#-bronnen**, inclusief pointercorrectie en early-reserve/finally, met preferredBase10000000 als nieuwe attempt9. Controleer werkelijk laden en zeven eigen allocations vóór callbacks. Het voorkeursadres garandeert geen werkelijke mapping; DYNAMICBASE blijft behouden. Geen oude executable hergebruiken.

## Minimale helperbrondelta en compilerroute

Werkmap: `PROEVEN/science-u30-40/20261013T183300/`. C bezit deze map volgens afzonderlijke toewijzing; bewaar bronkopieën/diffs/pins vóór wijziging, oude attempts/logs blijven intact. Gameplaykandidaat `SCIENCE-C1-CREDIT-OFF.prepared.dll`, SHA256 `622cdd87c7b9480e9740ca5baaf37190ed632852358db0f80f6b6b936b13d6ba`, fixturebytes (inclusief gecorrigeerde large-center-reader), modellen, Hostvalidator, callbacks en dertig bestaande cases blijven gelijk.

- `native-main.cs`: log vóór de bestaande `ReserveEngineBlocks` eigen PID, bitness, volledig mainmodulepad, **werkelijke** BaseAddress en ModuleMemorySize. Geen serializer vóór early-reserve invoegen. Behoud bestaande try/catch/finally en uniek `native-attempt9.json`; ook stdout/stderr krijgen eigen attempt9-namen.
- `native-fixtures.cs`: voeg uitsluitend VirtualQuery-P/Invoke met SetLastError en correcte x86 MEMORY_BASIC_INFORMATION toe: BaseAddress, AllocationBase, AllocationProtect, RegionSize, State, Protect, Type (28bytes; controleer Marshal.SizeOf). Gebruik pointer/UIntPtr-velden en gecontroleerde unsigned/64bit-intervalrekening, geen signed32-overflow. Kleine eigen queryroutine logt de zeven volledige intervallen00400000/00490000/00510000/00520000/00530000/00740000/00a70000, elk lengte10000hex. Loop bij kleinere regio's tot intervaleinde; queryfailure/nulvoortgang/overflow stopt vóór callbacks.
- Voor de allocaties: elk deel moet MEM_FREE zijn. Log BaseAddress/AllocationBase/RegionSize/State/Type/Protect en stop bij conflict; schrijf of unmap daar niets. Controleer expliciet dat de werkelijke mainmodule-range en de kandidaatvoorkeursreservering20000000 geen fixtureblok overlappen. Identificeer een helperbotsing alleen wanneer werkelijke module-range/AllocationBase die conclusie ondersteunt.
- Behoud per blok de bestaande `VirtualAlloc(wanted,0x10000,0x3000,4)`. Sla returnpointer en bij falen LastError **onmiddellijk** op vóór een andere API-call. Registreer iedere werkelijk door deze call verkregen niet-nulle pointer in de eigen lijst vóór een volgende controle die kan gooien; eis daarna exact `p==wanted`. Na succes controleert de queryroutine ieder deel op MEM_COMMIT/MEM_PRIVATE/AllocationBase==p/PAGE_READWRITE. Behoud de bestaande exacte blokset en owned-binding in `Run`. Geen succes op basis van alleen eerste pagina of lijstlidmaatschap.

Compileer vanuit deze map met de reeds aanwezige32bit-frameworkcompiler, zonder nieuw toolchainonderdeel. Concrete opdracht (A reconstrueerde deze route; niet als historisch succesvol commando claimen):

```text
csc.exe /nologo /target:exe /platform:x86 /baseaddress:0x10000000 /r:System.Web.Extensions.dll /out:native-fixtures.attempt9.exe native-main.cs native-fixtures.cs
```

Gebruik het vastgestelde bestaande absolute csc-pad en behoud eventueel aantoonbaar aanvullende bestaande opties/referenties. Geen slashpaths als bronnamen; nieuwe outputnaam, geen overschrijving. Geen wijzigingen aan ASLR/relocatiebeleid, fixtureadressen of DLLpreferredbase.

## Offlinevrijgave, één uitvoering en cleanup

C levert vóór starten aan root: twee kleine brondiffs/pins, ongewijzigde kandidaat-/fixture-/modelpins, compilerpad/opdracht/exitcode en offline PEdecode/hash. Verwacht x86 PE32, ImageBase10000000, geldige SizeOfImage, behouden flags/relocaties; eventuele afwijking expliciet beoordelen vóór vrijgave. Het oude SizeOfImagec000 is geen vaste eis voor gewijzigde bron. Controleer querystructuur28bytes, bereikslussen/eigendom/failurecleanup en behoud van de gecorrigeerde uitvoerpointer. Geen nieuwe fixturebouw nodig.

Na rootbron/PEreview precies **één** compiledhelperstart: eigen nieuwe executable, bestaande pakketargument plus `attempt9`, bestaande30-case finite run toegestaan. Gebruik de bestaande30s-deadline en korte controlepolls; log PID/path/creationtime/start/einde/werkelijk gemeten exitcode. Geen ASLRretry, tweede start, unmap, Hostguardbypass of alternatieve science-kandidaat. Geen game/CD-/GUI-/RPM-afhankelijkheid. Verse budgetcheck vóór compilatie/start; week≤25% waarschuwen, week≤10% of vijfuur≤5% projectwerk stoppen/checkpoint bewaren, pc aanlaten.

Behoud early-reserve vóór serializer/loader en beide finallyroutes: `ReserveEngineBlocks` ruimt gedeeltelijk verkregen eigen allocations op, `Run` ruimt zijn eigen allocations/module/reservering op, `Main.finally` blijft idempotente eindcleanup. Geef uitsluitend geregistreerde eigen pointers vrij; geen uit VirtualQuery afgeleide vreemde AllocationBase vrijgeven. Log cleanupresultaten/afwijkingen zonder de eerste failure te verliezen. Een timeout is failure: stop fixtureactiviteit volgens de bestaande helperafwikkeling, noteer of finally voltooid is en bevestig exact eigen proces afwezig. Geen exitcode0 of volledige cleanup verzinnen als de wrapper geen waarde oplevert. Geen vervolgattempt als cleanup of eigendom onzeker is.

## Meetlat, bewijsgrens en overdracht

Adresacceptatie: werkelijke helpermapping buiten alle zeven blokken en zeven volledige exact verkregen/eigen gecommitteerde RWallocations; conflictopname bij failure is een geldig diagnoseantwoord, geen PASS. Dit bewijst alleen setup.

De eigenlijke blocker is `isolated_SCI_center_above_int32`: bestaande verwachte center2147483648/current_S32147483672/margin3_x24294967284, gewenste locatie2/development3 en alle bestaande ESP/nonvolatile/x87/canarycontroles moeten slagen. Tijdelijke eigen dispatch moet worden hersteld; mapped kandidaat en Hostvalidator blijven bytegelijk. Hergebruik bestaande decoder/paritycontrole; onderscheid dertig volledige cases van nativecalls of alleen een samenvattende passflag. Geen nieuwe brede caseverzameling als voorwaarde.

Verwacht effect: bestaande C1-fixtures bereiken de laatste64bit-case zonder botsing met het eigen voorkeursadres. Neveneffect: eigen helpermapping en enkele setupqueries/logregels veranderen; gameplaycode niet. Onzekerheid: werkelijk CLR/ASLR-laadadres en andere bezette regio's kunnen ook met nieuw voorkeursadres allocatie blokkeren. Dan stopt deze poging met concreet regio-/mappingbewijs terug naar gerichte analyse. Geen gegarandeerd allocatiesucces beloven.

Alternatieven: oude exe mist actuele correcties; random bases/retry/unmap en guardversoepeling ontbreken als onderbouwde route. Alleen PEheader aanpassen mist de gecontroleerde hercompilatie van actuele bronnen. Daarom één expliciete compilebasis met werkelijk eigendomsbewijs.

Herstel: attempt9-brondelta desgewenst uit eigen vooraf bewaarde bronkopieën terugzetten; executable/logs als bewijs bewaren. Kandidaat/game/release/saves behoeven geen herstel omdat zij ongemoeid blijven. Na acceptatie is science-C1 nativefixturedekking op dit onderdeel aangevuld; echte hostacceptatie, sciencecredit/union, combinatie met U30 en gameplaywinst blijven afzonderlijke vervolgproeven. C draagt compacte uitkomst/counters/cleanup/pins aan root over; deze B-rol stopt na overdracht.
