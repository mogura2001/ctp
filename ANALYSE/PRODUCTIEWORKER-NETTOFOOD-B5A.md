# B5a: kandidaatwerkers en exact nettovoedsel

Gerichte A-terugvraag, 10 oktober 2026, 18:38 Europe/Amsterdam. Tussendoel: productiesteden met drie bergwerkers en één voedselwerker bij omvang4. Alleen de voedselgate vóór commit onderzocht. Geen spel/liveprobe, harness, test, ontwerp of patch; alleen bestaande bewijsstukken en drie begrensde aanvullende enginelezingen. Ownership uitsluitend dit bestand en VOORTGANG-ANALIST-B5A-FOOD.md.

**Uitkomst: de voedselrekening en alle fysieke/gebouw/rantsoeninvoer zijn gebonden; een algemeen geldige kandidaatgate zonder worker-/territorymutatie is nog niet bewezen. Het concrete resterende antwoord is actuele criminaliteit voor de kandidaat met vier gewone werkers zonder bards.** City+5cc+b0 is een bestaande cache zonder hier bewezen actualiteitsgarantie op het B5a-invoegpunt. Population+40/Happy4abd10 vernieuwt gelukscomponenten/details maar vernieuwt op dit gevolgde pad niet de crimecache. Normale bestaande engine-cacheupdates zijn geen nieuw verboden handeling: B kan een engine-query met gedocumenteerde cachesideeffects kiezen, mits de juiste kandidaatcrime hierdoor werkelijk wordt gebonden. Alleen het feit dat een getter schrijft is niet de blocker. Geen TileUtilitysom, nulbonussen of oude crimecache als vervangend eindbeleid.

## Dekkingsmatrix

| Benodigde stap | Bewijs / concrete binding | Status voor B |
|---|---|---|
| Deze stad naar actuele CityData | CityAgent+0c cityID; AiMain+2c Playerinterface; onderliggende Player+12c8-map/+12c0-lijst;4cb060→stadshandle;4da8b0→UnitData+58 | Gebonden, geen gegokte stadindex |
| Centrum en exact vier kandidaatposities | City+44c→4da9a0; TileUtility+28 extern→503f00 intern; native World516bc0 en510f70 | Gebonden; echte toelaatbaarheid blijft Population+60 |
| Huidige gebouwen, terreinbonus/flat/percent eenmaal | BuildingDB A7DD1C;45d540/45d6b0/45d730 met City+48/+4c en eigen buffers | Gebonden zonder CityData-refresh; cachevergelijking nodig voor identiteit met bestaande foodcall |
| Huidige foodwonderpercent | Owner Player+1170/+1174→WonderDB473f40, inclusief bestaande obsolescencechecks | Gebonden, geen tekstpercentage aannemen |
| Stadssom en afronding |494970; wonder via signed truncatie, crime via MSVCRT.floor | Exact gebonden |
| Onderhoud van vier normale toekomstige fieldworkers | PopDB A7DD44, werkertype-selectie4cdbf0; Hunger Record+30;4c27f0 ration;498205..498295 echte consumptie | Gebonden voor expliciet gevalideerde gewone PopDB/geen slaven; geen afgeronde Population+58 gebruiken |
| Actuele kandidaatcrime / actualiteit | Happy4abd10 en4aafe0 zijn schrijvers; gelezen Happy+b0 alleen bestaande cache | **Resterende blocker voor algemene gate** |

## Engine, stad en coördinaten

Machinecodebasis blijft originele civctp.exe SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, base400000/timestamp37d6f702, geen civctp.map. Passende Robotcom-map/DLL-binding wordt hergebruikt uit [workerroute](STADSROL-WORKERROUTE-B5A.md). Nieuwe alleen-lezen disassemblage betrof4cb060,473f40 en4cdbf0; relevante instructies/adressen staan hieronder. Geen runtimewaarneming van buffers of geladen records.

**Machinecode:**4cb060 is thiscall `bool(Player*, int* error, uint cityID, uint* unitHandle)`, `ret0c`, EAXbool. Hij zoekt exact cityID in Player+12c8 en haalt via Player+12c0→+0c-array de handle. Niet gevonden: error1, handle0, EAX0 op4cb0ba..4cb0cf; succes:error0 en handle op4cb0d2..4cb0f8. Vervolgens bestaande4da8b0 met ECX=&unitHandle geeft UnitData, waarvan+58 de CityData is. Owner City+4 moet overeenkomen met AiMain+20 en de echte Player in globalA7DD80[owner]; normale eigenaar1..31, geldige handle/pointers en total City+58c==4 vereisen. City+448≠0, slaven en bijzondere eigenaar-/netwerkcontext blijven unsupported en gaan naar oorspronkelijke verdeling.

Centrum uitsluitend via `4da9a0(this=&City+44c, outInternalMapPoint*)`, thiscall/ret4. Het is de echte cityunitpositie, niet een willekeurige TileUtility of extra inwoner. Elke kandidaat is een afzonderlijke actuele TileUtility+28 externe positie. Gebruik de reeds bewezen503f00-conversie en echte bounds/context; intern MapPointData gebruikt signed16 x/y/z op+0/+2/+4. Alle vier onderling verschillend en verschillend van centrum; z/context gelijk aan de ondersteunde gewone stad. Stad/radius/overlap/toelating blijven de eerder overgedragen Population+60-checks, inclusief opnieuw toetsen bij commit.

Native World is globalA7DD70. `516bc0(this=World*, int x,int y)` retourneert de werkelijke canonieke terrainindex voor de normale oppervlakcontext; geen tekstrecordvolgorde. `510f70(this=World*, const InternalMapPoint*)`, thiscall/ret4, volgt World+1c naar de echte cel en500110. Deze bestaande raw getter gebruikt echte terrain/good/improvement/rivier/centrumcontext; dus geen zelf verzonnen basis+farmmodel, toekomstige verbetering of dubbele centrumbonus. [World/celroute](BINAIR/terrain-food-v2-current-tile-and-level.txt), [raw celopbrengsten](BINAIR/engine-locatiewaarde-tilehelpers.txt), [terreinbinding](TERREIN-EN-IMPROVEMENTS.md). Raw integerfood en terrainbonus zijn afzonderlijke invoer van494970.

## Gebouwinvoer zonder de stad te vernieuwen

494280 vernieuwt drie caches met bestaande BuildingDB-getters; de functievervolging doet meer stadswijzigingen en is geen preview. [Refreshcalls](BINAIR/economy-city-total-yields.txt), [complete buffergetters](BINAIR/economy-gold-effect-array.txt). Elke getter is thiscall ECX=BuildingDB A7DD1C, args `(uint maskLo,uint maskHi,void* output)`, `ret0c`. Neem actuele City+48/+4c. De gevolgde getterlichamen schrijven uitsluitend de aangeleverde output; eigen private buffers vermijden CityData-/spelmutatie.

| Getter | Eigen buffer | Relevant foodveld | Oorspronkelijke cache |
|---|---|---|---|
|45d540 |0x2a0 bytes,24×7 int32 |`int32[7*terrain+2]` |City+fc+1c*terrain+8 |
|45d6b0 |0x1c bytes,7 int32 |index2/+8 |City+3a4 |
|45d730 |0x38 bytes,7 doubles |index2/+10h |City+3c8 |

45d540 sommeert record+78 bij terrein+70/resource+74;45d6b0 sommeert record+8c bij resource+88;45d730 sommeert record+98 bij resource+90. Effectindices komen uit DB+100/+108/+10c, aantallen uit+38/+40/+44, records uit+8 met stride108h. Ondersteun uitsluitend geldige loaded DB, indices/masken en resource0..6/terrain0..23; geen ongecontroleerde bufferwrite bij onverwachte data.

**Interpretatie/ontwerpvoorwaarde:** private aggregatie levert waarden uit actuele gebouwbits zonder cacheupdate. Voor exact dezelfde som die494970 met de nu aanwezige caches zou rekenen, moeten relevante private outputs gelijk zijn aan de relevante City-cachewaarden; ongelijkheid is gewone fallback, geen automatische updateraanroep. Zo wordt geen cacheactualiteit verondersteld. Alleen de vijf werkelijk gebruikte terrainfoodvelden en flat/foodpercent zijn nodig voor de combinatie. Een geplande gebouwverbetering telt niet mee.

Foodwondergetter `473f40(this=WonderDB A7DD5C,uint maskLo,uint maskHi)`, thiscall/ret8,EAXint. Owner Player+1170/+1174 zijn de actuele masks. Geen alternatieve naamresolver nodig:473f6c leest effectindices uit DB+294,473f8f vraagt het record op;473f99..473fdd doorloopt aanwezige Players en hun advances via464860/464850/4c2180 om obsolescence uit te sluiten;473ff5 leest Record+ac,474027 retourneert. De bestaande getter gebruiken behoudt die context, anders mogen percentages niet uit wonder.txt worden ingevuld.

## Exacte voedselrekening

Voor intern centrum `c` en precies vier kandidaatfieldworkers `p0..p3`, in toekomstige bevolkingsvolgorde:

```text
S = 0
voor q in [c,p0,p1,p2,p3]:
    S = double(S + terrainFoodBonus[WorldTerrain(q)])
    S = double(S + WorldRawFood(q))
T = double((S + flatFoodBonus) * (1 + foodPercent))
G = double(T - truncTowardZero((foodWonderPercent / -100) * T))
L = floor(double(G * kandidaatCrime))
A = double(G - L)
D = opeenvolgende som van (positieve toekomstHunger_i * actueleRation)
N = double(A - D)
voedselgate: A >= D, equivalent N >= 0 binnen geldige eindige rekenwaarden
```

4949c6..494a98 voegt perpositie **eerst terreinbonus, daarna rawfood** toe met doublespills.494ac7..494ae7 past flat en percent **eenmalig op de hele stadssom** toe.494b18..494b35 gebruikt wonderpercentage/-100,7256c6→ftol en aftrek van de signedtruncatie: dit is geen continu `T*(1+W/100)`.494b53..494b65 gebruikt de gebonden floor-import74335c;494b89..494b98 trekt dit verlies af. [Volledige functie](BINAIR/economy-city-food-sum-and-use.txt), [importbinding](BINAIR/economy-city-rounding-imports.json).

Behoud bij implementatie native x87-volgorde/spills en signed32-conversiegrenzen; een losse algebraïsche herschikking kan op integergrenzen verschillen. Niet-eindige waarden, ongeldige ratio/crime of ftol-overflow krijgen fallback. Geen eigen epsilon dat honger zou toestaan.494970 zelf schrijft City+60/+68/+70 en mag niet als preview worden aangeroepen.495250/TileUtilityfood werkt met perpositie-flatbonus en andere afronding; die som vervangt bovenstaande route niet.

## Onderhoud en toekomstige workerrecords

Echte stadsupdate498205..498295 sommeert positieve Hunger per inwoner maal Player4c27f0, schrijft City+78 en vervolgens City+58=`A-D`. Dit is dezelfde basis als pure behoeftegetter494ba0, maar494ba0 leest **huidige** types; veranderde kandidaattypes moeten dus expliciet passen. [Consumptievolgorde](BINAIR/economy-city-food-turn-order.txt), [Hungerrecord](BINAIR/economy-city-hunger-ration.txt), [rations](BINAIR/economy-city-player-modifiers.txt).

`4c27f0(this=ownerPlayer*)` retourneert actuele rationdouble in ST0 via Player+1318→4cb9a0→object+8; geen afgeronde FLIwaarde/governmentstand gebruiken. De gewone default1+0.25*stand is slechts een bestands-/setterles, geen vervanging voor actuele invoer.

City+590 bevat vier pophandles.4ccaa0 resolveert handle via PopPoolA7DD7C/4b23c0; signedbyte PopData+19 selecteert PopDB A7DD44/456b70, record+30 is Hunger. Voor toekomstige fieldworkers heeft4cdbf0 na placement+1c=0 expliciet: record+64 slavebit20 behouden; anders fieldbit2 behouden; anders selecteer eerste geschikte fieldrecord met hoogste **strikt hogere** TYPE_PREF+54, improvement+60 toegestaan, omvang tussen+58/+5c, current-governmentbit in+68. Cityomvang/gebouwgetters4dc570/4dc310 en owner Player+94 zijn dezelfde echte inputs. Deze selectiecode zelf schrijft PopData+19 en is dus geen previewcall.

Voor ondersteunde normale OG-toestand: record0 POP_WORKER heeft Hunger10; alle zeven niet-slaverecords hebben Hunger10, slave Hunger5. Loaded records/flags en fieldselectie moeten dit profiel bevestigen; dan veranderen de normale reset/specialist→worker-conversies de onderhoudsom niet en is494ba0 vóór commit bruikbaar voor D, of vier echte worker-Hungers×ration. Uitsluitend bestand lezen bewijst geen loaded DB. Afwijkend loaded profiel/slave/ongeldige typeindex: ordinary fallback; geen constante40 zonder die checks. De exacte selector is gebonden, maar geen nieuw algemeen typevoorspellerontwerp uitgewerkt.

## Exact resterende blocker: kandidaatcrime en veilige waarneming

494970 leest uitsluitend `double([City+5cc]+b0)`; de positiegetters lezen dezelfde cache. De crimeformule is al bewezen:

```text
k = clamp((governmentCrimeOffset - kandidaatHappiness)
          * governmentCrimeCoef * gebouwCrimeProduct
          * (1 - actueleWonderCrimePercent/100) / 100,0,1)
```

Governmentgetters4c2b70/4c2b50; gebouwfactor via499840→BuildingDB45d980 met actuele City+48/+4c; wonder viaowner4c1f70→WonderDB4721c0. Deze modifiers zijn gebonden; ontbrekende invoer is **geldige kandidaatHappiness/daadwerkelijk bijbehorende crime**, niet de naam van de coëfficiënt. [Crimeformule](BINAIR/economy-city-crime-binding.txt), [bestaande geluksanalyse](BARDS-EN-GELUKSVOORWAARDEN.md).

**Machinecode / sideeffects:** Happy4abd10 schrijft op4abd92 `Happy+50`,4abe03 `+58`,4abe52 `+60`,4abf1f/4abf22 en4abf86/4abf8a `+78/+7c`, en roept4ac8a0 aan op4abdb7/4abe2a/4abe77/4abf96. [Bestaande complete helper](BINAIR/happiness-bards-engine-input.txt). Population+40→52c460→4abd10 retourneert non-bard happiness; het gevolgde helperlichaam eindigt4ac04b zonder4aafe0/crimeupdate. Het is dus een bestaande engine-query met geluks/detailupdates, geen bewijs dat Happy+b0 aansluit op zijn geretourneerde happiness.

De concrete bestaande crime-cache-update is `4aafe0(this=Happy*,CityData*,ownerPlayer*)`, thiscall/ret8,double ST0; hij gebruikt Happy+0 en schrijft+b0/+b4 op4ab0a9/4ab0af en detail13 op4ab0d2. Hoofdrefresh492650 roept op4926b4 `4ab410(this=[City+5cc],City,0,&local20,1)` aan; deze thiscall/ret10 bereikt4aafe0 op4abcc8, maar schrijft ook City+38/count/componenten en kan andere statuscomponenten afhandelen. De bestaande andere caller49c9ed gebruikt `(City,1,&local18,0)` en bewaart/herstelt City+38; de volledige sideeffectveiligheid van die gehele caller wordt niet geclaimd. [Bestaande callers](BINAIR/economy-city-crime-city-object.txt), [hoofdrefresh/eindcall](BINAIR/economy-city-crime-full-update.txt). De twee flags zijn echte callerwaarden, hier niet als algemene veilige previewflags geïnterpreteerd.

Daarnaast is `4abce0(this=Happy*,CityData*,double happiness)`, thiscall/ret0c, de bestaande setter die Happy+0/+4 zet en4aafe0 opnieuw uitvoert. De gewone enginecaller4a7e5e gebruikt precies de stad en een berekende happinessdouble vóór zijn foodgetter. Dit bindt de crimeparameterroute, maar bewijst nog niet waar een geldige kandidaatHappiness voor B5a vandaan komt. B kan de oorspronkelijke query-/cache-update-route beoordelen; geen toestemming afleiden om fictieve happiness in de echte stad te schrijven of worker-/territoryplaatsingen te doen voor een preview.

Er is een **concreet mogelijk observatiepunt**, nog geen bewezen oplossing: de bestaande eerste SupplyEntertainers-call20020f56 roept reeds Population+40 op20021734; direct20021737 staat non-bard happiness als double op zijn ebp−0c, status op ebp−4, effect op ebp−14. Vóór20021748 wordt er het bestaande gecachete bardaantal aan toegevoegd. Die bestaande uitvoer in een latere B/C-ingreep alleen waarnemen vereist geen tweede muterende gettercall. Echter dit resultaat gebruikt deels gelukscomponentcaches en City+38, en er is hier **niet bewezen** dat het gelijk is aan het daadwerkelijke geluks/crime-resultaat voor vier kandidaatfieldworkers bij de volledige stadsupdate. Het los afvangen of lezen van oude Happy+b0 geeft die garantie niet.

Vervolg uitsluitend als B de algemene gate nodig heeft: bind op dit bestaande observatiepunt voor de afgebakende normale vierpop/nulbardcontext welke componenten ten opzichte van de kandidaat onveranderd blijven, of bind een normale engine-query/cache-update met gedocumenteerde sideeffects en de geldige invariant tot foodconsumptie. Geen brede heranalyse of nieuw screenshot-/emulatieframework. Tot dit antwoord beschikbaar is, kan B de draft met exact benoemde blocker afronden; de algemene driebergen+foodcommit heeft nog geen complete voedselgate. Speciale City+448/eigenaar/netwerkcontext blijft original fallback.

## Overdracht en acceptatie

De stad/tilebinding, bonusbuffers, wonderafronding en onderhoudsketen zijn aanvullend onderbouwd. Geen foodgate geïmplementeerd of getest en geen gameplayeffect. B kan een concrete begrensde draft reviewen; de algemene mutatievrije onderhoudsgate heeft één open kandidaatcrime-/actualiteitsbinding. De eerdere echte Populationchecks, finale bardvoorwaarden, gedeeltelijke-commitfallback en PopNeedsChanging-keuze uit de workerroute blijven noodzakelijk. Analysewerk van dit pakket stopt met deze exacte blocker.
