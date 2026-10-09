# B4: runtime-identiteit en volledige settlertypescope

9 oktober 2026, 14:35 Europe/Amsterdam. Eén gerichte C-terugvraag vóór afhankelijke producercode. De eerdere [ownerbindingvraag](ONTWERPTERUGVRAAG.md) is opgelost; zij wordt niet heropend. Beperkte offline C, geen spel-/binarywijziging, nativeenginequery, eigen nieuwe disassembler of emulator.

**Exacte terugvraag:** welke bestaande gebonden native naam-/type-resolver identificeert in de actuele geladen UnitDB het echte `UNIT_SETTLER`-type, met volledige ABI, owner-/bounds-/failurevoorwaarden, en welke gebonden native settlerpredicate herkent andere water/space/upgrade-settlertypekeuzes in de complete effectieve klassepreview? Lever alleen de minimale concrete route/bytes voor deze scopebeslissing. Een beschikbaarheidsbool, klassebenaming of vaste numerieke tekstindex bewijst die typeidentiteit niet. Dit is één typescopebindingvraag, geen verzoek om volledige unitdatabase- of techanalyse.

## Verplichte gekozen scope

Frozen [B4-producervoorstel](../../ONTWERP/PRODUCER-SETTLERVRAAG-B4.md), SHA535a2a8390bade32530610c2ca501fd247e7f4e8d50222b922a3e89366cc0794, onder 'Typevoorraad, assignments en claims': uitsluitend echte geladen UNIT_SETTLER, gecontroleerde UnitDB/legaliteit/movementbinding, **geen gegokt numeriek typeID**; andere/ongedefinieerde settlertypes of gemengde water/space/upgradescope zetten **hele pass uit**; niet-settlers behouden oorspronkelijke quota.

Deze poort bepaalt zowel beheerd t als welke overige selectedtype/q-combinaties het geheel ongeldig maken. Zij moet vóór native Desired afgerond zijn; een onbekend type pas tijdens de quota-adapter ontdekken mag geen deels gewijzigde pass opleveren. Geen vaste ID/alle-landtypes/klasse-labelheuristiek als vervanging.

## Reeds beschikbaar bewijs en precieze lacune

- [Choose_Unit_From_List](../../ANALYSE/BINAIR/settler-producer-b4-reads.txt:891) `20065900–20065997` initialiseert geselecteerd type op−1, leest lijstentries, roept `UnitDB+14` op `2006594c` aan en behoudt de laatste toegelaten entry en quota. De [enginebinding](../../ANALYSE/BINAIR/settler-producer-b4-engine-reads.txt:45) geeft vtable745098+14→531800. Deze query toetst typebeschikbaarheid/obsolete-tech; zij is geen UNIT_SETTLER-naamresolver of algemene settlercategoriepredicate. Output signedtype/q alléén bepaalt de verplichte scope dus niet.
- [Bestaande recordparser](../../ANALYSE/BINAIR/food-growth-unitdb-record-parser.txt:24), `46d3c6–46d414`, levert een concreet aanknopingspunt: tokenstring wordt gelezen via522160; StringDBglobalA7DCFC en call4660f0 leveren naam-ID; vervolgens `454200` wordt met ECX=UnitDB, naam-ID en indexoutput aangeroepen, daarna454310 recordlookup. Dit toont de callerroute maar de naamlookup-/454200-implementatie, volledig output-/returncontract en failguards zijn niet in deze bewijsdump opgenomen. Type-identiteit veilig uit dit callpatroon alleen reconstrueren zou juist de nog ontbrekende binding aannemen.
- [Gebonden recordlookup](../../ANALYSE/BINAIR/food-growth-unit-record-lookup.txt) `4542e0–454305` heeft wel een echte indexcheck:0<=type<DBcount en recordarray+8, stride2c8. Dit is **typeindex→record**, niet de gevraagde naam→actueletype-resolver. De ongecheckte454310-route en parserinsert/namecaller mogen niet zonder implementatie als read-only actuele lookup worden overgenomen.
- Bestaande transportbinding levert rawmovementland Record+30 bit80000000 en afzonderlijke UnitDB+d8/dc-predicates voor padflags. Die ondersteunen movement/callerbranches, maar benoemen niet welk loaded record UNIT_SETTLER is en classificeren niet aantoonbaar elke overige settlerkeuze. BUILDING_REMOVES_A_POP Record+40 bit4000 is gebonden als completion-/popvlag; deze mag zonder verdere bewijsbinding geen universele settlercategorietest worden.

De benodigde ingreeppunten en normale selectie blijven intact. De root kan deze ene resolver/predicatebinding aan A/B terugdragen. Geen nieuw producerframework, scheduler-/save-/pathfinderreconstructie of gameplayrun gevraagd. Als de bestaande UnitDB-interface zelf een geschikte naamlookup/settlemaskpredicate aanbiedt, volstaat haar concrete vtable/bytes/ABI plus read-/failureguards; een volledig nieuw protocol is niet nodig.

## Gepinde bewijsbestanden

| Bestand | SHA256 |
| --- | --- |
| Actueel B4-producervoorstel | 535a2a8390bade32530610c2ca501fd247e7f4e8d50222b922a3e89366cc0794 |
| Opgeloste A-ownerbinding | 0820ea7de6382ae49ea00d3f03a5deef95001220efba65f10768541631679251 |
| food-growth-unitdb-record-parser.txt | 40325190e788953e53dc3234802dae417ba6020f529665122b582d6e1ede7a8c |
| food-growth-unit-record-lookup.txt | 01cf8095d6fc2438ae506b9eb1547105a1a7f400a7cb6ac9e6dfeb35e064c254 |
| settler-producer-b4-reads.txt | 5ecafcb4d1d4ee476cca5aa1d271d193f30d4fb5a1b12c484ec2f4ee6c90caf |
| settler-producer-b4-engine-reads.txt | 9a888543e76542ea813411441e276e23c83630bf107efc36ac916a9d61ad0778 |

## Stand en vervolg

Voorbereid: hervatte opdracht gelezen en vorige ownerbinding opgelost. Offline gecontroleerd: nieuwe hashes/geleverde native readcontracten. Toegepast: niets. Nativeproducerfixtures/gameplay: niet gebouwd of uitgevoerd. Baselinecompositie nog niet beoordeeld; de eerder vastgestelde d4000/header250-collision blijft een routinebouwvereiste ná deze scopebinding. N25/N30 uitsluitend technische labels, productie-N pending.

Geen gameproces geopend/gelezen/bediend/gestart/gestopt; geen installatie, enginequery/free/fatalhandler, game-export of savewijziging. Alleen B4-owneddocumenten en eigen voortgang geschreven. Geen actieve helper/achtergrondrun. Budget14:34:50 bron14:33:51 Europe/Amsterdam: vijfuur75/week34, ok. Root bezit de volgende gerichte faseoverdracht; geen zelfstandig vervolgpakket.
