# Hoe AIP-aanvragen samenkomen in de bestaande AI

Onderzocht op 4 oktober 2026 binnen fase A. De eerder onbekende gedeeltelijke profielwerking is nu voor de normale laad-/switchroute uit de overeenkomende AI-DLL gevolgd. Geen spel gestart, gameplaybestand veranderd of binary gepatcht. Dit document beschrijft bestaande werking, geen openings- of modvoorstel.

## Uitkomst

De AI bouwt één **samengestelde effectieve AIP-toestand** op. Een `action load` leest niet telkens een nieuw bestand van disk en vervangt niet automatisch het complete beleid. Zij zoekt een eerder ingelezen AIP-object en past alleen zijn aanwezige onderdelen toe:

- Reguliere scalars overschrijven hun eigen veld; ontbrekende velden blijven staan.
- `Build_List_Classes` vervangt het hele blok van eenheidsklassen, inclusief de bijbehorende unitlijsten. Klassen uit verschillende AIPs worden niet op naam bij elkaar gevoegd.
- Iedere gebouwcategorie, wonderlijst en de onderzoekslijst wordt afzonderlijk als hele lijst vervangen als die aanwezig is. Weggelaten categorieën blijven behouden.
- Actions lopen na de fuzzy regels in hun geregistreerde lijstvolgorde. Bij conflicten wint de laatste uitgevoerde schrijver van het betreffende onderdeel.
- Er is in deze beginbeurt-/actionroute geen algemene terugzetting naar default vóór iedere beurt. De toestand blijft bestaan totdat een volgende passende load onderdelen overschrijft; zij wordt bovendien in de save bewaard.

Er zijn belangrijke uitzonderingen: een aanwezige goallimiet met waarde `UNLIMITED = -999999` wordt in de switch niet gekopieerd; eval/exec-retreatlimieten worden juist na iedere switch op die sentinel gezet. 'Laatste schrijver wint' moet voor deze limieten dus met die uitzondering worden gelezen.

Vijftien offlinecontroles met originele DLL-instructies ondersteunen de beschreven switches, actionvolgorde, doelgrensexcepties en behoud. Dat is geen volledige fuzzy-parserproef of waarneming van het actieve profiel in de gespeelde T60-saves.

## 1. Bewijsroute en reproduceerbaarheid

Robotcom.dll en robotcom.map komen overeen op timestamp **37b894e7** en imagebase **20000000**. DLL SHA256: **3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44**. De aanroepen, branches en velden hieronder zijn uit de bijbehorende instructies gelezen. De niet-overeenkomende civctp.map is niet gebruikt.

Disassemblage is opnieuw te maken met [Analyseer-AI-DLL.py](../PROEVEN/Analyseer-AI-DLL.py). De unieke [aip-load-* bewijsbestanden](BINAIR/aip-load-switch-and-parser.txt) bevatten headers met hash/timestamp. Sommige functiebereiken bevatten springtabellen of padding; alleen de gecontroleerde codebranches gelden als bewijs.

De bestaande tekstinventaris blijft de bron voor welke velden een werkelijk bestand bevat: [profiel-velden.csv](INVENTARIS/profiel-velden.csv), [declaraties](INVENTARIS/declaraties.md), [ARCHITECTUUR.md](ARCHITECTUUR.md) en [QUOTA-EN-OVERRIDES.md](QUOTA-EN-OVERRIDES.md). Hieronder worden die declaraties aan de aangetoonde laadbetekenis gekoppeld.

## 2. Disk lezen gebeurt bij opbouw van de AIP-manager

`AiMain::Init` maakt de globale AIP-manager alleen wanneer `g_AIP_manager` nog nul is. De gewone laadroute `AiMain::Load` heeft dezelfde controle. Bij managerinitialisatie:

1. `AIP_Manager::Init` (20067030) maakt de lijst van AIP-objecten.
2. De routine zoekt het pad `%s\\AIPs\\*.aip` via FindFirstFile/FindNextFile en maakt per gevonden bestand een apart AIP-object.
3. Op **2006715b** wordt `AIP::Load_AIP_File` (200628d0) aangeroepen, met geforceerd lezen.
4. `Load_AIP_File` gebruikt de iparser, leest scalars, unitklassen, gebouwlijsten en advances en registreert welke onderdelen aanwezig zijn.
5. De manager zet op **20067207** zijn initialisatieflag. Een reeds geïnitialiseerde manager doet dit werk niet opnieuw.

Nieuwe spelinitialisatie maakt vervolgens de eigen Planner/AIP-toestand en vraagt op **20002202–2000220c** expliciet **default.aip** aan. Het laden van alle bestandsobjecten en het actief toepassen van default zijn dus afzonderlijke stappen. De filesystem-enumeratievolgorde bepaalt niet de latere overridevolgorde.

`AIP::Init` geeft een nieuw object ook ingebouwde numerieke beginwaarden en lege lijstvelden. Dat gebeurt bij constructie. Een gedeeltelijk bestand erft bij toepassing niet automatisch alle ingebouwde waarden van zijn bronobject: zijn aanwezigheidsflags bepalen welke velden werkelijk naar de effectieve AIP gaan.

Een gewone `Update_AIP` leest geen bestand, maar zoekt in de bestaande managerlijst op bestandsnaam en roept Switch_AIP aan. De gevonden vergelijker is bytegewijs en hoofdlettergevoelig. Bij geen match keert deze route terug zonder switch; er wordt daar niet alsnog van disk geladen of automatisch default toegepast. De offlinecontrole bevestigt ook een onbekende naam en een hoofdletterverschil als no-op.

Bewijs: [initialisatie](BINAIR/aip-load-init-and-save.txt), [init/load-aanroepers](BINAIR/aip-load-lifecycle.txt), [bestandslezen](BINAIR/aip-load-entrypoints.txt) en `Update_AIP`/`Look_Up_New_AIP` in [switch/parser](BINAIR/aip-load-switch-and-parser.txt).

### Levensduur van deze cache

De manager is gedeeld via een globale pointer en referentietelling. Init en Load verhogen die telling. `AiMain::Cleanup` verlaagt haar op **20002788–2000278e**. Bij nul roept zij op **200027a1** de managerdestructor aan en zet daarna op **200027af** de globale pointer terug naar nul. Daarna kan een volgende Init/Load bestanden opnieuw lezen.

Dit verfijnt de README-uitleg 'bij applicatiestart': de bewezen grens is **manageropbouw en -vrijgave**. Een save herladen terwijl die manager blijft bestaan herleest de AIP-bestanden niet via deze route. Niet onderzocht is welke concrete menu-/loadactie alle AI-objecten werkelijk opruimt. Een latere proef moet haar daadwerkelijke lifecycle controleren; deze code bewijst niet dat alleen een volledige applicatieherstart mogelijk is.

Bewijs: [managerlevensduur](BINAIR/aip-load-manager-lifetime.txt). De aparte `Load_All_AIPs_In_Directory` bestaat en kan bestanden lezen; haar normale runtime-aanroepcondities zijn niet vastgesteld. Zij is geen bewezen automatische hot-reload na ieder bestandssave.

## 3. FLI-regels en actions vormen twee opeenvolgende passes

Voor de normale beginbeurt roept `FSFuzzyBeginTurnRules::Execute` op **2003625b** `FireRules(2)` aan. Die functie doet voor de gekozen section:

1. Symbolen initialiseren via `FliSymTab::InitForSection` op **20039079**.
2. De rulelijst doorlopen en `FliRule::Evaluate` aanroepen op **200390a8**.
3. Pas na die rulepass de actionlijst doorlopen en `FliAction::Evaluate` aanroepen op **200390e6**.

Een action voert haar load dus niet uit op het moment dat de runtime langs de overeenkomstige tekstregel zou lopen. Haar vergelijkingsvoorwaarde wordt gelezen tijdens de aparte actionpass. Hoe de volledige rulepass fuzzy waarden berekent en sorteert blijft een afzonderlijk onderzoeksonderwerp.

`FliAction` herkent het actionwoord `load` via de constructor (200380ed–20038105). `_fli_EndAction` → `FliEngine::EndAction` voegt actions via **AddTail** aan de lijst van de section toe (20039503). AddTail koppelt het vorige einde aan de nieuwe node; FireRules loopt vanaf de kop via het nextveld. Er is in deze route geen sortering van actions op prioriteit. Hun **geregistreerde volgorde** is hiermee bewezen. De koppeling aan de tekstvolgorde in een gewone section volgt uit de registratiecallbacks en aanwezige declaraties; er is geen volledige parse van nieuwe gewijzigde FLI-bestanden in deze controle uitgevoerd.

Als de actionvoorwaarde true is, gaat `FliAction::Evaluate` naar `AIP_Manager::Update_AIP`, met de eigen effectieve AIP op `AiMain+0x94` (Planner) plus `0x20`. Die manager haalt het benoemde bronobject op en roept `Switch_AIP` aan. De gewone publieke `AiMain::Load_AIP` gebruikt dezelfde managerroute.

De symbolentabelinitialisatie is iets anders dan een AIP-reset. `InitForSection` wist per-symbol outputverwerking en kan geregistreerde sectionbeginwaarden terugzetten; de onderzochte code herinitialiseert daarmee niet de effectieve Planner/AIP. Bestaande inputwaarden worden niet zonder meer gelijk aan outputdefaults behandeld.

Bewijs: [actionregistratie/-evaluatie](BINAIR/aip-load-fli-actions.txt), [passes en AddTail](BINAIR/aip-load-action-order.txt), [callbacks en symbolentabel](BINAIR/aip-load-registration-and-reset.txt), [symbolen](BINAIR/aip-load-symbol-reset.txt) en [runtime-callers](BINAIR/aip-load-runtime-callers.txt).

## 4. Reguliere scalars: aanwezig is overschrijven, afwezig is behouden

De parser vult per veld een aanwezigheidsbit of -byte. Bijvoorbeeld `build_troops_priority`:

- Parsernaam op **2005f64e**, resultaat naar AIP+8 op **2005f699**.
- Het succes bepaalt aanwezigheidsbit 1 in AIP+0x740, op **2005f69e–2005f6b9**.
- `Switch_Simple_AIP_Priorities` test hetzelfde bit op **20062ad7–20062ae1**.
- Alleen bij aanwezigheid worden de twee helften van de double op +8/+0xc naar de effectieve AIP gekopieerd (**20062ae3–20062aec**).

`build_buildings_priority` gebruikt een eigen veld/presencebit en blijft bij een bron zonder dat veld dus behouden. Ook de integer `num_city_defenders` is afzonderlijk gebonden: parser schrijft +0x248 en aanwezigheidbit 10 op +0x748; de switch controleert dat bit en kopieert op **2006360b–20063611**.

Er wordt niet gemiddeld tussen twee profielwaarden. Een normale scalar uit een later uitgevoerd aanwezig profiel vervangt de eerdere waarde. De numerieke nul is een aanwezige waarde; ontbreken wordt door metadata bepaald, niet door 'waarde is nul'. Een bronobject kan ingebouwde fallbackwaarden bevatten die door ontbrekende aanwezigheid nooit worden toegepast.

De parsers ondersteunen onderscheid tussen gevonden en ontbrekende velden. Voor struct-arrays schrijft `Get_Struct_Array_Element_Count` bij ontbreken status 1/resultaat -1; bij een gevonden record status 0 en de count uit het record. `Load_Double_If_There`/`Load_Int_If_There` schrijven een succesvolle waarde en leveren een aanwezigheidresultaat. Fouttakken en de diagnostiek voor ontbrekende defaultparameters bestaan, maar het volledige gedrag bij ongeldige bestanden is niet hier getest.

Bewijs: [scalarbindingen](BINAIR/aip-load-scalar-bindings.txt), [switch/parser](BINAIR/aip-load-switch-and-parser.txt) en [parserstatus](BINAIR/aip-load-parser-status-and-values.txt).

## 5. Unitklassen vervangen als één blok; gebouw-/researchlijsten per categorie

`Load_Supplemental_Build_List_Classes` zoekt **Build_List_Classes** op. Alleen als het arrayrecord aanwezig is, bouwt de routine de klassentabel met de bijbehorende unitlijsten en zet bit 4 van +0x7ac. `Switch_AIP` test dat bit op **20063731–2006373c** en neemt op **20063760–20063772** de complete tabelpointer en het klassenantal over (+0x7bc en +0x7b0).

Er is hier geen append of zoekactie 'alleen dezelfde klassenaam vervangen'. Het aantal klassen en het ene tabelobject worden als geheel vervangen. Een nieuwe unitlijst declareren zonder bijbehorend toegepast klassentabelblok is daarmee niet bewezen als toevoeging aan het actieve beleid.

Gebouw-/researchlijsten hebben daarentegen hun eigen bits en pointers:

| Onderdeel | Bit op +0x7ac | Pointerveld | Switchbranch |
| --- | ---: | --- | --- |
| Build_List_Classes | 4 | +0x7bc, count +0x7b0 | 20063731–20063772 |
| Wonder_List | 5 | +0x7d0 | 20063778–200637cf |
| Transportation_List | 6 | +0x7d4 | 200637d5–2006382d |
| Growth_List | 7 | +0x7d8 | 20063833–2006388b |
| Happiness_List | 8 | +0x7dc | 20063891–200638e9 |
| Production_List | 9 | +0x7e0 | 200638ef–20063947 |
| Gold_List | 10 | +0x7e4 | 2006394d–200639a5 |
| Science_List | 11 | +0x7e8 | 200639ab–20063a03 |
| Defense_List | 12 | +0x7ec | 20063a09–20063a62 |
| Miscellaneous_List | 13 | +0x7f0 | 20063a68–20063ac1 |
| Advancements_List | 14 | +0x7fc | 20063b85–20063bde |
| End_Game_Object_List | 15 | +0x7f4 | 20063ac7–20063b20 |
| Capitalization_List | 16 | +0x7f8 | 20063b26–20063b7f |

De namen en velden zijn gebonden via `Load_Building_Build_Lists`/`Load_Scientific_Advancement_List`, niet alleen via aangenomen veldvolgorde. Per aanwezig onderdeel wordt de pointer van het bronobject gebruikt. Eigendomsbits op +0x7cc bepalen of oude eigen opslag eerst wordt vrijgegeven; de normale switch verwijst daarna naar de vooraf geladen bronlijst. Er is geen samenvoeging van lijstentries.

Een weggelaten lijst en een aanwezige lege lijst zijn verschillende situaties op objectniveau. De offlinecontrole bevestigt vervanging door een aanwezig leeg containerobject. De precieze tekstsyntax en parseracceptatie voor een nieuw leeg #DATA-blok zijn niet onderdeel van die controle en worden niet als al getest gepresenteerd.

Bewijs: [lijstbindingen](BINAIR/aip-load-list-bindings.txt) en de volledige [switch/parser](BINAIR/aip-load-switch-and-parser.txt).

## 6. Goallimieten hebben een afzonderlijke sentinelregel

`MAX_EVAL_SETTLE_GOALS` wordt naar +0x2d0 geschreven, met aanwezigheidbyte +0x751. `MAX_EXEC_SETTLE_GOALS` gaat naar +0x450, met aanwezigheidbyte +0x781. De arrayloop op **2006363d–200636a2** verwerkt eval- en execlimieten.

Daar kopieert de code alleen als:

```text
veld aanwezig EN bronwaarde != -999999
```

Het vergeleken doublepatroon is 0xc12e847e00000000, oftewel −999999. Nul en gewone negatieve waarden worden wel gekopieerd. Een gedeeltelijk profiel dat voor zo'n limiet UNLIMITED opgeeft, laat in deze switch dus de eerdere limiet staan. De betekenis bij de latere limietberekening in Update_Max_Goals is een andere stap: een sentinel die al in de effectieve AIP staat wordt daar speciaal behandeld.

Daarnaast schrijft de switch op **200636f9–2006370c** altijd −999999 naar +0x368/+0x4e8. De parserbindingen koppelen deze aan **MAX_EVAL_RETREAT_GOALS** en **MAX_EXEC_RETREAT_GOALS**. Dit zijn de expliciete uitzonderingen op algemene afwezig-behoudende scalarwerking.

De bestaande no_settle (0/0) en yes_settle (−30/−5) vallen niet onder de niet-kopiëren-sentinel: hun limieten worden bij aanvraag toegepast. Dit is codebewijs van overridewerking, niet van de feitelijke fuzzy aanvraag in een T60-save.

Bewijs: [scalarbindingen](BINAIR/aip-load-scalar-bindings.txt), [limietloop/reset](BINAIR/aip-load-switch-and-parser.txt) en [offlinecontrole](BINAIR/aip-load-controle.json).

## 7. Concrete bestaande samenstellingen en effect tussen beurten

Onderstaande voorbeelden combineren de echte declaraties met de aangetoonde switchwerking. Zij veronderstellen dat de genoemde loads worden uitgevoerd; zonder de fuzzy waarden zijn het geen vastgestelde profielen van een specifieke gespeelde beschaving.

| Uitgevoerde loads | Effect op de samengestelde toestand |
| --- | --- |
| scimany → masssettle | Masssettle vervangt de unitklassen. Science-/gebouw-/wonderlijsten die masssettle niet declareert blijven uit de vorige toestand. |
| masssettle → citywall | Unitklassen blijven staan; citywall vervangt Growth/Defense en zijn aanwezige gebouwscalars/drempels. Niet ieder gebouwlijstobject wordt verwijderd doordat een drempel verandert. |
| scimany → citywall_science | De Advancements_List wordt in haar geheel vervangen; dit is geen toevoeging van defensieonderzoek naast de bestaande prioriteitslijst. |
| naval → supernaval | Beide kunnen bij volheid >0.9 worden aangevraagd. In de geregistreerde normale loaderreeks staat supernaval later en vervangt bij uitvoering het unitklassenblok van naval. |
| no_settle → yes_settle | Als beide actions uitvoeren, zetten de latere yes-limieten 30 evalueren/5 uitvoeren. Dit zegt niet dat beide fuzzy voorwaarden werkelijk tegelijk true worden. |
| Geen nieuwe load voor een eerdere tijdelijke categorie | Die categorie wordt door afwezigheid niet teruggezet. Een volgende toepasselijke basis-/tegenmode moet haar expliciet vervangen. |

De gewone aiploader bevat bijvoorbeeld afzonderlijke sally/nosally, lowdist/highdist, persoonlijke basisloads, masssettle, citywall, survival, naval/supernaval, oorlogsmodes, no/yes_settle, verkenning, troop-on/off en een late citywall_science-action. Citywall komt tweemaal als action voor. De volgorde en veldoverlap doen er dus toe; een profieltitel 'mode' garandeert geen geïsoleerde tijdelijke werking.

De reguliere persoonlijke AIP's worden via loadercondities opnieuw aangevraagd wanneer hun basisroute geldt. Daarmee kunnen hun aanwezige categorieën eerdere tijdelijke inhoud vervangen. Maar niet iedere basisload is iedere beurt gegarandeerd, en een gedeeltelijke basis zoals masssettle reset weggelaten research-/gebouwonderdelen niet. De effectieve toestand hangt daarom af van de uitgevoerde geschiedenis, niet uitsluitend van het laatst gekozen bestandslabel.

`Switch_AIP` kopieert op **20063be4–20063c0b** de naam van het laatst toegepaste bronobject naar +0x804. `GetCurrentAIPname` op 20066c80 leest precies dat naamveld; zie [naamgetter](BINAIR/aip-load-current-name.txt). **Die ene naam beschrijft niet alle nog behouden onderdelen.** Voor latere debugwaarnemingen is alleen 'current AIP = citywall_science' daarom onvoldoende bewijs van unit-, gebouw- of vestigingsbeleid.

De offline FireRules-controle laat de originele action/lookup/switchketen op synthetische symbolen uitvoeren en herhaalt de section met alle loads false. De effectieve toestand blijft in die tweede uitvoering exact behouden. Dat bevestigt de beschreven route zonder elke echte conditionele FLI-situatie te simuleren.

## 8. Samengestelde AIP-inhoud wordt in de save bewaard

`Planner::Serialize` roept op **2006e579** `AIP::Serialize` aan voor het eigen object op Planner+0x20. Die schrijft/leest op **20065486–2006549b** een blok van **0x7b0 bytes**, waaronder scalarwaarden en aanwezigheidsmetadata. Daarna volgt `AIP_Ptr_Data::Serialize` op **200654a5** voor de variabele lijstgegevens.

De pointerdata-serializer bewaart klassenaantal en iedere Build_List_Class, plus aanwezige gebouw-/wondercontainers en de advance-lijst. De leesbranch op **20065318** en verder maakt de opslag opnieuw aan, leest de unitklassen via hun serializers, de gebouwlijsten via Load_Building_List en de advances via Load_Science_List. Op **20065444–20065452** leest zij ook de opgeslagen naam. Een save bewaart dus de concrete samengestelde inhoud, niet slechts een bestandsnaam die alle onderdelen automatisch opnieuw uit disk haalt.

De `AiMain::Load`-route bouwt de eigen Planner via de archiveconstructor op **20003b5b**. Daarnaast kan zij de bron-AIP-manager opbouwen als die nog ontbreekt. Dat zijn twee lagen: **herstelde effectieve AIP** en **beschikbare bronprofielen voor volgende actions**. Nieuwe loads kunnen na laden onderdelen door nieuw ingelezen broninhoud vervangen; ongeschreven onderdelen blijven mogelijk uit de save. Er is in de onderzochte AIP-loadroute geen algemene default-switch na archiveherstel aangetoond.

Dit is gerichte disassemblage van serialisatie, geen nieuwe volledige Unicorn-saveproef of controle van een echte geladen AIP-toestand. Eventuele verdere applicatie-/enginecalls na laden zijn niet volledig gevolgd. Bewijs: [lifecycle en pointerserialisatie](BINAIR/aip-load-lifecycle.txt), [AIP-serialisatie en constructors](BINAIR/aip-load-init-and-save.txt).

## 9. Offlinecontrole en begrenzing

[aip-load-controle.py](BINAIR/aip-load-controle.py) mapt een kopie van de originele DLL in Unicorn en maakt uitsluitend synthetische objecten. Zij voert Switch_AIP, Switch_Simple_AIP_Priorities en in een aparte controle FireRules/FliAction/Update_AIP uit. Resultaat: **15 van 15 controles geslaagd**, in [aip-load-controle.json](BINAIR/aip-load-controle.json).

Gecontroleerd: afwezige geselecteerde velden behouden, scalaire overschrijving, volledig unitklassenblok vervangen, onafhankelijke Growth/Defense, researchvervanging, aanwezig leeg object, goallimieten nul/normaal negatief/sentinel/afwezig, vaste retreatreset, twee opeenvolgende schrijvers, true-only actionvolgorde, geen reset bij volgende section zonder load en geen switch bij onbekende/anders gecaseerde naam.

Grenzen: de parser heeft niet echte AIP-bestanden voor deze voorbeelden ingelezen; fuzzy regels zijn leeg en symboolwaarden staan vast; OS/timing/logging en sectioninitialisatie zijn gestubd; de bestemming heeft geen vrij te geven oude owned-lijsten; unitlijstinhoud, allocatorfouten en volledige applicatie-/save-/gameplayroutes worden niet gesimuleerd. De directorylifecycle, parseraanwezigheid en serialisatie zijn afzonderlijk met de echte disassembly onderbouwd. Er is geen prestatieverbetering gemeten.

## 10. Resterende vragen en noodzakelijke actualisaties

Dit onderzoek sluit de belangrijkste vraag 'gedeeltelijke vervanging of samenvoeging?' voor de normale AIP-route. Het lost nog niet op:

- Welke fuzzy waarden en baseloads een specifieke beschaving op een specifieke beurt krijgt; rulevolgorde, defuzzificatie en sectionstatus zijn nog geen volledig model.
- Welke volledige applicatieroute bij herladen de manager vernietigt, herbouwt of aanvullend profileswitches doet.
- Hoe ongeldige/lege tekstlijsten en parserfouten in alle gevallen worden afgehandeld; alleen het aangetoonde objectniveau is gecontroleerd.
- Hoe de nieuwe effectieve instellingen bestaande queues en reeds gemaakte goals beïnvloeden; load/switch verandert profieldata, niet bewezen onmiddellijk alle acties/voorraden.
- Hoe de onderzoekslijst vervolgens een concrete advance kiest en hoe de normale bouwscheduler de aanvragen toewijst.

De oudere onzekerheden in ARCHITECTUUR.md, QUOTA-EN-OVERRIDES.md, GEDEELDE-OPENING.md, DEKKING.md en BESLISKETENS-OVERZICHT.md moeten bij actualisatie naar dit nieuwe bewijs verwijzen. Vooral 'lijsten samenvoegen', 'alleen laatst gekozen AIP bepaalt beleid' en 'iedere beurt automatisch terug naar default' mogen niet als huidige werking worden aangenomen. De hoofdagent beheert die bestaande documenten; zij zijn voor deze deelopdracht niet aangepast.

Het volgende gerichte analysetraject kan de nu bekende effectieve researchlijst verbinden met de daadwerkelijke advancekeuze. Economy/growth, terrein/popplaatsing, handelsvoorraad en militaire matching blijven eveneens onderdeel van de nog niet afgeronde brede fase A.
