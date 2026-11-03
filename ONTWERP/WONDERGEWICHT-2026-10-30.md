# Labyrinth boven vroege unitbiedingen: afzonderlijke gewichtsproef

30 oktober 2026. Fase B voor Doel4 en de toegestane Labyrinthvrijstelling uit PROJECTDOELEN.md/LOCATIESELECTIE.md. Analyse overgedragen; rootreview/uitleg vereist voor C.

## Huidige en gewenste beslissing

[C3](../PROEVEN/WONDERBOUW-ROOT-PAIR-2026-10-30.json) bewijst zeven gewone AI-beurten, 47 naar49steden en nul Labyrinthqueues. Drie vooraf kansrijke steden vernieuwden hun queue; de Portugese stad behoudt daarna rangTRUE/bouwtijd41. Dit ontkracht een algemeen productiegebrek, maar onderscheidt doelcreatie, concurrentie en toelating niet.

[A](../ANALYSE/WONDERBOUW-VERVOLG-2026-10-29.md) bewijst de gewichtsroute: defaultwonderbasis19997500+9100=20006600 tegenover primary-landsettler20010500. Gewenst: een geschikte stad kan Labyrinth voorrang geven boven vroege unitproductie, terwijl andere steden uitbreiden. De driebergendefinitie en precies een wonderbouwer worden hiermee nog niet gerealiseerd.

## Exacte ingreep en onderbouwing

Maak een apart pakket op basis van wonders-2026-10-28. Wijzig uitsluitend `opening_wonders.aip`: Labyrinthgewicht **9100.0 naar30000.0**. De overige14kandidaatbestanden blijven bytegelijk; eigen manifest/diff/pins en herstelkopie. Persoonlijke herstellijsten behouden hun bestaande gewichten. Geen quota, limiet, threshold, DLL, technologie of regel wijzigen.

30000 is een proefwaarde: defaultwonderbod20027500 ligt2500boven Scout_Primary20025000 en7000boven masssettle_sandbag-landsettler20020500; defaultlandsettler ligt17000lager. Deze gewichten staan in default.aip/masssettle_sandbag.aip.15000 zou de twee eerstgenoemde concurrenten niet passeren. Dit bewijst geen actuele universele biedingsvolgorde of dat prioriteit de gemeten oorzaak is. Verwacht effect: bestaande wonderdoelen concurreren sterker, mits alle overige voorwaarden slagen.

## Minimale meting en afhankelijkheden

Behoud C1/C2/C3 en hun bewijsbestanden bytegelijk. Maak alleen een aparte C4-compositie: bind de geladen C1-modulevariabele WONDERS aan het nieuwe volledig gepinde pakket. Behoud de volledige tekstinventariscontrole en alle bron-/proces-/module-/codevenster-/owner-/handlecontroles, VM_READ en dubbele complete stabiele samples; geen atomiciteitsclaim. C3.HERE wordt de eigen map; C3.BASE blijft C2. Via C3.load_base/C2.load_base wordt alleen C1.WONDERS herbonden. Eigen pins omvatten alle oorspronkelijke70bronpins plus nieuwe pakket-/wrapperbestanden; bindingvensters/participants zijn hashgelijke kopie?n. Voeg uitsluitend een30000-lijstexpectation toe binnen dezelfde samples. De oude9100-metadataexpectation mag herkenbaar FAIL blijven: dat is historische metadata, geen validatiefout. Geen hash overslaan of oude verwachte bytes wijzigen.

C0: controleer exact de ene numerieke diff, pakketpins en dat een onverwachte tekstafwijking wordt geweigerd. Geen nieuw readerframework of nieuwe memoryvelden nodig.

## Succes, risico en herstel

Controle is de bewaarde9100-C3-run. Kandidaat: dezelfde9280c97a-archiefsave, eb6, deelnemers en mensprotocol; verse host, cd/focuscontrole, voorlezing, maximaal1n, native25naar26. Vereis effectieve30000-lijst bij7/7. Positief: minstens een nieuwe echte klasse9/type2 op dezelfde eigenaar/volledigehandle, vooraf nergens in die stadsqueue, stabiel plus CityStatus. Geen voltooiingsclaim. Vergelijk ook stadsaantallen en nieuwe wonderqueues per civ.

Risico: verdrongen defensie/settlers, meerdere wonderbouwers en uitbreidingvertraging; gedeelde state garandeert geen enkele bouwer. Dit is geen releaseacceptatie of bewijs van langetermijnwinst. Negatief: geen verdere gewichtsverhogingsreeks; richt vervolg op doelcreatie/toelating. Meerqueuegedrag vraagt later herhaling/gecombineerde benchmark. Alternatief15000 geeft een smallere defaultproef met bekende hogere concurrenten.

Normaal sluiten binnen15min/vanaf13min afwikkelen; count0, autosave archiveren en162pins/118aidata/38saves exact herstellen. CTP-og blijft intact; pc aan. VolledigeDoel4 OPEN.
