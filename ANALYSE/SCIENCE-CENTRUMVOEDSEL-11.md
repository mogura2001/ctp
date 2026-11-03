# Sciencecentrum reason11: volledige FoodReader-failureboom

19 oktober 2026, 19:34 Europe/Amsterdam. Gerichte read-only fase A voor Doel1/1a/5. Vraag: welke guard verklaart de vierde SCI-classificatie, en welke begrensde ingreep kan de concrete guard aantonen zonder UNKNOWN over te slaan? Alleen dit rapport gewijzigd; geen helper, reader, code, binary, spelstart of livegeheugenactie. Voldoende voor een diagnostisch B-voorstel; deze A stopt.

## Conclusie

**Het nulveld is geen waargenomen nulopbrengst. De vierde SCI-centerread retourneert niet-ondersteund; de concrete interne FoodReader-guard is nog niet opgeslagen.** Numeriek nulfood is door de reader ondersteund, en nul centrumfood betekent op zichzelf geen ongeschikte scienceplek. World+b8 retourneert altijd EAX1 in de gepinde wrapper en schrijft de integerfood apart; er is geen aangetoonde verwisseling van foodwaarde en succesboolean.

Geen huidige interface-/ABI-bug of specifieke wereldtoestand bewezen. Onder meer een aanwezige stad/eenheid, ongedekte goodcontext, somguard of verschil tussen eigen omgevingssom en native getter kan deze terugval geven. De bestaande data wist juist de onderscheidende waarden. De volgende stap is daarom één volledige **SCI-only FoodReader-failurediagnose**, niet een gameplayfix of langere benchmark. Hieronder staat de complete eindige boom zodat de volgende proef alle mogelijke interne ingangen onderscheidt.

## Gebonden bewijs en plaats van de fout

Diagnose `PROEVEN/u30-science-filter/20261017T124500/diagnostic-reader/host2/variant/T1.json`, SHA256 `4d0b49a61ed66c63a74e1cd342e695fd8b32505bb5a7dce675bf384d2a1bb5ae`. Dubbel stabiel, civ8/generation7/usable_diagnostic_evidencetrue; geen per-civ-historie. Onveranderde kandidaat-SHA256 `0ebafb11e08bc7dca74291dd8a8e9ea94441af09602ae2d94710217f19eabad9`, PE-base20000000/timestamp37b894e7. Engine-SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`; civctp.map niet gebruikt. Kandidaat- en enginehash zijn onafhankelijk herlezen; onderstaande adressen komen uit directe kandidaatdisassemblage of bestaande gevalideerde enginedumps.

Laatste centrum is externe CAPTURE `(28,73,0)`, SCIindex3. Header: state0/reason11/model1/conditions3/open_count20/H2status1/stand−1/R0,75/coverage0; alle geselecteerde indices−1, center_food0/center_key0. Werk-H3 heeft een geldige enum met één berg; minder dan drie bergen is geen H3fout. De volgende ORDER-index is geldig. SCIcalls=classified4/tiles60/primaryfood64/developmentfood27/totalfood91, context_error0/budget_exhausted0. Eerste sciencevoorbeeld0 heeft current centerfood15, gekozen food10/5/5, stand−1/R0,75, n1/2/3-marges35/30/25 en geen drie bergen; het is voorbereid, niet geselecteerd, Gcert0.

`science_model.py:95` zet reason11 vóór de rantsoen- en centerfase; dit ene getal is dus geen afzonderlijke voedsel-failurecode. De telling maakt het onderscheid:

- Iedere begonnen tile verhoogt tiles en vervolgens primaryfood eenmaal. Deze60tiles zijn alle vóór de laatste SCIcall voltooid: de vierde bewaart reason11, terwijl de tilefase vooraf reason12 schrijft. De vorige drie aanroepen moesten coverage1 bereiken om door te lopen. Max20tiles per aanroep verklaart precies3×20.
- De overige vier primaryfoodtoelatingen zijn de vier centerreads. De vierde call heeft dus de rantsoenchecks en zijn centeradmission gepasseerd. Stand−1/R0,75 klopt met `1+stand/4`; eigen context-/budgetfailure is bovendien niet gezet.
- Center-call op **200df14b** gaat werkelijk naar gedeelde H3FoodReader **200d64f5**; EAX0 springt op **200df152** naar science_bad200e022f. Het SCI-centerfoodveld wordt pas op **200df17e/184** geschreven; centerkey pas daarna, en reason12 pas op200df19c.
- De overige twee post-call failure-ingangen in deze fase zijn signed64-overflow200df170 en negatieve highword200df178. Die zijn bij een geldige terugkeer van deze ongewijzigde reader niet bereikbaar: de reader controleert reeds getter+bonus op0..INT32MAX. Met het gevalideerde calleecontract is de centerreadreturn0 daarmee de verklaarde foutgrens, niet een gemeten voedseltekort.

`food_bad` op200d697c wist alle40outbytes en geeft EAX0. SCI bewaart de lokale out40 niet; science_bad wist coverage/certifiable_count. Geen latere alleen-lezen decode kan deze verdwenen getter-/celwaarden herstellen.

## Volledige eindige FoodReader-badboom

Bron `PROEVEN/production-h3/components.py:reader` en `environment_add`; identieke interne readerbytes in deze kandidaat op RVA d64f5..d6994. Alle **37 directe bad-branches** staan hieronder; elke site kan een eigen branch-ID krijgen. Adressen zijn VA bij geladen AI-base20000000. De tabel bevat hun oorspronkelijke guard, geen nieuwe toelatingsregel.

| Bad-branch-VA's | Concrete voorwaarde | Te bewaren waarden bij die branch |
| --- | --- | --- |
| 200d653c | Geconverteerde interne z!=0. | externe en interne xyz. |
| 200d6558,200d6574 | unsigned x>=loaded width, respectievelijk y>=height (omvat negatieve signed16). | xyz, width/height. |
| 200d6588,200d6596,200d65a4,200d65bd,200d65d6 | Null: HostBinding.grid; grid+1c; laag0; x-kolom; uiteindelijke Cell. | relevante laatste pointer en dereferentie-offset, interne xyz; geen extra dereferentie na null. |
| 200d65ec | Cell+14 bevat bestaande cityhandle. | Cellpointer/cityhandle. |
| 200d660a | Cell+10 armyarray bestaat en `[array+30h]` unitcount!=0. | armyarray en count; geen aanname over unitfood of eigen/vreemd. |
| 200d661d | Terrain signedbyte unsigned>23. | terrainbyte. |
| 200d6629,200d6635,200d6641 | Terrain13/18/23: space/dead/dead-hill ongedekt. | terrainindex. |
| 200d665d,200d6669,200d6675,200d6681,200d668d,200d6699,200d66a5 | Alleen `isCenter!=0`: terrain10/11/12/14/15/16/17, water/special; normaal landcentrum vereist. | isCenter, terrainindex. |
| 200d66b9,200d66c5,200d66d3 | TerrainDB null; index>=count; recordarray null. | databasepointer/count/index/array (alleen al gelezen operands). |
| 200d66fc | Goodcode `(cellflags>>6)&7`>4. | flags, raw goodcode. Geen afwijzing van een gewone nulcode. |
| 200d67a2,200d67e5,200d6828,200d685f,200d6896 | JO na signed64-optelling van respectievelijk road/irrigation/mine/river/canal-food. | gekozen record, featurelevels/flags, betreffende environmentpointer/addend en som vóór/na/overflow. |
| 200d68aa,200d68b2 | Omgevingssom vóór native getter: high32!=0 of low32 negatief. | basefood, alle gebruikte addends, somhigh/low. |
| 200d68ef | World+b8-return EAX0. | native_called, returnEAX, output vóór/na (vooraf sentinel−1), world/slotbindingidentiteit. Gepinde wrapper geeft normaal altijd1. |
| 200d6901 | Geschreven native food != eigen gecontroleerde omgevingssom. | native output, eigen som, flags/terrain/goodcode/mainrecord/gekozenrecord en addends. Geen automatische clampcorrectie of gelijkstelling. |
| 200d6944 | JO bij optellen CITY_BONUS, alleen centrum en bonuspointer aanwezig. | bonuspointer/signedbonus, getterfood, som vóór/na/overflow. |
| 200d695a,200d6962 | Centrumtotaal na bonus: high32!=0 of low32 negatief. | dezelfde bonus-/gettersomwaarden. |

Ontbrekend environment of bonuspointer is op zichzelf **geen** bad-branch: de bijdrage wordt overgeslagen. Goodselectie zoekt terug naar een aanwezige subrecord en valt zo nodig op hoofdrecord terug. Bewaar daarom raw goodcode én werkelijk gekozen slot/record; een GOOD_INDEX uit tekst is geen lokale slotcode. De guardboom sluit gewone bestaande stad-/unitcontext bewust uit; een getriggerde guard kan een ondersteunde-scopegrens zijn en hoeft geen enginebug te betekenen.

## Nulfood en mogelijke celcontext

De native wrapper **00534340** converteert de externe MapPoint via503f00, roept World510f70→Cell500110 aan, schrijft integerfood op00534364 en zet EAX1 op00534366. Deze ABI/binding is eerder bewezen in `ANALYSE/BINAIR/candidate-food-h3-world-queries.txt`. Nulfood in de output verandert dat niet. De eigen guards200d68aa/b2 en200d695a/62 testen geen `<=0`: nul is toegestaan en kan naar food_success200d6968.

De bestaande rawgetter500110 bevat citybonus bij cityhandle, clamp van negatieve food en eventueel tijdelijke unitfood. De eigen reader sluit city/unitcontext en negatieve preclamps expliciet uit om geen onterechte nieuwe-stadcredit te geven. Het is dus onjuist alle huidige getterverschillen stilzwijgend als ongeschikte locatie te classificeren.

Nuttige extra aanwijzing binnen opgeslagen data: SCI0-werkplekindex10 is dezelfde externe `(28,73,0)`, met canonical `(28,45,0)`, H2-terrain7=JUNGLE, current_food0/flags0/spatial_reason2. Andere junglewerkplekken hebben food5/flags16. Dit ondersteunt een positiegebonden readerprobleem of ongedekte celcontext en geen algemene uitsluiting van jungle; de nul kan daar eveneens een niet-geschreven veld zijn. Geladen terrain.txt heeft voor gewone jungle basefood5/citybonus10 en is bytegelijk aan OG (SHAd1b8c038876d2a3a7abc963cc5e29c70ba29e449dfa6594709c452c0aa53b28f). Tekst bewijst geen actuele good/army-/flagscontext. Geen bezette-celguard als bewezen oorzaak presenteren; pass-time Cell+14/+10/unitcount ontbreken. De na afloop gelezen armyposities zijn niet de historische celtoestand tijdens deze query.

## Uitvoerbare overdracht naar B: één volledige diagnose

**Voorkeursroute: een afzonderlijke SCI-only kopie van de bestaande reader emitteren**, met identieke40byte-output, dezelfde20byte stdcall-argumenten/ret20 en dezelfde guards/uitkomsten. De gedeelde interne H3-reader, scoreadapter en developmentreader blijven bytegelijk. Bind uitsluitend `science_model`'s H3FoodReader-alias aan de nieuwe kopie. Factoryparameter voor labelnamespace/diagnostiek voorkomt dubbele `food_*`/environment_add-labels; standaardpad moet de oude bytes exact behouden. Dit zijn concrete bronpunten: `production-h3/components.py:reader/environment_add`, integratiebuilder `build_candidate.py` aliasbinding en readerdiagnostiekdecoder. Uitvoering maakt een nieuw eigen pakket; historische provenance niet muteren.

B kan in de vrije eigen Planheader **276..511** een maximaal236byte-record vastleggen. Reserveer stabiele branch-ID1..37 volgens bovenstaande tabel, schema/valid, owner/generation, SCIprefix/callkind en externe/interne positie. Registreer vóór elke oorspronkelijke bad-sprong de branch-ID, operands en een complete compacte foodberekeningscontext: flags/terrain/goodslot/gekozenrecord, cityhandle/unitcount waar bereikt, basefood/vijfaddends/som64, native_called/EAX/sentinel/output, bonus/centrumtotaal. Bewaar expliciete reached/validbits voor conditionele waarden; onbereikte nulvelden mogen geen meting heten. B moet layout exact passend toewijzen; als alle context niet binnen236bytes past, is bestaande eigen vrije scratch een aparte gebonden recordroute, geen foreign-objectuitbreiding.

De diagnose mag uitsluitend eigen geheugen schrijven tijdens de al gevalideerde SCIguard: scope1/guard1/owner+generation conform snapshot en passende callkind. Een diagnostiekcontextfout mag geen ongeldige eigen/foreign read veroorzaken of een oorspronkelijk UNKNOWN in succes veranderen. Gebruik bestaande gelezen registers/locals; geen extra native callbacks, nieuwe dereferenties of onbewezen unitinspectie alleen om een logveld te vullen. Bewaar EFLAGS/GPRs/x87 en resultaatbuffer/return exact, ook langs elke failure en bij onbereikte getter. `food_bad` moet nog steeds out40 wissen en EAX0 teruggeven. Geen negatief errorreturn gebruiken: de bestaande callers testen nul/nonzero.

Acceptatie vóór één volgende T0/n/T1: alle37 oorspronkelijke failure-ingangen hebben een unieke branch-ID/diagnosepad; guardwaarden en berekenings-/gettervelden zijn bij hun betreffende tak beschikbaar, caller-/stack/ret20/nonvolatile/x87 en shared-H3preservatie gecontroleerd. Relevante bestaande eigen-fixture-infrastructuur kan begrensde representatieve datacases leveren; geen nieuwe emulator of universele gamereconstructie. Laat de echte proef zowel het eerdere NOWvoorbeeld als de concrete eindige failure vastleggen; normale sluiting/herstel. Diagnose is UNKNOWN/geen selectiecredit. Het doel is één volgende waarneming met concrete guard en nodige waarden, geen vierde algemene meting die alleen reason11 herhaalt.

Daarna bepaalt de **waargenomen** guard de gameplayroute: bekende ontoelaatbare centrumcontext afzonderlijk negatief behandelen als dit bewijs toelaat; gettermismatch/coordinate/overflow als technische UNKNOWN onderzoeken/repareren; city/unitfood zo nodig via een bewezen afzonderlijke omgeving-/unitbijdrageroute ondersteunen. Nu geen blanket UNKNOWN-skip of behouden van eerdere Gcert na een contextfout voorstellen.

## Acceptatiestatus en stop

Bewezen: vierde fout ligt bij de gedeelde centrumreadgrens, niet bij rantsoenen of bewezen nulfood; volledige37-guardboom en uitvoerbare diagnostische B-route beschikbaar. Niet bewezen: welke interne guard de actuele cel triggert, welke interface-/scopeaanpassing gameplay verbetert, extra vraag of stichting. Root kan nu een onderbouwd voorstel maken; geen verdere A vereist vóór die diagnostische bronvoorbereiding. Budget19:31 vers vijf88/week86, geen grens. Deze rol stopt zonder achtergrondwerk; pcaan.
