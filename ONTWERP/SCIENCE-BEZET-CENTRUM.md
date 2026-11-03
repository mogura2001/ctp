# SCI: actueel bezet centrum lokaal uitsluiten

19 oktober2026,20:25 Europe/Amsterdam. Fase B voor Doel1/1a/5, op roots geaccepteerde [A-overdracht](../ANALYSE/SCIENCE-BEZET-CENTRUM.md),5/5vragen. Ownership uitsluitend dit bestand inclusief voortgang; anderen/historie behouden. **BrongateFALSE; geen uitvoering.**

## Beslissing en technische ingreep

Kandidaat068f bewees op centrum `(28,73,0)` SCI_CENTER/branch10/cityhandle0/unitcount2: de eigen FoodReader weigert aanwezige units vóór voedselberekening. Dat wordt nu reason11/coverage0 en wholepass23, waardoor eerdere geldige sciencealternatieven geen selectie bereiken. Dit bewijst geen voedseltekort, unitbonus, eigenaar of illegale stichting.

Gewenst: uitsluitend deze **vers gebonden positieve unitcount** wordt tijdelijk `NO_NOW1/OCCUPIED_CENTER_SCOPE/coverage1`, zonder voedselcredit. Coverage betekent een volledig bepaalde conservatieve scope-uitsluiting, geen uitgevoerde voedselanalyse. De volgende pass beoordeelt opnieuw; geen blacklist/nativeplaatsingswijziging. Dit dient nuttige uitbreiding en scienceherkenning. Bestaande FLI/AIP-aansturing biedt geen afhandeling van deze private return; aanvullende lokale code is nodig, geen algemene modding-hook.

C maakt een nieuw eigen pakket op basis van `PROEVEN/science-foodreader-diagnostiek/20261019T194200`: kandidaat `068ff459a19125fdd08db060450110210ad992698d27b920894f4502ac4aae4f`, manifest `beebdb07abeb5bf111869e53f1c15dbb6466ece17808022276241d6ee4e28e44`. Parent en gedeelde H3/score/development blijven intact/bytegelijk. Nieuw candidate/manifest/buildpins/reader; geen extra unitdereferenties, gettercallbacks of budgetwijziging.

**Private ABI-wijziging:** SCI-clone retourneert0=UNKNOWN,1=geldige foodread,2=uitsluitend actueel gebonden bezet SCIcentrum. Alleen de centrumcaller mag2 ontvangen/afhandelen. Tilecalls/gedeelde/developmentreader blijven0/1.

- `food_diagnostic.py:FoodStage/emit_reader`: eigen frame-returnspill standaard0; succes blijft1. Alleen actuele branch10 mag spill2 zetten. Historische first-centerfailurelatch blijft diagnose en is nooit beslisbron. Geen extra causaalscratch nodig.
- Vlak vóór return2 valideert de clone opnieuw scope1/guard1, eigen owner/generation tegenover huidige Plan én snapshot, huidige prefix=`classified−1`, primaryordinal, callkindSCI_CENTER/isCenter1, actuele externe centrumxyz tegenover eigen invocatiestaging en geldig begrensde ORDER/CAPTUREbinding. Padding is geen coördinaat. Eis huidige branch10, reeds gelezen cityhandle0 en signedcount>0. Iedere mismatch/negatieve count geeft oorspronkelijke0. Gebruik uitsluitend eigen state en reeds gelezen operands; geen stale latchvelden.
- Behoud out40wipe op dit afwijzingspad. De clonefailure-epiloog laadt de gevalideerde returnspill na de wipe in EAX; oorspronkelijke0 mag2 niet alsnog overschrijven. Behoud stdcall20/ret20, frame/canaries, flags/GPR/nonvolatile/x87. Logginghistorie blijft onafhankelijk.
- `science_model.py:model`: onmiddellijk na **centrumcall** eerst `EAX==2` aftakken, daarna de bestaande0/1/foodverwerking. Lokale handler zet state1, nieuwe afzonderlijke reason `OCCUPIED_CENTER_SCOPE`, coverage1, selectedindices−1/certifiable_count0; food-/margevelden blijven ongebruikt. Ga via `science_done`, inclusief oorspronkelijke x87restore, nooit via foodconsumer. C legt de unieke numerieke reasontoewijzing in schema/manifest vast en controleert botsingsvrijheid vóór build. Andere returns volgen bestaande routes; tilecaller mag2 niet als food aanvaarden.
- `food_diagnostic_layout.py`, builder/pins en eigen readerdecode krijgen dit private contract/reason. `union.py` blijft inhoudelijk gelijk: coverage1/state!=2 geeft regulier geen sciencealternatief en gaat verder. Reader onderscheidt `SCOPE_EXCLUDED_OCCUPIED_CENTER` van voedselanalyse; geen currentfood0/marges als waarneming. Gcert/selectedevidence blijven apart en streng.

## Volgorde en beperkte verificatie

C-bron/diff → rootreview → bouwvrijgave → candidate/pins/readercontrole → beperkte nativevrijgave → rootreview/gebruikersuitleg → één host. Alleen gewijzigde gevallen via bestaande infra; geen oude69suite herhalen:

1. Exact centerbranch10/count>0: return2/out40zero, modelstate1/nieuwreason/coverage1/indices−1, geen foodconsumer.
2. Tilebranch10, branch9/andereguard, count<0, verkeerde callkind/owner/generation/prefix/ordinal/external/context:0/UNKNOWN. Count0 volgt normale reader, geen2.
3. Twee opeenvolgende bezette centra, daarna een andere failure: ieder actueel geval correct, historische latch maskeert niets.
4. Normale0/1/out40/ret20/flags/GPR/x87 en callbackaantal behouden; callerinventaris sluit consumptie van2 elders uit. SCI0key-/margeberekening en shared/developmentbytes behouden; nieuwe reason uniek. Whole-diff verklaard, alle imports/pins exact.

## Eén proef en acceptatie

Nieuwe gate/verse budgetruimte/cd/count0/pins/29versebackups. Zelfde vasteT0 SHA256 `8c34364200e539870e0dea0790c98d7441925f52267d24cf0e0adb152141ad26`, zeven normale AI's/Deity/passieve mens; maximaal één vooraf verbruikt n-token, stabiel dubbelT0/T1, dezelfde procesidentiteit en zeven ronden−1→0. Geen extra arm/beurt.

Bewezen finite startshellmonitor45/90/135/180s vanaf originele processtart, PID/creation/window/screenshot+trace; Sleep<=45s/poll<=50s, laatste frame<=195/menu<=210 visueel bewezen. Geen automatische actiekeuze/klokreset. Werk600/sluitverzoek690/einde720s. Stop bij fout of volgende wholepassfailure na veilige uitlezing. Budgetweek<=10/vijf<=5: projectstop/checkpoint, pcaan.

Meet lokaal centrum3reason/coverage/geenfood; voortgang classified>4 indien geen volgende echte fout; SCI0keys `(27,45,0)/(29,42,0)/(27,43,0)/(28,42,0)`, stand−1/R0,75/marges35/30/25 behouden. Rapporteer reason/context/slots/Gcert/selected apart. Andere echte fout gaat gericht terug naar A; geen automatische skip. Geen30stedenclaim; extra vraag vraagt afzonderlijk Gcert>Dorig/nuttig tekort.

Normaalclose eigen PID/count0; herstel29verse hashes/Doel3releaseDLLeb6f, defaultautosave terug na dubbele archivering nieuwe autosave; eerdere archieven behouden. Alleen eigen bytegelijke alias weg/gateFALSE. Geen overschrijven bij mismatch/forcekill/herstel onder liveproces; checkpoint bij open herstel. Pcaan.

Effect: eerdere geldige alternatieven kunnen selectie bereiken. Onzeker: latere fouten/bronconflicten en werkelijk Gcert. Tijdelijk bezette goede locaties worden conservatief uitgesteld. Volledige unitvrije voedselondersteuning vraagt eigen A/B; blanketUNKNOWNskip of nativefood met unitbonus is geen alternatief binnen dit voorstel. Combinatie-effecten/native stichting vereisen latere afzonderlijke proef.

## Voortgang

20:24 gestart; vijf10%/week74%,bron9,9s oud. 20:25 B gereed voor rootreview; uitsluitend dit bestand, geen code/tests/game. Nacontrole20:25:08: vijf9%/week74%,bron14,3s oud, geen stopgrens. Doel1/1a/5 technisch/gameplay open; Doel3 behouden. Volgende oplevering uitsluitend C-bronvoorbereiding na vrijgave; brongateFALSE. Ontwerper stopt na overdracht; geen achtergrondwerk actief.
