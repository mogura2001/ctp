# Goudgebouwen en stadsinkomsten

5 oktober 2026, fase A. Deze analyse vervolgt [GOODS-EN-HANDELSROUTES.md](GOODS-EN-HANDELSROUTES.md): hoe gebouwpercentages de stadsinkomsten wijzigen en hoe de bestaande AI dat waardeert. Geen gameplayaanpassing of spelstart. Netto wetenschap, alle inhoudingen en uiteindelijke bouwkeuze blijven afzonderlijke vervolgketens.

## 1. Bewijs en bereik

De originele engine heeft SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp37d6f702 en imagebase400000. Robotcom.dll heeft SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, timestamp37b894e7 en imagebase20000000. De passende AI-map benoemt AI-functies; de niet-passende engine-map is niet gebruikt voor adressen. B betekent machinecodebinding, E uitvoering van originele instructies op synthetische objecten, T tekstconfiguratie. Deze controles bewijzen geen volledige gespeelde stadsbeurt.

## 2. Van gebouwflag naar stadsbonus

**T:** [improve.txt](../CTP-og/ctp_data/default/gamedata/improve.txt) geeft Bazaar en Bank allebei `IMPROVEMENT_FLAG_PRODUCTION_PERCENT PRODUCTION_TYPE_GOLD 50`. Bazaar kost675 productie/upkeep5, Bank1125/upkeep10. De kosten/getalwaarden uit de tekst zijn hier geen volledig netto investeringsmodel.

**B:** de [tokencontrole](BINAIR/economy-gold-parser-tokens.txt) geeft production-percent467 en gold-type510. Parser45eb90 gebruikt de maintable45f69c met index token−456. Entry467 gaat naar45f387. Daar gebruikt de typetable45f82c token−507: gold510 gaat naar45f3c3 en schrijft ImprovementRecord+90=4. Het percentinteger wordt op45f406–17 vermenigvuldigd met0.01 en opgeslagen als double op Record+98. Knowledge511 geeft type5. Zie [parserbinding](BINAIR/economy-gold-parser-binding.json), [geldige parserinvoer](BINAIR/economy-gold-parser-final.txt) en [cases](BINAIR/economy-gold-parser-cases.txt). Oude ruwe/misaligned zoekranges zijn geen zelfstandige parserbewijzen.

De database op globaal a7dd1c is via de echte BuildingDB-interface en constructor gebonden in [VOEDSEL-GROEI-EN-KOLONISTEN.md](VOEDSEL-GROEI-EN-KOLONISTEN.md). Parserverwerking bouwt per flag een lijst: count+44 en indexlijst+10c voor deze percentageflag. De list-builder controleert recordflagbits en gebruikt recordstride108. Zie [database/list-builder](BINAIR/economy-gold-parser-route.txt).

**B:** helper45d730 wist een array van zeven doubles. Voor ieder gebouw in de percentlijst test hij het bijbehorende eigendomsbit in de twee meegegeven32-bit woorden. Daarna telt hij Record+98 op bij array[Record+90]. Goudpercentages **tellen dus op**, zonder vermenigvuldiging van individuele gebouwfactoren. Een ander opbrengsttype komt in een ander arrayvak. Zie [originele aggregatie](BINAIR/economy-gold-effect-array.txt).

CityData gebruikt deze array vanaf+3b8. Het goudvak is +3b8+4*8=**+3d8**; kennis is+3e0. Een aangetoonde writer op49edee–49edfd geeft die array aan45d730 met stadsgebouwbits+48/+4c. Die functie49ecf0 bevat ook een conditionele gebouwverwijdering; haar aanwezigheid bewijst niet de complete cachelevensduur. Andere [call-kandidaten](BINAIR/economy-gold-cache-callers.txt) zijn apart opgenomen; de [geïnspecteerde schrijfcontexten](BINAIR/economy-gold-cache-write-paths.txt) tonen dezelfde arraybasis, maar volledige event-/savevolgorde blijft open.

## 3. Waar handelsinkomsten en regering in de berekening staan

**B:** de stadsroutine4972c0 verwerkt centrum-/werkeropbrengsten, extra componenten en good-handel. Op49755d wordt de teruggegeven handelscomponent toegevoegd aan het bedrag dat de volgende modifierfase ingaat. De good-component en wonderpercentage zijn afzonderlijk gebonden in [GOODS-EN-HANDELSROUTES.md](GOODS-EN-HANDELSROUTES.md). Die good-component is daarom geen geïsoleerde eindbetaling buiten de goudgebouwbonus.

Na verdere voorafgaande componenten staat het bedrag op4975ba in ebx. De [originele rekenbranch](BINAIR/economy-gold-arithmetic-entry.txt) voert vervolgens uit:

```text
metGebouwen = basisbedrag + integer(basisbedrag * somGoudPercentages)
voorInhoudingen = integer(metGebouwen * regering.GOLD_COEF)
```

Dit is de bewezen **deelbranch**, geen complete goudformule. De integerconversie gaat via de geïmporteerde ftol. De offlinecontrole vervangt uitsluitend die import door expliciete x87-truncatie; alle geteste vermenigvuldigingen en optellingen zijn de originele instructies. GOLD_COEF is parsergebonden in [ONDERZOEK-EN-REGERINGSKEUZE.md](ONDERZOEK-EN-REGERINGSKEUZE.md): Tyranny1, Theocracy1.25. De branch schrijft het bedrag naar zowel CityData+1c als+24 op497608–0b.

Voor een synthetisch basisbedrag150 geeft dit:

| Gebouwbonus | GOLD_COEF1 | GOLD_COEF1.25 |
| --- | ---: | ---: |
| Geen |150 |187 |
| Een gebouw+50% |225 |281 |
| Twee gebouwen+50% |300 |375 |

Deze bedragen zijn vóór latere inhoudingen. Ze nemen geen bouwkosten, upkeep, rijkswetenschapsinstelling, andere stadsinkomsten of wonder mee. De vijf-goodcomponent150 kan onderdeel zijn van het basisbedrag; het basisbedrag hoeft niet precies150 te zijn.

## 4. Latere verminderingen en wat de AI daadwerkelijk leest

**B:** na het opslaan van+24 verwerkt49760e–497759 een conditionele inhouding met CityData+cc/+d4 en+ d0, constants+298/+2a0 en een wondercallback. De betekenis en volledige voorwaarden van deze velden zijn hier nog niet gebonden. Daarna wordt CityData+1c minimaal0 gemaakt. Op497761–83 wordt integer(+1c * double([CityData+5cc]+b0)) opgeslagen in+20 en afgetrokken van+1c. De betekenis van dit modifierobject is hier nog open; alleen de arithmetic is aangetoond. Zie [rekenbranch en vervolg](BINAIR/economy-gold-city-tail.txt). Dit is geen volledige upkeep- of nettowetenschapsanalyse.

Population+54→52c630→Player4c9c10→CityData49ca60 schrijft twee outputs: eerst **+24**, daarna **+1c**. CityAgent::BeginTurn2001c16f–88 bewaart die als CityAgent+5c respectievelijk+60. AiGold::StoreProjectedIncome2000e820 telt+5c over steden. De geprojecteerde goudinput gebruikt dus het bedrag vóór de zojuist beschreven latere inhoudingen. Zie [Population-wrapper](BINAIR/economy-gold-population-input.txt), [echte Player-route](BINAIR/economy-gold-field-binding.txt), [City-getter](BINAIR/economy-gold-city-modifier-context.txt), [DLL-invoer](BINAIR/economy-gold-city-ai-inputs.txt) en [projectie](BINAIR/economy-gold-ai-projection.txt).

Een afzonderlijk CityAgent-veld+54 komt uit Player+7c→527d30→4c8730→4dda60→4e74a0, dat CityData+1c leest. Bewijs: [interface](BINAIR/economy-gold-ai-percent-input.txt), [Player](BINAIR/economy-gold-ai-percent-value.txt), [Unit-wrapper](BINAIR/economy-gold-ai-percent-unit.txt), [laatste getter](BINAIR/economy-gold-ai-percent-getter.txt). Deze actuele input is dus wel na de genoemde inhoudingen.

## 5. Bestaande AI-waardering van een goudgebouw

**B:** BuildingDB-effectwrapper523e40… geeft één gebouwbit aan45d730 en vertaalt array[4] naar effect-double+78. Zie de bestaande [BuildingDB-wrapper](BINAIR/food-growth-building-population.txt). CityAgent::UtilityGoldPercent20020390 test dat percentage positief is en retourneert:

```text
percentageVanKandidaat * CityAgent.huidigeGold(+54) * fz_gold_2_production
```

Bij percentage≤0 retourneert hij0. [Originele AI-code](BINAIR/economy-gold-ai-projection.txt). Dit is een utilityonderdeel; de volledige gebouwkeuze, onderhoud, tijdshorizon, competing goals en toelating moeten nog gevolgd worden. UtilityGoldInc20020270 waardeert apart een positieve vaste gold-increase uit effect+50, met dezelfde conversiefactor.

**Afleiding uit de gebonden branches:** percentage maal huidige opbrengst is geen exacte marginale simulatie van de kandidaat. Als een bestaande+50%-bonus al in de huidige inkomsten zit, wordt een tweede+50%-gebouw door deze utility op die reeds verhoogde inkomsten gewaardeerd. De engine telt de tweede bonus echter bij de oorspronkelijke bonus op. Zelfs zonder inhoudingen of afronding lopen beide uitkomsten dan uiteen. Met basis150, bestaande bonus50% en GOLD_COEF1: huidige225, utility vóór conversie112.5; echte verhoging van deze deelbranch75. Andere utilitycomponenten kunnen de uiteindelijke voorkeur nog beïnvloeden. Dit constateert een verschil in rekenmodel, geen bewezen verkeerde queue in een gespeelde beurt.

## 6. Controle en vervolgstap

[Controleer-Goudgebouwen.py](../PROEVEN/Controleer-Goudgebouwen.py) voert originele engine-aggregatie en inkomensarithmetic uit, plus de originele AI-percentageutility. [Resultaat](BINAIR/economy-gold-checks.json): **17/17** geslaagd. Het pakket controleert eigendomsbits inclusief gebouw33, stapeling, scheiding goud/kennis, nulwaarden, regeringfactor/afronding en positieve/niet-positieve utility. Governmentlookup is gemockt; ftol is vervangen door gedocumenteerde x87-truncatie. Voor de aggregatie en utility zijn geen externe callbacks gemockt.

Voor de projectdoelen is onderbouwd dat geconcentreerde handelsinkomsten door goudgebouwpercentages worden versterkt en dat de bestaande AI daarvoor al een utility heeft. Open blijven: volledige upstream-inkomsten, semantiek/volgorde van inhoudingen, onderhoud en rijksallocatie/science, complete cache-events, nettorendement per gebouw en uiteindelijke bouwdoelconcurrentie. De volgende gerichte stap is de rijksgoud-/wetenschapsallocatie volgen en die aan upkeep/militaire lasten koppelen. De analist onderzoekt onafhankelijk de worker/scientistketen. Fase A blijft open.
