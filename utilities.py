__author__ = 'Yogesh'

import arcpy
from arcpy import arcpy, AddMessage
import os

def get_fc_list_rec(workspace):
    for dir_path, dir_names, file_names in arcpy.da.Walk(workspace,
                                                      datatype = 'FeatureClass',
                                                      type = 'ALL'):
        for filename in file_names:
            yield os.path.join(dir_path, filename)

def load_fc(temp_fc):
    fc = arcpy.FeatureSet()
    fc.load(temp_fc)
    return fc


def fc2fcs(workspace):
    """
    Coverts all feature classes inside a workspace into featureset list works for GML, Shapefile,
    personal geodatabase, file geodatabase, sde geodatabase
    :param workspace:path of featureclass workspace
    :return:list of featureset objects
    """
    fcs = []
    fc_paths = get_fc_list_rec(workspace)
    for filename in fc_paths:
        arcpy.CopyFeatures_management(filename, 'in_memory/temp')
        fcs.append(load_fc('in_memory/temp'))
    return fcs


def get_file_list(workspace, file_ext):
    # http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-with-python
    for root, dirs, files in os.walk(workspace):
        for f in files:
            if f.endswith(file_ext):
                yield os.path.join(root, f)


def gpx2fc(workspace):
    # http://www.topografix.com/gpx.asp
    gpx_files = get_file_list(workspace, '.gpx')
    fcs = []
    for gpx_file in gpx_files:
        arcpy.GPXtoFeatures_conversion(gpx_file, 'in_memory/temp')
        fcs.append(load_fc('in_memory/temp'))
    return fcs

