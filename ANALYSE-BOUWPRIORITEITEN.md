# Bestaande AI: uitbreiding en bouwprioriteiten

Onderzoek van CTP I-bestanden, zonder gameplaywijzigingen of nieuwe speltest. Doel: de bestaande AI benutten voor snelle uitbreiding naar 25–30 steden. Onderstaande waarden zijn bestandsfeiten; voorspellingen blijven hypotheses.

## De aansturingsketen

Uitgewerkte analyse van aantallen, vestigingsstops en locatiekeuze: [UITBREIDING-BESLISKETEN.md](ANALYSE/UITBREIDING-BESLISKETEN.md). Deze bevat ook de verdachte Large/Gigantic-kaartsets, relevante functies in de gecompileerde engine/AI en de betekenis van de recente ±20-proef. De kleinere quotaruns zijn op verzoek gestopt; eerst wordt deze keten onderzocht.

`mainSciMany.fli` laadt `init.fli`, vervolgens de beurtregels uit `beginturnSciMany.fli`. Die beurtregels bevatten persoonlijkheid, inputs/outputs, economische instellingen en uiteindelijk `aiploader.fli`. Vergelijk de andere persoonlijkheidsroutes voordat een wijziging voor alle AI's wordt voorgesteld. Het generieke `beginturn.fli` heeft veel includes uitgecommentarieerd; dat bewijst niet dat de persoonlijkheidsroutes die regels overslaan.

`aiploader.fli` vraagt conditioneel AIP-profielen aan. Persoonlijkheidsprofielen bevatten bouwlijsten; aanvullende profielen wijzigen onderdelen voor verdediging, onderzoek, vestiging en oorlog. Daardoor moet een wijziging worden beoordeeld samen met alle toepasselijke profielen. De precieze afhandeling van opeenvolgende loads door de DLL is nog niet in runtime vastgesteld.

## Belangrijkste bevindingen

| Onderdeel | Bestandsfeit | Betekenis voor ons ontwerp |
| --- | --- | --- |
| Vroege uitbreiding | `aiploader.fli` vraagt masssettle aan bij vrede, drie genoemde kaartsets en fuzzy stadssets rond 1–5 steden | Geen expliciete uitbreidingsfase tot 25–30; controleer ook of de benchmarkkaart onder deze sets valt |
| Kaartselectie | `inputs.fli` definieert onder meer a48_96_map rond size_of_world=4608 met breedte 250 | Kaartnamen zijn fuzzy sets; niet zonder berekening aannemen dat iedere grote kaart hieronder valt |
| Settlerklasse | `masssettle.aip`: Land_Settler_Troops_Primary prioriteit 10500; Scout_Troops_Primary 25000 | Scouts kunnen sterke concurrentie vormen; een hoge settlerprioriteit alleen zegt niets over gewenste aantallen |
| Aantallen | masssettle en scimany gebruiken UNIT_SETTLER=-2 in primary; scimany gebruikt -1 in core | Aipdef.h noemt het veld units_per_city, maar verklaart negatieve waarden niet. Niet als twee settlers per stad interpreteren |
| Vestigingsstop | `no_settle.aip` zet MAX_EVAL_SETTLE_GOALS en MAX_EXEC_SETTLE_GOALS op 0 | Vestigingsdoelen kunnen worden uitgeschakeld, onafhankelijk van een hogere bouwprioriteit |
| Opnieuw vestigen | `yes_settle.aip` zet dezelfde limieten op -30 en -5 | Herinschakeling bestaat al; betekenis van negatieve goalwaarden nog vaststellen |
| Geluk | Loader koppelt negatieve city_delta-sets aan no_settling | Onderzoek/regering en uitbreiding moeten samen werken; gelukbeveiliging niet blind verwijderen |
| Oorlog | Verschillende oorlogsfasen activeren build_no_settlers | Onze uitbreidingsfase moet zinvolle dreigingsuitzonderingen behouden |
| Defensieonderzoek | citywall_science.aip begint met Stone Working, Bronze Working, Toolmaking; Theocracy staat bijna onderaan | Alleen de persoonlijke onderzoekslijst aanpassen kan onvoldoende zijn voor Religion → Theocracy |

De masssettle-regel gebruikt fuzzy lidmaatschappen en drempels; 'eerste vijf steden' is een benadering, geen exact bewezen omschakelpunt.

## Hoe bouwlijsten concurreren

De lokale commentaren in default.aip en masssettle.aip beschrijven primary-eenheden als voorrang hebbend op gebouwen/wonders. Core-lijsten worden ermee verweven; de eerste core-eenheid krijgt volgens het commentaar een verdubbelde score. Waarden boven 4000 kunnen daardoor gebouwen tijdelijk verdringen, boven 8000 volgens de toelichting tot de vraag is vervuld. Dit is ontwikkelaarscommentaar, geen gemeten productievolgorde.

Er zijn daarnaast globale goalprioriteiten, lijstprioriteiten, aantallen en maximale bouwduur. Vergelijk bijvoorbeeld geen globale build_buildings_priority=20000000 rechtstreeks met een lijstscore van 10500 alsof ze één sorteerlijst vormen.

Gebouwlijsten bevatten scores, geen gegarandeerde vaste queue. De DLL maakt de uiteindelijke keuze. De bestaande lijsten zijn dus een bruikbaar aangrijpingspunt, maar bewijzen nog geen eigen production/science-classificatie per stad.

## Wat AAIP ons hier leert

Directe bestandsvergelijking: `aiploader.fli` en `masssettle.aip` zijn gelijk in origineel en AAIP. AAIP biedt hier dus geen voorbeeld van een langere masssettle-fase.

In scimany.aip blijven de genoemde settleraantallen gelijk. De granaryscore in Growth_List stijgt van 9000 naar 9990; aqueduct van 9000 naar 9980. Production_List verandert eveneens: AAIP begint daar met mill (8960) en drug store (8950), waar origineel met fusion plant (10000) en population monitor (8980) begint. Dit toont hoe de mod bestaande lijsten gebruikt. Het bewijst niet dat de gekozen wijzigingen optimale groei of snellere uitbreiding opleveren.

## Eerste experiment ontwerpen

1. Stel eerst de betekenis van negatieve eenheidsquota en goalgrenzen vast uit aanvullende lokale documentatie of gerichte observatie.
2. Inventariseer de toepasselijke persoonlijkheden en overrides voor settlers, scouts, verdediging, gebouwen en onderzoek; bepaal hun effectieve samenhang.
3. Ontwerp een apart uitbreidingsprofiel, geladen op basis van stadsantal, dat de bestaande planner blijft gebruiken. Kies eerst één testgrens binnen 25–30 en documenteer uitzonderingen; voeg geen onbewezen engine-inputs toe.
4. Prioriteer Religion/Theocracy in alle vroege onderzoekspaden die anders kunnen ingrijpen en controleer de regeringskeuze. Zonder passende regering kan de gelukrem uitbreiding blokkeren.
5. Vergelijk eerst uitbreiding en legerlast vanaf dezelfde start. Voeg granary- en wonderwijzigingen afzonderlijk toe, zodat hun bijdrage meetbaar blijft.

Dit was de uitgangspositie vóór de quotaproeven. De SLIC-queueproef heeft voor dit experiment geen voorrang.

## Gemeten vervolg: drie saves op T60

Het daaropvolgende onderzoek van de vestigingsplanner staat in [VESTIGINGSDOELEN.md](ANALYSE/VESTIGINGSDOELEN.md). Nieuwe DLL-feiten: negatieve goallimieten zijn vaste aantallen, yes_settle gebruikt 30 evaluatie-/5 uitvoeringsdoelen, city_delta is max_cities_before_penalty minus num_cities en packing verwijdert nabijgelegen kandidaatlocaties. Dit vervangt de eerdere onzekerheden over deze specifieke onderdelen; de settlerbouwquota is een afzonderlijke berekening en is daarmee nog niet verklaard.

De handmatige runs vanaf dezelfde T0-start zijn nu voor alle zeven AI-beschavingen vergeleken. Volledig verslag en bewijs: [VERGELIJKING-T60.md](PROEVEN/settlerquota/reeks/VERGELIJKING-T60.md).

Locatiekwaliteit heeft nu onderzoeksvoorrang: [LOCATIEKWALITEIT.md](ANALYSE/LOCATIEKWALITEIT.md). De berekening in de echte executable is gevonden via de World-GUID/interface, zonder adressen uit de afwijkende engine-map te gebruiken. Voedsel/productie/goud/good-slots zijn via de actuele terreinparser gebonden. De gecorrigeerde scoreformule komt in 68 emulatorcontroles overeen met de originele machinecode. Zij waardeert goods-aanwezigheid, zonder monopoly-identiteiten te vergelijken, en kan berglocaties met toekomstig voedsel sterk onderschatten. Centrumflag en volledige cachelevensduur blijven open. Geen nieuwe spelstarts of gameplaywijzigingen.

Het einddoel is de locatiebeoordeling aanpassen aan onze productie-, science- en monopolyvereisten, met een vestigingsvolgorde die reageert op de uitbreidingsfase en behoeften van het rijk. De ontwerpvereisten zijn vastgelegd in [LOCATIESELECTIE.md](LOCATIESELECTIE.md#doel-locatiescore-aanpassen-aan-onze-vereisten). Alleen de bestaande score zwaarder laten meetellen is onvoldoende. De implementatieroute blijft onderwerp van het lopende onderzoek.

Vervolg: [SCORECACHE-EN-INGREEPPUNTEN.md](ANALYSE/SCORECACHE-EN-INGREEPPUNTEN.md). De scoretabel wordt in het archief bewaard en teruggelezen; dit is met originele instructies op twee synthetische tabellen gecontroleerd. Een nieuwe formule wordt daardoor niet automatisch bewezen actief door een oude save te laden. De score stuurt zowel kandidaatordening als doelaanmaak en latere prioriteit: nieuwe monopoly-/specialisatielogica moet vóór de selectie kunnen meetellen. De bestaande World-interface kan de echte GOOD_INDEX teruggeven. Volgende analyse bindt terrein/improvements en eigen good-tellingen; nog geen gameplaywijziging.

Maskeronderzoek uitgevoerd: [VESTIGINGSMASKER.md](ANALYSE/VESTIGINGSMASKER.md). Afstandsuitsluitingen blijven in de save bewaard; packing aanpassen herberekent het oude masker niet vanzelf. De planner kopieert dat masker. Buitenlandse stadsregistratie gebruikt vaste radius 3, stadsvernietiging geeft radius 2 terug. Gebruik voor een latere packing-vergelijking een start vóór relevante stadsregistraties, niet de bestaande T60-toestand als schone start. De zichtbare afstand en terugkoppeling van kandidaattekort naar settlerbouw worden nog onderzocht.

Vervolgonderzoek: [RUIMTE-BUREN-TRANSPORT.md](ANALYSE/RUIMTE-BUREN-TRANSPORT.md). De eerder hieronder nog onbekende eenheidsquotaformule is inmiddels uit de DLL vastgesteld: negatieve quota vragen een vast aantal, positieve quota een aantal per stad. −20 en +20 zijn dus verschillende opdrachten. Marine-aanvragen en bestaande defensieroutes zijn eveneens gevolgd; verdere analyse gaat eerst naar de levensduur van het locatiemasker.

De oorspronkelijke baseline heeft samen 49 steden en 104 stadsbevolking; zowel primary -20 als +20 heeft 66 steden en 124 stadsbevolking. Egyptians gaan van 9 naar 14 steden, Koreans van 5 naar 10, Mongols van 6 naar 16 en Assyrians van 7 naar 10. Welsh, Cubans en Nigerians hebben juist minder steden. De T20-telling was dus onvoldoende om een effect op stedenaantal uit te sluiten.

Daarbij stijgt de voorraad bestaande settlers van 3 naar 71/78. Militair onderhoud daalt van 753 naar 260/208. Beide tekens geven dezelfde stedenaantallen, maar niet dezelfde volledige eindtoestand: onder meer settlertelling, leger en huidige bouwkeuzes verschillen. De quotaformule is inmiddels uit de DLL vastgesteld: −20 vast, +20 per stad, met aanvullende bouwvraag voor gewenst minus bestaande en in productie zijnde eenheden. De actieve samengestelde lijst blijft onbekend; deze proef bewijst geen gelijke tekenbetekenis.

Welsh hebben in beide varianten 3 steden, 11/12 settlers en geen transportschip, tegenover 7 steden en 3 Triremes in de baseline. Ook Cubans hopen settlers op. Onderzoek daarom naast productie de bestaande vestigingsdoelen, stops, locaties en transportvraag. Een grote primary-quota is een aangrijpingspunt, maar geen bewezen eindoplossing voor 25–30 bruikbare steden. Eigendomswisselingen (Kashgar) betekenen bovendien dat stedenaantal niet uitsluitend eigen stichting meet. Geen nieuwe gameplaywijziging tijdens deze observatie uitgevoerd.
