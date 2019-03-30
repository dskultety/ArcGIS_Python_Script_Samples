#-------------------------------------------------------------------------------------
# Name:         Wetland Geodatabse Append v1.3
# Type:         ArcGIS Script Tool
# Purpose:      Adds IDOT wetland delineation project shapefiles to geodatabase
#               containing completed projects. Prior to appending the shapefiles
#               the input shapefiles are checked that they have the correct geometry
#               type and that the required attribute fields are complete.
#
# Author:       Skultety
#
# Created:      03/02/2017
#
# Upgrades:     Version 1.1 (06/13/2017) Modified to add additional messages to let the
#               user know which features were added to the database.
#               Version 1.2 (09/07/2017) Modified to look for Other Surface Waters as
#               a file name for waters sites.
#               Version 1.3 (03/09/2018) Modified to also accept file geodatabase as
#               an input file source. Disabled 'waters' as a viable name for other
#               surface water feature classes
#-------------------------------------------------------------------------------------

# Import system modules
import arcpy
import os
import sys

# Get tool inputs from Arc interface
arcpy.env.workspace = arcpy.GetParameterAsText(0)
outDirectory = arcpy.GetParameterAsText(1)

### Check data before adding
# Check if project boundary is a polygon
fcList = arcpy.ListFeatureClasses("Project*", "POLYGON")
if fcList == []:
    arcpy.AddError("Project boundary is not a polygon")
    sys.exit()
else:
    del fcList

# Check if attribute tables are complete
# Define function to check for feature class
def FieldExist(featureclass, fieldname):
    fieldList = arcpy.ListFields(featureclass, fieldname)
    fieldCount = len(fieldList)
    if (fieldCount == 1):
        return True
    else:
        return False

# Define function to check if field has values
# Indexing procedure has slight difference for shapefiles vs. geodatabase
# Get description of arcpy.env.workspace
desc = arcpy.Describe(arcpy.env.workspace)
# If workspace is folder of shapefiles use this method
if desc.workspaceType == 'FileSystem':
    def FieldComplete(featureclass, fieldname):
        x = 0
        with arcpy.da.SearchCursor(featureclass, ("FID", fieldname)) as cursor:
            for row in cursor:
                if (row[1] is None):
                    x += 1
                elif (row[1] == 0):
                    x += 1
                elif (row[1] == ""):
                    x += 1
        if x > 0:
            return False
        else:
            return True

# Else the geodatabase method will be used
else:
    def FieldComplete(featureclass, fieldname):
        x = 0
        with arcpy.da.SearchCursor(featureclass, ("OBJECTID", fieldname)) as cursor:
            for row in cursor:
                if (row[1] is None):
                    x += 1
                elif (row[1] == 0):
                    x += 1
                elif (row[1] == ""):
                    x += 1
        if x > 0:
            return False
        else:
            return True

# Check all features for sequence number and PID
fcList = arcpy.ListFeatureClasses()

for myFeatureClass in fcList:
    if (not FieldExist(myFeatureClass, "PID")):
        arcpy.AddError("Field 'PID' does not exist in " + myFeatureClass)
        sys.exit()
for myFeatureClass in fcList:
    if (not FieldComplete(myFeatureClass, "PID")):
        arcpy.AddError("At least one feature in " + myFeatureClass + " is missing a value in the 'PID' field.")
        sys.exit()

for myFeatureClass in fcList:
    if (not FieldExist(myFeatureClass, "Seq_Num")):
        arcpy.AddError("Field 'Seq_Num' does not exist in " + myFeatureClass)
        sys.exit()
for myFeatureClass in fcList:
    if (not FieldComplete(myFeatureClass, "Seq_Num")):
        arcpy.AddError("At least one feature in " + myFeatureClass + " is missing a value in the 'Seq_Num' field.")
        sys.exit()
del fcList

# Check for 'Site', 'Point' and 'Transect'
fcList = arcpy.ListFeatureClasses("Wetland*")
for myFeatureClass in fcList:
    if (not FieldExist(myFeatureClass, "Site")):
        arcpy.AddError("Field 'Site' does not exist in " + myFeatureClass)
        sys.exit()
for myFeatureClass in fcList:
    if (not FieldComplete(myFeatureClass, "Site")):
        arcpy.AddError("At least one feature in " + myFeatureClass + " is missing a value in the 'Site' field.")
        sys.exit()
del fcList

fcList = arcpy.ListFeatureClasses("Non*")
for myFeatureClass in fcList:
    if (not FieldExist(myFeatureClass, "Site")):
        arcpy.AddError("Field 'Site' does not exist in " + myFeatureClass)
        sys.exit()
for myFeatureClass in fcList:
    if (not FieldComplete(myFeatureClass, "Site")):
        arcpy.AddError("At least one feature in " + myFeatureClass + " is missing a value in the 'Site' field.")
        sys.exit()
del fcList

# fcList = arcpy.ListFeatureClasses("Water*")
# for myFeatureClass in fcList:
#     if (not FieldExist(myFeatureClass, "Site")):
#         arcpy.AddError("Field 'Site' does not exist in " + myFeatureClass)
#         sys.exit()
# for myFeatureClass in fcList:
#     if (not FieldComplete(myFeatureClass, "Site")):
#         arcpy.AddError("At least one feature in " + myFeatureClass + " is missing a value in the 'Site' field.")
#         sys.exit()
# del fcList

fcList = arcpy.ListFeatureClasses("Other*")
for myFeatureClass in fcList:
    if (not FieldExist(myFeatureClass, "Site")):
        arcpy.AddError("Field 'Site' does not exist in " + myFeatureClass)
        sys.exit()
for myFeatureClass in fcList:
    if (not FieldComplete(myFeatureClass, "Site")):
        arcpy.AddError("At least one feature in " + myFeatureClass + " is missing a value in the 'Site' field.")
        sys.exit()
del fcList

fcList = arcpy.ListFeatureClasses("Sampling*")
for myFeatureClass in fcList:
    if (not FieldExist(myFeatureClass, "Point")):
        arcpy.AddError("Field 'Point' does not exist in " + myFeatureClass)
        sys.exit()
for myFeatureClass in fcList:
    if (not FieldComplete(myFeatureClass, "Point")):
        arcpy.AddError("At least one feature in " + myFeatureClass + " is missing a value in the 'Point' field.")
        sys.exit()
del fcList


## Add features to geodatabase
# Add project boundary to geodatabase
try:
    # Set output feature class to append to
    outLocation = os.path.join(outDirectory, "IDOT_Wetlands.INHS_IDOT.Project_Boundaries")
    # Get list of project boundary feature classes
    fcList = arcpy.ListFeatureClasses("Project*", "POLYGON")
    # Process: Append the feature classes into the empty feature class
    arcpy.Append_management(fcList, outLocation, schema_type="NO_TEST")
    # Add message to user
    arcpy.AddMessage("Project boundary was added to the geodatabase")
    # Delete variables
    del(outLocation)

except:
    arcpy.AddWarning("Project Boundary was not added to geodatabase")

# Add wetland sites to geodatabase
try:
    # Set output feature class to append to
    outLocation = os.path.join(outDirectory, "IDOT_Wetlands.INHS_IDOT.Wetland_Sites")
    # Get list of project boundary feature classes
    fcList = arcpy.ListFeatureClasses("Wetland*", "POLYGON")
    # Process: Append the feature classes into the empty feature class
    arcpy.Append_management(fcList, outLocation, "NO_TEST")
    # Add message to user
    arcpy.AddMessage("Wetland Sites were added to the geodatabase")
    # Delete variables
    del (outLocation)

except:
    arcpy.AddWarning("Wetland Sites were not added to geodatabase")

# Add wetland sites lines to geodatabase
try:
    # Set output feature class to append to
    outLocation = os.path.join(outDirectory, "IDOT_Wetlands.INHS_IDOT.Wetland_Sites_Line")
    # Get list of project boundary feature classes
    fcList = arcpy.ListFeatureClasses("Wetland*", "LINE")
    # Process: Append the feature classes into the empty feature class
    arcpy.Append_management(fcList, outLocation, "NO_TEST")
    # Add message to user
    arcpy.AddMessage("Wetland Sites lines were added to the geodatabase")
    # Delete variables
    del (outLocation)

except:
    arcpy.AddWarning("Wetland Sites lines were not added to geodatabase")

# Add non wetland determination sites to geodatabase
try:
    # Set output feature class to append to
    outLocation = os.path.join(outDirectory, "IDOT_Wetlands.INHS_IDOT.Non_Wetland_NWI_Sites")
    # Get list of project boundary feature classes
    fcList = arcpy.ListFeatureClasses("Non*", "POINT")
    # Process: Append the feature classes into the empty feature class
    arcpy.Append_management(fcList, outLocation, "NO_TEST")
    # Add message to user
    arcpy.AddMessage("Non Wetland Determination Sites were added to the geodatabase")
    # Delete variables
    del (outLocation)

except:
    arcpy.AddWarning("Non Wetland Determination Sites were not added to geodatabase")

# Add sampling points to geodatabase
try:
    # Set output feature class to append to
    outLocation = os.path.join(outDirectory, "IDOT_Wetlands.INHS_IDOT.Sampling_Points")
    # Get list of project boundary feature classes
    fcList = arcpy.ListFeatureClasses("Sampling*", "POINT")
    # Process: Append the feature classes into the empty feature class
    arcpy.Append_management(fcList, outLocation, "NO_TEST")
    # Add message to user
    arcpy.AddMessage("Sampling Points were added to the geodatabase")
    # Delete variables
    del (outLocation)

except:
    arcpy.AddWarning("Sampling Points were not added to geodatabase")

# Add waters sites (polygon) to geodatabase
# try:
#     # Set output feature class to append to
#     outLocation = os.path.join(outDirectory, "IDOT_Wetlands.INHS_IDOT.Waters_poly")
#     # Get list of project boundary feature classes
#     fcList = arcpy.ListFeatureClasses("Water*", "POLYGON")
#     # Process: Append the feature classes into the empty feature class
#     arcpy.Append_management(fcList, outLocation, "NO_TEST")
#     # Add message to user
#     arcpy.AddMessage("Water Sites (polygon) were added to the geodatabase")
#     # Delete variables
#     del (outLocation)
#
# except:
#     arcpy.AddWarning("Waters Sites (polygon) were not added to geodatabase")
#
# # Add waters sites (lines) to geodatabase
# try:
#     # Set output feature class to append to
#     outLocation = os.path.join(outDirectory, "IDOT_Wetlands.INHS_IDOT.Waters_line")
#     # Get list of project boundary feature classes
#     fcList = arcpy.ListFeatureClasses("Water*", "LINE")
#     # Process: Append the feature classes into the empty feature class
#     arcpy.Append_management(fcList, outLocation, "NO_TEST")
#     # Add message to user
#     arcpy.AddMessage("Water Sites (lines) were added to the geodatabase")
#     # Delete variables
#     del (outLocation)
#
# except:
#     arcpy.AddWarning("Waters Sites (lines) were not added to geodatabase")

# Add other surface waters(polygon) to geodatabase
try:
    # Set output feature class to append to
    outLocation = os.path.join(outDirectory, "IDOT_Wetlands.INHS_IDOT.Waters_poly")
    # Get list of project boundary feature classes
    fcList = arcpy.ListFeatureClasses("Other*", "POLYGON")
    # Process: Append the feature classes into the empty feature class
    arcpy.Append_management(fcList, outLocation, "NO_TEST")
    # Add message to user
    arcpy.AddMessage("Other Surface Waters (polygon) were added to the geodatabase")
    # Delete variables
    del (outLocation)

except:
    arcpy.AddWarning("Other Surface Waterss (polygon) were not added to geodatabase")

# Add other surface waters (lines) to geodatabase
try:
    # Set output feature class to append to
    outLocation = os.path.join(outDirectory, "IDOT_Wetlands.INHS_IDOT.Waters_line")
    # Get list of project boundary feature classes
    fcList = arcpy.ListFeatureClasses("Other*", "LINE")
    # Process: Append the feature classes into the empty feature class
    arcpy.Append_management(fcList, outLocation, "NO_TEST")
    # Add message to user
    arcpy.AddMessage("Other Surface Waters (lines) were added to the geodatabase")
    # Delete variables
    del (outLocation)

except:
    arcpy.AddWarning("Other Surface Waters (lines) were not added to geodatabase")

# Add transects to geodatabase
try:
    # Set output feature class to append to
    outLocation = os.path.join(outDirectory, "IDOT_Wetlands.INHS_IDOT.Transects")
    # Get list of project boundary feature classes
    fcList = arcpy.ListFeatureClasses("Transect*", "LINE")
    # Process: Append the feature classes into the empty feature class
    arcpy.Append_management(fcList, outLocation, "NO_TEST")
    # Add message to user
    arcpy.AddMessage("Transects were added to the geodatabase")
    # Delete variables
    del (outLocation)

except:
    arcpy.AddWarning("Transects were not added to geodatabase")

# Refresh map view
arcpy.RefreshActiveView()
