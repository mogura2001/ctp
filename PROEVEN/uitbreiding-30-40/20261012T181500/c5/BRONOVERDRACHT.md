# C5 bronoverdracht — beperkte focus/cursorcorrectie

13 oktober 2026, 17:48 Europe/Amsterdam. **Bronvoorbereiding afgerond, uitvoerder gestopt voor rootreview.** Geen installatie, aliasaanleg op spelpad, procesquery, spelstart, GUI of RPM uitgevoerd. Gatefalse/baselinefalse. Oude C4-bronnen/resultaten/verbruiktegate zijn niet geschreven.

Voorstel `ONTWERP/UI-FOCUS-CURSOR-U30-40.md`, SHA256 `cef012ac5eb6b9f601bbaa998ebd0afd27d8ee6d83612e1ce451b44a7eb8add8`, is aan C5-manifestinputpins toegevoegd. C4→C5 eigen kopieën/diffs bewaren de bestaande kandidaat SHA256 `f4602a5653c86506cdee97d7af0b8ad80217f1198bee16dbb2f3a8abb8174810`; geen AI-policy, DLL of readerdecoder veranderd. Geteste release SHA256 `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890` blijft de daadwerkelijke basis/hersteldoel.

Controllerdelta: uitsluitend Action Capture passeert de globale OwnState BindWindow zonder vooraf RequireFocus. Binnen Capture opnieuw exacte OwnState/bounds; bij foregroundverlies één eigen `focus-restore-attempt.json` vóór de bestaande ongewijzigde Bedien-CTP Capture-aanroep. Bestaand record bij volgend verlies stopt vóór die toolaanroep. Na geslaagde Capture opnieuw RequireFocus en fysieke PNGdimensionmatch, anders reject. Read/Pass/Guard/Finish, deadline420/470/480, loadedbindings en herstelcontract behouden. Readerdelta uitsluitend C5-gate/labels.

Menu-ResetCursor via de bestaande tool staat in `UITVOERINSTRUCTIE.md`: Guard+actueleboundsmatch, originelePNGtargets, `-Action Click -ResetCursor`, daarna nieuwe Capture en zichtbare selectie. Geen geschatte FromX/FromY, geen nieuw Clickframework. ResetCursor uitsluitend in menu's vóór kaartload. Gewone bestaande toolfocuspoging is geen bewezen runtimeherstel; dat moet in de vrijgegeven arm blijken.

Eigen aliasowner wordt `C5_UI_LOAD_ALIAS_ONLY`; hetzelfde toekomstige exacte Juliuspad `000-U30-40-START-T0` is nog afwezig. Byteexacte vasteT0 `8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26`, aanvankelijkafwezigheidsrecord vóórcopy/count0 en oorspronkelijkehash-onlycleanup na19restore behouden. Nieuw zichtbaarautosavelabel `UITBREIDING-20261013-C5-U30-40-N30-AUTOSAVE`; nieuwe run-id `uitbreiding-20261013-c5-variant`. Geen bestaande save verplaatsen/overschrijven.

Offlinecontrole: alle eigen Pythonbronnen ASTPASS; PowerShellParserPASS zonder controlleruitvoering (`syntax-check.json`). `check_source.py` controleert daadwerkelijke19releasepins plus eigen19truebacks/19baseline/19variant,9saves/profiel enbackups, alleprotected/inputmanifest/T0pins, aliasafwezigheid. Statische diskbindingsrelease8sites52ranges/variant16sites54ranges. Geen reader-main/callback/processread. `source-manifest.json` SHA256 `4fa4136313a286b37ddbb3d8f6b4f79f9382c37a37b4309a4034498a01b9ef60`: acht eigen bronpins en67 expliciete backup-/stagingpins.

Alle zes geschreven bronbestanden hebben volledige C4→C5-diff naast de bron; original_core.py/participants.json bytegelijkgekopieerd. Bereid-script uitsluitend eigenkopie/bron/diffs/gatefalse; checkscript uitsluitendofflinebindings/pinsrapport, geen oude native suites. Er is nog geen C5variant/executionrecord.

| Tussendoel | Werkperiodeopbrengst / acceptatie | Open / volgende concrete oplevering |
| --- | --- | --- |
| Echteactivatie Doel1/1a | Beperkte uitvoeringscorrectie voorbereid en offlinegecontroleerd | Rootbronreview; aparte vrijgave bij vers voldoende budget/count0, daarna echt vasteT0+éénT1/7AI. Geen activatieacceptatie nu. |
| Doel3behoud | Geteste release19/9saves/profiel+trueback/stagingpins matchen | Combinatiegeladenbytes ennativepass nogongeobserveerd; eerdere releaseacceptatie behouden. |
| Uitbreiding30/40 | Geen nieuwe gameplayvoortgang | Langere benchmark, science/monopoly/transport enall7telemetry blijvenopen. |

Budget start17:45:01 bron15:45:00UTC/leeftijd0.7s week80/vijf73/stateok; laatste17:46:58 bron15:46:55UTC/leeftijd3.2s week80/vijf71/stateok. Geen budgetstop, pc blijft aan. Geen achtergrondrun/planning. Root beheert PROJECTSTATUS en vrijgave; deze overdracht verleent geen toestemming voor livewerk.
