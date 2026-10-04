# Windows-bediening van CTP

`Bedien-CTP.ps1` biedt Start, Status, Capture, Key, Click en DismissError. Het script bedient uitsluitend de executable in `CTP-proef`; voor invoer controleert het vensterfocus. Start opent bewust een zichtbaar spelvenster, omdat deze proef interactieve bediening onderzoekt.

Windows-GUI-toegang moet in deze sessie buiten de sandbox worden uitgevoerd. Binnen de sandbox zijn procesgegevens zichtbaar, maar waren de interactieve vensterhandles niet beschikbaar.

## Gecontroleerd in het spel

- Proefkopie gestart en hoofdmenu vastgelegd.
- Met muisinvoer naar Single Player en New Game gegaan.
- Deity geselecteerd gezien en een nieuwe partij gestart.
- Via toets `b` Rome gesticht en stadsnaam via Enter bevestigd.
- Via `n` beurt doorlopen: 4000 BC naar 3950 BC, met autosave.
- Een normale melding over een lege stadsqueue geopend.
- Een SLIC-runtimefoutvenster geïdentificeerd en de tekst via Windows uitgelezen.

Screenshot: `automatisering/ctp-window.png`. Vroege save bewaard als `automatisering/start-3950BC.sav`. Dit is een technische proefsave, nog geen overeengekomen benchmark.

## Bevindingen en beperkingen

Het spel gebruikt een eigen cursor. SetCursorPos alleen werkte niet betrouwbaar; relatieve mouse_event-invoer gaf een zichtbare menuovergang. DPI-awareness en een korte ingedrukte muisklik zijn ingesteld. Fullscreen/focuswisselingen kunnen zwarte opnames en verschuivende windowbounds geven. Inspecteer het resultaat na iedere actie; blind vaste coördinaten herhalen is niet betrouwbaar. Een inputcommando dat succesvol eindigt bewijst niet dat de gewenste spelactie plaatsvond.

De SLIC-proef liep bij de tweede beurt tegen deze fout aan: `In object AIQP_PlayerTurn, function _HasAdvance: Wrong type of argument`. In de proef stond een geciteerde technologienaam. De lokale tutorial gebruikt een string-ID, dus dit is in het bestand gewijzigd naar `ID_ADVANCE_AGRICULTURE`. Deze correctie moet nog na opnieuw laden van het script in een verse partij worden getest. De lopende partij bevat nog de oorspronkelijke scriptversie.

Het eerdere berichtpictogram bleek een gewone melding over de lege queue van Rome, niet een geslaagde proefmelding. Er is dus nog geen bewijs voor geslaagde queueaansturing of vijf beurten persistentie.

De bediening is hiermee aangetoond, maar nog geen volledig autonome benchmarkrunner. Volgende stap: proefscript opnieuw laden, runtimefouten verder corrigeren en de queueproef uitvoeren. Daarna kunnen we beurtvoortgang, dialoogafhandeling en resultaatregistratie in een gecontroleerde runner bundelen.

## Vervolgproef 1 oktober 2026

Een verse Deity-partij met de gecorrigeerde HasAdvance-aanroep bereikte 3950 BC en liep bij de volgende AI-beurt vast, zonder zichtbaar SLIC-foutvenster. Oorzaak nog niet vastgesteld. Daarna zijn geneste BuildingType-aanroepen vervangen door een vooraf berekende aiqp_silo. Een nieuwe partij bereikte vervolgens 3900 BC zonder foutvenster; omdat dit een andere kaart/start is, bewijst dit niet dat de wijziging de hang oplost.

Er is nog geen AIQP-resultaatmelding gelezen. De proefberichten hadden geen Show(); de lokale tutorial gebruikt dit voor het openen van berichten. Show() is nu toegevoegd, maar moet opnieuw geladen en getest worden. De huidige partij bevat die laatste wijziging nog niet. Queuewijziging en persistentie blijven onbewezen.

Click accepteert nu optionele FromX/FromY voor de waargenomen interne cursor. Kleine menuverplaatsingen werkten; een grote verplaatsing overschoot. Nog geen betrouwbare algemene muiskalibratie. Een toetsactie is geweigerd toen focus herstellen niet lukte; er is toen geen invoer verzonden.

## Editorobservatie 2 oktober 2026

Lokale editorhandleiding uitgelezen; fragmenten in editor-handleiding-fragmenten.txt. De handleiding beschrijft Show Map en Edit City voor een geselecteerde beschaving, met toegang tot Production Tab. Nog niet bevestigd dat AI-controle behouden blijft tijdens observeren.

Eerdere ai_queue_probe-include uitgeschakeld in CTP-proef/script.slc; backup PROEVEN/script-voor-observatie.slc. Geen quotavariant ge�nstalleerd. Nieuwe editorstart op Deity/Gigantic/8 beschavingen bereikt het voorwaardenvenster. Geen voorwaarden geaccepteerd. Screenshot editor-voorwaarden.png. Runtimecontrole van AI-steden/queues wacht op persoonlijke afhandeling van dit venster door gebruiker.

Editorvoorwaarden met expliciete toestemming gebruiker geaccepteerd. De daaropvolgende editorstart vraagt: Put your Call to Power CD in your CD-ROM drive, met Retry/Cancel. Editorobservatie daardoor nog niet uitgevoerd. Geen wijzigingen aan executable of CD-controle gedaan. Grote muisbewegingen zijn in Bedien-CTP.ps1 opgesplitst in stappen van maximaal5 pixels; de acceptatieklik werkte in deze proef, algemene betrouwbaarheid nog niet vastgesteld.

Na beschikbaar maken van de cd opnieuw geprobeerd: editor succesvol gestart op Deity/Gigantic/8 beschavingen, zonder nieuwe cd-melding. Show Map geactiveerd en volledige kaart zichtbaar gecontroleerd. Editorpaneel gesloten; daaropvolgende n-invoer bracht de datum van 4000 BC naar 3950 BC. AI-bouwqueues en behoud van AI-controle na spelerselectie zijn nog niet gecontroleerd. Cursorbeweging blijft afhankelijk van de werkelijk zichtbare interne positie: een klik met fout aangenomen startpositie sloot het paneel niet; de gecorrigeerde klik wel. Geen quotavariant geïnstalleerd.

## Werkende AI-stadsobservatie, 2 oktober 2026

Gebruiker heeft de juiste volgorde aangetoond: beschaving selecteren, Edit City openen, daarna een stad van die beschaving op de kaart selecteren. Terwijl Edit City open blijft, via Screens > CITY het City Status-overzicht openen. Eerdere mislukte selectie is geen bewijs dat AI-stadsobservatie onmogelijk is.

Zelf gecontroleerd in het geopende voorbeeld: Amsterdam, grootte 1, totaal 1 stad, huidige productie Warrior, resterende tijd weergegeven als 2, spelindicator Turn 3. Screenshot: automatisering/ai-amsterdam-turn3.png. City Status zelf gesloten en via Screens > CITY opnieuw geopend: dezelfde stad en productie zichtbaar. Geen bouwopdracht, Rush Buy, bevolkingswijziging of beurt uitgevoerd bij deze controle. Volledige queue en behoud van zelfstandige AI-productiekeuzes na hervatten nog niet bewezen; de huidige productie is wel uitleesbaar.

Bedien-CTP.ps1 heeft nu optionele -ResetCursor: relatieve kleine bewegingen naar de bovenste linkerrand, daarna naar de doelpositie. Hiermee is City Status in deze proef gesloten; opnieuw openen werkte vervolgens met de waargenomen FromX/FromY. Randkalibratie kan de kaart laten scrollen en is nog geen algemene betrouwbaarheidsgarantie.

Vanaf gesloten panelen zelf Turkse observatie uitgevoerd: Escape > Cheat Mode, van speler 6 viermaal min naar speler 2, Edit City openen, Screens > CITY. City Status selecteerde/centreerde Ankara automatisch; vooraf geen Turkse stad op de kaart aangeklikt. Zichtbaar op Turn 3: totaal 1 stad, Ankara grootte 1, productie Warrior, resterende tijd 4. Screenshot automatisering/ai-turken-turn3.png. Geen beurt of productieaanpassing uitgevoerd. Overzicht open gelaten. Hiermee ook zelfstandig openen van het overzicht voor een andere AI-beschaving aangetoond.

Herhaalbare stappen en gecontroleerde resultaten: zie [AI-STEDEN-BEKIJKEN.md](AI-STEDEN-BEKIJKEN.md).

## Vaste save en natuurlijke quotaproef, 2 oktober 2026

Save Game en Load Game zijn gecontroleerd: QUOTA-START-T0 op 4000 BC vóór de eerste beurt opgeslagen, bewaard en via het spel teruggeladen. Dezelfde save is gebruikt na volledige herstart voor een variant met uitsluitend primary-settlerquota nul. Beide runs bereikten twintig beurten (3000 BC). Checkpoints en waarnemingen: settlerquota/vaste-start/STARTMANIFEST.md. De AI bouwde en stichtte na observatie zelfstandig verder.

Bedien-CTP.ps1 ondersteunt nu Drag met X/Y en ToX/ToY. Via de titelbalk is City Status van 0,0 naar circa 800,292 verschoven, waardoor alle stadsrijen leesbaar werden naast de editor. Gecontroleerde UI-verplaatsing, geen gameplaywijziging. Dezelfde focus- en boundscontroles gelden; inspecteer het resultaat. Positie blijft gedurende de partij bewaard, maar was na herstart terug op 0,0.

Een menselijke b/Enter-poging in de baseline stichtte geen stad. Herhaling is door automatische goedkeuringscontrole geweigerd wegens mogelijke stadstichting; de variant hield de menselijke speler passief. Dit verschil is expliciet een proefbeperking. Oorspronkelijke AIPs na afloop hersteld; geen SLIC-queue-effect bewezen.
