# B4: oorspronkelijke neutrale territoriumeigenaar

9 oktober 2026, 14:23 Europe/Amsterdam. Gerichte fase A voor uitsluitend [de ownerbindingterugvraag](../PROEVEN/settler-b4/ONTWERPTERUGVRAAG.md). Gameplaydoel: veilige uitvoerbare directlandvestiging telt mee voor dynamische settlervraag. Wijzigingsvraag: welke oorspronkelijke World+54-call en welke normale neutraalcode kan de gekozen eigen/neutraal-gate gebruiken? Geen spelstart, procesactie, native call, emulator, producer, gameplaywijziging of binarypatch uitgevoerd.

**Ontwerpantwoord: neutraal is exact signed −1 (`EAX=FFFFFFFF`), afkomstig van ownerbyte `FF`.** De oorspronkelijke engine initialiseert gewone gridcellen daarmee en schrijft dezelfde −1 expliciet bij het verwijderen van territoriumeigenaarschap. World+54 retourneert dit als signed32 in EAX. Civ0 levert afzonderlijk EAX=0; andere negatieve waarden worden hierdoor niet tot neutraal verklaard. De concrete ontwerpblokker is opgelost.

## Gebonden versie en bewijssoort

Alle conclusies hieronder zijn statische machinecodebevindingen op:

- Engine `CTP-og/ctp_program/ctp/civctp.exe`: SHA256 `b1b5256fb0fb1a844548eb62e7b13d79a8b4f81b4499cfbe93e614bd5268ac79`, timestamp `37d6f702`, imagebase `00400000`.
- AI `CTP-og/ctp_program/ctp/dll/ai/robotcom.dll`: SHA256 `3025070d66fba516e4cdd70ae332055e1e4ef5162bf1b14c163b9bd128a35d44`, timestamp `37b894e7`, imagebase `20000000`; de bijbehorende robotcom.map is door het bestaande hulpmiddel op timestamp/base gecontroleerd. Alleen deze passende map levert de World-GUIDnaam.
- Geen adres of functienaam uit de niet-passende civctp.map gebruikt. Beschrijvende routinenamen hieronder zijn interpretaties van de getoonde instructies, geen herstelde enginebronnamen. Geen runtimewaarneming of gameplayeffect gemeten.

Het bestaande `Analyseer-Engine-Interfaces.py World 0x54` en gerichte VA-ranges via `Analyseer-Engine-Locaties.py` zijn hergebruikt. Eén exacte bytezoekactie vond FF-schrijvers op het reeds bewezen Cell+0e-field; alleen hun korte routines, initcallback en gridkoppeling zijn verder gevolgd. Geen volledige territory-, pad- of schedulerketen onderzocht.

## Dekkingsmatrix van deze beslisketen

| Schakel | Concrete binding | Bewijs / conclusie |
| --- | --- | --- |
| AI → interface | AiMain+30; bestaande caller200178b7 roept vtable+54 aan | Bestaande diplomatiepadcallback pusht positie en World; EAX≤0-skip is op zichzelf geen neutraalbewijs |
| Engine-interface | GUID `2037a9617ac8d11185a70060083a4082` op744eb8; QueryInterface5331b0; vtable7452e0 | QueryInterface vergelijkt deze exacte GUID en geeft dezelfde interfacepointer; matching GUID komt uit oorspronkelijke AI |
| Slot → wrapper | 7452e0+54 =745334: bytes `80385300` →533880 | Werkelijke pointer in dezelfde engine; directe slotbinding |
| Wrapper → getter | 53388c→503f00; 53389c→516c10 | Positieconversie gevolgd door actuele World-gridgetter; ret8 |
| Readbreedte/return | 516c2f: `0fbe420e`; 516c34: `c20400` | Signed byte Cell+0e → volledige signed32 EAX; getter thiscall/ret4 |
| Normale lege cel | Initcallback4ff860; 4ff885: `c6400eff` | Schrijft ownerbyte FF, terwijl city/pop/armyvelden op nul worden gezet |
| Init is echt gridinit | 505d64 pusht4ff860, stride34/count; callback72575b; gridmapping505e35–505e5e | Wereldcelarray wordt per34-bytecel geïnitialiseerd en via World+1c benaderbaar gemaakt |
| Verwijder eigenaarschap | 516ef0 leest dezelfde byte; 516ef4 vergelijkt inputowner; 516efb pusht−1 naar500a40 | Onafhankelijke native verwijderroute herstelt exact de normale neutraalwaarde |
| Eigen/neutraalbeslissing | `owner == civ || owner == -1`, met normale civ/contextvoorwaarden | Ontwerp kan source, endpoint en alle padpunten hiermee binden; civ0 en andere signed codes blijven apart |

## Exact call- en positiecontract

World+54 is op deze versie:

`int32 __stdcall World_owner(World* world, const MapPointData* external_position)`

De oorspronkelijke AI-caller pusht eerst positiepointer en daarna Worldpointer. Bij wrapperentry staan World op ESP+4 en positie op ESP+8, vervolgens EBP+8/+c na de proloog. Er is geen outputpointer. Wrapper533880 leest EBP+c, zet via503f00 de externe positie om in globale scratchpositie `00A7E320`, haalt de actuele engineWorldpointer uit `[00A7DD70]`, en roept thiscall516c10 aan met deze intern geconverteerde positie. Zij eindigt met `ret8`, EAX intact. De getter eindigt met `ret4`; de wrapper ruimt de twee interfaceargumenten op. De Worldparameter is in deze wrapper niet als de echte gridpointer gebruikt.

Getter516c10 leest signed16 z/x/y op positie+4/+0/+2, volgt World+1c → z → x → y, en leest **één byte op Cell+0e met MOVSX naar EAX**. FF wordt daarom FFFFFFFF; 00 wordt00000000. Geen AL-return, zero-extension, HRESULT of succesbool aannemen. Callers moeten alle32bits van EAX vergelijken; low-byte-truncatie van onverwachte input is geen contract.

Geef dezelfde geldige externe MapPointData als bij de andere Worldqueries door. Handmatig vooraf y−x uitvoeren converteert tweemaal. De bestaande503f00-route normaliseert x en zet extern y om naar intern y−x. Zij leest de zes coördinaatbytes van de bestaande achtbytepositie. Deze getter heeft geen eigen bounds-/nullcheck; de bestaande ontwerpvoorwaarden voor geldige posities/ondersteunde laag en dezelfde actuele passcontext blijven nodig. Door het gedeelde scratchveld hoort deze interfacecall in de reeds gekozen geserialiseerde oorspronkelijke AI-callcontext; geen reentrant/neven-threadclaim uit deze analyse.

## Waarom −1 normaal neutraal is

**Initialisatie:** 4ff860 begint met ECX→EAX; nulvelden omvatten Cell+14/+18 (city/pop), +10 en andere gekoppelde pointers. 4ff885 schrijft `FF` uitsluitend naar Cell+0e. Dit is geen losse ongebruikte constructor: 505d1f–505d3b berekent het product van de drie wereldafmetingen; 505d64 pusht4ff860 als initcallback, 505d6d pusht stride34, en 505d72 roept725720 aan. Deze helper zet voor ieder element ECX=cel en roept op72575b de callback aan; daarna verhoogt zij het adres met stride. De celarray wordt op World+34 bewaard. 505e35–505e5e berekent precies index×34 en plaatst de celadressen in de World+1c-grid die516c10 leest.

**Verwijdering:** de complete korte routine516eb0–516f41 doorloopt diezelfde grid. 516ef0 leest Cell+0e signed; 516ef4 vergelijkt met de opgegeven owner; alleen bij gelijkheid pusht516efb `−1` en roept516f00 setter500a40 aan. Deze setter leest de laagste byte van het stackargument en schrijft op500a46 naar Cell+0e. Daardoor worden precies de cellen van deze opgegeven eigenaar teruggezet naar FF. Deze combinatie van normale initialisatie en een expliciete owner→−1-verwijdering levert de gevraagde neutraalbinding zonder EAX≤0 als bewijs te misbruiken.

Reset500d10/500d19 schrijft eveneens FF en ruimt gekoppelde bezettingsvelden op. De gridloop50e8c4–50e8d3 roept deze reset op via World+1c; deze aanvullende machinecode is consistent met dezelfde lege-celwaarde. De semantiek van zijn archivevoorwaarde is voor deze vraag niet nodig en is niet verder onderzocht.

**Civ0 en andere codes:** setter500a40 bewaart een civwaarde bytegewijs zonder offset of omzetting naar −1. De bestaande ownerwissel515eb0/515efc vergelijkt de signed bestaande byte met de oude inputowner en schrijft de nieuwe inputowner via dezelfde setter. Owner0 blijft daardoor numeriek0 en de getter retourneert0, onderscheiden van −1. Het project behandelt civ0 als barbaren; deze analyse reconstrueert die reeds afgesproken classificatie niet opnieuw. De oorspronkelijke getter kan elk signedbytepatroon teruggeven; initialisatie/verwijdering bewijzen exactFF als normale neutraalcode, niet alle negatieve waarden. Een andere negatieve code blijft UNKNOWN in het gekozen ontwerp. De volledige lijst mogelijke speciale/corrupte codes blokkeert deze ingreep niet en wordt niet als extra onderzoek gestart.

## Minimale bytes voor de overdracht

| VA | Raw offset | Bytes / betekenis |
| --- | --- | --- |
| 00745334 | 343934 | `80385300`: World+54-pointer533880 |
| 00533880 | 132c80 | `558bec8b450cb920e3a70050e86f06fdff8b0d70dda7006820e3a700e86f33feff5dc20800`: volledige wrapper |
| 00516c10 | 116010 | `558bec8b45088b491c560fbf50040fbf308b14910fbf40028b0cb25e8b14810fbe420e5dc20400`: volledige getter |
| 004ff885 | fec85 | `c6400eff`: normale init van ownerbyteFF |
| 00516efb | 1162fb | `6aff8b0c13e83b9bfeff`: expliciet push−1 en call500a40 |
| 00500a40 | ffe40 | `558bec8a450888410e5dc20400`: volledige ownerbytesetter |

Het eigen/neutraalbeleid kan nu concreet worden vastgelegd als exacte EAX−1-toelating naast de actuele normale eigen civwaarde. EAX0 is geen neutraaltoelating; een niet-eigen normale civwaarde blijft vreemd; andere negatieve/ongeldige waarden blijven UNKNOWN. Ownership is alleen deze ene veiligheidspoort: de overige bestaande type-, endpoint-, dreigings-, pad- en claimvoorwaarden uit het B4-voorstel blijven nodig.

Bewijsdumps:

- [GUID/vtable/wrapper](BINAIR/b4-owner-native-binding-interface.txt), SHA256 `d993943fb61a415758d3578873e96a619bafe8821bf79847c106d49942c7d474`.
- [Getter/initcallback/grid/verwijdering/schrijver](BINAIR/b4-owner-native-binding-cells.txt), SHA256 `4e5eb0a084c1cadada0757785b9c11cdba805099372de2263a3f45e64f59c86c`.

Gerichte A-opdracht afgerond. Geen resterende ownerencodingblokker of noodzakelijke gebruikersinput. Ontwerper kan dit ene contract aan B4 toevoegen; geen toegepaste verbetering of geïntegreerde produceracceptatie geclaimd. Geen vervolgonderzoek gestart.
