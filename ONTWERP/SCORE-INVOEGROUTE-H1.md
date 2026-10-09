# H1: score-invoegroute en eerste afzonderlijke gedragsproef

7 oktober 2026, 21:50 Europe/Amsterdam. Fase B, na de door root geaccepteerde [H1-overdracht](../ANALYSE/INGREEP-LOCATIESCORE-H1.md) van 21:43. Alleen voorstel; geen payload gebouwd, DLL aangepast, spel bediend of nieuwe runtimeproef uitgevoerd. Root beheert de formele B→C-vrijgave. Dit document vult H1/B3 in [VERBETERPLAN](VERBETERPLAN.md) aan; de overige projectroute blijft gelden.

## Voorstel en doel

Voeg aan uitsluitend de proef-DLL één RX-sectie toe met een kleine native scoreadapter. Vervang de drie aangetoonde scorecalls gezamenlijk. Verifieer eerst een identiteitsvariant die dezelfde signed16-score teruggeeft. Bouw daarna, afzonderlijk vergelijkbaar, dezelfde adapter met één gameplaykenmerk: **verlaag een positieve score boven 1 met precies één punt wanneer het stadcentrum een berg is**. Dit is de kleinste representabele gedragsproef voor de voorkeur naast bergen te vestigen uit PROJECTDOELEN §7 en LOCATIESELECTIE. Het is een expliciete ontwerpkeuze/hypothese, geen bewezen optimaal gewicht, compleet productiestadbeleid of gerealiseerd doel7.

De uiteindelijke productiestad blijft minimaal drie gelijktijdig bruikbare bergwerkplekken plus haalbaar voedselonderhoud voor grootte4, met mijnontwikkeling en de afgesproken voedseltechnologie/timing. Science, monopoly, wonderbehoefte, urgentie en gezamenlijke benutting blijven einddoelen. De echte uitzondering voor stichting op een berg — benodigde bergen zijn anders niet bereikbaar — wordt door deze proef **niet** vastgesteld. Er komt daarom geen nieuw verbod of nulscore voor een bergcentrum. Een berglocatie met duidelijk betere oorspronkelijke kwaliteit kan nog winnen; ook dat is een begrenzing van deze proef.

## Huidige beslissing en aangetoonde oorzaak

De [oorspronkelijke score](../ANALYSE/LOCATIEKWALITEIT.md) groepeert huidige voedselopbrengsten, waardeert productie/goud en good-aanwezigheid, maar kent geen expliciete regel voor behoud van een berg als gewone laborerwerkplek. Een stadcentrum wordt door de [open-werkplekfilter](../ANALYSE/IMPROVEMENTCONSTRUCTIE-EN-STADSGEBIED.md) uitgesloten. Het ontbreken van die voorkeur is een aangetoonde beleidslacune; hiermee wordt niet beweerd dat iedere huidige bergstichting fout is of dat de huidige formule het centrum economisch volledig negeert.

FLI/AIP is eerst onderzocht: `settle_value_coef`, packing, limieten en typebonussen sturen de bestaande score/filters, maar herkennen geen bergcentrum, drie bruikbare bergen, toekomstvoedsel of gelijke good-identiteit. [AAIP](../ANALYSE/AAIP-LESSEN.md) wijzigt algemene packing/prioriteiten, niet deze berekening. Een hoger gewicht verandert de ontbrekende beslissing niet. Aanvullende native logica is hier nodig. De modroute berust op bewezen complete callinstructies, ABI en PE-invoegruimte; een aanwezige gegevensinterface alleen bewijst geen modding-hook.

| Punt | Huidig | Voorgesteld |
| --- | --- | --- |
| 200784bb / 20078517 | Gedeelde World+168-cache voor beide heapkandidaten | Dezelfde adapterwaarde voor beide kandidaten |
| 2007aa35 | Cachewaarde opnieuw ophalen; signed BX>0 | Dezelfde adapterwaarde bij nieuw GoalSettle |
| GoalSettle+48 / 200488e3 | Kwaliteit als double × settle_value_coef | Bestaande keten ontvangt nieuwe integerkwaliteit; geen vierde hook |
| Oude opgeslagen goals/cache | Kunnen oorspronkelijke waarden behouden | Wereldcache blijft intact; alleen nieuwe reads/goals volgen adapter |
| Maskers/quota/legaliteit/transport | Filters vóór/na score | Dit pakket verandert hun werking niet |

## Twee kleine varianten en volgorde

1. **H1-I, technische identiteit:** drie calls plus nieuwe sectie; adapter roept oorspronkelijke getter en retourneert `sign_extend(AX)`. Dit is geen gameplaywinst. Offline ABI/PE-validatie gaat vóór een begrensde native loadercontrole en latere T0-activatiecontrole.
2. **H1-M, eerste gameplaykenmerk:** onafhankelijk van de oorspronkelijke DLL bouwen met exact dezelfde infrastructuur, plus bergcentrumvoorkeur. Vergelijk met H1-I onder dezelfde overige bestanden. Een aparte buildvariant is een compile-time keuze, geen hot-loadswitch of nieuw saveveld.
3. Pas na review van uitkomsten: volledige productiongeschiktheid, daarna afzonderlijk science/monopoly/contextbeleid volgens VERBETERPLAN. Voeg geen feature toe alleen om de identiteitsadapter als eindresultaat te kunnen presenteren.

## Exact binary-/PE-contract

De onderstaande waarden gelden voor de overgedragen originele `robotcom.dll`: SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, timestamp `37b894e7`, imagebase `20000000`, machine014c/PE32. De engine-identiteit voor latere echte World-aanroepen is `civctp.exe` SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`; engine-map levert geen adressen.

De latere patcher werkt op een nieuwe kandidaatfile, leest uitsluitend het expliciet gekozen proefbestand en stopt bij iedere identiteitsafwijking. Geen fuzzy search naar vergelijkbare bytes, geen reeds gepatchte DLL als bron. Bewaar de werkelijke proef-DLL en haar hash; als die niet de verwachte originele hash heeft, stop en laat root een gecombineerde baseline vastleggen. Alleen de drie sites worden gewijzigd:

| RVA | Original | Nieuw bij adapter-RVA A | Return/NOP |
| --- | --- | --- | --- |
| 784bb | ff9168010000 | E8 + little-endian signed32(A−784c0) + 90 | 784c0; vervolg784c1 |
| 78517 | ff9168010000 | E8 + little-endian signed32(A−7851c) + 90 | 7851c; vervolg7851d |
| 7aa35 | ff9168010000 | E8 + little-endian signed32(A−7aa3a) + 90 | 7aa3a; vervolg7aa3b |

A wordt bij dit pakket `d4000`. Een RVA wordt naar bestandsoffset vertaald met de bestaande sectietabel; schrijf geen VA als fileoffset. De 6-byte instructies worden volledig vervangen, zonder omliggende instructies te verschuiven. De drie sites samen vormen één infrastructuurwijziging: alleen de doelcall aanpassen zou kandidaatordening missen.

Voeg de nulheader op fileoffset250h toe als `.h1` (8 bytes naam met nulvulling), VirtualAddress d4000h, VirtualSize L, PointerToRawData a1400h, SizeOfRawData align(L,200h), Characteristics **60000020h** (code, read, execute; geen write). Reloc/line pointers en aantallen0. Hercontroleer vrij headerbereik250h..277h en SizeOfHeaders400h. Bereken de start ook uit de huidige secties/filelengte en assert dat die de overgedragen waarden geeft; onverwachte overlay of overlap is stopreden.

NumberOfSections4→5; SizeOfImage wordt align(d4000h+L,1000h); SizeOfCode neemt toe met align(L,200h). SizeOfHeaders, entrypoint, imports, exports en bestaande sectionheaders/directorys blijven behouden. Stel de checksum reproduceerbaar op de berekende PE-checksum in; noteer haar wijziging in het manifest. Timestamp blijft origineel voor adresbinding; variantidentiteit is eigen SHA256/manifest en mag niet uit de timestamp worden afgeleid. Geen imports of nieuwe initializer. Payload/rawpadding worden achteraan toegevoegd. Alle overige byteverschillen moeten verklaard zijn door exact deze headers, checksum, drie sites en toevoeging.

### Reproduceerbare payload zonder toolchaininstallatie

Gebruik in C een kleine **vaste byte-emitter in Python via de bestaande `py`-launcher**, geen compilerinstallatie of vrije tekstassembler. Bron/recept en manifest horen dan bij het uitvoeringspakket. Het onderstaande register-/stackrecept is de volledige semantische invoer; geef elke instructie een vaste x86-encoding, labels en twee-pass fixups. `struct.pack('<i', target−next_instruction)` vult E8/E9 en lange conditionele branches0F8x; gebruik steeds lange branches om omvang niet iteratief te laten veranderen. Directe veldoperanden zijn getallen/RVA's, geen absolute VA's. De aanwezige lokale Capstone/pefile uit het H1-inspectierecept kunnen het resultaat onafhankelijk teruglezen; geen pip-installatie nodig. De emitter mag alleen deze eindige instructielijst ondersteunen en moet onbekende labels/ranges weigeren.

| Patroon | Bytebasis / fixup |
| --- | --- |
| push ebp; mov ebp,esp; push ebx/esi/edi | 55 8bec 53 56 57 |
| sub/add esp,20h | 83ec20 / 83c420 |
| call L; pop esi; sub esi,imm32 | e8+rel32; 5e; 81ee+u32(RVA van L) |
| movsx eax,word ptr [ebp+d8] | 0fbf45 + d8 |
| mov [ebp+d8],eax / mov eax,[ebp+d8] | 8945+d8 / 8b45+d8 |
| mov [ebp+d8],ax | 668945+d8 |
| call [ecx+168h] / [ecx+a8h] | ff9168010000 / ff91a8000000 |
| ret10h | c21000 |

Voor de overige eenvoudige register-/veld-/compare-instructies wordt de concrete encoding in het C-bronrecept naast de assembleerregel vastgelegd en door de terugdisassemblage gecontroleerd. Dit is nu een bouwroute, geen gebouwd of bytegeverifieerd payloadbestand. C moet één deterministische payload opleveren en dezelfde invoer tweemaal naar dezelfde hash bouwen. Geen claim van compilerbeschikbaarheid; `python` op PATH was hier een Store-alias, `py` werkt.

**Relocaties:** E8 naar de adapter blijft correct bij rebase. In de payload levert `call L / L: pop esi / sub esi,RVA(L)` de werkelijke modulebase. `g_settle_ai` wordt gelezen als `[esi+c6fb4h]`, `g_settle_z` als het **word** op `[esi+c6fb0h]` (store2007aba3/2007ae27 gebruikt16bit); geen absolute 200c6fb4h-operand. `RVA(L)` is een constant offset, geen pointer die door de loader moet worden gerelocateerd. Eigen code/data-adressen worden eveneens modulebase+RVA of rel32. Daarom bevat de toevoeging geen nieuwe absolute fixups. Bestaande .reloc blijft intact. Iedere toekomstige absolute adresoperand vereist een nieuwe relocatie en valt buiten dit recept.

## Adapter: stack, fallback en concrete rekenroute

Op entree: `[esp+4]=World`, `[esp+8/+c/+10]=x/y/z` in dwordslots; alleen hun lage signed16-betekenis is bewezen. Na `push ebp / mov ebp,esp` staan die op `[ebp+8/+c/+10/+14]`. Bewaar EBX/ESI/EDI/EBP. Met `sub esp,20h` na de drie bewaarde registers zijn de locals vrij:

- B op ebp−10h; signed32 x/y/z op −14h/−18h/−1ch.
- terrain output op −20h; packed positie x/y/z op −28h/−26h/−24h (zes bytes).
- EBX=World, ESI=werkelijke modulebase, EDI=huidige AiMain uitsluitend gedurende deze call.

Uitvoeringsrecept, geen aanname van gelijke ABI voor verschillende World-methoden:

```asm
push ebp
mov ebp,esp
push ebx
push esi
push edi
sub esp,20h
mov ebx,[ebp+8]
movsx eax,word ptr [ebp+0ch]
mov [ebp-14h],eax
mov [ebp-28h],ax
movsx eax,word ptr [ebp+10h]
mov [ebp-18h],eax
mov [ebp-26h],ax
movsx eax,word ptr [ebp+14h]
mov [ebp-1ch],eax
mov [ebp-24h],ax
; originele World+168 blijft ongepatcht; dit is geen recursie
push dword ptr [ebp-1ch]
push dword ptr [ebp-18h]
push dword ptr [ebp-14h]
push ebx
mov ecx,[ebx]
call dword ptr [ecx+168h]       ; callee ret10h
movsx eax,ax
mov [ebp-10h],eax
; H1-I springt hier direct naar done.
; H1-M:
cmp eax,1
jle done                      ; nul/negatief en laagste positieve behouden
call L
L: pop esi
sub esi,RVA(L)
mov edi,[esi+0c6fb4h]
test edi,edi
jz done
cmp [edi+30h],ebx
jne done
cmp dword ptr [ebp-1ch],0
jne done                      ; alleen aangetoonde ground-feature
cmp word ptr [esi+0c6fb0h],0
jne done
mov dword ptr [ebp-20h],-1     ; sentinel, niet als terrein aannemen
lea eax,[ebp-20h]
push eax                      ; int32* output
lea eax,[ebp-28h]
push eax                      ; pointer naar 3 packed signed16 velden
push ebx                      ; expliciete COM this
mov ecx,[ebx]
call dword ptr [ecx+0a8h]      ; eigen ABI: callee ret0ch
; eax is successtatus, terrein staat in output
 test eax,eax
jz done
mov eax,[ebp-20h]
cmp eax,8
je mountain
cmp eax,20
je mountain
cmp eax,22
jne done
mountain:
dec dword ptr [ebp-10h]
done:
mov eax,[ebp-10h]
add esp,20h
pop edi
pop esi
pop ebx
pop ebp
ret 10h
```

De originele call wordt altijd uitgevoerd, ook bij fallback. Retourneer B bij ontbrekende AiMain, World-mismatch, unsupported laag, mislukt/ongekend terrein of H1-I. Featurecontext wordt niet tussen calls opgeslagen. Geen heap/reservations wijzigen, wereldscore schrijven of gameplayactie uitvoeren. De getoonde checks bewijzen geen algemene geldigheid van een willekeurige native pointer: oorspronkelijke callers gebruiken al een geldige World/AiMain; directe/indirecte CleanSettleQueue-context blijft een runtimecontrolepunt. Een stale pointer/access violation wordt niet als succesvolle fallback verkocht. Geen generieke pointerprobe/SEH-recovery of nieuwe lifecycle-infrastructuur toevoegen.

**World+a8 ABI-bewijs:** [bestaande DLL-caller](../ANALYSE/BINAIR/terrain-food-ai-improvement.txt),2001e0b1..2001e0d6, pusht outputpointer, positiepointer en World en roept vtable+a8. [Echte wrapper](../ANALYSE/BINAIR/engine-locatie-kenmerken.txt),5342e0, leest positie op ebp+c, schrijft terreinindex naar output op ebp+10, retourneert EAX=1 en eindigt53430c met ret0ch. [Positieconversie503f00](../ANALYSE/BINAIR/terrain-food-v2-position-worker-tech.txt) leest expliciet woorden op+0/+2/+4, normaliseert/wrapt en zet y om. Adapter geeft de oorspronkelijke interfacecoördinaten door, zonder eigen y−x-conversie; anders ontstaat dubbele omzetting. Terreinnamen8/20/22 zijn parsergebonden in [TERREIN-EN-IMPROVEMENTS](../ANALYSE/TERREIN-EN-IMPROVEMENTS.md).

Geen x87-rekenwerk, controlwordwijziging of exception over de ABI. ECX/EDX/EFLAGS zijn vluchtig; EAX is volledig sign-extended. De originele getter garandeert alleen AX. Alle 65536 AX-patronen blijven in H1-I exact dezelfde signed16-interpretatie houden; oorspronkelijke niet-positieve scores worden dus niet stilzwijgend naar nul geklemd.

## Rangschikkingcontract van de eerste feature

Voor H1-M:

```text
B = sign_extend(original_AX)
S = B - 1, als context geldig, z=0, centrumterrain in {8,20,22}, B>1
S = B, anders
```

Positieve outputs blijven1..32767; geen wraparound, saturatie op65535 of kunstmatige afwijzing. Eenzelfde eigenaar/positie/toestand geeft dezelfde S in vergelijking en doelaanmaak. Geen reserveringsupdates tijdens heapgebruik. Het lezen van terrein is ongecachet; terrein mag niet tijdens één heapgebruik veranderen. Bij onverwachte re-entrancy/terrainwijziging is de proef ongeldig; dan gericht terug naar analyse.

Eén punt is de kleinste representabele verandering, geen afgeleide economische bergwaarde. Bij gelijke B>1 wint een niet-bergcentrum strikt van een bergcentrum. Een oorspronkelijk bergcentrum dat precies één punt beter was, wordt gelijk; bestaande x/y-tievolgorde kan dan beslissen. Bij een verschil van minimaal twee punten blijft de hogere oorspronkelijke score hoger. B=1 blijft gelijk. Deze marginale voorkeur kan in echte gameplay nauwelijks effect hebben; dat wordt gemeten, niet als volledige verbetering geclaimd. Geen vermenigvuldiging/bitpakking die positieve scorebereik of concurrentie met andere goals anders schaalt.

**Neveneffecten:** GoalSettle-prioriteit daalt voor getroffen doelen met één kwaliteitsunit×de werkelijk actieve settle_value_coef; ook concurrentie met andere doelen kan daardoor veranderen. Extra terrainquery per getroffen scorecall kost tijd. De adapter kent geen legale 3-bergen/voedselclassificatie en kan een bergcentrum benadelen dat later noodzakelijk blijkt. Juist daarom blijft de verandering klein en worden misclassificatie/taakrealisatie geregistreerd. Maskers kunnen beide gewenste kandidaatlocaties vooraf uitsluiten; scoreverbetering bewijst geen oplossing daarvan.

**Alternatieven:** alle bergcentra nul maken is te sterk zonder bewezen noodzaakuitzondering; een grote bergbonus/straffactor heeft geen onderbouwde schaal; verdubbeling plus tiebit wijzigt goalcompetitie en beperkt het signed16-bereik; alleen settle_value_coef mist het kenmerk. Volledige productiongeschiktheid nu bundelen zou food/overlap/ontwikkeling tegelijk veranderen en de eerste adapterproef onnodig complex maken.

## Offline en begrensde native verificatie in C

Dit document is gereviewd ontwerp; onderstaande checks zijn nog uit te voeren, niet nieuwe onderzoeksresultaten.

1. Patcher: exacte hash/callbytes/header-/alignmentasserts; bron niet wijzigen; kandidaat atomisch apart schrijven. Onafhankelijk teruglezen/disassembleren van volledige adapter, alle branches en drie targets. Rel32-target en fallthrough controleren, iedere return is ret10h, alle pushes/pops/localranges en beide nested callbackpopgroottes handmatig/symbolisch nalopen. Bestaande imports/exports/relocs vergelijken en diffmanifest beperken tot de genoemde mutaties.
2. Deterministische dubbele build en SHA256. Offline callbackfixtures testen: alle AX-patronen voor identiteit; mountain8/20/22 versus hill9/19/21, overige terrain0..23/−1; B=−32768/−1/0/1/2/32767; negatieve/highbits positieargumentslots; z≠0; null-AiMain; passende/mismatch World; getterstatus0; herhaalde/afwisselende civcontext. Meet registercanaries, exacte ESP na ret, x87-depth/controlword en geheugen-canaries. Fixtures zijn ABI-/rekenbewijs, geen engine-effect.
3. **Afzonderlijke 32-bit Windows-helper, zonder spel:** gebruik de aanwezige SysWOW64-PowerShell indien beschikbaar, met standaard .NET/PInvoke en een kleine native callshim uit dezelfde emitter; geen toolchaininstallatie. In eigen helperproces kandidaat eerst met LoadLibraryEx/DONT_RESOLVE_DLL_REFERENCES mappen voor RVA/sectie-/rebasecontrole; dit bewijst geen DllMain/importinitialisatie. Daarna een aparte helper met gewone LoadLibraryW voor echte loader/import/DllMainacceptatie en FreeLibrary; roep geen game-/AI-exports aan. Wanneer die eigen helper aan omgeving/dependencies faalt: fout vastleggen, geen installatie of spelstart als automatische vervanging. Helperpad/bitness vooraf controleren. Alleen de eigen helper mag fixture-World/vtable en g_settle_ai in zijn eigen modulekopie instellen en de payload met native shim aanroepen. Geen levende gameprocessen openen, geheugenscan of injection.
4. Rebasecontrole: reserveer in de eigen 32-bit helper preferredbase20000000h vooraf zodat de loader een andere basis gebruikt; controleer dan werkelijk andere basis, drie rel32-targets en modulebase/RVA-lezen. Geen absolute fallback naar200c6fb4h. Mapping/runtimecallbackfixtures kunnen ABI aantonen, geen effectieve civcontext of echte engine-opbrengst.

Er wordt nu geen extra emulator/observatortool geschreven. De uitvoerder kiest één noodzakelijke fixture-/native verificatiemethode om ABI/relocatie te controleren, zonder identieke tests redundant te stapelen. Een helpertest is aanvullend technische verificatie; daadwerkelijk spelgedrag volgt alleen in de afgesproken proef.

## Dezelfde benchmark, nieuwe doelen aantonen

Gebruik telkens exact [QUOTA-START-T0](../PROEVEN/settlerquota/vaste-start/STARTMANIFEST.md), SHA256 `8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26`, Deity/Gigantic/8spelers, dezelfde passieve menselijke invoer en checkpointprocedure. Geen nieuwe game, aangepaste save, hot-load of T60 als vervanging. De aanwezige acht B1-onderzoekslijstwijzigingen worden in **alle H1-benchmarkarmen constant gehouden**, met hun werkelijke hashes in het manifest. H1 is daardoor geen zelfstandige claim van B1-winst. De originele quotaresultaten zijn historie en geen nieuwe H1-baseline.

Armen: huidige proefconfiguratie zonder H1; dezelfde configuratie met H1-I; dezelfde met H1-M. Begin ieder arm na gecontroleerde proefprocesherstart opnieuw vanaf ongewijzigd T0. Vergelijk H1-I met controle voor infrastructuurgedrag, H1-M met H1-I voor alleen het kenmerk. Bij onvoldoende determinisme eerst baseline herhalen, niet ieder verschil aan de patch toeschrijven.

T0 bevat voor de beschreven AI2 geen steden, maar dit bewijst niet dat alle civs/goals vers zijn. Laat met de bestaande begrensde debug-/observatieroute aantonen dat na laden de betrokken heap nieuw opgebouwd wordt en een **nieuw** GoalSettle dezelfde S ontvangt. Een modulegeladen-hash bewijst niet dat oude opgeslagen doelen zijn herberekend. Noteer callplaats, AiMain/civ, x/y/z, B/S, terrain/context, nieuw doelmoment en opgeslagen GoalSettle+48. Verander geen save of doelen om activatie af te dwingen. Als oude doelen blijven bestaan, classificeer ze als oud en wacht binnen dezelfde T0-doorloop op aantoonbaar nieuwe doelen; kan dat niet worden vastgesteld, dan geen gameplayconclusie en een gerichte activatievraag terug naar de analist. Geen extra observerproject op eigen initiatief.

De andere installatie `D:\CTP` met PID19516 blokkeert nu speltests; die wordt niet bediend, gesloten, geopend of uitgelezen. Offline kandidaatbouw en de afzonderlijke eigen loaderhelper kunnen na C-vrijgave doorgaan; de latere echte benchmark wacht op een vrijgegeven runtime. Dit is geen kennislacune in de H1-bouwroute.

### Meetbare acceptatie

| Stap | Vereist bewijs |
| --- | --- |
| H1-I technisch | Deterministische bytes; drie juiste targets; onveranderd origineel; loader/relocatie/stack/registerchecks geslaagd; alle signed16-uitkomsten identiek |
| H1-M rekencontract | Exact S volgens formule voor alle genoemde branches; geen negatieve positieve-output of nieuwe nulscore; dezelfde S in kandidaat- en goalroute |
| Echte activatie | Gewijzigde proef-DLL daadwerkelijk geladen; juiste civ/World/laag; nieuw heapgebruik én nieuw GoalSettle met de adapterkwaliteit waargenomen |
| Kandidatenpaar | Bij gelijke B>1 en verder toegelaten grondlocaties krijgt niet-bergcentrum de hogere score; hoogtes8/20/22 allemaal herkend; tie-/maskeruitkomst apart vastgelegd |
| Gameplay | Vanaf dezelfde T0: aantal/positie/beurt van getroffen bergstichtingen, beschikbare bergwerkplekken en voedselmogelijkheden, taak/ontwikkeling en nuttige alternatieven; geen claim op ongetroffen selectie |
| Projectmeetlat | T25/T50/T100, beurtenstad25/30, bevolking/food/science/tech/regering, settlers/transport, last/verlies/wonders/goods; cijfers per normale AI en context |

Er is geen verzonnen prestatiedoel of gegarandeerde winst. Ontbreekt een vergelijkbaar geraakt kandidaatpaar in deze T0, dan mag de native fixture de berekening aantonen, maar de gameplaywinst blijft ongemeten. Geen nieuwe benchmarkstart om een gunstige uitkomst te zoeken. Een vermindering van bergcentra is pas nuttig als latere bruikbare werkplekken en economische functie niet slechter worden; de volledige doel7-uitzondering blijft nog te realiseren.

## Herstel, afhankelijkheden en onzekerheden

Bewaar voor ieder arm: originele/proef DLL-hash, alle overige game/aidatahashes (inclusief B1), exact T0/hash, bron-/emitterrecept, payloadhash, patchmanifest, helperbitness/resultaten en waarnemingen. Vervang een DLL uitsluitend wanneer het bedoelde proefproces gesloten is; alleen een door de uitvoerder exact gecontroleerd proefpad. CTP-og/AAIP blijven referenties. Rollback: herstel uitsluitend eigen proef-DLL uit de vastgelegde back-up, controleer haar hash en de drie oorspronkelijke bytes, behoud andermans B1-bestanden, herstart en laad opnieuw dezelfde T0. Een variante-save wordt niet door DLL-herstel een baseline.

De eerste feature hangt af van de bewezen World+a8-ABI en laag0/context, niet van volledige food-/workerplanning. Resterende onzekerheden zijn echte loaderacceptatie, onverwachte indirecte vergelijkercontext/re-entrancy, performance en zichtbare nieuwe-goalactivatie; die hebben concrete C-checks. **Geen onmisbaar ontbrekend analysegegeven voor het beschreven eerste pakket gevonden.** Er wordt daarom geen kunstmatige analistvraag gesteld om de overdracht te vullen. Bij een falende specifieke check gaat alleen de betreffende aangetoonde fout terug.

Vervolg naar de echte productiestad is concreet begrensd: bepaal voor een kandidaat ten minste drie gelijktijdig beschikbare bergwerkplekken via de bestaande gebieds-/populatiefilters, plus één voedselwerkplek met centrum, rations, crime/regering/Deity en toegestane improvementhorizon. Gebruik bestaande [opbrengstmodifiers](../ANALYSE/RANTSOENEN-EN-STADSOPBRENGSTEN.md) en [werkgebiedbewijs](../ANALYSE/IMPROVEMENTCONSTRUCTIE-EN-STADSGEBIED.md); de toekomstige toepassing op een nog niet bestaande stad is geen reeds bewezen volledige classifier. Als de eerstvolgende classifier daardoor blokkeert, vraag de analist gericht hoe die **kandidaat**, zonder cityID, bruikbaarheid en voedselplan exact kan beoordelen. Dit is toekomstige featureafhankelijkheid, geen blokkade om H1-I/H1-M te bouwen en afzonderlijk te toetsen.

Packing/masker×H1, productionclassifier×worker/improvementbeleid en H1×dynamische monopoly-/settlerreserveringen vereisen eigen combinatieproeven. Tech-/taak-/rijkwijziging tijdens een bestaande heap vraagt later een snapshot/herbouwcontract; geen dynamische gewichten in deze eerste zuivere functie. Root presenteert oorzaak, technische route, kleine proef en begrenzing aan de gebruiker vóór toepassing en beslist vervolgens de C-overdracht. Routinekeuzes binnen dit recept vragen geen extra strategisch akkoord.

