# B2a — technisch gebouwd en offline gecontroleerd

8 oktober 2026, 16:17 Europe/Amsterdam. Beperkte fase C onder rootvrijgave; alleen `PROEVEN/opening-b2` gewijzigd. Frozen voorstel SHA256 `ea5140b5505c11f457bdcdc3cf41fcc023e277bf247866228ad356919c9ef40e`. **Geen installatie of gameplaymeting.** N25 en N30 zijn beide technische fixtures; geen strategische stadsgrens gekozen.

Er zijn twee echte geïntegreerde vijf-hookkandidaten, elk met 4348 payloadbytes en 813 geheel gedecodeerde x86-instructies. De registratie, beginbeurt, Save, Load en reload-entry werken samen in dezelfde kandidaat. Het eerdere prepare.py-checkpoint is hiermee opgevolgd; [offline-results.json](offline-results.json) en de native-resultaten leggen de daadwerkelijke controles vast.

| Kandidaat | SHA256 | Native gevallen | Gewone loader |
| --- | --- | --- | --- |
| [B2a-N25-TECHNICAL](candidates/B2a-N25-TECHNICAL/robotcom.dll) | `9553d440365b029d47cd5b6c0717e6e96a6c2aeac3b1052bb80293736d35667a` | 88 geslaagd | Geslaagd |
| [B2a-N30-TECHNICAL](candidates/B2a-N30-TECHNICAL/robotcom.dll) | `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890` | 88 geslaagd | Geslaagd |

## Exacte ingrepen en toestand

De originele input-DLL blijft SHA `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`; engine SHA `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`. [build-inputs.json](build-inputs.json) bindt timestamps, imagebases en preimages. Alleen de vijf aangewezen oorspronkelijke vijfbytewindows veranderen, naast de nieuwe RX-section `.b2a` en sectioncount/SizeOfImage/SizeOfCode/checksum. Originele import-/relocatiedata en overige bestaande sections blijven gelijk. Alle nieuwe eigen adresverwijzingen zijn PIC/modulebase+RVA; de ondersteunde engine is bevestigd niet-ASLR met base400000.

| Oorspronkelijk RVA | Preimage | Nieuwe route |
| --- | --- | --- |
| 413da | `e81178ffff` | Originele AddSymbol, daarna completed/required, beide type0/null, defaults0/1, RegisterInit2 |
| 3625b | `e8902d0000` | Eigen latch/gate vóór originele FireRules2 |
| fe2d | `e88e29ffff` | Originele Save precies éénmaal, eigen record via echte gebonden Store-slot |
| fe51 | `e8fa2dffff` | Originele Load/EAX, host/archiveguard, boundedpeek, legacy of eigenrecordrestore |
| 61f0 | `558bec5356` | Capture/restore-wrapper, exact deze prologue éénmaal via trampoline naar61f5 |

Symbolen worden telkens bij de actuele AiMain/FliEngine opgezocht. Eigen doubles staan op+8/+c; **de werkelijk gebonden externalpointer staat op+0**, bewezen door constructor2003b6a2 en SetValue2003b7b3. Het oude checkpointlabel+4 is in onze bouwinputs gecorrigeerd. Geen+4-pointerguard blijft in read/restore/tests. +c2 bit2 wordt gezet; +68 bit2 blijft nul. Completion gaat uitsluitend0→1 bij cities≥fixtureN en activegovernment3; daarna blijft1 bij stadsverlies/andere regering. Required wordt altijd exact1−completed. Er zijn geen FLI/AIP-consequents/actions toegevoegd.

Het record is exact36bytes: 16-byte `CTP1B2OPENSTATE!`, little-endian version1, length36, civ-ID, completed0/1 en variantN. Het staat onmiddellijk achter de originele AiMain-payload, per civ. Bij eigen volledige marker worden alle velden gevalideerd vóór Load36; legacy consumeert niets en herstelt0/1. Een niet-lege volledig overeenkomende maar afgekapt markerprefix is een fout. Recordfouten laten de cursor onveranderd en retourneren Load0, zonder completionfallback.

Hostbinding leest alleen het main-imageadres van het eigen proces uit de PEB. Een andere base wordt direct afgewezen; de ondersteunde base krijgt eerst PE/Machine/timestamp/ImageBase/non-ASLR/bounds- en exacte Store/Load/Mode/fatal/managerfingerprintcontroles. Alleen daarna worden de concrete archivevtable/slots en layout toegelaten. Geen nieuw import, procesobserver, livegamehandle of injectie. De archiveguard controleert mode, niet-nul buffer, size≤capacity, unsigned overflow en buffer≤cursor≤geldig einde. Na de originele Save wordt opnieuw gevalideerd, zodat bufferverplaatsing werkt; na Store wordt geen oude pointer gebruikt.

## Acceptatie tegenover de meetlat

| Contract | Daadwerkelijk resultaat |
| --- | --- |
| Registratie/masks/per-civ | Originele call plus exact twee extras, type0/null, defaults0/1, RegisterInit2 en twee onafhankelijke civs native gecontroleerd |
| Fase-einde/geheugen | N−1/Theocracy, N/niet-Theocracy, N/Theocracy en latere terugval getest voor beide N; exact complementaire gate |
| ABI | ESP-cleanup, EBX/ESI/EDI/EBP, oorspronkelijke postcallstatusflags en x87-control/status/depth/waarden behouden in geslaagde fixtures |
| Originele Load-retour | 0,1,7 en87654321 getest; nul faalt vóór eigen consumptie, nonzero blijft exact behouden |
| Variant/legacy | Save0/1, exact alle36bytes, Load0/1, legacy na eerdere completed1, prefixtruncaties1..35 en ieder recordveld getest |
| Multi-civ/laatste data | Twee records met verschillende civ/completion worden ieder exact36 verbruikt; volgende managerbytes onveranderd |
| Archive-/symboolfouten | Foreign vtable, capacity/size/buffer/cursorfouten, ontbrekend nieuw symbool, werkelijke pointer+0/type/input-/initmaskers falen zonder recordconsumptie |
| Savebuffer | Verplaatsing tijdens originele Save gevolgd door correct record in nieuwe buffer native getest |
| Reload | Oude bit0/1 op callstack, exact originele prologue/rest éénmaal, daarna nieuwe symbolen opzoeken/herstellen; geen oude symbolenpointer hergebruikt |
| PE/rebase/loader | Deterministische herbouw, volledig gedecodeerde CFG/targets, exact verklaarde diff, gewone LoadLibrary en werkelijke rebase geslaagd; gemapte kandidaatbytes onveranderd |
| Load-foutpoort | Originele managerbytes52dec8: EAX0→call401560 vóór52dede. Eigen native parentfixture met expliciete fatal recorder toont geen nextcivvervolg |
| Save-foutpoort | Werkelijke kandidaat-thunk bereikt host+1560 met exact cdecl title/format; eigen recorder toont geen origineleSave/Store bij pre-fout. Onverwachte handlerretour eindigt volgens onafhankelijke decode inUD2 |

De fatale handler wordt **uitsluitend vervangen in eigen allocaties** door de benoemde recorder die terug naar de eigen shim springt. De originele AddSymbol/GetSymbol/FireRules/AiMainSave/Load/reload-rest zijn eveneens expliciete eigen stubs. Zelfstandige originele RegisterInit/SetValue-machinecode uit de kandidaatkopie werkt op eigen symbolen. Hostfingerprints worden eerst tegen een eigen exacte fixture gevalideerd; daarna zijn Store/Load/fatal callbacks in die eigen host vervangen. De adapters zelf blijven exacte kandidaatkopieën. De werkelijk gemapte kandidaat en gamebestanden zijn niet gepatcht. Geen game-export, echte enginehandler of daadwerkelijke enginecrash uitgevoerd; geen graceful herstel bewezen.

Er zijn **3090 beschermde bestanden** onder OG/AAIP/proef/vaste-start en **120 bestaande H1/H3-pakketbestanden** identiek gebleven. Dit omvat saves en gebruikerswijzigingen. De originele T0-hash blijft gelijk. Dit is geen bewijs dat de volledige engine die T0 met deze kandidaat al heeft geladen: originele payloadcalls zijn in native fixtures stubs. Werkelijke enginehostacceptatie, actuele geladen Theocracy-index3, parser/routing/FLI-activatie en echte T0/save/load/reload in de game blijven runtimepoorten. B2b/B2c, H3-combinatie en gameplaywinst zijn niet toegepast of gemeten.

## Reproduceerbaarheid, herstel en overdracht

[build.py](build.py) gebruikt uitsluitend de bestaande Python312, lokale pefile/Capstone en H1/H3-emitter. [fixture-recipes.py](fixture-recipes.py), [run-native.py](run-native.py) en [helper/Native.cs](helper/Native.cs) hergebruiken de bestaande eigen32-bit-helpermethode; iedere helper heeft maximaal45seconden en CREATE_NO_WINDOW. Alle vier laatste helpers beëindigden normaal, zonder timeout. [verify.py](verify.py) leest kandidaten en controleert onafhankelijke byte/PE/CFG/ABI/resultaathashes en inventories.

Voor reproduceerbaarheid: `py -3.12 PROEVEN/opening-b2/build.py`, daarna `fixture-recipes.py`, `run-native.py` en `verify.py` vanuit projectroot. Een eerste FXsave-registeroperand en het door root gevonden snapshot-EAX-clobber zijn vóór de finale succesvolle bytes gecorrigeerd. De retourfixtures0/1/andere-nonzero testen juist die snapshotfout. Het finale pakketmanifest bindt bron, kandidaten en alle resultaten.

Herstel behoeft nu geen gamebewerking: alleen deze kandidaten zijn gebouwd; de proef-DLL is origineel. De originele input is bovendien aanwezig in [backup/robotcom.original.dll](backup/robotcom.original.dll). Bewaar dit pakket voor rootreview. Indien later afzonderlijk geïnstalleerd, gelden eerst de versie-/installatievoorwaarden van frozen ontwerp en rootvrijgave. Een toekomstig variant-save met inline-record mag niet met de originele DLL geladen worden; baselineherstel gebruikt de ongewijzigde T0.

**Overdracht:** beperkte offline B2a-bouw/checks afgerond, root beoordeelt het concrete pakket. De specifieke offline foutpoort is getest met stubs en originele callerbytes. Geen nieuwe strategie gekozen. Geen installatie, GUI-run, B2b/B2c of algemene projectvoltooiing geclaimd. Voor afhankelijke productie-/gameplayproeven blijft N25/30 een gebruikerskeuze; de runtimepoorten hierboven blijven open.
