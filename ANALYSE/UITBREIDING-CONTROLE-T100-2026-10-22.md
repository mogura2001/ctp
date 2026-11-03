# Controle T100: handmatige eindpuntmeting

2026-10-22T16:42:16.183262+02:00 Europe/Amsterdam. Uitvoeringsevaluatie volgens UITBREIDING-LANG-MANUEEL-20261022.md; alleen opgeslagen bewijs en hashketens gelezen. Eigen werk afgerond en gestopt na overdracht.

1. Eindpunten en procesbinding

De Doel3-controle telt op T100 **86 steden**, per civ2..8: **14,14,15,4,13,14,12**. Alle zeven kennen Religion en Theocracy en hebben actieve regering3.

T0 en T100 zijn tweemaal stabiel gelezen in exact dezelfde instantie: PID5404/creationFILETIME134371530391028723/run-id uitbreiding-lang-20261022-release-v1. Executable, modulepad, enginehash en geteste AI-DLL eb6f58a7… zijn gelijk gebonden. Beide snapshots hebben de zes toepasselijke loadedchecks True en uitsluitend de kandidaat-only payloadcheck False. T0 heeft alle historische civvelden gelijk, met alleen ai_actor/effective_aip buiten vergelijking; advance_count138 gelijk. Deelnemers exact2..8.

Alle zeven processed_round-waarden gaan van−1 naar99: **100 native rondes verschil tussen de twee eindpunten**. Dit bewijst geen honderd afzonderlijk waargenomen éénbeurtsstappen. De gebruiker voerde de doorloop uit; start/close vermelden eerlijk n_consumed0, geen automatische tokens en uitsluitend T0/T100-snapshots. De eerste automatische intro-opname faalde op foreground vóór invoer. De verse, geladen T0-toestand bindt de handmatige overname volgens de ontwerpaanvulling. save_identity_proven en atomic_snapshot_proven blijven False.

| Civ | T100 steden in bezit | Religion/Theocracy | Actieve regering | Huidig onderzoek |
|---|---|---|---|---|
| 2 | 14 | beide bekend | 3 | Mechanical Clock |
| 3 | 14 | beide bekend | 3 | Printing Press |
| 4 | 15 | beide bekend | 3 | Cannon Making |
| 5 | 4 | beide bekend | 3 | Perspective |
| 6 | 13 | beide bekend | 3 | Nationalism |
| 7 | 14 | beide bekend | 3 | Cavalry Tactics |
| 8 | 12 | beide bekend | 3 | Gunpowder |

Gevraagd onderzoek, gevraagde regering en deadlines staan per civ in CONTROL-REVIEW.json; ze zijn uit dezelfde gebonden T100-snapshot overgenomen.

2. Save en herstelketen

De bewuste gebruikerssave UITBREIDING-CONTROLE-T100 is behouden en gelijk aan de hostkopie: SHA256 **daf39c45af52e20f933da9a2f243110803d4662fd18594438141cea0cc176ea7**. De volgende kandidaat-beforeinventaris en backup bewaren exact dezelfde bytes. De T100-koppeling berust op gebruikersbevestiging plus hetzelfde live eindpunt; er is geen afzonderlijke save-decoderbinding geclaimd.

De controle sloot normaal na448,629s, count0; herstelrecord16:38:08 bevestigt29 bestanden, twaalf bestaande archieven, release-DLL en gesloten controlepoorten. Onafhankelijk zijn voor alle29+12 de oorspronkelijke backups, de verse opvolgende beforehashes en opvolgende backups exact gelijk gecontroleerd. De nieuwe dertiende autosave is dubbel gelijk: **67163d3d14f7532bc254478d6b8494326dc65af7e6ddd5b78ce0fd30405bc2fc**; exacte autosavebeurt is onbekend.

De root heeft daarna om16:39:54 de kandidaat df3ac89d… geïnstalleerd en een nieuwe instantie gestart. De herstelclaim count0/release-DLL betreft het controle-einde vóór die opvolginstallatie; zij is geen actuele globale toestandsclaim. Deze evaluator heeft de kandidaat of het spel niet aangeraakt.

3. Bruikbare vergelijking en grenzen

T0/T100 kunnen als handmatige controle-eindpunten dienen voor bezit, onderzoek en regering tegenover een kandidaat met dezelfde vaste start en zeven native eindronden99. Rapporteer de individuele verschillen naast het totaal. Er is nog geen kandidaatwinnaar in dit controledocument.

Het oorspronkelijke automatische criterium101 snapshots/100 exclusieve tokens is **niet gehaald**. Geen historische T26 aan deze run vastplakken, geen T25/T50 of verloop interpoleren. Exacte eerste25/30/40-beurten en eerste actieveTheocracy zijn niet gemeten; ook T26-behoud ontbreekt in deze arm. Op T100 heeft geen civ25/30/40 steden, maar een eerdere overschrijding gevolgd door verlies kan uit twee eindpunten niet worden uitgesloten. Daarom geen fictieve “eerste30 >100”-uitkomst.

Bezitsaantallen zijn geen aantallen eigen stichtingen. De release meet geen settlervoorraad/-vraag, producentdiagnostiek of locatiecertificaten; nuttige stichtingen, queueophoping en laborerinzet blijven onbewezen. Doel1/1a en volledigeDoel5 blijven OPEN. De lopende kandidaatarm is uitsluitend roots verantwoordelijkheid.

Bewijs: [CONTROL-REVIEW.json](../PROEVEN/uitbreiding-lang-host/20261022/release-v1/CONTROL-REVIEW.json), exacte endpoint-/hosthashes en29+12 herstelketens. Budgetbron 2026-10-22T14:42:13.886Z: vijfuur91%/week50%, stateok. Evaluator gestopt; pc blijft aan.
