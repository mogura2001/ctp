# C2: bron gereed voor volledige rootreview

11 oktober 2026, 16:52 Europe/Amsterdam. **SOURCE_PREPARED_NOT_NATIVE_EXECUTED**. C2 afgerond; uitvoerder stopt. C1-manifest/proofs en bestaande gamebestanden zijn niet gewijzigd. Geen C3-vrijgavebestand aangemaakt, geen helpercase uitgevoerd, geen LoadLibrary/nativecall/gameactie.

Eigen bron: native-helper/Native.cs, native.ps1, run-native.py en cases.json. Twee bestaande ABIshims plus hun recipes exact gekopieerd, herkomst/hash in shim-provenance.json. Eigen positieve staging bevat acht gecorrigeerde AIPs/header; drie afzonderlijke negatieve stagingroots bevatten headerloze oude kandidaat, ontbrekende header en één onbekende advance-name. Geen gewijzigde DLL, IATpatch, imagecopy, parser/getterstub of enginecontext.

| Controle / binding | Bron gereed | Nog daadwerkelijk te meten |
|---|---|---|
| Originele DLL/PE/entrypoints/imports | SHA302507…5d44; gewone LoadLibraryW, actuele modulebase, timestamp, daadwerkelijke dependencyhashes/IATtargets; drie 24-byte preimages met HIGHLOW-normalisatie | Werkelijke load/imports/CRT/DllMain/x86-uitvoering |
| Drie callbacks plus diagnostiek | GameState54→eigen absolutepad; UnitDB0c→fixture1; Science50→gelogde naam/fixtureindex; GameState58→Diagnostic10→bounded tekst | Werkelijke calls; onbekende slot stopt eigen helper met slotnummer |
| ABI | Hergebruik argc1/2-shims; ESP/nonvolatiles/EAX; volledige x87-dumps en behoud CW/TOP/FTW/80-bit occupied registers | Werkelijke native ABIacceptatie; FIP/FDP/opcode/exceptionstatus worden geregistreerd, niet foutief exactgelijk geëist |
| Acht partials | Return én echte researchpresence/count98/alle98names/order/indices; overige scalar/listpresence afwezig | Werkelijke nativeparseracceptatie |
| Zeven switchketens | Restore→opening→restore; bronpresence verplicht; destinationpointer/count/indices raw gelezen omdat Switch_AIP destinationpresence niet zet; destinationpresence blijft onveranderd | Werkelijk native pointer-/inhoudbehoud |
| Negatieve drie | Headerless/missingheader geen stil geldige lijst zonder fout; onbekende naam daadwerkelijk−1 en nativeopslag−1 | Concrete parserdiagnostiek/uitkomst; geen claim dat loader negatieveScience-index zelf afwijst |
| Afwikkeling | Alles in eigen subprocess; bronnen/buffers/delegates/module tot procesexit levend; geen native destructor/free/FreeLibrary | Normale procesexit; OSreclaim is geen destructorbewijs |

Behouden nietresearchfixtures zijn **canarypointers/counts/bytes en drie onderscheidbaar ingevulde scalarvelden** (+8,+10,+248). Daarnaast wordt de volledige oorspronkelijke0x740-bytebaseline van het effectieveAIP vergeleken, met uitsluitend beide8-byte retreatuitzonderingen. Zij bewijzen uitsluitend behoud in deze eigenfixturecontext. Ze stellen geen echte UnitDB-/gebouw-/wonderrecordsemantiek of werkelijke consumptie daarvan voor. Constructorownership blijft native; initieel researchnull, native switch leent en wist eigen bit12. Geen fake ownershipbits of synthetische researchpresence gezet. Beide native retreatsentinels−999999 worden apart geassert.

18 eindige cases: acht `parse-opening_*`, zeven `switch-default/cleric/slaver/scifew/scimany/milfew/milmany`, drie `negative-headerless/missing-header/unknown-name`. caseplan bevat 33 absolute inputpins, fixture-union98/indices1000..1097, ctorboolfalse en vaste unitcount1. Volgende concrete CLI pas na root C3-vrijgave:

```powershell
& 'C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe' 'C:/GIT/ctp/PROEVEN/opening-b2/onderzoek-b2c-header/20261011T163848/native-helper/run-native.py' --case parse-opening_research
```

Runner laat alleen één exacte gepinde case toe; iedere case krijgt eigen nieuwe x86 PowerShell uit SysWOW64, verborgen venster, maximaal20s en4MiB per output. Timeout/oversize beëindigt uitsluitend de zelf via Popen gecreëerde helper met behouden handle; geen PIDzoekactie of gameproces. Abnormal exit/missingresult/timeout is FAIL; geen returnpointer-only PASS. Geen automatisch vervolg of herhaling. Root levert eerst C3-ROOT-VRIJGAVE.json met approved=true, planhash en volledige reviewed_source_pins; native.ps1 en runner eisen dit bestand en hashes. Geen recht op game/attach/download/install uit deze vrijgave.

Budget vóór/na ieder geval; unknown één hercheck. Eindbudgetfout bewaart native_case_pass afzonderlijk maar runnerpassfalse en expliciet checkpoint `BUDGET_STOP_OR_UNKNOWN_NO_NEXT_CASE`. Pc aan. Echte inputs, stdout/stderr/trace/native JSON/runnerstatus blijven ieder eigen onoverschrijfbaar resultaat; een instabiele of ontbrekende native resultfile telt niet als positief resultaat.

Uitsluitend broncontrole uitgevoerd: PowerShell Parser nul syntaxfouten; C# Add-Type puur gecompileerd in64-bit proces zonder Run/LoadLibrary/callbacks; Python ast.parse zonder code-uitvoering. Dit is geen x86 ABI-/parserproef. Geen helper-PID/nativecase/resultatenmap of C3-approval ontstaan.

Reviewpins native-helper/:

- source-manifest.json: f68dfa1647304b3ebaa6b8072485f172e1074d165ca3905120661ac53fe5cbbf
- Native.cs: 9c75d0464f3a9e46519128aae917fb7b6f31dfd03eb5571261d9a7ef3877cc8c
- cases.json: cf3ff0358a38c188c2e8d52c6d8b20437506ef19728cf40e81bcefd519c5d8d8

Source-manifest bindt24 bron-/shim-/plan-/stagingbestanden. Readiness: geen nieuwe kennislacune nodig voor deze beperkte bronpoort; concrete onverwachte import/interface/ABI/parseruitkomst in C3 blijft FAIL met adres/argumenten, geen permissieve extra stub of brede manager/FLI-analyse. Root moet definitieve bron/recipes/CLI volledig beoordelen vóór enige echte calls.

Rootreviewcorrectie16:51: een tijdelijke beperking van de scalarassertie tot drie gekozen fields berustte uitsluitend op een te smalle interpretatie van scope, zonder technisch bewijs. De gehele0x740-baselinecheck is vóór deze definitieve bronfreeze hersteld; pure C#compile opnieuw geslaagd, geen nativeuitvoering.

Budgetvooraf16:41:00 week88/vijf23ok; laatste16:51:39 bron14.8s oud, week86/vijf11ok. Geen budgetstop. Werk stopt voor C2-review. EchteScienceDB/FLIactions/government/researchselector/save/cache/host/gameplay blijven expliciet buiten de acceptatie.
