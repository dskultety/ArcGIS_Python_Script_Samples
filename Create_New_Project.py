#-------------------------------------------------------------------------------------
# Name:         Create_New_Project.py
# Type:         ArcGIS Script Tool for ArcGIS Desktop
# Purpose:      Creates folder and files for new wetland delineation GIS project.
#               Uses input county name to determine appropriate projection for county
#				(either IL State Plane zone East or West) and to determine if project 
#				is in an IDOT District 1 county (requires additional maps).
#               State plane zone and District 1 status are used to determine which
#               files should be written.
#
# Usage:		This code is provided as an example only. Usage of this code requires
#				replacing all file paths and templates with your own.
#
# Author:       Skultety
#
# Created:      04/24/2012
# Updated:      01/20/2016
# Copyright:    (c) Skultety 2016
#
#-------------------------------------------------------------------------------------

# Import modules
import arcpy
import os
import sys


# USER INPUTS FOR TOOL
# Use script tool interface to get user generated inputs
# Uses Arc Get Parameter as Text to get raw input of persons name
projectPerson = arcpy.GetParameterAsText(0)
# Uses Arc Get Parameter as Text to get raw input of project name
projectName = arcpy.GetParameterAsText(1)
# Uses Arc Get Parameter as Text to get raw input of project county
# This parameter is case sensitive!
# The next step will stop the script if entered county name is not in lists
projectCounty = arcpy.GetParameterAsText(2)


# DETERMINE STATE PLANE ZONE PROJECT IS IN BY COUNTY NAME
# Selects map template to use
# Lists include all counties in Illinois
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

# Check if project county is in state pLane zone East
if projectCounty in countyListEast:
    # Selects mxd template file East
    mxd = arcpy.mapping.MapDocument(r"D:\GIS Tools\Map Templates\StPl_IL_East_Blank.mxd")
# If project county was not in state pLane zone East then check if zone West
elif projectCounty in countyListWest:
    # Selects mxd template file West
    mxd = arcpy.mapping.MapDocument(r"D:\GIS Tools\Map Templates\StPl_IL_West_Blank.mxd")
    # If project county not in east or west list then script will stop and error message will be generated
else:
    arcpy.AddError("Error - County Not In List")
    arcpy.AddError("Check spelling & capitalization of county name")
    arcpy.AddError("Tool stopped, project not created")
    sys.exit()

# Check if project person is in person list
# Need to insert names in personList to make code usable
personList = ("name_person_1","name_person_2")
if projectPerson not in personList:
    arcpy.AddError("Error - Person Not In List")
    arcpy.AddError("Check spelling & capitalization of author's name")
    arcpy.AddError("Tool stopped, project not created")
    sys.exit()

# MAKE NEW DIRECTORY
# Sets project directory
projectDirectory = "W:\\spatial\\wetlands\\gis\\2016\\"

if not os.path.isdir(projectDirectory + projectPerson):
    os.mkdir(projectDirectory + projectPerson)

# Makes folder within 2016 projects within persons name with given project name
os.mkdir(projectDirectory + projectPerson + "\\" + projectName)
# Creates subfolders within above created project folder
os.mkdir(projectDirectory + projectPerson + "\\" + projectName + "\\GPS")
os.mkdir(projectDirectory + projectPerson + "\\" + projectName + "\\PDF")
os.mkdir(projectDirectory + projectPerson + "\\" + projectName + "\\Notes")
os.mkdir(projectDirectory + projectPerson + "\\" + projectName + "\\Files from Others")
os.mkdir(projectDirectory + projectPerson + "\\" + projectName + "\\Shapefiles Final")
os.mkdir(projectDirectory + projectPerson + "\\" + projectName + "\\Shapefiles in progress")
#os.mkdir(projectDirectory + projectPerson + "\\" + projectName + "\\Shapefiles in progress\\scratch")
# Creates subfolders with "Shapefile Final" folder, folder names are based upon state plane zone.
# Check if project county is in state pLane zone East
if projectCounty in countyListEast:
    os.mkdir(projectDirectory + projectPerson + "\\" + projectName + "\\Shapefiles Final\\Shapefiles_IL_StPL_East_NAD83")
    os.mkdir(projectDirectory + projectPerson + "\\" + projectName + "\\Shapefiles Final\\DGN_files_IL_StPL_East_NAD83")
# If project county was not in state pLane zone East then check if zone West
elif projectCounty in countyListWest:
    os.mkdir(projectDirectory + projectPerson + "\\" + projectName + "\\Shapefiles Final\\Shapefiles_IL_StPL_West_NAD83")
    os.mkdir(projectDirectory + projectPerson + "\\" + projectName + "\\Shapefiles Final\\DGN_files_IL_StPL_West_NAD83")


# CREATE INDIVIDUAL MXD FILES BASED ON COUNTY
# Output directory to write files to
outputDirectory = projectDirectory + projectPerson + "\\" + projectName
# District 1 county lists
# List of counties in District 1 with ADID or county inventory maps
countyListDistrict1ADID = ("DuPage", "Du Page", "Dupage", "Kane", "Lake", "McHenry", "Mc Henry", "Mchenry")
# List of counties in District 1 without ADID or county inventory maps
countyListDistrict1NoADID = ("Cook", "Will")

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

del mxd, projectCounty, projectDirectory, projectName, projectPerson
