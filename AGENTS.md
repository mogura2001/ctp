# CTP I AI-project

Dit project betreft Civilization: Call to Power I, altijd op Deity. Lees PROJECTDOELEN.md en de relevante analyses voordat je gameplay wijzigt. CTP-og blijft de originele referentie; CTP-AAIP is een leermodel, geen verplichte basis. Werkversie: CTP-proef.

## Zelfstandig opvolgen

De gebruiker wil zelfstandige projectopvolging met drie opeenvolgende rollen: ctp_analist (code/game begrijpen), ctp_ontwerper (wijzigingen voordragen met uitleg), ctp_uitvoerder (toepassen/testen). Lees AGENT-CTP.md en PROJECTSTATUS.md voor opdracht, faseoverdracht en hervatpunt. De definities staan in .codex/agents/. ctp_verbeteraar is de coördinatorrol; de hoofdagent kan die rol zelf vervullen. Werk binnen een actieve opdracht zelfstandig door; vraag niet na iedere afgeronde tussenstap of je verder mag. Geef korte voortgang en leg resultaten en de volgende concrete stap vast. Alleen stoppen voor noodzakelijke gebruikersinput, een expliciet stopverzoek, een werkelijke runtimegrens of het bereiken van de actieve einduitkomst.

De brede analyse M1/fase A is afgerond en overgedragen. PROJECTSTATUS.md bepaalt de actuele werkstap. Het doel van verdere analyse is uitsluitend weten hoe en waar wijzigingen nodig zijn om PROJECTDOELEN.md te realiseren. Per doel: huidige werking, concrete instel-/codepunten, uitvoerbare aanpassingsroute, noodzakelijke afhankelijkheden en resterende blokkades. Zodra dit voldoende is voor een onderbouwd voorstel, draagt de analist over; geen volledig begrip van de game als extra voorwaarde. Aanvullend onderzoek alleen voor een benoemde kennislacune die de eerstvolgende wijziging blokkeert. Tijdens analyse geen nieuwe spelstarts of gameplay-/binarywijzigingen. Daarna fase B: uitgewerkte voorstellen met uitleg; pas daarna fase C: toepassen en testen. Gebruik gerichte delegatie aan de rol van de huidige fase; vermijd onnodige agentvermenigvuldiging en geef iedere schrijver eigen bestanden. De hoofdagent beheert PROJECTSTATUS.md. Een rolbestand is geen voortdurend achtergrondproces; claim een actieve doelmodus of planning alleen na runtimebevestiging.

## Weekbudget

Sluit de pc uitsluitend af na een nieuwe, expliciete afsluitopdracht van de gebruiker. Het bereiken van een budgetgrens geeft geen toestemming voor een afsluitcommando: stop dan alleen projectwerk en bewaar het hervatpunt. Eerdere afsluitopdrachten zijn afgehandeld en gelden niet opnieuw.

Laatste gebruikersinstructie9okt2026: stop met het afsluiten van de pc. De eenmalige opdracht is afgehandeld en alle eerdere afsluittoestemmingen zijn vervallen/ingetrokken. Bij iedere budgetgrens uitsluitend projectwerk stoppen en hervatpunt bewaren; pc aanlaten. Geen afsluithelper, afsluitcommando of afsluitplanning uitvoeren zonder een nieuwe, expliciete afsluitopdracht van de gebruiker. Een doelcontinuatie, reset of hervatting geeft die toestemming niet.

Waarschuw bij 25% of minder **resterend** accountweekbudget en stop/pauzeer alle projectwerk bij 10% of minder resterend weekbudget. Stop ook bij 5% of minder **resterend** in het vijfuurvenster; na een bevestigde reset mag zelfstandig worden hervat als het weekbudget dit toestaat. Controleer actuele limietmetadata met PROEVEN/Controleer-Weekbudget.py; projecttokens zijn geen gebruikslimiet. Zie AGENT-CTP.md voor bron, meetmomenten, onbekende/verouderde standen en stop-/hervatprocedure. Deze gebruikersgrenzen gelden voor coördinator en alle deelagents.

## Bestaande AI eerst

Tijdens actief agentwerk geeft iedere rol minstens elke tien minuten korte voortgang, ook bij stagnatie. Vermeld afgerond werk, huidige activiteit, volgende uitkomst en blokkades; werk het eigen voortgangsbestand met tijdstip bij. Meld starten, afronden, onderbreken en wachten direct. De coördinerende agent geeft agentupdates tijdens een actieve run door aan de gebruiker. Zie AGENT-CTP.md voor de rapportageafspraak; dit activeert geen timer of planning wanneer geen agent draait.

Lees ANALYSE/ARCHITECTUUR.md voor de bestandsopbouw en ANALYSE/AAIP-LESSEN.md voor de vergelijking. ANALYSE/INVENTARIS bevat de volledige bestandsvergelijking van default/aidata en default/gamedata, declaraties en diffs. PROEVEN/Inventariseer-AI.ps1 kan de kerninventaris opnieuw opbouwen.

Onderzoek en benut eerst FLI/AIP-aansturing in ctp_data/default/aidata en de verschillen met AAIP. De gewone AI zit mede in de gecompileerde AI-DLL; linker-maps tonen symbolen, geen implementatie. SLIC is aanvullend. Gebruik scripts pas voor aantoonbaar ontbrekende mogelijkheden. CTP-II-documentatie bewijst geen CTP-I-ondersteuning.

TECHNISCHE-UITVOERBAARHEID.md beschrijft aanknopingspunten en onzekerheden. De eerdere aanbeveling daarin om eerst de SLIC-queueproef te doen is achterhaald: de gebruiker heeft gekozen voor onderzoek van bestaande bouwprioriteiten.

## Les uit binaire AI-analyse

Ontbrekende broncode betekent niet dat de implementatie ononderzoekbaar is. Gerichte disassemblage van robotcom.dll heeft concrete antwoorden opgeleverd over goallimieten, city_delta en de locatieuitsluiting door packing. Gebruik bij onverklaard AI-gedrag naast FLI/AIP daarom ook gerichte DLL-analyse voordat langdurige GUI-proeven worden ontworpen. Zie ANALYSE/VESTIGINGSDOELEN.md en PROEVEN/Analyseer-AI-DLL.py.

Controleer eerst dat map en binary overeenkomen (timestamp, imagebase en waar mogelijk verdere adrescontrole). Robotcom.map past bij de aanwezige robotcom.dll; civctp.map past niet bij civctp.exe. Leid uit symbolen alleen geen implementatie af. Leg machinecodebevindingen met adressen vast en onderscheid die van interpretaties en runtime-effecten. Verander de DLL niet voor alleen-lezen onderzoek.

## Spelbediening en tests

Lees PROEVEN/AUTOMATISERING.md voordat je het spel bedient. Gebruik PROEVEN/Bedien-CTP.ps1 voor de proefkopie. Het script controleert executable en focus. Windows-GUI-bediening vereiste uitvoering buiten de sandbox.

Bediening via hoofdmenu, Deity-start, b, Enter en n is aangetoond. Een geslaagd invoercommando bewijst geen geslaagde spelactie: controleer scherm en beurtvoortgang. CTP gebruikt een interne muiscursor; kleine relatieve bewegingen werkten, grote bewegingen kunnen overschieten. FromX/FromY zijn waargenomen cursorcoördinaten, geen garantie op een correcte klik. Fullscreen-bounds en beeldschaling kunnen veranderen.

Achtergrondbediening is niet aangetoond en is door de gebruiker uitgesteld. Een technische proefsave is geen vaste benchmark. De SLIC-queueproef is nog niet geslaagd; onderscheid voorbereide wijzigingen, runtimewaarnemingen en bewezen gameplay-effecten. Leg fouten en onzekerheden vast in het proefverslag.
