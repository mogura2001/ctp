///////////////////////////////////////////////////////////////////////////////
// 
// AIPDef.h
//
// Contains structure definitions and constants for the supplemental build
// lists in Civ3
//
// by The Mad Dr. I
//
///////////////////////////////////////////////////////////////////////////////




///////////////////////////////////////////////////////////////////////////////
//
// Build_List_Class
// -------------------
// Specifies a list of unit types, from which we should try to build one
struct Build_List_Class
{
	char class_name[80];				// The names of the build list
	double priority;					// How important to build form this list
};

#define UNLIMITED -999999

#define YES 1
#define NO 0

#define MAX_BUILD_LISTS 200

///////////////////////////////////////////////////////////////////////////////
//
// Build_List_Element
// 
// Specifies a type in a build list
struct Build_List_Element
{
	char unit_type_name[80];			// The names of a unit type
	double units_per_city;				// How many of this type per city
};


///////////////////////////////////////////////////////////////////////////////
//
// Building_Build_List_Element
// 
// Specifies a type in a build list
struct Building_Build_List_Element
{
	char building_name[80];			// The names of a unit type
	double priority;				// How many of this type per city
};


#define MAX_ELEMENTS 200


///////////////////////////////////////////////////////////////////////////////
//
// Advancement_Element
// 
// Specifies a type in a list of advancements
struct Advancement_Element
{
	char advancement_name[80];			// The names of a unit type
};


/*

  This stuff is not used yet in Civ

#define NUMBER_TO_HAVE 0
#define NUMBER_TO_BUILD 1
#define RATIO_TO_BUILD 2
#define RATIO_TO_HAVE 3

*/






