# Rijksbudget en omzetting van goud naar wetenschap

5 oktober2026, fase A. Vervolg op [GOUDGEBOUWEN-EN-STADSINKOMSTEN.md](GOUDGEBOUWEN-EN-STADSINKOMSTEN.md), parallel aan de analist voor bevolking/scientists. Dit pakket bindt de AI-aanvraag, regeringslimiet en omzetting van stadsinkomsten. Geen spelstarts, gamewijzigingen of binarypatches.

De bewijsadressen gelden voor de originele engine SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp37d6f702/imagebase400000, en AI-DLL SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, timestamp37b894e7/imagebase20000000. De passende AI-map levert symbolen; de niet-passende engine-map is niet gebruikt. B: gebonden machinecode; E: originele instructies op synthetische objecten; T: configuratietekst.

## 1. De AI vraagt de maximale onderzoeksfractie

**B:** FSAllocScience::Execute200376d0 controleert eerst ScienceAgent+b8 en kan ResearchScience aanroepen. Daarna vergelijkt hij totaal aantal advances+b0 met bekend aantal+64. Zolang totaal>bekend, vraagt Player+144 de double1.0; als alles bekend is, vraagt hij0.0. Dit is geen percentage uit de fuzzy budgetberekening. Bewijs: [originele framecode](BINAIR/economy-budget-ai-allocation.txt). De ScienceAgent-velden zijn ook gebonden in [BEVOLKING-EN-SCIENTISTS.md](BEVOLKING-EN-SCIENTISTS.md); de nulstelling van pop_science bij alles bekend is een aparte branch.

De echte Player-vtable744660 koppelt+144 aan528de0. Die wrapper leest Player+12e4 en roept4d2ff0 aan met de fractie en playerID. Zie [vtable](BINAIR/economy-budget-player-slots.json), [wrapper](BINAIR/economy-budget-player-wrappers.txt).

**B:** setter4d2ff0 leest Government+168. Als de aanvraag groter is, vervangt hij haar door dit maximum; op4d3080–82 schrijft hij de double naar het fractieobject. De verdere event-/netwerktakken zijn niet offline getest. Er is in de gevolgde setterbranch geen extra minimum0-clamp aangetoond; de AI-aanvraag gebruikt hier alleen0/1. Bewijs: [setter](BINAIR/economy-budget-setter-income.txt).

MAX_SCIENCE_RATE token504 wordt door Government-parser45adcf–45addc via522480 naar+168 geschreven. KNOWLEDGE_COEF token465 schrijft op45a8cb–45a8d5 naar+60. Zie [maximumtoken](BINAIR/economy-budget-science-cap-token.txt), [kennistoken](BINAIR/economy-budget-knowledge-token.txt), [exacte veldbranches](BINAIR/economy-budget-bound-fields.txt), [parsercontext](BINAIR/economy-budget-government-parser.txt) en de bestaande databasebinding in [ONDERZOEK-EN-REGERINGSKEUZE.md](ONDERZOEK-EN-REGERINGSKEUZE.md).

**T:** [govern.txt](../CTP-og/ctp_data/default/gamedata/govern.txt) geeft Tyranny MAX_SCIENCE_RATE0.5/KNOWLEDGE_COEF1/GOLD_COEF1, Theocracy0.6/1.25/1.25. De AI-aanvraag1 wordt in die regeringen dus respectievelijk0.5 en0.6. Dit verklaart een concreet onderzoeksvoordeel, maar nog geen volledige overstapafweging inclusief Anarchy en andere kosten.

## 2. Goudkosten en wetenschap zijn twee verschillende outputs

**B:** Player4b74b0 gebruikt het goudobject op+12dc. Als diens veld+8 positief is, berekent hij een ratio veld+4/veld+8 en bewaart die onder meer op Player+1178. Voor iedere stad gaat die double via4de180→4e83f0→CityData49e200. De verhouding gebruikt het actuele ledgersaldo, geen rechtstreekse lijst van gebouw- of legerkosten. Zie [volledige Player-start/loop](BINAIR/economy-budget-city-conversion.txt), [Unit-route](BINAIR/economy-budget-city-conversion-wrapper.txt), [CityData](BINAIR/economy-budget-city-conversion-final.txt).

49e200 leest CityData+1c, dus het stadsbedrag na de in het goudrapport beschreven inhoudingen, en de actuele onderzoeksfractie uit Player+12e4. De outputs zijn:

```text
goudkosten = stadsGold * rijksRatio * onderzoeksfractie
wetenschap = goudkosten * (1 + stadsKnowledgePercent)
```

Op49e239–49e240 krijgen beide outputs eerst dezelfde double. Op49e243–49e253 wordt uitsluitend de eerste verhoogd met CityData+3e0. Dat veld is de opgetelde knowledge-percentarray uit aanwezige gebouwen; type5 is afzonderlijk parsergebonden in het goudgebouwrapport. Een Academy/Publishing House/University-percentage werkt dus ook op deze goudomzetting. Dit pakket verklaart niet de afzonderlijke rechtstreekse scientistbonus of SCIENCE_PER_POP; daarvoor geldt het bevolkingsrapport.

Voor synthetische gold150, ratio0.8, fractie0.5 en knowledgebonus0.5 zijn goudkosten60 en wetenschap90. Dit is een branchvoorbeeld, zonder claim dat een gespeelde stad deze invoer heeft.

De Player-loop accepteert een stadsbijdrage alleen zolang de gecumuleerde double-goudkosten niet groter zijn dan goudobjectveld+0, de beschikbare kas in deze route. Hij blijft langs volgende steden lopen; dit is geen bewezen optimale verdeling tussen steden. Bij onderzoeksfractie>0.9999999 boekt de latere branch goudveld+4 af; anders integer(somgoudkosten). Zie [afrekenbranch](BINAIR/economy-budget-science-turn-arithmetic.txt), gelezen met de geldige functiestart4b74b0 uit het voorgaande bewijs.

Daarna vermenigvuldigt4b762d–4b763c de somwetenschap met Government+60. Op4b764a volgt een wondercallback; de positieve procentuele bijdrage wordt afzonderlijk afgerond en toegevoegd. Op4b767e–4b7687 komt Player+11e4 erbij. Het vervolg [DIRECTE-WETENSCHAP-EN-SCIENCEGEBOUWEN.md](DIRECTE-WETENSCHAP-EN-SCIENCEGEBOUWEN.md) bindt dit veld aan de afzonderlijk berekende en opgetelde directe stadswetenschap en verklaart de knowledgewonderflag. Directe wetenschap heeft haar regerings-/wonderfactor al gekregen en wordt hier niet opnieuw daarmee vermenigvuldigd. De uitkomst wordt geconverteerd naar integer en via4bb550 toegevoegd aan de onderzoeksvoorraad Player+12e0, met grens-/netwerkverwerking. Zie [Player-afrekening](BINAIR/economy-budget-city-conversion.txt), [voorraadbijschrijving](BINAIR/economy-budget-knowledge-factor.txt).

Het pad zonder positieve ledger+8, eventuele negatieve invoer en de volledige volgorde van specialistopbrengsten zijn nog open. De offlinecontrole test de CityData-omzetting; de hele Player-loop wordt hier niet geëmuleerd.

## 3. Ledger en fuzzy budget niet vereenzelvigen

Player+dc→528260→goudobject4a70a0 vult acht AI-outputs. AiGold::SetGoldLevels2000e7e0 bewaart die. Zie [wrapper](BINAIR/economy-budget-player-wrappers.txt), [ledgergetter](BINAIR/economy-budget-setter-income.txt), [DLL](BINAIR/economy-budget-ai-allocation.txt).

| AiGold-veld | Werkelijke bron in enginegoudobject |
| --- | --- |
| +4 | +8 |
| +8 | +c |
| +c | +10 |
| +10 | +1c |
| +14 | +18 |
| +18 | +20 |
| +1c | +24 |
| +20 | +0 |

Deze tabel bindt offsets, zonder onbewezen namen voor elke last. Goudobject4a7050 verhoogt+4 en+0 bij inkomsten;4a7070 verlaagt beide en clamped ze op0.4a71e0 schrijft+8=+10 + +c + +4. Op twee gevolgde calllocaties4b7a28/4b7abf wordt die herberekening aangeroepen. De volledige voorafgaande lasten-/stadsvolgorde is nog niet afgerond. Zie [ledgerhelpers](BINAIR/economy-budget-gold-ledger.txt), [call-kandidaten](BINAIR/economy-budget-expense-callers.txt), [geïnspecteerde turncontext](BINAIR/economy-budget-turn-order.txt).

Afzonderlijke lastbranches registreren bedragen in+14/+18/+1c. Het [kostenonderzoek](BINAIR/economy-budget-upkeep-binding.txt) bevat hun callers en verdere callbacks. Dat materiaal is nog geen volledige onderhouds-/militaire kostformule. In het bijzonder mogen goudlasten niet op basis van offsets gelijkgesteld worden aan Military Support Cost, dat ook de productie kan raken.

AiGold::CalcBudget2000e6f0 berekent intern scienceaandeel als `fz_budget_income_science / (fz_budget_income_science + fz_budget_income_savings + 1e-8)` en apart aandelen voor nieuwe gebouwen, wages en spaardoelen. Dit is een interne AI-budgetverdeling. FSAllocScience gebruikt in de hierboven bewezen route de afzonderlijke0/1-aanvraag. De complete gebruiksketen van alle interne budgetvelden blijft open; wijziging van budget_income_science alleen is geen bewezen verandering van de daadwerkelijke enginefractie.

## 4. Verificatie en betekenis voor de doelen

[Controleer-Wetenschapsallocatie.py](../PROEVEN/Controleer-Wetenschapsallocatie.py) controleert de twee binaryhashes en voert originele branches uit. [Resultaat](BINAIR/economy-budget-checks.json): **17/17** geslaagd. Vijf AI-aanvraaggevallen, zes regeringscapgevallen en zes CityData-omzettingen. Research/actioncallbacks en governmentlookup zijn gemockt; de CityData-formule heeft geen callbacks. Dit bewijst geen volledige economie, onderzoeksduur of gespeelde beurt.

De koppeling good-concentratie→goudgebouwbonus→onderzoeksfractie→knowledgegebouwbonus→Government.KNOWLEDGE_COEF is nu op de relevante branches onderbouwd. Onder gelijkblijvende ratio/gebouwen en vóór inhoudingen/afronding geven de drie tekstfactoren van Theocracy tegenover Tyranny samen `1.25 * (0.6/0.5) * 1.25 = 1.875` op dit goudonderzoekspad. Dat is een voorwaardelijke afleiding, geen voorspelde totale researchwinst: directe scientistopbrengsten, Anarchy, kosten en geluk kunnen anders doorwerken.

Vervolg5 oktober17:10: directe scienceformule en reset/accumulatie/bijschrijving zijn gekoppeld in het directe-sciencerapport,13/13 controles. Bouwdoelen en transport zijn afzonderlijk opgeleverd. Volgende noodzakelijke schakel: complete lasten-/gelukcontext, PW en Deity-/researchkostcorrecties. De volledige Player-loop is nog niet offline uitgevoerd. Fase A blijft open.
