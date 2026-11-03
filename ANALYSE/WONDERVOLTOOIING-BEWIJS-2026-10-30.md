# Labyrinthvoltooiing: overdracht A naar B

30 oktober2026 13:44CET. Twee vragen afgerond; geen spelstart of wijziging. Doel4: na de bewezen bouwstart werkelijk afbouwen en eigenaar vaststellen.

| Vraag | Voldoende route voor ontwerp | Grens |
| --- | --- | --- |
| Doorslaggevend bewijs | Bestaande Info/Wonder-lijst met wonder, beschaving en stad; eventueel echte voltooiingsmelding | UI-route nog niet in deze proef bediend |
| Begrensd vervolg | Dezelfde9280c97a-save, ongewijzigd30000-pakket, maximaal21 gewone n totaal | Geen voltooiings- of overlevingsgarantie |

## 1. Bestaand voltooiingsbewijs

De lokale gamehelp beschrijft `INFOWINDOW_WONDERBUTTON` expliciet als lijst van wie de wonders bezit en waar ze liggen: [help_str.txt](../CTP-og/ctp_data/english/gamedata/help_str.txt:744). [infoscreen.ldl](../CTP-og/ctp_data/english/uidata/layouts/infoscreen.ldl:243) bevat `InfoWonderList`, kolommen Wonder/Civilization/City en itemvelden WonderName/CivName/CityName. Open Info via Screens/INFO of de vastgelegde sneltoets `^7 OPEN_INFO_SCREEN` (Ctrl+7; [keymap](../CTP-og/ctp_data/default/uidata/keymap.txt:42)), kies de zichtbaar waargenomen Wonder-knop. Geen gegokte coordinaten. Een onbekende of verborgen eigenaar is geen bewezen ongebouwd-status; leg die beperking vast en eis dan een echte voltooiingsmelding. Dit geeft een uitvoerbare observatieroute zonder nieuwe reader.

Aanvullend: [script.slc](../CTP-og/ctp_data/default/gamedata/script.slc:712) definieert `46WonderComplete` en `47WonderComplete`; [info_str.txt](../CTP-og/ctp_data/english/gamedata/info_str.txt:194) onderscheidt voltooid van gestart/bijna klaar. Een daadwerkelijk getoonde melding met Labyrinth en AI-leider bewijst voltooiing; tekstdefinities alleen doen dat niet.

De bestaande completion-disassemblage bewijst vooral kostenvergelijkingen, niet de volledige constructiecommit. Player+1170/+1174 is in bestaande analyses als eigenaarswondermask gebonden, maar de complete writer-/ownershipovergang is hier niet herbewezen. Geen nieuwe memoryprojectie nodig. Global-built-raw, verdwijnen van een queue of WonderBlg-state blijven afzonderlijk onvoldoende.

## 2. Klein vervolg

Verse host, dezelfde archiefsave/eb6/deelnemers/passieve mens en30000-teksten. Leg in de Info/Wonder-lijst eerst vast dat Labyrinth nog geen eigenaar heeft. Herhaal de bewezen eerste beurt: native25 naar26 en nieuwe bouwqueue. Daarna maximaal20 extra normale beurten, dus maximaal21 n totaal/native46. Controleer queue-/beurtvoortgang met de bestaande reader; zodra Labyrinthqueues verdwijnen, of op de eindgrens, inspecteer de Info/Wonder-lijst en eventuele voltooiingsmelding. Vereis een nieuwe Labyrinth-eigenaar/stad tegenover de beginlijst; geen voltooiingsclaim uit queueverdwijning alleen.

Veracruz had16 resterende beurten; dat motiveert deze grens maar voorspelt geen uitkomst. Stop eerder bij voltooiing, menselijke nederlaag, onverwachte dialoog, deadline of budgetgrens. Oude passieve mens verloor rondT48; geen wereldwijziging om langer te kunnen meten. Dit kandidaatvervolg bewijst eventueel voltooiing, geen snellere voltooiing dan9100 of langetermijnwinst. B moet tijd-/herstelgrenzen vastleggen. Geen nieuwe A-blokkade; overdragen.
