# B2c: echte AIP-parser en begrensde uitvoerbaarheid

11 oktober 2026, 16:25 Europe/Amsterdam. Fase A, drie toegewezen vragen afgerond. Alleen bestaande bestanden gelezen en gevalideerde DLL-disassemblage naar stdout uitgevoerd; geen helper gemaakt, native call, spelstart, attach, installatie of patch. Ownership uitsluitend dit document en VOORTGANG-ANALIST-B2C-PARSER.md.

## Conclusie en benodigde ontwerpcorrectie

Het voorbereid pakket `PROEVEN/opening-b2/onderzoek-b2c/20261011T155803` bevat een concrete ontbrekende afhankelijkheid: alle acht nieuwe research-only AIPs beginnen direct met `Advancement_Element Advancements_List[MAX_ELEMENTS];` en missen `#include "aipdef.h"`. De volledige categorie is wel bytegelijk gekopieerd, maar die categorie is geen zelfstandig parserbestand. `aipdef.h` definieert zowel het structuurtype met `advancement_name[80]` als `MAX_ELEMENTS=200`. Originele `citywall_science.aip`, ook een onderzoeksprofiel, include deze header expliciet.

Vereiste B-correctie: plaats de bestaande headerinclude vóór de ongewijzigde categorie in ieder nieuw AIP, met gepinde bereikbare header in dezelfde AIPs-map. Behoud de exacte researchblokken/suffixen. Deze analyse verandert de kandidaat niet en trekt de rootacceptatie van blokgelijkheid/tekstplaatsing niet verder door naar parseracceptatie.

Een kleine toekomstige eigenprocesproef met de echte DLL-parser en loader is technisch aannemelijk en voldoende afgebakend. De bestaande B2-helper voert deze parser **nog niet** uit en kan niet ongewijzigd als parserbewijs dienen. Drie inhoudelijke callbacks en foutdiagnostiek volstaan voor deze partialroute; geen hele game of AIP-manager nabouwen. Dat is een route voor een B-voorstel, geen uitgevoerde native proef.

## Dekkingsmatrix

| Vraag / beslisketen | Huidige werking en bewijs | Uitkomst voor volgende fase |
| --- | --- | --- |
| 1. Bestand → iparser → researchlijst | Nieuw iparserobject per Load_AIP_File; type/define vereist expliciete include; eigen presence/count/naamresolutie | Onderbouwd; headercorrectie vereist |
| 2. Eigen 32-bit proces → echte parser/loader | Eigen AIP/AiMain, drie vtablecallbacks, echte CRT/imports, gerichte diagnostiek; bestaande loaderpatroon herbruikbaar | Technisch aannemelijk, niet aangeroepen; bounded B kan proef ontwerpen |
| 3. Research-only switch → andere categorieën behouden | Eigen researchpresencebit en pointer, gewone Switch_AIP; afwezigheid is geen wissen | Betekenisvolle native asserties bepaald; FLI en echte host apart open |

## 1. Bestaande parse- en laadroute

De gebruikte `CTP-og/ctp_program/ctp/dll/ai/robotcom.dll` en `robotcom.map` passen: timestamp `37b894e7`, preferred imagebase `20000000`, SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`. De bestaande `Analyseer-AI-DLL.py` controleert timestamp/base vóór iedere getoonde functie. `civctp.map` is niet gebruikt.

Hergebruikt bewijs: [AIP-LAADWERKING.md](AIP-LAADWERKING.md), [load-entrypoints](BINAIR/aip-load-entrypoints.txt), [researchparser](BINAIR/research-government-list-parser.txt), [switchcode](BINAIR/aip-load-switch-and-parser.txt), [constructor/init](BINAIR/aip-load-init-and-save.txt). Aanvullende directe interfaces zijn met hetzelfde bestaande disassemblyhulpmiddel gelezen, geen nieuw hulpmiddel.

- `AIP` constructor `200642a0`, thiscall, `(AiMain*, bool)`, `ret 8`, objectomvang `0xa08` uit managerallocatie. Roept `AIP::Init` `20063c20` aan en bewaart AiMain op `+800`. Alleen init raadpleegt voor deze route UnitDB via `AiMain+38`, vtableslot `+0c`, aantal voor eigen tijdelijke unitarrays; overige init is private opslag/standaardwaarden.
- `Load_AIP_File` `200628d0`, thiscall `(char* filename, bool force)`, `ret 8`, EAX objectpointer of null op expliciete file-open-fout. `force=true` voorkomt de gelijknamige-cachekortsluiting. Bestandnamen moeten binnen het naamveld `+804` passen; de bestaande openingnamen doen dat.
- `2006297d` alloceert een **nieuw 0x78-byte iparserobject**, constructor `2006ba60` thiscall `(AiMain*)`, `ret 4`. Deze zet struct/variabletabellen op nul (`2006ba91..99`) en init zijn eigen pathlijst. Geen vooraf geladen globale `Advancement_Element`-definitie of implicit aipdef-read.
- `200629b7..bd`: `AiMain+28` GameState, stdcall slot `+54` met de interfacepointer als argument, EAX aidatapad. Loader bouwt `%s\\AIPs` (`200629cd`), `Append_Path` `2006c9e0` thiscall `(char*)`, `ret 4`. Deze voegt een ontbrekende backslash toe en bewaart een eigen pathstring. `Parse_File` `2006bac0` thiscall `(filename)`, `ret 4`, opent met de echte CRT `fopen` en doorloopt gewone tokens/declaraties; include gebruikt recursief dezelfde parser op `2006b190`, zodat headerdeclaraties lokaal beschikbaar worden.
- **Onbekend type:** `Variable_Match` `20068e70` zoekt eigen structketen en daarna variableketen. Matchstruct levert typecode8 (`2006901f`); wanneer beide ontbreken ontstaat `-3` (`20069074..7f`: null → nul → minus3). De verse parser kent `Advancement_Element` niet. `Parse_File` dispatch `2006bd89..94` behandelt dit niet als de struct-arraydeclaratie; de struct-arraybranch van `Parse_Declaration` ligt op `2006b200`. Daardoor is een objectpointer als return van Load_AIP_File geen bewijs dat onderzoek daadwerkelijk geparsed is. De exact zichtbare foutmelding/return voor dit huidige foutbestand is niet native gemeten.
- De loader roept achtereenvolgens scalar-, unitklasse-, gebouw- en researchloaders op (`20062a5a/62/6a/72`). `Load_Scientific_Advancement_List` `2005f380` thiscall `(iparser*)`, `ret 4`, vraagt arraycount aan `Get_Struct_Array_Element_Count` `2006c960` thiscall `(name,int* status)`, `ret 8`. Afwezig: status1/resultaat−1; aanwezig: status0/count.
- Research loader wist vooraf bit14 van `AIP+7ac` en zet dit alleen na gevonden array (`2005f4b1..ba`). `AIP+7fc` wijst dan naar een 8-byte container: `+0 int* entries`, `+4 count`. Iedere naam wordt met echte `Get_Runtime_String_Field` `2006c850`, thiscall `(fieldpath,int* status,char* output)`, `ret 0c`, uit `%s[%d].advancement_name` gelezen. Daarna `AiMain+44` Science, stdcall vtableslot `+50`, `(Science*,char* name)` op `2005f4a4`, EAX advance-index; deze indices worden op volgorde opgeslagen. De loader zelf controleert de fieldstatus/negatieve naamindex niet opnieuw voordat hij verdergaat: asserties moeten beide afdekken.

## 2. Kleinste eigenprocesroute en afhankelijkheden

Hergebruik alleen het patroon van `PROEVEN/opening-b2/helper/Native.cs` en `native.ps1`: 32-bit proces, expliciet LoadLibrary van gepinde originele DLL, gewone importbinding/CRT/DllMain, RVA bij feitelijke modulebase en eigen allocaties. De bestaande `fixture` gebruikt LoadLibraryEx(flags1), kopieert het image en vervangt AddSymbol/GetSymbol/FireRules/archivecalls door expliciete stubs. Dat levert **geen** echte iparser of FLI-parseracceptatie; een ongebonden imagecopy met ontbrekende imports is ongeschikt voor FILE/CRT-parsercalls.

Voor toekomstige positieve partialcontrole zijn nodig:

1. Eigen AiMainopslag minstens door `+44`; `+28` GameStateinterface met slot54 terug naar gepinde, absolute staging-aidata-root, waar `AIPs/<candidate>` én `AIPs/aipdef.h` bereikbaar zijn. Geen globale gamepaden wijzigen of echte gamebestanden installeren.
2. `+38` UnitDBinterface met slot0c stabiele gedocumenteerde fixturecount voor constructorallocatie, begrensd/niet-negatief; dit is alleen shape-input, geen bewijs van een echte geladen UnitDB. Geen unitlijstnamecallback nodig zolang echte parse beweert dat Build_List_Classes afwezig is.
3. `+44` Scienceinterface met slot50 die iedere ontvangen naam logt en naar vooraf gepinde verwachte indexfixture vertaalt. Onbekende naam moet expliciet foutresultaat plus assertion opleveren; nooit default0. Dit bewijst werkelijke strings en volgorde vanuit de parser; stubindex is geen engine-ScienceDB-bewijs.

Callbacks zijn **stdcall** met expliciete interfacepointer op stack (caller doet geen add esp), niet thiscall. DLL-methodes hierboven zijn thiscall/ECX met eigen ret-cleanup. De bestaande eigen shims kunnen als patroon dienen; controleer ESP/nonvolatiles/x87 en gebruik echte allocator/destructorparen. AIP-geheugen blijft leven zolang een effectieve switched AIP naar zijn lijst wijst. Switch ownership op `+7cc` voorkomt dubbel vrijgeven; geen lijstbuffers blind zelf vrijmaken.

Voor negatieve header/path/fieldcontroles bovendien diagnostiek: `Report_Error` `200687d0` raadpleegt `iparser+24 → AiMain+28`, GameStateslot `+58` (`2006881f`) naar diagnostic-interface, diens slot `+10` (`2006882c`) ontvangt `(diagnostic*,char* text)`. Beide stdcall. Maak in B een eigen tekstrecorder voor deze exact begrensde callbacks, zonder enginehandlers/emulatie. `AiMain::Log` `200064f0` is in deze binary uitsluitend `ret 4`.

**Nuance optionalvelden:** de scalarhelpers zetten status vooraf op −17 (`2005f4f8`, `2005f601`). Get_Runtime_Int herkent dit op `2006c1a0..b2` en slaat ontbrekende-veldreport over op `2006c221..223`; Double heeft dezelfde sentinelroute. Dus geldige research-only partial hoeft geen foutmelding voor iedere afwezige scalar te genereren. Verkeerd type/ongeldige include/andere foutpaden blijven echte diagnostiekafhankelijkheden. Niet oplossen door parser of Load_AIP_File zelf te stubben.

Geen onvermijdelijke hele-hostkoppeling is in deze beperkte route gevonden. Niet geclaimd dat de bestaande helper al inzetbaar is; kleinste B-proef moet nog worden beschreven en C moet imports/ABI/pathfouten werkelijk controleren. Stop bij onverwachte nieuwe concrete interfacecall; scope niet uitbreiden tot manager/world/researchselectie.

## 3. Betekenisvolle toekomstige asserties en bewijsgrenzen

- Lees **alle acht** gecorrigeerde partials met exacte gepinde header en bytes; controleer force-load-return plus researchpresencebit14, eigen arraystatus0/count en werkelijk geschreven containercount, niet alleen een bool of ontbreken van crash.
- Vergelijk gelogde **alle naamcallbacks in volgorde** met categoriebron; opening_research/defaultrestore hebben 98 entries volgens de bestaande block-records, overige aantallen hun eigen gepinde record. Eerste twee Religion/Theocracy; ieder suffix volledig behouden. Vergelijk alle opgeslagen indices met de fixturemapping; geen onbekende naam/negatieve index. Dat bewijst parsergrammar/structfieldextractie en listmaterialisatie onder expliciete dependencies.
- Controleer overige lijstpresencebits4..13/15/16 uit, scalarpresence afwezig. Header definieert types/constanten, geen beleidslijsten. Controleer pointer/countvelden en echte parser getters, niet alleen regex van kandidaattekst.
- Een begrensde controlegeval zonder header moet ontbrekende daadwerkelijke Advancements_List/presence/count laten zien of expliciet parserfout; de bestaande foutkandidaat is nuttig als negatieve controle, zonder dit al als uitgevoerde test te presenteren. Apart onbereikbare header en onbekende naam voorkomt een permissieve stub die elk bestand goedkeurt.
- Voor het daadwerkelijke behoud: eigen effectieve AIP met geldige onderscheidbare unit/gebouw/wonder/scalarinhoud, researchpartial toepassen via **echte** `Switch_AIP` `20063720`, thiscall `(sourceAIP*)`, `ret 4`. Researchbit14branch `20063b85..de` vervangt de hele researchpointer; andere afwezige categorieën moeten exact behouden. Hou bronnen/containerlifetime vast. Controleer de bekende uitzondering: retreat eval/exec worden altijd −999999, en naamveld wordt laatste load. Vergelijk daarom de relevante behoudvelden gericht, geen onjuiste eis dat elk objectbyte ongewijzigd blijft.
- Restorepartial→openingpartial→restorepartial toont eigen onderzoeksvervanging en behoud onder drie expliciete switches. Dat bewijst nog geen door FLI werkelijk gekozen load of sectionvolgorde.

**Volgende afzonderlijke FLI-afhankelijkheid:** de echte FLI-parser moet actuele include-root, external inputregistraties en de volledige six/default beginsection naar symbolen/actions opbouwen. Bestaande AIP-controle gebruikt synthetische symbolen/lege rules; B2a-helper stubt AddSymbol/GetSymbol/FireRules. `FliEngine`constructor `200383e0` maakt echte symtab/functab en sections; `_fli_RunParser` `200426e0` roept fileopen/`_fli_Init`/yyparse aan, `_fli_parse_error` op `200cbe74`. Dit is een afzonderlijke registratie/include/callbackbinding, geen rechtstreeks bewezen B2b/B2c fullparse. Binnen deze A-taak geen nieuwe FLI/frameworkroute uitgewerkt; niet nodig om de headercorrectie en het onderbouwde partialvoorstel over te dragen.

Onbewezen blijven FLI rule/actionregistratie van de gewijzigde files, echte opening_required-input uit B2a, true/false-late overridevolgorde, eigen government-outputeffect, managerlifecycle in een game, save-/load-/reload van de samengestelde toestand, echte advance-name→indexdatabase, onderzoekselectie/vereisten en de benchmarkuitkomst. De partialparserproef moet deze expliciet buiten haar passclaim laten.

## Overdracht

Drie van drie vragen beantwoord op machinecode/bestandsniveau; geen runtimeclaim. Eerst B-correctie van de acht bestandheaders en vernieuwde tekstreview. Daarna kan de ontwerper een kleine eigenproces-AIP-parser/switchproef met bovenstaande meetlat voorstellen. FLI/realhost blijft een aparte volgende poort. Geen verdere brede analyse vereist voor deze overdracht.
