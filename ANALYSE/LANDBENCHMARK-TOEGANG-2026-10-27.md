# Toegang tot de nieuwe landbenchmark

27 oktober 2026, 16:04 CET (Europe/Amsterdam). Gerichte fase A voor Doel1/1a, twee vragen: bestaande gevalideerde save-/kaarttoegang en de kleinste bewezen observerroute. Alleen bestaande documenten en hulpmiddelen gelezen, plus bestandsgrootte en SHA256 gecontroleerd. Geen spelstart, UI, RPM, installatie, binarywijziging, nieuwe parser of raamwerk.

**Uitkomst:** geen bestaande gevalideerde offline saveparser gevonden die deze nieuwe save naar beurt, volledige kaart, landverbindingen en startcivs decodeert. De kleinste reeds bewezen route is één gewone wegwerplaadbeurt van de save, zonder `n`, gevolgd door Cheat Mode → Show Map en speler-/Unit Status-observatie. Daarna deze geladen toestand weggooien en de ongewijzigde start opnieuw laden voor de eigenlijke benchmark. Dit is een overdracht voor uitvoering, niet een uitgevoerde kaartcontrole.

## 1. Bestand en bestaande leestoegang

Nieuwe save: `CTP-proef/ctp_program/ctp/save/games/Julius/UITBREIDING-LAND-T0`, **352021 bytes**, SHA256 **`a670867460bae5d8d9196856d5ca88163b0eff951e9a9db42a05b83ee38d2301`**. Deze twee bestandsfeiten zijn hier onafhankelijk bevestigd. De naam T0 en de gebruikersbedoeling landbenchmark bewijzen nog geen beurt, kaarttype, afmetingen, Deity, starts of beschikbare ruimte.

Onderzochte bestaande ingangen:

| Ingang | Wat reeds bewezen of concreet aanwezig is | Grens voor deze opdracht |
|---|---|---|
| [STARTMANIFEST.md](../PROEVEN/settlerquota/vaste-start/STARTMANIFEST.md) en latere hostreviews | Oude vaste save via normale Load geladen; hash plus laadscherm/zichtbare datum en afzonderlijke runtimevelden gebruikt | Geen algemene offline save-decoder; oude instellingen gelden niet automatisch voor deze nieuwe save |
| [OPENINGSFASE-GEHEUGEN-B2.md](OPENINGSFASE-GEHEUGEN-B2.md) | Enginearchive, decompressed buffer/cursor/whole-archivelengte en eigen optionele completionrecord onderbouwd | Geen complete save-/World-parser. Dit heropenen om een kaart te reconstrueren is niet nodig voor de huidige ingang |
| [Lees-Onderzoeksactivatie.py:72](../PROEVEN/ai-uitlezen/Lees-Onderzoeksactivatie.py:72) | Bestaande readonly **live** decoder leest externe World-dimensies als drie signed16-waarden op World+14/+16/+18; serializerbinding benoemd | Geen diskdecoder, landconnectiviteitsanalyse of complete terreinexport. Externe coördinaten zijn niet zonder omzetting de interne H3-terraingrid |
| [ACTIVATIE-VESTIGING-H3.md](ACTIVATIE-VESTIGING-H3.md) en Controleer-Decoder.py | Begrensde goal-/owner-/cachedecode en dimensiegrenzen onderzocht; synthetische decoderchecks aanwezig | De oude observer accepteert expliciete oude DLLvarianten; hij is geen direct uitvoerbare observer voor iedere huidige release. Geen hashguards uitschakelen. Geen nieuwe-land-run of dimensies hier gemeten |
| [T60-vergelijking](../PROEVEN/settlerquota/reeks/VERGELIJKING-T60.md) | Drie saves normaal geladen en AI-steden/eenheden bekeken zonder beurt of opnieuw opslaan; bronhashes bleven gelijk | GUI-observatie, geen complete saveformatkennis of bewijs van ongestoorde vervolg-AI binnen dezelfde editorload |

De gerichte zoekactie naar save-/kaartleesmiddelen en decompression-/dimensiecode vond geen gevalideerde offline kaart-/startpositieroute. Dat is geen bewijs dat zo'n parser nergens kan bestaan. Een oude save-readerclaim mag evenmin uit bestandsnamen als `Lees-*` worden afgeleid: de aanwezige relevante readers lezen hoofdzakelijk een levend, expliciet gebonden proefproces.

De oude ManyIslands-aanduiding blijft een gebruikersmelding. Het oude STARTMANIFEST bevestigt Deity/Gigantic/acht spelers en de oude savehash, maar daarmee is het oude gegenereerde kaarttype niet alsnog zelfstandig vastgesteld. De nieuwe save mag niet op die aanname worden beoordeeld.

## 2. Kleinste bewezen normale route voor uitvoering

Benodigde bestaande middelen: [AUTOMATISERING.md](../PROEVEN/AUTOMATISERING.md), `PROEVEN/Bedien-CTP.ps1`, [AI-STEDEN-BEKIJKEN.md](../PROEVEN/AI-STEDEN-BEKIJKEN.md), [lokale editorhandleiding](../PROEVEN/editor-handleiding-fragmenten.txt). De Show Map-actie is daadwerkelijk aangetoond op2oktober; spelerselectie en City/Unit Status zijn daarna herhaald gebruikt. Geen nieuwe parser of enginecall nodig.

1. Root bewaart de exacte nieuwe save en inventariseert de huidige proefbestanden. Start de gewone CTP-proef met de behouden werkende configuratie. **Geen nieuwe kaart genereren en geen editorstart vanaf New Game:** we willen juist deze bestaande save beoordelen.
2. Normaal hoofdmenu → Single Player → Load Game → Julius → `UITBREIDING-LAND-T0`. Controleer de geselecteerde naam en zichtbare Turns-waarde vóór Load; leg die vast. Na Load de zichtbare datum/turn en starttoestand vastleggen. Niet op `n`, `b` of een start-/plaatsingsknop drukken.
3. Escape → Cheat Mode. Lees de getoonde Difficulty zonder op de cyclische wijzigingsknop te klikken. Kies uitsluitend **Show Map**. Volgens de lokale handleiding toont dit de gehele kaart en spelobjecten; AUTOMATISERING.md bevestigt dat dit daadwerkelijk werkte. Dit verandert de geladen observatietoestand en is geen bewezen zuiver readonly actie op die toestand. Daarom is dit een wegwerpload.
4. Leg overzichtskaart en zo nodig overlappende delen van de zichtbare kaart vast. Gebruik alleen de reeds werkende gewone kaartnavigatie. Een overzicht alleen kan smalle zeestraten of landbruggen verhullen; controleer zulke verbindingen op tegelschaal. Kaartzoom, exacte afmetingen of positiecoördinaten die de GUI niet betrouwbaar toont blijven UNKNOWN; geen niet-bewezen sneltoetsen of dimensionering uit pixels verzinnen.
5. Selecteer via Player+/− iedere aanwezige beschaving en controleer zichtbaar nummer/naam. Voor T0 zonder steden heeft CITY geen noodzakelijke functie: de oude proef meldde daar terecht dat eerst een stad nodig was. Gebruik de bestaande **Unit Status**-toegang voor startunits; Show Map maakt hun zichtbare kaartlocaties controleerbaar. Leg de werkelijk aangetroffen civs en hun startgroepen vast. Een eventuele nieuwe klik om een unit te centreren eerst visueel controleren; geen bewezen automatische centrering claimen als die nog niet is waargenomen. Niet bewegen of een opdracht geven.
6. Sluit het spel normaal **zonder Save Game/Save Map/Save Scenario**. Controleer bronhash en herstel eventuele gewone profiel-/autosavewijzigingen volgens de bestaande proefafspraken. Voor een prestatieproef een verse normale start met dezelfde originele save gebruiken; de Show Map-/editorload wordt niet doorgespeeld of als benchmarkstart opgeslagen.

Bij bediening: actuele bounds en interne cursor controleren, na iedere relevante actie een verse succesvolle opname; geen oude opname als nieuw bewijs gebruiken. Een geslaagd inputcommando bewijst geen geslaagde actie. De bestaande `Observeer-T60.ps1` bevat historische vaste coördinaten en is dus **geen blind uit te voeren nieuwe-T0-runner**. Zijn bewijswaarde is de herhaalde bestaande GUI-route; geen nieuw automatiseringsframework nodig.

Deze wegwerproute voorkomt dat het blootleggen van de kaart of spelerselectie de eigenlijke vergelijking besmet. Niet aannemen dat Cheat Mode uitsluitend cosmetisch is, of dat terugklikken van Hide Map alle veranderde geladen toestand herstelt. De handleiding zegt expliciet dat Cheat Mode de scoring van de huidige game aantast; opnieuw opslaan is hier onnodig.

## 3. Meetlat voor een bruikbare ruimtebenchmark

Een grote zichtbare landmassa is onvoldoende voor de claim **30 nuttige steden per AI zonder transportprobleem**. Maak twee acceptaties afzonderlijk:

**A. Start-/landcontrole:** geschikt om een vergelijking te starten zonder evidente kleine-eilandverwarring. Benodigde registratie:

| Per save / per civ | Vast te leggen waarneming | Wat daarmee nog niet bewezen is |
|---|---|---|
| Save-identiteit en T0 | Exacte hash, geselecteerde savenaam, laadscherm Turns0, geladen datum/starttoestand; Deity zichtbaar | Bestandsnaam T0 bewijst dit niet; datum alleen bewijst geen volledige gelijkheid |
| Deelnemers | Human apart; iedere aanwezige AI met spelernummer/naam en startunits/startgroep | Acht spelers of twee settlers uit de oude save niet overnemen |
| Landtoegang | Startgroep op welk zichtbaar verbonden landdeel; zee-onderbrekingen en smalle corridors expliciet fotograferen | Zelfde continent is niet automatisch veilig/bereikbaar; kusten kunnen alleen visueel verbonden lijken |
| Buren en concurrentie | Welke starts hetzelfde land delen en hoe hun bruikbare uitbreidingsgebieden elkaar overlappen | Eén continent per civ telt niet vanzelf als vrije eigen ruimte; vrede/veiligheid volgt niet uit afstand alleen |
| Terrein en functie | Voldoende zichtbare landroutes en groeivoedsel; geschikte science-/productionlocaties en eventuele monopolyplekken in bereik | Landtiles tellen is geen rolcertificering. Productie vraagt o.a. drie bergen plus voedselhaalbaarheid, science minimaal drie voedselverbeteringsmogelijkheden |
| Grenzen van toegang | Exacte dimensies alleen invullen bij betrouwbare UI/gebonden read; anders UNKNOWN. Voor onduidelijke kustverbindingen eveneens UNKNOWN | Geen exacte kaartoppervlakte of bereikbaarheid uit screenshots zonder betrouwbare schaal/coördinaten |

AcceptatieA moet per civ eindigen als **evident eiland-/transportbeperkt**, **bruikbaar voor een landvergelijking met beschreven concurrentie**, of **nog onbekend**. Vooraf aanwijzen welke civs primaire ruimte-meetpunten zijn; alle AI-uitkomsten blijven rapporteren. Achteraf alleen de beste civ selecteren is geen zuivere vergelijkingsopzet. Als een civ klein opgesloten zit, is zij voor dit beperkte ruimteonderzoek een afzonderlijke context, geen bewijs van slechte settlerproductie.

**B. Sterke capaciteitsclaim:** alleen als expliciet gewenst wordt te verklaren dat30 nuttige steden daadwerkelijk passen. Hiervoor moeten per meetciv ten minste30 verschillende wettelijke, voor de afgesproken functies geschikte centra kunnen worden aangewezen, met bruikbare landtoegang, gezamenlijke werkplek-/bergdekking en conflict-/burenvoorwaarden. Hetzelfde gebied mag niet zonder afweging als exclusieve capaciteit van meerdere civs worden opgeteld. Waar voedsel/improvements pas later beschikbaar zijn, de fasevoorwaarde benoemen. Ook zo'n locatieplan garandeert geen snelle uitvoering of afwezigheid van oorlog.

Een volledige capaciteitstelling is **geen voorwaarde om de korte visuele landcontrole uit te voeren**. Als zij niet gedaan wordt, noem de save een landbenchmark met vooraf beschreven ruime starts, geen bewezen30-stedenkaart voor iedereen. De beslisvraag of de AI aanwezige ruimte werkelijk benut blijft dan onderdeel van de gameplaymeting.

Voor de latere gelijkestartvergelijking: dezelfde onbewerkte save per versie; menselijke speler passief volgens vast protocol; vaste T25/T50/T100 en eerste25/30/40; per civ steden, bestaande settlers, huidige settlerfronten, regering en eventuele ruimte-/transportbeperkingen. Stadsbezit is niet automatisch eigen stichting of nuttige specialisatie. Regel-/rol-/bouwbaarheidscertificaten en kennisgrenzen van de AI blijven afzonderlijk van de omnisciente Show Map-beoordeling. De waarnemer die land ziet bewijst niet dat de AI die tegels al kent of volgens haar planner kan gebruiken.

## Overdracht en voortgang

**16:04 CET — afgerond en gestopt,2/2 vragen beantwoord.** Bestandsgrootte/hash bevestigd; geen gevalideerde offline kaartparser gevonden binnen de gerichte bestaande ingangen. Gewone Load → Cheat Mode → Show Map + speler/Unit Status is de kleinste reeds bewezen route; alleen uitvoeren als wegwerpload zonder beurt/stadplaatsing/opslaan. Exacte nieuwe dimensies, civs, starts en landverbindingen zijn nog niet waargenomen.

Volgende concrete oplevering bij uitvoering: één vastgelegde nieuwe-T0-laadcontrole plus per-civ-landtoegangstabel en kaartopnamen, daarna normaal sluiten en bronhashcontrole. Root archiveert save en beheert PROJECTSTATUS.md; deze analist heeft uitsluitend dit bestand geschreven. Geen andere helper of achtergrondanalyse actief. Doel1/1a nog OPEN; deze notitie bewijst geen gameplayverbetering. Pc blijft aan. Budgetbron15:00:40UTC: vijfuur92%/week85% resterend, stateok.
