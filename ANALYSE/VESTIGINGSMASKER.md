# Levensduur van het vestigingsmasker

Stap 2 van het vestigingsonderzoek, aangevuld met de vorm van de interne radius. Alleen-lezen onderzoek van de originele CTP I AI-DLL; geen spel gestart, save aangepast of gameplaybestand gewijzigd.

## Uitkomst

De AI bewaart per beschaving een blijvend uitsluitingsmasker voor land en ruimte. Stadsregistraties wissen kandidaatbits. Die bits worden in de save opgeslagen en bij laden teruggelezen. De vestigingsplanner kopieert dit masker naar een tijdelijk werkmasker; hij begint dus niet iedere beurt met een volledig opnieuw beoordeelde stadsafstand.

Een andere packing-waarde werkt bij volgende registraties van eigen steden. **De gevonden laad- en planroutines herstellen reeds gewiste bits niet op basis van een nieuwe packing-waarde.** Een packing-proef vanaf een T60-save bevat daardoor de uitsluitingen van het oude beleid. Voor een zuivere vergelijking hebben we een gemeenschappelijke start vóór relevante stadsregistraties nodig, of een afzonderlijk aangetoonde maskerherberekening. Die herberekening is nog niet beschikbaar.

## 1. Nieuw spel: maskers beginnen met enen

`AiMain::Init` roept de gewone `AiMap`-constructor aan op 20001c0e. Deze maakt twee `Bit_Table`-objecten voor het kaartformaat:

| AiMap-veld | Betekenis, vastgesteld via FlattenStaticSettle |
|---|---|
| +0x04 | Statisch landmasker, laag z = 0 |
| +0x08 | Statisch ruimtemasker, laag z != 0 |

De constructor vult de bitopslag met 0xffffffff: land op 20078738–20078748, ruimte op 200787b4–200787c4. Een bit op 1 betekent hier dat de afstandsuitsluiting deze locatie nog niet blokkeert. Het is **geen bewijs van geschikte grond, voldoende voedsel/productie, zichtbaarheid, wettelijke stichting of bereikbaarheid**: daarvoor bestaan aanvullende controles in de kandidaatselectie en settlerbiedingen.

Bron: [constructors en serialisatie](BINAIR/masker-levensduur.txt), [aanroepers](BINAIR/masker-load-aanroepers.txt).

## 2. Stadsregistratie wist locaties

`FlattenStaticSettle` kiest het land- of ruimtemasker en roept `FlattenCanSettle` aan. De laatste routine wist de bits in een gesloten vierkant van interne coördinaten: x0−r tot x0+r en y0−r tot y0+r, inclusief grenzen. Ieder punt gaat door `AiMap::Wrap`.

| Gebeurtenis | Gevonden radius | Bewijs |
|---|---|---|
| Eigen stad geregistreerd | Integerconversie van max(1, settler_packing) | 200047d1–20004802 |
| Buitenlandse stad geregistreerd | Vast 3 | push 3 op 200048ac, aanroep 200048af |

Een lagere eigen packing heft de buitenlandse uitsluitingsradius dus niet op. Dit is relevant voor gedeeld land. De engine bepaalt welke buitenlandse stadsregistraties de AI ontvangt; deze analyse bewijst niet dat alle onbekende buitenlandse steden direct worden geregistreerd.

De integerconversie loopt via een geïmporteerde runtimefunctie `__ftol`. De DLL zelf bevat daarvan slechts een sprongstub (20085dc0). Deze stap stelt daarom nog niet zelfstandig de exacte omzetting van bijvoorbeeld 3.7 vast. Gebruik eerst gehele packing-waarden om conversie-onzekerheid van een proef te scheiden.

Bron: [stadsregistratie](BINAIR/vestigings-bouwstop-en-packing.txt), [buitenlandse stad en stadsvernietiging](BINAIR/masker-stadsevents.txt), [maskerwrapper](BINAIR/packing-masker.txt), [bits wissen](BINAIR/vestigings-inputs-en-afstand.txt), [conversiestub](BINAIR/masker-integerconversie.txt).

## 3. Opslaan en laden bewaren de bits

`AiMain::Save` roept `AiMap::Serialize` aan op 20002844. De schrijfroutine slaat zowel de tabelafmetingen als de volledige bitopslag op:

- Land: 20078c93–20078cd8, bitgegevenslengte = aantal opslagwoorden × 4 bytes.
- Ruimte: 20078d47–20078d8c, dezelfde structuur.

`AiMain::Load` gebruikt de archive-constructor op 20002d8c. Die roept `AiMap::Serialize` aan op 20078c43. De leesroute maakt de twee tabellen opnieuw aan en leest ze via `Bit_Table::Serialize` (20078f87 en 20078fb7). De opgeslagen bitgegevens worden daar in de nieuw toegewezen opslag gelezen op 2007b1c8.

In deze route worden geen stadscirkels met de actuele packing opnieuw berekend. Een oorspronkelijke nul komt als nul terug. Latere engine-events zijn een afzonderlijke mogelijkheid; zij zijn geen aangetoonde algemene herberekening na laden.

## 4. Iedere planronde gebruikt een kopie

`InsertSettleGoals` kopieert het statische landmasker naar `g_can_settle_ground` (2007ab47–2007ab6e), en het ruimtemasker naar `g_can_settle_space` (2007ab70–2007ab90). De kandidaatvergelijking krijgt daarnaast een verwijzing naar het statische landmasker op 2007ab9b.

Tijdens doelkeuze kan de planner het tijdelijke masker verder afvlakken om doelen te spreiden. Die tijdelijke uitsluitingen zijn te onderscheiden van de blijvende uitsluitingen door stadsregistratie. Een nieuwe kandidaatboom is dus niet hetzelfde als een nieuw statisch afstandsmasker.

Bron: [InsertSettleGoals](BINAIR/vestigingsselectie.txt), [statische verwijzingen](BINAIR/masker-aanroepers.txt).

## 5. Stadsverlies en herstel zijn niet symmetrisch

De gevonden route `RegisterMyRemoveCity` verwijdert onder meer stad-, continent- en defensiereferenties, maar roept zelf geen `UnflattenSettle` aan. Eigendomsverlies betekent bovendien niet noodzakelijk dat de stad verdwenen is.

Er is een aparte gebeurtenis `RegisterCityDiedAt`: deze roept `UnflattenSettle` aan met **vaste radius 2** (20004e2c–20004e2f). Die routine zet de bits in dat interne vierkant weer op 1. Zij controleert daarin niet opnieuw de afstand tot andere steden.

Dit levert twee codebevindingen op, nog geen waargenomen gameplayfouten:

- Een eerdere uitsluiting met radius 3 of meer wordt door dit event slechts gedeeltelijk teruggegeven.
- Overlappende uitsluitingen worden in deze routine niet per overgebleven stad bijgehouden; het heropenen van een bit bewijst dus niet dat alle overige voorwaarden zijn vervuld.

Bron: [verwijderen en UnflattenSettle](BINAIR/masker-levensduur.txt), [event](BINAIR/masker-stadsevents.txt).

## 6. Interne radius: eerste concrete schets

Zonder kaartrand wist radius 1 onderstaand 3×3-blok; C is de stad. Dit zijn **interne coördinaten**, nog geen bewezen vertaling naar zichtbare isometrische afstanden.

```text
        x−1  x  x+1
y−1      X   X   X
y        X   C   X
y+1      X   X   X
```

| Integer radius | Intern blok | Aantal gewiste posities zonder wrap/overlap |
|---|---|---:|
| 1 | 3 × 3 | 9 |
| 2 | 5 × 5 | 25 |
| 3 | 7 × 7 | 49 |
| 4 | 9 × 9 | 81 |

`Wrap` wikkelt coördinaten af en verschuift bij overschrijding van de x-grens tevens y met een halve kaartmaat. Gebruik deze tabel daarom niet als gewone schermafstand of wettelijke minimumafstand. De precieze koppeling met zichtbare vakjes is het resterende deel van stap 3.

## Aanvulling: afstandsfilter en locatiekwaliteit zijn aparte stappen

De daaronder eerder nog onbekende engine-formule is inmiddels gevolgd en numeriek gecontroleerd: zie [LOCATIEKWALITEIT.md](LOCATIEKWALITEIT.md). De velden zijn voedsel, productie, goud en lokale good-slots; cachelevensduur en één centrumflag blijven nader onderzoek. De oude civctp.map blijft als adresbron onbruikbaar, maar de actuele World-GUID/interface bood een onafhankelijke route.

De buitenlandse radius geldt rond de geregistreerde **stad**, niet rond alle grenzen of vakjes van een buitenlandse beschaving. Binnen het gesloten interne vierkant verdwijnen kandidaten uit het normale selectiepad. Dit is AI-beleid; het bewijst geen wettelijke minimumafstand voor een menselijke speler. Eigen packing werkt op dezelfde manier met een instelbare radius: de default-output is 4, maar FLI stuurt verschillende dichtheden aan en de feitelijke waarde kan per registratie verschillen.

De kandidaatqueue vergelijkt ook locatiekwaliteit. `AiCellPtr::operator>` (20078460) toetst eerst het statische kandidaatbit; een uitgesloten locatie krijgt in deze vergelijking waarde nul. Voor een toegelaten locatie wordt de enginegetter op interface-offset 0x168 aangeroepen (200784bb en 20078517); de teruggegeven waarden worden onderling vergeleken. `InsertBestSettleGoal` roept dezelfde getter aan op 2007aa35 voordat een doel wordt aangemaakt. Bron: [vergelijker](BINAIR/locatiewaardering-vergelijker.txt) en [doelselectie](BINAIR/vestigingsselectie.txt).

Dit toont een keten van afstandsuitsluiting, engine-locatiewaarde, kandidaat-/continentfilters en daarna goalprioriteit plus settlerbereikbaarheid. De precieze formule van de engine-locatiewaarde is nog niet gereconstrueerd: de niet-overeenkomende civctp.map levert daarvoor geen betrouwbare implementatieadressen. Symbolen voor StaticSettlePoint/GetSettleValue zijn een aanknopingspunt, geen bewijs dat onze berg-, voedsel- of monopolycriteria worden gehanteerd. Voor de uiteindelijke scorecomponenten zie VESTIGINGSDOELEN.md, sectie 6.

## Gevolgen voor de proefaanpak

T60-saves zijn bruikbaar voor observatie van de gevolgen van het oude beleid; ze vormen geen schone start voor vergelijking van packing-beleid. De vaste T0-save is volgens het startmanifest voor Welsh nog stadloos. Dat maakt haar een kandidaat voor zo'n proef, maar bewijst niet de maskertoestand van alle beschavingen. Controleer vóór de latere proef de begintoestand en of de gekozen packing actief is vóór de eerste relevante stadsregistratie.

Volgende analyse: vertaal interne coördinaten naar zichtbare vakjes en onderzoek daarna hoe kandidaattekorten of onbereikbare doelen terugwerken op settlerproductie. Maak nog geen automatische settlerstop op basis van continentvolheid: die input meet iets anders dan het aantal uitvoerbare goede locaties.

Verificatie: robotcom.dll/map komen overeen, timestamp 37b894e7, imagebase 20000000, SHA256 3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44. Directe kruisverwijzingen zijn gecontroleerd in de betreffende routines; linker-symbolen alleen zijn niet als implementatiebewijs gebruikt. Geen wijziging aan de DLL. Reproduceerbaar via `PROEVEN/Analyseer-AI-DLL.py`.
