# Militaire ondersteuning, paraatheid en public works

6 oktober 2026, fase A. Alleen-lezen onderzoek; geen spelstarts of gewijzigde spelbestanden. T = tekstregels, B = machinecode, E = uitvoering van oorspronkelijke instructies met synthetische toestand. Geen volledige beurt of nieuwe gameplaymeting.

## Betekenis voor ons project

**T/B/E:** extra legereenheden kosten productie via SHIELD_HUNGER, regering en paraatheid. Public works wordt vervolgens uit de overgebleven productie genomen. Minder onnodige soldaten kan dus zowel bouwtempo als PW verbeteren. Dit is een productielast; een directe inhouding op scientist-science is hier niet gevonden. Eventuele verdringing van science via bevolkingsinzet, bouwtijd en economie moet afzonderlijk worden afgewogen.

Settlers hebben in de originele [Units.txt](../CTP-og/ctp_data/default/gamedata/Units.txt) SHIELD_HUNGER0. Hun hoge bouwkosten betekenen geen overeenkomstige militaire onderhoudslast. Warrior/Hoplite hebben hunger4, Triremes16. De onderzochte formule geeft per Warrior0.4/2/4 productie bij peace/alert/war, vóór afronding van het gezamenlijke budget; dit zijn geen per-unit afgeronde bedragen. Originele [govern.txt](../CTP-og/ctp_data/default/gamedata/govern.txt) gebruikt daarvoor0.1/0.5/1.

## Bestaande AI-aansturing

**T:** [set_military_readiness.fli](../CTP-og/ctp_data/default/aidata/set_military_readiness.fli) vraagt onder meer oorlogsniveau tijdens opening_gambit_time, met commentaar over bescherming tegen barbarians en vertraging. Commentaar bewijst geen concrete beurtgrens. Normale peace-/oorlogs-/survivalcondities vragen andere niveaus; fuzzy regels kunnen tegelijk bijdragen. De algemene beginturn.fli heeft de include uitgecommentarieerd, de persoonlijkheidsvarianten bevatten hem wel. Eén tekstregel bewijst dus geen feitelijke instelling voor iedere beschaving.

**B:** FSFuzzyBeginTurnPost20036280 zet de output desired_military_readiness om naar0 bij waarde<0.5,1 bij0.5–<1.5, anders2. Player-slot+e0 leidt via5290e0 naar4c1370 en4cf220. De setter bewaart de nieuwe toestand, gebruikt TURNS_TO_NEW_READINESS bij verhoging zonder force en berekent een HP-overgang uit oude/nieuwe READY_*_HP. Verlaging/force gebruikt duur1 en beginmarker−1. Volledige HP-/unitupdate en gereedkomen van die overgang zijn niet uitgevoerd. Zie [AI-control](BINAIR/economy-readiness-pw-ai-control.txt), [slots](BINAIR/economy-readiness-pw-player-slots.json), [enginegetters](BINAIR/economy-readiness-pw-engine-getters.txt) en [supportkern](BINAIR/economy-readiness-support-core.txt).

**B:** Player-slot+e8→529120 geeft zowel trunc(Readiness+10) als Readiness+10 / Player+11a8, bij nulproductie0. Die verhouding vult percent_cost_readiness. Zij gebruikt bruto totale productie, terwijl de werkelijke afdracht later een subtotal van deelnemende steden gebruikt. Zie [wrapper](BINAIR/economy-readiness-pw-engine-wrappers.txt) en [getters](BINAIR/economy-readiness-pw-engine-getters.txt).

**T/B:** [set_pw.fli](../CTP-og/ctp_data/default/aidata/set_pw.fli) vraagt PW-afdracht afhankelijk van opening, voorraad, oorlog, unitfocus en loon-/goudlast. [set_food_or_prod.fli](../CTP-og/ctp_data/default/aidata/set_food_or_prod.fli) schrijft dezelfde output; de samengestelde fuzzy-uitkomst blijft leidend. FSSetTaxes20029280 geeft production_tax via Player-slot+90 aan527e20→4bb380. Geldige waarde0–1 wordt naar gehele procenten afgekapt en als double op Player+1160 opgeslagen; buiten bereik blijft de eerdere waarde behouden. Zie [xrefs](BINAIR/economy-readiness-pw-output-xrefs.txt), [AI-control](BINAIR/economy-readiness-pw-ai-control.txt) en [setter](BINAIR/economy-readiness-per-unit-and-pw.txt).

## Eenheidskosten en vrijstellingen

**B/E:**4cf080 gebruikt echte unit-/recordgetters en berekent per eenheid:

`kosten = SHIELD_HUNGER × READY_niveau_COEF × (1 − readiness_wonderpercentage /100)`

Unit4da810→46ec50 leest UnitRecord+bc; parser46d5c7–d1 bindt dat aan token52 SHIELD_HUNGER. Queue-SHIELD_COST en Deity-productiekorting zijn een andere keten. Zie [unit-inputs](BINAIR/economy-readiness-unit-inputs.txt), [recordparser](BINAIR/food-growth-unitdb-record-parser.txt) en [Deity-kosten](DEITY-KOSTEN-EN-TECHNOLOGIEFASEN.md).

| Voorwaarde | Gevolg |
| --- | --- |
| UnitData+44 bit100 via4dcab0 | Kosten0; exacte herkomst/betekenis van deze instanceflag blijft open. |
| NEEDS_NO_SUPPORT via4dcad0 | Kosten0; token129→dispatchindex62→46bd4b zet UnitRecord+34 bit1000. |
| IS_SPECIAL_FORCES | Gebruik altijd READY_WAR_COEF; token230→index163→46c8b0 zet Record+40 bit100. |
| Gewone eenheid, toestand0/1/2 | Government+100/+110/+120; andere toestand coefficient0. |

Bronnen: [per-unitfunctie](BINAIR/economy-readiness-per-unit-and-pw.txt), [vrijstellingsgetters](BINAIR/economy-readiness-unit-exempt-getters.txt), [flagdispatch](BINAIR/economy-readiness-unit-flags-entry.txt), [token/casebinding](BINAIR/economy-readiness-unit-flags-binding.json), [regeringsparser](BINAIR/economy-budget-government-parser.txt) en [warvelden](BINAIR/economy-readiness-parser-completion.txt). Token489/490/492/494 binden duur/peace/alert/war in [tokenbewijs](BINAIR/economy-readiness-field-tokens.txt).

4cf3c0 telt doublekosten over armies/units bij elkaar in Readiness+10. Wondercallback471fe0 somt toepasselijke record+3c-bonussen met een obsolete-advancecontrole. Token455 WONDER_FLAG_REDUCE_READINESS_COST→470763→470779 bindt+3c. Sphinx heeft75, vervalt bij Age of Reason. Zie [wondertoken](BINAIR/economy-readiness-wonder-token.txt), [flagsparser](BINAIR/trade-goods-effect-flags-full.txt), [geldige case/tail](BINAIR/economy-readiness-parser-valid.txt) en [callback](BINAIR/trade-goods-effect-parser-route.txt). De callback is in de controles expliciet gemockt; het is geen gemeten volledige wonderlifecycle.

## Werkelijke verdeling over steden

**B:** Player4b7dd0 laat4dc900→4e49a0→City494280 eerst bruto productie berekenen, inclusief de eerder gebonden stadsmodifiers. City+98 bepaalt bijdrage aan het militaire subtotal, City+94 de PW-deelname.4942f0–494307 kopieert beide flags naar de outputs. De instelling/uitzonderingsherkomst van die flags is nog open. Zie [rijksfunctie](BINAIR/economy-readiness-production-deduction.txt), [City-wrapper](BINAIR/economy-readiness-city-final-binding.txt) en [flagoutputs](BINAIR/economy-readiness-final-eligibility.txt).

In de gewone context met Player+1184=0 is het gehele onderhoud `trunc(totaalkosten +1e-7)`. De ratio is dat bedrag gedeeld door het militaire subtotal. Bij subtotal<1 gebruikt de functie ratio0 en totale restschuld0. Een onbekende extra productiecredit op Player+1184 wordt eerst verrekend; die is geen aangetoond Deity-bonusveld. Player+1194 bepaalt het overslaan van shortagecallback4cf460. Volledige tekortreactie/disbanding valt buiten deze controle.

Voor iedere stad behalve de laatste voert494870 uit:

1. Bij City+98: trek `ceil(brutoproductie × onderhoudsratio)` af; anders0.
2. Bij City+94: trek `trunc(resterende productie × PW-tax +1e-6)` af; anders0.
3. Geef beide bedragen terug. Player telt de PW-bedragen bij voorraad Player+12f0 via4afb90.

**B/E:** de laatste stad gebruikt494900: trek de gehele restschuld af, bereken PW met trunc zonder epsilon, en begrens de eindproductie minimaal0. Deze functie raadpleegt City+94/+98 niet opnieuw. Bovenwaartse afronding bij eerdere steden kan de restschuld negatief maken; in een synthetische drie-stedencontext met productie1/1/1 en gezamenlijke last1 blijft0/0/2 over. Dat is budgetcorrectie tussen steden, geen gratis totale productie. De daadwerkelijke stadsvolgorde en bijzondere vrijstellingen verdienen aandacht bij latere gameplaymetingen.

Bij twee steden met ieder100 productie, gezamenlijke last40 en20% PW: iedere stad betaalt20 onderhoud en16 PW en houdt64 bouwproductie over; PW-voorraad stijgt32. Zie [stadsberekening](BINAIR/economy-readiness-pw-city-arithmetic.txt), [laatste stad](BINAIR/economy-readiness-final-eligibility.txt) en [rijksverdeling](BINAIR/economy-readiness-production-deduction.txt).

## Verificatie en grenzen

[Controleer-Militaire-Steun-En-PW.py](../PROEVEN/Controleer-Militaire-Steun-En-PW.py) voert oorspronkelijke instructies uit:9 eenheidsgevallen,6 gewone stadsgevallen,4 laatste-stadgevallen,6 belastingsettergevallen en4 rijksverdelingen. **29/29 slagen**, [resultaat](BINAIR/economy-readiness-pw-checks.json). Unit-/recordlookup en wonderpercentage zijn mocks; originele kostgetters/flagchecks/formules lopen. Rijksgevallen mocken bruto productie en handle-resolutie en zetten de bestaande shortage-bypassflag. Geen complete beurt, unitlijst-som, tekortreactie of HP-lifecycle wordt daarmee bewezen. De eerste verwachting bij7/7/7 productie vergat PW van de laatste stad; die rekenfout is gecorrigeerd en verklaard in de helper.

Engine-SHA b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79, imagebase400000, timestamp37d6f702. Geen adressen uit de niet-passende civctp.map. Tests gebruiken x87-controlword37f en [CRT-hulp](../PROEVEN/ctp_x87.py); exacte floating-pointgrenzen onder de echte gamecontrolword blijven runtime-onbekend. Onderzoeksmateriaal met een ongeldige beginboundary in parser-completion wordt niet als instructiebewijs gebruikt; parser-valid bevat de geldige wondercase/tail.

Voor de vervolgafweging moeten paraatheid en unitquota samen worden bekeken: goedkoop bouwen op Deity heft SHIELD_HUNGER niet op. Openingwar, transportlast, wonderbouw en PW concurreren om dezelfde productie. Een concrete alternatieve instelling volgt pas in fase B; eerst nog geluk/WGF, routekosten/Labyrinth en de overige relevante matrixvragen.
