# AI-steden en huidige productie bekijken

Gecontroleerd in CTP I op Deity, 2 oktober 2026. Gebruik uitsluitend CTP-proef en de bediening uit AUTOMATISERING.md.

## Werkwijze

1. Open Options met Escape en kies Cheat Mode.
2. Selecteer de gewenste beschaving met min en plus bij Player. Controleer naam en spelernummer; de laatste selectie kan bewaard zijn.
3. Open Edit City en laat dit paneel open staan.
4. Open rechts het Screens-menu en kies CITY. In de Turkse proef selecteerde en centreerde City Status automatisch Ankara, zonder voorafgaande kaartklik. Indien nodig kun je met Edit City open eerst een stad van de gekozen beschaving op de kaart aanklikken.
5. Lees het totale aantal steden en per stad de naam, grootte, huidige productie en resterende bouwtijd. Leg beurt en screenshot vast. Bij meer steden moeten alle rijen worden bekeken; dit is nog niet getest.
6. Voor een andere beschaving: sluit eerst City Status en Edit City, selecteer de volgende Player en herhaal vanaf stap 3.

Klik voor observatie niet op Build, Make Queue, Load Queue, Rush Buy of Disband en wijzig geen stadsnaam of grootte. Rush Buy is volgens de handleiding gratis terwijl Edit City open is en zou de meting veranderen.

Gebruik Bedien-CTP.ps1 en controleer het scherm na acties. De interne cursor kan bij focuswisselingen verspringen. FromX/FromY moeten de werkelijk waargenomen cursorpositie beschrijven. ResetCursor kan de kaart scrollen. Coördinaten kunnen bij andere vensterbounds of beeldschaling verschillen.

## Gecontroleerde waarnemingen

| Beschaving | Beurt | Steden | Stad | Grootte | Productie | Resterende beurten |
| --- | ---: | ---: | --- | ---: | --- | ---: |
| Nederlanders | 3 | 1 | Amsterdam | 1 | Warrior | 2 |
| Turken, speler 2 | 3 | 1 | Ankara | 1 | Warrior | 4 |

Bewijs: automatisering/ai-amsterdam-turn3.png en automatisering/ai-turken-turn3.png. Amsterdam is door de gebruiker geselecteerd; City Status is daarna zelfstandig gesloten en heropend. De Turkse observatie is zelfstandig vanaf gesloten panelen uitgevoerd.

Dit toont toegang tot huidige productie, niet tot de volledige toekomstige bouwqueue. Behoud van zelfstandige AI-productiekeuzes na observatie moet nog worden gecontroleerd door terugkeer naar de menselijke speler, beurtvoortgang en een nieuwe observatie van dezelfde AI-stad.

## Wat we geleerd hebben

- AI-steden zijn via de bestaande editor toegankelijk. De eerdere mislukte pogingen bewezen geen beperking van het spel.
- Selecteer eerst de beschaving en open vervolgens Edit City. Houd dit open tijdens stadsobservatie; City Status kan daarna via Screens > CITY worden geopend.
- In de Turkse proef was geen voorafgaande kaartklik nodig: het overzicht selecteerde Ankara automatisch.
- Het overzicht maakt stedental, stadsgrootte, huidige bouwkeuze en resterende bouwtijd zichtbaar. Daardoor kunnen we settlerbouw direct registreren in plaats van uitsluitend gestichte steden te tellen.
- Huidige productie is niet hetzelfde als een volledige toekomstige queue of een bewezen productiequota.
- Zelfstandige AI-aansturing na observatie, observatie van meerdere steden en algemene muisbetrouwbaarheid zijn nog niet bewezen.

## Volgende controle: settlerquota

Controleer eerst dat Ankara na hervatten zelfstandig productie verwerkt en keuzes blijft maken. Maak daarna de gecontroleerde starts met 2 en 10 AI-steden uit SETTLERQUOTA.md. Er is nog geen quotavariant geïnstalleerd of quotabetekenis bewezen.

## Actualisatie: natuurlijke proef
Het hierboven genoemde vervolg met kunstmatig geplaatste 2/10 steden is vervallen. Gebruik het herziene SETTLERQUOTA.md. In de natuurlijke proef is zelfstandige AI-productie en stichting na observatie gevolgd tot twintig beurten. City Status kan met Drag aan de titelbalk naast de editor worden gezet; alle drie stadsrijen zijn daarbij gelezen. Resultaten: settlerquota/vaste-start/STARTMANIFEST.md.

