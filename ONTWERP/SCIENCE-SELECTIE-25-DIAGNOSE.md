# SELECT25: één gebonden eerstefoutdiagnose

20 oktober 2026, fase B. [A-overdracht](../ANALYSE/SCIENCE-SELECTIE-25.md) door hoofdagent gelezen/geaccepteerd; dit voorstel vereist vóór toepassing dezelfde uitleg en B→C-review. Geen code, bouw, native uitvoering, RPM of spelbediening verricht.

## Beslissing en doel

Doel1/1a/5 vragen bruikbare science-locaties in uitvoerbare vestigingsplannen. Huidige laatste civ8/gen7 bereikt na de bezetcentrumfix selectie, maar de eerste direct_path retourneert0 vóór de puntenlus; cached_path propageert0 en selectie overschrijft reason21 met25. T1 queries1/points0/cutoff0 sluit de alternatieve-indexroute uit. Zestien onderliggende guards blijven ononderscheiden; een concrete implementatiefout is niet bewezen.

Gewenst: dezelfde beslissing en fallback, plus exact de eerste afwijzende guard en haar actuele operands. Bestaande FLI/AIP stuurt quota, prioriteiten en profielen; de bestaande inventaris/AAIP-vergelijking en A tonen geen instelling die vernietigde tijdelijke padoutputs bewaart. Aanvullende eigen diagnostische logica is dus nodig. De gebruikte native padinterface is bewezen in aanwezige bytes, geen algemene modding-hookclaim. Geen extra settlercredit, native0 blijft UNKNOWN.

## Eén kleine ingreep

Nieuw afzonderlijk pakket, uitsluitend afgeleid van `PROEVEN/science-bezet-centrum/20261020T184100`: kandidaat SHA256 `e45313fde4d25a726fa2e8d26dec21c0142ac195ea5c0c40a9b380fd549b166f`, manifest `2077ac8a05d17f6ef7690ceb3a3a9e5555aa8d0f9a23e9e2d9db703288a5396b`. Historische pakketten/release blijven intact.

Kies expliciete state-uitbreiding: record `[0x79804,0x79904)`, 256bytes. Plan blijft `0x79800`; generation blijft `[0x79800,0x79804)`. Header0..511 en scratch `[0x78800,0x79800)` zijn geen vrije opslag: union gebruikt minstens de eerste8bytes, science_layout reserveert4096. Geen onbewezen vrije-restclaim.

`integration_base.start_hook` wist aanvullend alleen dit record bij de bestaande generatiereset. `native.selection` begint een nieuwe finalisatie-invocation, en `source_path` stageert eigen slot-/vertrekidentiteit vóór cached_path. `path_cache` en `path` leggen de werkelijke eigen retouradressen vast. Verifieer onafhankelijk PIC-Plan tegen argument vóór recordwrites; bind scope1/guard0, owner/civ/generation en scratchsnapshot. Bindingfout onderdrukt alleen logging. Per owner/generatie/finalisatie latched uitsluitend de eerste fout; een volgende query kan een gepubliceerde fout niet overschrijven.

Vaste DWORD-indeling, alle offsets recordrelatief:

| Bereik | Inhoud |
| --- | --- |
| 0..19 | valid, schema1, size256, edge-ID, reachedmask |
| 20..35 | owner, generation, civ, onafhankelijke Plan-identiteit |
| 36..63 | drie callsite/return-RVA-paren: finalize→selection, selection→cached, cached→direct; finalisatieordinal |
| 64..95 | queryordinal, slotindex, prefix(Slot+76), role, departureindex, rawID, kind, type |
| 96..111 | eigen externe source8bytes en destination8bytes |
| 112..147 | raw native EAX, capacity, signed count, pointer, berekend pointereinde, boundsbereikt/resultaat, twee canaries, postquerycontext |
| 148..203 | first-entryadres, last-entryadres; first actual/source expected/last actual/destination expected canonical8bytes; vier canonicalreturnwaarden |
| 204..215 | direct-/cached-/selectionreturn |
| 216..255 | gereserveerd0, geen meting |

Reachedmask: bit0 callbinding,1 eigen bron/doel,2 nativecall teruggekeerd,3 postcontext gelezen,4/5 canaryvergelijking,6 rawreturnvergelijking,7 pointerguard,8 minimumcount,9 capaciteit,10 overflow,11/12 first-actual/source-conversie teruggekeerd,13/14 last-actual/destination-conversie teruggekeerd,15/16 first/last DWORDvergelijkingen bereikt,17/18/19 direct/cache/selectiepropagatie. Schema beschrijft dit exact; niet-bereikte velden worden ONBEREIKT. Een nuloutput na nativecall is een waargenomen outputslotwaarde, geen bewijs dat native die schreef. Conversiereturn0 geeft geen geldige canonical key.

Elke afwijzende edge krijgt een eigen landing vóór spillreset/free; IDs volgen deze parent-RVA's:

`1 dc3f8 context; 2 dc408 canary1; 3 dc418 canary2; 4 dc428 nativeEAX; 5 dc436 pointer; 6 dc448 count<1; 7 dc460 count>capacity; 8 dc46b overflow; 9 dc483 first-conversie; 10 dc49e source-conversie; 11 dc4b0 first-DWORD0; 12 dc4c2 first-DWORD4; 13 dc4e9 last-conversie; 14 dc504 destination-conversie; 15 dc516 last-DWORD0; 16 dc528 last-DWORD4`.

Bewaar operands wanneer bestaande code ze leest/produceert, vóór hergebruik van EBP-64/-72, EBP-36 en pointerfree. Neem postcontext uit dezelfde bestaande geheugenread, geen tweede engine-read. Gebruik uitsluitend eigen stack/buffers en bestaande conversieoutputs. First/last externe pathentry-xyz en padding blijven **ongelezen door diagnose**; alleen entryadres en bestaande canonical8bytes worden bewaard. Decoder toont keyxyz en padding afzonderlijk. Geen nieuwe foreign dereference, query of callback. Publiceer valid als laatste, pas nadat direct0→cached0→selectie25 voor dezelfde invocation is bevestigd.

Alle registers inclusief volatile registers, flags, ESP/EBP, x87 en stdcall-ret4/ret12 blijven behouden; logging gebruikt integerstores en eigen opslag. De oorspronkelijke twintig native argumentslots, ret50h, alle criteria/budgetten en eenmaal vrijgeven van iedere nonnull pointer via bestaande cdecl-free blijven exact gelijk.

## Reader, uitvoering en meetlat

Private `reader/Lees-Uitbreiding.py`, `partial_diagnostic.py` en nieuwe recorddecoder binden nieuwe kandidaat/manifest/bronpins, werkelijke state-RVA en exacte state_size`0x79904`. Werk `plan_layout.STATE_SIZE`, eventuele fooddecoder-sizeasserts, positive/partial ownbounds, builder-RW VirtualSize/rawalignment/SizeOfImage, manifest/runtimepins en native allocations/canarygrenzen consequent bij; **niet** PLAN_SIZE of generationoffset verhogen. Leid state-RVA opnieuw af uit gebouwde layout; parent-e3000 is geen nieuw vast adres.

Reader accepteert alleen volledige binding/reachedpropagatie en stabiele geldigheidscontrole rondom recordread; geen atomair-snapshotclaim. ORDER na order_roles heet slotvolgorde plus ongeldige attributierest, zonder prefix→CAPTUREclaims. Prefix komt uit slot; SCI0keys/marges35/30/25 en scope17 blijven afzonderlijke regressiemeetpunten.

Volgorde: (1) uitsluitend bron/diff/layout en beperkte fixturebron ter rootreview; (2) na review tweemaal bouwen, identieke bytes,16landingen/operands/bounds en behoud van ongewijzigde bodies aantonen; adresverschuivingen verklaren; (3) root controleert en draait afzonderlijk toegelaten beperkte nativecases; (4) daarna één host vanaf exact dezelfde vaste Deity-T0, T0-read, precies één `n`, T1-read. Geen nieuwe zwarteboxrun zonder deze telemetry.

Gebruik bestaande first-failure/ABI-infra met enkele gerichte eigen logger-/bindingfixtures: raw native0 versus één endpointguard, normale doorloop, verkeerde/stale binding en latch/reset. Postcontext/canary/pointer/count/overflow krijgen statische operand-/landingcontrole en begrensde eigen recordfixtures, geen volledige natuurlijke padscenario's. Controleer returns/registers/flags/x87/free en buitenrecordcanaries. Alle16landingen krijgen byte-/broncontrole; geen eis alle16guards natuurlijk synthetisch te bereiken, geen oude43/69suite of nieuw raamwerk.

Succes: actuele unieke edge + relevante operands/reachedstatus + volledige ketenbinding; fallback/geen foutcredit behouden. Alleen Gcert0 of native0 zonder context/outputs volstaat niet. Meer selected/desired is geen diagnose-eis. Extra stores/state zijn neveneffecten; corruptie, stale attributie en timing zijn risico's, begrensd door checks. Reader-only kan verdwenen outputs niet herstellen; gokken op ABI/padding/native0 of criteria versoepelen zijn ongefundeerde alternatieven. Combinatie met een latere reparatie krijgt een afzonderlijke proef.

Root beheert één hostpoort, verse29backups, behoud van alle vijf autosavearchieven, normale sluiting/count0 en hashherstel naar geteste Doel3-release; alias verwijderen, livegates FALSE. Bij misbinding of mislukte controle stoppen vóór host. Bij onvoldoende diagnose uitsluitend concrete ontbrekende operand/enginevraag terug naar A, geen brede routeanalyse. Budgetstop bewaart hervatpunt; pc aan.

Dit voltooit na review alleen SELECT25-B. Technische en hostacceptatie zijn nog OPEN; oorspronkelijke Doel1/1a/5 blijven OPEN en Doel3 AF.
