# Settlerklasseprioriteit bij gelijke totale vraag

22 oktober 2026, 17:48 Europe/Amsterdam. Gerichte fase A voor Doel1/1a. Drie vragen: verandert de huidige adapter bij D=Dorig de prioriteiten, wat zegt T100 hierover, en wat is de kleinste volgende B-ingreep? Alleen bestaande bronnen/bewijs gelezen; geen game, build, nativeproef, RPM, observer of gameplaywijziging. Analyse afgerond; B kan kiezen.

**Ja: de adapter kan bij exact dezelfde totale vraag de volledige prioriteitsverdeling veranderen.** Hij verplaatst alle bijdragen naar de eerste effectieve klasse die type t kiest. Native code gebruikt zowel klasseprioriteit als het aantal binnen die klasse om prioriteiten te maken. De consumer gebruikt bij een klein tekort juist de lage entries. Dit maakt de adapter een concrete plausibele verklaring voor meer settlerproductie zonder meer gewenste voorraad; het T100-paar bewijst deze causaliteit niet.

## 1. Van oorspronkelijke klassevolgorde tot gebruikte prioriteit

Huidige bronbasis blijft kandidaat `df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e`, manifest `5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152`, pakket `PROEVEN/selectie-pad-diagnose/20261020T192500`. De actuele builder gebruikt `policy.emit` en `integration_base.quota`; de oude `integration_base.finalize` is niet de huidige finalizer. Gepinde bronnen en de originele DLLbindingscontrole zijn reeds in [vraag/rem-A](SETTLERVRAAG-REM-2026-10-22.md) vastgelegd. Machinecode hieronder komt uit bestaande dumps van originele robotcom.dll SHA3025070d…/imagebase20000000/timestamp37b894e7; geen nieuwe disassemblage of onpassende civctp.map gebruikt.

**Klassevolgorde is bestands-/containerindex, geen ingebouwde primary/core/overflowdispatch.** Loader2005edc0 leest `Build_List_Classes[%d].class_name` en `.priority` vanaf index0, schrijft klassepriority als double op record+0 en laadt de lijst bij hetzelfde indexnummer (2005ee85–eeeC); volgende record is +0x10 (2005eef7–ef02). Zie [bestaande loaderdump](BINAIR/aip-load-switch-and-parser.txt). Desired begint eveneens index0 en loopt AIP+7bc-records met stride16 af (20065a1a–a39 en20065c89–ca1); er is hier geen klassesortering vóór Choose.

Per lijst kiest Choose20065900 het laatste database-toegelaten type, met bijbehorende q; niet het eerste lijstitem (20065931–98c). Type−1 betekent geen keuze. Desired roept Choose op20065a4c aan. Na de native clamp/tekenbehandeling geldt voor de positieve hoeveelheid a: q<0→a=abs(q), anders a=q×max(1,C); aantalbijdrage n=ceil(a). De bestaande guards/clamps blijven gelden. Gewenst per type op AIP+7c0 wordt met n verhoogd (20065ab0–ac7).

Native Desired maakt **per klasse** precies n prioriteitsentries voor dat gekozen type:

```
p[0] = P
p[k] = P + k * P/(a-1), k=1..ceil(a)-1
```

P is klasse+0. Voor één entry wordt de deling niet uitgevoerd. Bij gehele n>1 loopt de reeks van P naar2P. De noemer is de ongeronde a−1, niet ceil(a)−1: positieve fractiequota kunnen dus een ander eindpunt geven. Bewijs: eerste entry20065aea–b00; verdere entries20065b02–b26; lus20065c5e–c81. De commentaartekst in default.aip over “first unit doubled” is slechts uitleg. Deze exacte formule volgt uit machinecode.

De entries van alle klassen die hetzelfde type kiezen worden samen **oplopend gesorteerd** ingevoegd in AIP+7c4[type], twee backingarrays+18/+20 (vergelijk/insert20065bdc–c5c). De lijst is dus niet simpelweg de klassevolgorde. Vervolgens berekent Supplemental20065cc0 K=max(0,desired−Actual), met no_settling-gate vóór bouwdoelen. Het gebruikt indexK−1 terug naar0 (20065d65–d7d, dca–dcb), niet de hoogste K entries uit de volledige D-lijst. De native code kent bestaande voorraad hiermee impliciet de hoge rangplaatsen toe. Dit is geen expliciete historische assignment van afzonderlijke units aan klassen.

De gekozen entry wordt constructorparameter van Goal_Build_Supplemental20049550 (call20065da8), opgeslagen als goal+48/+68; goalrawpriority is entry plus Planner+28 (20049590–598 en Compute_Raw_Priority20049b30–b48). Dit zijn daadwerkelijk gebruikte bouwdoelprioriteiten. Stadsbouwbaarheid, voedsel/bevolking, andere goals en queue-admission bepalen nog of zo'n doel wordt gebouwd. Zie [consumerdump](BINAIR/settler-aanvulling-prioriteit.txt) en [bouwdoeldump](BINAIR/settler-aanvulling-bouwdoel.txt).

**Huidige adapter:** `integration_base.py:89` roept originele Choose aan en controleert dezelfde effectieve preview/list/type/q-sequentie. Voor t retourneert hij `-double(D-W)` en zet written=D; alle latere t-klassen krijgen +0.0. Native desired én entries worden coherent opgebouwd, maar alle D entries krijgen de eerste t-klasse en haar nieuwe reeks. Ook een klasse die t kiest met oorspronkelijke q0 kan de eerste drager worden: er is geen test “eerste positieve bijdrage”. Niet-settlers blijven origineel. D=Dorig is geen bypassvoorwaarde. Dit is een eerder expliciet gekozen gedrag, geen pas ontdekte implementatiefout; het bleek wel méér dan alleen een aantalsverandering.

### Concreet bestandsvoorbeeld: default.aip

[Default](../CTP-proef/ctp_data/default/aidata/AIPs/default.aip:261) heeft Land_SettlerPrimary als eerste klasse (P10500), SettlerCore later (P3500), Overflow daarna (P1501). Hun UNIT_SETTLER-q zijn respectievelijk−2 opregel339,−1 op483 en−2 op817. Sea/spaceklassen kiezen andere types. Indien deze keuzes effectief zijn, is Dorig5:

| Bijdrage | Oorspronkelijk | Adapter bijD5 |
|---|---|---|
|Landprimary, q−2/P10500|2 entries:10500,21000|5 entries:10500,13125,15750,18375,21000|
|Core, q−1/P3500|1 entry:3500|0|
|Overflow, q−2/P1501|2 entries:1501,3002|0|
|Gesorteerde volledige t-lijst|1501,3002,3500,10500,21000|10500,13125,15750,18375,21000|
|NativeDesired / totale entries|5/5|5/5|

| Actual | Tekort K | Oorspronkelijke entries gebruikt, aflopend | Adapterentries gebruikt, aflopend |
|---|---|---|---|
|4|1|1501|10500|
|3|2|3002,1501|13125,10500|
|2|3|3500,3002,1501|15750,13125,10500|
|0|5|21000,10500,3500,3002,1501|21000,18375,15750,13125,10500|

Dus ook “de eerste primarypriority blijft10500” betekent niet dat de oorspronkelijke gemengde prioritering behouden blijft. De totaalcount blijft5 maar heraanvulling kan veel harder tegen gebouwen, wonders en transport bieden. Het gemeenschappelijke Planner+28-addend is in deze tabel weggelaten. Andere effectieve profielen geven andere P/a/volgorde; “eerste=primary” is alleen voor dit concrete bestandsvoorbeeld bewezen. masssettle bijvoorbeeld heeft andere corevraag en prioriteiten. Een nominale priority boven8000 garandeert geen werkelijke bouwactie.

## 2. Wat T100 wel en niet ondersteunt

[C3](UITBREIDING-T100-RESULTAAT-2026-10-22.md) en `PROEVEN/uitbreiding-lang-host/20261022/VERGELIJKING.json` bevestigen op één vaste start121 tegenover86 steden opT100, alle zeven hoger en7/7actieveTheocracy. Geen civ bereikt25/30/40 in de101 kandidaatsnapshots. Dit is het resultaat van het volledige configuratiepaar, inclusief de prioriteitsadapter, niet een isolatie van deze ingreep.

De geldige gedeelde laatste civ8-passes hebben desired=Dorig5; geen gedeelde pass toont D>Dorig. Dat sluit prioriteitsverandering bij gelijke voorraad niet uit: native code bewijst dat die verandering mogelijk is en de adapter voert die zonder D>Dorig uit. Andersom bewijzen scalarD5 en stedenwinst niet welke effectieve t-klasse/priorityarray op ieder meetmoment actief was of welk bouwdoel een stad koos. Er is in deze overdracht geen runtime-entryarray-/queue-driverbewijs toegevoegd.

Civ4 heeft werkelijk nativeDesired6 opT42(Actual3/tekort3) enT45(Actual5/tekort1). Zonder eigen gebonden Dorig/Gcert kan dat zowel verschillende oorspronkelijke bijdragen als aanvullende certificering betreffen; niet invullen. T46..63civ0/context0/reason35 en UNKNOWN_EXACT_TOKEN_TYPE blijven onbekend, geenD5. T100-civ8 Gcert0/R16/D5 bewijst opnieuw geen locatieafhankelijke rem. NativeActual is geen volledige voorraad-/queue-/missieteller. Bezitswinst bewijst geen uitsluitend nuttige eigen stichtingen en geen causaliteit van deze priorityverdeling. Geen nieuw onderzoek naar volledige causaliteit nodig om B te laten kiezen.

## 3. Kleinste onderbouwde B-keuze en uitvoeringroute

**B moet nu expliciet kiezen of de consolidatie van klasseprioriteiten gewenst is.** Een vast hoogquotum is daarvoor niet nodig. Er zijn twee kleine onderbouwde routes; geen code of bestand is hier aangepast.

1. **Prioriteit versterken via bestaande AIP-aansturing.** Een beperkte vergelijking kan dezelfde bestaande totale vraag herverdelen: bij het defaultvoorbeeld primary−5, core0, overflow0 geeft dezelfde vijf native prioriteitsentries als de huidige consolidatie, zonder hogere voorraad dan de oorspronkelijke5. Dit is een meetvariant voor prioriteit, geen nieuw eindbeleid. De gekozen effectieve AIP-klassen en overrides moeten dit werkelijk laden: alleen default.aip wijzigen garandeert geen gezamenlijke opening. B kan hiervoor de reeds bewezen FLI/AIP-load/overrideketen hergebruiken. Alleen P verhogen in core/overflow reproduceert de vijfpuntsreeks niet automatisch. Een pure AIP-variant vervangt bovendien niet de dynamische Gcertvraag, 30/40-uitvoergates, locatiegebonden rem of transportbeoordeling; behoud die grenzen in de gekozen integratie en noem het beperkte doel van de variant.
2. **Lokale adapter behouden maar gelijke vraag echt native laten prioriteren.** Kleinste isolerende correctie is een passconstante `D==Dorig`-bypass in de beheerde t-route: na bestaande preview/typechecks en vóór W/written-verwerking de originele q retourneren voor **alle** t-klassen van die pass. Native maakt dan oorspronkelijke counts én prioriteiten, terwijl policy/read_policy/execute/arrivalgates behouden blijven. Omdat iedere t-klasse dezelfde bypass volgt, hoeft de managed W/writtenketen daar niet half mee te draaien. Alleen bij D≠Dorig blijft de huidige consolidatie actief. Dit is een technisch concrete route op `integration_base.quota`/hook20065a4c, geen toegepast voorstel. Geen achteraf desired-/prioritywrites. Indien B ook bij D≠Dorig oorspronkelijke prioriteitsvorm wil behouden, moet B de verdeling van extra/afgeknepen entries expliciet kiezen; dat is een volgende ontwerpkeuze, geen ontbrekende broncodekennis.

Route2 is de kleinste wijziging om het verborgen priorityverschil in de huidige combinatie afzonderlijk te toetsen; route1 kan aantonen of bestaande AIP-aansturing voor het gewenste prioriteitsdeel volstaat. Geen van beide is al als beter gameplaybeleid bewezen. Niet tegelijk onbekende quota, packing, rolpredicates en klassegewichten veranderen.

Minimale B→C-meetlat: gelijk D=Dorig5 moet oorspronkelijke vijfentries teruggeven in route2; niet-settlers en geselecteerde types onveranderd; ontbrekende context origineel/UNKNOWN; native tekort-/entrycoherentie. Bij een expliciet gekozen D>Dorig-case moeten echte extraentries blijven bestaan; Rclamp en R0 mogen niet worden omzeild. Voor route1 dezelfde totalevraag en aantoonbaar effectief AIP/klassevolgorde vóór het prioriteitsverschil vergelijken. Daarna één begrensde gelijkeT0-vergelijking van alleen de gekozen factor, met settlerproductie/steden én concurrentie met schepen/defensie/ondersteunende gebouwen. Geen nieuwe observer als automatische voorwaarde; benut bestaande native-integratiecontroles en vastgelegde hostvelden, en label ontbrekende causaliteitsvelden.

Behoud huidige beleidsgrenzen: opening30, vervolg tot40 uitsluitend onder actueleTheocracy volgens read_policy; OTHER_GOV buiten dit beleid; bestaande voorraad/fronten worden éénmaal via nativeActual afgetrokken. De huidige onvolledige Gcert blijft ondergrens met Dorigfallback: UNKNOWNnietnul. Verhoogde prioriteit mag een nog ontbrekende transportoplossing niet als extra veilige directe bestemming tellen. Volledige rem/hervatting en volledige achterqueueafhandeling blijven de concrete gaten uit de eerdere vraag/rem-A; zij blokkeren deze kleine prioriteitskeuze niet.

| Beslisketen | Bewijs | A-acceptatie / resterend |
|---|---|---|
|Klassevolgorde→Choose|Loader2005edc0, Desired200659a0, huidige native.preview|Beantwoord; concrete effectieve per-passklasse blijft runtimegrens|
|Choose-q→priorityentries→consumer|20065aea–b26, bdC–c5c;20065d65–dcb;20049550/49b30|Beantwoord; gelijke D garandeert geen gelijke prioriteiten|
|Huidige adapter→gelijkeDverandering|integration_base.quota/previewchecks; D-W/rest0|Beantwoord; expliciete Bkeuze nodig, geen foutclaim|
|T100→hypothese|C3/VERGELIJKING, scalargrenzen|Plausibel, geen bewezen driver; geen volledige causaliteitsanalyse vereist|
|Volgende wijziging|AIP-redistributie of gelijkeD-bypass vóórW|B kan voorstel maken; niets toegepast/getest|

Alle drie vragen beantwoord. Doel1/1a en volledigeDoel5 blijvenOPEN; Doel3 is behouden. Werk gestopt na overdracht, geen eigen helper/run actief. Budgetstart17:45:12: verse vijfuur31/week41/stateok; pc blijft aan.
