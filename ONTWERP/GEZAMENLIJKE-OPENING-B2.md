# B2 — gezamenlijke openingsvoorwaarde, regering en onderzoek

8 oktober 2026, 09:43 Europe/Amsterdam. **Herzien fase-B-voorstel; geen toegepaste wijziging of automatische B→C-vrijgave.** De brede analyse, [inputoverdracht](../ANALYSE/OPENINGSFASE-INGREEP-B2.md) en [geheugenoverdracht](../ANALYSE/OPENINGSFASE-GEHEUGEN-B2.md) zijn door root geaccepteerd. Ownership van deze ontwerprun: dit bestand en [eigen voortgang](../ANALYSE/VOORTGANG-ONTWERPER-B2.md). Root beheert PROJECTSTATUS.md.

**Status voor rootreview, 8 oktober 09:51:** de afgeleide gate is vervangen door eenmalige completion en het save/load/reload-contract. De foutpadvraag is beantwoord: Load geeft bij recordfout EAX=0 aan de bewezen fatale enginecaller; Save gebruikt expliciet dezelfde hostgebonden fatale handler. Geen graceful menuherstel geclaimd. N25/30 blijft open; root beoordeelt offline bouwen/controleren en latere kandidaatacceptatie. Geen C-vrijgave aangenomen.

## Beslissing die dit pakket verandert

Alle normale persoonlijkheden krijgen dezelfde **eenmalige opening**. Eén eigen voltooiingsbit begint op 0 en wordt uitsluitend 1 zodra het rijk tegelijk minstens N steden heeft en Theocracy werkelijk actief is. De opening blijft daarna voltooid, ook bij stadsverlies of een latere regering. Tijdens de onvoltooide fase bepalen gedeelde regels de regeringsvoorkeur en de onderzoekslijst. Persoonlijkheden blijven ingesteld; hun concurrerende regeringsconsequents werken pas wanneer de openingsvoorwaarde false is. Dit eindvoorstel vervangt de oude afgeleide gate uit de tussenstand volledig.

Dit realiseert de fasekoppeling en projectdoel 3 uit [PROJECTDOELEN](../PROJECTDOELEN.md), als noodzakelijke basis voor de gezamenlijke opening en doel 1. Het implementeert geen volledige uitbreiding, bouw-, leger-, groei-, PW- of stadrollenstrategie. [VERBETERPLAN B4](VERBETERPLAN.md) moet de uitvoerbare settlervraag, transport en buurcontext afzonderlijk regelen; de locatie-/rolpakketten blijven nodig voor [LOCATIESELECTIE](../LOCATIESELECTIE.md).

**N=25 of N=30 is nog een ontbrekende gebruikerskeuze.** De vraag is al gesteld; stilte is geen antwoord. Dit ontwerp laat N symbolisch. Root moet de keuze vastleggen vóór een daarvan afhankelijke productievariant of gameplayproef. Technische route- en grenscontroles kunnen met beide waarden als expliciete fixtures worden voorbereid, zonder één ervan tot strategie te verheffen.

Huidige oorzaken zijn aangetoond: masssettle kan onder haar kaart-/vredesvoorwaarden bij 1–5 steden activeren, maar niet opnieuw vanaf 6; set_govern vraagt Tyranny bij weinig steden en geeft vrijwel alleen Cleric Theocracy een rang; AIP-actions vervangen aanwezige categorieën in geregistreerde volgorde en herstellen een oude categorie niet wanneer een load wegvalt. [Fuzzybeleid](../ANALYSE/FUZZY-BELEID-EN-DEFUZZIFICATIE.md), [onderzoek/regering](../ANALYSE/ONDERZOEK-EN-REGERINGSKEUZE.md) en [AIP-laadwerking](../ANALYSE/AIP-LAADWERKING.md) bevatten het tekst- en machinecodebewijs. De overgedragen [ketens](../ANALYSE/BESLISKETENS-OVERZICHT.md) en [dekkingsmatrix](../ANALYSE/DEKKING.md) blijven de scopecontrole.

## B2a — eigen voltooiingsgeheugen, gate en compatibele variantload

FLI/AIP biedt de regel- en categorieaansturing, maar geen aangetoonde bestaande historische voltooiingsstatus. Een inputdeclaratie alleen levert geen native waarde. FliSymbol::Serialize 2003b740 is bovendien leeg: een eigen symbolenbit wordt momenteel niet geserialiseerd. Aanvullende native logica is dus nodig: registratie, beginbeurt, save, load en capture/restore rond de bestaande fuzzyreload. De [geheugenoverdracht](../ANALYSE/OPENINGSFASE-GEHEUGEN-B2.md) bindt de echte archive; geen SLIC-route of gegevensinterface als onbewezen modding-hook gebruiken.

### Registratie, faseovergang en ABI

Versiebinding: originele robotcom.dll SHA256 3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44, imagebase 20000000, timestamp 37b894e7. De engine heeft SHA256 b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79, imagebase 400000, timestamp 37d6f702. Robotcom.map past; civctp.map levert geen geldige engineadressen. Bind eventueel eerder vrijgegeven H3 via verklaarde diff en eigen kandidaathash; geen blinde herpatch of gecombineerde effectclaim.

| Ingrepen in robotcom | Originele bytes | Adapterwerking en vervolg |
| --- | --- | --- |
| Call RVA 413da, VA 200413da | E8 11 78 FF FF | Bestaande AddSymbol 20038bf0; beide nieuwe inputs; terug 200413df vóór parser |
| Call RVA 3625b, VA 2003625b | E8 90 2D 00 00 | Completion lezen/zo nodig zetten, gate schrijven; oorspronkelijke FireRules 20038ff0(section 2); terug 20036260 |
| Savecall RVA fe2d, VA 2000fe2d | E8 8E 29 FF FF | Oorspronkelijke AiMain::Save 200027c0, daarna eigen record; terug 2000fe32 |
| Loadcall RVA fe51, VA 2000fe51 | E8 FA 2D FF FF | Oorspronkelijke AiMain::Load 20002c50, daarna begrensde peek/restore; terug 2000fe56 |
| Reload-entry RVA 61f0, VA 200061f0 | 55 8B EC 53 56 | Entry-detour naar capture/restore-wrapper; trampoline met deze volledige prologue-instructies, vervolg 200061f5 |

De laatste entry-detour is een concrete ontwerpkeuze voor het bewezen begin van ReloadFuzzyLogic, geen reeds gebouwde hook. Zijn vijf bytes zijn vier volledige instructies. De trampoline voert ze precies éénmaal uit en springt naar de originele rest; de wrapper roept die met oorspronkelijke ECX/AiMain en één gekopieerd 4-byte argument aan. De originele reload keert terug met ret 4. Calls krijgen berekende rel32-targets; er zijn nog geen kandidaatbytes. Preimages: [input/lifecycle](../ANALYSE/BINAIR/opening-phase-b2-input-lifecycle.txt), [beginbeurt](../ANALYSE/BINAIR/opening-phase-b2-registration-and-rules.txt) en [save/load/reload](../ANALYSE/BINAIR/opening-memory-b2-ai-archive.txt).

Registreer vóór parsing **opening_completed** en **opening_required**, beide AddSymbol type 0/input met null doublepointer. Beginwaarden respectievelijk 0.0 en 1.0. AddSymbol 20038bf0 is thiscall: ECX=FliEngine; stack naam, doublepointer, defaultdouble, type; ret 14h. Voer eerst de bestaande registratie uit met haar oorspronkelijke argumenten/cleanup, daarna de twee extra calls. GetSymbol 200389e0 en RegisterInit 2003bf50(section 2) voor beide symbolen. Geen AddExternalSymbol/type 1 of herbestemde bestaande input.

Eigen doubleopslag staat op FliSymbol+8/+c bij null externe pointer. **+c2 bit 2 is gezet; +68 bit 2 blijft nul** voor beide inputs. Geen section-2-default/init die completion of gate terugzet. Er komen geen fuzzy consequents die completion schrijven. Zo is een exact 0/1-bit eigen per civ zonder extra AiMainveld of globale-only geschiedenis. [Type/opslag/masks](../ANALYSE/BINAIR/opening-phase-b2-input-contract.txt).

Vóór FireRules(2): ESI=actuele AiMain, engine=AiMain+c4. Zoek beide actuele symbolen; accepteer completion uitsluitend als exacte 0.0/1.0. Bij 0 lees signed32 eerste veld van object AiMain+8c en actieve regering via Player-interface AiMain+2c, slot +150 met die interface als expliciet stackargument. Slot +150→528f20 leest werkelijk actieve Player+94. Controleer dat de daadwerkelijk geladen Theocracy-index 3 is; tekstvolgorde van een ongebruikt bestand volstaat niet.

~~~text
if opening_completed == 0.0:
    if current_city_count >= N and active_government == 3:
        opening_completed = 1.0
opening_required = 1.0 - opening_completed
~~~

Dit is imperatieve adapterpseudocode, geen nieuwe FLI-syntaxis. Schrijf exact 0/1 met SetValue 2003b790 vóór de oorspronkelijke section-2-call. Completion=1 wordt nooit wegens actuele regering, cities, leeftijd of beurt teruggezet. De overgang wordt waargenomen op de eerstvolgende beginbeurt die beide eindvoorwaarden ziet; er wordt geen engine-event tussen frames verzonnen.

Behoud bij alle wrappers originele argumentvolgorde, cleanup en retourwaarden. Save consumeert één 4-byte archiveargument; Load twee 4-byte argumenten, GameState en archive, en levert oorspronkelijk EAX. Bewaar AiMain/archive op de eigen wrapperstack vóór doorroepen. SetValue consumeert acht bytes, Player-getter zijn expliciete interfaceargument. FireRules behoudt het reeds gepushte section 2, actuele engine-ECX en returnadres. Geen register-/flags-/x87-stack-/controlwordlek. Bewaar de oorspronkelijke staat na de call tijdens extra calls; herstel niet blind de invoerregisters van een oorspronkelijke call.

### Vast variantrecord: 36 bytes, formaatversie 1

Schrijf één record onmiddellijk na iedere oorspronkelijke AiMain-savepayload; niet achter het einde van de hele enginearchive. Na die payload volgen andere civs/managergegevens. Nieuwe saves bevatten ook vóór voltooiing expliciet 0. Het record bevat N om onbedoeld laden met een andere openingsstrategie af te wijzen. N blijft geparameteriseerd; dit ontwerp kiest geen 25- of 30-variant.

| Offset | Lengte | Exact formaat |
| --- | --- | --- |
| 0 | 16 | ASCII marker CTP1B2OPENSTATE!, hex 43 54 50 31 42 32 4F 50 45 4E 53 54 41 54 45 21 |
| 16 | 4 | Little-endian uint32 formaatversie=1 |
| 20 | 4 | Little-endian uint32 recordlengte=36 |
| 24 | 4 | Little-endian signed32 civ-ID, exact AiMain+20 |
| 28 | 4 | Little-endian uint32 completed=0 of 1 |
| 32 | 4 | Little-endian uint32 N=25 of 30, exact de geconfigureerde variantparameter |

Dit is een nieuw ontworpen formaat, geen al ondersteund saveveld. Geen structuurpadding of pointerbytes schrijven; bouw precies deze 36 bytes. Civ-ID komt uit bestaande init/loadbinding en is geen wereldturn. Geen opgeslagen AIP-naam, known-Theocracy of actuele regering als historische voltooiing afleiden.

### Enginearchive, save en begrensde load

Ondersteund contract is uitsluitend de bewezen singleplayer-enginebuild/archive. Concrete vtable is actuele enginebase+3462a8; slots +c Store→enginebase+186930, +10 Load→+1869f0, +14 IsStoring→+186c70. Constructor 586770 en echte save/load-callerdoorvoer zijn bewezen. QueryInterface retourneert E_NOINTERFACE; een positieve QI/GUID-binding wordt niet aangenomen.

Valideer vóór extra recordtoegang engine/build, vtable én slots. Archive+8 byte is mode (save=1/load=0); +c uint32 capacity; +10 uint32 geldig totaal; +14 bufferbegin; +18 cursor. Gebruik checked unsigned32-rekenwerk: buffer niet null, size≤capacity, geldig bufferinterval zonder pointeroverloop, cursor≥buffer, offset=cursor−buffer≤size, remaining=size−offset. Een andere archiveklasse krijgt geen layoutread of recordconsumptie. Geen veronderstelde eigen AI-bloblengte.

Savewrapper: valideer het ondersteunde archivecontract en completion; roep oorspronkelijke AiMain::Save precies éénmaal aan; schrijf daarna het eigen record via **echte Store-slot +c** met archive-this, bronbuffer en length36 als bestaande COM-stackargumenten. Store kan realloceren en verplaatst buffer/cursor; bewaar geen oude bufferpointer na Store. Completion wordt bij save niet opnieuw uit actuele steden/regering afgeleid. Gate is afleidbaar en wordt niet opgeslagen.

Loadwrapper: roep eerst oorspronkelijke AiMain::Load aan; bewaar oorspronkelijk EAX. Die bouwt FLI opnieuw via InitFuzzyOut20003c28 en leest haar laatste oude payload op20003c3c. Alleen na geslaagde originele load en bestaande nieuwe symbolen: valideer archive en peek direct binnen het bewezen remaininginterval. Gebruik **geen Load-call om te kijken**, geen cursorrewind en geen consumerende 0/1-read van volgende-civpresentie.

1. Bij remaining<16: vergelijk hoogstens de beschikbare bytes rechtstreeks. Zonder herkenbare niet-lege markerprefix is dit legacy en blijft cursor identiek. Een volledige prefix van de eigen marker die door archivetekort is afgekapt geldt conservatief als truncatiefout, niet als legacy.
2. Bij remaining≥16 en geen volledige marker: legacy; cursor identiek, completed=0, required=1. Geen byte van de volgende originele civ/managerdata consumeren. De marker begint met ASCII C en lijkt niet op de volgende-civpresentie 0/1; laatste-civgegevens moeten eveneens intact blijven.
3. Bij volledige marker: eis remaining≥36, versie1, lengte36, juiste civ-ID, completed0/1 en N gelijk aan variantparameter. Onbekende versie, verkeerde lengte/civ/N of afgekapt record is **variantformatfout**, geen legacyfallback. Een toevallige identieke 16-byte marker in oude data is een theoretische botsingsgrens; de originele T0 moet markerloos/cursoridentiek worden gevalideerd.
4. Consumeer uitsluitend het volledig gevalideerde record via echte Load-slot +10 naar eigen 36-byte stackopslag. Schrijf restored completed en required=1−completed naar de huidige symbolen. Cursor verschuift exact36 en staat daarna vóór de volgende oorspronkelijke managerdata. Bewaar oorspronkelijke EAX/ABI bij een geldige restore/legacy-load.

Bekende formatfout of ongeldig archivecontract mag niet met legacy0 of een verschoven cursor doorgaan. De [gerichte caller/handleranalyse](../ANALYSE/BINAIR/opening-fault-b2-caller-and-handler.txt) onderbouwt de volgende concrete keuze; de handler is niet uitgevoerd.

**Loadfout:** retourneer EAX=0 uit de eigen AiMain-loadcalladapter met oorspronkelijke argumentcleanup. RobotCom::Load voert na2000fe51 alleen pop ebp/ret 0xc uit en behoudt dat resultaat. Manager52dec8 test EAX; de zerotak52decc–52ded6 roept401560 aan vóór volgende-civstap52dede. Laat een ongeldig record ongeconsumeerd en schrijf geen completionfallback. Originele loadfailure volgt dezelfde nulroute; geldige legacy/variantload bewaart het oorspronkelijke EAX. Dit is nu een bewezen hostgebonden afbreekroute.

**Savefout:** Save is void; EAX=0 of alleen terugkeren weigert geen save. Kies een eigen save-error-thunk die na bevestiging van de ondersteunde enginebuild rechtstreeks **enginebase+1560 (401560)** aanroept. ABI: variadische cdecl met verplichte title/format-stackargumenten. Push eerst eigen constante formattekst "B2 save rejected: invalid opening state or archive contract.", daarna title "CTP I B2"; geen procenttekens of extra varargs. Beide null-terminated strings staan in eigen kandidaatgegevens. De thunk heeft geen normale succesretour; onverwachte handlerretour eindigt in eigen UD2-stopinstructie, nooit in Store/managervervolg. Een vooraf ongeldig archive/completion/symboolcontract faalt vóór de oorspronkelijke save; een fout daarna schrijft geen record en levert geen geaccepteerde save. Geen archivepeek of handlercall op een onbevestigde host.

**Werkelijk gevolg:**401560 formatteert in een lokaal buffer, roept4017a0 aan en doet op401598 opzettelijk een NULL-write. Dit is fatale afwikkeling die de spelrun kan beëindigen; **geen nette retour naar menu of behoud van onopgeslagen voortgang is bewezen**. Een onvolledig bestand uit zo'n fout is ongeldig en geen herstelstart. Herstel gebruikt nieuwe applicatieopbouw en originele T0 of eerder gevalideerde, correct gelabelde variant-save. Debuggercontinuatie/afwijkende hosterrorhandlers vallen buiten ondersteuning.

**C-poort vóór spelintegratie:** controleer de gebouwde wrappers/cleanup/hostbinding, nulresultaat→exacte managerzerotak vóór volgende-civread, en Save-thunk→exacte cdecl-handler zonder succesvervolg. Offline foutfixtures mogen de fatale handler door een expliciete recorder vervangen; noteer die stub en claim geen uitgevoerde enginecrash of graceful herstel. Deze fase B voert geen handler of gameprocesactie uit. Kandidaatacceptatie en rootvrijgave blijven nodig; andere engine-, scenario- en netwerkarchives zijn backlog. Geen verdere brede erroranalyse nodig.

### Reload, nieuwe game en oude T0

Reloadwrapper capturet completion als gevalideerde 0/1-waarde op **de eigen callstack vóór** de oude engine wordt vernietigd. Doorroep originele ReloadFuzzyLogic, die +c4 vernietigt/nul zet en via20006243 InitFuzzyOut opnieuw maakt. Zoek daarna beide nieuwe symbolen en herstel completion plus complementaire gate, zonder de vernietigde pointer te hergebruiken. Geen registratiedefault als historisch herstel behandelen. Bij ontbrekende symbolen of mislukte reload is dit een kandidaatfout, geen reset van een reeds voltooide opening. Entrydetour voorkomt afhankelijkheid van een onvolledig lijstje callers.

Nieuwe game: native registratie completed0/required1. Gewone load: nieuwe registratie, vervolgens recordrestore; markerloze originele **vroege T0** geeft altijd completed0/required1, ook nadat dezelfde applicatie eerder een variant met completed1 speelde. Fuzzyreload van dezelfde civ bewaart 0/1. Geen globale-only latch, oude pointer of historische waarde uit een vorige game overnemen. Gates zijn uitsluitend voor section2; init/section1-FireRules2004142c gebruikt ze niet.

| Toestand vóór relevante beginbeurt | completed erna / required |
| --- | --- |
| 0; N−1 steden, Theocracy actief | 0 / 1 |
| 0; N steden, Tyranny of Anarchy, of alleen aangevraagde Theocracy | 0 / 1 |
| 0; N steden én Theocracy werkelijk actief | 1 / 0 |
| 1; later andere regering en/of minder dan N steden | 1 / 0 |
| Variantload/reload met 1, latere regering | 1 / 0 |
| Opnieuw markerloze originele T0 laden | 0 / 1 |

Deze overgang blijft éénmaal voltooid. Tijdelijke onveiligheid vóór voltooiing pauzeert bestaande uitbreiding, geen latchreset; latere terugval is vervolgbeleid, geen openingheractivatie. Een willekeurige oude late-game-save zonder marker kan haar historische voltooiing niet bewijzen: haar legacy0-semantiek is expliciet en zij is geen correcte migratiebenchmark. Alleen de afgesproken vroege T0 is de ondersteunde vergelijkingsstart.

Bouwcontract: eigen PE-section voor adapters/naamdata, FileAlignment/SectionAlignment/SizeOfImage en code-/datatoegang controleren. Gebruik modulebase+RVA of volledige relocaties, inclusief enginevtable/slotbinding bij rebasing. Leg alle vijf ingreeppunten, trampolinelengte, extra section/header/relocatiebytes, recordversie/N en hashes vast. Ontwerpfase levert geen gebouwde bytes. Ontbrekende symbolen, maskers, governmentbinding of archivevalidatie laten de kandidaat falen; geen substitute state gebruiken.

## B2b — gedeelde regeringskeuze zonder concurrerende consequents

Voorgestelde inputs.fli-toevoeging gebruikt bestaande parserstijl en benoemt de native geregistreerde input:

~~~text
input opening_completed
input opening_required
    tri yes_opening_required(opening_required, 1.0, 0.5)
    tri no_opening_required(opening_required, 0.0, 0.5)
~~~

Bij uitsluitend 0/1 zijn de opening_required-memberships respectievelijk exact 0/1. Opening_completed heeft geen schrijvende fuzzyregel of benodigde membership; de native adapter beheert uitsluitend het eigen bit. Er is geen section-init/default of fuzzy fase-output nodig. De native registratie vindt vóór parsing plaats; bovenstaande tekst is geen vervanging daarvoor.

Nieuw set_govern_opening.fli bevat uitsluitend:

~~~text
if (yes_opening_required)
{
    gov_theocracy_1
    gov_tyranny_2
}
~~~

Beide sets bestaan in outputs.fli: Theocracy-output heeft range −2..12/default −1 en rang-1-set met center 1/radius 0.1; Tyranny dezelfde default en rang-2-set met center 2/radius 0.1. **Rang 2 is effectieve fallback, geen concurrerende rang 1.** De normale poll slaat onbekende/onbeschikbare kandidaten over, past bestaande filters toe en kiest strikt de kleinste positieve rang. Dus toegelaten Theocracy rang 1 wint van Tyranny rang 2; als Theocracy niet selecteerbaar is kan Tyranny dienen, voor zover die zelf de normale filters passeert. Ook Tyranny kan door haar stedenfilter uitvallen. Dan blijft de bestaande no-winnerroute gelden; geen geforceerde illegale overgang.

Geen availabilityinput, gok over techkennis of nieuw numeriek beleidsgewicht toevoegen. De constante 1/2 is de bestaande ordinale regeringsrang. Geen gelijkstand: twee rang-1-kandidaten zouden door de lagere Tyranny-index juist verkeerd uitpakken.

Maak daarnaast set_govern_after_opening.fli als exacte kopie van het bestaande set_govern.fli, met in **alle twaalf oorspronkelijke if-voorwaarden** de extra conjunctie "and no_opening_required". Behoud iedere oorspronkelijke voorwaarde en consequent, inclusief weinig-stedenregel, acht oorlog-/vredesregels, wormhole en beide focusregels. Bijvoorbeeld:

~~~text
if ((no_num_cities or a1to5_num_cities) and no_opening_required)
{
    gov_tyranny_1
}
~~~

Het gerichte tekstonderzoek vond alleen set_govern.fli als uitvoerende schrijver van deze gov-rangconsequents. Outputs.fli declareert sets; die declaraties zijn geen aanvullende beleidsregel. Section-2-outputdefaults −1 blijven intact. Tijdens opening schrijven de twaalf gewone regels niets; andere governmentoutputs krijgen geen positieve rang. Buiten opening worden de gedeelde openingconsequents overgeslagen en herstellen sectiondefaults de gewone uitgangswaarden voordat de oorspronkelijke voorwaarden hun rangen bepalen. Een vergeten positieve stale rang is een acceptatiefout. Het bestaande Fascism/Communism-bufferalias wordt hiermee niet gerepareerd; geen nieuwe late rangwijzigingen doen.

Laat PollNewGov, availability, Government+140 stedenfilter, Government+130 goudfilter en de enginewissel ongemoeid. Originele Theocracy-threshold is 40; 25/30 ligt daaronder. De engineaanvraag gaat via Anarchy en de aangetoonde deadline van normaal 1–4 rondes. Herhaalde aanvraag verlengt die deadline niet; de fase blijft tot echte voltooiing actief. Dit ontwerp belooft geen verdwenen Anarchy- of economische kosten.

## B2c — beperkte onderzoekscategorie en expliciet herstel

[B1](EERSTE-WIJZIGING.md) blijft de vaste onderzoeksbaseline: acht oorspronkelijke lijsten (default, cleric, milfew, milmany, scifew, scimany, slaver en citywall_science) beginnen met Religion, Theocracy en behouden daarna hun eigen oorspronkelijke restvolgorde. B2 verandert die acht bestanden niet opnieuw.

De openingsoverlay bezit **uitsluitend de gehele Advancements_List-categorie**. Maak opening_research.aip met exact het complete, ongewijzigde B1-default-lijstblok. Kopieer de echte declaratie, #DATA, alle records en #END_DATA; niet alleen twee advances opnemen:

~~~text
Advancement_Element Advancements_List[MAX_ELEMENTS];
#DATA
 "ADVANCE_RELIGION";
 "ADVANCE_THEOCRACY";
 ... alle overige B1-default-records, in dezelfde volgorde ...
#END_DATA
~~~

De puntjes zijn hier documentnotatie; zij mogen niet in het bestand komen. De eenduidige generatieregel is een exacte kopie van het bestaande B1-default-categorieblok, zonder zelfgekozen suffix. Geen scalars, Build_List_Classes, gebouwen, wonderlijsten of andere categorieën opnemen. Een echte gedeeltelijke AIP wordt door presenceflags uitgevoerd; het is geen volledig beleidsreset.

Voor herstel maak zeven eveneens uitsluitend research bevattende AIPs: opening_restore_default.aip, opening_restore_cleric.aip, opening_restore_milfew.aip, opening_restore_milmany.aip, opening_restore_scifew.aip, opening_restore_scimany.aip en opening_restore_slaver.aip. Ieder bevat een exacte categorieblokkopie van zijn benoemde B1-baseline. Maak deze bestanden vóór manageropbouw beschikbaar; load is hoofdlettergevoelig en leest niet alsnog een onbekende naam van disk.

De gewone route krijgt haar restore-action **vóór aiploader.fli**, en de gedeelde openingload **erna**. Voorbeeld Cleric:

~~~text
action load("opening_restore_cleric.aip") when (opening_required < 0.5)
#include "aiploader.fli"
#include "load_opening_research.fli"
~~~

Nieuw load_opening_research.fli:

~~~text
action load("opening_research.aip") when (opening_required > 0.5)
~~~

Dit gebruikt uitsluitend bestaande enkelvoudige numerieke actionvoorwaarden. Er is geen ongedocumenteerde samengestelde when-syntaxis of fuzzy tussenflag nodig.

De geregistreerde actionvolgorde geeft een controleerbaar contract:

| Fase | Volgorde voor research | Effectieve categorie na actionpass |
| --- | --- | --- |
| Opening true | Restore false; gewone loads; gedeelde research als laatste | B1-default-lijst, ook na eerste-beurtpersoonlijkheid en citywall_science |
| Opening false | Route-eigen restore; gewone loads; openingload false | Route-eigen B1-lijst, tenzij een latere bestaande researchwriter zoals citywall_science haar vervangt |
| Na voltooiing andere regering/stadsverlies | Gate blijft false; routeherstel en gewone loads | Geen opnieuw opgelegde openingslijst |
| Default false | Default-restore; geen gewone template-loader | B1-default-lijst |

Herstel is dus een expliciete schrijver, niet alleen het weglaten van de openingload. De pre-restore herstelt uitsluitend research en laat de bestaande laatste-writerprioriteit van citywall_science **buiten opening** intact. Restore werkt op iedere false-beurt; naast het opgeslagen completionbit is geen aparte categorietransitievlag nodig. Het normaliseert de researchbasis ook wanneer een gewoon profiel die beurt niet opnieuw geladen wordt. Daardoor wordt een oude opgeslagen openinglijst niet permanent de vervolgstrategie.

Binnen opening is het bewust gekozen researchsuffix van default gemeenschappelijk. Dit kan latere kandidaten anders ordenen dan Cleric/Slaver/science/militarylijsten en de citywall-science-suffix. Religion/Theocracy-prefix is al gelijk in B1; de extra gedeelde suffix is een aparte meetfactor, geen gegarandeerde winst. Lopend onderzoek wordt door een AIP-switch niet geannuleerd, en de bestaande selector/tijdtoets blijft functioneren. Op een klein eiland of bij onmiddellijke verdediging kan deze volgorde transport/defensie vertragen. Alleen een aangetoonde contextuitkomst rechtvaardigt een afzonderlijk ontworpen tijdelijke researchuitzondering; geen nieuwe onzeker beschikbare signalen verzinnen.

## Exacte normale routes en barbarenafscheiding

Doelbestanden voor eventuele uitvoering staan uitsluitend onder CTP-proef/ctp_data/default/aidata/ en de afzonderlijk gebouwde robotcom-kandidaat. CTP-og blijft referentie. Dit ontwerp heeft geen van die spelbestanden gewijzigd.

| Beginturnroute | B2b-include op de oude set_govern-plaats | B2c-restore vóór gewone loader |
| --- | --- | --- |
| beginturnCleric.fli | set_govern_opening.fli, daarna set_govern_after_opening.fli | opening_restore_cleric.aip |
| beginturnSlaver.fli | Dezelfde twee | opening_restore_slaver.aip |
| beginturnSciFew.fli | Dezelfde twee | opening_restore_scifew.aip |
| beginturnSciMany.fli | Dezelfde twee | opening_restore_scimany.aip |
| beginturnWarFew.fli | Dezelfde twee | opening_restore_milfew.aip |
| beginturnWarMany.fli | Dezelfde twee | opening_restore_milmany.aip |

Iedere zes-route-restore gebruikt "when (opening_required < 0.5)"; na de bestaande aiploader-include volgt load_opening_research.fli. Behoud alle overige includes, flags, regels en hun volgorde. Geen gewone personalityloader uitschakelen: hij levert categorieën die B2c niet bezit.

Default/beginturn.fli includeert al inputs.fli en outputs.fli. Voeg na die includes **alleen** set_govern_opening.fli, de action "load opening_restore_default.aip when opening_required < 0.5" en load_opening_research.fli toe. Laat de bestaande uitgecommentarieerde template-regels/hele aiploader uitgeschakeld. Default krijgt zo dezelfde openingsrangen en research, zonder dat dit pakket tevens een volledig nieuw Default-economie/legerbeleid invoert. Buiten opening worden geen nieuwe Default-persoonlijkheidsrangen bedacht; bestaande outputdefaults gelden.

BeginturnBarbarians.fli behoudt set_govern.fli en zijn barbarian.aip-load. Geen van de nieuwe regerings-/loadincludes komt daarin. Beide nieuwe native inputs mogen daar inert aanwezig zijn, maar er is geen barbarenconsequent/action die ze gebruikt. De generieke AiMain-save/load-adapters schrijven/lezen eveneens één eigen record voor de barbaren-AiMain; dat is formaatsymmetrie, geen toepassing van normaal beleid. **Bestandsrouting is hier de guard**, geen onbewezen "normal_civ"-input. De originele set_govern.fli blijft ongewijzigd. Controleer ook main/personality-include-expansies: een gedeelde nieuwe include mag niet indirect in barbaren section 2 belanden.

## Ruimte, dreiging en transport blijven werkende afhankelijkheden

B2 bezit geen unitklassen, bouwprioriteiten, settle-limits, packing, WGF/PW, verdedigerwaarden of marinecategorie. Bestaande no_settle/yes_settle, citywall/survival, war-modes, unit_focus, naval/supernaval en de overige gewone actions blijven hun bestaande velden schrijven. De nieuwe gate vervangt opening_game_strategy uit set_food_or_prod niet en is geen pauzesignaal. Een gebrek aan ruimte, transport of ernstig geluk kan het bestaande gedrag tijdelijk afremmen terwijl de strategische gate true blijft.

Dit behouden bewijst geen voldoende buurveiligheid of correcte transportoplossing. De reeds gemeten T60-reeks gaf 66 versus 49 AI-steden bij hoge vaste quota, maar 71/78 bestaande settlers versus 3; Welsh had 3 steden en geen transportschepen tegenover 7 steden en 3 Triremes in de baseline. Dat onderbouwt [B4 en de transportroute](VERBETERPLAN.md), **geen hoog vast settlerquotum als volledige opening**. Dit pakket introduceert geen quotum.

Build_List_Classes is een heel te vervangen blok inclusief unitlijsten. Een toekomstige primary-settlerwijziging kan niet als losse klassenaamoverlay worden toegevoegd. Gebouwen, wonders en advances zijn eveneens hele categorieën. Iedere toekomstige openingscategorie krijgt eerst een eigen expliciet bezit, concurrerende schrijvers en fase-false-herstel, plus ruimte-/dreiging-/transportproef. De beperkte researchownership van B2c mag niet als bewijs voor die andere onderdelen worden gepresenteerd.

## Verwacht effect, onzekerheid en alternatieven

Verwacht van B2a/b: de gezamenlijke regeringsvraag blijft actief voorbij de oude weinig-stedengrens en iedere normale persoonlijkheid kan toegelaten Theocracy kiezen met hogere rang dan Tyranny. Geleerde Theocracy, aanvraag en werkelijk actieve regering worden afzonderlijk gevolgd. B2a/c kan de gezamenlijke researchlijst op iedere echte openingsbeurt herstellen. Daarmee is de persoonlijke regering-/researchconcurrentie voor deze twee categorieën expliciet geregeld.

Materiële neveneffecten: Anarchy en regeringsgevolgen kunnen uitbreiding/geluk/economie tijdelijk verzwakken; gemeenschappelijk researchsuffix kan transport/defensie later maken. Voltooiing blijft bij latere terugval staan, zodat herstel van verloren steden/regering door vervolgbeleid moet gebeuren. Iedere civ krijgt bij false expliciet een researchbasis, ook als geen gewoon persoonlijkheidsprofiel herlaadt. Native adapters en het nieuwe saveformaat brengen versie-, ABI-, PE-, record-/archive- en reloadrisico mee. Variant-saves kunnen niet veilig met de originele DLL worden geladen. Deze risico's hebben gerichte acceptatiepunten hieronder; er is geen huidige gameplaymeting van B2.

Alternatieven: alleen num_cities als fase-einde mist werkelijk actieve Theocracy. Iedere beurt alleen steden/regering toetsen zou later Theocracy opnieuw afdwingen; een eigen completionbit voorkomt dit. Een bestaande input vervalsen verandert haar andere gebruikers. Een losse extra Theocracyconsequent laat oude rangen meedoen. Twee gelijke rang-1-outputs laten Tyranny door lagere index winnen. AIP-loads zonder expliciet herstel laten opgeslagen categorietoestand achter. Alleen FliSymbol-opslag zonder eigen record verliest geschiedenis bij load; globale-only state/agecutoff/known-Theocracy zijn geen historisch geheugen. AAIP integraal overnemen levert geen bewezen gezamenlijke opening volgens [AAIP-lessen](../ANALYSE/AAIP-LESSEN.md). Een B2a/b-only variant boven B1 is een afzonderlijke proef, geen volledige B2c/opening.

Er resteert geen noodzakelijke algemene analyse voor het bouwen van deze afgebakende offline kandidaat. De hostgebonden fatale save/load-afwikkeling is nu onderbouwd; correcte implementatie en controle van die exacte route blijven een C-poort vóór spelintegratie. Parseracceptatie, maskers, recordintegriteit en werkelijke activatie zijn eveneens uitvoeringscontroles. Bij een weerlegde verwachting alleen de concrete declaratie/call/mask/record/foutafwikkeling terug naar ctp_analist; geen volledige interpreter, scheduler of saveherconstructie als nieuwe drempel.

## Volgorde, gelijke start en meetbare acceptatie

1. **B2a afzonderlijk:** bouw een offline technische kandidaat met twee echte inputs en registratie/beginbeurt/save/load/reload-adapters, zonder gameplayconsequents/actions. Controleer beide N-grenzen als fixtures, completion0→1, per-civ opslag, record/legacy/ABI/reload en foutafwikkeling. Geen strategische N aannemen. De specifieke foutpoort moet vóór spelintegratie slagen; bouwen/offline controleren bewijst geen spelverbetering.
2. **B2b boven B1+B2a:** voeg uitsluitend regeringincludes/guards toe. Controleer parser, effectieve rangen en normale poll/overgang. Vervolgens dezelfde benchmark voor eerdere daadwerkelijke Theocracy en kosten van Anarchy. N-afhankelijke runtime pas na vastgelegde keuze.
3. **B2c boven dezelfde B1+B2a+B2b:** voeg research-only partials/actions toe. Meet categorieownership, fase-false-herstel en verschillen van het gemeenschappelijke suffix. Geen andere openingcategorie toevoegen.
4. **Combinatieproeven:** B1 research plus B2 government kan Anarchy/uitbreiding anders laten samenkomen; B2c kan defensie/transport beïnvloeden. H3-locatiebeoordeling plus B2 vereist een eigen gezamenlijke proef na afzonderlijke acceptatie. B4 vraag/transport en later regeringverlaten vereisen vervolgens hun eigen gecombineerde contextproeven. Geen parallelle onbekende gameplayfactoren in één causale run.

Gebruik steeds [dezelfde T0](../PROEVEN/settlerquota/vaste-start/STARTMANIFEST.md), SHA256 8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26, Deity/Gigantic/8 spelers. De controlegroep voor B2b is de geaccepteerde B1-baseline, niet willekeurig OG versus meerdere nieuwe factoren. Voor B2c blijft B2b constant. H3, rekentijdlimieten, spelregels, menselijke invoer en uitgeschakelde queueproef blijven in ieder paar identiek. Leg werkelijk toegepaste B1-status/hashes vast; ontwerpbestanden zijn geen bewijs dat B1 al actief is.

Start iedere run met nieuwe applicatie-/AIP-manageropbouw en dezelfde ongewijzigde T0, gelijk passief menselijk invoerlog en gelijke observatie-/savehandelingen. Een nieuwe manager leest bronnen, maar de save bevat effectieve AIP en lopend onderzoek. Toon vóór causale metingen de actuele input, de volgende beginbeurtactions en effectieve researchlijst/rangen aan. Geen voortgezette gewijzigde save als baselineherstel. Oude doelen, queues, score-/packingcaches worden door B2 niet magisch ververst.

Aanvullende overgangs- en contextsave mag alleen gepaard vanuit dezelfde gevalideerde voorgeschiedenis dienen. Als normale T0-doorgang niet vóór uitvoeringsgrenzen de relevante true→false/reloadtoestand oplevert, gebruik een expliciet gedocumenteerde technische fixture voor het contract en noem die geen gameplaybenchmark. Geen extra spelstart of savepatch als stilzwijgende vervanging.

| Acceptatiepunt | Meetbare uitkomst |
| --- | --- |
| Native registratie | Beide symbolen type 0/null externe pointer, eigen double; +c2 bit 2 gezet, +68 bit 2 nul, vóór parser geregistreerd |
| Faseovergang | Alle zes toestandgevallen exact; 0→1 uitsluitend bij steden≥N en actieve Theocracy; twee civs hebben verschillende completionbits zonder overschrijven |
| ABI/PE | Originele calls/returns en stackcleanup intact; geen register-/x87-/controlwordlek; uitsluitend benoemde callsites en nieuwe section/header/relocatiebytes verschillen |
| Reload/load | Nieuwe actuele symbolen gevonden, vastgelegde/herstelde 0 én 1; geen stale pointer, complementaire gate, geen section-1-gebruik |
| Legacy/T0 | Geen marker: oorspronkelijke cursor identiek en completion0/gate1; ook na een eerdere completed1-run; volgende civ/laatste managerdata onveranderd gelezen |
| Variantrecord | Save vóór/na voltooiing bewaart 0/1; exact 36 bytes per AiMain met civ/N/versie; load consumeert precies 36, meerdere civs en laatste civ correct |
| Foutpoort | Ongeldig record/archive: Load retourneert0→bewezen managerzerotak401560 vóór volgende civ; void Save roept hostgebonden cdecl401560 zonder succesvervolg. ABI/target/geen vervolg offline controleren met benoemde fatale-handlerstub; geen graceful herstel claimen |
| Routing/parser | Zes normale routes en Default accepteren nieuwe declaraties/includes; geen barbarenregeringsconsequent of onderzoeksload toegevoegd |
| Openingrangen | Theocracy na afronding naar integer rang 1, Tyranny rang 2; overige gewone kandidaten niet positief door concurrerende oude regels; geen ongeldige aliasbufferrest als winnaar |
| Poll/overgang | Beschikbare/toegelaten Theocracy wint; onbeschikbaar of harde-filterblokkade volgt gewone fallback/no-winner; Anarchydeadline niet ongewenst verlengd |
| Research true | Na volledige actionpass exact opening_research/B1-default, ook bij eerste-beurt- en citywall-science-writer |
| Research false | Expliciet routeherstel werkt; late bestaande citywall_science kan weer winnen; afwezigheid van gewone loads laat geen oude openinglijst staan |
| Niet bezeten categorieën | Extra partials bevatten geen classes/scalars/gebouwen/wonders; bestaande veiligheids-/transport-/gelukactions worden niet door B2c overschreven |
| Latere regeringsvrijheid | Completion1 blijft staan na gewone andere regering en stadsverlies; openingconsequents/actions activeren niet opnieuw, ook na save/load en reload |

Gameplaymeetlat per normale civ: T25/T50/T100, beurt Religion bekend, Theocracy bekend, eerste Theocracyaanvraag, elke Anarchybegin/eind, werkelijk actief worden, opening true/false, effectieve lijst en researchkeuze, beurt stad 25/30, bevolking, science, legerlast, verloren steden, queued/bestaande/onbestemde settlers en transport. Vergelijk eerdere werkelijk actieve Theocracy met B1-controle, plus uitbreiding en veiligheid; eerder aanvragen alleen is geen succes. Numerieke gameplaystreefwaarden worden na uitgangsmeting met de gebruiker bepaald, niet hier verzonnen.

Een technische acceptatie kan exact zijn. Een gameplayverbetering mag alleen worden geclaimd na vergelijkbare runs met bewezen activatie en expliciete nevenuitkomsten. Bij gelijk of slechter resultaat herzie de afzonderlijke factor; bij contextschade ontwerp gerichte uitzondering. Besteed extra aandacht aan klein eiland, gedeeld land, true→false, latere regeringskeuze en herladen. Geen herstelvariant die de opening weer true maakt na completion1. Achtergrondbediening/GUI is niet vrijgegeven binnen dit ontwerp.

## Herstel en overdracht

Vóór uitvoering maakt ctp_uitvoerder een manifest/back-up van de input-DLL, enginehash, alle acht B1-baselines en daadwerkelijk gewijzigde FLI-bestanden. Nieuwe AIPs/includes, alle vijf native ingrepen, recordversie/N en het bewezen foutpad horen in hetzelfde B2-versiemanifest. Herstel B2c afzonderlijk door eigen AIPs/includes/actions weg te nemen en de beginturnbestanden uit de directe B2b-back-up te herstellen. Herstel B2b naar B2a/B1-beginturns en verwijder eigen regeringsincludes. Volledig B2-herstel zet oorspronkelijke input-DLL en FLI terug, verwijdert eigen nieuwe bestanden en behoudt de gekozen B1-baseline. Geen bestanden van andere agents verwijderen.

Hashcontrole na herstel; applicatie/manager volledig opnieuw opbouwen en dezelfde ongewijzigde T0 herladen. Bewaar variant-saves afzonderlijk gelabeld met B2-buildhash/recordversie/N. **Geen variant-save met inline-record aan de originele DLL geven:** de gedeelde leesvolgorde zou verschuiven. Een B2-voortzettingssave is geen herstelde baseline; herstel gebruikt de originele T0 en gelijke invoer. Achterwaartse export/conversie van variant-saves is niet ontworpen en niet nodig voor deze proef. CTP-og blijft onaangeraakt; geen huidige gameprocessen bedienen/beëindigen vanuit deze ontwerprun.

Root presenteert vóór toepassing: eenmalige voltooiing bij N steden én echte Theocracy, opgeslagen eigen bit en nieuw variantrecord; latere regeringsvrijheid; rang1/Tyrannyfallback; research-only overlay met expliciet vervolg; behouden gewone veiligheidscategorieën; archive-/foutpoort en savecompatibiliteit; noodzakelijke B4/rollenvervolgstappen. Root beoordeelt B→C en de beperkte offline bouwopdracht, blijft eigenaar van de pending N-keuze en geeft spelintegratie pas na de specifieke foutpoort vrij. De ontwerper stopt na deze schriftelijke overdracht; geen actieve achtergrondrun, C-uitvoering of totale projectvoltooiing geclaimd.

De historische alleen-lezen auto-reviewafwijzing van 7 oktober blijft vastgelegd in de voortgang. Na verse bevestigde reset en actuele five/week-ok-stand is dezelfde gerichte read op 8 oktober geslaagd. Er resteert daardoor geen reviewblokkade op dit voorstel.

