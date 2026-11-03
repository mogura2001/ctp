# Settlervraag en locatieafhankelijke rem: gerichte A-overdracht

22 oktober 2026, 12:14 Europe/Amsterdam. Doel1/1a; uitsluitend drie blokkerende ontwerpvragen. Alleen bestaande bronnen en opgeslagen hostmetingen gelezen. Geen bouw, diagnostiek, native-uitvoering, RPM, spelstart of gameplaywijziging. Ownership uitsluitend dit document en VOORTGANG-VRAAG-REM-22.md. Analyse afgerond; volgende rol B.

**Uitkomst:** vraag5 is conform de huidige expliciete ondergrenspolicy, geen aangetoonde programmeerfout. Extra vraag boven5 is technisch mogelijk en wordt niet op het aantal bestaande settlers of steden afgeknepen. Een locatieafhankelijke verlaging onder Dorig vereist een betrouwbare bovengrens/dekkingsuitkomst die deze kandidaat uitdrukkelijk niet levert. Alleen `max(Dorig,Gcert)` verwijderen zou UNKNOWN ten onrechte als ruimtegebrek gebruiken.

## Bewijsbinding en actualiteit

De huidige kandidaat is `PROEVEN/selectie-pad-diagnose/20261020T192500/U30-40.prepared.dll`, SHA256 `df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e`; manifest `5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152`. Geen oude production-only B4-finalizer als actuele implementatie lezen. De builder roept `policy.emit` aan; deze gebruikt alleen wrappers/quota uit integration_base en `native.roles` delegeert aan `union.roles`.

De vijf hieronder gebruikte bronbestanden zijn tijdens deze analyse afzonderlijk hashgelijk aan de huidige manifestpins bevonden: policy.py `9fc8b418…`, native.py `cea06aac…`, integration_base.py `c1f336e3…`, union.py `e16dbfbc…`, build_candidate.py `b042c85e…`. Dit is een bestaande-bronbindingscontrole, geen nieuwe emissie of nativecontrole. De twee echte kandidaatarmen en hun herkomst staan in [bevestigingsresultaat](UITBREIDING-BEVESTIGING-2026-10-22.md) en `PROEVEN/science-duur-host/20261021/host3/VERGELIJKING.json`. Hun 25 tegenover20 steden zijn gemeten combinatiegedrag, geen bewijs van extra settleraanvraag of causale toeschrijving aan één instructie.

## 1. Huidige formule, consumer en waarom5 blijft

Voor het werkelijk geladen gewone UNIT_SETTLER-type t:

```
Dorig = som over alle effectieve klassen die t kiezen:
        q < 0 ? ceil(abs(q)) : ceil(q * max(1,C))
Gcert = aantal geselecteerde conflictvrije, volledig positief bewezen directe slots
D     = min(R, max(Dorig,Gcert))
nieuw native tekort = max(0,D-nativeActual[t])
```

`policy.original_demand` reconstrueert native clamp, teken, stadsmultiplier en geladen ceil-call uit volledige Choose-preview. Het telt niet alleen primary. Als bestandsfeit bevat default.aip voor t primary−2, core−1, overflow−2, samen5. masssettle heeft andere bijdragen. Dit bestandsvoorbeeld bewijst niet welk profiel in iedere gemeten pass effectief was; de gebonden laatste buffer bewijst rechtstreeks Dorig5. Alle zeven nativeDesired zijn gemeten steeds5.

`policy.read_policy` levert bij onvoltooide opening C<30 R=30−C; vanaf C≥30 onder actuele regering3 R=max(0,40−C); onvoltooide opening vanaf30 zonder actuele Theocracy R0. Completion1 plus Theocracy gebruikt40−C, ook na stadsverlies. Completion1 plus andere regering valt buiten deze policy en houdt native quota/vestiging. Daarom heeft civ8 opT26, C4/gov3/completion0, R26: actieve Theocracy vóór openingcompletion verhoogt het openingsbudget nog niet tot36. Geen wijziging van deze 30/40keuze nodig.

De quota-adapter op oorspronkelijke call20065a4c→Choose20065900 laat de originele selectie staan. Alleen de eerste klasse die t kiest retourneert `-double(D-W)`, latere t-bijdragen +0.0; W is de reeds werkelijk opgebouwde native desired, gecontroleerd tegen eigen written. Native Desired200659a0 maakt zowel aantallen als priorityentries. AIPUpdate20066b70 telt Actual op20066b7a, Desired op20066b81 en Supplemental op20066b88. Niet achteraf alleen de desired-double verhogen: de entries moeten overeenkomen.

NativeActual op AIP+7c8 is de enige native tekortaftrek. Het omvat native getelde armytypes (met eigen state17/18-uitsluiting) en één actuele frontunit per stad uit CityWhat2001cd50, category+1f4/type+1f0. Onderweg is al een bestaande unit. De producerclaims worden niet nogmaals afgetrokken. Armycacheaantallen of alle queuefronten zijn geen synoniem voor dit nativeActual; T26-civ4 toont bijvoorbeeld Actual3 tegenover vier waargenomen settlerfronten. De oorzaak van dat verschil is hier niet onderzocht en mag niet worden ingevuld. Achterliggende queueposities en missievrijheid blijven onbekend.

**Waarom5:** in de gedeelde civ8-passes is Gcert uitsluitend0,1 of2, steeds onder Dorig5 en R steeds boven5. De max behoudt dus5, ook bij Gcert0. Dat is de gekozen gedeeltelijke-certificeringspolicy. Gcert is een ondergrens; zelfs reason0, cutoff0 en een normaal beëindigde pass betekenen niet COMPLETE_G0.

**ConcreetT26:** de opgeslagen `PROEVEN/science-duurproef/20261022T114700/variant/T26.json` (SHA `ae46eaa6abc0a15fdfaffa6d763ba8a6ccf06392a63293a061dca18c62c8badf`) geeft civ8/generation182: candidates27, gate_queries27, gate_false27, known_count0, prefix_count0, classified0, slots0, Gcert0; departures6, pathqueries0, reason0, cutoff0, context1, R26, Dorig/desired5. Hier strandt de certificering vóór rol- en padbeoordeling: alle27 centra falen World+28. Dit is **geen aangetoond gebrek aan fysieke locaties**, geen vertrekbronnentekort en op deze pass geen reason42-fallback. World+28 is de bestaande lokale kaartkennisgate: wrapper00533580→004bbd50→004ebdf0 leest spelerkaartbit8000h met twee true-overrides. False betekent normale ontbrekende kaartkennis binnen dit contract; zie [kaartkennisfilter](../ONTWERP/U30-KAARTKENNISFILTER.md). Andere passes met reason42/23 zijn afzonderlijke fallback/onvolledigheid; niet op basis van hun nulbuffer aan T26 gelijkstellen.

## 2. Is extra vraag structureel onmogelijk door voorraad of steden?

**Nee.** `native.read_departure` en `native.selection` bewijzen vier soorten vertrekrecords:

| Kind | Herkomst | Matching |
|---|---|---|
|1|Gewone huidige single-settlerarmy, beperkte state/movement/cargo-branch en actuele positie|Eenmaal, via record+16 used-marker|
|2|Eigen huidige stad zonder t-front, CanBuild(t)=1|Herbruikbaar als nieuwbouworigin|
|3|Eigen huidige stad mét t-front, CanBuild(t)=1|Frontclaim eenmaal; daarna ook herbruikbaar nieuwbouworigin|
|4|Eigen huidige stad mét t-front, CanBuild(t)=0|Alleen frontclaim eenmaal|

Selectie probeert per slot existing→front→newbuild. Bij newbuild accepteert zij kind2/3 en gaat `select_add` via `select_buildorigin` langs de used-store heen. Ook als kind3 al een frontslot draagt, blokkeert record+16 deze newbuildtak niet. Eén bouwbare stad kan dus meer dan één toekomstig slot certificeren. Dat zegt niets over gelijktijdige queuecapaciteit of voltooiingstijd. Er is geen regel `Gcert <= settlers+fronten`, `Gcert <= steden` of `Gcert <= departures`. Geen nieuw mechanisme nodig om een stad vaker als toekomstig origin te mogen gebruiken.

Voorwaarde: diezelfde stad moet voor ieder slot een volledig positief veilig direct pad onderbouwen, en de slots mogen onderling niet conflicteren. Zonder enig kind2/3 is de geselecteerde voorraad wél begrensd door de bruikbare eenmalige kind1/3/4claims. Zonder enig positief vertrekpad ontstaat geen certificaat. Dit zijn echte eligibilityvoorwaarden, geen bewijs dat de huidige T26-nul daar ontstaat.

De werkelijke limieten zijn CAPTURE4096, bekende canonieke prefix64, rol/werkplekconflicten, selectedcap40, R, vertrekrecords32, padqueries128 en totaal4096padpunten; iedere query/search/pad heeft eigen4096grens. Finalize leest eigen stadsset eerst, leger-set daarna. Citytelling wordt ook bij niet-eligible steden bijgehouden; cap32 geldt voor toegevoegde vertrekrecords. Veel eligible steden kunnen daardoor armyrecords uit de technische bronprefix drukken; dit verhindert hergebruik van de opgenomen bouworigins niet, maar beperkt dekking. Sourceoverflow/cutoff is geen lege wereld.

Een verdere concrete beperking zit in `source_path`: cached_path0 gaat onmiddellijk naar select_bad/reason25 en final_fallback/Gcert0, voordat latere bronnen of nieuwbouwprioriteit worden geprobeerd. Return2 slaat alleen de bron over; return3 bewaart een bewezen selectieprefix wegens budget. Return0 bundelt momenteel nativequery-/context-/canary-/endpoint-/safetyonzekerheden. Zonder onderscheid daarvan mag B niet simpel alle nullen overslaan of als onbereikbaar tellen. Geen bewijs dat deze tak hetT26-resultaat veroorzaakte: T26 deed nul padqueries.

De opgeslagenT2-selectie bewijst twee verschillende toegewezen source-ID's bij departures2 en Gcert2; zij bewijst géén hergebruik van één bouworigin voor meerdere slots. Dat hergebruik is hier bron-/emitterbewijs. De vroegere native G6/Actual2-fixture bewijst technische quota-integratie, geen zes echte hostbestemmingen. In de huidige hostarmen is extra vraag boven Dorig niet aangetoond.

## 3. Kleinste uitvoerbare route en werkelijk blokkerende voorwaarden

**Extra vraag:** behoud de bestaande quota-adapter, Actualaftrek, herbruikbare bouworigins en 30/40gates. Het huidige pad kan al `Gcert>Dorig` leveren; vanaf zes bewezen slots bij Dorig5 en R≥6 wordt D≥6. Er hoeft geen vast quotum te worden gekozen of stad-/unitcountlimiet verwijderd. De eerstvolgende positieve acceptatie moet een echte gebonden pass tonen met Gcert>Dorig, coherent nativeDesired/entries en D>Actual, gevolgd door bruikbare productie/inzet. Alleen meer steden in de bestaande combinatie voldoet daar niet aan. Huidige data bewijzen niet dat er op deze start zes veilige, conflictvrije bekende NOW-slots beschikbaar zijn. Een cap verhogen of standaardvraag verhogen levert dat bewijs niet.

**Rem/hervatting:** de kleinste inhoudelijk geldige uitbreiding ligt in de huidige producer/finalizer, niet in een extra FLI-quotum of SLIC-planner. Maak naast positieve ondergrens een expliciete dekkingsuitkomst voor de **voor deze beslissing relevante** directe nuttige bestemmingen. Alleen bij betrouwbare complete dekking mag B een actuele voorraad D=min(R,Gcomplete) formuleren; nativeActual remt vervolgens vanzelf nieuw tekort wanneer bestaande/frontunits die vraag al dekken. Bij onvolledige rol-/kaart-/bron-/paddekking blijft de huidige Dorigfallback binnen R; UNKNOWN blijft onbekend. Herbeoordeling volgt elke nieuwe START/generation, zodat nieuwe kennis, veiligheid of bereikbaarheid de vraag kan hervatten. Geen persistente pauzelatch nodig.

Dit vereist geen algemene gamereconstructie. Wel zijn de volgende gerichte gaten voor een **daadwerkelijke volledige remclaim** onvermijdelijk:

1. Een betrouwbare bovengrens/dekkingscontract ontbreekt in de huidige uitvoer. Canonieke prefix64, World+28false, onvolledige rolunion (o.a. monopoly), beperkte native masks/packing en nativequery0 zijn geen negatieve ruimtebewijzen. B kan alleen een beperkte complete scope ontwerpen als zij de overige kansen uitdrukkelijk UNKNOWN houdt; een globale COMPLETE_G0 komt niet uit dit pakket. Voor de volgende ingreep eerst precies kiezen welke produceruitkomst voldoende complete dekking kan bewijzen, met bestaande gegevens en zonder extra strategie te verzinnen.
2. Transport is nu niet gecertificeerd. Een directe query die geen positief pad levert onderscheidt geen eilandtekort, gevaar, zoekcutoff of toekomstige transportbehoefte. Geen transportloze nul gebruiken. B kan behoudend UNKNOWN/transportuitgesteld blijven rapporteren; een volledige transportafhankelijke rem/hervatclaim vraagt afzonderlijk het concrete transportbewijs, geen volledige marinearchitectuur vooraf.
3. Voor **nieuwe native tekorten op basis van bestaande units/fronten** is de adapter uitvoerbaar. Voor voorkomen van ophoping met **alle bestaande queueposities en al uitgegeven requests** ontbreekt hier een complete telling/admissionbinding. NativeActual en CityWhat tellen niet aantoonbaar de hele queue; D verlagen annuleert reeds ingediende requests niet. Als B die bredere acceptatie verlangt, is de enige noodzakelijke technische terugvraag: exacte huidige settlerqueue-/pendingrequestteller of actuele request→queue-admissionpoort, met unieke identiteit en hercontrole vóór toevoeging. Geen ongerichte queue-/save-/ABI-analyse. Extra achterliggende queuecredit niet dubbel van nativeActual aftrekken; bij uitbreiding van de aftrek moet die credit expliciet disjunct zijn. Geen bestaande queue blind verwijderen.

Een gerichte optimalisatie van pad-UNKNOWN kan later meer positieve ondergrens leveren: onderscheid een lokaal onbeantwoord bron-bestemmingspaar van onbetrouwbare passcontext vóór elders verderzoeken. Dit is geen voorwaarde om het huidige mechanisme van extra vraag te begrijpen en geen automatische nieuwe opdracht. De bestaande diagnosebuffer is uitdrukkelijk geen beleidsinput.

## Dekkingsmatrix en overdracht

| Beslisketen | Huidige werking en ingreeppunt | Bewijssoort | A-status / acceptatielacune |
|---|---|---|---|
|Quota→vraag→tekort|policy.original_demand/finalize; integration_base.quota; native200655f0/659a0/66b70|Bestaande machinecode + gepinde emitterbron + native/hostwaarden|Vraag1 beantwoord; geen extra aanvraaghostbewijs|
|Kandidaten→kennis→rollen|policy.canonical_prefix→union.roles; World+28; current science/productionalternatieven|Gepinde bron + bestaande querybinding + T26 opgeslagen data|Vraag1 beantwoord; nul is ondergrens, niet fysieke nulruimte|
|Voorraad/front/bouworigin→Gcert|native.departures/selection; CityWhat2001cd50/CanBuild2001f330; current armycontract|Gepinde emitterbron, oorspronkelijke bindingsanalyse|Vraag2 beantwoord; originhergebruik aanwezig, echte hergebruikhostcase niet gemeten|
|Veilig pad→certificaat|native.path/path_cache/source_path; own/−1-owner, threat0, directland, budgets|Gepinde bron en eerdere machinecodebinding|Geen nieuwe safetykeuze; lokaalUNKNOWN versus context niet scheidbaar uit huidige return0|
|Vraagrem→hervatting|final_combine/START; huidige formule houdt Dorigfloor|Gepinde bron + T1..26waarden|Vraag3 route bepaald; complete relevante dekking ontbreekt voor verlaging|
|Voorraad+alle queues→geen ophoping|nativeActual telt units/front; oude requests blijven mogelijk|Machinecodebinding + expliciete huidige bewijsgrens|Volledige queue/admissionacceptatie open; specifieke terugvraag alleen indien B dit meeneemt|
|Opening30/vervolg40|read_policy + execute/arrivalgates|Gepinde bron + eerdere nativegrenschecks|Behoud bestaande keuze; natuurlijke30/40-runtimecase niet geobserveerd|

Actuele eigen functielocaties volgens huidige manifestlabels, RVA (basis20000000 alleen preferred, runtime herbaseren): read_policy0xda4fa; original_demand0xda720; canonical_prefix0xda87b; finalize_pass0xdaacf; quota_hook0xdb08d; read_departure0xdbb69; location_roles0xe3ee4; select_direct_plans0xe4eec. Dit zijn bestaande emitter-/manifestlocaties, geen nieuwe onafhankelijke disassemblageclaim. Oorspronkelijke Robotcom-map past; civctp.map wordt niet gebruikt. Oorspronkelijke bronbindingsdetails blijven in [type/vertrekclaims](TYPE-EN-VERTREKCLAIMS-B4.md), [uitbreidingsanalyse](UITBREIDING-30-40.md) en [30/40-ontwerp](../ONTWERP/UITBREIDING-30-40.md).

Alle drie gestelde vragen zijn beantwoord. Ontwerper kan een begrensd voorstel maken met huidige positieve extra-vraagroute en expliciete complete-dekking-/queuevoorwaarden voor remmen. Er is geen grond voor nog een brede analyse of een vastequota20-ingreep. Doel1/1a blijven OPEN; Doel3-behoud is bevestigd door de twee kandidaatarmen; volledigeDoel5 blijft OPEN. Analysewerk gestopt na overdracht; pc blijft aan.
