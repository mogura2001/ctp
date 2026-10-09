# B2: geheugen voor een eenmalig voltooide opening

Gerichte fase-A-terugvraag, **bijgewerkt 8 oktober 2026, 09:30 Europe/Amsterdam**. Gameplaydoel: iedere normale Deity-AI volgt de gezamenlijke opening totdat haar actuele stadsaantal minstens N is en Theocracy daadwerkelijk actief is. Daarna mag zij normale latere regeringen kiezen zonder opnieuw de opening in te gaan. N25/30 blijft gebruikers-/ontwerpparameter. Alleen-lezen onderzoek; geen build, binarypatch, spelstart, levende game-uitlezing of nieuwe emulator. De eerste09:22-blokkade is met de hieronder bewezen echte enginearchive opgelost; haar oorspronkelijke negatieve zoekresultaten blijven als onderzoekshistorie herkenbaar.

## Uitkomst en grens

Het minimale geheugen is **één eigen voltooiingsbit per AiMain**, met beginwaarde0 en uitsluitend de overgang0→1 bij gelijktijdig `cities>=N && active_government==Theocracy`. Een eigen type0 FliSymbol met null doublepointer kan dit bit tijdens de levensduur van de FLI-engine als0.0/1.0 dragen. De gewenste gate wordt `opening_required = !opening_completed`; stadverlies of een latere regering wist voltooiing niet.

**Dat symbool wordt momenteel niet geserialiseerd.** `FliSymbol::Serialize2003b740` is lege code. Load bouwt de FLI-engine opnieuw. Alleen de vorige inputroute toevoegen levert daarom geen savebestendige latch.

**Eén technisch onderbouwde route is nu beschikbaar:** eigen latch, optioneel gemarkeerd record onmiddellijk na de oorspronkelijke AiMain-savepayload, herstel na de oorspronkelijke AiMain-load, capture/restore rond bestaande fuzzyreload. Het blijft een gedeelde stream, maar de werkelijke enginearchive heeft nu bewezen buffer/cursor/whole-archivelengtevelden. Een bounded directe peek kan bij afwezige marker de cursor volledig ongemoeid laten. Geen afzonderlijke AI-bloblengte is nodig voor dit inline-recordcontract.

De ontwerper kan hiermee een concrete faseovergang en compatibele variantload uitwerken. Loaderacceptatie van de latere adapter, foutafhandeling en gameplay blijven fase-C-verificaties; er is geen toegepaste of gemeten verbetering. Andere scenario-/netwerkarchiveimplementaties worden alleen ondersteund wanneer zij hetzelfde gevalideerde contract hebben; de variantadapter mag een afwijkende vtable niet als dezelfde layout behandelen.

## Bewezen enginearchive en minimale peekroute

**B:** de gewone savefunctie begint op51bfd0; op51bff3–f6 wordt haar lokale archive `[ebp-2c]` via constructor586770 gemaakt. Die schrijft op586778 vtable7462a8 en initialisatievelden. De al bewezen51c6ea–f4 geeft precies deze lokale archive aan manager52dbe0, die haar naar RobotCom Save en AiMain::Save doorgeeft. [Callerconstructie](BINAIR/opening-memory-b2-caller-archive-init.txt), [constructor](BINAIR/opening-memory-b2-real-archive-constructor.txt).

De gewone load maakt haar lokale archive `[ebp-28]` op51caa1–a4 met dezelfde constructor. Het opgeslagen ongecomprimeerde byteaantal wordt op51cc80–ae gelezen;51ccb5 roept586810 met die lengte aan. Deze functie maakt een buffer met exact dat aantalbytes, zet+0c en+10 beide op de lengte,+14 en+18 op de nieuwe buffer,+8 op0. De savepayload wordt op51cd43 naar deze buffer gedecomprimeerd;51cd53–5b vergelijkt de werkelijk geproduceerde lengte met het opgeslagen aantal en gaat bij verschil naar de fouttak. [Loadconstructie](BINAIR/opening-memory-b2-load-archive-binding.txt), [buffer-/lengtebinding](BINAIR/opening-memory-b2-load-buffer-length.txt).

Dezelfde archive gaat op51d20b–15 naar408ff0. Deze leest haar argument op4090e8 en geeft het als derdeargument aan4f6400 op4090eb–f0. Deze routine herneemt precies dat argument op4f7f5f uit`[ebp+10]`, geeft het op4f7fa3–a6 aan managerconstructor52cdf0, die op52ce85–8b hetzelfde argument aan52dbe0 doorgeeft. De loadbranch52dec5 geeft dezelfde archive aan RobotCom::Load. Alleen deze argumentdoorvoer is onderzocht; overige gameplaywerking van de grote initialisatiefunctie is geen nieuwe analyse. [Doorvoer](BINAIR/opening-memory-b2-load-manager-archive.txt), [eindbinding](BINAIR/opening-memory-b2-archive-argument-through-init.txt), [managercall](BINAIR/opening-memory-b2-load-manager-constructor-call.txt).

| Werkelijk enginearchiveveld | Betekenis, uitsluitend aan enginebytes gebonden |
| --- | --- |
| +0 | Vtable7462a8; gebruik actuele enginebase+3462a8, geen vaste absolute adresaanname. |
| +8 byte | Storingmode;0 tijdens normale load,1 bij saveconstructie. |
| +0c uint32 | Gealloceerde buffercapaciteit. |
| +10 uint32 | Totaal geldige archivebytes; bij load exact gecontroleerde ongecomprimeerde lengte. |
| +14 pointer | Bufferaanvang. |
| +18 pointer | Actuele read/writecursor. |

[Concrete vtable](BINAIR/opening-memory-b2-real-archive-table.txt): +0→586700 QueryInterface,+4→586710 AddRef,+8→586730 Release,+c→586930 Store,+10→5869f0 Load,+14→586c70 IsStoring. **QI586700 retourneert altijd80004002/E_NOINTERFACE**; daarom gaf de GUIDzoeker geen tabel. De juiste GUID blijft744e88, maar er is geen positieve QI/GUIDbinding te claimen. De concrete binding volgt uit constructor, argumentdoorvoer en daadwerkelijke Store/Load-slotcode. [Virtuals](BINAIR/opening-memory-b2-real-archive-virtuals.txt).

Load5869f0 kopieert uit+18 en verhoogt alleen die cursor; zij voert geen eigen boundscheck uit. Store586930 groeit de buffer wanneer nodig, verplaatst+14 én+18 en verhoogt+10 met het opgeslagen byteaantal. De nieuwe saveadapter moet dus echte Store+0c gebruiken; geen oude bufferpointer over een Store-call behouden.

**Technisch aannemelijk adaptercontract, geen huidige runtimefunctie:** na geslaagde oorspronkelijke AiMain::Load, met eigen AiMain en dezelfde archive nog op de adapterstack:

1. Valideer de bekende engine/build en concrete vtable/slots, loadmode0, niet-nul bufferaanvang en `size<=capacity`. Reken als unsigned32 met expliciete overloopcontrole; eis dat het bufferinterval geldig is. Bij een afwijkende archiveklasse geen layoutread of recordconsumptie.
2. Eis `cursor>=buffer`; bereken pas daarna `offset=cursor-buffer` en eis `offset<=size`. Bereken `remaining=size-offset`. Zo wordt `cursor+recordlength` niet vooraf met mogelijk overflow gevormd.
3. Bekijk hoogstens de vastgelegde marker-/recordlengtebytes **direct binnen dit interval**, zonder Load-call of cursorwrite. Bij te weinig bytes voor een volledige marker of afwezige marker blijft de cursor identiek en het nieuw geregistreerde completionbit0: legacy/T0.
4. Bij volledige eigen marker: eis voldoende bytes voor het vaste record, juiste formaatversie/lengte, civ-ID en completionwaarde0/1. Civbinding kan gelezen worden uit AiMain+20: bestaande GameState-slot+c-initbinding; Load herstelt het op20002d5c. Gebruik geen wereldturn als historische voltooiing. Bekende marker met fout/truncatie is een variantformatfout, geen legacyfallback.
5. Consumeer pas het volledig gevalideerde record via echte Load+10 naar eigen tijdelijke opslag; schrijf het completionbit naar het nieuwe eigen FliSymbol. Behoud oorspronkelijk EAX/loadresultaat en ABI; één record per AiMain. De cursor staat daarna exact bij de volgende oorspronkelijke manager/civgegevens.

Een vast record van bijvoorbeeld32bytes (16-byte marker, versie, recordlengte, civ-ID en0/1-vlag) maakt de maximale peekklein en voorspelbaar; deze indeling is een ontwerpvoorbeeld, geen bestaand saveformaat of toegepaste keuze. Ontwerper moet de marker exact kiezen en bekende versies expliciet behandelen. Legacy-next-civpresentie is0/1; kies een marker die daar niet op lijkt. De volledige marker voorkomt dat losse managerwaarden als een record worden geïnterpreteerd, inclusief de laatste-civgrens. Normale onveranderde T0 hoeft geen vlag te krijgen; elke nieuwe variant-save schrijft juist ook de expliciete0toestand.

De complete5-byte calls in RobotCom zijn geschikte voorgestelde adapters: Savecall2000fe2d→200027c0 en Loadcall2000fe51→20002c50. Saveadapter voert eerst oorspronkelijke save uit en schrijft daarna eigen record via Store; loadadapter voert eerst oorspronkelijke load uit en doet daarna bovenstaand peek/herstel. Dit is een onderbouwde aanpassingsroute, nog geen hook/build. Vtable-/enginehashchecks, stackbalans, resultaatbehoud, twee civs met verschillende flags, legacyload herhalen en variant0/1save-load zijn noodzakelijke latere technische verificaties.

## Dekking van de beslisketen

| Schakel | Huidige werking en bewijs | Benodigde ingreep / status |
| --- | --- | --- |
| Eerste echte fase-einde | Bestaande bewezen stedenread AiMain+8c→signed32 en Player+150-governmentquery; kennis/aanvraag/Anarchy is geen actieve Theocracy. | Zet eigen completionbit alleen wanneer beide actuele voorwaarden gelden. Hergebruik [B2-ingreeproute](OPENINGSFASE-INGREEP-B2.md). |
| Per-civ runtimeopslag | AddSymbol type0/nullpointer bewaart double in eigen FliSymbol+8/+c; engine staat op AiMain+c4. | Eigen completioninput, geen bestaand veld of globale-only latch herbestemmen. Geen section2-initdefault die bit wist; +68-mask en +c2 blijven onderscheiden. |
| Beginbeurt | FireRules2-call2003625b heeft actuele AiMain in ESI. | Lees bit, toets fase-einde alleen zolang bit0, schrijf completion/gate vóór oorspronkelijke FireRules. |
| Gewone save | RobotCom Save2000fe20→AiMain::Save200027c0. AiMain-save schrijft eigen scalars/objecten, Planner/AIP en als laatste16bytes van AiMain+24 op20002c42. | Savecalladapter2000fe2d; daarna eigen gemarkeerd record via bewezen engineStore+c. |
| Gewone load | RobotCom Load2000fe40→AiMain::Load20002c50. InitFuzzyOut-call20003c28 herbouwt engine; daarna bestaande laatste16bytes worden geladen op20003c3c. | Loadcalladapter2000fe51; daarna bounded peek en herstel in nieuwe eigen symbool, met civ-/versiecontrole en behoud van Load-resultaat/ABI. |
| Archivebegrenzing | Engine-managerserializer52dbe0 geeft dezelfde EBX-archive door aan interfaceserialize524fc0 en RobotCom Save52dccd; volgende civpresentie-/interface-/AI-gegevens volgen in dezelfde stream. Load doet overeenkomstig RobotCom Load52dec5. | Geen onafhankelijke bloblengte nodig: exact eigen marker plus gevalideerde whole-archivebounds laten de legacycursor ongemoeid. Geen archive-eindeaanname. |
| Fuzzyreload | AiMain::ReloadFuzzyLogic200061f0 neemt oude engine uit+c4, vernietigt die, zet+c4 nul20006217 en roept InitFuzzyOut20006243. | Een adapter rond uitsluitend deze bestaande reload moet completionwaarde op de eigen callstack vastleggen en na succesvolle nieuwe registratie terugzetten. Dit is een technisch aannemelijke ontwerpvoorwaarde, nog niet gebouwde/uitgevoerde route. |
| Nieuwe game | InitFuzzyOut20002179 maakt nieuwe per-civ engine. | Completiondefault0; geen carryover uit vorige game of oude pointers. |
| Opnieuw dezelfde T0 laden | Legacy-save bevat geen completionbit; gewone Load herbouwt FLI. | Afwezige marker geeft0 zonder cursorwijziging, ongeacht voorafgaand variantverloop; later C-verifiëren. |
| Normale/fallback/barbaren | Bestaande B2-overdracht onderscheidt zes normale profielen, Default-fallback en barbaren. | Gate voor normale civs/fallback; barbarenbeleid ongemoeid. Een inert eigen symbool alleen is geen barbarenbeleid. |

## Direct machinecodebewijs

**B, passende AI-map:** robotcom.dll SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, imagebase20000000, timestamp37b894e7. Het bestaande hulpmiddel controleert map/imagebase/timestamp vóór disassemblage. [AI-save/load/reload](BINAIR/opening-memory-b2-ai-archive.txt), [symbolserializer/archivefuncties](BINAIR/opening-memory-b2-symbol-and-archive-boundary.txt).

`Serialize@FliSymbol2003b740` bevat alleen `push ebp; mov ebp,esp; pop ebp; ret4` op2003b740–744. Er worden geen symboolwaarde, archivebytes of pointers gelezen/geschreven. Een aanwezige functienaam in de map bewijst dus geen ondersteuning.

RobotCom-vtable20089728 bevat op **+10 Save2000fe20**, op **+14 Load2000fe40**; [slotbewijs](BINAIR/opening-memory-b2-robot-slots.txt). Beide lezen AiMain uit RobotCom+8. Let op de slotcorrectie tegenover de eerdere formulering in ACTIVATIE-ONDERZOEKSLIJST.md: enginecall52dccd is de **Save**-branch, niet Load. De ownerketen/civindex blijft geldig; de echte loadcall in dezelfde serializer staat op52dec5.

**B, engine zonder civctp.map:** engine SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, imagebase400000, timestamp37d6f702. [Gericht vervolg manager-serializer](BINAIR/opening-memory-b2-engine-ai-boundary.txt) hergebruikt de eerder bewezen52dbe0-caller/ownerketen. Op52de57 wijst ESI naar manager+218c;52deb9 schrijft de nieuwe RobotCom op+80;52dec3 pusht de actuele civ-interface,52deb8 dezelfde archiveEBX en52dec5 roept slot+14 aan. Daarna gaat de loop op52dede–ee5 naar de volgende civ. Deze route levert geen aparte AI-lengte op.

De dump [gedeelde archivecaller](BINAIR/opening-memory-b2-engine-archive-caller.txt) bevestigt51c6ea–f4→52dbe0 met dezelfde stackarchive; [aanvullende aanroepcontext](BINAIR/opening-memory-b2-shared-archive-construction.txt) toont de archive ook bij de voorafgaande Player-/enginegegevens. Gedeeltelijke ranges kunnen bij hun eerste adres midden in een instructie beginnen; uitsluitend genoemde gecontroleerde instructiegrenzen gelden als bewijs.

**Historisch09:22, vervangen door enginebewijs hierboven:** de DLL-eigen `CivArchive::Load20026e90` kopieert vanuit object+18 en verhoogt die pointer, zonder lokale grenscheck. Dit bewees niet dat de engine dat DLL-concrete object aanbiedt; die offsets waren toen geen rechtvaardiging voor layoutreads. Het nieuwe onderzoek bindt gelijksoortige velden onafhankelijk aan de werkelijke engineconstructor/vtable/code, en heeft geen DLL-layout aangenomen.

De eerdere [archive-interfacecheck](BINAIR/opening-memory-b2-engine-archive-interface.txt) vond de juiste GUID op744e88 maar geen gebonden concrete tabel. QI die altijd E_NOINTERFACE retourneert verklaart dit negatieve resultaat. De manager bewaart per volgende civ eerst een4-byte presentie0/1 op52dcb2/52dce2; na de laatste civ volgen andere managergegevens vanaf52dceb. Het nieuwe contract gebruikt directe bounded peek, geen consumerende0/1read of rewind/replay.

## Ontwerpvoorwaarden voor de gekozen richting

De completionwaarde en de afgeleide gate moeten eigen symbolen zijn; de naam `opening_completed` is voorlopig en bestaat momenteel niet. De ontwerper mag de bitsemantiek en reloadcapture uitwerken. Reset0 geldt bij nieuwe game en legacy-load; reload van dezelfde civ bewaart de huidige0/1 en mag geen oude symboolpointer behouden. Bij een fout/missend nieuwe symbool mag geen bit uit een andere civ of vorige game worden gebruikt. Init/defaultmaskers mogen het herstelde bit niet terugzetten tijdens eerste of volgende FireRules.

Een eventuale trailer moet herkenning, formaatversie, civbinding, beperkte lengte,0/1-validatie en foutafhandeling bevatten. Originele T0 zonder trailer blijft exact haar oorspronkelijke bytes gebruiken en wordt incomplete. Nieuwe variant-saves moeten ook vóór voltooiing expliciet0 en erna1 bewaren. Nieuwe saves terugladen in de originele DLL is geen bewezen compatibiliteit: het is een nieuw variantformaat dat apart gelabeld moet worden. Corrupt/onbekend formaat niet stilzwijgend als legacy interpreteren wanneer een bekende marker aanwezig is.

Herstel van een variantproef: oorspronkelijke bestanden/DLL terugzetten en de oorspronkelijke onveranderde T0 gebruiken. Een nieuwe variant-save met extra inlinebytes aan de originele DLL aanbieden zou de gedeelde leesvolgorde verschuiven; die richting mag niet als compatibel worden gepresenteerd.

De trailer kan niet worden gebaseerd op ‘rest van deze archive is mijn blob’, omdat volgende civs/enginegegevens daar staan. Zij mag ook niet een opgeslagen AIP-naam, knownTheoc, leeftijd/timer of bestaande regerings-/plannerwaarde als historische voltooiing gebruiken. AAIP-verschillen leveren voor deze eigen latch geen savebewijs; de bestaande identieke loader/set_govern zijn lessen uit bestanden, geen gemeten fasegeheugen.

**A→B-overdracht09:30:** runtimebit, echte archivebounds, adaptercalls en huidige reset-/reloadgrenzen zijn voldoende beschreven voor één onderbouwd voorstel. De eerdere bounds-/peekblokkade is opgelost. Geen andere gameplayketen, volledige saveconstructorreconstructie, observer of sidecar opgezet. Volledige save-integriteit/runtimegedrag, parseracceptatie, ABI en latere regeringskeuze horen bij latere gerichte C-verificatie. Onderzoek stopt hier; geen volledige gamereconstructie als extra voorwaarde.
