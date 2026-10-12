# B5a — contextmatrix Happy90/a8, begrensd checkpoint

**Actueel 11 oktober 2026, 16:05 Europe/Amsterdam: gerichte A-overdracht afgerond.** De onderaan toegevoegde hervatting bindt echte90-writers, ownertransfer-a8-clear en normale Playerlocalorder; alleen samecity AIalloc-relativeorder blijft exact open voor B. Onderstaande budgetstop is historie. Geen complete voedselgate, runtime- of gameplayacceptatie.

Fase A; 10 oktober 2026, 19:20 Europe/Amsterdam. **Gestopt wegens budgetgrens; geen complete voedselgate.** Opdracht: exact de drie vragen uit [context-B](../ONTWERP/PRODUCTIEWORKER-CONTEXT-B5A.md). Geen gameplay-, binary- of liveactie. Alleen onderstaande eerste writer-windowset is nieuw onderzocht; eerder aanvaarde formule/cache/projectieanalyse blijft basis.

## Nieuwe machinecodewaarneming

Originele engine `CTP-og/ctp_program/ctp/civctp.exe`, bestaande binding SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, imagebase `00400000`, timestamp `37d6f702`. Eén beperkte Capstone-lezing van het bekende Happy-gebied `004a9c00..004ad000`, geselecteerd op geheugenstores met displacement90/a8/ac; geen volledigheidsclaim voor de executable of alle indirecte writes.

| Store | Exacte bytes / instructie | Bewijs en begrenzing |
|---|---|---|
| `4a9e5b` | `89be90000000` / `mov [esi+90],edi` | In het reeds bekende initialisatieblok; aansluitend `4a9e61` schrijft94 en `4a9e67` schrijft98. Nieuwe window toont de store, maar deze beurt bindt niet opnieuw de functie-entry/EDI-bron/directe caller aan City+5cc. Geen actuele afstandsrefresh bewezen. |
| `4a9e09` | `89bea8000000` / `mov [esi+a8],edi` | Reeds bekende initialisatie; bijbehorende highword-store `4a9e6d`, bytes `89beac000000`. Geen allocatie-epochbewijs. |
| `4ab2f9` / `4ab2ff` | `898ea8000000` / `8996ac000000` | Reeds bewezen echte native duration-summary-store in4ab0f0; geen nieuwe caller-volgorde bewezen. |
| `4ac25a` / `4ac264` | `c786a800000000000000` / `c786ac00000000000000` | Nieuw aangetroffen expliciete nulstores. **Kandidaat voor relevante extra a8-origin**, niet al gebonden aan dezelfde Happy-instance: entry, ESI-herkomst, branch en directe caller nog ongelezene gerichte vervolgvragen. Niet uitvoeren of als veilige reset voorstellen. |

De nieuwe90-window bevat uitsluitend genoemde initialisatie-store; dat betekent niet dat90 elders niet geschreven wordt. Bestaande4aa2f0-assignment kopieert90/a8 niet; guarded4aa7d0 leest90 zonder refresh. Geen nulwaarde als eindbeleid afgeleid.

## Dekkingsmatrix van de drie beslisvragen

| Vraag / relevante edge | Geaccepteerde basis of nieuwe voortgang | Nog nodig voor B |
|---|---|---|
| Werkelijke actuele Happy90 voor dezelfde City/owner/centrum/actor | Init-storeadres/bytes gevonden;4aa7d0-read reeds gebonden | Entry/bron/caller van init afmaken indien relevant; vooral echte normale90-refreshwriter met Happy=City+5cc en concrete inputwijzigings/caller-edge. Actuele geldigheid nog onbekend. |
| a8 tussen nativeadvance en allocatie | Native4926b4→4ab410(0,1)→4ab0f0-sumstores geaccepteerd; extra nulstorepaar nu gevonden | Eerst één lokale functie-/callerwindow rond4ac25a om echte objectbinding/resetvoorwaarde vast te stellen; vervolgens alleen noodzakelijke same-city edge naaralloc20020fa9. Geen totale writerlijst geclaimd. |
| Gezamenlijke alloc→foodorde | Bekende AI-grens na20020f56/vóór20020fa9 en relevante food494970 | Geen nieuwe orde-edge onderzocht. Nog onbekend of90-context/a8-summary voor dezelfde City op deze grens gelden en of normaleadvance/contextwijziging vóór relevante494970 tussenkomt. Gelijke bytes zijn geen bewijs. |

Exact resterende runtimeonderscheiding, **alleen wanneer beperkte statische edges daarna onvoldoende blijken**: volg dezelfde cityID/CityData/Happy/owner/centrum/actor met nativeflags, sequence/thread/callnesting langs echte90-refreshwriter (nog te identificeren),4ab0f0-entry/sumstore,20020fa9 en494970. Stel vast welke daadwerkelijke refresh/advance ertussen gebeurt. Nog geen trace-B-besluit, readerbouw, trace-C-toestemming of Start; de onbekende90-writer verhindert nu een volledig concreet pinprotocol.

## Stop en hervatpunt

Start19:19:34, verse week70/vijf6/stateok. Na één windowset: helper19:20:02, bron19:19:39/leeftijd23s, week70/vijf5/**state stop**. Onderzoek onmiddellijk beëindigd. Dit bestand is een onvolledige maar concrete overdracht, geen invariant-/voedselgateclaim.

Na toegestane budgethervatting: eerst lokale binding4ac25a/264; daarna uitsluitend echte90-refreshwriter en noodzakelijke caller-edge. Geen compleet Happy/PlayerRounds-onderzoek als voorwaarde. Root kiest vervolg; pc aan.

## Hervatting 11 oktober 2026, 16:05 — A afgerond, gerichte overdracht naar B

De eerdere stopmelding hierboven is historie. **Nieuwe statische uitkomst:** de echte90-writers en extra a8-clear zijn aan City+5cc gebonden; binnen Player4b7890 staat afstandsrefresh→echte a8-advance→food→late update vast. Crossmodule samecityorder van AI20020fa9 tegenover dit pad blijft precies open. Geen volledige foodgate, B5-C-vrijgave of runtime-/gameplaybewijs.

Bewijs: engineSHA256 b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79, base400000/timestamp37d6f702 opnieuw bevestigd. Begrensde Capstone32-bit bodies/windows; specifieke E8/E9-targets en mov-displacement90-bytes waren kandidaatselectie, daarna object/callercontext gelezen. Geen civctp.map, blinde full-engine-disassembly, binarywrites, nieuwe hulpmiddelen, tests of spelstarts. Formule/getters/snapshot/workerallocatie niet opnieuw onderzocht.

### Extra a8-origin: echte owneroverdracht

4ac1b0(this=Happy*), thiscall/noargs/ret:4ac1b8 `8bf1` bindt ESI=ECX;4ac1be `8b9eb8000000` leest durationcontainer. Bij positieve count verwijdert hij telkens de eerste stride18h-entry;4ac243 `894308` decrementeert count,4ac246 loopt terug. Pas count<=0 (4ac1d1 `7e78`→4ac24b) geeft detailclear4ac900 van10h..1dh en4ac25a `c786a800000000000000` /4ac264 `c786ac00000000000000`: Happy+a8/ac worden0.

Echte caller49b200(this=City*,int newOwner), thiscall/ret4:49b21c haalt newOwner,49b220 bindt City=ESI; **49b35e `895e04` schrijft City+4=newOwner**.49b4af `8b8ecc050000` haalt Happy=[City+5cc],49b4c1 `e8ea0c0100`→4ac1b0. Upstream4e1ef2 haalt UnitData+18 als ownerargument,4e1ef5 `8b4e58` haalt City=UnitData+58,4e1ef9 `e80293fbff`→49b200. Deze native owneroverdracht leegt lijst én summary en wijzigt andere stadsgegevens; geen veilige preview/reset. Een eerdere epoch is bij ownerwijziging ongeldig, ook bij gelijke pointer/bytes.

### Echte90-refresh: Worldafstandstraversal

5102d0(this=World*,int offset,int x,int y,int owner,int* remainingCities), thiscall/ret14h (5106c3 `c21400`), werkt via World+1c/laagarrays en cityUnit op Cell+14.

|Writer / bytes|Echte Happybinding|Bron en voorwaarden|
|---|---|---|
|51033e `898290000000`|510328 ECX=&Cell+14;51032a→4da8b0;51032f `8b4058`→City;510335 `8b90cc050000`→Happy;51033b leest Cell+28|Worldlaag0; signedint(Cell+8)+offset op510304/30f→Cell+28. Alleen nietnul cityUnit en4da960(cityUnit)==owner op51030d..31e.|
|510429 `898190000000`|5103fc→4da8b0;510401 `8b7058`→City;510420 `8b8ecc050000`→Happy|Worldlaag1; signedintresultaat van `_ftol`7256c6 op51041b uit Cell+8 × grootste absolute native wrapped-coördinaatdelta + double[A7DD48+128]. Nietnul cityUnit en ownermatch op510363..37a.|

Tweede route haalt hoofdstadpositie uit Players[owner]+12d4 via4da9a0 (51039a..3b0), vergelijkt met `(x,y,layer1)` via5035e0 (5103bd/c0), neemt grootste absolute delta5103c5..3e0;5103e3..418 bindt globalA7DD48+128/+12c, signedintCell+8 en x87/_ftol-volgorde. Geen recordnaam/Cell+8-semantiek uit verkeerde map afgeleid, geen eigen afstandsformule als native vervanging.

Directe510120(this=World*,int owner,InternalPoint* source), thiscall/ret8: init510211 `e8ba000000`→5102d0; frontierloop510271 `e85a000000`→5102d0. Init bindt source x/y, owner en actuele Players[owner]+12c0.count als remainingCities. Worldcell+28/frontier veranderen echt: geen sideeffectvrije query.

Directe normale caller Player4b7890:4b7906 `8b86d4120000` haalt capitalhandle;4b790e `7433` absent→4b7943;4b7919 `e822aaffff` validity4b2340;4b7920 `7421` invalid→4b7943;4b792c `e86f300200` haalt capitalpositie via4da9a0;4b7931 `8b0e` owner=Player+0;4b7938 `8b0d70dda700` World=A7DD70;4b793e `e8dd870500`→510120(owner,&capitalPosition).

Verandering van geldige capitalhandle/positie vóór deze call verandert de refreshbron. De traversal schrijft alleen voor gevonden native eigen cityUnits. Zonder geldige hoofdstad refresh overgeslagen, zonder90-clear/epochmarker. Of concrete owner-/centrum-/terrain-/actorwijziging de Playerroute onmiddellijk activeert is niet bewezen. Andere triggers/Worldoptimalisatie gaan op backlog; relevante normale caller/tracepins nu exact, geen extra brede A nodig.

### Init/load/copy: oorsprong, geen versheid

4a9da0(this=Happy*) bindt ESI=ECX op4a9dbb `8bf1`, EDI=0 op4a9dbe `33ff`;90-store4a9e5b en a8-stores4a9e09/4a9e6d zijn nulinitialisatie. Cityconstructiepaden492142→4a9da0 gevolgd door492151 `8986cc050000`→City+5cc;492d17→4a9da0 gevolgd door492d20 dezelfde store.

Archive4aa040(this=Happy*,Archive*), thiscall/ret4:4aa061 EDI=Happy,4aa06c EBX=&Happy+b8. Grenzen[Happy,Happy+b8) naar586a30 (write4aa081) of586a50 (read4aa178); helpers rekenen end−begin=b8 bytes, gebruiken Archivevtable+0c/+10 op586a41/586a61. Omvat90/a8/ac. City4924c0 bindt49254b `e8f07a0100` met ECX=[City+5cc] op492544 `8b8fcc050000`. Load kan beide archiefwaarden leveren; afzonderlijke durationlijst bewijst geen actuele summary. Snapshot4a9f20→4aa2f0 op4a9f41 `e8aa030000`: reeds geaccepteerde assignment kopieert90/a8 niet. Geen volledige lijst van iedere indirecte memcpy/eventwriter geclaimd.

### Gewone a8-advance en lokale foodorde

4926b4→4ab410(0,1) is op zichzelf geen gewone-turnbewijs: ook initpad4b67e0→4dc1c0→4e5420→492650 bestaat. LocalUnitHandle→UnitPool4b23a0→UnitData+58;4e5427 `e924d2faff` tailcallt492650.

|Local order binnenPlayer4b7890|Bytes/callers|Echte city/flags|
|---|---|---|
|90-refresh bij geldige hoofdstad|4b793e `e8dd870500`|World510120, hierboven gebonden|
|Eerste cityloop|4b7972 `6a01`;4b797a `e8c1550200`→4dcf40|Player+12c0.data+0c handles;4dcf4e UnitPool;4dcf5a UnitData+58;4dcf5e→498700 met tweede argument1|
|Echte durationadvance|4987f0 `50`;4987f8 `57`;4987fa `e8112c0100`→4ab410|ECX=[City+5cc], CityESI, projectionEDI=0, advance=498700 tweede argument. Eerste loop0/1: echte4ab0f0-sumstore mogelijk; crime-A-overrides blijven gelden.|
|Foodloop daarna|4b79df valideert4b2300;4b79f3 `e8f8470200`→4dc1f0|Actuele citylist naar tijdelijk array;4dc203 resolveert;4dc20a→4e1960;4e1963 UnitData+58;4e1966→497f10;4981f6 `e875c7ffff`→494970|
|Late cityloop na food|4b7d13 `6a00`;4b7d22 `e819520200`→4dcf40|4987fa nu projection0/advance0: geen durationadvance/sumstore; andere Hupdates echt|

Dit is echte lokale volgorde, geen garantie dat iedere stad alle pins bereikt: citylist kan veranderen, ongeldige handles/overrides/earlyreturns bestaan;497f10 kan vóór4981f6 retourneren. **AIalloc-relativeorder niet bewezen.**

Overige gelezen cityquerycallwindows49bfbe,49c2de,49c3eb,49c5be,49c83b,49c9ed,49cad4,49cc54,49cebe,49cffd geven projection1/advance0. Extra concrete0/1-caller553a2c bindt UnitData+58→City+5cc met553a20 `6a01`,553a29 `6a00`,553a2c `e8df79f5ff`. Externe aanleiding/ordepositie niet onderzocht; deze extra advancecontext niet uitsluiten met alleen Playerlocalorder. Geen algemene eventreconstructie nodig.

### Definitieve kleine matrix / A→B

|Vraag|Bewezen|Exact open|
|---|---|---|
|90-origin/refresh|Init, archive, twee City+5cc-writers, guardedPlayercaller en inputs|Laatste echte writer/load/init vóórAI20020fa9, actuele capital/owner/centrum/context en latere wijziging|
|a8-origin/advance|Init, archive, ownerclear, native sumstore, gewone eerste0/1 en late0/0-loop|Laatst uitgevoerde advance/reset/load bijAIalloc; verdwenen last-roundentry; extra553a2c-context|
|alloc→food|Playerlocalorder90refresh→0/1H→food→0/0H|Crossmodule samecityorder20020fa9 tegenover eerste loop/food: kan0/1/contextwijziging naalloc en vóórfood komen?|

Als alloc vóór de eerste0/1-update valt, voorspelt huidige a8 de volgende foodcontext niet. Na die update blijft dezelfde owner/centrum/capital/events/flags nodig. Geen huidige cache blind als toekomstige crime, geen fictieve reset/extra advance/workerpreview/bonusuitsluiting; native Playerrefresh niet als vrije query uitvoeren.

**Voldoende voor het afzonderlijke beperkte trace-B-besluit uit context-B.** Volg werkelijke sequence/thread/callnesting voor dezelfde cityID/UnitHandle/CityData/Happy/owner/centrum/actor op20020fa9,51033e/510429 (met bron/capital510120),4ab0f0-entry + echte4ab2f9/+2ff-store en494970. Werkelijke projection/advance en directreturncaller onderscheiden4926b4/init,4987fa/ordinary en553a2c/extra. Nativeinit/load/49b200-ownerclear maakt eerdere context ongeldig. Werkelijk verdwenen last-roundentry vóór verwijdering observeren, geen achteraf reconstructie/cachegelijkheid als versheid. Geen observer/harness/game/code gemaakt of trace-C-toestemming. Gevolgd pad bewijst alleen dat pad; ontbrekende context UNKNOWN/NOT_OBSERVABLE.

**Stop:** A-oplevercriterium bereikt: writers/callers/origins gebonden, gewone localorder bewezen, ontbrekendeAI-edge exact benoemd. B kiest vervolg; geen verdere algemeneHappy/World/PlayerRoundsanalyse. Complete foodgate, B5-C/gameplay blijven open. Pc aan.
