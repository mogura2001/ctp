# Science C1: eigen helperadres buiten fixtureblokken

15 oktober 2026, 15:07 Europe/Amsterdam. Gerichte fase A, afgerond voor overdracht naar B. Alleen bestanden/PE-metadata gelezen; geen compiler, helper, callbacks, spel of procesgeheugen uitgevoerd/gelezen. Gameplaydoel 1/5: science-locaties meewegen. Deze analyse lost uitsluitend de setupvraag voor de nog ontbrekende centrum64/ABI-fixture op; zij levert geen nieuwe science- of gameplayacceptatie.

## Eindige vragen en dekking

| Beslisketen / vraag | Bevinding en bewijssoort | Route / voorwaarde | Status |
| --- | --- | --- | --- |
| Waarom faalt de vroege reservatie? | `native-main.cs:16` roept `ReserveEngineBlocks` aan vóór serializer/Run; `native-fixtures.cs:25–29` vraagt exact zeven blokken aan. Attempt8-overdracht registreert error487 op00400000 en0calls. PE-header van de gebruikte helper heeft preferredBase00400000. Dit is een adresbotsingshypothese, geen vastgestelde eigenaar van het bezette blok. | Werkelijke helpermapping en VirtualQuery nodig bij één volgende attempt. | Voor ontwerp voldoende; runtime-eigenaar blijft onbekend. |
| Kleinste compile/link-ingreep? | Bestaande oudere `native-fixtures.exe` heeft preferredBase10000000; attempt8 heeft00400000. Beide x86 PE32, SizeOfImage0000c000, DLLCharacteristics8540 en relocatiedirectory RVAa000/sizec. Bestandsfeit uit alleen-lezen struct-decoding. | Actuele twee C#-bronnen opnieuw compileren met expliciet `/baseaddress:0x10000000`, `/platform:x86` en een nieuwe attemptnaam; overige opties/referenties behouden. | Concrete route beschikbaar, nog niet gecompileerd. |
| Hoe onderscheidt één nieuwe attempt werkelijke vrije/eigen mapping van aannames? | Huidig `owned.Contains` controleert alleen de eigen lijst, geen OS-mapping; huidige launcher logt PID maar geen mapping. Bronfeit. | Kleine helper-only logging/check rond bestaande reservatie, hieronder. | Uitvoerbaar B-voorstel mogelijk. |

## Huidige bronnen en binding

Alles hieronder betreft `PROEVEN/science-u30-40/20261013T183300/`.

- `native-fixtures.attempt8.exe`: SHA256 `a72200e1a0e9917a9e398c132c492a681ea45d2887e9fac846d06a59c4da696e`, preferredBase00400000, virtueel voorkeursbereik00400000–0040bfff.
- `native-fixtures.exe`: SHA256 `6601b5f9778ddb0ed60a1bbb80a2eede74d1321b0f08b6455481dd5c715f6f27`, preferredBase10000000, virtueel voorkeursbereik10000000–1000bfff. Deze oudere executable niet hergebruiken: actuele pointercorrectie/early-reservatie zitten in de huidige bronnen, terwijl deze exe volgens preparation-audit ongewijzigd bleef.
- De zeven benodigde64KiB-blokken beginnen op00400000,00490000,00510000,00520000,00530000,00740000,00a70000. Alle liggen buiten10000000–1000bfff; ook de bestaande reservering op20000000 voor de kandidaat-DLL blijft ervan gescheiden.
- `native-fixtures.ps1` gebruikt Add-Type en is niet het te wijzigen startpad. De compiled launcher is `native-main.cs` plus `native-fixtures.cs` met System.Web.Extensions voor JavaScriptSerializer. De exacte succesvolle csc-opdracht is niet als script/commandolog in deze pakketmap aangetroffen; de overdracht meldt alleen de mislukte slashpath-opdracht en succesvolle compilatie vanuit de eigen map. Daarom is onderstaande opdracht een concrete reconstructie voor B, geen historisch gemeten commando:

```text
csc.exe /nologo /target:exe /platform:x86 /baseaddress:0x10000000 /r:System.Web.Extensions.dll /out:native-fixtures.attempt9.exe native-main.cs native-fixtures.cs
```

Gebruik de bestaande compiler en werkdirectory; geen nieuw toolchainonderdeel. Bewaar bestaande compileopties waar die aanvullend blijken. Microsoft documenteert BaseAddress als voorkeursadres, dus geen afdwinging van werkelijk laden: [C# compileropties](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-options/advanced#baseaddress). Beide bestaande bestanden hebben DYNAMICBASE; deze route verandert die vlag niet. Er wordt dus geen vaste mapping of gegarandeerde allocatieslaag geclaimd.

## Beperkte controle voor precies één toekomstige attempt

1. B/C bewaart actuele bron-/fixture-/candidatepins en bestaande attempts. Voeg uitsluitend in de eigen helper een compacte `VirtualQuery`-P/Invoke met correcte x86 MEMORY_BASIC_INFORMATION toe (7 velden,28bytes), plus logging/checks. Geen observerframework nodig. Log vroeg eigen PID/bitness/volledig modulepad, werkelijke mainmodule-BaseAddress en ModuleMemorySize. Dat zijn de eigen helpergegevens, geen CTP-procesgegevens.
2. Vóór reservatie: log voor elk van de zeven volledige64KiB-intervallen `BaseAddress`, `AllocationBase`, `RegionSize`, `State`, `Type`, `Protect`; loop alleen binnen dat interval wanneer VirtualQuery een kleinere regio teruggeeft. Een queryfout of enig niet-vrij deel stopt deze ene attempt vóór callbacks. Log de conflicterende regio; concludeer pas helperbotsing wanneer de werkelijke modulemapping/AllocationBase daarmee overeenkomt. Geen module-identiteit afleiden uit alleen een voorkeursadres.
3. Bestaande VirtualAlloc-aanvraag per blok behouden. Leg de teruggegeven pointer en LastError onmiddellijk vast bij falen, vóór volgende API-aanroep. Na succes vereist elk deel van het blok MEM_COMMIT, MEM_PRIVATE, AllocationBase gelijk aan de door deze poging exact verkregen blokpointer en verwachte RW-protectie; daarnaast bestaande owned-lijstbinding/exactsetcontrole behouden. Alleen zo'n verkregen pointer mag in cleanup worden vrijgegeven. Log tussentijds naar stdout zodat ook vroege setupfouten zichtbaar blijven. Een deels geslaagde set wordt alleen via eigen geregistreerde pointers opgeruimd.
4. Compileer naar nieuwe attemptnaam; decodeer offline x86/BaseAddress/SizeOfImage/flags en hash. Afwijkende header betekent stoppen vóór starten. Na rootreview precies één gecontroleerde helperstart met bestaande deadline/resultaatpad en huidige SCI-kandidaat622c...; geen retries, unmap, SCI-/Hostguardwijziging of aanpassing van fixtureadressen/callbacks. Bij nieuwe conflictstop leveren de mappinggegevens het concrete vervolgantwoord, geen automatische andere strategie.
5. Acceptatie van deze adrescorrectie vereist werkelijke helpermapping buiten alle zeven blokken én zeven aantoonbaar eigen allocations. Dit bewijst alleen setup. De centrum>2^31-case moet vervolgens eigen ESP/nonvolatile/x87/canary- en resultaatcontroles halen; daarvoor blijft het bestaande30-casepad bruikbaar. De bestaande29cases uit attempt6 blijven deelbewijs. Nieuwe helpercalls zijn gecontroleerde fixtures, geen echte enginequeries/gameplay. Stop/finallycleanup en procesafwezigheid bij afwikkeling vastleggen.

`VirtualQuery` beschrijft regio's met gelijke kenmerken; daarom is alleen een query op de eerste byte onvoldoende voor een algemeen interval: [Microsoft API-documentatie](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualquery).

## Overdracht en grenzen

A-vragen3/3 voldoende beantwoord om B uit te werken. De minimale adresingreep is expliciete helper-BaseAddress10000000 bij hercompilatie; de enige aanvullende bronwijziging betreft eigen mapping-/eigendomsbewijs. Geen aanpassing van SCI-kandidaat, sciencecredit, union, engine, saves of game. Runtime-eigenaar van attempt8-blok00400000 is niet achteraf vastgesteld; dit blokkeert het begrensde voorstel niet. Slagen van de nieuwe allocaties en de laatste ABI-case blijft C-werk. Analyse gestopt; geen actieve helper/run/planning achtergelaten.

Budgetcontrole15:04:49Europe/Amsterdam: bron13:04:31UTC/leeftijd18,2s, vijfuur51%, week92%, stateok. Pc blijft aan.
