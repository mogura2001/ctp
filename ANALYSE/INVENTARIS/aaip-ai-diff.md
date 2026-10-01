# Tekstverschillen origineel → AAIP

Alle gewijzigde AI-bestanden, met git-context. Geen semantische effectmeting.

## aidata/AIPs/cleric.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\cleric.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\cleric.aip"
index 31ea1e7..0c7123f 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\cleric.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\cleric.aip"
@@ -104,7 +104,7 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Land_Troops_Primary", 6000.0; 
 "Land_Strike_Troops_Primary", 6000.0; 
 "Land_Ranged_Troops_Primary", 6000.0; 
-"Sea_Troops_Primary", 5000.0; 
+"Sea_Troops_Primary", 6000.0; 
 "Air_Defender_Troops_Primary", 10000.0; 
 "Space_Defense_Troops_Primary", 10000.0; 
 // END PRIMARY  
@@ -114,27 +114,27 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Diplomatic_Troops_Core", 4500.0; 
 "Scout_Troops_Core", 2900.0; 
 "Spy_Troops_Core", 4500.0; 
-"Infector_Troops_Core", 4500.0; 
-"Ecoterrorist_Troops_Core", 4500.0; 
+"Infector_Troops_Core", 2500.0; 
+"Ecoterrorist_Troops_Core", 2500.0; 
 "Defend_Troops_Core", 3500.0; 
 "Assault_Troops_Core", 3500.0; 
 "Ranged_Troops_Core", 3500.0; 
-"Naval_Attack_Troops_Core", 1750.0; 
-"Naval_Defense_Troops_Core", 1750.0; 
+"Naval_Attack_Troops_Core", 3550.0; 
+"Naval_Defense_Troops_Core", 3550.0; 
 "Naval_Tranport_Troops_Core", 4501.0; 
 "Carrier_Naval_Transport_Troops_Core", 1650.0; 
-"Naval_Stealth_Troops_Core", 1750.0; 
+"Naval_Stealth_Troops_Core", 3550.0; 
 "Air_Attack_Troops_Core", 2000.0; 
 "Air_Bomber_Troops_Core", 2000.0; 
 "Air_Defender_Troops_Core", 2000.0; 
 "Space_Assault_Troops_Core", 2000.0; 
 "Space_Defense_Troops_Core", 2000.0; 
 "Space_Bomber_Troops_Core", 2000.0; 
-"Nuke_Troops_Core", 4500.0; 
-"Lawyer_Troops_Core", 5000.0; 
-"Branch_Troops_Core", 4500.0; 
-"Ad_Troops_Core", 4500.0; 
-"Terror_Troops_Core", 4500.0; 
+"Nuke_Troops_Core", 3500.0; 
+"Lawyer_Troops_Core", 3000.0; 
+"Branch_Troops_Core", 3000.0; 
+"Ad_Troops_Core", 3000.0; 
+"Terror_Troops_Core", 3500.0; 
 // END CORE  
 "Settler_Troops_Overflow", 3000.0; 
 "Cow_Troops_Overflow", 0.1; 
@@ -224,11 +224,11 @@ Build_List_Element Land_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_WARRIOR", 1.0;
+      "UNIT_WARRIOR", 0.5;
  "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 2.0;
- "UNIT_MUSKETEERS", 2.5;
- "UNIT_MACHINE_GUNNER", 1.0;
+ "UNIT_PIKEMEN", 1.3;
+ "UNIT_MUSKETEERS", 1.3;
+ "UNIT_MACHINE_GUNNER", 1.3;
  "UNIT_PLASMATICA", 1.0;
  "UNIT_LEVIATHAN", 0.1;
 #END_DATA  
@@ -242,12 +242,12 @@ Build_List_Element Land_Strike_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.5;
- "UNIT_SAMURAI", 0.5;
- "UNIT_KNIGHT", 0.5;
- "UNIT_CAVALRY", 0.5;
+ "UNIT_LEGION", 0.4;
+ "UNIT_SAMURAI", 0.4;
+ "UNIT_KNIGHT", 0.4;
+ "UNIT_CAVALRY", 0.4;
  "UNIT_TANK", 0.5;
- "UNIT_FUSION_TANK", 1.0;
+ "UNIT_FUSION_TANK", 0.8;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Land_Ranged_Troops_Primary  
@@ -259,9 +259,9 @@ Build_List_Element Land_Ranged_Troops_Primary[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "UNIT_GREEK_FIRE", 0.5;
- "UNIT_CANNON", 1.5;
- "UNIT_ARTILLERY", 1.0;
- "UNIT_BATTLEBOT", 1.25;
+ "UNIT_CANNON", 0.7;
+ "UNIT_ARTILLERY", 0.8;
+ "UNIT_BATTLEBOT", 1.0;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Sea_Troops_Primary  
@@ -273,11 +273,11 @@ Build_List_Element Sea_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", -1.0;
- "UNIT_LONGSHIP", -2.0;
- "UNIT_SHIP_OF_THE_LINE", -2.0;
- "UNIT_DESTROYER", -2.0;
- "UNIT_PLASMA_DESTROYER", -2.0;
+ "UNIT_TRIREMES", 0.25;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.30;
+ "UNIT_BATTLESHIP", 0.25;
+ "UNIT_PLASMA_DESTROYER", 0.30;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Air_Defender_Troops_Primary  
@@ -289,7 +289,7 @@ Build_List_Element Air_Defender_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_FIGHTER", -3.0;
+ "UNIT_FIGHTERS", -3.0;
  "UNIT_INTERCEPTORS", -3.0;
  "UNIT_STEALTH_FIGHTER", -3.0;
 #END_DATA  
@@ -331,8 +331,8 @@ Build_List_Element Slaver_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_CLERIC", -3.0;
- "UNIT_TELEVANGELIST", -3.0;
+      "UNIT_CLERIC", -1.0;
+ "UNIT_TELEVANGELIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Abolitionist_Troops_Core  
@@ -343,7 +343,7 @@ Build_List_Element Abolitionist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ABOLITIONIST", -3.0;
+ "UNIT_ABOLITIONIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Diplomatic_Troops_Core  
@@ -377,8 +377,8 @@ Build_List_Element Spy_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SPY", -3.0;
- "UNIT_CYBER_NINJA", -3.0;
+ "UNIT_SPY", -1.0;
+ "UNIT_CYBER_NINJA", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Infector_Troops_Core  
@@ -389,7 +389,7 @@ Build_List_Element Infector_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_INFECTOR", -2.0;
+ "UNIT_INFECTOR", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Ecoterrorist_Troops_Core  
@@ -400,7 +400,7 @@ Build_List_Element Ecoterrorist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_ECOTERRORIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Defend_Troops_Core  
@@ -411,14 +411,14 @@ Build_List_Element Defend_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 1.0;
- "UNIT_MUSKETEERS", 1.0;
- "UNIT_MACHINE_GUNNER", 1.0;
- "UNIT_PARATROOPER", 1.0;
- "UNIT_MARINES", 0.75;
+ "UNIT_HOPLITE", 0.7;
+ "UNIT_PIKEMEN", 0.7;
+ "UNIT_MUSKETEERS", 0.7;
+ "UNIT_MACHINE_GUNNER", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
  "UNIT_PLASMATICA", 0.25;
- "UNIT_LEVIATHAN", 0.75;
+ "UNIT_LEVIATHAN", 0.5;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Assault_Troops_Core  
@@ -447,10 +447,10 @@ Build_List_Element Ranged_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 0.75;
- "UNIT_CANNON", 0.75;
- "UNIT_ARTILLERY", 0.75;
- "UNIT_BATTLEBOT", 0.75;
+ "UNIT_GREEK_FIRE", 0.5;
+ "UNIT_CANNON", 0.5;
+ "UNIT_ARTILLERY", 0.5;
+ "UNIT_BATTLEBOT", 0.5;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Attack_Troops_Core  
@@ -461,11 +461,11 @@ Build_List_Element Naval_Attack_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", 0.15;
+ "UNIT_TRIREMES", 0.2;
  "UNIT_GREEK_FIRE_TRIREME", 0.15;
- "UNIT_LONGSHIP", 0.15;
- "UNIT_SHIP_OF_THE_LINE", 0.15;
- "UNIT_BATTLESHIP", 0.15;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.3;
+ "UNIT_BATTLESHIP", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Defense_Troops_Core  
@@ -476,8 +476,8 @@ Build_List_Element Naval_Defense_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_DESTROYER", 0.5;
- "UNIT_PLASMA_DESTROYER", 0.5;
+ "UNIT_DESTROYER", 0.3;
+ "UNIT_PLASMA_DESTROYER", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Transport_Troops_Core  
@@ -488,8 +488,8 @@ Build_List_Element Naval_Tranport_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TROOP_SHIP", 0.5;
- "UNIT_CRAWLER", 0.5;
+ "UNIT_TROOP_SHIP", 0.2;
+ "UNIT_CRAWLER", 0.2;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Carrier_Naval_Transport_Troops_Core  
@@ -522,7 +522,7 @@ Build_List_Element Naval_Stealth_Troops_Core[MAX_ELEMENTS];
 Build_List_Element Air_Attack_Troops_Core[MAX_ELEMENTS];  
 #DATA  
 //  
-//--------------------------------------------------------------------  
+//--------------------------------------------------------------------
  "UNIT_FIGHTER", 3.0;
  "UNIT_INTERCEPTORS", 3.0;
  "UNIT_STEALTH_FIGHTER", 3.0;
@@ -532,12 +532,12 @@ Build_List_Element Air_Attack_Troops_Core[MAX_ELEMENTS];
 //   
 // Defines the types of ground troops we want to be building  
 //  
-Build_List_Element Air_Bomber_Troops_Core[MAX_ELEMENTS];  
+Build_List_Element Air_Bomber_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
  "UNIT_BOMBER", 1.0;
- "UNIT_STEALTH_BOMBER", 1.0;
+ "UNIT_STEALTH_BOMBER", 1.0;  
 #END_DATA    
 ///////////////////////////////////////////////////////////////////////////////  
 // Air_Defender_Troops_Core  
@@ -606,7 +606,7 @@ Build_List_Element Lawyer_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LAWYER",  -10.0;
+ "UNIT_LAWYER",  -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Branch_Troops_Core  
@@ -617,7 +617,7 @@ Build_List_Element Branch_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_CORPORATE_BRANCH", -3.0;
+ "UNIT_CORPORATE_BRANCH", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Ad_Troops_Core  
@@ -628,7 +628,7 @@ Build_List_Element Ad_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SUBNEURAL_ADS", -3.0;
+ "UNIT_SUBNEURAL_ADS", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Terror_Troops_Core  
@@ -639,8 +639,8 @@ Build_List_Element Terror_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -3.0;
- "UNIT_INFECTOR", -3.0;
+ "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_INFECTOR", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Settler_Troops_Overflow  
@@ -922,13 +922,13 @@ Build_List_Element Wormhole_Probe_Troops[MAX_ELEMENTS];
 //  
 ///////////////////////////////////////////////////////////////////////////////  
 // Production threshholds 1.0 = top dog and 0.0 = loser  
-double Wonders_List_Threshhold =  0.8; 
-double Transportation_List_Threshhold =  0.6; 
+double Wonders_List_Threshhold =  0.6; 
+double Transportation_List_Threshhold =  0.4; 
 double Growth_List_Threshhold =  0.2; 
-double Happiness_List_Threshhold =  0.2; 
-double Production_List_Threshhold = 0.4; 
+double Happiness_List_Threshhold =  0.3; 
+double Production_List_Threshhold = 0.7; 
 double Gold_List_Threshhold =  0.4; 
-double Science_List_Threshhold =  0.2; 
+double Science_List_Threshhold =  0.5; 
 double Defense_List_Threshhold =  0.2; 
 double Miscellaneous_List_Threshhold =  0.0; 
 ///////////////////////////////////////////////////////////////////////////////  
@@ -940,15 +940,15 @@ Building_Build_List_Element Wonder_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
 "WONDER_WORMHOLE_DETECTOR", 20000.0; 
-"WONDER_STONEHENGE", 9250.0; 
+"WONDER_HAGIA_SOPHIA", 9350.0; //TLL 15/6/99 changed Hagia Sophia order to 2nd, increased priority
+"WONDER_STONEHENGE", 9100.0; 
 "WONDER_SPHINX", 9100.0; 
 "WONDER_LABRYINTH_OF_THE_MINOTAUR", 9250.0; 
 "WONDER_RAYAMANA", 9250.0; 
 "WONDER_PARTHENON", 9100.0; 
-"WONDER_I_CHING", 9100.0; 
+"WONDER_I_CHING", 9250.0; 
 "WONDER_THE_FORBIDDEN_CITY", 9100.0; 
 "WONDER_PHILOSOPHERS_STONE", 5000.0; 
-"WONDER_HAGIA_SOPHIA", 9250.0; 
 "WONDER_GUTTENBERGS_BIBLE", 9100.0; 
 "WONDER_EAST_INDIA_COMPANY", 9100.0; 
 "WONDER_GALILEOS_TELESCOPE", 9100.0; 
@@ -982,7 +982,7 @@ Building_Build_List_Element Transportation_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_AIRPORT", 7850.0; 
+"IMPROVE_AIRPORT", 9910.0; 
 "IMPROVE_RAIL_LAUNCHER", 7850.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
@@ -993,8 +993,9 @@ Building_Build_List_Element Growth_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 9000.0; 
-"IMPROVE_AQUEDUCT", 9000.0; 
+"IMPROVE_SILO", 9990.0; 
+"IMPROVE_AQUEDUCT", 9980.0; 
+"IMPROVE_BEEF_VAT", 7930.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1005,19 +1006,18 @@ Building_Build_List_Element Happiness_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "IMPROVE_MIND_CONTROL_EMITTER", 8999.0;
- "IMPROVE_TEMPLE", 8999.0;
- "IMPROVE_THEATER", 8999.0;
- "IMPROVE_CIRCUS", 8999.0;
- "IMPROVE_HOSPITAL", 7990.0;
- "IMPROVE_CATHEDRAL", 8999.0;
- "IMPROVE_MOVIE_PALACE", 8999.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_WATER_TRANSFORMER", 8999.0;
- "IMPROVE_HOUSE_OF_FREEZING", 8999.0;
- "IMPROVE_BODY_EXCHANGE", 8999.0;
- "IMPROVE_ARCOLOGIES", 8999.0;
+ "IMPROVE_TEMPLE", 9960.0;
+ "IMPROVE_THEATER", 9950.0;
+ "IMPROVE_CIRCUS", 9940.0;
+ "IMPROVE_HOSPITAL", 9930.0;
+ "IMPROVE_CATHEDRAL", 8960.0;
+ "IMPROVE_MOVIE_PALACE", 8949.0;
+ "IMPROVE_DRUG_STORE", 9920.0;
+ "IMPROVE_WATER_TRANSFORMER", 8939.0;
+ "IMPROVE_BODY_EXCHANGE", 8829.0;
+ "IMPROVE_ARCOLOGIES", 8919.0;
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+///////////////////////////////////////////////////////////////////////////////  N..
 //  
 // Production_List  
 //   
@@ -1025,17 +1025,18 @@ Building_Build_List_Element Production_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "IMPROVE_NANITE_FACTORY", 7990.0;
- "IMPROVE_MILL", 7990.0;
- "IMPROVE_FACTORY", 7990.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_POPULATION_MONITOR", 8980.0; 
- "IMPROVE_FUSION_PLANT", 10000.0;
- "IMPROVE_RECYCLING_PLANT", 9000.0;
- "IMPROVE_NUCLEAR_PLANT", 7990.0;
- "IMPROVE_ROBOTIC_PLANT", 7990.0;
- "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 7990.0;
- "IMPROVE_ZERO_EMISSION_VEHICLES", 8000.0;
+ "IMPROVE_MILL", 8960.0;
+ "IMPROVE_DRUG_STORE", 8950.0;
+ "IMPROVE_FACTORY", 5980.0;
+ "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 5890.0;
+ "IMPROVE_POPULATION_MONITOR", 5880.0; 
+ "IMPROVE_NUCLEAR_PLANT", 5990.0;
+ "IMPROVE_ROBOTIC_PLANT", 2890.0;
+ "IMPROVE_RECYCLING_PLANT", 6000.0;
+ "IMPROVE_ZERO_EMISSION_VEHICLES", 4990.0;
+ "IMPROVE_OIL_REFINERY", 3000.0;
+ "IMPROVE_FUSION_PLANT", 4000.0;
+ "IMPROVE_NANITE_FACTORY", 4990.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1045,13 +1046,12 @@ Building_Build_List_Element Gold_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_BAZAAR", 7980.0; 
-"IMPROVE_BANK", 7980.0; 
+"IMPROVE_BAZAAR", 9900.0; 
+"IMPROVE_BANK", 8990.0; 
 "IMPROVE_CITY_CLOCK", 7990.0; 
-"IMPROVE_TELEVISION", 7980.0; 
-"IMPROVE_AIRPORT", 7850.0; 
-"IMPROVE_HOUSE_OF_FREEZING", 8999.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7980.0; 
+"IMPROVE_TELEVISION", 6930.0; 
+"IMPROVE_AIRPORT", 8850.0; 
+"IMPROVE_HOUSE_OF_FREEZING", 6920.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1061,11 +1061,11 @@ Building_Build_List_Element Science_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_ACADEMY", 7950.0; 
+"IMPROVE_ACADEMY", 8980.0; 
+"IMPROVE_LIBRARY", 8970.0; 
 "IMPROVE_UNIVERSITY", 7950.0; 
-"IMPROVE_LIBRARY", 7950.0; 
-"IMPROVE_COMPUTER_CENTER", 7950.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7950.0; 
+"IMPROVE_COMPUTER_CENTER", 7850.0; 
+"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 6950.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1075,12 +1075,12 @@ Building_Build_List_Element Defense_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_CITY_WALLS", 7950.0; 
+"IMPROVE_CITY_WALLS", 9970.0; 
 "IMPROVE_SDI", 7950.0; 
 "IMPROVE_BIO_WARFARE_FILTERS", 7950.0; 
-"IMPROVE_FORCEFIELD", 7950.0; 
+"IMPROVE_FORCEFIELD", 8950.0; 
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+/////////////////////////////////////////////////////////////////////////////// N.. 
 //  
 // Miscellaneous_List  
 //   
@@ -1088,11 +1088,11 @@ Building_Build_List_Element Miscellaneous_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 8000.0; 
-"IMPROVE_CITY_WALLS", 7980.0; 
-"IMPROVE_BAZAAR", 8500.0; 
-"IMPROVE_COURTHOUSE", 7980.0; 
-"IMPROVE_POPULATION_MONITOR", 7980.0; 
+"IMPROVE_SILO", 9900.0; 
+"IMPROVE_CITY_WALLS", 9500.0; 
+"IMPROVE_BAZAAR", 9000.0; 
+"IMPROVE_COURTHOUSE", 8500.0; 
+"IMPROVE_POPULATION_MONITOR", 8000.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1111,42 +1111,46 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "ADVANCE_THEOCRACY"; 
- "ADVANCE_RELIGION"; 
  "ADVANCE_MINING"; 
+ "ADVANCE_STONE_WORKING"; 
+ "ADVANCE_ASTRONOMY";
+ "ADVANCE_RELIGION"; 
+ "ADVANCE_GEOMETRY"; 
  "ADVANCE_SHIP_BUILDING"; 
  "ADVANCE_AGRICULTURE"; 
  "ADVANCE_TOOLMAKING"; 
- "ADVANCE_ASTRONOMY"; 
  "ADVANCE_BRONZE_WORKING"; 
- "ADVANCE_STONE_WORKING"; 
+ "ADVANCE_MONARCHY"; 
+ "ADVANCE_IRON_WORKING"; 
+ "ADVANCE_ALCHEMY"; 
+ "ADVANCE_ENGINEERING";
  "ADVANCE_PHILOSOPHY"; 
  "ADVANCE_JURISPRUDENCE"; 
  "ADVANCE_WRITING"; 
  "ADVANCE_DOMESTICATION"; 
  "ADVANCE_CLASSICAL_EDUCATION"; 
- "ADVANCE_GEOMETRY"; 
  "ADVANCE_AGRICULTURAL_REVOLUTION"; 
  "ADVANCE_TRADE"; 
  "ADVANCE_BUREAUCRACY"; 
  "ADVANCE_PERSPECTIVE"; 
- "ADVANCE_ENGINEERING"; 
  "ADVANCE_BANKING"; 
- "ADVANCE_PRINTING_PRESS"; 
  "ADVANCE_GUNPOWDER"; 
- "ADVANCE_ALCHEMY"; 
- "ADVANCE_IRON_WORKING"; 
  "ADVANCE_STIRRUP"; 
  "ADVANCE_OCEAN_FARING"; 
  "ADVANCE_HULL_MAKING"; 
  "ADVANCE_CANNON_MAKING"; 
- "ADVANCE_AGE_OF_REASON"; 
  "ADVANCE_MECHANICAL_CLOCK"; 
+ "ADVANCE_OPTICS";
+ "ADVANCE_PRINTING_PRESS";
  "ADVANCE_INDUSTRIAL_REVOLUTION"; 
+ "ADVANCE_AGE_OF_REASON";
  "ADVANCE_MACHINE_TOOLS"; 
+ "ADVANCE_CAVALRY_TACTICS"; 
  "ADVANCE_RAILROAD"; 
  "ADVANCE_ECONOMICS"; 
  "ADVANCE_NATIONALISM"; 
  "ADVANCE_ELECTRICITY"; 
+ "ADVANCE_PHYSICS"; 
  "ADVANCE_COMPUTER"; 
  "ADVANCE_CORPORATION"; 
  "ADVANCE_DEMOCRACY"; 
@@ -1154,15 +1158,12 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_OIL_REFINING"; 
  "ADVANCE_CHEMISTRY"; 
  "ADVANCE_MEDICINE"; 
- "ADVANCE_OPTICS"; 
  "ADVANCE_MASS_PRODUCTION"; 
  "ADVANCE_ROBOTICS"; 
  "ADVANCE_AERODYNAMICS"; 
- "ADVANCE_PHYSICS"; 
  "ADVANCE_CONSUMER_ELECTRONICS"; 
  "ADVANCE_ELECTRIFICATION"; 
  "ADVANCE_TANK_WARFARE"; 
- "ADVANCE_CAVALRY_TACTICS"; 
  "ADVANCE_ENVIRONMENTALISM"; 
  "ADVANCE_SEA_COLONIES"; 
  "ADVANCE_ARCOLOGIES"; 
@@ -1170,7 +1171,7 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_ADVANCED_COMPOSITES"; 
  "ADVANCE_SUPERCONDUCTOR"; 
  "ADVANCE_SPACE_FLIGHT"; 
- "ADVANCE_JET_PROPULSION"; 
+ "ADVANCE_JET_PROPULSION";
  "ADVANCE_STEEL"; 
  "ADVANCE_QUANTUM_MECHANICS"; 
  "ADVANCE_ROCKETRY"; 
@@ -1193,7 +1194,7 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_TECHNOCRACY"; 
  "ADVANCE_AI_SURVEILLANCE"; 
  "ADVANCE_NANOASSEMBLY"; 
- "ADVANCE_WORMHOLES"; 
+ "ADVANCE_WORMHOLES";
  "ADVANCE_SPACE_COLONIES"; 
  "ADVANCE_INTELLIGENT_MATERIALS"; 
  "ADVANCE_WILDERNESS_PRESERVATION_ACT"; 
@@ -1205,7 +1206,6 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_CITY_STATE"; 
  "ADVANCE_COMMUNISM"; 
  "ADVANCE_FASCISM"; 
- "ADVANCE_MONARCHY"; 
  "ADVANCE_CLOAKING"; 
  "ADVANCE_ALIEN_ARCHEOLOGY"; 
 #END_DATA  
```

## aidata/AIPs/default.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\default.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\default.aip"
index 72c99b0..e3c2416 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\default.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\default.aip"
@@ -25,7 +25,7 @@ double fzwonder_priority_modifier = 19997500.0;
 double build_end_game_object_priority = 20000000.0; 
 double build_capitalization_priority = 20000000.0; 
 double settle_priority = 17000000.0; 
-double sally_priority = 0.0; 
+double sally_priority = 500000.0; // WW from 0.0
 double defend_priority = 457000.0; 
 double seige_priority = 405000.0; 
 double attack_troops_priority = 405000.0; 
@@ -42,22 +42,22 @@ double expel_priority = 7000.0;
 double chokepoint_priority = 1000.0; 
 /// begin special unit bids  
 double convert_priority = 1000000.0; 
-double bioterror_priority = 1500000.0; 
-double nanoattack_priority = 1500000.0; 
+double bioterror_priority = 100000.0; //WW from 1,500,000
+double nanoattack_priority = 100000.0; //WW from 1,500,000 
 double enslave_priority = 1000000.0; 
-double plant_nuke_priority = 1000000.0; 
-double create_park_priority = 1000000.0; 
+double plant_nuke_priority = 100000.0; //WW from 1,000,000 
+double create_park_priority = 100000.0; //WW from 1,000,000 
 double underground_railway_priority = 1000000.0; 
 double establish_embassy_priority = 1000000.0; 
-double franchising_priority = 2000000.0; 
+double franchising_priority = 200000.0; //WW from 2,000,000 
 double assasinate_ruler_priority = 1000000.0; 
 double steal_technology_priority = 1000000.0; 
 double injoin_priority = 1000000.0; 
-double incite_revolution_priority = 2000000.0; 
+double incite_revolution_priority = 1000000.0; //WW from 2,000,000 
 double cause_unhappiness_priority = 1000000.0; 
-double nuke_city_priority = 1000000.0; 
+double nuke_city_priority = 400000.0; //WW from 1,000,000 
 double reform_city_priority = 1000000.0; 
-double sue_franchise_priority = 2000000.0; 
+double sue_franchise_priority = 20000000.0; //WW increased from 2,000,000 
 double probe_wormhole_priority = 1000000.0; 
 double bonus_food_priority = 0.0; 
 double defuse_mines_priority = 0.0; 
@@ -120,7 +120,7 @@ double captured_city_modifier = 100000;
 // FORCE MATCHING  
 double min_defense_matching_force_ratio =  1.2; 
 double min_attack_matching_force_ratio =  1.2; 
-int num_city_defenders = 1; 
+int num_city_defenders = 2; //WW from 1
 // MAX BUILD TURNS  
 int max_build_building_rounds = 15.0; 
 int max_build_unit_rounds = 20.0; 
@@ -223,7 +223,7 @@ int max_build_wonder_rounds = 50.0;
 #define MAX_EXEC_UNDERGROUND_RAILWAY_GOALS -2 
 #define MAX_EXEC_NUKE_CITY_GOALS 0.1 
 #define MAX_EXEC_ENSLAVE_GOALS 0 
-#define MAX_EXEC_REFORM_CITY_GOALS 0.5 
+#define MAX_EXEC_REFORM_CITY_GOALS 0.25 //Changed by TLL 14/6/99
 #define MAX_EXEC_SUE_FRANCHISE_GOALS 0.5 
 #define MAX_EXEC_PROBE_WORMHOLE_GOALS -1 
 #define MAX_EXEC_WANDER_GOALS -1 
@@ -292,9 +292,9 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Space_Defense_Troops_Core", 2000.0; 
 "Space_Bomber_Troops_Core", 2000.0; 
 "Nuke_Troops_Core", 4500.0; 
-"Lawyer_Troops_Core", 5000.0; 
-"Branch_Troops_Core", 4500.0; 
-"Ad_Troops_Core", 4500.0; 
+"Lawyer_Troops_Core", 4000.0; 
+"Branch_Troops_Core", 4000.0; 
+"Ad_Troops_Core", 4000.0; 
 "Terror_Troops_Core", 4500.0; 
 // END CORE  
 "Settler_Troops_Overflow", 1501.0; 
@@ -385,11 +385,11 @@ Build_List_Element Land_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_WARRIOR", 1.0;
- "UNIT_HOPLITE", 1.0;
+      "UNIT_WARRIOR", 0.5;
+ "UNIT_HOPLITE", 1.5;
  "UNIT_PIKEMEN", 2.0;
- "UNIT_MUSKETEERS", 2.5;
- "UNIT_MACHINE_GUNNER", 1.0;
+ "UNIT_MUSKETEERS", 2.0;
+ "UNIT_MACHINE_GUNNER", 1.5;
  "UNIT_PLASMATICA", 1.0;
  "UNIT_LEVIATHAN", 0.1;
 #END_DATA  
@@ -625,9 +625,9 @@ Build_List_Element Naval_Attack_Troops_Core[MAX_ELEMENTS];
 //--------------------------------------------------------------------  
  "UNIT_TRIREMES", 0.15;
  "UNIT_GREEK_FIRE_TRIREME", 0.15;
- "UNIT_LONGSHIP", 0.15;
- "UNIT_SHIP_OF_THE_LINE", 0.15;
- "UNIT_BATTLESHIP", 0.15;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.25;
+ "UNIT_BATTLESHIP", 0.25;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Defense_Troops_Core  
@@ -849,7 +849,7 @@ Build_List_Element Scout_Troops_Overflow[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_WARRIOR", 0.75;
+ "UNIT_WARRIOR", 0.1;
  "UNIT_DIPLOMAT", 0.1;
  "UNIT_SPY", 0.75;
  "UNIT_SPY_PLANE", 0.75;
@@ -1104,6 +1104,8 @@ Building_Build_List_Element Wonder_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
 "WONDER_WORMHOLE_DETECTOR", 20000.0; 
+"X_LAB",  20000.0;  
+"EMBRYO_TANK",  20000.0;  
 "WONDER_STONEHENGE", 10000.0; 
 "WONDER_SPHINX", 9100.0; 
 "WONDER_LABRYINTH_OF_THE_MINOTAUR", 9100.0; 
@@ -1214,7 +1216,6 @@ Building_Build_List_Element Gold_List[MAX_ELEMENTS];
 "IMPROVE_TELEVISION", 7980.0; 
 "IMPROVE_AIRPORT", 7850.0; 
 "IMPROVE_HOUSE_OF_FREEZING", 8999.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7980.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1225,8 +1226,8 @@ Building_Build_List_Element Science_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
 "IMPROVE_ACADEMY", 7950.0; 
-"IMPROVE_UNIVERSITY", 7950.0; 
 "IMPROVE_LIBRARY", 7950.0; 
+"IMPROVE_UNIVERSITY", 7950.0; 
 "IMPROVE_COMPUTER_CENTER", 7950.0; 
 "IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7950.0; 
 #END_DATA  
@@ -1253,7 +1254,7 @@ Building_Build_List_Element Miscellaneous_List[MAX_ELEMENTS];
 //--------------------------------------------------------------------  
 "IMPROVE_SILO", 7950.0; 
 "IMPROVE_CITY_WALLS", 7980.0; 
-"IMPROVE_BAZAAR", 8500.0; 
+"IMPROVE_BAZAAR", 8400.0; 
 "IMPROVE_COURTHOUSE", 7980.0; 
 "IMPROVE_POPULATION_MONITOR", 7980.0; 
 #END_DATA  
@@ -1265,8 +1266,6 @@ Building_Build_List_Element End_Game_Object_List[MAX_ELEMENTS];
 #DATA    
 //    
 //--------------------------------------------------------------------    
-"X_LAB",  20000.0;  
-"EMBRYO_TANK",  20000.0;  
 "CONTAINMENT_FIELD", 20000.0;  
 "ET_COMMUNICATION_DEVICE",  20000.0;  
 "GENE_SEQUENCER",  20000.0;  
@@ -1326,6 +1325,7 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_MACHINE_TOOLS"; 
  "ADVANCE_COMPUTER"; 
  "ADVANCE_ELECTRICITY"; 
+ "ADVANCE_PHYSICS"; 
  "ADVANCE_RAILROAD"; 
  "ADVANCE_ECONOMICS"; 
  "ADVANCE_NATIONALISM"; 
@@ -1350,50 +1350,49 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_JET_PROPULSION"; 
  "ADVANCE_ROCKETRY"; 
  "ADVANCE_AERODYNAMICS"; 
- "ADVANCE_PHYSICS"; 
  "ADVANCE_PHARMACEUTICALS"; 
  "ADVANCE_CONSUMER_ELECTRONICS"; 
  "ADVANCE_ROBOTICS"; 
- "ADVANCE_GENETICS"; 
+ "ADVANCE_GENETICS";
  "ADVANCE_AGE_OF_REASON"; 
  "ADVANCE_QUANTUM_MECHANICS"; 
  "ADVANCE_SPACE_FLIGHT"; 
  "ADVANCE_ENVIRONMENTALISM"; 
  "ADVANCE_GLOBAL_COMMUNICATIONS_NETWORK"; 
- "ADVANCE_ADVANCED_COMPOSITES"; 
+ "ADVANCE_ADVANCED_COMPOSITES";
+ "ADVANCE_SEA_COLONIES"; 
+ "ADVANCE_SUPERCONDUCTOR"; 
  "ADVANCE_MULTINATIONAL_REPUBLIC"; 
  "ADVANCE_AI_SURVEILLANCE"; 
  "ADVANCE_SUBNEURAL_ADS"; 
  "ADVANCE_INTELLIGENT_MATERIALS"; 
  "ADVANCE_FUEL_CELLS"; 
  "ADVANCE_PERSONAL_ENCRYPTION"; 
- "ADVANCE_WORMHOLES"; 
  "ADVANCE_FUSION"; 
  "ADVANCE_UNIFIED_FIELD_THEORY"; 
  "ADVANCE_TECHNOCRACY"; 
- "ADVANCE_SUPERCONDUCTOR"; 
  "ADVANCE_HUMAN_CLONING"; 
  "ADVANCE_GLOBAL_DEFENSE_INITIATIVE"; 
  "ADVANCE_DEMOCRACY"; 
  "ADVANCE_ARCOLOGIES"; 
- "ADVANCE_SEA_COLONIES"; 
  "ADVANCE_SPACE_COLONIES"; 
  "ADVANCE_GENETIC_TAILORING"; 
+ "ADVANCE_ULTRAPRESSURE_MACHINERY";
+ "ADVANCE_WORMHOLES"; 
  "ADVANCE_ZERO_G_MANUFACTURING"; 
  "ADVANCE_CRYONICS"; 
  "ADVANCE_MIND_CONTROL"; 
- "ADVANCE_ULTRAPRESSURE_MACHINERY"; 
  "ADVANCE_ASTEROID_MINING"; 
  "ADVANCE_NANOASSEMBLY"; 
  "ADVANCE_WILDERNESS_PRESERVATION_ACT"; 
  "ADVANCE_GAIA_THEORY"; 
  "ADVANCE_VIRTUAL_DEMOCRACY"; 
  "ADVANCE_CITY_STATE"; 
+ "ADVANCE_CLOAKING";
  "ADVANCE_ALIEN_ARCHEOLOGY"; 
  "ADVANCE_NEURAL_SILICON_INTERFACE"; 
  "ADVANCE_LIFE_EXTENSION"; 
  "ADVANCE_COMMUNISM"; 
  "ADVANCE_ECOTOPIA"; 
  "ADVANCE_THEOCRACY"; 
- "ADVANCE_CLOAKING"; 
 #END_DATA  
```

## aidata/AIPs/defend_normal.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\defend_normal.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\defend_normal.aip"
index 5b4c189..12c3cda 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\defend_normal.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\defend_normal.aip"
@@ -5,4 +5,4 @@
 // Specifies the behavior of the Strategic Combat system for Civ  
 ///////////////////////////////////////////////////////////////////////////////  
 #include "aipdef.h"   
-int num_city_defenders = 1; 
+int num_city_defenders = 2; 
```

## aidata/AIPs/fallback.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\fallback.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\fallback.aip"
index e501526..bb48bc4 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\fallback.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\fallback.aip"
@@ -16,8 +16,8 @@
 // for testing purposes, I've put the ability specify any or all of them to  
 // be changed in a big fat wad when the AIP switches.  
     
-double build_buildings_priority = 20000000.0; 
-double build_troops_priority = 20000000.0; 
+double build_buildings_priority = 19998000.0; 
+double build_troops_priority = 20002000.0; 
 double seige_priority = 405000.0; 
 double attack_troops_priority = 405000.0; 
 double bombard_priority = 407000.0; 
```

## aidata/AIPs/gather.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\gather.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\gather.aip"
index 92e3604..f22f165 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\gather.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\gather.aip"
@@ -60,6 +60,7 @@ double distance_from_unit_priority_modifier = -500.0;
 // FORCE MATCHING  
 double min_defense_matching_force_ratio =  1.2; 
 double min_attack_matching_force_ratio =  2.4; 
+int num_city_defenders = 1; //WW inserted
 #define MAX_EVAL_SEIGE_GOALS -15 
 #define MAX_EVAL_EXPLORE_GOALS -15 
    
```

## aidata/AIPs/getarmy.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\getarmy.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\getarmy.aip"
index 86b0209..b7c8a50 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\getarmy.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\getarmy.aip"
@@ -40,38 +40,38 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Air_Defender_Troops_Primary", 10000.0; 
 "Space_Defense_Troops_Primary", 10000.0; 
 // END PRIMARY  
-"Settler_Troops_Core", 3500.0; 
+"Settler_Troops_Core", 3000.0; 
 "Slaver_Troops_Core", 6001; 
 "Abolitionist_Troops_Core", 6001; 
-"Diplomatic_Troops_Core", 0.1; 
-"Scout_Troops_Core", 0.1; 
-"Spy_Troops_Core", 0.1; 
-"Infector_Troops_Core", 0.1; 
-"Ecoterrorist_Troops_Core", 0.1; 
+"Diplomatic_Troops_Core", 4500.0; 
+"Scout_Troops_Core", 2900.0; 
+"Spy_Troops_Core", 4500.0; 
+"Infector_Troops_Core", 2500.0; 
+"Ecoterrorist_Troops_Core", 2500.0; 
 "Defend_Troops_Core", 3500.0; 
 "Assault_Troops_Core", 3500.0; 
 "Ranged_Troops_Core", 3500.0; 
-"Naval_Attack_Troops_Core", 1750.0; 
-"Naval_Defense_Troops_Core", 1750.0; 
-"Naval_Tranport_Troops_Core", 4501.0; 
+"Naval_Attack_Troops_Core", 3550.0; 
+"Naval_Defense_Troops_Core", 3550.0; 
+"Naval_Tranport_Troops_Core", 3550.0; 
 "Carrier_Naval_Transport_Troops_Core", 1650.0; 
-"Naval_Stealth_Troops_Core", 1750.0; 
+"Naval_Stealth_Troops_Core", 3550.0; 
 "Air_Attack_Troops_Core", 2000.0; 
 "Air_Bomber_Troops_Core", 2000.0; 
 "Air_Defender_Troops_Core", 2000.0; 
 "Space_Assault_Troops_Core", 2000.0; 
 "Space_Defense_Troops_Core", 2000.0; 
 "Space_Bomber_Troops_Core", 2000.0; 
-"Nuke_Troops_Core", 4500.0; 
-"Lawyer_Troops_Core", 5000.0; 
-"Branch_Troops_Core", 4500.0; 
-"Ad_Troops_Core", 4500.0; 
-"Terror_Troops_Core", 4500.0; 
+"Nuke_Troops_Core", 3500.0; 
+"Lawyer_Troops_Core", 3000.0; 
+"Branch_Troops_Core", 3000.0; 
+"Ad_Troops_Core", 3000.0; 
+"Terror_Troops_Core", 3500.0; 
 // END CORE  
 "Settler_Troops_Overflow", 3000.0; 
 "Cow_Troops_Overflow", 0.1; 
-"Slaver_Troops_Overflow", 0.1; 
-"Scout_Troops_Overflow", 0.1; 
+"Slaver_Troops_Overflow", 1500.0; 
+"Scout_Troops_Overflow", 1500.0; 
 "Defend_Troops_Overflow", 1500.0; 
 "Assault_Troops_Overflow", 1500.0; 
 "Ranged_Troops_Overflow", 1500.0; 
@@ -156,11 +156,11 @@ Build_List_Element Land_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_WARRIOR", 1.0;
+ "UNIT_WARRIOR", 0.5;
  "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 2.0;
- "UNIT_MUSKETEERS", 2.5;
- "UNIT_MACHINE_GUNNER", 1.0;
+ "UNIT_PIKEMEN", 1.3;
+ "UNIT_MUSKETEERS", 1.3;
+ "UNIT_MACHINE_GUNNER", 1.3;
  "UNIT_PLASMATICA", 1.0;
  "UNIT_LEVIATHAN", 0.1;
 #END_DATA  
@@ -174,12 +174,12 @@ Build_List_Element Land_Strike_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.5;
- "UNIT_SAMURAI", 0.5;
- "UNIT_KNIGHT", 0.5;
- "UNIT_CAVALRY", 0.5;
+ "UNIT_LEGION", 0.4;
+ "UNIT_SAMURAI", 0.4;
+ "UNIT_KNIGHT", 0.4;
+ "UNIT_CAVALRY", 0.4;
  "UNIT_TANK", 0.5;
- "UNIT_FUSION_TANK", 1.0;
+ "UNIT_FUSION_TANK", 0.8;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Land_Ranged_Troops_Primary  
@@ -191,9 +191,9 @@ Build_List_Element Land_Ranged_Troops_Primary[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "UNIT_GREEK_FIRE", 0.5;
- "UNIT_CANNON", 1.5;
- "UNIT_ARTILLERY", 1.0;
- "UNIT_BATTLEBOT", 1.25;
+ "UNIT_CANNON", 0.7;
+ "UNIT_ARTILLERY", 0.8;
+ "UNIT_BATTLEBOT", 1.0;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Sea_Troops_Primary  
@@ -205,11 +205,11 @@ Build_List_Element Sea_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", -1.0;
- "UNIT_LONGSHIP", -2.0;
- "UNIT_SHIP_OF_THE_LINE", -2.0;
- "UNIT_DESTROYER", -2.0;
- "UNIT_PLASMA_DESTROYER", -2.0;
+ "UNIT_TRIREMES", 0.25;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.30;
+ "UNIT_DESTROYER", 0.25;
+ "UNIT_PLASMA_DESTROYER", 0.30;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Air_Defender_Troops_Primary  
@@ -221,7 +221,7 @@ Build_List_Element Air_Defender_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_FIGHTER", -3.0;
+ "UNIT_FIGHTERS", -3.0;
  "UNIT_INTERCEPTORS", -3.0;
  "UNIT_STEALTH_FIGHTER", -3.0;
 #END_DATA  
@@ -263,7 +263,7 @@ Build_List_Element Slaver_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_HOPLITE",  -1.0;
+      "UNIT_SLAVER", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Abolitionist_Troops_Core  
@@ -274,7 +274,7 @@ Build_List_Element Abolitionist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ABOLITIONIST", -3.0;
+ "UNIT_ABOLITIONIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Diplomatic_Troops_Core  
@@ -285,7 +285,7 @@ Build_List_Element Diplomatic_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_DIPLOMAT", -2.0;
+ "UNIT_DIPLOMAT",  -2.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Scout_Troops_Core  
@@ -308,8 +308,8 @@ Build_List_Element Spy_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SPY", -3.0;
- "UNIT_CYBER_NINJA", -3.0;
+ "UNIT_SPY", -1.0;
+ "UNIT_CYBER_NINJA", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Infector_Troops_Core  
@@ -320,7 +320,7 @@ Build_List_Element Infector_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_INFECTOR", -2.0;
+ "UNIT_INFECTOR", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Ecoterrorist_Troops_Core  
@@ -331,7 +331,7 @@ Build_List_Element Ecoterrorist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_ECOTERRORIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Defend_Troops_Core  
@@ -342,15 +342,15 @@ Build_List_Element Defend_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 3.0;
- "UNIT_HOPLITE", 3.0;
- "UNIT_PIKEMEN", 3.0;
- "UNIT_MUSKETEERS", 3.0;
- "UNIT_MACHINE_GUNNER", 3.0;
- "UNIT_PARATROOPER", 3.0;
- "UNIT_MARINES", 3.0;
- "UNIT_PLASMATICA", 3.0;
- "UNIT_LEVIATHAN", 3.0;
+ "UNIT_HOPLITE", 0.7;
+ "UNIT_LEGION", 0.7;
+ "UNIT_PIKEMEN", 0.7;
+ "UNIT_MUSKETEERS", 0.7;
+ "UNIT_MACHINE_GUNNER", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.50;
+ "UNIT_PLASMATICA", 0.25;
+ "UNIT_LEVIATHAN", 0.50;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Assault_Troops_Core  
@@ -361,14 +361,14 @@ Build_List_Element Assault_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SAMURAI", 3.0;
- "UNIT_KNIGHT", 3.0;
- "UNIT_CAVALRY", 3.0;
- "UNIT_TANK", 3.0;
- "UNIT_PARATROOPER", 3.0;
- "UNIT_MARINES", 3.0;
- "UNIT_FUSION_TANK", 3.0;
- "UNIT_SWARM", 3.0;
+ "UNIT_SAMURAI", 0.5;
+ "UNIT_KNIGHT", 0.5;
+ "UNIT_CAVALRY", 0.5;
+ "UNIT_TANK", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
+ "UNIT_FUSION_TANK", 0.5;
+ "UNIT_SWARM", 0.25;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Ranged_Troops_Core  
@@ -379,10 +379,10 @@ Build_List_Element Ranged_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 1.5;
- "UNIT_CANNON", 1.5;
- "UNIT_ARTILLERY", 1.5;
- "UNIT_BATTLEBOT", 1.5;
+ "UNIT_GREEK_FIRE", 0.7;
+ "UNIT_CANNON", 0.7;
+ "UNIT_ARTILLERY", 0.7;
+ "UNIT_BATTLEBOT", 0.7;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Attack_Troops_Core  
@@ -393,11 +393,11 @@ Build_List_Element Naval_Attack_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", 0.25;
- "UNIT_GREEK_FIRE_TRIREME", 0.25;
+ "UNIT_TRIREMES", 0.2;
+ "UNIT_GREEK_FIRE_TRIREME", 0.15;
  "UNIT_LONGSHIP", 0.25;
- "UNIT_SHIP_OF_THE_LINE", 0.25;
- "UNIT_BATTLESHIP", 0.15;
+ "UNIT_SHIP_OF_THE_LINE", 0.3;
+ "UNIT_BATTLESHIP", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Defense_Troops_Core  
@@ -408,8 +408,8 @@ Build_List_Element Naval_Defense_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_DESTROYER", 0.5;
- "UNIT_PLASMA_DESTROYER", 0.5;
+ "UNIT_DESTROYER", 0.3;
+ "UNIT_PLASMA_DESTROYER", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Transport_Troops_Core  
@@ -420,8 +420,8 @@ Build_List_Element Naval_Tranport_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TROOP_SHIP", 0.5;
- "UNIT_CRAWLER", 0.5;
+ "UNIT_TROOP_SHIP", 0.2;
+ "UNIT_CRAWLER", 0.2;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Carrier_Naval_Transport_Troops_Core  
@@ -538,7 +538,7 @@ Build_List_Element Lawyer_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LAWYER",  -2.0;
+ "UNIT_LAWYER",  -10.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Branch_Troops_Core  
@@ -608,7 +608,7 @@ Build_List_Element Slaver_Troops_Overflow[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_SLAVER",  -1.0;
+      "UNIT_SLAVER", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Scout_Troops_Overflow  
@@ -620,9 +620,7 @@ Build_List_Element Scout_Troops_Overflow[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "UNIT_WARRIOR", 0.75;
- "UNIT_DIPLOMAT", 0.1;
- "UNIT_SPY", 0.75;
- "UNIT_SPY_PLANE", 0.75;
+ "UNIT_SPY_PLANE", 0.1;
  "UNIT_ECOTERRORIST", 0.75;
  "UNIT_INFECTOR", 0.75;
  "UNIT_CYBER_NINJA", 0.75;
@@ -644,7 +642,7 @@ Build_List_Element Defend_Troops_Overflow[MAX_ELEMENTS];
  "UNIT_PARATROOPER", 1.0;
  "UNIT_MARINES", 3.0;
  "UNIT_FUSION_TANK", 3.0;
- "UNIT_SWARM", 0.5;
+ "UNIT_SWARM", 1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Assault_Troops_Overflow  
@@ -672,10 +670,10 @@ Build_List_Element Ranged_Troops_Overflow[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 1.5;
- "UNIT_CANNON", 1.5;
- "UNIT_ARTILLERY", 1.5;
- "UNIT_BATTLEBOT", 1.5;
+ "UNIT_GREEK_FIRE", 3.0;
+ "UNIT_CANNON", 3.0;
+ "UNIT_ARTILLERY", 3.0;
+ "UNIT_BATTLEBOT", 3.0;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Attack_Troops_Overflow  
@@ -686,10 +684,10 @@ Build_List_Element Naval_Attack_Troops_Overflow[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", 2.0;
- "UNIT_GREEK_FIRE_TRIREME", 2.0;
- "UNIT_LONGSHIP", 2.0;
- "UNIT_SHIP_OF_THE_LINE", 2.0;
+ "UNIT_TRIREMES", 0.2;
+ "UNIT_GREEK_FIRE_TRIREME", 0.2;
+ "UNIT_LONGSHIP", 0.2;
+ "UNIT_SHIP_OF_THE_LINE", 0.2;
  "UNIT_BATTLESHIP", -5.0;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
@@ -713,9 +711,10 @@ Build_List_Element Naval_Tranport_Troops_Overflow[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", 2.0;
- "UNIT_DESTROYER", 0.5;
- "UNIT_PLASMA_DESTROYER", 0.5;
+ "UNIT_TRIREMES", 0.5;
+ "UNIT_TROOP_SHIP", 0.5;
+ "UNIT_AIRCRAFT_CARRIER", 0.5;
+ "UNIT_CRAWLER", 0.5;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Stealth_Troops_Overflow  
```

## aidata/AIPs/green_me.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\green_me.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\green_me.aip"
index 78d5932..f9403b2 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\green_me.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\green_me.aip"
@@ -22,7 +22,7 @@ Building_Build_List_Element Transportation_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
 "IMPROVE_AIRPORT", 0500.0; 
-"IMPROVE_RAIL_LAUNCHER", 7850.0; 
+"IMPROVE_RAIL_LAUNCHER", 9850.0; 
 #END_DATA  
 //  
 // Production_List  
@@ -31,16 +31,16 @@ Building_Build_List_Element Production_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "IMPROVE_FUSION_PLANT", 10000.0;
- "IMPROVE_POPULATION_MONITOR", 8980.0; 
- "IMPROVE_RECYCLING_PLANT", 9000.0;
- "IMPROVE_ZERO_EMISSION_VEHICLES", 8000.0;
- "IMPROVE_MILL", 7990.0;
- "IMPROVE_FACTORY", 7990.0;
+ "IMPROVE_FUSION_PLANT", 6000.0;
+ "IMPROVE_POPULATION_MONITOR", 9880.0; 
+ "IMPROVE_RECYCLING_PLANT", 9900.0;
+ "IMPROVE_ZERO_EMISSION_VEHICLES", 9000.0;
+ "IMPROVE_MILL", 8990.0;
+ "IMPROVE_FACTORY", 3990.0;
  "IMPROVE_DRUG_STORE", 8999.0;
  "IMPROVE_NUCLEAR_PLANT", 7990.0;
- "IMPROVE_ROBOTIC_PLANT", 7990.0;
+ "IMPROVE_ROBOTIC_PLANT", 2990.0;
  "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 7990.0;
- "IMPROVE_OIL_REFINERY", 7990.0;
+ "IMPROVE_OIL_REFINERY", 2990.0;
  "IMPROVE_NANITE_FACTORY", 7990.0;
 #END_DATA  
```

## aidata/AIPs/milfew.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\milfew.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\milfew.aip"
index c197c25..b35f6eb 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\milfew.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\milfew.aip"
@@ -102,7 +102,7 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Land_Troops_Primary", 6000.0; 
 "Land_Strike_Troops_Primary", 6000.0; 
 "Land_Ranged_Troops_Primary", 6000.0; 
-"Sea_Troops_Primary", 5000.0; 
+"Sea_Troops_Primary", 6000.0; 
 "Air_Defender_Troops_Primary", 10000.0; 
 "Space_Defense_Troops_Primary", 10000.0; 
 // END PRIMARY  
@@ -112,27 +112,27 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Diplomatic_Troops_Core", 4500.0; 
 "Scout_Troops_Core", 2900.0; 
 "Spy_Troops_Core", 4500.0; 
-"Infector_Troops_Core", 4500.0; 
-"Ecoterrorist_Troops_Core", 4500.0; 
+"Infector_Troops_Core", 2500.0; 
+"Ecoterrorist_Troops_Core", 2500.0; 
 "Defend_Troops_Core", 3500.0; 
 "Assault_Troops_Core", 3500.0; 
 "Ranged_Troops_Core", 3500.0; 
-"Naval_Attack_Troops_Core", 1750.0; 
-"Naval_Defense_Troops_Core", 1750.0; 
+"Naval_Attack_Troops_Core", 3550.0; 
+"Naval_Defense_Troops_Core", 3550.0; 
 "Naval_Tranport_Troops_Core", 4501.0; 
 "Carrier_Naval_Transport_Troops_Core", 1650.0; 
-"Naval_Stealth_Troops_Core", 1750.0; 
+"Naval_Stealth_Troops_Core", 3550.0; 
 "Air_Attack_Troops_Core", 2000.0; 
 "Air_Bomber_Troops_Core", 2000.0; 
 "Air_Defender_Troops_Core", 2000.0; 
 "Space_Assault_Troops_Core", 2000.0; 
 "Space_Defense_Troops_Core", 2000.0; 
 "Space_Bomber_Troops_Core", 2000.0; 
-"Nuke_Troops_Core", 4500.0; 
-"Lawyer_Troops_Core", 5000.0; 
-"Branch_Troops_Core", 4500.0; 
-"Ad_Troops_Core", 4500.0; 
-"Terror_Troops_Core", 4500.0; 
+"Nuke_Troops_Core", 3500.0; 
+"Lawyer_Troops_Core", 3000.0; 
+"Branch_Troops_Core", 3000.0; 
+"Ad_Troops_Core", 3000.0; 
+"Terror_Troops_Core", 3500.0; 
 // END CORE  
 "Settler_Troops_Overflow", 3000.0; 
 "Cow_Troops_Overflow", 0.1; 
@@ -222,11 +222,11 @@ Build_List_Element Land_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_WARRIOR", 1.0;
+ "UNIT_WARRIOR", 0.5;
  "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 2.0;
- "UNIT_MUSKETEERS", 2.5;
- "UNIT_MACHINE_GUNNER", 1.0;
+ "UNIT_PIKEMEN", 1.3;
+ "UNIT_MUSKETEERS", 1.3;
+ "UNIT_MACHINE_GUNNER", 1.3;
  "UNIT_PLASMATICA", 1.0;
  "UNIT_LEVIATHAN", 0.1;
 #END_DATA  
@@ -240,12 +240,12 @@ Build_List_Element Land_Strike_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.5;
- "UNIT_SAMURAI", 0.5;
- "UNIT_KNIGHT", 0.75;
- "UNIT_CAVALRY", 1.0;
- "UNIT_TANK", 1.25;
- "UNIT_FUSION_TANK", 1.25;
+ "UNIT_LEGION", 0.4;
+ "UNIT_SAMURAI", 0.4;
+ "UNIT_KNIGHT", 0.4;
+ "UNIT_CAVALRY", 0.4;
+ "UNIT_TANK", 0.5;
+ "UNIT_FUSION_TANK", 0.8;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Land_Ranged_Troops_Primary  
@@ -257,9 +257,9 @@ Build_List_Element Land_Ranged_Troops_Primary[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "UNIT_GREEK_FIRE", 0.5;
- "UNIT_CANNON", 1.5;
- "UNIT_ARTILLERY", 1.0;
- "UNIT_BATTLEBOT", 1.25;
+ "UNIT_CANNON", 0.7;
+ "UNIT_ARTILLERY", 0.8;
+ "UNIT_BATTLEBOT", 1.0;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Sea_Troops_Primary  
@@ -271,11 +271,11 @@ Build_List_Element Sea_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", -1.0;
- "UNIT_LONGSHIP", -2.0;
- "UNIT_SHIP_OF_THE_LINE", -2.0;
- "UNIT_DESTROYER", -2.0;
- "UNIT_PLASMA_DESTROYER", -2.0;
+ "UNIT_TRIREMES", 0.25;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.30;
+ "UNIT_BATTLESHIP", 0.25;
+ "UNIT_PLASMA_DESTROYER", 0.30;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Air_Defender_Troops_Primary  
@@ -329,7 +329,7 @@ Build_List_Element Slaver_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_SLAVER", -3.0;
+      "UNIT_SLAVER", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Abolitionist_Troops_Core  
@@ -340,7 +340,7 @@ Build_List_Element Abolitionist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ABOLITIONIST", -3.0;
+ "UNIT_ABOLITIONIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Diplomatic_Troops_Core  
@@ -351,7 +351,7 @@ Build_List_Element Diplomatic_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_DIPLOMAT",  -2.0;
+ "UNIT_DIPLOMAT", -2.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Scout_Troops_Core  
@@ -374,8 +374,8 @@ Build_List_Element Spy_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SPY", -3.0;
- "UNIT_CYBER_NINJA", -3.0;
+ "UNIT_SPY", -1.0;
+ "UNIT_CYBER_NINJA", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Infector_Troops_Core  
@@ -386,7 +386,7 @@ Build_List_Element Infector_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_INFECTOR", -2.0;
+ "UNIT_INFECTOR", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Ecoterrorist_Troops_Core  
@@ -397,7 +397,7 @@ Build_List_Element Ecoterrorist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_ECOTERRORIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Defend_Troops_Core  
@@ -408,15 +408,15 @@ Build_List_Element Defend_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_HOPLITE", 0.75;
- "UNIT_LEGION", 0.75;
- "UNIT_PIKEMEN", 0.75;
- "UNIT_MUSKETEERS", 0.75;
- "UNIT_MACHINE_GUNNER", 0.75;
- "UNIT_PARATROOPER", 0.75;
- "UNIT_MARINES", 0.50;
+ "UNIT_HOPLITE", 0.7;
+ "UNIT_LEGION", 0.7;
+ "UNIT_PIKEMEN", 0.7;
+ "UNIT_MUSKETEERS", 0.7;
+ "UNIT_MACHINE_GUNNER", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
  "UNIT_PLASMATICA", 0.25;
- "UNIT_LEVIATHAN", 0.50;
+ "UNIT_LEVIATHAN", 0.5;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Assault_Troops_Core  
@@ -427,15 +427,14 @@ Build_List_Element Assault_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.75;
- "UNIT_SAMURAI", 0.75;
- "UNIT_KNIGHT", 0.75;
- "UNIT_CAVALRY", 0.75;
- "UNIT_TANK", 0.75;
- "UNIT_PARATROOPER", 1.0;
- "UNIT_MARINES", 0.75;
- "UNIT_FUSION_TANK", 0.75;
- "UNIT_SWARM", 0.75;
+ "UNIT_SAMURAI", 0.5;
+ "UNIT_KNIGHT", 0.5;
+ "UNIT_CAVALRY", 0.5;
+ "UNIT_TANK", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
+ "UNIT_FUSION_TANK", 0.5;
+ "UNIT_SWARM", 0.25;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Ranged_Troops_Core  
@@ -446,10 +445,10 @@ Build_List_Element Ranged_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 0.75;
- "UNIT_CANNON", 0.75;
- "UNIT_ARTILLERY", 0.75;
- "UNIT_BATTLEBOT", 0.75;
+ "UNIT_GREEK_FIRE", 0.5;
+ "UNIT_CANNON", 0.5;
+ "UNIT_ARTILLERY", 0.5;
+ "UNIT_BATTLEBOT", 0.5;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Attack_Troops_Core  
@@ -460,11 +459,11 @@ Build_List_Element Naval_Attack_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", 0.15;
+ "UNIT_TRIREMES", 0.2;
  "UNIT_GREEK_FIRE_TRIREME", 0.15;
- "UNIT_LONGSHIP", 0.15;
- "UNIT_SHIP_OF_THE_LINE", 0.15;
- "UNIT_BATTLESHIP", 0.15;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.3;
+ "UNIT_BATTLESHIP", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Defense_Troops_Core  
@@ -475,8 +474,8 @@ Build_List_Element Naval_Defense_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_DESTROYER", 0.5;
- "UNIT_PLASMA_DESTROYER", 0.5;
+ "UNIT_DESTROYER", 0.3;
+ "UNIT_PLASMA_DESTROYER", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Transport_Troops_Core  
@@ -487,8 +486,8 @@ Build_List_Element Naval_Tranport_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TROOP_SHIP", 0.5;
- "UNIT_CRAWLER", 0.5;
+ "UNIT_TROOP_SHIP", 0.2;
+ "UNIT_CRAWLER", 0.2;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Carrier_Naval_Transport_Troops_Core  
@@ -605,7 +604,7 @@ Build_List_Element Lawyer_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LAWYER",  -10.0;
+ "UNIT_LAWYER",  -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Branch_Troops_Core  
@@ -616,7 +615,7 @@ Build_List_Element Branch_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_CORPORATE_BRANCH", -3.0;
+ "UNIT_CORPORATE_BRANCH", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Ad_Troops_Core  
@@ -627,7 +626,7 @@ Build_List_Element Ad_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SUBNEURAL_ADS", -3.0;
+ "UNIT_SUBNEURAL_ADS", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Terror_Troops_Core  
@@ -638,8 +637,8 @@ Build_List_Element Terror_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -3.0;
- "UNIT_INFECTOR", -3.0;
+ "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_INFECTOR", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Settler_Troops_Overflow  
@@ -737,7 +736,7 @@ Build_List_Element Ranged_Troops_Overflow[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 0.5;
+ "UNIT_GREEK_FIRE", 3.0;
  "UNIT_CANNON", 3.0;
  "UNIT_ARTILLERY", 3.0;
  "UNIT_BATTLEBOT", 3.0;
@@ -919,16 +918,15 @@ Build_List_Element Wormhole_Probe_Troops[MAX_ELEMENTS];
 //  
 ///////////////////////////////////////////////////////////////////////////////  
 // Production threshholds 1.0 = top dog and 0.0 = loser  
-double Wonders_List_Threshhold =  0.8; 
-double Transportation_List_Threshhold =  0.6; 
+double Wonders_List_Threshhold =  0.6; 
+double Transportation_List_Threshhold =  0.4; 
 double Growth_List_Threshhold =  0.2; 
-double Happiness_List_Threshhold =  0.2; 
-double Production_List_Threshhold = 0.4; 
+double Happiness_List_Threshhold =  0.3; 
+double Production_List_Threshhold = 0.7; 
 double Gold_List_Threshhold =  0.4; 
-double Science_List_Threshhold =  0.2; 
+double Science_List_Threshhold =  0.5; 
 double Defense_List_Threshhold =  0.2; 
-double Miscellaneous_List_Threshhold =  0.0; 
-///////////////////////////////////////////////////////////////////////////////  
+double Miscellaneous_List_Threshhold =  0.0; ///////////////////////////////////////////////////////////////////////////////  
 //  
 // Wonders_List  
 //   
@@ -979,7 +977,7 @@ Building_Build_List_Element Transportation_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_AIRPORT", 7850.0; 
+"IMPROVE_AIRPORT", 9910.0; 
 "IMPROVE_RAIL_LAUNCHER", 7850.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
@@ -990,8 +988,9 @@ Building_Build_List_Element Growth_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 9000.0; 
-"IMPROVE_AQUEDUCT", 9000.0; 
+"IMPROVE_SILO", 9990.0; 
+"IMPROVE_AQUEDUCT", 9980.0; 
+"IMPROVE_BEEF_VAT", 7930.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1002,18 +1001,18 @@ Building_Build_List_Element Happiness_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "IMPROVE_MIND_CONTROL_EMITTER", 8999.0;
- "IMPROVE_TEMPLE", 8999.0;
- "IMPROVE_THEATER", 8999.0;
- "IMPROVE_CIRCUS", 8999.0;
- "IMPROVE_HOSPITAL", 7990.0;
- "IMPROVE_CATHEDRAL", 8999.0;
- "IMPROVE_MOVIE_PALACE", 8999.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_WATER_TRANSFORMER", 8999.0;
- "IMPROVE_BODY_EXCHANGE", 8999.0;
- "IMPROVE_ARCOLOGIES", 8999.0;
+ "IMPROVE_TEMPLE", 9960.0;
+ "IMPROVE_THEATER", 9950.0;
+ "IMPROVE_CIRCUS", 9940.0;
+ "IMPROVE_HOSPITAL", 9930.0;
+ "IMPROVE_CATHEDRAL", 8960.0;
+ "IMPROVE_MOVIE_PALACE", 8949.0;
+ "IMPROVE_DRUG_STORE", 9920.0;
+ "IMPROVE_WATER_TRANSFORMER", 8939.0;
+ "IMPROVE_BODY_EXCHANGE", 8829.0;
+ "IMPROVE_ARCOLOGIES", 8919.0;
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+///////////////////////////////////////////////////////////////////////////////  N..
 //  
 // Production_List  
 //   
@@ -1021,17 +1020,18 @@ Building_Build_List_Element Production_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "IMPROVE_FUSION_PLANT", 10000.0;
- "IMPROVE_POPULATION_MONITOR", 8980.0; 
- "IMPROVE_MILL", 7990.0;
- "IMPROVE_FACTORY", 7990.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_NUCLEAR_PLANT", 7990.0;
- "IMPROVE_RECYCLING_PLANT", 9000.0;
- "IMPROVE_ZERO_EMISSION_VEHICLES", 8000.0;
- "IMPROVE_ROBOTIC_PLANT", 7990.0;
- "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 7990.0;
- "IMPROVE_NANITE_FACTORY", 7990.0;
+ "IMPROVE_MILL", 8960.0;
+ "IMPROVE_DRUG_STORE", 8950.0;
+ "IMPROVE_FACTORY", 5980.0;
+ "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 5890.0;
+ "IMPROVE_POPULATION_MONITOR", 5880.0; 
+ "IMPROVE_NUCLEAR_PLANT", 5990.0;
+ "IMPROVE_ROBOTIC_PLANT", 2890.0;
+ "IMPROVE_RECYCLING_PLANT", 6000.0;
+ "IMPROVE_ZERO_EMISSION_VEHICLES", 4990.0;
+ "IMPROVE_OIL_REFINERY", 3000.0;
+ "IMPROVE_FUSION_PLANT", 4000.0;
+ "IMPROVE_NANITE_FACTORY", 4990.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1041,13 +1041,12 @@ Building_Build_List_Element Gold_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_BAZAAR", 7980.0; 
-"IMPROVE_BANK", 7980.0; 
-"IMPROVE_CITY_CLOCK", 7950.0; 
-"IMPROVE_TELEVISION", 7980.0; 
-"IMPROVE_AIRPORT", 7850.0; 
-"IMPROVE_HOUSE_OF_FREEZING", 8920.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7980.0; 
+"IMPROVE_BAZAAR", 9900.0; 
+"IMPROVE_BANK", 8990.0; 
+"IMPROVE_CITY_CLOCK", 7990.0; 
+"IMPROVE_TELEVISION", 6930.0; 
+"IMPROVE_AIRPORT", 8850.0; 
+"IMPROVE_HOUSE_OF_FREEZING", 6920.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1057,11 +1056,11 @@ Building_Build_List_Element Science_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_ACADEMY", 7950.0; 
+"IMPROVE_ACADEMY", 8980.0; 
+"IMPROVE_LIBRARY", 8970.0; 
 "IMPROVE_UNIVERSITY", 7950.0; 
-"IMPROVE_LIBRARY", 7950.0; 
-"IMPROVE_COMPUTER_CENTER", 7950.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7950.0; 
+"IMPROVE_COMPUTER_CENTER", 7850.0; 
+"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 6950.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1071,12 +1070,12 @@ Building_Build_List_Element Defense_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_CITY_WALLS", 7950.0; 
+"IMPROVE_CITY_WALLS", 9970.0; 
 "IMPROVE_SDI", 7950.0; 
 "IMPROVE_BIO_WARFARE_FILTERS", 7950.0; 
-"IMPROVE_FORCEFIELD", 7950.0; 
+"IMPROVE_FORCEFIELD", 8950.0; 
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+/////////////////////////////////////////////////////////////////////////////// N.. 
 //  
 // Miscellaneous_List  
 //   
@@ -1084,11 +1083,11 @@ Building_Build_List_Element Miscellaneous_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 8000.0; 
-"IMPROVE_CITY_WALLS", 7980.0; 
-"IMPROVE_BAZAAR", 8500.0; 
-"IMPROVE_COURTHOUSE", 7980.0; 
-"IMPROVE_POPULATION_MONITOR", 7980.0; 
+"IMPROVE_SILO", 9900.0; 
+"IMPROVE_CITY_WALLS", 9500.0; 
+"IMPROVE_BAZAAR", 9000.0; 
+"IMPROVE_COURTHOUSE", 8500.0; 
+"IMPROVE_POPULATION_MONITOR", 8000.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1108,6 +1107,8 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
 //--------------------------------------------------------------------  
  "ADVANCE_STONE_WORKING"; 
  "ADVANCE_MINING"; 
+ "ADVANCE_MONARCHY"; 
+ "ADVANCE_RELIGION"; 
  "ADVANCE_ALCHEMY"; 
  "ADVANCE_IRON_WORKING"; 
  "ADVANCE_BRONZE_WORKING"; 
@@ -1116,11 +1117,10 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_AGRICULTURE"; 
  "ADVANCE_STIRRUP"; 
  "ADVANCE_DOMESTICATION"; 
- "ADVANCE_MONARCHY"; 
- "ADVANCE_RELIGION"; 
  "ADVANCE_PHILOSOPHY"; 
  "ADVANCE_JURISPRUDENCE"; 
  "ADVANCE_WRITING"; 
+ "ADVANCE_THEOCRACY"; 
  "ADVANCE_ENGINEERING"; 
  "ADVANCE_GEOMETRY"; 
  "ADVANCE_AGRICULTURAL_REVOLUTION"; 
@@ -1128,41 +1128,42 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_TRADE"; 
  "ADVANCE_CITY_STATE"; 
  "ADVANCE_BUREAUCRACY"; 
+ "ADVANCE_MECHANICAL_CLOCK";
+ "ADVANCE_OPTICS";
  "ADVANCE_CANNON_MAKING"; 
  "ADVANCE_CAVALRY_TACTICS"; 
  "ADVANCE_GUNPOWDER"; 
- "ADVANCE_PRINTING_PRESS"; 
- "ADVANCE_MECHANICAL_CLOCK"; 
  "ADVANCE_OCEAN_FARING"; 
+ "ADVANCE_HULL_MAKING";
  "ADVANCE_ASTRONOMY"; 
- "ADVANCE_HULL_MAKING"; 
  "ADVANCE_INDUSTRIAL_REVOLUTION"; 
  "ADVANCE_MACHINE_TOOLS"; 
  "ADVANCE_NATIONALISM"; 
  "ADVANCE_BANKING"; 
+ "ADVANCE_AGE_OF_REASON"; 
+ "ADVANCE_PERSPECTIVE"; 
+ "ADVANCE_PRINTING_PRESS"; 
  "ADVANCE_RAILROAD"; 
+ "ADVANCE_COMMUNISM"; 
  "ADVANCE_ECONOMICS"; 
  "ADVANCE_COMPUTER"; 
  "ADVANCE_ELECTRICITY"; 
+ "ADVANCE_PHYSICS"; 
  "ADVANCE_DEMOCRACY"; 
  "ADVANCE_CORPORATION"; 
  "ADVANCE_EXPLOSIVES"; 
  "ADVANCE_OIL_REFINING"; 
  "ADVANCE_CHEMISTRY"; 
  "ADVANCE_MEDICINE"; 
- "ADVANCE_OPTICS"; 
  "ADVANCE_FASCISM"; 
  "ADVANCE_ELECTRIFICATION"; 
- "ADVANCE_PERSPECTIVE"; 
  "ADVANCE_TANK_WARFARE"; 
  "ADVANCE_MASS_PRODUCTION"; 
  "ADVANCE_ROBOTICS"; 
  "ADVANCE_CONSUMER_ELECTRONICS"; 
  "ADVANCE_AERODYNAMICS"; 
- "ADVANCE_PHYSICS"; 
  "ADVANCE_QUANTUM_MECHANICS"; 
  "ADVANCE_ROCKETRY"; 
- "ADVANCE_AGE_OF_REASON"; 
  "ADVANCE_STEEL"; 
  "ADVANCE_SPACE_FLIGHT"; 
  "ADVANCE_JET_PROPULSION"; 
@@ -1171,10 +1172,12 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_INTELLIGENT_MATERIALS"; 
  "ADVANCE_ENVIRONMENTALISM"; 
  "ADVANCE_ADVANCED_COMPOSITES"; 
+ "ADVANCE_SEA_COLONIES"; 
+ "ADVANCE_SUPERCONDUCTOR";
  "ADVANCE_FUEL_CELLS"; 
- "ADVANCE_SUPERCONDUCTOR"; 
  "ADVANCE_FUSION"; 
  "ADVANCE_UNIFIED_FIELD_THEORY"; 
+ "ADVANCE_ULTRAPRESSURE_MACHINERY"; 
  "ADVANCE_ZERO_G_MANUFACTURING"; 
  "ADVANCE_ASTEROID_MINING"; 
  "ADVANCE_NANOASSEMBLY"; 
@@ -1193,15 +1196,11 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_MIND_CONTROL"; 
  "ADVANCE_GLOBAL_DEFENSE_INITIATIVE"; 
  "ADVANCE_GENETIC_TAILORING"; 
- "ADVANCE_ULTRAPRESSURE_MACHINERY"; 
  "ADVANCE_WILDERNESS_PRESERVATION_ACT"; 
  "ADVANCE_GLOBAL_COMMUNICATIONS_NETWORK"; 
  "ADVANCE_ALIEN_ARCHEOLOGY"; 
  "ADVANCE_SUBNEURAL_ADS"; 
- "ADVANCE_SEA_COLONIES"; 
  "ADVANCE_MULTINATIONAL_REPUBLIC"; 
- "ADVANCE_COMMUNISM"; 
  "ADVANCE_VIRTUAL_DEMOCRACY"; 
  "ADVANCE_ECOTOPIA"; 
- "ADVANCE_THEOCRACY"; 
 #END_DATA  
```

## aidata/AIPs/milmany.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\milmany.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\milmany.aip"
index 5abcc2d..a784eca 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\milmany.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\milmany.aip"
@@ -102,7 +102,7 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Land_Troops_Primary", 6000.0; 
 "Land_Strike_Troops_Primary", 6000.0; 
 "Land_Ranged_Troops_Primary", 6000.0; 
-"Sea_Troops_Primary", 5000.0; 
+"Sea_Troops_Primary", 6000.0; 
 "Air_Defender_Troops_Primary", 10000.0; 
 "Space_Defense_Troops_Primary", 10000.0; 
 // END PRIMARY  
@@ -112,27 +112,27 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Diplomatic_Troops_Core", 4500.0; 
 "Scout_Troops_Core", 2900.0; 
 "Spy_Troops_Core", 4500.0; 
-"Infector_Troops_Core", 4500.0; 
-"Ecoterrorist_Troops_Core", 4500.0; 
+"Infector_Troops_Core", 2500.0; 
+"Ecoterrorist_Troops_Core", 2500.0; 
 "Defend_Troops_Core", 3500.0; 
 "Assault_Troops_Core", 3500.0; 
 "Ranged_Troops_Core", 3500.0; 
-"Naval_Attack_Troops_Core", 1750.0; 
-"Naval_Defense_Troops_Core", 1750.0; 
+"Naval_Attack_Troops_Core", 3550.0; 
+"Naval_Defense_Troops_Core", 3550.0; 
 "Naval_Tranport_Troops_Core", 4501.0; 
 "Carrier_Naval_Transport_Troops_Core", 1650.0; 
-"Naval_Stealth_Troops_Core", 1750.0; 
+"Naval_Stealth_Troops_Core", 3550.0; 
 "Air_Attack_Troops_Core", 2000.0; 
 "Air_Bomber_Troops_Core", 2000.0; 
 "Air_Defender_Troops_Core", 2000.0; 
 "Space_Assault_Troops_Core", 2000.0; 
 "Space_Defense_Troops_Core", 2000.0; 
 "Space_Bomber_Troops_Core", 2000.0; 
-"Nuke_Troops_Core", 4500.0; 
-"Lawyer_Troops_Core", 5000.0; 
-"Branch_Troops_Core", 4500.0; 
-"Ad_Troops_Core", 4500.0; 
-"Terror_Troops_Core", 4500.0; 
+"Nuke_Troops_Core", 3500.0; 
+"Lawyer_Troops_Core", 3000.0; 
+"Branch_Troops_Core", 3000.0; 
+"Ad_Troops_Core", 3000.0; 
+"Terror_Troops_Core", 3500.0; 
 // END CORE  
 "Settler_Troops_Overflow", 3000.0; 
 "Cow_Troops_Overflow", 0.1; 
@@ -222,11 +222,11 @@ Build_List_Element Land_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_WARRIOR", 1.0;
+ "UNIT_WARRIOR", 0.5;
  "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 2.0;
- "UNIT_MUSKETEERS", 2.5;
- "UNIT_MACHINE_GUNNER", 1.0;
+ "UNIT_PIKEMEN", 1.3;
+ "UNIT_MUSKETEERS", 1.3;
+ "UNIT_MACHINE_GUNNER", 1.3;
  "UNIT_PLASMATICA", 1.0;
  "UNIT_LEVIATHAN", 0.1;
 #END_DATA  
@@ -240,12 +240,12 @@ Build_List_Element Land_Strike_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.5;
- "UNIT_SAMURAI", 0.5;
- "UNIT_KNIGHT", 0.5;
- "UNIT_CAVALRY", 0.5;
- "UNIT_TANK", 1.25;
- "UNIT_FUSION_TANK", 1.25;
+ "UNIT_LEGION", 0.4;
+ "UNIT_SAMURAI", 0.4;
+ "UNIT_KNIGHT", 0.4;
+ "UNIT_CAVALRY", 0.4;
+ "UNIT_TANK", 0.5;
+ "UNIT_FUSION_TANK", 0.8;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Land_Ranged_Troops_Primary  
@@ -257,9 +257,9 @@ Build_List_Element Land_Ranged_Troops_Primary[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "UNIT_GREEK_FIRE", 0.5;
- "UNIT_CANNON", 1.5;
- "UNIT_ARTILLERY", 1.0;
- "UNIT_BATTLEBOT", 1.25;
+ "UNIT_CANNON", 0.7;
+ "UNIT_ARTILLERY", 0.8;
+ "UNIT_BATTLEBOT", 1.0;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Sea_Troops_Primary  
@@ -271,11 +271,11 @@ Build_List_Element Sea_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", -1.0;
- "UNIT_LONGSHIP", -2.0;
- "UNIT_SHIP_OF_THE_LINE", -2.0;
- "UNIT_DESTROYER", -2.0;
- "UNIT_PLASMA_DESTROYER", -2.0;
+ "UNIT_TRIREMES", 0.25;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.30;
+ "UNIT_DESTROYER", 0.30;
+ "UNIT_PLASMA_DESTROYER", 0.30;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Air_Defender_Troops_Primary  
@@ -329,7 +329,7 @@ Build_List_Element Slaver_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_SLAVER", -3.0;
+      "UNIT_SLAVER", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Abolitionist_Troops_Core  
@@ -340,7 +340,7 @@ Build_List_Element Abolitionist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ABOLITIONIST", -3.0;
+ "UNIT_ABOLITIONIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Diplomatic_Troops_Core  
@@ -351,7 +351,7 @@ Build_List_Element Diplomatic_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_DIPLOMAT", -2.0;
+  "UNIT_DIPLOMAT", -2.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Scout_Troops_Core  
@@ -374,8 +374,8 @@ Build_List_Element Spy_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SPY", -3.0;
- "UNIT_CYBER_NINJA", -3.0;
+ "UNIT_SPY", -1.0;
+ "UNIT_CYBER_NINJA", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Infector_Troops_Core  
@@ -386,7 +386,7 @@ Build_List_Element Infector_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_INFECTOR", -2.0;
+ "UNIT_INFECTOR", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Ecoterrorist_Troops_Core  
@@ -397,7 +397,7 @@ Build_List_Element Ecoterrorist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_ECOTERRORIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Defend_Troops_Core  
@@ -408,15 +408,15 @@ Build_List_Element Defend_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_HOPLITE", 0.75;
- "UNIT_LEGION", 0.75;
- "UNIT_PIKEMEN", 0.75;
- "UNIT_MUSKETEERS", 0.75;
- "UNIT_MACHINE_GUNNER", 0.75;
- "UNIT_PARATROOPER", 0.75;
- "UNIT_MARINES", 0.50;
+ "UNIT_HOPLITE", 0.7;
+ "UNIT_LEGION", 0.7;
+ "UNIT_PIKEMEN", 0.7;
+ "UNIT_MUSKETEERS", 0.7;
+ "UNIT_MACHINE_GUNNER", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
  "UNIT_PLASMATICA", 0.25;
- "UNIT_LEVIATHAN", 0.50;
+ "UNIT_LEVIATHAN", 0.5;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Assault_Troops_Core  
@@ -427,15 +427,14 @@ Build_List_Element Assault_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.75;
- "UNIT_SAMURAI", 0.75;
- "UNIT_KNIGHT", 0.75;
- "UNIT_CAVALRY", 0.75;
- "UNIT_TANK", 0.75;
- "UNIT_PARATROOPER", 1.0;
- "UNIT_MARINES", 0.75;
- "UNIT_FUSION_TANK", 0.75;
- "UNIT_SWARM", 0.75;
+ "UNIT_SAMURAI", 0.5;
+ "UNIT_KNIGHT", 0.5;
+ "UNIT_CAVALRY", 0.5;
+ "UNIT_TANK", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
+ "UNIT_FUSION_TANK", 0.5;
+ "UNIT_SWARM", 0.25;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Ranged_Troops_Core  
@@ -446,10 +445,10 @@ Build_List_Element Ranged_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 0.75;
- "UNIT_CANNON", 0.75;
- "UNIT_ARTILLERY", 0.75;
- "UNIT_BATTLEBOT", 0.75;
+ "UNIT_GREEK_FIRE", 0.5;
+ "UNIT_CANNON", 0.5;
+ "UNIT_ARTILLERY", 0.5;
+ "UNIT_BATTLEBOT", 0.5;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Attack_Troops_Core  
@@ -460,11 +459,11 @@ Build_List_Element Naval_Attack_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", 0.15;
+ "UNIT_TRIREMES", 0.2;
  "UNIT_GREEK_FIRE_TRIREME", 0.15;
- "UNIT_LONGSHIP", 0.15;
- "UNIT_SHIP_OF_THE_LINE", 0.15;
- "UNIT_BATTLESHIP", 0.15;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.3;
+ "UNIT_BATTLESHIP", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Defense_Troops_Core  
@@ -475,8 +474,8 @@ Build_List_Element Naval_Defense_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_DESTROYER", 0.5;
- "UNIT_PLASMA_DESTROYER", 0.5;
+ "UNIT_DESTROYER", 0.3;
+ "UNIT_PLASMA_DESTROYER", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Transport_Troops_Core  
@@ -487,8 +486,8 @@ Build_List_Element Naval_Tranport_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TROOP_SHIP", 0.5;
- "UNIT_CRAWLER", 0.5;
+ "UNIT_TROOP_SHIP", 0.2;
+ "UNIT_CRAWLER", 0.2;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Carrier_Naval_Transport_Troops_Core  
@@ -605,7 +604,7 @@ Build_List_Element Lawyer_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LAWYER",  -10.0;
+ "UNIT_LAWYER",  -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Branch_Troops_Core  
@@ -616,7 +615,7 @@ Build_List_Element Branch_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_CORPORATE_BRANCH", -3.0;
+ "UNIT_CORPORATE_BRANCH", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Ad_Troops_Core  
@@ -627,7 +626,7 @@ Build_List_Element Ad_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SUBNEURAL_ADS", -3.0;
+ "UNIT_SUBNEURAL_ADS", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Terror_Troops_Core  
@@ -638,8 +637,8 @@ Build_List_Element Terror_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -3.0;
- "UNIT_INFECTOR", -3.0;
+ "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_INFECTOR", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Settler_Troops_Overflow  
@@ -737,7 +736,7 @@ Build_List_Element Ranged_Troops_Overflow[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 0.5;
+ "UNIT_GREEK_FIRE", 1.5;
  "UNIT_CANNON", 3.0;
  "UNIT_ARTILLERY", 3.0;
  "UNIT_BATTLEBOT", 3.0;
@@ -919,13 +918,13 @@ Build_List_Element Wormhole_Probe_Troops[MAX_ELEMENTS];
 //  
 ///////////////////////////////////////////////////////////////////////////////  
 // Production threshholds 1.0 = top dog and 0.0 = loser  
-double Wonders_List_Threshhold =  0.8; 
-double Transportation_List_Threshhold =  0.6; 
+double Wonders_List_Threshhold =  0.68; 
+double Transportation_List_Threshhold =  0.4; 
 double Growth_List_Threshhold =  0.2; 
-double Happiness_List_Threshhold =  0.2; 
-double Production_List_Threshhold = 0.4; 
+double Happiness_List_Threshhold =  0.3; 
+double Production_List_Threshhold = 0.7; 
 double Gold_List_Threshhold =  0.4; 
-double Science_List_Threshhold =  0.2; 
+double Science_List_Threshhold =  0.5; 
 double Defense_List_Threshhold =  0.2; 
 double Miscellaneous_List_Threshhold =  0.0; 
 ///////////////////////////////////////////////////////////////////////////////  
@@ -937,13 +936,13 @@ Building_Build_List_Element Wonder_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
 "WONDER_WORMHOLE_DETECTOR", 20000.0; 
-"WONDER_STONEHENGE", 9250.0; 
+"WONDER_STONEHENGE", 9100.0; 
 "WONDER_SPHINX", 9250.0; 
 "WONDER_LABRYINTH_OF_THE_MINOTAUR", 9250.0; 
-"WONDER_RAYAMANA", 9250.0; 
-"WONDER_PARTHENON", 9100.0; 
+"WONDER_RAYAMANA", 9100.0; 
+"WONDER_PARTHENON", 9250.0; 
 "WONDER_I_CHING", 9100.0; 
-"WONDER_THE_FORBIDDEN_CITY", 9250.0; 
+"WONDER_THE_FORBIDDEN_CITY", 9100.0; 
 "WONDER_PHILOSOPHERS_STONE", 5000.0; 
 "WONDER_HAGIA_SOPHIA", 9250.0; 
 "WONDER_GUTTENBERGS_BIBLE", 9100.0; 
@@ -979,7 +978,7 @@ Building_Build_List_Element Transportation_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_AIRPORT", 7850.0; 
+"IMPROVE_AIRPORT", 9910.0; 
 "IMPROVE_RAIL_LAUNCHER", 7850.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
@@ -990,8 +989,8 @@ Building_Build_List_Element Growth_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 9000.0; 
-"IMPROVE_AQUEDUCT", 9000.0; 
+"IMPROVE_SILO", 9990.0; 
+"IMPROVE_AQUEDUCT", 9980.0; 
 "IMPROVE_BEEF_VAT", 7930.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
@@ -1003,18 +1002,18 @@ Building_Build_List_Element Happiness_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "IMPROVE_MIND_CONTROL_EMITTER", 8999.0;
- "IMPROVE_TEMPLE", 8999.0;
- "IMPROVE_THEATER", 8999.0;
- "IMPROVE_CIRCUS", 8999.0;
- "IMPROVE_HOSPITAL", 7990.0;
- "IMPROVE_CATHEDRAL", 8999.0;
- "IMPROVE_MOVIE_PALACE", 8999.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_WATER_TRANSFORMER", 8999.0;
- "IMPROVE_BODY_EXCHANGE", 8999.0;
- "IMPROVE_ARCOLOGIES", 8999.0;
+ "IMPROVE_TEMPLE", 9960.0;
+ "IMPROVE_THEATER", 9950.0;
+ "IMPROVE_CIRCUS", 9940.0;
+ "IMPROVE_HOSPITAL", 9930.0;
+ "IMPROVE_CATHEDRAL", 8960.0;
+ "IMPROVE_MOVIE_PALACE", 8949.0;
+ "IMPROVE_DRUG_STORE", 9920.0;
+ "IMPROVE_WATER_TRANSFORMER", 8939.0;
+ "IMPROVE_BODY_EXCHANGE", 8829.0;
+ "IMPROVE_ARCOLOGIES", 8919.0;
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+///////////////////////////////////////////////////////////////////////////////  N..
 //  
 // Production_List  
 //   
@@ -1022,18 +1021,18 @@ Building_Build_List_Element Production_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "IMPROVE_FUSION_PLANT", 10000.0;
- "IMPROVE_POPULATION_MONITOR", 8980.0; 
- "IMPROVE_MILL", 7990.0;
- "IMPROVE_FACTORY", 7990.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_RECYCLING_PLANT", 9000.0;
- "IMPROVE_ZERO_EMISSION_VEHICLES", 8000.0;
- "IMPROVE_NUCLEAR_PLANT", 7990.0;
- "IMPROVE_ROBOTIC_PLANT", 7990.0;
- "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 7990.0;
- "IMPROVE_OIL_REFINERY", 7990.0;
- "IMPROVE_NANITE_FACTORY", 7990.0;
+ "IMPROVE_MILL", 8960.0;
+ "IMPROVE_DRUG_STORE", 8950.0;
+ "IMPROVE_FACTORY", 5980.0;
+ "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 5890.0;
+ "IMPROVE_POPULATION_MONITOR", 5880.0; 
+ "IMPROVE_NUCLEAR_PLANT", 5990.0;
+ "IMPROVE_ROBOTIC_PLANT", 2890.0;
+ "IMPROVE_RECYCLING_PLANT", 6000.0;
+ "IMPROVE_ZERO_EMISSION_VEHICLES", 4990.0;
+ "IMPROVE_OIL_REFINERY", 3000.0;
+ "IMPROVE_FUSION_PLANT", 4000.0;
+ "IMPROVE_NANITE_FACTORY", 4990.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1043,13 +1042,12 @@ Building_Build_List_Element Gold_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_BAZAAR", 7980.0; 
-"IMPROVE_BANK", 7980.0; 
-"IMPROVE_CITY_CLOCK", 7950.0; 
-"IMPROVE_TELEVISION", 7980.0; 
-"IMPROVE_AIRPORT", 7850.0; 
-"IMPROVE_HOUSE_OF_FREEZING", 8920.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7980.0; 
+"IMPROVE_BAZAAR", 9900.0; 
+"IMPROVE_BANK", 8990.0; 
+"IMPROVE_CITY_CLOCK", 7990.0; 
+"IMPROVE_TELEVISION", 6930.0; 
+"IMPROVE_AIRPORT", 8850.0; 
+"IMPROVE_HOUSE_OF_FREEZING", 6920.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1059,11 +1057,11 @@ Building_Build_List_Element Science_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_ACADEMY", 7950.0; 
+"IMPROVE_ACADEMY", 8980.0; 
+"IMPROVE_LIBRARY", 8970.0; 
 "IMPROVE_UNIVERSITY", 7950.0; 
-"IMPROVE_LIBRARY", 7950.0; 
-"IMPROVE_COMPUTER_CENTER", 7950.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7950.0; 
+"IMPROVE_COMPUTER_CENTER", 7850.0; 
+"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 6950.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1073,12 +1071,12 @@ Building_Build_List_Element Defense_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_CITY_WALLS", 7900.0; 
-"IMPROVE_SDI", 7900.0; 
-"IMPROVE_BIO_WARFARE_FILTERS", 7900.0; 
-"IMPROVE_FORCEFIELD", 7900.0; 
+"IMPROVE_CITY_WALLS", 9970.0; 
+"IMPROVE_SDI", 7950.0; 
+"IMPROVE_BIO_WARFARE_FILTERS", 7950.0; 
+"IMPROVE_FORCEFIELD", 8950.0; 
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+/////////////////////////////////////////////////////////////////////////////// N.. 
 //  
 // Miscellaneous_List  
 //   
@@ -1086,11 +1084,11 @@ Building_Build_List_Element Miscellaneous_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 8000.0; 
-"IMPROVE_CITY_WALLS", 7980.0; 
-"IMPROVE_BAZAAR", 8500.0; 
-"IMPROVE_COURTHOUSE", 7980.0; 
-"IMPROVE_POPULATION_MONITOR", 7980.0; 
+"IMPROVE_SILO", 9900.0; 
+"IMPROVE_CITY_WALLS", 9500.0; 
+"IMPROVE_BAZAAR", 9000.0; 
+"IMPROVE_COURTHOUSE", 8500.0; 
+"IMPROVE_POPULATION_MONITOR", 8000.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1117,18 +1115,25 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_RELIGION"; 
  "ADVANCE_AGRICULTURE"; 
  "ADVANCE_TRADE"; 
+ "ADVANCE_CITY_STATE"; 
+ "ADVANCE_BUREAUCRACY"; 
  "ADVANCE_WRITING"; 
  "ADVANCE_DOMESTICATION"; 
  "ADVANCE_PHILOSOPHY"; 
  "ADVANCE_JURISPRUDENCE"; 
+ "ADVANCE_THEOCRACY"; 
  "ADVANCE_CLASSICAL_EDUCATION"; 
- "ADVANCE_GEOMETRY"; 
- "ADVANCE_AGRICULTURAL_REVOLUTION"; 
  "ADVANCE_GUNPOWDER"; 
  "ADVANCE_ALCHEMY"; 
  "ADVANCE_IRON_WORKING"; 
+ "ADVANCE_GEOMETRY"; 
+ "ADVANCE_ENGINEERING";
+ "ADVANCE_CAVALRY_TACTICS"; 
+ "ADVANCE_STIRRUP";
+ "ADVANCE_MECHANICAL_CLOCK";
+ "ADVANCE_OPTICS";
+ "ADVANCE_AGRICULTURAL_REVOLUTION"; 
  "ADVANCE_PRINTING_PRESS"; 
- "ADVANCE_MECHANICAL_CLOCK"; 
  "ADVANCE_OCEAN_FARING"; 
  "ADVANCE_HULL_MAKING"; 
  "ADVANCE_CANNON_MAKING"; 
@@ -1136,15 +1141,15 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_MACHINE_TOOLS"; 
  "ADVANCE_COMPUTER"; 
  "ADVANCE_ELECTRICITY"; 
+ "ADVANCE_PHYSICS"; 
  "ADVANCE_RAILROAD"; 
  "ADVANCE_ECONOMICS"; 
  "ADVANCE_NATIONALISM"; 
  "ADVANCE_BANKING"; 
- "ADVANCE_BUREAUCRACY"; 
+ "ADVANCE_AGE_OF_REASON"; 
  "ADVANCE_FASCISM"; 
  "ADVANCE_ELECTRIFICATION"; 
  "ADVANCE_PERSPECTIVE"; 
- "ADVANCE_ENGINEERING"; 
  "ADVANCE_DEMOCRACY"; 
  "ADVANCE_CORPORATION"; 
  "ADVANCE_STEEL"; 
@@ -1152,58 +1157,51 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_OIL_REFINING"; 
  "ADVANCE_CHEMISTRY"; 
  "ADVANCE_MEDICINE"; 
- "ADVANCE_OPTICS"; 
  "ADVANCE_ASTRONOMY"; 
  "ADVANCE_TANK_WARFARE"; 
- "ADVANCE_CAVALRY_TACTICS"; 
- "ADVANCE_STIRRUP"; 
  "ADVANCE_MASS_PRODUCTION"; 
  "ADVANCE_JET_PROPULSION"; 
  "ADVANCE_ROCKETRY"; 
  "ADVANCE_AERODYNAMICS"; 
- "ADVANCE_PHYSICS"; 
  "ADVANCE_PHARMACEUTICALS"; 
  "ADVANCE_CONSUMER_ELECTRONICS"; 
  "ADVANCE_ROBOTICS"; 
  "ADVANCE_GENETICS"; 
- "ADVANCE_AGE_OF_REASON"; 
  "ADVANCE_QUANTUM_MECHANICS"; 
  "ADVANCE_SPACE_FLIGHT"; 
  "ADVANCE_ENVIRONMENTALISM"; 
  "ADVANCE_GLOBAL_COMMUNICATIONS_NETWORK"; 
  "ADVANCE_ADVANCED_COMPOSITES"; 
+ "ADVANCE_SEA_COLONIES"; 
+ "ADVANCE_SUPERCONDUCTOR"; 
  "ADVANCE_MULTINATIONAL_REPUBLIC"; 
  "ADVANCE_AI_SURVEILLANCE"; 
  "ADVANCE_SUBNEURAL_ADS"; 
  "ADVANCE_INTELLIGENT_MATERIALS"; 
  "ADVANCE_FUEL_CELLS"; 
  "ADVANCE_PERSONAL_ENCRYPTION"; 
- "ADVANCE_WORMHOLES"; 
  "ADVANCE_FUSION"; 
  "ADVANCE_UNIFIED_FIELD_THEORY"; 
  "ADVANCE_TECHNOCRACY"; 
- "ADVANCE_SUPERCONDUCTOR"; 
  "ADVANCE_HUMAN_CLONING"; 
  "ADVANCE_GLOBAL_DEFENSE_INITIATIVE"; 
  "ADVANCE_ARCOLOGIES"; 
- "ADVANCE_SEA_COLONIES"; 
  "ADVANCE_SPACE_COLONIES"; 
  "ADVANCE_GENETIC_TAILORING"; 
+ "ADVANCE_ULTRAPRESSURE_MACHINERY";
+ "ADVANCE_WORMHOLES";
  "ADVANCE_ZERO_G_MANUFACTURING"; 
  "ADVANCE_CRYONICS"; 
  "ADVANCE_MIND_CONTROL"; 
- "ADVANCE_ULTRAPRESSURE_MACHINERY"; 
  "ADVANCE_ASTEROID_MINING"; 
  "ADVANCE_NANOASSEMBLY"; 
  "ADVANCE_WILDERNESS_PRESERVATION_ACT"; 
  "ADVANCE_GAIA_THEORY"; 
  "ADVANCE_VIRTUAL_DEMOCRACY"; 
- "ADVANCE_CITY_STATE"; 
+ "ADVANCE_CLOAKING";
  "ADVANCE_ALIEN_ARCHEOLOGY"; 
  "ADVANCE_NEURAL_SILICON_INTERFACE"; 
  "ADVANCE_LIFE_EXTENSION"; 
  "ADVANCE_COMMUNISM"; 
  "ADVANCE_ECOTOPIA"; 
- "ADVANCE_THEOCRACY"; 
- "ADVANCE_CLOAKING"; 
 #END_DATA  
```

## aidata/AIPs/naval.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\naval.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\naval.aip"
index bc43bf8..202dd0d 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\naval.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\naval.aip"
@@ -100,7 +100,7 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Land_Troops_Primary", 6000.0; 
 "Land_Strike_Troops_Primary", 6000.0; 
 "Land_Ranged_Troops_Primary", 6000.0; 
-"Sea_Troops_Primary", 6000.0; 
+"Sea_Troops_Primary", 6500.0; 
 "Air_Defender_Troops_Primary", 10000.0; 
 "Space_Defense_Troops_Primary", 10000.0; 
 // END PRIMARY  
@@ -115,22 +115,22 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Defend_Troops_Core", 3500.0; 
 "Assault_Troops_Core", 3500.0; 
 "Ranged_Troops_Core", 3500.0; 
-"Naval_Attack_Troops_Core", 3050.0; 
-"Naval_Defense_Troops_Core", 3050.0; 
+"Naval_Attack_Troops_Core", 3550.0; 
+"Naval_Defense_Troops_Core", 3550.0; 
 "Naval_Tranport_Troops_Core", 4501.0; 
-"Carrier_Naval_Transport_Troops_Core", 3050.0; 
-"Naval_Stealth_Troops_Core", 3050.0; 
+"Carrier_Naval_Transport_Troops_Core", 1650.0; 
+"Naval_Stealth_Troops_Core", 3550.0; 
 "Air_Attack_Troops_Core", 2000.0; 
 "Air_Bomber_Troops_Core", 2000.0; 
 "Air_Defender_Troops_Core", 2000.0; 
 "Space_Assault_Troops_Core", 2000.0; 
 "Space_Defense_Troops_Core", 2000.0; 
 "Space_Bomber_Troops_Core", 2000.0; 
-"Nuke_Troops_Core", 4500.0; 
-"Lawyer_Troops_Core", 5000.0; 
-"Branch_Troops_Core", 4500.0; 
-"Ad_Troops_Core", 4500.0; 
-"Terror_Troops_Core", 4500.0; 
+"Nuke_Troops_Core", 3500.0; 
+"Lawyer_Troops_Core", 3000.0; 
+"Branch_Troops_Core", 3000.0; 
+"Ad_Troops_Core", 3000.0; 
+"Terror_Troops_Core", 3500.0; 
 // END CORE  
 "Settler_Troops_Overflow", 3000.0; 
 "Cow_Troops_Overflow", 0.1; 
@@ -220,11 +220,11 @@ Build_List_Element Land_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_WARRIOR", 1.0;
+ "UNIT_WARRIOR", 0.5;
  "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 2.0;
- "UNIT_MUSKETEERS", 2.5;
- "UNIT_MACHINE_GUNNER", 1.0;
+ "UNIT_PIKEMEN", 1.3;
+ "UNIT_MUSKETEERS", 1.3;
+ "UNIT_MACHINE_GUNNER", 1.3;
  "UNIT_PLASMATICA", 1.0;
  "UNIT_LEVIATHAN", 0.1;
 #END_DATA  
@@ -238,12 +238,12 @@ Build_List_Element Land_Strike_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.5;
- "UNIT_SAMURAI", 0.5;
- "UNIT_KNIGHT", 0.5;
- "UNIT_CAVALRY", 0.5;
+ "UNIT_LEGION", 0.4;
+ "UNIT_SAMURAI", 0.4;
+ "UNIT_KNIGHT", 0.4;
+ "UNIT_CAVALRY", 0.4;
  "UNIT_TANK", 0.5;
- "UNIT_FUSION_TANK", 2.0;
+ "UNIT_FUSION_TANK", 0.8;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Land_Ranged_Troops_Primary  
@@ -255,9 +255,9 @@ Build_List_Element Land_Ranged_Troops_Primary[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "UNIT_GREEK_FIRE", 0.5;
- "UNIT_CANNON", 1.5;
- "UNIT_ARTILLERY", 1.0;
- "UNIT_BATTLEBOT", 1.25;
+ "UNIT_CANNON", 0.7;
+ "UNIT_ARTILLERY", 0.8;
+ "UNIT_BATTLEBOT", 1.0;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Sea_Troops_Primary  
@@ -269,11 +269,11 @@ Build_List_Element Sea_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES",  -2.0;
- "UNIT_LONGSHIP",  -2.0;
- "UNIT_SHIP_OF_THE_LINE",  -3.0;
- "UNIT_DESTROYER",  -3.0;
- "UNIT_PLASMA_DESTROYER",  -3.0;
+ "UNIT_TRIREMES", 0.4;
+ "UNIT_LONGSHIP", 0.5;
+ "UNIT_SHIP_OF_THE_LINE", 0.5;
+ "UNIT_DESTROYER",  0.25;
+ "UNIT_PLASMA_DESTROYER", 0.30;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Air_Defender_Troops_Primary  
@@ -327,7 +327,7 @@ Build_List_Element Slaver_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_DIPLOMAT", -2.0;
+ "UNIT_DIPLOMAT", -2.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Abolitionist_Troops_Core  
@@ -338,7 +338,7 @@ Build_List_Element Abolitionist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ABOLITIONIST", -3.0;
+ "UNIT_ABOLITIONIST", 0.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Diplomatic_Troops_Core  
@@ -372,8 +372,8 @@ Build_List_Element Spy_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SPY", -3.0;
- "UNIT_CYBER_NINJA", -3.0;
+ "UNIT_SPY", -1.0;
+ "UNIT_CYBER_NINJA", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Infector_Troops_Core  
@@ -384,7 +384,7 @@ Build_List_Element Infector_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_INFECTOR", -2.0;
+ "UNIT_INFECTOR", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Ecoterrorist_Troops_Core  
@@ -395,7 +395,7 @@ Build_List_Element Ecoterrorist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_ECOTERRORIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Defend_Troops_Core  
@@ -406,15 +406,15 @@ Build_List_Element Defend_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 1.0;
- "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 1.0;
- "UNIT_MUSKETEERS", 1.0;
- "UNIT_MACHINE_GUNNER", 1.0;
- "UNIT_PARATROOPER", 1.0;
- "UNIT_MARINES", 0.75;
+ "UNIT_HOPLITE", 0.7;
+ "UNIT_LEGION", 0.7;
+ "UNIT_PIKEMEN", 0.7;
+ "UNIT_MUSKETEERS", 0.7;
+ "UNIT_MACHINE_GUNNER", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
  "UNIT_PLASMATICA", 0.25;
- "UNIT_LEVIATHAN", 0.75;
+ "UNIT_LEVIATHAN", 0.5;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Assault_Troops_Core  
@@ -425,7 +425,6 @@ Build_List_Element Assault_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.5;
  "UNIT_SAMURAI", 0.5;
  "UNIT_KNIGHT", 0.5;
  "UNIT_CAVALRY", 0.5;
@@ -433,7 +432,7 @@ Build_List_Element Assault_Troops_Core[MAX_ELEMENTS];
  "UNIT_PARATROOPER", 0.5;
  "UNIT_MARINES", 0.5;
  "UNIT_FUSION_TANK", 0.5;
- "UNIT_SWARM", 0.5;
+ "UNIT_SWARM", 0.25;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Ranged_Troops_Core  
@@ -444,10 +443,10 @@ Build_List_Element Ranged_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 0.75;
- "UNIT_CANNON", 0.75;
- "UNIT_ARTILLERY", 0.75;
- "UNIT_BATTLEBOT", 0.75;
+ "UNIT_GREEK_FIRE", 0.5;
+ "UNIT_CANNON", 0.5;
+ "UNIT_ARTILLERY", 0.5;
+ "UNIT_BATTLEBOT", 0.5;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Attack_Troops_Core  
@@ -458,11 +457,11 @@ Build_List_Element Naval_Attack_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", 0.75;
- "UNIT_GREEK_FIRE_TRIREME", 0.75;
- "UNIT_LONGSHIP", 0.75;
- "UNIT_SHIP_OF_THE_LINE", 0.75;
- "UNIT_BATTLESHIP", 0.15;
+ "UNIT_TRIREMES", 0.4;
+ "UNIT_GREEK_FIRE_TRIREME", 0.15;
+ "UNIT_LONGSHIP", 0.5;
+ "UNIT_SHIP_OF_THE_LINE", 0.5;
+ "UNIT_BATTLESHIP", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Defense_Troops_Core  
@@ -614,7 +613,7 @@ Build_List_Element Branch_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_CORPORATE_BRANCH", -3.0;
+ "UNIT_CORPORATE_BRANCH", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Ad_Troops_Core  
@@ -625,7 +624,7 @@ Build_List_Element Ad_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SUBNEURAL_ADS", -3.0;
+ "UNIT_SUBNEURAL_ADS", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Terror_Troops_Core  
@@ -636,8 +635,8 @@ Build_List_Element Terror_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -3.0;
- "UNIT_INFECTOR", -3.0;
+ "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_INFECTOR", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Settler_Troops_Overflow  
```

## aidata/AIPs/scifew.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\scifew.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\scifew.aip"
index 24b6052..11c7809 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\scifew.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\scifew.aip"
@@ -101,7 +101,7 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Land_Troops_Primary", 6000.0; 
 "Land_Strike_Troops_Primary", 6000.0; 
 "Land_Ranged_Troops_Primary", 6000.0; 
-"Sea_Troops_Primary", 5000.0; 
+"Sea_Troops_Primary", 6000.0; 
 "Air_Defender_Troops_Primary", 10000.0; 
 "Space_Defense_Troops_Primary", 10000.0; 
 // END PRIMARY  
@@ -111,27 +111,27 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Diplomatic_Troops_Core", 4500.0; 
 "Scout_Troops_Core", 2900.0; 
 "Spy_Troops_Core", 4500.0; 
-"Infector_Troops_Core", 4500.0; 
-"Ecoterrorist_Troops_Core", 4500.0; 
+"Infector_Troops_Core", 2500.0; 
+"Ecoterrorist_Troops_Core", 2500.0; 
 "Defend_Troops_Core", 3500.0; 
 "Assault_Troops_Core", 3500.0; 
 "Ranged_Troops_Core", 3500.0; 
-"Naval_Attack_Troops_Core", 1750.0; 
-"Naval_Defense_Troops_Core", 1750.0; 
+"Naval_Attack_Troops_Core", 3550.0; 
+"Naval_Defense_Troops_Core", 3550.0; 
 "Naval_Tranport_Troops_Core", 4501.0; 
 "Carrier_Naval_Transport_Troops_Core", 1650.0; 
-"Naval_Stealth_Troops_Core", 1750.0; 
+"Naval_Stealth_Troops_Core", 3550.0; 
 "Air_Attack_Troops_Core", 2000.0; 
 "Air_Bomber_Troops_Core", 2000.0; 
 "Air_Defender_Troops_Core", 2000.0; 
 "Space_Assault_Troops_Core", 2000.0; 
 "Space_Defense_Troops_Core", 2000.0; 
 "Space_Bomber_Troops_Core", 2000.0; 
-"Nuke_Troops_Core", 4500.0; 
-"Lawyer_Troops_Core", 5000.0; 
-"Branch_Troops_Core", 4500.0; 
-"Ad_Troops_Core", 4500.0; 
-"Terror_Troops_Core", 4500.0; 
+"Nuke_Troops_Core", 3500.0; 
+"Lawyer_Troops_Core", 3000.0; 
+"Branch_Troops_Core", 3000.0; 
+"Ad_Troops_Core", 3000.0; 
+"Terror_Troops_Core", 3500.0; 
 // END CORE  
 "Settler_Troops_Overflow", 3000.0; 
 "Cow_Troops_Overflow", 0.1; 
@@ -221,11 +221,11 @@ Build_List_Element Land_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_WARRIOR", 1.0;
+ "UNIT_WARRIOR", 0.5;
  "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 2.0;
- "UNIT_MUSKETEERS", 2.5;
- "UNIT_MACHINE_GUNNER", 1.0;
+ "UNIT_PIKEMEN", 1.3;
+ "UNIT_MUSKETEERS", 1.3;
+ "UNIT_MACHINE_GUNNER", 1.3;
  "UNIT_PLASMATICA", 1.0;
  "UNIT_LEVIATHAN", 0.1;
 #END_DATA  
@@ -239,12 +239,12 @@ Build_List_Element Land_Strike_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.5;
- "UNIT_SAMURAI", 0.5;
- "UNIT_KNIGHT", 0.5;
- "UNIT_CAVALRY", 0.5;
+ "UNIT_LEGION", 0.4;
+ "UNIT_SAMURAI", 0.4;
+ "UNIT_KNIGHT", 0.4;
+ "UNIT_CAVALRY", 0.4;
  "UNIT_TANK", 0.5;
- "UNIT_FUSION_TANK", 1.0;
+ "UNIT_FUSION_TANK", 0.8;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Land_Ranged_Troops_Primary  
@@ -256,9 +256,9 @@ Build_List_Element Land_Ranged_Troops_Primary[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "UNIT_GREEK_FIRE", 0.5;
- "UNIT_CANNON", 1.5;
- "UNIT_ARTILLERY", 1.0;
- "UNIT_BATTLEBOT", 1.25;
+ "UNIT_CANNON", 0.7;
+ "UNIT_ARTILLERY", 0.8;
+ "UNIT_BATTLEBOT", 1.0;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Sea_Troops_Primary  
@@ -270,11 +270,11 @@ Build_List_Element Sea_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", -1.0;
- "UNIT_LONGSHIP", -2.0;
- "UNIT_SHIP_OF_THE_LINE", -2.0;
- "UNIT_DESTROYER", -2.0;
- "UNIT_PLASMA_DESTROYER", -2.0;
+ "UNIT_TRIREMES", 0.25;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.30;
+ "UNIT_BATTLESHIP", 0.25;
+ "UNIT_PLASMA_DESTROYER", 0.30;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Air_Defender_Troops_Primary  
@@ -328,7 +328,7 @@ Build_List_Element Slaver_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_DIPLOMAT", -2.0;
+ "UNIT_SLAVER", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Abolitionist_Troops_Core  
@@ -339,7 +339,7 @@ Build_List_Element Abolitionist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ABOLITIONIST", -3.0;
+ "UNIT_ABOLITIONIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Diplomatic_Troops_Core  
@@ -373,8 +373,8 @@ Build_List_Element Spy_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SPY", -3.0;
- "UNIT_CYBER_NINJA", -3.0;
+ "UNIT_SPY", -1.0;
+ "UNIT_CYBER_NINJA", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Infector_Troops_Core  
@@ -385,7 +385,7 @@ Build_List_Element Infector_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_INFECTOR", -2.0;
+ "UNIT_INFECTOR", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Ecoterrorist_Troops_Core  
@@ -396,7 +396,7 @@ Build_List_Element Ecoterrorist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_ECOTERRORIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Defend_Troops_Core  
@@ -407,14 +407,15 @@ Build_List_Element Defend_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 1.0;
- "UNIT_MUSKETEERS", 1.0;
- "UNIT_MACHINE_GUNNER", 1.0;
- "UNIT_PARATROOPER", 1.0;
- "UNIT_MARINES", 0.75;
+ "UNIT_HOPLITE", 0.7;
+ "UNIT_LEGION", 0.7;
+ "UNIT_PIKEMEN", 0.7;
+ "UNIT_MUSKETEERS", 0.7;
+ "UNIT_MACHINE_GUNNER", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
  "UNIT_PLASMATICA", 0.25;
- "UNIT_LEVIATHAN", 0.75;
+ "UNIT_LEVIATHAN", 0.5;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Assault_Troops_Core  
@@ -443,10 +444,10 @@ Build_List_Element Ranged_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 0.75;
- "UNIT_CANNON", 0.75;
- "UNIT_ARTILLERY", 0.75;
- "UNIT_BATTLEBOT", 0.75;
+ "UNIT_GREEK_FIRE", 0.4;
+ "UNIT_CANNON", 0.5;
+ "UNIT_ARTILLERY", 0.5;
+ "UNIT_BATTLEBOT", 0.5;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Attack_Troops_Core  
@@ -457,11 +458,11 @@ Build_List_Element Naval_Attack_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", 0.15;
+ "UNIT_TRIREMES", 0.2;
  "UNIT_GREEK_FIRE_TRIREME", 0.15;
- "UNIT_LONGSHIP", 0.15;
- "UNIT_SHIP_OF_THE_LINE", 0.15;
- "UNIT_BATTLESHIP", 0.15;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.3;
+ "UNIT_BATTLESHIP", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Defense_Troops_Core  
@@ -472,8 +473,8 @@ Build_List_Element Naval_Defense_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_DESTROYER", 0.5;
- "UNIT_PLASMA_DESTROYER", 0.5;
+ "UNIT_DESTROYER", 0.3;
+ "UNIT_PLASMA_DESTROYER", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Transport_Troops_Core  
@@ -484,8 +485,8 @@ Build_List_Element Naval_Tranport_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TROOP_SHIP", 0.5;
- "UNIT_CRAWLER", 0.5;
+ "UNIT_TROOP_SHIP", 0.2;
+ "UNIT_CRAWLER", 0.2;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Carrier_Naval_Transport_Troops_Core  
@@ -602,7 +603,7 @@ Build_List_Element Lawyer_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LAWYER",  -10.0;
+ "UNIT_LAWYER",  -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Branch_Troops_Core  
@@ -613,7 +614,7 @@ Build_List_Element Branch_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_CORPORATE_BRANCH", -3.0;
+ "UNIT_CORPORATE_BRANCH", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Ad_Troops_Core  
@@ -624,7 +625,7 @@ Build_List_Element Ad_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SUBNEURAL_ADS", -3.0;
+ "UNIT_SUBNEURAL_ADS", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Terror_Troops_Core  
@@ -635,8 +636,8 @@ Build_List_Element Terror_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -3.0;
- "UNIT_INFECTOR", -3.0;
+ "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_INFECTOR", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Settler_Troops_Overflow  
@@ -917,16 +918,15 @@ Build_List_Element Wormhole_Probe_Troops[MAX_ELEMENTS];
 //  
 ///////////////////////////////////////////////////////////////////////////////  
 // Production threshholds 1.0 = top dog and 0.0 = loser  
-double Wonders_List_Threshhold =  0.8; 
-double Transportation_List_Threshhold =  0.6; 
+double Wonders_List_Threshhold =  0.6; 
+double Transportation_List_Threshhold =  0.4; 
 double Growth_List_Threshhold =  0.2; 
-double Happiness_List_Threshhold =  0.2; 
-double Production_List_Threshhold = 0.4; 
+double Happiness_List_Threshhold =  0.3; 
+double Production_List_Threshhold = 0.7; 
 double Gold_List_Threshhold =  0.4; 
-double Science_List_Threshhold =  0.2; 
+double Science_List_Threshhold =  0.5; 
 double Defense_List_Threshhold =  0.2; 
-double Miscellaneous_List_Threshhold =  0.0; 
-///////////////////////////////////////////////////////////////////////////////  
+double Miscellaneous_List_Threshhold =  0.0; ///////////////////////////////////////////////////////////////////////////////  
 //  
 // Wonders_List  
 //   
@@ -935,17 +935,17 @@ Building_Build_List_Element Wonder_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
 "WONDER_WORMHOLE_DETECTOR", 20000.0; 
-"WONDER_STONEHENGE", 10000.0; 
-"WONDER_SPHINX", 4000.0; 
-"WONDER_LABRYINTH_OF_THE_MINOTAUR", 10000.0; 
-"WONDER_RAYAMANA", 10000.0; 
-"WONDER_PARTHENON", 9100.0; 
-"WONDER_I_CHING", 4000.0; 
-"WONDER_THE_FORBIDDEN_CITY", 10000.0; 
-"WONDER_PHILOSOPHERS_STONE", 5000.0; 
-"WONDER_HAGIA_SOPHIA", 0.0; 
-"WONDER_GUTTENBERGS_BIBLE", 9100.0; 
-"WONDER_EAST_INDIA_COMPANY", 10000.0; 
+"WONDER_STONEHENGE", 9100.0; 
+"WONDER_SPHINX", 9100.0; 
+"WONDER_LABRYINTH_OF_THE_MINOTAUR", 9100.0; 
+"WONDER_RAYAMANA", 9250.0; 
+"WONDER_PARTHENON", 9250.0; 
+"WONDER_I_CHING", 9100.0; 
+"WONDER_THE_FORBIDDEN_CITY", 5000.0; 
+"WONDER_PHILOSOPHERS_STONE", 9250.0; 
+"WONDER_HAGIA_SOPHIA", 9250.0; 
+"WONDER_GUTTENBERGS_BIBLE", 10000.0; 
+"WONDER_EAST_INDIA_COMPANY", 9100.0; 
 "WONDER_GALILEOS_TELESCOPE", 10000.0; 
 "WONDER_LONDON_STOCK_EXCHANGE", 9300.0; 
 "WONDER_EMANCIPATION_PROCLAMATION", 9100.0; 
@@ -977,7 +977,7 @@ Building_Build_List_Element Transportation_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_AIRPORT", 7850.0; 
+"IMPROVE_AIRPORT", 9910.0; 
 "IMPROVE_RAIL_LAUNCHER", 7850.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
@@ -988,8 +988,8 @@ Building_Build_List_Element Growth_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 9000.0; 
-"IMPROVE_AQUEDUCT", 9000.0; 
+"IMPROVE_SILO", 9990.0; 
+"IMPROVE_AQUEDUCT", 9980.0; 
 "IMPROVE_BEEF_VAT", 7930.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
@@ -1001,18 +1001,18 @@ Building_Build_List_Element Happiness_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "IMPROVE_MIND_CONTROL_EMITTER", 8999.0;
- "IMPROVE_TEMPLE", 8999.0;
- "IMPROVE_THEATER", 8999.0;
- "IMPROVE_CIRCUS", 8999.0;
- "IMPROVE_HOSPITAL", 7990.0;
- "IMPROVE_CATHEDRAL", 8999.0;
- "IMPROVE_MOVIE_PALACE", 8999.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_WATER_TRANSFORMER", 8999.0;
- "IMPROVE_BODY_EXCHANGE", 8999.0;
- "IMPROVE_ARCOLOGIES", 8999.0;
+ "IMPROVE_TEMPLE", 9960.0;
+ "IMPROVE_THEATER", 9950.0;
+ "IMPROVE_CIRCUS", 9940.0;
+ "IMPROVE_HOSPITAL", 9930.0;
+ "IMPROVE_CATHEDRAL", 8960.0;
+ "IMPROVE_MOVIE_PALACE", 8949.0;
+ "IMPROVE_DRUG_STORE", 9920.0;
+ "IMPROVE_WATER_TRANSFORMER", 8939.0;
+ "IMPROVE_BODY_EXCHANGE", 8829.0;
+ "IMPROVE_ARCOLOGIES", 8919.0;
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+///////////////////////////////////////////////////////////////////////////////  N..
 //  
 // Production_List  
 //   
@@ -1020,17 +1020,18 @@ Building_Build_List_Element Production_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "IMPROVE_NANITE_FACTORY", 7990.0;
- "IMPROVE_MILL", 7990.0;
- "IMPROVE_FACTORY", 7990.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_POPULATION_MONITOR", 8980.0; 
- "IMPROVE_RECYCLING_PLANT", 9000.0;
- "IMPROVE_ZERO_EMISSION_VEHICLES", 8000.0;
- "IMPROVE_FUSION_PLANT", 10000.0;
- "IMPROVE_NUCLEAR_PLANT", 7990.0;
- "IMPROVE_ROBOTIC_PLANT", 7990.0;
- "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 7990.0;
+ "IMPROVE_MILL", 8960.0;
+ "IMPROVE_DRUG_STORE", 8950.0;
+ "IMPROVE_FACTORY", 5980.0;
+ "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 5890.0;
+ "IMPROVE_POPULATION_MONITOR", 5880.0; 
+ "IMPROVE_NUCLEAR_PLANT", 5990.0;
+ "IMPROVE_ROBOTIC_PLANT", 2890.0;
+ "IMPROVE_RECYCLING_PLANT", 6000.0;
+ "IMPROVE_ZERO_EMISSION_VEHICLES", 4990.0;
+ "IMPROVE_OIL_REFINERY", 3000.0;
+ "IMPROVE_FUSION_PLANT", 4000.0;
+ "IMPROVE_NANITE_FACTORY", 4990.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1040,13 +1041,12 @@ Building_Build_List_Element Gold_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_BAZAAR", 7980.0; 
-"IMPROVE_BANK", 7980.0; 
-"IMPROVE_CITY_CLOCK", 7950.0; 
-"IMPROVE_TELEVISION", 7980.0; 
-"IMPROVE_AIRPORT", 7850.0; 
-"IMPROVE_HOUSE_OF_FREEZING", 8920.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7980.0; 
+"IMPROVE_BAZAAR", 9900.0; 
+"IMPROVE_BANK", 8990.0; 
+"IMPROVE_CITY_CLOCK", 7990.0; 
+"IMPROVE_TELEVISION", 6930.0; 
+"IMPROVE_AIRPORT", 8850.0; 
+"IMPROVE_HOUSE_OF_FREEZING", 6920.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1056,11 +1056,11 @@ Building_Build_List_Element Science_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_ACADEMY", 7950.0; 
+"IMPROVE_ACADEMY", 8980.0; 
+"IMPROVE_LIBRARY", 8970.0; 
 "IMPROVE_UNIVERSITY", 7950.0; 
-"IMPROVE_LIBRARY", 7950.0; 
-"IMPROVE_COMPUTER_CENTER", 7950.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7950.0; 
+"IMPROVE_COMPUTER_CENTER", 7850.0; 
+"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 6950.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1070,12 +1070,12 @@ Building_Build_List_Element Defense_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_CITY_WALLS", 9950.0; 
+"IMPROVE_CITY_WALLS", 9970.0; 
 "IMPROVE_SDI", 7950.0; 
 "IMPROVE_BIO_WARFARE_FILTERS", 7950.0; 
-"IMPROVE_FORCEFIELD", 7950.0; 
+"IMPROVE_FORCEFIELD", 8950.0; 
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+/////////////////////////////////////////////////////////////////////////////// N.. 
 //  
 // Miscellaneous_List  
 //   
@@ -1083,11 +1083,11 @@ Building_Build_List_Element Miscellaneous_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 8000.0; 
-"IMPROVE_CITY_WALLS", 7980.0; 
-"IMPROVE_BAZAAR", 8500.0; 
-"IMPROVE_COURTHOUSE", 7980.0; 
-"IMPROVE_POPULATION_MONITOR", 7980.0; 
+"IMPROVE_SILO", 9900.0; 
+"IMPROVE_CITY_WALLS", 9500.0; 
+"IMPROVE_BAZAAR", 9000.0; 
+"IMPROVE_COURTHOUSE", 8500.0; 
+"IMPROVE_POPULATION_MONITOR", 8000.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1106,12 +1106,12 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "ADVANCE_SEA_COLONIES"; 
- "ADVANCE_ARCOLOGIES"; 
  "ADVANCE_ADVANCED_COMPOSITES"; 
  "ADVANCE_FUEL_CELLS"; 
  "ADVANCE_SUPERCONDUCTOR"; 
- "ADVANCE_ASTRONOMY"; 
+ "ADVANCE_MONARCHY"; 
  "ADVANCE_RELIGION"; 
+ "ADVANCE_ASTRONOMY"; 
  "ADVANCE_AGRICULTURE"; 
  "ADVANCE_SHIP_BUILDING"; 
  "ADVANCE_TOOLMAKING"; 
@@ -1121,30 +1121,35 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_MINING"; 
  "ADVANCE_TRADE"; 
  "ADVANCE_WRITING"; 
+ "ADVANCE_THEOCRACY";
  "ADVANCE_PHILOSOPHY"; 
+ "ADVANCE_IRON_WORKING"; 
+ "ADVANCE_ALCHEMY"; 
  "ADVANCE_JURISPRUDENCE"; 
  "ADVANCE_CITY_STATE"; 
  "ADVANCE_BUREAUCRACY"; 
  "ADVANCE_ENGINEERING"; 
+ "ADVANCE_STIRRUP";
  "ADVANCE_CLASSICAL_EDUCATION"; 
  "ADVANCE_GEOMETRY"; 
  "ADVANCE_AGRICULTURAL_REVOLUTION"; 
+ "ADVANCE_CAVALRY_TACTICS"; 
  "ADVANCE_BANKING"; 
- "ADVANCE_IRON_WORKING"; 
- "ADVANCE_ALCHEMY"; 
+ "ADVANCE_MECHANICAL_CLOCK";
  "ADVANCE_GUNPOWDER"; 
  "ADVANCE_OCEAN_FARING"; 
  "ADVANCE_HULL_MAKING"; 
+ "ADVANCE_OPTICS";
  "ADVANCE_PRINTING_PRESS"; 
  "ADVANCE_DEMOCRACY"; 
  "ADVANCE_CORPORATION"; 
- "ADVANCE_MONARCHY"; 
- "ADVANCE_MECHANICAL_CLOCK"; 
  "ADVANCE_INDUSTRIAL_REVOLUTION"; 
  "ADVANCE_MACHINE_TOOLS"; 
  "ADVANCE_CANNON_MAKING"; 
+ "ADVANCE_AGE_OF_REASON"; 
  "ADVANCE_RAILROAD"; 
  "ADVANCE_ELECTRICITY"; 
+ "ADVANCE_PHYSICS"; 
  "ADVANCE_COMPUTER"; 
  "ADVANCE_PERSPECTIVE"; 
  "ADVANCE_EXPLOSIVES"; 
@@ -1154,18 +1159,13 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_ECONOMICS"; 
  "ADVANCE_NATIONALISM"; 
  "ADVANCE_COMMUNISM"; 
- "ADVANCE_AGE_OF_REASON"; 
  "ADVANCE_PHARMACEUTICALS"; 
  "ADVANCE_CONSUMER_ELECTRONICS"; 
  "ADVANCE_AERODYNAMICS"; 
  "ADVANCE_MASS_PRODUCTION"; 
- "ADVANCE_PHYSICS"; 
- "ADVANCE_OPTICS"; 
  "ADVANCE_QUANTUM_MECHANICS"; 
- "ADVANCE_ELECTRIFICATION"; 
+ "ADVANCE_ELECTRIFICATION";
  "ADVANCE_TANK_WARFARE"; 
- "ADVANCE_CAVALRY_TACTICS"; 
- "ADVANCE_STIRRUP"; 
  "ADVANCE_STEEL"; 
  "ADVANCE_ROCKETRY"; 
  "ADVANCE_JET_PROPULSION"; 
@@ -1178,11 +1178,13 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_GENETIC_TAILORING"; 
  "ADVANCE_GENETICS"; 
  "ADVANCE_ROBOTICS"; 
- "ADVANCE_WORMHOLES"; 
  "ADVANCE_FUSION"; 
  "ADVANCE_UNIFIED_FIELD_THEORY"; 
  "ADVANCE_SPACE_COLONIES"; 
+ "ADVANCE_ARCOLOGIES";
  "ADVANCE_INTELLIGENT_MATERIALS"; 
+ "ADVANCE_WORMHOLES";
+ "ADVANCE_CLOAKING"; 
  "ADVANCE_ALIEN_ARCHEOLOGY"; 
  "ADVANCE_AI_SURVEILLANCE"; 
  "ADVANCE_CRYONICS"; 
@@ -1200,7 +1202,5 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_FASCISM"; 
  "ADVANCE_WILDERNESS_PRESERVATION_ACT"; 
  "ADVANCE_GLOBAL_DEFENSE_INITIATIVE"; 
- "ADVANCE_CLOAKING"; 
- "ADVANCE_THEOCRACY"; 
  "ADVANCE_ECOTOPIA"; 
 #END_DATA  
```

## aidata/AIPs/scimany.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\scimany.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\scimany.aip"
index 51f055a..21b6e9f 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\scimany.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\scimany.aip"
@@ -101,7 +101,7 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Land_Troops_Primary", 6000.0; 
 "Land_Strike_Troops_Primary", 6000.0; 
 "Land_Ranged_Troops_Primary", 6000.0; 
-"Sea_Troops_Primary", 5000.0; 
+"Sea_Troops_Primary", 6000.0; 
 "Air_Defender_Troops_Primary", 10000.0; 
 "Space_Defense_Troops_Primary", 10000.0; 
 // END PRIMARY  
@@ -116,22 +116,22 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Defend_Troops_Core", 3500.0; 
 "Assault_Troops_Core", 3500.0; 
 "Ranged_Troops_Core", 3500.0; 
-"Naval_Attack_Troops_Core", 1750.0; 
-"Naval_Defense_Troops_Core", 1750.0; 
+"Naval_Attack_Troops_Core", 3550.0; 
+"Naval_Defense_Troops_Core", 3550.0; 
 "Naval_Tranport_Troops_Core", 4501.0; 
 "Carrier_Naval_Transport_Troops_Core", 1650.0; 
-"Naval_Stealth_Troops_Core", 1750.0; 
+"Naval_Stealth_Troops_Core", 3550.0; 
 "Air_Attack_Troops_Core", 2000.0; 
 "Air_Bomber_Troops_Core", 2000.0; 
 "Air_Defender_Troops_Core", 2000.0; 
 "Space_Assault_Troops_Core", 2000.0; 
 "Space_Defense_Troops_Core", 2000.0; 
 "Space_Bomber_Troops_Core", 2000.0; 
-"Nuke_Troops_Core", 4500.0; 
-"Lawyer_Troops_Core", 5000.0; 
-"Branch_Troops_Core", 4500.0; 
-"Ad_Troops_Core", 4500.0; 
-"Terror_Troops_Core", 4500.0; 
+"Nuke_Troops_Core", 3500.0; 
+"Lawyer_Troops_Core", 3000.0; 
+"Branch_Troops_Core", 3000.0; 
+"Ad_Troops_Core", 3000.0; 
+"Terror_Troops_Core", 3500.0;
 // END CORE  
 "Settler_Troops_Overflow", 3000.0; 
 "Cow_Troops_Overflow", 0.1; 
@@ -221,11 +221,11 @@ Build_List_Element Land_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_WARRIOR", 1.0;
+ "UNIT_WARRIOR", 0.5;
  "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 2.0;
- "UNIT_MUSKETEERS", 2.5;
- "UNIT_MACHINE_GUNNER", 1.0;
+ "UNIT_PIKEMEN", 1.3;
+ "UNIT_MUSKETEERS", 1.3;
+ "UNIT_MACHINE_GUNNER", 1.3;
  "UNIT_PLASMATICA", 1.0;
  "UNIT_LEVIATHAN", 0.1;
 #END_DATA  
@@ -239,12 +239,12 @@ Build_List_Element Land_Strike_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.5;
- "UNIT_SAMURAI", 0.5;
- "UNIT_KNIGHT", 0.5;
- "UNIT_CAVALRY", 0.5;
+ "UNIT_LEGION", 0.4;
+ "UNIT_SAMURAI", 0.4;
+ "UNIT_KNIGHT", 0.4;
+ "UNIT_CAVALRY", 0.4;
  "UNIT_TANK", 0.5;
- "UNIT_FUSION_TANK", 1.0;
+ "UNIT_FUSION_TANK", 0.8;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Land_Ranged_Troops_Primary  
@@ -256,9 +256,9 @@ Build_List_Element Land_Ranged_Troops_Primary[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "UNIT_GREEK_FIRE", 0.5;
- "UNIT_CANNON", 1.5;
- "UNIT_ARTILLERY", 1.0;
- "UNIT_BATTLEBOT", 1.25;
+ "UNIT_CANNON", 0.7;
+ "UNIT_ARTILLERY", 0.8;
+ "UNIT_BATTLEBOT", 1.0;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Sea_Troops_Primary  
@@ -270,11 +270,11 @@ Build_List_Element Sea_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", -1.0;
- "UNIT_LONGSHIP", -2.0;
- "UNIT_SHIP_OF_THE_LINE", -2.0;
- "UNIT_DESTROYER", -2.0;
- "UNIT_PLASMA_DESTROYER", -2.0;
+ "UNIT_TRIREMES", 0.25;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.30;
+ "UNIT_BATTLESHIP", 0.25;
+ "UNIT_PLASMA_DESTROYER", 0.30;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Air_Defender_Troops_Primary  
@@ -328,7 +328,7 @@ Build_List_Element Slaver_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_DIPLOMAT", -2.0;
+ "UNIT_SLAVER", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Abolitionist_Troops_Core  
@@ -339,7 +339,7 @@ Build_List_Element Abolitionist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ABOLITIONIST", -3.0;
+ "UNIT_ABOLITIONIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Diplomatic_Troops_Core  
@@ -373,8 +373,8 @@ Build_List_Element Spy_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SPY", -3.0;
- "UNIT_CYBER_NINJA", -3.0;
+ "UNIT_SPY", -1.0;
+ "UNIT_CYBER_NINJA", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Infector_Troops_Core  
@@ -385,7 +385,7 @@ Build_List_Element Infector_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_INFECTOR", -2.0;
+ "UNIT_INFECTOR", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Ecoterrorist_Troops_Core  
@@ -396,7 +396,7 @@ Build_List_Element Ecoterrorist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_ECOTERRORIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Defend_Troops_Core  
@@ -407,14 +407,15 @@ Build_List_Element Defend_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 1.0;
- "UNIT_MUSKETEERS", 1.0;
- "UNIT_MACHINE_GUNNER", 1.0;
- "UNIT_PARATROOPER", 1.0;
- "UNIT_MARINES", 0.75;
+ "UNIT_HOPLITE", 0.7;
+ "UNIT_LEGION", 0.7;
+ "UNIT_PIKEMEN", 0.7;
+ "UNIT_MUSKETEERS", 0.7;
+ "UNIT_MACHINE_GUNNER", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
  "UNIT_PLASMATICA", 0.25;
- "UNIT_LEVIATHAN", 0.75;
+ "UNIT_LEVIATHAN", 0.5;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Assault_Troops_Core  
@@ -443,10 +444,10 @@ Build_List_Element Ranged_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 1.0;
- "UNIT_CANNON", 1.0;
- "UNIT_ARTILLERY", 1.0;
- "UNIT_BATTLEBOT", 1.0;
+ "UNIT_GREEK_FIRE", 0.5;
+ "UNIT_CANNON", 0.5;
+ "UNIT_ARTILLERY", 0.5;
+ "UNIT_BATTLEBOT", 0.5;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Attack_Troops_Core  
@@ -457,11 +458,11 @@ Build_List_Element Naval_Attack_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", 0.15;
+ "UNIT_TRIREMES", 0.2;
  "UNIT_GREEK_FIRE_TRIREME", 0.15;
- "UNIT_LONGSHIP", 0.15;
- "UNIT_SHIP_OF_THE_LINE", 0.15;
- "UNIT_BATTLESHIP", 0.15;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.3;
+ "UNIT_BATTLESHIP", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Defense_Troops_Core  
@@ -472,8 +473,8 @@ Build_List_Element Naval_Defense_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_DESTROYER", 0.5;
- "UNIT_PLASMA_DESTROYER", 0.5;
+ "UNIT_DESTROYER", 0.3;
+ "UNIT_PLASMA_DESTROYER", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Transport_Troops_Core  
@@ -484,8 +485,8 @@ Build_List_Element Naval_Tranport_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TROOP_SHIP", 0.5;
- "UNIT_CRAWLER", 0.5;
+ "UNIT_TROOP_SHIP", 0.2;
+ "UNIT_CRAWLER", 0.2;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Carrier_Naval_Transport_Troops_Core  
@@ -602,7 +603,7 @@ Build_List_Element Lawyer_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LAWYER",  -10.0;
+ "UNIT_LAWYER",  -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Branch_Troops_Core  
@@ -613,7 +614,7 @@ Build_List_Element Branch_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_CORPORATE_BRANCH", -3.0;
+ "UNIT_CORPORATE_BRANCH", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Ad_Troops_Core  
@@ -624,7 +625,7 @@ Build_List_Element Ad_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SUBNEURAL_ADS", -3.0;
+ "UNIT_SUBNEURAL_ADS", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Terror_Troops_Core  
@@ -635,8 +636,8 @@ Build_List_Element Terror_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -3.0;
- "UNIT_INFECTOR", -3.0;
+ "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_INFECTOR", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Settler_Troops_Overflow  
@@ -918,13 +919,13 @@ Build_List_Element Wormhole_Probe_Troops[MAX_ELEMENTS];
 //  
 ///////////////////////////////////////////////////////////////////////////////  
 // Production threshholds 1.0 = top dog and 0.0 = loser  
-double Wonders_List_Threshhold =  0.8; 
-double Transportation_List_Threshhold =  0.6; 
+double Wonders_List_Threshhold =  0.6; 
+double Transportation_List_Threshhold =  0.4; 
 double Growth_List_Threshhold =  0.2; 
-double Happiness_List_Threshhold =  0.2; 
-double Production_List_Threshhold = 0.4; 
+double Happiness_List_Threshhold =  0.3; 
+double Production_List_Threshhold = 0.7; 
 double Gold_List_Threshhold =  0.4; 
-double Science_List_Threshhold =  0.2; 
+double Science_List_Threshhold =  0.5; 
 double Defense_List_Threshhold =  0.2; 
 double Miscellaneous_List_Threshhold =  0.0; 
 ///////////////////////////////////////////////////////////////////////////////  
@@ -937,16 +938,16 @@ Building_Build_List_Element Wonder_List[MAX_ELEMENTS];
 //--------------------------------------------------------------------  
 "WONDER_WORMHOLE_DETECTOR", 20000.0; 
 "WONDER_STONEHENGE", 9000.0; 
-"WONDER_SPHINX", 4000.0; 
+"WONDER_SPHINX", 9100.0; 
 "WONDER_LABRYINTH_OF_THE_MINOTAUR", 10000.0; 
-"WONDER_RAYAMANA", 10000.0; 
-"WONDER_PARTHENON", 9125.0; 
-"WONDER_I_CHING", 9100.0; 
-"WONDER_THE_FORBIDDEN_CITY", 10000.0; 
-"WONDER_PHILOSOPHERS_STONE", 5000.0; 
-"WONDER_HAGIA_SOPHIA", 0.0; 
-"WONDER_GUTTENBERGS_BIBLE", 9100.0; 
-"WONDER_EAST_INDIA_COMPANY", 9250.0; 
+"WONDER_RAYAMANA", 9250.0; 
+"WONDER_PARTHENON", 9255.0; 
+"WONDER_I_CHING", 9250.0; 
+"WONDER_THE_FORBIDDEN_CITY", 5000.0; 
+"WONDER_PHILOSOPHERS_STONE", 9250.0; 
+"WONDER_HAGIA_SOPHIA", 9250.0; 
+"WONDER_GUTTENBERGS_BIBLE", 9250.0; 
+"WONDER_EAST_INDIA_COMPANY", 9100.0; 
 "WONDER_GALILEOS_TELESCOPE", 9250.0; 
 "WONDER_LONDON_STOCK_EXCHANGE", 9300.0; 
 "WONDER_EMANCIPATION_PROCLAMATION", 9100.0; 
@@ -978,7 +979,7 @@ Building_Build_List_Element Transportation_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_AIRPORT", 7850.0; 
+"IMPROVE_AIRPORT", 9910.0; 
 "IMPROVE_RAIL_LAUNCHER", 7850.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
@@ -989,8 +990,8 @@ Building_Build_List_Element Growth_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 9000.0; 
-"IMPROVE_AQUEDUCT", 9000.0;
+"IMPROVE_SILO", 9990.0; 
+"IMPROVE_AQUEDUCT", 9980.0; 
 "IMPROVE_BEEF_VAT", 7930.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
@@ -1002,18 +1003,18 @@ Building_Build_List_Element Happiness_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "IMPROVE_MIND_CONTROL_EMITTER", 8999.0;
- "IMPROVE_TEMPLE", 8999.0;
- "IMPROVE_THEATER", 8999.0;
- "IMPROVE_CIRCUS", 8999.0;
- "IMPROVE_HOSPITAL", 7990.0;
- "IMPROVE_CATHEDRAL", 8999.0;
- "IMPROVE_MOVIE_PALACE", 8999.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_WATER_TRANSFORMER", 8999.0;
- "IMPROVE_BODY_EXCHANGE", 8999.0;
- "IMPROVE_ARCOLOGIES", 8999.0;
+ "IMPROVE_TEMPLE", 9960.0;
+ "IMPROVE_THEATER", 9950.0;
+ "IMPROVE_CIRCUS", 9940.0;
+ "IMPROVE_HOSPITAL", 9930.0;
+ "IMPROVE_CATHEDRAL", 8960.0;
+ "IMPROVE_MOVIE_PALACE", 8949.0;
+ "IMPROVE_DRUG_STORE", 9920.0;
+ "IMPROVE_WATER_TRANSFORMER", 8939.0;
+ "IMPROVE_BODY_EXCHANGE", 8829.0;
+ "IMPROVE_ARCOLOGIES", 8919.0;
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+///////////////////////////////////////////////////////////////////////////////  N..
 //  
 // Production_List  
 //   
@@ -1021,18 +1022,18 @@ Building_Build_List_Element Production_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "IMPROVE_FUSION_PLANT", 10000.0;
- "IMPROVE_POPULATION_MONITOR", 8980.0; 
- "IMPROVE_MILL", 7990.0;
- "IMPROVE_FACTORY", 7990.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_RECYCLING_PLANT", 9000.0;
- "IMPROVE_ZERO_EMISSION_VEHICLES", 8000.0;
- "IMPROVE_NUCLEAR_PLANT", 7990.0;
- "IMPROVE_ROBOTIC_PLANT", 7990.0;
- "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 7990.0;
- "IMPROVE_OIL_REFINERY", 7990.0;
- "IMPROVE_NANITE_FACTORY", 7990.0;
+ "IMPROVE_MILL", 8960.0;
+ "IMPROVE_DRUG_STORE", 8950.0;
+ "IMPROVE_FACTORY", 5980.0;
+ "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 5890.0;
+ "IMPROVE_POPULATION_MONITOR", 5880.0; 
+ "IMPROVE_NUCLEAR_PLANT", 5990.0;
+ "IMPROVE_ROBOTIC_PLANT", 2890.0;
+ "IMPROVE_RECYCLING_PLANT", 6000.0;
+ "IMPROVE_ZERO_EMISSION_VEHICLES", 4990.0;
+ "IMPROVE_OIL_REFINERY", 3000.0;
+ "IMPROVE_FUSION_PLANT", 4000.0;
+ "IMPROVE_NANITE_FACTORY", 4990.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1042,13 +1043,12 @@ Building_Build_List_Element Gold_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_BAZAAR", 7980.0; 
-"IMPROVE_BANK", 7980.0; 
-"IMPROVE_CITY_CLOCK", 7950.0; 
-"IMPROVE_TELEVISION", 7980.0; 
-"IMPROVE_AIRPORT", 7850.0; 
-"IMPROVE_HOUSE_OF_FREEZING", 8920.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7980.0; 
+"IMPROVE_BAZAAR", 9900.0; 
+"IMPROVE_BANK", 8990.0; 
+"IMPROVE_CITY_CLOCK", 7990.0; 
+"IMPROVE_TELEVISION", 6930.0; 
+"IMPROVE_AIRPORT", 8850.0; 
+"IMPROVE_HOUSE_OF_FREEZING", 6920.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1058,11 +1058,11 @@ Building_Build_List_Element Science_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_ACADEMY", 7950.0; 
+"IMPROVE_ACADEMY", 8980.0; 
+"IMPROVE_LIBRARY", 8970.0; 
 "IMPROVE_UNIVERSITY", 7950.0; 
-"IMPROVE_LIBRARY", 7950.0; 
-"IMPROVE_COMPUTER_CENTER", 7950.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7950.0; 
+"IMPROVE_COMPUTER_CENTER", 7850.0; 
+"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 6950.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1072,12 +1072,12 @@ Building_Build_List_Element Defense_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_CITY_WALLS", 9999.0; 
-"IMPROVE_SDI", 7999.0; 
-"IMPROVE_BIO_WARFARE_FILTERS", 7999.0; 
-"IMPROVE_FORCEFIELD", 7999.0; 
+"IMPROVE_CITY_WALLS", 9970.0; 
+"IMPROVE_SDI", 7950.0; 
+"IMPROVE_BIO_WARFARE_FILTERS", 7950.0; 
+"IMPROVE_FORCEFIELD", 8950.0; 
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+/////////////////////////////////////////////////////////////////////////////// N.. 
 //  
 // Miscellaneous_List  
 //   
@@ -1085,11 +1085,11 @@ Building_Build_List_Element Miscellaneous_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 8000.0; 
-"IMPROVE_CITY_WALLS", 7980.0; 
-"IMPROVE_BAZAAR", 8500.0; 
-"IMPROVE_COURTHOUSE", 7980.0; 
-"IMPROVE_POPULATION_MONITOR", 7980.0; 
+"IMPROVE_SILO", 9900.0; 
+"IMPROVE_CITY_WALLS", 9500.0; 
+"IMPROVE_BAZAAR", 9000.0; 
+"IMPROVE_COURTHOUSE", 8500.0; 
+"IMPROVE_POPULATION_MONITOR", 8000.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1110,6 +1110,8 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_SPACE_COLONIES"; 
  "ADVANCE_INTELLIGENT_MATERIALS"; 
  "ADVANCE_ARCOLOGIES"; 
+ "ADVANCE_MONARCHY"; 
+ "ADVANCE_RELIGION"; 
  "ADVANCE_SHIP_BUILDING"; 
  "ADVANCE_TOOLMAKING"; 
  "ADVANCE_TRADE"; 
@@ -1119,53 +1121,52 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_BRONZE_WORKING"; 
  "ADVANCE_MINING"; 
  "ADVANCE_PHILOSOPHY"; 
+ "ADVANCE_THEOCRACY";
  "ADVANCE_GEOMETRY"; 
  "ADVANCE_JURISPRUDENCE"; 
- "ADVANCE_RELIGION"; 
  "ADVANCE_DOMESTICATION"; 
  "ADVANCE_BUREAUCRACY"; 
  "ADVANCE_CITY_STATE"; 
+ "ADVANCE_IRON_WORKING"; 
+ "ADVANCE_ALCHEMY"; 
+ "ADVANCE_ENGINEERING"; 
+ "ADVANCE_CAVALRY_TACTICS"; 
+ "ADVANCE_STIRRUP"; 
  "ADVANCE_CLASSICAL_EDUCATION"; 
+ "ADVANCE_MECHANICAL_CLOCK";
+ "ADVANCE_OPTICS";
  "ADVANCE_BANKING"; 
  "ADVANCE_AGRICULTURAL_REVOLUTION"; 
- "ADVANCE_ENGINEERING"; 
- "ADVANCE_IRON_WORKING"; 
- "ADVANCE_ALCHEMY"; 
  "ADVANCE_GUNPOWDER"; 
- "ADVANCE_MONARCHY"; 
  "ADVANCE_HULL_MAKING"; 
  "ADVANCE_ASTRONOMY"; 
  "ADVANCE_OCEAN_FARING"; 
- "ADVANCE_MECHANICAL_CLOCK"; 
- "ADVANCE_OPTICS"; 
  "ADVANCE_DEMOCRACY"; 
  "ADVANCE_CORPORATION"; 
  "ADVANCE_PRINTING_PRESS"; 
  "ADVANCE_ECONOMICS"; 
+ "ADVANCE_CANNON_MAKING"; 
  "ADVANCE_NATIONALISM"; 
  "ADVANCE_AGE_OF_REASON"; 
  "ADVANCE_MACHINE_TOOLS"; 
  "ADVANCE_INDUSTRIAL_REVOLUTION"; 
- "ADVANCE_CANNON_MAKING"; 
+ "ADVANCE_PERSPECTIVE"; 
  "ADVANCE_OIL_REFINING"; 
  "ADVANCE_CHEMISTRY"; 
  "ADVANCE_RAILROAD"; 
  "ADVANCE_MEDICINE"; 
  "ADVANCE_ELECTRICITY"; 
+ "ADVANCE_PHYSICS"; 
  "ADVANCE_COMPUTER"; 
  "ADVANCE_EXPLOSIVES"; 
  "ADVANCE_PHARMACEUTICALS"; 
  "ADVANCE_ELECTRIFICATION"; 
  "ADVANCE_COMMUNISM"; 
  "ADVANCE_CONSUMER_ELECTRONICS"; 
- "ADVANCE_PERSPECTIVE"; 
  "ADVANCE_AERODYNAMICS"; 
  "ADVANCE_MASS_PRODUCTION"; 
- "ADVANCE_CAVALRY_TACTICS"; 
- "ADVANCE_STIRRUP"; 
  "ADVANCE_STEEL"; 
- "ADVANCE_PHYSICS"; 
- "ADVANCE_ROCKETRY"; 
+ "ADVANCE_ROCKETRY";
  "ADVANCE_QUANTUM_MECHANICS"; 
  "ADVANCE_JET_PROPULSION"; 
  "ADVANCE_TANK_WARFARE"; 
@@ -1173,10 +1174,12 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_GLOBAL_COMMUNICATIONS_NETWORK"; 
  "ADVANCE_SPACE_FLIGHT"; 
  "ADVANCE_ADVANCED_COMPOSITES"; 
+ "ADVANCE_SEA_COLONIES";
+ "ADVANCE_SUPERCONDUCTOR";
  "ADVANCE_ROBOTICS"; 
  "ADVANCE_FUEL_CELLS"; 
- "ADVANCE_SUPERCONDUCTOR"; 
  "ADVANCE_WORMHOLES"; 
+ "ADVANCE_CLOAKING"; 
  "ADVANCE_ALIEN_ARCHEOLOGY"; 
  "ADVANCE_FUSION"; 
  "ADVANCE_UNIFIED_FIELD_THEORY"; 
@@ -1188,10 +1191,8 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_HUMAN_CLONING"; 
  "ADVANCE_GENETICS"; 
  "ADVANCE_GENETIC_TAILORING"; 
- "ADVANCE_SEA_COLONIES"; 
  "ADVANCE_VIRTUAL_DEMOCRACY"; 
  "ADVANCE_LIFE_EXTENSION"; 
- "ADVANCE_CLOAKING"; 
  "ADVANCE_GLOBAL_DEFENSE_INITIATIVE"; 
  "ADVANCE_PERSONAL_ENCRYPTION"; 
  "ADVANCE_TECHNOCRACY"; 
@@ -1202,7 +1203,6 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_ECOTOPIA"; 
  "ADVANCE_WILDERNESS_PRESERVATION_ACT"; 
  "ADVANCE_SUBNEURAL_ADS"; 
- "ADVANCE_THEOCRACY"; 
  "ADVANCE_FASCISM"; 
  "ADVANCE_GAIA_THEORY"; 
 #END_DATA  
```

## aidata/AIPs/slaver.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\slaver.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\slaver.aip"
index 6d9b4fa..08f093d 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\slaver.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\slaver.aip"
@@ -105,37 +105,37 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Land_Troops_Primary", 6000.0; 
 "Land_Strike_Troops_Primary", 6000.0; 
 "Land_Ranged_Troops_Primary", 6000.0; 
-"Sea_Troops_Primary", 5000.0; 
+"Sea_Troops_Primary", 6000.0; 
 "Air_Defender_Troops_Primary", 10000.0; 
 "Space_Defense_Troops_Primary", 10000.0; 
 // END PRIMARY  
-"Settler_Troops_Core", 3500.0; 
+"Settler_Troops_Core", 3000.0; 
 "Slaver_Troops_Core", 6500.0; 
 "Abolitionist_Troops_Core", 6001; 
 "Diplomatic_Troops_Core", 4500.0; 
 "Scout_Troops_Core", 2900.0; 
-"Spy_Troops_Core", 4500.0; 
-"Infector_Troops_Core", 4500.0; 
-"Ecoterrorist_Troops_Core", 4500.0; 
+"Spy_Troops_Core", 4500.0
+"Infector_Troops_Core", 2500.0; 
+"Ecoterrorist_Troops_Core", 2500.0; 
 "Defend_Troops_Core", 3500.0; 
 "Assault_Troops_Core", 3500.0; 
 "Ranged_Troops_Core", 3500.0; 
-"Naval_Attack_Troops_Core", 1750.0; 
-"Naval_Defense_Troops_Core", 1750.0; 
-"Naval_Tranport_Troops_Core", 4501.0; 
+"Naval_Attack_Troops_Core", 3550.0; 
+"Naval_Defense_Troops_Core", 3550.0; 
+"Naval_Tranport_Troops_Core", 3550.0; 
 "Carrier_Naval_Transport_Troops_Core", 1650.0; 
-"Naval_Stealth_Troops_Core", 1750.0; 
+"Naval_Stealth_Troops_Core", 3550.0; 
 "Air_Attack_Troops_Core", 2000.0; 
 "Air_Bomber_Troops_Core", 2000.0; 
 "Air_Defender_Troops_Core", 2000.0; 
 "Space_Assault_Troops_Core", 2000.0; 
 "Space_Defense_Troops_Core", 2000.0; 
 "Space_Bomber_Troops_Core", 2000.0; 
-"Nuke_Troops_Core", 4500.0; 
-"Lawyer_Troops_Core", 5000.0; 
-"Branch_Troops_Core", 4500.0; 
-"Ad_Troops_Core", 4500.0; 
-"Terror_Troops_Core", 4500.0; 
+"Nuke_Troops_Core", 3500.0; 
+"Lawyer_Troops_Core", 3000.0; 
+"Branch_Troops_Core", 3000.0; 
+"Ad_Troops_Core", 3000.0; 
+"Terror_Troops_Core", 3500.0; 
 // END CORE  
 "Settler_Troops_Overflow", 3000.0; 
 "Cow_Troops_Overflow", 0.1; 
@@ -225,11 +225,11 @@ Build_List_Element Land_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_WARRIOR", 1.0;
+ "UNIT_WARRIOR", 0.5;
  "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 2.0;
- "UNIT_MUSKETEERS", 2.5;
- "UNIT_MACHINE_GUNNER", 1.0;
+ "UNIT_PIKEMEN", 1.3;
+ "UNIT_MUSKETEERS", 1.3;
+ "UNIT_MACHINE_GUNNER", 1.3;
  "UNIT_PLASMATICA", 1.0;
  "UNIT_LEVIATHAN", 0.1;
 #END_DATA  
@@ -243,12 +243,12 @@ Build_List_Element Land_Strike_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.5;
- "UNIT_SAMURAI", 0.5;
- "UNIT_KNIGHT", 0.5;
- "UNIT_CAVALRY", 0.5;
+ "UNIT_LEGION", 0.4;
+ "UNIT_SAMURAI", 0.4;
+ "UNIT_KNIGHT", 0.4;
+ "UNIT_CAVALRY", 0.4;
  "UNIT_TANK", 0.5;
- "UNIT_FUSION_TANK", 1.0;
+ "UNIT_FUSION_TANK", 0.8;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Land_Ranged_Troops_Primary  
@@ -260,9 +260,9 @@ Build_List_Element Land_Ranged_Troops_Primary[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "UNIT_GREEK_FIRE", 0.5;
- "UNIT_CANNON", 1.5;
- "UNIT_ARTILLERY", 1.0;
- "UNIT_BATTLEBOT", 1.25;
+ "UNIT_CANNON", 0.7;
+ "UNIT_ARTILLERY", 0.8;
+ "UNIT_BATTLEBOT", 1.0;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Sea_Troops_Primary  
@@ -274,11 +274,11 @@ Build_List_Element Sea_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", -1.0;
- "UNIT_LONGSHIP", -2.0;
- "UNIT_SHIP_OF_THE_LINE", -2.0;
- "UNIT_DESTROYER", -2.0;
- "UNIT_PLASMA_DESTROYER", -2.0;
+ "UNIT_TRIREMES", 0.25;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.30;
+ "UNIT_BATTLESHIP", 0.25;
+ "UNIT_PLASMA_DESTROYER", 0.30;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Air_Defender_Troops_Primary  
@@ -332,7 +332,7 @@ Build_List_Element Slaver_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_SLAVER", -3.0;
+      "UNIT_SLAVER", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Abolitionist_Troops_Core  
@@ -377,8 +377,8 @@ Build_List_Element Spy_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SPY", -3.0;
- "UNIT_CYBER_NINJA", -3.0;
+ "UNIT_SPY", -1.0;
+ "UNIT_CYBER_NINJA", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Infector_Troops_Core  
@@ -389,7 +389,7 @@ Build_List_Element Infector_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_INFECTOR", -2.0;
+ "UNIT_INFECTOR", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Ecoterrorist_Troops_Core  
@@ -400,7 +400,7 @@ Build_List_Element Ecoterrorist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_ECOTERRORIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Defend_Troops_Core  
@@ -411,15 +411,15 @@ Build_List_Element Defend_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.75;
- "UNIT_HOPLITE", 0.75;
- "UNIT_PIKEMEN", 0.75;
- "UNIT_MUSKETEERS", 0.75;
- "UNIT_MACHINE_GUNNER", 0.75;
- "UNIT_PARATROOPER", 0.75;
- "UNIT_MARINES", 0.50;
+ "UNIT_HOPLITE", 0.7;
+ "UNIT_LEGION", 0.7;
+ "UNIT_PIKEMEN", 0.7;
+ "UNIT_MUSKETEERS", 0.7;
+ "UNIT_MACHINE_GUNNER", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
  "UNIT_PLASMATICA", 0.25;
- "UNIT_LEVIATHAN", 0.50;
+ "UNIT_LEVIATHAN", 0.5;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Assault_Troops_Core  
@@ -430,15 +430,14 @@ Build_List_Element Assault_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.75;
- "UNIT_SAMURAI", 0.75;
- "UNIT_KNIGHT", 0.75;
- "UNIT_CAVALRY", 0.75;
- "UNIT_TANK", 0.75;
- "UNIT_PARATROOPER", 1.0;
- "UNIT_MARINES", 0.75;
- "UNIT_FUSION_TANK", 0.75;
- "UNIT_SWARM", 0.75;
+ "UNIT_SAMURAI", 0.5;
+ "UNIT_KNIGHT", 0.5;
+ "UNIT_CAVALRY", 0.5;
+ "UNIT_TANK", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
+ "UNIT_FUSION_TANK", 0.5;
+ "UNIT_SWARM", 0.25;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Ranged_Troops_Core  
@@ -449,10 +448,10 @@ Build_List_Element Ranged_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 0.75;
- "UNIT_CANNON", 0.75;
- "UNIT_ARTILLERY", 0.75;
- "UNIT_BATTLEBOT", 0.75;
+ "UNIT_GREEK_FIRE", 0.5;
+ "UNIT_CANNON", 0.5;
+ "UNIT_ARTILLERY", 0.5;
+ "UNIT_BATTLEBOT", 0.5;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Attack_Troops_Core  
@@ -463,11 +462,11 @@ Build_List_Element Naval_Attack_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", 0.15;
+ "UNIT_TRIREMES", 0.2;
  "UNIT_GREEK_FIRE_TRIREME", 0.15;
- "UNIT_LONGSHIP", 0.15;
- "UNIT_SHIP_OF_THE_LINE", 0.15;
- "UNIT_BATTLESHIP", 0.15;
+ "UNIT_LONGSHIP", 0.25;
+ "UNIT_SHIP_OF_THE_LINE", 0.3;
+ "UNIT_BATTLESHIP", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Defense_Troops_Core  
@@ -478,8 +477,8 @@ Build_List_Element Naval_Defense_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_DESTROYER", 0.5;
- "UNIT_PLASMA_DESTROYER", 0.5;
+ "UNIT_DESTROYER", 0.3;
+ "UNIT_PLASMA_DESTROYER", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Transport_Troops_Core  
@@ -490,8 +489,8 @@ Build_List_Element Naval_Tranport_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TROOP_SHIP", 0.5;
- "UNIT_CRAWLER", 0.5;
+ "UNIT_TROOP_SHIP", 0.2;
+ "UNIT_CRAWLER", 0.2;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Carrier_Naval_Transport_Troops_Core  
@@ -608,7 +607,7 @@ Build_List_Element Lawyer_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LAWYER",  -10.0;
+ "UNIT_LAWYER",  -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Branch_Troops_Core  
@@ -619,7 +618,7 @@ Build_List_Element Branch_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_CORPORATE_BRANCH", -3.0;
+ "UNIT_CORPORATE_BRANCH", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Ad_Troops_Core  
@@ -630,7 +629,7 @@ Build_List_Element Ad_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SUBNEURAL_ADS", -3.0;
+ "UNIT_SUBNEURAL_ADS", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Terror_Troops_Core  
@@ -641,8 +640,8 @@ Build_List_Element Terror_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -3.0;
- "UNIT_INFECTOR", -3.0;
+ "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_INFECTOR", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Settler_Troops_Overflow  
@@ -924,13 +923,13 @@ Build_List_Element Wormhole_Probe_Troops[MAX_ELEMENTS];
 //  
 ///////////////////////////////////////////////////////////////////////////////  
 // Production threshholds 1.0 = top dog and 0.0 = loser  
-double Wonders_List_Threshhold =  0.8; 
-double Transportation_List_Threshhold =  0.6; 
+double Wonders_List_Threshhold =  0.6; 
+double Transportation_List_Threshhold =  0.4; 
 double Growth_List_Threshhold =  0.2; 
-double Happiness_List_Threshhold =  0.2; 
-double Production_List_Threshhold = 0.4; 
+double Happiness_List_Threshhold =  0.3; 
+double Production_List_Threshhold = 0.7; 
 double Gold_List_Threshhold =  0.4; 
-double Science_List_Threshhold =  0.2; 
+double Science_List_Threshhold =  0.5; 
 double Defense_List_Threshhold =  0.2; 
 double Miscellaneous_List_Threshhold =  0.0; 
 ///////////////////////////////////////////////////////////////////////////////  
@@ -942,22 +941,22 @@ Building_Build_List_Element Wonder_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
 "WONDER_WORMHOLE_DETECTOR", 20000.0; 
-"WONDER_STONEHENGE", 9250.0; 
+"WONDER_STONEHENGE", 9100.0; 
 "WONDER_SPHINX", 9250.0; 
-"WONDER_LABRYINTH_OF_THE_MINOTAUR", 9250.0; 
+"WONDER_LABRYINTH_OF_THE_MINOTAUR", 9350.0; 
 "WONDER_RAYAMANA", 9250.0; 
-"WONDER_PARTHENON", 9100.0; 
+"WONDER_PARTHENON", 9150.0; 
 "WONDER_I_CHING", 9100.0; 
 "WONDER_THE_FORBIDDEN_CITY", 9100.0; 
 "WONDER_PHILOSOPHERS_STONE", 5000.0; 
 "WONDER_HAGIA_SOPHIA", 9250.0; 
 "WONDER_GUTTENBERGS_BIBLE", 9100.0; 
-"WONDER_EAST_INDIA_COMPANY", 9100.0; 
+"WONDER_EAST_INDIA_COMPANY", 9500.0; 
 "WONDER_GALILEOS_TELESCOPE", 9100.0; 
-"WONDER_LONDON_STOCK_EXCHANGE", 9300.0; 
-"WONDER_EMANCIPATION_PROCLAMATION", 9100.0; 
+"WONDER_LONDON_STOCK_EXCHANGE", 9500.0; 
+"WONDER_EMANCIPATION_PROCLAMATION", 10000.0; 
 "WONDER_EDISONS_LAB", 10000.0; 
-"WONDER_HOLLYWOOD", 9100.0; 
+"WONDER_HOLLYWOOD", 9400.0; 
 "WONDER_WORD_INTELLIGENCE_AGENCY", 9100.0; 
 "WONDER_INTERNET", 10000.0; 
 "WONDER_THE_PILL", 9100.0; 
@@ -984,7 +983,7 @@ Building_Build_List_Element Transportation_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_AIRPORT", 7850.0; 
+"IMPROVE_AIRPORT", 9910.0; 
 "IMPROVE_RAIL_LAUNCHER", 7850.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
@@ -995,8 +994,8 @@ Building_Build_List_Element Growth_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 9000.0; 
-"IMPROVE_AQUEDUCT", 9000.0; 
+"IMPROVE_SILO", 9990.0; 
+"IMPROVE_AQUEDUCT", 9980.0; 
 "IMPROVE_BEEF_VAT", 7930.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
@@ -1008,18 +1007,18 @@ Building_Build_List_Element Happiness_List[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "IMPROVE_MIND_CONTROL_EMITTER", 8999.0;
- "IMPROVE_TEMPLE", 8999.0;
- "IMPROVE_THEATER", 8999.0;
- "IMPROVE_CIRCUS", 8999.0;
- "IMPROVE_HOSPITAL", 7990.0;
- "IMPROVE_CATHEDRAL", 8999.0;
- "IMPROVE_MOVIE_PALACE", 8999.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_WATER_TRANSFORMER", 8999.0;
- "IMPROVE_BODY_EXCHANGE", 8999.0;
- "IMPROVE_ARCOLOGIES", 8999.0;
+ "IMPROVE_TEMPLE", 9960.0;
+ "IMPROVE_THEATER", 9950.0;
+ "IMPROVE_CIRCUS", 9940.0;
+ "IMPROVE_HOSPITAL", 9930.0;
+ "IMPROVE_CATHEDRAL", 8960.0;
+ "IMPROVE_MOVIE_PALACE", 8949.0;
+ "IMPROVE_DRUG_STORE", 9920.0;
+ "IMPROVE_WATER_TRANSFORMER", 8939.0;
+ "IMPROVE_BODY_EXCHANGE", 8829.0;
+ "IMPROVE_ARCOLOGIES", 8919.0;
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+///////////////////////////////////////////////////////////////////////////////  N..
 //  
 // Production_List  
 //   
@@ -1027,18 +1026,18 @@ Building_Build_List_Element Production_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "IMPROVE_FUSION_PLANT", 10000.0;
- "IMPROVE_POPULATION_MONITOR", 8980.0; 
- "IMPROVE_MILL", 7990.0;
- "IMPROVE_FACTORY", 7990.0;
- "IMPROVE_DRUG_STORE", 8999.0;
- "IMPROVE_NUCLEAR_PLANT", 7990.0;
- "IMPROVE_ROBOTIC_PLANT", 7990.0;
- "IMPROVE_RECYCLING_PLANT", 9000.0;
- "IMPROVE_ZERO_EMISSION_VEHICLES", 8000.0;
- "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 7990.0;
- "IMPROVE_OIL_REFINERY", 7990.0;
- "IMPROVE_NANITE_FACTORY", 7990.0;
+ "IMPROVE_MILL", 8960.0;
+ "IMPROVE_DRUG_STORE", 8950.0;
+ "IMPROVE_FACTORY", 5980.0;
+ "IMPROVE_ARTIFICIAL_WOMB_COMPLEX", 5890.0;
+ "IMPROVE_POPULATION_MONITOR", 5880.0; 
+ "IMPROVE_NUCLEAR_PLANT", 5990.0;
+ "IMPROVE_ROBOTIC_PLANT", 2890.0;
+ "IMPROVE_RECYCLING_PLANT", 6000.0;
+ "IMPROVE_ZERO_EMISSION_VEHICLES", 4990.0;
+ "IMPROVE_OIL_REFINERY", 3000.0;
+ "IMPROVE_FUSION_PLANT", 4000.0;
+ "IMPROVE_NANITE_FACTORY", 4990.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1048,13 +1047,12 @@ Building_Build_List_Element Gold_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_BAZAAR", 7980.0; 
-"IMPROVE_BANK", 7980.0; 
+"IMPROVE_BAZAAR", 9900.0; 
+"IMPROVE_BANK", 8990.0; 
 "IMPROVE_CITY_CLOCK", 7990.0; 
-"IMPROVE_TELEVISION", 7980.0; 
-"IMPROVE_AIRPORT", 7850.0; 
-"IMPROVE_HOUSE_OF_FREEZING", 8920.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7980.0; 
+"IMPROVE_TELEVISION", 6930.0; 
+"IMPROVE_AIRPORT", 8850.0; 
+"IMPROVE_HOUSE_OF_FREEZING", 6920.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1064,11 +1062,11 @@ Building_Build_List_Element Science_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_ACADEMY", 7950.0; 
+"IMPROVE_ACADEMY", 8980.0; 
+"IMPROVE_LIBRARY", 8970.0; 
 "IMPROVE_UNIVERSITY", 7950.0; 
-"IMPROVE_LIBRARY", 7950.0; 
-"IMPROVE_COMPUTER_CENTER", 7950.0; 
-"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 7950.0; 
+"IMPROVE_COMPUTER_CENTER", 7850.0; 
+"IMPROVE_EMBEDDED_KNOWLEDGE_CHIP", 6950.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1078,12 +1076,12 @@ Building_Build_List_Element Defense_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_CITY_WALLS", 7950.0; 
+"IMPROVE_CITY_WALLS", 9970.0; 
 "IMPROVE_SDI", 7950.0; 
 "IMPROVE_BIO_WARFARE_FILTERS", 7950.0; 
-"IMPROVE_FORCEFIELD", 7950.0; 
+"IMPROVE_FORCEFIELD", 8950.0; 
 #END_DATA  
-///////////////////////////////////////////////////////////////////////////////  
+/////////////////////////////////////////////////////////////////////////////// N.. 
 //  
 // Miscellaneous_List  
 //   
@@ -1091,11 +1089,11 @@ Building_Build_List_Element Miscellaneous_List[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-"IMPROVE_SILO", 5000.0; 
-"IMPROVE_CITY_WALLS", 7980.0; 
-"IMPROVE_BAZAAR", 8500.0; 
-"IMPROVE_COURTHOUSE", 7980.0; 
-"IMPROVE_POPULATION_MONITOR", 7980.0; 
+"IMPROVE_SILO", 9900.0; 
+"IMPROVE_CITY_WALLS", 9500.0; 
+"IMPROVE_BAZAAR", 9000.0; 
+"IMPROVE_COURTHOUSE", 8500.0; 
+"IMPROVE_POPULATION_MONITOR", 8000.0; 
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 //  
@@ -1108,36 +1106,39 @@ Building_Build_List_Element Miscellaneous_List[MAX_ELEMENTS];
 ///////////////////////////////////////////////////////////////////////////////  
 //  
 // Advancements_List  
-//   
+//   N..
 Advancement_Element Advancements_List[MAX_ELEMENTS];  
 #DATA  
 //  
-//--------------------------------------------------------------------  
+//-------------------------------------------------------------------- 
+ "ADVANCE_CORPORATION"; 
+ "ADVANCE_BUREAUCRACY";
  "ADVANCE_AGRICULTURE"; 
  "ADVANCE_TOOLMAKING"; 
+ "ADVANCE_TRADE"; 
  "ADVANCE_MINING"; 
+ "ADVANCE_BANKING";
  "ADVANCE_SHIP_BUILDING"; 
+ "ADVANCE_THEOCRACY";
  "ADVANCE_DOMESTICATION"; 
  "ADVANCE_BRONZE_WORKING"; 
  "ADVANCE_STONE_WORKING"; 
+ "ADVANCE_MONARCHY"; 
+ "ADVANCE_RELIGION"; 
  "ADVANCE_JURISPRUDENCE"; 
  "ADVANCE_WRITING"; 
  "ADVANCE_GEOMETRY"; 
- "ADVANCE_MONARCHY"; 
  "ADVANCE_IRON_WORKING"; 
- "ADVANCE_RELIGION"; 
  "ADVANCE_CITY_STATE"; 
- "ADVANCE_PHILOSOPHY"; 
- "ADVANCE_TRADE"; 
- "ADVANCE_BUREAUCRACY"; 
+ "ADVANCE_PHILOSOPHY";  
+ "ADVANCE_ALCHEMY"; 
+ "ADVANCE_ENGINEERING"; 
  "ADVANCE_ASTRONOMY"; 
- "ADVANCE_THEOCRACY"; 
- "ADVANCE_BANKING"; 
  "ADVANCE_STIRRUP"; 
- "ADVANCE_ENGINEERING"; 
- "ADVANCE_ALCHEMY"; 
  "ADVANCE_CLASSICAL_EDUCATION"; 
  "ADVANCE_HULL_MAKING"; 
+ "ADVANCE_MECHANICAL_CLOCK"; 
+ "ADVANCE_OPTICS";
  "ADVANCE_MEDICINE"; 
  "ADVANCE_AGRICULTURAL_REVOLUTION"; 
  "ADVANCE_GUNPOWDER"; 
@@ -1146,11 +1147,10 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_PRINTING_PRESS"; 
  "ADVANCE_MACHINE_TOOLS"; 
  "ADVANCE_CANNON_MAKING"; 
- "ADVANCE_MECHANICAL_CLOCK"; 
- "ADVANCE_OPTICS"; 
  "ADVANCE_CAVALRY_TACTICS"; 
  "ADVANCE_NATIONALISM"; 
  "ADVANCE_CHEMISTRY"; 
+ "ADVANCE_CONSUMER_ELECTRONICS";
  "ADVANCE_PHYSICS"; 
  "ADVANCE_AGE_OF_REASON"; 
  "ADVANCE_DEMOCRACY"; 
@@ -1158,8 +1158,7 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_ELECTRICITY"; 
  "ADVANCE_RAILROAD"; 
  "ADVANCE_INDUSTRIAL_REVOLUTION"; 
- "ADVANCE_STEEL"; 
- "ADVANCE_CORPORATION"; 
+ "ADVANCE_STEEL";  
  "ADVANCE_OIL_REFINING"; 
  "ADVANCE_EXPLOSIVES"; 
  "ADVANCE_COMMUNISM"; 
@@ -1172,22 +1171,21 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_QUANTUM_MECHANICS"; 
  "ADVANCE_GLOBAL_DEFENSE_INITIATIVE"; 
  "ADVANCE_JET_PROPULSION"; 
- "ADVANCE_MASS_PRODUCTION"; 
- "ADVANCE_CONSUMER_ELECTRONICS"; 
+ "ADVANCE_MASS_PRODUCTION";  
  "ADVANCE_GENETICS"; 
  "ADVANCE_COMPUTER"; 
  "ADVANCE_SPACE_FLIGHT"; 
  "ADVANCE_ENVIRONMENTALISM"; 
  "ADVANCE_GLOBAL_COMMUNICATIONS_NETWORK"; 
  "ADVANCE_ADVANCED_COMPOSITES"; 
+ "ADVANCE_SEA_COLONIES"; 
+ "ADVANCE_SUPERCONDUCTOR"; 
  "ADVANCE_MULTINATIONAL_REPUBLIC"; 
  "ADVANCE_ROBOTICS"; 
- "ADVANCE_WORMHOLES"; 
  "ADVANCE_UNIFIED_FIELD_THEORY"; 
  "ADVANCE_LIFE_EXTENSION"; 
  "ADVANCE_AI_SURVEILLANCE"; 
  "ADVANCE_ARCOLOGIES"; 
- "ADVANCE_SEA_COLONIES"; 
  "ADVANCE_SPACE_COLONIES"; 
  "ADVANCE_INTELLIGENT_MATERIALS"; 
  "ADVANCE_FUSION"; 
@@ -1195,20 +1193,20 @@ Advancement_Element Advancements_List[MAX_ELEMENTS];
  "ADVANCE_NEURAL_SILICON_INTERFACE"; 
  "ADVANCE_PERSONAL_ENCRYPTION"; 
  "ADVANCE_TECHNOCRACY"; 
- "ADVANCE_SUPERCONDUCTOR"; 
  "ADVANCE_HUMAN_CLONING"; 
  "ADVANCE_GENETIC_TAILORING"; 
+ "ADVANCE_ULTRAPRESSURE_MACHINERY"; 
+ "ADVANCE_WORMHOLES"; 
  "ADVANCE_ZERO_G_MANUFACTURING"; 
  "ADVANCE_CRYONICS"; 
  "ADVANCE_ECOTOPIA"; 
  "ADVANCE_MIND_CONTROL"; 
- "ADVANCE_ULTRAPRESSURE_MACHINERY"; 
  "ADVANCE_SUBNEURAL_ADS"; 
  "ADVANCE_ASTEROID_MINING"; 
  "ADVANCE_NANOASSEMBLY"; 
  "ADVANCE_WILDERNESS_PRESERVATION_ACT"; 
  "ADVANCE_GAIA_THEORY"; 
- "ADVANCE_VIRTUAL_DEMOCRACY"; 
+ "ADVANCE_VIRTUAL_DEMOCRACY";
+ "ADVANCE_CLOAKING";  
  "ADVANCE_ALIEN_ARCHEOLOGY"; 
- "ADVANCE_CLOAKING"; 
 #END_DATA  
```

## aidata/AIPs/supernaval.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\supernaval.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\supernaval.aip"
index 73a0e88..394f125 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\supernaval.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\supernaval.aip"
@@ -93,18 +93,18 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 #DATA  
 //LIST NAME PRIORITY  
 //----------------------------------------------------  
-"Land_Settler_Troops_Primary", 10500.0; 
+//"Land_Settler_Troops_Primary", 10500.0; //WW
 "Sea_Settler_Troops_Primary", 11000.0; 
 "Space_Settler_Troops_Primary", 11000.0; 
 "Scout_Troops_Primary", 25000.0; 
 "Land_Troops_Primary", 6000.0; 
 "Land_Strike_Troops_Primary", 6000.0; 
 "Land_Ranged_Troops_Primary", 6000.0; 
-"Sea_Troops_Primary", 6000.0; 
+"Sea_Troops_Primary", 7000.0; 
 "Air_Defender_Troops_Primary", 10000.0; 
 "Space_Defense_Troops_Primary", 10000.0; 
 // END PRIMARY  
-"Settler_Troops_Core", 3500.0; 
+//"Settler_Troops_Core", 3000.0; //WW
 "Slaver_Troops_Core", 6001; 
 "Abolitionist_Troops_Core", 6001; 
 "Diplomatic_Troops_Core", 2500.0; 
@@ -115,24 +115,24 @@ Build_List_Class Build_List_Classes[MAX_BUILD_LISTS];
 "Defend_Troops_Core", 3500.0; 
 "Assault_Troops_Core", 3500.0; 
 "Ranged_Troops_Core", 3500.0; 
-"Naval_Attack_Troops_Core", 3050.0; 
-"Naval_Defense_Troops_Core", 3050.0; 
-"Naval_Tranport_Troops_Core", 4501.0; 
-"Carrier_Naval_Transport_Troops_Core", 3050.0; 
-"Naval_Stealth_Troops_Core", 3050.0; 
+"Naval_Attack_Troops_Core", 3550.0; 
+"Naval_Defense_Troops_Core", 3550.0; 
+"Naval_Tranport_Troops_Core", 7550.0; 
+"Carrier_Naval_Transport_Troops_Core", 1650.0; 
+"Naval_Stealth_Troops_Core", 3550.0; 
 "Air_Attack_Troops_Core", 2000.0; 
 "Air_Bomber_Troops_Core", 2000.0; 
 "Air_Defender_Troops_Core", 2000.0; 
 "Space_Assault_Troops_Core", 2000.0; 
 "Space_Defense_Troops_Core", 2000.0; 
 "Space_Bomber_Troops_Core", 2000.0; 
-"Nuke_Troops_Core", 4500.0; 
-"Lawyer_Troops_Core", 5000.0; 
-"Branch_Troops_Core", 4500.0; 
-"Ad_Troops_Core", 4500.0; 
-"Terror_Troops_Core", 4500.0; 
+"Nuke_Troops_Core", 3500.0; 
+"Lawyer_Troops_Core", 3000.0; 
+"Branch_Troops_Core", 3000.0; 
+"Ad_Troops_Core", 3000.0; 
+"Terror_Troops_Core", 3500.0; 
 // END CORE  
-"Settler_Troops_Overflow", 3000.0; 
+//"Settler_Troops_Overflow", 3000.0; //WW
 "Cow_Troops_Overflow", 0.1; 
 "Slaver_Troops_Overflow", 1500.0; 
 "Scout_Troops_Overflow", 1500.0; 
@@ -220,11 +220,11 @@ Build_List_Element Land_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_WARRIOR", 1.0;
+ "UNIT_WARRIOR", 0.5;
  "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 2.0;
- "UNIT_MUSKETEERS", 2.5;
- "UNIT_MACHINE_GUNNER", 1.0;
+ "UNIT_PIKEMEN", 1.3;
+ "UNIT_MUSKETEERS", 1.3;
+ "UNIT_MACHINE_GUNNER", 1.3;
  "UNIT_PLASMATICA", 1.0;
  "UNIT_LEVIATHAN", 0.1;
 #END_DATA  
@@ -238,12 +238,12 @@ Build_List_Element Land_Strike_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.5;
- "UNIT_SAMURAI", 0.5;
- "UNIT_KNIGHT", 0.5;
- "UNIT_CAVALRY", 0.5;
+ "UNIT_LEGION", 0.4;
+ "UNIT_SAMURAI", 0.4;
+ "UNIT_KNIGHT", 0.4;
+ "UNIT_CAVALRY", 0.4;
  "UNIT_TANK", 0.5;
- "UNIT_FUSION_TANK", 2.0;
+ "UNIT_FUSION_TANK", 0.8;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Land_Ranged_Troops_Primary  
@@ -255,9 +255,9 @@ Build_List_Element Land_Ranged_Troops_Primary[MAX_ELEMENTS];
 //  
 //--------------------------------------------------------------------  
  "UNIT_GREEK_FIRE", 0.5;
- "UNIT_CANNON", 1.5;
- "UNIT_ARTILLERY", 1.0;
- "UNIT_BATTLEBOT", 1.25;
+ "UNIT_CANNON", 0.7;
+ "UNIT_ARTILLERY", 0.8;
+ "UNIT_BATTLEBOT", 1.0;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Sea_Troops_Primary  
@@ -269,11 +269,11 @@ Build_List_Element Sea_Troops_Primary[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES",  -3.0;
- "UNIT_LONGSHIP",  -3.0;
- "UNIT_SHIP_OF_THE_LINE",  -4.0;
- "UNIT_DESTROYER",  -4.0;
- "UNIT_PLASMA_DESTROYER",  -4.0;
+ "UNIT_TRIREMES", 0.45;
+ "UNIT_LONGSHIP", 0.45;
+ "UNIT_SHIP_OF_THE_LINE", 0.50;
+ "UNIT_BATTLESHIP", 0.25;
+ "UNIT_PLASMA_DESTROYER", 0.30;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Air_Defender_Troops_Primary  
@@ -327,7 +327,7 @@ Build_List_Element Slaver_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
-      "UNIT_DIPLOMAT", -2.0;
+      "UNIT_DIPLOMAT", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Abolitionist_Troops_Core  
@@ -338,7 +338,7 @@ Build_List_Element Abolitionist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ABOLITIONIST", -3.0;
+ "UNIT_ABOLITIONIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Diplomatic_Troops_Core  
@@ -372,8 +372,8 @@ Build_List_Element Spy_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SPY", -3.0;
- "UNIT_CYBER_NINJA", -3.0;
+ "UNIT_SPY", -1.0;
+ "UNIT_CYBER_NINJA", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Infector_Troops_Core  
@@ -384,7 +384,7 @@ Build_List_Element Infector_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_INFECTOR", -2.0;
+ "UNIT_INFECTOR", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Ecoterrorist_Troops_Core  
@@ -395,7 +395,7 @@ Build_List_Element Ecoterrorist_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_ECOTERRORIST", -1.0;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Defend_Troops_Core  
@@ -406,15 +406,15 @@ Build_List_Element Defend_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 1.0;
- "UNIT_HOPLITE", 1.0;
- "UNIT_PIKEMEN", 1.0;
- "UNIT_MUSKETEERS", 1.0;
- "UNIT_MACHINE_GUNNER", 1.0;
- "UNIT_PARATROOPER", 1.0;
- "UNIT_MARINES", 0.75;
+ "UNIT_HOPLITE", 0.7;
+ "UNIT_LEGION", 0.7;
+ "UNIT_PIKEMEN", 0.7;
+ "UNIT_MUSKETEERS", 0.7;
+ "UNIT_MACHINE_GUNNER", 0.7;
+ "UNIT_PARATROOPER", 0.5;
+ "UNIT_MARINES", 0.5;
  "UNIT_PLASMATICA", 0.25;
- "UNIT_LEVIATHAN", 0.75;
+ "UNIT_LEVIATHAN", 0.5;
 #END_DATA  
 ///////////////////////////////////////////////////////////////////////////////  
 // Assault_Troops_Core  
@@ -425,7 +425,6 @@ Build_List_Element Assault_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_LEGION", 0.5;
  "UNIT_SAMURAI", 0.5;
  "UNIT_KNIGHT", 0.5;
  "UNIT_CAVALRY", 0.5;
@@ -433,7 +432,7 @@ Build_List_Element Assault_Troops_Core[MAX_ELEMENTS];
  "UNIT_PARATROOPER", 0.5;
  "UNIT_MARINES", 0.5;
  "UNIT_FUSION_TANK", 0.5;
- "UNIT_SWARM", 0.5;
+ "UNIT_SWARM", 0.25;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Ranged_Troops_Core  
@@ -444,10 +443,10 @@ Build_List_Element Ranged_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 0.75;
- "UNIT_CANNON", 0.75;
- "UNIT_ARTILLERY", 0.75;
- "UNIT_BATTLEBOT", 0.75;
+ "UNIT_GREEK_FIRE", 0.5;
+ "UNIT_CANNON", 0.5;
+ "UNIT_ARTILLERY", 0.5;
+ "UNIT_BATTLEBOT", 0.5;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Attack_Troops_Core  
@@ -458,11 +457,11 @@ Build_List_Element Naval_Attack_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_TRIREMES", 0.75;
- "UNIT_GREEK_FIRE_TRIREME", 0.75;
- "UNIT_LONGSHIP", 0.75;
- "UNIT_SHIP_OF_THE_LINE", 0.75;
- "UNIT_BATTLESHIP", 0.15;
+ "UNIT_TRIREMES", 0.5;
+ "UNIT_GREEK_FIRE_TRIREME", 0.2;
+ "UNIT_LONGSHIP", 0.7;
+ "UNIT_SHIP_OF_THE_LINE", 0.7;
+ "UNIT_BATTLESHIP", 0.3;
 #END_DATA       
 ///////////////////////////////////////////////////////////////////////////////  
 // Naval_Defense_Troops_Core  
@@ -614,7 +613,7 @@ Build_List_Element Branch_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_CORPORATE_BRANCH", -3.0;
+ "UNIT_CORPORATE_BRANCH", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Ad_Troops_Core  
@@ -625,7 +624,7 @@ Build_List_Element Ad_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_SUBNEURAL_ADS", -3.0;
+ "UNIT_SUBNEURAL_ADS", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Terror_Troops_Core  
@@ -636,8 +635,8 @@ Build_List_Element Terror_Troops_Core[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_ECOTERRORIST", -3.0;
- "UNIT_INFECTOR", -3.0;
+ "UNIT_ECOTERRORIST", -2.0;
+ "UNIT_INFECTOR", -2.0;
 #END_DATA     
 ///////////////////////////////////////////////////////////////////////////////  
 // Settler_Troops_Overflow  
@@ -737,7 +736,7 @@ Build_List_Element Ranged_Troops_Overflow[MAX_ELEMENTS];
 #DATA  
 //  
 //--------------------------------------------------------------------  
- "UNIT_GREEK_FIRE", 0.5;
+ "UNIT_GREEK_FIRE", 3.0;
  "UNIT_CANNON", 3.0;
  "UNIT_ARTILLERY", 3.0;
  "UNIT_BATTLEBOT", 3.0;
```

## aidata/AIPs/takecity.aip
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\takecity.aip" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\takecity.aip"
index bd385a7..67cd1ed 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\AIPs\\takecity.aip"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\AIPs\\takecity.aip"
@@ -51,7 +51,7 @@ double max_misc_bid_bonus = 1000.0;
 // If a particular type of goal prefers (but does not demand) some type  
 // of unit, add this to the priority  
     
-double distance_from_unit_priority_modifier = -500.0; 
+double distance_from_unit_priority_modifier = -1500.0; 
     
     
     
@@ -60,6 +60,7 @@ double distance_from_unit_priority_modifier = -500.0;
 // FORCE MATCHING  
 double min_defense_matching_force_ratio =  1.2; 
 double min_attack_matching_force_ratio =  1.2; 
+int num_city_defenders = 1; //WW inserted
 #define MAX_EVAL_SEIGE_GOALS -15 
 #define MAX_EVAL_EXPLORE_GOALS -15 
    
```

## aidata/diplomacy_accepted.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\diplomacy_accepted.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\diplomacy_accepted.fli"
index ec10e0b..4c5752d 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\diplomacy_accepted.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\diplomacy_accepted.fli"
@@ -12,14 +12,26 @@ output diplomatic_regard_delta[-20, 20] = 0.0
 	tri love_him_more(diplomatic_regard_delta, 8, 2.0)
 	right worship_him_more(diplomatic_regard_delta, 12, 4)
 
+///////////////////////////////////
+////////// SET LOYALTY  ///////////
+///////////////////////////////////
+	// N: values changed	
+
+output loyalty_modifier [-20, 20] = 0
+	tri benedict_arnold(loyalty_modifier, -10.0, 1.0)
+	tri trust_much_less(loyalty_modifier, -2.0, 1.0)
+	tri trust_less(loyalty_modifier, 0, 0)
+	tri trust_more(loyalty_modifier, 2.0, 1.0)
+	tri trust_much_more(loyalty_modifier, 5.0, 1.0)
+
 input he_accepted_greetings
 right yes_he_accepted_greetings(he_accepted_greetings, 1.0, .5)
 
 
-//accepted greetings
+//accepted greetings...N: changed
 	if(yes_he_accepted_greetings)
 	{
-		love_him_more
+		same_like_him
 	}
 
 //accepted advance demand
@@ -28,7 +40,7 @@ right yes_he_accepted_demand_advance(he_accepted_demand_advance, 1.0, .5)
 
 	if(yes_he_accepted_demand_advance)
 	{
-		like_him_more
+		love_him_more
 	}
 
 //accepted gold demand
@@ -37,7 +49,7 @@ right yes_he_accepted_gold_demand(he_accepted_gold_demand, 1.0, .5)
 
 	if(yes_he_accepted_gold_demand)
 	{
-		like_him_more
+		love_him_more
 	}
 
 //accepted map demand
@@ -49,31 +61,34 @@ right yes_he_accepted_demand_map(he_accepted_demand_map, 1.0, .5)
 		like_him_more
 	}
 
-//accepted leave our lands demand
+//accepted leave our lands demand..N: changed
 input he_accepted_demand_leave_our_lands
 right yes_he_accepted_demand_leave_our_lands(he_accepted_demand_leave_our_lands, 1.0, .5)
 
 	if(yes_he_accepted_demand_leave_our_lands)
 	{
 		like_him_more
+		trust_more
 	}
 
-//accepted reduce pollution demand
+//accepted reduce pollution demand..N: changed
 input he_accepted_demand_reduce_pollution
 right yes_he_accepted_demand_reduce_pollution(he_accepted_demand_reduce_pollution, 1.0, .5)
 
 	if(yes_he_accepted_demand_reduce_pollution)
 	{
 		like_him_more
+		trust_more
 	}
 
-//accepted stop piracy demand
+//accepted stop piracy demand..N: changed
 input he_accepted_demand_no_piracy
 right yes_he_accepted_demand_no_piracy(he_accepted_demand_no_piracy, 1.0, .5)
 
 	if(yes_he_accepted_demand_no_piracy)
 	{
-		love_him_more
+		like_him_more
+		trust_more
 	}
 
 //accepted stop trade demand
@@ -85,13 +100,14 @@ right yes_he_accepted_demand_stop_trade(he_accepted_demand_stop_trade, 1.0, .5)
 		like_him_more
 	}
 
-//accepted attack enemy
+//accepted attack enemy..N: changed
 input he_accepted_demand_attack_enemy
 right accepted_attack(he_accepted_demand_attack_enemy, 1.0, 0.5)
 
 	if(accepted_attack)	
 	{
-		like_him_more
+		love_him_more
+		trust_more
 	}
 
 //accepted exchange advance 
@@ -103,13 +119,32 @@ right yes_he_accepted_exchange_advance(he_accepted_exchange_advance, 1.0, .5)
 		love_him_more
 	}
 
+// N: added..accepted exchange advance at war 
+input war_with_him
+	left no_war (war_with_him, 0.0, .5)
+	right yes_war (war_with_him, 1.0, .5)
+
+	if(yes_he_accepted_exchange_advance
+		and yes_war)
+	{
+		same_like_him
+	}
+
 //accepted exchange map
 input he_accepted_exchange_map
 right yes_he_accepted_exchange_map(he_accepted_exchange_map, 1.0, .5)
 
 	if(yes_he_accepted_exchange_map)
 	{
-		love_him_more
+		like_him_more
+	}
+
+// N: added..accepted exchange map at war
+
+	if(yes_he_accepted_exchange_map
+		and yes_war)
+	{
+		same_like_him
 	}
 
 //accepted advance offer
@@ -127,28 +162,39 @@ right yes_he_accepted_offer_gold(he_accepted_offer_gold, 1.0, .5)
 
 	if(yes_he_accepted_offer_gold)
 	{
-		love_him_more
+		like_him_more
 	}
 
-//accepted map offer
+//accepted map offer..N: changed
 input he_accepted_offer_map
 right yes_he_accepted_offer_map(he_accepted_offer_map, 1.0, .5)
 
 	if(yes_he_accepted_offer_map)
 	{
-		love_him_more
+		same_like_him
 	}
 
 
-//accepted cease fire
+//accepted cease fire..N: changed
 input he_accepted_offer_cease_fire
 right yes_he_accepted_offer_cease_fire(he_accepted_offer_cease_fire, 1.0, .5)
 
 	if(yes_he_accepted_offer_cease_fire)
 	{
-		love_him_more
+		like_him_more
 	}
 
+// N: added..accepted cease fire not at war
+input he_accepted_offer_cease_fire
+right yes_he_accepted_offer_cease_fire(he_accepted_offer_cease_fire, 1.0, .5)
+
+	if(yes_he_accepted_offer_cease_fire
+		and not yes_war)
+	{
+		like_him_more
+	}
+
+
 //accepted permanent alliance
 input he_accepted_offer_alliance
 right yes_he_accepted_offer_alliance(he_accepted_offer_alliance, 1.0, .5)
@@ -164,5 +210,5 @@ right he_accepted_ecopact(he_accepted_offer_pact_end_pollution, 1.0, 0.5)
 
 	if(he_accepted_ecopact)
 	{
-		love_him_more
+		like_him_more
 	}
```

## aidata/diplomacy_begin.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\diplomacy_begin.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\diplomacy_begin.fli"
index 51a1b6a..09bc41c 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\diplomacy_begin.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\diplomacy_begin.fli"
@@ -113,6 +113,7 @@ input time
 	////////////////////////////////////////////////////////
 	////////// HOW MANY PLAYERS IS HE FIGHTING?  ///////////
 	////////////////////////////////////////////////////////
+	// N: added 8/11/99
 
 	input num_he_is_at_war
 		tri he_fights_zero(num_he_is_at_war, 0.0, 0.5)
@@ -124,6 +125,15 @@ input time
 		tri he_fights_six(num_he_is_at_war, 6.0, 0.5)
 		tri he_fights_seven(num_he_is_at_war, 7.0, 0.5)
 		tri he_fights_eight(num_he_is_at_war, 8.0, 0.5)
+		tri he_fights_nine(num_he_is_at_war, 9.0, 0.5)
+		tri he_fights_ten(num_he_is_at_war, 10.0, 0.5)
+		tri he_fights_eleven(num_he_is_at_war, 11.0, 0.5)
+		tri he_fights_twelve(num_he_is_at_war, 12.0, 0.5)
+		tri he_fights_thirteen(num_he_is_at_war, 13.0, 0.5)
+		tri he_fights_fourteen(num_he_is_at_war, 14.0, 0.5)
+		tri he_fights_fifteen(num_he_is_at_war, 15.0, 0.5)
+		tri he_fights_sixteen(num_he_is_at_war, 16.0, 0.5)
+
 
 
 	////////////////////////////////////////////////////////////////
@@ -262,12 +272,12 @@ input time
 	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 	////////// HOW MANY SOLDIERS DOES HE HAVE IN MY LAND?  /////////////////////
 	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
-
+	// Changed again--to set new border policy--WAIS..N.
 	input military_incursions
 		left no_incursions(military_incursions, 0, 0.5)
 		tri few_incursions(military_incursions, 1, 0.1)
-		tri many_incursions(military_incursions, 3, 0.5)
-		right floods_incursions(military_incursions, 4, 0.5)
+		tri many_incursions(military_incursions, 2, 0.5)
+		right floods_incursions(military_incursions, 3, 0.5)
 
 	///////////////////////////////////////////////////////////////////////////////////
 	////////// HOW DO I FEEL ABOUT HIM?  /////////////////////
@@ -282,7 +292,7 @@ input time
 		tri like_him(diplomatic_regard_towards_him, 70, 12)
 		right love_him(diplomatic_regard_towards_him, 90, 12)
 
-	////////////////////////////////////////////////////////////////////////////////////////////////////////
+	////////////////////////////////////////////////////////////////////////////////////////////////////////N: adjusted...changed back
 	////////// HOW MUCH DO I WANT TO FIGHT HIM?  /////////////////////
 	////////////////////////////////////////////////////////////////////////////////////////////////////////
         
@@ -423,6 +433,14 @@ input time
 		tri six_at_war(at_war_count, 6.0, 0.5)
 		tri seven_at_war(at_war_count, 7.0, 0.5)
 		tri eight_at_war(at_war_count, 8.0, 0.5)
+		tri nine_at_war(at_war_count, 9.0, 0.5)
+		tri ten_at_war(at_war_count, 10.0, 0.5)
+		tri eleven_at_war(at_war_count, 11.0, 0.5)
+		tri twelve_at_war(at_war_count, 12.0, 0.5)
+		tri thirteen_at_war(at_war_count, 13.0, 0.5)
+		tri fourteen_at_war(at_war_count, 14.0, 0.5)
+		tri fifteen_at_war(at_war_count, 15.0, 0.5)
+		tri sixteen_at_war(at_war_count, 16.0, 0.5)
 
 	///////////////////////////////////////////
 	////////// WHAT IS MY RANKING?  ///////////
@@ -439,21 +457,23 @@ input time
 	/////////////////////////////////////////////////////////////////////
 	////////// HOW MANY SOLDIER DO I HAVE IN FOREIGN LAND?  /////////////
 	/////////////////////////////////////////////////////////////////////
+	// N: WAIS--Wandering AI Syndrome--changed
 
 	input my_military_incursions
-		left no_my_incurions(my_military_incursions, 0, 0.5)
-		tri some_my_incurions(my_military_incursions, 2, 1)
-		right many_my_incurions(my_military_incursions, 6, 3)
+		left no_my_incurions(my_military_incursions, 0, 0.25)
+		tri some_my_incurions(my_military_incursions, 1, 0.5)
+		right many_my_incurions(my_military_incursions, 2, 1)
 
 ///////////////////////////////////
 ////////// SET LOYALTY  ///////////
 ///////////////////////////////////
+	// N: values changed	
 
 output loyalty_modifier [-20, 20] = 0
 	tri benedict_arnold(loyalty_modifier, -10.0, 1.0)
-	tri trust_much_less(loyalty_modifier, -5.0, 1.0)
-	tri trust_less(loyalty_modifier, -1.0, 1.0)
-	tri trust_more(loyalty_modifier, 1.0, 1.0)
+	tri trust_much_less(loyalty_modifier, -2.0, 1.0)
+	tri trust_less(loyalty_modifier, 0, 0)
+	tri trust_more(loyalty_modifier, 2.0, 1.0)
 	tri trust_much_more(loyalty_modifier, 5.0, 1.0)
 
 	//////////////////////////////////////////////////////
@@ -470,11 +490,19 @@ output loyalty_modifier [-20, 20] = 0
 	////////// FIGHT MY FRIENDS, TRUST YOU LESS  /////////
 	//////////////////////////////////////////////////////
 
+	// N: changed
+	if(twice_attacked_my_friends)
+	{
+		trust_much_less
+	}	
+
+	// N: added
 	if(thrice_attacked_my_friends)
 	{
-		trust_less
+		benedict_arnold
 	}	
 
+
 	//////////////////////////////////////////////////////
 	////////// BREAK TREATIES, TRUST YOU LESS  ///////////
 	//////////////////////////////////////////////////////
@@ -485,6 +513,12 @@ output loyalty_modifier [-20, 20] = 0
 		trust_much_less
 	}
 	
+	if( (sometimes_broke_treaties or often_broke_treaties)
+		and not human )
+	{
+		benedict_arnold
+	}
+	
 	if( (sometimes_broke_treaties or often_broke_treaties)
 		and human ) 
 	{
@@ -494,7 +528,7 @@ output loyalty_modifier [-20, 20] = 0
 	if (( rarely_broke_treaties or sometimes_broke_treaties or often_broke_treaties)
 		and not human)
 	{
-			trust_less
+			trust_much_less
 	}
 			 
 /////////////////////////////////////
@@ -529,7 +563,7 @@ output loyalty_modifier [-20, 20] = 0
 		tri little_like_strength(dip_regard_strength_delta, 5.0, 5.0)
 		tri much_like_strength(dip_regard_strength_delta, 10.0, 5.0)
 
-	// LIKE HIM LESS IF HE'S IN FIRST PLACE AND I'M NOT IN LAST PLACE
+	// N: not LIKE HIM LESS IF HE'S IN FIRST PLACE AND I'M NOT IN LAST PLACE
 	if(	hes_in_first_place 
 		and not iam_in_last_place 
 		and not iam_in_top_ten_percent
@@ -537,22 +571,25 @@ output loyalty_modifier [-20, 20] = 0
 		and not my_best_friend
 		and not human )
 		{
-			much_hate_strength
+			little_hate_strength
+			trust_much_less
 		}
-
+	
+	// N: changed
 	if(	hes_in_first_place 
 		and human
 		and not iam_in_last_place 
 		and not iam_in_top_ten_percent )	
 		{
-			much_hate_strength
+			tiny_hate_strength
+			trust_much_less
 		}
 
 //	if(	hes_in_first_place 
 //		and not iam_in_last_place 
 //		and (neutral_towards_him or dislike_him))
 //		{
-//			little_hate_strength
+//			tiny_hate_strength
 //		}
 
 	// LIKE HIM MORE IF I'M IN LAST AND HE'S IN FIRST EXCEPT WHEN HE'S MY WORST ENEMY
@@ -570,6 +607,68 @@ output loyalty_modifier [-20, 20] = 0
 		{
 			little_like_strength
 		}
+	////////////////////////////////////////////////////////////
+	//////////   REGARD LOST DUE TO LAST PLACE...N   //////////
+	////////////////////////////////////////////////////////////
+
+	// N: added...If you're in last place and close,
+	// and I'm warlike, I'll bully you a lot
+	if(	iam_in_first_place
+		and warlike	
+		and hes_in_last_place
+		and yes_closest_capitol 
+		and yes_he_shares_continent 
+		and not my_worst_enemy)
+		{
+			loath_him_more
+		}
+
+	// N: added...If you're in last place & not close,
+	// and I'm warlike, I'll bully you somewhat
+	if(	iam_in_first_place
+		and warlike	
+		and hes_in_last_place
+		and yes_he_shares_continent  
+		and not my_worst_enemy)
+		{
+			dislike_him_more
+		}
+
+////////////////////////////////////////////////////////////////////////////////////////
+//////////   SET STRENGTH OF STATE OF WAR      ///////////
+////////////////////////////////////////////////////////////////////////////////////////
+// 
+// when unit regard is less than 20, we target the enemy.
+
+output unit_regard_delta[-100, 100] = 0.0
+	tri go_to_hot_war(unit_regard_delta, 10, 80.0)
+	tri go_to_hot_war_prep(unit_regard_delta, 25, 1.0)
+	tri go_to_cold_war(unit_regard_delta, 35, 1.0)
+	tri go_to_cold_war_prep(unit_regard_delta, 50, 0.5)
+	tri go_to_peace_partial(unit_regard_delta, 60, 0.55)
+	tri go_to_peace_full(unit_regard_delta, 80, 2.0)
+
+	////////////////////////////////////////////////////////////
+	////////// N: added.. UNDERDOG AI CATCHING UP     //////////
+	////////////////////////////////////////////////////////////
+	// special plan and war settings...N: moved up here
+
+		output special_plan[0.0, 2.0] = 0.0
+		tri yes_special_plan(special_plan, 1.0, 0.5)
+
+	// N: added...If I'm in last place and weak,
+	// try to steal more tech to catch up
+	if(	iam_in_last_place
+		and warlike	
+		and hes_in_first_place
+		and not yes_war)
+		{
+			same_like_him
+			go_to_cold_war
+			yes_special_plan
+		}
+
+
 	////////////////////////////////////////////////////////////
 	//////////   REGARD LOST BECAUSE HE'S TOO CLOSE   //////////
 	////////////////////////////////////////////////////////////
@@ -580,7 +679,7 @@ output loyalty_modifier [-20, 20] = 0
 		and warlike
 		and zero_at_war )
 		{
-			much_hate_strength
+			super_hate_strength
 		}
 
 	// LIKE HIM MORE IF HE'S CLOSE, ON THE SAME CONTINENT, AND I'M PEACEFUL
@@ -598,17 +697,20 @@ output loyalty_modifier [-20, 20] = 0
 	////////// REGARD LOST TO SPECIAL ACTIONS  //////////////////////
 	//////////////////////////////////////////////////////////////////////////////////////
 
-	// LIKE HIM LESS IF HE USES UNCONVENTIONAL ATTACKS ON ME
+	// LIKE HIM LESS IF HE USES UNCONVENTIONAL ATTACKS ON ME..N: changed
 	if((once_unconned_me or often_unconned_me) 
 		and (love_him or like_him))
 	{
 		hate_him_more
+		trust_much_less
 	}
 
+	// N: changed	
 	if((once_unconned_me or often_unconned_me) 
 		and (neutral_towards_him or dislike_him))
 	{
-		dislike_him_more
+		loath_him_more
+		benedict_arnold
 	}
 	
 	///////////////////////////////////////////////////////////////////////
@@ -623,6 +725,7 @@ output loyalty_modifier [-20, 20] = 0
 	if(pirated_a_little)
 		{
 			little_hate_pirate
+			trust_much_less
 		}
 
 	if(blue_beard)
@@ -640,13 +743,14 @@ output loyalty_modifier [-20, 20] = 0
 		tri tiny_hate_incursion(dip_regard_incursion_delta, -1.0, 5.0)
 		tri zero_hate_incursion(dip_regard_incursion_delta, 0.0, 5.0)		
 
-	// LIKE HIM LESS IF HE WALKS ON MY LANDS AND WE'RE NOT ALLIES
+	// LIKE HIM LESS IF HE WALKS ON MY LANDS AND WE'RE NOT ALLIES...N: changed
 		if(	few_incursions 
 			and warlike 
 			and yes_he_has_been_warned_to_LEAVE_OUR_LANDS
 			and not yes_alliance)
 		{
 			tiny_hate_incursion
+			trust_much_less
 		}
 
 		if(	few_incursions 
@@ -681,18 +785,19 @@ output loyalty_modifier [-20, 20] = 0
 		{	
 			zero_hate_incursion
 		}
-
+		
+		// N: changed
 		if(many_incursions 
 			and peaceful 
 			and human
 			and yes_he_has_been_warned_to_LEAVE_OUR_LANDS 
 			and not yes_alliance )
 		{
-			much_hate_incursion
+			tiny_hate_incursion
 		}
 
+		// N: changed, no longer just human
 		if(floods_incursions 
-			and human
 			and yes_he_has_been_warned_to_LEAVE_OUR_LANDS
 			and not yes_alliance )
 		{
@@ -710,6 +815,7 @@ output loyalty_modifier [-20, 20] = 0
 	///////////////////////////////////////////////////////////////////////////////////////////
 	//////////   REGARD LOST TO HIM ATTACKING ME   /////////
 	///////////////////////////////////////////////////////////////////////////////////////////
+	// N: last input added
 
 	output dip_regard_attack_delta[-100, 0] = 0
 		tri shift_three_hate_attack(dip_regard_attack_delta, -60.0, 20.0)
@@ -717,6 +823,7 @@ output loyalty_modifier [-20, 20] = 0
 		tri shift_one_hate_attack(dip_regard_attack_delta, -20.0, 20.0)
 		tri much_hate_attack(dip_regard_attack_delta, -10.0, 5.0)
 		tri little_hate_attack(dip_regard_attack_delta, -5.0, 5.0)
+		tri okay_hate_attack(dip_regard_attack_delta, -2.0, 2.0)
 
 		// IF I'M PEACEFUL AND WE'RE GOOD FRIENDS, GIVE HIM ONE BREAK WHEN HE ATTACKS ME.
 		if(once_attacked_me and not warlike and (like_him or love_him)) 
@@ -766,28 +873,64 @@ output loyalty_modifier [-20, 20] = 0
 			much_hate_attack
 		}
 
+		// N: If I'm breaking border policies like a
+		// dizzy manic squirrel, & peaceful...well, okay 
+		if(once_attacked_me
+			and peaceful
+			and not yes_war
+			and not hot_war_prep
+			and many_my_incurions)
+		{
+			okay_hate_attack
+		}
+
+		// N: If I'm breaking border policies like a
+		// dizzy manic squirrel, & warlike, hmm, well, okay 
+		if(once_attacked_me
+			and warlike
+			and not yes_war
+			and not hot_war_prep
+			and many_my_incurions)
+		{
+			okay_hate_attack
+		}
+
+		// N: If I'm breaking border policies like a dizzy
+		// manic squirrel, & we're allied or at peace, well, okay 
+		if(once_attacked_me
+			and (yes_alliance or yes_cease_fire)
+			and not hot_war_prep
+			and many_my_incurions)
+		{
+			okay_hate_attack
+		}
+
+
 	///////////////////////////////////////////////////////////////////////////////
 	//////////   REGARD LOST TO REJECTION     //////////
 	//////////////////////////////////////////////////////////////////////////////
 
-		// DISLIKE HIM IF HE WON'T AGREE TO OUR REQUESTS
+		// DISLIKE HIM IF HE WON'T AGREE TO OUR REQUESTS..N: changed
+		// Changed to neutral...N.
 		if(some_rejected_requests and not warlike)
 		{
-			dislike_him_more
+			same_like_him
 		}
 
-		// DISLIKE HIM A LOT IF HE WON'T AGREE 
+		// DISLIKE HIM A LOT IF HE WON'T AGREE..N: changed
 		// AND IF I'M WARLIKE
+		// Changed to dislike...N.
 		if(some_rejected_requests and warlike)
 		{
 			dislike_him_more
 		}
 
-		// DISLIKE HIM A LOT IF HE WON'T AGREE A LOT 
+		// DISLIKE HIM A LOT IF HE WON'T AGREE A LOT..N: changed
+		// Changed to hate...N. 
 		if(many_rejected_requests)
 		{
-			hate_him_more
-		}
+			hate_him_more	
+      		}
 
 	////////////////////////////////////////////////////
 	//////////   REGARD GAINED FROM ACCEPTANCE  ////////
@@ -803,21 +946,23 @@ output loyalty_modifier [-20, 20] = 0
 	//////////   REGARD GAINED FROM HIM FIGHTING MY FOES ///
 	////////////////////////////////////////////////////////
 
-	// LIKE HIM MORE IF HE ATTACKS OUR ENEMIES
+	// LIKE HIM MORE IF HE ATTACKS OUR ENEMIES..N: changed all
 	if( once_attacked_my_enemies 
 		and no_war
 		and not my_worst_enemy
 		and not love_him )
 		{
-			like_him_more
+			love_him_more
+			trust_more
 		}
 		
-	if(	twice_attacked_my_enemies 
+	if(	twice_attacked_my_enemies
 		and no_war
 		and not my_worst_enemy
 		and not love_him )
 		{
 			love_him_more
+			trust_more
 		}
 		
 	if(	thrice_attacked_my_enemies
@@ -826,13 +971,14 @@ output loyalty_modifier [-20, 20] = 0
 		and not love_him )
 		{
 			worship_him_more
+			trust_much_more
 		}	
 
 	////////////////////////////////////////////////////////
 	//////////   REGARD LOST FROM HIM FIGHTING MY FRIENDS ///
 	////////////////////////////////////////////////////////
 
-	// LIKE HIM LESS IF HE ATTACKS OUR FRIENDS
+	// LIKE HIM LESS IF HE ATTACKS OUR FRIENDS..N: changed
 	if(	twice_attacked_my_enemies 
 		and not my_best_friend)
 		{
@@ -855,19 +1001,6 @@ output loyalty_modifier [-20, 20] = 0
 	//		shift_to_hatred_more
 	//	}
 		
-////////////////////////////////////////////////////////////////////////////////////////
-//////////   SET STRENGTH OF STATE OF WAR      ///////////
-////////////////////////////////////////////////////////////////////////////////////////
-// 
-// when unit regard is less than 20, we target the enemy.
-
-output unit_regard_delta[-100, 100] = 0.0
-	tri go_to_hot_war(unit_regard_delta, 10, 80.0)
-	tri go_to_hot_war_prep(unit_regard_delta, 25, 1.0)
-	tri go_to_cold_war(unit_regard_delta, 35, 1.0)
-	tri go_to_cold_war_prep(unit_regard_delta, 50, 0.5)
-	tri go_to_peace_partial(unit_regard_delta, 60, 0.55)
-	tri go_to_peace_full(unit_regard_delta, 80, 2.0)
 
 	////////////////////////////////////////////////////////////////////////////////
 	////////// DO WE HAVE A CEASE FIRE /////////////////////
@@ -877,8 +1010,7 @@ output unit_regard_delta[-100, 100] = 0.0
 		left no_cease_fire(cease_fire_with_him, 0.0, .5)
 		right yes_cease_fire(cease_fire_with_him, 1.0, .5)
 	
-	output special_plan[0.0, 2.0] = 0.0
-		tri yes_special_plan(special_plan, 1.0, 0.5)
+
 
 	// if he's my best friend, then let's not fight
 	if(	my_best_friend 
@@ -939,7 +1071,13 @@ output unit_regard_delta[-100, 100] = 0.0
 	{
 		very go_to_hot_war
 	}
-
+	
+	// N: If we're at war with another AI, fight
+	if (yes_war
+	    and not human	 )	
+	{
+		very go_to_hot_war
+	}			
 	///////////////////////////////////////////////////////
 	////////// DO WE HAVE AN ALLIANCE /////////////////////
 	///////////////////////////////////////////////////////
@@ -1053,7 +1191,7 @@ output unit_regard_delta[-100, 100] = 0.0
 		and not backstabber
 		and not yes_tired )
 	{
-		go_to_hot_war
+		go_to_hot_war_prep
 	}
 
 	// GO TO WAR IF I'M NOT AT WAR WITH ANYONE
@@ -1104,7 +1242,8 @@ output unit_regard_delta[-100, 100] = 0.0
 		and not (maybe_trust_him or completely_trust_him or distrust_him) 
 		and not love_him )
 	{
-		kinda like_him_more	
+		kinda like_him_more
+		trust_more	
 	}
 
 	if( made_stop_trade and not violate_stop_trade 
@@ -1134,7 +1273,7 @@ output unit_regard_delta[-100, 100] = 0.0
 	// LIKE HIM MORE AND TRUST HIM MORE IF HE KEEPS THE LEAVE LANDS AGREEMENT
 	if(	yes_leave_our_lands and not violate_leave_our_lands)
 	{
-		kinda like_him_more
+		like_him_more
 	}
 
 	if(	yes_leave_our_lands and not violate_leave_our_lands
@@ -1186,7 +1325,7 @@ input have_end_pollution
 	if(violate_reduce_pollution)
 	{
 		benedict_arnold
-		loath_him_more
+		dislike_him_more
 	}	
 
 	if(yes_reduce_pollution and not violate_reduce_pollution )
@@ -1214,7 +1353,7 @@ input have_end_pollution
 		 and human )	
 	{	
 		benedict_arnold	
-		loath_him_more
+		dislike_him_more
 	}
 		
 	if ( yes_attack_enemy 
@@ -1230,27 +1369,32 @@ input have_end_pollution
 	}
 
 	////////////////////////////////////////////////////////////////
-	//////////   REGARD LOST BECAUSE HE'S ABOUT TO WOIN   //////////
+	//////////   REGARD LOST BECAUSE HE'S ABOUT TO WIN   //////////
 	////////////////////////////////////////////////////////////////
 
+	// N: changed
 	if(	yes_he_built_wormhole 
 		and human)
 		{
 			super_hate_strength
-			go_to_hot_war
+			very go_to_cold_war
+			benedict_arnold
+			yes_special_plan
 		}
 
-	// hate ai's that are winning, but don't go overboard
+	// hate ai's that are winning, but don't go overboard..N: changed
 	if(	yes_he_built_wormhole 
 		and not human )
 		{
 			much_hate_strength
+			benedict_arnold
 		}
 
 	////////////////////////////////////////////////////////////////////////////
 	//////////   STOP FIGHTING EVERYONE ELSE IF HUMAN HAS WORMHOLE TECH   //////
 	////////////////////////////////////////////////////////////////////////////
 
+	// N: changed
 	if(	not yes_he_built_wormhole 
 		and yes_someone_built_wormhole
 		and not human 
@@ -1258,24 +1402,27 @@ input have_end_pollution
 		{
 			like_him_more
 			go_to_cold_war
+			trust_more
 		}
 
 	////////////////////////////////////////////////////////
 	//////////   REGARD LOST BECAUSE HE'S HUMAN   //////////
 	////////////////////////////////////////////////////////
 
+	// N: changed
 	if(	human 
 		and warlike )
 		{
-			distain_him_more
+			dislike_him_more
+			trust_much_less
 		}
 	
-//	if(	human
-//		and ( afraid_of_him or terrified_of_him )
-//		not warlike )
-//		{
-//			distain_him_more
-//		}
+	// N: changed and added
+	if(	human
+		and not warlike )
+		{
+			same_like_him
+		}
 
 ////////////////////////////////////////////////////////////////////////////////////////////////////////
 ///// SET UP MY MEMORY OF MY RESPONSES TO HIS DEMANDS BASED ON HOW MUCH I LIKE HIM  ////////////////////
@@ -1332,4 +1479,82 @@ input have_end_pollution
 		his_long_decay_DEMAND_LEAVE_OUR_LANDS
 	}		
 
+/////////////////////////////////////////////////////////////////////////////////
+///////////////////////NORDICUS WANDERING AI SYNDROME FIX////////////////////////
+////////////////////////////////////////////////////////////////////////////////
+	input i_will_leave_his_lands
+		tri yes_i_will_leave_his_lands(i_will_leave_his_lands, 1.8, 0.5)
+
+		// N: WAIS added (I'll leave your lands if you're scary
+		// and I'm not going to fight you)
+		if(some_my_incurions 
+			and peaceful 
+			and (afraid_of_him or terrified_of_him)
+			and not hot_war_prep 
+			and not yes_alliance )
+		{
+			yes_i_will_leave_his_lands
+		}
+		
+		// N: WAIS added (I'll leave your lands if you're peaceful
+		// and we're neutral and I'm not fighting anyone)
+		if(some_my_incurions 
+			and peaceful
+			and not yes_war
+			and zero_at_war
+			and (not dislike_him or not hate_him)
+			and not yes_alliance )
+		{
+			yes_i_will_leave_his_lands
+		}
+
+		// N: WAIS added (I'll leave your lands if we're
+		// enjoying a Cease Fire and I like you okay)
+		if(some_my_incurions 
+			and war
+			and not my_worst_enemy
+			and yes_cease_fire
+			and not hot_war_prep
+			and not yes_alliance )
+		{
+			yes_i_will_leave_his_lands
+		}
+
+		// N: WAIS added (I'll leave your lands if we're enjoying a
+		// an Alliance or Peace Treaty and I'm not fighting anyone)
+		if(some_my_incurions 
+			and not yes_war
+			and zero_at_war
+			and (yes_cease_fire or yes_alliance)
+			and (like_him or love_him)
+			and not hot_war_prep
+			and not yes_alliance )
+		{
+			yes_i_will_leave_his_lands
+		}
+
+		// N: WAIS added (I'll leave your lands if we're at Peace
+		// and I'm trespassing like a blindfolded drunk)
+		if(many_my_incurions 
+			and not yes_war
+			and zero_at_war
+			and yes_cease_fire
+			and not hot_war_prep
+			and not yes_alliance )
+		{
+			yes_i_will_leave_his_lands
+		}
+
+		// N: WAIS added (I'll leave your lands if you're peaceful
+		// and we're neutral and neither of us fights anyone)
+		if(some_my_incurions 
+			and peaceful
+			and not yes_war
+			and zero_at_war
+			and he_fights_zero
+			and (not dislike_him or not hate_him)
+			and not yes_alliance )
+		{
+			yes_i_will_leave_his_lands
+		}
 
```

## aidata/diplomacy_pre_incoming.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\diplomacy_pre_incoming.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\diplomacy_pre_incoming.fli"
index 6705309..6e41767 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\diplomacy_pre_incoming.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\diplomacy_pre_incoming.fli"
@@ -318,7 +318,7 @@ output diplomatic_regard_delta[-50, 50] = 0.0
 	
 input military_incursions
 	left no_incursions(military_incursions, 0, 0.2)
-	tri few_incursions(military_incursions, 2, 1.5)
+	tri few_incursions(military_incursions, 2, 1.8)
 	right many_incursions(military_incursions, 3, 1)
 
 /////////////////////////////////////
@@ -460,6 +460,7 @@ input contact_gained
 		tri yes_he_gets_map(he_gets_map, 1, .5)
 
 	// don't use input last_got_map; it means nothing
+	// N: preceding: normalized
 
 	if(	yes_he_gets_map and not yes_i_gain_map)
 		{
@@ -470,7 +471,7 @@ input contact_gained
 		and terrified_of_him 
 		and not my_worst_enemy) 
 		{
-			average_reason_to_accept
+			good_reason_to_accept
 		}
 	
 	if(	yes_he_gets_map and not yes_i_gain_map 
@@ -480,6 +481,24 @@ input contact_gained
 			best_reason_to_accept
 		}
 	
+	// N: added...If we're allied, have a map
+	if(	yes_he_gets_map and not yes_i_gain_map 
+		and yes_alliance 
+		and not hate_him ) 
+		{
+			best_reason_to_accept
+		}
+
+	// N: added...If we have a treaty, have a map
+	if(	yes_he_gets_map and not yes_i_gain_map 
+		and yes_cease_fire 
+		and not hate_him
+		and not yes_war) 
+		{
+			best_reason_to_accept
+		}
+
+
 	if(	yes_he_gets_map and not yes_i_gain_map	
 		and yes_enough_me_giving_in_to_DEMAND_MAP 
 		and not love_him )
@@ -488,18 +507,28 @@ input contact_gained
 			no_way_give_adv
 			dislike_him_more
 		}
+	// N: added..If I'm tough & don't like you, watch it!
+	if(	yes_he_gets_map and not yes_i_gain_map	
+		and yes_enough_me_giving_in_to_DEMAND_MAP 
+		and not (like_him or love_him ))
+		{
+			zero_reason_to_accept
+			no_way_give_adv
+			hate_him_more
+		}
+
 
-		// Now set regard based on our responses.
+		// N: all changed...Now set regard based on our responses.
 		if(	yes_he_gets_map and not yes_i_gain_map 
 			and best_reason_to_accept)
 			{	
-				like_him_more
+				same_like_him
 			}
 
 		if(	yes_he_gets_map and not yes_i_gain_map  
 			and good_reason_to_accept)
 			{	
-				like_him_more
+				same_like_him
 			}
 
 		if(	yes_he_gets_map and not yes_i_gain_map  
@@ -702,7 +731,7 @@ input contact_gained
 		and my_best_friend 
 		and zero_at_war)
 	{
-		good_reason_to_accept
+		best_reason_to_accept
 	}
 
 	if(	yes_i_will_attack_third_party 
@@ -755,7 +784,7 @@ input contact_gained
 		if(	yes_i_will_attack_third_party   
 			and average_reason_to_accept)
 			{	
-				same_like_him
+				like_him_more
 			}
 
 		if(	yes_i_will_attack_third_party   
@@ -769,8 +798,9 @@ input contact_gained
 	/////////////////////////////////////////////////////
 	///		return k_AVERAGE_VALUE;
 
+	// N: Wandering AI Syndrome attempted fix...changed to one-point-eight
 	input i_will_leave_his_lands
-		tri yes_i_will_leave_his_lands(i_will_leave_his_lands, 1, 0.5)
+		tri yes_i_will_leave_his_lands(i_will_leave_his_lands, 1.8, 0.5)
 
 		if(yes_i_will_leave_his_lands)
 		{
@@ -787,19 +817,52 @@ input contact_gained
 			and not my_worst_enemy 
 			and not yes_war)
 		{
-			good_reason_to_accept
+			best_reason_to_accept
 		}
 
 		if(	yes_i_will_leave_his_lands 
 			and yes_he_is_scary
 			and not yes_war)
 		{
-			good_reason_to_accept
+			best_reason_to_accept
 		} 
 		
-			// set regard based on responses.
+		// N: added
+		if(	yes_i_will_leave_his_lands 
+			and (like_him or love_him or neutral_towards_him)
+			and not yes_war)
+		{
+			best_reason_to_accept
+		} 
+
+		// N: added
+		if(	yes_i_will_leave_his_lands 
+			and not (dont_trust_him or distrust_him)
+			and not yes_war)
+		{
+			best_reason_to_accept
+		} 
+
+		// N: added
+		if(	yes_i_will_leave_his_lands 
+			and iam_in_last_place
+			and not yes_war)
+		{
+			best_reason_to_accept
+		} 
+
+		// N: added
+		if(	yes_i_will_leave_his_lands 
+			and hes_in_first_place
+			and not yes_war)
+		{
+			best_reason_to_accept
+		} 
+
+
+			// set regard based on responses..N: the above four and this one changed
 			if(	yes_i_will_leave_his_lands   
-			and good_reason_to_accept)
+			and best_reason_to_accept)
 			{	
 				same_like_him
 			}
@@ -883,6 +946,22 @@ input contact_gained
 //		dislike_him_more
 //	}
 
+	// N: added	
+	if( yes_reduces_pollution
+		and like_him 
+		and not distrust_him )
+		{
+			good_reason_to_accept
+		}
+
+	// N: added	
+	if( yes_reduces_pollution
+		and peaceful
+		and not yes_war  )
+		{
+			good_reason_to_accept
+		}
+
 
 	// stop piracy
 	// pirate
@@ -944,12 +1023,13 @@ input contact_gained
 		love_him_more
 	}
 
+	// N: changed
 	if(	yes_i_gain_advance 
 		and yes_war 
 		and yes_he_is_scary)
 	{
 		best_reason_to_accept
-		love_him_more
+		like_him_more
 	}
 
 	if(	yes_i_gain_advance 
@@ -1106,18 +1186,19 @@ input contact_gained
 			good_reason_to_accept
 		}
 
+	// N: regard changed to neutral	
 	if( yes_i_gain_map and not yes_he_gets_map
 		and best_reason_to_accept
 		and not yes_just_saw_your_map)
 		{
-			love_him_more
+			same_like_him
 		}
 
 	if( yes_i_gain_map and not yes_he_gets_map
 		and good_reason_to_accept
 		and not yes_just_saw_your_map)
 		{
-			like_him_more
+			same_like_him
 		}
 
 
@@ -1140,10 +1221,10 @@ input contact_gained
 	}
 
 	if( yes_gains_cease_fire
-		and love_him
+		and (like_him or love_him)
 		and not distrust_him)
 		{
-			best_reason_to_accept
+			good_reason_to_accept
 		}
 
 	// If we have been at war for a very long time, 
@@ -1161,7 +1242,7 @@ input contact_gained
 		and not yes_war 
 		and ( afraid_of_him or terrified_of_him)) 
 		{
-			good_reason_to_accept
+			best_reason_to_accept
 		}
 
 	// If we are at war for a longer time, then consider
@@ -1196,7 +1277,7 @@ input contact_gained
 		and not yes_we_just_made_a_peace_treaty
 		and not love_him)
 	{
-		love_him_more
+		like_him_more
 	}
 
 	if(	yes_gains_cease_fire 
@@ -1210,11 +1291,41 @@ input contact_gained
 	if(	yes_gains_cease_fire 
 		and average_reason_to_accept
 		and not yes_we_just_made_a_peace_treaty
-		and not love_him)
+		and not love_him )
 	{	
 		same_like_him
 	}
 
+	// N: If we are not at war and we like or love you
+	// then accept a peace treaty
+	if(	yes_gains_cease_fire
+		and not yes_war
+		and human
+		and (like_him or love_him )
+		and not distrust_him)
+		{
+			best_reason_to_accept
+		}
+
+	// N: If we are not at war and you're scary
+	// then accept a peace treaty
+	if(	yes_gains_cease_fire
+		and not yes_war
+		and (afraid_of_him or terrified_of_him ))
+		{
+			best_reason_to_accept
+		}
+	// N: If we are not at war and we are peaceful
+	// then accept a peace treaty
+	if(	yes_gains_cease_fire
+		and zero_at_war
+		and human
+		and peaceful
+		and not distrust_him )
+		{
+			best_reason_to_accept
+		}
+
 	/////////////////////////////
 	/// RESPOND TO ALLIANCE ///
 	/////////////////////////////
@@ -1258,9 +1369,10 @@ input contact_gained
 		and peaceful
 		and completely_trust_him)
 	{
-		average_reason_to_accept
+		best_reason_to_accept
 	}
 
+	// N: changed
 	if(	yes_gains_alliance 
 		and not hate_him
 		and not dislike_him
@@ -1268,10 +1380,12 @@ input contact_gained
 		and not yes_war
 		and yes_too_many_enemies) 
 	{
-		average_reason_to_accept
+		good_reason_to_accept
 	}
 
+	// N: changed
 	if(	yes_gains_alliance 
+		and human
 		and not love_him
 		and equal_to_him 
 		and warlike) 
@@ -1290,19 +1404,47 @@ input contact_gained
 	if(	yes_gains_alliance 
 		and hes_in_first_place
 		and iam_in_last_place
-		and not my_worst_enemy
-		) 
+		and not my_worst_enemy) 
+	{
+		best_reason_to_accept
+	}	
+	
+	// N: added...
+	if(	yes_gains_alliance 
+		and ai
+		and warlike
+		and not yes_war
+		and not hate_him
+		and not my_worst_enemy) 
 	{
 		best_reason_to_accept
 	}	
 	
-	// set regard based on responses.
+	// N: added...
+	if(	yes_gains_alliance 
+		and ai
+		and yes_neutral
+		and not yes_war
+		and not hate_him
+		and not my_worst_enemy) 
+	{
+		best_reason_to_accept
+	}	
+
+	// set regard based on responses...N: added
 		if(	yes_gains_alliance 
-			and good_reason_to_accept)
+			and best_reason_to_accept)
 		{
 			love_him_more
 		}
 
+
+		if(	yes_gains_alliance 
+			and good_reason_to_accept)
+		{
+			like_him_more
+		}
+
 		if(	yes_gains_alliance 
 			and average_reason_to_accept)
 		{	
@@ -1339,6 +1481,32 @@ input contact_gained
 			best_reason_to_accept
 		}
 
+	// N: added
+	if( yes_end_pollution_pact
+		and ai
+		and like_him 
+		and not distrust_him )
+		{
+			good_reason_to_accept
+		}
+
+	// N: added
+	if( yes_end_pollution_pact
+		and like_him 
+		and not distrust_him )
+		{
+			good_reason_to_accept
+		}
+
+	// N: added
+	if( yes_end_pollution_pact
+		and peaceful
+		and not yes_war )
+		{
+			best_reason_to_accept
+		}
+
+
 ///////////////////////////////
 /// RESPOND TO  EXCHANGES  ////
 ///////////////////////////////
@@ -1371,25 +1539,29 @@ input contact_gained
 	{
 		found
 	}
-	
+
+	// N: changed	
 	if(	yes_he_gains_advance and yes_i_gain_advance 
 		and dislike_him)
 	{
-		bad_reason_to_accept
+		average_reason_to_accept
 	}
 
+	// N: changed
 	if(	yes_he_gains_advance and yes_i_gain_advance 
 		and neutral_towards_him)
 	{
-		average_reason_to_accept
+		good_reason_to_accept
 	}
 
+	// N: changed
 	if(	yes_he_gains_advance and yes_i_gain_advance 
 		and (like_him or love_him))
 	{
-		average_reason_to_accept
+		good_reason_to_accept
 	}
 
+	// N: changed
 	if(	yes_he_gains_advance and yes_i_gain_advance 
 		and my_best_friend
 		and love_him)
@@ -1397,18 +1569,28 @@ input contact_gained
 		good_reason_to_accept
 	}
 
+	// N: changed
 	if(	yes_he_gains_advance and yes_i_gain_advance
 		and good_reason_to_accept)
 	{	
-		love_him_more
+		like_him_more
 	}
 
+	// N: changed...
 	if(	yes_he_gains_advance and yes_i_gain_advance 
 		and average_reason_to_accept)
 	{	
 		same_like_him
 	}
 
+	// N: added...
+	if(	yes_he_gains_advance and yes_i_gain_advance 
+		and yes_war)
+	{	
+		same_like_him
+	}
+
+
 	///////////////////////////////////////////////
 	////////// RESPOND TO EXCHANGE MAP  ///////////
 	///////////////////////////////////////////////
@@ -1432,28 +1614,39 @@ input contact_gained
 			best_reason_to_accept
 		}
 
+		// N: changed
 		if(	yes_he_gets_map and yes_i_gain_map 
 			and (like_him or love_him) 
 			and afraid_of_him 
 			and not distrust_him
 			and not yes_just_saw_your_map)
 		{
-			good_reason_to_accept
+			best_reason_to_accept
 		}
 
+		// N: changed	
 		if(	yes_he_gets_map and yes_i_gain_map 
 			and (not hate_him or not dislike_him) 
-			and not distrust_him
+			and peaceful
+			and not yes_just_saw_your_map)
+		{
+			best_reason_to_accept
+		}
+
+		// N: added	
+		if(	yes_he_gets_map and yes_i_gain_map 
+			and not yes_war 
+			and (equal_to_him or stronger_than_him)
 			and not yes_just_saw_your_map)
 		{
 			good_reason_to_accept
 		}
 
-			// Now, set regard based on our responses.
+			// Now, set regard based on our responses...both: N..
 			if(	yes_he_gets_map and yes_i_gain_map 
 				and best_reason_to_accept)
 			{	
-				like_him_more
+				same_like_him
 			}
 	
 			if(	yes_he_gets_map and yes_i_gain_map  
@@ -1471,3 +1664,18 @@ input contact_gained
 	{
 		worst_reason_to_accept
 	}
+
+	// N: added
+	if(not found
+		and like_him)
+	{
+		average_reason_to_accept
+	}
+	// N: added
+	if(not found
+		and love_him)
+	{
+		good_reason_to_accept
+	}
+
+
```

## aidata/diplomacy_pre_outgoing.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\diplomacy_pre_outgoing.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\diplomacy_pre_outgoing.fli"
index 0206d13..443ccd8 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\diplomacy_pre_outgoing.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\diplomacy_pre_outgoing.fli"
@@ -389,7 +389,134 @@ input contact_gained // 0 - 100; 100 = yes
 		best_message_to_send
 		found
 	}
+
+
+	///////////////////////////////////////////////////////
+	///// DO WE HAVE AN ALLIANCE ..N: moved////////////////
+	///////////////////////////////////////////////////////
+
+	input alliance_with_him
+		left no_alliance(alliance_with_him, 0.0, .5)
+		right yes_alliance(alliance_with_him, 1.0, .5)
 	
+
+	/////////////////////////////////////////////////////
+	/// SHOULD I OFFER CEASE FIRE OR PEACE TREATY////////
+	///N: moved up here//////////////////////////////////
+	////////////////////////////////////////////////////
+	/// 	return k_GOOD_VALUE;
+
+	// 12/31 I have doubts about the afraid of him and hatfields n mccoys stuff
+
+	input gains_cease_fire
+		right yes_gains_cease_fire(gains_cease_fire, 1, .5)
+
+	// N: changed priority back again
+	if(yes_gains_cease_fire)
+	{
+		med_priority
+	}
+
+	if(	yes_gains_cease_fire 
+		and not my_worst_enemy
+		and yes_war
+		and yes_too_many_enemies
+		and not (distrust_him or dont_trust_him)
+		and not yes_human)
+	{
+		good_message_to_send
+		found
+	}
+
+	if(	yes_gains_cease_fire 
+		and not my_worst_enemy 
+		and equal_to_him 
+		and yes_bored_of_war 
+		and yes_war 
+		and (not distrust_him or not dont_trust_him))
+		{
+			bad_message_to_send
+			found
+		}
+
+	// N...changed...added	
+	if(	yes_gains_cease_fire 
+		and not my_worst_enemy 
+		and peaceful 
+		and not yes_war 
+		and (not distrust_him or not dont_trust_him)
+		and not yes_alliance) 
+		{
+			okay_message_to_send
+			found
+		}
+
+	// N...added	
+	if(	yes_gains_cease_fire 
+		and not yes_war 
+		and yes_alliance) 
+		{
+			worst_message_to_send
+			found
+		}
+
+
+	if(	yes_gains_cease_fire 
+		and not my_worst_enemy 
+		and yes_war 
+		and yes_fear 
+		and not one_at_war 
+		and (not distrust_him or not dont_trust_him)) 
+		{
+			good_message_to_send
+			found
+		}
+
+	if(	yes_gains_cease_fire 
+		and yes_war 
+		and yes_terror 
+		and (not distrust_him or not dont_trust_him))
+		{
+			good_message_to_send
+			found
+		}
+
+	if(	yes_gains_cease_fire 
+		and yes_war 
+		and yes_sick_of_war
+		and not dont_trust_him)
+		{
+			good_message_to_send
+			found
+		}
+
+	if(	yes_gains_cease_fire 
+		and yes_war 
+		and warlike 
+		and not yes_sick_of_war)
+		{
+			worst_message_to_send
+			found
+		}
+
+	if(	yes_gains_cease_fire 
+		and yes_chase_the_rabbit 
+		and not yes_human)
+		{
+			best_message_to_send
+		}
+
+
+
+	////////////////////////////////////////////////////////
+	////////// DO WE HAVE A CEASE FIRE ..N: added///////////
+	////////////////////////////////////////////////////////
+
+	input cease_fire_with_him
+		left no_cease_fire(cease_fire_with_him, 0.0, .5)
+		right yes_cease_fire(cease_fire_with_him, 1.0, .5)
+
+
 //////////////////////////
 /// SHOULD I DEMAND   ////
 //////////////////////////
@@ -433,15 +560,29 @@ input contact_gained // 0 - 100; 100 = yes
 		med_priority
 	}
 	
+	// N...changed all
 	if(	advance_to_me and not advance_to_him 
 		and (like_him or love_him))
 		{
-			wont_demand_adv
+			thinkin_bout_demandin_adv
 			found
 			rand_min_25
 			rand_max_100
 		}
-		
+	
+	// N: added
+	if(	advance_to_me and not advance_to_him 
+		and warlike
+		and equal_to_him
+		and not yes_ive_been_losing)
+		{
+			thinkin_bout_demandin_adv
+			found
+			rand_min_25
+			rand_max_100
+		}
+
+	
 	if(	advance_to_me and not advance_to_him 
 		and ( dislike_him or hate_him )  
 		and little_stronger_than_him 
@@ -468,6 +609,21 @@ input contact_gained // 0 - 100; 100 = yes
 			rand_max_100
 
 		}
+	// N: added...If I'm tough, we're allied or in a treaty,
+	// gimme some tech!	
+	if(	advance_to_me and not advance_to_him 
+		and not (yes_alliance or yes_cease_fire)
+		and stronger_than_him 
+		and not (love_him or hate_him)
+		and not yes_war)	
+		{
+			gimmee_adv
+			good_message_to_send
+			found
+			rand_min_25
+			rand_max_100
+
+		}
 
 
 	// demand gold
@@ -570,6 +726,48 @@ input contact_gained // 0 - 100; 100 = yes
 				rand_min_25
 				rand_max_100
 			}
+	
+		// N: added
+		if(	(i_gain_gold or i_gain_much_gold or i_gain_incredible_gold)
+			and stronger_than_him 
+			and not yes_war
+			and not yes_terror
+			and (dislike_him or hate_him)
+			and not yes_i_just_asked_for_gold )
+			{
+				best_message_to_send
+				found
+				rand_min_25
+				rand_max_100
+			}
+	
+		// N: added
+		if(	(i_gain_gold or i_gain_much_gold or i_gain_incredible_gold)
+			and stronger_than_him 
+			and yes_alliance
+			and not yes_terror
+			and not yes_i_just_asked_for_gold )
+			{
+				best_message_to_send
+				found
+				rand_min_25
+				rand_max_100
+			}
+
+		// N: added
+		if(	(i_gain_gold or i_gain_much_gold or i_gain_incredible_gold)
+			and stronger_than_him 
+			and yes_cease_fire
+			and not yes_terror
+			and not yes_i_just_asked_for_gold )
+			{
+				best_message_to_send
+				found
+				rand_min_25
+				rand_max_100
+			}
+
+
 
 	// stop trade
 	// stop trading
@@ -634,14 +832,14 @@ input contact_gained // 0 - 100; 100 = yes
 		found
 	}
 	
-	// Threaten him to force him not to trade with our enemies.	
+	// Threaten him to force him not to trade with our enemies...N: changed	
 	if(	consider_stop_trade 
 		and hes_trading_with_3rd 
 		and low_third_party_regard 
 		and (hate_him or dislike_him) 
 		and stronger_than_him) 
 	{
-		good_message_to_send
+		best_message_to_send
 		rand_min_25
 		rand_max_100
 		found
@@ -669,7 +867,27 @@ input contact_gained // 0 - 100; 100 = yes
 	//	{
 	//		return 750;
 	//	}
-	//	return 0;	
+	//	return 0;// N: war inputs added	
+
+	input num_he_is_at_war
+		tri he_fights_zero(num_he_is_at_war, 0.0, 0.5)
+		tri he_fights_one(num_he_is_at_war, 1.0, 0.5)
+		tri he_fights_two(num_he_is_at_war, 2.0, 0.5)
+		tri he_fights_three(num_he_is_at_war, 3.0, 0.5)
+		tri he_fights_four(num_he_is_at_war, 4.0, 0.5)
+		tri he_fights_five(num_he_is_at_war, 5.0, 0.5)
+		tri he_fights_six(num_he_is_at_war, 6.0, 0.5)
+		tri he_fights_seven(num_he_is_at_war, 7.0, 0.5)
+		tri he_fights_eight(num_he_is_at_war, 8.0, 0.5)
+		tri he_fights_nine(num_he_is_at_war, 9.0, 0.5)
+		tri he_fights_ten(num_he_is_at_war, 10.0, 0.5)
+		tri he_fights_eleven(num_he_is_at_war, 11.0, 0.5)
+		tri he_fights_twelve(num_he_is_at_war, 12.0, 0.5)
+		tri he_fights_thirteen(num_he_is_at_war, 13.0, 0.5)
+		tri he_fights_fourteen(num_he_is_at_war, 14.0, 0.5)
+		tri he_fights_fifteen(num_he_is_at_war, 15.0, 0.5)
+		tri he_fights_sixteen(num_he_is_at_war, 16.0, 0.5)
+
 
 	input he_attacks_enemy
 		right consider_attacks_enemy(he_attacks_enemy, 1, 0.5)
@@ -725,6 +943,123 @@ input contact_gained // 0 - 100; 100 = yes
 		rand_max_100
 	}
 
+	// reduce to love only...N: added...if human		
+	if(consider_attacks_enemy 
+		and love_him
+		and human
+		and not yes_war 
+		and he_is_stronger_than_3rd 
+		and i_am_weaker_than_3rd 
+		and my_best_friend
+		and not yes_i_ve_asked_enough_about_attacking_enemy)
+	{
+		good_message_to_send
+		found
+		rand_min_25
+		rand_max_100
+	}
+
+
+	// N: added...If we're Allies, & ai, attack my enemy		
+	if(consider_attacks_enemy 
+		and (like_him or love_him)
+		and ai
+		and not yes_war 
+		and he_is_stronger_than_3rd 
+		and i_am_weaker_than_3rd 
+		and yes_alliance
+		and not yes_i_ve_asked_enough_about_attacking_enemy)
+	{
+		best_message_to_send
+		found
+		rand_min_25
+		rand_max_100
+	}
+
+	// N: added...If we're Allies, & you're human,
+	// attack my enemy		
+	if(consider_attacks_enemy 
+		and (like_him or love_him)
+		and human
+		and not yes_war 
+		and he_is_stronger_than_3rd 
+		and i_am_weaker_than_3rd 
+		and yes_alliance
+		and not yes_i_ve_asked_enough_about_attacking_enemy)
+	{
+		good_message_to_send
+		found
+		rand_min_25
+		rand_max_100
+	}
+
+
+	// N: added...If we're Allies and you're already		
+	// attacking my enemy, I'll shut up
+	if(consider_attacks_enemy 
+		and (like_him or love_him)
+		and not yes_war 
+		and (he_fights_one or he_fights_two)
+		and yes_ive_been_winning 
+		and yes_alliance
+		and not yes_i_ve_asked_enough_about_attacking_enemy)
+	{
+		bad_message_to_send
+		found
+		rand_min_25
+		rand_max_100
+	}
+	// N: added...If we're Allies and you're human and		
+	// already attacking my enemy, I'll shut up
+	if(consider_attacks_enemy 
+		and (like_him or love_him)
+		and human
+		and not yes_war 
+		and (he_fights_one or he_fights_two)
+		and yes_ive_been_winning 
+		and yes_alliance
+		and not yes_i_ve_asked_enough_about_attacking_enemy)
+	{
+		bad_message_to_send
+		found
+		rand_min_25
+		rand_max_100
+	}
+
+
+	// N: added...If we're Allies & you're attacking		
+	// my enemy and I'm losing, attack my enemy more!
+	if(consider_attacks_enemy 
+		and not yes_war 
+		and not yes_ive_been_winning
+		and yes_humbled_this_turn 
+		and i_am_weaker_than_3rd 
+		and yes_alliance
+		and not yes_i_ve_asked_enough_about_attacking_enemy)
+	{
+		good_message_to_send
+		found
+		rand_min_25
+		rand_max_100
+	}
+
+	// N: added...If we're Allies & ai & you're attacking		
+	// my enemy and I'm losing, attack my enemy more!
+	if(consider_attacks_enemy 
+		and not yes_war 
+		and ai
+		and not yes_ive_been_winning
+		and yes_humbled_this_turn 
+		and i_am_weaker_than_3rd 
+		and yes_alliance
+		and not yes_i_ve_asked_enough_about_attacking_enemy)
+	{
+		best_message_to_send
+		found
+		rand_min_25
+		rand_max_100
+	}
+
 	// leave lands
 	// demand leave
 	/////////////////////////////////////////////////
@@ -904,8 +1239,62 @@ input contact_gained // 0 - 100; 100 = yes
 		rand_min_25
 		rand_max_100
 		found
-	}	
-	
+	}	
+	
+	// N: added...Hey, I'm a peaceful AI who's chokin on
+	// smoke over here, so cut it out!	
+	if(	high_global_pollution 
+		and stronger_than_him 
+		and peaceful 
+		and average_his_pollution)
+	{
+		best_message_to_send
+		rand_min_25
+		rand_max_100
+		found
+	}
+
+	// N: added...Hey, I'm an AI who's chokin on
+	// smoke over here, so, you, AI, cut it out!	
+	if(	high_global_pollution 
+		and ai 
+		and not yes_war
+		and peaceful 
+		and average_his_pollution)
+	{
+		best_message_to_send
+		rand_min_25
+		rand_max_100
+		found
+	}
+
+	// N: added...Hey, I'm a warlike AI who's chokin on
+	// smoke over here, so cut it out or else!	
+	if(	high_global_pollution 
+		and warlike 
+		and not yes_war 
+		and average_his_pollution)
+	{
+		good_message_to_send
+		rand_min_25
+		rand_max_100
+		found
+	}
+
+	// N: added...Hey, I'm a powerful AI whose farms
+	// are turnin to swamp, so cut it out or else!	
+	if(	high_global_pollution 
+		and iam_in_first_place
+		and not yes_war
+		and average_his_pollution)
+	{
+		best_message_to_send
+		rand_min_25
+		rand_max_100
+		found
+	}
+
+
 	// demand map
 	/////////////////////////////////////////////////
 	/// SHOULD I DEMAND THAT YOU GIVE ME A MAP   ////
@@ -951,6 +1340,18 @@ input contact_gained // 0 - 100; 100 = yes
 		rand_max_100
 		found
 	}
+	//N: added...If we're allied, gimme a map!
+	if(	yes_he_gets_map and not yes_i_gain_map 
+		and yes_alliance
+		and not yes_war 
+		and got_map_centuries_ago
+		and not yes_ive_got_your_map )
+	{
+		best_message_to_send
+		rand_min_25
+		rand_max_100
+		found
+	}
 
 
 	////////////////////////////////////////////////////
@@ -1092,6 +1493,38 @@ input contact_gained // 0 - 100; 100 = yes
 		found
 	}
 
+	// N: added...If I'm losing a war with you, &
+	// I'm peaceful, I'll offer tech to encourage peace
+	if(advance_to_him and not advance_to_me
+		and yes_war 
+		and yes_ive_been_losing
+		and yes_humbled_this_turn
+		and (afraid_of_him or terrified_of_him)
+		and peaceful) 
+	{
+		best_message_to_send
+		rand_min_25
+		rand_max_100
+		found
+	}
+
+	// N: added...If I'm losing a war with you, &
+	// I'm warlike, I'll offer tech to encourage peace
+	if(advance_to_him and not advance_to_me
+		and yes_war 
+		and yes_ive_been_losing
+		and yes_humbled_this_turn
+		and (afraid_of_him or terrified_of_him)
+		and warlike) 
+	{
+		good_message_to_send
+		rand_min_25
+		rand_max_100
+		found
+	}
+
+
+
 	/////////////////////////////
 	/// SHOULD I GIVE GOLD   ////
 	/////////////////////////////
@@ -1192,6 +1625,39 @@ input contact_gained // 0 - 100; 100 = yes
 			like_him_more
 		}
 
+		// N: added...If we're at war & I'm losing,
+		// and I'm peaceful, I'll offer gold to encourage peace
+		if(	gives_him_gold 
+			and yes_war 
+			and peaceful
+			and yes_terror
+			and yes_ive_been_losing
+			and yes_humbled_this_turn 
+			and not yes_he_said_yes_recently_to_OFFER_GOLD)
+		{
+			best_message_to_send
+			rand_min_25
+			rand_max_100
+			found
+		}
+
+		// N: added...If we're at war & I'm losing,
+		// and I'm warlike, I'll offer gold to encourage peace
+		if(	gives_him_gold 
+			and yes_war 
+			and warlike
+			and yes_terror
+			and yes_ive_been_losing
+			and yes_humbled_this_turn
+			and not yes_he_said_yes_recently_to_OFFER_GOLD )
+		{
+			good_message_to_send
+			rand_min_25
+			rand_max_100
+			found
+		}
+
+
 	// offer map
 	// give map
 	///////////////////////////
@@ -1255,6 +1721,18 @@ input contact_gained // 0 - 100; 100 = yes
 			rand_max_100
 			found
 		}
+		//N: added...If we're allied, have a map
+		if(	yes_he_gets_map and not yes_i_gain_map 
+			and yes_alliance
+			and not yes_youve_got_my_map
+			and not yes_war ) 
+		{
+			good_message_to_send
+			rand_min_25
+			rand_max_100
+			found
+		}
+
 
 ////////////////////////////
 /// SHOULD I EXCHANGE   ////
@@ -1292,6 +1770,7 @@ input contact_gained // 0 - 100; 100 = yes
 	{
 		medlow_priority
 	}
+	// N: changed
 
 		if(advance_to_me and advance_to_him 
 			and ai 
@@ -1300,7 +1779,7 @@ input contact_gained // 0 - 100; 100 = yes
 			and not hes_in_first_place 
 			and not iam_in_first_place)
 		{
-			good_message_to_send
+			best_message_to_send
 			found
 		}
 
@@ -1315,7 +1794,7 @@ input contact_gained // 0 - 100; 100 = yes
 			found
 		}
 
-		// make you feel like you're someones best friend
+		// you feel like you're someones best friend
 		if(	advance_to_me 
 			and advance_to_him 
 			and my_best_friend
@@ -1328,19 +1807,33 @@ input contact_gained // 0 - 100; 100 = yes
 			found
 		}
 
-		// make you feel like someone is peaceful
+		// N...Changed...you feel like someone is peaceful
 		if(	advance_to_me 
 			and advance_to_him 
 			and peaceful 
 			and not my_worst_enemy
 			and not yes_war )
 		{ 
+			best_message_to_send
+			rand_min_25
+			rand_max_100
+			found
+		}
+
+		// N: added...feel like warlike is peaceful
+		if(	advance_to_me 
+			and advance_to_him 
+			and warlike
+			and (love_him or like_him) 
+			and not yes_war)
+		{
 			good_message_to_send
 			rand_min_25
 			rand_max_100
 			found
 		}
 
+
 	/////////////////////////////////
 	/// SHOULD I  EXCHANGE MAPS   ///
 	/////////////////////////////////
@@ -1354,12 +1847,12 @@ input contact_gained // 0 - 100; 100 = yes
 	// alone. 
 	
 
-	// inputs under demand
+	// inputs under demand...N: priority changed
 	if(	yes_i_gain_map 
 		and yes_he_gets_map
 		and not yes_he_has_been_asked_to_EXCHANGE_MAP)
 	{
-		low_priority
+		med_priority
 	}
 
 	if(	yes_i_gain_map 
@@ -1382,6 +1875,7 @@ input contact_gained // 0 - 100; 100 = yes
 		found
 	}
 
+	// N: changed
 	if(	yes_i_gain_map and yes_he_gets_map 
 		and love_him 
 		and my_best_friend 
@@ -1389,110 +1883,70 @@ input contact_gained // 0 - 100; 100 = yes
 		and not yes_he_has_been_asked_to_EXCHANGE_MAP
 		and not yes_youve_got_my_map)
 	{
-		good_message_to_send
+		best_message_to_send
 		rand_min_25
 		rand_max_100
 		found
 	}
-
-
-////////////////////////
-/// SHOULD I ALLY   ////
-////////////////////////
-
-	///////////////////////////////////
-	/// SHOULD I OFFER CEASE FIRE   ///
-	///////////////////////////////////
-	/// 	return k_GOOD_VALUE;
-
-	// 12/31 I have doubts about the afraid of him and hatfields n mccoys stuff
-
-	input gains_cease_fire
-		right yes_gains_cease_fire(gains_cease_fire, 1, .5)
-
-	if(yes_gains_cease_fire)
+	// N: added...If we're allies, let's trade maps
+	if(	yes_i_gain_map and yes_he_gets_map 
+		and yes_alliance 
+		and not yes_war
+		and not yes_he_has_been_asked_to_EXCHANGE_MAP
+		and not yes_youve_got_my_map)
 	{
-		high_priority
+		best_message_to_send
+		rand_min_25
+		rand_max_100
+		found
 	}
-
-	if(	yes_gains_cease_fire 
-		and not my_worst_enemy
-		and yes_war
-		and yes_too_many_enemies
-		and not (distrust_him or dont_trust_him)
-		and not yes_human)
+	// N: added...If we have a treaty, let's trade maps
+	if(	yes_i_gain_map and yes_he_gets_map 
+		and yes_cease_fire
+		and not yes_war
+		and not yes_he_has_been_asked_to_EXCHANGE_MAP
+		and not yes_youve_got_my_map)
 	{
-		good_message_to_send
+		best_message_to_send
+		rand_min_25
+		rand_max_100
 		found
 	}
 
-	if(	yes_gains_cease_fire 
-		and not my_worst_enemy 
-		and equal_to_him 
-		and yes_bored_of_war 
-		and yes_war 
-		and (not distrust_him or not dont_trust_him))
-		{
-			bad_message_to_send
-			found
-		}
-
-	if(	yes_gains_cease_fire 
-		and not my_worst_enemy 
-		and yes_war 
-		and yes_fear 
-		and yes_bored_of_war 
-		and (not distrust_him or not dont_trust_him)) 
-		{
-			good_message_to_send
-			found
-		}
-
-	if(	yes_gains_cease_fire 
-		and not my_worst_enemy 
-		and yes_war 
-		and yes_fear 
-		and not one_at_war 
-		and (not distrust_him or not dont_trust_him)) 
-		{
-			good_message_to_send
-			found
-		}
-
-	if(	yes_gains_cease_fire 
-		and yes_war 
-		and yes_terror 
-		and (not distrust_him or not dont_trust_him))
-		{
-			good_message_to_send
-			found
-		}
-
-	if(	yes_gains_cease_fire 
-		and yes_war 
-		and yes_sick_of_war
-		and not dont_trust_him)
-		{
-			good_message_to_send
-			found
-		}
-
-	if(	yes_gains_cease_fire 
-		and yes_war 
-		and warlike 
-		and not yes_sick_of_war)
-		{
-			worst_message_to_send
-			found
-		}
+//	// N: added...if we're at war & peaceful, I may
+//	// exchange maps to help us win 	
+//	if(	yes_i_gain_map and yes_he_gets_map 
+//		and peaceful 
+//		and equal_to_him 
+//		and yes_war
+//		and not yes_he_has_been_asked_to_EXCHANGE_MAP
+//		and not yes_youve_got_my_map)
+//	{
+//		okay_message_to_send
+//		rand_min_25
+//		rand_max_100
+//		found
+//	}
+//
+//	// N: added...if we're at war & warlike, I'll
+//	// exchange maps to help us win 	
+//	if(	yes_i_gain_map and yes_he_gets_map 
+//		and warlike 
+//		and equal_to_him 
+//		and yes_war
+//		and not yes_he_has_been_asked_to_EXCHANGE_MAP
+//		and not yes_youve_got_my_map)
+//	{
+//		good_message_to_send
+//		rand_min_25
+//		rand_max_100
+//		found
+//	}
 
-	if(	yes_gains_cease_fire 
-		and yes_chase_the_rabbit 
-		and not yes_human)
-		{
-			best_message_to_send
-		}
 
+////////////////////////
+/// SHOULD I ALLY   ////
+////////////////////////
 	/////////////////////////////////
 	/// SHOULD I OFFER ALLIANCE   ///
 	/////////////////////////////////
@@ -1527,7 +1981,7 @@ input contact_gained // 0 - 100; 100 = yes
 			and not yes_war 
 			and (not distrust_him or not dont_trust_him))
 		{
-			okay_message_to_send
+			good_message_to_send
 			found
 		}
 	
@@ -1537,7 +1991,7 @@ input contact_gained // 0 - 100; 100 = yes
 			and not yes_war 
 			and (not distrust_him or not dont_trust_him))
 		{
-			okay_message_to_send
+			good_message_to_send
 			found
 		}
 
@@ -1552,6 +2006,41 @@ input contact_gained // 0 - 100; 100 = yes
 			found
 		}
 
+		// N: added...
+		if(does_gain_alliance
+			and ai
+			and warlike 
+			and like_him 
+			and not zero_at_war 
+			and not yes_war 
+			and (not distrust_him or not dont_trust_him) )
+		{
+			best_message_to_send
+			found
+		}
+
+		// N: added...
+		if(does_gain_alliance
+			and ai
+			and neutral_towards_him 
+			and like_him 
+			and not zero_at_war 
+			and not yes_war 
+			and (not distrust_him or not dont_trust_him) )
+		{
+			best_message_to_send
+			found
+		}
+
+		// N: added: don't ask for alliance if allied
+		if(	does_gain_alliance 
+			and yes_alliance  
+			and not yes_war )
+		{
+			worst_message_to_send
+			found
+		}
+
 	///////////////////////////////////
 	/// SHOULD I OFFER AN ECOPACT   ///
 	///////////////////////////////////
@@ -1617,6 +2106,31 @@ input contact_gained // 0 - 100; 100 = yes
 			found
 		}
 
+		// N: added
+		if(	yes_end_pollution_pact 
+			and high_global_pollution 
+			and peaceful
+			and not yes_war)
+		{
+			good_message_to_send
+			rand_min_25
+			rand_max_100
+			found
+		}
+
+		// N: added
+		if(	yes_end_pollution_pact 
+			and high_global_pollution 
+			and iam_in_first_place
+			and not yes_war)
+		{
+			good_message_to_send
+			rand_min_25
+			rand_max_100
+			found
+		}
+
+
 ///////////////////////
 /// NOTHING FOUND   ///
 ///////////////////////
@@ -1628,3 +2142,14 @@ input contact_gained // 0 - 100; 100 = yes
 			low_priority
 		}
  
+		// N: added
+		if(not found
+			and not (distrust_him or dont_trust_him)
+			and not hate_him ) 
+		{
+			okay_message_to_send
+			med_priority
+		}
+ 
+
+
```

## aidata/diplomacy_rejected.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\diplomacy_rejected.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\diplomacy_rejected.fli"
index 4cb150e..c4b2afe 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\diplomacy_rejected.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\diplomacy_rejected.fli"
@@ -26,6 +26,7 @@ output diplomatic_regard_delta[-20, 20] = 0.0
 	///////////////////////////////////////////////////////
 	////////// HOW MUCH DO I WANT TO FIGHT HIM?  //////////
 	///////////////////////////////////////////////////////
+	// N: changed and changed back
 
 	input unit_regard_towards_him
 		tri hot_war(unit_regard_towards_him, 10, 11)
@@ -38,12 +39,13 @@ output diplomatic_regard_delta[-20, 20] = 0.0
 	////////////////////////////////////////////////////////////////////
 	////////// HOW MANY SOLDIERS DOES HE HAVE IN MY LAND?  /////////////
 	////////////////////////////////////////////////////////////////////
+	// N: changed
 
 	input military_incursions
-		left no_incursions(military_incursions, 0, 0.5)
-		tri few_incursions(military_incursions, 1, 0.1)
-		tri many_incursions(military_incursions, 3, 0.5)
-		right floods_incursions(military_incursions, 4, 0.5)
+		left no_incursions(military_incursions, 0, 0.25)
+		tri few_incursions(military_incursions, 1, 0.5)
+		tri many_incursions(military_incursions, 2, 0.1)
+		right floods_incursions(military_incursions, 3, 0.1)
 
 //////////////////////////////////////////////////////////
 //////////   SET STRENGTH OF STATE OF WAR      ///////////
@@ -78,9 +80,15 @@ input relative_strength
 	input he_rejected_demand_advance
 		right yes_he_rejected_demand_advance(he_rejected_demand_advance, 1.0, .5)
 
+      output special_plan[0.0, 2.0] = 0.0
+		tri yes_special_plan(special_plan, 1.0, 0.5)
+
+	// N: changed
 	if(yes_he_rejected_demand_advance)
 	{
 		dislike_him_more
+		go_to_cold_war
+		yes_special_plan
 	}
 
 /////////////////////////////////////////////
@@ -89,6 +97,7 @@ input relative_strength
 	input he_rejected_gold_demand
 		right yes_he_rejected_gold_demand(he_rejected_gold_demand, 1.0, .5)
 
+	// N: changed
 	if(yes_he_rejected_gold_demand and (dislike_him or hate_him))
 	{
 		dislike_him_more
@@ -131,19 +140,21 @@ input relative_strength
 	input he_rejected_demand_leave_our_lands
 		right yes_he_rejected_demand_leave_our_lands(he_rejected_demand_leave_our_lands, 1.0, .5)
 
+	// N: changed
 	if(yes_he_rejected_demand_leave_our_lands 
 		and (many_incursions or floods_incursions)
 		and hot_war_prep )
 	{
-		dislike_him_more
-		go_to_hot_war
+		hate_him_more
+		very go_to_hot_war
 	}
 
+	// N: changed
 	if(yes_he_rejected_demand_leave_our_lands 
 		and (many_incursions or floods_incursions)
 		and not ( hot_war_prep or hot_war ) )
 	{
-		dislike_him_more
+		hate_him_more
 		go_to_hot_war_prep
 	}
 
@@ -186,9 +197,10 @@ input relative_strength
 	input he_rejected_demand_attack_enemy
 		right rejected_attack(he_rejected_demand_attack_enemy, 1.0, 0.5)
 
+	// N: changed
 	if(rejected_attack)
 	{
-		dislike_him_more
+		hate_him_more
 	}
 
 //////////////////////////////////////////////////////
@@ -197,11 +209,19 @@ input relative_strength
 	input he_rejected_exchange_advance
 		right yes_he_rejected_exchange_advance(he_rejected_exchange_advance, 1.0, .5)
 
+	// N: changed
 	if(yes_he_rejected_exchange_advance)
+	{
+		same_like_him
+	}
+
+	// N: added
+	if(yes_he_rejected_exchange_advance and equal_to_him)
 	{
 		dislike_him_more
 	}
 
+		
 
 //////////////////////////////////////////////////////
 //////////   EXCHANGE MAP REJECTED    ///////////
@@ -253,7 +273,14 @@ input relative_strength
 	input he_rejected_offer_cease_fire
 		right yes_he_rejected_offer_cease_fire(he_rejected_offer_cease_fire, 1.0, .5)
 
+	// N: changed
 	if(yes_he_rejected_offer_cease_fire)
+	{
+		hate_him_more
+	}
+
+	// N: added
+	if(yes_he_rejected_offer_cease_fire and not hot_war)
 	{
 		dislike_him_more
 	}
@@ -264,11 +291,19 @@ input relative_strength
 input he_rejected_offer_alliance
 right yes_he_rejected_offer_alliance(he_rejected_offer_alliance, 1.0, .5)
 
+	// N: changed
 	if(yes_he_rejected_offer_alliance)
+	{
+		same_like_him
+	}
+
+	// N: added
+	if(yes_he_rejected_offer_alliance and equal_to_him )
 	{
 		dislike_him_more
 	}
 
+
 //////////////////////////////////////////////////////
 //////////   TREATY ECOPACT REJECTED    ///////////
 //////////////////////////////////////////////////////
```

## aidata/inputs.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\inputs.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\inputs.fli"
index c77445b..2c78edd 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\inputs.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\inputs.fli"
@@ -28,7 +28,7 @@ input unit_to_city_best_human_ratio
 	right aover4unit_to_city_best_human_ratio(unit_to_city_best_human_ratio, 4.0, 0.1)
 
 input unit_to_city_ratio
-	left dangerously_low_unit_to_city_ratio(unit_to_city_ratio, 3.0, 0.1)
+	left dangerously_low_unit_to_city_ratio(unit_to_city_ratio, 2.5, 0.1) //Edited TLL 13/6/99 (from 3.0)
 	
 input i_agreed_to_stop_polluting
 	tri yes_i_agreed_to_stop_polluting(i_agreed_to_stop_polluting, 1.0, 0.5)
@@ -40,7 +40,7 @@ input can_space_settle
 	tri yes_can_space_settle(can_space_settle, 1.0, 0.5)
 
 input can_sea_settle
-	tri yes_can_sea_settle(can_space_settle, 1.0, 0.5)
+	tri yes_can_sea_settle(can_sea_settle, 1.0, 0.5) //edited TLL 13/6/99
 
 input diff_level
 	tri chieftain(diff_level, 0.0, 0.5)
@@ -75,6 +75,7 @@ input highest_enemy_strength_ratio
 	tri i_am_equal_to_strongest(highest_enemy_strength_ratio, 1.5, 0.6)
 	tri i_am_stronger_2x_to_4x_than_strongest(highest_enemy_strength_ratio, 3.0, 1.0)
 	right i_am_stronger_4x_plus_than_strongest(highest_enemy_strength_ratio, 5.0, 1.0)
+	right i_am_stronger_1halfx_plus_than_strongest(highest_enemy_strength_ratio, 2.5, 1.0) //Added by TLL 13/6/99
 
 input highest_human_enemy_strength_ratio
 	tri i_am_weaker_4x_plus_than_strongest_human(highest_human_enemy_strength_ratio, 0.15, 0.15)
@@ -82,6 +83,7 @@ input highest_human_enemy_strength_ratio
 	tri i_am_equal_to_strongest_human(highest_human_enemy_strength_ratio, 1.5, 0.6)
 	tri i_am_stronger_2x_to_4x_than_strongest_human(highest_human_enemy_strength_ratio, 3.0, 1.0)
 	right i_am_stronger_4x_plus_than_strongest_human(highest_human_enemy_strength_ratio, 5.0, 1.0)
+	right i_am_stronger_1halfx_plus_than_strongest_human(highest_human_enemy_strength_ratio, 2.5, 1.0) //Added by TLL 13/6/99
 
 input total_enemy_strength_ratio
 	tri i_am_weaker_4x_plus_than_total_enemies(total_enemy_strength_ratio, 0.15, 0.15)
@@ -167,10 +169,7 @@ input lowest_unit_regard
 	tri peace_with_most_hostile(lowest_unit_regard, 90.0, 15)
 
 input total_military_incursions
-	tri no_incursions(total_military_incursions, 0.0, 0.1)
-	tri one_incursion(total_military_incursions, 1.0, 0.1)
-	tri few_incursions(total_military_incursions, 3.0, 1.9)
-	right many_incursions(total_military_incursions, 6.0, 1.0)
+//removed TLL 13/6/99 - to avoid conflict with similarly named strings in diplomacy AI
 
 // set the military readiness costs
 input percent_cost_readiness
@@ -179,7 +178,7 @@ input percent_cost_readiness
 	tri costly_army_pcr(percent_cost_readiness, 0.30, 0.1)
 	right ouch_army_pcr(percent_cost_readiness, 0.4, 0.1)
 
-// how many people am I fighting
+// how many people am I fighting...N: added 8/11/99
 input at_war_count
 	tri zero_at_war(at_war_count, 0.0, 0.5)
 	tri one_at_war(at_war_count, 1.0, 0.5)
@@ -188,6 +187,16 @@ input at_war_count
 	tri four_at_war(at_war_count, 4.0, 0.5)
 	tri five_at_war(at_war_count, 5.0, 0.5)
 	tri six_at_war(at_war_count, 6.0, 0.5)
+	tri seven_at_war(at_war_count, 7.0, 0.5)
+	tri eight_at_war(at_war_count, 8.0, 0.5)
+	tri nine_at_war(at_war_count, 9.0, 0.5)
+	tri ten_at_war(at_war_count, 10.0, 0.5)
+	tri eleven_at_war(at_war_count, 11.0, 0.5)
+	tri twelve_at_war(at_war_count, 12.0, 0.5)
+	tri thirteen_at_war(at_war_count, 13.0, 0.5)
+	tri fourteen_at_war(at_war_count, 14.0, 0.5)
+	tri fifteen_at_war(at_war_count, 15.0, 0.5)
+	tri sixteen_at_war(at_war_count, 16.0, 0.5)
 
 input land_continents_full
 	left empty_continent(land_continents_full, 0.1, 0.3)
@@ -225,6 +234,7 @@ input num_cities
 	tri a1_num_cities(num_cities, 1.0, 0.5)
 	tri a2to3_num_cities(num_cities, 2.5, 0.6)
 	tri a2_num_cities(num_cities, 2.0, 0.5)
+	tri a2to4_num_cities(num_cities, 3.0, 1.1) //Added by TLL 12/6/99
 	tri a1to5_num_cities(num_cities, 3.0, 2.5)
 	tri a1to7_num_cities(num_cities, 4.0, 3.5)
 	tri a3to5_num_cities(num_cities, 4.0, 1.5)
@@ -270,6 +280,7 @@ input time
 	right a200plus_turns(time, 210.0, 10.0)
 	right diamond_time(time, 400, 50.0)
 	right not_ancient_time(time, 100, 5.0)
+	tri a0to40_turns(time, 20.0, 20.0) //defined TLL 14/6/99
 
 output opening_gambit_time[0.0, 2.0] = 0.0
 	tri yes_opening_gambit_time(opening_gambit_time, 1.0, 0.5)
@@ -279,12 +290,25 @@ output opening_gambit_time[0.0, 2.0] = 0.0
 		yes_opening_gambit_time
 	}
 
+	// N: new map sizes added, old ones corrected--8/11/99
 input size_of_world
 	tri a24_48_map(size_of_world, 1152, 250.0)
 	tri a32_64_map(size_of_world, 2048, 250.0)
 	tri a48_96_map(size_of_world, 4608, 250.0)
-	tri a64_128_map(size_of_world, 1152, 250.0)
-	tri a70_140_map(size_of_world, 8192, 250.0)
+	tri a64_128_map(size_of_world, 8192, 250.0) // corrected..N
+	tri a70_140_map(size_of_world, 9800, 250.0) // corrected..N
+	tri a86_172_map(size_of_world, 14792, 250.0)
+	tri a102_204_map(size_of_world, 20808, 250.0)
+	tri a118_236_map(size_of_world, 27848, 250.0)
+	tri a134_268_map(size_of_world, 35912, 250.0)
+	tri a150_300_map(size_of_world, 45000, 250.0)
+	tri a166_332_map(size_of_world, 55112, 250.0)
+	tri a182_364_map(size_of_world, 66248, 250.0)
+	tri a198_396_map(size_of_world, 78408, 250.0)
+	tri a214_428_map(size_of_world, 91592, 250.0)
+	tri a230_460_map(size_of_world, 105800, 250.0)
+	tri a246_492_map(size_of_world, 121032, 250.0)
+
 
 input wgf_prod_setting
 input wgf_gold_setting 
@@ -338,6 +362,7 @@ input total_pop_size
 	tri one_total_pop(total_pop_size, 1.0, 0.25)
 	tri two_total_pop(total_pop_size, 2.0, 0.25)
 
+	// N: added more players--8/11/99
 input num_players_in_game
 	tri three_players(num_players_in_game, 3.0, 0.5)
 	tri four_players(num_players_in_game, 4.0, 0.5)
@@ -345,3 +370,27 @@ input num_players_in_game
 	tri six_players(num_players_in_game, 6.0, 0.5)
 	tri seven_players(num_players_in_game, 7.0, 0.5)
 	tri eight_players(num_players_in_game, 8.0, 0.5)
+	tri nine_players(num_players_in_game, 9.0, 0.5)
+	tri ten_players(num_players_in_game, 10.0, 0.5)
+	tri eleven_players(num_players_in_game, 11.0, 0.5)
+	tri twelve_players(num_players_in_game, 12.0, 0.5)
+	tri thirteen_players(num_players_in_game, 13.0, 0.5)
+	tri fourteen_players(num_players_in_game, 14.0, 0.5)
+	tri fifteen_players(num_players_in_game, 15.0, 0.5)
+	tri sixteen_players(num_players_in_game, 16.0, 0.5)
+	tri seventeen_players(num_players_in_game, 17.0, 0.5)
+	tri eighteen_players(num_players_in_game, 18.0, 0.5)
+	tri nineteen_players(num_players_in_game, 19.0, 0.5)
+	tri twenty_players(num_players_in_game, 20.0, 0.5)
+	tri twentyone_players(num_players_in_game, 21.0, 0.5)
+	tri twentytwo_players(num_players_in_game, 22.0, 0.5)
+	tri twentythree_players(num_players_in_game, 23.0, 0.5)
+	tri twentyfour_players(num_players_in_game, 24.0, 0.5)
+	tri twentyfive_players(num_players_in_game, 25.0, 0.5)
+	tri twentysix_players(num_players_in_game, 26.0, 0.5)
+	tri twentyseven_players(num_players_in_game, 27.0, 0.5)
+	tri twentyeight_players(num_players_in_game, 28.0, 0.5)
+	tri twentynine_players(num_players_in_game, 29.0, 0.5)
+	tri thirty_players(num_players_in_game, 30.0, 0.5)
+  	tri thirtyone_players(num_players_in_game, 31.0, 0.5)
+	tri thirtytwo_players(num_players_in_game, 32.0, 0.5)
\ No newline at end of file
```

## aidata/outputs.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\outputs.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\outputs.fli"
index 7ce2ff6..463ebee 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\outputs.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\outputs.fli"
@@ -49,8 +49,8 @@ output military_aip[0.0, 5.0] = 5.0
 // 10% excess Food
 output min_food_factor[0.0, 3.0] = 1.5
 	tri no_growth_min_food_factor(min_food_factor, 1.0, 0.1)
-	tri average_growth_min_food_factor(min_food_factor, 1.5, 0.1)
-	tri high_growth_min_food_factor(min_food_factor, 2.0, 0.1)
+	tri average_growth_min_food_factor(min_food_factor, 1.5, 0.1) 
+	tri high_growth_min_food_factor(min_food_factor, 1.7, 0.1) //WW from 2.0
 
 // force the ai to use expectations
 output use_expectations[0.0, 3.0] = 0.0
@@ -59,29 +59,29 @@ output use_expectations[0.0, 3.0] = 0.0
 // pick roads or no roads
 output inst_road_coef[0.0, 100.0] = 0.0
 	tri zero_roads(inst_road_coef, 0.0, 0.001)
-	tri no_roads(inst_road_coef, 0.01, 0.001)
+	tri no_roads(inst_road_coef, 0.05, 0.001) // TTL from 0.0, WW from .01
 	tri yes_roads(inst_road_coef, 1.0, 0.001)
 
-// weight the choice of wgf
-output wgf_production[0.0, 20.0]= 7.5
-	tri work_forgetit_wgf_production(wgf_production, 6.0, 0.5)
-	tri work_little_wgf_production(wgf_production, 8.0, 0.5)
-	tri work_ave_wgf_production(wgf_production, 10.0, 0.5)
-	tri work_hard_wgf_production(wgf_production, 24.0, 0.5) // from 12
+// weight the choice of wgf // WW minimized deviation of settings 
+output wgf_production[0.0, 20.0]= 5.0 // WW from 7.5
+	tri work_forgetit_wgf_production(wgf_production, 3.0, 0.5)
+	tri work_little_wgf_production(wgf_production, 4.0, 0.5)
+	tri work_ave_wgf_production(wgf_production, 5.0, 0.5)
+	tri work_hard_wgf_production(wgf_production, 6.0, 0.5) // from 12
 
-output wgf_food[0.0, 45.0]= 0.2 
-	tri feed_lots_wgf_food(wgf_food, 0.5, 0.5)
+output wgf_food[0.0, 45.0]= 0.5 // WW from 0.2 
+	tri feed_lots_wgf_food(wgf_food, 3.0, 0.5)
 	tri feed_well_wgf_food(wgf_food, 4.0, 0.5)
 	tri feed_ave_wgf_food(wgf_food, 5.0, 0.5)
-	tri feed_nothing_wgf_food(wgf_food, 25.0, 0.5)
+	tri feed_nothing_wgf_food(wgf_food, 6.0, 0.5)
 // increased feed nothing to 25 to keep food as low as possible
 
 output wgf_gold[0.0,20.0]= 3.0
-	tri care_not_wgf_gold(wgf_gold, 0.1 , 0.1)
+	tri care_not_wgf_gold(wgf_gold, 3.0 , 0.1)
 	tri pay_lots_wgf_gold(wgf_gold, 4.0, 0.1)
-	tri pay_ave_wgf_gold(wgf_gold, 8.0, 0.1)
-	tri pay_little_wgf_gold(wgf_gold, 10.0, 0.1)
-	tri pay_nothing_wgf_gold(wgf_gold, 25.0, 0.1)
+	tri pay_ave_wgf_gold(wgf_gold, 5.0, 0.1)
+	tri pay_little_wgf_gold(wgf_gold, 6.0, 0.1)
+	tri pay_nothing_wgf_gold(wgf_gold, 6.0, 0.1)
 
 output set_wgf[0.0, 9.0] = 5.0
 	tri growth_prod_gold_deficit_set_wgf(set_wgf, 1.0, 0.5)
@@ -106,80 +106,80 @@ output budget_income_wages[0.0, 1.0] = .5
 	tri ninety_budget_income_wages(budget_income_wages, 0.95, 0.05)
 	tri max_budget_income_wages	(budget_income_wages, 1.0, 0.05)
 
-output desired_military_readiness[0.0, 2.0] = 0.0
+output desired_military_readiness[0.0, 2.0] = 1.0 // WW from 0.0
 	tri peace_military_readiness(desired_military_readiness, 0.0, 0.25)
 	tri ready_military_readiness(desired_military_readiness, 1.0, 0.25)
 	tri war_military_readiness(desired_military_readiness, 2.0, 0.25)
 
-output production[0.0, 1.3] = 0.99
-	tri low_production(production, 0.33, 0.2)
-	tri med_production(production, 0.66, 0.2)
-	tri high_production(production, 0.99, 0.2)
+output production[0.0, 1.3] = 0.50 // WW from .99
+	tri low_production(production, 0.50, 0.2) //WW from .33
+	tri med_production(production, 0.50, 0.2) //WW from .66
+	tri high_production(production, 0.50, 0.2) //WW from .99 for all sections
 
-output food[0.0, 1.3] = 0.33
-	tri low_food(food, 0.33, 0.2)
-	tri med_food(food, 0.66, 0.2)
-	tri high_food(food, 0.99, 0.2)
+output food[0.0, 1.3] = 0.50 // WW from .33
+	tri low_food(food, 0.50, 0.2)
+	tri med_food(food, 0.50, 0.2)
+	tri high_food(food, 0.50, 0.2)
 
-output science[0.0, 1.3] = 0.33
-	tri low_science(science, 0.33, 0.2)
-	tri med_science(science, 0.66, 0.2)
-	tri high_science(science, 0.99, 0.2)
+output science[0.0, 1.3] = 0.50 // WW from .33
+	tri low_science(science, 0.50, 0.2)
+	tri med_science(science, 0.50, 0.2)
+	tri high_science(science, 0.50, 0.2)
 
-output happiness[0.0, 1.3] =0.1
-	tri low_happiness(happiness, 0.33, 0.2)
-	tri med_happiness(happiness, 0.66, 0.2)
-	tri high_happiness(happiness, 0.99, 0.2)
+output happiness[0.0, 1.3] =0.50 // WW from .10
+	tri low_happiness(happiness, 0.50, 0.2)
+	tri med_happiness(happiness, 0.50, 0.2)
+	tri high_happiness(happiness, 0.50, 0.2)
 
 output defense[0.0, 1.3]=0.33
-	tri low_defense(defense, 0.33, 0.2)
-	tri med_defense(defense, 0.66, 0.2)
-	tri high_defense(defense, 0.99, 0.2)
+	tri low_defense(defense, 0.50, 0.2)
+	tri med_defense(defense, 0.50, 0.2)
+	tri high_defense(defense, 0.50, 0.2)
 
 output offense[0.0, 1.3]=0.33
-	tri low_offense(offense, 0.33, 0.2)
-	tri med_offense(offense, 0.66, 0.2)
-	tri high_offense(offense, 0.99, 0.2)
+	tri low_offense(offense, 0.50, 0.2)
+	tri med_offense(offense, 0.50, 0.2)
+	tri high_offense(offense, 0.50, 0.2)
 
 //priorities of population placement
 // 100 is 1x in principle
 // 
-output pop_gold[0,2000] = 150 
+output pop_gold[0,2000] = 100 // WW from 150
 	tri zero_pop_gold (pop_gold, 0.0, 10.0)
 	tri low_pop_gold (pop_gold, 10, 10.0)
-	tri med_pop_gold (pop_gold, 150, 100.0)
+	tri med_pop_gold (pop_gold, 100, 100.0) // used WW from 150
 	tri high_pop_gold (pop_gold, 300, 100.0)
 	tri super_high_pop_gold(pop_gold, 1000.0, 100.0)
 
-output pop_production_max[-1000,10000] = 110.0 // was 100, 450, 900 -- trying 100, 650, 1200
-	tri low_pop_production_max (pop_production_max, 10, 100.0)
-	tri med_pop_production_max (pop_production_max, 110, 100.0)
-	tri high_pop_production_max (pop_production_max, 400, 100.0)
+output pop_production_max[-1000,10000] = 110.0 // was 100, 450, 900 -- trying 100, 650, 1200 --WW set to these below
+	tri low_pop_production_max (pop_production_max, 200, 100.0)
+	tri med_pop_production_max (pop_production_max, 100, 100.0) // used
+	tri high_pop_production_max (pop_production_max, 1500, 100.0)
 
 output pop_production_min[0,2000] = 110.0
 	tri super_low_pop_production_min (pop_production_min, 10, 100.0)
-	tri low_pop_production_min (pop_production_min, 50, 10.0)
-	tri med_pop_production_min (pop_production_min, 110, 10.0)
+	tri low_pop_production_min (pop_production_min, 100, 10.0) //used WWfrom50
+	tri med_pop_production_min (pop_production_min, 150, 10.0) // WW from 110
 	tri high_pop_production_min (pop_production_min, 200, 10.0)
 
-output pop_food_max[0,1000] = 100.0
+output pop_food_max[0,1000] = 100.0 // WW minimized deviation of settings
 	tri super_low_pop_food_max (pop_food_max, 10.0, 10.0)
-	tri low_pop_food_max (pop_food_max, 50.0, 10.0)
+	tri low_pop_food_max (pop_food_max, 75.0, 10.0)
 	tri med_pop_food_max (pop_food_max, 100.0, 10.0)
-	tri high_pop_food_max (pop_food_max, 200.0, 10.0)
+	tri high_pop_food_max (pop_food_max, 150.0, 10.0)
 	tri odd_pop_food_max (pop_food_max, 113.0, 100.0) // force people to move
 
-output pop_food_min[0,1000] = 10.0
-	tri low_pop_food_min (pop_food_min, 10.0, 10.0)
-	tri med_pop_food_min (pop_food_min, 100.0, 10.0)
-	tri high_pop_food_min (pop_food_min, 200.0, 10.0)
+output pop_food_min[0,1000] = 100.0 // WW from 10, min deviation of settings 
+	tri low_pop_food_min (pop_food_min, 50.0, 10.0)
+	tri med_pop_food_min (pop_food_min, 75.0, 10.0)
+	tri high_pop_food_min (pop_food_min, 125.0, 10.0)
 	tri odd_pop_food_min (pop_food_min, 113.0, 10.0) // force people to move
 
-output pop_science[0, 25000] = 150.0
+output pop_science[0, 25000] = 100.0 // WW from 150, min deviation of settings 
 	tri zero_pop_science (pop_science, 0.0, 10.0)
-	tri low_pop_science (pop_science, 10, 10.0)
-	tri med_pop_science (pop_science, 150, 10.0)
-	tri high_pop_science (pop_science, 200, 10.0)
+	tri low_pop_science (pop_science, 75, 10.0)
+	tri med_pop_science (pop_science, 100, 10.0)
+	tri high_pop_science (pop_science, 125, 10.0)
 	tri super_pop_science (pop_science, 400, 10.0)
 
 output pop_happiness[0, 1000] = 0.0
@@ -196,11 +196,11 @@ output max_crime[0.0,100.0]=15.0
 
 // percent of city production that goes into the terrain improment pool 
 // actual range is between 0 and 1.0
-output production_tax[0.0, 1.0]=0.99
-	tri super_zero_production_tax(production_tax, 0.001, 0.1)
-	tri zero_production_tax(production_tax, 0.0, 0.00025)
-	tri low_production_tax(production_tax, 0.10, 0.00025)
-	tri med_production_tax(production_tax, 0.30, 0.00025)
+output production_tax[0.0, 1.0]=0.20 // WW from .99
+	tri super_zero_production_tax(production_tax, 0.001, 0.1) 
+	tri zero_production_tax(production_tax, 0.0, 0.00025) 
+	tri low_production_tax(production_tax, 0.10, 0.00025) 
+	tri med_production_tax(production_tax, 0.20, 0.00025) //TLL 13/6/99
 	tri high_production_tax(production_tax, 0.50, 0.00025)
 	tri super_high_production_tax(production_tax, 0.80, 0.00025)
 	tri max_production_tax(production_tax, 1.0, 0.00025)
@@ -230,10 +230,10 @@ output explore_priority[0.0, 100.0] = 0.01 // how much do we want to explore?
 // settling
 
 output settler_packing[0.0, 10.0] = 4 //target average distance between cities
-	tri truly_dense_settler_packing(settler_packing, 3.0, 0.5)
-	tri dense_settler_packing(settler_packing, 3.5, 0.5)
-	tri loose_settler_packing(settler_packing, 4.0, 0.5)
-	tri very_loose_settler_packing(settler_packing, 4.5, 0.5)
+	tri truly_dense_settler_packing(settler_packing, 3.7, 0.5) // WW from 3.0
+	tri dense_settler_packing(settler_packing, 3.7, 0.5)
+	tri loose_settler_packing(settler_packing, 3.7, 0.5)
+	tri very_loose_settler_packing(settler_packing, 3.7, 0.5) // WW from 4.5
 
 // modulate the net utility functions
 output wonder_uscale[0.0, 10000] = 1.0
@@ -406,8 +406,21 @@ output i_want_this_gov_VIRTUAL_D[-2.0, 12.0]=-1.0
 	tri gov_virtual_d_9 (I_want_this_gov_VIRTUAL_D, 9.0, 0.1)
 	tri gov_virtual_d_10 (I_want_this_gov_VIRTUAL_D,10.0, 0.1)
 
+//Added by TLL 5/5/99
+output i_want_this_gov_FUNDAMENTALISM[-2.0, 12.0]=-1.0
+	tri gov_fundamentalism_1 (I_want_this_gov_FUNDAMENTALISM, 1.0, 0.1)
+	tri gov_fundamentalism_2 (I_want_this_gov_FUNDAMENTALISM, 2.0, 0.1)
+	tri gov_fundamentalism_3 (I_want_this_gov_FUNDAMENTALISM, 3.0, 0.1)
+	tri gov_fundamentalism_4 (I_want_this_gov_FUNDAMENTALISM, 4.0, 0.1)
+	tri gov_fundamentalism_5 (I_want_this_gov_FUNDAMENTALISM, 5.0, 0.1)
+	tri gov_fundamentalism_6 (I_want_this_gov_FUNDAMENTALISM, 6.0, 0.1)
+	tri gov_fundamentalism_7 (I_want_this_gov_FUNDAMENTALISM, 7.0, 0.1)
+	tri gov_fundamentalism_8 (I_want_this_gov_FUNDAMENTALISM, 8.0, 0.1)
+	tri gov_fundamentalism_9 (I_want_this_gov_FUNDAMENTALISM, 9.0, 0.1)
+	tri gov_fundamentalism_10 (I_want_this_gov_FUNDAMENTALISM,10.0, 0.1)
+
 // set the government that I want -- counts from one
-//output I_want_this_gov[0,14] = 11.0
+//output I_want_this_gov[0,14] = 12.0
 //	tri gov_tyranny (I_want_this_gov, 1.0, 0.5)
 //	tri gov_monarchy (I_want_this_gov, 2.0, 0.5)
 //	tri gov_theocracy (I_want_this_gov, 3.0, 0.5)
@@ -415,20 +428,21 @@ output i_want_this_gov_VIRTUAL_D[-2.0, 12.0]=-1.0
 //	tri gov_democracy (I_want_this_gov, 5.0, 0.5)
 //	tri gov_communism (I_want_this_gov, 6.0, 0.5)
 //	tri gov_fascism (I_want_this_gov, 7.0, 0.5)
-//	tri gov_ecotopia (I_want_this_gov, 8.0, 0.5)
-//	tri gov_multicorp (I_want_this_gov, 9.0, 0.5)
-//	tri gov_technocracy (I_want_this_gov, 10.0, 0.5)
-//	tri gov_virtual_d (I_want_this_gov, 11.0, 0.5)
+//	tri gov_fundamentalism (I_want_this_gov, 8.0, 0.5)
+//	tri gov_ecotopia (I_want_this_gov, 9.0, 0.5)
+//	tri gov_multicorp (I_want_this_gov, 10.0, 0.5)
+//	tri gov_technocracy (I_want_this_gov, 11.0, 0.5)
+//	tri gov_virtual_d (I_want_this_gov, 12.0, 0.5)
 
 output i_want_this_gov_uscale[0,10000] = 10000
 	tri gov_dont_care_uscale (i_want_this_gov_uscale, 0.1, 0.1)
 	tri gov_give_me_uscale (i_want_this_gov_uscale, 10000.0, 0.1)
 
-// was 1, 8, 30, trying 8, 50
-output inst_prod[0,100] = 1.0
-	tri few_mines(inst_prod, 1.0, 0.5)
-	tri default_mines(inst_prod, 8.0, 0.5)
-	tri tons_mines(inst_prod, 30.0, 0.5) 
+// was 1, 8, 30, trying 8, 50 ---WW to current
+output inst_prod[0,100] = 10.0 // WW from 1.0
+	tri few_mines(inst_prod, 5.0, 0.5)
+	tri default_mines(inst_prod, 10.0, 0.5)
+	tri tons_mines(inst_prod, 15.0, 0.5) 
 	
 // was 5, 10, 15
 output inst_food[0, 100] = 10.0 
```

## aidata/personality.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personality.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personality.fli"
index d6af998..19ef5cd 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personality.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personality.fli"
@@ -53,6 +53,6 @@ fuzzy_pre_outgoing_diplomacy {
     output exchange_map_coeff[0, 10000] = 1.0
     output give_advance[0, 10000] = 1
 
-	// Won't send the same message more often than this many turns
-	output diplomatic_persistence[0, 10000] = 10
+	// Won't send the same message more often than this many turns...changed to fifteen from ten..N.
+	output diplomatic_persistence[0, 10000] = 15
 }
```

## aidata/personalityCleric.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalityCleric.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalityCleric.fli"
index 9ba2645..98f56a5 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalityCleric.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalityCleric.fli"
@@ -28,7 +28,7 @@ fuzzy_pre_outgoing_diplomacy {
     output exchange_map_coeff[0, 10000] = 1
     output give_advance[0, 10000] = 1
 
-	// Won't send the same message more often than this many turns
-	output diplomatic_persistence[0, 10000] = 17
+	// Won't send the same message more often than this many turns...changed to twenty from seventeen..N.
+	output diplomatic_persistence[0, 10000] = 20
 }
 
```

## aidata/personalityDefault.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalityDefault.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalityDefault.fli"
index d6af998..8d80667 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalityDefault.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalityDefault.fli"
@@ -53,6 +53,6 @@ fuzzy_pre_outgoing_diplomacy {
     output exchange_map_coeff[0, 10000] = 1.0
     output give_advance[0, 10000] = 1
 
-	// Won't send the same message more often than this many turns
-	output diplomatic_persistence[0, 10000] = 10
+	// Won't send the same message more often than this many turns...changed to thirteen from nine..N.
+	output diplomatic_persistence[0, 10000] = 13
 }
```

## aidata/personalitySciFew.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalitySciFew.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalitySciFew.fli"
index 39a1c5d..227c018 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalitySciFew.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalitySciFew.fli"
@@ -53,6 +53,6 @@ fuzzy_pre_outgoing_diplomacy {
     output exchange_map_coeff[0, 10000] = 1
     output give_advance[0, 10000] = 1
 
-	// Won't send the same message more often than this many turns
-	output diplomatic_persistence[0, 10000] = 13
+	// Won't send the same message more often than this many turns...changed to fifteen from thirteen..N.
+	output diplomatic_persistence[0, 10000] = 15
 }
```

## aidata/personalitySciMany.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalitySciMany.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalitySciMany.fli"
index 977d6da..3d46614 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalitySciMany.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalitySciMany.fli"
@@ -29,6 +29,6 @@ fuzzy_pre_outgoing_diplomacy {
     output exchange_map_coeff[0, 10000] = 0
     output give_advance[0, 10000] = 1
 
-	// Won't send the same message more often than this many turns
-	output diplomatic_persistence[0, 10000] = 9
+	// Won't send the same message more often than this many turns...changed from nine to thirteen..N.
+	output diplomatic_persistence[0, 10000] =13 
 }
```

## aidata/personalitySlaver.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalitySlaver.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalitySlaver.fli"
index 1670dad..5920fb4 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalitySlaver.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalitySlaver.fli"
@@ -27,7 +27,7 @@ fuzzy_pre_outgoing_diplomacy {
     output exchange_map_coeff[0, 10000] = 1
     output give_advance[0, 10000] = 1
 
-	// Won't send the same message more often than this many turns
-	output diplomatic_persistence[0, 10000] = 10
+	// Won't send the same message more often than this many turns...changed to thirteen from ten..N.
+	output diplomatic_persistence[0, 10000] = 13
 }
 
```

## aidata/personalityWarFew.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalityWarFew.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalityWarFew.fli"
index e2bfad2..fc150f5 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalityWarFew.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalityWarFew.fli"
@@ -26,7 +26,7 @@ fuzzy_pre_outgoing_diplomacy {
     output exchange_map_coeff[0, 10000] = 1.0
     output give_advance[0, 10000] = 1
 
-	// Won't send the same message more often than this many turns
-	output diplomatic_persistence[0, 10000] = 5.0
+	// Won't send the same message more often than this many turns...changed to eight from five..N.
+	output diplomatic_persistence[0, 10000] = 8.0
 }
 
```

## aidata/personalityWarMany.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalityWarMany.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalityWarMany.fli"
index 8fb18cb..a0ea94a 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\personalityWarMany.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\personalityWarMany.fli"
@@ -26,7 +26,7 @@ fuzzy_pre_outgoing_diplomacy {
     output exchange_map_coeff[0, 10000] = 1.0
     output give_advance[0, 10000] = 1
 
-	// Won't send the same message more often than this many turns
-	output diplomatic_persistence[0, 10000] = 15.0
+	// Won't send the same message more often than this many turns...changed to seventen from fifteen..N.
+	output diplomatic_persistence[0, 10000] = 17.0
 }
 
```

## aidata/set_food_or_prod.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_food_or_prod.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_food_or_prod.fli"
index 5bafaf3..3d879cf 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_food_or_prod.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_food_or_prod.fli"
@@ -26,7 +26,6 @@
 
 	if(a2_num_cities and not yes_barbarian)
 	{	
-		even_city_growth_ratio
 		very zero_production_tax
 		growth_prod_gold_deficit_set_wgf
 		high_production
@@ -35,7 +34,6 @@
 
 	if(a3to5_num_cities and not yes_barbarian and yes_warrior) 
 	{
-		even_city_growth_ratio
 		growth_prod_gold_set_wgf
 		very zero_production_tax
 		high_production
@@ -44,27 +42,22 @@
 
 	if(a5to9_num_cities and not yes_barbarian and yes_warrior)
 	{
-		even_city_growth_ratio
-		med_production_tax
+		very med_production_tax
 		high_production
 		growth_prod_gold_set_wgf
-		yes_opening_game_strategy
 	}
 
 	if(a3to5_num_cities and not yes_barbarian and yes_scientist) 
 	{
-		even_city_growth_ratio
 		growth_prod_gold_set_wgf
-		med_production_tax
+		very zero_production_tax
 		yes_opening_game_strategy
 	} 
 
 	if(a5to9_num_cities and not yes_barbarian and yes_scientist) 
 	{  
-		even_city_growth_ratio
 		growth_prod_gold_set_wgf
-		med_production_tax
-		yes_opening_game_strategy
+		very med_production_tax
 	} 
 
 	if(a3to5_num_cities 
@@ -72,9 +65,8 @@
 	and not yes_scientist
 	and not yes_warrior) 
 	{
-		even_city_growth_ratio
 		growth_prod_gold_set_wgf
-		med_production_tax
+		very zero_production_tax
 		yes_opening_game_strategy
 	} 
 
@@ -83,10 +75,8 @@
 	and not yes_scientist
 	and not yes_warrior) 
 	{  
-		even_city_growth_ratio
 		growth_prod_gold_set_wgf
-		med_production_tax
-		yes_opening_game_strategy
+		very med_production_tax
 	} 
 
 
@@ -98,7 +88,6 @@
 // if barbarian then forget food
 if (yes_barbarian) 
 { 
-	max_production_city_growth_ratio
 	very zero_production_tax	
 	high_production		
 	yes_opening_game_strategy	
```

## aidata/set_inst_priority.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_inst_priority.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_inst_priority.fli"
index 44be80f..2a5d599 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_inst_priority.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_inst_priority.fli"
@@ -1,12 +1,12 @@
 // set_inst_priority.fli
 if(not farm_count )
 	{
-		tons_mines
+		default_mines
 	}
 
 if( farm_count )
 	{
-		tons_mines
+		default_farms
 	}
 
 
```

## aidata/set_pw.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_pw.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_pw.fli"
index 0ec2984..7420f97 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_pw.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_pw.fli"
@@ -35,21 +35,21 @@ if(	zero_at_war
 	and yes_enough_pw
 	and not yes_opening_game_strategy )
 	{
-		super_zero_production_tax
+		very low_production_tax
 	}
 
 if (not zero_at_war 
 	and yes_enough_pw
 	and not yes_opening_game_strategy )
 	{
-		super_zero_production_tax
+		very low_production_tax
 	}
 
 if(	zero_at_war 
 	and not yes_enough_pw
 	and not yes_opening_game_strategy)
 	{
-		super_high_production_tax
+		very med_production_tax
 	}
 
 if (not zero_at_war 
@@ -57,24 +57,24 @@ if (not zero_at_war
 	and not yes_opening_game_strategy
 	)
 	{
-		med_production_tax
+		very med_production_tax
 	}
 
 if (yes_i_can_build_wormhole_probe)
 {
-	super_zero_production_tax
+	very zero_production_tax
 }
 
 if (yes_focus_on_units)
 {
-	super_zero_production_tax
+	very zero_production_tax
 }
 
 if (not yes_enough_pw
 	and dangerously_high_gold_and_wages_cost 
 	and not yes_focus_on_units)
 	{
-		very super_high_production_tax
+		very high_production_tax
 	}
 
 //if (two_thousand_plus_desired_mine_pw)
```

## aidata/set_resource_desire.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_resource_desire.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_resource_desire.fli"
index 240dfce..6c632ba 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_resource_desire.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_resource_desire.fli"
@@ -19,7 +19,7 @@
 
 // high production is the default behavior
 if (not yes_opening_game_strategy
-	and not yes_barbarian)
+	and not a5to9_num_cities and not yes_barbarian)
 {
 	med_pop_production_max // 101
 	low_pop_production_min // 50
@@ -27,9 +27,8 @@ if (not yes_opening_game_strategy
 } 
 
 if(	not yes_opening_game_strategy 
-	and not yes_barbarian)
+	and not a5to9_num_cities and not yes_barbarian)
 {
-	even_city_growth_ratio
 	growth_prod_gold_set_wgf
 }	
 
```

## aidata/set_science_speed.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_science_speed.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_science_speed.fli"
index 77cba5c..323fa25 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_science_speed.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_science_speed.fli"
@@ -29,7 +29,6 @@ if (not yes_opening_game_strategy
 if(not yes_opening_game_strategy 
 and not yes_barbarian)
 {
-	even_city_growth_ratio
 	growth_prod_gold_set_wgf
 }	
 
@@ -56,4 +55,4 @@ if (yes_barbarian) {
 	high_pop_production_min
 	low_pop_food_max
 	low_pop_food_min
-}
\ No newline at end of file
+}
```

## aidata/set_settle_density.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_settle_density.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_settle_density.fli"
index 39fec79..8600291 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_settle_density.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_settle_density.fli"
@@ -19,7 +19,7 @@
 
 	if(a1_num_cities and yes_settle_dense)
 	{
-		truly_dense_settler_packing
+		dense_settler_packing
 	}
 
 	if((a2_num_cities or a3to5_num_cities) and yes_settle_dense)
@@ -50,21 +50,21 @@ output settle_patience[0.0, 10000.0] = 500.0
 
 	if(dense_settler_packing and not yes_survival_mode_aip)
 	{
-		settler_get_best_spot
+		settler_default_behavior 
 		normal_settle_patience
 	}
 
 	if(truly_dense_settler_packing and not yes_survival_mode_aip)
 	{
-		settler_get_best_spot
-		short_settle_patience
+		settler_default_behavior 
+		normal_settle_patience
 	}
 
 	if(loose_settler_packing 
 		and ( yes_survival_mode_aip or not zero_at_war ))
 	{
 		settler_watch_for_enemies
-		normal_settle_patience
+		long_settle_patience
 	}
 
 	if(	dense_settler_packing 
```

## aidata/set_wgf.fli
```diff
diff --git "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_wgf.fli" "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_wgf.fli"
index 35c31f4..58a394a 100644
--- "a/C:\\GIT\\ctp\\CTP-og\\ctp_data\\default\\aidata\\set_wgf.fli"
+++ "b/C:\\GIT\\ctp\\CTP-AAIP\\ctp_data\\default\\aidata\\set_wgf.fli"
@@ -21,11 +21,11 @@ if(prod_growth_gold_deficit_set_wgf) // 2
 	feed_ave_wgf_food
 }
 
-if(growth_prod_gold_set_wgf) // 3
+if(growth_prod_gold_set_wgf) // 3 used for over 5 cities
 {
-	pay_lots_wgf_gold
+	pay_ave_wgf_gold //	WW from lots
 	work_ave_wgf_production
-	feed_nothing_wgf_food
+	feed_ave_wgf_food //	WW from nothing
 }
 
 if(prod_growth_gold_set_wgf) // 4
@@ -75,18 +75,18 @@ if(dangerously_high_gold_and_wages_cost)
 // up to turn 100; feed 5
 	if( a0to100_turns )
 	{
-		lowest_food_max
+		low_food_max //WW from lowest
 		lowest_food_min
 	}
 
 // between 100 and 200; feed 7.5
 	if( a100to200_turns )
 	{
-		low_food_max
+		average_food_max //WW from low
 		low_food_min
 	}
 
-// after 100 and 200; feed 10
+// between 200 and 300; feed 10
 	if(	a200to300_turns 
 		and not yes_money_crisis)
 	{
```

