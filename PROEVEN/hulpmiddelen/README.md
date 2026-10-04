# Hulpmiddelen voor alleen-lezen binaire analyse

`../Analyseer-AI-DLL.py` gebruikt Capstone 5.0.9 en pefile 2024.8.26.
Lokaal geïnstalleerd in `python/`, geen gamebestand of globale Python-installatie gewijzigd.

Reproduceerbaar met een beschikbare Python:

```powershell
python -m pip install --target PROEVEN/hulpmiddelen/python capstone==5.0.9 pefile==2024.8.26
python PROEVEN/Analyseer-AI-DLL.py Update_Max_Goals InsertSettleGoals
```

Het script controleert map/binary-timestamps en imagebase. De aanwezige engine-map
past niet bij civctp.exe; `--engine` weigert daarom analyse. Robotcom past wel.
Symbolen begrenzen de disassemblage; ingebedde data kunnen als instructies worden
afgedrukt. Interpretatie vereist handmatige controle van branches en aanroepen.

`../Analyseer-Engine-Locaties.py` biedt daarnaast alleen-lezen onderzoek van de
aanwezige executable zonder de afwijkende engine-map. `--world` vindt de World
COM-interface via de GUID uit de overeenkomende AI-DLL. Een gevonden kandidaat
moet worden gecontroleerd via QueryInterface, AddRef/Release en de bekende
AI-interface-offset. `VA:lengte` (hexadecimaal) toont een expliciet gekozen
codebereik, geen automatisch bewezen functiegrens. Bewijs en interpretaties staan
in `ANALYSE/LOCATIEKWALITEIT.md`. Beide tools veranderen geen binaries.

`../Controleer-Locatiescore.py` gebruikt bovendien Unicorn 2.1.4 voor uitvoering
van de oorspronkelijke puntberekening op synthetische kaartwaarden. Installatie
in dezelfde lokale map: `python -m pip install --target PROEVEN/hulpmiddelen/python unicorn==2.1.4`.
Het hulpmiddel controleert de SHA256 van de engine, start geen spel en verandert
geen executable of save. Het controleert de double-score vóór de externe
integerconversie; gameplay, database-loading en AI-selectie vallen buiten deze
controle. Resultaten: `ANALYSE/BINAIR/score-formulecontrole.json`.

`../Controleer-Scorecache.py` gebruikt dezelfde emulator voor de originele
archiefroute op synthetische scoretabellen. Archief-I/O wordt nagebootst; actieve
AI-spelers en echte saves vallen buiten deze controle. Twee verschillende
kaartafmetingen bevestigen exact bewaren en herstellen van de 16-bit waarden,
zonder scoreopbouw binnen die route. Resultaten:
`ANALYSE/BINAIR/score-cache-controle.json`.

De engine-analysetool heeft ook `--calls` (kandidaten voor directe calls),
`--refs` (ruwe 32-bit referenties) en `--tokens` (integer vóór een exact
tokenkeyword). Referenties en tokens zijn zoekresultaten; controleer de
aanroepende code, metadataopbouw en springtabellen voordat ze een binding bewijzen.
