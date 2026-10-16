# C1 native fixture attempt8 — gestopt voor rootreview

2026-10-14 15:59 Europe/Amsterdam. Ownership uitsluitend deze map. Deze werkperiode voerde één begrensde native helperstart uit; geen game/GUI/RPM/installatie, sciencecredit of union. C1 nativeacceptatie blijft gedeeltelijk.

De door root aangewezen fixturefout is toegepast en offline gecontroleerd: `prepare_native_fixtures.py` herlaadt na `r.zero(m('ebp',20),40)` de uitvoerpointer met `r.mov('edi',m('ebp',20))`. In `fixture-large-center-reader.bin` is op offset31 exact `8b bd 14 00 00 00` toegevoegd (89→95 bytes); alle overige bytes en andere callbackpins zijn gelijk. Oud SHA256 `13ec5eed57865fd0e228652e69b80998b8b001366edf1a5d85ba58b163a8d523`, nieuw `c91f08224232e75b354bb8957d5f7dc314aad69af1d3586ae63b70bccca76dd2`. Oude bron/fixture/pins/CS/wrapper/exe zijn bewaard als `*.before-attempt8`; bron-diffs en native-attempt8-preparation-audit.json geven exacte wijzigingen. Herstel: deze zes bewaarde bestanden naar hun oorspronkelijke eigen namen kopiëren; kandidaat/gamebestanden behoeven geen herstel.

Wegens attempt7 error487 op00530000 is in de bestaande compiledwrapper één finite setupcorrectie voorbereid en door root gereviewd: exact zeven benodigde eigen64KiBblokken00400000/00490000/00510000/00520000/00530000/00740000/00a70000 vóór serializer/loader/imageallocatie reserveren, set en eigenaarschap in Run controleren, failure/finallycleanup. Geen ASLRretry, unmap, echte hostpatch of SCI/Hostguardomzeiling. Bestaande PS-entry blijft ondersteund; deze poging gebruikte uitsluitend `native-fixtures.attempt8.exe`, SHA256 `a72200e1a0e9917a9e398c132c492a681ea45d2887e9fac846d06a59c4da696e`. Eerste compilecommand met slashpaths faalde CS1504; compilatie in eigen map slaagde. Dit waren compilaties, geen native modelcalls.

Root gaf precies één attempt8 vrij. Verse budgetbron13:56:45.847UTC/leeftijd8.4s: vijf88/week49/stateok. Werkelijke helperPID8736, 32bit, start13:57:17.2985624UTC, eind13:57:17.4464749UTC, HasExited=true/binnen30s. OS ExitCode is **null/onbekend**; wrappercatch bewaart pass=false, geen exit0/1 als gemeten claim. Native-attempt8-process.json/stdout/stderr/native-attempt8.json zijn het bewijs.

**Resultaat: vroege eigenreservatie faalt op00400000 met Windows error487. Nul nativecalls, nul voltooide cases, nul dispatchpatches.** De complete30-case SCI-reeks, inclusief gecorrigeerde centrum>2^31 en volledige ESP/nonvolatile/x87/canarycontrole, is hierdoor in attempt8 niet bereikt. Geen tweede start/retry. De eigen helper-PE heeft preferredImageBase00400000 en DLLCharacteristics8540/DYNAMICBASE=true; dit ondersteunt een mogelijke loader-/adresbotsing, maar bewijst de werkelijk bezette module op het faalmoment niet. Geen geheugenmapping/unmap van echte host gedaan. Terug naar root/ontwerper voor concrete eindige fixtureadresoplossing; geen vervangende strategie uitgevoerd.

`native-attempt8-final-checks.json` en `native-attempt8-decoded-results.json` leggen de failure zonder fictieve parity-PASS vast: nativepass=false, decoderparity=null wegens0savedcalls, lege decodedlijst. De reviewfrozen science_result.py/model/candidate zijn ongewijzigd. Coverage0-parityNone en only-valid-future zijn daardoor behouden, maar leveren geen nieuwe runtimecase op.

| Meetlat | Huidige status/bewijs |
| --- | --- |
| Fixturepointer correct/herstelbaar | Toegepast en offline exactbytegecontroleerd; runtime-effect nog open |
| Candidate/SCI/Host/H3-behoud | CandidateSHA `622cdd87c7b9480e9740ca5baaf37190ed632852358db0f80f6b6b936b13d6ba` gelijk; oorspronkelijke21packagepins gelijk |
| Beschermde release/saves/profiel/dependencies | Alle29beschermdebestanden en4dependencies actueel hashgelijk |
| Historische attempts1..7 | Alle21bestaande result/logbestanden hashgelijk; geen overschrijving |
| Sciencegevallen/ABI | Attempt6 behield29completecases van30calls; laatste geïsoleerdecentrumcase faalde x87 doorfixturebug. Attempt8 voegt0call/0case toe; gecorrigeerde suite nog niet geaccepteerd |
| Querytellers | Attempt8 geen queries. Attempt6 max20case mat spatial20/primary+developmentfood41/available20/position20/delta20; dit zijn gecontroleerde callbacks, geen echte enginequeries |
| Echte World/host/gameplay | Onbewezen; geen echte enginequery of gameplayverbetering geclaimd |

Uitvoerderscounters deze werkperiode:1helperstart,0nativecalls,0completecases,0fixturedispatchpatches,0gamewrites,0RPM,0GUI,0installaties/starts van CTP. Sciencecredit=false/union=false; actievePlan0x54800 behouden. Synthetische enginepincontext en gecontroleerde dispatch blijven eerlijk als fixtures gelabeld.

Werk gestopt; helperPID8736 is bij15:58:31Europe/Amsterdam afwezig in Get-Process. Geen actieve helper/run of planning achtergelaten. Eerstvolgende oplevering: rootreview van deze failure en een expliciet afgebakende fixtureadresoplossing; daarna pas afzonderlijk één nieuwe proefvrijgave. Laatste budgetbron13:57:37.711UTC/leeftijd18.9s/vijf87/week49/stateok. Pc blijft aan; geen afsluithelper/commando/planning.
