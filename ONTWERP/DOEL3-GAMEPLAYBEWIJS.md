# Doel 3: Religion, Theocracy en werkelijk Theocracy gebruiken

12 oktober 2026, 12:08 Europe/Amsterdam. Fase B, compact vervolg op de afgeronde brede A-overdracht en bestaande B1/B2-ontwerpen. Alleen dit voorstel en het eigen voortgangsbestand zijn gewijzigd. Geen code, installatie, proef of spelbediening. Root beoordeelt en legt de uitleg aan de gebruiker voor vóór C. Zie FOCUS-DRIE-SESSIES.md: sessie 1 moet naar echte gameplaymeting leiden, technische deelpasses tellen niet als bereikt doel.

## Oorzaak, gewenste beslissing en minimale variant

De bestaande effectieve onderzoekslijst stuurt de kandidaatvolgorde. De originele meeste lijsten zetten Theocracy achteraan; citywall_science kan een persoonlijkheidslijst vervangen. Niet-Cleric-regeringsregels vragen doorgaans geen Theocracy. Onderzoek unlockt haar, maar een afzonderlijke poll moet haar vervolgens aanvragen en de engine moet Anarchy voltooien. Dit is aangetoond in ANALYSE/ONDERZOEK-EN-REGERINGSKEUZE.md en AIP-LAADWERKING.md, geen verklaring uitsluitend uit modclaims.

Gewenst: bij iedere normale autonome herkeuze eerst onbekend Religion, daarna onbekend en beschikbaar Theocracy; vervolgens werkelijk actieve regering 3 zodra de bestaande overstapvoorwaarden dat toelaten. Geen kunstmatig leren, annuleren, regeringswisselen of steden plaatsen. Persoonlijkheden mogen na voltooide opening weer verschillen.

**Gebruik uitsluitend bestaande B1 + B2a-N30 + B2b. B2c is voor deze proef niet nodig.** B1 dekt alle acht aangetoonde normale schrijvers van Advancements_List, inclusief citywall_science. De overige normale AIPs bevatten geen aanvullende onderzoekslijst. Noscience is leeg, maar in de aanwezige normale FLI-route niet geladen. Als de benchmark werkelijk een lege/ongewijzigde lijst laat zien, documenteer die echte schrijver; voeg niet preventief een overlay, parserframework of achttien fixtures toe.

**Nieuw echt activatiebewijs12okt:** PROEVEN/activatie-h3-runtime/2026-10-12/20261012T115257/H1-I/A.json en B.json zijn hier gelezen en hun zeven civregels2..8 samengevat. A bevat oude gecachede lijsten bij T0. Na één gewone pass heeft B bij alle zeven de effectieve prefix Religion(index12),Theocracy(index18). Civs2/3/4/6/8 vragen Religion,5/7 Theocracy; last_ai_request en engine_current stemmen per civ overeen. Dit bewijst daadwerkelijke B1-activatie/keuze in deze T0 op T1, geen geleerd-bits of actieve Theocracy en geen ongepatchte T1-baselinevergelijking. De H1-identiteitsadapter verandert geen researchroute. Een algemene parser-/cacheproef is dus geen noodzakelijke volgende poort; meet nu leren en regering. De concrete indices zijn hier een waarneming, geen hardgecodeerde readerinputs.

N30 is nu door de gebruiker gekozen en vervangt de oude open N-keuze. Het bestaande B2a-geheugen beëindigt de gezamenlijke opening éénmaal bij minstens 30 steden én actieve Theocracy. **Dit is geen vestigingsstop.** De afspraak blijft nuttige veilige/bereikbare vestiging tot maximaal 40 onder Theocracy. B4, een cap30 op settlervraag, andere quota, H1/H3 en stadsrollen worden niet in deze doel3-variant opgenomen. De nieuwe 30→40-vraagroute is een afzonderlijke wijziging; deze proef claimt haar niet te realiseren.

## Reeds gebouwde ingreep en exacte pins

Gebruik PROEVEN/opening-b2/candidates/B2a-N30-TECHNICAL/robotcom.dll, SHA256 **eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890**. Het bestand is op de originele DLL gebouwd, bevat vijf registratie/beginturn/save/load/reload-ingrepen en 4348 payloadbytes, geen H3-combinatie. Bestaande 88 native gevallen en gewone loader zijn geaccepteerd; niet opnieuw draaien zonder gewijzigde bytes of nieuwe concrete fout. Het manifest gebruikt historische labels production_N_chosen=false/BUILT; laat dat historische bewijs intact en leg de huidige N30-selectie/installatie apart vast.

| Pakket | Manifest SHA256 | Gebruik |
| --- | --- | --- |
| PROEVEN/research-b1/manifest.json | 04e473b88d7e45ff158f4d1e2252c72164a0ffcf06d5766c89def9c9d7b58cbd | Acht reeds aanwezige B1-AIPs, per bestand after_sha256; before-backups voor originele onderzoeksbaseline |
| PROEVEN/opening-b2/B2a-N30-TECHNICAL.manifest.json | 34562e21a9539cccae059a4746ed246039266b6ac8238ff4968c591307fe96ef | N30, vijf hooks, payload, relocatie-/PE-contract |
| PROEVEN/opening-b2/regering-b2b/20261010T180801159/manifest.json | e1bacd6b0fbed849563fb167b2aae6f9b2cdf01878ddc03a3756698f97e2c5a1 | Tien hieronder genoemde tekstkandidaten |

De acht B1 after-hashes staan in het manifest en worden bij installatie gecontroleerd: default, cleric, milmany, milfew, scimany, scifew, slaver en citywall_science. Alleen Religion/Theocracy zijn binnen hun oorspronkelijke 98-recordlijsten verplaatst. Geen nieuw researchbestand nodig.

De tien B2b-kandidaten komen ongewijzigd uit de genoemde candidate/-map, naar CTP-proef/ctp_data/default/aidata:

| Bestand | SHA256 |
| --- | --- |
| inputs.fli | 0c58c6916e4c1ca9da1c0d0584a10be639721e384a414d1a00c0614a354a1e9a |
| set_govern_opening.fli | d922b5118b5657153dbd6f138be01f4063bc4212725b9c79ec3505b7836c0aa2 |
| set_govern_after_opening.fli | bcf10201718243a9e783d62d9b897857116adcc06c1a545a86b7355747ce0707 |
| beginturnCleric.fli | c4aca8b67cd431dd4d69c43ae2704d248703a1544956aea756462e0ff2867f6e |
| beginturnSlaver.fli | 38abcf43699db6ee35a321d48fd91f2b09c8e7dc0b186b2917d1da6f501c5efa |
| beginturnSciFew.fli | ae559effa370011f0d995caa305c8a20381b23a6d371ed72e1fa289dab8ad652 |
| beginturnSciMany.fli | 09b47e1fb4bd72c674c790f508a052077f1e5992fa50459bb423317fe2b68c0e |
| beginturnWarFew.fli | 32173fd7b373074efe12fa758b10ac27bf8509ca1216b900ea364d9303313b6b |
| beginturnWarMany.fli | 3fdf419769a44e63c1e53b6b15a18c6b71d4849882af85c08c2ea4ece3e2ca0a |
| beginturn.fli | bdb70672cfcbd757c1e71abdffb3a30f9d15dfaaba98f8d0f8bf9fddaaf40103 |

B2b registreert beide declarations passend bij de B2a-native inputs. Tijdens opening krijgt Theocracy rang1, Tyranny rang2; twaalf oude regeringsvoorwaarden schrijven alleen buiten opening. Default schrijft de openingvoorkeur; barbaren behouden hun oude route. De poll, steden-/goudfilters, techvoorwaarden en Anarchy-timer blijven origineel. Grootte40 blokkeert Theocracy als nieuwe kandidaat (threshold<=cities), geen bewezen automatische val van reeds actieve Theocracy. Daarom vóór40 overstappen, niet het filter tijdens deze proef veranderen.

## Kleinste noodzakelijke observeraanpassing

Hergebruik in een **eigen doel3-readerkopie** de bestaande PROEVEN/ai-uitlezen/Lees-Onderzoeksactivatie.py: uitsluitend ReadProcessMemory/OpenProcess0x410, huidige player/robot/AiMain/Science-ownerbinding, effective research list, herkeuzevlag, last_ai_request en engine_current. Laat de H1/H3-reader en actuele H1-uitvoerarm ongemoeid. Haar huidige variantlijst accepteert B2 niet: voeg geen onvertrouwde variant toe door controles uit te zetten.

De nieuwe binding accepteert uitsluitend originele DLL en gepinde N30-kandidaat. Controleer werkelijk geladen headers/SizeOfImage, de vijf hookwindows, volledige B2a-payload en gebruikte oorspronkelijke observerranges met de bestaande relocatieregels. Bind N30 aan kandidaat/payloadmanifest; een schijfnaam of positief menu is geen loaded-N30-bewijs. Geen algemene variant/plugin-interface bouwen. Test alleen de veranderde variantbinding en nieuwe scalarreads, niet opnieuw alle oude H3/goalfixtures.

Voor iedere bij T0 vastgelegde normale civ worden de volgende reeds analytisch gebonden velden toegevoegd:

| Waarneming | Mutatievrije bron en bestaand bewijs |
| --- | --- |
| Religion/Theocracy bekend | S=*(Player+12ec); K=*(S+1c); lees één byte K+advance-index. 4c2183→474b60; 474b7d/80 in ANALYSE/BINAIR/research-government-v2-parser-turn-route.txt. Engine-known retourneert de bytewaarde; nul=onbekend, niet-nul=bekend. Gebruik alleen geldige werkelijk geladen database-indices/namen, geen gegokte vaste indices. |
| Actieve regering | signed32 Player+94; 528f20, geschreven door4c3170 |
| Gevraagde regering en deadline | signed32 Player+11d8 en Player+11dc;4c2ee3..4c2f16 |
| Deadline voltooide ronde | Player+11ac en voltooiingsvlag+11e0;4b8660..6e en4b8a3d..6d |
| Actueel stadsantal | bestaande AiMain+8c-object eerste signed32, gebonden B2-beginturnroute; player-owned bestaande stadscontainer kan kruiscontrole geven |

Lezen vereist volledige bereik-/pointercontrole en twee overeenkomende snapshots aan een rustige grens. Null/verdwenen owner/instabiele toestand wordt UNKNOWN, nooit bekend/gov3 of verwijdering uit de meetgroep. De twee known-bytes sluiten de laatste mogelijke leeslacune: hiervoor is **geen aanvullende A** nodig. Er wordt geen native getter remote aangeroepen.

T0 leg civ-ID, naam en werkelijk normale AI-status vast; inventariseer alle deelnemende AI's en sluit uitsluitend mens/barbaren uit. De bestaande actorfilter alleen is onvoldoende als een civ later verdwijnt: behoud haar manifestregel en rapporteer verlies/niet-observeerbaar. Registreer per beurt onderzoektargets, known-bits, gov/doel/deadline en steden. Beurtlabel uit daadwerkelijke scherm/voortgang plus native verwerkte ronde; een meegegeven --turn-parameter bewijst zelf geen beurt. Geen GUI-technologie-/regeringswijziging voor het uitlezen.

## Twee identieke starts en bewijsgrens

QUOTA-START-T0 SHA256 **8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26**, Deity/Gigantic/8 spelers, vóór eerste beurt. Beschavingen niet uit het Welsh-voorbeeld afleiden: bij werkelijk laden complete deelnemersmanifest maken. Voor iedere arm nieuwe applicatie/manageropbouw. Native load van deze originele markerloze T0 en effectief lijst-/inputherstel zijn nog echte hostpoorten; geen savepatch of hot-reload als vervanging.

**Baseline A:** originele DLL3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44, originele acht onderzoeksprofielen uit B1-backups, oorspronkelijke inputs/beginturn/regeringsroute. **Variant B:** B1+B2a-N30+B2b. Executable SHA b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79, regels, overige aidata, quota en menselijke invoer gelijk. Dit is een expliciete combinatieproef van onderzoek+regering om doel3 te bewijzen; zij is geen afzonderlijke causale winstclaim voor ieder B2-hook. Bestaande quota-T60-saves zijn geen baseline hiervoor.

Mens passief in beide armen: geen stichting, beweging, queue, diplomatie of edit-acties; dezelfde gewone beurtvoortgang, observatie-/savehandelingen. Gebruik bestaande bedien- en save/loadroute; geen nieuwe UI-frameworkbouw. Begin met variant om de al voorbereide wijziging snel in echte autonome keuzes te beoordelen; voer vervolgens baseline tot hetzelfde resultaatmeetmoment uit. Beide armen vanaf exact T0, geen doorgespeelde H1-save hergebruiken.

Lees T0 en na iedere volledige gewone beurt tot de twee advances en actieve Theocracy voor alle deelnemers vastliggen. Bewaar checkpoints T25/T50/T60/T100 indien bereikt. **T60 is diagnosecheckpoint, T100 uiterste geplande eerste beoordelingspunt**, geen verzonnen garantie uit65-basiskosten. Zodra alle normale civs aan de uitkomst voldoen, kan de eerste vergelijking eerder stoppen; baseline komt tot exact dezelfde eindbeurt. Als T100 nog civs mist: doel NIET bewezen, vermeld per civ ontbrekend onderzoek, wetenschap/laatste target, native filter, deadline of uitval. Geen deadlineverlenging zonder gerichte verklaring en geen timeout als technisch onmogelijk verklaren.

Per civ rapporteer T0-known/current; iedere nieuwe autonome request/current-keuze; eerste Religion-known; eerste Theocracy-known; eerste aanvraagdoel3/Anarchy; deadline; eerste active3. Known-overgang tussen twee opeenvolgende snapshots geeft het gemeten beurtinterval; beweer geen exact intra-turn-eventtijdstip. Een civ die bijT0 iets al kende slaat die stap over, met expliciet T0-bewijs.

**Gameplay-PASS** vraagt voor iedere manifest-AI: effectieve B1-lijst op relevant herkeuzemoment; onbekende Religion eerst en Theocracy als eerstvolgende benodigde onbekende advance; beide werkelijk bekend; native aanvraag/Anarchy en active3 uiterlijk de bewezen eigen deadline/volgende rustige observatie. Bij bekendheid tijdens een AI-pass mag de eerste volgende poll nodig zijn: noteer feitelijk welke verwerkte ronde de aanvraag doet. Vergelijk alle civs met baseline; eerder leren/overschakelen waar baseline achterloopt, en declareer gelijke uitkomsten als gelijk, niet automatisch verbetering. Compleet doelbereik én veranderd gedrag moet uit trace blijken, niet uit prefix of rang alleen.

Neveneffecten: andere defensie-/transportadvances komen later; Anarchy kan tijdelijk productie/wetenschap remmen. Meet op de gelijke eindbeurt ook civuitval/stadsverlies en steden zodat die schade zichtbaar is. De inhoudelijke keuze Religion→Theocracy bestaat al; geen nieuw akkoord voor ieder bestand. Root beslist over afwijkende noodstrategie op basis van werkelijk gemeten schade.

## Eén voorwaardelijke functionele blokkade, geen preventief extra pakket

**B1-prefixen zijn plausibel maar geen harde garantie van de verlangde opeenvolging:** Choose_Next_Science20066ba0 kiest de eerste direct onderzoekbare kandidaat die kosten/max(1,science) < max_time_to_research haalt; een later snel item kan Religion/Theocracy passeren. Bekend geldig lopend T0-onderzoek loopt door. B2c verandert dezelfde suffixlijst en lost deze tijdtoets niet op.

Alleen als echte trace een normale herkeuze toont met target Religion/Theocracy onbekend/direct onderzoekbaar maar een later item gekozen, gaat precies deze bewezen selectorbranch terug naar A/B voor een minimale prioriteitscorrectie vóór de tijdtoets. Geen volledige prerequisitegraph of economy-reconstructie. De huidige proef wordt dan als niet-bereikt behouden; geen selectieve uitzondering tot PASS rekenen. Een lege/foutieve geladen lijst is een activatie-/routingfout, eveneens geen bewijs van technische onhaalbaarheid. Afwezigheid van broncode/helperrechten/tijd is geen harde onhaalbaarheid.

## Uitvoering, saves en herstel

C-voorbereiding mag nu eigen reader/binding/pakketmanifest gereedmaken en root laten reviewen. **Geen installatie terwijl huidige H1-arm leeft.** Wacht op haar bewezen normale exit/allcount0 en herstel van originele DLL. De specifieke éénmalige H1-machtiging is uitsluitend H1, geen machtiging om die live-instantie in B2 om te zetten of haar480s-grens op te rekken. Root hanteert voor deze benchmark de bestaande projectmachtiging en concreet gereviewde uitvoering; een reviewerweigering wordt gerapporteerd, niet omzeild.

Maak vóór installatie van beide armen bytebackups/hashmanifest van de echte werkbestanden, inclusief aanwezigheid/afwezigheid van twee nieuwe FLI's. Behoud alle gebruikerssaves en profielbytes. Controleer uiteindelijke gewijzigde set: acht research-AIPs, acht bestaande B2b-bestanden, twee nieuwe B2b-includes en één DLL; verder geen verschillen. CTP-og/AAIP blijven onaangeroerd.

Variant-save heeft per AI inline36byte B2record(version1,N30). Label iedere save met run-ID/N30 en eigen sha256; zij mag **niet** met originele DLL ofN25 geladen worden. Eén normaal save→normaal sluiten→zelfdeN30-versie laden→identieke known/gov/manifeststatus controleert herstelbare voortgang; opgelopen gebeurtenis-/beurtverschillen benoemen. Geen record handmatig aanpassen. Baseline krijgt eigen markerloze save en originele DLL. T0 blijft onaangetast en is de herstelstart.

Na arm: normaal sluiten, succesvolle exit/allcount0 vaststellen; originele werk-DLL/FLI's/AIPs naar echte pre-run-bytebackups herstellen, nieuwe includes alleen verwijderen indien vóór installatie afwezig. Eindhashes en behouden T0/profiel/saves vastleggen. Installatieversie, twee traces/saves, vergelijkingstabel en resultaatconclusie naar root voor VERSIES/PROJECTSTATUS. Geldige save/load en loader zijn noodzakelijke poorten, **geen zelfstandig afgerond gameplaydoel**.

Overdracht: bestaand C-pakket voldoende om de eerste echte doel3-proef te starten na readerreview en H1-afwikkeling. Geen nieuwe algemene analyse nodig. Volledige gameplay-PASS en verdere uitbreiding tot40 zijn nog niet aangetoond.
