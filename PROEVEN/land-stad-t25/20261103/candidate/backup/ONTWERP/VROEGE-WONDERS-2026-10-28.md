# Alleen Labyrinth tijdens de opening

B voor Doel4, na geaccepteerde [A3/3](../ANALYSE/VROEGE-WONDERS-INGREEP-2026-10-27.md). Rootreview/uitleg vóór C. Actuele zeven routes/lijsten gelezen; niets toegepast.

Huidig: persoonlijke Wonder_List bevat onder andere Stonehenge/Sphinx vóór Labyrinth. Aanwezige categorieën vervangen elkaar; laatste uitgevoerde schrijver wint. Gewenst: tijdens opening uitsluitend Labyrinth als nieuwe wonderlijstkandidaat, daarna volledige eigen lijst. Dit benut bestaande FLI/AIP; geen aanvullende logica, DLL- of spelregelwijziging.

Maak onder `CTP-proef/ctp_data/default/aidata/AIPs/` **opening_wonders.aip**:

```text
#include "aipdef.h"
Building_Build_List_Element Wonder_List[MAX_ELEMENTS];
#DATA
"WONDER_LABRYINTH_OF_THE_MINOTAUR", 9100.0;
#END_DATA
```

9100.0 is het bestaande default-Labyrinthgewicht, geen nieuwe optimale schatting. Categorieprioriteit, wonderthreshold, bouwtijd/admission blijven intact; dit garandeert geen productie. Alleen vooraan zetten of gewicht0 sluit alternatieve wonders niet uit.

Maak daarnaast **opening_restore_wonders_P.aip**, P exact `default`, `cleric`, `slaver`, `scifew`, `scimany`, `milfew`, `milmany`: dezelfde include, gevolgd door het volledige oorspronkelijke blok van `Building_Build_List_Element Wonder_List[MAX_ELEMENTS];` tot en met diens `#END_DATA` uit `P.aip`, bytegelijk inclusief volgorde/gewichten/comments. Geen andere declaraties.

Voeg onderstaande twee acties als laatste actieve statements vóór de sluitende beginturnbrace toe; bij zes routes na `#include "aiploader.fli"`, bij default na bestaande actieve includes zonder diens uitgeschakelde loader te activeren:

```text
action load("opening_restore_wonders_P.aip") when (opening_required < 0.5)
action load("opening_wonders.aip") when (opening_required > 0.5)
```

| Exact beginturnbestand | P |
| --- | --- |
| beginturn.fli | default |
| beginturnCleric.fli | cleric |
| beginturnSlaver.fli | slaver |
| beginturnSciFew.fli | scifew |
| beginturnSciMany.fli | scimany |
| beginturnWarFew.fli | milfew |
| beginturnWarMany.fli | milmany |

B2-N30 levert bestaande opening_required: opening eindigt via opgeslagen latch bij minstens30steden én actieveTheocracy. Geen nieuwe beurtgrens/reactivering ontwerpen. Barbarian blijft ongemoeid. Alle nieuwe partials moeten vóór manageropbouw beschikbaar zijn; gewone saveload bewijst geen diskrefresh. B2c-researchpartials zijn niet geïnstalleerd en worden niet toegevoegd. Bestaande queued wonders worden niet geannuleerd.

**Volgorde:** C0 maakt uitsluitend `VERSIES/wonders-2026-10-28/`: candidate met7 gewijzigde beginturns/8 nieuwe AIPs, exacte backups, manifest met relatieve paden/size/SHA256/beforehash/vooraf-afwezig, broncategoriehashes/headerpin, volledige diff en resultaten. Statische controles: echte tokens/header/declaratie/#DATA,7 exact gekopieerde herstelblokken, slechts Wonder_List aanwezig,7 juiste laatste actionparen, barbarian en alle overige categorieën/research/units/regering behouden. Geen live-installatie; oude synthetische33controles zijn geen parser-/queuebewijs en hoeven niet opnieuw.

Daarna afzonderlijke korte C-proef: verse spelstart voor parseracceptatie/geen parsefouten plus effectief lijstbewijs; in gepinde wegwerpsave met lege queue en geschikte bouwstad controleren: opening→precies1Labyrinth-entry; bouwbaar→echte CityStatus-Labyrinthproductie; onbouwbaar→geen alternatief wonder; opening_completed→exact eigen lijst. Geschikte bouwstad voldoet aan wonder-rangthreshold of bewezen opslaguitzondering én bouwtijd/admission; een gewone eenstadstart voldoet niet automatisch. Geen100beurtenvoorwaarde. Elk ontbrekend bewijs blijft OPEN; geen nieuw uitleesframework.

Gelijke benchmarkstart/versiepins/mensprotocol voor controle en kandidaat; uitsluitend deze factor verschilt. Minder wonderkeuze kan productie naar andere doelen verschuiven; combinatie met uitbreiding vraagt eigen gepaarde proef. Wonderstad, voltooiingssnelheid en definitief latewonderbeleid blijven open. Herstel na normale sluiting: archiveren gewijzigde saves/profiel,7 beforebytes terug,8 uitsluitend eigen hashgecontroleerde nieuwe bestanden verwijderen; alle beforehashes/inventaris exact, DLL gelijk, pc aan. Onverwachte afwijking stopt voor review.
