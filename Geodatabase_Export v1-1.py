#-------------------------------------------------------------------------------------
# Name:         Geodatabse Export v1.1
# Type:         ArcGIS Script Tool
# Purpose:      Exports IDOT wetland delineation project boundaries and wetland sites
#               from the geodatabase to a file geodatabase so the laters can have
#               additional tables joined.
#
# Author:       Skultety
#
# Created:      02/22/2018
# Updated:      03/07/2018
#
# Upgrades:     v1.1 - Includes BMP project boundaries in export
#-------------------------------------------------------------------------------------

# Import modules
import arcpy
import os
import sys

# Get tool inputs from ArcMap tool dialog
workspace1 = arcpy.GetParameterAsText(0)
workspace2 = arcpy.GetParameterAsText(1)
workspace3 = arcpy.GetParameterAsText(2)
outDirectory = arcpy.GetParameterAsText(3)
gdbName = arcpy.GetParameterAsText(4)

# Create new file geodatabase
try:
    gdbName = gdbName + ".gdb"
    arcpy.CreateFileGDB_management(outDirectory, gdbName)
    outGDB = os.path.join(outDirectory, gdbName)
except:
    arcpy.AddError("File geodatabase could not be created.")
    sys.exit()

# Copy features from IDOT Delineations
try:
    arcpy.env.workspace = workspace1
    outFeatureClass = os.path.join(outGDB, arcpy.ListFeatureClasses("IDOT_Wetlands.INHS_IDOT.Project_Boundaries")[0])
    arcpy.CopyFeatures_management(arcpy.ListFeatureClasses("IDOT_Wetlands.INHS_IDOT.Project_Boundaries")[0], outFeatureClass)
    outFeatureClass = os.path.join(outGDB, arcpy.ListFeatureClasses("IDOT_Wetlands.INHS_IDOT.Wetland_Sites")[0])
    arcpy.CopyFeatures_management(arcpy.ListFeatureClasses("IDOT_Wetlands.INHS_IDOT.Wetland_Sites")[0], outFeatureClass)
except:
    arcpy.AddError("Features from IDOT Delineations could not be exported")
    sys.exit()

# Copy features from IDOT Delineations Pre GPS
try:
    arcpy.env.workspace = workspace2
    outFeatureClass = os.path.join(outGDB, arcpy.ListFeatureClasses("IDOT_Wetlands.INHS_IDOT.Project_Boundaries_Drawn")[0])
    arcpy.CopyFeatures_management(arcpy.ListFeatureClasses("IDOT_Wetlands.INHS_IDOT.Project_Boundaries_Drawn")[0], outFeatureClass)
    outFeatureClass = os.path.join(outGDB, arcpy.ListFeatureClasses("IDOT_Wetlands.INHS_IDOT.Wetland_Point")[0])
    arcpy.CopyFeatures_management(arcpy.ListFeatureClasses("IDOT_Wetlands.INHS_IDOT.Wetland_Point")[0], outFeatureClass)
except:
    arcpy.AddError("Features from IDOT Delineations Pre GPS could not be exported")
    sys.exit()

# Copy features from IDOT BMPs
try:
    arcpy.env.workspace = workspace3
    outFeatureClass = os.path.join(outGDB, arcpy.ListFeatureClasses("IDOT_Wetlands.INHS_IDOT.BMP_Project_Boundaries")[0])
    arcpy.CopyFeatures_management(arcpy.ListFeatureClasses("IDOT_Wetlands.INHS_IDOT.BMP_Project_Boundaries")[0], outFeatureClass)

except:
    arcpy.AddError("Features from IDOT BMPs could not be exported")
    sys.exit()
