# C2a — minimale builderadapter, alleen bron

23 oktober 2026. C1 is rootgeaccepteerd in REVIEW-PAD-LOKAAL-23.md.
Deze nieuwe map bevat uitsluitend de volgende bronstap; C1 en historische
pakketten blijven bevroren. Geen compose/emissie/build/native/RPM/game/install.

build_candidate.py laadt in een verse interpreter de gepinde C1-source_imports
vóór import van de historische builder. Exacte native/policy/Trace/layout-
module-identiteiten worden gecontroleerd. De historische OUT blijft een
alleen-lezen inputpad voor science/inputpins/integration/development. Alleen
compose() wordt hergebruikt; de historische verify_base wordt vervangen en
historische main wordt nooit aangeroepen. De bestaande compositiecode,
oorspronkelijke-byteclassificatie, B2/H3- en relocatiebehoud blijven dezelfde.

Vóór compose vereisen eigen entry en eigen verify_base een nieuwe rootgate,
de exacte C1-SOURCE-PINS-SHA4a2799b… plus alle152 onderliggende pins, huidige
ouderDLLdf3ac89d…/manifest5b05daf3…, historische builderb042c85e… en eigen
SOURCE-PINS. De gate is nu FALSE; toekomstige vrijgave moet exact de dan
reviewde SOURCE-PINS-SHA noemen. Daarmee zijn builderbron, C1 en de vaste
outputmap20261023T155300-build gebonden. De eigen mutable gate staat buiten
de onveranderlijke bronpins; de bevroren C1-FALSEgate blijft wel gepind.
De oude ROOT-BRONREVIEW kan deze adapter niet vrijgeven. Native/RPM/game/
installatie moeten ook bij een latere bouwvrijgave FALSE blijven.

De eigen main kan later uitsluitend drie nieuwe bestanden direct in deze map
schrijven: U30-40.prepared.dll, U30-40.payload.bin en candidate-manifest.json.
Een bestaande output wordt niet overschreven. Er is geen reader/candidate-
kopie, CTP-proefinstallatie of uitvoering van een binary. Herhaalcompositie
voor determinisme vereist afzonderlijke verse interpreters; deze C2a-check
doet geen compositie. Alle gates blijven gesloten na bronoverdracht.

Het nieuwe manifest bindt effectieve C1-modulepaden en hashes, daadwerkelijke
nieuwe emitterlabels/callparen, state/generation/Planlayout, zestien landings,
local4returnmask en schone0/4/cache/selectiesemantiek. Historische source- en
dependencylijsten/proposalhashes blijven afzonderlijke provenance. De16 oude
parent-edge-RVA's worden expliciet historical_parent_edge_rva genoemd; hun
werkelijke nieuwe landings komen uit de nieuwe emissie. De oude quotaformule,
prioriteiten en budgets blijven de bestaande manifestvelden behouden.

check_sources.py doet AST/syntax en echte imports in een verse interpreter,
controleert alle bronpins en de expliciete weigering door de gesloten gate.
Het roept geen emitter, compose, main, native of RPM aan. SOURCE-REVIEW.json
en SOURCE-PINS.json registreren die beperkte controle; ADAPTER-ENTRY.diff
toont alleen de vervangen oude entry/verify/manifest/outputroute. De volledige
historische composebody is hergebruikt en wordt niet gekopieerd of aangepast.

Na rootreview en afzonderlijke bouwvrijgave zijn noodzakelijke bytechecks:

- Nieuwe RX/RW-adressen, exacte Plan0x79800/generation+0x79800/record+0x79804/
  state0x79904; secties, rawpadding, relocaties, checksum en classificatie van
  alle oorspronkelijke gewijzigde en aangehangen bytes.
- Nieuwe compareguard-PIClabels,320stackframe en balans pushad/8scratchbytes,
  canonicalcall-ret12 en echte selection→cache→direct-returnadressen.
- Exacte native20args/ret80, alle originele native1endpoint-/safetyroutes,
  schone0 naar4 via één bestaande cleanup en nonnull exact-eenmaal-free.
- Alle16hardfailurelandings, local4branch en4/4/1reachedmask, cachewaarde1..4,
  expliciete2/4source_next,3prefixstop,0/anderehardfallback en beste-positieve-
  snapshot/commitguard; diagnoseUNKNOWN bij niet-representeerbare combinatie.
- Werkelijke module/source mappings en nieuwe manifestcall-/labeladressen
  vergelijken met gedecodeerde bytes; B2/H3/overige bodies en oorspronkelijke
  quota/prioriteits-/30/40code behouden; twee verse composities deterministisch.

Dit zijn komende controles, geen uitgevoerde byte- of nativeacceptatie.
Geen harness of fixture aangepast. Werk stopt na C2a-bronoverdracht; volgende
oplevering is onafhankelijke rootbronreview, niet automatisch een build.
