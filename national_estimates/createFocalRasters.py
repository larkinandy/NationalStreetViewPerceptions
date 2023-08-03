########### createFocalRasters.py ###########
# Author: Andrew Larkin
# Date Created: Aug 3rd, 2023
# Summary: given rasters of national TS perceptions at 0.0008333 degrees resolution,
#          create rasters of TS perceptions at 500m and 1000m resolution

# import dependencies
import arcpy
import pandas as ps
import os
from multiprocessing import Pool
arcpy.env.overwriteOutput= True

# define global constants
PARENT_FOLDER = "insert absolute folderpath where perception rasters are stored here"
RASTER_INPUT = PARENT_FOLDER + "PerceptionRasters/"
INTERMEDIATE_FOLDER = PARENT_FOLDER + "TempRasters/"
BUFFER_RASTERS = PARENT_FOLDER + "PerceptionBuffers/"
BUFFER_DISTANCES = [500,1000]
COMPARISON_LEVELS = ["ci","ct"]
LABELS = ["be","na","sc","sw","re"]
YEARS = [2008,2012,2016,2020]
MERCATOR_COORD = 'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]'
WGS84_COORD = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'

# sanity check to test if 500m and 1000m rasters were already created for a single input raster
# INPUTS:
#    shortName (string) - part of filename nomenclature which corresponds to the input raster
# OUTPUTS: 
#    true if 500m and 1000m rasters were already created for the input raster.  False otherwise
def testIsComplete(shortName):
    outputFiles = []
    for buffer in BUFFER_DISTANCES:
        curOutput = BUFFER_RASTERS + shortName + "_" + str(buffer) + ".tif"
        if not(os.path.exists(curOutput)):
            outputFiles.append(curOutput)
    if(len(outputFiles)==0):
        return(True)
    return(False)

# create 500m and 1000m rasters from a single input raster
# INPUTS:
#    datatuple (tuple) - contains data needed to load raster and create outputs
#         comparisonLevel - either 'ci' or 'ct' (city or census tract)
#         label - 'be','na','re','sw', or 'sc' (beuaty, nature, relaxing, safety for walking, or safety from crime)
#         year - 2008, 2012, 2016, or 2020
def processOneRaster(dataTuple):
    compareLevel,label,year = dataTuple[0], dataTuple[1], dataTuple[2]
    shortName = "geo_" + str(year) + "_" + label + "_" + compareLevel
    # test if 500m and 1000m were already created.  If so skip the rest of the function
    if(testIsComplete(shortName)):
        print("buffers for %s already complete " %(shortName))
        return
    # project the raster into a GCS that uses meters rather than decimal degrees
    projectedRaster = INTERMEDIATE_FOLDER + shortName + "proj.tif"
    if not(os.path.exists(projectedRaster)):
        arcpy.management.ProjectRaster(
            in_raster=RASTER_INPUT + shortName + ".tif",
            out_raster=INTERMEDIATE_FOLDER + shortName + "proj.tif",
            out_coor_system=MERCATOR_COORD,
            resampling_type="BILINEAR",
            cell_size="100 100",
            geographic_transform=None,
            Registration_Point=None,
            in_coor_system=WGS84_COORD,
            vertical="NO_VERTICAL"
        )
    # create 500m and 1000m products from the projected raster using focal statistics
    for buffer in BUFFER_DISTANCES:
        out_raster = arcpy.ia.FocalStatistics(
            in_raster=INTERMEDIATE_FOLDER + shortName + "proj.tif",
            neighborhood="Circle " + str(buffer) + " MAP",
            statistics_type="MEAN",
            ignore_nodata="DATA",
            percentile_value=90
        )
        out_raster = arcpy.sa.Int(out_raster)
        out_raster.save(INTERMEDIATE_FOLDER + shortName + "_" + str(buffer) + ".tif")

        # reproject the raster back into it's native GCS to preserve distance and shape relationships
        arcpy.management.ProjectRaster(
            in_raster=INTERMEDIATE_FOLDER + shortName + "_" + str(buffer) + ".tif",
            out_raster= BUFFER_RASTERS + shortName + "_" + str(buffer) + ".tif",
            out_coor_system=WGS84_COORD,
            resampling_type="BILINEAR",
            cell_size="0.0008333 0.0008333",
            geographic_transform=None,
            Registration_Point=None,
            in_coor_system=MERCATOR_COORD,
            vertical="NO_VERTICAL"
        )
    print("completed calculating buffers for %s" %(shortName))

# convert a floating point raster to int to save disk space
# INPUTS:
#    inRaster (string) - absolute filepath to the floating point raster
#    outRaster (string) - absolute filepath to the int raster to create
def convertRasterToInt(inRaster,outRaster):
    if(os.path.exists(outRaster)):
        print("%s already exists" %(outRaster))
        return
    raster = arcpy.Raster(inRaster)
    raster = arcpy.sa.Int(raster)
    raster.save(outRaster)

# transform metadata into tuples to distribute workload across multiple CPUs
def prepRastersParallel():
    parallelTuples = []
    # create one tuple for each year/comarison level/perception combination. 
    # one tuple goes to one CPU worker
    for year in YEARS:
        for compare in COMPARISON_LEVELS:
            for label in LABELS:
                dataTuple = (compare,label,year)
                parallelTuples.append(dataTuple)
    return(parallelTuples)

if __name__ == '__main__':
    parallelTuples = prepRastersParallel()
    print("number of rasters to calculate buffers for: %i" %(len(parallelTuples)))
    pool = Pool(processes=8)
    res = pool.map_async(processOneRaster,parallelTuples)
    a = res.get()
