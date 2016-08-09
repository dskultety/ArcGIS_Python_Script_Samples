#-------------------------------------------------------------------------------
# Name:        	Change_Map_Date_and_Export.py
# Type:        	ArcGIS Script Tool for ArcGIS Desktop
# Purpose:     	Loops through all mxd files in a folder and first changes the date
#              	field to an input value specified in the tool dialogue box and then
#              	exports the maps to pdf.
#              	Version 1.1 - Checks if folder called "pdf" exists within the
#              	workspace, previous version would fail if folder did not exist.
#              	If folder does not exist it will be created before exporting maps.
#
# Usage:		This code is provided as an example only. Usage of this code requires
#				map layouts with a text layout element named "Date" to be modified
#				by this code.
#
# Author:      	Skultety
#
# Created:     	09/18/2012
# Updated:      01/20/2016
# Copyright:   	(c) Skultety 2016
#-------------------------------------------------------------------------------

#Import modules
import arcpy
import os

#Get parameters
#Project workspace is folder
projectWorkspace = arcpy.GetParameterAsText(0)
#Date is text string
newDate = arcpy.GetParameterAsText(1)

#Set enviroment variables
arcpy.env.workspace = projectWorkspace

#Loops through mxd files
for filename in os.listdir(projectWorkspace):
    fullpath = os.path.join(projectWorkspace, filename)
    if os.path.isfile(fullpath):
        if filename.lower().endswith(".mxd"):

            mxd = arcpy.mapping.MapDocument(fullpath)
            #Gets the mxd file name to use in the pdf name
            mxdName = filename[:-4]

            #Change Date
            try:
                #Select DATE element in map layout.
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    if elm.name == "Date":
                        #Replace text
                        elm.text = newDate

                #Save MXD
                mxd.save()

            except:
                arcpy.AddError("Step 1 FAILED!")

            #Export Map
            if os.path.isdir(projectWorkspace + "\\PDF"):
                try:
                    #Determine if mxd has data driven pages
                    if hasattr (mxd, 'dataDrivenPages'):
                        #If it has data driven pages will export all pages
                        mxd.dataDrivenPages.exportToPDF(projectWorkspace + "\\PDF\\" + mxdName,"ALL")
                    #Else export map
                    else:
                        arcpy.mapping.ExportToPDF(mxd, projectWorkspace + "\\PDF\\" + mxdName)

                except:
                    arcpy.AddError("Step 2 FAILED!")

            else:
                try:
                    os.mkdir(projectWorkspace + "\\PDF")
                    #Determine if mxd has data driven pages
                    if hasattr (mxd, 'dataDrivenPages'):
                        #If it has data driven pages will export all pages
                        mxd.dataDrivenPages.exportToPDF(projectWorkspace + "\\PDF\\" + mxdName,"ALL")
                    #Else export map
                    else:
                        arcpy.mapping.ExportToPDF(mxd, projectWorkspace + "\\PDF\\" + mxdName)

                except:
                    arcpy.AddError("Step 2 FAILED!")

#Delete variables from entire tool
del projectWorkspace, newDate