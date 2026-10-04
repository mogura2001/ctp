# Onderzoek en regeringskeuze in de bestaande CTP I-AI

Analyse van 4 oktober 2026, fase A. Originele gamebestanden en binaries zijn alleen gelezen; geen spel gestart. Dit pakket verklaart de concrete keuzeketen en levert geen toegepast voorstel. De brede fase A is hiermee niet afgerond.

## 1. Uitkomst en bewijsgrenzen

De effectieve `Advancements_List` bepaalt een geordende lijst van kandidaten. De AI kiest de eerste onbekende, direct onderzoekbare advance waarvan de totale enginekosten gedeeld door actuele wetenschapsuitgaven onder haar tijdsgrens vallen. Als geen geschikte kandidaat snel genoeg is, kiest zij alsnog de eerste direct onderzoekbare advance. Zij zoekt in deze normale route geen ontbrekende prerequisite voor een niet onderzoekbaar lijstitem. Religion en Theocracy achtereenvolgens kunnen daarom alleen gekozen worden als de benodigde advances zelf bruikbaar in de effectieve lijst voorkomen.

Onderzoek unlockt een regering; een aparte regeringspoll kiest die regering aan de hand van fuzzy rangen en filters. Een hoge onderzoekspositie voor Theocracy is dus geen opdracht om haar ook als regering te gebruiken. Profielwisselingen onderbreken in de onderzochte route evenmin een lopend onderzoek.

Bewijsniveaus: **T** = tekstconfiguratie, **B** = oorspronkelijke machinecode, **E** = offline uitvoering van oorspronkelijke instructies met synthetische gegevens. Er zijn hier geen nieuwe runtimewaarnemingen. `robotcom.map` past bij DLL-timestamp `37b894e7`, imagebase `20000000`, SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`. Engine-adressen komen uit werkelijke interfaceconstructors/tabellen in `civctp.exe`, timestamp `37d6f702`, imagebase `400000`, SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`; de niet passende engine-map is niet gebruikt. Zie [enginebindingen](BINAIR/research-government-engine-tables.txt).

## 2. Van bestandslijst naar effectief AIP

De reeds bewezen [AIP-laadwerking](AIP-LAADWERKING.md) geldt ook voor onderzoek: een aanwezige onderzoekslijst vervangt deze categorie volledig; een ontbrekende lijst behoudt de effectieve lijst. Er is geen samenvoeging van advances en geen algemene reset bij iedere nieuwe beurt. De laatste toepasselijke schrijver van deze categorie bepaalt de lijst; de laatst geladen bestandsnaam beschrijft niet alle effectieve onderdelen.

`Load_Scientific_Advancement_List`, `2005f380`, leest de arraygrootte, haalt per index `advancement_name` op en laat `AiMain+44`, vtableslot `+50`, de naam naar een engine-index omzetten (`2005f4a4`). De lijst wordt een array van vierbyte-indexen in dezelfde volgorde. De pointer staat op AIP `+7fc`; aanwezigheid gebruikt bit14 op `+7ac`. Zie [parser](BINAIR/research-government-list-parser.txt). Ongeldige advancenamen en parserfouten zijn hier niet getest.

**T:** posities in de bestanden, vanaf 1 geteld; deze positie is geen voorspelling van de gekozen beurt. De complete tekstextractie staat in [lijstvolgorden](BINAIR/research-government-list-orders.json).

| Lijst | OG Religion / Theocracy | AAIP Religion / Theocracy |
| --- | --- | --- |
| default | 7 / 97 | 7 / 98 |
| cleric | 2 / 1 | 5 / 1 |
| milmany | 7 / 97 | 7 / 16 |
| milfew | 12 / 98 | 4 / 16 |
| scimany | 15 / 96 | 5 / 15 |
| scifew | 7 / 97 | 6 / 17 |
| slaver | 13 / 19 | 14 / 9 |
| citywall_science | 7 / 97 | 7 / 97 |
| noscience | lege lijst | lege lijst |

AAIP schuift Theocracy voor meerdere persoonlijkheden naar voren, maar laat `citywall_science` met haar late Theocracy staan. Een toepasselijke override kan dus de eerdere verbetering vervangen. De `cleric`-volgorde Theocracy vóór Religion is functioneel mogelijk: de niet beschikbare Theocracy wordt eerst overgeslagen, Religion kan gekozen worden; bij een volgende herkeuze kan Theocracy beschikbaar zijn. Dit is afleiding uit T+B, geen gemeten AAIP-resultaat. De profielaanvraagroute blijft beschreven in [architectuur](ARCHITECTUUR.md), [AAIP-lessen](AAIP-LESSEN.md) en [gedeelde opening](GEDEELDE-OPENING.md).

## 3. Wanneer wordt opnieuw gekozen?

`FSAllocScience::Execute`, `200376d0`, controleert ScienceAgent `+b8`. Alleen als die vlag niet nul is, roept zij `ResearchScience` (`200376e8`) aan. Die haalt het effectieve AIP uit `AiMain+94`, Planner `+20`, en roept `Choose_Next_Science` aan (`20025d94`). Bij een geldige keuze stuurt zij de index naar Science-interface `+24` en bewaart deze op ScienceAgent `+bc`; zij zet de herkeuzevlag vervolgens op nul. Bij geen kandidaat bewaart zij `-1` en zet eveneens de vlag op nul. Zie [normale route](BINAIR/research-government-science-route.txt) en [keuzefuncties](BINAIR/research-government-ai-chain.txt).

`ScienceAgent::Init`, `20023ac0`, begint met `+b8=1` en `+bc=-1`. `RegisterLearnedScience`, `20025de0`, zet de vlag opnieuw wanneer het huidige doel ongeldig/buiten bereik/bekend is. Er staat daarbij letterlijk een `<=0`-test op de huidige advance-index; index0 krijgt dezelfde herkeuzebehandeling als een ongeldige index. Wanneer een andere advance wordt geleerd terwijl een geldig huidig doel nog onbekend is, blijft de vlag in deze eventroute ongewijzigd. De event werkt tevens de kennisadministratie bij. Wanneer alle advances zijn geteld als geleerd, zet zij de vlag weer nul. `ScienceAgent::BeginTurn`, `20024420`, is alleen een `ret`.

De onderzochte AIP-switch wijzigt de lijst en zet deze ScienceAgent-vlag niet. Daarom is het vervangen van de lijst tijdens een beurt geen onmiddellijke onderzoeksannulering. Een lege effectieve lijst geeft bij een herkeuze `-1`; daarna zorgt uitsluitend een later ander AIP laden in de onderzochte route niet voor een nieuwe poging. Alle overige mogelijke schrijvers van deze vlag zijn niet uitputtend onderzocht.

`ResearchNext`, `20025cb0`, bevat een aparte graf-/prerequisiteanalyse, maar de [directe crossreferences](BINAIR/research-government-xrefs.txt) vinden geen aanroep daarvan. De normale aangetoonde keuzeketen gebruikt deze functie niet. Een aanwezige functienaam bewijst geen actieve plannerroute; eventuele indirecte aanroepen zijn hiermee niet uitgesloten.

## 4. Exacte selectie van een advance

**B:** `AIP::Choose_Next_Science`, `20066ba0–20066c7d`:

1. Geen lijst of lege lijst: retourneer `-1`.
2. Loop de indices in lijstvolgorde.
3. Science-interface `+20` niet nul: advance is al bekend; overslaan (`20066be7–bec`).
4. Science-interface `+3c` moet exact **1** retourneren; anders overslaan (`20066bfb–c01`).
5. Bewaar de eerste aldus toegelaten advance als fallback (`20066c03–c09`).
6. Haal totale enginekosten via interface `+40` op. Deel deze door `max(1, AiGold+18)`.
7. Is die verhouding **strikt kleiner** dan `fz_max_time_to_research`, kies onmiddellijk deze advance (`20066c48–c55`). Gelijkheid valt buiten deze snelle keuze.
8. Is het einde bereikt zonder snelle keuze, retourneer de fallback; zijn er geen toegelaten advances, retourneer `-1`.

Dus een later goedkoop item kan een eerder duur item passeren, maar alleen doordat de eerste de tijdsgrens mist. Het algoritme zoekt niet het goedkoopste item van de hele lijst. De fallback voorkomt dat alle direct onderzoekbare advances wegens lange onderzoeksduur worden geweigerd.

`InitFuzzyOut` registreert `max_time_to_research` op `2003ea4a–54`, met beginwaarde **100** en outputtype1. In de originele aidata is geen aparte tekstdeclaratie van deze naam aangetroffen. De registratie is geen bewijs dat iedere save of ieder later fuzzy moment nog exact100 heeft. Zie [binding](BINAIR/research-government-fuzzy-bindings.txt) en [referenties](BINAIR/research-government-threshold-binding.txt).

De deler is actuele **wetenschapsuitgave**, niet de abstracte prioriteit `sci_*` en niet direct een specialistenaantal. `AiMain+ c8` is `AiGold`; `SetGoldLevels`, `2000e7e0`, vult `AiGold+18` via Player-slot `+dc`. Dat slot is `528260`, dat de finance-administratie uitleest via `4a70a0`; de zesde aangeleverde resultaatpointer krijgt finance `+20`. `GetExpenses` gebruikt hetzelfde AiGold-veld voor de vijfde expense-ratio, en `FSFuzzyBeginTurnPre` bindt die aan `income_expense_science` (`200350e7`, `20035100`). Zie [budgetroute](BINAIR/research-government-budget-beginturn.txt), [inputbinding](BINAIR/research-government-income-input.txt), [enginegetter](BINAIR/research-government-gold-income-binding.txt) en [financekopie](BINAIR/research-government-gold-write.txt). Dit benoemt de invoer; de volledige berekening van netto science en budgetverdeling blijft een afzonderlijke economieketen.

## 5. Enginevoorwaarden en Religion → Theocracy

**B:** GameState-slot `+4c`, `526020`, levert het object uit GameState `+28`; de constructor `5309b0` zet vtable `744fe0`. De overeenkomende DLL-init plaatst dit object in `AiMain+44`. Government komt via GameState-slot `+2c`, `525fd0`, uit `+2c`; constructor `5261c0` zet vtable `7444f0`, DLL-init plaatst dit in `AiMain+48`. Zie [getters](BINAIR/research-government-engine-getters.txt), [constructors](BINAIR/research-government-engine-construct-change.txt), [bestaande GameState-opbouw](BINAIR/food-growth-gamestate-construct.txt) en [bestaande DLL-init](BINAIR/terrain-food-ai-interface-init.txt).

Science `+20` → `530bd0` → Player `4c2180`: bekende-advancecontrole. Science `+3c` → `530d30` → `475c00`: retourneert nul voor een bekende advance, anders **1 + de recursieve aantallen van alle nog onbekende prerequisites**. Een onbekende advance zonder ontbrekende prerequisites geeft dus1. De functie telt gedeelde prerequisitepaden recursief en dedupliceert die niet zichtbaar; voor de AI-filter `==1` is vooral het ontbreken van enige onbekende prerequisite bepalend. Zie [enginevoorwaarden](BINAIR/research-government-engine-availability.txt).

Science `+40` → `530d50` → `475990`: totale kosten uit de engine. De functie gebruikt advance-recordkosten `+58`, reeds bekende advances, een verdere coefficient en mogelijk een aftrek, gevolgd door verschillen tussen de speler-/difficultyroute. Het volledige benoemen van die kostencorrecties is hier open. De selectie gebruikt deze uitkomst; zij deelt niet simpelweg de basiskosten uit `advance.txt` door science.

**T:** [advance.txt](../CTP-og/ctp_data/default/gamedata/advance.txt) heeft een eigen Religionrecord vanaf regel149, zonder vermelde prerequisite en met `ADVANCE_COST65`; Theocracy vanaf221 vereist Religion en kost65. Beide ontbreken: opgetelde **basiskosten130**. De eerdere waarde20/pad85 in de vroege strategieanalyse was onjuist en is bij de eigenaar gemeld. Basiskosten130 bewijzen geen Deity-beurttal of werkelijk betaalde kosten.

**T:** [govern.txt](../CTP-og/ctp_data/default/gamedata/govern.txt) koppelt Theocracy aan `ENABLING_ADVANCE ADVANCE_THEOCRACY`. Government-slot `+68`, `526590`, haalt de enabling index uit het record via `464840`, veld `+8`. `WillOfThePeople` initialiseert per regering een beschikbaarheidsvlag via deze enabling index en Science `+20` (`2005d340–363`); op `RegisterLearnedScience`, `2005e4d0`, zet zij beschikbaar op1 wanneer de enabling advance de nieuw geleerde index is of `-1`. `AiMain::RegisterLearnedScience`, `20005300`, stuurt hetzelfde event naar zowel ScienceAgent als WillOfThePeople. Dit is de concrete koppeling tussen geleerd onderzoek en regeringsbeschikbaarheid; het levert nog geen voorkeur voor die regering op.

## 6. Welke regering wil de AI?

**T:** [set_govern.fli](../CTP-og/ctp_data/default/aidata/set_govern.fli) vraagt bij nul of1–5 steden Tyranny. Daarboven verschillen de ranglijsten per persoonlijkheid, oorlog/vrede, focus op units en wormhole-probe. Theocracy staat alleen in de clericregels; gewone warrior/scientist/slavervoorkeuren noemen haar niet. [outputs.fli](../CTP-og/ctp_data/default/aidata/outputs.fli) declareert de rangen met beginwaarde `-1`: een gewone rang1 is gewenst boven rang2; `-1` betekent geen reguliere kandidaat.

**B:** de concrete rangbuffer staat op `200c64f0 + regeringindex*8`. Theocracy-output bindt op `200411f5–ff` buffer `200c6508`, index3, overeenkomend met de originele recordvolgorde. `RankGovernment`, `2005e520`, leest deze double en rondt voor de gewone indices naar de dichtstbijzijnde integer, halve positieve waarden naar beneden; het resultaat wordt een signed byte. Geen positieve rang: niet selecteerbaar in de normale poll. Regeringen vanaf index12 krijgen intern standaardrang1; de originele tabel heeft indices0–11.

Een concrete afwijking in deze binary: **`i_want_this_gov_FASCISM` en `i_want_this_gov_COMMUNISM` registreren beide dezelfde pointer `200c6528`**, respectievelijk op `2004127c–86` en `20041297–a1`. Dit is rangbufferindex7, de originele Fascism-index; Communism staat in `govern.txt` op index6. De tekstnamen vormen dus geen twee onafhankelijke bufferplaatsen. Hoe overlappende fuzzy outputs bij defuzzificatie/reset exact combineren, en wat er in bestaande saves op index6 staat, is nog open. Er wordt hier geen gemeten verwisseling van regeringen geclaimd.

## 7. Poll, harde filters en beslisactie

`FSWillOfThePeople::Execute`, `2002af20`, roept `PollNewGov`, `2005e3b0`, aan. Die actualiseert stats, haalt de actieve regering op via Player-slot `+150`, en loopt kandidaten **index1 tot aantal−1**. Zij sluit Anarchyindex0 als normale gewenste kandidaat uit.

Voor iedere kandidaat berekent `RankGovernment` de fuzzy rang en enkele filters:

- Government-slot `+b8` moet een waarde **groter** dan het aantal eigen steden leveren. Bij `grens <= aantal steden` wordt rang99 geretourneerd (`2005e5aa–c0`). Het getterobject is daadwerkelijk dezelfde Government-interface; `526820` leest record `+140`. De precieze parserbinding van dit veld naar de tekstnaam `TOO_MANY_CITIES_THRESHOLD` is in dit pakket nog niet gevolgd; die naamkoppeling blijft apart van de bewezen vergelijking.
- Een tweede filter gebruikt Government `+c0`, `526860`, recorddouble `+130`, zowel voor huidige als kandidaat-regering. Als de kandidaatwaarde lager is en `AiGold+4 / huidige waarde * kandidaatwaarde` minder is dan de som `AiGold+8,+c,+10,+14`, wordt rang99 teruggegeven (`2005e5d2–631`). De veldnaam en volledige economische interpretatie zijn nog open; dit mag niet als eenvoudig unitquotum worden behandeld.

De poll verwerkt uitsluitend beschikbare kandidaten met positieve geretourneerde rang. Zij bewaart tevens `UtilityGoverment` en rang per kandidaat. Voor **gewone indices1–11** wint alleen een **strikt kleinere rang** dan de beste bewaarde rang (`2005e452–459`). Een kandidaat met dezelfde rang vervangt de eerste niet, ongeacht hogere utility. De laagste database-index wint daardoor bij een reguliere gelijkstand. Pas voor index12 en hoger kan een utilityvergelijking een niet lagere rang alsnog laten winnen. `UtilityGoverment` wordt wel berekend; berekening betekent niet automatisch dat zij de keuze van originele regeringen bepaalt. Zie [rang en poll](BINAIR/research-government-ai-chain.txt).

Als er een winnaar is en diens index afwijkt van de actieve regering, roept de poll Player-slot `+14c` aan (`2005e4a7`), en leest daarna de werkelijk actieve index opnieuw via `+150` (`2005e4b3`). Er is hier geen extra timer of 'pas op beurt X'-voorwaarde in de AI-poll aangetroffen. Dat sluit engineovergang en beschikbaarheidsfilters niet uit.

De [frame-tabel](BINAIR/research-government-frame-table.txt), [uitvoerder](BINAIR/research-government-execution-budget.txt) en [frame-initialisatie](BINAIR/research-government-order-income.txt) verbinden de relevante volgorde: fuzzy Rulesframe4, Postframe5, WillOfThePeopleframe23, later AllocScienceframe12. De normale interpreter begint op instructie0 en verhoogt bij gewone frame-opcode1 de positie. Een regeringspoll is dus geen onderdeel van `Choose_Next_Science`; leren kan haar beschikbaarheidsvlag via een apart event bijwerken.

## 8. Regeringswisseling in de engine

Player `+14c` is `528f00` → `4c2d40`; `+150` is `528f20`, dat actieve regering `Player+94` leest. De wisselroute weigert dezelfde regering, negatieve/te grote indexen en een niet bekende enabling advance (`4c2d60–dac`). De verdere networktakken zijn niet functioneel uitgewerkt.

Voor een speler die al in Anarchy staat, kan de route de doelregering op `+11d8` bijwerken en onder een beurtvoorwaarde meteen voltooien. Bij een speler buiten Anarchy met veld `+11e0 ==0` bewaart zij het doel, berekent een eindbeurt met `random_result % const_field+370 + 1 + huidige beurt`, en roept `4c2f60` met regering0 aan (`4c2edb–f16`). Bij `+11e0 !=0` volgt een directe aanroep met de doelregering (`4c2f2e–31`). `4c2f60` schrijft de aangevraagde actieve index op `Player+94` (`4c3170`) en verwerkt verdere stads-/eenheidsgevolgen. Zie [overgang](BINAIR/research-government-engine-transition.txt) en [verzoekroute](BINAIR/research-government-engine-construct-change.txt).

De betekenis van `Player+11e0`, de daadwerkelijke afrondingscaller op volgende beurten en de parserbinding van const `+370` naar `MAX_GOVERNMENT_CHANGE_TURNS` zijn nog open. Daarom: het tekstfeit MAX_GOVERNMENT_CHANGE_TURNS4 bewijst op zichzelf geen exacte AI-overgangsduur. Er zijn aantoonbaar meerdere enginepaden; nog niet aangetoond welk daarvan iedere normale Deity-AI in onze saves gebruikt. Tijdens een overgang kan de AI opnieuw pollen; het ontbreken van een eigen AI-wachttimer betekent niet dat de engine iedere aanvraag direct voltooit.

## 9. Save en offline controle

Effectieve onderzoekslijsten staan in de AIP-save, zoals al bewezen in AIP-LAADWERKING. Ook ScienceAgent bewaart haar huidige doel en herkeuzevlag: schrijven `20023eed–f0b`, laden `2002427a–28c`. Zie [science-serialisatie](BINAIR/research-government-science-budget-save.txt). Een herladen save hoeft daarom niet meteen de nieuw gekozen tekstlijst te gebruiken om het lopende onderzoek te vervangen. De complete engineonderzoekvoortgang, regeringovergang en fuzzy rangbuffers in saves zijn hier niet opnieuw gereconstrueerd.

[Controleer-Onderzoekskeuze.py](../PROEVEN/Controleer-Onderzoekskeuze.py) voert de originele DLL-instructies uit met synthetische lijst/COM-resultaten. **14/14 geslaagd**, [uitkomsten](BINAIR/research-government-checks.json): ontbrekende/lege lijst, bekende advances, prerequisitefilter, geen toegelaten item, eerste snelle kandidaat, langzaam item passeren, strikte tijdsgrens, fallback, nulscience naar1, hogere science, werkelijk doorgeven van gekozen index en leeg-resultaat met flagreset.

Deze controle is geen echte parserproef, enginekostenproef, fuzzy-inferentieproef, regeringspollproef of gameplaybenchmark. Enginecallbacks zijn gestubd; de originele selectie en aanvraagcode loopt. De regeringresultaten hierboven zijn machinecodebevindingen en hebben in dit pakket geen zelfstandige emulatiecontrole gehad.

## 10. Gerichte open branches voor vervolg

1. Bind Government-record `+140`, `+130` en const `+370` via de werkelijke parser aan tekstnamen; benoem de economische regeringsfilter zonder veldnaamgok. Dit bepaalt of een gewenste Theocracykeuze ondanks rang1 wordt afgewezen.
2. Bind `Player+11e0` en de volgende-beurtafhandeling van regeringswisseling. Dit bepaalt de echte AI-overgangskosten en wanneer de actieve regering zichtbaar wordt.
3. Onderzoek de fuzzy defuzzificatie/reset bij de gedeelde Fascism/Communism-buffer en initialisatie van rangindex6. Dit is een concrete later-game-bugkandidaat, nog geen uitgewerkt wijzigingsvoorstel.
4. Benoem de enginekostenfactoren en het volledige netto-scienceproces alleen zover nodig voor Deity-strategie en timing. De eerste-keuzeregel zelf is aangetoond.
5. Volg overige schrijvers van de herkeuzevlag en echte advance-/government-events rond load. De huidige AIP-override maakt lopend onderzoek niet automatisch ongedaan; een eventuele andere resetroute moet afzonderlijk aangetoond worden.
6. Meet in fase C vanuit dezelfde benchmark de effectief gebruikte lijst, gekozen advances, geleerd Religion/Theocracy en werkelijk actieve regering per beurt. Een lijstpositie alleen is geen bewezen gedragsverbetering.

Aan de hoofdagent overgedragen: de foutieve Religionbasiskosten in de vroegere analyse; de opgeloste onbekende lijst-naar-keuzeschakel; de resterende regerings-/sciencegrenzen. Andere bestaande analyses en PROJECTSTATUS.md worden door hun eigenaar bijgewerkt.
