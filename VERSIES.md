# Versies en installatie van de CTP I-proef

Momentopname: 9 oktober 2026, 15:40 Europe/Amsterdam. Deze registratie onderscheidt voorbereide bestanden, de werkelijk aanwezige proefconfiguratie en gemeten gameplay. PROJECTSTATUS.md bepaalt het actieve werk; geen van onderstaande technische resultaten bewijst het volledige projectdoel.

| Versie / pakket | Wijziging | Status | Bewijs / herstel |
| --- | --- | --- | --- |
| Originele referentie | CTP-og | Referentie; blijft ongewijzigd | Beschermde inventaris in de uitvoeringspakketten |
| B1 | Religion en Theocracy vooraan in acht onderzoekslijsten; overige volgorde behouden | Aanwezig in CTP-proef, offline gecontroleerd; effectieve runtimekeuze nog niet aangetoond | [Manifest](PROEVEN/research-b1/manifest.json), [verslag](PROEVEN/research-b1/UITVOERVERSLAG.md), backups in hetzelfde pakket |
| H1-I | Identiteitsadapter op de drie locatiescorecalls | Afzonderlijke kandidaat, technisch gecontroleerd; niet geïnstalleerd | [Pakketmanifest](PROEVEN/score-h1/package-manifest.json), [verslag](PROEVEN/score-h1/RESULTATEN.md) |
| H1-M | Technische bergcentrumprobe: maximaal één punt minder | Afzonderlijke kandidaat, technisch gecontroleerd; niet geïnstalleerd | Zelfde H1-pakket; hypothese, geen volledige berglocatiestrategie |
| H3 | Drie open bergwerkplekken plus andere huidige voedselplek en expliciet voedselscenario; afzonderlijke ontwikkelberekening | Kandidaat technisch gecontroleerd, 82 native cases; niet geïnstalleerd. Echte engineacceptatie, overhead en gameplay nog ongemeten | [Ontwerp](ONTWERP/PRODUCTIELOCATIES-H3.md), [verslag](PROEVEN/production-h3/RESULTATEN.md), [pakketmanifest](PROEVEN/production-h3/package-manifest.json) |
| B2a | Eenmalige openingsvoltooiing, eigen inputs en save/load/reload | N25/N30 technisch geaccepteerd, elk 88 native cases; niet geinstalleerd. Echte host/T0/FLI-activatie open | [Voorstel](ONTWERP/GEZAMENLIJKE-OPENING-B2.md), [resultaten](PROEVEN/opening-b2/RESULTATEN.md), [pakketmanifest](PROEVEN/opening-b2/package-manifest.json); N niet gekozen |
| B2b/c | Gedeelde regeringsvoorkeur en onderzoekscategorie met expliciet herstel | Ontwerp gereed; niet toegepast. Volgt na technische B2a-acceptatie | Zelfde voorstel; N25/30 nog onbeslist |
| B4 | Dynamische settlervraag; eerste directe productievariant met H3/B2 | Vier PREPARED-emissies N25/N30 baseline+B4 gebouwd; geen technische/native acceptatie, installatie of gameplaybewijs. Volledige science/monopoly/transportpolicy open | [Producerontwerp](ONTWERP/PRODUCER-SETTLERVRAAG-B4.md), [builder](PROEVEN/settler-b4/build.py); huidig bouwcheckpoint hieronder |
| H3-observer | Exacte original/H1-I/H3-loadedbytes en nieuwe geregistreerde doelen/Q-B, normale AI zonder civ0/mens | Offline technisch geaccepteerd, 52 controles; nog geen liveuitlezing/activatiebewijs | [Resultaten](PROEVEN/ai-uitlezen/activatie-h3-resultaten.md), [pakket](PROEVEN/ai-uitlezen/activatie-h3-package.json) SHA8786005d046b0a99fc6907af6b99b1e134ecb90668e021494beac8e5b1ad7564 |

Het [beperkte directlandproducerontwerp](ONTWERP/PRODUCER-SETTLERVRAAG-B4.md) is afgerond: H3-current productieplannen, veilige routequeries en unieke claims. Producerbron en PREPARED-emissies zijn geschreven; native/combinatieacceptatie nog open. Science/monopoly/transport en volledige gameplaypolicy blijven open. Observerreader SHA `ff43655e52ddc2a9c593ff64ef564c6cda54a2c11e04cc364cfbd5fface69365`, zes definitieve pakketartefacten door root gehasht zonder afwijking. Nieuwe echte goals/causale scorecall/heapordening/overhead blijven onderscheiden runtimepoorten.

## B4-bouwcheckpoint 9 oktober, 15:39

Vier PREPARED-bestanden en payloads door root aan hun individuele manifesthash getoetst: gelijk. Geen technische vrijgave. N25/N30 blijven fixtures, geen gekozen productiebeleid. H3-RVA d4000/bytes behouden; B2 opnieuw geemitteerd op d7000, B4 op d9000 en eigen vluchtige RW-state op dc000. Controlebestanden bevatten alleen H3/B2. Onderstaande hashes beschrijven deze eerste emissie; bij verdere broncorrecties opnieuw bouwen en vastleggen.

| PREPARED-artefact | SHA256 op dit checkpoint |
| --- | --- |
| [B4-N25](PROEVEN/settler-b4/B4-N25.manifest.json) | 3bab9d23486ce79e9c12170415a039847be77093e145893d4b4e42d883484b98 |
| [B4-N30](PROEVEN/settler-b4/B4-N30.manifest.json) | 5812b6d882e7f26f806f02f2818a2f275a2b354459626c3b7ad8cc90446a6a79 |
| [Controle-N25](PROEVEN/settler-b4/BASELINE-N25.manifest.json) | 3b1a0ce1023ee041ea08c3ba6132e353e720a1d851ce841027ed8482b12f8519 |
| [Controle-N30](PROEVEN/settler-b4/BASELINE-N30.manifest.json) | be2368421c9e4ee709e674b3e22eb5d5f548b41f67623d7ce53b927b44b867d3 |

Frozen producerontwerp6e310ea5c15f7b3cc42ad75f586bab6bdf14bdee6e63a6639ac7c5f9b2717501. Aanvulling15:43: [statische checks](PROEVEN/settler-b4/prepared-checks.json) vierpass/2010 B4-instructies; [eigen helperprocessen](PROEVEN/settler-b4/native-predicate-processes.json) exit0 en elk32 owner/conflict/ordercases met ABI/x87. Root las resultaten/fixturecode: uitsluitend deze predicates getoetst. Volledige producer/wrappers/path/type/DFS/currentpositie, gewone loader/rebase, beschermde inventaris en echte host/gameplay blijven open; PREPARED-status behouden. Er is niets geinstalleerd; herstel van deze bron-/bouwstap vraagt geen gameactie. C bij vijfuur5% interrupted, checkpoint in PROJECTSTATUS.

De coordinator controleerde alle 74 B2a-pakketartefacten: geen hashafwijkingen. Pakketmanifest SHA `297a51a8bf4e6d0da0dd379beab7b28b310d88bfa63eef4dac20e17482416634`; kandidaat N25 `9553d440365b029d47cd5b6c0717e6e96a6c2aeac3b1052bb80293736d35667a`, N30 `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890`. Fatale foutpaden zijn met expliciete eigen teststubs gecontroleerd; geen echte enginehandler of graceful herstel bewezen. B2b/c en gecombineerde H3-variant zijn niet toegepast.

## Werkelijk gecontroleerde proefbestanden

De coördinator heeft op 8 oktober opnieuw de acht actuele B1-AIPs aan hun `after_sha256` in het manifest getoetst: acht overeenkomsten, geen afwijkingen. Beide aanwezige H1-kandidaten matchen hun pakketmanifest. De huidige proef gebruikt nog de originele DLL, met de B1-onderzoekslijsten:

- Engine: `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`.
- Geïnstalleerde robotcom.dll: `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`.
- H1-I-kandidaat: `59ed9310f0e5aa9bba0902cc4436f1db6fba9ecab79cb8d5fe49683f869da2d0`.
- H1-M-kandidaat: `e13e00762d3de4662e1c24af8524ef06780ef3f5a612a1c5ca0306b3c23c152f`.
- Vast H3-ontwerp: `be16e3844ca7ae0396bd31ac28478855ff906c4091b529605e0bd91a41a71248`.
- H3-kandidaat: `f93be3629decd38a94117ba774aac3673db2cd2b9e1a0d8a1dde42f7b8e4fd9c`.
- H3-pakketmanifest: `f781d4f361af9e8054f4d3ba5176dd6f4c86b2f27cbf4e0b1c533147bad4a665`.

De huidige hele-installatiecontrole wordt door de uitvoerder bijgehouden; deze korte hashcontrole vervangt haar niet. Aanwezigheid op disk bewijst geen effectief geladen AIP, nieuw vestigingsdoel of betere spelbeslissing.

De coördinator heeft alle 80 H3-pakketartefacten aan hun manifest getoetst: geen afwijkingen. De teruggelezen testresultaten horen bij bovenstaande kandidaat; de proef-DLL is opnieuw als origineel bevestigd. De positieve hostheaderfixtures gebruiken een eigen validatorcopy met aangepast helperbasisadres. Acceptatie door de oorspronkelijke validator in de echte engine blijft een afzonderlijke runtimecontrole. Het pakket krijgt dus uitsluitend technische acceptatie binnen de beperkte C-opdracht.

## Vergelijkingsbasis en volgende installatie

De vaste QUOTA-START-T0 blijft SHA256 `8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26`, Deity/Gigantic/8 spelers. Gebruik dezelfde menselijke invoer en meet alle normale AI-beschavingen, zonder mens en barbaren. T25/T50/T100 en het bereiken van stad25/30 blijven de hoofdmeetmomenten.

H3 wordt afzonderlijk tegen H1-I vergeleken, met dezelfde acht B1-lijsten; H1-M, packing, quota en B2 worden niet tegelijk toegevoegd. B2 krijgt eerst eigen technische/gedragscontrole en daarna een aparte combinatieproef. De oude T60-quotasaves zijn historisch bewijs van quota-effecten, geen baseline met B1/H1/H3.

Een latere installatie vereist een eigen vastgelegde vorige DLL/configuratie, herstelkopie, gesloten proefproces, exacte kandidaat- en configuratiehashes en aantoonbare activatie na herstart/laden. Opgeslagen oude AIPs/doelen worden niet vanzelf vervangen door nieuwe bestanden. Herstel gebruikt de geregistreerde vorige proefversie en dezelfde startsave. Andere installaties, waaronder D:\CTP, blijven ongemoeid. De huidige C-opdracht staat uitsluitend kandidaatbouw toe; zij installeert niets.
