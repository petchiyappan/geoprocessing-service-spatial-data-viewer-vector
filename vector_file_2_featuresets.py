from arcpy import AddMessage,AddError

__author__ = 'Yogesh'


import arcpy
import zipfile
import os.path
import shutil
import utilities


# Function to unzipping the contents of the zip file
#
def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)

def main():
    arcpy.env.overwriteOutput = True

    inzip = arcpy.GetParameterAsText(0)  #r'C:\Users\Yogesh\Desktop\temp\states_21basic.zip'
    file_type= arcpy.GetParameterAsText(1)

    #is it required
    shutil.rmtree(arcpy.env.scratchFolder)

    unzip(inzip,arcpy.env.scratchFolder)

    fcs = []
    if file_type == 'shp' or file_type == 'gml':
        fcs = utilities.fc2fcs(arcpy.env.scratchFolder)
    elif file_type == 'gdb' or file_type == 'mdb' or file_type == 'sde':
        #gdbworkspace input eg. c:/temp/temp.gdb
        fcs = utilities.get_geodb(arcpy.env.scratchFolder,file_type)
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
        fcs = utilities.gpx2fc(arcpy.env.scratchFolder)
    else:
        AddError("unknown file type")

    arcpy.SetParameter(2,fcs)

if __name__ == "__main__":
    main()