# U30: gerichte verklaring laatste pass reason44

15 oktober 2026, 14:43 Europe/Amsterdam. **Fase A gereed voor B; geen gameplayherstel bewezen.** Doel1/1a: nuttige uitbreiding naar30, daarna tot40 onder Theocracy. Vraag: verklaar C10/civ8/generation7/status5/reason44 vóór een lange uitbreidingstest. Ownership alleen dit rapport en VOORTGANG-REASON44.md. Geen spelstart, procesread, fixturecall, build, bron-/gameplay-/binarywijziging uitgevoerd.

**Uitkomst:** de huidige waarneming onderscheidt vier falende helpercalls niet. Een concrete fout in de foutregistratie is wel bewezen: `final_bad` overschrijft hun bestaande codes met44. Een concrete fout in de gameplayberekening/hostbinding is uit deze gegevens niet aangetoond. Nul steden is geen directe foutvoorwaarde en bewijst dus evenmin een natuurlijke verklaring. De minimale volgende ingreep is bestaande foutcodes behouden, met één begrensde activatiepass; geen nieuw observerframework of lange benchmark nodig om dit onderscheid te maken.

Bewijslabels: **F** bestandsfeit; **M** machinecode; **R** bestaande runtimewaarneming; **A** afleiding. Basis: [huidige uitbreidinganalyse](UITBREIDING-30-40.md), [review](REVIEW-UITBREIDING-30-40.md), [bestaande B](../ONTWERP/UITBREIDING-30-40.md). Brede A blijft afgesloten; AAIP levert hier geen runtimebewijs.

## 1. Vaststaand bewijs en grenzen

- **R:** [T0](../PROEVEN/uitbreiding-30-40/20261012T181500/c10/variant/T0-direct.json) heeft generation0 en lege eigen buffer. [T1](../PROEVEN/uitbreiding-30-40/20261012T181500/c10/variant/T1-direct.json) heeft generation7/civ8, policy1/remaining30/government1/engine_count0, context0/Dorig0/Gcert0/desired0/reason44. Scope0/owner0/status5 zijn de onvoorwaardelijke afsluitwrites van `scope_hook`, geen bewijs van geslaagde finalisatie. De buffer geldt uitsluitend voor de laatste pass, niet voor alle zeven AI's.
- **F/M:** [policy.py](../PROEVEN/uitbreiding-30-40/20261012T181500/policy.py) `finalize_pass` schrijft policyvelden pas na succesvolle `read_policy`. Na alle vier helpers schrijft hij context1; de latere selectie/fallback kan dit niet terugzetten. `unknown` schrijft alleen status0/reason/EAX0. De directe fout ligt daarom vóór context1.
- **R:** civ8 heeft native type4 met displaynaam Settler, settlercategorie true/water-spacebits0, native desired5/Actual2/tekort3 en twee eenheden type4. De eigen desired0/Dorig0 bewijst dus geen native nulvraag. De exacte `UNIT_SETTLER`-tokenidentiteit blijft ongecertificeerd: de reader leest t/types alleen bij context1. `UNKNOWN_EXACT_TOKEN_TYPE` bewijst niet dat `resolve_type` zelf faalde.
- **A:** deze gevolgtrekking veronderstelt de normale enkele Desired-call per AIPUpdate. De bestaande caller toont die volgorde; er is geen bewijs voor herintreding of een extra schrijver. De snapshots zijn tweemaal stabiel, geen atomaire opname van alle beslismomenten.

## 2. Dekkingsmatrix beslisketen

| Schakel | Huidige werking / ingreeppunt | C10-conclusie |
| --- | --- | --- |
| Startschoonmaak en scope | `integration_base.py` start_hook wist eigen Plan; scope_hook zet scope1 vóór AIPUpdate | Generatie7 is bereikt; oorspronkelijke legeT0-waarden zijn vervangen |
| Scopeguard + read_policy | `policy.py` eerste twee final_bad-routes; read_policy leest echte C, regering en B2-latch | Uitgesloten als bron van deze44: positieve policyvelden volgen alleen na geslaagde read_policy |
| Buiten beleid | policy0→status6/reason43 | Uitgesloten: policy1 |
| bind_host | `integration_base.py:host`; AiMain+94/+80/+38/+2c/+30/+34, civ, Planner+AIP/owner/scheduler, H3Host, interfaces/slots, bind_inputs | **Mogelijk**, bestaande interne reason30; bind_inputs36 wordt nog eens door bind_bad naar30 overschreven |
| resolve_type | `native.py:resolve_type`; StringDB tokenlookup, UnitDB name→index/count, ordinary-settlerflags | **Mogelijk**, bestaande reason10; geen t/types in opgeslagen C10-read |
| preview_scope | `native.py:preview`; AIP+7b0/+7bc, effectieve klassepointer/type/quotum, begrensde selectie | **Mogelijk**, bestaande reason11; geen klassen/preview in opgeslagen C10-read |
| original_demand | `policy.py:original_demand`; geselecteerde klassen, native clamp/sign/ceil, signed32-som | **Mogelijk**, bestaande reason40; Dorig0 betekent onafgemaakt/ongecertificeerd, niet bewezen natuurlijke nul |
| Productiepredicate, city/armysets, routes en matching | Pas na context1; canonical_prefix/production_roles/read_set/select_direct_plans | Uitgesloten als oorzaak van44; hun fallback behoudt context1 en gebruikt42 of eigen reden |
| Budget/stichting30–40 en Doel3 | Andere adapters en ongewijzigde B2N30; deze pass C0/gov1 | Geen40-grensgeval; geen nieuw bewijs voor uitbreidingseffect of combinatiebehoud |

## 3. Machinecode en vaste bindings: gerichte twijfel opgelost

**M/F:** offline gelezen kandidaat SHA256 `f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810`. De actuele policy/integration_base/native/build_candidate/input-pins hebben exact de vijf manifestpins. `prepare.py` is een auditbron, geen emitterdependency in dit manifest. Geen rebuild uitgevoerd.

Gerichte decode van de echte kandidaat bevestigt: finalize RVAda613; read_policy-call **200da642**; bind_host **200da6a8→200d9000**; resolve_type **200da6b6→200dafb3**; preview_scope **200da6c4→200db2e7**; original_demand **200da6d2→200da324**; overschrijven reason44 **200da834**. Dit koppelt de bronconclusie aan de werkelijk geteste kandidaat, niet alleen aan functienamen.

De15 bevroren inputbodies zijn bytegelijk aan de betreffende kandidaat/enginebytes; alle zes UnitDB-slots kloppen. Ook de drie extra bind_host-slots zijn juist: engine vtableRVA3452e0+54→533880,344660+c→5273a0,346220+c→5826a0. Hiermee is een vaste preimage-/slottypefout niet aangetoond; dynamische objectidentiteit wordt hiermee niet gemeten. AI-relocaties worden in bind_inputs module-relative vergeleken.

Robotcom PE timestamp37b894e7/base20000000 past bij de eerder gevalideerde Robotcom.map. De betrokken oorspronkelijke bodies zijn behouden. Engine timestamp37d6f702/base400000/hashb1b5256f...; **geen civctp.map gebruikt**. Bewijs hergebruikt: [native Desired](../PROEVEN/uitbreiding-30-40/20261012T181500/scheduler-result-binding.txt), [movementcaller](BINAIR/build-goals-queue-ai-legacy-and-unit.txt), [UnitDB](BINAIR/b4-typeddepartures-unitdb-interface.txt), [tokenlookup](BINAIR/b4-typeddepartures-name-and-category.txt), [H3-hostbron](../PROEVEN/production-h3/host-validator.py).

**M:** native Desired200659e8–20065a0e leest de citysetcount en maakt er minimaal1 van. **F:** original_demand doet hetzelfde met engine_count; geen test C>0 in de vier helpers. Ontbrekende steden kunnen later geen bouworigins opleveren, maar die keten ligt na context1. Een nulstad kan alleen indirect samengaan met een ontbrekende/ongeldige dynamische invoer; die specifieke invoer is niet opgeslagen. De eerdere geslaagde read_policy valideert B2Host en H3Host al; zonder tussentijdse mutatie zijn hun identieke vaste hostchecks als latere oorzaak onwaarschijnlijk. Dit sluit de aanvullende bind_host-owner/interfacechecks niet uit.

## 4. Minimale overdracht aan ctp_ontwerper

**Direct ontwerpbaar:** behoud de vier reeds bestaande helperfoutcodes bij mislukte helperreturn. Maak de twee vroege scope/read_policy-guardroutes herkenbaar als44 (of afzonderlijke bestaande reasonwaarden). Laat een helperfailure vanuit finalize naar de gewone epiloog gaan met zijn status0/EAX0/reason intact, in plaats van `unknown(44)` opnieuw uit te voeren. Laat in bind_host een bind_inputs-failure zijn36 behouden in plaats van die door30 te vervangen. Dit verandert geen fallback-, quota-, cap- of savebeleid en past in de bestaande reader, die reason al vastlegt. Hier is uitsluitend de route beschreven; geen code toegepast.

**Voldoende eerstvolgende meetlat:** één normale pass met dezelfde T0 en gepinde kandidaat, vervolgens dezelfde bestaande reader. Uitkomst10/11/30/36/40 wijst de nog ontbrekende helper aan; context1 betekent dat deze vier checks zijn gepasseerd. Als de helpercode30 of10/11 nog meerdere voorwaarden omvat, vervolg uitsluitend met een onderscheiden leafcode in die ene functie of de concrete door dat resultaat aangewezen bestaande invoer. Geen volledige hostreconstructie vooraf. Eerdere capture-redenen mogen niet als finale fout worden gebruikt: bij return0 zet ieder van deze helpers zelf zijn eigen foutcode; behoud uitsluitend die daadwerkelijke callfailure. Een succesvolle helper mag een oudere capturewaarschuwing laten staan.

**Geen aangetoonde gedragsreparatie:** ontbreekt nog welke dynamische guard daadwerkelijk false was. Een foutieve guard verwijderen, zero-city overslaan of quota verhogen is daardoor ongefundeerd. Zelfde44 kan nu verschillende oorzaken verhullen; langere GUI-proeven lossen dat niet betrouwbaar op. B moet de begrensde foutregistratiecorrectie en technisch passende controle/rollback uitwerken; C voert pas daarna uit. Bestaande fixturestubsuccess bewijst geen echte hostbinding. Gameplayacceptatie voor Doel1/1a blijft open, Doel3-releasebewijs blijft de eerdere aparte meting.

**Acceptatiestatus:** vragen1 en3 beantwoord; vraag2 eindig beantwoord als: concrete overschrijffout bewezen, concrete gameplay-/bindingsfout niet identificeerbaar uit het huidige bewijs. Dat blokkeert een gedragsfix, maar niet het bovenstaande minimale B-voorstel. Overgedragen, analyse gestopt. Niet-blokkerend: uitslag van overige zes passes en science-/monopoly-/transportdekking; geen heropening van die analyses.
