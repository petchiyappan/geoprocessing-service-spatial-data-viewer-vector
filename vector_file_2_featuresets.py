__author__ = 'Yogesh'


import arcpy

arcpy.env.overwriteOutput = True

inzip= arcpy.GetParameter(0)
file_type= arcpy.GetParameter(1)

arcpy.SetParameter(2,["String Hi","String Hi"])