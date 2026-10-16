# U30 H2: World+28 is een kaartkennisgate

16 oktober 2026, 17:43 Europe/Amsterdam. Gerichte fase A voor Doel1/1a: waarom de eerste productieclassificatie H2 reason3 geeft; voldoende voor B. Alleen deze analyse en eigen voortgang geschreven. Geen spelstart, GUI/RPM, nativecall, build, gameplay- of binarywijziging.

**Antwoord:** de echte `World+28` is geen plaatsingslegaliteitstest. Hij leest bit15 van een spelergebonden kaartveld, met twee overrides die altijd true geven. Dit past bij **verkendheid**, tegenover de naburige query op de overige15bits die bij actuele zichttelling past. De precieze oorspronkelijke namen zijn interpretatie; onderstaande bitsemantiek is machinecode. Een false is normale ontbrekende kaartkennis, geen aangetoonde ABI-/hostfout. H2 mag daarom nog steeds UNKNOWN zeggen over productiegeschiktheid; de U30-caller behandelt deze lokale onbeschikbaarheid als wholepass reason23. Of B dit lokaal moet overslaan of de kaartkennisvoorwaarde moet vervangen, is een ontwerpkeuze; het gameplaydoel is niet tot verkende locaties beperkt.

## Evidence en exacte falsecategorie

Bestandsbinding opnieuw gecontroleerd: engine SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp37d6f702, base400000; echte vtable7452e0+28 bevat533580. Geen civctp.map. Gericht RO gedecodeerd:533580 via bestaand bewijs; nieuw4ebdf0–4ebe62,4ebfa0–4ec01b en aangrenzende bitmapbewerkingen. Een eerste aangrenzende decode begon binnen een voorafgaande functie op4ebc00; die losse eerste instructies zijn geen bewijs. Alleen hieronder genoemde vast afgebakende bodies/operaties worden gebruikt.

`533580` krijgt expliciete `World*, MapPointData*`, converteert via503f00 naar globale scratcha7e320, neemt Player uit World+0c en roept4bbd50 aan. Die neemt Player+1304 en geeft het MapPoint als twee DWORDs door aan4ebdf0 (thiscall, ret8). De helper gebruikt dezelfde argumentvolgorde en ret8; geen gewijzigde call/guard vereist. Hergebruik [H2](PRODUCTIEKANDIDAAT-H2.md) en [bestaande wrappercode](BINAIR/production-candidate-h2-position-and-cell.txt).

Voor object `V = Player[+1304]`, geconverteerde signed16-coördinaten `u,v`, is de echte werking:

```text
if DWORD[a45148] != 0: return 1                      # 4ebdf3–4ebe04
P = DWORD[a7dd80][DWORD[V+4]]                        # 4ebe07–13
if P != 0 and DWORD[P+1344] != 0: return 1           # 4ebe15–28
j = signed16(u + v)
while j >= signed16(V.word2): j -= V.word2           # 4ebe2b–45
row = DWORD[V+14][signed16(u)]                       # 4ebe47–50
return unsigned16(row[j]) >> 15                     # 4ebe53–60
```

Er is **één falsecategorie** binnen het geldige coördinaten-/objectcontract: beide true-overrides zijn uit (de Player-arrayentry mag daarbij null zijn) én bit8000h op het opgevraagde vakje is0. Geen aparte falsepaden voor stad0, bergen, voedsel, terrein, vijand, bezetting of stichtingsafstand. Ongeldige pointers/indices worden hier niet als false bewaakt; die mogen niet als normale lokale afwijzing worden verborgen. Functie4ebfa0 heeft dezelfde overrides/indexering maar retourneert `(word & 7fffh)>0` op4ec00f–15. Aangrenzende4ebd00 zet8000h op alle vakjes;4ebdb0 wist de lage bits en behoudt8000h. Dat ondersteunt de interpretatie 'historisch verkend' versus 'actueel zicht', zonder CTP-II of niet-passende symbolenkaart als bewijs. Namen van beide overridevelden zijn niet nodig voor de herstelroute en blijven backlog.

## Dekkingsmatrix en runtimegrens

| Beslisschakel | Bewezen werking | Gevolg voor wijziging |
| --- | --- | --- |
| Echte engine-/callbinding | Bovenstaande SHA/base/vtableslot, wrapper/stdcall8 en Player-thiscall8 | Geen aangetoonde ABI- of verkeerde-slotbug |
| Centrum | current_model kopieert positie naar H3+116/+120 vóór capacity; nulpositie heeft geen H2reason3 | Ruwe `0000050000000000` is het aangeboden MapPoint0,5,0; geen foodmeting. De reader labelt het conservatiever als UNKNOWN; ruwe bytes plus code onderbouwen uitsluitend het callargument |
| H2 | components.py h2: World+28false → status0/reason3/count−1/mountains−1; World+ac herhaalt intern dezelfde gate en geeft bijfalse count0 | Dit is onbekende productiegeschiktheid buiten kaartkennis; niet bewijs voor onbruikbare fysieke locatie of geen bergen |
| H3 | model.py: capacity0 → status0/reason10 vóór rantsoenen/food | Geen WGF-/foodonderzoek nodig voor deze witness |
| U30 | native.py production_roles: eerste positieveB roept H3 aan; EAX0 → roles_bad/reason23 | Lokale onbeschikbaarheid wordt ten onrechte als passfout behandeld als onze policy alleen bekende locaties wil certificeren |
| Runtime | [PAIR-PROOF](../PROEVEN/u30-reason23/20261016T131100/host1/PAIR-PROOF.json): civ8/gen7/context1/classified1/h3calls1/slots0, H3 0/10, H2 0/3 | Onder gepinde code lokale gatefalse gemeten; geen bewijs van falende andere guards, zeven losse classificaties of extra uitbreiding |

Deze witness bindt geladen kandidaatb6f272d.../engineb1b525... en zeven native-ronden−1→0 met éénn. UI-afwijking/save-identiteit/atomiciteit blijven de expliciete grenzen uit PAIR-PROOF. Sluiting/herstel29bestanden en Doel3release zijn rootoverdracht; geen eigen procesmeting gedaan.

## Kleinste concrete route naar B

**Voorkeur: een lokale kaartkennisfilter in `production_roles`, vóór H3-budgetincrement/call.** Na positieveB en vóór `h3calls>=64`: vraag dezelfde gepinde World+28 met hetzelfde centrum/World (push centrum, push World, call vtable+28, ret8). Bij EAX0 → uitsluitend `roles_next`; anders bestaande H3-route. De helper zelf en zijn UNKNOWN-semantiek blijven intact. Zo verbruiken onbekende vakjes geen van64dure H3-calls en wordt geen verborgen kaartfood gelezen. `classified` blijft een bezochte-kandidatenteller; h3calls wordt werkelijk aangeroepenH3. Deze route vraagt in B het bestaande bindingmanifest te behouden/uit te breiden voor exact deze query en de source/callstack/nonvolatile-regels te reviewen; geen nieuwe enginepatch of FLI/AIP-verandering.

De absoluut kleinste callerdelta is bij H3-EAX0 alleen het samenhangende H3reason10/H2status0/reason3-geval lokaal overslaan, alle andere UNKNOWN naar roles_bad. Dat behoudt echter verspilling van de64H3-calls op onbekende vakjes, waardoor de eerstvolgende hele-passfallback nog steeds kan optreden; de voorafgaande filter voorkomt dat specifieke probleem, maar is geen vastgelegde beleidskeuze. Geen blanket UNKNOWN→skip en geen H2reason3→'fysiek ongeschikt' omzetten. Een gate die bij de herhaalde interne call onverwachtfalse wordt, mag nog steeds de bestaande fallback geven.

Een tweede optie is de visibility-/verkendheidsgate uit H2 vervangen of opheffen als productiegeschiktheid ook voor onbekend terrein moet worden bepaald. **Alleen de expliciete H2-gate weghalen volstaat niet:** World+ac herhaalt intern World+28 en levert daar count0. Het exact ontbrekende antwoord voor deze tweede optie is welke ondersteunde lijstquery/route dezelfde werkplekken buiten deze kaartkennisgate oplevert, en welke AI-perceptieafspraak daarbij geldt. Dat is hier niet bewezen; er is geen algemene claim dat de nativeAI alle ongeziene terreininfo behoort te gebruiken of juist niet mag gebruiken. B moet de lokale-skiproute afwegen tegen een afzonderlijk begrensde vervolgvraag voor die alternatieve route. Lokale skip is een conservatieve vervolgstap, geen bewijs dat het volledige uitbreidingsdoel blijvend tot verkend terrein mag worden vernauwd.

B heeft voldoende evidence voor die concrete keuze en een onderbouwd lokaal voorstel, met deze tweede route expliciet open. Meetlat voor C: bekende positieve centra volgen ongewijzigd H3; gatefalse levert geen slot/certificaat en geen H3-call; volgende kandidaat wordt bezocht; overige host/context/laag/model/index/food-UNKNOWN behouden fallback. Runtime moet vervolgens aantonen dat de echte eerste gatefalse wordt gepasseerd en of latere bekende locaties certificaten geven. Geen claim dat deze wijziging30steden, hogere vraag of extra stichting al bewijst. Overige lokale UNKNOWN-categorieën en precieze overridebenamingen blokkeren B niet. Analyse gereed en gestopt; geen achtergrondwerk, pcaan.
