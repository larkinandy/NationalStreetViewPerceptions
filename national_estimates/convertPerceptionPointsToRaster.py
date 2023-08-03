########### convertPerceptionPointsToRaster.py ###########
# Author: Andrew Larkin
# Date Created: Aug 3rd, 2023
# Summary: given a geodatabase of perception point data,
#          convert points to raster with approximate cell size equivalent to 
#          the distribution of street view point sampling ()

# import dependencies
import arcpy
arcpy.env.overwriteOutput=True
from multiprocessing import Pool
import os

# define global constants
PARENT_FOLDER = "insert absolute folderpath where geodatabase is stored here"
GDB = PARENT_FOLDER + "PerceptionGDB.GDB"
GEO_FOLDER = PARENT_FOLDER + "GeoReferenced/"
RASTER_FOLDER = PARENT_FOLDER + "PerceptionRasters/"


# create a raster from one attribute field in a point geodatabase
# INPUTS:
#    year (int) - year of interest, perceptions were calculated for every 4 years
#    perception (string) - perception name and comparison level (needs to match attribute field in geodatabasae)
def convertToRaster(year,perception):
    inDataset = "geo_" + str(year) + "_point"
    outRaster = GEO_FOLDER + "geo_" + str(year) + "_" + perception + ".tif"
    if (os.path.exists(outRaster)):
        print("%s already exists" %(outRaster))
        return
    arcpy.conversion.PointToRaster(
        in_features= GDB + "/" + inDataset,
        value_field=perception,
        out_rasterdataset=outRaster,
        cell_assignment="MEAN",
        priority_field="NONE",
        cellsize=0.0008333,
        build_rat="BUILD"
    )

# convert a floating point raster to int to save disk space.  Estimates range from 0 to 1000
#    year (int) - year of interest, perceptions were calculated for every 4 years
#    perception (string) - perception name and comparison level
def convertRasterToInt(year,perception):
    inRaster = GEO_FOLDER + "geo_" + str(year) + "_" + perception + ".tif"
    outRaster = RASTER_FOLDER + "geo_" + str(year) + "_" + perception + ".tif"
    if(os.path.exists(outRaster)):
        print("%s already exists" %(outRaster))
        return
    raster = arcpy.Raster(inRaster)
    raster = arcpy.sa.Int(raster)
    raster.save(outRaster)

# given a year of interest, calculate national perceptions and comparison levels for that year
# INPUTS:
#    year (int) - year of interest
def convertAllPerceptionsToRaster(year):
    # key:
    #    be: beauty, na: nature quality, re: relaxing, sw: safety for walking, sc: safety from crime
    #    ci: city level comparison, ct: census tract comparisons 
    for outcome in ['be_ci','be_ct','na_ci','na_ct','re_ci','re_ct','sw_ci','sw_ct','sc_ci','sc_ct']:
        print("creating raster for year %i and outcome %s " %(year,outcome))

        convertToRaster(year,outcome)

def roundRasterToInt(year):
    # key:
    #    be: beauty, na: nature quality, re: relaxing, sw: safety for walking, sc: safety from crime
    #    ci: city level comparison, ct: census tract comparisons 
    for outcome in ['be_ci','be_ct','na_ci','na_ct','re_ci','re_ct','sw_ci','sw_ct','sc_ci','sc_ct']:
        print("creating raster for year %i and outcome %s " %(year,outcome))
        convertRasterToInt(year,outcome)


if __name__ == '__main__':
    years = [2008,2012,2016,2020]
    pool = Pool(processes=len(years))
    res = pool.map_async(convertAllPerceptionsToRaster,years)
    res.get()    

    res = pool.map_async(roundRasterToInt,years)
    res.get()    