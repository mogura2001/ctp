# Doel 3: onderzoek naar Theocracy en regeringswissel

12 oktober 2026, sessie1. **Doel3 opgeleverd en geaccepteerd: gepaarde gameplayverbetering, normale herlaadcontrole en werkversie-installatie bewezen.** Het volledige AI-project is hiermee niet voltooid.

| Op beurt26, zeven normale AI's | Origineel | B1 + B2a-N30 + B2b |
| --- | ---: | ---: |
| Religion bekend | 5/7 | 7/7 |
| Theocracy bekend | 1/7 | 7/7 |
| Actieve Theocracy | 0/7 | 7/7 |

Het is dezelfde gepinde Deity-start QUOTA-START-T0. Alle zeven deelnemers2..8 blijven in de vergelijking; mens en barbaren zijn uitgesloten. Root controleert de gelijke volledige T0-researchlijsten, bekende technologie, huidige research, regeringsvelden, citycount en native ronde. Iedere arm heeft 27 rustige dubbele snapshots en 26 gewone n-passes met voor alle deelnemers precies native+1. Geladen oorspronkelijke/N30-modulebindings zijn daadwerkelijk gecontroleerd. Geen kunstmatige technologie, geplaatste steden, regeringswijzigingen of menselijke gameplayacties. Stadsaantallen per deelnemer zijn gelijk opT26: drie, behalve civ6 met twee.

| Civ-ID | Religion bekend vanaf | Theocracy bekend/aangevraagd vanaf | Theocracy actief vanaf |
| --- | ---: | ---: | ---: |
| 2 | T6 | T13 | T14 |
| 3 | T5 | T16 | T20 |
| 4 | T6 | T23 | T26 |
| 5 | T0 | T10 | T12 |
| 6 | T4 | T12 | T16 |
| 7 | T0 | T12 | T13 |
| 8 | T5 | T20 | T24 |

Iedere variantdeelnemer vraagt regering3 aan op dezelfde beurt waarop Theocracy bekend wordt. De engine voltooit vervolgens de gewone Anarchy-overgang. De twee reeds bijT0 bekende Religion-technologieën worden terecht overgeslagen. Beide runs zijn normaal gesloten, count0 en oorspronkelijke bestandstoestanden hersteld; exitcodes zijn onbekend en worden niet als exit0 gerapporteerd.

## Wijziging en bewijs

De acht B1-onderzoekslijsten zetten Religion/Theocracy vooraan. B2b laat de zes normale persoonlijkheidsroutes tijdens de opening Theocracy verkiezen met Tyranny als terugval. B2a-N30 levert het openingsgeheugen; de gekozen opening eindigt bij30steden plus actieveTheocracy. Zie [uitgewerkt voorstel](../ONTWERP/DOEL3-GAMEPLAYBEWIJS.md). De geaccepteerde N30-DLL is `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890`.

Direct bewijs: [oorspronkelijke varianttrace](../PROEVEN/doel3/20261012T122000/ROOT-VARIANT-TRACE.json) en [onafhankelijke gepaarde roottrace](../PROEVEN/doel3/20261012T165300-baseline2/ROOT-PAIRED-TRACE.json). De tweede trace controleert opnieuw alle oude variant-snapshotsha's en iedere baselinebeurt; 7/7 actieveTheocracy tegenover0/7 op hetzelfde meetpunt.

## Grenzen en resterende oplevering

Dit is één vaste benchmark met zeven AI-beschavingen, aangevuld met statische routecontrole van de gewone research-/persoonlijkheidsregels. Het bewijst geen werking op iedere willekeurige kaart of later spelstadium. Uitbreiding naar30, verdere vestiging tot40, specialisatie, monopoly en oorlogvoering zijn afzonderlijke open doelen. De historische openingslatch is in deze drie-stedenrijken nog niet daadwerkelijk voltooid.

De N30-autosave is exact bewaard met de benodigde DLL-versie. Normaal herladen matcht voor alle zeven exact de oorspronkelijkeT26 op alle acht vooraf gekozen velden; één gewone vervolgbeurt houdt voor iedereen bekende advances en actieveTheocracy. [Root-herlaadreview](../PROEVEN/doel3/20261012T165300-baseline2/ROOT-RELOAD-REVIEW.md) controleert oorspronkelijke/nieuwe savehashes, native+1 en normale afwikkeling.

De geteste versie staat sinds12okt17:31:48 in CTP-proef. Root heeft de19variantbestanden, overige118beschermdewerkpins en alle9bestaandesaves onafhankelijk gecontroleerd. InstallOnly startte geen spel; geen nieuwe runtimeproef nodig voor identieke gameplaybytes. [Werkversie/terugzetten](../PROEVEN/doel3/20261012-release-v1/README.md) en [installatiebewijs](../PROEVEN/doel3/20261012-release-v1/variant/postflight.json). Hiermee is één oorspronkelijk gameplaydoel binnen de eerste van de drie afgesproken werksessies aantoonbaar opgeleverd. Volgende wijziging: uitbreiding/settleraanvraag, met behoud van deze werkversie.
