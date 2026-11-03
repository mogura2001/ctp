# Rootreview pad-lokaal-onbekend — C1

23 oktober 2026,15:53 Europe/Amsterdam. Volledige bronoverdracht en de drie diffs gelezen. Alle152 SOURCE-PINS onafhankelijk exact; diffbestanden opnieuw tegen ouder/nieuwe bron vergeleken. SOURCE-PINS SHA4a2799b02e68fc2338c655d1f28983e6ee83bcd05a074abb2131521e436f737f.

C1 geaccepteerd als bron voor verdere technische verificatie. Bestaande nativefuncties wijzigen uitsluitend path/path_cache/selection; zes kleine snapshot-/vergelijkhelpers toegevoegd. Policy en diagnoselayout zijn bytegelijk; overige bestaande nativefuncties AST-gelijk. Geen emissie/native/gameplay uitgevoerd door deze review.

Gecontroleerd: pushad/scratchstack en frame320 bewaren pass- en paaridentiteit; daadwerkelijke selection/cache/direct-returnlabels en bron-/slotpointers worden vergeleken. De beste positieve bron heeft een eigen snapshot, die vóór commit opnieuw wordt vergeleken. Lokale4 ontstaat uitsluitend na native0, lege outputs, intacte context/canaries en actuele pairguard; cleanup blijft dezelfde enginefree/epiloog. Cache accepteert alleen1..4, hard0 niet; source_next2/4 behoudt positieve selectie,3 behoudt gecommitte prefix,0/andere code trekt selectie in. Alle safety-/endpointregels en aantals-/prioriteitsformules blijven behouden.

Diagnose is aanvullend: oude hard0branch blijft; local4 wordt alleen gepubliceerd bij volledig gebonden4/4/1 en schone operands. Een latere query maakt die ene recordcombinatie UNKNOWN. Geen diagnoseveld stuurt beleid. Bronreview bewijst nog geen correcte machinecode, ABI of werkelijke uitbreiding.

Volgende concrete stap: afzonderlijke minimale C2-builderbron voorbereiden die deze lokale modules expliciet in de bestaande compose-route opneemt en uitsluitend in een nieuwe eigen bouwmap schrijft. Historische builder/main niet uitvoeren of bestanden overschrijven. Review die adapter vóór emissie; eigen adressen/bytes/manifest opnieuw binden. Daarna pas afzonderlijke beperkte nativegevallen volgensB. Geen spel/installatie/RPM-vrijgave.
