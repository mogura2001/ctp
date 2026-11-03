# Kaartkennisfilter — bronoverdracht voor rootreview

17 oktober 2026, 12:00 Europe/Amsterdam. Uitvoerder heeft uitsluitend bronnen voorbereid in deze nieuwe map. Geen kandidaatbouw, nativecompilatie/nativecall, RPM, installatie, spelstart of gameplaymeting. Deze eigen runtime stopt na de overdracht; geen achtergrondwerk of actieve doelmodus geclaimd. Pcaan.

Basis: onveranderde type10-kandidaat `b6f272d2503edf5f1cf03f927ebd40ff5dd82b1a2c9d9c948beb4e7215baed62`; reader uit reason23-host1. `provenance.json` en `preparation-manifest.json` bewaren exacte historische bronpins; `SOURCE-PINS.json` is het actuele broncheckpoint. Geen science-C2. Baselinebackup blijft Doel3-release `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890`. Alleen eigen map/eigen voortgang geschreven; root bezit PROJECTSTATUS.md.

De compacte review staat in `diffs/`. `prepare_kaartfilter.py` reproduceert de bronkopieën/delta; het script schrijft alleen eigen bronnen en mag niet na een latere bouw/staging blind opnieuw worden uitgevoerd. `input-pins.py` heeft uitsluitend de gepinde bestandsbytes gelezen. `check_sources.py` heeft AST/layout/pins gecontroleerd, zonder emit/compose. Alle broncontroles hieronder zijn afgerond; kandidaatcontrole/runtime blijven open.

| Bestand | Exacte wijziging en begrenzing |
| --- | --- |
| native.py | Plan-DWORDs prefix_count224, known_count228, gate_queries232, gate_false236. Consumer valideert `0<=prefix<=64`, `prefix<=known<=candidates<=4096` (signed vergelijkingketen sluit ook negatieve known/candidates uit). Loopt tot prefix_count; ORDERindex signed>=0 en unsigned<candidates vóór *8. Bron-candidates-cutoff verwijderd; h3calls64guard en overige roles ongewijzigd |
| policy.py | Alleen canonical_prefix gewijzigd: vier counters nul, nodes0 en candidates0..4096 vóór VISITED. Eerst iedere canonical_key, daarna World+28 met originele CAPTUREpointer bewaard op EBP−32. False markeert index−1; true telt known. Zelfde comparator/minimumscan/ties, max64true, prefix_count per store, cutoff bij known>64; nulknownreturn1. Geen CAPTUREcompactering |
| integration_base.py | Alleen bind_host krijgt extra WorldvtableRVA3452e0/slot28==enginebase+133580; mismatch bestaande reason30 |
| input-pins.py/json | Drie volledige A-bodies additief; mismatch bestaande bind_inputs/reason36. Zeven UnitDB-slots en16oude bodies behouden |
| build_candidate.py | Eigen stage/provenance en readerbron/input-pins.json als kandidaatdependencies; bestaand wholefile-diff/PE/rel32/checksum/B2behoudpad behouden. Nog NIET uitgevoerd |
| reader/Lees-Uitbreiding.py | Vier DWORDs in bestaande complete samples; extra loaded Worldslot/bodyranges. Staat moet bij exact nieuwe kandidaat/manifest/state-RVA horen. Unique-H3attributie bij reason23/context1/h3calls1/slots0 en geldige prefixcounters, met `1<=classified<=prefix_count`; classified hoeft niet1 te zijn. Andere slotinterpretaties UNKNOWN. Geen VISITEDlijst uitlezen |
| reader/runtime-pins.json | Kandidaat-/manifesthash/state-RVA bewust null: reader weigert runtime. Na afzonderlijke bouw/rootreview invullen; dan rootgate en pakketpins hiermee binden. Buiten kandidaatmanifest-sources gehouden om een manifesthashcirkel te voorkomen |

`source-checks.json` bevestigt: Python-AST geldig, alle bestaande nativefuncties behalve roles AST-identiek, alle policyfuncties behalve canonical_prefix AST-identiek, alle integrationfuncties behalve host AST-identiek. Alle oude P-offsets en arrays/strides/caps/ORDER/PLAN_SIZE gelijk. Nieuwe velden beslaan224..239; H3HostBinding144..167 en quota168 onaangeroerd; CAPTURE begint512. Het bestaande `m('esi',224)` blijft H3-slotrelatief. START wist nog dezelfde0x54800bytes. Geen engine/H3/B2bronwijziging.

Engine vast op SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp37d6f702/base400000; vtableRVA345308 bevat533580. `gate-body-pins.json` bevat volledige bytes/disassembly/hash en eindinstructies:

| RVA | Lengte | Laatste instructie | Einde exclusief |
| --- | --- | --- | --- |
| 133580 | 37 (25h) | 5335a2 ret8 | 5335a5 |
| bbd50 | 28 (1ch) | 4bbd69 ret4 | 4bbd6c |
| ebdf0 | 115 (73h) | 4ebe60 ret8 | 4ebe63 |

De laatste body gebruikt de door A genoemde inclusieve grens4ebe62, geen gegokte lengte. Geen aangrenzende NOP/volgende functie gepind. De gatecall is push external/push World/call[vtable+28], callee ret8 zonder caller-addESP. Bestaande proloog/epiloog bewaart nonvolatiles; nieuwe code voegt geen x87 toe. EDI overleeft canonical_key en de stdcallgate; externe pointer staat in eigen lokale ruimte buiten callclobbered registers.

Resterende risico's/acceptatie: querytrue is alleen kaartkennis, geen productiecertificaat. Max4096wrappercalls/64H3/64prefix; tijdkosten niet gemeten. Herhaalde interne H2gate kan nog UNKNOWN/reason23 opleveren; andere downstreamfouten blijven zichtbaar. Nulknown geeft alleen helperreturn1, downstream stad/context/vertrekchecks blijven bestaan en kunnen falen. Oorspronkelijke vraag/finale min-maxformule/native queue blijven intact. Geen hogere vraag, H3certificaat, extra stichting of30/40steden bewezen.

Volgende poort: rootreview van deze bronnen/pins/diffs. Daarna afzonderlijke bouwvrijgave, kandidaat/PE/disassembly/branchchecks en nieuwe hashes vastleggen; daarna pas beperkte directe helperfixture uit `CALLER-CONTROLES.md` en afzonderlijke hostvrijgave. Cases a..h zijn ONGETEST; geen volledige oude suite of fixedaddressloader voorbereid. Herstel bron: deze nieuwe map buiten gebruik laten; historische basis intact. Geen geïnstalleerde bestanden of saves gewijzigd.
