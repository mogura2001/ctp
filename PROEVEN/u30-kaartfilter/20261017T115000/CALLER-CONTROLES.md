# Begrensd callerplan — nog ONGETEST

17 oktober 2026, fase C bronoverdracht. Geen fixture gebouwd, gecompileerd of aangeroepen. Eerst rootbronreview en afzonderlijke bouw-/nativevrijgave. Dit plan is de beperkte voorbereiding; er is geen nieuwe loader, observer of algemene suite toegevoegd.

Hergebruik uitsluitend de eigen allocaties (`Mem`, `RX`, `Read`, `Clear`) en de bestaande `Call`-shim/stack/nonvolatile/x87-controles uit `PROEVEN/settler-b4/NativeProducer.cs`, zoals reeds overgenomen door `PROEVEN/uitbreiding-30-40/20261012T181500/c2/NativeU40.cs`. Geen oude `Setup`, `RuntimeInputsGuard`, `read_policy`, `bind_host`, resolver-, finale-pass- of volledige pipeline-suite uitvoeren. Geen fixed-addressallocatie of engine-DLL laden. Alleen rechtstreeks `canonical_prefix` en `production_roles`, in eigen geheugen, met eigen Plan van 0x54800 bytes en rode zones rondom ORDER/CAPTURE/slots.

De begrensde fragmentroute mag de twee helpers uit de eigen emitterbronnen aanbieden met gecontroleerde helperlabels/stubs. Een bestaande `canonical_key` mag rechtstreeks met passende eigen map/vtable-input worden hergebruikt; anders is een expliciete ret12-stub voor deze callercontrole toegestaan, die eigen keys kopieert of op één geselecteerde index faalt. Dit bewijst dan uitsluitend de key-failurevolgorde van de caller, geen nieuwe dekking van de reeds behouden canonical_key-implementatie. De echte H3PosCompare of dezelfde bestaande kleine comparatorstub behoudt de lexicografische keyvolgorde en ties. De World+28-ret8-stub controleert expliciete World-pointer en originele CAPTUREpositie en geeft de gecontroleerde true/false-verdeling; test met callclobber van EAX/ECX/EDX. World+168 gebruikt de bestaande score-ret16-stub. H3Classifier-ret16 mag gecontroleerd UNKNOWN, assessed-no-plan of een bestaand geldig supported-fixtureantwoord geven. Alle substituties in het resultaat noemen. Geen echte hostguard verwijderen om een finale pass te laten slagen.

| Geval | Concrete verwachting | Status |
| --- | --- | --- |
| a | candidates0 en allefalse: prefix0; consumerreturn1, slots0/h3calls0 | ONGETEST |
| b | 65 canoniek oplopende keys; eerste64false, index64true: ORDER0=64, prefix1, gate65/false64/known1 | ONGETEST |
| c | Ongeordende keys met gemengde gates en ties: exact kleinste64truekeys, gelijke bestaande bronindex-tievolgorde; CAPTURE ongewijzigd | ONGETEST |
| d | 65true: prefix64/cutoff1; 4096false: gate4096/prefix0/H3calls0; rode zones/ORDER ongewijzigd buiten64 | ONGETEST |
| e | Ongeldige key ook op een falsegate-index: reason41; gate voor die index niet aangeroepen. nodes!=0, candidates−1/4097: reason41 vóór scratchgebruik | ONGETEST |
| f | prefix−1/65, prefix>known, known>candidates, candidates4097; ORDER−1/candidates: reason23, geen ongeldige CAPTURE-toegang | ONGETEST |
| g | Overige H3UNKNOWN en gesimuleerde later interne gatefalse: reason23; geen blanket skip. Afzonderlijke h3calls>=64-guard blijft reason23 | ONGETEST |
| h | False/truegate, leeg/succes/failureprefix, normale/failureconsumer: dezelfde shim controleert ESP en EBX/ESI/EDI/EBP, x87 blijft intact | ONGETEST |

Voor iedere case: exact input, output, counters en guardzones rapporteren. Oude native-uitkomsten zijn geen bewijs voor deze delta. Stubs bewijzen niet de echte enginegate, bitsemantiek, hostbinding of gameplay. Als deze beperkte aanpassing niet direct uitvoerbaar is: concrete blokkade en ONGETEST aan root, geen fixtureherbouw als vervanging. Root beslist over aanvullende statische/hostdekking.
