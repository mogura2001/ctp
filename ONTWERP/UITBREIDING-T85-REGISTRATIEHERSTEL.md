# T85: eenmalig herstel van registratie vóór invoer
22 oktober 2026, 17:02 Europe/Amsterdam. Fase B; alleen ontwerp, geen code/RPM/input. Eindige aanvulling op de langere kandidaatproef; Doel1/1a blijven OPEN.
1. Oorzaak volgens rootbewijs: Pass85 faalde op Set-Content van host/start.json ná exclusieve T85-token maar vóór Budget/OwnState/Key; de token is geen bewijs van verzonden n.
2. Behoud de oorspronkelijke helper, bronpins en mislukte T85-consumed.json ongewijzigd. Nieuwe afzonderlijke helperkopie krijgt eigen hash/pins en rootreview vóór enige invoer.
3. Deze operationele uitzondering geldt uitsluitend Turn85, kandidaat U30-40, PID40488/creationFILETIME134371535950250712 en dezelfde eigen host/venster/run-id. Geen algemene retryroute.
4. Packagepad wordt expliciet aan het bestaande ouderpakket gebonden; start.json uitsluitend het reeds gebruikte exacte eigen hostpad. Geen afgeleid willekeurig pad of nieuwe processelectie.
5. Voor toelating: volledige oorspronkelijke bron-/binary-/module-/proces-/venster-/budget-/deadlineguards; originele T84 geaccepteerd; originele foutlocatie/log bewijst dat Key niet bereikt werd.
6. Eis bewaarde T84-preinput-recheck.json met exact dezelfde state/instance als T84, alle zeven native83, start.n_consumed84, en afwezigheid van T85-n.txt én geaccepteerde T85.json. Laat root dit vóór helpervrijgave bevestigen.
7. Ontbrekende n-log alleen volstaat niet. Iedere tegenstrijdigheid, onbekende invoerstatus of veranderde ronde stopt zonder n; deze uitzondering verleent geen toestemming voor ambiguë invoerretry.
8. Maak exclusief één afzonderlijk T85-herstel-token via CreateNew; bind run/PID/creation, originele mislukte-tokenhash, T84- en recheckhash. Hergebruik of verwijder de oude T85-token niet.
9. Registreer n_consumed85 vóór Key: serialiseer het verder ongewijzigde startrecord naar een unieke eigen tijdelijke sibling; flush/sluit, dan atomaire File.Replace naar exact host/start.json.
10. Maximaal vier metadata-IO-herkansingen met100ms tussenruimte; uitsluitend IOException en alleen zolang vaststaat dat bestemming nog de verwachte oude inhoud heeft en de eigen bron intact is. Geen invoerherkansing.
11. Niet-IO-fout, onduidelijke Replace-uitkomst, onverwachte inhoud of uitgeputte herkansingen: fataal stoppen vóór Key, bewijs/tokens/temp bewaren; geen rollback bij ambiguïteit.
12. Lees na bewezen Replace de exacte bestemming terug: inhoud gelijk aan verwachte start met n_consumed85; controleer opnieuw verse budget-/OwnState-/pins-/window-/tijdguards. Een hierna falende guard verbruikt herstel-token definitief.
13. Daarna exact één gewone bestaande Key -Keys n zonder Captureflags. Volg exact bestaande30s-poll, stabiele tweevoudige toestand, alle zeven ronden83→84 en huidige matching/pins. Geen extra Key, herstart of herstel-token bij fout.
14. Succes is uitsluitend een volgens bestaande guards geaccepteerde T85.json/pass met zeven native84. Bewaar originele fout, beide tokens, atomaire registratielog en helperhash als afwijkingsbewijs.
15. Alleen na dat succes mogen T86..T100 weer de oorspronkelijke ongewijzigde Pass volgen. Bij mislukking: geen automatische T100-herstart; root bewaart laatst geldige toestand en volgt bestaande normale afsluit-/herstelroute.
16. Bestaande100beurten-/4500s-/geen-n-vanaf4380s-grenzen blijven; tijd gaat niet opnieuw lopen. Budget week<=10%/vijfuur<=5% stopt, week<=25% waarschuwt; unknown/stale eenmaal herlezen, daarna stoppen.
17. De proef bevat dan één extra consumptiemarker door bewezen vóór-invoerregistratiefout; rapporteer100 geslaagde natuurlijke beurtstappen alleen bij daadwerkelijk bewijs, nooit “vlekkeloos100tokens”.
18. Verwacht effect: dezelfde natuurlijke T85 alsnog mogelijk zonder tweede n. Neveneffect: extra operationele afwijking; geen wijziging van AI of meetlat. Alternatief stoppen is geldig; volledige herstart is voor deze lokale fout niet nodig.
19. Rootreview van bewijs/helperdiff/pins is de laatste poort vóór uitvoering; voorstel zelf is geen livevrijgave. Herstel van spelbestanden/autosave alleen volgens bestaand plan na bewezen procesexit; pc blijft aan.
20. B-vragen exact85scope, atomaire metadata, geldigheidsbewijs en uitkomst zijn beantwoord. Ontwerper draagt over en stopt; geen achtergrondwerk.
