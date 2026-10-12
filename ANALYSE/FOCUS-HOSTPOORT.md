# Focus als poort naar hostobservatie

Gerichte fase A, 10 oktober 2026, 12:08 Europe/Amsterdam. Tussendoel **wijzigingen daadwerkelijk actief**, voorwaarde voor H1-I/H3. Alleen F1/F2 onderzocht; brede analyse blijft afgerond. Ownership uitsluitend dit bestand en VOORTGANG-ANALIST-FOCUS.md. Geen spelstart, proces-/focusmutatie, input, capture, livegeheugenlezing of gamewijziging uitgevoerd.

**F1 en F2 zijn voldoende beantwoord voor B.** De actuele ontbrekende schakel is een betrouwbare gelegenheid om het exact gebonden proefvenster in foreground te observeren. De eerdere fout bewijst een geweigerde focusaanvraag, geen crash of defect menu. Er is geen onderbouwde garantie voor automatisch focusherstel. De kleinste route hergebruikt de bestaande opname en harde focuscontrole; zo nodig stelt de gebruiker één keer zelf het proefvenster voorop. Een beperkte Capture-wachtstand kan die gelegenheid betrouwbaar afbakenen zonder focus te forceren. Dit is een ontwerpbare route, nog geen toegepaste toolwijziging of runtimebewijs.

## Dekkingsmatrix

| Vraag / beslisschakel | Huidige werking en bewijs | Concrete route / voorwaarden | Restgrens |
| --- | --- | --- | --- |
| F1: proces → hoofdvenster | Bedien-CTP selecteert precies één civctp op het absolute proefpad; Refresh levert MainWindowHandle. Historische Status noemt PID20536, handle330040, titel CivCTP, Responding=True; resultaat meldt visible=True. | Behoud exacte proefpadcontrole; bind een toekomstige start aan eigen PID/CreationDate en hercontroleer voor opname. | Status bewijst geen menutekening. Numerieke handle/foregroundwaarde op het afzonderlijke Capture-moment niet vastgelegd. |
| F1: hoofdvenster → focusaanvraag | Regels96–98: niet-nul handle; bij GetForegroundWindow()!=handle volgt SetForegroundWindow(handle). Bewaarde fout is exact de false-tak op98. | Focusguard behouden; documenteer aanvraagresultaat afzonderlijk van waargenomen foreground. | Waarom Windows weigerde is niet gemeten; foreground-PID/desktop/lock/menucondities ontbreken. |
| F1: focus → schermpixels | Pas na98 volgen350ms wachten, nieuwe foregroundvergelijking op101, bounds op103 en CopyFromScreen op111. | Alleen opnemen als het eigen hoofdvenster werkelijk foreground is en positieve actuele bounds heeft; opname daadwerkelijk inspecteren. | Deze stappen zijn in de mislukte Capture niet bereikt. Geen nieuw beeld; oude capture is geen menubewijs. |
| F2: gelegenheid → herkenbaar menu | Bestaande Capture slaat SetForegroundWindow over als de eigen handle al foreground is. Start opent een normaal zichtbaar venster; huidige automatische focusuitkomst onbekend. | B kan één originele start met een Capture-only gelegenheid ontwerpen: bestaande methode, eventueel begrensd alleen-lezen wachten op foreground; zo nodig één vooraf afgestemde gebruikerfocus. | Geen gegarandeerde automatische focusroute, geen nieuwe runtimeproef in A. Zonder gemeten focus of herkenbaar beeld blijft NOT_OBSERVABLE. |
| F2: menupass → H1-I/H3 | Bestaande host- en H3-voorstellen scheiden menu, afwikkeling, geladen bytes, T0 en echte AI-pass. | Eerst originele menucontrole/afwikkeling reviewen; daarna afzonderlijke H1-I-hostcontrole, daarna bestaande H3-activatieprocedure. | Menu opent alleen de hostpoort; AI-activatie, nieuwe goals, ordening, overhead en gameplay blijven afzonderlijk open. |

## F1 — exacte codegate en bewijssoort

Bron: [Bedien-CTP.ps1](../PROEVEN/Bedien-CTP.ps1), op deze analyse gemeten SHA256 `3594e4f32b26265cfc3fa900fcd61f245656940929968b231b19315a734b5f1d`, gelijk aan eerdere C-pin. Relevante volgorde:

```text
96  nul MainWindowHandle -> stoppen
97  foreground != MainWindowHandle ?
98    SetForegroundWindow false -> "Unable to foreground the game window."
100  wacht350ms
101  foreground != MainWindowHandle -> "Game is not foreground; refusing input/capture."
103  GetWindowRect moet slagen
107  breedte/hoogte moeten positief zijn
111  Graphics.CopyFromScreen(...)
113  bitmap.Save(.../automatisering/ctp-window.png)
```

Dit is **bestandsfeit**, geen analyse van enginecode. [Capture-fout](../PROEVEN/hoststart-controle/2026-10-09/original-menu/capture-error.txt), [Status](../PROEVEN/hoststart-controle/2026-10-09/original-menu/status-01.txt) en [C-resultaat](../PROEVEN/hoststart-controle/2026-10-09/original-menu/RESULTATEN.md) zijn **historische runtimewaarnemingen**: op de Capture-aanvraag was de helper door96 gekomen, de eerste foregroundvergelijking ongelijk en SetForegroundWindow false. Hij stopte vóór hercontrole, bounds of opname. De Status-handle330040 is de laatst vastgelegde handle, niet een afzonderlijk gelogde waarde binnen Capture. Geen input verzonden, geen nieuwe screenshot verkregen. Titel/Responding/zichtbaarheid en een mislukte focusaanvraag bewijzen geen menupass, crash of H1-causaliteit.

Microsoft beschrijft dat [SetForegroundWindow](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow) bij geweigerde activatie nul retourneert. Windows beperkt welke processen dit mogen; zelfs voldoen aan de beschreven voorwaarden garandeert geen toestemming. Onder meer foreground-/laatste-inputrelatie, actieve menu's en een foregroundlock kunnen relevant zijn. Dit verklaart **mogelijke mechanismen**, niet de historische oorzaak. Geen specifieke lock, andere app, UAC, sessie of desktop gemeten. De API-documentatie levert hier geen concrete foutoorzaak uit alleen bool=false; de bestaande import bewaart ook geen SetLastError. Geen achteraf geconstrueerde Win32-foutcode als diagnose gebruiken.

[GetForegroundWindow](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getforegroundwindow) geeft de actuele foregroundhandle, die tijdens activatieverlies tijdelijk nul kan zijn. Daarom kan een ongelijkheidsmeting zonder opgeslagen handle geen andere app identificeren. [CopyFromScreen](https://learn.microsoft.com/en-us/dotnet/api/system.drawing.graphics.copyfromscreen?view=windowsdesktop-9.0) kopieert schermpixels; het is geen achtergrondvensterrenderer. Focusguard verwijderen maakt deze opname niet tot bewezen CTP-menubewijs.

Huidige afwikkelgrens is al opgelost: [10okt-C](../PROEVEN/hoststart-controle/2026-10-09/original-menu/close-mainwindow/RESULTATEN.md) meet buiten sandbox PID20536 afwezig, nul sluitaanvragen,15pins/profiel gelijk. Root heeft dit geaccepteerd. Dit bewijs geldt uitsluitend die oude PID op dat moment; vóór iedere toekomstige start blijft een verse succesvolle alle-civctp-procespoort vereist. Historische verdwijningsoorzaak is geen blocker voor dit ontwerp.

## F2 — minimale overdraagbare route

**Ingreeppunt:** uitsluitend het Capture-pad rondom regels96–103 van de bestaande bediening. De opname zelf, huidige executablecontrole en harde foregroundvoorwaarde blijven bruikbaar. Is de gebruiker vóór Capture klaar met focussen en blijft het venster voorop, dan kan de huidige tool al werken zonder nieuwe focusaanvraag. Om timing zonder extra UI-interactie tussen focus en opname te laten werken, kan B een kleine expliciete Capture-only wachtoptie uitwerken. Geen implementatie gemaakt in A.

Benodigde ontwerpvoorwaarden voor zo'n optie:

1. Een begrensde gelegenheid met alleen bestaande GetForegroundWindow/vensteridentiteit-reads. Geen SetForegroundWindow, keys, clicks of manipulatie van andere vensters in deze wachtmodus; geen loops die foreground proberen af te dwingen. Harde deadline en korte wachtstappen, geen achtergrondmonitor. Alleen de aan deze ene start gebonden PID/CreationDate/proefpad/hoofdvenster accepteren; verdwijnen, gewijzigde identiteit of queryfout stopt. Geen onbegrensde herbinding aan een andere civctp.
2. Als de gewone start zelf foreground oplevert, kan deze gelegenheid direct slagen. Anders moet B/root **vooraf** concreet uitleggen dat de gebruiker éénmaal het werkelijk zichtbare eigen CTP-proefvenster voorop zet en dat daar geen spelklik/toets of instellingenwijziging bij hoort. Alleen een automatische foregroundmeting sluit de wachtpoort; een bericht 'gefocust' is geen API-bewijs. Niet wachten op een onbevestigde nieuwe start/focusactie tijdens A. Is gebruikerfocus niet beschikbaar of niet gelukt binnen het venster: NOT_OBSERVABLE, geen tweede start of focusworkaround.
3. Na waargenomen juiste foreground de bestaande350ms-hercontrole behouden, dan actuele handle/eigenaar/bounds opnieuw valideren en onmiddellijk de bestaande CopyFromScreen uitvoeren. Voor en na opname foreground vastleggen; bij verschil opname verwerpen als betrouwbaar menubewijs. Dit begrenst maar elimineert de race niet: herkenbaar normaal menu in de actuele opname blijft de acceptatievoorwaarde. Zwart, vreemd scherm of dialoog krijgt een concrete eigen uitkomst; geen achtergrondopname als fallback.
4. Bewaar in het bestaande unieke C-resultaatpad de startbinding, wachtbegin/deadline, foregroundmetingen en eigen handle, bounds, opname-/fouttijd en screenshot. Geen andere-appinhoud verzamelen om de weigering te verklaren. Bewaar een bestaand vast screenshot vooraf zoals eerder en kopieer de nieuwe opname direct naar uniek bewijs; geen nieuw screenshotframework.

B kiest een korte totale observatiegrens en legt afwikkeling afzonderlijk vast. B/C moet bestaande [HOSTSTART-CONTROLE](../ONTWERP/HOSTSTART-CONTROLE.md) aanpassen aan deze **nieuwe** poging/route: eerdere C is gesloten en haar focusweigering is geen retryvenster. Houd originele DLL/15pins, B1, profiel/CD/compat/display en normale start vast; nieuwe toolhash/diff expliciet reviewen als de wachtoptie wordt toegevoegd. Vóór C budget en actuele procespoort controleren buiten sandbox met expliciete foutafhandeling. Deze analyse had geen actuele proces-/desktopmetadata nodig en heeft die niet bevraagd.

Normale zichtbare menu-exit kan alleen met nieuwe herkenbare actuele opname/focus en bekende cursor; anders volgt eigen PIDgebonden afwikkelhandoff. Geen nieuwe installatie/start zolang oude instantie open/onbekend is. Het bestaande beperkte afwikkelvoorstel kan B concreet herbindbaar uitwerken voor de nieuwe eigen instantie; nooit PID20536 als nieuwe target hergebruiken.

Na `MENU_PASS` plus bevestigde afwikkeling: rootreview → apart H1-I-menuvoorstel met dezelfde bekende inputs/verse voorafstate/herstel → bij hostacceptatie de bestaande [H3-activatieprocedure](../ONTWERP/ACTIVATIECONTROLE-H3.md). Eén originele menupass verklaart de oude H1-I-crash niet. Menu bewijst geen geladen kandidaatbytes, T0, scorecallback, Q/B, heap of echte passtijd; B2/B4 blijven buiten deze route.

## Acceptatie en hervatpunt

| Tussendoel | Geboekte voortgang deze A | Acceptatie / open | Volgende concrete oplevering |
| --- | --- | --- | --- |
| Wijzigingen daadwerkelijk actief / hostpoort | F1/F2 afgerond: exacte gate, bewijsgrenzen en beperkte route bepaald | Analyse gereed voor B; originele menu-/AI-acceptatie open | B werkt één originele menucontrole uit, inclusief Capture-gelegenheid, eventuele eenmalige gebruikerfocus, meetlat en afwikkeling. |
| Goede locaties kiezen / H3 | Hostvoorwaarde verduidelijkt; geen nieuwe gameplaydelta | Bestaande offlineacceptatie geldig; runtime/gameplay open | Na hostreview afzonderlijk H1-I en H3 volgens bestaande overdrachten. |

Niet-blokkerende backlog: historische foregroundhandle/oorzaak, effectieve desktop/lockcondities, waarom oude PID verdween. Geen brede crash/init/UAC-reconstructie, nieuwe emulatie of extra focus-APIprobes nodig voor B. Alleen terug naar A bij een nieuw benoemd resultaat dat de concrete route werkelijk blokkeert.

Analist stopt na overdracht; geen spel/helper/achtergrondrun actief vanuit deze opdracht. Laatste budgetcontrole12:06:43, bron12:06:24, leeftijd19s: week98%, vijfuur85%, state ok; geen stopreden. Nieuwe eenmalige afsluitopdracht uitsluitend root; deze agent heeft geen shutdown/helper/planning uitgevoerd. PROJECTSTATUS.md blijft rootownership.
