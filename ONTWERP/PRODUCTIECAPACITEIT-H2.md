# H2 — drie momenteel open bergwerkplekken

7 oktober2026,22:10 Europe/Amsterdam. Afzonderlijk fase-B-pakket na rootacceptatie van [PRODUCTIEKANDIDAAT-H2](../ANALYSE/PRODUCTIEKANDIDAAT-H2.md). Alleen ontwerp; geen build, test, gameplaywijziging of toepassing. [H1](SCORE-INVOEGROUTE-H1.md) blijft zelfstandig en wordt niet herschreven. Root beslist over C-vrijgave.

## Beslissing en doel

Ontwerp één herbruikbare capaciteitquery zonder cityID: bepaal of een kandidaat op landlaag0 **minstens drie verschillende, momenteel open bergwerkplekken** heeft volgens de bestaande World-interface. De oorzaak is aangetoond: de oorspronkelijke algemene locatiescore kent geen expliciete driebergencapaciteit; kaartbergen kunnen al door andere arbeiders of stadscentra bezet zijn. World+ac heeft de benodigde huidige filters en World+a8 geeft de canonical bergindices8/20/22. Het predicate levert controleerbare informatie aan de volgende productionclassifier; het schrijft geen scorebonus, stadstaak of reservering.

De projectdefinitie blijft drie bruikbare bergen **plus voedselonderhoud voor vier inwoners**, mijnontwikkeling, timing en gezamenlijke benutting. Een waar H2-resultaat is daarom geen productiestad. Geen extra gewicht of hogere vestigingsprioriteit op alleen H2; daarmee zou een slecht voedbare locatie ten onrechte kunnen winnen. Science/monopoly, naast-bergenvoorkeur, noodzaakuitzondering, kust, wondertaak en overlap blijven onderdeel van [VERBETERPLAN](VERBETERPLAN.md)/LOCATIESELECTIE.

FLI/AIP blijft verantwoordelijk voor bestaande prioriteiten, packing en goallimieten. H2 bouwt de ontbrekende inhoudelijke test uit native interfacequeries; tekstgewichten kunnen die niet vervangen. De bewezen H1-callroute levert later een invoegpunt, niet het enkele bestaan van deze interfaces.

## Eigen query-/uitkomstcontract

De volgende functie en resultstruct zijn **ontwerpkeuzes voor eigen payloadcode**, geen bestaande engine-interface:

`H2_Capacity(AiMain*, World*, MapPointData const* canonical_center, H2Result*)`

Eigen ABI: x86 stdcall, vier pointerargumentslots, `ret10h`, EAX=statusenum. Bewaar EBX/ESI/EDI/EBP en stackbalans; ECX/EDX/EFLAGS vluchtig. Geen x87-rekenwerk. De caller moet geldige native pointers en een eigen writable resultaatbuffer leveren; null-AiMain/World wordt inhoudelijk UNKNOWN, een ongeldige outpointer is geen herstelbare query. AiMain+30 moet dezelfde World zijn. Civ komt uitsluitend uit AiMain+20, geen CityAgent/CityData of geconstrueerde cityhandle.

| status | Betekenis | Bruikbaar voor classifier |
| --- | --- | --- |
| 0 UNKNOWN | Context/laag/query niet beoordeelbaar of data ongeldig | Geen ja/nee-capaciteitsclaim; bestaande scorefallback |
| 1 ASSESSED_LT3 | Query volledig geldig; exact minder dan3 unieke open bergen | Deze momentopname voldoet niet aan capacityvoorwaarde |
| 2 ASSESSED_GE3 | Query volledig geldig; minstens3 unieke open bergen | Alleen capacityvoorwaarde voldaan; voedsel-/ontwikkelplan vereist |

`H2Result` is256bytes: int32 status op+0, reason op+4, open_count op+8, mountain_count op+c; daarna20 eigen entries van12bytes: positie8bytes (signed16 x/y/z op+0/+2/+4, padding+6 altijd0), terrain int32 op+8. Alleen entries0..open_count−1 zijn geldig bij ASSESSED. open_count/mountain_count zijn dan exacte aantallen0..20. UNKNOWN gebruikt beide aantallen−1 en alle entries0. EAX moet dezelfde status zijn als result.status.

reason=0 bij ASSESSED. Eigen UNKNOWNredenen:1 CONTEXT;2 UNSUPPORTED_LAYER;3 CENTER_GATE_REJECTED;4 INVALID_COUNT;5 INVALID_POSITION;6 TERRAIN_QUERY_FAILED;7 INVALID_TERRAIN. Deze enums zijn foutcodes, geen gewichten. Afgewezen centrumquery blijft onderscheiden van een geldig beoordeelde lijst met0bergen. Geen gedeeltelijk getelde driebergenlijst als geslaagd resultaat teruggeven wanneer een latere tilequery faalt.

`canonical_center` is de geldige MapPointData van de bestaande H1-kandidaatopbouw. Deze inputpreconditie voorkomt een eigen kaartnormalisator/dimensie-interface. Voor willekeurige externe coördinaten is deze API niet vrijgegeven. Outputposities zijn de door de engine geconverteerde/wrapped MapPointData; vergelijk x/y/z, negeer padding. Verwijder een teruggegeven centrum defensief. Geen eigen y−x-omzetting, vierkante radius of schermcoördinaten.

## Bestaande queries en exact scratchgebruik

De [H2-analyse](../ANALYSE/PRODUCTIEKANDIDAAT-H2.md) en gerichte [positie-/gate-ABI](../ANALYSE/BINAIR/production-candidate-h2-position-and-cell.txt) binden drie verschillende methoden:

| Query | Rechts-naar-links pushvolgorde | Stack bij callee-entry | Return |
| --- | --- | --- | --- |
| World+28 | center, World | esp+4 World; +8 center | EAX gate; `ret8` op5335a2 |
| World+ac | rawarray, countpointer, center, civ, World | esp+4 World; +8 civ; +c center; +10 countpointer; +14 array | Countoutput; `ret14h`; EAX niet als bool gebruiken |
| World+a8 | terrainoutput, position, World | esp+4 World; +8 position; +c int32output | EAX1/outputindex; `ret0ch` |

Haal telkens de World-vtable uit `[World]` en call het juiste slot; geen engineadresconstant of import toevoegen. Iedere method heeft haar eigen argumentlijst/popgrootte. World+28 gebruikt de bij World horende Player-route; World+ac krijgt dezelfde actuele civ als de normale AI-caller. Er wordt geen extra semantische naam of volledige legaliteitsclaim aan de gate gegeven.

Reserveer voor World+ac **exact twintig8-byte positieobjecten,160bytes**, als lokale rawscratch. Gebruik hiervoor niet de eigen12-byte resultaatentries. Count begint0. De bewezen engine heeft maximaal20uitvoeren; boundscontrole na return controleert de uitkomst, voorkomt op zichzelf geen corrupte native write. Fixtureguards/native canaries zijn een C-verificatie van dit ABI-contract.

Resultbuffer en scratch zijn eigendom van de caller/huidige call, niet van een globale cache. De wrapper zelf gebruikt bestaande globale engine-scratch: H2 wordt uitsluitend in dezelfde seriële, niet-reentrante AI-context aangeroepen. Geen achtergrondthread, parallelle query of geneste H2-call tijdens een World-callback. Een lokale buffer maakt de enginewrapper niet vanzelf thread-safe.

## Algoritme, inclusief duplicates en fouten

```text
initialiseer resultaat UNKNOWN/CONTEXT, counts=-1, entries=0
controleer geldige huidige AiMain/Worldcontext en canonical inputcontract
als center.z != 0: UNKNOWN/UNSUPPORTED_LAYER
als World+28(World, center) == 0: UNKNOWN/CENTER_GATE_REJECTED
raw[20×8] = 0; count=0
World+ac(World, AiMain.civ, center, &count, raw)
als count<0 of count>20: UNKNOWN/INVALID_COUNT
voor i=0..count-1:
    p = raw[i×8].signed16_xyz
    als p.z != center.z: UNKNOWN/INVALID_POSITION
    als p.xyz == center.xyz: sla over
    als p.xyz al in voorlopige unieke lijst: sla over
    terrain=-1
    als World+a8(World,&raw[i×8],&terrain)==0:
        UNKNOWN/TERRAIN_QUERY_FAILED
    als terrain niet in0..23: UNKNOWN/INVALID_TERRAIN
    voeg p (padding0),terrain aan voorlopige eigen lijst toe
    tel berg als terrain8 of20 of22
bij elke fout: wis gedeeltelijke lijst; beide counts=-1
na volledige geldige loop:
    publiceer exacte unieke lijst en counts
    status=ASSESSED_GE3 als mountains>=3, anders ASSESSED_LT3
```

Voorlopige lijst kan lokaal zijn of in de resultaatbuffer staan zolang fouten de gedeeltelijke gegevens volledig wissen vóór return. Maximaal20entries; eenvoudige O(20²)vergelijking volstaat. Geen allocatie, externe container of nieuwe bibliotheek nodig. Loop stopt niet vroeg na de derde berg: anders ontbreekt een volledige footprint voor voedselkeuze en kan een latere queryfout verborgen blijven.

Een lege lijst na een vooraf toegelaten gate is ASSESSED_LT3 met0bergen. De gate wordt ook binnen World+ac gebruikt; een stabiele selectiecontext is daarom preconditie. Een gewijzigde gate/wereldtoestand tussen reads betekent een ongeldige momentopname, geen bewijs van werkelijk nulcapaciteit. In C constateren bij re-entrancy/contextwisseling: stop de integratie en leg de concrete gebeurtenis voor aan de analist; geen event-/observerproject op voorhand bouwen.

De bestaande wrapper doet503f00/503f70-conversie. Eigen x/y/z-gelijkheid is geldig voor haar canonical teruggegeven posities en de canonical kandidaatinput. Pool-/kleinekaartgedrag is geen bewezen complete werkplaatsingsgarantie. Exacte duplicaten tellen eenmaal; paddingverschil telt niet als nieuw vakje. Er komt geen zelfbedachte kaartbreedte of modulo. Een toekomstige caller met nietcanonical input moet eerst een bewezen canonical route krijgen.

## Huidige open plekken, eigendom en overlap

World+ac gebruikt bestaande511030/Cell+18/Cell+14 en army-ownerbranches. Zowel eigen als buitenlandse aanwezige laborers en bestaande stadscentra worden daardoor niet geteld. De payload omzeilt die checks niet. Een lege tile in overlappende footprints blijft wel beschikbaar: overlap alleen is geen uitsluiting of afstandsstraf.

Dit is een **momentopname**, geen permanente exclusiviteit. H2 kan dezelfde lege berg voor twee kandidaatcentra melden; dat is correcte huidige capaciteit en nog geen gezamenlijk uitvoerbaar stadsplan. Nieuwe kolonistenreserveringen, latere workerverplaatsing, stichting en tijdstip binnen een eventuele bevolkingsreset vragen een later plan-/herbeoordelingscontract. H2 schrijft geen tileclaim en sluit geen andere stad uit. Daadwerkelijke Population-plaatsing blijft aan echte stad/inwonerhandles en de bestaande enginevoorwaarden gebonden.

## Aansluiting op driebergen-plus-voedselclassifier

Plaats de H2-query als eigen relatieve subroutine in dezelfde H1-payloadsectie; hergebruik emitter, modulebase/RVA-aanpak, header-/reloc-/hashcontract. Geen vierde hook of nieuwe DLL is nodig. H2 verandert de bestaande drie sites niet opnieuw buiten een nieuwe, afzonderlijk gebouwde variant; H1-I/H1-Mbronnen zijn in eigendom van de uitvoerder. Geen gedeelde cache, saveveld, stadstaak of hot-load.

Het volgende classifiercontract is expliciet **eigen ontwerp, nog niet geïmplementeerd**:

```text
capacity = H2_Capacity(current_ai, World, center)
capacity.UNKNOWN -> classifier.UNKNOWN -> oorspronkelijke scorefallback
capacity.ASSESSED_LT3 -> geen huidige driebergencapaciteit; andere stadsfuncties blijven mogelijk
capacity.ASSESSED_GE3 -> zoek een gezamenlijk plan:
    kies3 verschillende bergentries
    kies1 andere, verschillende open voedselwerkplek
    beoordeel centrum + deze4werkers en ontwikkeling/timing
    alleen bij bewezen onderhoudsdekking: productionplanbeoordeeld
```

Kies niet blind de eerste driebergen. Een good/omgeving kan ook op een berg food leveren; als dat de voedselwerker wordt, moeten drie **andere** bergwerkplekken overblijven. Alle vier plekken moeten verschillend zijn; centrum telt als voedselbijdrage volgens de echte centrumregel maar nooit als één van de drie laborerbergen of de vierde laborerplek. Hergebruik dezelfde H2-unieke lijst voor het gezamenlijke plan, zodat capaciteit en voedsel niet op verschillende footprintmomenten berusten.

De voedselbeoordeling moet onderscheid maken tussen onderhoud dat nu haalbaar is en toekomstig onderhoud na aanleg/tech. Normaal geen eerste generatie foodimprovements; Ocean Faring/Agricultural Revolution zijn leidend, met alleen de afgesproken Labyrinthuitzondering. Geen fictieve farmopbrengst, crime0, centrumfood20 of lage rantsoenstand als stilzwijgende default. Een later waar toekomstplan bewijst niet dat snelle stichting nu verstandig is. Productiongeschiktheid en vestigingsurgentie blijven aparte uitkomsten; een hele slechte voedselontwikkeling wordt niet met alleen het capaciteitpredicate overruled.

**Eén gerichte vervolg-A-vraag voor de volgende classifier:** welke bestaande query-/leesroute, met exacte ABI en velden, geeft vóór stichting zonderCityID het voedselbudget van één hypothetische grootte4-stad op dit kandidaatcentrum met3gekozen bergwerkers en1gekozen voedselwerker, inclusief werkelijke centrumbehandeling, huidig terrein/improvement, toegestane improvementvariant/tech, huidige rations en toepasselijke crime/stadsmodifiers? Hergebruik de reeds bewezen City494970/inlineconsumptie en Improvementgetters; bind uitsluitend de ontbrekende kandidaatinputs of een aantoonbaar conservatieve berekenbare grens. Geef UNKNOWN wanneer een noodzakelijk nietbestaand stadsgegeven niet eerlijk is af te leiden. Geen mockCityID/fictieve CityData en geen volledige economie-/groei-/geluksanalyse.

Deze vraag blokkeert een **volledige voedselconforme scorefeature**, niet het bouwen van het concrete capaciteitpredicate. H2 heeft zelf geen onmisbaar ontbrekend analysegegeven. Oude rapportpassages waarin de gehele consumptie onbekend was zijn achterhaald: [RANTSOENEN-EN-STADSOPBRENGSTEN](../ANALYSE/RANTSOENEN-EN-STADSOPBRENGSTEN.md) heeft normale centrum-/foodsom en werkelijke inlineonderhoudsberekening al gebonden. De resterende vraag is toepassing op een nog niet bestaande kandidaatstad.

## Verwacht effect, alternatieven en afzonderlijke controles

Verwacht resultaat van H2: betrouwbare tri-stateinformatie voor volgende planselectie, inclusief het verschil tussen driekaartbergen en drie momenteel beschikbare werkplekken. Geen zelfstandige gameplaywinstclaim. Kosten: maximaal1gate+1openquery+20terrainqueries en≤190dedupvergelijkingen per kandidaat. Werkelijke tijd wordt in C gemeten, geen uitkomst of vaste CPUkost verzonnen. Unknownfallback kan bruikbare plannen missen; conservatieve beschikbaarheid kan eigen herplaatsbare bergen tijdelijk afwijzen. Geen globalfail of permanente afwijzing van de locatie op UNKNOWN/LT3.

Alternatieven: rawkaartbergen tellen overschat bezette bergen; geometrie zelf bouwen verliest army-/bezettings-/wrapfilters; Player+120 met verzonnenCityID is ongeldig; driebergenbonus zonderfood mist de projectdefinitie; alle overlap straffen sluit nuttige dichte locaties uit. Daarom de bestaande enginequery gebruiken en de capaciteit apart publiceren.

Later in C, na rootreview/uitleg/vrijgave, met dezelfde H1-fixture/nativehelperroute en alleen relevante gevallen:

| Geval | Vereiste uitkomst |
| --- | --- |
| 3openbergvarianten8/20/22 | GE3,count3 |
| 3ruwebergen waarvan1 door eigen of vreemde laborer bezet | LT3,max2; enginefilter wordt benut |
| 1berg als bestaand stadscentrum | Niet tellen |
| 3openplekken waarvan hills9/19/21 | Geen bergcount voor hills |
| Open tile in overlappende stadsfootprints | Nog beschikbaar, geen afstandsafwijzing |
| Dezelfde xyz tweemaal met ander padding | Eenmaal tellen |
| Centrum teruggegeven door fixture | Verwijderen; niet als bergwerker tellen |
| Gatefalse / geldige count0 | UNKNOWNreason3 / LT3,count0 onderscheiden |
| count−1 of21, foutstatus, terrain−1/24 of andere laag | UNKNOWN,geen gedeeltelijke counts |
| Civ/worldwisseling | Eigen actuele context; geen vorige lijst/pointers hergebruiken |
| ABI | +28ret8,+acret14h,+a8ret0ch; rawstride8, eigenstride12; canaries/stack/registers intact |

Fixtures bewijzen eigen verwerking van engine-antwoorden, geen volledige placeability. De bestaande oorspronkelijke filter-/footprintcontroles worden hergebruikt; geen nieuwe emulatie/observer voor dit voorstel. Query-onlyH2 mag bij integratie met H1 dezelfde score als zijn gekozen H1baseline teruggeven. Een onverwachte score-/goalwijziging is dan geen capaciteitwinst maar een fout of ongeldig vergelijkingspaar.

## Benchmark, herstel en overdracht

H2bouw/ABI is een afzonderlijk uitvoeringspakket; voor echte classifier/gameplay later exact dezelfde QUOTA-START-T0/hash `8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26`, dezelfde B1achtAIPs en passieve menselijke invoer. H1baselinevariant expliciet kiezen/vastleggen en constant houden; verander alleen H2respectievelijk de latere voedselclassifier. Nieuwe heap/goalactivatie aantonen; oude opgeslagen doelen worden niet automatisch herberekend. Geen nieuwe game, savepatch/hot-load of doelmutation. D-gamePID19516 blijft ongemoeid; echte run wacht op rootvrijgegeven runtime.

Bewaar emitterrecept/payload-/DLL-/baselinehashes en diffmanifest zoals H1. Rollback van een latere H2variant herstelt de vastgelegde vorige proef-DLL, niet automatisch OG wanneer B1/H1 de baseline is. Behoud andermans bestanden; herstart en dezelfde ongewijzigde T0. Variante-save is geen herstelde start. H2introduceert geen eigen opgeslagen metadata.

Volgorde: rootreview/uitleg → eventueel C voor query-onlycapacity → gerichte bovenstaande voedselroutevraag → B voor gezamenlijk3berg+voedselplan/urgentie → aparte C-classifierproef. Masker×classifier, worker/improvement×capacity en meerdere kandidaten×gezamenlijke bergbenutting krijgen eigen combinatieproeven. Het enkele H2predicate voltooit geen productiestad-/projectdoel. Ontwerper stopt bij deze beperkte concrete overdracht.
