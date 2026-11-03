# Landtest: menselijke nederlaag blokkeert T100

27 oktober 2026,17:19 CET. Gerichte fase A, uitsluitend bestaande lokale CTP-I-documentatie, UI-layouts en configuratie gelezen. Geen spel/RPM/UI/installatie/binarywijziging. Opdracht afgerond en gestopt.

**Geen reeds bewezen neutrale observer- of beschermingsoptie gevonden die doorspelen na menselijke eliminatie garandeert.** Wel bestaat een concreet maar onbeproefd GUI-aanknopingspunt: Close op het nederlaagscherm, daarna mogelijk Continue op het highscorevenster. De layouts bewijzen de knoppen, niet dat de overgebleven AI's na menselijke eliminatie verder kunnen spelen.

## Feit en bewijsgrens

Root rapporteert geldige T0..47; de verbruikte T48-invoer kreeg geen +1 binnen30s. [T48-stop.png](../PROEVEN/landvergelijking/20261027/release-v1/host/T48-stop.png) toont DEFEAT, menselijke steden0/populatie0 en Turns47. Dit ondersteunt een eindspelstop, **geen hangclaim**. Het verlies van de onbeschermde menselijke settler is de verklaring van root; de precieze dader/verliesgebeurtenis is hier niet afzonderlijk vastgesteld. Kandidaatarm niet gestart; root beheert herstel.

## Gerichte lokale controle

- [victoryscreen.ldl:229](../CTP-og/ctp_data/english/uidata/layouts/victoryscreen.ldl:229): VictoryWindow.OkButton gebruikt `str_ldl_Close`. [Regel552](../CTP-og/ctp_data/english/uidata/layouts/victoryscreen.ldl:552): HighScoreWindowPopup.ContinueButton gebruikt `str_ldl_CONTINUE`. De proefkopie bevat dezelfde knopnamen. Geen bewijs van hun callbackgedrag na eliminatie; Continue kan ook de volgende eindspelstap openen. Niet als werkende spectatorfunctie presenteren.
- [readme.doc:718](../CTP-og/help/readme.doc:718) documenteert doorspelen wanneer iemand het **Alien Endgame** wint. [info_str.txt:157](../CTP-og/ctp_data/english/gamedata/info_str.txt:157) noemt doorgaan na3000AD zonder score. Geen van beide beschrijft doorgaan met een uitgeroeide menselijke speler.
- `str_ldl_CONTINUE_GAME` hoort in [spnewgame.ldl:230](../CTP-og/ctp_data/english/uidata/layouts/spnewgame.ldl:230) bij het Single Player-startvenster. De tekst bewijst geen nederlaagoverride.
- [readme.doc:868](../CTP-og/help/readme.doc:868) beschrijft `/attach <player#>` als AI-overname van een Hotseat-speler; `/detach` geeft de omgekeerde overname. Dit verandert besturing en is geen neutrale singleplayerobserverroute.
- `NoHumansOnHost`, `AiOn`, `GameWatchDirectory` en `AlienEndGame` komen in profielbestanden voor. Geen gevonden documentatie bindt die aan menselijke onkwetsbaarheid of doorgaan na eliminatie. Niet op basis van namen omschakelen. De editorhandleiding biedt Show Map en spelerselectie, maar geen gedocumenteerde bescherming tegen verlies.

## Kleinste vervolgbeslissing

**Geen tweede lange arm vanaf dezelfde onbeschermde start starten.** Als de verloren toestand weer beschikbaar is, kan een afzonderlijke korte GUI-verificatie uitsluitend Close/Continue beoordelen; pas echte verdere native rondestappen bewijzen doorspelen. Die verificatie is hier niet uitgevoerd of als werkende route aangenomen.

Zonder zo'n bevestiging moet B één expliciet overlevingsprotocol voor de mens in een **afzonderlijke benchmarkclone** voordragen, bijvoorbeeld bescherming/verplaatsing van bestaande menselijke startunits of een beschermde menselijke vestiging. Root/gebruiker kiest de concrete afwijking vóór uitvoering; deze notitie plaatst of wijzigt niets.

Dat introduceert confounds: andere menselijke locaties/zichtbaarheid beïnvloeden contact, routes en AI-doelen; een stad verandert grondclaims, economie, handel en dreiging; extra verdediging of afzondering verandert militaire afwegingen en beschikbare ruimte. Globale vrede, geen barbaren of AI-overname zouden nog bredere gedragswijzigingen zijn. Daarom beide armen vanaf exact dezelfde nieuwe clone/herkomsthash, identiek passief protocol en eerst een overlevingscontrole totT100. Oude T0..47 blijven uitsluitend bewijs van de oorspronkelijke start; niet als eerste helft van het nieuwe paar combineren.

Laatste verse budgetbron16:16:09UTC: vijfuur63%/week72% resterend. Geen achtergrondwerk; pc blijft aan.
