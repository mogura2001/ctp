# B1 — Religion en Theocracy vooraan in bestaande onderzoekslijsten

Voorstel van 7 oktober 2026, fase B. Nog niet toegepast. Alleen de ontwerperbestanden zijn geschreven. De coördinator moet dit voorstel aan de gebruiker uitleggen en B→C overdragen voordat een uitvoerder spelbestanden verandert.

## Beslissing en begrenzing

Voorgesteld wordt één factor te veranderen: de rangorde van twee advances in alle normale AIP-onderzoekslijsten. Iedere lijst begint voortaan met Religion, vervolgens Theocracy; de overige advances houden hun bestaande relatieve volgorde. Dit ondersteunt projectdoel 3 en de gezamenlijke opening uit [PROJECTDOELEN](../PROJECTDOELEN.md). Het is de eerste stap in [VERBETERPLAN](VERBETERPLAN.md), geen volledige openingsimplementatie.

De huidige selector doorloopt de effectieve lijst en kiest het eerste onbekende, direct onderzoekbare item dat haar tijdtoets haalt; anders gebruikt zij de eerste direct onderzoekbare kandidaat als fallback. Zij zoekt in deze route geen ontbrekende prerequisites. Theocracy staat in de meeste huidige lijsten bijna achteraan. Bovendien vervangt een latere citywall_science-load de onderzoekslijst opnieuw. De oorzaak is dus concrete kandidaatvolgorde plus overridewerking, geen gebrek aan een onderzoekmogelijkheid. Zie [onderzoek/selectie](../ANALYSE/ONDERZOEK-EN-REGERINGSKEUZE.md), [laadwerking](../ANALYSE/AIP-LAADWERKING.md) en [fuzzybeleid](../ANALYSE/FUZZY-BELEID-EN-DEFUZZIFICATIE.md).

De gewenste beslissing is bij een reguliere herkeuze eerst Religion onderzoeken als die nog onbekend is, daarna de rechtstreeks beschikbaar geworden Theocracy. De bestaande tijdtoets blijft gelden: een langzaam vroeg lijstitem kan nog worden gepasseerd door een later snel item. Er wordt geen gegarandeerde opeenvolging of onmiddellijke onderzoeksannulering geclaimd.

Dit verandert geen regeringsrangen. Niet-clericpersoonlijkheden vragen in de huidige gewone regels meestal geen Theocracy aan. Ook settlervraag, stedenomvang, defensie, voedselbeleid en specialisatie worden hiermee nog niet gerealiseerd. B2 en de technische vervolgroute blijven noodzakelijk.

## Exacte technische ingreep

Doelmap uitsluitend `CTP-proef/ctp_data/default/aidata/AIPs/`. Acht bestaande bestanden:

| Bestand | Huidige positie Religion / Theocracy (vanaf 1) | Nieuwe positie |
| --- | --- | --- |
| default.aip | 7 / 97 | 1 / 2 |
| cleric.aip | 2 / 1 | 1 / 2 |
| milmany.aip | 7 / 97 | 1 / 2 |
| milfew.aip | 12 / 98 | 1 / 2 |
| scimany.aip | 15 / 96 | 1 / 2 |
| scifew.aip | 7 / 97 | 1 / 2 |
| slaver.aip | 13 / 19 | 1 / 2 |
| citywall_science.aip | 7 / 97 | 1 / 2 |

De posities zijn gebaseerd op de actuele OG-lijsten uit het onderzoeksrapport; de twee tokens staan op dezelfde plaatsen in de aanwezige proefkopie. De uitvoerder controleert vóór toepassing volledige hashgelijkheid van deze bestanden met de gedocumenteerde baseline; bij een verschil eerst diff lezen en eigenaarschap afstemmen, geen ander werk overschrijven.

Per bestand uitsluitend het `#DATA`-blok van `Advancement_Element Advancements_List[MAX_ELEMENTS]` wijzigen. Neem de bestaande recordregels, verplaats Religion en Theocracy naar de eerste twee recordposities, verwijder hun oude voorkomens en behoud alle overige records in dezelfde volgorde. De resulterende beginrecords zijn:

```text
 "ADVANCE_RELIGION";
 "ADVANCE_THEOCRACY";
```

Formele transformatie: voor de huidige geordende lijst L wordt L' = [Religion, Theocracy] gevolgd door L zonder deze twee bestaande voorkomens. Aantallen en multiset van de advance-records blijven exact gelijk. Geen nieuwe advance, gewicht, MAX_ELEMENTS-waarde, fuzzyinput, syntaxconstructie, technologievoorwaarde of globale regel toevoegen. Bestaande encoding, CRLF en overige bytes behouden; alleen de verplaatsing binnen dit blok mag verschillen.

Alle geïdentificeerde onderzoeksschrijvers zijn meegenomen: default bij initialisatie, zes normale persoonlijkheidsprofielen en citywall_science als late override. masssettle, survival_mode, naval/supernaval en de overige huidige AIPs leveren geen aanvullende onderzoekslijst. `barbarian.aip` en `noscience.aip` blijven apart: beide hebben een declaratie; noscience heeft een lege lijst. In de huidige aidata is geen normale `load(noscience.aip)` gevonden. Dat sluit alternatieve/scenario-aanroepers niet uit. Als die in de benchmark actief blijkt, onderzoek de daadwerkelijke caller voordat een lege lijst stilzwijgend wordt gevuld.

## Waarom de bestaande interface dit kan uitvoeren

`Load_Scientific_Advancement_List2005f380` maakt de advance-indexarray in tekstvolgorde; de aanwezigheidsflag is AIP+7ac bit14, arraypointer+7fc. `Switch_AIP` vervangt deze hele categorie bij aanwezigheid. `AIP::Choose_Next_Science20066ba0` gebruikt die volgorde en vraagt bekende/direct onderzoekbare status en totale kosten op via de echte Science-interface. `FSAllocScience200376d0` → `ScienceAgent::ResearchScience20025d80` geeft de gekozen index door aan Science+24. De caller op200376e8 en selectorcall op20025d94 zijn vastgelegd in het bestaande bewijsbestand research-government-science-route.txt; de route vereist geen nieuwe aanroepmogelijkheid.

Er zijn 14 bestaande oorspronkelijke-instructiecontroles voor de selector en 15 voor de normale AIP-load/switchroute. Hun callbacks/fixtures zijn begrensd; zij zijn geen echte gewijzigde parser-/fullturnproef. Daarom volgen een tekstcontrole en een werkelijke activatiecontrole in fase C. Een nieuwe DLL-hook of SLIC-script is voor B1 niet nodig.

`advance.txt`: Religion heeft geen genoemde prerequisite; Theocracy vereist Religion. Beide hebben basiskosten65. De normale selectie eist Science+3c exact1: geen onbekende prerequisites. Bekende advances worden overgeslagen. Concreet:

- Beide onbekend: Religion is direct kandidaat; Theocracy wordt overgeslagen totdat Religion bekend is.
- Religion bekend, Theocracy onbekend: Theocracy wordt de eerste directe kandidaat, onder de bestaande tijdtoets.
- Beide bekend: overige lijstvolgorde functioneert verder zoals voorheen.
- Lopend geldig onderzoek: de AIP-switch wijzigt de herkeuzevlag niet; dat onderzoek loopt normaal door. Het nieuwe beleid wordt pas bij een herkeuze beoordeeld.

## Kosten, verwacht effect en neveneffecten

Verwacht: eerdere beschikbaarheid van Theocracy bij civs die haar anders pas laat selecteren, ook wanneer citywall_science later wordt geladen. De clericvolgorde Theocracy→Religion werkte al door de beschikbaarheidsfilter; de normalisering daar hoeft dus geen winst te leveren.

Er zijn geen extra bonussen. Bestaande Deitykosten blijven gelden. [Kostenbewijs](../ANALYSE/DEITY-KOSTEN-EN-TECHNOLOGIEFASEN.md) geeft normaal K = basiskosten + 25 × aantal bekende advances, daarna eventuele bijzondere aftrek en K + trunc(K × tijdperkcorrectie). Ancient is −0,10. Dus130 opgetelde basiskosten is geen werkelijk betaald pad. Zonder bijzondere aftrek bij acht bekende advances kost Religion239; bij daarna negen bekende advances kost Theocracy261. Samen500 onder die voorbeeldvoorwaarden; het werkelijk startkennisniveau moet worden uitgelezen.

Vroeger onderzoek kan dezelfde advances tegen een kleiner known-techbedrag leren. Dat is een berekende verwachting, geen al gemeten besparing. Beide advances veranderen het tijdperk niet rechtstreeks.

Neveneffect: uitstel van bijvoorbeeld Bronze Working, Stone Working, Ship Building, Mining of Trade voor zover nog onbekend. Dit kan verdediging, kolonisatie over water en handelsopbouw vertragen. Juist citywall_science begint nu met Stone Working voor de vroege defensietaak; de voorgestelde gedeelde onderzoeksrichting verschuift die afweging. De benchmark moet dit als risico meten, inclusief klein eiland en AI-buren; geen aanname dat Religion altijd belangrijker is dan onmiddellijke overleving. Een nadelige contextuitkomst gaat terug naar B2/ontwerp voor een aantoonbare tijdelijke uitzondering.

Automatisch vroeger Theocracy gebruiken volgt niet uit dit pakket. De regering moet apart worden gerangschikt, aangevraagd en actief worden; de normale wissel heeft Anarchy en1–4 rondes wachttijd. Haar40-stedenkandidaatfilter sluit25–30 niet uit. Geen wijziging aan die filters of timers voorstellen in B1.

## Alternatieven en afhankelijkheden

Alleen default wijzigen wordt verworpen: eerste-beurtpersoonlijkheden en latere citywall_science vervangen de lijst. AAIP integraal kopiëren wordt verworpen: AAIP heeft andere lijsten én globale regels en realiseert onze opening niet. Eén nieuw gedeeld research-AIP als laatste load is een bruikbaar later alternatief, maar vraagt extra FLIactie/gating en kan tijdelijke defensieoverschrijvingen onbedoeld verdringen. Acht verplaatsingen beperken B1 tot de bewezen bestaande route.

Een harde garantie dat Theocracy altijd direct volgt zou ook de bestaande tijdtoets moeten veranderen; dat valt buiten deze ingreep en behoeft nieuwe analyse als zij in de proef het gewenste onderzoek structureel tegenhoudt. Een contextuele tijdelijk hogere transport-/defensieadvance vraagt een afzonderlijk uitgewerkt besluit, geen stilzwijgend verruimde lijst in fase C.

Open gebruikerskeuze25 versus30 is voor deze rangordewijziging niet noodzakelijk. De expliciete strategische voorkeur Religion→Theocracy bestaat al. De coördinator legt de gevolgen uit; er wordt niet voor elke verplaatsing nieuw akkoord gevraagd.

## Activatie en dezelfde benchmarkstart

Gebruik voor baseline en B1 exact [QUOTA-START-T0.sav](../PROEVEN/settlerquota/vaste-start/STARTMANIFEST.md), SHA256 `8C34364200E539870E0DEA0790C98D7441925F52267D24CF0E0ADB152141AD26`, Deity/Gigantic/8 spelers. Alle normale AI-civs meten; menselijke speler en barbaren afzonderlijk houden. Leg de aanwezige civs, persoonlijkheden, kaart/instellingen, versiehashes en beginonderzoek/kennis vast; de Welshbeschrijving in het manifest bewijst niet de begintoestand van iedere civ.

Baseline moet opnieuw dezelfde passieve menselijke invoer krijgen: geen menselijke stichting, verplaatsing, queue-, diplomatie- of stadswijziging; alleen gelijke beurtvoortgang en gelijke uitlees-/savehandelingen. Beide runs hetzelfde invoerlog en dezelfde observatiemomenten. Geen vroegere b/Enterpoging in slechts één run herhalen. De bestaande T60-quotaresultaten zijn aanvullend bewijs van ander beleid, geen B1-baseline.

De AIP-manager leest disk bij opbouw en cachet bronobjecten. Een gewone save-load hoeft de disk niet opnieuw te lezen. Effectieve lijsten, lopend onderzoek en herkeuzevlag zijn in de save opgeslagen. Daarom:

1. Spel volledig afsluiten; baseline/proefbestanden en savehash controleren en exact vastleggen. Dezelfde executable, DLL, spelregels, rekentijdlimieten en uitgeschakelde SLIC-queueproef gebruiken.
2. Applicatie opnieuw starten en dezelfde T0 laden. Herstart maakt de manager opnieuw mogelijk, maar bewijst nog niet dat iedere civ haar opgeslagen lijst al heeft vervangen.
3. Vóór een causale benchmarkconclusie aantonen dat bij de relevante beginbeurt een van de acht gewijzigde lijstschrijvers actief wordt, en dat de effectieve L' respectievelijk eerstvolgende reguliere advancekeuze hiermee overeenkomt. Bij een opgeslagen lopend onderzoek wachten op het normale herkeuzemoment en dat vastleggen; niet annuleren.
4. Als bestaand read-only uitlezen niet voldoende activatiebewijs biedt, laat ctp_analist uitsluitend de lijst-/herkeuzeactivatie van deze T0 aantonen. Geen savepatch, kunstmatig nieuwe start of veronderstelde hot-reload als vervanging. Een volledige gameplayrun zonder aantoonbare activatie heeft geen geldige B1-conclusie.

Score- en packingcaches veranderen niet in B1. Voor latere locatieproeven blijft hun eigen activatiebewijs vereist.

## Controle en meetbare succescriteria

Offline vóór toepassing: back-up/manifest van de acht doelbestanden; exact aantal tokens en multiset per lijst; L' eerste twee en oude restvolgorde; alleen deze acht verschillen; alle andere AI-/game-/binarybestanden gelijk aan baseline. Geen tests toevoegen die slechts de bewerking herhalen. Een nieuwe daadwerkelijke parser-/runtimeactivatiecheck is wel relevant. Bestaande14/15 controles hoeven niet opnieuw uitgebreid te worden als hun onderzochte code niet verandert.

Technische acceptatie vereist acht geldige ingelezen lijsten, aantoonbare actieve L' bij de relevante civs en correcte keuze voor onbekend/bekend Religion en Theocracy volgens de bestaande beschikbaarheids-/tijdregels. Een UI- of logwaarneming moet effectieve keuze tonen, niet uitsluitend een bestandsnaam.

Gameplaymeetlat: T25/T50/T100 en doorlopend Religion geleerd, Theocracy geleerd, werkelijke regering/Anarchy, steden25/30 indien bereikt. Per civ tevens gekozen onderzoeksvolgorde, science, bevolking, settlervoorraad/queues, transport, militaire last, verlies en eventuele citywall-context vastleggen. Alle hoofdmetingen identiek in beide runs; kloktijden zijn geen spelbeurten.

Een eerste B1-winst is eerder geleerd Theocracy bij achterlopende normale civs, verklaard door de gewijzigde actieve lijst; geen systematische verslechtering van tijdige transport/veiligheid/uitbreiding. Geef per civ verschil in leerbeurt en gevolgen; als beide runs dezelfde research opleveren door beginvoorraad, bekendheid of tijdtoets, is dat geen bewezen winst. Voor numerieke prestatiedrempels ontbreekt nog de uitgangsmeting; die niet verzinnen. Bij duidelijke contextschade behouden wij B1 niet automatisch. Twijfel door toeval of afwijkende activatie vraagt een gerichte herhaling, geen onbegrensde reeks.

## Herstel en overdracht aan C

Herstel uitsluitend de acht bestanden uit de B1-back-up en controleer de volledige hashes; respecteer andere wijzigingen. Sluit en herstart de applicatie. Begin opnieuw vanaf de ongewijzigde T0; een save uit B1 bevat effectieve lijsten/researchvoortgang en is geen teruggedraaide baseline. Bewaar varianten/metingen afzonderlijk met manifest. Geen echte save overschrijven, CTP-og wijzigen of lopend onderzoek manipuleren.

Gereed voor coördinatorreview: inhoud, afbakening, risico's en uitvoering zijn concreet. B→C volgt pas na uitleg aan gebruiker en formele overdracht. Een activeringsprobleem gaat gericht terug naar analyse; een negatief gameplayresultaat naar ontwerp. De volledige route en technische vervolgvraag blijven in VERBETERPLAN staan.
