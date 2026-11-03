# Science: begrensde duurproef van de bestaande kandidaat

21 oktober 2026, 14:50 Europe/Amsterdam. Fase B, drie beslissingen afgerond; gereed voor rootreview en uitleg vóór C. Alleen voorstel: geen code, bouw, native uitvoering, RPM of spelbediening uitgevoerd.

Aanleiding is de geaccepteerde [SELECT25-uitkomst, A4/4](../ANALYSE/SCIENCE-SELECTIE-25-UITKOMST.md). Op de echte T1 is één science-NOW-plan met veilige directe route geselecteerd: huidig voedsel en marges35/30/25, Gcert1, Dorig=desired5. Gcert1 verhoogt de vraag niet omdat Dorig5 groter is. Het oude verschil met reason25 heeft geen bewezen oorzaak. Een nieuwe diagnose of reparatie is daarom geen voorwaarde voor deze meting.

Dit voorstel toetst voortgang naar Doel1/1a en het onderdeel science-NOW-herkenning/selectie van Doel5. Gewenst is dat de bestaande erkenning gedurende echte opeenvolgende beurten bruikbaar blijft, zonder slechtere uitbreiding of verlies van de bewezen Religion→actieveTheocracy-opening. Selectie alleen bewijst geen toewijzing, stichting, sciencebouwqueue of laborerinzet.

De bestaande FLI/AIP-route blijft geheel gelijk. De brede [beslisketens](../ANALYSE/BESLISKETENS-OVERZICHT.md), [dekkingsmatrix](../ANALYSE/DEKKING.md) en de gerichte A-overdracht onderbouwen de huidige DLL-selectie en combinatie met oorspronkelijke vraag. Alleen FLI/AIP-quota wijzigen zou de NOW-/routecertificatie niet meten en voegt een tweede factor toe. Geen SLIC, nieuwe hook, gewichten of beleid.

## Beslissing 1 — T0 tot en met T26; bestaande Doel3-variant als controle

**Voer één nieuwe kandidaatarm uit, maximaal26 natuurlijke n-beurten vanaf dezelfde vasteT0.** T25 is het afgesproken vroege uitbreidingsmeetpunt; T26 voegt slechts één beurt toe en maakt vergelijking mogelijk met het eerder werkelijk waargenomen moment waarop alle zeven AI's actieveTheocracy bereikten. T1 alleen is te kort voor uitbreiding; T50/60/100 zijn voor deze eerste begrensde meting niet nodig. De proef eindigt opT26 of eerder bij een stopvoorwaarde. Geen automatische verlenging wegens een ongunstig of onduidelijk resultaat.

De opgeslagen **variant** in `PROEVEN/doel3/20261012T122000/variant/T0.json` tot `T26.json` is een bruikbare historische controlearm voor steden, onderzoek en regering. Dit heet in dat oude pakket “variant”, maar is voor deze vergelijking de geteste Doel3-releasecontrole; gebruik niet de oorspronkelijke ongewijzigde-gamebaseline uit hetzelfde onderzoeksproject.

Alleen-lezen verificatie bij dit ontwerp:

- Alle19 `manifest.files[].variant_sha256` zijn exact gelijk aan de huidige releasebestanden én de overeenkomende beschermde bestanden in de hostbefore van21oktober. Dit omvat de acht AIPs, inputs, twee regering-FLI's, zeven beginturnroutes en DLL. Geen afwijking.
- Alle overige oorspronkelijke `manifest.protected`-paden buiten die19 zijn op schijf eveneens exact gelijk; de oorspronkelijke lijst telt118. Ook executable en profiel zijn daarmee gelijk. Dit is een vergelijking met bewaarde pins, geen nieuwe procesmeting.
- Alle27 opgeslagen snapshots zijn `stable_twice`, binden geladen DLL `eb6f58a7…74890`, hebben alle loadedchecks waar, dezelfde deelnemers2..8 en voor elkT native rondeT−1. Alle26 `Tn-pass.json` bewijzen één n en alle zeven ronden+1 binnen dezelfde opgeslagen instantie. Het verslag beschrijft passief menselijk spel zonder handmatige AI-acties.
- VasteT0 SHA256 `8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26`; deelnemers2..8, mens uitgesloten. Alle oude T0-meetvelden zijn gelijk aan de nieuwe21oktT0, met uitsluitend procesafhankelijke `ai_actor`/`effective_aip`-pointers buiten die vergelijking. De reader beweert zelf terecht geen atomische snapshot of rechtstreeks bewezen save-identiteit; savehash, laadprocedure/beelden en deze toestandsovereenkomst vormen samen de startbinding.

| Bewijsbron | SHA256 |
| --- | --- |
| Oud `manifest.json` | `3ee74baaa993793465975e9c996f03c699e334e24b297aa22fbbc5ba189806d4` |
| Oud `participants.json` | `a1cbed61f3f2a623b24f2357a4a81ab788c10ec04931f9f516e883e01af3d3dc` |
| Oud variant/T0.json | `989b0494d55d89f45515efc2ac94e9deaa5085f3f89f620dba5d5720a62b1997` |
| Oud variant/T26.json | `2bd396309011952ea37ab4743527bf4c1a91f3a1099881773b575da8fab209e6` |
| Oud ROOT-VARIANT-TRACE.json | `90c1f3da641b480f10266033e6d8b6717d2746da1762b58093bb3725c26d9ded` |
| Host21okt/host1/before.json | `f391391689c7b3210e185c1be26a38a537ecec64f382d01f8447d208d7bf1cec` |

Controleer in C deze bindingsvergelijking opnieuw tegen de nieuwe preflight; bestanden kunnen na dit voorstel veranderen. Bij een echte relevante afwijking: stop vóór installatie, vermeld concreet pad/hash. Geen stille afwijking accepteren of onmiddellijk een nieuwe controlearm starten; root beoordeelt eerst of herstel van dezelfde configuratie volstaat.

Historische steden per civ2..8:

| T | Steden2..8 | Totaal |
| --- | --- | --- |
| 1 | 0,0,0,0,1,1,0 | 2 |
| 5 | 1,1,2,1,1,1,2 | 9 |
| 10 | 2,2,2,2,2,2,2 | 14 |
| 15 | 2,2,2,2,2,2,2 | 14 |
| 20 | 3,3,3,2,2,2,3 | 18 |
| 25 en26 | 3,3,3,3,2,3,3 | 20 |

Bewaar iedere nieuweT0..T26, niet alleen deze tabelmomenten. Vergelijk per civ steden, Religion/Theocracy bekend, huidig onderzoeksdoel, gevraagde/actieve regering en deadline; rapporteer tevens totale steden en eerste overgangsmomenten. Bij de kandidaat meet men daarnaast bestaande settlers, huidige settlerqueuefronten, nativeDesired/Actual/deficit, en actuele laatste gedeelde pass: Gcert/Dorig/R/desired, context/reason, geclassificeerde locaties, NOW/selected evidence, query/punten/cutoff en bestaand diagnoserecord. Die gedeelde gegevens horen uitsluitend bij de expliciet gebonden laatste civ/generation, niet bij alle zeven.

De oude controle bevat **geen** settlervoorraad/queuefronten/vraag: daarvoor geen verzonnen nulwaarden of gepaarde verschillen. Nieuwe kandidaatwaarden zijn beschrijvend. Volledige queue en missievrijheid blijven UNKNOWN; `nativeActual` is geen synoniem voor alle aanwezige settlers. Zonder nieuwe interface geen stadscoördinaten/stichting op een geselecteerde plek claimen.

**Acceptatie vooraf:**

1. Meetproef geldig: exacte hashes/config/start, 27 stabiele snapshots, 26 eenmalige n-tokens en bij iedere stap alle zeven rondes+1; normale afsluiting/herstel. Bij voortijdige stop alleen het bereikte traject rapporteren, geen T26-resultaat.
2. Herkenning over tijd aangetoond: actuele, gebonden science-NOW-selectie met strikt positief huidig voedselbewijs opT1 én minstens één latere passT2..T26. Een later UNKNOWN/routefalen wordt als beperking gerapporteerd, nooit automatisch NOW. Dit rondt uitsluitend deze beperkte herkenningsmeting af.
3. Positief uitbreidingssignaal op deze start: T26-totaal **meer dan20 steden**, geen civ onder diens eigen historischeT26-aantal, én alle zeven Religion/Theocracy bekend en actieve regering3 opT26. De per-civT25/T26- en volledige stadstrajecten blijven zichtbaar. Dit is een conservatieve proefacceptatie, geen nieuw strategisch streefaantal.
4. Bij gelijke steden: geen uitbreidingswinst aangetoond. Bij minder steden of gemiste Theocracy: kandidaat niet als verbetering uitrollen; rapporteer concrete civ/beurt en bestaande counters. Een enkel historisch paar bewijst geen algemene causaliteit of reproduceerbaarheid; geen onbewezen nondeterminismeclaim. Bij positief signaal kan een gerichte herhaling later nodig zijn vóór algemene uitrol.

Doel1/1a of volledigeDoel5 worden niet AF door Gcert, deze kleine meetduur of alleen bovenstaande signalen. Dertig steden, nuttige stop/hervatvraag en dertig→veertig, ontwikkeling/bouwqueues/laborers en andere kaartcontexten blijven aparte acceptatievragen. Verwacht wordt zicht op behoud en eventuele remming/ondersteuning van uitbreiding; extra steden zijn geen voorspeld zeker effect omdat opT1 Gcert1<Dorig5 is.

## Beslissing 2 — kleine readeradapter in een nieuw eigen pakket

Kopieer/adapter uitsluitend de bestaande gepinde reader-/controlbron naar een nieuw eigen pakket, bijvoorbeeld `PROEVEN/science-duurproef/<eigen-tijdstip>/`. Historische pakketten blijven ongewijzigd. Geen nieuw loggerraamwerk, nativefixture of DLL-bouw.

Broningreep: `PROEVEN/selectie-pad-diagnose/20261020T192500/reader/Lees-Uitbreiding.py` SHA256 `db164c59641d58487cb35226da4e7485a1e3a891b912abc5b8c6c6772006810c`. De huidige CLI kent al `release-v1` en `U30-40`, maar regel294 sluit runtime af op alleen kandidaatT0/T1. Vervang in de eigen adapter uitsluitend deze eindige scope door geheleT0..T26 plus een expliciet rootvrijgegeven arm. Gebruik de bestaande gebonden getters, scalars, voorraad-/frontcache-/armytellingen en huidige loggerdecoders. Geen nieuwe foreignreads, pointerketens, callbacks of writes.

Twee exacte bindings blijven onderscheiden:

- Doel3-release SHA256 `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890`: bestaande releasebinding, geen U30-40-sharedstate lezen of nieuwepayloadcheck als waar presenteren.
- Ongewijzigde kandidaat SHA256 `df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e`; manifest `5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152`, eigenstate RVAeb000/497924bytes. Behoud alle actuele module-/payload-/window-/recordbindings en stable_twice.

De nieuwe livepoort bindt PID/creation, arm, run-id, T0..26 en eigen outputdirectory, kandidaat/releaseverwachte diskhash en alle eigen/gebruikte bronpins. Bij huidige kandidaat is de geïnstalleerde DLL-pin **df3ac89d**, niet de vooraf herstelde releasehash. Pre-installatiecontrole verwacht juist releaseeb6f. Outputdirectory vooraf aanmaken; ieder pad nieuw en binnen het eigen pakket. Oude gates blijven FALSE. Voor deze uitvoering wordt alleen de kandidaatarm geopend; releaseondersteuning is geen opdracht voor een extra livecontrolearm.

C1 levert kleine brondiff, eigen pins en gesloten poorten voor rootreview. Beperkte offlinecontrole: syntax/import zonder main/RPM, offline binding van beide exacte binaries, acceptatieT0/T26 en afwijzing−1/27/verkeerdearm, opgeslagenT0/T1 en historischeT26-scalarstructuur bruikbaar zonder nieuwe metingen. Bestaande decoderinhoud en betekenis niet wijzigen. Geen herhaling van de oude native7/43/69-suites voor dezelfde DLL. Een gevonden noodzakelijke extra getter gaat eerst met concrete blokkade terug; geen verborgen scopetoename.

## Beslissing 3 — bestaande eenbeurtsrunner, eindig en herstelbaar

Hergebruik in de nieuwe controladapter `PROEVEN/doel3/20261012-release-v1/Doel3.ps1`, **Pass-regels228–255**, SHA256 `b96c810731e879df5bc8a98cff3fc56b0891bfe716bd34d335aaa28ce27d2443`. De root behoudt GUI/hostownership. Uitvoerder bezit uitsluitend nieuwe reader/controlbron en beperkte offlinecontrole; geen eigen ongecoördineerde hoststarts.

Exacte noodzakelijke delta tegenover die bestaande Pass:

1. Vereis de laatst geaccepteerde eigen snapshot, dezelfde PID/creation/arm, deelnemers2..8, stabiel en turnn−1. Check frisse accountlimieten, huidige deadline en proces-/vensteridentiteit vóór iedere invoer. VoorT0 zeven rondes−1; vervolgens exact iedere ronde+1.
2. Schrijf **vóór** de n-invoer het unieke `(run-id, turn)`-consumptietoken met exclusieve nieuwe-bestandscreatie. Token eenmaal verbruikt blijft verbruikt bij fout/onderbreking. Geef exact één n. Geen herstart van dezelfde Pass, geen blinde inputretry.
3. Poll maximaal30s op de reeds verzonden beurt. Alleen specifiek herkende tijdelijke snapshotinstabiliteit mag binnen diezelfde termijn opnieuw worden gelezen; geen generieke exceptionretry en geen extra n. Accepteer pas twee volledige gelijke snapshots en alle zeven native rondes exact+1; bij uitblijven/overslaan/missende civ stoppen, scherm bewaren en normaal sluiten. T26 is de harde beurtgrens.

Maak vóór installatie verse29backups en verifieer nu **zes** bestaande science-autosavearchieven: de vijf uit host21/host1/before plus diens nieuwe `U30-SELECTIEPAD-20261021-HOST1-AUTOSAVE`. Archiveer eigen nieuwe autosave dubbel onder een unieke duurproefnaam en packagecopy; overschrijf geen bestaande archive. Verifieer vasteT0 en overige named saves. Installeer uitsluitend deze reeds technisch gecontroleerde kandidaat; overige18releaseconfigbestanden blijven gelijk. Geen native/build nodig.

Gebruik dezelfde eindige menulaadroute met exacteT0-alias/hash en beeldcontrole; start geen nieuw gegenereerd spel. Intro mag tot180s duren; begrens loadfase op300s vanaf processtart. Voor deze langere26-beurtsarm is de oude éénbeurthostdeadline ontoereikend: nieuwe maximale totale looptijd **1500s**, geen nieuwe n vanaf1440s, minstens60s voor gewone afsluiting/archivering/herstel. Een onvoltooide beurt door deadline wordt niet als gemeten geaccepteerd. Controleer budget tijdens polling en tussen beurten; stop bij vijfuur≤5% of week≤10%, waarschuwing week≤25%, verouderde bron eenmaal herlezen volgens AGENT-CTP. Geen nieuwe start als verse ruimte onvoldoende is om deze eindige arm plus herstel uit te voeren.

Gebruik de recente bound-input/capture/normal-close/restorehulpen: exacte executable/PID/creation/window, korte wachtmomenten, geen forcekill. Normaal CloseMainWindow eenmaal, maximaal10s exit afwachten; herstel pas na bewezen count0. Bij niet normaal sluiten geen DLL tijdens levend proces vervangen. Na exit: kandidaat vervangen door geteste release, alle29beforetoestanden exact controleren, zes oude archieven behouden, eigen autosave dubbel controleren, alleen eigen hashgelijke alias verwijderen, alle eigen livepoorten FALSE, pc aan. Budgetstop stopt uitsluitend projectwerk.

Risico's: latere passes kunnen bestaande decodergrenzen bereiken; snapshotinstabiliteit of dialoog kan voortgang stoppen; historische controle is geen simultane of herhaalde causaliteitsproef. Vóór C alleen deze kleine bron-/poortdelta reviewen; geen extra engine-instrumentatie als preventief werk. Combinatie-effecten worden hier juist gemeten: dezelfde volledige kandidaat inclusief behouden Doel3, science/uitbreidingslogica en diagnostische bytes versus Doel3 alleen. Verschil mag niet uitsluitend aan de logger of één science-instructie worden toegeschreven.

Alternatieven: uitsluitendT1 blijven observeren beantwoordt geen duur-/uitbreidingsvraag; een nieuwe Doel3-controlearm verdubbelt nu spelwerk zonder ontbrekende stads-/regeringsinformatie; een andere DLL, nieuwe quota of diagnose verandert meer dan de te toetsen factor. Daarom eerst deze ene begrensde kandidaatarm.

**Overdracht B→C:** drie beslissingen gereed, geen strategische gebruikerskeuze ontbreekt. Rootreview/uitleg → uitsluitend eigen reader/control-C1 → bronreview en beperkte offlinecontroles → root beheerde kandidaatT0..26 → compacte vergelijking per civ, geldigheid/beperkingen en volledig herstelbewijs. Voorstelagent gestopt na overdracht; geen achtergrondwerk.
