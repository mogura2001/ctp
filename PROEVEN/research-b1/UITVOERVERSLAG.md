# B1-uitvoering

Afgerond 7 oktober 2026, 20:09 Europe/Amsterdam. Status: **toegepast en offline gecontroleerd; echte parser-/saveactivatie en gameplaywinst nog niet aangetoond**. Er draait geen B1-proefrun.

De formele B→C-overdracht van PROJECTSTATUS (19:57) en de inhoudelijk gelijk gebleven definitieve ontwerpversie zijn gevolgd. Ontwerphash: `64DA8067A92D83A32B4234DE1D55B3A80DBCEE838E4585B5AF8066170F4DC19E`. Alleen de acht toegewezen CTP-proef-AIPs zijn gewijzigd. PROJECTSTATUS, ontwerp, OG/AAIP, andere spelbestanden en bestaande saves zijn niet door deze uitvoerder gewijzigd.

## Toepassing en controles

Voorbereiding 20:03:23; toepassing/offlinecontrole 20:04:21. Alle acht doelbestanden waren vóór toepassing volledig bytegelijk aan hun actuele OG-referentie, met de acht beschreven oorspronkelijke posities. Er zijn dus geen bestaande gebruikerswijzigingen in deze bestanden overschreven.

| Bestand | Religion/Theocracy vóór | Na | Records |
| --- | --- | --- | ---: |
| default.aip | 7/97 | 1/2 | 98 |
| cleric.aip | 2/1 | 1/2 | 98 |
| milmany.aip | 7/97 | 1/2 | 98 |
| milfew.aip | 12/98 | 1/2 | 98 |
| scimany.aip | 15/96 | 1/2 | 98 |
| scifew.aip | 7/97 | 1/2 | 98 |
| slaver.aip | 13/19 | 1/2 | 98 |
| citywall_science.aip | 7/97 | 1/2 | 98 |

De bestaande volledige recordregels zijn verplaatst binnen het werkelijke `Advancements_List`-`#DATA`-blok. Multiset, recordaantal, relatieve restvolgorde, recordbytes, overige bestandsbytes, bestandslengte, encoding en CRLF zijn behouden. Alle records verwijzen naar bestaande advance.txt-technologieën. De aanvullende onafhankelijke blockcontrole gebruikt de laatste werkelijke declaratie; een eerste tijdelijke audit selecteerde per ongeluk een eerdere becommentarieerde syntaxillustratie en faalde terecht. Een inline audit had tevens een native-shellquotingfout; de audit uit bestand is daarna geslaagd. Er is door die fouten geen spelbestand gewijzigd.

Een baseline/nameting van **621 bestanden** omvat alle default/aidata- en default/gamedata-bestanden, alle exe/DLL/map-bestanden onder ctp_program, userprofile en bestaande saves in de drie kopieën. Exact de acht toegewezen AIPs verschillen; **613 bestanden zijn onveranderd**. Dit is gelijkheid tegenover de actuele baseline, inclusief bestaande verschillen tegenover OG. Grafische assets buiten deze afgebakende gameplay/binaryinventaris zijn niet als volledig gehasht gepresenteerd.

De proefbinary is bytegelijk aan OG en de geanalyseerde versie: civctp.exe SHA256 `B1B5256FB0FB1A844548EB62E7B13D79A8B4F81B4499CFBE93E614BD5268AC79`, timestamp `37d6f702`, imagebase `400000`; robotcom.dll SHA256 `3025070D66FBA516E4CDD70AE332055E1E4EF5162BF1B14C163B9BD128A35D44`, timestamp `37b894e7`, imagebase `20000000`. De passende robotcom-mapbinding wordt uit de bestaande analyse gebruikt; de niet passende civctp-map wordt niet gebruikt voor implementatieclaims. De eerdere SLIC-queue-include blijft uitgeschakeld.

Beide T0-kopieën (vaste-start/QUOTA-START-T0.sav en proef-save/games/Julius/QUOTA-START-T0) behouden SHA256 `8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26`.

## Bewijsbestanden en herstel

[manifest.json](manifest.json) bevat exacte doel-/back-uppaden, alle vóór-/nahashes, posities en CRLF-aantallen. [backup](backup/) bevat de acht ongewijzigde baselines. De acht `.diff`-bestanden beschrijven de recordverplaatsingen. [inventory-before.json](inventory-before.json), [inventory-after.json](inventory-after.json), [offline-results.json](offline-results.json) en [version-save-audit.json](version-save-audit.json) leggen de controles vast. De diff van milfew toont door het bestaande ontbreken van een laatste newline een END_DATA-regel in de diffcontext; die daadwerkelijke eindbytes zijn onveranderd.

Toepassings-/herstelhelper: [Pas-B1-Toe.py](Pas-B1-Toe.py). Aanvullende read-only versiecontrole: [Controleer-B1-Versie.py](Controleer-B1-Versie.py). Geen herhaling van de bestaande 14/15 originele selector-/switchcontroles: onderzochte code is niet gewijzigd.

Voor herstel eerst uitsluitend de B1-proefinstantie afsluiten en controleren dat geen nieuwe gebruikerswijziging in de acht bestanden staat. Vanuit C:\GIT\ctp:

```powershell
& 'C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe' PROEVEN/research-b1/Pas-B1-Toe.py restore
```

De helper weigert herstel bij een afwijkende actuele nahash of back-uphash en overschrijft dus geen latere gebruikerswijziging. Zij herstelt alleen de acht bestanden. Herstel is voorbereid, niet uitgevoerd. Daarna de proefapplicatie volledig opnieuw starten en de originele T0 laden. Een B1-vervolgsave bevat gewijzigde effectieve lijsten en onderzoekstoestand en geldt niet als herstelde baseline.

## Runtimegrens en terugvraag

Bij de procescontrole stond civctp PID3944 uit **D:\CTP\ctp_program\ctp\civctp.exe** open; [runtime-state.json](runtime-state.json) bewaart de waarneming. Dit is een andere installatie. Er is geen invoer, sluiting, patch of GUI-startpoging uitgevoerd. Bedien-CTP.ps1 weigert starten zolang enig civctp-proces aanwezig is. Root heeft expliciet opgedragen deze gebruikersgame te laten staan en de grens niet te omzeilen.

De bestaande PROEVEN-hulpen leverden bij gerichte zoekopdrachten geen ReadProcessMemory/OpenProcess-uitlezing van de effectieve onderzoekslijst. Voor de normale route geldt bestaande machinecodebewijs: managerbronlijsten worden bij manageropbouw ingelezen/gecachet; de save herstelt afzonderlijk effectieve lijsten, huidig onderzoek en herkeuzevlag. Daarom bewijzen diskbestanden en een herstart op zichzelf geen actief B1-beleid. Geen echte parseracceptatie, volgende reguliere researchkeuze, learnt-turn of regeringswisseling is gemeten.

Concrete overdracht naar analist/root: bind voor deze ongewijzigde T0 de normale AI-civs, hun effectieve Planner/AIP.Advancements_List (+7fc), bronnen/overwrites, ScienceAgent-doel/herkeuzevlag en bekende Religion/Theocracy **read-only** aan een echte geladen proefinstantie, of aan aantoonbaar overeenkomende savevelden. Maak onderscheid tussen de gecachete acht bronlijsten en elke civ haar opgeslagen effectieve lijst. Toon bij de relevante reguliere beginbeurt/lijstswitch of L' actief wordt en bij natuurlijke herkeuze de daadwerkelijk gekozen advance onder de bestaande beschikbaarheids-/tijdtoets. Geen nieuwe partij, savepatch, onderzoeksannulering of alternatieve save als vervanging. Root heeft hiervoor inmiddels een gericht A2-analistenpakket gestart.

Pas na beschikbaarheid van een vrije CTP-proefinstantie en deze uitleesroute kan de minimale daadwerkelijke activatiecontrole volgen: volledige herstart, dezelfde T0, volledig passieve menselijke speler, gelijke invoer/observatie bij baseline en B1. Er is geen lange T100-run uitgevoerd.

De technische acceptatie is dus gedeeltelijk: acht exacte tekstwijzigingen/offline-invarianten geslaagd; acht echte ingelezen lijsten en effectieve keuze nog open. Alle gameplaycriteria (Religion/Theocracy-leerbeurten, veiligheid/transport/uitbreiding en echte regering) zijn **niet gemeten**. Geen verbetering geconcludeerd.

Budget: verse meting 19:59:29 week90/vijfuur34, 20:04:00 week89/vijfuur30; laatste rootmelding20:09:49 week87/vijfuur18, state ok. Er is geen stopgrens bereikt.
