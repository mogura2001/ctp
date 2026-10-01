# Lessen uit de vergelijking met AAIP

Bronnen: daadwerkelijke bestanden, AAips Readme Original.doc en Dip Readme.doc. Leesbare ASCII-fragmenten van de binaire Word-bestanden staan in INVENTARIS; dit is geen volledige Word-conversie en kan tekst/tekens missen. Claims hieronder zijn verklaringen van de modmakers, geen eigen benchmarkresultaten.

| README-doel | Werkelijke wijziging | Les voor ons |
| --- | --- | --- |
| Minder onnodige landeenheden | Gewijzigde quota in persoonlijkheids-AIP's en oorlog/marineprofielen | Zowel normale toestand als overrides controleren; lager quotum kan onderhoud verminderen maar veiligheid schaden |
| Sterkere marine | Marineklassen, samenstelling en aantallen gewijzigd | Niet iedere scheepsquota stijgt: naval core triremes 0.75→0.4, battleship 0.15→0.3; 'meer marine' is geen uniforme factor |
| Betere groei | Silo 9000→9990, aqueduct 9000→9980 in scimany; gewijzigde gebouwlijsten | AIP-lijsten zijn bruikbaar; AAIP's algemene groeidoel is niet onze specifieke uitbreidings-/stadstypekeuze |
| Meer conventionele oorlog | Diverse moderne speciale acties/eensheden lager gewaardeerd | Middelen verschuiven tussen instrumenten; alleen totaal eenheden tellen mist het effect |
| Garnizoenen | Default en defend_normal naar 2; gather/takecity naar 1 | De mod maakt onderscheid tussen normale verdediging en invasie; 2 als vaste norm past niet automatisch bij onze Theocracy-strategie |
| Betere voedsel/mijnbalans | set_inst_priority verandert tons_mines naar default_mines/default_farms; outputs herdefinieert centra | Lees regels en outputwaarden samen; naam 'tons' beschrijft geen vast aantal verbeteringen |
| Evenwicht bevolkingsinzet | pop_gold default150→100, pop_science150→100; min/max en sets veranderd | Wetenschap verlagen kan onderdeel van herverdeling zijn; geen bewijs voor optimale scientists per science-stad |
| Minder extreme WGF-keuzes | set_wgf wages/rations en outputs-sets gewijzigd | Geluk, kosten en groei moeten samen worden gemeten |
| Normalere PW-belasting | med_production_tax0.30→0.20 en regels in set_pw/opening veranderd | Alle schrijvende regels bekijken; een default veranderen bewijst geen constante 20% |
| Minder opvullen tussen eigen steden | Packing-centra gelijkgetrokken naar3.7; settler_get_best_spot vervangen door default_behavior | AAIP-doel kan botsen met onze bewuste dichte vestiging bij goede locaties; niet klakkeloos overnemen |
| Betere AI op trage machines | Const tijdslimieten25/250/3000→125/1250/15000ms | Rekentijd kan uitkomst beïnvloeden; gelijk houden tussen benchmarks en apart testen |
| Rustiger diplomatie | Persistence bijvoorbeeld SciMany9→13, WarFew5→8; diplomatie-eventregels gewijzigd | Berichtfrequentie en onderhandelingslogica apart beoordelen; tekstaanpassing bewijst geen strategiewijziging |

## Grenzen en afwijkingen

De loader en masssettle zijn identiek. AAIP bewijst dus geen uitbreidingstrategie tot 25–30 steden en geen dynamische production/science-bouwqueues. set_govern is eveneens gelijk; nieuwe government-outputdeclaraties zijn op zichzelf geen nieuwe overstapregel.

AAIP wijzigt ook globale spelregels in Const: onder meer franchise-effect0.5→0.35, piracygold30→50, veteran chance0.1→0.15, slavengarnizoensverhouding3→2, opstandskans5→10, eindjaar3000→3200 en vervuiling. Dit beïnvloedt meer dan de AI. Een vergelijking van complete installaties vermengt dus betere beslissingen met andere spelregels.

De README is niet volledig gelijk aan de aanwezige diff: sommige Const-veranderingen staan wel in de bestanden maar niet in de opgesomde README-regels. Neem feitelijke inhoud als versiebron. De units.txt-aanpassing wordt aanbevolen in de README; een aanbeveling is geen bewijs dat zij in deze kopie is toegepast.

## Praktische werkwijze

Gebruik AAIP als voorbeeldenbank, niet als bewezen optimale basis. Neem per wijziging doel, concrete bestanden, afhankelijke outputs/overrides, verwacht effect en meetcriterium op. Houd globale balanswijzigingen en rekentijd apart van strategiewijzigingen. Begin met dezelfde spelregels als origineel; vergelijk dan gerichte AI-aanpassingen. Ondersteun claims van de modmakers met onze eigen meetmomenten25/50/100 en de beurten waarop stad25/30 ontstaan.
