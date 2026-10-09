# H1-I / H1-M — technische kandidaatbouw

7 oktober 2026, 22:11 Europe/Amsterdam. Beperkte fase C van root: uitsluitend kandidaatbouw en begrensde technische verificatie. Ontwerp [SCORE-INVOEGROUTE-H1](../../ONTWERP/SCORE-INVOEGROUTE-H1.md), SHA256 `02AC9A121906022314A3204F69A4700D5854B5B680722A352C693D31F3802668`. De kandidaten zijn **voorbereid, op aparte bestanden toegepast, offline gecontroleerd en native technisch gemeten**. Ze zijn **niet geïnstalleerd in CTP-proef en niet in gameplay gemeten**.

## Resultaat tegenover technische criteria

| Criterium | Werkelijk resultaat |
| --- | --- |
| Exacte originele bron, herstelbaarheid | Proef-DLL origineel `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`; identieke [backup](backup/robotcom.original.dll). Beide varianten onafhankelijk vanuit deze bytes gebouwd. Geen installatie om terug te draaien. |
| Determinisme | Elke variant tweemaal uit dezelfde bron in geheugen gebouwd; bytes, payload en manifest identiek. Atomische aparte kandidaatwrites; afwijkend bestaand bestand wordt geweigerd. |
| H1-I | [Kandidaat](candidates/H1-I/robotcom.dll), SHA256 `59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0`; payload87 bytes; checksum `a2e3f`. Alle65536 AX-patronen native precies als signed16 teruggegeven, inclusief oorspronkelijke negatieve scores. |
| H1-M | [Kandidaat](candidates/H1-M/robotcom.dll), SHA256 `e13e00762d3de4662e1c24af8524ef06780ef3f5a612a1c5ca0306b3c23c152f`; payload215 bytes; checksum `a652e`. Native formule `S=B−1` uitsluitend voor B>1, geldige ground-context en terrain8/20/22; anders B. |
| PE, calls en branches | Onafhankelijk teruggelezen met bestaande pefile/Capstone. RVA784bb/78517/7aa35 elk E8 naar d4000 plus NOP; dezelfde adapter voor beide kandidaten en nieuwe-doelroute. Alle branches landen op instructiegrenzen. Alle CFG-paden eindigen met exact gebalanceerde ESP en ret10h; originele callbackret10h en terreinret0ch onderscheiden. |
| Bestaande PE-inhoud | Alle bestaande sectionheaders en directories identiek. Nieuwe `.h1` RX60000020, RVA d4000, raw a1400, rawsize200; SizeOfImage d5000. Alleen toegestane headers/checksum/drie sites/append wijzigen. Per variant32 werkelijk verschillende oorspronkelijke bytes; manifest bevat volledige before/after ranges. Geen nieuwe imports, exports, initializers of relocaties. |
| Native rebase | Preferredbase20000000 gereserveerd in eigen 32-bit helper. H1-I daadwerkelijk geladen op08660000, H1-M op08d40000. Drie targets en gemapte payload gecontroleerd. H1-M leest werkelijk eigenmodule+RVA; g_settle_z bewust met niet-nul bovenwoord getest om WORDlezing te bewijzen. |
| Gewone loader | Afzonderlijke eigen32-bit processen: beide gewone LoadLibraryW en FreeLibrary geslaagd op20000000. Dit bewijst loader/import/DllMainacceptatie in deze helperomgeving, geen gameactivatie. Geen AI/game-export aangeroepen. |
| ABI/canaries | Elke native case: exacte ESP vóór/na, EBX13579bdf/ESI2468ace0/EDI76543210/EBP55aa33cc, x87 controlword037f, diepte2/TOP6/tagc0 en registerinhoud gelijk vóór/na; World/vtable/AiMain/contextcanaries intact. Moduleimage na herstel van uitsluitend eigen fixtureglobals volledig identiek. |
| Beschermde bestanden | Voor/na volledige3090-bestandsinventaris van CTP-og, AAIP, proef en vaste-startmap identiek; bestaande saves, gebruikerswijzigingen, binaries en alleacht B1-AIPs bewaard. |
| Echte activatie/gameplay | Niet uitgevoerd. Geen bewijs van nieuw heapgebruik, nieuw GoalSettle+48, actief civprofiel, bergstichting of projectdoelwinst. |

## Native methode en concrete dekking

Eén fixturemethode: aanwezige `C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe`, standaard .NET/PInvoke, vaste eigen x86-shim/callbackbytes uit dezelfde eindige emitter. Helpers gebruikten uitsluitend eigen allocaties en eigen DONT_RESOLVE-mapping. Geen gameproces geopend/bediend, DLL geïnstalleerd, tool geïnstalleerd, save veranderd of pc afgesloten.

[H1-I-fixture](H1-I.native-fixture.json): PID20380,66158 cases, waarvan65536 identiteitsoutputs. [H1-M-fixture](H1-M.native-fixture.json): PID20824,622 cases. Per variant overige622 cases: zes scoregrenzen −32768/−1/0/1/2/32767 × alle terrain−1/0..23; terrain8/20/22 en hill9/19/21 met status0, geen outputwrite/sentinel, nullowner, Worldmismatch, z en globalz elk1/−1/32767/−32768;40 herhaalde/afwisselende AiMain-contexten met wisselende bergen/heuvels en vervuilde hoge positieargumenthelften. Originele getter ontving steeds precies sign-extended laag16; terrein ontving oorspronkelijke packed x/y/z, zonder y−x-omzetting. Bovenste EAX-helft van fixturegetter was bewust a55a. De context wordt per call gelezen.

[Gewone loader I](H1-I.native-loader.json): PID9140; [M](H1-M.native-loader.json): PID21248. Alle vier helpers exit0 en beëindigd; werkelijke looptijd0.609..1.188s, begrensd op45s per proces. [Procesverslag](native-processes.json). Geen extra emulator- of GUI-serie.

De native helper roept de adapter aan met fixtureWorld. De exacte drie calltargets zijn zowel offline als in de rebased mapping gecontroleerd; echte comparator-/GoalSettle-uitvoering is niet aangeroepen. Gelijke scoreformule op die routes volgt uit dezelfde target/payload, terwijl echte heap-/doelactivatie nog apart moet worden waargenomen. Geldige fixturepointers bewijzen geen fallback voor willekeurige stale pointers. Geen SEH/pointerprobe toegevoegd.

## Exacte ingreep en reproduceerbaarheid

[build.py](build.py) bevat alleen vaste x86-encodings, eindige labels/tweepassfixups en exacte hash-/header-/callasserts. [verify.py](verify.py) leest kandidaten onafhankelijk terug, controleert toegestane byteverschillen, PE/directorys, callbacks, module-PIC, globaleWORDoperand, volledige disassembly en alle CFG-stackpaden. [H1-I-manifest](H1-I.manifest.json) en [H1-M-manifest](H1-M.manifest.json) bevatten iedere gewijzigde fileoffset en before/afterbytes, iedere payloadinstructie, labels en hashes. Volledige [I-disassembly](H1-I.disassembly.txt) / [M-disassembly](H1-M.disassembly.txt) en [offline-resultaten](offline-results.json) beschikbaar.

Proloog bewaart EBP/EBX/ESI/EDI;32 bytes locals na de12 bytes bewaarde registers. B−10h, x−14h/y−18h/z−1ch, terrain−20h en zes packedbytes−28h..−23h zijn onderling disjunct en vallen binnen de allocatie. Onderste vier bytes zijn vrij. Alleen oorspronkelijke scorequery altijd; H1-I daarna naar epiloog. H1-M controleert B/context/lagen, gebruikt sentinel−1 en originele World+a8-interface, decrementeert maximaal eenmaal. EAX wordt volledig sign-extended. EFLAGS/ECX/EDX blijven vluchtig.

Recepten, bron en logs staan uitsluitend in `PROEVEN/score-h1`. Bouw: `py PROEVEN/score-h1/build.py`; onafhankelijk lezen: `py PROEVEN/score-h1/verify.py`; native: `py PROEVEN/score-h1/run-native.py`; eindinventory: `py PROEVEN/score-h1/finalize.py`. Geen installatie bij deze commando's. De builder overschrijft bestaande afwijkende artefacten niet. Een nieuwe native run zou eigen meetlogs vervangen; die is niet nodig voor dit gereviewde pakket.

[Pakketmanifest](package-manifest.json) bindt alle bron-/artefacthashes, huidige acht B1-AIPs, originele DLL en vaste T0-inventory. [Voorinventory](protected-before.json), [na bouw](protected-after-build.json), [na native](protected-after-native.json) omvatten volledige installaties en saves. QUOTA-START-T0 blijft SHA256 `8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26`. B1 is constant bewaard en krijgt geen gemeten winstclaim.

## Overdracht

Technische kandidaatcriteria geslaagd; geen aangetoonde bouw-/ABI-/loaderblokkade terug naar ontwerp. Root kan kandidaten, manifest, native resultaat en beschermde inventory reviewen en de volgende beperkte C-stap bepalen. Deze eerste opdracht geeft geen installatiemandaat. Latere proef vereist gecontroleerde proefprocesherstart vanaf exact T0, actuele modulehash, geldige civ/World/laag, nieuw heapgebruik en nieuw GoalSettle met de adapterkwaliteit; oude opgeslagen doelen worden niet automatisch herberekend. D:\CTP/PID19516 blijft ongemoeid. Volledige production/science/monopoly-, voedsel-, transport-, quota- en taakdoelen blijven vervolgstappen; er is geen gameplayverbetering geconcludeerd.
