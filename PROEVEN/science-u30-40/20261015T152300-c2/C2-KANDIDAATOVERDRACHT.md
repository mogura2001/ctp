# C2 kandidaat — alleen gebouwd en statisch gecontroleerd

15 oktober 2026, 19:40 Europe/Amsterdam. Rootbronreview b52b6c... en build-onlygate vooraf gecontroleerd; native/game FALSE. Verse startbudgetbron10,8s: vijf40/week75/stateOK. Bestaande build_candidate.py precies eenmaal uitgevoerd: exit0, interne doublecompose bytes/payload/manifest gelijk. Bestaande check_candidate.py precies eenmaal: exit0. Geen rebuild/correctie nodig.

Kandidaat `U30-40.prepared.dll` SHA256 `18d8516bf915d137acbc679c695bf4163540d01007888d875da24183035b230d`.
Manifest `candidate-manifest.json` SHA256 `265b5ee53bcc5adc4216f0df2471b45b95c41d2d3e5d8121cf8fb78eea888167`.
Payload SHA256 `7791c54f569d4e7959cb01e3e288464530055ca4450152cd4e70ccc7cc1ed0e3`.

Checker bewijst binnen deze offline scope: volledige diff reconstrueert kandidaat;80 oorspronkelijke gewijzigdebytes alleen verklaarde hooks/headers;540160toegevoegdebytes;0onverklaard. Oude sectieheaders behouden en wijzigingen in oude secties alleen benoemdehooks. B2payload/d4000/vijfB2hooks exact; bestaande relocatiedirectory/HIGHLOW ongewijzigd; checksum geldig.6587instructies buildergedecodeerd;1409directe branches checkerbeoordeeld, eigen targets op instructiestarts. Geen ABI-/loader-/engine-PASS hieruit afleiden.

Concrete layout: interneH3 RVA d6000; extensie d9000. Nieuwe RXsectie .u40c RVA d6000/virtual41593/raw41984; eindevirtual e0279. Nieuwe RWsectie .u40s RVA e1000/virtual0x79804/raw498176; volledignul. Pass e1000, generation15a800. Result/ALT/scratch volgens Planrelatief54800/74800/78800/eind79800, niet overlappend met bestaande arrays/pathcache. SCI dd310, development dfd04, location_roles dc328, postSCIcontext dc738, eindcontext dc9fe; alle code- en guardlabels gecontroleerd binnenRX/op instructiestarts.

De20correctiecheckpointpins zijn opnieuw gecontroleerd met uitsluitend de verwachte door root gewijzigde buildgate als uitzondering. Alle historische source-diffs bytegelijk; nieuwe kandidaatsourcediffs hebben aparte namen. `build-only-results.json` bevat alle concrete checks/secties/labels; `candidate-manifest.json` bevat volledige diff/recipe/pins en C1manifest-/C2voorstelbinding. `build-only-package.json` pint de bron-/kandidaatartefacten voor root.

**Bestaande beperking:** deze C2 bevat nog de oorspronkelijke resolve_type-enginecount+1-guard. De nieuwe parsercorrectie wordt volgens rootsopdracht in een afzonderlijk pakket voorbereid; zij is niet stil gecombineerd. Dit pakket is dus geen vrijgegeven werkelijkehostversie. Nieuwe callers/positieveunion moeten na rootkandidaatreview nog met de beperkte gewijzigde B4–7cases worden getoetst; nativecompile/calls zijn nu0. Geen installatie/RPM/GUI/game/spelwijziging.29C1cases blijven deelbewijs en centrum64 PENDING. Doel1/1a/5 en Doel3combinatiebehoud blijven onvoltooid/onbewezen door deze build. Deze buildrol stopt bij overdracht; pcaan.
