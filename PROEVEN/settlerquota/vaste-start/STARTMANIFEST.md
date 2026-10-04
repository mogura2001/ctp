# Vaste start voor de natuurlijke quotaproef

Laatste uitvoering: de varianten primary -20 en +20 zijn tot T20 voltooid vanaf deze start. Kleinere varianten zijn op verzoek gestopt (-10 onvolledig, +10/±5 niet uitgevoerd). Proef-AIPs hersteld, spel afgesloten. Zie [reeksresultaten](../reeks/RESULTATEN.md) en [uitbreidingsbeslisketen](../../../ANALYSE/UITBREIDING-BESLISKETEN.md).

- Spel: CTP I, CTP-proef, Deity, Gigantic, 8 spelers.
- Startsave: QUOTA-START-T0.sav, 4000 BC, vóór de eerste beurt.
- SHA256: 8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26.
- AI-speler 2: Arawn, Welsh. Na laden twee settlers; nog geen steden.
- Opslaan en terugladen via het spel zijn gecontroleerd. Bewijs: ai-T0-na-laden.png.
- Alle proef-AIPs zijn bij aanvang hersteld en op hash gelijk aan CTP-og.
- De eerdere SLIC-queueproef is uitgeschakeld.

## Uitvoering en beperkingen

Dit vervangt de eerdere opstelling met kunstmatig geplaatste steden. Geen steden plaatsen, bevolking veranderen of AI-bouwopdrachten geven. Varianten moeten telkens deze exacte startsave gebruiken. Alleen de onderzochte quota wijzigen; prioriteiten en overige settlerklassen behouden. Herstart voor iedere variant. Of een geladen save de gewijzigde AIP-aansturing gebruikt, moet afzonderlijk worden vastgesteld.

De menselijke settler is na de eerste beurt nog aanwezig, zonder menselijke stad. Een poging met b/Enter heeft geen stad gesticht; daarom telt deze niet als geslaagde actie. Voor de lopende baseline blijft de menselijke speler passief. Een herhaling moet dezelfde menselijke acties gebruiken, of beide runs opnieuw vanaf T0 uitvoeren met een expliciet vastgelegde passieve bediening.

## Waarnemingen oorspronkelijke AI

| Beurt vanaf save | Datum | AI-steden | Settlers | Huidige productie |
| --- | --- | ---: | ---: | --- |
| 0 | 4000 BC | 0 | 2 | Geen steden |
| 1 | 3950 BC | 0 | 2 | CITY meldt dat eerst een stad nodig is |
| 5 | 3750 BC | 1 | 1 | Cardiff grootte 1, Warrior, resterend 3 beurten; 1 Warrior aanwezig |
| 10 | 3500 BC | 2 | 0 | Cardiff grootte 1, Settler, resterend 9 beurten; 2 Warriors en 1 Phalanx aanwezig. Swansea-productie nog niet uitgelezen. |
| 20 | 3000 BC | 3 | 1 | Alle steden grootte 1. Cardiff: Granary 9; Swansea: Phalanx 1; Pentraeth: Phalanx 6. Twee Warriors en één Phalanx aanwezig. |

Baseline gecontroleerd tot twintig beurten. Checkpoints T5, T10, T15 en T20 bewaard. T15 is alleen een checkpoint, geen volledige stads-/unittelling. De savehash van T0 blijft gelijk. De AI heeft na observatie zelfstandig verder gebouwd en gesticht.

## Variant alleen-primary-nul

In dertien normale AIPs is uitsluitend UNIT_SETTLER in Land_Settler_Troops_Primary op 0 gezet. Overige bytes zijn tegen de originele bestanden gecontroleerd. Core, overflow, prioriteiten en barbarenbestand behouden. Bestanden en wijzigingslijst: ../alleen-primary-nul/.

Het spel is volledig herstart en dezelfde T0-save geladen. De menselijke b/Enter-invoer uit de baseline is niet herhaald: automatische goedkeuringscontrole wees die af wegens mogelijke stadstichting. Beide runs houden nul menselijke steden; het verschil in invoer blijft een beperking. Ook observatiemomenten zijn niet volledig identiek: de variant heeft checkpoints op T5 maar geen volledige telling op dat moment.

| Beurt | Datum | Steden | Settlers | Huidige productie |
| --- | --- | ---: | ---: | --- |
| 0 | 4000 BC | 0 | 2 | Geen steden |
| 10 | 3500 BC | 2 | 0 | Cardiff grootte 1: City Wall 7; Swansea grootte 1: Settler 6. Twee Warriors en één Phalanx aanwezig. |
| 20 | 3000 BC | 3 | 0 | Alle steden grootte 1. Cardiff: Mounted Archer 4; Swansea: Phalanx 1; Pentraeth: productieveld leeg. Twee Warriors en twee Phalanxes aanwezig. |

Op T10 verschilt Cardiff van de baseline (Settler 9 versus City Wall 7). Dat ondersteunt invloed op latere productie, maar is nog geen bewijs voor de precieze betekenis van negatieve quota. De variant bouwt nog steeds een settler in Swansea; nul in primary is dus geen totale blokkade van settlerproductie.

## Eindvergelijking en status

Beide runs hebben na twintig beurten drie steden. Baseline heeft één losse settler, primary-nul geen. De bestaande AI heeft zelfstandig steden gesticht en bouwopdrachten gekozen; geen steden of AI-queues zijn handmatig geplaatst. Het verschil in productie ondersteunt de hypothese dat primary-quota productieaansturing beïnvloedt. Het bewijst niet dat -2 exact twee gelijktijdige settlers vraagt, noch welke concurrerende settlerklasse Swansea heeft aangestuurd.

Een directe uitlezing van het runtimequotum of actieve AIP ontbreekt. Herstart, gecontroleerde bestandsverschillen en gedragsverschillen ondersteunen dat de variant invloed heeft, maar vervangen geen directe bevestiging van het laad-/overridegedrag. De afwijkende menselijke begininvoer en observatiemomenten zijn extra beperkingen; voor een sterkere causale conclusie is een herhaalde baseline met dezelfde passieve bediening zinvol.

Na afloop is CTP-proef gesloten. Alle proef-AIPs zijn hersteld en hun hashes gelijk bevonden aan CTP-og. De T0-savehash is ongewijzigd. Varianten, tussensaves en screenshots blijven bewaard. Eerst laad-/overridegedrag en herhaalbaarheid verder controleren; pas daarna negatieve quota als bewezen aantallen behandelen.

Een ontbrekende stad na één beurt is geen quota-uitkomst. Eerst natuurlijke stichting en productie volgen. De gewenste meetduur is circa twintig beurten. Vergelijk daarna met een variant vanaf dezelfde save en trek alleen conclusies waarvoor de actieve configuratie en observaties voldoende bewijs geven.

## Actualisatie: passieve baseline herhaald
De baseline is volledig herhaald met dezelfde passieve bediening en observatiemomenten als primary-nul. De T10/T20-metingen zijn gereproduceerd. Gebruik deze herhaling voor de vergelijking; zie [HERHALING-PASSIEF.md](HERHALING-PASSIEF.md). Het verschil in oorspronkelijke b/Enter-invoer geldt niet voor dit vergelijkingspaar. De interne quotabetekenis blijft onbewezen.

