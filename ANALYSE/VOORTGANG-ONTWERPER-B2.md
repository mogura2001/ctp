# Voortgang ontwerper B2

Gerichte foutpoortherziening op 8 oktober 2026, gestart om 09:49 Europe/Amsterdam en afgerond voor rootreview. Ownership uitsluitend dit bestand en ONTWERP/GEZAMENLIJKE-OPENING-B2.md. Geen implementatie, build, tests, handleruitvoering, spelbediening of procesactie. Geen actieve achtergrondrun/shutdown.

Afgerond: rootbewijs opening-fault-b2-caller-and-handler.txt volledig gelezen. RobotCom::Load behoudt adapter-EAX; manager52dec8 test nul en roept via52decc–52ded6 handler401560 aan vóór volgende-civstap52dede. Handler formatteert, roept4017a0 en doet op401598 deliberate NULL-write. Ontwerp kiest bij ongeldige load expliciet EAX=0 met juiste cleanup. Void Save gebruikt een eigen thunk rechtstreeks naar hostbase+1560, cdecl title/format met vaste korte tekst zonder procenttekens; geen normale succesretour en UD2 bij onverwachte handlerretour. Geen graceful menuherstel of behoud van onopgeslagen werk geclaimd. Ongeldig bestand is geen herstelstart.

De concrete foutpoort is hiermee ontworpen; kandidaatimplementatie/ABI/hostbinding en geen managervervolg blijven gerichte C-acceptatie. Offline controles mogen fatale handler expliciet stubben; dat is geen uitgevoerde enginecrash. Geen nieuwe algemene analyse nodig. Het bestaande completion/save/load/reload/record-, FLI- en researchherstelontwerp blijft intact. Root kan de afgebakende offline bouwopdracht beoordelen. N25/30 blijft pending gebruikerskeuze; technische fixtures voor beide zijn toegestaan, geen productievariant gekozen. B4-overdracht blijft afzonderlijk vervolgwerk, buiten deze run.

Eerdere herziening eindigde om 09:45: permanente completion0→1 bij steden≥N én actieve Theocracy; twee eigen inputs, vijf native ingrepen, record36 met marker/versie/civ/completed/N, begrensde legacy-T0peek en reloadstackcapture. Latere regering/stadsverlies heractiveert niet. Barbarenbeleid blijft apart. Variant-saves niet aan originele DLL geven; herstel gebruikt originele T0/B1 of een eerder gevalideerde passende variant-save.

Stopgrenzen week≤10% en vijfuur≤5%. Gewone exec faalt door deny-read ACLs; geautoriseerde documentreads/-edits vereisten require_escalated. Historische automatische readafwijzing van 7 oktober is na verse reset opgelost. Ontwerprun afgerond; alleen review/kandidaatacceptatie en pending N blijven.
Afrondingstijd Europe/Amsterdam: 2026-10-08 09:52:13. Verse budgethelper bij afronding:
{
  "reported_at_utc": "2026-10-08T07:52:02.499Z",
  "checked_at_utc": "2026-10-08T07:52:13.555034+00:00",
  "age_seconds": 11.1,
  "windows": {
    "five_hour": {
      "remaining_percent": 12.0,
      "used_percent": 88.0,
      "window_minutes": 300,
      "reset_at_unix": 1791461065
    },
    "weekly": {
      "remaining_percent": 55.0,
      "used_percent": 45.0,
      "window_minutes": 10080,
      "reset_at_unix": 1791987559
    }
  },
  "stop_reasons": [],
  "weekly_remaining_percent": 55.0,
  "five_hour_remaining_percent": 12.0,
  "state": "ok"
}
