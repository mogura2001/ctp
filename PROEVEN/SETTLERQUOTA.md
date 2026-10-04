# Testplan: betekenis van settlerquota

## Geldende opstelling

De gebruiker heeft gekozen voor een natuurlijke partij vanaf één identieke save vóór de eerste beurt. Het eerdere plan met kunstmatig geplaatste steden is vervallen. De eerder gegenereerde varianten wijzigen ook prioriteiten en meerdere klassen; gebruik die niet voor deze vergelijking.

1. Gebruik CTP-proef, Deity. Bewaar een startsave vóór de eerste beurt en controleer terugladen. De gecontroleerde save en hash staan in settlerquota/vaste-start/STARTMANIFEST.md.
2. Begin met oorspronkelijke AIPs. Laat de AI zelfstandig stichten en bouwen. Plaats geen steden, geef geen bevolking of technologie en verander geen AI-queues.
3. Houd de menselijke acties gelijk tussen runs. Volg circa twintig beurten. Noteer op vaste meetmomenten AI-steden, settlers, huidige productie en beschikbare bevolking. Bewaar bewijsbeelden en checkpoints.
4. Maak daarna een variant die uitsluitend de onderzochte settlerquota verandert. Behoud prioriteiten, core/overflow en overige gameplayregels. Leg alle gewijzigde bestanden en waarden vast.
5. Herstart en laad exact dezelfde startsave. Controleer of de gewijzigde AIP-aansturing daadwerkelijk wordt gebruikt: een bestandswijziging alleen bewijst dit niet, omdat saves AI-state kunnen bewaren.
6. Herhaal dezelfde menselijke bediening en meetmomenten. Vergelijk eerst oorspronkelijk versus nul. Op verzoek van de gebruiker volgt een reeks met alleen primary -20 en +20, eventueel daarna -10/+10 en -5/+5 als deze extra informatie opleveren. Meet T0, T10 en T20, met passieve checkpoints op T5/T15. Ook sterke waarden hoeven binnen twintig beurten geen verschillende aantallen steden op te leveren; beoordeel tevens de bouwopdrachten.
7. Herstel oorspronkelijke proef-AIPs na afloop. Rapporteer waarnemingen en onzekerheden apart van conclusies.

## Wat de proef kan aantonen

Een verschil in latere settlerbouw kan productieaansturing ondersteunen. Het actuele aantal settlers is geen rechtstreekse uitlezing van een quota: stichting, reistijd, bevolking, productie en andere settlerklassen beïnvloeden dit. Een geladen save test geen oorspronkelijke toekenning van startunits.

De eerdere verse startcontrole gaf twee AI-settlers bij zowel baseline als de brede nulvariant. Dat bewijst niet dat de productiequota geen effect heeft. Zie QUOTA-RESULTATEN.md.

## Lopende uitvoering

Actualisatie: -20 en +20 zijn vanaf dezelfde T0-save tot T20 voltooid. Beide blijven settlers bouwen waar de baseline naar een gebouw/legerunit wisselt, maar hebben op T20 hetzelfde aantal steden en losse settlers als de baseline. De gebruiker heeft verdere kleinere proeven gestopt en gevraagd eerst de uitbreidingsbeslissingen te analyseren. -10 is onvolledig; +10 en ±5 zijn niet uitgevoerd. Oorspronkelijke AIPs hersteld, proefgame afgesloten. Zie [reeksresultaten](settlerquota/reeks/RESULTATEN.md) en [beslisketen](../ANALYSE/UITBREIDING-BESLISKETEN.md). Onderstaande eerdere uitvoering is historische context.

Opslaan en terugladen zijn gecontroleerd. De oorspronkelijke AI en alleen-primary-nul zijn elk twintig beurten gevolgd vanaf dezelfde save. Daarna is de oorspronkelijke AI opnieuw twintig beurten gevolgd met dezelfde passieve menselijke bediening en observatiemomenten als de nulvariant. De gemeten baseline-uitkomsten op T10/T20 zijn herhaald. Zie [STARTMANIFEST.md](settlerquota/vaste-start/STARTMANIFEST.md) en [HERHALING-PASSIEF.md](settlerquota/vaste-start/HERHALING-PASSIEF.md).

Op T10 bouwt de passieve baseline twee settlers tegelijk en primary-nul één. Op T20 hebben beide drie steden; de baseline heeft één losse settler en primary-nul geen. Dit ondersteunt invloed op latere productie. De exacte betekenis van negatieve quota en het interne laad-/overridegedrag blijven onbewezen. De volgende reeks is op verzoek gewijzigd naar -20/+20, met kleinere waarden indien nuttig. Zie [RESULTATEN.md](settlerquota/reeks/RESULTATEN.md).
