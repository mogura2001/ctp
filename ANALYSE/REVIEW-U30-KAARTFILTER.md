# Rootreview U30-kaartkennisfilter

17 oktober 2026, 11:50 Europe/Amsterdam. A-overdracht U30-H2-GATE28 en volledig B-voorstel ONTWERP/U30-KAARTKENNISFILTER.md gelezen. B inhoudelijk geaccepteerd en gebruiker uitleg gegeven vóór C.

De ingreep behandelt beide aangetoonde oorzaken: helepassfallback op lokale onbekendheid én verdringing van bekende locaties door onbekende vroege keys. Alleen een skip bij H3 zou onvoldoende zijn. Filter in keyfase, allekeysvalidatie, eigen prefixcount en nulcount als normale lege selectie passen bij de bestaande eindformule/nativevraag. Nieuwe query wordt vóór gebruik expliciet gebonden; H3Host alleen dekt World+28 niet. Andere UNKNOWNcategorieën worden niet verborgen.

C mag uitsluitend eigen bronvoorbereiding doen in PROEVEN/u30-kaartfilter/20261017T115000, met reader en begrensde callerfixturevoorbereiding. Root moet vervolgens de werkelijke bron/pins/layout/ABI en verschillen beoordelen vóór kandidaatbouw of native-uitvoer. Geen installatie-/spelvrijgave op basis van B alleen. Hoofdrisico's bij review: verkeerde externe versus canonieke positie, callclobber, Planoffsetoverlap, prefix-/ORDERgrenzen, keyguards vóór filter, gewijzigde readerattributie en pinprovenance. De betekenis van ongezien terrein voor het volledige project blijft open; dit ontwerp vernauwt het einddoel niet.

Releasecontrole11:41:19pins gelijk, geïnstalleerde DLL eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890. Geen nieuw gameplaybewijs. Eerdere Theocracy-acceptatie behouden; uitbreiding30–40 en overige doelen blijven open.

## Bronreview12:03 — bouwvrijgave, nog geen native/game

Volledige BRONOVERDRACHT/CALLER-CONTROLES en diffs gelezen. Onafhankelijk SOURCE-PINS.json hash69632b90d6d5fcc79533f4917bf706196185e6bcae99ea1747ffbf60dbc99b79 en alle29bestanden exact; ongewijzigde functies in native/policy/integration onafhankelijk AST-identiek. Nieuwe reader behoudt rawbytes en interpreteert slechts de unieke H3call bij geldige prefixinvarianten; niet meer ten onrechte classified1 vereist. runtimepins nog null/failclosed; postbuild pins moeten apart in rootgate/pakket worden gebonden om manifestcirkel te vermijden.

Semantische review: keyvalidatie vóór gate; oorspronkelijke externe CAPTUREpointer op EBP−32; EDI/nonvolatiles behouden, stdcallret8 zonder calleradd; false-index−1 vóór prefixkeuze; min64known en eigen prefixcount; nulknown bereikt geen best−1store. Consumer signed vergelijkingketen sluit ook negatieve known/candidates uit; ORDERindex bewaakt vóór *8; andere H3UNKNOWN blijven reason23. Plan224..239 is vrij, arrays/PLAN_SIZE gelijk. Onafhankelijk drie bodybytes37/28/115 en Worldslot345308→533580 exact tegen gepinde engine bevestigd. Geen benoemde bronblokkade.

Bouwvrijgave TRUE: eigen compose/doublecompose/PE/branche-/byteclassificatie en hashes controleren. Native/game/install blijft FALSE. Daarna beperkte helperfixturebron reviewen vóór compilatie/run. Geen volledige oude suite of nieuwe fixedaddressfixture. Exacte kandidaat moet nog worden gereviewd vóór een spelproef.

## Kandidaat en callerbron12:17

Werkelijke canonical_prefix-disassembly en semantische checker gelezen: key→externalpointer→World+28-stdcall, sentinel, min64known/counter en consumerbounds conform bron. Kandidatemanifest vermeldt738be4098dadc6657b121519213e794ce3ec095025fdc940f6c30a5d89661d66, manifestd48b63b2363f0bfce2fe4b7d44a83b90951a524ecf3f300bf9661b50080be2a9, eigenRWde000/54804. Statische wholefile/PE/B2/branches en offline trusted_binding gerapporteerd geslaagd; onafhankelijke definitieve BUILD-PINS-hashcheck volgt vóór host.

Volledige caller/NativeCaller.cs en fixture-recipes.py gelezen. Alleen .u40c in willekeurig eigen geheugen, directe helperallowlist, eigen Plan/World/stubs, twee jumps uitsluitend in eigen image; echte H3PosCompare. Bestaande shim toetst stack/nonvolatile/x87, Plan/ORDERcanaries en gateWorld/externalpointer. 4096DWORD-gatetable past in eigen0x5000state. H3stubstatus1 bewijst alleen no-planroute, geen supportedslotcertificaat. Geen gameproces, engine-DLL, fixedaddress, host/resolver/finalepass bereikt.

Vrijgave beperkte compilatie en één helperrun met maximaal45s: TRUE na vastgelegd checkpoint en expliciete extensionRVAcontrole. Geen installer/gamevrijgave; failure terugmelden zonder testsuppressie/loaderretry. De callerresultaten bewijzen de selectie-/callercontrolflow, niet enginebitsemantiek of gameplay.

## Nativecaller en hostvrijgave12:26

BUILD-PINS476d6dbb6df8469023c1cd8297f70dcf085e7c87f23541ded0aa3edbe7cf68aa onafhankelijk bevestigd op51bestanden en alle manifestsourcepins. Callerbron vooraf gelezen; één eigen x86helper PID30992 eindigde normaal exit0 in3,875s,39helpercalls. Log/PASSlabels gelezen:65eerste64false bereikt index64, gemengde keys/ties/CAPTUREbehoud,65known/cutoff,4096false, key/count/nodes/prefix/ORDERguards, UNKNOWNreason10/11 en H3budget intact; ABI/x87/canaries bij iedere call. Geen supportedslot-, echteengine- of gameplayclaim. Oorspronkelijk omvangrijk resultaat door PowerShellmetadata bewaard; compacte kopie uit ongewijzigde logs, geen extra run.

Vrijgave één eigen hostarm vanuit vasteT0/éénn/T1 na verse budget-/proces-/29backup-/pincontrole: TRUE. Alleen nieuwe738be409...-kandidaat, geen sciencecompositie, geen extra beurt/startretry; gebonden reader/stabieleT0/T1, normale sluiting en29hashherstel/autosavebehoud. Capture alleen bij bevestigd succes als bewijs gebruiken. Bij andere fout geen voorbijgefilterde normale gatefalse als succes claimen. Root voert uit volgens bestaande Bediening; pc blijft aan.
