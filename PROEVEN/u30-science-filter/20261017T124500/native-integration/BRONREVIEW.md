# Gerichte native-integratie: broncheckpoint, geen native-uitvoering

17 oktober 2026, Europe/Amsterdam. Alleen deze nieuwe submap en het toegewezen voortgangsbestand zijn gewijzigd. Kandidaat/bronnen/manifest blijven intact. `INPUT-CHECKPOINT.json` bevestigt de62 BUILD-PINS inclusief kandidaat0ebafb11…/manifest9b518945…. De18 reeds geslaagde own-byte-readergevallen zijn niet herhaald.

`NativeCaller.cs` hergebruikt de finite VirtualAlloc/VirtualProtect/VirtualFree- en shim1–3-infrastructuur van de kaartfiltercaller. Geen vaste allocatieadressen, LoadLibrary, engineproces, RPM of spelbediening. De oorspronkelijke `.u40c` wordt naar eigen geheugen gekopieerd; Plan is exact eigen image+label `pass_state`/e1000, generation direct na0x79800. Geen externe Plan die de echte PIC-countercontext zou omzeilen. Kandidatenlabel-RVA's zijn gelezen, geen installatieadressen voorgeschreven. Alle allocaties vallen onder finally/VirtualFree en gecontroleerde cleanup.

De rode16bytes vóór Plan liggen in ongebruikte sectionpadding: zij worden vóór RX gezet en daarna alleen gelezen. De16bytes na Plan zijn eigen bufferstaart; de eerste DWORD is in deze directe fixture de generationgrenscanary. ORDER heeft eigen grenscanaries. Iedere directe call controleert ESP, EBX/ESI/EDI/EBP en exact de bestaande x87-state inclusief controlword. Geen guard bewijst volledige memory safety.

## Geplande eindige cases

| Criterium | Concrete native broncase na vrijgave | Bewijsgrens |
| --- | --- | --- |
| B4 dubbele rol | Eén werkelijk `location_roles`-centrum produceert twee ALTrecords en één slot, productie5keys/science4keys | H3 en SCI zijn expliciete inputstubs |
| B4 keys | Echte vijfde productiekey tegen vierde sciencekey; disjunctie; overlap uitsluitend buiten mandatorykeys; vier unieke keys/duplicaat | Echte `plan_conflict`/`validate_alternative` |
| B4 alternatieve selectie | Tweede productiecentrum deelt alleen een productiewerker met eerste; conflictvrije science behoudt zijn eigen centrum. Afwijzende science deelt echte key14; tweede existingclaim blijft−1 | Echte `select_direct_plans`/choose; endpoint/pad zijn true-stubs |
| B5 bronclaims | Ordinary existing eenmaal; front kind4 eenmaal; nieuwbouw kind2 voor beide slots herbruikbaar | Geen engine-bronontdekking/padbewijs |
| B5 gezamenlijke vraag | Twee productie+drie scienceslots via één nieuwbouworigin→selectie5; echte `final_combine` Dorig2/G5/R10→D5 | Actual2→tekort3 blijft ONGETEST |
| B6 filter | Allefalse→geenSCI; originele index65 na65false; nulbekend→prefix0/0SCI | Echte prefix/caller, World+28-stub |
| B7 cutoff | 65bekend→cutoff1, prefix64,64complete commits, SCIbudgetmarker0 | SCIresult is own input |
| B7 SCI-callbudget | Seed calls63, twee centra: eerste complete SCIcommit→64, tweede vóórquery geblokkeerd, alleen eerste slot blijft | Echte uitgezonden union.counter, geen synthetic decrement |
| B7 gekoppelde counter | Echte c2_count_4(primary_food256,total_food264): ieder afzonderlijk op limiet blokkeert beide increments en synthetische continuationwrite; succes laat gate232/236 intact | Begrensd geëxtraheerd echt fragment; alleen PIC-subimm en uitgaande failreturn verplaatst |
| B7 context | SCIcallback wijzigt owner, met cutoff0 én1; scorecallback wijzigt owner terwijl SCIcalls al64: contextfout vóór budgettak, geenSCI | Echte postSCI-/counterguard; volledige finalizefallback wordt niet uitgevoerd |
| ABI/grenzen | Stack/register/x87/canaries na iedere call; gecontroleerde cleanup | Directe fixture, geen loader-/gameacceptatie |

De gekoppelde fragmentadapter voert de181 originele bytes vanaf `c2_count_4_pc−7` tot `_done` uit. Alle interne branches blijven bytegelijk. De `sub esi,modulepc`-immediate wordt op de private fragment-PC afgestemd zodat `lea ebx,own pass` nog naar dezelfde eigen image+e1000 wijst. Alleen de laatste failjmp krijgt een lokale return. Succes bereikt een synthetische writecounter(state80); fail bereikt die niet. Dit toetst echte admissioncontrol en gekoppelde offsets; het is geen echte H3FoodReader-/enginequery.

## Expliciete stubs en open dekking

`prepare_fixtures.py` is uitsluitend reviewbare bron. Zij is **niet uitgevoerd**. Gate gebruikt de bestaande finite stub; canonical_key kopieert begrensde eigen inputpunten; score retourneert1 en kan owner wijzigen; H3 schrijft status2/coverage1/vier eigen productiepunten; SCI schrijft status2/coverage1/drie eigen foodkeys; endpoint en cached_path retourneren1. Geen enkele stub bewijst engine-science, voedselmarges, spatial, terreinomzetting of bereikbaarheid. `combine` maakt uitsluitend de exacte112byte-frame voor de echte `final_combine`/`final_done`; het rekent geen policy na.

ONGETEST: alle overige interne SCI-querycounterlimieten, callbackfout precies bij de laatste eindguard na budgetbranch, volledige finalizefallback die eerder Gcert intrekt, veertig geselecteerde/ALT64/SCI64-overrunnegatieven, cap0/completion/anderegov door volledige policy, typebody native, engine-SCI en Actual-aftrek. Ongewijzigde type/cap/policy/layout/preservatie is eerder statisch onderzocht volgens `ANALYSE/REVIEW-U30-SCIENCE-FILTER.md` en het immutable `candidate-static-checks.json`/`integration-static-checks.json`. Actual ligt in de oorspronkelijke native Desired/quotaketen; `integration_base.py::quota` bewaart W en retourneert slechts D−W. Geen alternatieve subtractie in deze fixture. Het gevraagde Actual2→deficit3 krijgt daarom geen PASS.

Geen109oude cases, nieuw framework, kandidaatwijziging of readertest. Root beoordeelt deze concrete deeldekking vóór eventuele compile/nativevrijgave en beslist afzonderlijk over host. Huidige status: **VOORBEREID**, NIET gecompileerd/uitgevoerd/nativegecontroleerd; geen gameplayverbetering bewezen.
