# H3 — voedselbudget vóór stichting

7 oktober2026,22:22 Europe/Amsterdam. Gerichte A-overdracht na H2. Alleen-lezen; geen gameplay/codewijziging, spelstart, liveproces, fictieve city-ID/CityData of nieuwe tests.

## Antwoord

**Een conditioneel voedselbudget voor centrum+3bergen+1voedselwerker bij grootte4 is ontwerpbaar.** Huidige positionele food, de werkelijke Player-rantsoenfactor, geladen centrumenvironment en toekomstige fooddeltas zijn bereikbaar zonder city-ID. Een **exacte onvoorwaardelijke** nettovoorspelling ontbreekt omdat de nieuwe stad nog geen bonuscache/happiness/crime heeft. Geen crime0, standaardrantsoenen of centrumfood20 invullen als werkelijk kandidaatgegeven.

Dit geeft de ontwerper voldoende route voor H2+H3 samen: capaciteit, expliciete foodscenario's en voorwaarden combineren; onzekerheid als conditioneel/UNKNOWN bewaren. Geen verder constructor-, scheduler- of economieonderzoek nodig voor deze overdracht.

## Dekkingsmatrix en concrete invoer

| Gegeven | Route zonder city-ID | Betekenis/grens |
| --- | --- | --- |
| Vier open werkplekken | H2: World+ac, terrein+a8; kies3 unieke bergposities en één andere open positie | Centrum afzonderlijk; geen vijfde inwoner. Een hoogste-foodtile kiezen mag de3bergen niet opeten |
| Huidig food | **World+b8→534340→510f70→Cell500110** | Werkelijke huidige omgeving/improvements/goods; **+bc is productie**, niet food |
| Onderhoud | Vier expliciet veronderstelde POP_WORKER hebben ieder HUNGER10 | Consumptie **D=40×werkelijke rantsoenfactor**; andere bevolking/stand vraagt herberekening |
| Werkelijke rantsoenfactor | AiMain+2c→eigen Player-interface; interface+8→Player; Player+1318→object; **double object+8** | Getter4c27f0→4cb9a0. Stand op object+48; geen defaultstand of AI-schatting gebruiken |
| Regering | Bestaande Government-interface AiMain+48; echte Player-getters4c2b50/4c2b70 leveren CRIME_COEF/OFFSET | RATIONS_COEF beïnvloedt happiness; geen extra bewezen consumptievermenigvuldiger of FOOD_COEF |
| Futurefood | AiMain+50/Improvement: +10 typebeschikbaarheid, +20 positionele toelating, **+48 fooddelta** | +38 is absolute environmentcomponent, geen volledige tilefood/delta |
| Centrumcorrectie | Geselecteerd terrain/goodrecord+50→ENV_CITY_BONUS; environment+0=integerfood | Cell500110 voegt deze alleen bij Cell+14-cityhandle toe |
| Nieuwe stadseffecten | City+3a4 vlakfood, +3c8 foodpercent, typebonuslijst, foodwonderpercentage, [City+5cc]+b0 crime | Zonder toekomstige echte stad geen actuele query; als expliciete modelinputs behandelen |

Hergebruik: [RANTSOENEN-EN-STADSOPBRENGSTEN](RANTSOENEN-EN-STADSOPBRENGSTEN.md), [TERREIN-EN-IMPROVEMENTS](TERREIN-EN-IMPROVEMENTS.md), [PRODUCTIEKANDIDAAT-H2](PRODUCTIEKANDIDAAT-H2.md), [GELUK-WGF-EN-STADSOMVANG](GELUK-WGF-EN-STADSOMVANG.md).

Nieuwe [World-slot-/ABI-binding](BINAIR/candidate-food-h3-world-queries.txt) leest de echte vtable7452e0. World+b8 neemt World, MapPointData*, int32-output*: ESP+4/+8/+c, ret0ch; EAX=1 in de gebonden wrapper. Lees de geschreven foodwaarde en geef H2-MapPointData rechtstreeks door; wrapper503f00 verzorgt omzetting. Improvement-fooddeltas retourneren double in x87ST0; latere payload moet die return consumeren en ABI/controlword bewaren.

AllocWGF::GetCurrentRation20059610 is een schatting uit eigen velden+f0/+100/+f8/+30; [dump](BINAIR/candidate-food-h3-ration-ai.txt). Zij is niet gelijkgesteld aan de autoritatieve Player-rantsoenfactor. Deze laatste is door oorspronkelijke setter/getter bewezen als Const.BASE_RATIONS + stand×Const.UNIT_RATIONS, in OG 1+0.25×stand. Lees de werkelijke factor; kies niet stilzwijgend stand0.

## Centrumfood: wat verandert bij stichting?

De normale foodsum494970 telt **centrum eenmaal plus vier inwonersbijdragen**. Drie bergwerkers+één voedselwerker geven dus vijf voedselposities en vier hungerbijdragen. Bergfood hoeft geen0 te zijn: goods/rivier/improvements kunnen opbrengst veranderen.

Bij een ongesticht centrum ontbreekt de cityhandle op Cell+14; gewone Worldfood bevat daarom nog niet de uitsluitend citygebonden ENV_CITY_BONUS. Alleen vijf huidige queries optellen mist deze bijdrage; overal10/20 toevoegen is evenmin verantwoord.

Een concrete versiegebonden **geladen veldroute** is beschikbaar, zonder bestaande stad te faken:

1. Bestaande World-grid **[engineglobaalA7DD70]+1c** geeft na correcte intern geconverteerde z/x/y de huidige Cell. Cell+d=terrainindex, +0=flags, +14=cityhandle.
2. **TerrainDB globaalA7DD3C**: count+0, recordarray+8, stridec0. Getter455b10 controleert index; [bestaand bewijs](BINAIR/terrain-food-v2-engine-getters.txt).
3. Hergebruik de selectie uit500110: goodbits(flags&1c0), lokaal slot en teruglopen langs record+a0+4×slot; geldige good-subrecord gebruiken, anders hoofdrecord. GOOD_INDEX is geen lokale slotindex.
4. Lees geselecteerde record+50; bij aanwezige environment lees integer+0. Token993 ENV_CITY_BONUS→+50 en ENV_FOOD1005→environment+0 zijn gebonden in [veldbewijs](BINAIR/terrain-food-v2-environment-field-binding.txt).

Globals moeten via de daadwerkelijk geladen enginebasis/RVA worden gelezen met fingerprint-/datacontrole. Dit is een route voor later native modelwerk, geen geschreven helper of wijziging van de cel.

Voor gewone ondersteunde landcontext zonder bestaande city, tijdelijke unit-foodbijdrage of negatieve omgevingssom vóór clamp is toekomstige centrumfood **huidig food+gelezen citybonus**. Dit moet als ondersteunde conditie worden gecontroleerd. Cell500110 op500221–22a clampt eerst; de no-citybranch daarna kan bovendien tijdelijke army-/unitfood toevoegen, terwijl een cityhandle die branch overslaat. Blind huidige food+citybonus kan daardoor te hoog worden. In zulke gevallen de pure omgevingstermen uit de bewezen helper volgen of UNKNOWN geven. Speciale/dead-terreinpaden blijven afzonderlijke ongedekte gevallen. Geen verdere reconstructie nodig om die grens duidelijk te maken.

## Huidig versus toekomstig food

Huidig plan gebruikt daadwerkelijke food op de drie gekozen bergen en vierde werkplek, plus de ondersteunde hypothetische centrumwaarde. Nog niet aangelegde improvements tellen niet als huidige opbrengst.

Voor toekomstig food: selector1=IRR2 is op de gebonden gewone shallow/deep-waterrecords gekoppeld aan Ocean Faring, op land aan Agricultural Revolution. Gebruik typebeschikbaarheid én positielegaliteit, en **huidig food+positionele delta+48**. Food1+food2 niet stapelen; een absolute+38-bijdrage niet opnieuw als complete tilefood optellen. De delta bevat bestaande niveau-/goodcontext. Een onbekende tech geeft hoogstens pending potentieel; dat onderhoud is nu niet beschikbaar.

Normaal geen toekomstige IRR1-aanleg als oplossing rekenen. Reeds bestaande IRR1 blijft wel werkelijk huidig food. De Labyrinth-uitzondering vraagt een expliciete wondertaak en geldt niet voor ieder centrum. Materials/tijd zijn bereikbaar via de bestaande Improvement-/environmentroutes uit het terreinrapport; PW-, groei- en bouwplanning blijven buiten H3. Eventuele mine-foodverandering via dezelfde echte delta opvragen, niet veronderstellen.

## Conditioneel budget en precieze beperking

De normale bewezen foodsum en inline consumptie geven:

    R = echte Player-rantsoenfactor
    D = R × sum(max(Hunger_i,0)) = 40×R voor4 POP_WORKER
    S = (F_citycenter + F_M1 + F_M2 + F_M3 + F_F
         + hypothetische terrein-/vlakke stadsbonussen)
        × (1 + hypothetische cityFoodPercent)
        × (1 + toepasselijk foodWonderPercent/100)
    nettoFood = S - floor(S×crime) - D

De centre+vierworker-som, floor-crime-inhouding en dezelfde hunger/rations in echte update498205–295 zijn eerder bewezen. Geen extra regerings-foodfactor toevoegen; Theocracyproductiefactor1.25 is geen foodbonus.

Crime komt uit nieuwe stadshappiness, regering en crime-effecten. WGF, bevolking, stedenaantal, afstand, garnizoen/gebouwen en overige context beïnvloeden happiness. Een bestaand stadje kopiëren bewijst niet de nieuwe locatiecrime; de bekende happinesssubtotalen zijn geen exacte voorspelling.

**Veilige conditionele toets:** bij onderbouwde S_min≥0 en crime_max<1 is S_min×(1−crime_max)≥D voldoende voor onderhoud, want floor-inhouding is hoogstensS×crime. Crime_max moet een expliciete gerechtvaardigde ontwerpvoorwaarde zijn. Zonder informatie resteert alleen crime≤1; dat geeft normaal geen positieve onderhoudsgarantie bijD>0. Geen verzonnen10%-grens kiezen.

**Scenario-uitkomst:** lever brutofoodS onder benoemde centrum/gebouw/wondervoorwaarden, werkelijkD en vereiste maximale crime. VoorS>0 is crime≤1−D/S voldoende; een negatieve grens zegt dat dit scenario zelfs vóór crime onvoldoende brutofood heeft. Een scenario zonder gebouwbonus is een hypothese, geen bewezen constructoruitkomst of universele ondergrens. Lever apart huidige/pending-fooduitkomsten en voorwaarden; conditioneel voedbaar is nog geen bewezen duurzame productionstad.

De ontbrekende gegevens voor **exact netto vóór stichting** zijn toekomstige CityData-type/flat/percentbonuscache, toepasselijke foodwondereffecten, happiness/crime en bijzondere branch+448. Er is geen gebonden algemene candidate-cityquery voor die toestand. Autoritatieve CityData-/Population-netfoodqueries vereisen echte city-ID's; geen fictieve handle gebruiken.

Deze beperking houdt een conditioneel H2+H3-ontwerp niet tegen. Eerste ondersteunde normale landgevallen met echte rations/gelezen centrumcorrectie en expliciete bounds/scenario's uitwerken; ongedekte context UNKNOWN. Later werk pas wanneer het gekozen voorstel werkelijk exacte nieuwe-stadsmodifiers nodig heeft.

## Bewijsgrens en overdracht

Geen nieuwe emulatie/testserie. Alleen gerichte querydisassemblage en één AI-getterdump toegevoegd; bestaande celhelper-, parser-, consumptie- en stadsfoodcontroles hergebruikt. Enginehash b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79, timestamp37d6f702/imagebase00400000; robotcom.dll/map37b894e7/imagebase20000000. Civctp.map niet als adresbron gebruikt.

Root/ontwerper kunnen nu het gezamenlijke capacity+foodvoorstel maken. Geen H1uitvoerder-/H2ontwerpbestanden of PROJECTSTATUS gewijzigd. Deze gerichte analyse stopt; overige varianten, volledige constructor/happinessvoorspelling, save/events en economie blijven backlog.
