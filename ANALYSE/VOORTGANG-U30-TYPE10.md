# Momentopname gerichte U30-type10-analyse

15 oktober 2026, 19:40 Europe/Amsterdam. Rol: ctp_analist; **afgerond en gestopt**, geen achtergrondrun/timer. Ownership uitsluitend dit bestand en U30-TYPE10.md. PROJECTSTATUS.md blijft van root.

- Gestart na echte R44-2-overdracht: doel1/1a; verklaar uitsluitend de falende `resolve_type`-guard of lever de kleinste noodzakelijke onderscheiding.
- Afgerond: R44-2-paar/T1, bestaande naam/category-/UnitDB-bewijzen, actuele token/units, source en werkelijke kandidaatinstructies gelezen. Geteste kandidaat8610 en engineb1b5256f gepind; negen echte enginebodies en zes vtableslots offline gecontroleerd, exacte token op RVAdcc54. Geen vaste token-/ABI-/countfout aangetoond.
- Nieuwe concrete conclusie na roots gerichte maskvraag: Record+34&20h/+dc is IS_SPACE_LANDER (token125→case58→46bd14), geen landmovement. Gewone UNIT_SETTLER heeft die ruimteflag niet. De resolver vereist dus een verkeerde eigenschap. Echte landmovement staat Record+30/80000000h (token66→46b82b).
- Juiste vervanging machinecodegebonden: dezelfde UnitDB-vtable+1c→531940/ret8 retourneert Record+30&FF000000h. TEST80000000h/nonzero vereist landmovement; geen BOOL1- of signedpositivevergelijking. d8=IS_SPACE_LAUNCHER blijft onveranderd en is geen failureguard.
- Oplevering: [U30-TYPE10.md](U30-TYPE10.md) bevat de guardmatrix, exacte parse-/slot-/bodybytes, minimale guardfix en keuze tegen aparte voorafgaande leafdiagnose. Kleine bestaande-reader-aanvulling rawt/types/d8/raw30/raw34 kan tijdens toekomstige proef; geen nieuw framework.
- Open: precieze uitgevoerde leaf is nog niet runtime-gecertificeerd, maar de verkeerde eis is zelfstandig bewezen en blokkeert een B-herstelvoorstel niet. Eerstvolgende reviewbare uitkomst: klein B-voorstel +dc→+1c/80000000h met pinning, vervolgens gecontroleerde C/éénpassmeting indien vrijgegeven.
- Acceptatie: twee eindige A-vragen beantwoord tot overdrachtsgrens; doel1/1a gameplayacceptatie open, geen nieuw oorspronkelijk doel afgerond. Geen spel/GUI/RPM/nativefixture/build/code-/binarywijziging uitgevoerd. Alleen twee eigen analysebestanden geschreven.
- Budgetcontrole19:31:42: verse bron17:31:06UTC/leeftijd36,2s, vijfuur70/week80/stateok; stopgrenzen5/10 blijven gelden. Pc aanlaten; geen afsluitopdracht of planning.
- Hervatpunt bij gerichte terugvraag: de werkelijk gemeten leaf toetsen aan de matrix, geen heropening van alle units/engine. Deze rol wacht niet actief en draait niet door.
