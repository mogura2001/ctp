# Science C1: bereikbare foodreaderroute en C2-grens

15 oktober 2026, 15:19 Europe/Amsterdam. Gerichte fase A afgerond,2/2 beslisvragen beantwoord. Doel1/5 blijft science-locatieherkenning en nuttige uitbreiding/specialisatie volgens PROJECTDOELEN.md en het bestaande B-voorstel. Alleen de relevantie van één ontbrekende fixturecase is onderzocht; geen codewijziging, rebuild, helper/callback/game/procesread of nieuwe adresstrategie.

**Conclusie:** `isolated_SCI_center_above_int32` is niet bereikbaar via de echte huidige H3FoodReader. Deze onvoltooide synthetische domeinuitbreidingscase hoeft daarom de voorbereiding en beperkte technische C2-integratie van de ongewijzigde bereikbare readerroute niet te blokkeren. Zij blijft expliciet PENDING; de volledige30-casefixture krijgt geen PASS en C1 krijgt geen volledige native-/host-/gameplayacceptatie. Root/ontwerper moet deze bewijsgrens expliciet in de C2-overdracht opnemen.

## Vraag1: kan centrumfood2147483648 werkelijk worden doorgegeven?

Nee, bij de huidige kandidaat622c... en ongewijzigde reader. De onderbouwing betreft bron én werkelijk gelezen kandidaatbytes, geen alleen commentaar:

| Beslisketen | Concreet punt en controle | Gevolg |
| --- | --- | --- |
| Binding SCI→gedeelde reader | `build_candidate.py:64` bindt H3FoodReader aan de bestaande interne H3labels van U30–40. Kandidaatbytes bij SCI-centercall RVA0x13384c zijn `e8a42cfaff`, relatief doelRVA0xd64f5. Worker-callRVA0x13392c heeft hetzelfde doel. | Echte SCI-centercall gebruikt de gedeelde reader, niet de bijzondere callback. |
| H3-implementatie werkelijk behouden | Alleen-lezen kandidaatSHA256 `622cdd87c7b9480e9740ca5baaf37190ed632852358db0f80f6b6b936b13d6ba` gecontroleerd. ReaderRVA0xd64f5,1196bytes tot poscmp, exact gelijk aan de bestaande `H3-SCORE_CURRENT.manifest.json`-recipe tussen food_reader/poscmp, verplaatst naar interneH3RVA0xd6000. | De hieronder beschreven guard staat in deze kandidaat; geen aanname uit alleen een oude bronkopie. |
| Huidige food vóór bonus | `components.py:reader`: signed64 environmentberekening vereist high32=0 en low32 niet-negatief; gelijkheid met echte World+0xb8-getter verplicht. | Getterfood is alleen ondersteund binnen0..2147483647. |
| Centrum na CITY_BONUS | `components.py` centerbranch leest signed32bonus, telt signed64 op en controleert overflow, high32=0 en low32 niet-negatief. KandidaatRVA0xd6950 `81bddcffffff00000000` cmp high,0;0xd695a `0f851c000000` jne food_bad;0xd6960 `85c0` test eax,eax;0xd6962 `0f8814000000` js food_bad. Zonder bonus blijft dezelfde eerdere grens gelden. | Ondersteund totaalcentrum ligt eveneens in0..2147483647. GetterINT32MAX+bonus1 produceert high0/low80000000 en gaat naar food_bad. |
| Ongeldige readeruitkomst | food_badRVA0xd697c wist40outputbytes en retourneert EAX0. `science_model.py:107` test EAX direct na centercall en springt bij nul naar science_bad. | Er wordt geen2147483648 als geldig centrum naar SCI doorgelaten; geen NOW-credit uit deze input. |
| Afwijkende isolated fixture | `native-fixtures.cs:152–159` vervangt tijdelijk uitsluitend de eerste SCI-centercall met `fixture-large-center-reader.bin`. `prepare_native_fixtures.py:18–20` schrijft status1/getter2147483647/bonus1 zonder de echte readerguard uit te voeren. | Dit test SCI's ruimere interne signed64-rekencontract geïsoleerd. Het test geen bereikbare H3-readeracceptatie en creëert juist de input die deze reader afwijst. |

SCI's centrumveld en sommen blijven signed64. De correctie van SCI's highsigncontrole is geldig defensief gedrag, maar maakt het domein van de huidige H3FoodReader niet ruimer. Mocht een latere wijziging die readerguard verruimen, dan wordt deze nu onbereikbare grenscase wél een vereiste vóór credit op dat ruimere domein.

## Vraag2: wat blijft werkelijk voor C2 onzeker?

De bestaande29completecases uit attempt6 omvatten de bereikbare science-herkenning en bijbehorende ESP/nonvolatile/x87/canarycontroles, onder gecontroleerde callbacks/synthetische enginecontext. Zij omvatten onder meer earlyNOW zonder bergen, tech/placefalse bij huidige food, futurepositief zonder huidigecredit, PRESENT/MIXED, lokale versus gedeeldeUNKNOWN, duplicaten/centrumalias, halveconsumptie/nulmarge, callerprecision en maximaal20tiles. Dit is deelbewijs voor de beschreven route, geen algemene hostcertificering. Attempt8/9 leveren0nieuwecases; de laatste fixturepointercorrectie heeft nog geen geslaagde runtimecase opgeleverd.

| Vervolgbeslissing | Minimale echte onzekerheid / vereiste bewijs | Status |
| --- | --- | --- |
| C2-bronintegratie voorbereiden | ScienceNOW alleen uit geldige huidige reader/capacity/spatialcontext; gedeelde reader onveranderd; falende reader geeft geen credit. Geen afhankelijke domeinverruiming toestaan. | Onderbouwde vervolgstap; bijzondere centrum64case is hiervoor geen inhoudelijke blocker. |
| C2 gewijzigde beslissing accepteren | Eén centrum/tweerollen telt eenmaal;4sciencekeys versus5productionkeys; shared claims/Actual eenmaal; rolalternatief zonder voortijdig bronverbruik; juiste Gcert/D/tekort; allocator/reset/lifetime/serialcaller/bounds/cutoff en ABI aan nieuwe calls. | Nog ongemeten integratiepunten; eigen beperkte gewijzigde gevallen uit B-meetlat4–7 blijven vereist.29predicatecases bewijzen dit niet. |
| Werkelijke scienceherkenning claimen | Echte World+34/host/scratch/versiecontext, querykosten en serieel gedrag in de ondersteunde huidige wereld. | Open; fixtures gebruiken gecontroleerde callbacks. C2-offlinebeslissing sluit dit niet af. |
| Doel1/5 afronden | Echte scienceNOW-locatie zonder drie bergen draagt bij aan unieke certificering; waar vraagwinst geclaimd wordt Gcert>Dorig/D>Actual plus nuttig ingezette extra voorraad/stichting en voedselontwikkeling/groei. GelijkeT0/7normaleAI's/Deity, U30–40-hostactivatie en Doel3behoud blijven vereist. | Volledig open gameplaymeetlat volgens B; niets afgezwakt. |

De relevante onzekerheid verschuift daarmee van een kunstmatig verwijd readerdomein naar het werkelijk nieuwe C2-call-/claim-/levensduurcontract. Dat volgt uit de expliciet begrensde invoerroute en de bestaande B-volgorde, niet uit een wens om een groene test te verkrijgen. Geen onbekende runtime-uitkomst als PASS registreren. Geen nieuwe extremefixture/adresinfrastructuur nodig als voorwaarde voor C2-bronvoorbereiding; daadwerkelijke C2-nativebewijsvoering blijft een afzonderlijke uitvoeringsopdracht met eigen haalbare testprocedure.

Bronnen: `ONTWERP/SCIENCELOCATIES-U30-40.md:91–107`, `ANALYSE/REVIEW-SCIENCE-C1.md`, pakket `NATIVE-C1-OVERDRACHT.md` en `NATIVE-ATTEMPT9-RESULTAAT.md`; huidige bronnen/manifest/kandidaat hierboven. Bestaande rootreview behoudt statisch bron-/kandidaatbewijs, verleent op zichzelf nog geen union-/spelvrijgave. Analist levert hier de relevantiebeoordeling voor een expliciete B/C-overdracht.

Werk gestopt. Budget15:16:22Europe/Amsterdam: bron13:16:12UTC/leeftijd10,3s, vijfuur31%, week89%, stateok. Pc blijft aan; geen actieve run/planning door deze agent.
