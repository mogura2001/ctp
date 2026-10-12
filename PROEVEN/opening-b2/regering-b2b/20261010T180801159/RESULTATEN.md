# B2b kandidaatteksten voorbereid

10 oktober2026,18:10 Europe/Amsterdam. Status **PREPARED_OFFLINE_TEXT_ONLY_NOT_INSTALLED**. Frozen ontwerp GEZAMENLIJKE-OPENING-B2.md SHAea5140b5505c11f457bdcdc3cf41fcc023e277bf247866228ad356919c9ef40e; alleen B2b, boven de bestaande B1/B2a-basis. Geen strategische N gekozen.

candidate/ bevat tien echte CRLF-bestanden, oorspronkelijke bytes/comments behouden:

- inputs.fli: opening_completed/opening_required plus yes/no_opening_required-memberships.
- set_govern_opening.fli: uitsluitend Theocracy rang1 en Tyranny rang2 bij yes_opening_required.
- set_govern_after_opening.fli: alle twaalf oude voorwaarden/consequents/comments behouden, iedere if extra no_opening_required. Terugnemen van uitsluitend de guardbytes levert bytegelijk de originele set_govern.fli op.
- Zes Cleric/Slaver/SciFew/SciMany/WarFew/WarMany-beginturns: op de oude regeringincludeplaats opening gevolgd door after_opening.
- Default/beginturn.fli: alleen openinginclude na outputs; oude uitgecommentarieerde template/aiploader intact.

Statisch gecontroleerd: actieve include-expansies vanaf alle acht personalityroutes. Zes normale routes bereiken beide nieuwe regeringsincludes en niet de oude; Default alleen opening. Barbaren blijven via mainBarbarians→beginturnBarbarians de oude set_govern en barbarian.aip gebruiken; gedeelde inputs-declaraties zijn daar inert. Geen B2c-actions, researchoverlay/restores, nieuwe outputwaarden of ander regeringsbeleid toegevoegd. candidate.diff daadwerkelijk gelezen: uitsluitend bovenstaande wijzigingen. routing.json is tekstuele bereikbaarheid, geen native parser of rangmeting.

Broncontrole: alle116 aidata-bestanden matchen de geaccepteerde gepinde PROEVEN/opening-b2/protected-before.json, inclusief acht B1-AIPs. Alle116 na voorbereiding ongewijzigd; volledige bytebackups en geverifieerde hashes in backup/ en backup-manifest.json. manifest.json bevat per kandidaat oorspronkelijke en nieuwe hash/omvang; candidate.diff en byte-diff.json tonen regel- en byteverschillen. prepare-text.py is alleen deze concrete offline tekstgeneratie, geen observer/native/harness.

Geen installatie, CTP-proef/CTP-og/binarywijziging, Start, GUI, live-reader, native-uitvoering of parserframework. Werkelijke FLI-parseracceptatie, native registratie/effectieve rangen/defaultreset/pollovergang, gekozen N en echte gameplay blijven open. Geen verbetering uit tekstvoorbereiding geconcludeerd. H1-live blijft afzonderlijk geweigerd tot expliciete gebruikersgoedkeuring.

Laatste verse budget18:09:14 week83/vijf90 stateok. Uitvoerder stopt voor rootreview van kandidaatbestanden/diff/manifest; pc blijft aan. Volgende handoff: rootreview van B2b-only tekstpakket en afzonderlijke opdracht voor de nog open parser/native/hostpoorten; huidige taak geeft geen installatie- of spelvrijgave.
