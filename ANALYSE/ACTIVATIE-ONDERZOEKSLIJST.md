# Alleen-lezen activatiecontrole van de onderzoekslijst

Bijgewerkt: 7 oktober 2026, 20:14 Europe/Amsterdam. Afgebakende A2-analyse voor B1; geen runtimewaarneming en geen bewijs dat QUOTA-START-T0.sav met B1 een nieuwe onderzoekslijst gebruikt.

## Uitkomst

Coördinatorcontrole7 oktober20:20: [Controleer-Decoder.py](../PROEVEN/ai-uitlezen/Controleer-Decoder.py) geslaagd met6 beperkte synthetische gevallen; [resultaat](../PROEVEN/ai-uitlezen/decoder-results.json). Verplaatste modulebasissen/naamlookup en verschil tussen laatste AI-aanvraag en engine-current worden gecontroleerd, evenals afwijzing van verkeerde civ-/AIP-eigenaar, te lange lijst en ongeldige advance-index. Geen echt proces geopend; Windows-module-/handlecontroles en live velden blijven onbewezen. Statische review van main toont alleen QUERY_INFORMATION/VM_READ en voorafgaande exacte proefpad-/hashchecks; geen geheugenwrites of spelstart. Geen brede foutpaddekking of atomair snapshot geclaimd.

Coördinatorreview7 oktober20:17: rapport en voorbereide helper gelezen; Python-AST-syntaxcontrole geslaagd zonder proces te openen. Canonieke managercaller51c6ea/51c6f4 en de32-civ-loop (52dce6:cmp edi,0x20) rechtstreeks in bestaande dumps gecontroleerd, evenals actuele onderzoeksstore475f68. Dit vervangt geen decoder-/foutpadcontrole of live validatie. De eerdere tekst hieronder over nog niet gecontroleerde syntax beschrijft de analistenoverdracht; die beperkte syntaxstap is inmiddels uitgevoerd.

Er is een canonieke objectketen gevonden waarmee een gecontroleerd CTP-proef-proces per AI de **effectieve opgeslagen onderzoekslijst**, **herkeuzevlag**, **laatste AI-aanvraag** en **actuele engine-onderzoeksindex** kan tonen. Een bronbestand of de laatst gebruikte AIP-naam bewijst deze activatie niet. Een geheugenscan naar mogelijk oude objecten is niet nodig.

De hieronder genoemde adressen zijn de voorkeursadressen van de originele binaries. De engine-map is niet gebruikt; robotcom.map past bij de DLL. Een runtimelezer moet modulebasissen corrigeren en eerst de exacte executable-/module-identiteit controleren.

## Canonieke civ- en objectbinding

De echte engine-savecaller leest op **51c6ea** de manager uit **globaal A7DDB8** en roept op **51c6f4** de functie **52dbe0** aan. Die functie gebruikt op **52dc75–7b** dezelfde civ-index `edi` voor de Playerstable uit **A7DD80**. Zij haalt op **52dcc2** het RobotCom-object op uit **manager+220c+4*civ**, en roept op **52dccd** zijn Load-slot **+10** aan. De overeenkomstige DLL-functie **2000fe40** geeft dit door aan AiMain::Load, via **RobotCom+8**. Constructor **2000fcc0**, store **2000fd04**, bindt dat veld aan AiMain; de RobotCom-vtable is **20089728**.

Dit is een ownerketen vanaf een echte manager, geen toevallige heapmatch. De engine-loop sluit een civ zonder Player of met niet-nul **Player+1190** uit. De betekenis van dat uitsluitveld wordt hier niet nieuw benoemd. De observer volgt dezelfde actorfilter.

Aanvullende eigenaarschecks: **AiMain+20** komt in Init van GameState-slot+0c (**20001ba4–a7**); **AiMain+44** bevat de Science-interface. De echte Science-constructor **5309b0** bewaart de civ-index op **Science-interface+0c**, en haalt de Player uit **[A7DD80][civ]** voor **+8**. Haar vtable is **744fe0**. Deze drie civ-/Playerbindingen moeten overeenkomen.

Bewijs: [exacte savecallercontext](BINAIR/research-activation-final-binding.txt), [volledige manager-loadfunctie en actuele setter](BINAIR/research-activation-engine-load-and-current.txt), [originele COM-layout](BINAIR/research-activation-com-and-layout.txt), [bestaande AiMain-init](BINAIR/terrain-food-ai-interface-init.txt), [Science-constructor](BINAIR/research-government-engine-construct-change.txt). De voorlopige contextstarts **51c6b0**, **52d5d0** en **52dc72** vallen niet allemaal op instructiegrenzen; deze prefixes leveren geen bewijs. De conclusies gebruiken de afzonderlijk benoemde geldige instructies en de volledige functie **52dbe0**.

## Effectieve lijst en onderzoeksstatus

| Gegeven | Alleen-lezen route | Bewijs |
|---|---|---|
| Eigen effectieve AIP | AiMain+94 → Planner; AIP is Planner+20 | Bestaande [AIP-laadwerking](AIP-LAADWERKING.md) en ResearchScience20025d80 |
| Lijstcontainer | AIP+7fc | Choose_Next_Science20066bab |
| Aantal en data | container+4: aantal; container+0: datapointer; data+4*i: signed advance-index | 20066bb9,20066bdb,20066be0 |
| Eigenaarscontrole | AIP+800 moet terug naar dezelfde AiMain wijzen | 20066bd5 en bestaande parser |
| ScienceAgent | AiMain+120 | Init20002071 en Load20003822; bestaande analyseroutes |
| Herkeuze | ScienceAgent+b8 | FSAllocScience200376d0; alleen niet-nul roept ResearchScience aan |
| Laatste AI-aanvraag | ScienceAgent+bc | ResearchScience20025d80; kan -1 zijn |
| Actueel engineonderzoek | Player+12ec → Advances; Advances+8 | Science-slot+24→530bb0→4bbad0→475f60; store475f68 |

De laatste AI-aanvraag en het actuele engineonderzoek worden apart gerapporteerd. ScienceAgent+bc is geen zelfstandige garantie dat de engine dezelfde keuze verwerkt heeft. De rechoosevlag bepaalt bovendien of een nieuwe lijst meteen een nieuwe aanvraag kan veroorzaken. De save herstelt de effectieve AIP en deze ScienceAgent-status; gewijzigde bronprofielen zijn een andere laag.

De lijstlayout is eerder gecontroleerd met originele Choose_Next_Science-instructies in [Controleer-Onderzoekskeuze.py](../PROEVEN/Controleer-Onderzoekskeuze.py). A2 voegt geen nieuwe gameplayproef of herhaling van die testserie toe. Zie [bestaande keuzeanalyse](ONDERZOEK-EN-REGERINGSKEUZE.md) en [originele keuzefunctie](BINAIR/research-government-ai-chain.txt).

## Index naar werkelijk ingelezen advancenaam

Science-slot **+50**, **530e50**, zet de naam eerst via **StringDB[A7DCFC]**, lookup **4660f0**, om naar een string-ID. Vervolgens zoekt **44cd20** deze ID in **AdvanceDB[A7DD00]**. Dat object heeft **count+0**, **records+8**, stride **8c**; ieder record begint met de string-ID. Omgekeerd haalt **44cd60** de ID van een bepaalde recordindex op en roept **466320** aan. Die gebruikt **StringDB+4** als pointerarray, kiest `array[string_id]` en retourneert **entry+8**, de naamstringpointer. Daardoor hoeft de lezer tekstregelvolgorde niet gelijk te stellen aan runtime-indexen.

Bewijs: [Science-slots en naamlookup](BINAIR/research-activation-engine-entry.txt), [AdvanceDB-lookup](BINAIR/research-activation-engine-research-name.txt), [exacte stringgetter](BINAIR/research-activation-final-binding.txt), [bestaande AIP-parser](BINAIR/research-government-list-parser.txt).

## Voorbereide observer en grens

[Bind-Onderzoeksactivatie.py](../PROEVEN/ai-uitlezen/Bind-Onderzoeksactivatie.py) leest uitsluitend originele bestanden en produceert de gerichte offline disassemblage. Geen proces wordt geopend. Originele SHA256-identiteit wordt vooraf gecontroleerd.

[Lees-Onderzoeksactivatie.py](../PROEVEN/ai-uitlezen/Lees-Onderzoeksactivatie.py) is vóór de afrondingsinstructie geschreven, maar **nog niet statisch uitgevoerd/gecontroleerd, synthetisch getest of in een echt CTP-proef-proces gevalideerd**. Deze helper is een voorbereid artefact; hij mag pas na die resterende controle als uitvoerbare uitleesroute worden gebruikt. Hij vraagt alleen QUERY_INFORMATION/VM_READ, controleert het exacte CTP-proef-executablepad vóór geheugenlezen, hercontroleert dat pad op het readhandle, vereist exacte engine-/DLL-modulepaden en originele schijfhashes, vergelijkt geheugenheaders, begrenst indices/geheugenlezingen en vereist twee gelijke waarnemingen. Hij start/sluit geen spel, schrijft geen geheugen en installeert geen hook. Het D:\CTP-proces is niet geopend of uitgelezen.

Hervatpunt: controleer eerst syntax en de kleine pure `observe`-decoder offline, beoordeel identiteit-/foutpaden en valideer daarna uitsluitend bij een toegelaten CTP-proef-proces de module- en objectketen. Houd het spel op een rustig beurtgrensmoment. Twee gelijke samples zijn geen atomair enginesnapshot. De lezer bewijst evenmin welke save geladen is; daarvoor moet de uitvoerder de exacte startsave en laadhandeling afzonderlijk vastleggen.

Voor B1 zijn vervolgens drie waarnemingen nodig: direct na laden van exact dezelfde startsave, na een toegelaten AIP-switch en na een echte herkeuze. Vergelijk de effectieve lijst met de B1-volgorde; noteer rechoose, laatste aanvraag en engine-current afzonderlijk. A2 wijzigt geen lijst/vlag/save en schrijft geen resultaat van deze toekomstige proef vooruit.
