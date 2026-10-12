# B2c researchtekst voorbereid

11 oktober 2026, 16:02 Europe/Amsterdam. Status **PREPARED_ONLY_NOT_INSTALLED**. Deze opdracht is afgerond en stopt voor rootreview. Geen native parser, actions, researchselectie of gameplay uitgevoerd.

Bevroren voorstel: ONTWERP/GEZAMENLIJKE-OPENING-B2.md, SHA256 ea5140b5505c11f457bdcdc3cf41fcc023e277bf247866228ad356919c9ef40e. Directe basis: de voorbereide B2b-kandidaat PROEVEN/opening-b2/regering-b2b/20261010T180801159; manifesthash e1bacd6b0fbed849563fb167b2aae6f9b2cdf01878ddc03a3756698f97e2c5a1 bevestigd. Deze basis is niet geïnstalleerd; ook deze nieuwe map verandert de werkversie niet.

candidate/ bevat een gecombineerde tekstkandidaat van negentien bestanden:

- Acht nieuwe research-only AIPs: opening_research uit B1-default, plus zeven route-eigen opening_restore-bestanden voor default, cleric, slaver, scifew, scimany, milfew en milmany.
- Eén nieuwe load_opening_research.fli met uitsluitend de beschreven load bij opening_required > 0.5.
- Zeven gewijzigde B2b-beginturns: zes normale routes met restore bij opening_required < 0.5 vóór hun gewone aiploader en openinginclude erna; Default met restore/openingloader direct na de bestaande B2b-openinginclude.
- Drie bytegelijke B2b-bestanden meegeleverd voor een complete laag: inputs.fli en beide set_govern-includes. Die zijn niet opnieuw ontworpen of gewijzigd.

Dit zijn zestien B2c-wijzigingen/nieuwe bestanden plus drie ongewijzigde B2b-bestanden. Geen N gekozen, geen oorspronkelijke B1-AIP herschreven, geen unit-, bouw-, wonder-, scalar- of andere AIP-categorie toegevoegd. Elke nieuwe AIP is precies één volledige Advancements_List-declaratie, #DATA, interne comments, alle98 records en #END_DATA: 2866 bytes. Alle oorspronkelijke categorybytes, CRLF en route-eigen restvolgorde behouden. Geen puntjes of verkorte lijsten. category-blocks.json geeft voor de acht B1-baselines (inclusief de ongewijzigde citywall_science-referentie) bronhash, byteoffset/-lengte, categoryhash en de volledige geordende98 records. static-checks.json bewijst de acht echte kandidaatbestanden bytegelijk aan hun oorspronkelijke bronranges; alle19 kandidaatdiskhashes matchen manifest.json.

Statische include-expansie vanaf alle acht personalityroutes en beginbeurt-actionvolgorde vastgelegd in routing.json. Iedere zes normale routes heeft39 loads: één restore, alle37 bestaande gewone loads in exact dezelfde volgorde en één openingload. De bestaande late citywall_science-action blijft vóór de nieuwe openingload. Default heeft precies twee nieuwe researchloads; het oude template/aiploadercommentaar blijft bytegelijk uitgeschakeld. Barbaren behouden hun oude set_govern en enige barbarian.aip-load, zonder bereikbare nieuwe regering-/researchinclude. Gedeelde B2b-inputdeclaraties zijn daar inert. De zeven beginturns keren bij uitsluitend verwijderen van de beschreven ingevoegde bytes exact terug naar hun directe B2b-basis. candidate.diff is hierop gelezen.

Dit bewijst tekstuele plaatsing en categoriebezit; het bewijst nog niet dat de echte parser de partials accepteert, de actions werkelijk vuurt of de selector andere research kiest. Bij een echte manageropbouw moeten alle nieuwe AIPs vooraf op disk staan; bestaande managers lezen een onbekende loadnaam niet alsnog in. Tijdens opening is de bedoelde laatste schrijver B1-default, na opening routeherstel met gewone latere writers intact. Deze effecten zijn ontwerpverwachtingen, geen uitgevoerde actionpass. Het gemeenschappelijke defaultsuffix kan transport/defensie vertragen; geen gunstig gameplayeffect aangenomen.

Bronbescherming: het bestaande protected-before.json hergebruikt, geen nieuwe inventarisframework. Vóór voorbereiding matchten116 huidige aidata-bestanden en huidige engine/originele AI-DLL hun bestaande pins. Alle118 bronnen na voorbereiding bytehashgelijk; ook alle tien B2b-kandidaatbronnen bleven gelijk (source-after.json:128 checks). backup/ bevat18 geverifieerde directe bytebackups: tien B2b-bestanden en acht volledige B1-AIPs. backup-manifest.json vermeldt bron/hash/omvang. Er zijn alleen bestanden in deze eigen pakketmap en het toegewezen voortgangsbestand geschreven; CTP-og en andere gebruikers-/agentbestanden zijn niet veranderd.

Mogelijk later B2c-herstel: zet uitsluitend de zeven beginturns terug uit deze directe B2b-backup en verwijder de negen eigen nieuwe researchbestanden na manifest-/ownershipcontrole. Laat de drie ongewijzigde B2b-bestanden en B1-baselines behouden. Dit is een beschreven herstelroute; geen installatie of herstel uitgevoerd. Bewaar variant-saves volgens het bestaande B2-ontwerp, geef een B2a-inline-recordsave niet aan een originele DLL.

Reviewpins:

- manifest.json: 017c57960864d7675f4b7ae500007f0b24e104e19ca917a272d9ed54c5af183a
- candidate.diff: afb8a45d60f64485f40407ea4641dd382ff20f5621505fd1cbafe533b79da78d
- routing.json: 476b112c19cfd4db169e20bdba665680464c55a514ec6edcc352afdbd992eb37
- category-blocks.json: 61a757510d1d738f02c3e443373a98966d6020c304f1cf4bc02c1da3c068d07a

Laatste verse budget16:01:25: bron16:00:47/leeftijd37.9s, week98%, vijfuur86%, stateok. Geen budgetstop en geen pc-afsluitactie. Volgende oplevering ligt bij root: deze manifest/categorydiff/routering beoordelen, daarna afzonderlijk de noodzakelijke parser/native-/hostpoorten vrijgeven. Deze opdracht geeft daarvoor geen uitvoeringstoestemming en claimt geen totale projectvoltooiing.
