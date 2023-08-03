########### createPerceptionGeoDatabase.py ###########
# Author: Andrew Larkin
# Date Created: Aug 3rd, 2023
# Summary: calculate TS perception scores for all MSAs in the US


# import dependencies
import arcpy
import pandas as ps
import os
from multiprocessing import Pool
arcpy.env.overwriteOutput= True

# define global constants
PARENT_FOLDER = 'insert absolute folderpath where geolocated data is stored'
GDB = PARENT_FOLDER + "PerceptionGDB.GDB"
GEO_FOLDER = PARENT_FOLDER + "GeoReferenced/"

#  convert long data format to wide data format, which is better for a Geodatabase attribute table
# INPUTS:
#   inData (pandas dataframe) - dataset to convert to wide format
# OUTPUTS:
#   input data converted to wide format, also as a pandas dataframe
def reformatGeoData(inData):
    keeps = ['panId','imgLat','imgLon','imgYear']
    kvLabel = {
        'beauty':'be',
        'nature':'na',
        'relaxing':'re',
        'safe_walk':'sw',
        'safe_crime':'sc'
    }
    kvComp = {
        'census_tract':'ct',
        'city':'ci'
    }
    for label in kvLabel.keys():
        for comp in kvComp.keys():
            newName = kvLabel[label] + "_" + kvComp[comp]
            oldName = label + "_" + comp
            inData[newName] = inData[oldName]*10
            inData[newName] = inData[newName].astype('int')
            keeps.append(newName)
    inData = inData[keeps]
    return(inData)

# combine georeferenced perceptions from all MSAs to create a national
# georeferenced perception CSV 
# INPUTS: 
#   year (int) - year of perceptions to combine
def combineGeo(year):
    index=0
    curFolder = GEO_FOLDER + str(year)

    # get list of MSA perceptions that need to be combined
    geoFiles = os.listdir(curFolder)
    dataFrames = []

    # load each perceptions for each MSA and then concatenate together
    for file in geoFiles:
        tempData = ps.read_csv(curFolder + "/" + file)
        dataFrames.append(reformatGeoData(tempData))
        index+=1
        if(index%500==0):
            print(index)
    newDF = ps.concat(dataFrames)
    newDF.to_csv(GEO_FOLDER + 'geo_' + str(year) + ".csv",index=False)

# add national georeferenced perceptions from a csv file into a geodatabase
# INPUTS:
#    year (int) - year of perceptions to combine
def createGeoPoint(year):
    file = GEO_FOLDER + "geo_" + str(year) + ".csv"
    filename = "geo_" + str(year) + "_point"
    filepth = GDB + "/" + filename
    print(file)
    print(filepth)

    # create point file in geodatabase using the georeferenced perception csv
    try:
        a = arcpy.management.XYTableToPoint(file, filepth, "imgLon", "imgLat", None, 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')
        print(a)
    except Exception as e:
        print(str(e))

# for a single year of interest, combine georeferenced data from multiple MSAs and then load the combined
# data into a geodatabase
def processSingleYear(year):
    print("started to process year %i" %(year))
    combineGeo(year)
    print("finished combineGeo for year %i" %(year))
    createGeoPoint(year)
    print("completed process year %i" %(year))

if __name__ == '__main__':
    # parallel processing currently doesn't work - CPU workers have conflicting temporary file 
    # read/writes in the ArcPro scratch database.  To make this work in parallel define a unique 
    # ArcPro scratch database for each CPU worker in the multiprocessing pool. 
    #yearset = [2008,2012,2016,2020]
    #pool = Pool(processes=len(yearset))
    #res = pool.map(processSingleYear,yearset)

    # run in a for loop since parallel processing is currently not functional
    for year in [2008,2012,2016,2020]:
        createGeoPoint(year)