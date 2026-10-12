# Rootreview en budgetstop

10 oktober 2026,13:18 Europe/Amsterdam. Alleen voorbereiding; geen nieuwe installatie/start/T0-load/pass/live-reader. Uitvoerder interrupted, overige deelagents completed. Pc aan, geen afsluitactie.

Verse budget13:17:11, bron13:17:03: vijfuur5%, week85%, reset1791641525=16:12:05 lokaal. Hervat pas na verse metadata die reset en voldoende ruimte bevestigt.

Root las code/CLI. Nog geen livevrijgave. Drie beperkte correcties blijven nodig:

- Finish:10s-reserve opnieuw direct vóór CloseMainWindow;480s-grens vóór iedere query en na terugkeer, geen exitacceptatie buiten480s/10s.
- Guard: echte Process.Path/StartTime na GetProcessById ook aan startrecord binden.
- Read: succesvolle JSON.instance.pid, creationtime_filetime (FromFileTimeUtc naar Unixms) en executable aan startrecord binden vóór n/B-acceptatie. Observer zelf behouden.

Vier bronhashes bij stop gelijk aan VOORBEREIDING.md; correcties nog niet toegepast. Originele proef-DLL hash3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44 bevestigd. MENU_PASS/exit/herstel uit eerdere H1-I-hostproef blijven geaccepteerd. Echte AI-activering en gameplay open.

Volgende oplevering: dezelfde uitvoerder alleen drie routinecorrecties laten aanpassen, gewijzigde syntax/hash/diff reviewen; daarna afzonderlijk H1-I-T0-arm vrijgeven met bestaande lezer en exact h1-20261010/A/B-scope. H3 volgt na apart resultaatreview, geen extra doelenzoekbeurten.
