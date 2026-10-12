# B2c-header C1: correctietekst voorbereid

11 oktober 2026, 16:39 Europe/Amsterdam. **PREPARED_STATIC_ONLY_NOT_INSTALLED_NOT_NATIVE_TESTED**. C1 afgerond; uitvoerder stopt voor rootreview. Geen C2/helper/native/parser/gameactie uitgevoerd. Bestaande andere CTP-installatie ongemoeid gelaten.

Overgedragen addendum ONTWERP/B2C-HEADER-EN-PARSER.md SHA256 333f90383c016c5811fd0f5a101a34ded2b875194b48898c7b16e58b0b96bf0a. Bevroren B2-voorstel ea5140b5505c11f457bdcdc3cf41fcc023e277bf247866228ad356919c9ef40e ongewijzigd. Directe tekstbron: PROEVEN/opening-b2/onderzoek-b2c/20261011T155803, manifest 017c57960864d7675f4b7ae500007f0b24e104e19ca917a272d9ed54c5af183a.

Alle negentien kandidaten naar candidate/ gekopieerd. Alleen de acht research-AIPs kregen exact ASCII `#include "aipdef.h"` plus CRLF als prefix: 21 bytes, geen BOM. Elk bestand is nu 2887 bytes; na strippen zijn de oorspronkelijke 2866 bytes exact gelijk. Iedere route behoudt alle 98 geordende advance-namen en exact haar gepinde broncategorierange/hash. Elf overige bestanden bytegelijk. candidate.diff volledig gelezen: uitsluitend acht ingevoegde include-regels.

staging/AIPs/aipdef.h bevat de exacte headerkopie uit CTP-proef, 1846 bytes, SHA256 26dc25bc4f086ad6e355323fc8818680a1d81531148b6b41710c12d6571a2f47. Deze stagingkopie is een afhankelijkheid; geen gameplaybeleid of installatie. category-blocks.json en routing.json zijn bytegelijk uit het oude pakket gekopieerd. Routering niet opnieuw geanalyseerd of als runtime bewezen.

Bronbescherming hergebruikt de bestaande 118 bronpins en voegt alleen de direct betrokken oude pakketbestanden, acht B1-broncategorieën/header en beide voorstellen toe: 168 unieke beschermde bestanden, voor/na gelijk. protected-before.json en protected-after.json binden de bytes. Geen oorspronkelijke header, oude kandidaat, engine, DLL, FLI of save gewijzigd. Geen herstel nodig; rollback is dit pakket niet installeren.

Reviewpins:

- manifest.json: af3a9a5ccb0f2bdc725e501aa41c7b83ae8997817ff4fc383a4e6a17361d5798
- candidate.diff: 7aaa12c8b127ff092a8be022cb80e252be6e5a3eb5fe5ffebd89f7f540421f6a
- static-checks.json: ee155eabb32a2b0220a1bae1e9eca83d991dfee2ab0de2c934ae75490adba1aa

Dit bewijst alleen de beschreven prefixcorrectie, categoriebehoud en bronbescherming. Echte parseracceptatie, Switch_AIP, FLI-actions, onderzoekkeuzes en gameplayverbetering blijven open. Volgende concrete oplevering: rootreview van C1; pas na afzonderlijke overdracht C2-helperbron zonder uitvoering.

Budgetvooraf 16:37:33: bron 4.8s oud, week89/vijf27, stateok. Eindstand staat in budget-end.json. Geen budgetstop of pc-afsluiting; werk stopt vanwege de afgesproken C1-reviewpoort.
