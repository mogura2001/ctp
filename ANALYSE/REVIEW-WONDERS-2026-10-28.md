# Review vroege wonderkeuze

28 oktober 2026, 17:27 CET. Root vervult coördinatorrol.

## B geaccepteerd

[Voorstel](../ONTWERP/VROEGE-WONDERS-2026-10-28.md) volledig gelezen, aansluitend op de geaccepteerde [A-overdracht](VROEGE-WONDERS-INGREEP-2026-10-27.md). De bestaande `action load("...") when (...)`-syntax en `input opening_required` zijn tegen de actuele werkversie gecontroleerd. Persoonlijke lijsten worden volledig vervangen en later expliciet hersteld; gedeeltelijk laden behoudt andere categorieën volgens [AIP-laadwerking](AIP-LAADWERKING.md). Alleen Labyrinth met bestaand defaultgewicht 9100 is de gekozen openingslijst. De onderbouwde route vereist geen DLL-wijziging.

Vóór C aan de gebruiker uitgelegd: tijdens de gezamenlijke opening alleen Labyrinth, na de bestaande 30-steden-plus-Theocracy-overgang de eigen wonderlijsten terug. Eerst een afzonderlijk pakket met herstelkopieën en controles; daarna afzonderlijke spelverificatie.

## C0 geaccepteerd, 17:30 CET

Pakketchecker volledig gelezen en zelfstandig opnieuw uitgevoerd zonder outputbestand te overschrijven: PASS. Daarnaast onafhankelijke rawbytecontrole van alle vijftien kandidaatbestanden: zeven FLI-bestanden worden exact before door uitsluitend de twee toegevoegde actions te verwijderen; zeven herstelblokken zijn exact de echte bronblokken; de nieuwe openingspartial bevat alleen de juiste wondertoken. Manifest SHA256 `878e4d000a996389ccf9fb4da09cb2ffa03afe7cc924f6c4fca27957c9fb5195`. [Rootcontrole](../PROEVEN/wonders-runtime/20261028/ROOT-C0-REVIEW.json). Alle huidige 118 aidata-bestanden, DLL en 38 saves behouden.

Volgende uitvoeringsstap aan gebruiker uitgelegd: korte verse laad-/beurtproef met tijdelijk pakket, dezelfde herlaadbare menselijke T0 en maximaal één n, daarna normale sluiting en exact herstel. Geen editorwijzigingen of extra steden/eenheden; geen onderzoekkeuze nodig bij de eerste beurt. Parseracceptatie en stabiele beurt zijn aparte resultaten; effectieve wonderlijst en echte Labyrinthproductie blijven afzonderlijk te bewijzen.

## Korte echte laad-/beurtproef, 17:37 CET

Vijftien kandidaatbestanden tijdelijk geïnstalleerd met verse backups en hashgelijke c6ba-startalias. Eigen PID35152 startte 16:31:24UTC; nieuw gestart spel laadde werkelijk Rome1/4000BC. Eén vooraf geregistreerde n verwerkt naar zichtbaar3950BC; geen zichtbare parsefout. Geen extra beurt, onderzoekkeuze, editor- of productieaanpassing. Dit bewijst geslaagde start/load/eerste beurt met het pakket, geen onafhankelijk geïnstrumenteerde parse van iedere nieuwe partial of effectieve wonderlijst.

Normaal gesloten 16:37UTC, daarna 162 pins exact hersteld; acht eigen partials en alias verwijderd na hashcontrole. Gewijzigde autosave eerst apart bewaard. Root heeft volledige aidata118/save38-inventarissen onafhankelijk vergeleken: exact. Release eb6/c6ba-start intact, geen spel actief, pc aan. [Resultaat](../PROEVEN/wonders-runtime/20261028/ROOT-RESULT.json).

Nog open: effectieve Wonder_List, werkelijke Labyrinthqueue, onbouwbaar-geval en persoonlijkheidsherstel. Volgende noodzakelijke stap is uitsluitend die lijst/queue uitlezen via bestaande gebonden observatie; geen brede analyse of honderdbeurtenproef.

## Reviewcriteria

Acceptatie van C0 vereist zeven minimale FLI-diffs, acht nieuwe wonder-only AIPs, zeven exacte beforekopieën, exacte herstelblokken en de juiste laatste actionparen op alle zeven normale routes. Controleer ook dat alle andere huidige aidata, DLL en saves ongewijzigd zijn. De barbarenroute valt buiten de ingreep.

Statische syntax-, token- en categoriecontroles bewijzen geen echte spelparseracceptatie, effectieve runtimelijst of queue. De oude synthetische switch-/bouwdoelcontroles worden niet opnieuw uitgevoerd voor onveranderde enginebranches. Nieuwe kandidaat nog niet geïnstalleerd.

Doel 4 blijft open: runtime lijst/queue/onbouwbaarheid/herstel, wonderproductiestad en definitieve latere wonderkeuze ontbreken nog. Dit voorstel vervangt die volledige acceptatie niet.
