# Rootreview normale padspelproef

23 oktober 2026, 16:42 Europe/Amsterdam. Ontwerp [PAD-SPELPROEF-2026-10-23.md](../ONTWERP/PAD-SPELPROEF-2026-10-23.md), SHA256 `06aff0ac59d76e46a8650c0d9b84a4861db57754b264cf0cc704bdf7cd940ef7`, volledig gelezen. B3/3 geaccepteerd; gewijzigde testvolgorde en blijvende bewijsgrens aan gebruiker uitgelegd.

De gewone CTP-proef-app mag later de reeds statisch gecontroleerde kandidaat laden via haar normale modbestand. Eerst één natuurlijke beurt, dan rootreview; opnieuw review na26, maximaal100 binnen dezelfde procesklok4500s/no-new4380. Referentie is de opgeslagen oude kandidaatdf3 met121steden opT100, niet een opnieuw te spelen controle. Bronvoorbereiding wordt beperkt tot bestaande readerbinding en immutable beurtketen; geen nieuwe waarnemer of wijziging van gameplaybeleid bovenop het geaccepteerde pad-B.

Acceptatie is uitdrukkelijk gescheiden: C1/C2 bewijzen bron/bytes, T0/T1 alleen normale hostcompatibiliteit, een gebonden LOCAL_UNKNOWN_PAIR alleen die ene lokale propagatie, stadstrajecten alleen gemeten uitbreiding op deze start. Nativefoutgevallen/ABI zijn NIET GETEST; een ontbrekende lokale diagnose blijft UNKNOWN. De automatisch afgebroken rawharnasroute wordt niet herhaald of gewijzigd.

Afzonderlijke C4-bronreview vereist vóór hostvrijgave: nieuwe manifest/state/importbinding, alle werkelijk gebruikte bronnen gepind, exacte eigen uitvoerpaden, startrecord read-only/n0, CreateNew-token/passketen en checkpoints vóórT2/T27. Geen herstelretry na ambigu verbruik. Alle huidige uitvoeringspoorten blijvenFALSE.

Hostvoorwaarden: beschikbare gewone cd, vers budget, geen levend spel bij bestandwissel, volledige actuele save-/configbackups, exacte vaste start, volledige zeven-civtoestand tweemaal stabiel en actuele proces/module/vensterbinding. Stop/normalclose/herstel blijven verplicht; geen restore onder levend spel. Doel3-releaseeb6 terug en pcaan. CD E:readyFalse is momenteel de concrete startblokkade; bronvoorbereiding kan onafhankelijk af.

Dit is ontwerpacceptatie, geen spel-/installatie-/RPM-vrijgave en geen nieuwe gameplayacceptatie. Doel3AF; Doel1/1a/volledige5OPEN. Volgende reviewbare oplevering: C4-bron/diffs/pins en gerichte offline admissionchecks van uitvoerder_host_pad_23.
