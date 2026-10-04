# Voortgang CTP I AI

Bijgewerkt: 4 oktober 2026. Dit bestand is het hervatpunt voor de vaste projectagent; de oorspronkelijke doelen en analyses blijven de inhoudelijke bron.

Voor de actuele werkzaamheden van de analist: [VOORTGANG-ANALIST.md](ANALYSE/VOORTGANG-ANALIST.md). De analist onderhoudt dat eigen voortgangsbestand bij relevante deelresultaten; dit projectstatusbestand blijft bij de coördinerende agent. Beide zijn momentopnamen, geen live procesmonitor.

Rapportageafspraak: tijdens actief werk minstens iedere tien minuten concrete feedback, ook bij stagnatie; direct bericht bij afronding, onderbreking of wachten. Zie AGENT-CTP.md. Deze afspraak activeert geen losstaande timer of geplande taak.

**Projectdoel gepauzeerd:** op 4 oktober 14:58 heeft de gebruiker gevraagd 'rond af voor nu'. Status `paused` is door de doelruntime bevestigd. Geen actief onderzoek of deelagentwerk. Ook na de vijfuurreset wordt niet automatisch hervat: deze latere gebruikerspauze gaat voor de eerdere resetafspraak. Resultaten en onderstaande hervatpunten blijven behouden; verdere uitvoering wacht op een hervatopdracht.

**Budgetgrenzen:** weekwaarschuwing bij ≤25% resterend, weekstop bij ≤10%; vijfuurstop bij ≤5% resterend en zelfstandig hervatten na bevestigde reset als het weekbudget dit toestaat. De actieve sessielog bevat uitleesbare limietmetadata; PROEVEN/Controleer-Weekbudget.py controleert beide vensters en de actualiteit. Laatste verse controle op 4 oktober 13:54: week87%, vijfuur20% resterend, dus geen grens geraakt; vijfuur-resetmelding 1791129333. Dit is een tijdgebonden meting, geen actuele permanente stand. Zie AGENT-CTP.md voor de stop-/hervatprocedure.

## Actuele mijlpaal M1 / fase A

**Vijfuurstop bevestigd, 4 oktober 14:05:** verse sessiemelding 14:04:32 gaf 5% resterend in het 300-minutenvenster, week85%. Alle inhoudelijke analyse/ontwerp/tests zijn toen gestopt. Analist voltooid; de hoofdagent heeft op reset gewacht totdat de gebruiker om 14:58 expliciet pauzeerde. Gemelde reset `1791129333` = 4 oktober 17:55:33 Europe/Amsterdam. Bij een latere hervatopdracht eerst verse budgetcontrole; de reset alleen heft de gebruikerspauze niet op.

**Hervatpunt na budgetreset:** onderzoek-/regeringsrapport is gelezen en gecontroleerd (34 links,14/14 codecontroles); dekkingsmatrix bijgewerkt. Eerst Government-recordvelden +140/+130 en overgangscontext +11e0 binden. Onafhankelijke voedselroute: UnitRecord+40 bit4000 naar BUILDING_REMOVES_A_POP en Player+4/aanroepargument binden, daarna 496a50/4cc6b0-verwijderingsgevolgen. De laatste korte OR-immediatezoekopdracht leverde geen kandidaten en verandert deze onzekerheid niet. Brede fase A blijft open; geen gamebestanden of binaries veranderd.

**Brede functionele analyse van code, spelregels en AI-beslisketens.** De gebruiker heeft de scope verbreed: eerst begrip als fundament, daarna wijzigingsvoorstellen met uitleg, pas daarna toepassing en tests. Geen nieuwe spelstarts of gameplay-/binarywijzigingen tijdens fase A.

Gereed wanneer:

- De onderwerpen uit AGENT-CTP.md staan in ANALYSE/DEKKING.md met bewijsstatus, relevante analyses en open vragen.
- De beslisketens en afhankelijkheden zijn beschreven: van spelregel en AI-input via selectie/prioriteiten tot actie en savegedrag.
- Voor mechanismen waarop voorstellen moeten steunen zijn essentiële kennislacunes opgelost of als technische grens met bewijs beschreven.
- AAIP-claims zijn waar relevant gekoppeld aan daadwerkelijke verschillen, zonder claims als runtimebewijs te behandelen.
- De analyseoverdracht aan fase B bevat conclusies, open punten en hun impact. Een inventarisatie alleen is nog geen afgeronde analyse.

## Rollen en volgende fasen

| Fase | Agent | Status |
| --- | --- | --- |
| A: bestaande game/AI begrijpen | ctp_analist | Huidige fase; dekking en beslisketens uitwerken |
| B: wijzigingen met uitleg voordragen | ctp_ontwerper | Wacht op analyseoverdracht |
| C: toepassen en testen | ctp_uitvoerder | Wacht op uitgewerkt en uitgelegd voorstel |

De hoofdagent coördineert en beheert dit statusbestand. ctp_verbeteraar blijft een herbruikbare coördinatorrol; geen extra coördinatorsessie nodig. Geen drie agents tegelijk wijzigingen aan dezelfde scope laten voorbereiden of uitvoeren.

## Reeds onderbouwd

| Onderdeel | Bron / uitkomst |
| --- | --- |
| Quota | Negatief vast aantal; positief per stad; aanwezige en in productie zijnde eenheden tellen mee. Zie ANALYSE/RUIMTE-BUREN-TRANSPORT.md |
| Bestaande proeven | ±20 meer steden bij sommige civs, maar veel ongebruikte settlers; geen bewezen eindbeleid. Zie PROEVEN/settlerquota/reeks/VERGELIJKING-T60.md |
| Kandidaatmasker | Packing-uitsluitingen worden bewaard; nieuw packing herstelt oude uitsluitingen niet vanzelf. Zie ANALYSE/VESTIGINGSMASKER.md |
| Locatiescore | Voedselgroepen, productie/goud en good-aanwezigheid; 68 formulecontroles tegen originele instructies. Zie ANALYSE/LOCATIEKWALITEIT.md |
| Scorecache | Tabelserialisatie en exact herstel in twee synthetische controles; volledige applicatie-updatecondities nog open. Zie ANALYSE/SCORECACHE-EN-INGREEPPUNTEN.md |
| Selectie | Score werkt al in kandidaatordening, daarna doelaanmaak en prioriteit; alleen een late bonus kan goede locaties missen |
| AIP-load | Effectieve toestand is samengesteld, blijft tussen beurten bestaan en wordt gesaved; aanwezigheid bepaalt scalarkopie, lijsten worden per categorie vervangen. UNLIMITED-uitzondering en cachelevensduur geduid; 15 offlinecontroles. Zie ANALYSE/AIP-LAADWERKING.md |
| Groeivoorraad/silo | Granary-buffer en groeivoorraad zijn afzonderlijk; na groei met silo helft nieuwe basisdrempel, zonder silo oude drempel aftrekken. 24 gecontroleerde originele codegevallen met externe mocks. Volledige consumptie/settler/modifiers nog open; zie ANALYSE/VOEDSEL-GROEI-EN-KOLONISTEN.md |
| Goods | World-interface geeft echte GOOD_INDEX via offset 0xb4; eigen good-tellingen nog niet volledig geduid |

## Eerstvolgende werkzaamheden

1. Inventariseer bestaande kennis per onderwerp en leg dekkingsmatrix/onderzoeksgaten vast. Hergebruik onze analyses; geen herstart vanaf nul.
2. Beschrijf de samenhangende beslisketens en bepaal welke gaten eerst opgelost moeten worden.
3. Hervat gericht terrein-/improvementbinding en eigen good-tellingen als onderdeel van de brede analyse. Duid lokaal/import/export en beschikbare voorraad voordat die als monopolyvoorraad wordt gebruikt.
4. Onderzoek de overige spel- en AI-mechanismen die de opening, economie, onderzoek, bouwkeuzes, specialisatie, handel en marine bepalen.
5. Lever de analyseoverdracht; laat daarna pas de ontwerper ingrepen, prioriteiten en proeven voorstellen.

## Werkafspraken en blokkades

- CTP-og ongewijzigd; werkversie CTP-proef; AAIP alleen leermodel.
- Geen nieuwe GUI-proeven tijdens fase A. Eventuele latere doorloop door de gebruiker bundelen in een concrete proefopdracht.
- De 25–30-grens en andere nog open strategische keuzes hoeven onafhankelijke analyse niet te blokkeren.
- De custom agentconfiguratie is voorbereid; automatische detectie door de client is nog niet bewezen. Doelmodus is inmiddels expliciet geactiveerd en bevestigd; er is geen afzonderlijke geplande taak ingesteld.
- Eén schrijver voor dit statusbestand: de coördinerende agent. Deelagents leveren hun eigen analyses en melden hun voortgang.

## Uitvoering op 4 oktober 2026

Eerder is de sessieagent `/root/ctp_verbeteraar` gestart voor terrein-/voedselpotentieel. Bij controle na de onderbreking is deze sessieagent niet actief en is het bedoelde eindrapport niet aanwezig. Er was wel een tussentijdse melding over bestaande terrein- en improvementinterfaces; behandel die nog niet als afgerond onderzoek. De nieuwe drie-fasenindeling neemt deze onderzoeksvraag over. Een sessieagentstart bewijst geen automatische detectie van de TOML-rol of geactiveerde doelmodus/planning.

De sessieagent `/root/ctp_analist` heeft het eerste analysepakket opgeleverd: ANALYSE/DEKKING.md en ANALYSE/BESLISKETENS-OVERZICHT.md. Volgens zijn eindrapport zijn alle 73 lokale verwijzingen gecontroleerd. Dit pakket inventariseert bestaande kennis en prioriteert onderzoeksgaten, maar rondt fase A niet af. Ontwerper en uitvoerder zijn niet gestart.

De analist is daarna met een follow-up gestart voor effectieve AIP-loadwerking: volgorde, vervangen/samenvoegen van lijsten en scalars, defaults/behoud en samenhang tussen beurten. Beoogd resultaat: ANALYSE/AIP-LAADWERKING.md. De tienminuten-rapportageafspraak is bij die start expliciet meegegeven. De huidige fase blijft analyse zonder spelstarts of gameplaywijzigingen.

Dit AIP-pakket is om 13:35 afgerond: 15/15 offlinecontroles, 29 gecontroleerde bronverwijzingen en eigen voortgang bijgewerkt. De hoofdagent heeft de overdracht gelezen. De analist is om 13:41 daadwerkelijk met de volgende follow-up gestart: effectieve onderzoekslijst → concrete advancekeuze → regeringskeuze. Ownership: ANALYSE/ONDERZOEK-EN-REGERINGSKEUZE.md, BINAIR/research-government-* en eigen voortgang; andere bestanden blijven bij de hoofdagent. De nieuwe budgetgrenzen zijn meegegeven en gecontroleerd vóór de start.

De hoofdagent heeft onafhankelijk het eerste voedsel-/groeipakket vastgelegd in ANALYSE/VOEDSEL-GROEI-EN-KOLONISTEN.md. Player/GameState/BuildingDB/Population/Government zijn via echte GUID-/constructorroutes gebonden; 24 granary-/groeivoorraadcontroles slagen. Alle 21 lokale rapportverwijzingen bestaan. Volledige voedselconsumptie, stadsunitfactor/default, Deity-/geluksmodifiers en settler-voltooiing zijn expliciete vervolgvragen, geen bewezen eindformules. Oudere partial-override-onzekerheden in QUOTA, GEDEELDE-OPENING, ARCHITECTUUR, DEKKING en BESLISKETENS zijn naar het afgeronde AIP-rapport verwezen/geactualiseerd. De volgende coördinatorstap is de voedselketen vervolgen terwijl de analist onderzoek/regering uitwerkt. Fase A blijft open.

De uitleesbare budgetcontrole onderscheidt nu beide vensters; 14 offlinegevallen controleren grenswaarden, voorrang bij beide stopredenen, ontbrekende vensters en verouderde meldingen. De gecontroleerde stopprocedure staat in AGENT-CTP.md; er is geen aparte geplande hervattaak of serverlimiet geïnstalleerd. Een uitsluitend vijfuurstop wacht binnen de actieve doelopdracht op bevestigde reset; een weekstop pauzeert het doel volgens de gebruikersinstructie.

Om 13:55 heeft de coördinator de geluksmodifier aan VERY_HAPPY_THRESHOLD 85 gebonden en de verkeerde term 'ongeluksvoorwaarde' in het groeirapport gecorrigeerd. Ook de Religionkosten in ANALYSE-EARLY-GAME.md zijn gecorrigeerd naar 65, gecombineerd pad naar Theocracy 130. Settler-/unit-toelating en enqueue zijn nu via echte Player-slots tot CityData en BuildQueue gevolgd; productie/voltooiing, population-loss en voorraadgevolgen blijven het concrete hervatpunt. De analist rondt zijn onderzoek-/regeringspakket af; nieuw breed werk heeft nu lagere prioriteit dan het vastleggen van de lopende ketens bij dalend vijfuurbudget. Geen gamebestanden gewijzigd.

Om 13:59 is de unitvoltooiingsbranch op 48f7eb gevolgd: bit4000 van UnitRecord+40 geeft een contextafhankelijke bevolking<2-controle; na aanmaak bestaat een conditionele groeivoorraad-aftrek van integer(CITY_GROWTH_COEFFICIENT), clamp0, plus bevolkingsselectie/verwijderingsaanroep. Nog geen volledige settlerregel: flagtokenbinding, Player+4/aanroepargument en verwijderingsgevolgen blijven open. Alle adressen en bewijsbestanden staan in het voedselrapport. Laatste verse budgetmelding 13:58:37: week86%, vijfuur12% resterend; analist heeft afronding als eerstvolgende taak. Volgend rootwerk: overdracht onderzoek/regering controleren en ontbrekende flag-/contextbindingen volgen binnen de beschikbare limiet.

Onderzoek/regering is om 14:01 door de analist opgeleverd, om 14:02 door de coördinator gelezen: 14/14 originele DLL-controles, 34 lokale rapportlinks. Selectie, fallback, aanvraag, herkeuze/save, regeringsbeschikbaarheid/rang/gelijkstand en beide wisseltakken zijn uitgewerkt. Communism/Fascism delen een outputbuffer. Open essentiële branches staan expliciet in het rapport; pakket is geen afronding van fase A. De analist is na overdracht klaar en krijgt vóór budgetreset geen nieuw breed pakket. Het voedselrapport bevat inmiddels 34 bestaande lokale links. Volgende fase-A-opdrachten: regeringfiltervelden en wisselcontext binden; food/settler-flagcontext vervolgen; vervolgens terrein/improvements en goods-tellingen. Laatste verse budgetmelding 14:02: week86%, vijfuur8% resterend. Bij vijfuur≤5% uitsluitend hervatstatus vastleggen en wachten op bevestigde reset (gemeld tijdstip 17:55:33 Europe/Amsterdam).
