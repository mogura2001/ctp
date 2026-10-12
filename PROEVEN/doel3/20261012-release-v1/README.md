# Doel 3 — release v1

**Geïnstalleerd in CTP-proef op 12 oktober 2026 om 17:31:48 Europe/Amsterdam.** Het spel is bij deze installatie niet gestart. De geteste variant blijft geïnstalleerd.

Deze versie bevat B1 + B2a-N30 + B2b: Religion → Theocracy als onderzoeksprioriteit, het gezamenlijke openingsprofiel en de voorkeur voor Theocracy tijdens die opening. De 19 geïnstalleerde bestanden zijn bytegelijk aan de geteste versie. CTP-og, CTP-AAIP, alle negen bestaande saves en het gebruikersprofiel zijn behouden.

In de vaste Deity-benchmark vanaf QUOTA-START-T0 hadden op beurt 26 **alle zeven AI's Theocracy geleerd en actief**. In de originele baseline kende één AI Theocracy en gebruikte geen AI deze regering. De stadsantallen per AI waren gelijk. De N30-save is normaal herladen: alle zeven beschavingen kwamen gezamenlijk exact overeen met de oorspronkelijke T26-toestand op alle acht afgesproken velden. Eén gewone vervolgbeurt naar T27 behield beide technologieën en actieve Theocracy bij alle zeven.

Bewijs: [gepaarde vergelijking](../20261012T165300-baseline2/baseline/T26-PAARVERGELIJKING.json), [herlaadresultaten](../20261012T165300-baseline2/variant/HERLAAD-RESULTATEN.md) en de huidige [installatiecontrole](variant/postflight.json) met [procescontrole](variant/process-postflight.json).

De geïnstalleerde AI-DLL heeft SHA256:

`eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890`

N30-saves bevatten per AI een record van 36 bytes, versie 1, N=30. Laad deze uitsluitend met deze N30-DLL, niet met de originele DLL of de N25-versie. De oorspronkelijke QUOTA-START-T0 blijft beschikbaar als herstelstart.

De uitgevoerde installatieopdracht was:

```powershell
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File C:/GIT/ctp/PROEVEN/doel3/20261012-release-v1/Doel3.ps1 -Action InstallOnly -Arm variant
```

`InstallOnly` gebruikte de bestaande budget-, proces-, bestands- en backuppoorten en stopte vóór spelstart. Het bestaande uitvoeringsrecord wordt bewaard; voer deze installatie niet opnieuw uit als tweede poging.

Herstellen kan wanneer alle CTP-processen gesloten zijn:

```powershell
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File C:/GIT/ctp/PROEVEN/doel3/20261012-release-v1/Doel3.ps1 -Action RestoreNoStart -Arm variant
```

De herstelroute accepteert alleen de exacte geïnstalleerde of oorspronkelijke bytes. Onverwachte wijzigingen blijven behouden en blokkeren herstel. Zij zet de echte backups terug en verwijdert de twee nieuwe FLI-bestanden alleen als deze vooraf afwezig waren. Een later gegenereerde N30-autosave wordt eerst exact bewaard in het eigen archief en onder het zichtbare label `DOEL3-20261012-release-v1-N30-AUTOSAVE`. Daarna wordt het oorspronkelijke defaultautosavepad hersteld vóór herstel van de DLL. Andere saves en het profiel worden niet teruggedraaid. Er wordt geen proces geforceerd gesloten.

De overgang van de opening bij minstens 30 steden én actieve Theocracy is technisch opgenomen, maar nog niet in een partij met 30 steden aangetoond. Dit is geen vestigingsstop: doorgaan naar goede locaties tot maximaal 40 onder Theocracy blijft een afzonderlijk uitbreidingsdoel. Stadsrollen, locatiescore, nieuwe quota en de overige AI-doelen zijn geen onderdeel van deze release. Het volledige project is nog niet afgerond. Root beheert de centrale versie- en doelacceptatie.
