# H1 — per-civ locatiescore aan de AI-zijde

7 oktober 2026, 21:38 Europe/Amsterdam. Gerichte fase-A-overdracht; geen spelstart, proces-/geheugentoegang, gewijzigde gamebestanden of kandidaatbinary. De brede A-overdracht blijft geldig.

## Antwoord en begrenzing

**Een concrete kansrijke route is beschikbaar:** voeg later aan de proefversie van `robotcom.dll` een eigen uitvoerbare PE-sectie toe en vervang uitsluitend de drie bestaande scorecalls op **200784bb, 20078517 en 2007aa35** door een relatieve call naar dezelfde scoreadapter. Die adapter ontvangt de bestaande World/positieargumenten en verkrijgt de actuele **AiMain** uit **g_settle_ai**, zodat zij per beschaving kan rekenen. De bestaande kandidaatvergelijking, positieve-scorecontrole en GoalSettle-constructor verwerken vervolgens dezelfde nieuwe kwaliteit. Geen gedeelde enginecache of interfacevtable hoeft daarvoor te worden overschreven.

Dit is een onderbouwde invoegroute voor de ontwerper, geen gebouwde/laadbaar bewezen mod en geen gemeten gameplayverbetering. De drie calls zijn complete instructies met voldoende ruimte, de eigenaar wordt vóór heapopbouw ingesteld, de echte getter-ABI is gebonden en de PE bevat ruimte voor de extra sectionheader. De ontwerper kan nu een herstelbaar eerste adapterpakket uitwerken. Verdere reconstructie van scheduler, alle events of savecyclus is hiervoor geen voorwaarde.

Het gameplaydoel blijft production-, science- en monopolylocaties volgens [PROJECTDOELEN](../PROJECTDOELEN.md) en [LOCATIESELECTIE](../LOCATIESELECTIE.md). De eerste technische adapterproef realiseert nog geen volledige specialisatie. Geen numerieke kwaliteitsgewichten gekozen.

## Huidige beslisketen en dekking

| Beslisschakel | Huidige werking / bewijs | Concrete ingreep / grens |
| --- | --- | --- |
| FLI/AIP | Packing, goallimieten, typebonussen en `settle_value_coef`; geen complete production/science/monopolyscore | Profielcoëfficiënt blijft een later gewicht op kwaliteit. AAIP-diffs zijn lessen, geen gemeten effect of bewijs van deze hook |
| Eigenaarscontext | `InsertSettleGoals` 2007aaf0 ontvangt AiMain; store 2007ab95 schrijft deze naar g_settle_ai | Dezelfde AiMain beschikbaar voor beide comparatorcalls en doelcreatie binnen deze selectiepass |
| Kandidaatopbouw | Ground 2007a080 en Space 2007a2f0 bouwen een heap van 6-byte AiCellPtr-objecten; x/y en heapindex, geen eigen scoreveld | Eerste scorecalladapter verandert de vergelijking tijdens invoegen, vóór beperkte doelselectie |
| Kandidaatordening | Vergelijker 20078460 leest World+168; statisch uitgesloten positie krijgt nul; signed 16-bit vergelijking | Calls 200784bb / 20078517 naar gedeelde nieuwe beoordeling; bestaande tie-/maskerlogica blijft geldig binnen haar bereik |
| Doelaanmaak | InsertBestSettleGoal 2007a7c0 leest World+168 op 2007aa35; alleen signed BX>0 wordt GoalSettle | Derde adaptercall levert dezelfde representatie/formule; kwaliteit wordt signed extended en als double doorgegeven op 2007aa92 |
| Concurrentie met andere doelen | GoalSettle 20048820 leest double kwaliteit op +48 en vermenigvuldigt op 200488e3 met settle_value_coef | Geen vierde hook nodig om nieuwe doelkwaliteit hier te laten meetellen; algemene prioriteit/typebonus blijven invloed hebben |
| Maskers / legaliteit / continentquota | Kwaliteit wordt pas gebruikt nadat diverse bestaande filters werken | Deze hook heft uitsluiting, packing, veiligheids-/continentfilters of gebrek aan transport niet op. Kwaliteitsafhankelijke maskeruitzondering is afzonderlijk werk |
| Oude opgeslagen toestand | Engine heeft gedeelde opgeslagen 16-bit scorecache; reeds bestaande goals kunnen een oudere kwaliteit dragen | Ongecachete adapterwaarde komt niet uit die wereldtabel. Eerste proef vereist aantoonbaar nieuw opgebouwde kandidaten en nieuw aangemaakte goals; bestaande goals worden door deze drie calls niet automatisch bijgewerkt |

Huidige globale score en savebewijs worden hergebruikt uit [LOCATIEKWALITEIT](LOCATIEKWALITEIT.md) en [SCORECACHE-EN-INGREEPPUNTEN](SCORECACHE-EN-INGREEPPUNTEN.md). De hook voegt per-civ logica toe op de plaatsen waar de AI nu de gedeelde score leest.

## Machinecode: eigenaar, kaart en positie

Nieuw gericht bewijs: [callcontext](BINAIR/score-hook-h1-callcontext.txt), [directe vergelijkercallers](BINAIR/score-hook-h1-comparator-callers.txt), [heaphelpers](BINAIR/score-hook-h1-heap-callers.txt). Robotcom.map en binary passen: timestamp **37b894e7**, imagebase **20000000**, SHA256 **3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44**. Engine-map wordt niet als adresbron gebruikt.

- **2007ab13:** EBX = AiMain-argument. **2007ab95:** `[200c6fb4] = EBX` (`g_settle_ai`). **2007ab9b:** statisch masker uit deze AiMap naar `[200c6fb8]`. **2007aba3:** g_settle_z = 0. **2007abac:** GroundBuildSettleTree met deze AiMain. De civ-/masker-/laagcontext staat dus vóór de eerste vergelijking.
- Beide comparatorcalls halen World uit **AiMain+30** en gebruiken x/y uit AiCellPtr+0/+2, laag uit **g_settle_z 200c6fb0**. Op **2007ae27** wordt laag 1 gezet vóór SpaceBuildSettleTree. De comparator is een thiscall met ECX=this, andere AiCellPtr op stack, boolachtige long in EAX, `ret 4`.
- **2007a915:** ESI = AiMain bij doelcreatie. Positie staat op EBP−40/−3e/−3c als drie 16-bit velden. **2007aa26:** World = `[ESI+30]`; **2007aa35:** dezelfde World+168-aanroep. AiMain is ook direct in ESI beschikbaar; de gekozen gezamenlijke adapter gebruikt de reeds ingestelde globale context binnen de bewezen pass.
- Civ-identiteit **AiMain+20** is eerder aan GameState-slot+0c gebonden; zie [ACTIVATIE-ONDERZOEKSLIJST](ACTIVATIE-ONDERZOEKSLIJST.md). Voor de adapter is de eigenaarpointer genoeg; geen engine-Playerglobaal of profielnaam nodig om de civ te raden.

De gerichte directe-referentiecontrole vindt zes comparatorcalls: Ground **2007a275**, Space **2007a47c**, CleanSettleQueue **2007b06c/2007b08e**, ShiftDown **2007b30b/2007b328**. De heaphelpers roepen daadwerkelijk 20078460 aan. Een extra directe-referentiecontrole vindt **geen directe CleanSettleQueue-call** ([bewijs](BINAIR/score-hook-h1-clean-callers.txt)); dit sluit indirect gebruik niet uit. Geen algemene claim dat iedere toekomstige/indirecte aanroep dezelfde eigenaar heeft. De adapter krijgt daarom als ontwerpvoorwaarde: werken binnen de aangetoonde selectiecontext, contextchecks/fallback en geen eigenaarpointer langdurig bewaren.

## ABI en kwaliteitcontract

[Read-only PE-/ABI-controle](BINAIR/score-hook-h1-pe-abi.txt) bevestigt voor alle drie adressen exact **ff9168010000**, één volledige 6-byte instructie `call dword ptr [ecx+168]`.

Op entree van de vervangende adapter:

| Stack / register | Betekenis |
| --- | --- |
| ESP+0 | Retouradres |
| ESP+4 | World-interfacepointer (`this` expliciet op stack) |
| ESP+8 / +0c / +10 | x / y / z in 4-byte argumentslots; alleen de laagste 16 bits hebben de bewezen betekenis |
| EAX | Uitvoer: nieuwe kwaliteit, betekenisvol als signed 16-bit waarde |

De echte enginewrapper **00535500** haalt deze drie positieargumenten op, roept **005238d0** aan en eindigt op **0053551b met `ret 10h`**. De interne getter gebruikt signed 16-bit x/y/z en leest alleen AX uit de wereldtabel; de hoge EAX-bits zijn geen betrouwbaar 32-bit scorecontract. De adapter moet de lage positiehelften expliciet sign-extenden en EAX eenduidig zetten.

Behoud EBX/ESI/EDI/EBP en exacte ESP-balans; ECX/EDX zijn vluchtig. Retour via `ret 10h`; de caller ruimt deze vier argumenten niet op. De originele getter laat geen floating-pointreturn achter. Eigen rekenwerk mag geen x87-stackwaarden achterlaten of de controlword blijvend veranderen. Gebruik voor de eerste technische adapter uitsluitend integerwerk waar mogelijk; geen exception over deze grens en geen gameplayacties vanuit scoreberekening.

Voor een smalle eerste ingreep zonder wijziging van de vergelijker: **bruikbare kwaliteit 1..32767, nul voor expliciete afwijzing**. Signed `cmp ax,cx` op 20078524 met jle/jl ordent; 32768..65535 zouden als negatief gelden. Bij gelijke score volgt de bestaande tievolgorde: kleinere x, daarna kleinere y krijgt voorrang. Laat bonus/formule in een bredere tussenrepresentatie rekenen en expliciet begrenzen; geen wraparound en geen louter unsigned clamp op 65535.

Op **2007aa5f–62** wordt signed BX>0 geëist. **2007aa7c–8e** sign-extendt BX naar een integer, converteert naar double en geeft die aan GoalSettle 20048600 door. De latere kwaliteitgetter op GoalSettle+48 is bestaand bewijs, geen nieuw rolmetadataformaat. Een rijkere kwaliteitsrepresentatie buiten dit contract vraagt een apart ontwerp.

## Gekozen uitvoerbare invoegroute

**Ontwerp-/implementatieroute, nog niet toegepast:** plaats zelfvoorzienende x86-code in een nieuwe RX-sectie, bijvoorbeeld `.h1`, van de proef-DLL. Alle drie callplaatsen krijgen **E8 rel32 + 90**: vijf bytes relatieve call en één NOP. Na `ret 10h` wordt de NOP uitgevoerd en gaat de originele code verder op de bestaande zes-byte grens. Er worden geen instructieprefix, branch of SEH-proloog doormidden geknipt.

De offline PE-controle toont:

- PE32 / x86, machine 014c, vier bestaande secties. Vrije 40-byte nulheader op bestandsoffset **250h**, vóór eerste raw sectie/headergrens **400h**.
- Bestaande image eindigt op **RVA d4000**. Nieuwe sectie kan beginnen op **d4000**, raw bij **a1400**. SectionAlignment **1000h**, FileAlignment **200h**. Dit zijn startwaarden voor deze exacte binary, geen universele patchadressen.
- Relocations aanwezig en niet gestript; certificaatdirectory leeg. Bestaande imports zijn KERNEL32 en MSVCRT.

Een latere bestandspatcher moet sectionheader, NumberOfSections, SizeOfImage, codegrootte en raw-/virtualafmetingen coherent schrijven, payload/headers controleren en alleen de proefkopie muteren. Bestaande exports, entrypoint, imports, relocations en secties behouden. Gebruik rel32 voor eigen calls en EIP-relatieve moduleadresbepaling (`call/pop` plus RVA-delta) voor g_settle_ai; dan ontstaan door deze adapter geen nieuwe absolute fixups. Absolute adresconstanten zouden juist correcte extra relocations vereisen.

**Laadroute:** code blijft onderdeel van dezelfde robotcom-PE die de game al als AI-DLL gebruikt. De bestaande code bereikt de nieuwe sectie rechtstreeks via E8; geen tweede DLL, nieuwe import, externe initializer of bijzondere DllMain is nodig. Uitvoerbaarheid door de Windows-loader is hier een PE-onderbouwde verwachting; laden van een gewijzigde proef-DLL is pas een fase-C-waarneming. Geen claim dat bestaande engine-interface beschikbaarheid op zichzelf moddingondersteuning bewijst.

De gedeelde adapter kan conceptueel `kwaliteit(AiMain, World, signed16 x,y,z)` uitvoeren, originele World+168 oproepen voor fallback/basis en eigen kenmerken via bestaande vtablequeries lezen. Voor fallback moet zij oorspronkelijke callbackargumenten opnieuw pushen en niet recursief zichzelf oproepen: de gekozen route verandert alleen drie callplaatsen, niet World+168.

## Kenmerken en minimale ontwerpvoorwaarden

Reeds bewezen datatoegang kan worden hergebruikt; geen nieuw compleet kenmerkenonderzoek:

| Gameplaykenmerk | Beschikbare route | Nog afzonderlijk uit te werken |
| --- | --- | --- |
| Production | World+a8 geeft echte terreinindex; bergen **8/20/22**, bewezen footprint van twintig omliggende tiles; zie [TERREIN-EN-IMPROVEMENTS](TERREIN-EN-IMPROVEMENTS.md) | Drie **bruikbare** bergen, voedselonderhoud, overlap/toekomstig gezamenlijk plan en ontwikkeltijd vragen eigen concrete eerste featurekeuze |
| Science | Bestaande terrein-/food-/improvement-/techinterfaces in hetzelfde rapport | Groei, drie aanlegbare foodtiles en ontwikkeling volgens afgesproken timing; numerieke waardering niet gekozen |
| Monopoly | World+b4 geeft GOOD_INDEX; AiMain+2c geeft eigen Player-interface; Player+b8 levert per stad/good lokale en beschikbare tellingen; AiMain+8c eigen CityAgents | Rijksaggregatie, handelsgeschiktheid en reserveringen zijn ontwerpwerk; niet iedere getelde good is vrij inzetbaar. Zie [GOODS-EN-HANDELSROUTES](GOODS-EN-HANDELSROUTES.md) |

De eerste adapterberekening moet **zuiver en ongecachet** zijn: geen globale wereldscore schrijven, geen nieuwe opgeslagen metadata, geen wijziging van rijksbehoefte tijdens heapvergelijkingen. Dezelfde eigenaar/positie/formule levert binnen één heapgebruik dezelfde uitkomst. Een reservering die na iedere GoalSettle verandert kan de al opgebouwde heap ongeldig maken; zulke dynamische planning vraagt een latere snapshot/herbouwroute, geen stilzwijgende toevoeging aan deze eerste hook.

Verdere voorwaarden vóór uitvoering:

1. Exacte DLL-hash en callbytes in de feitelijke proefkopie controleren; alle RVA's tegen werkelijk geladen modulebasis interpreteren. Geen koppeling aan niet-passende civctp.map.
2. Native payload reproduceerbaar bouwen: voor de kleine ABI-adapter kan een controleerbare assembler/byte-emitter zonder externe imports volstaan; uitgebreidere featurecode vereist een passende x86-bouwroute. Geen compiler op PATH gevonden door root, geen toolchain geïnstalleerd of bronproject geclaimd.
3. Contextcontroleren: niet-null AiMain, passende World-pointer en ondersteunde laag; voor ongedekte context/laag originele score teruggeven. Geen langdurige opslag van raw eigenaarpointers.
4. Eerste feature en scorebereik expliciet door ontwerper kiezen. De toekomstfunctie en urgentie onderscheiden; drie bergen alleen zijn nog geen voedselhaalbare productiestad. Geen volledig einddoel vervangen door één technische bonus.
5. Activatieproef laat nieuw opgebouwde kandidaten én nieuw gecreëerde goals zien. Bij oude goals is herberekening/invalidation niet door deze route bewezen. Voor het eerste pakket een startsituatie zonder zulke oude doelen gebruiken of die concrete activatievraag vóór C oplossen; geen volledige savecyclus reconstrueren als standaardopdracht.
6. Rollback: originele proef-DLL met hash, payload/patchmanifest, bron/buildrecept en ongewijzigde beginsave bewaren; variant-save niet als herstelde referentie presenteren. Gameproces herstarten voor DLLvervanging hoort bij C.

## Controles, bewijsgrenzen en overdracht

[score-hook-h1-inspect.py](BINAIR/score-hook-h1-inspect.py) leest uitsluitend beide referentiebinaries, vergelijkt hashes/mapbinding, controleert de drie volledige callinstructies en vrije sectionheader, en disassembleert de echte getterwrapper tot `ret 10h`. Alle assertions zijn geslaagd; DLL-hash na lezen gelijk. Geen emulatie, aangepaste bytes, spel- of laadproef. Het bestaande disassemblagehulpmiddel is uitsluitend voor de genoemde functies/targets gebruikt.

**Geen aangetoond structureel obstakel voor deze smalle invoegroute.** Nog te bouwen payload, daadwerkelijke loaderacceptatie en runtimecorrectheid zijn voorwaarden voor het latere uitvoeringspakket. Masker-/bereikbaarheidsuitzonderingen, dynamische reserveringen, oude goalvernieuwing en complete production/science/monopolyformules worden concrete vervolgvragen zodra de gekozen eerste feature ervan afhangt. Geen extra analysepakket gestart.

Overgedragen aan ctp_ontwerper via root: werk één reproduceerbaar adaptervoorstel uit rond de drie scorecalls, ABI/PE-/scorecontract en contextfallback; definieer daarna het eerste gameplaykenmerk en passende kandidaatpaar-/herstelproef. Deze H1-analyserun stopt na overdracht; geen achtergrondactiviteit.
