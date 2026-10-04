# Vergelijking drie handmatige T60-saves

Op T60 hebben de twee quotavarianten samen 66 AI-steden, tegenover 49 in de oorspronkelijke baseline (+34,7%). De totale stadsbevolking stijgt van 104 naar 124 (+19,2%). Daar staat een grote voorraad losse settlers tegenover: 71 bij -20 en 78 bij +20, versus 3 in de baseline. Een hoge primary-quota beïnvloedt dus zichtbaar de settlerproductie en uiteindelijke uitbreiding, maar vormt nog geen goede uitbreidingsstrategie.

## Methode en bewijs

Alle zeven AI-beschavingen geobserveerd via Cheat Mode > spelerselectie > Edit City > City Status en Unit Status. Menselijke Romans/Julius (speler 1) uitgesloten. Gebruiker heeft de drie runs vanaf dezelfde vaste T0-save gespeeld. De baseline gebruikt oorspronkelijke AIP-waarden, geen uniforme -2; de varianten wijzigen uitsluitend UNIT_SETTLER in Land_Settler_Troops_Primary van dertien normale AIPs.

De eindtoestanden zijn geladen en visueel gecontroleerd op 1000 BC (T60); de +20-save toont ook Turns 60 in het laadscherm. Tijdens deze analyse zijn geen beurten gespeeld, steden geplaatst, productieopdrachten gewijzigd of saves opnieuw opgeslagen. De oorspronkelijke AIPs bleven geïnstalleerd tijdens het uitsluitend lezen van deze eindtoestanden; dit is geen vervolg van de varianten onder hun proefconfiguratie.

| Variant | Bewaarde kopie | SHA256 |
| --- | --- | --- |
| Baseline | baseline/T60-gebruiker.sav | 42DB1F21ECB6A8A2079B8A675DFF72792BB060E1CC4CFB5E3AC32F77DA03A77D |
| -20 | min20/T60-gebruiker.sav | 3A15D526950A7ABF0DE3874E477F555667E34250F770415928898638AE99F547 |
| +20 | plus20/T60-gebruiker.sav | 4DD0984913D3DE5376E7BDDDF8FB47796F427E3FD643804EFED29C302A1DB7D3 |

Volledige screenshots: `<variant>/observatie-T60/Pn-player.png`, `Pn-cities.png` en `Pn-units.png`. Voor lijsten langer dan negen rijen ook `Pn-cities-bottom.png`. De compacte `Pn-overzicht.png` combineert uitsneden daarvan. De aanvankelijk verkeerde Welsh/min20-eenhedenopname is vervangen en het overzicht opnieuw opgebouwd. Meetgegevens ook in [METINGEN-T60.csv](METINGEN-T60.csv).

Stadsbevolking is de som van stadsgroottes, afgeleid uit de indicator (10.000 weergegeven inwoners per grootte-eenheid) en gecontroleerd met stadsrijen. Losse settlers zijn alle bestaande Settler-eenheden in Unit Status; dit bewijst niet dat elk daarvan stil staat of een opdracht mist. 'In bouw' telt huidige settlerproductie over alle stadsrijen, geen toekomstige queue. Onderhoud is de weergegeven Military Support Cost, geen totale economische kosten van een beschaving.

## Steden per beschaving

| Beschaving | Baseline | -20 | +20 | Verschil variant / baseline |
| --- | ---: | ---: | ---: | ---: |
| Welsh | 7 | 3 | 3 | -4 |
| Cubans | 7 | 6 | 6 | -1 |
| Egyptians | 9 | 14 | 14 | +5 |
| Nigerians | 8 | 7 | 7 | -1 |
| Koreans | 5 | 10 | 10 | +5 |
| Mongols | 6 | 16 | 16 | +10 |
| Assyrians | 7 | 10 | 10 | +3 |
| **Totaal** | **49** | **66** | **66** | **+17** |

Beide tekens leveren op dit meetpunt voor iedere beschaving dezelfde steden en stadsbevolking. De overige eindtoestanden zijn niet identiek.

## Volledige metingen

| Beschaving (speler) | Variant | Steden | Stadsbevolking | Losse settlers | Settlers in bouw | Militair onderhoud |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Welsh (2) | Baseline | 7 | 15 | 0 | 3 | 82 |
| Welsh (2) | -20 | 3 | 9 | 11 | 3 | 34 |
| Welsh (2) | +20 | 3 | 9 | 12 | 3 | 24 |
| Cubans (3) | Baseline | 7 | 16 | 2 | 1 | 136 |
| Cubans (3) | -20 | 6 | 13 | 17 | 3 | 38 |
| Cubans (3) | +20 | 6 | 13 | 21 | 3 | 20 |
| Egyptians (4) | Baseline | 9 | 19 | 0 | 2 | 104 |
| Egyptians (4) | -20 | 14 | 26 | 13 | 4 | 36 |
| Egyptians (4) | +20 | 14 | 26 | 13 | 6 | 36 |
| Nigerians (5) | Baseline | 8 | 16 | 0 | 2 | 124 |
| Nigerians (5) | -20 | 7 | 15 | 5 | 7 | 44 |
| Nigerians (5) | +20 | 7 | 15 | 5 | 7 | 44 |
| Koreans (6) | Baseline | 5 | 11 | 1 | 2 | 65 |
| Koreans (6) | -20 | 10 | 16 | 3 | 8 | 31 |
| Koreans (6) | +20 | 10 | 16 | 3 | 8 | 31 |
| Mongols (7) | Baseline | 6 | 12 | 0 | 0 | 121 |
| Mongols (7) | -20 | 16 | 24 | 8 | 5 | 38 |
| Mongols (7) | +20 | 16 | 24 | 8 | 5 | 38 |
| Assyrians (8) | Baseline | 7 | 15 | 0 | 2 | 121 |
| Assyrians (8) | -20 | 10 | 21 | 14 | 3 | 39 |
| Assyrians (8) | +20 | 10 | 21 | 16 | 5 | 15 |
| **Totaal** | **Baseline** | **49** | **104** | **3** | **12** | **753** |
| **Totaal** | **-20** | **66** | **124** | **71** | **33** | **260** |
| **Totaal** | **+20** | **66** | **124** | **78** | **37** | **208** |

## Analyse per beschaving

- **Welsh:** beide varianten blijven op drie steden hangen en bouwen in alle drie nog settlers, met al elf/twaalf bestaande settlers. De baseline heeft drie Triremes; beide varianten geen enkel schip in Unit Status. De oorspronkelijke units.txt definieert Triremes met CAN_CARRY_SMALL_LAND en TRANSPORT_CAPACITY 2. Ontbrekend transport is dus een concrete kandidaat voor het niet ontsluiten van nieuwe gebieden; routes, bereikbaarheid en individuele settleropdrachten zijn niet onderzocht. Dit is geen bewijs dat alleen de eilandgrootte de oorzaak is. De baseline bereikt immers zeven steden.
- **Cubans:** zes in plaats van zeven steden, maar zeventien/eenentwintig settlers tegenover twee. Baseline heeft twee Triremes en één Fire Trireme; -20 één Trireme, +20 geen schip. De -20-save bouwt nog een Trireme in Guantanamo; +20 daar Marketplace. Dit vraagt dezelfde controle van transport en vestigingsmogelijkheden. +20 heeft daarnaast minder militaire eenheden dan -20.
- **Egyptians:** jouw telling bevestigd: negen naar veertien steden (+55,6%), bevolking negentien naar zesentwintig. Beide varianten hebben dertien settlers en onderhoud 36 versus 104 in de baseline. -20 bouwt settlers in Thebes, Memphis, Sinai en Sebennytos; +20 ook in Alexandria en Giza. Baseline Thebes bouwt Sphinx; de varianten daar Settler. De productiekeuze reageert dus duidelijk, ook waar de uiteindelijke stedentelling gelijk is. Dit bewijst geen totale wonderhistorie.
- **Nigerians:** zeven in plaats van acht steden en vijf settlers, terwijl alle zeven steden settlers bouwen. Kashgar staat in de baseline bij Nigerians en in beide varianten bij Mongols. Het verschil in totaal omvat dus ook verschillende eigendomsuitkomsten; een eindstand onderscheidt stichting, verovering en conversie niet.
- **Koreans:** vijf naar tien steden, bevolking elf naar zestien, met drie losse settlers. Acht van de tien steden bouwen nog settlers; Seoul bouwt Caravan en Anyang City Wall. In deze eindstand relatief weinig bestaande settlers per stad vergeleken met de andere varianten, maar inzet en uitbreidingstempo zijn zonder tussensaves niet vastgesteld.
- **Mongols:** zes naar zestien steden (+166,7%), bevolking verdubbelt van twaalf naar vierentwintig. Acht losse settlers en vijf steden met settlerproductie. Grootste winst, maar deels kan ook stadsbezitverschil meespelen (Kashgar). De overige productie omvat onder meer Caravans, Aqueducts, Granaries, Marketplace en Knights; Gushun Usu heeft geen weergegeven huidige productie. Nog geen gerichte production/science-specialisatie vastgesteld.
- **Assyrians:** zeven naar tien steden en bevolking vijftien naar eenentwintig. -20 heeft veertien settlers en drie settlerbouwers; +20 zestien en vijf. Nineveh bouwt Phalanx bij -20 maar Settler bij +20; Gasur Archer bij -20 maar Settler bij +20. Onderhoud daalt van 121 naar 39/15. +20 is dus duidelijk anders dan -20 ondanks hetzelfde aantal steden.

## Wat dit bewijst en wat nog open staat

De eerdere T20-meting was te vroeg en te beperkt om het effect op het aantal steden te beoordelen. T60 toont bij vier van zeven beschavingen meer steden, bij drie minder. In totaal levert de wijziging meer steden en stadsbevolking en veel minder militaire onderhoudslast op. Dat laatste bewijst nog geen hogere netto research of voldoende veiligheid: onderzoek, inkomsten, infrastructuur en dreigingen zijn niet volledig gemeten.

De grote settlervoorraden maken permanente ±20-instelling ongeschikt als bewezen eindoplossing. Vooral Welsh/Cubans laten zien dat productie en succesvolle vestiging afzonderlijke problemen zijn. Dit corrigeert ook de eerdere hypothese dat een groter negatief getal eenvoudigweg meer steden betekent. Beide grote waarden kunnen een onvervulde vraag creëren; verschillen tussen hun eindtoestanden bewijzen nog niet welke berekening de DLL voor ieder teken gebruikt. Randomness en vervolginteracties kunnen eveneens verschillen veroorzaken. Eén run per variant op één kaart bewijst geen algemene prestatie.

Geen beschaving bereikt op T60 ons gewenste bereik van 25–30 steden. Deze proef levert een bruikbaar aangrijpingspunt, geen voltooiing van de projectdoelen.

## Aanbevolen vervolganalyse

Onderzoek eerst de bestaande aansturing voor het daadwerkelijk gebruiken van de aanwezige settlers: no_settle/yes_settle en city_delta, vestigingsdoelen, locatiewaardering/afstand en transportvraag voor eilanden. Vergelijk Welsh/Cubans als voorbeelden van ophoping en Egyptians/Mongols als voorbeelden van succesvolle uitbreiding. Bepaal pas daarna een begrensde settlervraag binnen onze gezamenlijke uitbreidingsfase, met ruimte voor transport, minimale veiligheid en de afzonderlijke Labyrinth-productiestad. We moeten sturen op 25–30 bruikbare steden, niet op een grote voorraad settlers. Dit is een voorstel; geen nieuwe gameplaywijziging uitgevoerd.

## Bedieningsfouten en afsluitcontrole

Tijdens baseline-observatie is een overbodige poging gedaan het stadsvenster van de menselijke speler zonder steden te openen. Dat gaf een melding; die is gesloten, geen stad geplaatst. De correcte Welsh-opname is daarna opnieuw gemaakt. Bij min20/Welsh verschoof een vensterdrag de interne cursor, waardoor de eerste eenhedenopname nog het stadsvenster liet zien. De cursorreferentie in Observeer-T60.ps1 is gecorrigeerd, Unit Status opnieuw geopend en de opname vervangen. Deze fout betreft bediening, geen gemeten gameplay-effect.

Na de observaties zijn alle drie bron-savehashes opnieuw gecontroleerd en ongewijzigd. Alle veertig oorspronkelijke proef-AIPs zijn op hash gelijk aan CTP-og. De spelinterface is teruggezet naar de menselijke speler en de observatiepanelen zijn gesloten; geen eindtoestand opnieuw opgeslagen.
