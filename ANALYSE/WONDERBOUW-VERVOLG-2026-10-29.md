# Wonderbouw: drie beslisvragen voor B

29 oktober 2026, 15:14 CET. Doel4 OPEN; A-overdracht gereed, werk gestopt. Hergebruik [bouwketen](BOUWDOELEN-EN-QUEUE.md), [C2-resultaat](../PROEVEN/wonderbewijs-host/20261029/ROOT-RESULT.json) en inspection.json: exacte token/SID1450/index2 AF,47 echte bezette queues, geen Labyrinth, geen n. Alleen gerichte disassemblage; engine b1b5256f…/release-DLL eb6f58a7… opnieuw gepind, geen civctp.map.

| Keten | Voldoende voor ontwerp | Runtime OPEN |
| --- | --- | --- |
| Queueovergang | Voor/naproof hieronder | Nieuwe Labyrinthqueue |
| Prioriteit/vrijstelling | Tekstroute en beperking | Productiekeuze/één bouwer |
| Geschiktheid | Minimale velden gebonden | Geschikte stad/admission |

## V1 — Blokkeert een bezette beginqueue de hele éénbeurtproef?

Nee:20066500 en20049389–91 eisen leegte bij doelcreatie/uitvoering, niet permanent vanaf laadmoment; engine4911e2–e4 weigert een dan nietlege queue. Natuurlijke voltooiing kan een gelegenheid openen; of dit vóór diezelfde AI-beslissing gebeurt is hier niet gemeten. Geen gegarandeerde vervanging of bouwbelofte.

Toereikend nieuwqueuebewijs: dezelfde gepinde save/owner/volledigehandle; vóór nergens in die stadsqueue klasse9/type2; precies1n/native+1; na echte node klasse9/type2, stabiel gelezen en City Status bevestigd. Dat bewijst een nieuwe aanvraag ondanks bezet T0. Claim oude-itemvoltooiing alleen met afzonderlijk voltooiingsbewijs; anders uitsluitend queueovergang. Negatief resultaat onderscheidt timing/concurrentie/admission niet. Geen lange run nodig.

## V2 — Hoe concurreert Labyrinth en remt bestaande state dubbele bouw?

Default.aip: wonderbasis19997500+9100=20006600; primary-settlerbasis20000000+10500=20010500, verschil3900. build_troops_off geeft een andere basis; effectieve profielen lezen. Formules2004946d–83/20049b30–4e, gezamenlijke matching bewezen; geen universele hoogste-getalgarantie.

Kleinste tekstroute: alleen openings-Wonder_List-gewicht wijzigen; B kiest gewicht tegen werkelijk effectieve unit-/settlerbiedingen en herstelpartials. Bestaande threshold/bouwtijd richt geschiktheid op productiesteden. Dit geeft voorrang onder geschikte steden, geen expliciete éénstadvrijstelling; geen quota/threshold/kosten ongemerkt wijzigen.

AiMain+124→WonderTable+8→72-byte WonderBlg per index.2000f8d0→2000f1b0 zet gedeeldrecord+20=3 (`c7412003000000`), vóór engineacceptatie. CanInsert2000f806–12 verlangt state1: nieuwe doelen geremd. Maar CanBuild2000f09b–aa laat3 toe; reeds gemaakte doelen worden daarmee niet aantoonbaar uitgesloten. Eén bouwer per civ dus niet gegarandeerd; mislukte enqueue kan state3 achterlaten. Herstel/resynchronisatie backlog.

## V3 — Welke velden eerst inspecteren?

CityAgent signed productie+38, stock+28, incumbent+1f0, flag+1f8; AIP wonderthreshold+250 en maxrounds+734 (=Planner+754).33 bestaande controles blijven geldig. Stockuitzondering:≥500, productie≥30, trunc(stock/productie)≥5. Rang i/N via oplopende CityAgent+2c-key (20065ecd/f95 en200660e6–f2); lees alle eigen keys, behandel grensoverschrijdende ties als UNKNOWN.

Kosten: WonderBlg+8 double, getter2000f840→2000f0f0 (`dd4108`); initialisatie2000ed96 haalt actor+4c/slot24. Echte vtable745298+24→533070→474750→WonderRecord+38 (`8b4038`). AI-bouwtijd=trunc((cost+0.5−stock)/productie), bij productie<1 trunc(cost+0.5); eis≤maxrounds en vrije cache/flag. Geen nativecall nodig. Enginequeuekosten kennen afzonderlijke Deity-aanpassing.

B: voeg uitsluitend deze velden toe aan bestaande stabiele projectie, inspecteer één kansrijke stad en ontwerp maximaal1n-vergelijking. Wereldraw0-semantiek/admission blijft UNKNOWN/backlog; geen extra reconstructievoorwaarde.
