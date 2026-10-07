# Werkelijke Deitykosten en technologiefasen

Analyse van 6 oktober 2026, fase A. Alleen oorspronkelijke configuratie en machinecode gelezen; geen spelstart, gameplaywijziging of ontwerp. Dit afgebakende pakket sluit kosten- en tijdperkvragen; de brede spelanalyse blijft open.

## 1. Uitkomst

De normale AI op Deity krijgt tijdperkafhankelijke kortingen op onderzoek en productie. Die factoren worden werkelijk gebruikt, maar op verschillende momenten:

- **Onderzoek:** eerst `ADVANCE_COST + SCIENCE_HANDICAP × bekende advances`, vervolgens een eventuele speciale aftrek, daarna de tijdperkkorting. Deity heeft `SCIENCE_HANDICAP25`.
- **Productie:** de engine verlaagt de aangeleverde basiskosten bij het toevoegen/vervangen van een queuenode. Die opgeslagen nodekosten worden vervolgens met de productievoorraad vergeleken.
- **AI-bouwtijdschatting:** de aangetoonde unit- en gebouwgetters leveren de basiskosten. Deze schatters gebruiken de Deitykorting niet. De gewone researchkeuze gebruikt juist de gecorrigeerde enginekosten.
- **Tijdperk:** geen kalenderdatum of algemene advance-age-index. De engine kiest het hoogste tijdperk waarvan alle eigen enabling advances bekend zijn; als geen tijdperk voldoet, valt zij terug op index0.

Dit verklaart waarom tekstkosten en door de AI betaalde kosten niet mogen worden gelijkgesteld. Het bewijst geen aantal beurten zonder de actuele kennis, inkomsten, productie, voorraad en overige toelatingsvoorwaarden.

Bewijsniveaus: **T** configuratie, **B** oorspronkelijke instructies, **E** offline uitvoering van die instructies met synthetische records. Robotcom.dll: SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, timestamp `37b894e7`, imagebase `20000000`; de robotcom-map past. Engine: SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp `37d6f702`, imagebase `400000`. Engineadressen zijn uit werkelijke instructies/tabellen afgeleid; de niet passende civctp-map is geen adresbewijs.

## 2. Parser, waarden en context

Canonical registratie bindt `AI_TECHNOLOGY_COST` aan token310 en `AI_PRODUCTION_COST_ADJUSTMENT` aan311. Parser **458475–458513** verlangt respectievelijk token310/311 en vijf numerieke waarden; zij schrijft doubles naar DiffRecord **+150..+170** en **+178..+198**. Zie [canonical tokens](BINAIR/deity-costs-canonical-tokens.txt), [volledige parser](BINAIR/deity-costs-research-parser.txt) en [afgebakende arrays](BINAIR/deity-costs-final-parser-and-completion.txt). De bestaande [difficulty-loader](BINAIR/economy-growth-difficulty-record-loading.txt) leest zes records van512 bytes; globale tabel is `A7DD54`, actuele difficulty-index komt uit het object achter `A7A6A4`.

**T:** [originele DiffDB](../CTP-og/ctp_data/default/gamedata/DiffDB.txt), regels528–529, en [AAIP DiffDB](../CTP-AAIP/ctp_data/default/gamedata/DiffDB.txt) hebben dezelfde Deitywaarden:

| Index | Tijdperk | Onderzoekcorrectie | Productiecorrectie | Nominaal resterende kosten onderzoek / productie |
| --- | --- | --- | --- | --- |
| 0 | Ancient | −0,10 | −0,05 | 90% / 95% |
| 1 | Renaissance | −0,20 | −0,15 | 80% / 85% |
| 2 | Modern | −0,30 | −0,30 | 70% / 70% |
| 3 | Genetic | −0,40 | −0,40 | 60% / 60% |
| 4 | Diamond | −0,60 | −0,50 | 40% / 50% |

De laatste kolom is een nominale verhouding, geen exacte integerformule. De code telt een afzonderlijk naar nul afgekapt correctiebedrag bij de kosten op. Zie afronding hieronder.

**B:** research **475a17–475a9a** en queue **490d90–490e0d** kiezen deze AI-arrays bij Player+4 exact1 in singleplayer. De netwerkcontext gebruikt extra globals `A44C9C/A44C98` en predicate579f60; wanneer die contextpredicate waar is, wordt de AI-arrayroute overgeslagen. Andere Player-types krijgen bij research de scalar **DiffRecord+1d0**; bij deze queuecorrectie krijgen zij geen overeenkomstige korting. Dit sluit aan op de reeds gebonden singleplayer-type1 in [kolonisten/AI-context](VOEDSEL-GROEI-EN-KOLONISTEN.md). Een volledige multiplayerproef is hier niet uitgevoerd.

## 3. Wat laat de factoren omslaan?

De gebruikte selector **44eee0–44ef8c** leest AgeDB achter `A7DD4C` en begint bij de hoogste index. Iedere age heeft een52-byte record met aantal voorwaarden op+0 en advance-indices vanaf+4. Alle voorwaarden worden via **Player4c2180 → Advances474b60** getest. Eén onbekende prerequisite verwerpt deze age; de volgende lagere age wordt geprobeerd. Eerste geslaagde age geeft haar index terug. Geen geslaagde age geeft0. De costcallers begrenzen index≥5 op4. Zie [selector/getters](BINAIR/deity-costs-age-getters.txt) en [echte Player-known-getter](BINAIR/deity-costs-control-fixture-entries.txt).

Parser **44eb79–44ebea** bindt token458 `AGE_NUM_ADVANCES` aan record+0 en herhaalde token459 `AGE_ENABLING_ADVANCE` aan record+4, +8 enzovoort. De globale AgeDB-constructie is verbonden op **4072f6–4072fe**. Zie [age-parser](BINAIR/deity-costs-final-field-bindings.txt), [canonical tokens](BINAIR/deity-costs-canonical-tokens.txt) en [globale constructie](BINAIR/deity-costs-loader-and-stock-threshold.txt).

**T:** [age.txt](../CTP-og/ctp_data/default/gamedata/age.txt) vereist:

| Index | Alle vereiste advances |
| --- | --- |
| 0 | Toolmaking |
| 1 | Alchemy, Classical Education, Engineering, Banking |
| 2 | Age of Reason, Railroad, Medicine, Ocean Faring, Cannon Making |
| 3 | Robotics, Space Flight, Genetics |
| 4 | Wormholes, Neural Silicon Interface, Arcologies |

De selector verlangt niet daarnaast alle voorwaarden van de tussenliggende ages. De normale technologiegrafiek kan eerdere kennis uiteraard indirect vereisen; dit pakket maakt daarvan geen aparte complete late-gameanalyse. Ocean Faring alleen activeert index2 niet. Religion/Theocracy veranderen de age niet rechtstreeks.

## 4. Volledige normale onderzoeksformule

Science-interface **744fe0+40 →530d50 →475990** gebruikt de volgende keten:

1. Geen geldige Player-pointer: resultaat `7fffffff`.
2. Neem advance-record+58 (`ADVANCE_COST`).
3. Voeg **Advances+18 × Player4c2c70** toe. Advances+18 wordt bij nieuw geleerde advance verhoogd op **475132–475136** en bij verwijdering verlaagd op **475346–47534c**. Dit is de bekende-advanceteller, niet het aantal steden.
4. Getter4c2c70 leest Player+12e8-object+c0. Constructor **4b2db4/4b2dc2** bindt dit object aan **4a13e0**; **4a1447–4a144b** kopieert DiffRecord+20 naar object+c0. Parser **458031–45803b** schrijft token272 `SCIENCE_HANDICAP` naar DiffRecord+20. Op Deity is dat25.
5. Als advance-record+74 bit1 aanstaat, wordt een bedrag uit **472940**, op basis van Player-wondermasker4c1f70, afgetrokken. Dit is een afzonderlijke bijzondere branch; de exacte flagnaam en volledige wondervoorwaarden blijven open.
6. Voor normale singleplayer-AI: `K + trunc_x87(K × AI_TECHNOLOGY_COST[age])`, met K de uitkomst na bovenstaande stappen.

Bewijs: [researchinstructies](BINAIR/deity-costs-research-parser.txt), [objectconstructor](BINAIR/deity-costs-property-object-init.txt), [handicapcopy en parser](BINAIR/deity-costs-handicap-copy-parser.txt), [canonical SCIENCE_HANDICAP](BINAIR/deity-costs-canonical-extra-tokens.txt), [teller bij leren/verwijderen](BINAIR/deity-costs-record-field-candidates.txt) en [speciale aftrekbranch](BINAIR/deity-costs-special-research-deduction.txt).

**E, conditionele voorbeelden:** Religion heeft tekstkosten65. Zonder speciale aftrek, Ancient, drie bekende advances: K140, resultaat126. Bij acht bekende advances: K265, resultaat239. Bij vervolgens negen bekende advances en Theocracy-basiskosten65: K290, resultaat261. Deze laatste twee kosten zouden samen500 bedragen bij ongewijzigde voorwaarden. DiffDB noemt `AI_START_ADVANCES8`, maar dit pakket bewijst niet dat iedere feitelijke start precies acht advances kent; de voorbeelden lezen geen echte save uit.

De normale [AIP-researchkeuze](ONDERZOEK-EN-REGERINGSKEUZE.md) deelt deze **gecorrigeerde totale** kosten door `max(1,AiGold+18)` en vergelijkt strikt met haar tijdsgrens. Zij trekt de reeds verzamelde onderzoeksvoorraad in deze selectieroute niet af. De normale Player-completionroute doet dat wel: **4bb5f6–4bb648** vergelijkt voorraad Player+12e0 met **475980→475990**, trekt bij voldoende voorraad dezelfde kosten af, begrenst negatieve voorraad en vervolgt via474f10. Zie [completioncaller](BINAIR/deity-costs-completion-links.txt) en [cost-xrefs](BINAIR/deity-costs-research-xrefs.txt). De aparte resterende-beurtengetter475f20 trekt voorraad af en deelt door scienceopbrengst; dit is geen vervanger voor de eerder bewezen AIP-deadline.

## 5. Basiskosten, queuekosten en bouwschatters

UnitDB-vtable745098 slot24 is **531960**, dat via4542e0 uitsluitend UnitRecord+50 leest. De unitparser bindt token34 `SHIELD_COST` aan+50 op **46d42c–46d433**. Gebouwinterfaceconstructor5239b0 zet table744318; slot10 is **523a90→45cc40→BuildingRecord+38**. Zie [slotwaarden](BINAIR/deity-costs-cost-slots.json), [constructor](BINAIR/deity-costs-building-construct.txt), [unitreader](BINAIR/deity-costs-control-fixture-entries.txt), [gebouwreader](BINAIR/deity-costs-building-base-reader.txt) en [bestaande unitparser](BINAIR/food-growth-unitdb-record-parser.txt). De vier offline getterproeven geven dezelfde basiskosten in Ancient en Diamond.

Gebouwenqueue **498c53–498c63** en wonderenqueue **498e22** geven record+38 als kosten aan Queue491290. De laatste roept toelating4910c0 aan, daarna op **4912f3** de toevoeging490cf0. De bestaande [bouwanalyse](BOUWDOELEN-EN-QUEUE.md) bindt de unit/gebouw/wonder-klassen1/3/9 en echte Playerrequests.

**490cf0** herhaalt toelating per klasse, haalt eigenaar op, bepaalt age en berekent `C + trunc_x87(C × AI_PRODUCTION_COST_ADJUSTMENT[age])`. Pas daarna schrijft zij de kosten naar nieuwe node+0, type naar+4 en klasse naar+8 (**490e45–490e64**). De overeenkomstige vervangroute **490ea0** past dezelfde factor toe op **490f2f–490f6c**. Zie [formule en opgeslagen node](BINAIR/deity-costs-production-formula.txt), [queuewrapper](BINAIR/deity-costs-cost-entrypoints.txt). De korting is dus geen rechtstreekse extra stadsproductie of PW-bonus.

Voor basiskosten135 geeft Ancient-nodekosten129. Labyrinth heeft tekstkosten2160; dezelfde formule geeft nominaal2052 in Ancient. Eligibility, wonderconcurrentie en daadwerkelijke productie bepalen nog steeds of dit ooit wordt voltooid. Bestaande nodekosten worden in de gevolgde completionvergelijkingen gelezen; daar wordt niet opnieuw de huidige agekorting berekend. Een tijdperkwisseling alleen verlaagt die bestaande node in deze aangetoonde vergelijking niet. Andere resynchronisatiepaden zijn niet uitputtend onderzocht.

BuildFront **48f790** dispatcht klassen1/3/9 naar respectievelijk **48f7eb,48fac8,48fc1d**. Units en gebouwen vergelijken node+0 met aangeleverde voorraad; gelijkheid mag verder. Wonders controleren eerst globale wonderbeschikbaarheid, vervolgens op **48fc3f–48fc45** dezelfde kostendrempel. Andere toelatings-, locatie-, pop- en wonderbranches blijven gelden. De negen vergelijkingproeven bewijzen alleen deze grens, geen volledige constructie. Zie [vergelijkingen](BINAIR/deity-costs-building-wonder-completion.txt), [unitbranch](BINAIR/deity-costs-control-fixture-entries.txt) en [wonderdrempel](BINAIR/deity-costs-final-parser-and-completion.txt).

**AI-tijdschatters2001cba0/2001cc00** vragen juist de bovenstaande basiskostengetters op. De unitschatter deelt de basis integer door productie en negeert in deze body opgeslagen productie; de gebouwschatter gebruikt `(basis+0,5−voorraad)/productie`, gevolgd door integerconversie. De wondervariant2001cc60 heeft een afzonderlijke WonderTable-kostencache; deze body leest geen difficultyfactor. De eerdere harde unit-/wondertijdgrenzen uit de bouwanalyse mogen daarom niet worden opgevat als garanties over de echte discounted completionduur. Zie [oorspronkelijke schatters](BINAIR/deity-costs-ai-build-estimates.txt). Volledige wondercache-initialisatie en individuele eligibility blijven apart open.

Raakvlak met militair onderhoud: **Unit4da810→46ec50** leest UnitRecord+bc, dat parser46d5c7 aan token52 `SHIELD_HUNGER` bindt. Dit is een andere tekstwaarde dan SHIELD_COST; queuekorting bepaalt deze getter niet. Zie [getter](BINAIR/deity-costs-research-completion.txt) en [canonical token](BINAIR/deity-costs-canonical-extra-tokens.txt). De daadwerkelijke readinessformule wordt door de coördinator afzonderlijk onderzocht.

## 6. Afronding, controles en resterende grenzen

[Controleer-Deitykosten.py](../PROEVEN/Controleer-Deitykosten.py) levert **66/66** controles op oorspronkelijke instructies. Vijf agekeuzes,25 researchgevallen,15 klasse/era-queuewrites, drie agevoorwaarden, human-context, speciale aftrek, ontbrekende Player, twee vroege researchvoorbeelden, vier databasegetters en negen voorraadgrenzen. [Definitieve resultaten](BINAIR/deity-costs-controls.json).

Research/age/getters gebruiken echte interfaces en synthetische records. Queueproeven vervangen admission/cityvalidity/eigenaar/heap; alleen formule en nodewrite worden daar werkelijk uitgevoerd. Speciale researchaftrek gebruikt mask/aftrek-mocks. Vergelijkingsproeven stoppen vóór de daaropvolgende constructieacties. De geïmporteerde CRT-conversie gebruikt [gedeelde ftol-stub](../PROEVEN/ctp_x87.py), bewaart en herstelt x87-controlword; gewone arithmetic blijft extended precision/nearest in de fixture.

De eerste controle gebruikte een gewoon Python-doublemodel en vond **vijf verschillen**, bewaard in [eerste modelafwijkingen](BINAIR/deity-costs-first-double-model-gaps.json). Voorbeeld:140×opgeslagen−0,3 ligt in extended precision iets boven−42; naar nul afkappen geeft−41, dus kosten99. Een afgeronde doubletussenuitkomst maakt er−42 en98 van. Het definitieve onafhankelijke model vermenigvuldigt de exact opgeslagen IEEE-double als rationale waarde, en kapt daarna af; de kleine controleproducten passen binnen extended precision. Dit is geen ongefundeerde correctie naar een passend resultaat.

De daadwerkelijke runtime-x87-precisie is hiermee niet gemeten. Rond exacte integerdrempels kan zij één punt verschil maken; percentages en berekeningsvolgorde zijn wel gebonden. Oude saves, netwerkbranches, alle speciale wonderaftrekken, overige schrijvers van queuekosten en echte end-to-endbeurten zijn niet nagebootst. Geen nieuwe testsessie is nodig om de bovenstaande lokale implementatie vast te stellen; een latere benchmark moet de actuele kennis, age, kosten en voorraad expliciet meten.
