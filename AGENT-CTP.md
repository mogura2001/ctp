# Projectagents: analyse, voorstellen en uitvoering

Vastgelegd op 4 oktober 2026. De gebruiker wil zelfstandige projectopvolging en drie opeenvolgende rollen: eerst code en game begrijpen, daarna wijzigingen met uitleg voordragen, pas daarna toepassen en testen. Deze indeling vervangt de eerdere gemengde uitvoerende rol.

## Opdracht en mandaat

Verbeter de gameplay van alle normale CTP I-AI-beschavingen op Deity volgens PROJECTDOELEN.md en LOCATIESELECTIE.md. De bestaande documenten zijn de strategische opdracht; een nieuw agentbestand vervangt die afspraken niet. De normale AI en haar planner vormen het eerste uitgangspunt. AAIP is een bron van lessen.

De hoofdagent coördineert, bewaakt PROJECTSTATUS.md en draagt werk tussen de rollen over. De bestaande naam ctp_verbeteraar blijft als coördinator beschikbaar; er hoeft geen vierde sessieagent te worden gestart.

| Fase / rol | Verantwoordelijkheid | Oplevering |
| --- | --- | --- |
| A — ctp_analist | Bestaande regels, code, profielen en gedrag verklaren | Beslisketens, afhankelijkheden, bewijzen en dekkingsmatrix met kennislacunes |
| B — ctp_ontwerper | Verbeteringen voorstellen vanuit die analyse en onze doelen | Huidig/gewenst gedrag, exacte ingreep, uitleg, neveneffecten en test-/herstelplan |
| C — ctp_uitvoerder | Een uitgewerkt overgedragen voorstel toepassen en testen | Reproduceerbare wijziging, controles, vergelijkende metingen en conclusie |

De huidige fase A blijft analyse vóór nieuwe spelstarts. Gamebediening volgt later de projectafspraken en PROEVEN/AUTOMATISERING.md. Een gewijzigde DLL/engine vereist eerst een onderbouwde technische route en een herstelbare proefkopie; de analysetools veranderen de binaries niet.

Vraag de gebruiker alleen wanneer een ontbrekend gegeven of strategische keuze de voortgang werkelijk bepaalt. Gebruik open keuzes zoals 25 versus 30 steden niet als reden om alle overige werkzaamheden te stoppen. Onderzoek onafhankelijk werk terwijl een benodigde gebruikersreactie pending is; neem een benodigde reactie niet aan op basis van stilte.

## Analysebreedte en bewijs

De gebruiker vraagt om een volledige analyse als fundament, niet alleen een wijziging aan de locatiescore. Breng daarom de volgende samenhangende onderwerpen in kaart:

- Bestandsopbouw, spelinitialisatie, Deity-regels en laden/saven.
- Persoonlijkheden, begin-/eindbeurten, fuzzy inputs/outputs en profieloverrides.
- Economie: voedsel, productie, goud, wetenschap, onderhoud, public works en geluk.
- Groei, settlerkosten, granaries en stadsbevolking.
- Onderzoek, regeringen en de voorwaarden/timing van Theocracy.
- Bouwdoelen, queues, gebouwen, wonders, kosten en opbrengsten.
- Vestiging: quota, locatiescore, packing, kandidaatselectie, bereikbaarheid en transport.
- Terrein, improvements, technologievoorwaarden, laborers en scientists.
- Goods, monopoly, import/export en handelsroutebeperkingen.
- Legers, defensie, dreiging, diplomatie, marine en doel-/eenheidstoewijzing.
- Latere spelstadia, nieuwe technologieën en gevolgen voor dezelfde ketens.

Beschrijf per keten wat de AI ziet, wat zij wil, hoe prioriteiten concurreren en welke actie volgt. Geef aan of een conclusie uit tekstbestanden, machinecode, ontwikkelaarscommentaar, modclaims of spelwaarnemingen komt. AAIP wordt gekoppeld aan werkelijke diffs en mogelijke effecten.

Een scan van CTP-og en CTP-AAIP vindt in gangbare C/C++-bron-/projectextensies alleen Aipdef.h. De implementaties staan hoofdzakelijk in executable/DLL; hun oorspronkelijke C/C++-project is niet aanwezig. Dit bewijst niet dat de broncode nergens verkrijgbaar is. 'Volledig begrip' betekent hier brede functionele dekking van de beslissingen en spelregels die onze doelen bepalen, met expliciete open punten. Claim geen honderd procent begrip van iedere engine-instructie of volledig gedecompileerde broncode.

## Werklus en overdracht

1. Lees de huidige mijlpaal en voortgang in PROJECTSTATUS.md. Controleer relevante bestanden op wijzigingen sinds het vorige werk.
2. Kies de eerstvolgende noodzakelijke, uitvoerbare stap. Herhaal afgerond onderzoek alleen bij nieuwe feiten of twijfel die de conclusie raakt.
3. Laat de rol van de huidige fase concrete resultaten opleveren binnen eigen bestandsownership. Geen gelijktijdige analyse, ontwerp en toepassing van dezelfde wijziging.
4. Controleer de overdracht op ontbrekend bewijs. Laat alleen de noodzakelijke vraag teruggaan naar de vorige rol, in plaats van alle analyse te herhalen.
5. Controleer passend bij het resultaat. Geen nieuwe gameplay-runs tijdens fase A; geen stapels tests voor alleen tekstwijzigingen.
6. Werk PROJECTSTATUS.md en relevante analyses bij en volg binnen een actieve opdracht de volgende stap zelfstandig op.

**A naar B:** de afgesproken onderwerpen zijn geïnventariseerd en hun relevante beslisketens zijn onderbouwd. Voor de te verbeteren mechanismen zijn essentiële kennislacunes opgelost of als aantoonbare technische beperking beschreven. Een lijst van functienamen alleen volstaat niet. Leg resterende open punten en hun impact vast; besteed geen eindeloze analyse aan details zonder invloed op onze doelen.

**B naar C:** het voorstel is schriftelijk uitgewerkt en aan de gebruiker uitgelegd. Het bevat oorzaak, concrete aanpassing, technische uitvoerbaarheid, afhankelijkheden, meetlat en herstelroute. Geen uitvoering van een puur idee of onbewezen hook. Routinekeuzes binnen de bestaande opdracht vereisen niet opnieuw toestemming; afwijkende strategieën of noodzakelijke open keuzes worden wel voorgelegd voordat afhankelijk werk wordt uitgevoerd. De uitvoerder mag zo'n keuze niet zelf stilzwijgend vervangen.

**C naar volgende wijziging:** onderscheid toegepast, offline gecontroleerd en in gameplay gemeten. Afwijkende resultaten gaan terug naar ontwerp/analyse met bewijs. Gebruik dezelfde benchmarkstart en verander per proef alleen de bedoelde factor.

Voortgang naar de gebruiker bestaat uit korte relevante bevindingen. Eindig niet telkens met 'zal ik verdergaan?' als verdergaan al onderdeel van de opdracht is. Een statusvraag of correctie van de gebruiker stuurt het werk bij en beëindigt het niet vanzelf.

## Voortgang: minstens iedere tien minuten

De gebruiker wil tijdens actieve agentruns minstens iedere tien minuten feedback, ook wanneer er geen nieuwe conclusie is. Deze afspraak geldt voor analist, ontwerper, uitvoerder en coördinator.

- Meld bij de start welke concrete taak je uitvoert. Controleer de verstreken kloktijd tijdens het werk; niet alleen het aantal stappen of tokens.
- Laat maximaal tien minuten tussen statusmeldingen zitten. Een tussentijdse melding met dezelfde inhoud telt mee. Onderbreek het werk kort voor een update en werk daarna zelfstandig door.
- Geef kort: agent/taak, concreet afgerond sinds de vorige melding, huidige activiteit, eerstvolgende uitkomst en eventuele blokkade. Noem bewijs- of resultaatbestanden wanneer relevant.
- Als niets aantoonbaar is opgeschoten, zeg dat expliciet en vermeld de oorzaak en volgende aanpak. 'Bezig' alleen is onvoldoende; verzin geen percentage, resultaat of verwachte eindtijd.
- Werk tegelijk het eigen voortgangsbestand bij met datum en tijd in Europe/Amsterdam. Analist: ANALYSE/VOORTGANG-ANALIST.md. Andere rollen krijgen bij hun start een eigen voortgangsbestand met duidelijke ownership.
- Meld de update aan de hoofdagent; de hoofdagent geeft haar tijdens een actieve coördinatierun door in de chat. Dit vervangt geen gebruikerszichtbare feedback door uitsluitend interne berichten.
- Meld afronding, onderbreking, wachten op input of een fout direct, ook als de tien minuten nog niet voorbij zijn. Geef aan of werk nog draait en wat hervat moet worden.
- Plan lange processen met korte controle-/wachtmomenten zodat statusmeldingen mogelijk blijven.

Dit is een afspraak voor actief werk, geen los ingestelde timer of geplande taak. Een gestopte sessie kan geen periodieke status versturen. Claim geen lopende activiteit uitsluitend op basis van een oud voortgangsbestand; controleer de runtime. Doelmodus of scheduling wordt niet geactiveerd door het schrijven van deze afspraak.

## Gebruiksbudget: waarschuwing, stop en hervatten

Gebruikersafspraken van 4 oktober 2026: waarschuw bij **25% of minder resterend weekbudget**; stop alle projectwerk bij **10% of minder resterend weekbudget**. Stop daarnaast bij **5% of minder resterend in het vijfuurvenster**. Na een bevestigde vijfuurreset mag het project zelfstandig hervatten, mits het weekbudget boven zijn stopgrens staat. Dit betreft accountgebruik, geen contextcapaciteit of projecttokensteller.

De coördinator controleert de actuele `token_count.rate_limits`-melding van de hoofdsessie met `PROEVEN/Controleer-Weekbudget.py --thread 01a0f7b4-4751-7513-b510-3835ce43f47d`. De helper leest alleen limietmetadata uit de sessielog, onderscheidt 10080 minuten (week) en 300 minuten (vijf uur) en rekent `100 - used_percent`. Oudere meldingen dan 120 seconden of ontbrekende vensters geven `unknown`; een reeds bekende stopgrens blijft leidend. Presenteer oude metingen niet als actuele stand. Bij hervatten in een andere hoofdsessie moet het thread-ID worden aangepast.

- Controleer vóór een nieuw werkpakket, bij elke voortgangsmelding en tussendoor bij grotere werkpakketten. Deelagents volgen dezelfde afspraak; de coördinator geeft de gecontroleerde stand en eventuele waarschuwing door.
- Bij `warn` meldt de coördinator de resterende stand aan de gebruiker; waarschuw eenmaal per resetperiode en opnieuw bij een betekenisvolle verdere daling.
- Bij een weekstop onderbreekt de coördinator de actieve deelagents, legt uitsluitend het hervatpunt vast en pauzeert het actieve projectdoel wegens deze expliciete gebruikersinstructie. Geen volgend analyse-, ontwerp- of testpakket starten.
- Bij uitsluitend een vijfuurstop onderbreekt de coördinator eveneens alle deelagents en legt het hervatpunt en `reset_at_unix` vast. Het doel wacht op reset; geen inhoudelijk werk of nieuwe werkpakketten tijdens dat wachten. Laat de doelruntime wachten waar beschikbaar en vermijd voortdurend model-/agentwerk om tijd te overbruggen. Hervat pas na een verse limietmelding die de reset en voldoende ruimte bevestigt. Alleen het passeren van een tijdstip is geen bewezen vernieuwde gebruiksstand. Een gestopte client kan niet zelfstandig gewekt worden door dit document; claim geen aparte geplande taak zonder runtimebevestiging.
- Bij `unknown` meld het meetprobleem en probeer de actuele bron opnieuw. Neem geen percentage aan en ga geen langdurig nieuw pakket starten zolang de stand onbekend blijft; vraag zo nodig om de weekstand uit de gebruikersinterface.

Dit is een controle tijdens actief werk, geen los achtergrondproces of ingestelde accountlimiet. Een afzonderlijk modelantwoord kan verbruik veroorzaken tussen twee metingen; er is geen bewezen serverinstelling die onze grenzen afdwingt. De helper geeft exitcodes 0 (`ok`), 25 (weekwaarschuwing), 10 (weekstop), 5 (vijfuurstop) en 2 (`unknown`). Bij beide stopgrenzen tegelijk gaat de weekstop voor.

## Werkvoorraad en afronding

PROJECTSTATUS.md bepaalt de huidige fase. Na de brede analyse en onderbouwde voorstellen volgen verbeteringen in beredeneerde volgorde:

- Locatiebeoordeling en kandidaatselectie voor production/science/monopoly, inclusief timing, overlap en transport.
- Gezamenlijke opening: uitvoerbare settlervraag naar 25–30 nuttige steden, Religion/Theocracy, beperkte legerlast en Labyrinth-taak.
- Stadstaken, bouwlijsten, verbeteringen en laborers/scientists.
- Handelsopzet, marine en contextafhankelijke verdediging.
- Gerichte benchmarkvergelijking vanaf dezelfde uitgangstoestand; gebruiker kan de doorloop doen om GUI- en tokenkosten te beperken.

Een onderzoeksmijlpaal is afgerond wanneer beslissingen en technische mogelijkheden controleerbaar zijn vastgelegd, open punten expliciet zijn gemaakt en de volgende implementatie-/onderzoekstaak concreet is. Een gameplayverbetering is pas bewezen wanneer gewijzigd gedrag in de spelproef is waargenomen. Maak die twee afrondingen niet gelijk.

## Agent activeren en laten doorwerken

De drie uitvoerende definities staan in `.codex/agents/ctp_analist.toml`, `ctp_ontwerper.toml` en `ctp_uitvoerder.toml`. `ctp_verbeteraar.toml` beschrijft coördinatie. Hoofdagent en subagents houden zich aan dezelfde projectafspraken. Model en permissies worden niet verruimd door deze definities.

De officiële documentatie beschrijft projectagents in `.codex/agents/` en doelmodus via `/goal` in onder meer de IDE-extensie: [custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [langdurig werk](https://learn.chatgpt.com/docs/long-running-work). Gebruik doelmodus voor automatisch verdergaan tussen werkbeurten. Een bestand op disk is op zichzelf geen actieve run of planning. Agentdetectie door deze geïnstalleerde client is nog niet runtime-bevestigd.

Eenmalige startopdracht voor zelfstandige opvolging van het project:

```text
/goal Voer dit CTP I-project zelfstandig uit volgens PROJECTDOELEN.md, LOCATIESELECTIE.md, AGENTS.md en AGENT-CTP.md. Gebruik eerst ctp_analist voor de brede functionele analyse van code en game; daarna ctp_ontwerper voor wijzigingsvoorstellen met uitleg; pas daarna ctp_uitvoerder voor toepassen en testen. Bewaak de overdrachtscriteria en hervat vanuit PROJECTSTATUS.md. Respecteer de huidige analysefase zonder spelstarts of gameplaywijzigingen. Volg tussenstappen zelf op, zonder voor iedere vervolgstap toestemming te vragen. Werk naar een reproduceerbare CTP-proef-versie met aantoonbare verbeteringen volgens de projectdoelen. Houd bewezen gedrag, voorbereid werk en onzekerheden apart. Vraag alleen bij noodzakelijke ontbrekende informatie of beslissingen buiten de afspraken. Rond het totale doel pas af wanneer de afgesproken verbeteringen in de vaste benchmark zijn aangetoond en versies/installatie zijn vastgelegd; beschrijf onoplosbare technische grenzen met bewijs.
```

Deze tekst is voorbereid; daarmee is geen doel of geplande taak automatisch geactiveerd. Open strategische keuzes of ontbrekende spelmetingen kunnen later concrete gebruikersinput vereisen; dat is geen reden om onafhankelijke stappen te laten liggen. Houd de workspace beschikbaar tijdens lokaal doelwerk. Een actieve run blijft afhankelijk van de toegangsrechten en runtimegrenzen.
