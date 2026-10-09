# H3 — productiepotentie met drie bergen en voedselplan

7 oktober 2026, 22:33 Europe/Amsterdam. Afzonderlijk fase B na geaccepteerde [H2-capaciteit](PRODUCTIECAPACITEIT-H2.md) en definitieve [H3-voedselanalyse](../ANALYSE/KANDIDAATVOEDSEL-H3.md). Alleen voorstel; geen build, test, toepassing of spelbediening. H1-C is technisch geaccepteerd maar nog niet geïnstalleerd; root beslist over dit nieuwe C-pakket na review en uitleg.

## Voorgestelde beslissing

Voeg één klein inhoudelijk kenmerk toe aan de bewezen H1-scoreadapter: **een minimale voorkeur van één kwaliteitsunit voor een ondersteund kandidaatplan met drie verschillende open bergwerkplekken, één andere open voedselwerkplek en een positieve huidige voedselmarge in een expliciet scenario**. Gebruik H1-I als constante baseline, zodat de bergcentrumprobe H1-M geen tweede factor wordt.

Het scenario heeft vier gewone werkers, de werkelijk gemeten rantsoenen, gelezen toekomstig centrumenvironment en het actuele voedsel van alle vier werkplekken. Nieuwe stadstype-/vlakke/percent-/wonderbonussen zijn in dit referentiescenario expliciet afwezig; de toekomstige echte stad kan andere waarden krijgen. Crime wordt **niet voorspeld**: publiceer de maximaal toelaatbare crime voor dit scenario. Dit is een voorkeur voor fysieke capaciteit en voedselruimte, geen label 'gegarandeerd duurzaam productiestad'. Er komt geen straf voor locaties die hier niet aan voldoen: zij kunnen science-, monopoly- of uitbreidingslocaties zijn.

Een locatie die alleen na nog niet aangelegde IRR2-improvements voedbaar wordt krijgt in dit pakket geen vroege bonus. Hetzelfde geldt voor UNKNOWN, minder dan drie beschikbare bergen en een scenario zonder positieve huidige voedselruimte. Toekomstig food en mijnontwikkeling worden afzonderlijk beschreven; zij worden niet bij huidig food opgeteld.

De uiteindelijke doelen blijven: naast bergen vestigen met de echte noodzaakuitzondering, drie bruikbare bergen en één voldoende voedselwerker bij grootte4, mijnen/ontwikkeling, kust en gezamenlijke bergbenutting, juiste vestigingsurgentie, science/monopoly en transport. De −1-probe en dit +1-kenmerk realiseren die hele strategie niet. Voor de volgende stap is geen volledige stadshappinessforecast vereist.

## Oorzaak en bestaande aansturing

De oorspronkelijke score groepeert huidige food en productie/goud, maar kent geen afzonderlijk plan van drie gelijktijdig beschikbare bergwerkers plus één voedselwerker. [H2](../ANALYSE/PRODUCTIEKANDIDAAT-H2.md) toont dat bezette laborerposities en stadscentra moeten worden uitgesloten; raw bergtelling overschat capaciteit. [H3](../ANALYSE/KANDIDAATVOEDSEL-H3.md) toont dat het centrum apart meetelt, bergen food kunnen leveren en de echte rantsoenfactor noodzakelijk is. De nieuwe stad heeft nog geen CityData-cache/crime; bestaande cityqueries met een verzonnen ID zijn onbruikbaar.

FLI/AIP is eerst onderzocht: packing/limieten/settle_value_coef beïnvloeden de bestaande kwaliteit maar voegen dit plan niet toe. Daarom aanvullende native logica op de drie al bewezen H1-scorecalls; geen nieuwe SLIC-route of hook afleiden uit de gegevensinterfaces. Bestaande kandidaatmaskers/legaliteit/quota en GoalSettle-prioriteitsketen blijven gelden.

## Kleinste integratie en representatie

Bouw een nieuwe H3-variant vanuit dezelfde vastgelegde oorspronkelijke DLL/H1-I-bronroute. Dezelfde drie calls op200784bb/20078517/2007aa35 bereiken één adapter in een nieuwe RX-sectie; hergebruik de geaccepteerde emitter/PE-/reloc-/loaderroute en bronmanifesten. H1-C-bestanden worden niet door de ontwerper aangepast. Eigen functies worden relatief aangeroepen; geen vierde hook, nieuwe import, saveveld of globale wereldscore.

```text
B = sign_extend(original_AX)
als B<=0: return B
plan = EvaluateCurrentPlan(AiMain, World, canonical_center)
als plan.current_status == SUPPORTED_SCENARIO en plan.Ffood > 0 en plan.S0 > plan.D:
    return min(32767, B+1)
anders:
    return B
```

EAX volledig sign-extenden en via de bestaande ret10h-ABI teruggeven. Nul/negatief B blijft exact behouden; geen nieuwe kandidatentoelating of -afwijzing. Positieve scores blijven1..32767. B32767 satureert, B32766 kan32767 worden. Bij gelijke B wint het beschreven fysieke/current-foodplan met positieve marge; een verschil van1 kan gelijk worden, een verschil van minstens2 wordt niet omgekeerd. Eén punt is de kleinste representabele proefkeuze, **geen bewezen economische waarde of optimaal gewicht**. Dezelfde formule komt via alle drie sites in heapordening en nieuw GoalSettle+48 terecht. Geen bonus alleen achteraan bij doelprioriteit.

Dit kenmerk beloont huidige fysieke voedselruimte onder scenario, niet lage voorspelde crime of een gegarandeerde toekomstige taak. De werkelijke GoalSettle-prioriteitsverandering is één×actieve settle_value_coef; ook concurrentie met andere doelen kan daardoor verschuiven. Geen voedselmarge in tientallen willekeurige scorepunten omzetten, verdubbeling/bitpakking of nieuwe harde productiestadclassificatie.

## Input-, ABI- en ownershipcontract

Gebruik dezelfde actuele AiMain/World/civ/laagchecks als H1/H2, met alleen landlaag0 en canonical MapPointData. Eigen resultaat/scratch is caller-owned op stack; geen langdurige raw pointers bewaren. H2 levert256bytes met unieke posities/terreinen, status UNKNOWN/LT3/GE3 en momentopname. World+ac gebruikt intern globale scratch; alle queries blijven serieel en niet-reentrant in dezelfde selectiecontext. H2 wordt ongewijzigd semantisch hergebruikt: count0 is niet hetzelfde als gateafwijzing, duplicates/padding/centrum tellen niet dubbel en bestaande arbeiders/centra blijven uitgesloten.

| Invoer | Aangetoonde route en ABI | Gebruik |
| --- | --- | --- |
| Open posities/terrain | H2: +28ret8, +acret14h/count/20×8bytes, +a8ret0ch | Drie verschillende bergindices8/20/22 en een vierde andere plek |
| Actueel tilefood | World+b8→534340; push output,positie,World; ret0ch; EAX1 | Lees int32output; +bc is productie en wordt hier niet als food gebruikt |
| Werkelijke rantsoenen | AiMain+2c Player-interface; +8 echte Player; +1318 WGF-object; double+8 en stand+48 | Geen AllocWGF-schatting of stand0; onbekend/nonfinite/niet-positief→UNKNOWN |
| Centrumenvironment | Gecontroleerde loaded-enginegrid/TerrainDB/goodrecordroute uit H3 | Alleen beschreven normale context; geen city-ID of fictieve cityhandle |
| Developmentdelta | Improvement=AiMain+50; +48(type,positie) | double in x87ST0, consumeer altijd; nooit absolute+38 als volledige tilefood gebruiken |

Verbeterings-ABI uit bestaande dumps: +10 neemt Improvement,type, ret8/EAX beschikbaarheid; +20 neemt Improvement,type,0,positie,&state, ret14h/EAX predicate (nul in de bestaande caller, niet een verzonnen cityID); +48 neemt Improvement,type,positie, ret0ch/doubleST0. Pushvolgorde is steeds omgekeerd. De bestaande +20state wordt als raw state genoteerd, zonder alle onbekende statewaarden te hernoemen. Eigen classifierfunctie gebruikt stdcall(AiMain*,World*,center*,Result*), ret10h/EAX eigen status; H1-getteradapter behoudt zijn bestaande ABI.

Geen exception over de ABI; EBX/ESI/EDI/EBP en ESP behouden. Iedere x87-return wordt direct met fstp naar eigen qwordslot geconsumeerd. Houd x87-depth/controlword gelijk aan entree; geen integer-conversie onder een stil gewijzigde roundingmode. De rekenregels hieronder gebruiken integerfood/rationale marges waar mogelijk; pendingdeltas blijven apart als gevalideerde doubles.

## Gecontroleerd centrum en tijdelijke food

De loaded veldroute is versiegebonden aan engineSHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`/timestamp37d6f702 en DLLSHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`. In C blijft rootcontrole van werkelijke executable/baselinehash noodzakelijk; de afwijkende civctp.map levert geen adressen.

**Eigen modulebasiskeuze:** leid de enginebasis uit de gecontroleerde echte World-vtable af: slot+b8-adres minus RVA134340h, en controleer dat slot+a8 dezelfde basis+RVA1342e0h geeft. Controleer PE32/MZ/PE/timestamp en de aangewezen oorspronkelijke wrapperinstructies (relocated operands apart) voordat loaded globale velden worden gelezen. Dit is een voorgestelde binding aan de reeds bewezen wrappers, geen algemene modulezoeker of ondersteuning voor andere binaries. De door root gecontroleerde proefengine heeft imagebase400000h, DYNAMIC_BASE=false en een lege relocatiedirectory. Ondersteun daarom expliciet uitsluitend de vastgestelde enginebasis400000h; de vtable-afleiding dient als contextcontrole, niet als nieuwe algemene ASLRroute. Alleen de H1-DLL heeft het bestaande rebasecontract. Mismatch→UNKNOWN. In de eigen nativehelper kan de bestaande fixtureaanpak de benodigde pointer-/datareads expliciet modelleren; zij bewijst geen echte enginecontext. De modelreader krijgt intern een eigen HostBinding met gevalideerde enginebasis/grid/DB/Playerpointers; productie laat alleen de beschreven fingerprint/contextvalidator die binding maken. Positieve fixturegevallen mogen dezelfde modelreader met uitsluitend eigen fixtureallocaties en expliciet FIXTURE-hostbinding aanroepen, terwijl de productievalidator afzonderlijk verkeerde host/basis/headers moet afwijzen. Fixturetoegang mag nooit in een geïnstalleerde productievariant als fallback actief zijn.

Gebruik enginebasis+RVA67DD70h voor World-gridpointer en +RVA67DD3Ch voor TerrainDB. Converteer canonical positie eenmaal met de bewezen bestaande503f00 (enginebasis+RVA103f00h, ECX=&lokale interne8bytepositie, één stackpositiepointer, ret4). Dit interne object wordt alleen voor veldreads gebruikt; World-methoden krijgen steeds externe MapPointData. Controleer interne x/y tegen de geladen kaartmaten op enginebasis+RVA67DF20h/+67DF22h en z0. Grid+1c[z][x][y] gebruikt4bytepointerstride. Null/bounds-/recordfout→UNKNOWN voor die positie.

TerrainDB: count+0, array+8, recordstridec0h, signed terrainbyte Cell+d. Selecteer het gewone record of hetzelfde good-subrecord als500110; lokale goodbits zijn `(Cell.flags>>6)&7`, niet GOOD_INDEX. Voor deze eerste ondersteunde route geen malformed lokale slotwaarden aannemen: alleen0..4 ondersteunen, dan de bestaande terugloop langs a0+4×slot naar een geldige subrecord volgen. Andere encoding→UNKNOWN. Speciale DEAD/DEAD_HILL/SPACE en ongedekte centrumcontext→UNKNOWN. Het centrum moet gewone landcontext zijn en Cell+14 moet0 zijn.

Voorkom tijdelijke unit-food als blijvende terreincapaciteit: ondersteun in deze eerste variant alleen posities zonder armylist of met count0 (Cell+10→count+30). Een aanwezige armylist wordt niet stilzwijgend aangenomen food0; die positie krijgt FOOD_UNKNOWN. Dat is conservatief en kan bruikbare kandidaten missen, maar hoeft geen verdere unitanalyse te blokkeren. Het centrum moet ondersteund zijn; voor werkplekken kan de zoeklus unsupported posities overslaan en een plan zoeken op vier ondersteunde plekken. Als geen geldig plan gevonden wordt terwijl geschikte posities UNKNOWN bleven, resultaat UNKNOWN, geen bewezen tekort.

Controleer de gewone omgevingssom volgens500110: basefood record+8, huidig road/IRR/minelevel uit flags, canal+54, river+58, overeenkomstige environmentfood+0. Wegen via+5c/+60/+64, IRR via+68/+6c/+70, mine via+74/+78/+7c; geen familyselectie verwisselen. Gebruik checked64tussenrekening; ontbrekend environment draagt0, ongeldige pointers/data niet. Negatieve som vóór oorspronkelijke clamp of int32overflow→FOOD_UNKNOWN. Vergelijk de ondersteunde no-citysom met World+b8-output; verschil is UNKNOWN, geen nieuwe correctiefactor.

Centrumtoekomstfood in deze ondersteunde context: `Fcenter=current_centerfood+selected_record.ENV_CITY_BONUS.food`. ENV_CITY_BONUS is pointer+50, food integer+0; ontbrekend environment geeft0. Controleer de som zonder negatieve preclamp/overflow. Zo is een gelezen centrumcorrectie mogelijk zonder universeel+10/+20. Raw huidige food op werkplekken telt huidige improvements/goods/minefood werkelijk mee; er wordt nergens mountainfood0 aangenomen.

## Het huidige plan, scenario en crimegrens

Zoek gezamenlijk vier verschillende open posities. Voor SCORE_CURRENT is een vierde plek uitsluitend een voedselplek als haar ondersteunde huidige Ffood>0. Een food0plek wordt overgeslagen, ook als rijke centrum-/bergfood anders S0>D zou opleveren. Voor iedere dergelijke vierde voedselplek F: neem drie andere bergposities met de hoogste **huidige** foodwaarden. Dit maximaliseert het brutofood van dit beperkte scenario voor die F; het claimt geen optimale productie/mijnplanning. Omdat alle bergen als capaciteit gelijk worden behandeld, volstaat een top3selectie zonder alle combinaties te enumereren. Kies daarna het plan met hoogste som; bij gelijke som lexicografisch x/y/z van F en gesorteerde bergtriple voor determinisme. Foodplek mag zelf een berg zijn, maar dan moeten drie andere bergen overblijven. Centrum staat niet in de workerentries.

```text
S0 = Fcenter + Fmountain1 + Fmountain2 + Fmountain3 + Ffood
R = werkelijke Player-rantsoenfactor
D = 40×R    # 4 expliciet veronderstelde gewone werkers met Hunger10
margin0 = S0-D
crime_sufficient_max = (S0-D)/S0, alleen als S0>0
```

Referentiescenario **ZERO_NEW_CITY_MODIFIERS**: geen nieuwe type/flat/percentfoodcache en geen foodwonderpercentage. Dit zijn benoemde modelvoorwaarden, geen beweerde constructorwaarden, actuele ondergrens of actuele crime0. S0 is brutofood vóór de onbekende crime-inhouding. De gewone bewezen stadssom telt het centrum eenmaal en vier workerbijdragen; consumptie telt vier Hungerwaarden, geen vijfde inwoner. Theocracyproductiefactor1.25 is geen foodbonus.

Voor OG-constregels is R=1+0.25×werkelijke stand. Verifieer de gelezen double tegen de gelezen stand en deze vastgelegde regels; gebruik ze niet als vervanging van de echte factor. Dan is D=40+10×stand een exact checked64integer. Bij nietpassende factor/stand/constidentiteit of R≤0: UNKNOWN. Deze strikte ondersteuning vermijdt een nieuw fixedpoint-/roundingbeleid voor willekeurige modregels. Vergelijk S0 en D als checked64integers; sla de crimegrens exact op als signed numerator(S0−D), positive denominatorS0. Een gerenderde decimal is toelichting, geen nieuwe drempel.

Bij S0>D is er positief fysiek voedselbuffer onder dit scenario. **Onder dezelfde genoemde scenariovoorwaarden** is crime≤(S0−D)/S0 voldoende voor onderhoud, want S−floor(S×crime)≥S×(1−crime). Een negatieve grens betekent scenario onvoldoende zelfs vóór crime; S0=D vereist crime0 voor deze voldoende toets en krijgt geen bonus; S0≤0 heeft geen geldige ratio. Geen actuele citycrime of10%-tolerantie invullen. Crime kan in werkelijkheid boven de vereiste grens liggen en de stad kan verhongeren; daarom heet de uitkomst SUPPORTED_SCENARIO, niet PRODUCTION_SUSTAINED.

Aanvullende hypothetische bonus-/wonder-/crimewaarden mogen later uitsluitend als expliciet gelabelde scenarioinputs worden bekeken; zij veranderen deze eerste scorevariant niet. Zonder een gerechtvaardigde crime_max of nieuwe-stadscaches bestaat geen universele onderhoudsgarantie. Er is geen alsnog noodzakelijke brede A-vraag voor dit beperkte huidige-foodkenmerk.

## Pendingfood en mijnontwikkeling apart

Eigen classifier heeft twee compile-time/call-modes: SCORE_CURRENT en EXPLAIN_DEVELOPMENT. Beide gebruiken dezelfde huidige-planfunctie. SCORE_CURRENT draait op de drie scorecalls en voert **geen toekomstige improvementqueries** uit. EXPLAIN_DEVELOPMENT levert later met dezelfde bestaande verificatieroute de ontwikkelgegevens van gekozen plannen; het is geen nieuwe observer/helper of hot-loadswitch en verandert de score niet. Daardoor is H3 een echte scorefeature met een beperkte verklaringsroute, geen alleen querycomponent.

Voor EXPLAIN_DEVELOPMENT:

- Reeds bestaande IRR1 blijft werkelijk huidig food. Nieuwe IRR1 telt normaal niet als ontwikkeloplossing. Zonder bewezen Labyrinth-taakinvoer is die uitzondering uitgeschakeld; een wensprofiel of nabijheid van bergen is geen wondertaakbewijs.
- Selector1=IRR2: voor de gebonden gewone landrecords1/4/5 en water10/11 geldt Agricultural Revolution respectievelijk Ocean Faring. Andere records alleen bij hun bewezen geladen environment/advancebinding; anders pending-onbekend. Vraag +10typeavailability en +20positionele predicate apart. False+10 bewijst niet alleen ontbrekende tech (obsoletecontext kan ook spelen); label AVAILABILITY_PENDING/UNKNOWN_REASON, niet fictief 'researchen lost alles op'. False+20 is geen klaar bouwplan.
- Een ondersteunde +48delta geeft alleen een scenario `Ffuture=Fcurrent+delta`; geen food1+food2 stapelen of+38 nogmaals optellen. Een ontbrekend targetenvironment geeft geen aanlegpotentieel. PENDING_TECH/PLACE_UNKNOWN, READY_NOT_BUILT en ALREADY_PRESENT blijven onderscheiden. Een uitgevoerde plaatsing is niet bewezen door een truequery.
- Kies ook voor een pendingfoodplan drie andere bergplekken en één verschillende foodplek. Een plek met huidigefood0 en positieve food pas na IRR2 mag uitsluitend in dit pendingplan voorkomen; zij krijgt geen huidige bonus. Publiceer S_pending en de eigen vereiste crimegrens, plus beschikbaarheid/plaatsing/advancevoorwaarden. **Geen S_pending als S0 gebruiken en geen earlybonus uit pendingmarge.** Een waardevolle toekomstige locatie kan later opnieuw worden beoordeeld; deze variant verklaart haar lage huidige urgentie maar sluit haar niet permanent uit.
- Voor de drie gekozen bergplekken: lees werkelijk huidig minelevel. Waar nieuw mine1(selector6) of een latere mineupgrade wordt beschreven, vraag diens echte +48fooddeltas op en voer type-/positiechecks uit; een mijn kan food wijzigen. Publiceer het gezamenlijke mine+foodscenario afzonderlijk. Pas de delta nooit op een reeds identieke aanwezige mine toe alsof het extra opbrengst is; ontbrekende tech/plaatsing blijft pending. De huidige +1bonus blijft op het **actuele workerfoodplan**, niet op een onbewezen drie-mijnenonderhoudsclaim.
- Materialskosten/tijd komen uit geladen doel-environment+20/+24 of de reeds bewezen getterroutes. Noteer volledige targetkosten en tijdveld als regelinformatie, zonder onbewezen gratis upgrade/PW-afboeking of voltooiingsbeurt te voorspellen. PW-voorraad, aanleg/workeractie en groei tot4 zijn latere planning; het scenario alleen reserveert geen materialen of arbeiders.

De keuze SCORE_CURRENT houdt dit eerste pakket klein. Developmentresultaten zijn voor doelconforme opvolging, niet voor toekomstige opbrengst als huidige waarde behandelen. Het einddoel drie verbeterde bergwerkers+food opgrootte4 vereist nog werkertoewijzing, mijnbouw, growthbeleid en echte stadsonderhoudsvalidatie.

## Eigen uitvoer en pure functie

Eigen `H3Result` is een caller-owned structuur, nog geen engine/saveformaat. Leg in C een vaste offsettabel vast: status/reason/modelID; actual R/stand/D; centerfood/citybonus/center-conditions; H2-status/open_count; gekozen4entryindices/posities; S0/margin0 en rationele crimegrens; unsupported-entrymask; developmentmode/resultaten apart. Geen ongeïnitialiseerde of gedeeltelijke TRUE-uitvoer. ModelID=ZERO_NEW_CITY_MODIFIERS en statuslabels zijn verplicht om een conditionele uitkomst niet als echte citynetfood te presenteren. Bij UNKNOWN score B, met gerichte reason. Bij beoordeeld tekort score B, met exact scenario; een andere stadsfunctie blijft open.

De uitkomst is ongecachet en zuiver ten opzichte van gameplay: geen cel-/wereldscore-/reservatie-/goal-/workerwijziging, geen nieuwe claims op bergen. Herhaalde call bij dezelfde civ/positie/wereld/rations levert dezelfde kwaliteit. H2-openplekken kunnen later bezet raken en meerdere kandidaatcentra kunnen dezelfde berg bieden. De eerste variant reserveert niets; consistente wereldtoestand tijdens heapopbouw en de latere doelaanmaak is een verificatievoorwaarde. Bij statewijziging/re-entrancy wordt de proef ongeldig en gaat uitsluitend die gebeurtenis terug naar analyse. Geen time-outafhankelijke scorefallback die binnen één heap verschillende resultaten geeft.

## Kosten en concrete stop-/meetgrens

Vergelijkers kunnen dezelfde positie vele malen lezen; daarom geen vrijblijvende claim dat20queries goedkoop zijn. Per volledige SCORE_CURRENT-call maximaal1gate+1openquery+20terrainqueries+21foodqueries = **43 extra directe World-calls vanuit onze code boven de ene oorspronkelijke +168getter**, plus boundedloadeddatareads/top3zoeklus≤400tilevergelijkingen. Een volledige adaptercall heeft daarmee maximaal44 eigen directe World-calls; interne nestedenginecalls vallen buiten deze teller (World+ac kan zelf World+28 aanroepen). Hun looptijd blijft wel onderdeel van de gemeten overhead; maximaal86 extra (88 totaal) per comparator met twee nieuwe beoordelingen; hoeveel comparators daadwerkelijk optreden is te meten. B≤0 en H2-LT3 stoppen vroeg. Geen persistent cache/eventmodel op voorhand; geen clocktimeout in de functionele code.

**Voorlopige technische acceptatiegrens, expliciete ontwerpkeuze:** in een later vrijgegeven gelijke T0-pass mag H3-scorewerk in totaal maximaal10% van de gemeten H1-I-AI-passtijd toevoegen; totale AI-passtijd mag daardoor niet meer dan1.10×de controle bedragen. Meet tellers/looptijd met de bestaande toegestane verificatieroute en vergelijk identieke meetpunten. Tevens nooit>43extra eigen directe World-calls (44totaal inclusief originele getter; interne nestedenginecalls niet meetellen in deze aantalgrens) per volledige scorecall of>20rawposities; overschrijding is een implementatiefout. Deze10% is een praktische eerste overheadgrens, geen spelregel of bewezen prestatiewaarde. Bij geen betrouwbare timing nog geen runtimeperformanceacceptatie claimen.

Bij overschrijding: stop de proef/acceptatie van deze variant en herzie gericht (bijvoorbeeld een expliciet begrensde per-passsnapshot, alleen nadat haar refreshpunt is bewezen). Geen stil nieuwe cache of minder consistente score inbouwen. Verkeer in EXPLAIN_DEVELOPMENT wordt apart geteld en hoort niet bij comparatorhotpath. Native fixturetiming bewijst geen echte World-querykosten; standalonelaad/rebase/ABI is wel uitvoerbaar terwijl de GUI wacht.

## Meetlat, alternatieven en herstel

Latere C-checks gebruiken de bestaande H1-nativefixture-/loaderroute, geen nieuwe emulatie/observer in fase B. Vergelijk minstens:

| Kandidaatpaar/edge | Gewenst verschil |
| --- | --- |
| Zelfde B,3openbergen+apartefood; positieve versus negatieve huidige scenariomarge | Alleen positief huidige ondersteunde plan krijgt+1 |
| 3kaartbergen waarvan1werker/citybezette versus3open | Alleen werkelijk beschikbare3kunnen een plan vormen |
| Rijke centrum-/bergfood geeft S0>D, maar alle mogelijke andere vierde plekken hebben huidigfood0 | Geen huidig plan met voedselrol en geen bonus; eventuele IRR2oplossing blijft pending |
| De hoogstefoodtile is één van precies3bergen | Niet tegelijk alsfood en één van3bergen gebruiken; anderefoodplek nodig |
| Zelfde center/food onder twee echte rationstanden | D/crimegrens en bonus veranderen alleen volgens werkelijk onderhoud |
| Een huidige farm/mine/good levert bergfood | Werkelijke food meetellen; geen0aanname |
| Zelfde scenario alleen door pendingIRR2 voldoende | Pendinggrens apart; huidige scorebonus0 |
| Centrumcitybonus/goodsubrecord/negativepreclamp/unitfood | Echte gelezen passende correctie of UNKNOWN; geen universeel centrum20 |
| Crimegrens laag/hoog bij onbekende daadwerkelijkecrime | Beide blijven conditioneel; geen sustainlabel of fictievecrime |
| B−32768/−1/0/1/32766/32767 | Nonpositive behouden, positievebonusclamp32767 |
| Gate/queryfout/laag/world/rationmismatch | ReasonUNKNOWN en oorspronkelijke B; geen gedeeltelijk succes |

Een gameplayverbetering is pas bewezen na geobserveerde keuze én werkelijke ontwikkeling/foodonderhoud; het scenario-/orderingbewijs alleen is voorbereiding. Hergebruik exact QUOTA-START-T0/hash `8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26`, Deity/Gigantic/8spelers, dezelfde acht B1-AIPs en passieve menselijke invoer. Vergelijk constante H1-I versus H3; niet tegelijk H1-M/packing/quotum/onderzoek wijzigen. Nieuw heapgebruik én nieuw GoalSettle met dezelfde S aantonen; oude goals zijn niet automatisch herberekend. D-gamePID19516 blijft ongemoeid; echte GUI-run wacht op rootvrijgegeven runtime.

Meet T25/T50/T100, stad25/30, locatie/beurt/bruikbare bergen/foodplek, huidige en pendingvoorwaarden, daadwerkelijke4inwonersinzet/mijnbouw/netfood, onderzoek/regering/verlies/lasten/wonders/goods. Geen verzonnen winstpercentage of gegarandeerde groei4. Minderwaardiger science/monopoly/uitbreiding verdringen is een mogelijk neveneffect van zelfs een kleine bonus; registreer dat. H3×H1-M, maskers/overlap, worker/improvementbeleid en gezamenlijke bergen krijgen eigen combinatieproeven.

Alternatieven: groteproductionbonus en alleen3bergen overschatten slechtefood; toekomstigefood direct optellen versnelt onvoedbare stichting; universeelcrime0/10% of standaardcentrum20 zijn onbewezen; volledige forecast als eis heropent onnodig brede analyse. De gekozen beperkte voorkeur geeft fysieke kwaliteit een aantoonbare toepassingsroute, met herkenbare scenariovoorwaarden en conservatieve fallback.

Bewaar bron-/emitterrecept, bekendeH1baseline en kandidaat-/payload-/engine-/config-/savehashes, alle exacte byteverschillen/ABI-/timingresultaten. Installeer niets zonder de afzonderlijke C-vrijgave. Herstel bij een latere proef uitsluitend de vastgelegde eigen DLLbaseline terwijl het gecontroleerde proefproces gesloten is, behoud andereB1bestanden, hashcontrole/herstart/zelfdeT0. Variante-save is geen herstelde baseline. Dit pakket schrijft geen opgeslagen rolmetadata.

Overdracht: genoeg voor uitvoerder om één H3-SCORE_CURRENT-kandidaat plus begrensde model/developmentfunctie te bouwen met de bekende emitter. Exacte encodings/structoffsets zijn C-implementatie, geen nieuw analistproject. Onvoorwaardelijke echte citycrime/bonuscaches blijven aantoonbaar ontbrekend; het concrete alternatief is het hierboven gelabelde huidige fysieke scenario. Geen onmisbare nieuwe A-vraag voor dit eerste scorepakket. Rootreview/uitleg gaat vóór toepassing; ontwerper stopt bij deze oplevering.


