# C2b — statische byteoverdracht

23 oktober2026,16:10 Europe/Amsterdam. Alleen toegewezen C2-VERIFY gewijzigd.
C1/C2a-bronnen, historische pakketten en de drie bouwoutputs bleven intact.
Geen RPM, native, testharness, spel of installatie uitgevoerd of voorbereid.

De ene toegestane tweede compose is in een verse interpreter uitgevoerd,
zonder main of schrijven van een kandidaat. Kandidaat- en payloadbytes zijn
rechtstreeks exact gelijk aan de eerste bouw. KandidaatSHAacfeec096ea39e1ff38435214769f4d24074e640b856e08d1c82cc09ea7a4984;
bewaarmanifestSHA0a10a7c7f1af1ecd0d71e549296a4e31ea850f100812515d519fa4055e497d4d.

De eerste checker gaf manifest_object/manifest_serialized FALSE: de verse
Pythonmanifestdict bevat tuples (execute_slot_HIGHLOW), opgeslagen JSONlijsten;
directe LF-encoding verschilt bovendien van Windows-write_text met81002CRLF.
DETERMINISM.json bewaart deze oorspronkelijkeFalse en de tweedecomposehash.
MANIFEST-REPRESENTATION.json legt de correctie vast: tweede geserialiseerde
LFmanifestSHA90ee277d8008f4072aaf8ddc0b806b6d57f3be047ff0f3dd3de4750ebd238ab3
is exact gelijk aan de SHA van het bewaarde manifest na alleen universele
newlinelezing. Er is geen derde compose uitgevoerd en geen output herschreven.
De afwijking was checkerrepresentatie, geen byteverschil in DLL/payload.

BYTE-REVIEW.json registreert de geslaagde uitsluitend statische controles:

- Alle oorspronkelijke verschillen:82bytes, disjuncte named patches, exacte
  before/after/full_diff inclusief alle aangehangen bytes;0onverklaard.
- PE-checksum, RX/RW-flags, relocaties gelijk aan basis/ouder, execute-slot
  HIGHLOW behouden; state0xef000/0x79904 helemaal nul, generation+0x79800.
  B2/H3 én tussenpadding bytegelijk aan ouder; payload en RW/rawpadding exact.
-15607extensionrecipe-regels binden aan echte PE-bytes;15609extension-
  instructies onafhankelijk Capstone-gedecodeerd;4622directe targets exact.
  De bestaande compose decodeerde in totaal17097instructies inclusief H3.
-6807instructieregels buiten direct_path/cached_path/selectie ASM-gelijk;
  verschoven bytes uitsluitend dezelfde benoemde branch-/PIC-adressen.
  De hele native1endpoint-/safetyloop blijft ASM-gelijk.
- Werkelijke finalize→selection→cache→directcallparen, Plan/globalgeneration-
  materialisatie en alle effectieve manifestlabels gecontroleerd.11passguards
  en7pairguards bewaren registers en tonen gebalanceerde scratchsuccess/fail-
  exits. Eigenframe320 en alle16beste-bronwoorden worden bewaard/teruggelezen;
  commitwrite volgt pas na de creditguard.
- Alle16hardfailurelandings behouden. Edge4 heeft precies4ingangen:
  onverwachte nativecode en3dirty-zerooutputguards. Schone native0branch test
  cap/count/pointer0 en keert4 via dezelfde cleanup terug.20nativeargs en
  volledige enginefree-route zijn bytegelijk aan ouder, direct/cache-ret12 en
  select-ret4 blijven; daadwerkelijke callee/ABI-werking blijft native-open.
- Cachewaarde1..4 expliciet begrensd; selectie1credit/2en4source_next/3prefix-
  stop/0enanderehardfallback. Diagnosemaskers zijn ook in uitgegeven bytes
  aanwezig, local4mask en4/4/1propagatie gelijk aan manifest; historische
  parentedge-RVA's duidelijk provenance. Effectieve C1-modulemappings exact.

Bij controle is alleen de checker verfijnd: een te brede cmp-eax4telling telde
ook twee bronkindguards, daarna beperkt tot de twee daadwerkelijke cache-
resultaatguardsequenties; de lokale functiedefinitievolgorde is gecorrigeerd.
Er is geen blokkerende kandidaatbytefout gevonden of kandidaatcode aangepast.

Dit is C2b technisch statisch bewijs, nog geen native-ABI- of gameplayacceptatie.
Rootreview blijft nodig. Eigen bouwgate is volgens root alleen voor bouwen
TRUE; overige gates blijvenFALSE. Volgende stap uitsluitend na afzonderlijke
rootopdracht; geen nieuwe nativeharnessbron voorbereid. Uitvoerder gestopt.
