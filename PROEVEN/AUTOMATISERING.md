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
