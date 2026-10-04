# Herhaling met gelijke passieve bediening

Deze baseline gebruikt dezelfde T0-save als alleen-primary-nul. Alle AIPs zijn vooraf op hash gelijk aan CTP-og gecontroleerd. Het spel is volledig herstart. Geen menselijke b/Enter-invoer, geen stadsstichting, geen wijzigingen aan AI-queues, bevolking of technologie.

De observatievolgorde volgt de nulquota-run: T0 Unit Status van speler 2, terug naar speler 1, vijf beurten, checkpoint T5 zonder editorobservatie, vijf beurten, City Status en Unit Status op T10. Het stedenvenster wordt aan de titelbalk verplaatst zodat beide stadsrijen zichtbaar zijn. Arawn/Welsh wordt vanaf dezelfde start gevolgd.

| Beurt | Datum | Steden | Losse settlers | Bouwkeuzes |
| --- | --- | ---: | ---: | --- |
| 0 | 4000 BC | 0 | 2 | Geen steden |
| 10 | 3500 BC | 2 | 0 | Cardiff grootte 1: Settler 9; Swansea grootte 1: Settler 6. Twee Warriors en één Phalanx aanwezig. |
| 20 | 3000 BC | 3 | 1 | Alle steden grootte 1. Cardiff: Granary 9; Swansea: Phalanx 1; Pentraeth: Phalanx 6. Twee Warriors en één Phalanx aanwezig. |

Op T10 komt Cardiff overeen met de eerdere baseline. Onder dezelfde passieve bediening bouwt de oorspronkelijke AI twee settlers tegelijk, de primary-nul-run één. Dit versterkt de aanwijzing dat de onderzochte quota latere productie beïnvloedt. Het bewijst niet de exacte betekenis van -2, de actieve profielnaam of de wijze waarop meerdere settlerklassen samengaan.

Bewijs: baseline-passief-T0-units.png, baseline-passief-T10-city.png. Checkpoints krijgen de prefix baseline-passief en vervangen geen eerder proefmateriaal.

## Uitkomst

De volledige herhaling bereikte twintig beurten. De gemeten bouwkeuzes en eenheden op T10/T20 komen overeen met de eerdere baseline. Voor vergelijking met primary-nul gebruiken we voortaan deze passieve baseline: de menselijke bediening en observatiemomenten zijn gelijk gehouden. Beide bereiken drie steden op T20, maar de baseline heeft één losse settler en primary-nul geen. Op T10 bouwt de baseline twee settlers tegelijk, primary-nul één.

Dit is herhaalbaar bewijs dat de gewijzigde bestanden in deze proef samengaan met andere productie. De uitleg van negatieve quota als een vast rijksaantal is nog niet bewezen. Evenmin is de precieze actieve AIP/lijst intern uitgelezen. Een volgende proef met alleen primary -4 kan testen of een grotere negatieve waarde meer gelijktijdige settlerbouw uitlokt; houd daarbij core/overflow en prioriteiten gelijk en gebruik opnieuw T0. Een enkele actuele telling blijft onvoldoende voor de exacte formule.

Bewijs T20: baseline-passief-T20-city.png en baseline-passief-T20-units.png. Checkpoints T5/T10/T15/T20 bewaard. Geen AIPs gewijzigd tijdens deze herhaling. Na observatie terug naar speler 1 zonder nieuwe beurt; CTP-proef blijft open met oorspronkelijke AIPs.
