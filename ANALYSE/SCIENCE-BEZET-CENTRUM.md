# SCI: bewezen bezet centrum lokaal afhandelen

19 oktober 2026, 20:24 Europe/Amsterdam. Gerichte fase A voor Doel1/1a/5; vijf beslisvragen hieronder afgehandeld. Alleen dit rapport gewijzigd. Geen code/reader/binary/helper/game gewijzigd of gestart. Analyse stopt zodra B op deze overdracht kan voortbouwen; geen verdere brede reconstructie nodig. Budget20:21 vers vijf18/week75, pcaan.

## Uitkomst voor B

De bewezen fout is **de eigen FoodReader-scopeguard voor aanwezige units**, niet een voedseltekort of mislukte enginegetter. Een onderbouwde kleine eerste ingreep is: uitsluitend een **vers gebonden SCI_CENTER-failure op branch10 met positieve unitcount** behandelen als tijdelijke lokale scope-uitsluiting, expliciet `NO_NOW / OCCUPIED_CENTER / coverage1`, zonder voedselcredit. Dan gaat de union door met de overige centra en blijven eerdere geldige SCI-NOWalternatieven beschikbaar voor gewone gezamenlijke selectie.

Dit is bewust een conservatieve certificeringsregel: “dit bezette centrum telt in deze pass niet mee voor onze extra SCI-voorraadbehoefte”. Het zegt niet dat stichting daar illegaal is of dat de locatie slecht voedsel heeft. Native vestigingsdoelen/plaatsingslogica worden hiermee niet gewijzigd. Andere FoodReader-guards, workerreadfailures, cityhandlebranch9, contextmismatches en budgetfouten blijven hun bestaande uitkomst houden. Geen algemene UNKNOWN-skip.

Belangrijk: de bestaande **first-centerfailurelatch is geen actuele per-call-beleidscode**. Gebruik haar niet zonder huidige identiteit; zie vraag4 voor de benodigde verse oorzaakoverdracht. Dit voorkomt dat een latere echte fout door een oude branch10 wordt gemaskeerd.

## 1. Wat de echte guard betekent

Bewijs: `PROEVEN/science-foodreader-host/20261019/host1/variant/T1.json`, SHA256 `012de2a7982a71386ffcaa0c2227abfd1c8d38515c6a17f0ecb4b5affdc80b11`. Kandidaat `068ff459a19125fdd08db060450110210ad992698d27b920894f4502ac4aae4f`, manifest `beebdb07abeb5bf111869e53f1c15dbb6466ece17808022276241d6ee4e28e44`. Diagnose BOUND_COMPLETE_GUARD_OPERANDS/usabletrue; laatste civ8/generation7/prefix3/primaryordinal64/callkindSCI_CENTER.

Externe positie `(28,73,0)` wordt intern `(28,45,0)`; de vierde16bitwaarde74 in de interne rawbytes is padding, geen z of coördinaat. Cellpointer179373484; cityhandle0; armyarray195128928; unitcount2; guard_a2/guard_b0. Native_called0 en alle voedsel-/terrein-/getterwaarden ONBEREIKT. De oorspronkelijke guard staat op **200d660a**: `[Cell+10h]+30h != 0 → food_bad`. De nieuwe clone gebruikt dezelfde semantiek met aparte diagnose.

Dit bewijst twee units in de native celarray tijdens die read. Het bewijst **niet** hun eigenaar, type, missie of voedselbijdrage. Noem ze niet automatisch eigen settlers. Hun aanwezigheid is ook geen algemene vestigingslegaliteitstest. De reader weigert de context omdat de normale rawfoodgetter tijdelijke unitfood kan toevoegen; hij berekent in dit geval geen voedsel. SCIstate0/reason11/coverage0 wordt daardoor wholepassreason23/Gcert0, ook al was SCI0 al een geldig voorbereid voorbeeld.

## 2. Native voedselpad en route zonder tijdelijke unitbonus

Hergebruikte enginebinding: World+b8 **00534340**, schrijft food op534364, retourneert EAX1 op534366; World510f70→Cell500110. Enginehash onafhankelijk herlezen `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, base400000/timestamp37d6f702; geen civctp.map. Bestaand volledige bewijs: `ANALYSE/BINAIR/engine-locatiewaarde-tilehelpers.txt` en `KANDIDAATVOEDSEL-H3.md`.

| Native plek | Werking |
| --- | --- |
| 50012e–50017c | Selecteert terrein/goodrecord uit echte flags en TerrainDB. |
| 50018f–50020c | Basefood + geselecteerde road/irr/mine/rivier/kanaalbijdragen. |
| 50020c–50021e | Alleen bij aanwezige cityhandle: ENV_CITY_BONUS toevoegen. |
| 500221–50022a | Negatieve som naar0 clampen. |
| 50022a–50022c | Bij cityhandle!=0 direct naar eindreturn; geen unitfoodtak. |
| 50022e–50025e | Bij cityhandle0: loopt over Cell+10-array, count op+30h, entries op+4+4i; vraagt per unit het record en test record+208h. Nul/negatieve bijdragen worden overgeslagen. |
| 500260–50027a | **Alleen de eerste positieve unitfoodbijdrage** wordt aan de eerder berekende som toegevoegd; daarna eindigt deze getter. Het is geen som van alle units en count2 bewijst dus geen tweemaalbonus. |

De enige aanvullende ontbrekende edge is direct in de echte engine gecontroleerd: **004da870** leest de unit-ID, resolveert via native unitpool **004b23e0**, leest UnitData+30h (type) en vraagt UnitDB **004542e0**. De aanroeper test dus de voedselbijdrage **UnitRecord+208h**, geen army-owner of settlerkenmerk.

Een toekomstige volledige ondersteuning is technisch voorstelbaar: bereken zuivere omgeving uit de bestaande readertermen; lees dezelfde begrensde unitarray/ID→recordketen, bepaal exact de eerste positieve native bijdrage en verifieer native getter gelijk aan de bijbehorende clamped omgevingssom plus die bijdrage. Voor het hypothetische nieuwe centrum telt daarna alleen omgeving plus eenmaal terrein/good-CITY_BONUS, zonder tijdelijke unitbonus. Daarvoor zijn actuele count-/ID-/pool-/recordbinding, stabiele cel/owner/generatie, signed32/native overflow en signed64-omgevingsguards nodig. Blind de native getterwaarde gebruiken, alle unitfood optellen of `count×bonus` aftrekken is fout.

Die uitbreiding vraagt meer foreign reads en nieuwe ondersteunde context. **De huidige ene bewijsbare lokale uitsluiting heeft deze uitbreiding niet nodig.** Zij kan B nu uitvoeren; volledige unitvrije food blijft een afzonderlijke verbetering om later ook bezette goede locaties te certificeren. Er is nog geen bewijs dat de huidige twee units überhaupt positieve unitfood leveren.

## 3. Kleinste lokale afhandeling en grens van coverage

Concrete route in een nieuw eigen pakket: laat de SCI-only clone branch10 en out40wipe behouden, maar lever de verse precieze oorzaak mee via eigen state met return0, of via een expliciete private return2 zoals bij vraag4. In `science_model.model`, onmiddellijk na de centrum-H3FoodReader-call en uitsluitend op die afgewezen-centerroute:

1. Controleer dat het verse oorzaaksrecord exact deze actuele gebonden centerinvocatie betreft; branch10, count>0, cityhandle0 en geldig voorafgaand cel-/coördinatenpad.
2. Zet voor dit centrum een benoemde lokale toestand: bestaande NO_NOW1 met een nieuw uniek reason `OCCUPIED_CENTER_SCOPE` is de kleinste route. Coverage1 betekent hier **een volledig bepaalde conservatieve afwijzing binnen de huidige certificeringsscope**, niet een uitgevoerde voedselanalyse. Ontwerp/decoder moeten dat expliciet noemen.
3. Laat alle selectedindices−1, alle food-/margevelden ongebruikt en geef geen SCI-NOW2/foodcredit. Return via science_done zodat oorspronkelijke x87-/stackafwikkeling behouden blijft. Union accepteert alleen state2 als science-alternatief; state1 gaat regulier naar roles_commit en vervolgens het volgende centrum.
4. Alle niet-exacte gevallen volgen het bestaande science_bad/wholepassfallback. Negatieve unitcount, ontbrekende oorzaak, verkeerde callkind, oude identiteit en conflicterende context zijn geen lokale negatieve uitkomst.

Dit behoudt eerdere gecommitte positieve alternatieven, maar garandeert **geen** selectie of Gcert>0: bronclaims, veilige paden, conflicten en latere echte fouten blijven gelden. SCI0 bewijst al huidige foodkeys/positieve marges; diens bewijs wordt niet vervangen door de negatieve scope-uitkomst van centrum3.

Branch9 (bestaande stad) blijft buiten deze wijziging. Ook workerreadbranch10 krijgt geen verzonnen food0 of positieve coverage voor voedselwaarden. De gedeelde H3-productieclassifier kan bij andere centra vóór SCI nog een echte fout geven; deze eerste ingreep verandert die keten niet. Geen claim dat alle bezette productie-/sciencecentra hiermee volledig ondersteund zijn.

## 4. Codepunten, verse oorzaak en invarianten

Bronpunten in `PROEVEN/science-foodreader-diagnostiek/20261019T194200`: `food_diagnostic.py` FoodStage/emit_reader, `food_diagnostic_layout.py`, `science_model.py` centerread-failurepad, builder/labels/pins en de eigen readerdecode. `union.py` hoeft voor de bestaande state!=2/coverage1-route niet inhoudelijk te veranderen. Werk in een nieuw pakket; historische kandidaten/release onveranderd.

**Latchgevaar:** `FoodStage.failures_and_publish` bewaart de eerste centerfailure per owner/generation. Nadat centrum3 lokaal zou zijn afgewezen, kan bij centrum4 een andere failure optreden terwijl die historische record nog branch10 bevat. Een handler op alleen `branch_id==10` zou dan een echte fout overslaan. Exacte matching van prefix/ordinal voorkomt dat, maar zou meerdere bezette centra binnen dezelfde generatie niet meer ondersteunen.

Een robuuste keuze voor B is naast de historische236byte-diagnoselatch een klein **actueel per-invocation oorzaaksrecord** in vrije eigen SCI-scratch reserveren, bijvoorbeeld na de bestaande owner/generatievelden vanaf Plan+78808h (exact bereik eerst aan layout toetsen). Reset het bij iedere gebonden SCIclone-entry en publiceer branch/callkind/count/cityhandle/owner/generation/prefix/primaryordinal/externe centrumkey vóór de oorspronkelijke failure-return; validmarker als laatste. Success/bindingfailure mag geen oud geldig oorzaakrecord achterlaten. De bestaande firstfailurehistorie blijft diagnose, niet de beslisbron.

**Een nog kleinere B-optie is een directe getypeerde return uit alleen de private SCIclone:** 0=UNKNOWN,1=normale foodread,2=exact vers gebonden CENTERbranch10/count>0. De centerhandler moet2 dan expliciet afhandelen vóór de bestaande nul/nonzero-foodreadtest; hij mag2 nooit als geldige out40-fooddata consumeren. Tilecalls blijven0/1, gedeelde H3 blijft0/1, out40 blijft bij afwijzing gewist en de historische diagnose blijft afzonderlijk. De clone heeft de actuele callkind/owner/generatie/prefix/argumentbinding al in haar eigen frame; daarmee kan een directe typed return de extra scratch-oorzaakopslag vermijden. B kiest en specificeert deze private contractwijziging, inclusief contextvalidatie vlak vóór return en aangepaste negatieve cases; deze A past haar niet toe.

Bij een oorzaakrecord valideert de modelhandler scope1/guard1, eigen owner/generatie tegenover scratchsnapshot, huidig prefix=classified−1, huidig primaryordinal, callkindCENTER en exact huidig CAPTUREcentrum. Bij typed return gebeurt die verse validatie in de clone, met expliciete2-afhandeling in het model. Foreign-objectguards blijven staan; de lokale afhandeling mag geen nieuwe unititems derefereren of de clone alsnog native food laten opvragen. ABI20bytes/ret20, out40wipe, oorspronkelijke UNKNOWN-return0, GPR/EFLAGS/nonvolatile/x87, alle querybudgetten en context-onlypostguards blijven behouden. De gedeelde H3-reader/score/developmentroute blijft bytegelijk. Geen in-place engine-/cell-/queuewijziging.

Tijdelijkheid is essentieel: START wist de eigen passstate; een volgend echte planronde beoordeelt de locatie opnieuw. De regel is geen persistente blacklist en zegt niet dat een unitbezetting een permanent gebrek aan vestigingsruimte is. Plaatsings-/verdedigingsveiligheid en transport blijven latere bestaande selectievoorwaarden.

## 5. Eindige verificatie en acceptatiestatus

Na B en bron/pinreview: kleine gerichte offline/nativecases op de bestaande infrastructuur, geen nieuw harness. Vereist onderscheid: exact centerbranch10/count>0 wordt lokaal NO_NOW/coverage1; workerbranch10, branch9/andere branch, count<0, oude prefix/ordinal/owner/generatie en contextfout blijven UNKNOWN; twee opeenvolgende centerread-failures waarvan de tweede een andere guard heeft mogen de eerste latch niet hergebruiken. Positief SCI0 blijft dezelfde echte huidige key/marge-uitkomst; normale clone-return/out40 en gedeelde H3 blijven behouden.

Daarna **één afzonderlijke vaste T0→T1-proef, maximaal één n**, dezelfde zeven AI's/Deity/passieve mens en bestaande identiteit/budget/tijd/herstelpoorten. Meet: huidige branch10-oorzaak exact gebonden; centrum3 expliciet lokaal afgewezen met foodvelden niet als meting; SCI0 huidige keys `(27,45,0)/(29,42,0)/(27,43,0)/(28,42,0)`, stand−1/R0,75/marges35/30/25 behouden; classified gaat voorbij4 als geen andere echte fout optreedt; reason/context/slots/Gcert en eventuele bron-/padselectie afzonderlijk uitlezen. Stop bij een andere wholepassfailure en benoem die, geen automatische verdere skip of langere benchmark.

Volledige reason0 en werkelijke SELECTED-evidence zou aantonen dat de eerdere geldige wetenschapscasus de gezamenlijke selectie kan bereiken. Extra vraag vereist afzonderlijk Gcert>Dorig/aanvullend native tekort; gewenste vraag5 kan onveranderd blijven. Een korte technische pass bewijst geen veilige stichting, worker-/scientistinzet, stadsontwikkeling, economie of30→40steden. Doel1/1a/5 blijven open; Doel3 blijft bewezen behouden.

**Overdracht:** vijf van vijf vragen voldoende beantwoord voor B. Concrete oorzaak armycount_nonzero is nu bewezen; alleen het exacte beperkte geval wordt lokaal uitgesloten. Een onderbouwde ontwerper kan de verse oorzaakoverdracht en lokale scope-uitkomst uitwerken zonder verdere A of spelstart. Deze rol is gestopt; geen achtergrondwerk, pcaan.
