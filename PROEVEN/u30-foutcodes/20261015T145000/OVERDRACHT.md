# U30 foutcodes — C naar root

15 oktober 2026, 14:55 Europe/Amsterdam. **Voorbereid en offline gecontroleerd; niet geïnstalleerd of in gameplay gemeten.** Root beheert vanaf overdracht `live/` en de bestaande `c10/C10-ROOT-VRIJGAVE.json`. Gate is nu FALSE. Geen spelstart, UI of procesread uitgevoerd door deze uitvoerder.

Kandidaat `U30-40.prepared.dll`: `8610db83d4e424006f6c8ee3912bac11fd432dd2bb6264c7c9ed5b94fe67dc17`.
Manifest `candidate-manifest.json`: `6bf3d57db8aa1f9c36ae5407292cfd597175420c22e16996a5d593737f8f3437`.
Herstel-DLL `release-v1.robotcom.backup.dll`: `eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890`.

Exacte wijziging: vier finalize-helperfailuretakken gaan naar bestaande `final_done`, één bind_inputs-failuretak naar bestaande `bind_done`. De twee vroege finalizeguards blijven44. Zie `policy.py.u30-source-diff.txt`, `integration_base.py.u30-source-diff.txt` en `binary-diff.json`. Tegen geteste U30 f460 veranderen precies7 bytes: vijf rel32-displacementbytes en twee PE-checksumbytes. Labels, layout, overige recipebytes, prologen/epilogen, wrappers, B2payload/vijf hooks en relocaties blijven gelijk. Geen FLI/AIP gewijzigd.

De bestaande builder/checker zijn hergebruikt met dezelfde pakketdiepte en zonder gewijzigde pinchecks. Oude manifest-/bronpins zijn behouden in `provenance.json` en `provenance/old-candidate-manifest.json`; eigen bronpins staan in nieuwe kandidaatmanifest en `package-pins.json`. De kandidaat is deterministisch tweemaal gebouwd, 4384 instructies gedecodeerd. `candidate-static-checks.json` bevat de bestaande volledige statische uitslag.

Beperkte bestaande C2 compiledfixture: `c2/native-policy-result-r4.json`, `policy-process-r4.json`, `policy-r4.stdout.log`. Elf nativecalls, exit0, terminal bevestigd; kandidaat onveranderd. Twee vroege44, helper10/11/30/40 en36 door host én finalize behouden EAX0/status0/reason/context0. Één bestaande successpipeline behoudt Dorig2/Gcert6/desired6/context1/status5, nativeActual2/priority6/written6 en afsluiting owner/scope0. Iedere call gebruikt de bestaande stack-/callee-saved-/x87controle; success hookcalls controleren exact x87snapshot, interne rekenhelper controleert controlword/depth. Flagsbehoud wordt niet apart native geassert; bestaande flags/x87-wrapperbytes zijn exact ongewijzigd. Changed host/finalizecode bleef byte-intact.

Fixtures gebruiken synthetische callbacks en een eigen gemapte kopie. Voor succesvolle binding is `bind_inputs` bewust vervangen door bestaande true4, omdat synthetische callbackbytes niet de echte enginefingerprints zijn. Failure36 gebruikt juist de echte bind_inputsguard. Dit bewijst foutretourgedrag/fixture-ABI, geen echte hostsuccess of gameplay. Eerste beperkte poging `r3` faalde op verkeerde testinput voor40 (native clamp); bron staat in `*.attempt1`, logs behouden. Finale bron gebruikt q2×INT_MAX-citycount voor bestaande overflowguard40; finale `.source-diff.txt` en pins zijn bijgewerkt. Geen extra suite uitgevoerd.

De C10-reader is gekopieerd op dezelfde diepte. Alleen NEW_HASH en MANIFEST_HASH veranderen. `original_core.py` en `participants.json` zijn bytegelijk; PID/exepath/creationtime/module/loadedcode en tweemaal stabiele reads blijven intact. Offline `trusted_binding('U30-40')` slaagt (54 ranges,16 sites) zonder proceshandle. Zie `reader-offline-checks.json` en drie readerdiffs. De reader accepteert uitsluitend zijn eigen outputmap; maak `c10/variant/` aan voor de latere snapshots.

Rootcommando's na afzonderlijke interne vrijgave, installatie en exacte procesbinding; vul de werkelijk vastgelegde PID in:

```powershell
$py='C:/Users/Stephan/AppData/Local/Programs/Python/Python312/python.exe'
$p='C:/GIT/ctp/PROEVEN/u30-foutcodes/20261015T145000'
& $py "$p/c10/Lees-Uitbreiding.py" --pid $ctpPid --variant U30-40 --run-id U30-FOUTCODES-20261015T145000 --snapshot-label T0 --turn 0 --pass-label before-one-n --manifest "$p/c10/participants.json" --output "$p/c10/variant/T0-direct.json"
& $py "$p/c10/Lees-Uitbreiding.py" --pid $ctpPid --variant U30-40 --run-id U30-FOUTCODES-20261015T145000 --snapshot-label T1 --turn 1 --pass-label after-one-n --manifest "$p/c10/participants.json" --output "$p/c10/variant/T1-direct.json"
```

T0 moet generation0/leeg en zeven rondes−1 tonen. T1 dezelfde PID/creationtime/modules, zeven rondes0. Eén n uitsluitend door root met verbruikt inputtoken. Context0 +10/11/30/36/40 onderscheidt helper; context1 is gepasseerde checks; positieve policy +44 is afwijkend. Laatste buffer is niet per civ en niet atomair. Zie B voor600/690/720s-afwikkelgrenzen en geen180s-minimum.

Minimale installatie/herstelroute voor root: eerst verse budget/count0, eigen echte backups en nieuwe hashcontrole tegen `protected-state.json` (19release/negen saves/profiel; 29/29 nu gecontroleerd), aliasafwezigheid/eigendom. Dat bestand beschermt hashes en vormt zelf geen backup. Vervang uitsluitend `CTP-proef/ctp_program/ctp/dll/ai/robotcom.dll` door eigen kandidaat, na controle van de huidige eb6f... en kandidaathash. Verifieer de kopie. De18 FLI/AIP blijven huidige releasebytes. Geen DLLwissel in een bestaand proces: nieuwe start laadt code; reader verifieert werkelijk geladen bytes en modulebinding. Voor deze foutcodewijziging is geen data-/savecacheverandering nodig.

Na normale exit en verse count0: archiveer eventuele nieuwe autosave met kandidaathash, herstel uitsluitend DLL naar eigen geteste eb6f... backup en controleer alle19/negen/profiel/defaultautosave. Verwijder alleen eigen bytegelijke alias. Geen hergebruik van historische Doel3-RestoreNoStart om naar originele instellingen terug te gaan. Root bewaakt normale sluiting en backups/aliasarchief. Bij afwijkende bestanden bewaren en stoppen voor gerichte review.

Acceptatie Doel1/1a: diagnose technisch voorbereid, echte helperoorzaak en gameplayuitbreiding open. Doel3release is onaangeroerd en huidig eb6f... opnieuw geverifieerd. Geen claim over science/monopoly/transport/30–40-uitbreiding. Uitvoerderswerk afgerond; geen helper of spelrun actief namens deze agent. Volgende oplevering is roots ene T0→T1-onderscheidingsproef.
