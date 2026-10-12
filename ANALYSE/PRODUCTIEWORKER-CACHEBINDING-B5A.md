# B5a: actuele steden-, afstands- en tijdelijke gelukssom

Gerichte A, 10 oktober 2026, 19:02 Europe/Amsterdam. Alleen de drie cachevragen uit [crimeoverdracht](PRODUCTIEWORKER-CRIME-B5A.md). Geen game/live/patch/harness/tests; uitsluitend eigen analyse/progress. Bestaande foodrekening en native projectie/restore blijven geaccepteerd als analysebewijs.

**Uitkomst:** a0 kan uit actuele owner/government/citydata eventvrij opnieuw worden berekend. De volledige4aa7d0-route voor+30 is nu gebonden, inclusief echte invoer, scalar/detailwrites en actorresetguard; hij blijkt zelf nog signedint Happy+90 te hergebruiken. De voorgestelde projectie1/advance1 vernieuwt a0/+30 maar **niet a8** en kan eventcode oproepen. De complete gate blijft daarom afhankelijk van precies één afgebakende runtime-contextbinding voor Happy+90 en+a8, met de onderscheidende velden/callers hieronder. Geen volledige PlayerRounds-/Happyreconstructie voortgezet.

## Dekkingsmatrix

| Component | Concrete uitkomst | Nog nodig |
|---|---|---|
|a0/4aa5c0 | Exact actuele ownercitytelling, echte governmentvelden, eventvrije rekenroute | B implementeert de gebonden aritmetiek/guards; geen nativeeventcall als preview |
|+30/4aa7d0 | Complete functie/inputbranch/formule, writes+30/+88/details1, geen PopData/workerposities | Actuele native provenance van input Happy+90 voor dezelfde city/ownercontext |
|a8/4ab0f0 | Beide flags en sum-before-decrement/last-roundeffect volledig gebonden | Concrete native advance-epoch versus allocatie/foodobservatie; niet live uitgevoerd |
|projectie1/advance1 |0x4ab17e verhindert a8-som/write;4ab666/6ce vragen beide andere helpers op | Geen complete refreshroute; timer/angerrestore alleen sluit dit gat niet |

**Bewijs:** bestaande volledige4aa5c0-/4ab0f0-/4ab410dumps, nieuwe gerichte complete4aa7d0-disassemblage plus alleen noodzakelijke49a2b0,4c2cb0,4c29f0/4c2a10-inputgetters. Native engine SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, base400000/timestamp37d6f702 opnieuw bevestigd. Geen civctp.map. Geen runtimeactualiteit of nieuwe gameplayclaim.

## 1. a0: actuele telling, niet blind de native eventhelper aanroepen

`4aa5c0(this=Happy*,ownerPlayer*)`, thiscall/ret4,double ST0, leest owner Player+94→GovernmentDB A7DD34/455750. Echte waarden: GovernmentRecord+140 signedint threshold; +148 double coefficient. Hij telt niet simpelweg Player+12c0.count: alle huidige cityhandles uit `[Player+12c0]+0c` worden via UnitPoolA7DD74/4b2300 op geldigheid gecontroleerd;4dc570(this=&cityUnitHandle,int* outPopulation),ret4, moet population>=1 opleveren. Daarna N=max(1,aantal). [Complete functie](BINAIR/happiness-wgf-government-and-difficulty.txt).

```text
threshold = int32(actualGovRecord+140)
coefficient = double(actualGovRecord+148)
N = max(1,count(valid ownercityhandles with actual population>=1))
cityCountHappiness = 0                    als N<=threshold
cityCountHappiness = -(N-threshold)*coefficient anders
```

De aritmetiek staat4aa698..4aa6dd; double/x87-spills behouden. Nativevelden worden niet door tekstwaarden of een neutral owner vervangen. Actualowner is City+4=AiMain+20, echte Player uitA7DD80; dezelfde CityAgent-cityIDbinding blijft vereist. Geldige Player/DB/arrays/records en eindige coefficient zijn voorwaarden, geen nieuw beleid.

**Sideeffectgrens:** bij overschrijding volgt native4aa6e0→53ca30 en55bcf0; een branch maakt een berichtobject en roept53cd60 op4aa72d aan. Daarna4aa745 schrijft detail15 en4aa74d/+753 Happy+a0/+a4. Deze nativehelper is daarom geen gegarandeerd eventvrije query. Dat eventpad overslaan door een fictieve actor/flags te gebruiken is niet toegestaan.

**Overdraagbare route:** alleen de hierboven exact gebonden actuele telling/getterwaarden/aritmetiek gebruiken; geen4aa5c0-eventbranch uitvoeren. Het resultaat kan als eigen previewcomponent worden gebruikt of als correcte tijdelijke componentrefresh van echte Happy+a0/+a4 vóór het gebonden normale projectie1/0-pad, met expliciete backup/restore: native4aa2f0 kopieert a0 niet. Dit schrijft geen fictieve finale H, maar een werkelijk berekende component. De gewone bonusrijke stad blijft ondersteund. Dit is technische A-route, geen toegepast B-codeontwerp.

## 2. +30: complete4aa7d0, invoer+90 is geen verse afstandsberekening

`4aa7d0(this=Happy*,actualCityData*,actualOwnerPlayer*)`, thiscall/ret8,double ST0. Native schrijft uitsluitend Happy+30/+34,Happy+88/+8c en detail1 in het gevolgde eigen lichaam. Geen populationlijst/type/tileworkerposities gelezen; geen plaatsingsactie. De cityunitcentrumpositie wordt opgehaald4aa815..4aa81b maar er staat in deze functie **geen berekening van nieuwe afstand** uit die positie. Happy+90 wordt alleen gelezen op4aa83e.

Actuele invoer/branches:

-49a2b0(this=City*) vraagt het echte BuildingDB45cf80-predicaat op met City+48/+4c. De flagnaam wordt hier niet uit een niet-passende map afgeleid; exact native predicaat behouden.
-4c2cb0(this=Player*,outInternalPoint*) gebruikt handle op `[Player+12d4]`; absent handle0 retourneertfalse, geldige handle retourneerttrue en de echte unitpositie via4da9a0.
-Player+1194 is een echte native uitsluitingsflag. Predicaattrue of flag1194!=0 geeft volgens4aa939..4aa966 component0 en distancecomponent0. Dit is de bestaande contextbranch, geen door ons opgelegde nulbonus-/ownerreset.
-Anders: Player+12e8→Difficulty+98 double, Happy+90 signedint, Player+94→GovernmentRecord+88/+90/+98 doubles, actuele ownerwondermask+1170/+1174→Wonder4723a0.

Formule van de normale branch, met exact de native clamps en echte inputs:

```text
als nativeBuildingPredicate==true of Player1194!=0:
    effectiveDistance = 0; distanceHappiness = 0
anders:
    als own unitHandle ontbreekt en native positionqueryfalse:
        distance = GovRecord+98
    anders:
        distance = min(double(Happy90)+Difficulty98, GovRecord+98)
    effectiveDistance = max(0,distance - GovRecord+90)
    distanceHappiness = -effectiveDistance * GovRecord+88
    als nativeWonder4723a0Percent>0:
        distanceHappiness -= distanceHappiness*(percent/100)
```

Native+88/+30stores zijn4aa8c2/+8ca/+8dd; wonderstap4aa8f4..4aa915; details/return4aa928..4aa936. De bestaande regeringtekst noemt EMPIRE_DISTANCE_SCALE/MIN/MAX_EMPIRE_DISTANCE; de machinecodeformule gebruikt bovenvermelde echte recordvelden en getters, geen tekstgetal als geladen waarde.

**Belangrijke actor-sideeffect:**4c2cb0 kan bij een **ongeldige nietnulhandle** onder de normale context op4c2cea..4c2cf0 `[Player+12d4]=0` schrijven. Root verbiedt een actorreset als preview. Vóór een native4aa7d0-refresh moeten handle0 of een werkelijk geldige handle via UnitPool4b2300 vaststaan. Ongeldige nietnulhandle geeft ordinary fallback/afgebakende ongeldige-contextmelding, geen reparatie/reset door onze preview. De geldige native branches veranderen de actor niet; ordinarygebouw-/wonderbonussen behouden.

**Recompute-route:** na actuele a0-rekening kan native4aa7d0 onder bovenstaande actor/DBguard veilig zijn eigen+30/+88 en details vernieuwen; native scalarrestore4aa2f0 dekt+30/+88. Actualowner/stad/centrum blijven echt. Dit sluit stale+30 ten opzichte van huidige gov/diff/wonder/predicate, maar claimt **niet** dat het onderliggende Happy+90 op die allocatie vers is. De volledige helper bindt dat cache-inputgat nu concreet; geen nieuwe onbegrensde afstands-/Worldanalyse gedaan. Als90 dezelfde geldige citycontext heeft, beïnvloedt een keuze van vier legale gewone werkervakjes deze helper niet.

## 3. a8: flags en native advance-epoch

`4ab0f0(this=actualHappy*,actualCity*,actualOwnerPlayer*,int projection,int advance)`, thiscall/ret10,double ST0. De oorspronkelijke hoofdroute4ab4bb geeft zijn flags ongewijzigd door. Op4ab175 springt advance0 naar4ab307. Op4ab17e springt projection!=0 eveneens naar4ab307. Op die bestemming wordt bestaande Happy+a8/+ac teruggegeven; er is dan geen nieuwe som.

Alleen `projection==0 && advance!=0` loopt de event/durationlijst: Happy+b8→containercount+8/data+0c, entriesstride18h. Entry+8/+0c vormt de doublebijdrage; entry+0 is de counter; entry+10 detailcategorie.4ab1c7..4ab1cd telt de bijdrage **vóór**4ab1ed de counter decrementeert; verlopen entries worden daarna verwijderd.4ab2f9/+2ff schrijft pas de resulterende som naar+a8/+ac. Een entry die deze native advance verdwijnt kan dus wel de rechtmatige laatste-roundbijdrage in de opgeslagen som hebben. [Complete flag/list/sumcode](BINAIR/happiness-wgf-engine-base.txt).

Daarom:

-Een bestaande lijst opnieuw optellen levert niet bewezen dezelfde actuele summary.
-Projection1/advance1 slaat de volledige lijstsom/write over; hij maakt a8 niet actueel.
-Projection0/advance1 vernieuwt a8 maar boekt entries af; dat is geen previewrefresh.
-Een gekopieerde Happy met lege private durationlijst is geen echte actuele summary.

Concrete normale caller4926b4→4ab410 gebruikt `(City,0,&local20,1)` en kan de summaryadvances uitvoeren. Concrete projectiecaller49c9ed gebruikt `(City,1,&local18,0)` en behoudt summary/duurentries. De aanwezigheid van die callers bewijst niet de benodigde actualiteitsvolgorde ten opzichte van FSAllocatePopulation2002a820 en zijn huidige stad. Geen onbekende beurtvolgorde als vaststaand gepresenteerd.

## Afwijzing van projectie1/advance1 als complete predictor

Voor a0/+30 kiest4ab666 en4ab6ce de recompute-callees wanneer advance!=0. Native a0helper kan echter bovengenoemd eventpad uitvoeren; +30 gebruikt nog90. Happy+94-decrement wordt eveneens aangezet op4ab4cc..4ab4e1; anger+28-decay is reeds onvoorwaardelijk. Snapshotrestore dekt94/28/+30/+88 enCity38, maar nieta0/a8. Zelfs met aanvullende backups is **4ab17e→4ab307** het beslissende tegenbewijs: a8 is niet herberekend. De flagcombinatie voorspelt daarmee niet bewezen de eerstvolgende gewone foodupdate.

De minimale mogelijke route blijft: actuele eventvrije a0-rekening, guarded native+30-refresh met gevalideerde90-context, oorspronkelijke projectie1/0 + nulbardfinalisatie en scalar/City38restore, crime uit dezelfde actuele kandidaat-H. Daarvoor is nog de hieronder exact omschreven contextproef nodig; geen fictieve Hwrite, nieuwe groei-/durationpolicy of bonusuitsluiting.

## Exact ontbrekend runtimebewijs; geen oprekmissie

Statische bestaande dumps hebben geen gevalideerde epochmarker bij CityAgent/AiMain→Happy+a8 of bij Happy+90 op het allocatiepinpunt. Geen complete gate vrijgeven op deze cacheaanname. De kleinste volgende **C-waarneming**, pas na B/autoriseerde runtime, is één begrensde trace voor dezelfde echte gewone vierpopstad, zonder workerpreview:

| Meetpin | Exact opnemen | Te onderscheiden vraag |
|---|---|---|
|4ab0f0-entry/return |ECX Happy, City/owner args, projection/advance, returncaller, voor/na+a8/+ac en+b8-lijstcount; indien native advance loopt de daadwerkelijk verdwenen laatste entry en haar bijdrage | Welke bestaande native0/1-advance maakte de authoritative huidige summary; wordt die summary daarna op allocatie behouden? |
|B5a na20020f56/vóór20020fa9 |cityID/CityData/Happy/owner-identiteit,Happy+a8/+ac,Happy+90,Player+94/1194/12d4,citycentrum | Is dit exact dezelfde citycontext/summary, geen oudere/andere eigenaar? |
|Gerichte native write van `[Happy+90]` |schrijvend calleradres en echte city/owner/centrum/actorcontext; nativewaarde vóór/na | Welk bestaand mechanisme maakt90 actueel en is die context onveranderd bij allocatie? Geen scan van alle Worldcallbacks. |
|494970-entry op relevante foodupdate |dezelfde echte CityData/Happy/owner,a8/90/crime+b0 en volgnummer t.o.v.allocatie/normaladvance | Wordt de gevalideerde H/crimecontext daadwerkelijk voor deze foodberekening gebruikt, of eerst opnieuw door een normale update veranderd? |

Dit is een specifiek observeerbare onderscheidingsproef, geen uitgevoerd logger-/debugger-/harnessontwerp. Alleen trace-order en werkelijk native writes/entries tellen als bewijs; geen herberekende verdwenen entry of aangenomen actuele cache. Bij gewijzigde externe context geeft de observatie geen voorspelling over die latere verandering. Normale cache/detailupdates en gewone bonus/overridebranches blijven zichtbaar; worker-/territorypreview blijft uitgesloten.

De exacte nieuwe vraag is daarmee eindig: **authoritative90/a8-inputcontext op de bestaande allocatie- en foodpins**, niet alle PlayerRounds. Root kan B/C-vervolg kiezen of deze specifieke binding terugvragen. A stopt hier; geen volledige gate-/implementatie-/gameplayacceptatie. Pc aan.
