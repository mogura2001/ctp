# Directe wetenschap en sciencegebouwen

5 oktober 2026, fase A. Dit rapport sluit de directe stadswetenschap aan op [bevolkingsinzet](BEVOLKING-EN-SCIENTISTS.md) en [goudonderzoek](RIJKSBUDGET-EN-WETENSCHAP.md). Geen spelstarts, gameplaywijzigingen of binarypatches. B betekent gebonden oorspronkelijke machinecode, E uitvoering van oorspronkelijke instructies op synthetische objecten, T configuratietekst.

De engine heeft SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, imagebase400000 en timestamp37d6f702. De niet-passende engine-map is niet gebruikt.

## 1. Directe stadswetenschap is een afzonderlijke bijdrage

**B:** CityData-functie49e7b0 telt de sciencebonus van elke inwoner via4ccc50, gebouwbijdragen en modifiers. De geldige functiestart en return49e93d staan in [de volledige functie](BINAIR/economy-science-city-total.txt). Population-getter4ccc50 leest de sciencebonus uit PopulationRecord+4c; Player4c2950 leest via455750 GovernmentRecord+60, eerder parsergebonden aan KNOWLEDGE_COEF. Zie [getters](BINAIR/economy-science-government-pop-getters.txt) en [regeringsbinding](RIJKSBUDGET-EN-WETENSCHAP.md).

De normale stadsupdate slaat het resultaat op CityData+2c op en geeft het via4bb530 door aan de eigenaar. Deze laatste functie **telt** de integer bij Player+11e4 op. Bewijs: [stadsaanroep49831c–498333](BINAIR/economy-science-city-player-final.txt), [accumulator](BINAIR/economy-science-player-extra-add.txt), [callers](BINAIR/economy-science-player-extra-callers.txt). De tweede range in het stadsaanroepbestand begint misaligned en geldt niet als bewijs; de Player-volgorde hieronder gebruikt een aparte volledige functiedump.

Voor de gevolgde normale route geldt, met `trunc` als integerconversie richting nul:

```text
inwonerBasis = som(bonus_i + trunc(bonus_i * (stadsWonderPct + rijksPopPct) / 100))
basis = inwonerBasis + trunc(populatie * som(SCIENCE_PER_POP)) + stadsFlatScience
metGebouwen = basis + trunc(basis * stadsKnowledgePercent)
metRegering = trunc(metGebouwen * Government.KNOWLEDGE_COEF)
directScience = metRegering + trunc(metRegering * rijksKnowledgePct / 100)
```

SCIENCE_PER_POP wordt via45e470 uit aanwezige gebouwen gesommeerd; het vermenigvuldigt de **totale bevolking**, inclusief voedselwerkers. De directe sciencebonus per inwoner komt afzonderlijk uit diens populationtype. Parser en gebouwgetter zijn gebonden in [BEVOLKING-EN-SCIENTISTS.md](BEVOLKING-EN-SCIENTISTS.md). CityData+3b0 is de flat-sciencecache, +3e0 de additieve knowledge-percentcache. De volledige herbouw van die caches is geen onderwerp van deze controle.

Wondergetter4722b0 leest Record+48 en sommeert actieve toepasselijke percentages; token459 WONDER_FLAG_INC_KNOWLEDGE_PERCENT bereikt parserbranch470837. Bewijs: [token](BINAIR/economy-science-wonder-token.txt), [getters en toepassingsfilters](BINAIR/economy-science-wonder-getters.txt), [parser](BINAIR/trade-goods-effect-flags-full.txt). De twee eerdere callbacks473c70/474230 lezen respectievelijk Record+a0/+c0 met stads- en rijksbits. Hun veldgebruik is aangetoond, maar hun volledige tekstflagbinding blijft hier open. De synthetische percentages in de controles zijn daarom geen claims over specifieke wonders.

De directe functie leest geen onderzoeksfractie, goudledger of criminaliteitsfactor. Dit zegt alleen dat die factoren in **deze** berekening niet worden toegepast: hun gevolgen voor groei, populationtype, gebouwen of de andere onderzoeksbijdrage kunnen wel van belang zijn.

## 2. Een concreet voorbeeld verklaart de sciencegebouwen

**T:** de originele [population-definities](../CTP-og/ctp_data/default/gamedata/pop.txt) geven POP_WISEMAN sciencebonus10. Gebouwwaarden komen uit [improve.txt](../CTP-og/ctp_data/default/gamedata/improve.txt); regeringsfactoren uit [govern.txt](../CTP-og/ctp_data/default/gamedata/govern.txt). Het interne record IMPROVE_LIBRARY wordt hier met zijn recordnaam benoemd; dit rapport bewijst geen koppeling aan een gelokaliseerde interfacenaam.

**E:** acht inwoners, waarvan zes scientists met bonus10 en twee gewone inwoners met bonus0; geen flat-science- of wonderbonus:

| Gebouwen/regering | Directe wetenschap | Relevante tekstwaarden |
| --- | ---: | --- |
| Geen / Tyranny | 60 | KNOWLEDGE_COEF1 |
| Academy / Tyranny | 96 | +50% knowledge en0.5 science per pop |
| Academy / Theocracy | 120 | KNOWLEDGE_COEF1.25 |
| IMPROVE_LIBRARY / Theocracy | 100 | +25% knowledge en0.5 science per pop |
| University / Theocracy | 112 | +50% knowledge, geen SCIENCE_PER_POP-veld |
| Academy + University / Theocracy | 160 | knowledgepercentages tellen op tot100% |

Voor Academy/Theocracy: `(6*10 + trunc(8*0.5))*1.5 = 96`, vervolgens `96*1.25 = 120`. Een extra10% rijksknowledgebonus geeft132. Afrondingen vinden op meerdere afzonderlijke stappen plaats.

Dit voorbeeld beoordeelt alleen directe wetenschap. Academy kost540 productie/upkeep4, IMPROVE_LIBRARY540/6 en University1350/12. De netto-afweging vereist ook goudonderzoek, onderhoud, bouwtijd, gemiste settlerproductie en toekomstige groei. Dit is dus geen definitieve bouwvolgorde. De bevolking mag niet worden behandeld alsof zes scientists op elke grootte8-locatie voldoende voedsel overhouden.

Scientists kunnen in de onderzochte enginebranches al zonder Academy wetenschap leveren. Wachten op een sciencegebouw is een strategische afspraak van de gebruiker, geen hier aangetoonde algemene unlockvoorwaarde. De AI-keuze tussen terreinwerker en scientist staat afzonderlijk in het bevolkingsrapport.

## 3. Geen dubbele regeringsbonus bij rijksbijschrijving

**B:** Player-update4b7890 zet Player+11e4 op0 bij4b78e9 en loopt daarna langs stadsupdates. Bij4b7d5f roept hij4b74b0 aan, de eerder gebonden goudonderzoek-/afrekenroute. Zie [volledige Player-update](BINAIR/economy-science-player-turn.txt), [cash-callers](BINAIR/economy-science-cash-allocation-callers.txt), [veldreferenties](BINAIR/economy-science-player-extra-refs.txt).

4b74b0 past regering- en wonderfactoren eerst op de **goudsciencebijdrage** toe. Daarna komt Player+11e4 erbij en gaat de geconverteerde som via4bb550 naar de onderzoeksvoorraad. Zie [Player-afrekening](BINAIR/economy-budget-city-conversion.txt) en [voorraad](BINAIR/economy-budget-knowledge-factor.txt). Vervolg17:23 bindt de stadsloop verder:4b79f3→4dc1f0→4e1960→497f10, dus de oorspronkelijke normale CityData-update. [Unit-wrapper](BINAIR/economy-expense-upkeep-pop-and-setters.txt), [actuele CityData-aanroep](BINAIR/economy-expense-city-action-order.txt).

De directe stadswetenschap heeft haar regering-/knowledgewonderfactor dus al gekregen. Vermenigvuldig de opgetelde directe science niet nogmaals met de cash-regeringsfactor. Deze statische volgorde is gekoppeld; de volledige stadsloop, kostenadministratie en gespeelde beurt zijn niet offline uitgevoerd.

## 4. Verificatie, correctie en resterende vragen

[Controleer-Directe-Wetenschap.py](../PROEVEN/Controleer-Directe-Wetenschap.py) controleert de enginehash en voert49e7b0 plus tweemaal de echte accumulator4bb530 uit. [Resultaat](BINAIR/economy-science-direct-checks.json): **13/13**. Getest zijn onder meer gewone inwoners, scientists, verschillende knowledge-/regeringscombinaties, twee SCIENCE_PER_POP-records inclusief bit33, fractionele bevolkingbonus, flat science en wonderpercentages. Populationbonus, ownerlookup en drie wondergetters zijn expliciete mocks; de echte gebouwsom, regeringsgetter en rekeninstructies worden uitgevoerd. Geen volledige parser, citycacheherbouw, plaatsing, geluk of spelbeurt is gesimuleerd.

Een eerdere testhulp zette de x87-afronding overal op afkappen om de geïmporteerde integerconversie te benaderen. Daardoor kon de procentberekening120+10% in de fixture131 geven. De herstelde [ctp_x87.py](../PROEVEN/ctp_x87.py) bewaart de caller-controlword en gebruikt afkappen alleen rondom FISTP; floor gebruikt tijdelijk neerwaartse afronding. De fixtures starten met0x37f. De sciencecontrole geeft nu132. Dit is een **correctie van de testomgeving**, geen aangetoond foutief gamegedrag. De werkelijke CRT/controlword van een gespeelde game is niet opgenomen.

Vanwege die correctie zijn betrokken bestaande controles opnieuw uitgevoerd: stadsopbrengsten26/26, stadssommen10/10, groeivoorraad24/24, groeicontext24/24 en goudgebouwen17/17. Het actuele goudresultaat is [v2](BINAIR/economy-gold-building-checks-v2.json); de overige resultaten behouden hun bestaande bestandsnamen. Er zijn geen gamebinaries veranderd.

Open voor de brede analyse: volledige lasten-/gelukcontext, cacheherbouw bij gebouw-/populationevents, Deity-/researchkosten, de twee aanvullende wonderflagbindings en groei versus directe wetenschap over een resterende spelduur. De formule geeft een controleerbare grondslag voor die afwegingen; zij bewijst nog geen betere science-AI. Fase A blijft open.
