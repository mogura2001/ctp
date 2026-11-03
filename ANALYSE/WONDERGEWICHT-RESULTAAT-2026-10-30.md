# Labyrinthprioriteit: bewezen nieuw gameplaygedrag

**Proef geslaagd:** alleen openingsgewicht9100 naar30000 veranderen levert drie nieuwe echte Labyrinthbouwopdrachten op, tegenover nul in de controle. Mexico, Spanje en Portugal beginnen ieder in één stad. Alle zeven AI's laden de bedoelde lijst met uitsluitend Labyrinth.

Beide versies laden dezelfde gepinde2700BC-save/eb6-DLL/deelnemers en krijgen precies één gewone beurt. Root vergeleek de beginstanden: zeven civs met dezelfde relevante technologie-/regerings-/onderzoeksgegevens, alle47bestaande stadsidentiteiten/queues en productie-/voorraad-/rang-/tijdvelden. Na afloop native25naar26 bijalle7; beide49steden, perAI gelijke aantallen. Van vijftien kandidaatbestanden verschillen veertien niet; alleen het openingswondergewicht verandert.

| AI | Volledige stadshandle | Controle9100 na beurt | Variant30000 na beurt |
| --- | --- | --- | --- |
| Mexicanen2 |268435520| Unitklasse1/type5 | Wonderklasse9/type2 |
| Spanjaarden5 |268435476| Unitklasse1/type14 | Wonderklasse9/type2 |
| Portugezen8 |268435479| Unitklasse1/type8 | Wonderklasse9/type2 |

Exacte token/SID/indexbinding identificeert type2 als Labyrinth. Vooraf staat het bij geen van deze steden in de queue; eigenaar/volledigehandle blijven gelijk. Alle vier complete metingen zijn tweemaal stabiel en alle geladen codecontroles slagen. [Root-AB-bewijs](../PROEVEN/WONDERGEWICHT-ROOT-AB-2026-10-30.json).

Root inspecteerde ook [City Status](../PROEVEN/wondergewicht-host/20261030/candidate/citystatus-visible.png):2650BC, Mexicanen8steden, Veracruzsize2 produceertLabyrinth, nog16beurten. Dit bevestigt visueel de productie in dezelfde civ; de native stadsnaam is niet apart uitgelezen.

**Af:** gewenste vroege lijst én daadwerkelijke bouwstart in deze vaste proef. **Open:** voltooiing, langere uitbreidingseffecten, speciale wonderstad/bergwerkers, onbouwbaar-geval, herstel van persoonlijkheidslijsten na30steden en latere wonderkeuze. Geen volledigeDoel4-, optimalegewicht- of releaseacceptatie.

Normale sluiting na701s/count0;162pins en volledige118aidata-/38save-inventarissen exact hersteld. Autosave apart bewaard. [Uitvoerdersverslag](../PROEVEN/wondergewicht/20261030/RUNTIME-RESULTAAT.md), [getest pakket](../VERSIES/wondergewicht-2026-10-30/README.md). De variant staat klaar maar is momenteel niet permanent geïnstalleerd. Pc blijft aan.
