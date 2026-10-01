# Technische uitwerking van de gezamenlijke opening

## Vastgestelde bedoeling

Alle normale AI-persoonlijkheden volgen eerst snelle uitbreiding naar 25–30 steden, Religion → Theocracy, beperkte noodzakelijke legerlast en alleen nuttige vroege bouwkeuzes. Daarna krijgen hun eigen voorkeuren meer invloed. Barbaren vallen buiten deze gezamenlijke strategie. Dit document is een uitvoerbaar onderzoeks- en wijzigingsontwerp; de genoemde nieuwe bestanden bestaan nog niet en er is geen gameplay gewijzigd.

## Scheid strategie van tijdelijke toestand

Gebruik een eigen gedeelde uitbreidingsvoorwaarde naast de bestaande persoonlijkheidsflags. De bestaande `opening_game_strategy` blijft een economische openingsvlag: set_food_or_prod zet haar en andere bestanden gebruiken haar voor groei, wegen en bevolkingsinzet. Die vlag blind verlengen tot 30 steden verandert meerdere subsystemen tegelijk.

Voor de eerste proef stellen we 30 steden als kandidaatgrens voor, binnen de afgesproken bandbreedte. Dit is nog geen definitieve keuze. `num_cities` bestaat als engine-input en ondersteunt vergelijkingen; daarmee kan een proef uitbreiding bij num_cities<30 scheiden van de fase daarna. Dit telt geen onderweg zijnde settlers en voorkomt dus niet vanzelf overshoot. Er is geen betrouwbare settlertelling gevonden in inputs.fli.

De gewenste volledige overgang vereist ook actieve Theocracy. In de geïnventariseerde FLI-inputs is geen aangetoonde huidige-government- of specifieke advance-input gevonden. De governmentoutputs zijn wensen, geen terugmelding. `city_delta` is evenmin bewijs dat Theocracy actief is. Ontwerp daarom twee afzonderlijke onderdelen:

- Uitbreidingsbeleid gekoppeld aan het bestaande stadsantal.
- Gemeenschappelijk onderzoek en Theocracy-voorkeur, los van de persoonlijkheid tijdens de opening.

Een voorlopige overgang op alleen stadsantal is een vereenvoudiging die we expliciet moeten testen, geen uitvoering van de volledige afgesproken voorwaarde. Voeg geen fictieve input current_government of has_theocracy toe. Onderzoek de engine-interface alleen wanneer deze terugmelding noodzakelijk blijkt.

Verlies van steden kan een regel num_cities<30 opnieuw activeren. Voor een eerste experiment kan dat herstel ondersteunen; het is geen bewezen eenmalige faseovergang. Een permanente 'opening voltooid'-status vergt aangetoonde opslag/persistentie. Ook een permanente stop op 30 zou botsen met latere verovering of kolonisatie: 30 is onze vroege fasegrens, geen eeuwig maximum.

## Voorgestelde bestanden en verantwoordelijkheden

| Bestand in werkversie | Aanpassing |
| --- | --- |
| beginturnSciFew/SciMany/WarFew/WarMany/Cleric/Slaver.fli | Gedeelde fasevoorwaarde vóór de set-regels beschikbaar maken; oorspronkelijke identiteit behouden |
| Default-route | Eerst bepalen of deze in onze tests actief is; generieke templates bevatten uitgecommentarieerde includes en mogen niet als volwaardige route worden aangenomen |
| gedeelde_opening.fli (nieuw voorstel) | Eigen fasevoorwaarde op num_cities, uitgesloten voor barbaren; geen misbruik van economische openingflag |
| set_govern.fli | Bestaande persoonlijkheids-/Tyranny-regels tijdens gedeelde opening conditioneel uitsluiten; exclusieve gedeelde rangorde met Theocracy als eerste keuze |
| aiploader.fli | Eén gemeenschappelijk openings-AIP kiezen; eerste-beurtpersoonlijkheidsloads en latere modes expliciet controleren op conflicten |
| AIPs/gedeelde_opening.aip (nieuw voorstel) | Gedeelde eenheidsklassen/quota, vroege gebouw-/wonderkeuzes en onderzoeksvolgorde voor de bestaande planner |
| AIPs/gedeeld_onderzoek.aip (nieuw voorstel) | Alleen gezamenlijke onderzoeksvolgorde; beschermen tegen citywall_science zolang opening actief is |
| Defensie/oorlogsprofielen | Tijdens opening alleen noodzakelijke afwijkingen toestaan; volledige bouwlijsten uit getarmy/survival_mode kunnen de gedeelde keuzes vervangen |

Nieuwe bestandsnamen zijn voorstellen, geen enginecommando's. De bestaande action load-syntax en AIP-structuren zijn het uitgangspunt. Nieuwe fuzzy-outputnamen moeten compileerbaar en lokaal bruikbaar blijken voordat ze worden ingezet.

## Regering en onderzoek

`set_govern.fli` vraagt oorspronkelijk Tyranny bij weinig steden en bevat voor de meeste persoonlijkheden geen vroege Theocracy-voorkeur. Alleen gov_theocracy_1 toevoegen aan het einde kan conflicterende fuzzy aanbevelingen mengen. Sluit daarom de oorspronkelijke rangorderegels in de gedeelde fase uit en geef één gezamenlijke rangorde. Laat de engine beschikbaarheid en overstap uitvoeren; rangorde, fallback en overstaptiming moeten in het spel worden bevestigd.

Onderzoekslijst: Religion, daarna Theocracy, daarna een bewust samengestelde vervolglijst. Geen gratis advances. Een lijst met slechts twee items heeft een onbekende fallback na afronding; behoud dus een volledige geldige vervolglijst. De precieze vervolgvolgorde voor granary, mines, Labyrinth en voedseltechnologie wordt afzonderlijk vastgesteld.

`citywall_science.aip` zet defensieonderzoek voorop en Theocracy bijna onderaan. Tijdens gedeelde opening moet de normale defensieaanvraag niet automatisch dit onderzoek vervangen. Een expliciete noodonderzoeksuitzondering kan later worden toegevoegd bij aantoonbare noodzaak, met herstel van het gezamenlijke pad zodra de nood voorbij is.

## Samenwerking met tijdelijke profielen

| Situatie | Gewenst gedrag tijdens gezamenlijke opening | Bestaand conflict / controle |
| --- | --- | --- |
| Vrede, ruimte beschikbaar | Settlers en herhaalbare kolonistenproductie prioriteren | masssettle stopt rond eerste vijf steden; scouts hebben eigen hoge klasseprioriteit |
| Nabije menselijke hoofdstad | Veiligheid beoordelen, noodzakelijke verdediging | citywall stuurt gebouwen en citywall_science onderzoek; nabijheid alleen bewijst geen concrete aanval |
| Oorlog | Noodzakelijke verdediging en bruikbare militaire inzet; uitbreiding waar verantwoord | Oorlogsfasen vragen build_no_settlers; niet blind uitschakelen of elke oorlog als totale expansiestop houden |
| Geluk-/stadsgrensproblematiek | Tijdelijk minder vestigen en economie/regering herstellen | no_settle beheert vestigingsgoals; no_settling-output beheert andere settlerrem. Beide apart volgen |
| Continent gevuld | Bestaande marine-/transportplanning benutten | naval/supernaval kunnen klasseprioriteiten en quota wijzigen |
| Doelomvang bereikt | Settlerdruk verminderen, groei en ontwikkeling laten overnemen | Geen permanente blokkade van latere kolonisatie of verovering |
| Uitzonderlijke Labyrinth-stad | Eén geschikte stad vrijstellen | AIP-lijsten bieden nog geen bewezen selectie van precies één bergproductiestad |

Maak geen volledige AIP kopie voor elke dreiging. Streef naar een gemeenschappelijke basis met beperkte uitzonderingen, maar bevestig eerst hoe gedeeltelijke AIP-loads samensmelten. Alleen 'het openingsprofiel als laatste laden' kan veiligheidsinstellingen opnieuw overschrijven. Leg per profiel vast welke velden het mag vervangen.

## Eerste proef bewust begrenzen

De eerste implementatieproef behandelt gedeeld onderzoek/regering en uitbreiding; exacte per-stadqueues, Labyrinth-selectie, monopolyplanning en tiletoewijzing blijven afzonderlijke doelen. Stel eenheidsquota pas in na verduidelijking van negatieve waarden. Neem AAIP's voorbeeld van lagere landeenheden mee, maar niet haar garnizoennorm van twee of haar bredere stadsafstand als automatische keuze.

Behoud oorspronkelijke spelregels en tijdslimieten bij vergelijking. AAIP verandert ook globale balans en AI-rekentijd; dat hoort niet ongemerkt in dit experiment. Haal de onafgeronde SLIC-queueproef uit de actieve testconfiguratie voordat we een baseline uitvoeren, met behoud van het proefbestand als onderzoeksmateriaal.

## Validatie vóór en tijdens de eerste proef

1. Controleer voor alle normale persoonlijkheden de actieve includes en ieder profiel dat onderzoeks-/bouwlijsten kan schrijven. Verifieer dat barbaren ongewijzigd blijven.
2. Bevestig eenheidsquota, gedeeltelijke overrides, governmentrangorde en script-/FLI-inlezen bij applicatiestart. Geen statische succesclaim voor runtimegedrag.
3. Maak een vaste Deity-start en een uitgangsmeting zonder eigen queue-script. Log instellingen, persoonlijkheden en toegepaste bestandsversie.
4. Controleer de nieuwe regels bij 1, 5, 10, 25, 29 en 30 steden; dit zijn testgevallen, geen beweerde reeds aanwezige saves. Controleer vrede, oorlog en gelukrem afzonderlijk.
5. Observeer Religion/Theocracy-keuze, werkelijke regering, settlers onderweg, stedental, legerlast en bouwkeuzes. Een gewenste output is geen bewezen actie.
6. Vergelijk turn25/50/100 en stichtingsbeurt stad25/30. Controleer stadsverlies en economische schade. Noteer specifiek of de AI bij faseovergang nog buiten Theocracy zit.

## Eerstvolgende concrete werkzaamheden

Maak een veldmatrix voor alle bouw-/onderzoeksoverrides en verduidelijk negatieve quota. Ontwerp daarna de kleinste werkversiewijziging met exclusieve governmentregels, gezamenlijke onderzoekslijst en een apart stadsantalcriterium. De exacte Theocracy-terugmelding en Labyrinth-stad blijven expliciet open; geen ongeteste fictieve engine-inputs of claim van volledige stadsspecialisatie.
