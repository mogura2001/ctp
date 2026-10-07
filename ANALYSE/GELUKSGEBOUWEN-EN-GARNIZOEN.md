# Geluksgebouwen en garnizoen — fase A

Afgebakend onderzoek, 6 oktober 2026. Bestaande engine en AI onderzocht; geen spelstarts of gameplay-/binarywijzigingen. Dit vervolgt [geluk/WGF](GELUK-WGF-EN-STADSOMVANG.md) en [militaire lasten](MILITAIRE-STEUN-PARAATHEID-EN-PW.md).

## Garnizoen is een begrensde geluksbron

De echte component `4aad10` vraagt regering en eenheden op de stadspositie op. Alleen eenheden met **EXERTS_MARTIAL_LAW** tellen mee. Token126 wordt via selector59/case46bd21 geschreven op UnitRecord+34, bit200; getter4db220 leest precies dat bit. Dit is geen algemene telling van alle militaire of aanwezige eenheden. [Component](BINAIR/happiness-defense-garrison-candidate.txt), [getter](BINAIR/happiness-defense-getters-completion.txt), [canonieke tokens](BINAIR/happiness-defense-tokens.txt), [dispatchbinding](BINAIR/happiness-defense-field-dispatch.json), [flagwriter](BINAIR/happiness-defense-unit-flag.txt), [units](../CTP-og/ctp_data/default/gamedata/Units.txt).

De onbegrensde component is:

`min(aantal meetellende eenheden, MAX_MARTIAL_LAW_UNITS) × MARTIAL_LAW_EFFECT`.

Government-parser45a9e1/45a9fe/45aa1b koppelt tokens475/476/477 aan +a0/+a8/+b0. Playergetters4c2a30/4c2a50/4c2a70 lezen maximum/effect/threshold. [Parser](BINAIR/happiness-wgf-government-parser.txt), [getters](BINAIR/happiness-defense-getters-completion.txt), [thresholdgetter en caller](BINAIR/happiness-defense-fields-and-cap.txt).

| Originele regering | Maximum | Effect per eenheid | Threshold |
| --- | ---: | ---: | ---: |
| Tyranny | 4 | 1 | 80 |
| Monarchy | 3 | 1 | 80 |
| Theocracy | 1 | 1 | 80 |
| Communism | 2 | 1 | 80 |
| Fascism | 2 | 2 | 80 |
| Democracy, City State, latere overige regeringen | 0 | 0 | 80 |

Anarchy heeft5/effect1. Waarden komen uit [govern.txt](../CTP-og/ctp_data/default/gamedata/govern.txt). Een eerste chatmelding koppelde de aantallen aan verkeerde regeringen; de broncontrole en bovenstaande tabel corrigeren dat.

De caller `4aba60–4abad8` past de component alleen toe wanneer het **tot dan opgebouwde geluk** onder threshold ligt. Hij schrijft `min(threshold, eerder geluk + component)` terug als double. Een aparte integeroutput gebruikt `trunc(delta+0.5)`; die afgeronde output is niet de opgeslagen gelukwaarde. Bij geluk≥threshold krijgt die output0. Voorbeelden met Theocracy en vier meetellende aanwezige eenheden:74→75,79.5→80,80→80,85→85. De component kan dus zelf geen geluksniveau boven80 leveren. [Caller](BINAIR/happiness-defense-fields-and-cap.txt), [controle-uitkomsten](BINAIR/happiness-defense-controls.json).

Gebouw-/wonder-/overige componenten worden vervolgens afzonderlijk berekend. De grens80 is daarom geen absoluut maximum voor de finale stad. De eerder gebonden happy-growth-grens85 blijft een andere regel. [Volledige geldige caller tot gebouwen](BINAIR/happiness-defense-building-caller-and-switch.txt), [groei](VOEDSEL-GROEI-EN-KOLONISTEN.md).

## Gebouwen: vast effect en regeringstabel

`IMPROVEMENT_FLAG_HAPPY_INC461` gaat via jumptable45f69c naar45efae en schrijft integer BuildingRecord+68. `HAPPY_INC_SWITCH462` gaat naar45f009: de parser maakt op+100 een tabel per regering, vult de default en schrijft de benoemde uitzonderingen op de juiste regeringindex. [Dispatch](BINAIR/happiness-defense-field-dispatch.json), [volledige parser](BINAIR/economy-expense-parsers-full.txt), [tokens](BINAIR/happiness-defense-tokens.txt).

Engine45d1c0 loopt de effectlijst BuildingDB+2c/+f4 en telt alleen bezit op basis van CityData+48/+4c mee. Effecten komen uit Record+68. Engine45d3b0 loopt de afzonderlijke lijst+30/+f8 en leest Record+100[currentGovernment]. Caller4abbb6/4abbe7 telt beide uitkomsten op in de gebouwcomponent Happy+78. De recordstride is264 bytes. [Echte somfunctie](BINAIR/happiness-defense-getters-completion.txt), [switchfunctie en caller](BINAIR/happiness-defense-building-caller-and-switch.txt).

Beide functies bevatten bovendien procentuele wondercallbacks: een conditionele vermindering bij Record+e8, plus een verhoging voor leden van de lijst BuildingDB+d0/+198. Hun effectnamen en volledige wonderlifecycle zijn hier niet gebonden. De controles hieronder zetten die percentages op0; de eenvoudige som geldt dus binnen die expliciete context.

| Origineel gebouw | Geluk | Basiskosten | Upkeep | Beschikbaar vanaf |
| --- | ---: | ---: | ---: | --- |
| Temple | +2 | 270 | 2 | Religion |
| Theater | +1 | 495 | 1 | Philosophy |
| Circus | +2 | 1035 | 8 | Engineering |
| Cathedral | +3 normaal, +5 Theocracy, +1 Communism | 2475 | 10 | Perspective |
| Drug Store | +3; daarnaast productiebonus | 3000 | 10 | Pharmaceuticals |
| House of Freezing | 0 normaal, +5 Theocracy; daarnaast goudbonus | 5000 | 25 | Cryonics |

[Originele gebouwen](../CTP-og/ctp_data/default/gamedata/improve.txt). Basiskosten zijn geen daadwerkelijk betaalde Deitykosten; zie [Deity-kosten](DEITY-KOSTEN-EN-TECHNOLOGIEFASEN.md). Gebouwupkeep en loonbetaling zijn apart onderbouwd in [lasten](ONDERHOUD-LONEN-EN-DEITY-INKOMSTEN.md).

De gewone AI heeft al `CityAgent::UtilityBlgHappy20020090`: niet-positieve aangeleverde bonus levert0, waarna bestaande geluksgrenzen/fuzzy minimum, stadsgegevens en specialist/rationcontext de waarde bepalen. `ScienceAgent::GetBuildingHappyWorth20025370` vraagt daarnaast de gebouwinterface om een gelukswaarde. Dit zijn bestaande waarderingen, geen bewijs dat een bepaald gebouw daadwerkelijk de bouwconcurrentie wint. De precieze aansluiting van regeringstabellen/wonderuitzonderingen op die AI-invoer blijft open. [AI-evaluatie](BINAIR/happiness-defense-ai-evaluation.txt), [bouwconcurrentie](BOUWDOELEN-EN-QUEUE.md).

## Betekenis voor onze doelen en bewijsgrens

Meer garnizoenen dan het regeringsmaximum leveren in deze keten geen extra geluk. Onder Theocracy is één meetellende eenheid voldoende voor deze component; extra eenheden moeten hun defensieve waarde rechtvaardigen. Hun productieonderhoud blijft afzonderlijk bestaan. Dit is geen aanbeveling om bedreigde steden met één eenheid te verdedigen.

Sciencegroei verhoogt de eerder gebonden bevolkingsstraf. Geluksgebouwen kunnen daarom nuttig blijken wanneer zij benodigde specialisten vrijmaken of groei mogelijk maken. De huidige afspraak om overbodige gebouwen te vermijden vraagt om een concrete marginale afweging, geen automatische uitsluiting van alle geluksgebouwen. Een klein gebouw kan ook voor een productiestad nuttig zijn als het een productieverhogende werkdag haalbaar maakt; dat vergt de volledige stadscontext. Er is hier nog geen optimale bouwqueue voorgesteld.

[Controleer-Geluksgebouwen-En-Garnizoen.py](../PROEVEN/Controleer-Geluksgebouwen-En-Garnizoen.py) voert **17/17** controles uit:7 garrisongevallen,4 caller-caps en6 vaste/switch-gebouwsommen. De echte component, militaire flaggetter, regeringsgetters en gebouwloops worden uitgevoerd. City/World/unitpool/recordlookups, UI/detail, 64-bit shift en wonderpercentages zijn expliciete mocks; de cap begint op een geldige interne instructie met expliciete callerregisters. Geen finale geluksupdate, riot/revolt, bardvrijmaking, defensietoewijzing of spelbeurt geëmuleerd. [Uitkomsten](BINAIR/happiness-defense-controls.json).

Engine SHA256 b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79, base400000/timestamp37d6f702; engine-map niet gebruikt. AI matching map/DLL blijft de bekende binding. Eerdere kandidaat4aa990 beschreef geen martial-lawcomponent; zij wordt hier niet als bewijs gebruikt. Een aanvankelijk verkeerd uitgelijnde callerstart4abb90 is vervangen door disassemblage vanaf de echte functiestart4ab410.

Resterende relevante grenzen: exacte AI-gebouweigenschap versus government-switch, overige gelukscomponenten/bardutility, pollution/riotcontext, wonderpercentages en hun obsolescence. Vervolg gericht waar deze grenzen een ontwerpbeslissing bepalen; dit pakket maakt brede fase A niet automatisch gereed.
