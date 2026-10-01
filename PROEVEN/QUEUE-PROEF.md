# Queueproef voor CTP I

## Klaargezet

`CTP-proef` is een zelfstandige kopie van `CTP-og`. Alleen deze kopie bevat het proefscript, de berichtteksten en DebugSlic=Yes. Origineel en AAIP blijven onaangeroerd.

De proef kiest de eerste stad van AI-speler 2, leest terrein/goods en probeert een granary achteraan de bestaande queue toe te voegen. Zij controleert direct het resultaat en vervolgens maximaal vijf AI-beurten. Zij voegt niets opnieuw toe en geeft geen gebouwen, inwoners of middelen cadeau. De granary is uitsluitend een herkenbaar testobject, geen vastgestelde definitieve bouwkeuze.

De functieargumenten zijn gecontroleerd tegen de CTP-I-documentatie van ontwikkelaar Joe Rumsey: [SLIC Function Reference](https://apolyton.net/articles/civilization-news/ctp1/modification-ab/9312863-slic-function-reference). De trigger- en variabelensyntax volgt lokale tutorials en zijn [SLIC-taalspecificatie](https://apolyton.net/articles/civilization-news/ctp1/modification-ab/9312681-slic-scripting-language). Dit vervangt geen echte compilatie of speltest.

## Uitvoeren

1. Start `C:\GIT\ctp\CTP-proef\ctp_program\ctp\civctp.exe` met die map als werkdirectory. Gebruik de proefkopie.
2. Start een nieuw normaal singleplayer-spel op Deity, zonder tutorial, met mens als speler 1 en ten minste AI-speler 2. Voor een geladen save is nog niet bekend of de nieuwe scripts worden ingelezen.
3. Noteer eventuele SLIC-fouten letterlijk. Bij een fout is de proef niet geslaagd.
4. Zodra speler 2 een stad heeft, verschijnt bij de mens een bericht over toegevoegd, overgeslagen of mislukte readback. De toegevoegd-melding heeft een eyepoint naar de stad. Voor inspectie van een verborgen AI-stad kan de editor nodig zijn; verander haar queue zelf niet.
5. Controleer de queue en productievoortgang, laat vijf AI-beurten verlopen en noteer ieder vervolgbericht. De AI kan het item verwijderen, laten staan of normaal voltooien.
6. Bewaar de start en uitkomst via de normale savefunctie in de proefkopie. Een nieuw spel waarin speler 2 direct geen geschikte stad heeft kan een herhaling vragen.

Een overgeslagen proef is geen bewijs dat queueaansturing faalt. De bevolking kan ook te klein zijn om de granary snel af te bouwen; alleen persistentie is voor deze korte proef vereist.

## Resultaatregistratie

Statisch gecontroleerd: alle gebruikte functienamen hebben een overeenkomstig SLIC-symbool in de lokale executable-map, alle proefbericht-ID's bestaan, accolades zijn gebalanceerd en de script-/tekstimports plus debuginstellingen zijn aangebracht. Geen SLIC-compiler uitgevoerd.

| Onderdeel | Resultaat |
| --- | --- |
| Script geladen zonder fout | Nog niet uitgevoerd |
| AI-stad geselecteerd | Nog niet uitgevoerd |
| Terrein/goods uitlezen zonder fout | Nog niet uitgevoerd; waarden aiqp_terrain/aiqp_goods in debugcontext |
| Queue direct gewijzigd en teruggelezen | Nog niet uitgevoerd |
| Queue na vijf AI-beurten | Nog niet uitgevoerd |
| Normale productie blijft behouden | Nog niet uitgevoerd |
| Laden van save met nieuwe scripts | Nog niet uitgevoerd |

Er is in deze workspace geen bestaande save gevonden. Er is ook geen beschikbare tool voor interactieve bediening van de spelinterface. De runtimeproef moet daarom nog in het spel worden uitgevoerd; de voorbereidende statische controles zijn geen succesbewijs.

Update: inmiddels is Windows-bediening via `Bedien-CTP.ps1` aangetoond en een technische proefsave gemaakt. De eerste runtimepoging gaf een HasAdvance-argumentfout; die is in het proefbestand gecorrigeerd volgens de lokale tutorial, maar nog niet opnieuw getest. De bovenstaande resultaatvelden blijven open. Zie [AUTOMATISERING.md](AUTOMATISERING.md) voor bewijs en beperkingen.

Als de queueproef slaagt, testen we pas een conditionele bouwregel voor één science-stad. Deze proef onderzoekt nog geen exacte scientists- of bergtiletoewijzing, toekomstige stadslocaties of monopolyhandelsplanning. Een verdwenen/vernietigde doelstad valt buiten deze eerste korte proef; gebruik een rustige teststart.

Vervolg: de tweede verse runtimeproef bereikte 3900 BC zonder SLIC-foutvenster na vereenvoudiging van geneste BuildingType-aanroepen. Geen AIQP-bericht gelezen, dus geen bevestigde queuewijziging. Show() is nu aan alle proefberichten toegevoegd op basis van de lokale tutorial; herladen en hertesten blijft nodig. Zie het vervolgverslag in AUTOMATISERING.md.
