									aidata\README.TXT

   These files are all loaded into memory when the application starts up,
and then made active based on the behavior of the active .fli or the player index.


Structure:

		Personality
		    |
			V
		  Main{who}
   +------+--------------+--------+	
   |      |              |        |
   V	  V              V        V 
  I.    II.          III.       IV.
  Init  Begin{who}   Diplomacy  Endturn

		  |
		  V
   def_personality_who_{who}
		  +
		  |
		  V
  def_personality_{behavior clusters}
		  

Starting fli files for each personality:

personality.fli					- unused template for personalities
personalityDefault.fli			-
personalityBarbarians.fli		- first fli called for this personality
personalityCleric.fli			- first fli called for this personality
personalitySciFew.fli			- first fli called for this personality
personalitySciMany.fli			- first fli called for this personality
personalitySlaver.fli			- first fli called for this personality
personalityWarFew.fli			- first fli called for this personality
personalityWarMany.fli			- first fli called for this personality

Pointed to (one-for-one) by each personality fli:

main.fli						- unused template for personalities
mainBarbarians.fli				- first fli called for this personality
mainCleric.fli					- 
mainSciFew.fli					- 
mainSciMany.fli					- 
mainSlaver.fli					- 
mainWarFew.fli					- 
mainWarMany.fli					- 

I. Initialization

init.fli						- used, but not relevant.

  Defines who I am, what my science should be and how I should settle.
Also includes all of the shared inputs and all of the shared outputs.  

II.(a) Begin Turn (personality specific)

beginturn.fli					- unused template
beginturnBarbarians.fli			- 
beginturnCleric.fli				- 
beginturnSciFew.fli				- 
beginturnSciMany.fli			- 
beginturnSlaver.fli				- 
beginturnWarFew.fli				- 
beginturnWarMany.fli			- 

  Define personality files allow us to share the rest of the files:

def_personality_who_barbarian.fli - set flags to be the barbarian personality
def_personality_who_cleric.fli	  - set flags to be a cleric personality
def_personality_who_scientist.fli - set flags to be a scientist personality
def_personality_who_slaver.fli	  - set flags to be a slaver personality
def_personality_who_warrior.fli	  - set flags to be a warrior personality

def_personality_science_fast.fli  - set flags to build science slowly
def_personality_science_slow.fli  - set flags to build science slowly
def_personality_settle_dense.fli  - set flags to build cities close together
def_personality_settle_loose.fli  - set flags to build cities far apart personality

II.(b) Begin Turn (common)

  Setup input and output variables:

inputs.fli						- specific shared variables for strategic system
input_responses.fli				- all of the memory variables for dip system  
input_deals.fli					- all of the input variables for whether I have deals with opponent
outputs.fli						- 
output_aipnames.fli				- 

  Set the strategic variables, regarding the desireability to build mines or
farms, amount of gold to spend, WGF, etc.

set_budget.fli					- 
set_food_or_prod.fli			- 
set_food_or_prod_barbar.fli		- 
set_food_or_prod_sci.fli		- 
set_govern.fli					- 
set_govern_sci.fli				- 
set_govern_theocrat.fli			- 
set_govern_war.fli				- 
set_inst_priority.fli			- 
set_military_readiness.fli		- 
set_military_readiness_bar.fli	- 
set_pw.fli						- 
set_resource_desire.fli			- 
set_resource_desire_barbar.fli	- 
set_science_speed.fli			- 
set_science_speed_high.fli		- 
set_science_speed_slow.fli		- 
set_settle_dense.fli			- 
set_settle_loose.fli			- 
set_settle_density.fli			- 
set_wgf.fli						- 

  File for switching the aip files to produce the current aip state:

aiploader.fli					- 

III. Diplomacy

Pointed to (one-for-one) by each personality fli:

diplomacy.fli					- template for personalities

diplomacyBarbarians.fli			- 
diplomacypeacebackstab.fli		- call set_peace and set_backstab
diplomacypeaceloyal.fli			- 
diplomacywarbackstab.fli		- 
diplomacywarloyal.fli			- call set_loyal and set_war

Called by personality specific fli's:

diplomacy_set_average_trust.fli	- I will keep my word most of the time (unused)
diplomacy_set_backstab.fli		- I will backstab you
diplomacy_set_loyal.fli			- I will keep my word even if I hate you
diplomacy_set_opportunist.fli	- opposite of backstab (unused)
diplomacy_set_peace.fli			- I am peaceful
diplomacy_set_war.fli			- I am warlike

Systems of rules run once per opponent:

diplomacy_begin.fli				- do I like you or not

diplomacy_pre_incoming.fli		- reaction to messages sent to me
diplomacy_pre_outgoing.fli		- consideration of messages I want to send

diplomacy_accepted.fli			- reaction to my messages that were accepted
diplomacy_rejected.fli			- reaction to my messages that were rejected

IV. Endturn

endturn.fli						- used, but not relevant.

Miscellaneous files:

Text4.txt						- excerpt from fsdiplomacy
inputs_dip_incoming_mess.txt	-
strategic_ai_config.txt			- used to set threat map cell size (and other strategic map parameters)
aipplan.txt						- 

README.txt						- this file

