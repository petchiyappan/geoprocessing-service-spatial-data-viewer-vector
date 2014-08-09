import arcpy
import shutil
import tbx_converter

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "vector file to featureset"
        self.description = "Generate featureset from geospatial vector data"
        self.canRunInBackground = False

    def getParameterInfo(self):
        #Define parameter definitions

        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input Zip",
            name="in_zip_file",
            datatype="File",
            parameterType="Required",
            direction="Input")

        # Second parameter
        param1 = arcpy.Parameter(
            displayName="File Type",
            name="file_type",
            datatype="String",
            parameterType="Required",
            direction="Input")

        param1.filter.type = "ValueList"
        param1.filter.list = ['gml', 'gpx', 'shp', 'gdb', 'mdb', 'sde']
        param1.value = 'gdb'

        # Third parameter
        param2 = arcpy.Parameter(
            displayName="Output Features",
            name="out_features",
            datatype="DEFeatureClass",
            #datatype="GPFeatureLayer",
            #datatype="String",
            parameterType="Optional",
            multiValue="True",
            direction="Output")

        #param2.parameterDependencies = [param0.name]
        #param2.schema.clone = True

        params = [param0, param1, param2]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.env.overwriteOutput = True

        inzip = parameters[0].valueAsText  #r'C:\Users\Yogesh\Desktop\temp\states_21basic.zip'
        file_type = parameters[1].valueAsText

        #is it required
        shutil.rmtree(arcpy.env.scratchFolder)

        tbx_converter.unzip(inzip, arcpy.env.scratchFolder)

        fcs = []
        if file_type == 'shp' or file_type == 'gml':
            fcs = tbx_converter.fc2fcs(arcpy.env.scratchFolder)
        elif file_type == 'gdb' or file_type == 'mdb' or file_type == 'sde':
            #gdbworkspace input eg. c:/temp/temp.gdb
            fcs = tbx_converter.get_geodb(arcpy.env.scratchFolder,file_type)
        elif file_type == 'dwg':
            pass
            #for converting drawing files
        elif file_type == 'dgn':
            pass
        elif file_type == 'dxf':
            pass

        elif file_type == 'geojson':
            pass
            #for converting geojson

        elif file_type == 'topojson':
            pass
        elif file_type == 'kml' or file_type == 'kmz':
            pass

        elif file_type == 'gpx':
            fcs = tbx_converter.gpx2fc(arcpy.env.scratchFolder)
        else:
            messages.AddError("unknown file type")
        messages.AddMessage(fcs[0].JSON[1:100])
        #parameters[2].value = fcs
        arcpy.SetParameter(2,fcs)

        return


