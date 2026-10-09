# B2: afgeleide openingsvoorwaarde vóór de gedeelde FLI-regels

Gerichte fase-A-overdracht, 7 oktober 2026, 22:38 Europe/Amsterdam. Vraag: hoe krijgen alle normale persoonlijkheden een gezamenlijke opening die pas uitgaat bij voldoende steden én daadwerkelijk actieve Theocracy? Geen keuze tussen25/30, geen gameplaywijziging, spelstart of nieuwe emulator/test. De brede analyse blijft afgerond.

## Uitkomst

Eén technisch aannemelijke route is een **nieuwe, echt geregistreerde FLI-input**, voorlopig opening_required genoemd, met een lokale double in de FliSymbol van iedere AiMain. Registreer haar in InitFuzzyOut vóór de personality-parser en ververs haar onmiddellijk vóór de bestaande beginbeurt-FireRules-call. De bestaande AddSymbol/GetSymbol/RegisterInit/SetValue-methoden ondersteunen dit zonder een nieuw veld in AiMain of een nieuwe opgeslagen fasevlag:

    opening_required = (current_city_count < N || active_government != THEOCRACY) ? 1.0 : 0.0

N blijft een ontwerp-/gebruikersparameter. Onderzoek of een regeringsaanvraag telt niet als actieve regering; Anarchy houdt de voorwaarde dus waar. De inputnaam hierboven bestaat momenteel niet. Een nieuwe inputs.fli-declaratie en gedeelde regels/actions horen bij de latere wijziging.

## Dekking van de noodzakelijke keten

| Stap | Huidige werking / bewezen toegang | B2-ingreep of noodzakelijke voorwaarde |
| --- | --- | --- |
| Engine per civ | InitFuzzyOut2003cc70 maakt FliEngine en bewaart haar op AiMain+c4; actuele AiMain staat daar in ESI. | Voeg één input toe aan deze engine, vóór parsing. |
| Registratie vóór regels | Laatste bestaande AddSymbol-call200413da; SetCurrentEngine200413e6; personalityfilename200413f0; parser200413fd; Init/SortAllRules2004141f. | Calladapter bij200413da voert eerst de bestaande registratie uit, vervolgens de nieuwe inputregistratie. |
| Steden | FSFuzzyBeginTurnPre leest op20034fab AiMain+8c en laadt op20034fb1 het eerste signed32-veld; schrijft dit als fz_num_cities op20034fb3. | Lees dezelfde actuele civ-count rechtstreeks; gebruik geen overgebleven globale input van een andere civ. |
| Actieve regering | AiMain+2c is Player-interface; slot+150 →528f20 → echte Player+94. | Query slot+150 met de actuele Player-interface. Originele geladen Theocracy-index is3; bind deze aan de gebruikte governmentdatabase, niet aan een niet passende engine-map. |
| Verversing | FSFuzzyBeginTurnRules200356a0 heeft AiMain in ESI. Na eenmalige inputregistratie komt zowel eerste als volgende uitvoering bij20036253–25b. | Adapter voor de volledige5-byte call2003625b naar FireRules20038ff0: zoek eigen symbool, bereken waarde, SetValue, voer oorspronkelijke FireRules(2) uit. |
| Gebruik | FireRules initializeert sectioninputs, verwerkt regels en daarna actions in geregistreerde volgorde. | Nieuwe input mag geen section2-initwaarde hebben die haar actuele waarde overschrijft; gedeelde openingregels en load-actions moeten haar gebruiken. |
| Override | AIP-load vervangt alleen aanwezige categorieën; geen algemene reset per beurt; laatste schrijver per categorie wint. | Ontwerp guards/volgorde en expliciet herstel per getroffen categorie, inclusief research en governmentoutputs. |

Dit is een uitvoerbaar analysecontract, geen reeds gebouwde hook of bewezen gameplay-effect.

## Minimale input-/hookvoorwaarden

AddSymbol20038bf0 is thiscall: ECX=FliEngine, stackargumenten naam, double-pointer, defaultdouble, FLI_SYM; callee ret14h. De bestaande num_cities-registratie2003dcf7–dd07 gebruikt type0: input. **Gebruik AddSymbol type0**, niet AddExternalSymbol20038c20, dat type1 doorgeeft. Een null double-pointer is ondersteund: FliSymbol-constructor2003b6a0–bd schrijft de default dan naar symbool+8/+c; SetValue2003b7b3–c3 schrijft daar eveneens bij null pointer. Iedere civ heeft zo haar eigen waarde; geen extra gedeelde globale double nodig.

Na registratie GetSymbol200389e0 op de nieuwe naam en RegisterInit2003bf50 met section2. RegisterInit zet bit2 in symbool+c2, zoals de bestaande beginbeurtinputs op200357b4–c2. Dit is **een ander masker** dan +68: InitForSection2003b8df–91a overschrijft de waarde uitsluitend wanneer bit2 van +68 gezet is. Declareer de nieuwe input/membershipsets zonder initial/default-opdracht voor section2; controleer in fase C dat +68 bit2 nul blijft. Zo overleeft SetValue vlak vóór FireRules de sectioninitialisatie. RegisterInit is geen verversing van de waarde.

De adapter bij2003625b moet de oorspronkelijke thiscall FireRules(section2) behouden: ECX=AiMain+c4, reeds gepushte section2, originele return naar20036260 en stackbalans. Herstel registers/ABI die de omringende code gebruikt; geef de extra query haar eigen stackargumenten. Het Player-COM-governmentquery heeft de interfacepointer als expliciet stackargument en retourneert signed32 EAX. Geen hardcoded echte Playerpointer, geen geplande doelregering gebruiken.

De registratiehook moet ook werken wanneer ReloadFuzzyLogic200061f0 de engine vernietigt en via20006243 InitFuzzyOut opnieuw aanroept. Zoek het symbool bij de actuele engine; bewaar geen pointer over reload. De waarde wordt vóór iedere relevante beginbeurt afgeleid, waardoor een oude eventueel bewaarde waarde geen bron van waarheid is. Een complete saveketen is hiervoor geen analysevoorwaarde.

## Bestandsroute en semantiek voor ontwerp

De zes gewone beginturnCleric/Slaver/SciFew/SciMany/WarFew/WarMany.fli includen inputs.fli, set_govern.fli en aiploader.fli. Een gedeelde include/gate kan daarom hun bestaande aansturing gebruiken. De fallback beginturn.fli heeft set_govern/aiploader uitgecommentarieerd: zij moet expliciet in het ontwerp worden meegenomen wanneer Default onder alle normale persoonlijkheden valt. beginturnBarbarians.fli gebruikt wel inputs/set_govern, maar heeft de gewone aiploader niet. Houd barbaren buiten de gedeelde openingsregels; een inert geregistreerd symbool alleen verandert hun beleid niet.

Een input toevoegen garandeert nog geen gezamenlijke opening. Bescherm de gewenste regeringsrangen tegen concurrerende persoonlijkheidsconsequents; bescherming van de onderzoekslijst moet de echte actionvolgorde en gedeeltelijke overlays respecteren. Leg noodzakelijke ruimte-/dreigings-/gelukreacties expliciet vast. Een laatste gedeelde overlay is alleen correct voor de categorieën die zij bewust beheert en met benoemde uitzonderingen. Bij fase-einde moeten categorieën die de normale profielen niet herschrijven expliciet hun gekozen vervolgwaarde krijgen; het wegvallen van een load is geen herstel.

De afgeleide conditie is geen permanente latch: verlies van steden of Theocracy maakt haar weer waar. Indien het ontwerp een onomkeerbare eenmalige overgang verlangt, is dat een andere semantiek waarvoor toestand nodig is. Deze taak kiest die strategie niet. Beperk de nieuwe input tot section2; initial-section1-FireRules2004142c loopt nog vóór deze beginbeurtverversing.

## Bewijs en overdracht

**B**: oorspronkelijke robotcom.dll SHA2563025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44, imagebase20000000, timestamp37b894e7; robotcom.map past. Gerichte dumps: [registratie en beginbeurt](BINAIR/opening-phase-b2-registration-and-rules.txt), [registratie-/parser-/reloadvolgorde](BINAIR/opening-phase-b2-input-lifecycle.txt), [inputtype, null-pointeropslag en maskers](BINAIR/opening-phase-b2-input-contract.txt).

**T+B hergebruikt**: [architectuur](ARCHITECTUUR.md), [fuzzybeleid](FUZZY-BELEID-EN-DEFUZZIFICATIE.md), [AIP-load en overrides](AIP-LAADWERKING.md), [onderzoek/regeringsquery en overgang](ONDERZOEK-EN-REGERINGSKEUZE.md), met name BINAIR/research-government-engine-construct-change.txt. Engineadressen zijn aan echte interfacecode gebonden; civctp.map past niet en is geen adresbewijs.

Ontwerper kan nu één native registratie-/beginbeurtadapter plus gedeelde FLI/AIP-gate uitwerken. Bouw-/parseracceptatie, correcte maskers, verschillende civwaarden, gewone/fallback-/barbarenroutes en overgang bij werkelijk actieve Theocracy zijn latere C-verificaties; niet uitgevoerd. Geen technisch aangetoonde blokkade resteert voor dit voorstel. Volledige interpreter/scheduler/save/personalityreconstructie blijft buiten scope. Verse budgetcontrole22:37:32: week72%, vijfuur18%, stateok.
