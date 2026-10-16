# Science attempt9 — voorbereid voor rootreview

15 oktober 2026, 15:13 Europe/Amsterdam. Bronnen gecompileerd/offline gecontroleerd; **geen helper gestart**. Toepassing uitsluitend helperbronnen, SCI-kandidaat/modellen/callbackfixtures/30cases onveranderd. `native-attempt9-preparation.json` pint alle vooraf bestaande bestanden behalve de twee gewijzigde helperbronnen; alle pins bevestigd. Oude evidence/attempts blijven behouden. `native-attempt9-offline-checks.json` bewijst volledige casebodygelijkheid en behoud gecorrigeerde centerreaderpointer.

Bronnen: `native-main.cs` en `native-fixtures.cs`, herstelkopieën `*.before-attempt9`, kleine afzonderlijke `*.attempt9.diff.txt`. Main logt eigen PID/bitness/path/werkelijke modulebase+size vóór early-reserve en serializer. Query heeft zeven x86MBIvelden, verwachte28bytes met runtimeassert; unsigned64-intervallen lopen door tot elk64KiB-einde met nulvoortgang-/overflowchecks. Alle zeven intervallen zijn vrij gecontroleerd vóór allocation. Iedere niet-nulle eigen VirtualAllocpointer wordt onmiddellijk geregistreerd vóór controle; exactpointer en volledigeCOMMIT/PRIVATE/AllocationBase/RW worden daarna geëist. Werkelijke mainmodule en kandidaatreservation worden op overlap uitgesloten. Geen unmap/retry/hostguardbypass. Cleanup logt uitsluitend eigen pointers/module/reservation en behoudt eerste fout; sticky CleanupOk blokkeert PASS bij cleanupfout.

Compilatie: bestaande `C:/Windows/Microsoft.NET/Framework/v4.0.30319/csc.exe`, exactcommand/exit0 in `native-compile-attempt9.json`. Nieuwe output `native-fixtures.attempt9.exe`, SHA256 `935d86579ab880294a552401793ce86c982aa82f17e2781cf0b30fc211f47e81`. OfflinePE: x86PE32, ImageBase10000000, SizeOfImagee000, DllCharacteristics8540/DYNAMICBASE behouden, relocatiedirectoryc000/12bytes. Werkelijke mapping nog niet gemeten; preferredbase garandeert dat niet. SCI-kandidaat blijft `622cdd87c7b9480e9740ca5baaf37190ed632852358db0f80f6b6b936b13d6ba`.

Na concrete rootvrijgave precies één start, werkdirectory dit pakket:

```text
native-fixtures.attempt9.exe C:\GIT\ctp\PROEVEN\science-u30-40\20261013T183300 attempt9
```

Gebruik bestaande30s-deadline met korte polls; nieuwe logs `native-attempt9-stdout.txt`/`native-attempt9-stderr.txt`, procesrecord `native-attempt9-process.json`, resultaat `native-attempt9.json` (moeten vooraf afwezig zijn). Capture PID/exactpath/creationtime/werkelijkexit. Geen tweede poging. Setupmapping/sevenblocks en30volledige cases tellen afzonderlijk. Centrumcase moet center2147483648/current_S32147483672/margin3_x24294967284/location2/development3 en bestaandeESP/nonvolatile/x87/canaries halen. Decoder/parity bestaand hergebruiken, callbacks en tijdelijke dispatchrestore controleren. stdout bevat iedere regiocheck/allocatie/cleanup. Bij conflict/timeout/fout eerlijk bewijs terug naar root; geen alternatieve mappingstrategie.

Herstelbronnen kunnen uit `*.before-attempt9`; binaries/logs behouden als evidence. Geen game/release/saves te herstellen. Voorbereiding afgerond, uitvoerder wacht zonder actieve helper op rootvrijgave. NativeABI/sciencecredit/union/host/gameplay blijven open.
