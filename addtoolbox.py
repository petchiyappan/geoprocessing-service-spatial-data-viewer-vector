__author__ = 'Yogesh'

import arcpy
from arcpy import AddMessage, AddError
# Import custom toolbox
arcpy.AddToolbox(r'C:\Users\Yogesh\Documents\GitHub\geoprocessing-service-spatial-data-viewer-vector\gp_arcscript1.pyt')

try:
    # Run tool in the custom toolbox.  The tool is identified by
    #  the tool name and the toolbox alias.
    arcpy.Tool(r"C:\Users\Yogesh\Desktop\temp\fells_loop_gpx.zip",'gpx')
    AddMessage('successfully completed')
except arcpy.ExecuteError:
    AddError(arcpy.GetMessages(2))

