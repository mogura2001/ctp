# Verduidelijking van quota en profieloverrides

## Negatieve quota: inmiddels uit de DLL vastgesteld

De eerdere onzekerheid hieronder is achterhaald door gerichte disassemblage: zie [RUIMTE-BUREN-TRANSPORT.md](RUIMTE-BUREN-TRANSPORT.md). Negatieve eenheidsquota vragen ceil(abs(q)) vast; positieve quota ceil(q × max(1, steden)). De AI trekt bestaande en in productie zijnde eenheden hiervan af en vraagt voor het tekort bouwdoelen aan. −20 is dus een gelijktijdige, herhaald aan te vullen behoefte, geen verplichte eerste twintig bouwopdrachten. Primary is een bouwklasse; core en overflow kunnen aanvullende vraag leveren.

De hieronder beschreven quota-proef is hierdoor niet meer nodig om tekenbetekenis en afronding vast te stellen. Ook gedeeltelijke profielloads zijn inmiddels uit de DLL gevolgd en offline gecontroleerd: zie [AIP-LAADWERKING.md](AIP-LAADWERKING.md). De feitelijke productievolgorde en actieve fuzzy aanvragen in de gespeelde saves blijven afzonderlijke vragen. De oude quotatekst hieronder blijft als onderzoeksverloop herkenbaar:

Aipdef.h noemt units_per_city, maar beschrijft de negatieve variant niet. Positieve waarden zijn volgens de lokale structuurdocumentatie een gewenste hoeveelheid per stad; afronding, telling van bestaande/onderweg/in productie zijnde eenheden en combinatie van meerdere lijsten blijven enginegedrag.

De hypothese voor een negatieve waarde is een vast rijksaantal: -2 zou dan een vraag naar twee eenheden betekenen, onafhankelijk van het aantal steden. Dat past bij settlers/scouts en verschillende speciale eenheden. Het is nog geen bevestigde CTP-I-regel. De historische analyse van modmaker Celestial Dawn noemt deze uitleg zelf een gok: [AIP Comments](https://apolyton.net/articles/civilization-news/ctp1/modification-ab/9312887-ctp-modification-aip-comments). Ook de betekenis van negatieve goallimieten laat die bron open.

Daarom geen -2→-30-wijziging doen om dertig steden te krijgen. Zelfs bij een vast aantal betekent een settlerquotum vermoedelijk gelijktijdige vraag naar settlers, niet een einddoel voor steden. Geconsumeerde settlers bij stadsstichting en herhaalde productie maken dat onderscheid essentieel.

Gerichte verificatie: vergelijk dezelfde ene settlerlijst bij 2 en 10 steden, met identieke prioriteiten en voldoende bevolking/productie/ruimte, achtereenvolgens met -2 en +0.5. Noteer bestaande settlers, productiequeues en nieuwe opdrachten. Verwijder concurrerende settlerlijsten uit die geïsoleerde proefconfiguratie of registreer hun invloed. Onderscheid gewenste aantallen van feitelijk gerealiseerde aantallen. Geen proef uitgevoerd voor dit verslag.

## Welke profielen schrijven welke onderdelen?

De volledige declaratiematrix staat in [profiel-velden.csv](INVENTARIS/profiel-velden.csv). Zij toont velden in bestanden, niet bewezen runtime-overwritegedrag.

| Profiel | Eenheidsklassen/quota | Onderzoekslijst | Gebouwlijsten |
| --- | --- | --- | --- |
| Persoonlijkheids-AIP's en default | Ja | Ja | Ja |
| masssettle / sandbag | Ja | Nee | Nee |
| getarmy | Ja | Nee | Nee |
| survival_mode | Ja | Nee | Nee |
| naval / supernaval | Ja | Nee | Nee |
| citywall | Nee | Nee | Growth en Defense |
| citywall_science | Nee | Ja | Nee |
| noscience | Nee | Ja | Nee |
| green_me | Nee | Nee | Transportation en Production |

gather, takecity en fallback bevatten geen complete eenheidsklassen- of onderzoeks-/gebouwlijstdeclaraties in deze matrix; ze wijzigen wel andere scalars en/of goalgrenzen. Een profieltitel als 'oorlog' betekent dus niet dat het hele beleid wordt vervangen. noscience en green_me zijn aanwezig, maar hun actieve load-route is niet aangetoond in de onderzochte loader.

## Gevolgen voor de gedeelde opening

1. masssettle alleen verlengen is onvoldoende: het bevat geen gezamenlijk onderzoek en geen gezamenlijke gebouwlijsten. Die blijven afhankelijk van andere geladen profielen.
2. Een compleet gezamenlijk openings-AIP kan de basis leveren. Daarna mogen getarmy/survival/naval de gewenste eenheidsklassen veranderen; bepaal vooraf welke lijsten we willen behouden of toestaan.
3. citywall behoeft een aangepaste openingvariant of aangepaste aanvraag: het verandert granary-/defensieprioriteiten. citywall_science moet tijdens de opening worden beschermd tegen verdringing van Religion/Theocracy.
4. Regeringskeuze ligt in FLI en wordt niet opgelost door een nieuwe AIP-onderzoekslijst. Sluit conflicterende Tyranny-/persoonlijkheidsvoorkeuren afzonderlijk uit.
5. Vestigingsgoals en settlerproductie zijn aparte remmen. no_settle zet goals op nul; de no_settling-output kan settlerbouw sturen. Een hogere quota heft deze remmen niet automatisch op.

De gedeeltelijke vervanging is op 4 oktober uit de originele DLL gevolgd: gewone scalars alleen bij aanwezigheid; het volledige eenheidsklassenblok ineens; gebouwcategorieën, wonder- en onderzoekslijst afzonderlijk. Weggelaten onderdelen blijven tussen beurten staan en worden gesaved. Actions lopen na de rulepass in geregistreerde volgorde. Goallimiet UNLIMITED wordt bij switches juist niet gekopieerd; retreatlimieten worden altijd daarop gezet. Zie [AIP-LAADWERKING.md](AIP-LAADWERKING.md), met vijftien offlinecontroles. De daadwerkelijk aangevraagde samenstelling van iedere benchmarkbeschaving is daarmee nog niet gemeten.

## Concrete vervolganalyse

Eenheidsquota en gedeeltelijke lijstloads hoeven niet opnieuw met GUI-proeven geraden te worden. Volg nu de effectieve researchlijst tot daadwerkelijke advancekeuze, FLI-regeringwensen tot overstap en bouwdoelen tot de productiequeue. Nieuwe gameplayvoorstellen volgen pas na de afgesproken brede analyseoverdracht; alleen lijstinhoud wijzigen is nog geen bewezen gezamenlijke opening.
