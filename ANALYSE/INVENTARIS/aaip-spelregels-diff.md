# Spelregelverschillen origineel - AAIP

## gamedata/Const.txt
```diff
diff --git "a/CTP-og\\ctp_data\\default\\gamedata\\Const.txt" "b/CTP-AAIP\\ctp_data\\default\\gamedata\\Const.txt"
index d15cab8..42f67d5 100644
--- "a/CTP-og\\ctp_data\\default\\gamedata\\Const.txt"
+++ "b/CTP-AAIP\\ctp_data\\default\\gamedata\\Const.txt"
@@ -17,7 +17,7 @@ MERIDIAND 60  # north of this is the equatioral region
 MERIDIANE 70  # north of this is south desert
 MERIDIANF 95  # north of this is the south mild, south is the south pole
 
-# the humidity controls the ditrabution of forest, jungle, swamp, grass, plains, desert
+# the humidity controls the distribution of forest, jungle, swamp, grass, plains, desert
 #	tundra and glacier
 # A bump map is randomly generated.  The bumps range from 0 to 100.  High bumps are
 #  wet terrain, low vallies are dry terrain. 
@@ -129,8 +129,8 @@ PACT_CAPTURE_CITY_EXPIRES	10	# number of rounds before this agreement expires
 # REWARD_CAPTURE_CITY_EXPIRES	10	# number of rounds before this agreement expires
 CEASE_FIRE_EXPIRES	10		# number of rounds before this agreement expires
 SHORT_CEASE_FIRE_EXPIRES	5	# number of rounds before any other agreement expires
-END_OF_GAME_YEAR_EARLY_WARNING	2900
-END_OF_GAME_YEAR				3000
+END_OF_GAME_YEAR_EARLY_WARNING	3100
+END_OF_GAME_YEAR				3200
 CAPTURE_CITY_FOR_GOLD_MULTIPLIER	100	# amount to multiply gold reward by
 PACT_END_POLLUTION_EXPIRES	50	# number of rounds before this agreement expires
 LEAVE_OUR_LANDS_EXPIRES		10	# number of rounds before this agreement expires
@@ -143,9 +143,9 @@ PATIENCE_LOST_THRESHOLD		5
 
 
 
-AI_GOAL_TIME_SLICE 25	# time in milliseconds for an AI frame
-AI_MAX_TIME_SLICE  250  # (in milliseconds)if the ai exceeds this time its turn is ended
-AI_TOTAL_TIME_SLICE 3000 # (in milliseconds) if the total time in time in the ai player  exceeds this its turn is ended
+AI_GOAL_TIME_SLICE 125	# time in milliseconds for an AI frame
+AI_MAX_TIME_SLICE  1250  # (in milliseconds)if the ai exceeds this time its turn is ended
+AI_TOTAL_TIME_SLICE 15000 # (in milliseconds) if the total time in time in the ai player  exceeds this its turn is ended
 
 ENTRENCHMENT_BONUS 0.5  # defense bonus for being entrenched
 PARADROP_DISTANCE 20 # how far away can paratroopers drop?
@@ -163,7 +163,7 @@ MAX_PARTY_CHANCE 0.5    # the chance of hearing gossip at a party where the
 GOSSIP_MAP_RADIUS 10    # When a map is revealed through gossip, a circle of
 		                # this radius appears
 HEAR_GOSSIP_CHANCE 0.02 # How likely a diplomat next to a capitol is to hear gossip
-FRANCHISE_EFFECT 0.5    # How much production a franchise steals
+FRANCHISE_EFFECT 0.35   # How much production a franchise steals
 TURNS_TO_SUE_FRANCHISE 0 # How many turns a lawsuit takes to expel a franchise
 
 SLAVER_ELITE_CHANCE 0.0 # Chance of a slaver becoming elite in a successful raid
@@ -225,7 +225,7 @@ CITY_GROWTH_COEFFICIENT 175          # Amount of food per citizen required to gr
 RIOT_LEVEL              73
 POWER_POINTS_TO_MATERIALS 1  # 1 power point can be converted to x materials
 MAX_AIRLIFT_STACK_SIZE 2
-GOLD_FROM_PIRACY 30
+GOLD_FROM_PIRACY 50
 NO_PIRACY_EXPIRES	5
 SPACE_LAUNCH_COST 1000
 SPACE_LAND_COST 1000
@@ -236,7 +236,7 @@ WORMHOLE_RETURN_TIME 5
 WORMHOLE_VISIBLE_TO_ALL_TURNS 5
 MAX_GOVERNMENT_CHANGE_TURNS 4
 
-POLLUTION_FORCES_ANARCHY 1000
+POLLUTION_FORCES_ANARCHY 2000
 FOOD_TO_POLLUTION_COEF 1.0			# pollution to food ratio produced by food vats
 
 
@@ -262,10 +262,10 @@ ATTACK_CONVERTER_UNHAPPINESS_AMOUNT -3.0
 MIN_START_DISTANCE_COEFFICIENT 0.45
 MAX_START_DISTANCE_COEFFICIENT 0.6
 MAX_SAME_TILES 4
-COMBAT_VETERAN_CHANCE 0.1
+COMBAT_VETERAN_CHANCE 0.15
 
 STOP_TRADE_ROUNDS 5
-LEAVE_OUR_LANDS_ROUNDS 3
+LEAVE_OUR_LANDS_ROUNDS 10
 REDUCE_POLLUTION_ROUNDS 10
 CAPTURE_CITY_ROUNDS 5
 END_POLLUTION_ROUNDS 10
@@ -280,14 +280,14 @@ CAPTURE_KILL_POP_CHANCE 1.0
 SCALED_POP_ANCIENT		10000
 SCALED_POP_RENAISSANCE		10000
 SCALED_POP_MODERN		100000
-SCALED_POP_GENETIC		1000000
-SCALED_POP_DIAMOND		5000000
+SCALED_POP_GENETIC		750000
+SCALED_POP_DIAMOND		1500000
 
 PIRACY_KILLS_TRADER_CHANCE 80
-UPRISING_CHANCE_PER_UNGUARDED_SLAVE 5
+UPRISING_CHANCE_PER_UNGUARDED_SLAVE 10
 MAX_DISBAND_SIZE 3
 MAX_REQUESTS_PER_PLAYER_PER_TURN 3
-SLAVES_PER_MILITARY_UNIT 3
+SLAVES_PER_MILITARY_UNIT 2
 MIN_ABSOLUTE_START_DISTANCE 5
 
 #
@@ -299,7 +299,7 @@ MAP_SIZE_MEDIUM		48	96	2
 MAP_SIZE_LARGE		64	128	2
 MAP_SIZE_GIGANTIC	70	140	2
 
-RAIL_LAUNCH_POLLUTION 50
+RAIL_LAUNCH_POLLUTION 5
 SPACE_FUEL_COST 5
 NON_SPACE_FUEL_COST 100
 
@@ -330,6 +330,6 @@ BIO_INFECTION_UNHAPPINESS -5
 MIN_ECO_PACT_VIOLATION_LEVEL 200
 NANO_INFECTION_TERRORIST_DEATH_CHANCE 0.25
 BIO_INFECTION_TERRORIST_DEATH_CHANCE 0.25
-FLOOD_CHANGES_COAST_TO_WATER_CHANCE 0.5
+FLOOD_CHANGES_COAST_TO_WATER_CHANCE 0.1
 AI_CHEAT_ECO_PACT_MIN 10
 AI_CHEAT_ECO_PACT_MAX 50
```
## gamedata/gw.txt
```diff
diff --git "a/CTP-og\\ctp_data\\default\\gamedata\\gw.txt" "b/CTP-AAIP\\ctp_data\\default\\gamedata\\gw.txt"
index 1062556..2a7c5dc 100644
--- "a/CTP-og\\ctp_data\\default\\gamedata\\gw.txt"
+++ "b/CTP-AAIP\\ctp_data\\default\\gamedata\\gw.txt"
@@ -7,11 +7,11 @@ GLOBAL_WARMING_TRIGGER
 	POLLUTION_TILE_FOREST			25		POLLUTION_TILE_TO_JUNGLE
 	POLLUTION_TILE_FOREST			5		POLLUTION_TILE_TO_PLAINS
 	POLLUTION_TILE_GLACIER			50		POLLUTION_TILE_TO_TUNDRA
-	POLLUTION_TILE_GRASSLAND		25		POLLUTION_TILE_TO_FOREST
-	POLLUTION_TILE_GRASSLAND		5		POLLUTION_TILE_TO_DESERT
+	POLLUTION_TILE_GRASSLAND		25		POLLUTION_TILE_TO_PLAINS
+	POLLUTION_TILE_GRASSLAND		5		POLLUTION_TILE_TO_FOREST
 	POLLUTION_TILE_HILL			25		POLLUTION_TILE_TO_FOREST
 	POLLUTION_TILE_JUNGLE			20		POLLUTION_TILE_TO_SWAMP
-	POLLUTION_TILE_JUNGLE			10		POLLUTION_TILE_TO_DESERT
+	POLLUTION_TILE_JUNGLE			10		POLLUTION_TILE_TO_PLAINS
 	POLLUTION_TILE_MOUNTAIN			0		POLLUTION_TILE_TO_MOUNTAIN
 	POLLUTION_TILE_BROWN_HILL		0		POLLUTION_TILE_TO_BROWN_HILL
 	POLLUTION_TILE_BROWN_MOUNTAIN		0		POLLUTION_TILE_TO_BROWN_MOUNTAIN
@@ -19,7 +19,7 @@ GLOBAL_WARMING_TRIGGER
 	POLLUTION_TILE_WHITE_MOUNTAIN		0		POLLUTION_TILE_TO_WHITE_MOUNTAIN
 	POLLUTION_TILE_PLAINS			25		POLLUTION_TILE_TO_GRASSLAND
 	POLLUTION_TILE_PLAINS			5		POLLUTION_TILE_TO_DESERT
-	POLLUTION_TILE_SWAMP			25		POLLUTION_TILE_TO_OCEAN
-	POLLUTION_TILE_SWAMP			5		POLLUTION_TILE_TO_JUNGLE
+	POLLUTION_TILE_SWAMP			25		POLLUTION_TILE_TO_JUNGLE
+	POLLUTION_TILE_SWAMP			5		POLLUTION_TILE_TO_PLAINS
 	POLLUTION_TILE_TUNDRA			25		POLLUTION_TILE_TO_PLAINS
 	}
```
## gamedata/hscore.txt
```diff
diff --git "a/CTP-og\\ctp_data\\default\\gamedata\\hscore.txt" "b/CTP-AAIP\\ctp_data\\default\\gamedata\\hscore.txt"
index 12025a4..15ee40e 100644
Binary files "a/CTP-og\\ctp_data\\default\\gamedata\\hscore.txt" and "b/CTP-AAIP\\ctp_data\\default\\gamedata\\hscore.txt" differ
```
## gamedata/profile.txt
```diff
diff --git "a/CTP-og\\ctp_data\\default\\gamedata\\profile.txt" "b/CTP-AAIP\\ctp_data\\default\\gamedata\\profile.txt"
index 5001ad3..96d0886 100644
--- "a/CTP-og\\ctp_data\\default\\gamedata\\profile.txt"
+++ "b/CTP-AAIP\\ctp_data\\default\\gamedata\\profile.txt"
@@ -1,3 +1,5 @@
+#This is the MAX HIGH Profile
+#
 # Number of players in the game, including the Barbarians must be a least 3 players and not more then 32, but with that many it will go verrrrry slowly and is not supported
 #
 NumPlayers= 6
@@ -17,7 +19,7 @@ UnitAnim= Yes
 GoodAnim= No
 TradeAnim= Yes
 WaterAnim= Yes
-LibraryAnim= No
+LibraryAnim= Yes
 WonderMovies= Yes
 BounceMessage= No
 MessageAdvice= Yes
@@ -71,9 +73,9 @@ CombatLog= No
 UseLeftClick= Yes
 ShowZoomedCombat= Yes
 UseFingerPrinting= No
-UseRedbookAudio= No
-RequireCD= No
-Prophylaxis= No
+UseRedbookAudio= Yes
+RequireCD= Yes
+Prophylaxis= Yes
 
 #
 # Screen Res Settings
@@ -123,8 +125,6 @@ DiplomacyLog= No
 #uncomment this to skip past an age 1-5 - debug exe only
 CheatAge= 0
 
-ShowTradeRoutes=Yes
-
 MapPlugin0=dll\\map\\geometric.dll
 MapPlugin1=dll\\map\\crater.dll
 MapPlugin2=dll\\map\\plasma2.dll
```
