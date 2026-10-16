# U30: eerste locatiebeoordeling eindigt in reason23

16 oktober 2026, 13:08 Europe/Amsterdam. Gerichte fase A voor Doel1/1a; drie beslisvragen beantwoord voor een klein fase-B-observatievoorstel. Geen spelstart, GUI, RPM, build, nativecall, spel-/binarywijziging of nieuw framework uitgevoerd. Ownership uitsluitend dit bestand en VOORTGANG-U30-REASON23.md. De werkelijke H3-suboorzaak blijft ongemeten; brede fase A wordt niet heropend.

## Antwoord voor ontwerp

**De bewaarde gegevens wijzen de eerste `production_roles`-locatie aan, maar bewaren het bestaande H3Result niet. Er is geen concrete predicate-, offset-, scratch- of callfout aangetoond. De kleinste volgende ingreep is een readeruitbreiding voor de al aanwezige slot0buffer, met dezelfde ongewijzigde kandidaat. Een diagnostische DLL is vooraf niet nodig.**

1. `reason23/classified1` laat bronmatig H3-UNKNOWN, modelmismatch, centrumkeyfout, vier workerindex-/keyfouten en de H3-callcapbranch als directe ingangen zien. De cap is bij de eerste kandidaat uitgesloten. Model/index/keyfouten zijn onder het bestaande geldige seriële broncontract grotendeels invariantschendingen; H3-UNKNOWN blijft de gewone plausibele route. Dat is een gevolgtrekking, geen waargenomen H3-return.
2. Werkelijke kandidaatcalls, stackcontracten, result/slotlayout en gepinde enginequeries kloppen op de gecontroleerde punten. Er is dus geen onderbouwde gameplayherstelpatch uit deze bestanden alleen. Ook ontbrekende bergen of een niet-positieve foodmarge verklaren op zichzelf reason23 niet: die gaan via `roles_next`.
3. Lees in een later afzonderlijk vrijgegeven proef met dezelfde kandidaat **één bestaande eigen slotbuffer van1152bytes**, plus drie extra scalars in de bestaande headerread. Dat onderscheidt H3-UNKNOWN van een inconsistente ondersteunde uitkomst en geeft de reeds bestaande H3/H2-reason. De vroege/onvolledige redenen hieronder zijn expliciete grenzen; geen zestienleaftelemetrie vooraf ontwerpen.

`engine_count0` is **geen expliciete H3-faalguard**. Het telt voor policy/R en Dorig; de originele vraag gebruikt bij0 de multiplier1. H3/H2 krijgen geen city-ID of citycount en zijn juist voor vóór stichting gebouwd. Een geldige nulstedencontext kan wel een afgewezen centrumgate, aanwezige units, ongedekte foodcontext of onpassende daadwerkelijke rantsoenen bevatten. Geen van deze concrete toestanden is hier als oorzaak gemeten.

## Identiteit en bewijssoorten

- **Runtimebewijs R:** [PAIR-PROOF](../PROEVEN/u30-type10/20261015T194300/host1/PAIR-PROOF.json), [T0](../PROEVEN/u30-type10/20261015T194300/host1/variant/T0.json) en [T1](../PROEVEN/u30-type10/20261015T194300/host1/variant/T1.json). Laatste civ8/generatie7: context1, classified1, reason23, Gcert0, Dorig/desired5, remaining30, engine_count0, cutoff0 en pathqueries0. Zeven native-ronden−1→0, maar uitsluitend één gedeelde laatste helperbuffer. Geen per-civcertificaat voor de overige zes; geen extra productie/uitbreiding bewezen.
- **Bestandsfeit F:** kandidaat `b6f272d2503edf5f1cf03f927ebd40ff5dd82b1a2c9d9c948beb4e7215baed62`, manifest `fa5392c650bc2647d072a9e828256b2a07c43d40d7893dee1efd2276ef431e27`; tijdens dit onderzoek opnieuw gehasht. T0 `fff62c3c4d50f8ac8ac92444c40cb59468d61d81e47e3eed0881c2b238d45e21`, T1 `1a9238841706c8f591281e121b70537b7aa3c934f1364434f80dbae60de7d86f`, gelijk aan paarbewijs. Alle veertien H3 Python/bin-dependencies zijn gelijk aan het kandidaatmanifest.
- **Machinecode M:** gerichte RO-decoding uit precies deze kandidaat, geen reconstructie/emissie; onderstaande VAs gebruiken geladen/preferred AI-basis20000000. RX d6000 voor H3, uitbreiding d9000, eigen state-RVA dd000, omvang54804 inclusief generatie. H3Classifier200d6149, capacity200d61d9, food_reader200d64f5, current_model200d6a21, plan_select200d6d5e, H3Host200d7eac. Geen symbolenkaart als implementatiebewijs gebruikt.
- **Engine F/M:** opnieuw SHA `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp37d6f702, imagebase400000. Werkelijke World-vtable7452e0: +28→533580, +a8→5342e0, +ac→534510, +b8→534340, +168→535500. Geen civctp.map gebruikt.
- **Gevolgtrekking I:** uitsluitingen gelden onder de gepinde code, onbeschadigde eigen buffer en het bestaande seriële/lifetimecontract. De snapshots bewijzen geen atomaire totale wereldtoestand. Onverwachte invariantschendingen mogen niet als normale negatieve locatie worden weggefilterd.

Hergebruik: [type10-review](REVIEW-U30-TYPE10.md), [type/vertrekbindingen](TYPE-EN-VERTREKCLAIMS-B4.md), [H2](PRODUCTIEKANDIDAAT-H2.md), [H3-food](KANDIDAATVOEDSEL-H3.md), PROEVEN/production-h3/{layout,components,model,build-current,x86}.py en bestaande H3-native-fixtureverslag. De historische82fixtures gebruikten expliciete eigen allocations; zij zijn geen echte enginevoedselacceptatie voor deze host. De niet-geïnstalleerde science-C2-union bewijst deze productie-effecten evenmin.

## Dekkingsmatrix beslisketen

| Schakel/guard | Werkelijke werking/ingreeppunt | Wat de bewaarde data uitsluiten of openlaten |
| --- | --- | --- |
| Policy, host, type, preview, Dorig | policy.py finalize zet context1 pas na bind_host/resolve_type/preview_scope/original_demand | R context1: eerdere reason10/44-blokker gepasseerd; geen terugkeer naar resolveronderzoek nodig |
| Capture en canonical_prefix | Status2 vereist; prefix maakt alle centrumkeys vóór roles | I gepasseerd om reason23 te bereiken; malformedcapture/prefix hebben22/41 of42 |
| Eerste locatie/rawB | native.py roles196–209;200dc440 verhoogt classified vóór World+168;200dc476 slaat B<=0 over | R classified1 +23: eerste kandidaat, positieve B, geen latere kandidaat of normale B-afwijzing |
| H3-callcap |200dc482–492: vergelijk h3calls>=64, daarna increment; START wist gehele pass, uitsluitend roles verhoogt deze teller | I uitgesloten bij classified1; eerdere H3-score/modelcalls wijzigen deze eigen teller niet |
| H3-return0 |200dc4be call200d6149;200dc4c5 EAX0→200dc6a1 | Open gewone route. Reeds bestaande H3Result bevat hoofdreason en deels H2-subreason; reader bewaart ze niet |
| Geen productieplan |200dc4cb–4d1: EAX!=2→roles_next | Geen verklaring voor23: te weinig bergen, volledig ondersteund geen plan geven1, geen fout |
| ModelID |200dc4d7–4e1: slot+136 moet1 zijn | Directe guard, maar classifier én current_model schrijven onvoorwaardelijk model1; geen bronmatige afwijking gevonden |
| Positieve marge |200dc4e7–505: signed high<0 of margin==0→roles_next | Geen verklaring voor23: een ondersteund negatief/nulmargescenario wordt normaal overgeslagen |
| Centrumkey |200dc523–533 call canonical_key→0 geeft23 | Directe guard. Zelfde centrum werd door prefix gevalideerd; bij onveranderde dimensies/converter hoort deze te slagen. Geen waargenomen keyresultaat |
| Vier workerindices/keys |200dc57f–671: iedere index>=0 en<slot+224; entry=slot+272+12*index; canonical_key moet1 geven | Directe guards. plan_select kiest alleen ondersteunde indices uit open_count; food_reader controleerde hun intern z0/x/y. Geen aangetoonde verkeerde offsets of onvoorwaardelijke fout. Inconsistente status2 vereist gerichte vraag, geen UNKNOWN-naar-skipblindpatch |
| Setvoorraad, veiligheid, matching | Pas na geslaagde production_roles: read_set/order/select | Niet bereikt in deze laatste pass; geen bron-/Army-/padonderzoek als voorwaarde voor23 |
| Fallback/cleanup | roles_bad zet0/reason23; finalize Gcert0 en D=min(R,max(Dorig,G)); scope_end zet status5/scope0/owner0 | R desired5 is behouden nativevraag, geen gecertificeerde5locaties. Cleanup wist slotdata niet; pas volgende START wist het hele eigen buffer |

### ABI/layoutcontrole voor de concrete twijfel

De eigen call op200dc4aa–4be pusht `out=slot+128`, `position`, `World`, `AiMain`. H3Classifier krijgt deze op EBP+14/+10/+c/+8, eindigt op200d61d6 met ret10h, en retourneert result.status. De interne current_model-call heeft vijf argumenten en ret14h. Nonvolatile EBX/ESI/EDI/EBP worden behouden door de geëmiteerde helpers. Geen verkeerde argumentvolgorde of EAX-boolverwisseling gevonden; World+ac gebruikt count als uitkomst.

| Gelezen veld | H3Result-offset | Slot-offset | Controle |
| --- | --- | --- | --- |
| modelID |8 |136 | juiste constante1 |
| margin64 |64/68 |192/196 | juiste signed-high/unsigned-low positieve toets |
| open_count |96 |224 | juiste headercount |
| gekozen vier indices |100/104/108/112 |228/232/236/240 | juiste workerindices |
| H2-entry0 |128+16 |272 | juiste12bytes per entry; positie eerste8bytes |

Result1024 past exact in slot[128,1152). Geen overlap met slotkeys[0,128) of het volgende slot. Classifierlocals[-40,-17] bevatten24bytes HostBinding binnen de stackruimte[-44,-13]; savedregisters liggen[-12,-1]. Capacity gebruikt160bytes scratch[-204,-45], count[-208,-205], binnen zijn frame. current_model FSAVE108bytes[-144,-37] overlapt de quarterlocal[-24,-17] niet. Dit zijn statische checks van de benoemde overlap-/ABI-twijfel, geen nieuwe native-ABI-acceptatie.

## Kleinste ontbrekende observatie voor fase B

**Geen kandidaatwijziging nodig.** Uitbreiding van uitsluitend de bestaande `shared_state()` in de eigen toekomstige reader, onder exact dezelfde loaded binding en `stable_sample` als de andere velden:

1. Voeg `candidates` op Plan+68, `slots` op+80 en `h3calls` op+128 toe aan de bestaande scalaire headerreads. Bestaand civ/generation/status/reason/context/classified blijft het passlabel.
2. Voeg **één bounded read van1152bytes op `AIbase + state_rva + 0x40600`** toe. Voor deze kandidaat is slot0-RVA11d600, H3Result-RVA11d680. Bewaar de bytes volledig als ruwe eigen slotdata; decodeer H3[128:1152] volgens de bestaande layout. Geen pointer uit deze bytes dereferencen, geen enginequery, geen extra hook of andere per-civbuffer.
3. Neem diezelfde bytes/scalars op in beide reads die `stable_sample` vergelijkt. Koppel uitsluitend bij identieke exacte modulebinding en dezelfde civ/generatie. Bij de huidige gewenste herhaling reason23/classified1/h3calls1/slots0 is dit de niet-overschreven eerste H3-uitkomst. Andere combinaties krijgen geen automatische firstcalltoeschrijving.
4. Decodeer minimaal H3.status/reason/modelID, h2_status, open_count, unsupported_entry_mask, vier indices en H2.status/reason/count/mountains. Bewaar marge/voorwaarden als conditioneel scenario. **Ongeïnitialiseerde velden niet als gemeten nulfood/geen bergen classificeren.** Bij status2 zijn de reeds meegelezen H2-entryposities en slotcentrum/keys beschikbaar voor de eventueel inconsistente keyroute.

Dit meet het directe normale faalpad en kiest de eerstvolgende gerichte vraag. De volledige1152bytes zijn kleiner en eenvoudiger dan een extra eigen diagnoseprotocol en bevatten alle bestaande layoutvelden; slechts de eerste144 H3bytes zouden een status2-keyprobleem niet voldoende verklaren. Het werkelijk geëvalueerde centrum staat bij een vroege hostfout nog niet in dit slot. **Geen gok naar centrum0,0:** alleen indien dat later nodig blijkt, kan een aparte bounded read van ORDER[0] en de bijbehorende CAPTURE-entry worden voorgesteld. Die uitbreiding is nu geen prerequisite.

| H3-status/reason in toekomstige read | Wel bewezen / eerstvolgende gerichte vraag | Expliciete grens |
| --- | --- | --- |
|0/14 | classifier faalt in H3Host vóór current_model;200d619c→200d61c6 | Overige H3/H2velden blijven zero. Hostvalidator publiceert geen individuele guard; header alleen kan **niet** aanwijzen welke hostcheck faalde. bind_host had dezelfde validator eerder gepasseerd; eerst die inconsistentie/context beoordelen |
|0/10 | current_model bereikt capacity niet succesvol; H2-header ligt op H3+128 | H2.reason1=context,2=laag,3=World+28false,4=count>20,5=entrylaag,6=terraincall,7=terrainindex. Reason10 zonder H2reason vraagt onderscheid van de vroege nullpositie; geen volledige H2-heranalyse |
|0/11 | Werkelijke WGF/stand/factor ondersteundheidscheck faalt | H3 bewaart stand/factor slechts zover de code ze bereikte; zero bij vroege afbreking is geen volledige gemeten rantsoentoestand |
|0/12 | Centrumfood of latere rekenroute niet ondersteund | current_model zet12 op200d6bf1, na food_readercall; bij mislukking wist food_reader zijn40bytes en publiceert geen subreason. De read kiest deze keten, maar onderscheidt niet iedere Cell/DB/foodmismatch/overflowguard; dan uitsluitend die aangetoonde twijfel opvolgen |
|0/13 | Geen ondersteund volledig plan en unsupported_entry_mask!=0 | Mask identificeert ongedekte werkplekken, niet de interne reden van ieder falend food_readerpad |
|2/model1/geldige indices | Geen gewone H3-UNKNOWN; key/invariantketen onderzoeken met bestaande entries/slotbytes | Geen reason23 als normale locatieafwijzing wegpoetsen; huidige buffer mist exacte falende canonical-keyreturn |
|1 of ongeldig/zeroresult bij h3calls1 | Onverenigbaar met het verwachte gepinde directe pad of snapshottoeschrijving | Eerst binding/lifetime/observatie afwijzen; geen geldig tekortcertificaat |

Faaladressen zijn aan de exacte bytes gebonden. Bij reason12 volgt200d6bf1 (`mov [edi+4],12`) op food_readercall200d6bec; de foutbranch is200d6bfd→200d6d3b. Een volgende fase-C-uitvoerder moet de adres-/manifestbinding van zijn eigen reader opnieuw controleren.

## Overdracht en acceptatie

Alle drie beslisvragen voldoende beantwoord voor B: bronpaden afgebakend, geen aantoonbare concrete herstelpatch, minimale bestaande-bufferobservatie en haar grenzen uitvoerbaar gespecificeerd. **Geen uitspraak dat de echte faalguard al gevonden is.** Ontwerper kan nu één klein reader-only voorstel maken; C pas na review/uitleg/actuele proefvrijgave. Geen hergebruik van een verbruikte hostgate, geen nieuwe start binnen deze analyse. De vorige proef is volgens rootoverdracht gesloten/hersteld; deze agent deed geen nieuwe proceswaarneming.

Geen algemene H3-semantiek, alle zestienleafcases, nieuwe emulator, sciencecompositie, N40beleid of lange benchmark als voorwaarde. Bij vastgestelde lokale legitieme UNKNOWN kan B daarna onderbouwd beslissen tussen behouden wholepassfallback en beperkte lokale uitsluiting; type/host/invariantfouten mogen daarbij niet ongemerkt verdwijnen. Een blanket `roles_bad→roles_next` is nu niet onderbouwd.

Doel1/1a: analyseoverdracht gereed; ontwerp/uitvoering van deze observatie open, gameplaydoel open. Doel3: geen werk verricht of gewijzigd. Laatste eigen budget13:05:21 vers vijf48/week61/state ok; root meldde13:07 vijf41/week60. Analyse stopt bij deze overdracht; pc blijft aan, geen achtergrondwerk of timer.
