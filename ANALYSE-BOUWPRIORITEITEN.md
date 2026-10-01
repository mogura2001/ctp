# Bestaande AI: uitbreiding en bouwprioriteiten

Onderzoek van CTP I-bestanden, zonder gameplaywijzigingen of nieuwe speltest. Doel: de bestaande AI benutten voor snelle uitbreiding naar 25–30 steden. Onderstaande waarden zijn bestandsfeiten; voorspellingen blijven hypotheses.

## De aansturingsketen

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

Nog geen getallen gewijzigd: eerst quota verduidelijken en een baseline maken. De SLIC-queueproef heeft voor dit experiment geen voorrang.
