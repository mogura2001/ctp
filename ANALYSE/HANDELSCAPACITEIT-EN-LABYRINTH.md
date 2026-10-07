# Handelscapaciteit, caravans en Labyrinth — fase A

Afgebakende overdracht, 6 oktober 2026. Onderzoek van bestaande CTP I-instructies; geen voorstel, spelstart of game-/binarywijziging. De goodwaardering, lokale bewerkte goods en vier stadsroutes zijn eerder behandeld in [GOODS-EN-HANDELSROUTES.md](GOODS-EN-HANDELSROUTES.md). Dit pakket sluit de afzonderlijke capaciteitspoort en wondervrijstelling.

## 1. Hoofdbevinding

Een caravan levert in de originele records één transportpunt. Een route gebruikt één punt. Labyrinth laat de engine routes aanmaken boven de beschikbare capaciteit, maar het aantal gebruikte punten blijft oplopen. De gewone AI-routefunctie vraagt eerst de ruwe beschikbare capaciteit op en stopt bij nul of minder. In deze keten benut de AI de Labyrinth-vrijstelling dus niet om zonder extra caravans verdere eigen good-routes te maken. Dit is een concrete beperking van de bestaande beslisketen, geen bewezen beschrijving van alle diplomatieke of menselijke handelsroutes.

De vrijstelling vervalt zodra **enige aanwezige speler** een obsolete advance van het wonder kent. Voor Labyrinth is dat Age of Reason; uitsluitend de wetenschap van de eigenaar controleren zou de gevonden implementatie verkeerd beschrijven.

## 2. Van records naar caravanpunten

OG `UNIT_CARAVAN` heeft `SHIELD_COST750`, `MAX_MOVEMENT1`, `ENABLING_ADVANCE ADVANCE_TRADE` en `IS_TRADER`. AAIP behoudt deze waarden. `WONDER_LABRYINTH_OF_THE_MINOTAUR` heeft basiskosten2160, Ship Building als enabling advance, Age of Reason als obsolete advance en `WONDER_FLAG_FREE_TRADE_ROUTES`. Die gameplayvelden zijn in AAIP gelijk; een commentaarverschil is geen regelwijziging. [Recordvergelijking](BINAIR/trade-capacity-labyrinth-aaip-records.txt), [OG Units](../CTP-og/ctp_data/default/gamedata/Units.txt), [OG Wonder](../CTP-og/ctp_data/default/gamedata/Wonder.txt).

De echte parser bindt `IS_TRADER103` via selector `46d108+(103−10)` en jumptable `46ce28` aan case36, `46bb01`. Die zet UnitRecord `+34 bit100`. `MAX_MOVEMENT49` wordt als double op `+a0` opgeslagen; dit is geen apart capaciteitstoken. Na gewone unitcreatie `4b4ef0→4ea960` filtert `4b5378` op het traderbit. De trader gaat in de afzonderlijke lijst `Player+12d0`; `4b53b6–4b53cc` haalt Record `+a0` op, converteert naar integer en voegt het toe aan **Player+98**. Bij de originele caravan is dat één punt. [Tokens](BINAIR/trade-capacity-labyrinth-canonical-tokens.txt), [dispatch](BINAIR/trade-capacity-labyrinth-trader-dispatch.json), [flagwriter](BINAIR/trade-capacity-labyrinth-flag-writers.txt), [MAX_MOVEMENT-parser](BINAIR/food-growth-unitdb-record-parser.txt), [creatie en counters](BINAIR/trade-capacity-labyrinth-caravan-and-route-counter.txt), [unitpool](BINAIR/trade-capacity-labyrinth-trader-unitpool-create.txt).

Dit volgt dezelfde queuevoltooiing als gewone units; de bekende eligibility en klasse1-queue zijn hergebruikt uit [BOUWDOELEN-EN-QUEUE.md](BOUWDOELEN-EN-QUEUE.md). De echte Deity-korting staat in [DEITY-KOSTEN-EN-TECHNOLOGIEFASEN.md](DEITY-KOSTEN-EN-TECHNOLOGIEFASEN.md). Basiskosten750 zijn daarom geen vaste werkelijk betaalde Deitykosten. Geen nieuwe volledige caravanbouw is geëmuleerd.

## 3. Capaciteit gebruiken en teruggeven

| Gegeven | Engine | AI-interface |
|---|---|---|
| Totale transportpunten | Player+98; getter4b9c80 | Playertable744660, slot9c→527e80 |
| Gebruikte punten | Player+9c | Onderdeel van de beschikbare-capaciteitsgetter |
| Beschikbare punten | 4b9c70: total−used, zonder clamp of wondercontrole | Slot98→527e60 |
| Kosten van een route | wrapper4d7250→pool4b23c0→4d9ba0: constant1.0 | De AI gebruikt beschikbare punten als integer |

[Interfacebinding](BINAIR/trade-capacity-labyrinth-player-points-interface.txt), [onverbruikte getter](BINAIR/trade-capacity-labyrinth-flag-list-build-and-unspent.txt), [routekost](BINAIR/trade-capacity-labyrinth-route-cost-getter.txt).

Routeaanmaak loopt via Player-interface `+a0→527ea0→4c9100→4b9c90`. De eigen goodroute heeft type0. Bij `used≥total` controleert `4b9d59–4b9d84` de actieve free-routewonderfunctie; zonder vrijstelling faalt deze toelatingsbranch. De afzonderlijke stadsroutecapaciteiten blijven daarnaast bestaan. [Volledige routeaanmaak](BINAIR/trade-capacity-labyrinth-route-create-full.txt).

Na routepoolcreatie registreert `4b9fb0` het verbruik. `4b9fef` schrijft `used+routecost` **ook bij Labyrinth**. Bij overschrijding controleert `4ba067` opnieuw de vrijstelling. Een route moet bovendien een niet-nul statusveld `RouteData+c4` hebben. Anders trekken `4ba0a9–4ba0b3` de eerder toegevoegde kosten weer af, wordt routeverwijdering met reden8 aangevraagd en krijgt de caller handle0. De geslaagde branch schrijft de routehandle bij `4ba1af`. De exacte bredere betekenis van statusveld+c4 en callback4d5440 is hier niet getypeerd. [Registratie](BINAIR/trade-capacity-labyrinth-final-bindings.txt), [rollback/return](BINAIR/trade-capacity-labyrinth-counter-returns.txt).

Bij verwijderen `4d6eb0→4d6ed0` bereikt het payerpad `4d70a4→4ba360`. Routewrapper4d71c0 leest payer `RouteData+24`. Als die overeenkomt met Player+0 en `RouteData+140` nul is, trekt `4ba391` één punt af van used. Total blijft staan; ook een eerder vrijgestelde route geeft zijn geboekte verbruik terug. Het guardveld+140 voorkomt deze aftrek wanneer gezet; `4d9bb0` zet het op1. Alle schrijvers/levenscyclus van dat guardveld zijn niet onderzocht. [Verwijderroute](BINAIR/trade-capacity-labyrinth-caravan-complete-and-release.txt), [payer/getters](BINAIR/trade-capacity-labyrinth-final-bindings.txt), [counterrelease](BINAIR/trade-capacity-labyrinth-caravan-and-route-counter.txt), [guardwriter](BINAIR/trade-capacity-labyrinth-route-cost-getter.txt).

## 4. FREE_TRADE_ROUTES werkelijk toegepast

Token487 is de canonieke wonderflag. Parser4705c0 berekent flagindex `487−455=32`, markeert de 64-bit recordmask op `+30/+34` en schrijft dus `+34 bit1`. De generieke flagcase accepteert deze vlag zonder extra getal. De echte databaseopbouw4711fb–4712d0 verzamelt per flag de recordindices; voor index32 staan count en lijst op WonderDB `+94/+26c`. [Flagparser](BINAIR/trade-capacity-labyrinth-flag-writers.txt), [generieke case](BINAIR/trade-capacity-labyrinth-route-cost-getter.txt), [lijstbouwer](BINAIR/trade-capacity-labyrinth-free-list-and-caravans.txt), [loopstaart](BINAIR/trade-capacity-labyrinth-effect-list-loop-tail.txt).

Actieve-effectgetter473280 loopt de betreffende wonderindices langs en intersecteert ze met de aangeleverde eigenaarsmask, in de Playercalls `+1170/+1174`. Recordlookup454760 gebruikt stride d0. Getter464860 leest **obsolete count Record+2c**; getter464850 leest **obsolete advance Record+c+4*i**. Zonder obsolete advances is het effect meteen actief. Anders controleert4732e0–47331e alle32 spelersslots, en per bestaande speler alle obsolete advances via echte known-getters4c2180→474b60. Zodra één ervan bekend is, vervalt dit wonder als effectbron. Een eventueel tweede free-routewonder kan vervolgens nog geldig blijken. [Actieve-effectfunctie](BINAIR/trade-capacity-labyrinth-create-and-free.txt), [exacte obsolete/getterbinding](BINAIR/trade-capacity-labyrinth-obsolete-and-trader-parser.txt), [record/known-getters](BINAIR/trade-capacity-labyrinth-final-bindings.txt).

Dit bewijst de vrijstellingstoets op nieuwe aanvragen, niet wat op de omslagbeurt met alle bestaande overcapaciteitsroutes gebeurt. De volledige obsolete-eventafhandeling en eventuele automatische annulering blijven open.

## 5. AI-selectie en terugkoppeling

`FSConnectTradeRoutes::Execute200292e0` vraagt eerst `GetBestFreight20025ea0`: de ScienceAgent moet een bruikbaar freightunitindex hebben. Deze getter leest de bestaande cache; dit pakket bewijst niet de volledige cachekeuze. De enabling advance Trade en gewone unitvoorwaarden blijven afzonderlijk van Ship Building/Labyrinth. [AI-caravanacties](BINAIR/trade-capacity-labyrinth-ai-caravan-action.txt), [bestaande routeroute](BINAIR/trade-goods-ai-route.txt).

`ConnectGoods20029950` vraagt via Player-slot98 de beschikbare punten op. `20029984` stopt bij nul of minder; de positieve lokale teller gaat naar `GoalRoute::Connect20048450`. Die vraagt stadsroutecapaciteiten op, probeert de engineaanmaak en verlaagt de teller bij succes. Hier ontbreekt een Labyrinth-vrijstelling van de voorafgaande capaciteitspoort. Zelfs wanneer de engine een route met total0 accepteert, doet deze AI-route geen poging. [ConnectGoods](BINAIR/trade-goods-ai-route.txt), [GoalRoute-aanvraag](BINAIR/trade-goods-connect-action.txt), [werkelijke capaciteitinterface](BINAIR/trade-capacity-labyrinth-player-points-interface.txt).

Caravanbouw ontstaat via een afzonderlijk `GoalFreight`. `PretestFreight2002b540` vereist routegoals en een lege stadsqueue. `InsertFreightGoal2002b7b0` telt positieve, onvervulde routegoals en berekent vervolgens het tekort:

`aantal gewenste routes + fz_freight_reserve − beschikbare punten − capaciteit van reeds ingeplande freightbouw`.

Voltooide caravans zitten al in total. `IsConstructingFreight2001c410` vergelijkt de gecachete bouwunit met bestfreight en leest bij gelijkheid diens integercapaciteit via UnitDB-slot18. De functie trekt die output af en maakt alleen bij positief resterend tekort een GoalFreight. Dit is geen vaste AIP-caravanunitquota. Ook hier is in de gevolgde functie geen actieve free-routewondertoets aanwezig. [Pretest/tekort/planner](BINAIR/trade-capacity-labyrinth-ai-freight.txt), [ingeplande capaciteit](BINAIR/trade-capacity-labyrinth-queued-freight.txt).

`EnqueueBuildFreight2001d3a0` gebruikt bestfreight, de gewone Player+50-aanvraag met klasse1, en de stadsbuildcache. `RegisterBuiltFreight2001c5d0` verwerkt de voltooiingsmelding in die cache/doelcallback. De volledige engine→AI-eventdispatch is niet opnieuw gevolgd. OG en AAIP initialiseren `freight_coef` beide op100 in init.fli68; de actieve fuzzy oorsprong/default van `fz_freight_reserve` en de volledige GoalFreight-rawutility worden hier open gelaten. [Enqueue/cache/event](BINAIR/trade-capacity-labyrinth-ai-caravan-action.txt), [OG init](../CTP-og/ctp_data/default/aidata/init.fli), [AAIP init](../CTP-AAIP/ctp_data/default/aidata/init.fli).

## 6. Verificatie en resterende grenzen

[Controleer-Handelscapaciteit.py](../PROEVEN/Controleer-Handelscapaciteit.py) voert **23/23 controles** op originele engine-instructies uit: twee flagwriters, vijf ruwe beschikbaarheidsgevallen, vier actieve-effectgevallen, zes registratie/rollbackgevallen, drie releasegevallen en drie tradercapaciteitswrites. [Definitieve uitkomsten](BINAIR/trade-capacity-labyrinth-controls.json).

De wonderpredicate gebruikt echte record-, obsolete- en known-getters met synthetische records/spelers; alleen de CRT64shift wordt vervangen. Charge/release gebruiken echte routecost1 en echte vrijstelling, maar routepoollookup, UI, notificatie en delete zijn expliciete recorders/mocks. De tradercontrole voert alleen het reeds bereikte countersegment uit; zij bewijst geen gehele unitcreatie of gamebeurt. FTOL bewaart de x87-controlword; integerroutekosten maken deze gevallen niet afhankelijk van een ongeteste fractiedrempel.

Een eerste fixture had de obsolete-recordvelden verkeerd ingevuld en gaf twee afwijkingen. De echte getters toonden+2c/+c; fixture gecorrigeerd en eerste uitkomst behouden in [eerste obsolete-fixture](BINAIR/trade-capacity-labyrinth-first-obsolete-fixture.json). De verwachte spelregel is niet aangepast om een test te laten slagen.

Engine SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp37d6f702, imagebase400000; AI matching map/binary blijft de bestaande binding37b894e7/base20000000. De niet-passende civctp.map levert geen engineadressen.

Essentiële open grenzen: bestaande overcapaciteitsroutes op obsolete-omslag; caravanverwijdering/herstel van total; volledige freightreserve/utility en bestfreight-cache; buitenlandse handelsaanvragen/diplomatie; volledige queue/event/schedulerafhandeling en werkelijk spelgedrag. Deze grenzen blokkeren de hier aangetoonde capaciteitspoort niet. Ze horen bij vervolgdekking, niet bij een claim dat brede fase A klaar is.
