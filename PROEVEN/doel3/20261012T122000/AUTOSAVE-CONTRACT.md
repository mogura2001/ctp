# Eigen autosave: versies behouden

12 oktober 2026 12:46 Europe/Amsterdam. Alleen bronvoorbereiding; deze functies nog niet uitgevoerd.

InstallStart maakt v??r de installatie een echte bytekopie/hash van het bestaande exacte CTP-proef/ctp_program/ctp/save/games/Julius/AUTOSAVE-Julius in de eigen armmap (AUTOSAVE.before + autosave-before.json). De eigen labelnaam moet dan ontbreken; er worden geen bestaande usernamed saves overschreven.

Na succesvolle actuele count0, v??r originele DLL/bestandsrestore, vergelijkt ArchiveAndRestoreAutosave de defaultautosave met het pre-runrecord. Ongewijzigd: rapporteer UNCHANGED_DEFAULT. Gewijzigd: bewaar de nieuwe bytes exact in eigen arm AUTOSAVE.after-N30 ?n in de spelmap DOEL3-20261012T122000-N30-AUTOSAVE. Beide kopie?n plus de nog aanwezige bron moeten dezelfde nieuwe hash hebben. Nogmaals count0/actuele bronhash, dan exact de originele autosavebackup naar het defaultpad terugzetten (of uitsluitend dit exacte pad verwijderen als het vooraf afwezig was). Beide resolvable doelpaden blijven exact in de expliciet genoemde Julius-map; geen recursive/Move/shell-built deletion.

De N30-save mag alleen met DLL eb6f58a7350f6fafd63336d0c335baa2d7d09db8ef62bc80f73db99395874890 worden geladen. De zichtbare bestandsnaam draagt N30; interne saveheader niet gewijzigd of gedecodeerd, we claimen geen bewezen nieuwe GUI-titel. Eigen autosave-archive.json registreert nieuwe hash/archief/zichtbaar label/required DLL/origineel herstel. Baseline gebruikt dezelfde bytes-behoudroute met ORIGINAL-label en originele DLL. Na herstel zijn named T0/quota?20/default-user-saves niet teruggezet of gewijzigd; profiel wordt niet gereverteerd. Geen claim dat alle saves bytegelijk zijn: er kan aantoonbaar een nieuwe autosave bestaan en die wordt onder versie bewaard.

Bij ontbrekende/gewijzigde backup, reeds bestaand label, gewijzigde bron tijdens archivering, ontbrekende defaultautosave na echte wijziging, onduidelijke processen of budgetstop: stop v??r DLL-herstel en meld de precieze toestand. Geen kill/retry/andere-save-rollback. Herstelbestanden blijven reviewbaar.
