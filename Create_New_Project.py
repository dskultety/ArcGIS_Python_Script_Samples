#-------------------------------------------------------------------------------------
# Name:         Create New Project 2017 v2.2.1
# Type:         ArcGIS Script Tool
# Purpose:      Creates folder and files for new wetland delineation GIS project.
#               Uses input county name to determine if project is in IL State Plane
#               zone East or West and if project is in an IDOT District 1 county.
#               State plane zone and District 1 status are used to determine which
#               files should be written.
#
# Author:       Skultety
#
# Created:      04/24/2012
# Updated:      03/07/2018
#
# Upgrades:     Version 1.1 was upgraded from version 1.0 to create subfolders in
#               Shapefiles Final folder for shapefiles and dgn files. Names of
#               subfolders is based on the state plane zone of the input county.
#
#               Version 2.0 tool revised to change folder structure and eliminate
#               author folder.
#               Version 2.1 adds a project size selection of Small or Large, if Large
#               is selected than an overview map is created.
#               Version 2.2 replaces in progress folder with file geodatabase.
#               Version 2.2.1 adds in progress folder back into script.
#               Version 2.3 uses a user specified location where the project should
#               be created, replaces in progress folder with a file geodatabase, and
#               uses mxd templates that are locared on the network. 
#-------------------------------------------------------------------------------------

# Import modules
import arcpy
import os
import sys

# USER INPUTS FOR TOOL
# Use script tool interface to get user generated inputs
# Uses Arc Get Parameter as Text to get raw input of project directory
projectDirectory = arcpy.GetParameterAsText(0)
# Uses Arc Get Parameter as Text to get raw input of project name
projectName = arcpy.GetParameterAsText(1)
projectName = "\\" + projectName
# Uses Arc Get Parameter as Text to get raw input of project county
# This parameter is case sensitive!
# The next step will stop the script if entered county name is not in lists
projectCounty = arcpy.GetParameterAsText(2)
# Uses Arc Get Parameter as Text to get raw input of project size
projectSize = arcpy.GetParameterAsText(3)

# DETERMINE STATE PLANE ZONE PROJECT IS IN BY COUNTY NAME
# Selects map template to use
# Counties in State Plane East Zone
countyListEast = ("Boone","Champaign","Clark","Clay","Coles","Cook","Crawford","Cumberland","Dekalb","De Kalb","DeKalb","Dewitt","De Witt","DeWitt","Douglas",\
"Dupage","DuPage","Du Page","Edgar","Edwards","Effingham","Fayette","Ford","Franklin","Gallatin","Grundy","Hamilton","Hardin","Iroquois","Jasper","Jefferson",\
"Johnson","Kane","Kankakee","Kendall","Lake","Lasalle","La Salle","LaSalle","Lawrence","Livingston","Macon","Marion","Massac","Mchenry","Mc Henry","McHenry",\
"Mclean","Mc Lean","McLean","Moultrie","Piatt","Pope","Richland","Saline","Shelby","Vermilion","Wabash","Wayne","White","Will","Williamson")
# Counties in State Plane West Zone
countyListWest = ("Adams","Alexander","Bond","Brown","Bureau","Calhoun","Carroll","Cass","Christian","Clinton","Fulton","Greene","Hancock","Henderson","Henry",\
"Jackson","Jersey","Jo Daviess","JoDaviess","Jodaviess","Knox","Lee","Logan","Macoupin","Madison","Marshall","Mason","Mcdonough","McDonough","Mc Donough","Menard",\
"Mercer","Monroe","Montgomery","Morgan","Ogle","Peoria","Perry","Pike","Pulaski","Putnam","Randolph","Rock Island","Sangamon","Schuyler","Scott","St. Clair","St.Clair",\
"Saint Clair","Stark","Stephenson","Tazewell","Union","Warren","Washington","Whiteside","Winnebago","Woodford")

# Check if project county is in state plane zone East
if projectCounty in countyListEast:
    # Selects mxd template file East
    mxd = arcpy.mapping.MapDocument(r"redacted_path\StPl_IL_East_Blank.mxd")
# If project county was not in state plane zone East then check if zone West
elif projectCounty in countyListWest:
    # Selects mxd template file West
    mxd = arcpy.mapping.MapDocument(r"redacted_path\StPl_IL_West_Blank.mxd")
    # If project county not in east or west list then script will stop and error message will be generated
else:
    arcpy.AddError("Error - County Not In List")
    arcpy.AddError("Check spelling & capitalization of county name")
    arcpy.AddError("Tool stopped, project not created")
    sys.exit()

# MAKE NEW DIRECTORY
# Makes folder within designated project directory with given project name
os.mkdir(projectDirectory + projectName)
# Creates subfolders within above created project folder
os.mkdir(projectDirectory + projectName + "\\GNSS")
os.mkdir(projectDirectory + projectName + "\\PDF")
os.mkdir(projectDirectory + projectName + "\\Notes")
os.mkdir(projectDirectory + projectName + "\\Files from IDOT")
os.mkdir(projectDirectory + projectName + "\\GIS Files Final")
arcpy.CreateFileGDB_management(projectDirectory + projectName, "In_Progress.gdb")

# Creates subfolders with "GIS Files Final" folder, folder names are based upon state plane zone.
# Check if project county is in state pLane zone East
if projectCounty in countyListEast:
    os.mkdir(projectDirectory + projectName + "\\GIS Files Final\\Shapefiles_IL_StPL_East_NAD83")
    os.mkdir(projectDirectory + projectName + "\\GIS Files Final\\DGN_files_IL_StPL_East_NAD83")
# If project county was not in state pLane zone East then check if zone West
elif projectCounty in countyListWest:
    os.mkdir(projectDirectory + projectName + "\\GIS Files Final\\Shapefiles_IL_StPL_West_NAD83")
    os.mkdir(projectDirectory + projectName + "\\GIS Files Final\\DGN_files_IL_StPL_West_NAD83")


# CREATE INDIVIDUAL MXD FILES BASED ON COUNTY
# Output directory to write files to
outputDirectory = projectDirectory + projectName
# District 1 county lists
# List of counties in District 1 with ADID or county inventory maps
countyListDistrict1ADID = ("DuPage", "Du Page", "Dupage", "Kane", "Lake", "McHenry", "Mc Henry", "Mchenry")
# List of counties in District 1 without ADID or county inventory maps
countyListDistrict1NoADID = ("Cook", "Will")

if projectSize == "Small":
    if projectCounty in countyListDistrict1ADID:
        # Save a copy as Figure 1 Project Location Map
        mxd.saveACopy(outputDirectory + "\\Fig1_Project_Location.mxd")
        # Save a copy as Figure 2 NWI
        mxd.saveACopy(outputDirectory + "\\Fig2_NWI.mxd")
        # Save a copy as Figure 3 ADID Map
        mxd.saveACopy(outputDirectory + "\\Fig3_ADID.mxd")
        # Save a copy as Figure 4 Soils
        mxd.saveACopy(outputDirectory + "\\Fig4_Soils.mxd")
        # Save a copy as Figure 5 Determination Map
        mxd.saveACopy(outputDirectory + "\\Fig5_Determination_Map.mxd")

    elif projectCounty in countyListDistrict1NoADID:
        # Save a copy as Figure 1 Project Location Map
        mxd.saveACopy(outputDirectory + "\\Fig1_Project_Location.mxd")
        # Save a copy as Figure 2 NWI
        mxd.saveACopy(outputDirectory + "\\Fig2_NWI.mxd")
        # Save a copy as Figure 3 Soils
        mxd.saveACopy(outputDirectory + "\\Fig3_Soils.mxd")
        # Save a copy as Figure 4 Determination Map
        mxd.saveACopy(outputDirectory + "\\Fig4_Determination_Map.mxd")

    else:
        # Save a copy as Figure 1 Project Location Map
        mxd.saveACopy(outputDirectory + "\\Fig1_Project_Location.mxd")
        # Save a copy as Figure 2 NWI
        mxd.saveACopy(outputDirectory + "\\Fig2_NWI.mxd")
        # Save a copy as Figure 3 Wetland Determination Map
        mxd.saveACopy(outputDirectory + "\\Fig3_Determination_Map.mxd")

elif projectSize == "Large":
    if projectCounty in countyListDistrict1ADID:
        # Save a copy as Figure 1 Project Location Map
        mxd.saveACopy(outputDirectory + "\\Fig1_Project_Location.mxd")
        # Save a copy as Figure 2 NWI
        mxd.saveACopy(outputDirectory + "\\Fig2_NWI.mxd")
        # Save a copy as Figure 3 ADID Map
        mxd.saveACopy(outputDirectory + "\\Fig3_ADID.mxd")
        # Save a copy as Figure 4 Soils
        mxd.saveACopy(outputDirectory + "\\Fig4_Soils.mxd")
        # Save a copy as Figure 5 Determination Overview Map
        mxd.saveACopy(outputDirectory + "\\Fig5_Overview_Map.mxd")
        # Save a copy as Figure 6 Determination Map
        mxd.saveACopy(outputDirectory + "\\Fig6_Determination_Map.mxd")

    elif projectCounty in countyListDistrict1NoADID:
        # Save a copy as Figure 1 Project Location Map
        mxd.saveACopy(outputDirectory + "\\Fig1_Project_Location.mxd")
        # Save a copy as Figure 2 NWI
        mxd.saveACopy(outputDirectory + "\\Fig2_NWI.mxd")
        # Save a copy as Figure 3 Soils
        mxd.saveACopy(outputDirectory + "\\Fig3_Soils.mxd")
        # Save a copy as Figure 4 Determination Overview Map
        mxd.saveACopy(outputDirectory + "\\Fig4_Overview_Map.mxd")
        # Save a copy as Figure 4 Determination Map
        mxd.saveACopy(outputDirectory + "\\Fig5_Determination_Map.mxd")

    else:
        # Save a copy as Figure 1 Project Location Map
        mxd.saveACopy(outputDirectory + "\\Fig1_Project_Location.mxd")
        # Save a copy as Figure 2 NWI
        mxd.saveACopy(outputDirectory + "\\Fig2_NWI.mxd")
        # Save a copy as Figure 3 Determination Overview Map
        mxd.saveACopy(outputDirectory + "\\Fig3_Overview_Map.mxd")
        # Save a copy as Figure 4 Wetland Determination Map
        mxd.saveACopy(outputDirectory + "\\Fig4_Determination_Map.mxd")

del mxd, projectCounty, projectDirectory, projectName
