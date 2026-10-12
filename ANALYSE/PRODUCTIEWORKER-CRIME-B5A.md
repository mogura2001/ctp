# B5a: vier gewone werkers, kandidaatgeluk en criminaliteit

Gerichte A-terugvraag, 10 oktober 2026, 18:51 Europe/Amsterdam. Alleen de overgebleven Happiness/crimebinding voor het driebergen+foodplan; de [foodformule/inputroute](PRODUCTIEWORKER-NETTOFOOD-B5A.md) blijft afgerond. Geen game/live/patch/harness/tests; ownership uitsluitend dit bestand en VOORTGANG-ANALIST-B5A-CRIME.md.

**Uitkomst:** de normale engine heeft een concrete projectie/queryroute die geen worker-/territoryplaatsing vraagt en de echte gebouw-/wonderbonussen behoudt. De bestaande Population+40-uitvoer alleen is echter aantoonbaar geen volledige kandidaatHappiness. Voor de algemene voedselgate blijft één gerichte binding open: de actualiteit van drie componentcaches die het normale projectiepad bewust hergebruikt, op de B5a-allocatiegrens. Dit is de minimale vervolgkennis; geen hele Happy-/PlayerRoundsreconstructie nodig. Normale cache/detailrefresh is toegestaan als ontwerpkeuze, geen fictieve Hwrite of ongevalideerde oude crimecache.

## Beslisketen en bewijs

| Vraag | Aangetoond | Overdracht/open |
|---|---|---|
| Is Population+40 direct de exacte kandidaatH? | Nee:4abd10 laat Happy+28,+a8 en Player+1188 weg ten opzichte van4ab410; verschil ligt vóór de begrensde martial law. | Ook `getterH + gemiste termen` achteraf is algemeen onvoldoende wegens cap. |
| Heeft de engine een echte projectiequery? | City49c990 gebruikt Happy4ab410 met `(City,1,outInt,0)`, vervolgens productiequery, daarna scalarrestore4aa2f0. | Concrete normale protocolkeuze beschikbaar;49c990 zelf retourneert productie, geen H/crime. |
| Welke sideeffects/flags zijn werkelijk gebonden? | Projectie1/advance0 voorkomt durationlijstafboekingen en timer94-decrement. Andere caches/details worden vernieuwd; anger+28 wordt tijdelijk vervallen en via originele queryrestore hersteld. | Geen algemene sideeffectvrije getterclaim. Niet extra normalen-turnflags0/1 gebruiken. |
| Waar kan exact nulbard-H ontstaan? | Normale finalisatie4abcb7..4abcc6: actuele wonder+gebouw+barterm+prebardH; bards zitten pas hier, na martial law. | Voor vier betaalde fieldworkers met dezelfde contentmentflag en luxury0 is barterm0. Exacte rekenvolgorde behouden, geen losse aftrek uit afgerond totaal. |
| Zijn alle combinaties gelijk in H? | In deze expliciete sloten worden alleen popcontentmentflags en luxury gelezen; geen werkervakjesposities. Centrum/eigenaar/WGF/gebouwen/wonders blijven echt. | Brede claim pas bij de genoemde componentcachebinding; geen bonusrijke gewone steden uitsluiten. |
| Is de volledige huidige-contextactualiteit bewezen? | Projectieadvance0 gebruikt Happy+a0,+30,+a8 als caches. Query noemt geen versheidstag. | **Open: exact deze cache-epoch/current-inputbinding bij allocatie.** |

**Bewijsniveau:** machinecode uit bestaande dumps plus kleine complete vervolglezingen49c990,4a9f20,4aa2f0 en een49cc00-callervenster. Laatstgenoemde blijkt een goud/loonquery en is geen H-route; niet verder onderzocht. Geen runtime-/gameplaywaarneming. Engine SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, base400000, timestamp37d6f702 opnieuw bevestigd; Robotcom-pins uit bestaande workerroute. Geen civctp.map gebruikt.

## Waarom de oorspronkelijke non-bard-query niet volstaat

Population+40 is stdcall `52c460(PopulationInterface*,cityID,int* error,double* H,double* bardEffect)`, ret14h. Hij resolveert dezelfde ownerPlayer via interface+8/citymap, CityData via UnitData+58, en roept `4abd10(this=City+5cc,CityData*)`, thiscall/ret4,double ST0. De caller20021734 schrijft H naar ebp−0c, effect naar ebp−14, error naar ebp−4; vóór20021748 staat daar de oorspronkelijke non-bard-uitvoer. Dat blijft bruikbare AI-invoer voor de bestaande bardgrenzen, geen exacte foodcrimegarantie. [Query/caller](BINAIR/happiness-bards-engine-input.txt), [SupplyEntertainers](BINAIR/happiness-bards-ai.txt).

Concrete tegenbinding uit de volledige bestaande lichamen:

-4ab681..4ab6bb verwerkt/vervalt Happy+28 en telt hem mee;4abd10 doet dit niet.
-4aba20..4aba3b telt `Player4c35a0() + Happy+a8` mee.4c35a0 leest actuele signedint Player+1188.4abd10 doet dit niet.
-Dit gebeurt **vóór** de hoofdroute-cap4aba60..4abad8, terwijl4abd10 zijn eigen cap4abec7..4abf1a op het kleinere subtotal toepast. Daarom corrigeert een simpele toevoeging na de query die cap niet altijd.
-De hoofdroute heeft daarnaast echte overridebranches Happy+94, Wonder471e40 en Building45d910, die de gewone finalisatie kunnen omzeilen;4abd10 heeft alleen de owner0-uitzondering aan zijn begin. Geen universele gelijkheid voor gewone steden met veel bonussen claimen.

[Hoofdroute](BINAIR/economy-city-crime-full-update.txt), [Playerextra](BINAIR/happiness-wgf-setter-and-final.txt). Dit is positief machinecodebewijs van ontbrekende termen/branches, geen numerieke runtimevergelijking.

## Concrete normale query, ABI en sideeffects

`4ab410(this=Happy*,CityData* city,int projection,int* martialLawOutput,int advance)`, thiscall, ret10h, geen H-return in ST0/EAX: de H/crime-uitvoer wordt in Happy+0/+b0 opgeslagen. Owner wordt in4ab421..4ab427 uit de **echte City+4** en globalPlayersA7DD80 gehaald. CityData blijft via de eerder gebonden CityAgent+0c/AiMain+2c-cityID-route komen; actualowner moet AiMain+20 zijn.

De bestaande cityquery49c990 is thiscall `(CityData*,int* productionBefore,int* productionAfter)`, ret8. Hij doet:

```text
49c9cc:4a9f20(this=&privateHappySnapshot,source=actualHappy)
49c9ed:4ab410(this=actualHappy,actualCity,1,&localInt,0)
49c9fd:restore actualCity+38
49ca04:494280(actualCity,...,1)       # productiequery, niet nodig als H-query
49ca34:4aa2f0(this=actualHappy,source=&privateHappySnapshot)
49ca46:4aa000(this=&privateHappySnapshot)
49ca5b:ret8
```

Deze normale route bewijst een bestaand query/snapshot/restoreprotocol; geen worker-/territoryactie in dit callerlichaam. Zijn productiecache-updates zijn wel echte sideeffects. B kan een **beperkte H-query volgens dit gebonden protocol** ontwerpen;49c990 blind als H/crimegetter aanroepen levert geen bruikbare H-output na return omdat die hersteld is.

Flagbetekenis begrensd door code:4ab410 passeert projection/advance aan4ab0f0;4ab175/4ab17e doet durationlijstaftrek uitsluitend bij `advance!=0 && projection==0`. Met1/0 wordt de bestaande Happy+a8-summary gelezen zonder lijstdecrement. Happy+94 wordt alleen gedecrementeerd als advance!=0 op4ab4cc..4ab4e1. De afzonderlijke anger+28-decay4ab681..4ab699 is **niet** door die flags uitgeschakeld: queryrestore is relevant, niet optioneel wegdenken. [Duration/flags](BINAIR/happiness-wgf-engine-base.txt), [hoofdroute](BINAIR/economy-city-crime-full-update.txt).

4a9f20 is de bestaande snapshotconstructor, thiscall(ret4), met eigen durationcontainer/detailsallocaties.4aa2f0 is scalarassign, thiscall(ret4), en kopieert onder meer H+0,anger+28,bard+70,building+78,wonder+80,crime+b0,forcecounter+94. Hij kopieert **niet** Happy+a0/+a8 of de ownerpointers+b8/+bc. Daarom is een snapshot geen algemeen zelfstandig volledig gekloond Happy-object waarop willekeurig nieuwe flags kunnen worden uitgevoerd. Het bestaande projectiepad houdt die niet-gerestaureerde caches juist onveranderd. De detailupdates op de originele Happy+bc blijven echt; de normale constructor/destructor/pointerlevensduur moet B behouden. Geen bytecopy of tijdelijke PopData/CityDatavervalsing gebruiken.

Normale full-refreshcaller4926b4 gebruikt `(City,0,&local20,1)`. Dit is een beurtupdate met duration/timer/componentupdates, geen equivalent van de projectiequery. De aanwezigheid van die caller bewijst niet dat hij precies vóór onze allocatie heeft plaatsgevonden. [Bestaande callers](BINAIR/economy-city-crime-city-object.txt).

## Nulbard-kandidaat en exacte finalisatie

Voor vier **gewone betaalde** inhabitants moeten de werkelijk geladen recordflags contentmenttotalbit4 behouden; geplande fieldrecord(s) moeten luxury0 hebben, te valideren via de echte recordroute van4ccc20. De gewone workerrecordwaarde is BONUS_LUXURY0; geen nieuwe recordoffset raden. Hcount City+38 blijft4 en de poplijstomvang blijft4. Slaven/afwijkende flags vallen buiten deze gewone vierpopcontext; alle normale gebouw/wonderbonussen blijven in de query.

De hoofdroute leest poprecords op slechts de noodzakelijke plaatsen:4ab469→4cccb0 voor de contentmenttelling;4abb39→4ccc20 voor luxury/bardbijdrage. Vóór4abad8 is geen bardbijdrage toegevoegd. Centrumgebonden garrison4aad10 blijft hetzelfde centrum/echte garnizoen; ordinary workerlocaties zijn geen garrisonposities. Op de normale finalisatie is:

```text
P = Happy+0 op4abcb7, na contentment/WGF/overige context en martial-lawcap
W = double(ebp-10), tevens Happy+80
B = double(ebp-08), tevens Happy+78
E = double(ebp-18), tevens Happy+70 (actuele specialistluxury)
normale H = double(x87(W+B+E+P))
kandidaat met vier gewone luxury0 fieldworkers: Hcandidate = double(x87(W+B+0+P))
```

4abcb7/4abcba/4abcc1/4abcc4/4abcc6 tonen precies die optellingen/spill. Een ontwerp moet deze echte queryfinalisatie observeren/gebruiken als het een bitexacte kandidaatwaarde wil; `afgerond Happy+0 - afgerond Happy+70` is een algebraïsche benadering en kan op afrondgrenzen verschillen. Dit pinpunt is een mogelijk B-ingreeppunt, geen toegepast observer-/patchontwerp. Native call4abcc8 berekent vervolgens crime uit de **werkelijke** H op Happy+0; zijn cache mag niet worden gebruikt als candidate-E nog niet0 was.

De eerder genoemde gewone gebouw-/wonderoverridebranches blijven meegenomen: als de echte query de normale finalisatie overslaat, kan die branch niet langs het nulbard-finalisatiepinpunt worden behandeld. B moet de echte branch-H en crimeverversing gebruiken. Bij de vroege exits wordt4abcc8 niet bereikt; zelfs een normale native-query is dan geen bewijs dat de bestaande crimecache bij zijn nieuwe H hoort. Geen nieuwe uitsluiting van die bonusrijke steden en geen stil gebruik van oude crime op zulke exits.

Voor de preview kan B de reeds gebonden crimeformule op eigen rekenwaarden toepassen met actuele Government4c2b70/4c2b50, echte City499840/Building45d980 en ownerWonder4721c0.4aafe0 is thiscall `(Happy*,actualCity*,actualOwnerPlayer*)`, ret8,double ST0, en schrijft crime/detail13;4abce0 is thiscall `(Happy*,actualCity*,double H)`, ret0c, en schrijft echte H plus crime. Laatstgenoemde vraagt een reeds geldige actuele H: geen fictieve candidate-H in de echte stad zetten om een previewgetter te krijgen.

## Minimum open binding en geldigheidsgrens

Het projectiepad `advance=0` hergebruikt exact:

1. **Happy+a0/+a4**, stedencomponent:4ab674 leest cache; normale advance!=0-call4ab66b→4aa5c0 werkt hem bij uit de actuele eigenaar/steden/regering. Complete4aa5c0 is reeds aanwezig in [bestaand bewijs](BINAIR/happiness-wgf-government-and-difficulty.txt). Nog nodig: waarom die cache bij deze allocatie overeenkomt met actuele Player-citycount/government, of veilige normale refresh van uitsluitend deze component inclusief echte detail/eventsideeffects.
2. **Happy+30/+34**, component van4aa7d0:4ab6dd leest cache; advance!=0-call4ab6d4 werkt hem bij. Bestaande analyse benoemt dit als afstand/component, maar complete4aa7d0-input-/writebinding ontbreekt hier. Minimale nieuwe calleelezing is alleen **4aa7d0**: echte actuele City/Player/centruminputs, geen workertileafhankelijkheid, sideeffects en veilige query-actualisering vaststellen.
3. **Happy+a8/+ac**, duration-summary van4ab0f0: projectie1/advance0 leest de bestaande summary. Lijst- en flagcode is al compleet gebonden; nog nodig: current summary versus normale advance-epoch bij allocatie. De normale loop telt een entrybijdrage vóór zijn counterdecrement/evt.verwijdering (4ab1c7..4ab1ed), en bewaart de som pas4ab2f9/+2ff. Daardoor kan de geldige huidige summary nog een laatste-roundbijdrage bevatten waarvan de entry al verwijderd is: blind de nu aanwezige lijst opnieuw sommeren bewijst geen gelijkheid. Een advance-call opnieuw afboeken of een lege privécontainer als echte lijst behandelen is geen bewijs van current summary.

Dit zijn drie caches in **éénzelfde actuele-query/epochvraag**, geen verzoek om alle gelukscomponenten te reconstrueren. Andere normale componenten/bonussen blijven door de echte query meegerekend. Het plan mag niet om deze vraag heen gewone bonusrijke steden, wondereffecten of tijdelijke gelukseffecten stil uitsluiten.

Na deze binding geldt de kandidaatwaarde uitsluitend voor het waargenomen actuele city/owner/round-contextsnapshot en gewone vierpopflags; alle vierplekcombinaties gebruiken dezelfde H zolang count/contentment/luxury, centrum, garnizoen, WGF, gebouw/wonder/government en externe gelukscontext gelijk blijven. Een kandidaatcommit die territory/owner/eventcontext verandert voldoet niet automatisch aan die invariant; echte native legality en de eerdere beperkte-commitfallback blijven nodig. De relevante foodberekening494970 moet dezelfde geverifieerde crimecontext gebruiken of een normale actuele refresh krijgen. Geen garantie tegen latere oorlog, gebeurtenis, WGF- of gebouwverandering claimen.

## Afronding

A stopt met het exacte minimum open antwoord hierboven. Gevonden: tegenbewijs voor directe Population+40-gelijkstelling; bestaande projectieflags/restoreprotocol; precieze nulbard-finalisatie en normale crime-ABI. B kan die route met de drie-cachebinding als expliciete blocker uitwerken. Algemene voedselgate nog niet compleet geaccepteerd; geen implementatie/gameplayacceptatie. Pc aan.
