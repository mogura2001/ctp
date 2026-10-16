# U30 reason23: bestaande H3-uitkomst bewaren

16 oktober 2026, 13:10 Europe/Amsterdam. **Fase B gereed voor rootreview en uitleg vóór C.** Basis: door root geaccepteerde [A-overdracht en dekkingsmatrix](../ANALYSE/U30-REASON23.md), drie beslisvragen beantwoord. Doel1/1a: nuttige settlervraag naar30 steden, daarna verdere nuttige uitbreiding tot40 onder Theocracy. Dit voorstel neemt alleen een observatieblokkade weg; het voltooit geen gameplaydoel. Ownership: dit bestand en het eigen voortgangsbestand; PROJECTSTATUS.md blijft van root.

## Beslissing en exacte ingreep

Huidig: de laatste bewaarde pass civ8/generatie7 eindigt met context1/classified1/reason23/Gcert0. De nativevraag5 blijft behouden. H3-UNKNOWN is plausibel, maar de reader bewaart het bestaande H3Result niet; een concrete fout in predicate, ABI of layout is niet aangetoond. Gewenst: de bestaande uitkomst van uitsluitend deze laatste pass bewaren en daarmee de volgende noodzakelijke vraag kiezen. Geen verandering van de AI-beslissing of UNKNOWN-afhandeling.

De bestaande FLI/AIP-route is afgedekt in de [beslisketens](../ANALYSE/BESLISKETENS-OVERZICHT.md) en [vorige B-overdracht](U30-TYPE10.md): quota/profielen geven geen aangetoonde instelling om deze eigen H3-buffer te bewaren. De ontbrekende mogelijkheid betreft de externe reader, niet extra gameplaylogica. De bekende eigen buffer is geen bewijs van een algemene modding-hook; SLIC of een diagnostische DLL is hiervoor niet nodig.

Maak een **nieuwe eigen proefmap en readerkopie** vanuit de geaccepteerde type10-reader; laat het historische pakket intact. Kandidaat blijft SHA256 `b6f272d2503edf5f1cf03f927ebd40ff5dd82b1a2c9d9c948beb4e7215baed62`, manifest `fa5392c650bc2647d072a9e828256b2a07c43d40d7893dee1efd2276ef431e27`. Geen rebuild, DLL-/gameplaywijziging of sciencecompositie.

1. Voeg in de eigen bestaande `shared_state()` uitsluitend header-scalars `candidates=Plan+68`, `slots=Plan+80`, `h3calls=Plan+128` toe.
2. Voeg per snapshot één exact begrensde read van1152bytes toe op `AIbase + state_rva + 0x40600`; `state_rva=0xdd000`, dus slot0-RVA `0x11d600`. Controleer het gehele bereik tegen dezelfde exacte geladen module en eigen stateomvang `0x54804`; `0x40600+1152=0x40a80` past daarin. Bewaar alle slotbytes als rawhex. Geen pointers uit de bytes volgen, extra enginecalls, ORDER-/CAPTURE-read of nieuwe buffers/hooks.
3. Neem scalars én slotbytes op in beide bestaande `stable_sample`-metingen. Eis dezelfde volledige modulebinding, civ/generatie en identieke snapshots. Decodeer H3 uit slot[128:1152] met de **bestaande H3-layout**, zonder een tweede layout te verzinnen: status/reason/modelID, h2_status, open_count, unsupported_entry_mask, vier indices en H2.status/reason/count/mountains; behoud bestaande marge/voorwaarden en entryposities conditioneel.

De stappen zijn afzonderlijk offline controleerbaar; pas hun gezamenlijke stabiele snapshot beantwoordt de runtimevraag. Firstcalltoeschrijving uitsluitend bij reason23/classified1/h3calls1/slots0 in dezelfde laatste pass. Andere combinaties krijgen UNKNOWN voor die toeschrijving. Geen certificering van de overige zes AI's uit één gedeelde buffer.

## Interpretatiegrenzen

| H3-uitkomst | Toegestane conclusie en volgende vraag |
| --- | --- |
|0/reason14 | H3Host faalt vóór current_model; geen individuele hostguard zichtbaar. Overige zero-initialisatie is geen gemeten food-/bergtoestand. |
|0/reason10 | Capacityketen faalt; gebruik bestaande H2.reason. Ontbrekende subreason laat de vroege nullpositie open. |
|0/reason11 | WGF/stand/factor niet ondersteund; alleen reeds geschreven velden gelden als waarneming. |
|0/reason12 | Centrumfood/rekenroute niet ondersteund; gewiste fooddata bewijst geen specifieke Cell/DB/mismatch/overflowguard. |
|0/reason13 | Geen ondersteund plan met unsupported_entry_mask; mask lokaliseert entries, niet hun leafguard. |
|2/model1/geldige indices | Onderzoek key/invariantketen met bestaande slot-/entrybytes; exacte falende keyreturn ontbreekt. |
|1, ongeldig resultaat of onjuiste passbinding | Eerst observatie/lifetime/binding afwijzen; geen tekortcertificaat. |

Onbereikte velden blijven conditioneel UNKNOWN, ook als rawhex nul bevat. Een later noodzakelijke leafdiagnose gaat gericht terug naar A. Geen blanket `roles_bad→roles_next`.

## Controle, korte proef en herstel

**Volgorde:** reader uitbreiden → beperkte offline review → rootreview/uitleg → één nieuwe T0/n/T1-arm → herstel. Offline bewijs: kleine brondiff; exacte readbounds en modulepins; rawhex decodeert tot1152bytes, H3-slice tot1024; vaste bestaande offsets/typen gebruiken en ongeldige tellingen/indices zonder dereference rapporteren. Controleer met bewaarde bytes de decoder en conditional-UNKNOWNlabels; geen fixtureframework, nativecalls of build nodig. Nieuwe readerhash en provenance vastleggen; kandidaat/manifest en enginehash/pins blijven exact.

C volgt daarna dezelfde geaccepteerde type10-procedure met **nieuwe backup, actuele pins en ongebruikte gate**. Dezelfde vaste Deity-T0-start/savehash en instellingen; één autonome `n`, één T1, geen lange benchmark. Leg PID/creation/modulebinding, stabiele T0/T1, civ/generatie en turnvoortgang vast. Alleen de reader verandert. Stop bij bindings-/stabiliteitsfout of afwijkend passpatroon en rapporteer de grens; geen extra ronde toevoegen.

Succes: offline omvang/layout/binding correct; stabiele rawslot/scalars beschikbaar; bij het vereiste passpatroon één H3-uitkomst met bovengenoemde begrensde conclusie, of expliciet een inconsistente observatie. Geen belofte van extra settlers/steden. Extra leestijd kan timing beïnvloeden; twee gelijke snapshots bewijzen geen atomaire wereldtoestand. Deze korte proef test observatie plus ongewijzigde kandidaat; latere beleids- of sciencecombinaties vereisen een eigen proef.

Sluit de eigen game normaal volgens bestaand draaiboek, archiveer nieuwe output/autosave, herstel alle29 beschermde bestanden naar de gecontroleerde Doel3-release, verifieer hashes/defaultautosave, verwijder alleen de eigen alias en sluit/verbruik de gate. Reader is buiten de game: terugkeer naar de oude reader volstaat voor die wijziging. Pc blijft aan. Alternatieven: opnieuw blind dezelfde header meten levert geen onderscheid; nieuwe DLL-telemetrie/vooraf extra captures zijn nu onnodig. Open blijft uitsluitend de echte H3-oorzaak; geen ontbrekende strategische gebruikerskeuze.
