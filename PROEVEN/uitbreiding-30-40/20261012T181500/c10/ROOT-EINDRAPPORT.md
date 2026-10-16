# C10: één echte AI-ronde

Werkperiode gestopt op budgetgrens 14okt17:09:26: vijfuur5%, week36%, verse bron28,8s oud. Alle deelagents runtime completed; geen projectwerk meer actief. Hervatpunt hieronder bewaard. Pc blijft aan.

14 oktober 2026, 17:07 Europe/Amsterdam. De gebruiker laadde de startsave en bevestigde precies één beëindigde beurt. Root stuurde geen `n`.

De bestaande alleen-lezen reader mat in dezelfde instantie PID7896 alle zeven AI's eerst op native ronde -1 en daarna op ronde 0. Beide snapshots zijn tweemaal stabiel; modulebinding, hashes en alle geladen-codecontroles komen overeen. Dit bewijst dat de U30-40-kandidaat geladen was tijdens één gewone spelronde. Het bewijst nog geen hogere settlervraag of snellere uitbreiding. Gcert/Dorig/R zijn per civ onbekend wegens de overschreven gedeelde buffer. Save-identiteit en atomische snapshot blijven onbewezen.

Bewijs: [ROOT-PAIR-AND-RESTORE.json](variant/ROOT-PAIR-AND-RESTORE.json), [T0](variant/T0-direct.json), [T1](variant/T1-direct.json).

Procedurele afwijkingen zijn expliciet bewaard: intro-focusstabilisatie mislukte; de bestaande instantie werd na menselijk laden gebonden zonder klokreset. Capture bleef zwart met spelcursor. Directe read-only metingen vonden plaats onder de interne 15%-werkreserve, maar boven de gebruikersgrenzen. Sluiting vond na de 690/720s-deadline plaats. Daarom geen volledige controllerprotocolacceptatie claimen.

Om 17:05:36 was de exact gecontroleerde eigen instantie na één normaal sluitverzoek beëindigd; verse OSquery gaf nul CTP-processen. Geen force. Herstel voltooid 17:05:48; root verifieerde daarna onafhankelijk 19 releasebestanden, negen bestaande saves, profiel en vijf bronpins (34 matches), aliasafwezigheid en herstelde default-autosave. De nieuwe U30-autosave is in twee kopieën met bijbehorende DLL-hash bewaard. Gate is verbruikt; geen spel of helper draait vanuit deze proef. Pc blijft aan.

Voortgang tegenover doelen: doel3 Religion/Theocracy blijft bewezen en geïnstalleerd. Uitbreiding/doel1 is technisch voorbereid en nu geladen tijdens één echte ronde; gameplayacceptatie blijft open, inclusief 30/40-overgang en ruimte/transport/veiligheid. Science-C1 blijft gedeeltelijk: 29 fixturegevallen eerder gemeten, laatste centrum64/ABI-controle nog open door helperadresbotsing. Wonderkeuze, stadsspecialisatie, berg-/laborerinzet, monopoly/handel, groeibeleid, legerlast en naval warfare zijn nog niet in gameplay opgeleverd.

Gerichte uitlezing van de bestaande laatste-passbuffer: T0 geheel nul; T1 civ8/generation7, status5/reason44, remaining30/policy1/government1/engine_count0, desired0/Gcert0/Dorig0/context0/path_queries0. Dit toont dat eigen policygegevens geschreven zijn. `policy.py:47-59` koppelt reason44 aan `final_bad`; dat kan meerdere voorwaarden samenvoegen. `integration_base.py:84` schrijft daarna status5 en wist scope/owner bij einde AIPUpdate. Daarom is scope0 hier geen zelfstandig bewijs van een scopefout. De laatste pass bereikt geen geslaagde combinatieberekening/status4. Geen bewijs van hetzelfde resultaat voor de zes eerdere civs; gedeelde buffer is overschreven. Ook geen bewijs dat de fout structureel blijft nadat steden zijn gesticht.

Volgende oplevering: gerichte analyse van de bestaande laatste-passbevinding: welke `final_bad`-voorwaarde past bij policy1/remaining30/context0 en zero-city civ8? Onderscheid bind_host, resolve_type, preview_scope en original_demand zonder een hele nieuwe observer te bouwen. Pas na onderbouwde verklaring/benodigde minimale correctie een begrensde gepaarde uitbreidingstest vanaf dezelfde T0, met menselijke beurtbediening. Geen hergebruik van de verbruikte C10-startgate; geen brede analyse als voorwaarde.
