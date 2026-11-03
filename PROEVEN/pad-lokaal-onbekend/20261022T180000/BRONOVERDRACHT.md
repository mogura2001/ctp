# C1 bronoverdracht — schone native padnul

23 oktober 2026, Europe/Amsterdam. Alleen bron voorbereid voor rootreview.
Geen kandidaatbouw, emissie, nativefixture, RPM, installatie of gameplay.
ROOT-VRIJGAVE.json blijft op alle velden FALSE. Historische CHECKPOINT-*
beschrijft alleen het onvoltooide kopiecheckpoint van 22 oktober.

Basis: selectie-pad-diagnose/20261020T192500, DLL
df3ac89dd2a9a26e8ddeda58a4285cc010ec69d0b3d2bf8637f239c2b31a4b1e,
manifest 5b05daf368ae3779f89c7234be45b29e1503b70afb62e710c5a450bd58a3a152.
Het geaccepteerde voorstel PAD-LOKAAL-ONBEKEND-2026-10-22.md bepaalt de scope.

## Uitvoerende wijziging

Alleen native.py, path_diagnostic.py en reader/path_failure_decoder.py wijzigen
inhoudelijk. policy.py en path_diagnostic_layout.py zijn bytegelijk aan de basis.
source_imports.py bindt de lokale overrides en de bestaande gepinde dependencies;
check_sources.py controleert syntax/imports, identieke nativearguments/free/safety,
gesloten gates en provenance. Importeren roept geen emitter/helperfunctie aan.
De adapter bevat geen kandidaatbuilder of automatische vervolgactie.

pass_compare vergelijkt de herbaseerde eigen pass_state, scope1/guard0/context1,
context_error0/status2/reason0, owner en generation met scratch+78800/+78804,
positieve generation met de globale generation, civ1..31 met owner+20 en actuele
ownerinterfaces. Bestaande bind_host/bind_inputs blijven het oorspronkelijke
vtables/callee/fingerprintbewijs leveren; de nieuwe guard bindt niets opnieuw.

De selectiestack groeit van96 naar320 eigen bytes (ABI-ret4 gelijk).
pass_snapshot bewaart eenmaal de17 onveranderlijke Planinputs op EBP-64..-128:
owner/civ/generation/host/path/world/player/t/d8/planner/scheduler/udb/map/aip/
types/slots/departures. pair_snapshot bewaart per paar vertrekwoorden
0/4/8/12/16/20 op-144..-164, slotwoorden0/4/72/76/28/80 op-176..-196,
canonieke bron op-208/-204 en bestemming op-216/-212. Alle vallen binnen320.
Een gekozen positieve bron bewaart deze16 paarwoorden apart op-240..-300.
Vóór commit worden ze teruggenomen en opnieuw vergeleken met de actuele beste
bron en bestemming. Een later lokaal4 kan die positieve snapshot niet vervangen.

pair_compare bewaart GPR met pushad plus8 tijdelijke stackbytes en vergelijkt
de onveranderlijke Planinputs, huidige slot-/vertrekindices en argumentpointers,
prefix/rol, bron-ID/kind/claim/object, externe bytes en opnieuw geconverteerde
canonieke keys met die eigen snapshots. Het bindt het echte selection→cache→
direct-callpad met de eigen returnlabels. Het herschrijft geen snapshot om een
mismatch op te lossen en leest geen Traceveld. Controle bij source_pre/post,
cache_pre/post en direct_pre/post; passcontrole ook vóór verderzoeken,
bestekeuze en succesvolle selectiereturn. Iedere mismatch gaat naar hard0.
De existing/front/newbuild-admissie blijft inclusief eenmalige claim behouden.

Na de bestaande postcontext-/canarychecks en actuele pair_compare splitst
alleen nativeEAX0 af: cap/count/pointer alle0 geeft lokale4. Alle andere
nativecodes dan0/1 en native0 met afwijkende outputs blijven hard0. Native1
doorloopt dezelfde volledige endpoint-/safetyketen. Lokale4 roept unknown niet
aan, levert geen credit/used-markering en loopt via bestaande path_free/epiloog.
De oorspronkelijke20args, direct/cache-ret12, callee-ret80 en cdecl005866e0-free
blijven gelijk; nonnullbuffer krijgt nog steeds één free. Lokale4 heeft NULL.

Cache bewaart uitsluitend expliciet1/2/3/4 onder dezelfde type/source/destkey;
hard0 wordt niet gecachet. START wist de cache met de bestaande Planreset.
Geen pointer of externe pathbytes worden gecachet. Cachehit geeft geen query.
Selectie:1 enige credit;2/4 source_next;3 bestaande gecommitte-prefixstop;
0/andere integer select_bad. Source_next reset geen beste bron of SELECTED.
Alle caps blijven gelijk:128queries/cache,4096punten,32vertrekken,64slots,
40selected/R. Quotaformule, prioriteitsconsolidatie, Actual en30/40gates gelijk.

## Diagnosecompatibiliteit

De bestaande schema1/256bytes en zestien historische edges blijven gelijk.
Schone4 kan dezelfde edge4operanden laten staan, maar valid blijft0 totdat
direct4/cache4/selectie1 geldig voortplanten. publish_local bindt de opgeslagen
eigen bron-/slotobjecten en de bestaande call/Plan/generation/reachedmask.
Bij een latere echte query klopt de querybinding niet meer: record blijft
ongepubliceerd UNKNOWN. Geen volledig causaal verloop of verloren prefix claimen.
De decoder behoudt de oude hard0/cache0/selectie0/reason25branch; uitsluitend
gebonden schone4/4/1 geeft LOCAL_UNKNOWN_PAIR, selected=false/certified=false/
no_route=false. Dit bewijst geen alternatief pad of extra geselecteerd slot.

## Controle en volgende poorten

SOURCE-REVIEW.json bevat de daadwerkelijk uitgevoerde C1-syntax/importcontrole;
diffs/ de compacte brondiff; SOURCE-PINS.json alle eigen en gebruikte historische
bronpins plus de volledige reeds bevroren dependencyset. Geen emitter is
geïnstantieerd of aangeroepen. Deze broncontrole bewijst geen native ABI of
gameplaywerking. Er staat geen nieuwe DLL/EXE/BIN in dit pakket.

Na rootbronreview is een aparte C2-bouwpoort nodig met herbinding van eigen
emissieadressen, callsites, state/generationlayout en manifest. De huidige
historische builder blijft ongewijzigd en mag niet stil als nieuwe builder
worden aangeroepen: de lokale adapter en nieuwe semantiek moeten expliciet
worden opgenomen. Ook de zestien diagnose-landinglabels en returnmask4 worden
dan op eigen bytes gecontroleerd; historische RVA's zijn geen patchlijst.

Voor een later afzonderlijk vrijgegeven nativepoort zijn bestaande
selectie-pad-diagnose/20261020T192500/native-v2/NativePathLoggerCaller.cs en
settler-b4/NativeProducer.cs met bestaande query/cache/selectie/ABI-stubs
herbruikbaar als patroon, plus de bestaande fixture_sources.py
voor dezelfde bounded Tracevorm. De oude loggerfixture maakt alleen fictieve
frames en test geen nieuwe uitvoeringsguard. Pas haar frames/snapshots en
globalgeneration daarom eerst expliciet aan; voer haar nu niet uit. Nodig:
schone0→4→positief;4-cachehit;positief vóór later4;prefix/claims/conflict;
stale bindings en alle hard0varianten;onveranderde1-safety/2/3;128/4096grenzen;
exact-eenmaal-free/ABI en gelijke quota/priorityentries. Nativeacceptatie en
eventuele hostpoort/horizon beslist root afzonderlijk.

Doel1/1a blijven OPEN: eerder121vs86 hoort bij de bestaande kandidaat, geen
claim over deze ongebouwde ingreep. Geen25/30/40 of volledige rem aangetoond.
Herstel: dit bronpakket verwijderen/negeren na behoud pins; historische basis
en CTP-proef/CTP-og zijn niet gewijzigd. Werk stopt na deze C1-overdracht.
