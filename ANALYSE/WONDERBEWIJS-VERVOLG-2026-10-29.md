# Wonderbewijs: overdracht A naar B

29 oktober 2026, 14:39 CET. Doel4; drie beslisvragen afgerond als ontwerpinvoer. Alleen bestandslezing en gerichte pefile/Capstone-disassemblage; geen runtimewaarneming, spelstart of wijziging. Adressen hieronder zijn engine-VA, base400000. Engine SHA256 b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79, timestamp37d6f702 opnieuw gecontroleerd; civctp.map niet gebruikt.

| Beslisketen | Dekking | Resterend bewijs |
| --- | --- | --- |
| Effectieve lijst | Runtime AF: controle33/kandidaat1 bij7AI | Onafhankelijke indexidentiteit |
| Tokenbinding | Machinecoderoute AF | Kleine stabiele projectie |
| Werkelijke queue | Layout AF | Nieuwe Labyrinthnode waarnemen |
| Geschikte proefstaat | Inspectiecriteria AF | Savegeschiktheid UNKNOWN |

## V1 — Hoe nativeindex2 onafhankelijk binden?

Parser2005f094–a3 gebruikt actor+4c/virtualslot30. Originele/release-DLL hebben hier dezelfde bytes `8b424c8d559403f38b085250ff5130894608`; huidige release eb6f58a7… volledig gehasht. Bestaand bewijs: [parser](BINAIR/build-goals-queue-ai-list-parser.txt), [interfaceconstructie](BINAIR/terrain-food-engine-interface-binding.txt).

GameState-table744420+30→525fe0→GameState+30; constructor524e2f→532ac0 zet vtable745298 (`c70098527400`). Slot30→5330d0 resolveert exact token via4660f0 en daarna SID→index via454810. WonderDB=`u32(A7DD5C)`: count+0, records+8, strideD0, tokenSID+4; 45482a bevat `81c1d0000000`.

StringDB=`u32(A7DCFC)`, bucketarray+8,547 buckets. Resolver4660fe–127 sommeert tokenbytes inclusief nul met16-bit rotate-left1 en neemt modulo547. Boomnode+0=SID,+4=exacte tokenpointer,+c/+10=kinderen;466171–1b6 volgt strcmp en levert SID. Zoek uitsluitend `WONDER_LABRYINTH_OF_THE_MINOTAUR`, vergelijk SID met WonderDB-record2+4 en eis unieke index. Eenmaal per compleet sample; begrens pointers/naam/visited/count. Node+8 is weergavetekst, geen tokenbewijs. Geen Wonder.txt-volgordebewijs. Native2=Labyrinth blijft tot deze meting OPEN.

## V2 — Welke minimale echte queue-/techprojectie?

[Verzoekroute](BINAIR/build-goals-queue-engine-request.txt): echte stadshandle→pool=`u32(A7DD74)`;4b23a0 zoekt bucket `pool+0xc+4*(handle&1023)`. 4a686d vergelijkt node+0xc met volledige handle; kinderen+4/+8. Gevonden node+58→CityData (4e22e3: `8b4958`). Eis dezelfde eigenaar/stadidentiteit; geen verzonnen handle.

Queue=CityData+450; count+0, head+8, tail+c. Node+4=type,+8=klasse,+10=next; klasse9 en onafhankelijk gebonden index2 bewijzen wonderqueue. Leeg vóór/nietleeg na onderscheiden.4911c0–e4 en490e10–69 bewijzen lezing/schrijving; [admission](BINAIR/build-goals-queue-engine-admission.txt). CityAgent+1f0/+1f4 blijft cache.

**V2-aanvulling14:46 CET, eigenaarpoort AF:** poolnode+18 is civ-eigenaar: getter4da960 resolveert volledige handle via4b23e0→4a68a0 en leest op4da970 `8b4018`. Queuekosten490d87–95 gebruikt dit resultaat als index in PlayerarrayA7DD80.4a68ad–b9 vergelijkt node+c met volledige32-bithandle, kinderen+4/+8; hetzelfde object als lookup4a6860. Eis dus `u32(node+c)==handle` én `i32(node+18)==civ_id` vóór node+58.

CityData+4 is eveneens civ-eigenaar:498cc4 `8b5604` pusht dit als spelerargument naar4745a0;4745da–dd gebruikt het om PlayerarrayA7DD80 te indexeren. Eis `i32(CityData+4)==civ_id`. Stadidentiteit komt uit de volledige handlelookup en de directe node+58-pointer, niet uit een aangenomen extra CityData-IDveld.

Verwar AIcity-ID niet met handle:4c81e5–8220 zoekt AIcity-ID in Player+12c8 (root+8; keynode+0, kinderen+4/+8, payloadpointer+c).5864b6–bd bevestigt volledige keyvergelijking. Payload+0 levert slotindex;4c827f–8291 leest handle uit `u32(u32(Player+12c0)+c)+4*slotindex` en geeft die aan4dc280→4b23a0. Gebruik uitsluitend dit passende playerstadslot, gebonden aan gevalideerdeAIcityset; ontbrekend/ongeldig/mismatch→weigeren. Engine-identiteit opnieuw gelijk gecontroleerd; geen runtime.

Prerequisite-index=WonderRecord+8. Bestaande Doel3-reader leest bekendbyte via Player+12ec→Science+1c;474b60 bevestigt dit.4745a0 vereist prerequisite bekend, wereldnietgebouwd en geen obsolete advance bij enige bestaande speler. Gebouwdveld=`u32(u32(A7A69C)+14)[index]`; obsolete count=record+2c, indexes vanaf+c (464850/60). Configuratie: ShipBuilding, AgeOfReason, kosten2160; geen runtimebezit aangenomen.

## V3 — Welke save eerst inspecteren?

Voorkeur U30-40/host/AUTOSAVE-after SHA9280c97a… boven release-v1/host/AUTOSAVE-after SHA396f8348… wegens menselijke nederlaag rondT48 in laatste bron. Beide restore.json melden exacte opgeslagen beurt UNKNOWN; T26/T47-logs bewijzen die savebeurt niet. T100-saves zijn oudere eilandproeven; geschiktheid eveneens UNKNOWN.

Inspecteer later één bestaande stad: lege echte queue, ShipBuilding bekend, wereldbeschikbaarheid/obsoletevoorwaarden, threshold of opslaguitzondering en bouwtijd≤50/admission; [voorwaarden](BOUWDOELEN-EN-QUEUE.md). Onbouwbaar→geen alternatief en opening_completed→eigen lijst apart meten. Geen savewijziging/100beurtenrun nodig. B kan nu ontwerpen; uitvoering en Doel4-acceptatie blijven OPEN. Werk gestopt.
