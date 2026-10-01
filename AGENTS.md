# CTP I AI-project

Dit project betreft Civilization: Call to Power I, altijd op Deity. Lees PROJECTDOELEN.md en de relevante analyses voordat je gameplay wijzigt. CTP-og blijft de originele referentie; CTP-AAIP is een leermodel, geen verplichte basis. Werkversie: CTP-proef.

## Bestaande AI eerst

Lees ANALYSE/ARCHITECTUUR.md voor de bestandsopbouw en ANALYSE/AAIP-LESSEN.md voor de vergelijking. ANALYSE/INVENTARIS bevat de volledige bestandsvergelijking van default/aidata en default/gamedata, declaraties en diffs. PROEVEN/Inventariseer-AI.ps1 kan de kerninventaris opnieuw opbouwen.

Onderzoek en benut eerst FLI/AIP-aansturing in ctp_data/default/aidata en de verschillen met AAIP. De gewone AI zit mede in de gecompileerde AI-DLL; linker-maps tonen symbolen, geen implementatie. SLIC is aanvullend. Gebruik scripts pas voor aantoonbaar ontbrekende mogelijkheden. CTP-II-documentatie bewijst geen CTP-I-ondersteuning.

TECHNISCHE-UITVOERBAARHEID.md beschrijft aanknopingspunten en onzekerheden. De eerdere aanbeveling daarin om eerst de SLIC-queueproef te doen is achterhaald: de gebruiker heeft gekozen voor onderzoek van bestaande bouwprioriteiten.

## Spelbediening en tests

Lees PROEVEN/AUTOMATISERING.md voordat je het spel bedient. Gebruik PROEVEN/Bedien-CTP.ps1 voor de proefkopie. Het script controleert executable en focus. Windows-GUI-bediening vereiste uitvoering buiten de sandbox.

Bediening via hoofdmenu, Deity-start, b, Enter en n is aangetoond. Een geslaagd invoercommando bewijst geen geslaagde spelactie: controleer scherm en beurtvoortgang. CTP gebruikt een interne muiscursor; kleine relatieve bewegingen werkten, grote bewegingen kunnen overschieten. FromX/FromY zijn waargenomen cursorcoördinaten, geen garantie op een correcte klik. Fullscreen-bounds en beeldschaling kunnen veranderen.

Achtergrondbediening is niet aangetoond en is door de gebruiker uitgesteld. Een technische proefsave is geen vaste benchmark. De SLIC-queueproef is nog niet geslaagd; onderscheid voorbereide wijzigingen, runtimewaarnemingen en bewezen gameplay-effecten. Leg fouten en onzekerheden vast in het proefverslag.
