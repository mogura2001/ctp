# U30: gerichte verklaring resolverfailure10

15 oktober 2026, 19:40 Europe/Amsterdam. **Gerichte fase A gereed voor B: concrete verkeerde guard aangetoond; herstel nog niet toegepast of in gameplay aangetoond.** Doel1/1a: nuttige uitbreiding naar30, daarna tot40 onder Theocracy. Concrete vraag: welke voorwaarde in `resolve_type` verklaart de echte laatste R44-2-pass met reason10, en wat is de kleinste uitvoerbare vervolgingreep? Ownership uitsluitend dit rapport en VOORTGANG-U30-TYPE10.md. Geen spelstart, GUI, procesread/RPM, nativefixture, build, code- of binarywijziging uitgevoerd.

**Uitkomst:** `resolve_type` eist ten onrechte `IS_SPACE_LANDER` van de gewone Settler: +dc leest Record+34&20h. Dit is via de echte token125/parserdispatch/schrijftak aangetoond. Landmovement staat in Record+30/80000000h en is via dezelfde UnitDB-vtable **+1c→531940** beschikbaar. Vervang de verkeerde +dc/nonzero-eis door de +1c-query met `TEST EAX,80000000h`/nonzero. Laat de andere resolverchecks staan. Een aparte leafdiagnose-DLL is hiervoor geen voorwaarde. De bestaande reason10-opname bewijst nog niet dat geen eerdere guard óók faalde; de foutieve eis is zelfstandig concreet genoeg voor deze kleine reparatie.

Bewijslabels: **F** bestandsfeit; **M** machinecode; **R** bestaande runtimewaarneming; **A** afleiding. Brede A blijft afgesloten. Hergebruikt: [reason44](U30-REASON44.md), [foutcodereview](REVIEW-U30-FOUTCODES.md), [typecontract](TYPE-EN-VERTREKCLAIMS-B4.md), [naamlookup](BINAIR/b4-typeddepartures-name-and-category.txt), [UnitDB-interface](BINAIR/b4-typeddepartures-unitdb-interface.txt). AAIP levert voor deze specifieke helper geen gemeten bewijs of noodzakelijke wijzigingsbasis.

## 1. Nieuwe waarneming en huidige werking

**R:** [PAIR-PROOF](../PROEVEN/u30-foutcodes/20261015T145000/r44-2/PAIR-PROOF.json) bindt kandidaat `8610db83d4e424006f6c8ee3912bac11fd432dd2bb6264c7c9ed5b94fe67dc17` aan één eigen instantie/T0→precieséénn→T1; alle zeven native processed_rounds−1→0. Laatste buffer: civ8/generation7, reason10/context0, policy1/remaining30/government1/engine_count0. Dit is uitsluitend bewijs over de laatste pass; overige zes helperuitkomsten zijn niet bewaard.

**F/M/A:** `policy.finalize` passeert `bind_host` vóór `resolve_type`. De nieuwe foutcoderoute bewaart diens10; `preview_scope` en `original_demand` zijn bij deze failure niet aangeroepen. De bestaande `scope_hook` schrijft bij afsluiten status5/scope0/owner0. Status5 betekent dus niet dat de resolver is geslaagd. Het is ook geen nieuwe reason44 of natuurlijke nulvraag.

**R:** [T1](../PROEVEN/u30-foutcodes/20261015T145000/r44-2/variant/T1.json) bevat bij civ8 type4/SID6083/displaynaam Settler, native settlercategorie true, water/spacebits0, native desired5/Actual2/tekort3 en twee legers type4. De reader heeft hiervoor actuele UnitDB/StringDBpointers, recordarray en een count in2..4097 kunnen lezen. Dat sluit afwezige volledige DBs op het latere leesmoment uit. Het bewijst zonder atomaire opname niet welke waarden de resolver eerder zag, en de displaynaam certificeert niet de exacte tokenlookup.

**F:** de bestaande reader neemt `t` en `types` alleen bij context1 op en bewaart geen SIDlookupoutput, boolreturn, ruwe Record+34 of afzonderlijke +dc-return. Daardoor kan reason10 zowel vóór als ná het schrijven van `t` zijn ontstaan. Geen raw-bufferdump is in variant aanwezig; alleen T0.json/T1.json. De reeds beëindigde instantie hoeft niet opnieuw onderzocht te worden.

## 2. Dekkingsmatrix van de resolverketen

De adressen hieronder zijn failurebranches in de werkelijk geteste kandidaat; alle gaan naar **200db197**, waar status0/reason10/EAX0 worden geschreven. De leafnummers zijn alleen labels voor deze matrix, geen verplichte nieuwe foutcodes. Na de hieronder aangetoonde guardfout is instrumentatie van alle leaves niet nodig vóór het herstelvoorstel.

| Leaf | Beslissing / branchadres | Huidige onderbouwing en resterende kennis |
| --- | --- | --- |
|100| StringDBpointer nul, 200dafdf | M: leest enginebase+67dcfc. R: reader gebruikte geldige pointer later. Passmoment niet bewaard. |
|101| Stringlookupreturn !=1, 200db011 | M: correcte thiscall/ret8 naar4660f0. Exacte runtimebool ontbreekt. |
|102| SIDoutput bleef−1, 200db021 | M: vooraf−1, successbody schrijft node-ID. Bij normale success1 hoort deze guard niet te falen; waarde ontbreekt. |
|103| UnitDBpointer nul, 200db02f | M: enginebase+67dd18. R: latere reader kon DB lezen. |
|104| Rawcount<2, 200db041 | R: latere reader accepteerde2..4097; rawcount passmoment ontbreekt. |
|105| Rawcount>4097, 200db04d | Zelfde grens als reader; geen bewijs van een vaste onjuiste cap. |
|106| Recordarraypointer nul, 200db061 | R: latere reader kon records lezen; pointer passmoment ontbreekt. |
|107| Array+count×2c8 heeft unsigned carry, 200db06f | M: count<=4097 maakt de multiply zelf bounded; guard is een gewone overflowcheck, geen pointervalidatie. |
|108| SID→UnitDB-indexlookupreturn !=1, 200db0a0 | M: correcte thiscall/ret8 naar4543b0; zoekt Record+4 met stride2c8. SID/bool/index ontbreken. |
|109| Interfacecount+1 != rawcount, 200db0c7 | M: +c→531770 retourneert exact rawcount−1 uit dezelfde globale DB. Geen off-by-one-fout in de vergelijking. |
|110| Lookupindex negatief, 200db0d5 | M: lookup success schrijft zijn niet-negatieve loopindex; runtimeoutput ontbreekt. |
|111| Lookupindex>=interfacecount, 200db0e1 | M: beschermt trailing niet-interface-entry. Type4 zou bij de aanwezige vele geldige types passen; exacte lookupidentiteit ontbreekt. |
|112| Algemene settlercategorie !=1, 200db107 | M: +40→531a50 reduceert Record+34&F naar0/1. R: type4 is categorie1, maar resolved t ontbreekt. |
|113| Spacebit !=0, 200db123 | M: +44→531dc0 retourneert mask&8. R: type4bit0; resolved t ontbreekt. |
|114| Waterbit !=0, 200db13f | M: +48→531de0 retourneert mask&2. R: type4bit0; resolved t ontbreekt. |
|115| Verkeerd vereiste ruimte-landerflag ontbreekt, 200db15b | **Concrete fout:** +dc→532040 retourneert Record+34&20h=`IS_SPACE_LANDER`. Gewone UNIT_SETTLER declareert dit niet. Landmovement staat elders; zie §4. |

`+d8→532020` leest Record+34&10h=`IS_SPACE_LAUNCHER` en normaliseert die naar eigen d8=0/1 voor de latere padquery. Dit is **geen failureguard**: zowel nul als nietnul slaagt. Zij kan daarom niet zelfstandig reason10 veroorzaken. Haar gebruik in de padquery blijft hier ongewijzigd.

## 3. Benoemde eenvoudige contracttwijfels gecontroleerd

**F/M:** offline-only gelezen engine SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, imagebase400000/timestamp37d6f702. Alle negen enginebodies uit het bestaande `input-pins.py.pins()` zijn bytegelijk; de functie is uitsluitend als read-only pinberekening gebruikt, haar schrijvende main is niet aangeroepen. Geen civctp.map gebruikt. Zes werkelijke pointers in vtable745098: +c531770, +40531a50, +44531dc0, +48531de0, +d8532020, +dc532040. Het kandidaatbestand heeft exact de geteste8610-hash.

**F/M:** de emitterlabelberekening en echte kandidaatbytes leveren op RVAdcc54 precies `UNIT_SETTLER\0`. De functie berekent ESI=actuele AI-modulebase en gebruikt `lea eax,[esi+dcc54]`, dus geen losse verkeerde absolute stringpointer. `units.txt` declareert UNIT_SETTLER; english/gamedata/gl_str.txt koppelt deze token aan Settler. De gewone unit heeft land/mountainmovement en land/mountainsettling. Deze bestandsfeiten bewijzen geen actuele tokenboominhoud, maar er is geen spellings-/NUL-/casefout in de aangeboden constante.

**M:** Stringlookup krijgt ECX=`[enginebase+67dcfc]`, push `&sid`, push tokenpointer, callee-cleanup8. Zijn successpad4661af–4661c1 schrijft de node-ID en retourneert1; de boomhelper4662b0 doet hetzelfde. UnitDBlookup krijgt ECX=`[enginebase+67dd18]`, push `&type`, push sid, ret8. Het gebruik van `engine()` vóór beide calls verandert EAX, niet ECX. De voorafgaande bounded arrayberekening verandert ECX evenmin. De thiscallcontracten zijn hier dus juist toegepast; de muterende insert454200 wordt niet aangeroepen.

**M:** de interfacecalls pushen de interface als expliciet eerste stackargument; count gebruikt ret4 en traits ret8. Dit past bij de echte bodies. `types=rawcount−1` wordt opgeslagen, vervolgens wordt alleen een tijdelijke EAX met1 verhoogd voor de vergelijking. `checked_type` gebruikt de opgeslagen count met `<`, niet `<=`. De combinatie is intern juist en bewaart de in eerdere A vastgelegde uitsluiting van de trailing entry. Een vaste index4 of het weggooien van deze countguard zou geen onderbouwde reparatie zijn.

## 4. Concrete fout: ruimte-lander in plaats van landmovement

De gerichte vervolgvraag naar de definitie van bit20h veranderde de uitkomst. De aanvankelijke beschrijving als landmovement in deze werknotitie was onjuist; onderstaande parserbinding corrigeert haar.

**M:** de reeds gebonden UnitRecordparser **0046b7f0** trekt op `0046b80b` tien van token af, gebruikt op `0046b81e` de bytecasetabel `0046d108` en springt op `0046b824` via `0046ce28`. Alleen de relevante tokenroutes en schrijftakken zijn offline gelezen, niet de gehele executable:

| Tokenfeit / dispatch | Werkelijke schrijftak | Betekenis voor de fout |
| --- | --- | --- |
| op009f6bfc staat int125 gevolgd door `IS_SPACE_LANDER`; token125→case58→0046bd14 | `8b4334 0c20 894334`: mov eax,[ebx+34]; or al,20h; mov [ebx+34],eax | De door +dc geëiste bit20h betekent ruimte-lander. |
| op009f69f8 staat int124 gevolgd door `IS_SPACE_LAUNCHER`; token124→case57→0046bd07 | `8b4334 0c10 894334`: dezelfde write met10h | Bestaande d8-query is launcherflag, geen failureguard. |
| op009ef510 staat int66 gevolgd door `MOVEMENT_TYPE_LAND`; token66→case2→0046b82b | 0046b831 `81c900000080`: OR ECX,80000000h;0046b83c schrijft Record+30 | De echte landmovementbit staat in een ander veld. Reeds beschreven in TRANSPORT-EN-VESTIGINGSACTIES.md. |
| token97 SETTLE_LAND→case30→0046bab3; token98 SETTLE_MOUNTAINS→case31→0046bac0 | Record+34 krijgt respectievelijk bit1 en bit4 | De algemene low-F-settlercategorie zegt niets over ruimte-landerbit20h. |

**F:** [actuele units.txt](../CTP-proef/ctp_data/default/gamedata/units.txt:294) UNIT_SETTLER bevat MOVEMENT_TYPE_LAND, MOVEMENT_TYPE_MOUNTAIN, SETTLE_LAND en SETTLE_MOUNTAINS, maar geen IS_SPACE_LANDER/IS_SPACE_LAUNCHER. Andere eenheden declareren die ruimteflags expliciet. De gewone settler heeft dus tekstueel geen reden om aan de +dc-eis te voldoen. **A:** als de correcte normale tokenresolver zijn bedoelde type bereikt, verhindert deze onjuiste ruimte-eis zijn successpad. De bestaande T1 meet het ruwe bit niet, dus claim niet dat de exacte uitgevoerde leaf al runtime-gecertificeerd is.

**M: correcte vervanging via dezelfde interface.** Vtable00745098+1c (entry007450b4, pointerbytes `40195300`) wijst naar00531940. Complete body531940–53195d, lengte1eh:

```text
55 8bec 8b450c 8b0d18dda700 50 e88e29f2ff
8b4030 25000000ff 5d c20800
```

Deze functie krijgt `(UnitDB_interface*, int32 type)` op de stack, ret8. Zij haalt het huidige record via4542e0 en retourneert `Record+30 & FF000000h` in EAX. Dit is een **bitmask**, geen BOOL. Gebruik na dezelfde geldige t/boundscheck `iface(...,[t],0x1c)` gevolgd door `TEST EAX,80000000h`; nul→dezelfde type_bad, nietnul→verder. Vergelijk niet met1 en gebruik geen signed>0: de gewone landbit is juist de hoge bit. De categoriequery+40 blijft wel een genormaliseerde0/1, de countquery+c blijft rawcount−1; deze contracten mogen niet worden verwisseld.

## 5. Minimale overdracht aan ontwerp en readerkeuze

**Direct ontwerpbaar herstel:** vervang uitsluitend de onjuiste +dc/nonzero-eis in `native.resolve_type` door de boven bewezen +1c/80000000h-test. Houd naamlookup, count/bounds, algemene settlercategorie, water/space-uitsluiting en d8-normalisatie intact. Voeg slot1c→RVA131940 en de volledige1eh-body aan bestaande vaste inputpins/bindguard toe; bind in de bestaande reader dezelfde echte body als de kandidaat dit nieuwe interfacecontract gebruikt. Er is geen nieuwe module, enginepatch of vaste typeindex nodig. Scope is de helperguard, niet het uitbreidingsbeleid of science-C2.

**Voldoende technische controle na B:** echte531940-bodyret8 en maskerresultaten toetsen: land80000000h moet slagen, land+andere beweging ook; nul/alleen andere beweging moet falen. Fixture met gewone settlercategorie/geenwater-space/geenruimte-lander moet deze guard passeren; landerflag zonder landmovement mag niet slagen. Bewijs ongewijzigde overige resolver-/fallbackbranches en pinning; bestaande gestubde naamlookups blijven beperkt bewijs, geen actuele StringDBtest. Daarna kan één begrensde echte T0→éénn→T1 aantonen of context1 wordt bereikt of een volgende concrete helperfailure overblijft. Dit bewijst op zichzelf geen uitbreiding naar30/40 steden.

**Goedkope readeraanvulling:** lees de al bestaande eigen `t`/+44, `types`/+48 en `d8`/+120 ook bij context0 als ongecertificeerde tussenwaarden. Leg voor het bijbehorende geldige indexrecord de al bestaande raw+30/raw+34 naast hun gemaskeerde uitleg vast. Dit gebruikt uitsluitend bestaande gebonden readroutes; geen nieuwe nativecall of DLL is voor die observatie vereist. `types=0` wijst op failure vóór de countwrite; geldige types met t4 op een latere traitcheck; `d8=0` alleen onderscheidt niets doordat start0 en succes0 mogelijk zijn. Bij t4 en raw34&20h==0 zou de ongewijzigde kandidaat deterministisch de verkeerde laatste guard raken, mits eerdere traits aan hun voorwaarden voldoen.

Een reader-only volledige DB/tokencontrole kan de actuele toestand ná de pass controleren, maar bewaart niet de werkelijke returnbool/SID/tijdelijke count op het eerdere callmoment. Zij onderscheidt dus niet gegarandeerd alle vroege leaves; dat is **geen voorwaarde voor herstel van deze reeds bewezen verkeerde eis**. Voorkeur: eerst dit concrete B-guardherstel, optioneel de kleine readeraanvulling tijdens dezelfde toekomstige proef, geen extra voorafgaande leafdiagnose-DLL/guardframework/GUIrun. Pas als een gecorrigeerde kandidaat opnieuw10 geeft en de kleine reads het niet oplossen, is uitsluitend de overgebleven vroege leaf te onderscheiden.

**Acceptatie en stop:** beide eindige A-vragen zijn beantwoord: een concrete verkeerde semantische guard en de juiste vervangende nativecall/maskerroute zijn bewezen. A→B bereikt, analyse gestopt. Doel1/1a blijft gameplay-open; geen extra oorspronkelijk doel afgerond. Open zijn toepassing, passende technische controle en echte successwaarneming, niet de hele engine of alle unitflags. Volgende reviewbare oplevering is het kleine B-voorstel voor dit guardherstel.
