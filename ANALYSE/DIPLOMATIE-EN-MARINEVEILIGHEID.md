# Diplomatie, gedeeld land en marineveiligheid

Fase A, 7 oktober 2026. Afgebakende hervatting van bestaande analyse; geen spelstart, gameplaywijziging of binarypatch. Dit rapport hergebruikt [dreiging/stadsverdediging](DREIGING-EN-STADSVERDEDIGING.md), [ruimte/buren](RUIMTE-BUREN-TRANSPORT.md), [transportuitvoering](TRANSPORT-EN-VESTIGINGSACTIES.md), [bouwconcurrentie](BOUWDOELEN-EN-QUEUE.md) en [AAIP-lessen](AAIP-LESSEN.md).

De huidige AI heeft afzonderlijke diplomatieke houding, militaire houding, formele relaties, terreintoegang en beschikbare transportmiddelen. Deze voorwaarden lopen niet gelijk. Gedeeld land is al een diplomatie-input; een actieve afspraak om land te verlaten kan transportpaden duurder maken. Dat bewijst geen algemene veilige settlerroute of automatische defensieve openingsstrategie. De marine gebruikt bestaande legerdoelen, transport en bombardementaanvragen; schipquota alleen bepalen het resultaat niet.

## Bewijs en lokale dekking

Robotcom.dll SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, imagebase20000000, timestamp37b894e7; robotcom.map past. Civctp.exe SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, imagebase400000, timestamp37d6f702; de afwijkende civctp.map is niet gebruikt. AI-functies zijn via passende symbolen en daadwerkelijke instructies gebonden; enginefuncties via bytes en de al bewezen Player-vtable744660.

| Keten | Spelgegevens en selectie | Prioriteit/actie | Save en bewijsstatus | Resterende grens |
|---|---|---|---|---|
| Regard en oorlog | Foreigner+60/+68, gedeelde bonus+70; formele relatie afzonderlijk | Fuzzy-regardupdate → hot/coldpredicates → dreigings-/aanvalfilters | Velden expliciet in Foreigner-serialisatie; machinecode en lokale controles | Volledige diplomatiepass met alle berichten/bonussen niet gespeeld |
| Gedeeld continent | ComputeLandContinentShared → Foreigner+d0 → he_shares_continent | Bestaande FLI-regels beïnvloeden regard, naast kracht/afstand/persoonlijkheid | Input/callbinding en tekstfeit; geen universele openingsomschakeling bewezen | Defensieve reactie en uitbreiding blijven concurrerende plannerbeslissingen |
| Leave-lands-afspraak | Actieve agreementtype5 → +204 en AiMain+13c; tile-eigenaar en unitregard | Transportpad kan extra kosten krijgen; geen generieke dreigingsscore | +204 wordt opgeslagen/geladen; acht lokale suffixcontroles | Volledig pad/ontmoetingspunt, refreshvolgorde en werkelijke route blijven open |
| Gewone aanval | Hot/coldfilter voor enumeratie, hot voor normale GoalAttack-aanmaak | Doelprioriteit en legerbod → rally/generieke uitvoering → transport indien nodig | Vtable/callbinding; bestaande transportcontroles hergebruikt | Alle invasie-/stadsaanvaldoelen en concrete scheduleruitkomst niet gereconstrueerd |
| Bombardement | Unit/doelcompatibiliteit, cargo, pad/range, echte targetquery | ArrivedAtTask → ActionTryToBombard → Player+19c/+198 | Drie oorspronkelijke AI-requestcontroles met externe mocks | Geen gehele engineorder, schade, doelvernietiging of vlootoperatie geëmuleerd |

Dit is een lokale dekkingsmatrix voor de toegewezen ketens, geen percentage van de volledige gameanalyse.

## 1. Regard betekent twee verschillende houdingen

SetupForeignerVars2002d560 schrijft bij2002eaa9–2002eabb:

```text
diplomatic_regard_towards_him = Foreigner+60 + Foreigner+70
unit_regard_towards_him       = Foreigner+68 + Foreigner+70
```

De eerste houding beïnvloedt onderhandeling; de tweede houding wordt ook door de reeds bewezen hot/coldhelpers gebruikt. IsAtHotWar toetst de som+68/+70≤20, IsAtColdWar≤40. Een lage diplomatieke regard alleen verklaart daarom niet iedere militaire keuze. De API SetFZRegard2000cc60 schrijft zijn drie integerargumenten naar+60,+68,+70 en kopieert het derde tevens naar+78. UpdateMiscInfo kan bij de onderzochte alliancebranch+78 weer naar+70 kopiëren. De complete herkomst/levensduur van alle bonusbijdragen blijft open. [Inputs en writes](BINAIR/diplomacy-naval-diplomat-pass-inputs.txt), [API](BINAIR/diplomacy-naval-regard-and-goals.txt), [misc/alliance](BINAIR/diplomacy-naval-misc-ceasefire.txt), [bestaande predicates](DREIGING-EN-STADSVERDEDIGING.md).

Na FireRules20038ff0 telt de diplomatie-update bij2002f85e de huidige basis+60 bij de diplomatie-delta en afzonderlijke strength/general/message/pillage/incursion/attack/piracyoutputs op. Waarden boven100 worden100; een negatief resultaat wordt5. SetDiplomaticRegard2000d7e0 bewaart de double in+60 en verstuurt de afgekapt-integerwaarde via Player+284. De echte wrapper52b9c0 vertaalt deze naar categorieën en vraagt verdere engine-opslag4cf9c0 aan. Dit is geen wijziging van de hot/coldpredicate zelf. [Updateformule](BINAIR/diplomacy-naval-diplomat-pass-inputs.txt), [setter](BINAIR/diplomacy-naval-regard-and-goals.txt), [enginewrapper](BINAIR/diplomacy-naval-engine-treaty-wrappers.txt).

`unit_regard_delta` is ondanks de naam in deze route **geen getal dat steeds bij de oude militaire regard wordt opgeteld**. Fragment2002f94b–2002f9c4 gebruikt de output als nieuwe absolute waarde wanneer deze strikt boven5 ligt. Bij≤5 behoudt het de bestaande unit_regard_towards_him-input. Vervolgens wordt boven100 geklemd; een negatieve gekozen waarde wordt11. Het resultaat wordt naar+68 geschreven en de output wordt0. Dat sluit aan bij de oorspronkelijke FLI-outputsets go_to_hot_war10, go_to_cold_war35 en go_to_peace_full80. Bij bijvoorbeeld bestaande80 en output35 wordt35 opgeslagen; bij output5 blijft80 bestaan. Het hergebruik van een input inclusief+70 is zichtbaar, maar de gehele bonus-/passvolgorde is niet geëmuleerd. [Originele update](BINAIR/diplomacy-naval-diplomat-pass-inputs.txt), [FLI-declaraties/regardregels](../CTP-og/ctp_data/default/aidata/diplomacy_begin.fli).

De individuele diplomatie gebeurt aantoonbaar in FSDiplomat::Execute2002d110 via SetupForeignerVars, met parameters die onder meer section8 en conditioneel6 kiezen. FSFuzzyDiplomacy::Execute20037660 zelf is in deze binary slechts een return1-stub; zijn naam bewijst geen afzonderlijk werkende regardpass. De volledige sectie-/parserwerking behoort tot de aparte fuzzyanalyse van de coördinator. [Werkelijke diplomaatpass](BINAIR/diplomacy-naval-diplomat-pass-inputs.txt), [stub](BINAIR/diplomacy-naval-individual-pass.txt).

## 2. Formele relaties en gebeurtenissen

UpdateAlliance2000cd70 gebruikt Player+264→52b6b0: de wrapper levert1.0 bij relatieveld3, anders0. UpdateWar2000cd90 gebruikt Player+268→52b6e0: relationele waarde0 betekent1.0, anders0. Dit zijn daadwerkelijke engine-relatiequeries, anders dan hot/coldregard. UpdateCeaseFire2000cd40 vraagt agreementtype7 via Player+1c4 op. [AI-queries](BINAIR/diplomacy-naval-treaty-fuzzy-and-bid.txt), [slots](BINAIR/diplomacy-naval-player-slots.json), [enginequeries](BINAIR/diplomacy-naval-engine-treaty-wrappers.txt).

Concrete events kunnen fuzzy-gewenste waarden direct overrulen:

- HotwarAttackedMe2000c750 telt het aangeleverde bedrag bij de aanvalsteller op, bewaart het rondetijdstip, verlaagt bases+60/+68 bij≥20 naar19 en zet+70,+78,+204 op0.
- HeBrokeCeaseFire2000cc90 trekt10 van loyalty+118 af, verlaagt diplomatieke base bij≥20 naar15, militaire base bij **>20** naar15 en zet+70/+204 op0. De cache+78 blijft in deze functie staan.
- HeBrokeAlliance2000ccf0 trekt eveneens10 van loyalty af en zet bases bij≥20 op19 en+204 op0. Het wist+70/+78 hier niet. Een positieve bonus kan daarom ondanks deze basisverlaging de hot/coldsom beïnvloeden.
- RegisterBrokeTreaty20034c30 verhoogt de gebroken-verdragenteller+1d8 met1 voor een aanwezige andere Foreigner. Het slaat de eigen speler en ontbrekende Foreigner over; de tweede eventparameter wordt in deze functie niet gebruikt.

Deze branches zijn lokaal gecontroleerd, inclusief exact20. Ze bewijzen geen complete treaty-/oorlogeventvolgorde. [Events](BINAIR/diplomacy-naval-regard-update-attack.txt), [verdragsreacties](BINAIR/diplomacy-naval-treaty-fuzzy-and-bid.txt), [controles](BINAIR/diplomacy-naval-controls.json).

## 3. Gedeeld land is al zichtbaar voor diplomatie

UpdateDiplomaticState2000ce70 vraagt ComputeLandContinentShared2000d330 op en bewaart het resultaat in+d0. SetupForeignerVars2002ed81 schrijft juist dat veld naar he_shares_continent. De eerdere overlapanalyse wordt hergebruikt; dit is niet de hoeveelheid resterende geschikte vestigingsplaatsen. [Staatupdate](BINAIR/diplomacy-naval-state-and-path.txt), [inputbinding](BINAIR/diplomacy-naval-diplomat-pass-inputs.txt), [overlapmaat](RUIMTE-BUREN-TRANSPORT.md).

De originele diplomacy_begin.fli heeft al regels voor een dichtstbijzijnde hoofdstad op hetzelfde continent: warlike en zero_at_war geven much_hate_strength; peaceful en aanvullende relatievoorwaarden geven little_like_strength. Formele oorlog, ceasefire en alliance hebben daarnaast hun eigen regels. Dit verklaart een bestaande indirecte burenreactie via regard. Het is geen aangetoonde algemene beslissing om bij iedere AI-buur de snelle uitbreiding te verlaten, voldoende verdedigers te bouwen of settlers te escorteren. De eerdere strategische dreiging/defensiedoelen blijven de afzonderlijke aansluitingen. [Originele diplomatieregels](../CTP-og/ctp_data/default/aidata/diplomacy_begin.fli), [defensie](DREIGING-EN-STADSVERDEDIGING.md).

## 4. Het diplomatieveld in het transportpad is een afspraak

De eerder onbekende Foreigner+204 is in UpdateMiscInfo2000bb50–2000bb72 de booleanuitkomst van Player+1c4 met agreementtype5. Een positieve uitkomst zet AiMain+13c op1. SetupForeignerVars2002f69e–2002f6bc koppelt type5 via HeAgreed aan `have_leave_our_lands`; hiermee is de enumsemantiek aan echte CTP I-code gebonden. [Veldrefs](BINAIR/diplomacy-naval-foreigner-204-refs.txt), [schrijver](BINAIR/diplomacy-naval-misc-ceasefire.txt), [FLI-binding](BINAIR/diplomacy-naval-diplomat-pass-inputs.txt).

Player+1c4→52a2c0 dereferentieert de aangeleverde Foreigner-pointer om de speler-ID te krijgen, leest het agreementtype via zijn pointer en zoekt in4bc720 de agreement met passende soort en betrokken speler. Daarna controleert het actief/ongeldig-status. De objectpointer in de AI-call is dus hier passend bij de echte interface; behandel haar niet als foutief speler-ID. De precieze richtings-/acceptatie-/vervaleventcyclus van leave-landsafspraken is niet gereconstrueerd. [Echte wrapper](BINAIR/diplomacy-naval-engine-treaty-wrappers.txt), [agreementlookup](BINAIR/diplomacy-naval-engine-bombard-and-agreement.txt).

TransportPathCallback20017650 voegt in suffix200178a1–200178fc een extra floatpadkost toe wanneer AiMain+13c actief is, World+54 een eigenaar1..31 geeft, daarvoor een Foreigner bestaat, +204 actief is en de **basis** unitregard+68≥20. De extra kost is de cached globale float2009bf20; eerdere callbackinitialisatie berekent tweemaal ComputeMaxMoveCost. Bij regard19.99 ontbreekt die kost, bij20 bestaat ze. De predicate telt hier+70 niet op. De route wordt hierdoor duurder; zij wordt in deze suffix niet categorisch verboden. [Callback](BINAIR/diplomacy-naval-state-and-path.txt), [grenscontroles](BINAIR/diplomacy-naval-controls.json).

Dit veld is daarmee geen militaire kaartdreiging. World+90/+94 zijn eerder aan mapbits gebonden. Die predicates en de assault/capturebranches mogen niet als algemene bescherming van settlers of automatische marinescorte worden beschreven. Volledige A*, kust-/ontmoetingspuntkeuze, refresh van+13c en uitgevoerde orders blijven grenzen van dit pakket. [Bestaande veiligheid/bereikbaarheid](TRANSPORT-EN-VESTIGINGSACTIES.md).

## 5. Gewone aanval gebruikt generieke transportuitvoering

Insert_Attack_Goals2002c4e0 enumereert buitenlandse legers wanneer hot of cold geldt en roept SetupSpecialGoals aan. Een normale nieuwe GoalAttack wordt in2002c591–2002c5f8 alleen gemaakt wanneer ForeignAgent+74 nog geen doel bevat en hot opnieuw true is. Add_Goal registreert het doel; +74 bewaart de pointer. Dit is de gewone legeraanvalroute, geen bewijs dat alle speciale acties of stadsaanvallen dezelfde voorwaarden hebben. [Aanmaakvoorwaarden](BINAIR/diplomacy-naval-regard-and-goals.txt).

ActionBidToAttack200143d0 wijst onder meer de gevolgde armyflag4, een citytarget in de betreffende branch en een leger zonder aanval/cargo af; verdere takken toetsen bereik/continent en combineren afstand, wachttijd en combatbonus. Compute_Raw_Priority20045e30 gebruikt het effectieve Planner-profiel plus de generieke ArmyGoal-score. Deze score concurreert via de bestaande planner met verdediging, vestiging en andere doelen. De volledige bodformule/scheduler-gelijkstanden zijn niet opnieuw geëmuleerd. [Bod en prioriteit](BINAIR/diplomacy-naval-turn-and-request.txt), [bouwconcurrentie](BOUWDOELEN-EN-QUEUE.md).

GoalAttack::Execute_Task20045c30 kan squads laten verzamelen via Ok_To_Rally/Rally_Troops en bereikt daarna ArmyGoal::Execute_Task200443c0. De GoalAttack-vtable bindt slot80/8c/9c aan de generieke GotoTaskSolution/FollowPathToTask/TryTransport. FindPath20017ef0 en FindPathToBoard20019600 geven TransportPathCallback door aan het bestaande pathinterface. Aanvaldoelen kunnen dus dezelfde concrete carrier-/boarding-/debarkingketen gebruiken als vestiging. Dit bewijst bestaande mogelijkheden, geen geslaagde invasie, geschikte vlootsamenstelling of tactisch optimale aanval. [Uitvoering](BINAIR/diplomacy-naval-turn-and-request.txt), [vtable](BINAIR/diplomacy-naval-attack-vtable.txt), [padcallbinding](BINAIR/diplomacy-naval-request-route.txt), [eerder gecontroleerde carrier-/actievoorwaarden](TRANSPORT-EN-VESTIGINGSACTIES.md).

## 6. Bombardement heeft een concrete query en actie

GoalBombard::PretestBid2004aff0 gebruikt de generieke legerpretest, doelgroep-/unitcompatibiliteitsqueries en sluit in de laatste branch geladen cargo uit. WithinRange2004af10 toetst agenttype, resterende padpunten, subtask en CanBombardTarget; transportsubtasks hebben afzonderlijke branches. De volledige UnitDB-capabilitybenamingen en alle doel-aanmaakvoorwaarden zijn hier niet nieuw gebonden. [Doelfilters](BINAIR/diplomacy-naval-bombard-requests.txt).

Bij gewone aankomst roept ArrivedAtTask2004af80 ActionTryToBombard200165b0 herhaald aan zolang het true terugkrijgt. De actie vraagt het doelvakje via goal-slot5c op, toetst Player+19c en vraagt pas bij true Player+198 aan met dezelfde armyID en doelpositie. False beëindigt de herhalingsbranch; daarna bestaan back-away/state-/doelafhandelingstakken. De lokale helper bevestigt dat een false query geen actie uitgeeft en dat een uitgegeven actie zijn daadwerkelijke Player-antwoord teruggeeft. [AI-code](BINAIR/diplomacy-naval-bombard-requests.txt), [drie requestcontroles](BINAIR/diplomacy-naval-controls.json).

De echte Player+19c is529a60→4795f0→484ac0: targetquery via aanwezige targetinformatie en unitchecks. Player+198 is529950: armylookup, doelconversie, type0x16-aanvraag via479770→485730→485940 en verdere uitkomstqueries via479a50→487310. Hiermee zijn query en actie tot concrete engine-aanvragen verbonden. De volledige orderuitvoering, tijd-/schaderegels en unitverlies zijn niet geëmuleerd. [Slots](BINAIR/diplomacy-naval-player-slots.json), [geldige wrapper/functionstarts](BINAIR/diplomacy-naval-bombard-engine-binding-v2.txt), [targetquery](BINAIR/diplomacy-naval-bombard-target-check.txt), [orderaansluiting](BINAIR/diplomacy-naval-bombard-order-tail.txt).

Het eerdere bewijsbestand engine-bombard-and-agreement bevat een range die bij5299e0 midden in een instructie begint; die prefix is geen bewijs. De interpretatie hierboven gebruikt het nieuwe volledige529950-begin en het geldige529a60-begin. Geen conclusie is afgeleid uit die onjuist begonnen prefix.

## 7. Savegedrag en AAIP-lessen

Foreigner::Serialize20009d80 schrijft+60/+68/+70/+78 via PutDOUBLE en leest ze in de andere serialisatietak terug. +204 wordt bij2000a41b–2000a42d expliciet als vier bytes geschreven en bij2000aed3–2000aee1 hersteld. Diplomatieke toestand begint na laden dus niet aantoonbaar steeds opnieuw neutraal. Hoe live engine-agreements, caches, schedulerdoelen en orderlijsten in een volledige save samen worden hersteld, is niet met een echte saveherlading gecontroleerd. De bestaande AIP-saveanalyse wordt hergebruikt; nieuwe profieltekst is niet automatisch een reset van opgeslagen diplomatie/plannertoestand. [Serialisatie](BINAIR/diplomacy-naval-regard-update-attack.txt), [profielpersistentie](AIP-LAADWERKING.md).

AAIP verandert de primaire naval Triremesquota van−2 naar0.4 en klassegewicht6000 naar6500; de gewone Triremeslijst gaat0.75 naar0.4. Dit verandert bouwvraag en concurrentie via de bewezen quota, geen engine-carriercapaciteit of nieuwe tactische scheduler. [OG naval](../CTP-og/ctp_data/default/aidata/AIPs/naval.aip), [AAIP naval](../CTP-AAIP/ctp_data/default/aidata/AIPs/naval.aip), [quota/transport](RUIMTE-BUREN-TRANSPORT.md).

In diplomacy_begin.fli verlaagt AAIP onder meer de military-incursions-centra3→2 en4→3 en de eigen incursions-drempels2→1 en6→2; het wijzigt ook loyalty-/regardregels. Dat kan de sterkte en timing van diplomatieke/borderreacties beïnvloeden via de hier gebonden inputs. Het bewijst geen beter grensbeleid of veiligere marineoperatie. README-claims blijven modmakersclaims; de complete mod bevat bovendien andere regels/rekentijden. [Bestaande concrete diffs](INVENTARIS/aaip-ai-diff.md), [AAIP-vergelijking en grenzen](AAIP-LESSEN.md).

## 8. Controle en impact op A→B

**27/27 controles** slagen op de oorspronkelijke DLL-instructies: één API-fieldcheck, zes event-/exact20checks, drie treaty-counterbranches, zes unitregard-updatecases, acht transportpadkostbranches en drie bombardrequestcases. Eventrondetijd gebruikt uitsluitend een in-memory ftol-CRT-substituut met behoud van caller-controlword; andere fixtures gebruiken synthetische objecten. De unitregard- en padkostchecks beginnen op expliciet aangegeven geldige fragmentgrenzen met register-/frametoestand. World-eigenaar, goalpositie en Player-bombardementantwoorden zijn benoemde externe mocks. Er is geen hele diplomatiepass, padzoeker, combat of spelbeurt uitgevoerd. [Helper](../PROEVEN/Controleer-Diplomatie-Marine.py), [gevallen/mocks/resultaat](BINAIR/diplomacy-naval-controls.json).

Voor de analyseoverdracht is nu onderbouwd welke bestaande signalen gedeeld land en formele afspraken vertegenwoordigen, hoe militaire houding doelvorming beïnvloedt en waar transport/bombardement concrete engine-aanvragen bereiken. Overblijvende gaten betreffen de volledige bonus-/bericht-/agreementeventcyclus, complete observation/cache-refresh, alle invasie-/stadsaanval-/bombarddoel-aanmaakvoorwaarden, capaciteitboekhouding/scheduler, echte orders en combat, escorte en volledige saveherstelcontext. Zij beperken claims over tactiek en feitelijke marineveiligheid; zij blokkeren niet het afzonderlijk beoordelen van bestaande profielquota, defensievraag, bereikbaarheid en requests.

Er is geen nieuwe uitvoerbare escort-hook of uniform burenbeleid aangetoond. Een later voorstel dat zo'n mogelijkheid nodig heeft, moet de benodigde schakel eerst gericht onderbouwen. Een latere marineverbetering vereist naast bouwaantallen een vaste scenariovergelijking van daadwerkelijk vervoer, landing/aanval, verlies en opbrengst. Dit rapport levert huidige werking en grenzen aan de ontwerper; het past geen verbetering toe en verklaart de volledige projectdoelen niet bereikt.
