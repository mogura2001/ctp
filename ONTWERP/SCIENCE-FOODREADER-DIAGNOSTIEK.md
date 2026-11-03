# Eén SCI-only FoodReader-diagnose met concrete guard en operands

19 oktober2026,19:39 Europe/Amsterdam. Gerichte fase B voor Doel1/1a (nuttige uitvoerbare uitbreiding) en Doel5 (science-locaties). Root heeft [A-overdracht](../ANALYSE/SCIENCE-CENTRUMVOEDSEL-11.md) geaccepteerd. Projectafspraken, [ketens/dekking](../ANALYSE/DEKKING.md), PROJECTDOELEN en LOCATIESELECTIE blijven gelden. Ownership: uitsluitend dit voorstelbestand, inclusief eigen voortgang. Geen implementatie of proef uitgevoerd.

## Oorzaak, huidige en gewenste beslissing

Diagnosehost2 met kandidaat `0ebafb11e08bc7dca74291dd8a8e9ea94441af09602ae2d94710217f19eabad9` bereikte de vierde SCI-centerread op externe `(28,73,0)`, prefix3, laatste civ8/generation7. De read retourneert0, waarna science reason11/coverage0 en pass reason23/Gcert0 volgen. Het nulveld is geen gemeten nulopbrengst: `food_bad` wist out40 voordat de huidige reader hem kan bewaren. De concrete interne guard is daardoor onbekend. A onderscheidt37 directe bad-branches en heeft rantsoen-/budgetfout als verklaring van deze waarneming uitgesloten. Een bestaande stad/eenheid of andere ongedekte context is mogelijk, maar niet bewezen.

Het eerdere voorbereide SCI0 heeft centrumfood15, foodkeys10/5/5, stand−1/R0,75 en marges35/30/25, zonder drie bergen; geen selectie of extra vraag. Gewenst is in **één volgende T0/n/T1-proef** zowel dit eerdere voorbeeld als de concrete laatste FoodReader-guard met de nodige waarden bewaren. De beslissing van reader/model blijft gelijk: niet-ondersteund retourneert0, out40 wordt gewist, geen UNKNOWNskip of extra positieve credit.

De bestaande FLI/AIP-/AAIP-route uit [architectuur](../ANALYSE/ARCHITECTUUR.md), [AAIP-lessen](../ANALYSE/AAIP-LESSEN.md) en het [integratievoorstel](U30-SCIENCE-FILTER-INTEGRATIE.md) ontsluit geen verdwenen interne FoodReader-operands. Aanvullende eigen diagnostische code is nodig; gegevensbeschikbaarheid is geen bewijs van een algemene modding-hook. Geen fuzzy-input, gewicht, SLIC, voedselregel of querybudget toevoegen.

## Kleine ingreep en bronownership

C maakt één **nieuw eigen pakket** onder `PROEVEN/science-foodreader-diagnostiek/` met eigen bronkopieën, kandidaat/manifest/BUILD-pins, eigen diagnostische reader en later `host1`. Historische `PROEVEN/production-h3/components.py`, alle62 bestaande BUILD-pins, parentpakket en diens historische readers/hosts blijven intact. Begin met exacte provenance van bovengenoemde kandidaat/manifest `9b518945a76cd0369a781de5b8f63be5fc7df963050cb04567a3fa6f6afa58ad`, engine `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79` en Doel3-release.

Gebruik een **eigen kopie/factoryadapter** van `production-h3/components.py:reader/environment_add` met expliciete namespace- en diagnoseparameter. Zonder diagnose moet de factory bij dezelfde plaatsing exact de oorspronkelijke readerbytes/labels/branches leveren. Het bestaande gedeelde H3-payload blijft via zijn oorspronkelijke gepinde bron samengesteld en bytegelijk, inclusief gedeelde FoodReader, classifier, scoreadapter, developmentreader en hun callbindings. Geen historische factory aanpassen om de kopie mogelijk te maken.

Emitteer daarnaast één clone met eigen namespace, bijvoorbeeld `sci_food_diag_*`, inclusief alle interne good-/environment-/failurelabels. Bind **alleen** `science_model`'s `H3FoodReader`-alias aan deze clone: centrum en primaire tiles. De afzonderlijke `science_development`-alias `food_reader` blijft op de originele gedeelde reader. Laat de science_model-bron, beslisvolgorde, guards, budgetcalls en uitkomsten intact; alleen zijn twee FoodReader-calltargetrel32's veranderen naar de clone. Default-H3 en overige modelbeslisinstructies moeten bytegelijk blijven waar RVA's gelijk blijven; onvermijdelijke adres-/rel32wijzigingen in de nieuwe compositie worden afzonderlijk verklaard. Geen extra nativecallback, foreign-objectuitbreiding of dereferentie voor logging.

De clone houdt `stdcall(World,pos,HostBinding,out40,isCenter)`, vijf32-bitargumenten, `ret20`, out40-layout en EAX0/1 exact aan. Vergroot uitsluitend zijn private stackframe voor een236-byte stagingrecord en noodzakelijke eigen spills. Publiceer failuredata vóór de oorspronkelijke `food_bad`-wipe; behoud wipe40/EAX0 en het oorspronkelijke epiloogpad. Bewaar per instrumentatiefragment EFLAGS/GPR's/stack en raak x87/controlword niet aan. Vooral ADD/ADC→JO, CMP/TEST→Jcc en native-returnEAX mogen niet door logging worden veranderd. PUSHFD/PUSHAD en tegengestelde herstelvolgorde zijn een mogelijke lokale techniek; C toont de werkelijke behoudsroute en correcte aangepaste framegrenzen.

## Exact diagnosecontract: Plan276..511,236bytes

Alle offsets hieronder zijn **decimaal Plan-relatief**, little-endian; einde512 is exclusief en CAPTURE begint512. Geen extra persistente scratch nodig. Een private stackstagingrecord krijgt dezelfde layout. Totale eigen state blijft0x79804=497668; het nieuwe stateRVA wordt uit de nieuwe compositie afgeleid en gepind, niet het oude0xe1000 overgenomen. Bestaande velden0..275 en alle arrays vanaf512 blijven disjunct/ongewijzigd.

| Offset(s) | Type/veld |
| --- | --- |
|276,280,284,288|u32 schema_version=1, valid(0/1), branch_id(1..37), callkind(1=SCI_CENTER,2=SCI_PRIMARY_TILE)|
|292,296,300,304|u32 owner, generation, prefix_index, primary_food_ordinal|
|308,312|u32 reached_lo/reached_hi:64-bit veldgeldigheid, geen synthetische meting uit nul|
|316..323,324..331|8bytes externe MapPoint, interne MapPoint; ruwe padding behouden|
|332,334|u16 geladen width,height; eigen reachedbit per dimensie|
|336,340,344,348|u32 Worldargument, laatst bereikte pointer_parent, pointer_offset, pointer_value|
|352,356,360,364|u32 Cell, cityhandle, armyarray; i32 unitcount|
|368,372,376,380|i32 gesigneerde terrainbyte, u32 TerrainDB, i32 geladen count, u32 recordarray|
|384,388,392|u32 mainrecord, werkelijk chosenrecord, cellflags|
|396,398|u16 raw_goodcode, werkelijk gekozen goodslot; levels volgen exact uit cellflags|
|400,404,408,412,416,420|i32 basefood en road/irrigation/mine/river/canal-addends|
|424,428..435,436..443|u32 huidige environmentpointer; i64 omgevingssom vóór/na de laatste bereikte additie|
|444,448,452,456|u32 native_called; i32 native_return_EAX, native_output_before(sentinel−1), native_output_after|
|460,464,468..475,476..483|u32 bonuspointer, i32 signedbonus, i64 centrumtotaal vóór/na bonus|
|484,488,492|u32 oorspronkelijke failure-EFLAGS, reeds geladen native-vtable, addend_stage(0=base,1..5=road..canal,6=bonus)|
|496,500,504,508|u32 out40pointer, HostBindingpointer, guard_operand_a, guard_operand_b|

Reachedbits hebben precies deze betekenis (hogere44..63 zijn gereserveerd0):0 metadata/schema/identiteit/callkind/prefix/ordinal;1 extern;2 intern;3 width;4 height;5 World;6 pointertriple;7 Cell;8 cityhandle;9 armyarray;10 unitcount;11 terrain;12 TerrainDB;13 count;14 recordarray;15 mainrecord;16 chosenrecord;17 cellflags;18 rawgood;19 chosengood;20 basefood;21..25 road..canal-addend;26 environmentpointer;27/28 som vóór/na;29 native_called;30 native_return;31 sentinelbefore;32 outputafter;33 bonuspointer;34 bonus;35/36 centrum vóór/na;37 failureflags;38 nativevtable;39 addendstage;40 outpointer;41 bindingpointer;42/43 guardoperands. Het record bevat dus elke benodigde operand óf expliciet ONBEREIKT, nooit een als meting gepresenteerde default.

Een logisch reeds geëvalueerde maar afwezige feature/environment mag addend0 met reachedbit krijgen, met flag/pointerbewijs; een nog niet bereikte feature niet. Bij basisinitialisatie krijgen somvóór/somna beide de werkelijk geïnitialiseerde signed64-base en stage0, expliciet zonder claim dat een optelling plaatsvond. Daarna bevatten zij het laatste werkelijk bereikte additiepaar; bonus gebruikt zijn afzonderlijke centrumpaar. Guardoperands zijn de twee concrete32-bitwaarden van de genomen guard: bij signed64-guards low/high en de volledige som elders; bij JO is originele overflowflag verplicht. Levels road/irrigation/mine en river/canalpresence worden uitsluitend volgens de bestaande bron uit de bewaarde flags gedecodeerd. Ruwe goodcode en fallbackslot worden apart gelogd; tekstuele GOOD_INDEX is geen lokale slotcode.

Per SCI-clonecall wordt alleen het private stagingrecord geïnitialiseerd. Leid callkind uit het bestaande isCenterargument af; prefix=`classified−1`, ordinal uit de bestaande primary_foodcounter. Activeer publicatie uitsluitend bij de eigen PIC-gebonden Plan, scope1/guard1, owner!=0, owner/generation gelijk aan de bestaande snapshot op0x78800/+4, generation>0, 0<=prefix<prefix_count<=64, SCI_calls==classified en passende SCI-callsite/callkind. C legt de twee gepinde callers vast. Dit gebruikt alleen eigen al geldige state, geen nieuwe enginepointerketen. Als diagnosebinding niet klopt: geen ongeldige writes/foreignreads en oorspronkelijke readerroute/onbekendresultaat behouden; geen succes fabriceren. Live reader accepteert geen record met ontbrekende/mismatchede binding.

Een **failurelatch** voorkomt verlies door latere lokale SCI-tilereads: zonder gelatchte centrumfailure mag iedere echte primaire tilefailure de vorige tilefailure vervangen. De eerste centrumfailure vervangt een eventuele tilefailure en wordt voor die owner/generation bewaard; latere successes of tiles overschrijven haar niet. Dit bewaart de relevante centrumfailure die de pass beëindigt, ook als hetzelfde vak eerder als tile faalde. Geen succesrecord nodig: het eerdere SCI0/NOWvoorbeeld blijft in de bestaande bounded ScienceResultdiagnostiek. START wist de volledige Plan, dus geen vorigepassrecord; owner/generation blijven afzonderlijke readerchecks. Bij publicatie valid eerst0, daarna payload, valid1 als laatste; uitsluitend complete failurepaden krijgen valid1. Staging hoeft geen nieuwe persistentieteller/allocator.

## Alle37 failure-ingangen in dezelfde kandidaat

IDvolgorde is vast volgens A en wordt in bron/manifest/decoder identiek vastgelegd. Onderstaande VA's zijn **parentprovenance bij base20000000**, geen hardgecodeerde nieuwe adressen; manifest koppelt elke ID aan de nieuwe emit-/guardlabels.

| ID | Parent-VA laatste4hex | Guard / concrete operands |
| --- | --- | --- |
|1|653c|interne z!=0; externe/interne xyz|
|2,3|6558,6574|unsigned x>=width / y>=height; exacte coördinaat/bound|
|4..8|6588,6596,65a4,65bd,65d6|null grid, grid+1c, laag0, x-kolom, Cell; parent/offset/value en bereikte xyz|
|9|65ec|cityhandle!=0; Cell/handle|
|10|660a|armyarray+30count!=0; array/count|
|11|661d|terrain unsigned>23; oorspronkelijke signedbyte/vergelijkoperand|
|12..14|6629,6635,6641|terrain13/18/23; terrain/vergelijkconstante|
|15..21|665d,6669,6675,6681,668d,6699,66a5|isCenter en terrain10/11/12/14/15/16/17; callkind/terrain/constante|
|22..24|66b9,66c5,66d3|TerrainDB null, index>=count, recordarray null; bereikte pointer/count/index|
|25|66fc|rawgood>4; flags/rawcode|
|26..30|67a2,67e5,6828,685f,6896|JO bij road/irrigation/mine/river/canal; flags/records/stage/envpointer/addend/som vóór/na/OF|
|31,32|68aa,68b2|pregetter high!=0 / low negatief; base/alle reeds geëvalueerde addends/som|
|33|68ef|World+b8 EAX0; called/EAX/sentinel/output/World/vtable/bindingspins|
|34|6901|getteroutput!=eigensom; beide waarden/flags/terrain/goodslots/records/addends|
|35|6944|JO bij CITY_BONUS; bonuspointer/bonus/getterfood/centrum vóór/na/OF|
|36,37|695a,6962|centrumhigh!=0 / low negatief; bonus-/gettersomwaarden|

Vang waarden **op hun oorspronkelijke lees-/berekeningsmoment**, vóór vernietiging of registerhergebruik. Neem geen extra memoryoperandread om een logveld later te vullen: voor bijvoorbeeld `cmp [Cell+14],0` of `[armyarray+30]` mag de clone de oorspronkelijke enkele load expliciteren, operand naar private staging kopiëren en dezelfde vergelijking uitvoeren, met exact register-/flagsherstel. Geen herlezen na null, geen unitinspectie. Parentpointer vastleggen vóór de oorspronkelijke dereferentie; pointer_value pas uit die oorspronkelijke load. Native-vtable is de reeds geladen ECX vóór de bestaande indirecte call, geen nieuwe slotdereferentie. De targetbody komt uit reeds verplichte loadedpins. Getteroutput alleen na de bestaande call uit de reeds aanwezige eigen local kopiëren; native_called0 is bereikt bewijs vóór de call, geen returndiagnose.

Alle guardbranches behouden hun oorspronkelijke predicate. Instrumenteer de genomen edge met unieke landinglabel, registreer originele EFLAGS en relevante operandwaarden, publiceer bounded, ga dan naar dezelfde `food_bad`-semantiek. Laat niet alle branches via één generieke marker met ontbrekende context lopen. Bewaar vóór iedere originele signed64-additie de som en gebruikte operand; leg na ADD/ADC de som en flags vast zonder JO te wijzigen. Een mathematisch onbereikbare JO blijft geregistreerd/bewijsbaar aanwezig; de echte T1 hoeft niet alle37 guards te triggeren.

## Poorten en beperkte verificatie

Volgorde: C-bronvoorbereiding/diff/layout/IDs → **rootbronreview** → afzonderlijke bouwvrijgave → doublecompose/PE/rel32/preservatie/readerpins → beperkte bestaande nativefixture-infra na rootvrijgave → **rootcandidate-/hostreview en gebruikersuitleg** → één host. Geen compile/native/install/start uit alleen dit B. Geen universeel framework of ongewijzigde oude suites herhalen.

De volgende controles zijn noodzakelijk voor de gewijzigde factor:

- Default factoryreader bij dezelfde plaatsing byte-identiek aan parent; hele oorspronkelijke H3-payload en developmentbinding behouden. Science_model-instructiediff verklaart alleen beide clonecalls/adresrelocatie, geen nieuwe beslisbranch. Alle37 oorspronkelijke bad-edges elk precies één unieke ID, geen ontbrekende/dubbele ID, geen labelbotsing.
- Exact236byte-layout/reachedbits, headerdisjunctie, state0x79804, private stackframegrenzen, zero-init/reset, publicatievalidlast, centrumfailureprioriteit en owner/generationbinding. Bounds weigeren ongeldige IDs/callkind/prefix/reachedreservedbits; geen buitenboundsread/write.
- Gebruik de bestaande finite caller-/stubfixture-infra voor de **uitgezonden clone**: failurelogpad van alle37 IDs met controle van bijbehorende operands/reachedbits en origineel out40/EAX0/ret20. Waar guardJO met normale int32-addends niet natuurlijk bereikbaar is, een expliciet synthetisch geïnjecteerde genomen edge met gecontroleerde prestate gebruiken: bewijs van log-/preservatiepad, geen bereikbaarheid in de game claimen. Overige guards gericht met de al bestaande datastubs laten nemen waar uitvoerbaar. Geen engine-/wereldsimulator bouwen om37 natuurlijke toestanden na te bootsen.
- Representatieve normale nulfood-/positievefood-/bonus-/goodfallbackroutes leveren exact dezelfde out40/EAX als de originele reader; nul blijft ondersteund. Controleer feature-absentie, pregetterfailure en native-gettermismatch, behoud sentinel en callbackaantal. ABIcheck omvat ESP/frame/canaries, stdcall20, nonvolatile en instrumentatie-GPR/EFLAGS en x87/controlword, ook bij vroege null/JO/nativefailure. Geen extra callbacks/derefs: emitted controlflow/foreign-loadinventaris plus stubcalltellers waar beschikbaar, niet alleen sourceclaims.
- Readerdecode op bounded eigen bytes: valid/reached/owner/generation en correcte guardoperands; rawhex bewaart ook ongeldige/halfgeschreven records als ongecertificeerde diagnose. Eerder prepared SCI0 en bestaande `selected_evidence` blijven gescheiden; reason23 levert geen selectedcredit. Pin alle gewijzigde en daadwerkelijk geïmporteerde sources/readers/build-/manifestdependencies; nieuwe loaded candidate/enginebindings volledig, nul onverklaarde binarywijzigingen.

Een niet uitvoerbare vereiste case gaat met concrete ontbrekende dekking naar root; geen verzonnen PASS of stilzwijgende scopeverlaging. De37logpaden hoeven geen37GUI-runs: dit ontwerp vraagt precies één echte T1. Historische testgetallen zijn provenance, geen acceptatie van de nieuwe clone.

## Eén vasteT0/n/T1-host en herstel

Na alle poorten één nieuwe `host1` met eigen gate, nieuwe candidatehash/manifest/readerpins en29verse daadwerkelijk gecontroleerde backups. Dezelfde `QUOTA-START-T0` SHA256 `8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26`, zeven normale AI's/Deity/passieve human, geen editor/gifts/workeractie. Root behandelt GUI volgens AUTOMATISERING en bestaande Bedien-CTP.ps1. Maximaal één vooraf verbruikt n-token; T0/T1 beide tweevoudig complete stabiele snapshots van dezelfde PID/creationtime/modules/owner/generation. Controleer zichtbare beurt en zeven AI-ronden−1→0; bestaande save-identiteit-/atomiciteitsgrenzen blijven expliciet.

Herbruik de bewezen **eindige startshellmonitor**: in dezelfde shell-exec als start absolute capturedoelen45/90/135/180s vanaf originele processtart, exact PID/creation/window, screenshot+echte tracetijden. Resterende Sleeps<=45s, execyield/recenteoutputpoll<=50s. Geen automatische menuklik/introskip/actiekeuze. Laatste historische frame<=195s door root visueel beoordelen; menu<=210s moet uit tijdige framewaarneming blijken, anders normaalstop. Monitor eindigt na laatsteframe/fout/eigenprocesweg, geen achtergrondtimer/framework. Geen klokreset. Werk/afwikkelbesluit uiterlijk600s, sluitverzoek vóór690s, einde720s.

Vóór pakket/start/token/observaties vers budget met afwikkelreserve, procescount0/cd/pins/aliaschecks; week<=25% waarschuwen, week<=10% of vijfuur<=5% projectstop/checkpoint, pcaan. Bij onbekende/verouderde limieten eerst bron oplossen volgens AGENT-CTP. Stop bij binding/context/focus/CD/modal/stabiliteit/beurtfout. Bij reason23 eerst de ene veilige complete diagnose uitlezen, daarna direct normaalclose; bij reason0 eveneens naT1 sluiten. Geen T5/T10, extra token of tweede proef zonder afzonderlijk B.

Archiveer alle bron-/candidate-/readerpins, beperkte cases, T0/T1/rawrecord/sciencevoorbeeld, scherm-/trace- en sluit-/herstelbewijs. Na normaalclose uitsluitend eigen PID en bevestigde exit/count0 alle29 beschermde bestanden/saves/profiel naar **verse voorafhashes** herstellen, inclusief Doel3release DLL `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890`. Nieuwe autosave eerst tweemaal bewaren (proefmap en herkenbare aparte gebruikerssave), oorspronkelijke defaultautosave herstellen; bestaande controle-/integratie-/diagnoseautosavearchieven behouden. Alleen eigen bytegelijke alias verwijderen; gate verbruikt/FALSE. Bestaande specifieke autosave-uitzondering en overige guards behouden. Bij mismatch geen gebruikerswijziging overschrijven; bij sluitfout geen forcekill/DLLherstel onder lopend proces, maar concrete open toestand/checkpoint melden. Reader-/candidate-rollback blijft eigen pakket naast behouden parent; geïnstalleerde Doel3releasehash is aparte herstelpoort. Pcaan, geen afsluiting/planning.

## Acceptatie, onzekerheid en exacte vervolgbeslissing

Technisch geaccepteerd: default/sharedpreservatie en37-IDmapping aantoonbaar, layout/ABI/gerichte logpaden gecontroleerd, nieuw package/pins/reader gebonden. **Hostdiagnose geaccepteerd** vraagt één stabiel en correct aan laatste SCI-centerfailure gekoppeld record met concrete ID1..37, owner/generation/prefix/callkind/externe positie en alle voor die guard vereiste reachedoperands, naast het eerdere sciencevoorbeeld; normale sluiting/herstel bewezen. Een record met alleen reason11 of branchID zonder vereiste waarden voldoet niet. Is het eerdere voorbeeld niet gereproduceerd, benoem dit afzonderlijk; een complete actuele failurediagnose blijft bruikbaar. Geen enkele diagnostische acceptatie sluit Doel1/1a/5 af.

Bij city/unit-/terrain-scopeguard: gerichte A met echte waarden naar de kleinste veilige afzonderlijke beoordeling van die centrumcontext; pas een later B bepaalt of een bewezen negatieve locatie-uitkomst mogelijk is. Bij coördinaat/null/range/overflow/gettermismatch: gerichte A naar precies de vastgelegde guard en operands, daarna afzonderlijke technische reparatie/scopeondersteuning. Bij nativeEAX0: exacte bestaande wrapper-/geladenbinding opnieuw gericht beoordelen met return/outputdata; geen nulfoodinterpretatie. Geen automatic UNKNOWNskip, budgetverruiming, behoud van eerdere Gcert na passfailure of clampcorrectie. Als geen complete toegeschreven failure verschijnt: ONVOLDOENDE_BEWIJS/NIET_GEREPRODUCEERD met exact ontbrekende velden; root bepaalt één gericht vervolg, geen automatische reeks markers/runs.

Verwacht effect is een beslisbare oorzaak in één T1, zonder veranderd gameplaybeleid. Risico's: instrumentatie kan register-/flags/stackfouten of extra looptijd introduceren; daarom genoemde preservatiepoorten en harde hostgrenzen. Het echte resultaat kan een ondersteunde-scopegrens tonen en hoeft geen enginebug te zijn. Alternatieven: dezelfde ongewijzigde binary opnieuw lezen kan gewiste operands niet terugbrengen; één algemene marker vereist herhaalproeven; de gedeelde reader instrumenteren raakt ook H3/development; generieke logging/extra liveinspectie voegt onnodige invloed toe. De SCI-onlyclone met volledig bounded failurecontext is de kleinste gerichte route. Een latere gameplayfix vereist eigen B en gelijke benchmark; combinatie met productie/science-union en behoud van Doel3 moeten dan afzonderlijk gemeten worden.

## Eigen voortgang

- **19 oktober2026,19:37 Europe/Amsterdam — gestart:** gerichte A gelezen,37guardroute en bronpunten gecontroleerd; uitsluitend eigen voorstelbestand. Budget19:37:41 vers vijf78%/week84%,2,6s oud, geen grens.
- **19 oktober2026,19:41 Europe/Amsterdam — ontwerp gereed:** exact236byte-schema/reachedbits/37IDs, SCI-onlyclone/factorynamespace, failurelatch vóór wipe, behouds- en beperkte fixturepoorten, één-T1-host en herstel uitgewerkt. Geen bron/binary/game/tests uitgevoerd. Doel1/1a/5: B gereed voor rootreview, technisch/gameplay open; Doel3 ongewijzigd. Volgende reviewbare oplevering is uitsluitend C-bronvoorbereiding in nieuw eigen pakket na rootuitleg/review. Geen onmisbare A-vraag vóór deze diagnostische route. Verse budgetcontrole19:40:58: vijf74%/week84%, bron2s oud, geen grens. Ontwerper draagt over en stopt; geen achtergrondwerk actief.
