# Gerichte A-terugvraag: techvrije IRR2-ruimte voor early science

13 oktober 2026, 18:24 Europe/Amsterdam. **Eén vraag beantwoord; gereed voor gerichte B-correctie.** Basis is ONTWERP/SCIENCELOCATIES-U30-40.md, aangeleverde SHA256 b0201f5c8e161d35b86c0f04b8bd48d485553ab27a111d65af491edd4894a1f8. Alleen analyse, eigen dit bestand en VOORTGANG-SCIENCELOCATIES.md. Geen spelstart/GUI/livequery/nativefixture/helper/code- of binarywijziging.

## Antwoord

**Ja, bestaande bindingen kunnen ruimtelijke IRR2-toelating onafhankelijk van actuele technologie, eigendom en aanvragen beoordelen.** De concrete ontbrekende route is **World+34→533620→516c40**, naast het geladen **hoofd-TerrainRecord+6c** en het effectieve foodenvironment. Zij heeft geen Player-/city-ID-/worker-/advance-/PW-input. Daarmee kan vroege science-NOW op **huidig onverbeterd food** en drie huidige ruimtelijk geschikte toekomstige IRR2-werkplekken worden beoordeeld, terwijl development PENDING blijft bij +10/+20false.

**Drie positieve loaded ENV_IRR2-pointers plus alleen de H2-open-footprint zijn onvoldoende voor de sterkere claim 'ruimtelijk toegelaten IRR2'.** De echte IRR2-Worldbranch heeft een extra ruimtelijke voedings-/watercontexttoets516c40. Deze hoeft geen nieuwe stad te zien, maar kan false zijn op gewone lege terreintiles. Het ontbrekende onderscheid is dus nu concreet te toetsen zonder toekomstige stad te simuleren. Loaded ENV/open footprint blijven een zwakker terreinpotentieelkenmerk wanneer die extra toets false/unknown is; false betekent niet bewezen permanent onverbeterbaar.

## Drie bronpunten en dekkingsmatrix

| Punt | Aangetoond oorspronkelijk gedrag | Gevolg voor het ontwerp |
| --- | --- | --- |
| **1. Loaded terrein is een aparte mogelijkheid** | Parser ENV_IRR2-token1000→4676a8→TerrainRecord+6c; environmentfood+0, materials+20,time+24,advance+44. TerrainDB455b10: count/array/stridec0. H3 food_reader selecteert het effectieve goodrecord voor actuele food; techgetter4685e0 selecteert eveneens een goodrecord vóór+6c/+44 | Blijf currentfood, effectieve foodomgeving en enabling advance gescheiden lezen. Een positief environment is geen huidige opbrengst of volledige aanlegtoelating |
| **2. World splitst de intrinsieke test uit** | **4d43e0→455b10 leest hoofdrecord op Cell+d**, selector1-jumptable4d45dc→**4d4454**: hoofdrecord+6c moet bestaan, dan **4d4466→516c40** moet true zijn. Deze branch leest geen advance, Player, city-ID, PW of aanvraag | Fysiek IRR2-kenmerk: hoofd-ENV_IRR2 aanwezig, effectief positief foodenvironment, actuele open footprint, en gebonden ruimtelijke predicate true. Niet uitsluitend positieve good-ENV tellen wanneer het hoofdrecord ontbreekt |
| **3. Actuele bouwbaarheid is een andere vraag** | Improvement+20→526ad0→Player4bfd70: bestaande citycheck5154e0 op4bfda1; gebied/eigenaar515af0 op4bfe69; advance474b60 op4bff5d/80/4bfffd/4c0022; materials alleen onder conditionele outputcontext4c006b–df; bestaande/pending context4d3fc0 op4c012f; World4d43e0 op4c0155; level/installation/request-state4c01a0 op4c016b. Wrapper vervolgt met +28 en World4d43e0 | +20false mag de zelfstandige fysieke wetenschapstest niet meer automatisch uitsluiten. Bewaar raw bouwstatus en development-PENDING/UNKNOWN; beloof geen huidige aanvraag of aanleg |

Bestaand bewijs: [terreininterfaces](TERREIN-EN-IMPROVEMENTS.md), [H2](PRODUCTIEKANDIDAAT-H2.md), [H3](KANDIDAATVOEDSEL-H3.md), BINAIR/terrain-food-v2-environment-field-binding.txt, terrain-food-v2-canonical-sort-and-legality.txt, terrain-food-v2-level-and-legal-start.txt, terrain-food-v2-parser-completion-and-eligibility.txt, terrain-food-engine-improvement-details.txt, improvement-construction-admission-and-completion.txt. Aanvulling hieronder bindt alleen de ontbrekende Worldbranch en callback; geen brede heropening.

## Exacte nieuwe ruimtelijke query en bewijs

De echte engine-Worldinterfacetabel **7452e0+34 bevat533620** (vier-byte PE-read). **533620** neemt World-interface en externe MapPointData*, converteert via503f00 naar intern, en roept516c40 aan met het echte World-object uit globalA7DD70. **ret8/EAX**: conceptueel `spatial_food_context(World*, MapPointData*) -> int`. Geen civ-, city- of improvementargument toevoegen. Positieinput, owner/generatie, z0 en HostBinding blijven die van H2/H3. Alleen de huidige gewone ondersteunde engineversie gebruiken en deze extra slot/bodybinding in C pinnen.

Bij callee-entry: ESP+4=World*, ESP+8=externe MapPointData*. Push positie, dan World; callee ruimt8bytes op. Op ondersteund z0 geeft EAX exact0/1, uit de geïnitialiseerde World+38c en uitsluitend0/1writes. Het niet-z0-pad516c53–61 retourneert1 zonder deze grondscan: **niet gebruiken voor science**. Deze query draait op ieder van de drie voedselvakjes, niet op het kandidaatstadscentrum als vervanging voor alle tiles.

**516c40** initialiseert World+38c=0, World+388=1 en laat **49fdd0** een lokale positieomgeving aflopen met wrapnormalisatie49fb20 en callback World.vtable+0. Dit is een query met bestaande gedeelde scratch, geen letterlijk geheugen-onveranderende functie; serieel/niet-reentrant in dezelfde AI-context. Geen eigen World/city/worker object verzinnen. Niet zelf scratchvelden wijzigen.

De scan49fdd0 heeft drie rijen van ieder drie posities. In **interne** x/y-coördinaten t.o.v. de onderzochte foodtile: dx+1 met dy−2,−1,0; dx0 met dy−1,0,+1; dx−1 met dy0,+1,+2. Dus de foodtile zelf is inbegrepen. 49fb20 verzorgt iedere normalisatie/wrap; deze tabel is branchuitleg, geen nieuw extern-coördinatenalgoritme. Het betreft de lokale context van de improvementtile, geen vereiste bestaande stad en geen tweede twintigtiles-stadsfootprint. H2 bepaalt afzonderlijk dat de tile binnen de kandidaatstad ligt en open is.

**Alle vijf ondersteunde foodcontexten nemen dezelfde branch:** 4d4417–23 dispatcht op improvementselector1, niet op land/water of terreinindex. Zowel1/4/5 als10/11 gaan via hoofdrecord+6c en516c40. Geen aparte fishery-/water-IRR2-Worldbranch. Een waterflag kan de lokale predicate laten slagen doordat de tile zelf wordt bezocht; de exacte nativeflagtest behouden, niet op grond van de terreinnaam true invullen. World4d43e0 gebruikt hoofdrecord; positieve effectieve good-ENV zonder hoofd+6c is dus niet voldoende. Beide concrete recordvoorwaarden apart toetsen.

Callbackbinding: native World-vtable **744170+0=5107b0** (PE-read); initialisatie505a0f schrijft744170 naar World+0. **5107b0** branch mode1→51086c. Zij zet World+38c=1 wanneer een bezochte cel:

- flagmask **0x80c** heeft (510895–99: huidige IRR-bits0x0c of rivier0x800 volgens reeds gebonden cellflags), of
- predicate **514bc0** true geeft (5108a0–a7; 514be1 test Cell.flags & **0x42000000**), of
- een aanwezige installationrecord met typeveld+18 gelijk **0,1,2** oplevert (5108e2→500c10→4d3380,5108ee–510908).

Deze zijn concrete machinecodecondities; de namen/voltooide projectstatus van die installationtypen zijn hier niet verder gereconstrueerd. Gebruik de oorspronkelijke predicate, geen eigen aanname 'iedere waterachtige tile' of 'lege tile bevat automatisch irrigatie'. Zij vraagt geen werker/stad/tech; World+ac verwijdert juist huidige laborers/centra. Een positieve ruimtelijke toets zegt dat **de bestaande engine nu de aparte IRR-ruimtecontext accepteert**, niet dat alle latere omstandigheden gelijk blijven.

Minimaal bewijs uit gerichte RO-disassemblage:

```text
4d440b movsx eax, byte ptr [edx+0xd]  ; werkelijk cellterrain
4d4410 call 455b10                   ; hoofd-terreinrecord
4d4454 mov eax, [esi+0x6c]           ; IRR2
4d4459 je 4d45ce                    ; ontbrekend => false
4d4466 call 516c40                  ; extra ruimtecontext
4d446d je 4d45ce                    ; ruimtefalse => false
4d4473 mov eax,1 / ret0ch           ; Worldselector toegelaten
53362c call 503f00                  ; externe positie converteren
53363c call 516c40 / ret8           ; zelfstandige interfacequery
516c66 mov [World+388],1            ; querymode
516c70 call 49fdd0                  ; lokale scan
516c75 mov eax,[World+38c] / ret4   ; ruimtelijke predicate
510895 test [Cell],0x80c
5108a0 call 514bc0
5108ff / 510915 mov [World+38c],1
```

Reproduceer met bestaand PROEVEN/Analyseer-Engine-Locaties.py, RO-ranges `4d43e0:240 516c40:83 533620:25 5107b0:178 514bc0:30 49fdd0:103 505a00:15`; vtables/switch zijn data, geen als instructies geïnterpreteerde tabelbytes. De gericht gelezen volledige functieheaders/returns zijn valide. Eerste brede dump begon enkele niet-gebruikte ranges misaligned; die zijn geen bewijs. Alleen de hierboven vanaf geldige starts gedecodeerde branches en expliciete tabelreads gebruiken.

Engine telkens onafhankelijk gedrukt/gecontroleerd: SHA256 **b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79**, imagebase400000/timestamp37d6f702. Geen civctp.mapadressen. Robotcom.map blijft alleen passend DLL-bewijs; hier geen enginekaartbewijs. Geen instructies uitgevoerd, geen nieuw runtimebewijs.

## Praktische kleine overdracht aan ctp_ontwerper

Voor ondersteunde plains1/grass4/desert5/shallow10/deep11, normaal landcentrum/z0, geldige loaded host/Cell/DB/goodcontext:

1. Enumereer dezelfde H2-open plekken; iedere tile één canonieke key, centrum apart. Hoofd-TerrainRecord+6c aanwezig, effectief positief gebonden IRR2-foodenvironment en geldig datamodel. Voor PRESENT-IRR2/3 blijft bestaande huidige niveaucontrole gelden; niet downgraden.
2. Vraag **World+34(tile)** om de afzonderlijke ruimtelijke context. True geeft huidige fysieke IRR2-toelating zonder tech/request/Playerbouwgate. False bewaart STRUCTURAL_POTENTIAL/SPATIAL_PENDING; fout/onvertrouwde context UNKNOWN. Geen toekomstige irrigatieketen of hypothetische aanleg gebruiken om false naartrue te forceren.
3. Bij minstens drie zulke open ruimtelijk geschikte tiles en positieve **onverbeterde currentfood**-scenario's n1/2/3 kan locatie-NOW voor de bestaande conditionele Gcert gelden, **ook vóór enabling tech en bij +20false**. Ontwikkeling blijft afzonderlijk PENDING/UNKNOWN/PRESENT/READY. Native endpoint/type/veilig direct pad, gekozen mandatorykeys, één gedeelde matching en crime-/modifiercondities blijven nodig; niets aan futurefood toevoegen in NOW.

Dit vervangt uitsluitend de B-eis dat iedere nog niet aangelegde NOW-foodmogelijkheid al +10 én+20 moet accepteren. +10/+20/+48 blijven uitleg/ontwikkeling; geen false diagnose tot 'alleen tech ontbreekt' maken. Een ruimtelijke querytrue plus hoofd-ENV verklaart precies het eerder ontbrekende onderscheid.

**UNKNOWN/grens:** bare loaded potentials zonder positieve ruimtecontext; ongedekte andere terreinen/goodcontext; onbekende data/host/ABI; door bezetting/claims niet gezamenlijk bruikbare tiles. Ruimtefalse is geen permanent tekort: later bestaand irrigatienetwerk of terreincontext kan veranderen. Futureketens/transformatie ontwerpen is een aparte vraag en blokkeert de hierboven voldoende positieve route niet. Geen aanleg/PW/groeibeurt/nettofoodgarantie of toekomstige ownership voorspellen. De native huidige worker-/installationaansturing moet zulke locaties later nog ontwikkelen; geen volledige sciencegameplayacceptatie uit Gcert.

Einduitkomst: **1/1 terugvraag beantwoord.** Earlyscience hoeft niet uitsluitend na IRR2-tech te worden gecrediteerd. Ontwerper kan de concrete extra ruimtelijke predicate en aparte readiness verwerken; geen verdere analyse nodig voor deze positieve, conditionele route. Analyse stopt bij overdracht.
