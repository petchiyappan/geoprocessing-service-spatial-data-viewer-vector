__author__ = 'Yogesh'

import arcpy
import os


def fc2fcs(workspace):
    """
    Coverts all feature classes inside a workspace into featureset list works for GML, Shapefile
    :param workspace:path of featureclass workspace
    :return:list of featureset objects
    """
    fcs = []
    for dirpath, dirnames, filenames in arcpy.da.Walk(workspace,
                                                      datatype='FeatureClass',
                                                      type='ALL'):
        for filename in filenames:
            arcpy.CopyFeatures_management(os.path.join(dirpath, filename), 'in_memory/temp')
            fc = arcpy.FeatureSet()
            fc.load('in_memory/temp')
            fcs.append(fc)
    return fcs


def get_file_list(workspace, file_ext):
    # http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-with-python
    for root, dirs, files in os.walk(workspace):
        for f in files:
            if f.endswith(file_ext):
                yield os.path.join(root, f)


def gpx2fc(workspace):
    #http://www.topografix.com/gpx.asp
    gpx_files = get_file_list(workspace, '.gpx')
    fcs = []
    for gpx_file in gpx_files:
        arcpy.GPXtoFeatures_conversion(gpx_file, 'in_memory/temp')
        fc = arcpy.FeatureSet()
        fc.load('in_memory/temp')
        fcs.append(fc)
    return fcs

