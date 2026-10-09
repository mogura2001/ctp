# B4-direct: één blokkerende ownerbinding

**Checkpointstatus 9 oktober 2026, 14:35 Europe/Amsterdam: OPGELOST.** De gerichte [A-ownerbinding](../../ANALYSE/NEUTRAAL-EIGENAARSCHAP-B4.md), SHA0820ea7de6382ae49ea00d3f03a5deef95001220efba65f10768541631679251, en de rootgereviewde ontwerpaanvulling SHA535a2a8390bade32530610c2ca501fd247e7f4e8d50222b922a3e89366cc0794 binden World7452e0+54→533880→516c10, stdcallret8, signed32owner, neutraal exact−1 via init4ff885/verwijder516efb. Hieronder blijft de oorspronkelijke vraag met haar toenmalige bewijsgrens ongewijzigd als provenance. Dit is geen resterende ownerblokker.

9 oktober 2026, 14:16 Europe/Amsterdam. Fase C, alleen voorcontrole; geen afhankelijk producer-/quotapakket gebouwd. Root bezit PROJECTSTATUS/VERSIES. Dit checkpoint is geen B4a-0- of mockproducerresultaat.

**Exacte terugvraag aan de ontwerper:** bind voor de oorspronkelijke engine SHA `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79` de actuele `World+54`-wrapper, return-ABI/readbreedte en de specifieke oorspronkelijke territoriumwaarde die werkelijk geen eigenaar betekent. Lever de minimale bestaande bytes/adressen voor wrapper->getter en de neutraalinitialisatie/schrijver of een ondubbelzinnige native neutraalpredicate. Hoe onderscheidt B4 deze waarde van civ0/barbaren en andere ongedefinieerde signed codes? Geen nieuwe safetystrategie nodig; alleen de reeds verplicht gekozen eigen/neutraal-gate concreet binden.

## Waarom deze binding de uitvoering blokkeert

[Het concrete voorstel](../../ONTWERP/PRODUCER-SETTLERVRAAG-B4.md) onder 'Directe veiligheid in juiste coördinaten' eist eigen of de **gebonden oorspronkelijke neutraalencoding** en verbiedt gokken -1/0. De producer beoordeelt source, destination en alle padpunten. Zonder die encoding kan hij de gekozen directe vestigingsscope niet volledig certificeren. Onbekende codes als UNKNOWN afwijzen is vereist voor echte onverwachte input, maar het ontbrekende contract voor normale neutrale bestemmingen door steeds UNKNOWN vervangen levert geen voltooide geïntegreerde technische producer. Alleen eigen terrein toelaten zou deze beschreven strategie wijzigen. Beide worden daarom niet als vervanging gebouwd.

De relevante aangeleverde B4-P-bewijzen noemen World+54 als eigenaarread maar binden geen neutraalwaarde. `settler-producer-b4-engine-reads.txt` bevat in de onderzochte vtable-readsecties geen World+54-wrapperbinding. De reeds bestaande onderstaande code verkleint de onzekerheid wel, maar lost haar niet op:

- [Bestaande padcallback](../../ANALYSE/BINAIR/diplomacy-naval-state-and-path.txt:483), `200178b0–200178c1`: World via AiMain+30, `push pos; push World; call [vtable+54]` op `200178b7`; vervolgens `test eax,eax; jle 200178fc; cmp eax,20h; jge 200178fc`. Dat is de predicate **1..31** voor deze extra diplomatieke padkosten. Alle codes <=0 nemen samen de skiproute; dit bewijst niet dat één daarvan neutraal is.
- [Bestaande enginegetter](../../ANALYSE/BINAIR/terrain-food-v2-ai-city-yields-engine.txt:349), `00516c10–00516c34`: de mapgridroute eindigt op `00516c2f: 0fbe420e`, `movsx eax,byte ptr [cell+0e]`; `ret4`. Dat bewijst een signed-byte-eigenaargetter in deze eerder gebonden pop/workerroute. De dump bevat hier geen neutraalinitialisatie/schrijver en bewijst zelfstandig geen World+54->deze getter-binding.

Er is geen bewijs om 0, -1, een andere negatieve waarde of alle negatieve waarden als neutraal toe te laten. Geen nieuwe volledige pathfinder/territoryanalyse gevraagd.

## Daadwerkelijk gecontroleerde versie en hooks

Alleen-lezen gecontroleerd met bestaande lokale Python312/pefile, zonder builderimport of gamecalls. Input `PROEVEN/production-h3/backup/robotcom.original.dll`: SHA `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, timestamp `37b894e7`, imagebase `20000000`.

| VA | Bestandspositie | Werkelijke preimage | Controle |
| --- | --- | --- | --- |
| 2002b079 | 2a479 | e882550400 | Exact gelijk |
| 2007abac | 79fac | e8cff4ffff | Exact gelijk |
| 20066b81 | 65f81 | e81aeeffff | Exact gelijk |
| 2002b0d8 | 2a4d8 | e893ba0300 | Exact gelijk |
| 20065a4c | 64e4c | e8affeffff | Exact gelijk |

Geen patch uitgevoerd. **Baselinecompositie nog niet beoordeeld.** H3 en B2a zijn afzonderlijke oorspronkelijke-basiskandidaten; hun builders gebruiken beide `.h3`/`.b2a` op RVA d4000 en headerwindow250. Rechtstreeks kopiëren/overplakken vormt dus geen compositie. Na beantwoording moet de toegewezen B4-builder de bestaande emitters hergebruiken en hun plaatsing/rel32/PIC/headers opnieuw verklaren; geen wijziging aan bestaande builders. Dit is een routinebouwvereiste, geen tweede ontwerpterugvraag. H3-currentresult is beschikbaar als caller-owned1024bytes met gekozen indices100/104/108/112 en canonicalcenter116; B2a heeft concrete symbolenbinding met externalpointer+0, doubles+8/+c, inputmask+c2 en initmask+68. Er is geen samengestelde baseline vervaardigd of als geaccepteerd gepresenteerd.

Gecontroleerde bestaande kandidaathashes:

| Kandidaat | SHA256 |
| --- | --- |
| H3-SCORE_CURRENT | f93be3629decd38a94117ba774aac3673db2cd2b9e1a0d8a1dde42f7b8e4fd9c |
| B2a-N25-TECHNICAL | 9553d440365b029d47cd5b6c0717e6e96a6c2aeac3b1052bb80293736d35667a |
| B2a-N30-TECHNICAL | eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890 |

Gelezen bewijs-/ontwerphashes:

| Bestand | SHA256 |
| --- | --- |
| ONTWERP/PRODUCER-SETTLERVRAAG-B4.md | 807f10ce5bfb88af44d9cafc5b623d548c56bf5af42f1dce5e607ee500b7b8f8 |
| ONTWERP/DYNAMISCHE-SETTLERVRAAG-B4.md | ed3ec6dd5158980b389ad80bb7b2017fe608b7138d878e11175bce2c51a5af21 |
| ANALYSE/PRODUCER-SETTLERVRAAG-B4.md | 0cc39ee7df6a232d03340ca08b0dbb7f52d1e9103706a2c0e1bfc06dd41de3c3 |
| ANALYSE/BINAIR/terrain-food-v2-ai-city-yields-engine.txt | 59e25a3057c00595b914c4d626a037a069dddf65a510548aee2e417d8f508bd34 |
| ANALYSE/BINAIR/diplomacy-naval-state-and-path.txt | 98b1f4934a4bb384182be100bc62bf9308acf7865f386be887041a37e8c4650d |
| ANALYSE/BINAIR/settler-producer-b4-engine-reads.txt | 9a888543e76542ea813411441e276e23c83630bf107efc36ac916a9d61ad0778 |

## Status en hervatten

Voorbereid: beperkte opdracht gelezen en exact blockercheckpoint. Offline gecontroleerd: vijf oorspronkelijke hookpreimages, versie en drie bestaande kandidaathashes. Toegepast: niets. Native producer-/ABI/claim/pathbufferfixtures: niet gebouwd/uitgevoerd. In gameplay gemeten: niets. H3-production-only blijft een technische subset; N25/N30 blijven pending productiebeleid. Save/load/cache/lifetimegedrag van de nieuwe producer is nog niet geïmplementeerd of getest.

Geschreven uitsluitend dit verslag en `ANALYSE/VOORTGANG-UITVOERDER-B4.md`. Beschermde directories/pakketten zijn niet geschreven; geen volledige nieuwe beschermde inventoryclaim gedaan. Geen installatie, GUI, gameprocesactie, liveprocesread/injectie, export of echte enginequery/free/fatalhandler. D-game blijft ongemoeid. Er is geen native helper of andere actieve achtergrondrun.

Root draagt alleen de bovenstaande exacte binding terug aan ontwerp. Na bindend antwoord kan dezelfde beperkte C-opdracht worden hervat; geen zelfstandig vervolgpakket. Budget14:16:34, bron14:16:22 Europe/Amsterdam: vijfuur93/week37, ok.
