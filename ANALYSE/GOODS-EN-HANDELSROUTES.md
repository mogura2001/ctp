# Goods, stadsvoorraad en interne handelsroutes

Bijgewerkt: 5 oktober 2026, 10:54 Europe/Amsterdam. Fase A, alleen-lezen onderzoek. Geen spelstarts, gewijzigde gamebestanden of gewijzigde binaries.

## Conclusie voor onze projectdoelen

De bestaande AI waardeert het verzamelen van gelijke goods al in haar interne handelsplanner. De locatiescore waardeert alleen aanwezigheid van goods; die vestigingsschakel houdt dus geen rekening met de good-identiteiten waarmee de handelsplanner wel rekent. De planner gebruikt bestaande stadsvoorraad, geen voorspelling van een toekomstige monopoly-stad.

De onderzochte enginevoorraad telt goods op het centrum en op werkelijk door inwoners gebruikte terreinposities. Good-aanwezigheid in het toekomstige stadsgebied is daarom potentieel, nog geen huidige handelsvoorraad. Bevolkingsplaatsing is onderdeel van de te verbeteren keten.

Originele regeringen laten ieder vier inkomende en vier uitgaande routes toe. Dit zijn afzonderlijke grenzen per stad. Een lokaal exemplaar plus vier importen kan vijf gelijke exemplaren opleveren; meerdere lokale exemplaren kunnen daarboven komen. De grenzen betreffen routelijsten, niet een bovengrens van vijf voor de totale good-voorraad.

De basisberekening voor good-goud groeit driehoekig met het aantal gelijke exemplaren. Dit onderbouwt het gebruikersdoel van concentratie. De volledige netto-opbrengst, monopoly-label/threshold, goudgebouwen, piraterij en routekosten zijn hiermee nog niet volledig uitgewerkt.

## Bewijskader

T = tekstregels; B = oorspronkelijke machinecode; E = oorspronkelijke instructies op synthetische objecten met expliciete mocks. Geen nieuw gameplaybewijs R.

robotcom.dll SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, timestamp `37b894e7`, imagebase `20000000`. De bijbehorende AI-map is door de tools gecontroleerd. civctp.exe SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp `37d6f702`, imagebase `400000`. Engine-adressen komen uit de werkelijke binary/interfaceketen; de afwijkende engine-map is niet gebruikt.

AAIP-leerpunt: goods.txt en govern.txt zijn byte-identiek aan de originele bestanden, gecontroleerd met SHA256 in [de vergelijking](BINAIR/trade-goods-aaip-reference.json). Good-waarde en regeringsroutegrenzen zijn dus geen AAIP-wijziging. Dit bewijst niet dat alle handelsaansturing of binaries van AAIP gelijk zijn.

## 1. Wat geeft de Player-interface terug?

**B:** FindUnconnectedGoods (`20029360`) gebruikt Player-slot `b8` op `20029457`. De echte Player-interface heeft tabel `744660`; dit slot wijst naar `528060`. Die methode zoekt de eigen stad, haalt CityData via `4da8b0`/UnitData+58 op en schrijft twee tellingen per good-index:

| Output | Getter | CityData-veld | Betekenis in gevolgde herbouwroute |
| --- | --- | --- | --- |
| Eerste telling | `496d30` | arraypointer `+5c4` | Lokaal verzamelde exemplaren vóór routemutaties |
| Tweede telling | `496d10` | arraypointer `+5b8` | Beschikbare exemplaren na aftrek/toevoeging door routes |

Bronnen: [GUID/Player-binding](BINAIR/trade-goods-player-binding.txt), [volledige getter](BINAIR/trade-goods-city-getters.txt), [arrays/getters](BINAIR/trade-goods-arrays-update.txt), [AI-aanroep](BINAIR/trade-goods-ai-route.txt).

Bij niet gevonden stad zet de interface de statusoutput op1. De tellingen worden dan niet in deze route geschreven. De onderzochte interne planner gebruikt eigen CityAgents; dit is geen bewijs dat iedere fout-/loadtoestand veilige tellingen oplevert.

## 2. Hoe wordt die voorraad gevuld?

**B:** CityData-routine `49dd60` wist beide arrays en de totalen `+5bc/+5c8`. Daarna:

1. Zij vraagt World `514f60` om de good-identiteit op de centrumpositie; bij gevonden good verhoogt zij beide type-tellingen.
2. Zij loopt de bevolking op CityData `+590`, aantal `+58c`. Alleen bevolking waarvoor `4cca70` waar is telt mee: die wrapper leest PopData-byte `+1c` en test gelijk aan0.
3. De positie van zo'n inwoner komt uit `4ccb30`, PopData `+20/+24`. World `514f60` bepaalt daar de good. Bij aanwezigheid verhogen beide arrays dezelfde good-index.
4. In routelijst CityData `+594`/items `+5a0` verlaagt routetype0 de beschikbare telling, minimum0. De lokale telling blijft staan.
5. In routelijst `+5a4`/items `+5b0` verhoogt routetype0 de beschikbare telling. Andere routetypes kunnen voedsel-/geldvoorraden veranderen en worden hier niet als goods geteld.

De richting is tevens gebonden door de capaciteitsketen: `+594` is de uitgaande lijst, `+5a4` de inkomende. Routewrapper `4d72e0` haalt uit de routepool de data op; `4d8290` schrijft RouteData `+28/+2c` als type en resource-index/bedrag. Type0 is de good-route in de gevolgde aanmaakroute. De eerdere offsets+10/+14 zijn op6 oktober gecorrigeerd tijdens het vervolgonderzoek; zie [oorspronkelijke writer](BINAIR/trade-capacity-labyrinth-create-and-free.txt).

Bronnen: [herbouw en routeaanpassingen](BINAIR/trade-goods-net-import-export.txt), [bevolkingspredicate/positie](BINAIR/trade-goods-workers-gold.txt), [routewrapper](BINAIR/trade-goods-route-types.txt), [aanmaakroute](BINAIR/trade-goods-limit-create-route.txt).

Een verwante goudopbrengstroutine `4972c0` kan dezelfde lokale arrays herberekenen afhankelijk van haar argument. Het volledige schema van alle aanroepmomenten blijft open. De [operandscan](BINAIR/trade-goods-array-references.txt) bevat kandidaten; die scan alleen bewijst geen objecttype of semantiek van iedere gevonden instructie.

Strategische gevolgtrekking: tel voor toekomstige locaties zowel aanwezige als daadwerkelijk te verzamelen goods. Een science-stad die alle betreffende terreinwerkers vervangt door specialists hoeft haar lokale voorraad niet automatisch te behouden. Dit is een code-afgeleide aandachtspunt; het concrete effect per benchmarkstad is nog niet gemeten.

## 3. Good-waarde en engineopbrengst

**T:** [goods.txt](../CTP-og/ctp_data/default/gamedata/goods.txt) bevat17 records, ieder `GOOD_GOLD_VALUE 10`.

**B:** global `a7ddd0` is de good-database. Initialisatie `407597` maakt het object; `4075ac` bewaart de pointer; `4075b1` roept parser `459e10` aan. Die gaat via `459e30`, recordlookup `456570` en `459f80` naar veldparser `45a0f0`. Token354 is `GOOD_GOLD_VALUE`; de switch `45a107–115` herkent354, en `45a1d6–df` schrijft de gelezen integer op record `+30`.

GameState-slot50 (`526030`) geeft object `+34`; constructor `5310f0` zet Resource-vtable `745050`. AI-init bewaart dit als AiMain+54. Resource-slot0c (`5311c0`) leest de good-waarde uit dezelfde database/record+30; slot14 (`5311e0`) geeft het aantal good-types.

Bronnen: [init](BINAIR/trade-goods-db-init.txt), [databaseparser](BINAIR/trade-goods-value-parser.txt), [recordroute](BINAIR/trade-goods-value-record.txt), [token](BINAIR/trade-goods-value-token.txt), [veldparser](BINAIR/trade-goods-value-field.txt), [GameState-binding](BINAIR/trade-goods-gamestate-binding.txt), [constructorrouting](BINAIR/food-growth-gamestate-construct.txt), [Resource-constructor](BINAIR/trade-goods-resource-construct.txt), [Resource-slots](BINAIR/trade-goods-resource-value.txt), [AI-init](BINAIR/terrain-food-ai-interface-init.txt).

**B/E:** CityData-routine `4971f0` berekent voor ieder type met positieve beschikbare telling N:

`basis-good-goud = GOOD_GOLD_VALUE * N * (N + 1) / 2`

Zij somt die waarden en telt het resultaat bij CityData+28 op. Verderop kan een wonderbonus volgen. Callback `473720` leest recordveld+9c en controleert obsolete-advances. Dit veld is nu aan WONDER_FLAG_MULTIPLY_TRADE_ROUTES gebonden: token492, switchindex492-456=36, jumptabel470e34, case470bc6, write470bdc–be5 naar+9c. Global a7dd5c wordt via470f20 gemaakt en4710e0 geparsed; die recordroute roept4705c0 aan. Zie [token](BINAIR/trade-goods-multiplier-token.txt), [binding](BINAIR/trade-goods-multiplier-binding.json), [database-init](BINAIR/trade-goods-effect-db-init.txt), [parserroute](BINAIR/trade-goods-effect-parser-route.txt), [flagparser](BINAIR/trade-goods-effect-flags-full.txt) en [callback](BINAIR/trade-goods-gold-modifier.txt).

De toepassing49726f–298 telt `integer(huidige component * percentage * 0.01)` bij de huidige component op. In [Wonder.txt](../CTP-og/ctp_data/default/gamedata/Wonder.txt) heeft Dinosaur Park waarde300: in deze berekening is dat een verhoging met300%, dus viermaal de eerdere component bij exacte gehele uitkomsten. De effectbits en hun verspreiding over steden zijn niet volledig gevolgd; hier wordt geen gemeten bonus voor iedere stad geclaimd. Goudgebouwen zijn een afzonderlijke modifierketen. De basisformule blijft een opbrengstcomponent, geen volledig besteedbaar geld.

Bij waarde10 geeft N=1/2/3/4/5 de component10/30/60/100/150. Vijf afzonderlijke exemplaren geven samen50; vijf in één stad150. Dit is een rekenvergelijking bij gelijke overige omstandigheden. Bron: [engineberekening](BINAIR/trade-goods-workers-gold.txt).

## 4. Hoe waardeert de AI een interne route?

**B/E:** `GoalRoute::EstimateRouteBenifit`, `200482a0`, leest de beschikbare bronvoorraad S en bestemmingsvoorraad D van hetzelfde good-type. Zij berekent het verschil tussen de driehoekige opbrengsten vóór en na verplaatsing:

`bod = (D + 1 - S) * goodwaarde * fz_gold_2_production * geschatte resterende rondes`

Bronvoorraad kleiner dan1 en bestemmingslaag1 krijgen een negatieve sentinel. Een route naar dezelfde CityAgent wordt eveneens geweigerd in de eerdere branch. De laagbetekenis en het volledige geschatte spelduurmodel zijn niet in dit pakket herleid.

Bij S=1 wordt het concentreren naar D=4 in deze berekening hoger gewaardeerd dan naar D=1. Bij S=3,D=1 daalt het gezamenlijke basis-good-goud; het bod is negatief. De gewone AI begrijpt dit marginale concentratievoordeel dus al. Wat ontbreekt aan de vestigingsscore en welke verdere plannerbeperkingen spelen zijn afzonderlijke vragen.

**B:** CollectCityBids (`200295c0`) kiest een andere eigen stad met routecapaciteit en veilige piraterijmarker. Het beginvoordeel moet de startwaarde1 strikt verbeteren; bij gelijk voordeel kan lagere routekost beslissen (`20029736–788`). Zij past daarna nog prioriteiten aan met bestemmingsbevolking en het aantal bruikbare doelen van hetzelfde type (`20029862–8f3`). Dat is geen volledige optimalisatie van alle mogelijke routenetwerken.

FindUnconnectedGoods maakt per stad/type één doel wanneer lokaal >0 én lokaal == beschikbaar. Een stad met export/import van dat type kan daardoor buiten deze bronselectie vallen. Ook meerdere lokale exemplaren leveren in deze loop één doel op, geen doel per exemplaar. Die concrete beperking moet bij de uiteindelijke monopoly-opzet worden meegenomen; andere handels-/diplomatieroutes zijn hier niet onderzocht.

Bronnen: [bodfunctie](BINAIR/trade-goods-benefit.txt), [bron- en bestemmingsselectie](BINAIR/trade-goods-ai-route.txt), [uitvoering/verbinding](BINAIR/trade-goods-connect-action.txt).

## 5. Vier importen en vier exporten

**T/B:** [govern.txt](../CTP-og/ctp_data/default/gamedata/govern.txt) zet MAX_INCOMING_TRADE en MAX_OUTGOING_TRADE beide op4 in de twaalf originele records. Parser `45ae60–72` schrijft token509 naar Government+190; `45ae7d–8f` schrijft token510 naar +194. De [tokenidentiteiten](BINAIR/trade-goods-limit-identities.txt) en [veldschrijvers](BINAIR/trade-goods-parser-candidates.txt) binden de namen.

Player-slot294 (`52bbf0`) geeft de actuele inkomende lijstgrootte via `49ebd0` en grens Government+190, daarna uitgaande lijstgrootte via `49ebe0` en grens+194. Die regering komt uit de Player van de interface; bij de onderzochte interne route zijn bron en bestemming eigen steden. Bron: [capaciteitsbinding](BINAIR/trade-goods-routecapacity-binding.txt) en [volledige getter](BINAIR/trade-goods-capacity-gold.txt).

GoalRoute::ConnectRoute controleert capaciteit vóór aanmaak. Player-slot a0 (`527ea0`) gaat via Player `4c9100` naar routepool `4b9c90`. Die controleert ook in de engine de uitgaande bronlijst tegen+194 en inkomende bestemminglijst tegen+190. Ook een geldige AI-utility bewijst dus geen geslaagde route. Bron: [interface](BINAIR/trade-goods-create-binding.txt), [Player-aanmaak](BINAIR/trade-goods-create-engine.txt), [poolchecks](BINAIR/trade-goods-limit-create-route.txt).

ConnectGoods kiest het hoogste positieve doel en markeert het na de verbindingspoging als voldaan. ConnectRoute vermindert de beschikbare handelscapaciteit alleen na succesvolle interface-uitkomst. Execute kan opnieuw kandidaten/biedingen berekenen wanneer de terugmeldvlag dat vraagt. De volledige caravankosten, Labyrinth-vrijstelling, verbinding/pathfinding en retrygevallen zijn nog open.

## 6. Offline verificatie en resterend werk

[Controleer-Handelsbod.py](../PROEVEN/Controleer-Handelsbod.py) voert originele instructies uit:15 controles van AI-bod/filter,8 van de engine-goodcomponent. **23/23 slagen**, [resultaat](BINAIR/trade-goods-benefit-checks.json). Ook een geval met verschillende lokale en beschikbare tellingen bevestigt gebruik van de beschikbare telling voor het bod. SHA-controle voorkomt stil toepassen op andere binaries. AI-interfaces, good-waardegetter, positie en resterende-rondescallback zijn expliciete mocks; de originele x87-berekening loopt. In de enginegevallen wordt alleen de recordgetter gestubd en stopt de uitvoering vóór andere stadsinkomsten/procentmodifier. Geen complete beurt of gameplaybenchmark.

Gerichte resterende schakels voor brede fase A:

1. Alle voorraadherbouwmomenten, reserveringen/offers en save-/loadgedrag; onderscheid beschikbaar, lokaal, aangeboden en nog te verzamelen.
2. Bevolkingsplaatsing voor bruikbare goods en overlap tussen steden; mogelijke wisselwerking met scientists.
3. Good-goud naar goudgebouwen, overheid/crime/onderhoud/science en werkelijk netto-opbrengst.
4. Routekosten/caravans, Labyrinth, piraterij/veiligheid en mislukte routepogingen.
5. Buitenlandse handel, monopoly-threshold50 en wereldvoorraad; de naam monopoly is geen bewijs dat alleen de driehoekformule speelt.
6. Pas in fase B een voorstel voor locatiescore/voorraadplanning; pas in fase C de effectief geladen regels en uitkomsten meten vanaf dezelfde benchmarkstart.
