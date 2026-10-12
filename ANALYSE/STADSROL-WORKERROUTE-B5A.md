# B5a: stateless workerroute voor productiesteden

Gerichte fase A, 10 oktober 2026, 18:25 Europe/Amsterdam. Tussendoel **productiesteden goed inzetten**: drie verschillende bergwerkers en één voldoende voedselwerker bij omvang4, onder echte toelatingschecks. Alleen het eerste technische ingreeppunt/reset/afronding, stad/inwoner/tilebinding, overlap en herberekening zonder nieuwe savevelden onderzocht. Geen B-ontwerp, patch, native harness, liveprobe of spelstart. Ownership uitsluitend dit bestand en VOORTGANG-ANALIST-B5A.md.

**Voldoende voor B.** De concrete route is `FSAllocatePopulation2002a820 → CityAgent::PlaceAllPop20020bd0 → SatisfyMinimumCityRequirements20020eb0`, met het kleine invoeggebied vóór de eerste minimumfoodcall **20020fa9**. Daar zijn centrumtallies geïnitialiseerd en de eerste entertainerfase al uitgevoerd. Voor herstel is de omvattende call **20020d81** de passende grens: oorspronkelijke reset/list/counters opnieuw opbouwen en de oorspronkelijke minimum-/utilityroute vervolgen. Blind vier workers vóór20020d81 plaatsen is onjuist: de minimumroutine initialiseert haar food/prodtallies opnieuw en entertainers hebben dezelfde inwoners nodig. B moet expliciet kiezen hoe bestaande geluksvoorwaarden prioriteit behouden en wanneer herallocatie plaatsvindt. Nieuwe persistente rolmetadata is voor een actuele, per allocatie opnieuw berekende taak **niet technisch noodzakelijk**.

## Dekkingsmatrix

| Beslisschakel | Huidige werking / concrete binding | Route en voorwaarden | Open grens voor B |
| --- | --- | --- | --- |
| Allocatie-entry / trigger | Execute2002a820 heeft vier PopNeedsChanging-calls en vier PlaceAllPop-calls; één binnenroute bereikt alle citylistgroepen. PopNeedsChanging200209f0 controleert bestaande gewichten/flags/status en daarna turn%5 tegenover listindex%5. | Hergebruik één PlaceAllPop-/minimumroute; bepaal taak bij elke werkelijk uitgevoerde allocatie uit actuele stad/wereld. | Behouden fasering versus gerichte vroegere invalidatie is een expliciete ontwerpkeuze. Een nieuwe rolhook wordt niet vanzelf elke beurt aangeroepen. |
| Stad voorbereiden | PlaceAllPop20020bd0 leest echte totalen/Population-status, reset eigen citizens en bouwt actuele twintig kandidaatvakjes. | Originele volgorde en foutchecks bewaren; geen eigen poparray/cellwrites. | Geen garantie dat elke geometrische vierplekcombinatie uitvoerbaar is. |
| Plan vóór minimumfood | Minimumroutine initialiseert centrumproductie/food op20020eda..20020f08; SupplyEntertainers20020f56 gaat vóór minimumfood20020fa9. | Pas na deze initialisatie plannen/plaatsen met dezelfde tellers en kandidaatlijst; daadwerkelijke geluksbehoefte moet voor het vierworkerplan gedekt zijn. | Finale min_happiness-bardfase200210f1 mag niet door lege counters worden uitgehold. B moet onhaalbare vierworkerplannen afwijzen/fallbacken. |
| Echte workeractie | Population+60→52c6e0→4c9fe0→510d00→5005d0→4ccb00→4cd660. | Exact cityID, geldige inwonerindex/civ/externe positie; bool én foutoutput toetsen. Alleen geslaagde actie in counters/tallies/lijst verwerken. | PlaceACitizen20021500 negeert zijn aanvraagresultaat; die helper is geen veilige nieuwe commitprimitive. |
| Overlappende vakjes | Enumerator filtert huidige worker en city; finale Cell/Popcode herhaalt checks en schrijft één Cell+18-handle. | Alleen actuele open plekken gebruiken; bij afwijzing het plan verwerpen/herplannen. | Eerder toegewezen worker blokkeert latere stad. Geen globale bergketenoptimalisatie, nieuwe reservation of andere stadsvoorrang aangetoond. |
| Mislukte deelcommit / afronding | Player+11c is echte reset; +24c/+250 zijn conditionele snapshot/changed-pop-synchronisatie. Oorspronkelijke minimumtail ververst AI-citygetters, dan Maximize en +250. | Herstel dezelfde allocatie naar volledige gewone verdeling; oorspronkelijke afronding eenmaal behouden. | Reset is bevolkingherplanning, geen volledige rollback van engine-neveneffecten. Fallbackvoorwaarden hieronder zijn nodig. |

## Bewijsbasis en nieuwe beperkte lezing

Hergebruikt: [bevolking](BEVOLKING-EN-SCIENTISTS.md), [stadsopbrengsten](RANTSOENEN-EN-STADSOPBRENGSTEN.md), [stadsgebied](IMPROVEMENTCONSTRUCTIE-EN-STADSGEBIED.md), [bardvoorwaarden](BARDS-EN-GELUKSVOORWAARDEN.md), [terrein](TERREIN-EN-IMPROVEMENTS.md), [H2-terreinbinding](PRODUCTIEKANDIDAAT-H2.md) en [B5-opdracht](../ONTWERP/VERBETERPLAN.md). Bestaande27/27 bevolkingcontroles niet herhaald.

**B = machinecode**, **I = route-inferentie**; geen nieuwe runtime-/gameplaywaarneming. Voor de beperkte nieuwe enginelezingen zijn originele enginehash/base/timestamp bevestigd: SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`,400000,37d6f702. Robotcom SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`,20000000,37b894e7; Robotcom.map timestamp/imagebase passend gecontroleerd. Geen civctp.map gebruikt. Alleen benoemde callees via inline read-only pefile/capstone gelezen; geen nieuw scriptbestand, test, executable-reconstructie of procesactie.

### 1. Entry, werkruimte en ABI

**B:** [allocation-entry](BINAIR/population-scientists-allocation-entry.txt) legt PlaceAllPop vast als **thiscall**: ECX=CityAgent; stackargs AiMain*, vijf doubles food/productie/gold/science/happiness, twee longs; `ret34h`. Geen nieuwe cityrolparameter. CityAgent+0c is het bestaande stads-ID; AiMain+20 civ, +2c Playerinterface, +30 Worldinterface, +40 Populationinterface. CityAgent+210 is de bestaande positiepointer, door FindOpenTiles via SetPos2001c350 opnieuw ververst.

PlaceAllPop heeft lokale inwonerindices/remainers op ebp−8/−c voor de afzonderlijke groep en ebp−4/−10 voor gewone burgers. Totaal komt in EBX. De twintig TileUtility*-entries beginnen op ebp−60; records staan in dezelfde stackframe op ebp−420. Recordstride30h, positie op+28 (externe MapPointData in acht bytes), fooddouble+8/productiedouble+10/golddouble+18/extra+20. Geen pointer of rolplan daarbuiten bewaren. [FindOpenTiles](BINAIR/terrain-food-v2-ai-tile-input.txt) vraagt World+ac en Player+120 voor huidige stadsgebonden tilewaarden, geen raw terrainopbrengst invullen.

**B:** SatisfyMinimumCityRequirements20020eb0 is eveneens thiscall, `ret54h`: AiMain*, vier long&-tellers, totaal, TileUtility**, zeven doubles. Vanaf zijn eigen EBP: +0c/+10 afzonderlijke index/remain, +14/+18 gewone index/remain, +1c totaal, +20 lijst; centrumproductie op ebp−0c, centrumfood op ebp−14. Call20020d81 kan een begrensde wrapper dezelfde interface laten behouden; ingevoegde logica moet nonvolatile registers, stackcleanup en x87-toestand behouden. Dit is een gebonden ingreeproute, geen al ontworpen emitter/patch.

### 2. Reset en afronding: drie slots zijn niet hetzelfde

**Nieuwe B:** Player-vtable744660 heeft +24c=52b4e0, +11c=528680, +250=52b520. De oorspronkelijke volgorde is calls20020cec/20020d00, FindOpenTiles20020d14, UpdateProductionBonuses20020d2a, minimum20020d81, eventueel Maximize20020dd4, afronding20020de3.

| Slot / ABI | Gemeten machinecode | Betekenis / grens |
| --- | --- | --- |
| +24c: stdcall(PlayerInterface*,cityID), ret8 | 52b4fd resolveert stad via4cb060;52b514 roept CityData49e6c0. Bij globalA44C9C≠0 worden via4ce680 poptype+19→+1f, positie+20/+24→+30/+34 en placementstate+1c→+1d gekopieerd. | Beginvergelijking/synchronisatie van bestaande popstate; **geen werkerreset**, geen gegarandeerde algemene yieldrefresh. |
| +11c: stdcall(PlayerInterface*,cityID,outError*), ret0c | 528680 resolveert stad, roept49db10 voor huidige specialistvoorwaarden, loopt huidige CityData+584.count/+590.pophandles;528739/52873b/528740 vraagt4cc9e0(1,−1). | Echte reset van alle inhabitants van deze stad naar niet-tileplaatsing via4cdf20. Eigen bestaande workerposities komen vrij. |
| +250: stdcall(PlayerInterface*,cityID), ret8 | 52b53d resolveert stad;52b554→49e710. Bij dezelfde global doorloopt die pophandles en4ce6a0 vergelijkt bewaarde/currenttype, positie en placementstate; afwijkingen voeren bestaande synchronisatiecalls uit. | Eindvergelijking/synchronisatie; **geen bewezen volledige stadsopbrengstfinalisatie**. Behouden aan de oorspronkelijke uitgang. |

Concrete resetketen: `528740→4cc9e0→4cdf20`;4cdf51..4cdf66 zet bij overgang naar niet-tile de oude workerhandle nul via `510fa0→5005b0`;5005b6 schrijft **Cell+18**. Daarna Pop+1c=1 en positiecomponenten−1; argument−1 laat4cde00 het huidige specialisttype onder gebouw/omvang/regeringschecks valideren. [Bestaande +11c-prefix](BINAIR/population-scientists-engine-interface.txt), nieuwe vervolgadressen in deze analyse.

**B:** oorspronkelijke minimumtail200210f6..2002113b bewaart Population+5c/+50/+54-opvragen in bestaande CityAgentvelden en roept CalcEstimatedCityProduction2001c970. Niet rechtstreeks naar PlaceAllPop-exit springen na workerplaatsing: deze tail, gewone resterende allocatie en +250 horen bij de route. Geen nieuwe engine-yieldcyclus/savehook onderzoeken om dit bestaande pad te behouden.

### 3. Stad, inwoner en finale toelating

**B, bestaande wrapper plus gericht vervolg:** Population-vtable744948+60=52c6e0. ABI **stdcall** `(PopulationInterface*, uint32 cityID, int32 inhabitantIndex, int32 civ, externalMapPointData*, int32* outError)`, `ret18h`, EAX bool. Wrapper valideert positiecomponenten tegen kaartbounds, converteert via503f00 en neemt de echte Player uit interface+8. Een vroeg afgewezen positie retourneertfalse zonder gegarandeerde foutoutputwrite: EAX apart toetsen, foutoutput vooraf initialiseren. Index ook expliciet `0≤i<total`; het gevolgde Playerpad controleert de bovengrens, geen algemene negatieve-indexveiligheid aannemen.

4c9fe0 zoekt **dit cityID** in Player+12c8; de gevonden index resolveert via Player+12c0-array/4da8b0 een stad met CityData op+58. Total via49a420; inwonerhandle uit CityData+590[i]. Output is eerst1 bij onvindbare stad/te hoge index en wordt0 vóór het Worldrequest. Dat0 bewijst geen tilesucces: World/Pop kan nog afwijzen en EAXfalse teruggeven. Geen gegokt poprecord-ID, eigenhandle, stadindex of directcellwrite nodig.

De volledige noodzakelijke plaatsingspoort:

```text
52c742 ->4c9fe0
4ca0b8 ->510d00
510d27 ->5005d0
5005d7/+14 cityhandle !=0: reject
5005de/+18 workerhandle !=0: reject
5005e5..500623: bestaande army-/owner/diplomatiepredicate, niet omzeilen
50062c ->4ccb00 ->4cd660(PopData*,internalPos*)
4cd69c ->4dcfc0 ->4e53c0: stadgebonden radiuspredicate
4cd6c9: eigen centrumpositie: reject
4cd703..4cd748: andere worker: reject
4cd76a..4cd786: andere cityhandle: reject
4cd789..4cd82a: bestaande armychecks opnieuw
4cd885 ->510fa0 ->5005b0: nieuwe Cell+18=deze pophandle
4cd88a..4cd898: placementstate0 en nieuwe poppositie
4cdaad..4cdac2: bool1, ret4
```

4e53c0 vereist werkelijk CityData (+58), geeft centrumpositie door aan4e47e0 en vergelijkt resultaat met double6.25 op744008. De eigen afstand-/wrapformule hoeft niet te worden nagebouwd: Populationrequest behoudt deze native predicate. Geen eigen vierkante-radiuscheck als substituut.

**Overlapconclusie B/I:** er is één workerhandle per cel. Enum534510/511030 sluit een huidige worker/stadcentrum uit; de finale plaatsing weigert die toestand opnieuw. Binnen de huidige sequentiële allocatie blijft een eerder toegewezen worker een blokkade voor een latere stad. De reset geeft uitsluitend deze stadsinhabitants vrij; hij vraagt geen andere stad haar workers af te staan. Een per-stadplan moet vier unieke **actueel open** posities kiezen. Geen globale optimum-, beurtvolgordeprioriteit of planningsreservation uit deze code afleiden.

### 4. Kleinste inpassing met betrouwbare fallback

**I:** laat rol/plan tijdens de huidige allocatie uit opnieuw verkregen open tiles, actuele stad/inhabitants en echte opbrengsten ontstaan. World+a8→5342e0/ret0c leest bergindices8/20/22; bestaande tile-/centrum-/hungeropvragen rekenen actuele modifiers en rantsoenen. Een toekomstige mine/farmopbrengst mag niet als huidige voedseldekking tellen. Een plan voor vier gewone workers past niet automatisch bij slaven/bards/meer of minder bevolking; B moet ondersteunde toestand expliciet begrenzen en overige gevallen gewone fallback geven.

De eerste **plaatsings**gelegenheid vóór minimumfood is **na20020f56, vóór20020fa9**. De eerdere vóór-entertainergelegenheid kan een plan alleen voorbereiden: het vierworkerplan mag de geluksbehoefte niet opeten. Ook de latere echte min_happiness-grens op200210f1 moet worden afgedekt voordat alle vier gewone inwoners worden gebruikt. Alleen behoud van de eerste entertainercall is hiervoor onvoldoende; die heeft een eigen tijdelijke callergrens. Deze noodzakelijke keuze gaat naar B: haalbaar plan met nul benodigde bards onder alle behouden voorwaarden, anders gewone verdeling. Geen toegestane honger/geluksovertreding om drie miners te tonen.

B kan de eerste minimumfoodcall met dezelfde ABI omgeven en de omvattende20020d81-grens gebruiken voor herstel. Gebruik de bestaande Population+60-toelating voor **elke exacte geplande plek**, verwerk uitsluitend succesvolle commits in indices/remainers, CityAgent+b8 en +d8/+dc, de gezamenlijke food/prodtallies en kandidaatentries. Geen gebruikte tile opnieuw door de minimum-/utilityfase laten kiezen. [PlaceACitizen](BINAIR/population-scientists-minimum-placement.txt) op20021554/2002163c controleert EAXniet maar telt/verwijdert toch; die oorspronkelijke tekortkoming mag een nieuw geslaagd workerplan niet bewijzen. [PutCitizenBestTile](BINAIR/population-scientists-utility-actions.txt) controleert succes wel, maar kan naar een andere kandidaat doorlopen en bewijst dus niet dezelfde vierplekcombinatie.

**Noodzakelijke veilige fallback bij gedeeltelijk mislukte commit:** niet verdergaan met alsof alle vier aanvragen geslaagd zijn. Binnen dezelfde allocatie, vóór de gewone afronding, via de echte +11c alle inhabitants van deze stad opnieuw resetten; counters/status uit echte Population opnieuw bepalen, eigen bestaande tileboekhouding/tallies terugzetten en FindOpenTiles/UpdateProductionBonuses opnieuw gebruiken. Daarna **zonder een tweede rolpoging in die invocation** de volledige oorspronkelijke minimum-/utilityroute uitvoeren, inclusief alle entertainerfases, refresh-tail en oorspronkelijke +250. Geen bewaarde pointer/lijst of tallies van vóór de gedeeltelijke commit hergebruiken. Een call-local bypass kan dit begrenzen; geen saveveld nodig. B moet de exacte wrapper/abortverbinding en cleanup uitwerken; in A geen implementatie gedaan.

Dit is **herplanning van bevolkingsplaatsing**, geen bit-identieke rollback van alle engineeffecten.4cd837..4cd84e kan bij veranderde tileowner de bestaande owner-/territoryroute uitvoeren; plaatsing voert ook bestaande meld-/synchronisatiecalls uit. Reset maakt Cell+18 vrij maar wist niet aantoonbaar al die neveneffecten. B moet expliciet een veilige ondersteunde eigenaarscontext en fallbackclaim kiezen; geen zelfgemaakte territory-/eventrollback. Bij ongeldig geworden stad/owner/bounds of mislukte reset geen verdere gegokte commit: stop deze rolroute onder de bestaande hostfoutafspraak. Geen volledige territory-/netwerkreconstructie nodig om dit ontwerpcriterium te benoemen.

### 5. Geen nieuwe rolpersistentie nodig, maar de trigger blijft een keuze

**I op B:** een plan dat alleen deze allocatie bestuurt, kan geheel uit bestaande actuele stad, inhabitants, beschikbare tiles en opbrengsten worden berekend en na terugkeer verdwijnen. De engine bewaart haar gewone workerstate; de nieuwe route voegt geen rol-ID, gereserveerde tilepointer of save-record toe. Dit ondersteunt een *huidige productiegeschiktheid*, niet vanzelf een permanente rol die later queues/wonders/improvementuitzonderingen blijft sturen. Dat verdere beleid hoort bij latere B5/B6, niet bij deze blocker.

**B:** PopNeedsChanging is thiscall ECXCityAgent, args AiMain*, drie doubles plus citylistindex, `ret20h`. Rechtstreekse caches+110/+118/+120 dekken productie/food/gold. Science/happiness, een nieuwe rol, minebouw, voedselverbetering of tileclaim worden daar niet rechtstreeks vergeleken. Bestaande statuschecks kunnen herallocatie triggeren, maar alle mogelijke rolwereldwijzigingen zijn daarmee niet bewezen gedekt. Bij geldige ongewijzigde toestand geldt de laatste5-fasering; foutoutputs van eerdere statusqueries kunnen zelfs eerderfalse leveren. Dus geen onvoorwaardelijke garantie 'ieder nieuw plan werkt volgende beurt'.

B moet kiezen: de bestaande trigger/fasering houden met duidelijk vertraagde herbeoordeling, of een **gericht gebonden actuele taak-check vóór de bestaande gate** toevoegen die eerdere herallocatie vraagt. De vier bestaande sites zijn2002a8c5/2002a959/2002aa1f/2002aad5; PlaceAllPop-sites2002a91b/2002a9b0/2002aa73/2002ab82. Niet alle Population-statuschecks blindtrue maken. Een taakcheck vóór reset moet rekening houden met eigen al gewerkte vakjes: World+ac noemt die bezet, dus alleen open bergen tellen is daar geen goede test van een bestaande rol. De minimale per-allocatieroute zonder vroegtrigger vermijdt die extra taakcheck; B mag deze keuze expliciet maken. Geen volledige cachedstatus/savecallerreconstructie vooraf vereist.

## Overdracht en acceptatie

| Tussendoel | Daadwerkelijke voortgang | Acceptatiestatus | Eerstvolgende oplevering |
| --- | --- | --- | --- |
| Productiesteden goed inzetten / B5a | Entry, echte reset/afronding, city/pop/tile-ABI, finale overlapchecks en stateless route gebonden | Gerichte analyse gereed voor B; geen workerwijziging of gameplay aangetoond | Ontwerper werkt één beperkt B5a-voorstel uit met ondersteunde vierpoptoestand, voedsel/geluksvoorwaarden, exacte invoeg-/fallbackgrens en triggerkeuze. |
| Goede locaties / workerafhankelijkheid | Geometrische bergen onderscheiden van op dit moment werkelijk toewijsbare werkplekken | H3-offlineacceptatie ongewijzigd; geen globale rol-/claimprioriteit bewezen | B5a gebruikt actuele legaliteit; latere globale roltoewijzing apart. |

Niet-blokkerende backlog: globale overlapoptimalisatie/hysterese, permanente rolemetadata voor queues, complete netwerk-/meldingsemantiek, alle Population-status/savecallers. Alleen gericht terug naar A als het concrete B-voorstel een van die schakels noodzakelijk maakt. Geleverde adressen/voorwaarden volstaan voor de eerste stateless workerroute; geen extra harness of gamereconstructie nodig.

Analist stopt na overdracht. Pc aan; geen shutdown/helper/timer. Laatste eigen budget18:25:39, bron18:24:52 (46.9s): week80/vijfuur73/stateok. PROJECTSTATUS blijft rootownership. Onafhankelijk van pending H1-livegoedkeuring, geen spelactie uit deze A.
