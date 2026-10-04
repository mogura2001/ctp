# Reeks primary-settlerquota ±20, eventueel ±10 en ±5

**T60-vervolg voltooid:** alle zeven AI-beschavingen vergeleken in [VERGELIJKING-T60.md](VERGELIJKING-T60.md), met [METINGEN-T60.csv](METINGEN-T60.csv) en screenshots. Baseline: 49 steden, 104 stadsbevolking, 3 settlers. -20/+20: beide 66 steden en 124 stadsbevolking, maar 71/78 settlers. De onderstaande T10/T20-waarnemingen en overdrachten blijven historische resultaten; de langere proef toont wel degelijk verschillen in uitbreiding.

Elke run gebruikt QUOTA-START-T0.sav, SHA256 8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26. Deity, speler 2 Arawn/Welsh; menselijke speler blijft passief. Volledige herstart per variant. Alleen UNIT_SETTLER in Land_Settler_Troops_Primary van de dertien normale AIPs wordt gewijzigd. Core, overflow, prioriteiten en barbarian.aip blijven oorspronkelijk. Geen steden, bevolking, technologie of AI-bouwopdrachten handmatig gewijzigd.

Quotareeks.ps1 voert afzonderlijke bedieningsstappen uit; de waargenomen schermen en speldata bepalen of een stap is geslaagd. Per variant worden gewijzigde AIPs, wijzigingen.csv, screenshots en autosave-checkpoints op T10/T20 bewaard. De getallen achter bouwopdrachten zijn resterende beurten.

| Variant | Beurt | Steden | Losse settlers | Overige eenheden | Bouwopdrachten (alle steden grootte 1) |
| --- | ---: | ---: | ---: | --- | --- |
| Origineel, passieve herhaling | 10 | 2 | 0 | 2 Warriors, 1 Phalanx | Cardiff Settler 9; Swansea Settler 6 |
| Origineel, passieve herhaling | 20 | 3 | 1 | 2 Warriors, 1 Phalanx | Cardiff Granary 9; Swansea Phalanx 1; Pentraeth Phalanx 6 |
| -20 | 0 | 0 | 2 | Geen | Geen steden |
| -20 | 10 | 2 | 0 | 2 Warriors | Cardiff Settler 6; Swansea Settler 6 |
| -20 | 20 | 3 | 1 | 2 Warriors | Cardiff Settler 4; Swansea Settler 4; Pentraeth Phalanx 5 |
| +20 | 0 | 0 | 2 | Geen | Geen steden |
| +20 | 10 | 2 | 0 | 2 Warriors | Cardiff Settler 6; Swansea Settler 6 |
| +20 | 20 | 3 | 1 | 2 Warriors | Cardiff Settler 4; Swansea Settler 4; Pentraeth Phalanx 5 |

## Voorlopige waarneming

-20 verandert de productie ten opzichte van de baseline: op T10 ontbreken de extra Phalanx en drie resterende bouwbeurten in Cardiff; op T20 blijven twee steden settlers bouwen. Het aantal gestichte steden en losse settlers is op T20 gelijk aan de baseline. Dit bewijst nog geen precieze formule of einddoel van de quota. De actieve AIP/lijst en intern geladen quota worden niet rechtstreeks uitgelezen. Gelijk startaantal in deze geladen-saveproef bepaalt niet hoe een nieuwe wereld zijn starteenheden aanmaakt.

De +20-run is op T10 gelijk aan -20 voor de gemeten steden, grootte, productie en eenheden. Dit zegt nog niet dat beide tekens dezelfde betekenis hebben: een grote vaste vraag en een grote vraag per stad kunnen beide meer settlers vragen dan er beschikbaar zijn. Kleinere waarden kunnen een grens zichtbaar maken; een langere natuurlijke run kan eveneens nodig zijn.

Voor min20 en plus20 zijn de dertien bewaarde variantbestanden onafhankelijk gecontroleerd: buiten de inhoud van het primary-blok gelijk aan oorspronkelijk; binnen het blok alleen de numerieke UNIT_SETTLER-waarde gewijzigd. T0-savehash ongewijzigd. Beide runs zijn tot T20 voltooid en gelijk voor de gemeten variabelen.

## Stop van kleinere runs op verzoek

De gebruiker heeft tijdens -10 gevraagd de kleinere runs te stoppen en eerst de beslisketen voor aantallen en locaties te onderzoeken. -10 bereikte T10/3500 BC, maar er is geen City/Unit Status-meting op T10 uitgevoerd: deze run is onvolledig en telt niet mee als vergelijkingsresultaat. +10 en ±5 zijn niet uitgevoerd. De oorspronkelijke proef-AIPs zijn allemaal hersteld en op SHA256 gelijk aan CTP-og gecontroleerd; de proefgame is afgesloten zodat geen variant in het geheugen blijft draaien. Onderzoek en resultaten blijven bewaard.

## Overdracht voor handmatige T60-proef

Op verzoek primary -20 opnieuw geïnstalleerd in de dertien normale proef-AIPs en CTP-proef volledig gestart. De vaste T0-save is onder Julius/QUOTA-START-T0 beschikbaar; hash bij installatie gecontroleerd. De gebruiker laadt zelf T0 en speelt passief tot T60, met een afzonderlijke save. Geen beurt door de assistent gespeeld bij deze overdracht. CTP-proef blijft voor deze proef op -20 staan; de eerdere herstelstatus betreft de vorige afsluiting.

## Handmatige -20-save ontvangen; overdracht +20

De gebruiker meldt de -20-run tot T60 voltooid. Bestand Julius/quota--20-T60 (451882 bytes) is ongewijzigd gekopieerd naar min20/T60-gebruiker.sav; beide SHA256 3A15D526950A7ABF0DE3874E477F555667E34250F770415928898638AE99F547. Beurt en spelmetingen zijn nog niet uit de save gecontroleerd.

Meetbeschaving voor de T60-vergelijking wordt op verzoek Egyptians: volgens de gebruiker heeft Welsh te weinig uitbreidingsruimte op zijn kleine eiland. De eerdere Welsh-metingen blijven historische waarnemingen en worden niet rechtstreeks vergeleken met Egyptische tellingen. Vergelijk Egyptians tussen -20, +20 en oorspronkelijke baseline vanaf dezelfde T0-save.

+20 geïnstalleerd (uitsluitend primary in dertien normale AIPs) en proefgame volledig herstart. Gebruiker laadt zelf QUOTA-START-T0 en maakt een afzonderlijke +20-T60-save; assistent speelt geen beurten. De proefbestanden blijven voor deze run op +20 staan.

## +20-save ontvangen; standaardbaseline voor T60 klaargezet

Gebruiker meldt +20 tot T60 voltooid en ziet zelf weinig verschil; nog geen gecontroleerde Egyptische metingen. Julius/quota-+20-T60 (452102 bytes) gekopieerd naar plus20/T60-gebruiker.sav. Bron en kopie SHA256 4DD0984913D3DE5376E7BDDDF8FB47796F427E3FD643804EFED29C302A1DB7D3.

Op verzoek alle oorspronkelijke AIPs hersteld en op hash gelijk aan CTP-og gecontroleerd. Geen uniforme quota ingesteld: de baseline gebruikt alle originele profielwaarden (masssettle primary -2), inclusief oorspronkelijke core/overflow/prioriteiten. Proefgame afgesloten voor herstel en daarna volledig opnieuw gestart. Vaste T0-save opnieuw beschikbaar gemaakt met gecontroleerde oorspronkelijke hash. Gebruiker laadt zelf T0 en speelt passief tot T60 voor vergelijking van Egyptians. De proefbestanden staan nu op standaard; eerdere -20/+20-overdrachten zijn historische status.
