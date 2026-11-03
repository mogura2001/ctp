# Uitbreiding: bevestigingsresultaat 22 oktober 2026

2026-10-22T12:03:47.877039+02:00 Europe/Amsterdam. Alleen opgeslagen bewijs beoordeeld; geen nieuwe GUI-, RPM-, native-, bouw- of installatieactie. Uitvoerder afgerond en gestopt na overdracht.

De tweede kandidaatrun bevestigt **25 steden op T26 tegenover 20 in de historische Doel3-controle (+5; +25%)**. De stadsaantallen van alle zeven civs zijn op ieder van de 27 meetmomenten exact gelijk aan de eerste kandidaatrun. Deze herhaling volgt het gewone protocol met 26 tokens en 26 n-acties, zonder T1-herstelafwijking.

1. Meetgeldigheid en herstel

Alle 27 snapshots zijn stable_twice, alle geladenchecks zijn waar, deelnemers zijn 2..8 en de native rondes lopen exact van −1 tot 25. Ze binden dezelfde PID17460, creation134371362632601070 en run-id science-duur-20261022-host3; kandidaat df3ac89d… en manifest5b05daf3… zijn gelijk aan de eerste arm. De eigen 185 bronpins zijn nu exact; SOURCE-PINS SHA256 02a067eef32b1f7ce44186f4c17edbd3bfee31650725980b796b797258e38556.

Alle 26 gewone passes hebben één n, zeven rondes exact+1, een succeslog en een unieke token met exacte vorige snapshothash en procesbinding. Er zijn precies26 gewone tokens en geen aparte hersteltoken. De T1-foregroundcapture vond vóór tokencreatie plaats; de gewone T1-pass voltooide vervolgens. T0 heeft alle historische civvelden gelijk, met uitsluitend ai_actor/effective_aip buiten vergelijking, en advance_count138; dit geldt ook tegenover host2. Readerflags voor rechtstreeks bewezen save-identiteit en atomiciteit blijven false: de vaste savehash, laadprocedure en deze scalargelijkheid vormen samen de startbinding.

Normale afsluiting na540,227s, exit/count0. Alle29 beforebestanden en zeven bestaande archieven zijn opnieuw hashgelijk; nieuwe autosave is dubbel gelijk op af4888a6cbd7f356494afe624028b7673f8d6c0104ba97e22834bf88b9d04ec6. Reader/control/hostgatesFALSE en geteste Doel3-DLL eb6f58a7… hersteld. De autosave heeft geen bewezen exacte T26-binding. Root-HOST-PROOF SHA256 e1d545e90d1354f1eeab871a85559c6c5eaf491366ca0aac51433e5855fc7dac.

2. Volledig traject en NOW-herkenning

Volgorde civ2..8; beide kandidaatarmen hebben dezelfde waarden.

| T | Historische controle | Beide kandidaatarmen | Totaal oud→nieuw |
|---|---|---|---|
| 5 | 1,1,2,1,1,1,2 | 1,1,2,1,1,1,2 | 9→9 |
| 10 | 2,2,2,2,2,2,2 | 2,2,2,2,2,2,2 | 14→14 |
| 15 | 2,2,2,2,2,2,2 | 2,2,2,2,2,2,2 | 14→14 |
| 20 | 3,3,3,2,2,2,3 | 3,4,3,2,2,2,3 | 18→19 |
| 25 | 3,3,3,3,2,3,3 | 3,4,4,3,3,3,4 | 20→24 |
| 26 | 3,3,3,3,2,3,3 | 3,4,5,3,3,3,4 | 20→25 |

De JSON bewaart alle27 trajecten per civ voor controle, host2 en host3. T26-verschillen zijn [0,+1,+2,0,+1,0,+1]; geen civ eindigt onder zijn controle. Alle zeven kennen Religion en Theocracy en hebben actieve regering3. De eerste actieve Theocracy-momenten zijn in beide kandidaatarmen gelijk: T14/20/26/12/16/13/23; controle T14/20/26/12/16/13/24.

Gebonden science-NOW-selectie met strikt positieve huidige voedselmarges is opnieuw aangetoond op T1/2/18/22/23/24, exact dezelfde zes meetmomenten als host2. Dit geldt uitsluitend voor laatste civ8, generation7×T. T1 één selectie met marges35/30/25; T2 twee met35/30/25 en25/20/15; T18 één met25/20/15; T22 één met30/30/30; T23 één met35/30/25; T24 één met30/30/30. Andere passes worden niet automatisch als NOW beschouwd. Dit bewijst selectie en huidig voedsel, geen stichting op die centra, sciencebouwqueue of laborerinzet.

3. Wat nu bevestigd is en wat openblijft

De positieve vroege uitbreidingsuitkomst is reproduceerbaar in twee kandidaatarmen op één vaste start. De tweede arm bevestigt exact dezelfde vijf extra steden; het gaat om25 totaal over zeven civs, met3–5 per civ. Dit is geen universeel effect over kaarten of bewijs dat één specifieke instructie de winst veroorzaakt.

Alle zeven nativeDesired-waarden blijven op T1..T26 steeds5. De gebonden civ8 heeft steeds desired=Dorig5: extra vraag boven Dorig is nergens in deze gedeelde buffers aangetoond. Op T26 heeft civ8 Gcert0/classified0/slots0 en toch vraag5. Locatieafhankelijke rem/hervatting is dus niet bewezen; Gcert/Dorig van de andere zes civs blijven onbekend. nativeActual is geen totale voorraad; volledige queues en missievrijheid blijven UNKNOWN.

Acceptatie: de begrensde duurproef en bevestiging zijn gemeten; het vroege +25%-signaal en beperkte NOW-herkenning zijn bevestigd. Doel1/1a en volledigeDoel5 blijven OPEN: tijd tot30 steden per civ, nuttige30→40 en rem bij onvoldoende veilige/bereikbare locaties zijn nog niet gemeten. De volgende oplevering is roots eindige A-vraag over het bestaande vraag5/remgat; deze evaluator start geen extra onderzoek of proef.

Bewijs: [VERGELIJKING.json](../PROEVEN/science-duur-host/20261021/host3/VERGELIJKING.json) bevat exacte bron-/snapshot-/token-/pass-/n-loghashes, alle27 stadstrajecten, gedeelde laatste-passes en herstelchecks. Budgetbron 2026-10-22T10:02:12.543Z: vijfuur40%/week58%, stateok. Werk gestopt; pc blijft aan.
