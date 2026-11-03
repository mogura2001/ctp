# Vroege wonders: gerichte A-overdracht

27 oktober2026,18:06 CET. Doel4; drie vragen. Alleen bestaande analyse en actuele aidata gelezen. Geen code/build/test/native/RPM/spel/binarywijziging. **A gereed3/3; B kan voorstellen. Doel4 niet volledig AF.**

## 1. Welke effectieve schrijvers moeten worden geraakt?

Actuele werkversie is B1+B2a-N30+B2b ([release](../PROEVEN/doel3/20261012-release-v1/README.md)). B2 levert opening_required en regeringssturing, geen geïnstalleerd compleet gezamenlijk wonder-AIP. `opening_research.aip` en de zeven researchrestore-AIPs ontbreken; B2c bleef voorbereiding. [GEDEELDE-OPENING.md](GEDEELDE-OPENING.md) is historisch voorlopig.

In `CTP-proef/ctp_data/default/aidata/AIPs/` declareren zeven normale bestanden **Wonder_List**: `default.aip`, `cleric.aip`, `slaver.aip`, `scifew.aip`, `scimany.aip`, `milfew.aip`, `milmany.aip`. Barbarian is afzonderlijk en blijft ongemoeid. De acht huidige researchschrijvers zijn deze zeven plus `citywall_science.aip`; onderzoekslijsten vervangen geen wonderlijst. Overige actuele normale AIP-overrides declareren geen Wonder_List.

`aiploader.fli:221–226` laadt persoonlijkheden; tijdelijke modes volgen; citywall_science komt op554. Default/beginturn.fli heeft de oude aiploader uitgecommentarieerd. Daarom default én zes persoonlijkheidsbeginturns meenemen, niet uitsluitend default.aip wijzigen. Zie [AIP-LAADWERKING.md](AIP-LAADWERKING.md): aanwezige Wonder_List vervangt de categorie; ontbreken behoudt de vorige, ook over beurten/save heen.

## 2. Kleinste tekstbestandsroute met herstel

Onderbouwde route: één nieuwe **wonder-only openingspartial** plus zeven wonder-only herstelpartials, telkens met `#include "aipdef.h"`, `Building_Build_List_Element Wonder_List[MAX_ELEMENTS];`, `#DATA`/`#END_DATA`. Openingspartial bevat uitsluitend de echte token **`WONDER_LABRYINTH_OF_THE_MINOTAUR`**, positief gewicht; defaultbrongewicht9100 is een beschikbare B-keuze. Herstelpartials kopiëren exact de volledige eigen bestaande Wonder_List inclusief gewichten/volgorde.

Voeg per normale beginturnroute als laatste acties toe: eigen wonderrestore wanneer `opening_required < 0.5`, openingspartial wanneer `opening_required > 0.5`; bij zes routes ná aiploader, bij default aan het actieve einde. Exacte bestanden: `beginturn.fli`, `beginturnCleric.fli`, `beginturnSlaver.fli`, `beginturnSciFew.fli`, `beginturnSciMany.fli`, `beginturnWarFew.fli`, `beginturnWarMany.fli`. Milfew/milmany horen bij WarFew/WarMany. Alle nieuwe partials moeten vóór manageropbouw beschikbaar zijn; alleen herladen is geen bewezen diskrefresh.

Zo verdringen eerste-beurtpersoonlijkheid en researchoverrides de opening niet, terwijl de latere eigen wonderlijst expliciet terugkomt. Alleen oorspronkelijke lijstentries verwijderen zou ze ook ná de opening verliezen. Gewicht0 of Labyrinth alleen vooraan zetten sluit andere wonders niet uit wanneer Labyrinth onbouwbaar is.

[BOUWDOELEN-EN-QUEUE.md](BOUWDOELEN-EN-QUEUE.md) bewijst eerste geschikte lijstitem, categorieprioriteit, wonderthreshold, harde bouwtijdtoets en herhaalde engine-admission. Behoud die voorwaarden; geen Wonder.txt/technologie-/kosten-/globale beschikbaarheidswijziging. B kiest het openingsgewicht expliciet. Bestaande queued wonderopdrachten worden hiermee niet geannuleerd.

## 3. Kleine meetroute, geen honderdbeurtenvoorwaarde

C controleert later uitsluitend categorydelta/header/routing en behoud van research/units/regering; hergebruik bestaande parser-/switch- en33 bouwdoelcontroles waar passend. Daarna korte passende save: lege stadsqueue, Labyrinth beschikbaar/bouwbaar, eerdere lijstconcurrent eveneens relevant. Eerste acceptatie: effectieve lijst is één Labyrinth-entry en geen ander wonder wordt als nieuwe lijstkandidaat aangeboden. Tweede: echte City Status toont nieuw Labyrinth in productie; lijstkeuze alleen bewijst geen enqueue. Gebruik bestaande editor/City Status-werkwijze of bestaande gebonden observatie waar toereikend; geen nieuw readerframework.

Afzonderlijk controleren: Labyrinth onbouwbaar → geen alternatief wonder; opening_completed → eigen volledige lijst hersteld. Geen vaste T100 nodig. Wonderstadvrijstelling, sneller voltooien, strategische winst en definitieve latewonderlijst blijven open. Werk gestopt na overdracht.
