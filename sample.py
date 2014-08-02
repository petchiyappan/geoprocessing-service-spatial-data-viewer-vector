__author__ = 'Yogesh'


import arcpy
import os

# Function to unzipping the contents of the zip file
#
def unzip(source_filename, dest_dir):
    import zipfile,os.path
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


arcpy.env.overwriteOutput = True

inzip= r'C:\Users\Yogesh\Desktop\temp\states_21basic.zip'
file_type = 'shapefile'
print (inzip)
sc=r'C:\Users\Yogesh\Documents\ArcGIS\scratch'
print (sc)

unzip(inzip,sc)

workspace = sc


fcs=[]
for dirpath, dirnames, filenames in arcpy.da.Walk(workspace,
                                                  datatype="FeatureClass",
                                                  type="ALL"):
    for filename in filenames:
        arcpy.CopyFeatures_management(os.path.join(dirpath, filename),"in_memory/temp")
        fc=arcpy.FeatureSet()
        fc.load("in_memory/temp")
        print fc.JSON[1:300]
        fcs.append(fc)

arcpy.SetParameter(2,fcs)