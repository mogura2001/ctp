# Bards en geluksvoorwaarden — fase A

6 oktober 2026. Gericht vervolg op [bevolkingsplaatsing](BEVOLKING-EN-SCIENTISTS.md), [WGF](GELUK-WGF-EN-STADSOMVANG.md) en [garnizoen/gebouwen](GELUKSGEBOUWEN-EN-GARNIZOEN.md). Geen spel-/binarywijzigingen. Dit bindt de bestaande bardaanvraag, niet de volledige riot/revoltcyclus.

## Bestaande AI vult bards aan vóór de vrije scientistkeuze

`CityAgent::SupplyEntertainers20021710` vraagt Population-slot40 om status, geluk zonder huidige bardbijdrage en effect per bard. Hij begint met `aangeleverd geluk + gecachet bardaantal × effect`. Zolang dit onder de door de caller aangeleverde geluksgrens ligt, er inwoners over zijn en de positieteller onder de aangeleverde limiet ligt, vraagt hij Population+34 en +3c met type1 aan. Daarna verhoogt hij het lokale bardaantal/positieteller en verlaagt de nog beschikbare bevolking. [Echte functie](BINAIR/happiness-bards-ai.txt).

Voorbeeld onder synthetische invoer: geluk72, bardbonus1, grens75 vraagt3 bards, zolang drie plaatsen/inwoners beschikbaar zijn. Een geluksgebouw dat deze behoefte verlaagt kan inwoners vrijmaken voor voedsel, bergen of scientists. Dat vrijmaken is een strategische afleiding; daadwerkelijke herplaatsing en queueconcurrentie zijn hier niet uitgevoerd.

Het laatste double-argument wordt in deze helper niet rechtstreeks gelezen. De grens die de caller doorgeeft moet dus apart van de fuzzy-/crimeberekening worden onderscheiden; deze functie zelf voert geen volledige criminaliteitsoptimalisatie uit. De herhaalde SupplyEntertainers-aanroepen en hun plaats vóór/na minimumfood staan al in [bevolkingsrapport](BEVOLKING-EN-SCIENTISTS.md).

De twee specialistrequests delen een foutoutput. De gevolgde helper controleert die na de calls niet; hij verhoogt zijn boekhouding ook wanneer een recorder-mock daar een fout teruggeeft. Dit bewijst een ontbrekende lokale controle, niet dat normale bardplaatsing in het spel mislukt. Bij effect0 blijft hij aanvragen tot inwoners/posities op zijn; het is daarom belangrijk dat de echte effectinvoer positief en de caches actueel zijn.

## Waar komt de geluksinvoer vandaan?

Population-table744948+40 wijst naar52c460. Deze zoekt de stadsindex in de Player-populationmap, gebruikt de echte stadshandle en roept `Happy4abd10(CityData)` aan. Het resultaat gaat naar de geluksoutput. CityData49eab0 levert daarnaast de gecachete specialistgegevens; deze wrapper gebruikt specifiek CityData+400 als bard-effectbasis. Een wondercallback474230 wordt omgezet naar `1+percentage/100` en ermee vermenigvuldigd. Het oorspronkelijke POP_BARD heeft BONUS_LUXURY1. De volledige schrijver/refresh van CityData+400 en de wondereffectnaam zijn hier niet opnieuw gebonden. [Wrapper/Happy-functie/getter](BINAIR/happiness-bards-engine-input.txt), [Pop.txt](../CTP-og/ctp_data/default/gamedata/Pop.txt).

Happy4abd10 reconstrueert de huidige niet-bardcomponenten: bestaande basis/size/steden/andere caches, actuele WGF, begrensde martial law en vaste/switchgebouwen/wonders. Hij telt de bardcomponent Happy+70 niet op in zijn geretourneerde som. De AI voegt daarom het gecachete eigen bardaantal toe. Dit is geen kale uitlezing van Happy+0 en geen volledige herberekening van alle wereld-/stadsgebeurtenissen. Bij owner0 gebruikt de vroege branch alleen de basiscomponent; dat is geen normale-beschavingscase.

## Verificatie en gevolgen voor het ontwerp

[Controleer-Bardaanvragen.py](../PROEVEN/Controleer-Bardaanvragen.py) voert **8/8** originele DLL-controles uit: voldoende geluk, één/drie benodigde bards, inwonerslimiet, positielimiet, effect0, reeds gecachete bard en requestfout. [Uitkomsten](BINAIR/happiness-bards-controls.json). Population-status/effect zijn expliciete mocks, requests recorders; CityAgent-tellers zijn synthetisch. De wrapper/Happy-route is statisch gevolgd, niet volledig geëmuleerd. Geen bewering over werkelijk vrijgemaakte scientists, riots, geslaagde engineplaatsing of een volledige beurt.

Binaries gebruiken dezelfde gecontroleerde SHA/base/timestamp als eerdere rapporten; engine-map niet gebruikt. Deze helper heeft geen nieuwe slider-, specialist- of bouwplanner nodig om de bestaande route te verklaren.

Voor de gewenste science-stad is het aantal resterende scientists afhankelijk van voedsel én geluk. Onze regels bij omvang8/10 moeten dus een geluksvoorwaarde krijgen in een later voorstel. Voor een productiestad met3 bergwerkers+1 voedselwerker kan bardbehoefte die indeling onmogelijk maken: locatieopbrengst alleen bewijst geen werkend vierpopmodel. WGF, regering, gebouwen en veiligheid horen bij de haalbaarheidsberekening. De actuele doelregels worden met dit analyserapport niet stilzwijgend gewijzigd.

Open grenzen die een later voorstel kunnen raken: specialistcache-refresh, exact government-switch-effect in AI-gebouwinvoer, complete crime/riot/revoltreactie en tijdelijke callergrenzen. Volledige event-/schedulerafhandeling alleen vervolgen als een ontwerp daarvan afhangt.
