									aidata\AIPs\README.TXT

   These files are all loaded into memory when the application starts up,
and then made active based on the .fli in aidata\*.fli .

Aipdef.h				- include file used by the .AIP files
aip_data.xls			- master spread sheet used to generate the .AIP files (Ctrl-M to make)
aipgen.xls				- used to create the science lists
sci advances.xls		- help figure out build lists for science personalities
mil advances.xls		- help figure out build lists for military personaliies



I. Personality AIPS: 

  what: defines basic personality state

  when: loaded at beginning of sequence

default.aip				- first AIP loaded

barbarian.aip
cleric.aip
milfew.aip				- 
milmany.aip				- 
scifew.aip				- 
scimany.aip				-
slaver.aip				-

II. Modes
		
citywall.aip

  what: stop building buildings, except defensive buildings, build
  units, and only do science for building walls.

  when: at the beginning of the game if AI is close to human


fallback.aip			- 
gather.aip				- 
getarmy.aip				- 
gohome.aip				- 
gotohim.aip				- 
highdist.aip			- 
impatient.aip			- 
islandsettle.aip		- 
killarmy.aip			- 
leavehome.aip			- 
limited_explore.aip		-
lowdist.aip				- 
manycaravans.aip		- 
masssettle.aip			-
naval.aip				- 
no_settle.aip			- 
nosally.aip				- 
noscience.aip			- 
patient.aip				- 
pulse.aip				- 
runfromhim.aip			- 
sally.aip				- 
supernaval.aip			-
survival_mode.aip		-
takecity.aip			-
transport.aip			-
twosettlers.aip			-
unlimited_explore.aip	-
verypatient.aip			-
yes_settle.aip			-

III. Test AIPs

test-attack.aip			-
test-defense.aip		-
test-harass.aip			-
test-seige.aip			-
test.aip				-
test2.aip				-
test3.aip				-

IV. Misc:

README.txt				- This file
