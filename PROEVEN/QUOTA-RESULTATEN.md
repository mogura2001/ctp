# Eerste quotacontrole: startsettlers

Uitgevoerd op 2 oktober 2026 in CTP-proef. Geen wijziging aan CTP-og of CTP-AAIP.

## Opstelling en waarnemingen

Twee verse editorpartijen, Deity, Gigantic, 8 beschavingen, menselijke speler Romans. Geen n of andere beurtopdracht uitgevoerd vóór telling. AI-speler 2 gekozen; Edit City open gehouden en Screens > UNIT gebruikt. Unit Status toont het aantal per eenheidstype.

| Configuratie | Datum | AI-speler 2 | Settlers | Inwoners |
| --- | --- | --- | ---: | ---: |
| Bestaande proef-AIPs | 4000 BC | Ethiopians, Sheba | 2 | 0 |
| controle-nul | 4000 BC | Naam niet afzonderlijk vastgelegd | 2 | 0 |

Bewijs: automatisering/quota-baseline-start-2settlers.png en automatisering/quota-nul-start-2settlers.png. De kaarten verschillen; geen identieke seed of vaste startscenario gebruikt. Het venster toont geen actieve AIP-naam, dus werkelijk laden van een specifiek profiel is niet afzonderlijk bewezen.

Nulvariant: primaire landsettlerquota 0, primaire klasseprioriteit 30000, core/overflow-quota en klasseprioriteit 0 in de gegenereerde AIP-bestanden. Alle variantbestanden behalve barbarian.aip geïnstalleerd; bestandshashes gecontroleerd. Applicatie vervolgens herstart en een verse partij gestart. DiffDB.txt niet gewijzigd.

De originele Deity-sectie bevat afzonderlijk AI_START_UNITS 2 (regel 518) en EXTRA_SETTLER_CHANCE 1 (regel 535). De namen en waarden zijn vastgesteld; exacte enginebetekenis is nog niet bewezen.

## Voorlopige conclusie

De nulquota verminderde in deze meting het aantal startsettlers niet. Dit ondersteunt de scheiding tussen starttoekenning en AIP-productievraag en pleit tegen de hypothese dat deze quota rechtstreeks het aantal startsettlers bepaalt. Het bewijst niet de betekenis van negatieve quota, afronding, queue-telling of alle mogelijke startinvloeden.

## Uitvoeringsbeperkingen en herstel

Bij aanvang draaide geen proefproces. Een Capture-opdracht mislukte; de daarna bekeken bestaande screenshot was oud en is niet als nieuwe meting gebruikt. Proefkopie gestart. Na variant-herstart was het venster tijdelijk 640x480 met zwart introbeeld; klikopdrachten zijn wegens coördinaten buiten het venster geweigerd. Escape herstelde het hoofdmenu; daarna de verse start uitgevoerd.

Na de meting zijn alle proef-AIPs uit backup-voor-test teruggezet en hashes gecontroleerd. De lopende applicatie is nog gestart met de nulvariant; voor verdere proeven eerst herstarten. Screenshots en backup blijven bewaard.

## Nog uit te voeren

- Controleer zelfstandig AI-gedrag na observeren en hervatten.
- Maak gecontroleerde starts met 2 en 10 AI-steden, voldoende bevolking/productie/vestigingsruimte en identieke uitgangstoestand per variant.
- Meet eerst nulcontrole, daarna -2 en +0.5: huidige productie per stad, aanwezige settlers en veranderingen na stadsstichting.
- Bevestig dat de gewijzigde productieaansturing daadwerkelijk actief is voordat vaste vraag versus vraag per stad wordt geconcludeerd.

## Natuurlijke vergelijking vanaf dezelfde T0-save, 2 oktober 2026

Oorspronkelijke AI en variant alleen-primary-nul zijn elk twintig beurten gevolgd vanaf exact QUOTA-START-T0. Geen kunstmatige steden, bevolking, technologie of AI-queues. Alleen de primary-settlerquota in dertien normale AIPs gewijzigd; overige bytes gecontroleerd. App volledig herstart tussen runs.

| Meetpunt | Oorspronkelijk | Alleen primary nul |
| --- | --- | --- |
| T0 | 0 steden, 2 settlers | 0 steden, 2 settlers |
| T10 | 2 steden, 0 settlers; Cardiff bouwt Settler (9) | 2 steden, 0 settlers; Cardiff bouwt City Wall (7), Swansea Settler (6) |
| T20 | 3 steden, 1 settler; Cardiff Granary (9) | 3 steden, 0 settlers; Cardiff Mounted Archer (4) |

De veranderde bouwkeuze ondersteunt invloed op productie; de betekenis van -2 is hiermee nog niet bewezen. Primary nul blokkeert niet alle settlerbouw. Actieve runtimequota en lijstoverrides zijn niet direct uitgelezen. De baseline bevatte een onsuccesvolle menselijke b/Enter-poging; herhaling daarvan is door automatische goedkeuringscontrole geweigerd wegens mogelijke stadstichting en daarom weggelaten. Beide runs hebben nul menselijke steden, maar begininvoer en observatiemomenten waren niet volledig identiek. Deze beperking maakt een herhaling met identieke passieve bediening wenselijk.

Alle proef-AIPs zijn na afloop hersteld en op hash gelijk aan CTP-og; spel gesloten. Savehash bleef gelijk. Volledige waarnemingen, bewijs en checkpoints: [STARTMANIFEST.md](settlerquota/vaste-start/STARTMANIFEST.md). Het eerdere plan met kunstmatig geplaatste 2/10 steden is vervallen; zie het herschreven SETTLERQUOTA.md.

## Herhaling met dezelfde passieve bediening

De oorspronkelijke AI is nogmaals twintig beurten gevolgd vanaf dezelfde T0-save, zonder b/Enter en met dezelfde observatiemomenten als primary-nul. T10: twee steden, nul losse settlers, Cardiff Settler 9 en Swansea Settler 6. T20: drie steden, één losse settler, Cardiff Granary 9, Swansea Phalanx 1, Pentraeth Phalanx 6. Twee Warriors en één Phalanx aanwezig. Deze metingen komen overeen met de eerdere baseline.

Gebruik deze herhaling als vergelijking met de nulvariant: het verschil in menselijke begininvoer is daarmee weggenomen. Er blijft verschil in productie: twee versus één settleropdracht op T10; één versus nul losse settlers op T20. De precieze formule van negatieve quota en de actieve profiel-/lijstnaam zijn niet direct uitgelezen. Volledig verslag: [HERHALING-PASSIEF.md](settlerquota/vaste-start/HERHALING-PASSIEF.md). Het spel blijft na deze herhaling open op T20, terug bij speler 1, met oorspronkelijke AIPs.

## Extreme primary-quota en stop kleinere runs

-20 en +20 zijn vanaf dezelfde passieve T0-save tot T20 gevolgd. Beide hebben T10: twee steden, nul losse settlers, twee Warriors; Cardiff en Swansea Settler 6. T20: drie steden, een losse settler, twee Warriors; Cardiff en Swansea Settler 4, Pentraeth Phalanx 5. Alle steden grootte 1. De baseline had op T20 hetzelfde aantal steden en losse settlers maar andere bouwopdrachten en een extra Phalanx. De quota verandert dus de waargenomen productie, maar de exacte formule en verdere uitbreiding zijn hiermee niet bewezen.

De gebruiker heeft kleinere proeven gestopt ten gunste van codeonderzoek. -10 bereikte T10 zonder stads-/eenhedenmeting en is onvolledig; +10 en +/-5 zijn niet uitgevoerd. Alle oorspronkelijke proef-AIPs op hash hersteld; proefgame afgesloten; T0-hash ongewijzigd. Zie [reeksresultaten](settlerquota/reeks/RESULTATEN.md) en [uitbreidingsbeslisketen](../ANALYSE/UITBREIDING-BESLISKETEN.md).
