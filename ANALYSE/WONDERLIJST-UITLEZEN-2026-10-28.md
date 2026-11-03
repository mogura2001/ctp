# Wonderlijst: kleinste runtimeprojectie

28 oktober 2026, 17:41 CET. Doel4; gerichte A gereed. Geen spel, codewijziging, emulatie of test. Release-DLL eb6f58a7… opnieuw gehasht; genoemde originele vensters onveranderd. Dit is uitleg voor B, geen runtimebewijs.

| Beslisketen | Dekking | Restant |
| --- | --- | --- |
| Effectieve wondercategorie | Concrete layout AF | Echt uitlezen |
| Openingssymbolen | Read-only route AF | Begrensde projectie implementeren |
| Lijst naar productie | Meetroute bekend | Geschikte bestaande stad/save UNKNOWN |

## 1. Layout en identiteit

Hergebruik gevalideerde actor uit de bestaande reader: `planner=u32(actor+0x94)`, `aip=planner+0x20`; eis `u32(aip+0x800)==actor`. `list=u32(aip+0x7d0)`, `data=u32(list)`, `count=i32(list+4)`. Null en lege lijst afzonderlijk registreren; begrens count op200. Per record32bytes: doublegewicht op+0, signed engine-wonderindex op+8, categorie op+0x18 (wonder=-1). Bewijs: [switch](AIP-LAADWERKING.md), `build-goals-queue-ai-list-parser.txt` op2005f072/2005f0a3/2005f0aa/2005f160, `build-goals-queue-ai-core.txt` op20066513–20066542. Lees alleen stabiele, begrensde data; geen onbenoemde recordvelden interpreteren.

De parser resolveert de token via `actor+0x4c`, virtualslot0x30 (2005f094–2005f0a3). Een reeds gevalideerde directe engine-index→tokenreader ontbreekt. Label een index dus niet op basis van Wonder.txt-volgorde. Eerste lijstacceptatie kan count1/gewicht9100 en de gepinde één-tokenpartial aantonen; onafhankelijke native tokenbinding blijft expliciet open.

## 2. Kleinste hergebruik

Neem een eigen dunne projectiewrapper rond `PROEVEN/doel3/20261012-release-v1/Lees-Doel3.py`: behoud exact eb6-`trusted_binding`, `verify_loaded`, PID/executable/modules/creationtime en `stable_sample`; voeg alleen velden toe aan `observe_goal3`. Geen land-HOSTPLAN/gates kopiëren of permissies verbreden. Pin wrapper, originele reader/core, B2-manifest/payload en actuele tekstmanifesten. Geen oude bestanden wijzigen.

Openingssymbolen zijn doubles op symbol+8; `FliEngine=u32(actor+0xc4)`. Nieuwe gerichte disassemblage van GetSymbol200389e0–20038ad7 is bytegelijk origineel/release: `table=u32(engine)`, bucketarray=`u32(table+4)`, bucketcount=`i32(table+8)` (20038a82–20038a97); nodes bevatten nameptr+0, symbolptr+4, next+8 (20038aa4–20038ac3). Een begrensde bucket-/ketenscan op exacte namen vermijdt native GetSymbol-aanroepen. Eis unieke `opening_required`/`opening_completed`, 0/1 en complement, externe pointer symbol+0 nul, inputmask+0xc2 bit4 aanwezig; zie `opening-b2/build.py`. Limieten en visitedsets laten falen bij inconsistentie, niet onbeperkt doorzoeken.

## 3. Korte meetroute

Zelfde c6ba-T0: controle en kandidaat elk verse start/max1n; lees alle zeven actors op rustige grens. Daarna bestaande geschikte stad inspecteren: lege queue, Labyrinth beschikbaar, wonderthreshold/opslaguitzondering en bouwtijd/admission gehaald. Geen stad/bonus plaatsen. Echte City Status-productie apart bewijzen. Onbouwbaar→geen alternatief en opening_completed→eigen volledige lijst vragen afzonderlijke geschikte toestand; geschikte save momenteel UNKNOWN. Geen100beurtenvoorwaarde of nieuw uitleesframework. Overdracht naar B kan nu.
