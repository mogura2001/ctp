# Gepaarde uitbreidingstest op de nieuwe landstart

27 oktober 2026, 16:32 CET. Fase B na de overgedragen brede analyse, de geteste uitbreiding en [nieuwe kaartcontrole](../PROEVEN/landbenchmark/20261027/KAARTBEOORDELING.md). Voorstel gereed; root legt de uitleg aan de gebruiker voor uitvoering uit en beoordeelt bron en host afzonderlijk. Geen nieuwe gameplaywijziging of bouwopdracht.

## Doel en vergelijking

Doel1/1a vraagt snelle nuttige uitbreiding naar30, vervolgens bruikbare verdere vestiging tot40; Doel3/Theocracy moet behouden blijven. De bestaande kandidaat gaf op de oude kaart121 tegenover86 steden. Die kaart mengde uitbreiding met eiland-/transportbeperkingen. De nieuwe kaart heeft visueel veel land, maar geen bewezen30-locatiecapaciteit voor iedere civ. Daarom beide versies opnieuw vanaf exact dezelfde nieuwe start meten. Oude totalen zijn geen controlearm voor deze kaart.

Er verandert geen FLI/AIP-regel, beleidsformule of binary. De eerdere FLI/AIP- en DLL-analyse en bron-/byteacceptatie blijven van toepassing. De proef vergelijkt het bestaande complete uitbreidingspakket; zij is geen nieuwe isolatie van iedere interne branch.

| Arm | Exacte bron/binding |
|---|---|
| Controle `release-v1` | Geteste Doel3-release, `CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll`, SHA256 `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890`; verse backup vóór installatie |
| Kandidaat `U30-40` |19 bestanden onder `VERSIES/uitbreiding-2026-10-22-T100/files/`, volgens `manifest.json`, manifestSHA `c665c92f19e37abe49d627a86070306b93519a7088399e90763a2a102a36e950`; DLL `df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e` |
| Beiden | `UITBREIDING-LAND-T0`, archief `PROEVEN/landbenchmark/20261027/UITBREIDING-LAND-T0.original`, SHA `a670867460bae5d8d9196856d5ca88163b0eff951e9a9db42a05b83ee38d2301`; nieuwe gepinde `participants.json` uit dezelfde map |

Root heeft de19 pakketbestanden en19 actuele baselinebestanden exact gecontroleerd. De achttien niet-DLL-bestanden blijven gelijk. Afgewezen padkandidaatacfe niet gebruiken. CTP-og/AAIP en historische bronnen blijven onaangeroerd.

## Kleinste uitvoeringsbron

Maak één eigen nieuw tweearmenpakket. Hergebruik de bestaande reader `PROEVEN/uitbreiding-lang/20261022T122400/Lees-Duur.py`: die bindt beide juiste DLL-varianten al. Alleen eigen namespace/pins/deelnemerspad/startbinding aanpassen. Laat dezelfde bestaande `native_expansion_state`-getters ook voor `release-v1` lopen; de bestaande `shared_state` retourneert daar None. Geen nieuwe resolver, geheugenvelden, enginecalls of observer. Baseline `loaded_settler_type` kan UNKNOWN blijven; vergelijk bestaande per-type `native_stock`/settlercategorieën, settlerarmies en fronten eerlijk. Geen kandidaat-rawtype op baseline plakken. Volledige queues/missievrijheid blijven UNKNOWN.

Neem het immutable protocol van `20261026c-host/Pass-Duur.ps1` over voor beide armen: eigen CreateNew startn0, token/pass/snapshot per beurt, PID/fullFILETIME/window/run/helper/voorgaande hashes; geen registratie herschrijven. Behoud variantgebonden loadedchecks en modulebinding. Minimale checks: hashes/diffs, syntax, beide scopepaden en ongewijzigde getters; geen herbouw of herhaling van de oude101 referentiemetingen.

## Uitvoering en meetlat

Eerst controle, dan kandidaat; afzonderlijke normale spelstarts/herstel. Per arm maximaal100 gewone `n`/101 stabiele snapshots, mens1 passief, AI2..8 allemaal rapporteren. Gebruik steeds de onbewerkte T0; nooit de Show Map/editorload doorspelen. Geen verkenning, stichting, AI-selectie of queuebediening tijdens de run.

Intro maximaal240s en zichtbare load/T0 maximaal360s: de laatste echte intro vereiste191s. Hard4500s en geen nieuwe `n` vanaf4380s, steeds vanaf oorspronkelijke processtart; reviews resetten geen klok.

T0: savehash/laadnaam/Turns0/4000BC, eigen proces/modulebinding, tweemaal stabiel alle zeven native ronde−1. Controle-T0 is het anker; kandidaat-T0 moet dezelfde gemeenschappelijke oorspronkelijke civscalars hebben, behalve actor/AIP-pointers en expliciete armdiagnose. Onverklaarde afwijking stopt vergelijking. Save-identiteit en atomiciteit niet als afzonderlijk bewezen markeren.

T1: precies één token/één `n`, alle zeven stabiel ronde0; rootreview vóórT2. Daarna totT26, rootreview vóórT27, vervolgens maximaalT100. Deze reviews bewijzen compatibiliteit, geen foutgevallen of beleidswinst. Een gewone onbereikte/overschreven diagnose blijft UNKNOWN; echte bindingmismatch stopt.

Bewaar alle tussenmetingen. Rapporteer per civ T25/T50/T100 steden, aanwezige settlerarmies, per-type Desired/Actual/tekort, settlerfronten, Religion/Theocracy/actieve regering en eerste bezit>=25/30/40. Fronten zijn geen volledige queues; bezit geen bewezen nuttige eigen stichting. Diagnosebuffer slechts aan de werkelijk gebonden laatste civ toeschrijven.

Positieve uitbreiding op deze start: hoger T100-totaal, geen lagere individuele eindstand en behoud van de afgesproken vroege Religion/Theocracy-opening. Rapporteer per AI de feitelijke regering opT26/T100, eerste actieveTheocracy en eerste gelijktijdige waarneming van minstens30 steden én actieveTheocracy afzonderlijk. Na die gecombineerde openingsmijlpaal mag een latere regering volgen; anders danTheocracy opT100 is dan niet automatisch regressie. Onverklaard verlaten vanTheocracy vóór die mijlpaal blijft een te onderzoeken regressie; de voorafgaande normale Despotism-/Anarchyfase is op zichzelf geen fout. Gemengde uitkomsten afzonderlijk tonen; gelijk is geen winst. Doel1 niet afronden op totaal of bezit: nuttige30-stedenopening vereist aanvullend bewijs. Doorgroei/rem op40, nulruimte, transport en missies niet uit deze metingen afleiden. Eén paar is beschrijvend, geen algemene causale/statistische garantie; alleen bij beslissende onzekerheid gericht herhalen.

## Stop en herstel

Vóór iedere arm vers budget, count0, gewone cd, exacte19config/118effectieve beschermde bestanden, verse backups van alle huidige saves/archieven/profiel en unieke hashgelijke alias. Alleen de geteste arm installeren; geen bestand onder levend spel vervangen. Iedere input vereist verse budget/binding/voorgaande snapshot en ongebruikte beurt. Poll maximaal30s; alleen bekende tijdelijke instabiliteit herlezen. Fout/focusverlies/dialog/sprong/ontbrekende civ/tijd/budget stopt verdere input; geen blinde retry.

Budget week<=25% waarschuwen, week<=10% of vijfuur<=5% stoppen; unknown/stale eenmaal herlezen. Normaal eigen CloseMainWindow, maximaal10s; geen forcekill/herstel onder levend spel. Na count0 autosave dubbel uniek archiveren plus packagecopy/hash, alle before/config/saves/profiel exact herstellen, alleen eigen hashgelijke alias verwijderen. Releaseeb6 terug, gatesFALSE/count0; pc aan. Bij vroegtijdige stop uitsluitend het gezamenlijke gemeten interval vergelijken, geen automatischeT101.

## Overdracht en voortgang

16:32 CET: voorstel afgerond en ontwerper gestopt. Geen code/install/build/RPM/UI/spel uitgevoerd. Volgende oplevering: rootreview/uitleg, daarna minimale C-bron en afzonderlijke hostvrijgave. Alternatieven: oude kaart hergebruiken behoudt de confounder; alleen een nieuwe kandidaat zonder nieuwe controle geeft geen gepaarde vergelijking; nu quota/telemetrie uitbreiden mengt factoren. Geen nieuwe strategische gebruikerskeuze nodig. Laatst gecontroleerd15:29:52UTC: vijfuur56%/week79%, stateok.
