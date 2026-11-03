# Wonderlijstprojectie — C0, 29 oktober 2026

Voorbereid en offline gecontroleerd. Geen installatie, spelstart, proceshandle/RPM of gameplaymeting door deze C0. Doel4 blijft OPEN. Het pakket voegt uitsluitend effectieve Wonder_List en opening_required/completed toe aan de bestaande releasewaarneming van alle zeven AI's.

`Lees-Wonderlijst.py` laadt de originele `Lees-Doel3.py` en `original_core.py` via absolute paden met unieke modulenamen. Ook reeds geïmporteerde `original_core`/`doel3original_core` worden niet hergebruikt of veranderd. De in-memory bronprojectie verandert alleen de core-import, twee verplichte CLI-argumenten en de exacte creation-FILETIME-check onmiddellijk na GetProcessTimes, vóór modules/decoder. De originele bestanden blijven intact. `release-projection.diff` maakt deze drie vervangingen reviewbaar. De oorspronkelijke trusted_binding, verify_loaded, stable_sample, observe_goal3 en scalar_state zijn AST-gelijk. De toegevoegde wonderwaarneming omhult observe_goal3 en draait binnen dezelfde twee volledige stabiele samples. OpenProcess blijft 0x410 (QUERY_INFORMATION|VM_READ).

Pins omvatten wrapper/fixturechecker/diff/documentatie, originele reader/core/participants, eb6-DLL en B2manifest/payloadbinding, tekstmanifest/baseline/checker/diff en alle15 staged tekstbestanden. Actuele aidata moet bij iedere sample exact overeenkomen met control118 of candidate126 (118+8), inclusief alle ongemodificeerde bestanden. Het eigen participantsmanifest is een bytegelijke gepinde kopie van PROEVEN/landbenchmark/20261027/participants.json voor de c6ba-LAND-start; de oude release-civnamen worden niet gebruikt. Variant voor deze proef: B2a-N30-TECHNICAL met eb6f58a7… en payload7825bac0…/4348bytes/RVA0xd4000; beide armen houden diezelfde DLL.

Lijst: ownercontrole actor→planner+0x20→actor, container/data/count0..200,32bytes per record, finite gewicht, niet-negatieve signed native index en categorie−1. Null en leeg staan apart. Symbolen: maximaal4096 buckets en4096 unieke nodes totaal, visitedset tegen cycli/hergebruik, naamterminatie binnen128bytes, unieke exacte namen, externe pointer0, inputmask&4, flags+0x68&4=0 en byte+0x6a&1=0. Doubles zijn exact positieve0 of1 en complementair. Inconsistentie verwerpt de read. Geen enginecalls of writes.

`opening_list_expectation` meldt bij opening_required1 kandidaat PASS uitsluitend bij count1/gewicht9100/categorie−1 en controle PASS bij meerdere entries; anders FAIL. Buiten de opening: NOT_APPLICABLE. Brongewichten/counts en categoryhashes van alle zeven gepinde persoonlijke herstelpartials worden meegeschreven; `source_weight_sequence_matches` vergelijkt uitsluitend gewichtenvolgorde. Dit identificeert geen token of persoonlijkheid. `native_token_binding` blijft UNKNOWN: index17 in de fixture is willekeurig. Een count1/9100-metingen plus één-tokenpartial bewijzen geen onafhankelijke native Labyrinthbinding, enqueue of productie.

Offline hercontrole (Python312 exactpad):

```powershell
& 'C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe' C:/GIT/ctp/PROEVEN/wonderlijst-meting/20261029/check_offline.py
```

De eindige fixtures testen geldige decode, null/leeg, bounds/pointers/owner, cyclische/duplicaatketen, symbolflags/waarden, categorie/index/gewicht en exacte creationtime. Zij emuleren geen spelgedrag. `offline-result.json` is het eerste bewaarde resultaat; hercontrole zonder --output overschrijft het niet. Bron-/payloadbinding wordt offline werkelijk met de oorspronkelijke trusted_binding gecontroleerd.

Na rootreview, uitsluitend binnen een afzonderlijk toegestane hostproef, behoudt de normale CLI alle originele argumenten. Voorbeeld met werkelijk gemeten PID en 64bit creation-FILETIME invullen:

```powershell
& 'C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe' C:/GIT/ctp/PROEVEN/wonderlijst-meting/20261029/Lees-Wonderlijst.py --pid $exactPid --creation-filetime $exactCreationFiletime --wonder-arm control --variant B2a-N30-TECHNICAL --run-id wonder-control-20261029 --snapshot-label T1 --turn 1 --pass-label quiet --manifest C:/GIT/ctp/PROEVEN/wonderlijst-meting/20261029/participants.json --output C:/GIT/ctp/PROEVEN/wonderlijst-meting/20261029/control-T1.json
```

De kandidaat gebruikt `--wonder-arm candidate` en een eigen run-id/output. Die bestanden mogen nog niet bestaan. Geen hostgates/framework zijn toegevoegd. De wrapper bewijst zelf niet de geladen save of een atomair snapshot. Root beheert vooraf verse budget/proces/backups/versiepins, gelijke c6ba-T0 en invoer, gewone verse host per arm/max1n, rustige meetgrens, alle7AI's, daarna normaal sluiten/count0/archiveren/exact herstel. Lees AUTOMATISERING vóór spelbediening. Geen GUI of kandidaatinstallatie behoort tot deze C0-opdracht. Geen wijzigingen aan CTP-og/CTP-proef/saves of originele projectbron; herstel van C0 vereist alleen bewaren/verwijderen van deze eigen projectmap, nooit terugzetten van gebruikersbestanden.
