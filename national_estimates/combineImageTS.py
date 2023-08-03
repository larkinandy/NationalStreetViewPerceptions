########### combineImageTS.py ###########
# Author: Andrew Larkin
# Date Created: Aug 3rd, 2023
# Summary: given TS perception scores for all images in an MSA, 
# average TS scores from multiple viewing angles taken at the same location
# and join with GSV metadata (e.g. latitude, longitude, panorama date).
# Finally, create national Quadrennial perception estimates from 2008-2020.

#import dependencies
import pandas as ps
import os

# define global constants
RASTER_YEARS = [2008,2012,2016,2020]
PARENT_FOLDER = "insert abolute filepath to where project is stored here"
PERCEPTIONS_FOLDER = PARENT_FOLDER + "Perceptions/" # where TS perception scores are stored
LINK_FOLDER = PARENT_FOLDER + "IdLink/" # where GSV metadata (for linking and georeferencing) is stored
GEOREFERENCED_FOLDER = PARENT_FOLDER + "GeoReferenced/" # where georeferenced perception estimates are stored
GEODATABASE_FOLDER = PARENT_FOLDER + "PerceptionGDB.gdb"

# load GSV metadata from file and drop uneeded variables to reduce memory footprint
# INPUTS:
#    inFilepath (string) - absolute filepath to metadata csv
# OUTPUTS:
#    GSV metadata as a pandas dataframe
def loadGeoLink(inFilepath):
    geoLink = ps.read_csv(inFilepath)
    geoLink.drop(['gridId','GEOID','county','imgMonth','fileName','rasterDiff','t'],axis=1,inplace=True)
    print("completed loading georeferenced data")
    return geoLink

# join perceptions and GSV metadata for a single MSA. Average perceptions for locations with multiple 
# viewing angles and perception scores
# INPUTS:
#    geoData (pandas dataframe) - contains GSV metadata include panoid and latitude,longitude
#    curMSA (string) - MSA to created joined data for
# OUTPUTS:
#    joinedAvgs (pandas dataframe) - perceptions and GSV metadata joined into a single pandas dataframe
def geoLinkData(geoData,curMSA):
    perceptionData = ps.read_csv(PERCEPTIONS_FOLDER + curMSA + "_perception_scores.csv")
    idLinker = ps.read_csv(LINK_FOLDER + curMSA + ".csv")
    idLinker = idLinker.rename({'filename': 'img_id'}, axis=1) 

    # join GSV metadata and perceptions
    joined = ps.merge(idLinker,perceptionData,how='inner',on='img_id')
    joined.drop(['img_id'],axis=1,inplace=True)

    # calculate average perceptions of multiple images taken at the same location
    avgs = joined.groupby('panId').mean()
    joinedAvgs = ps.merge(avgs,geoData,how='inner',on='panId')
    return(joinedAvgs)

# subset perception scores for every 4 years and save to csv
# INPUTS:
#    msaData (pandas dataframe) - perception scores for the current MSA
#    curMSA (string) - MSA to create 4 years subsets for
def saveMSAYearSubsets(msaData,curMSA):
    for year in RASTER_YEARS:
        outputFolder = GEOREFERENCED_FOLDER + str(year) + "/"
        outputFile = outputFolder + curMSA + "_geo.csv"
        tmp = msaData[msaData['rasterYear']==year]
        tmp.to_csv(outputFile,index=False)

# georeference data for a single MSA and create 4 year subsets
# INPUTS:
#    geoData (pandas dataframe) - contains GSV metadata include panoid and latitude,longitude
#    curMSA (string) - MSA to create 4 years subsets for
def processMSA(geoData,curMSA):
    linkedData = geoLinkData(geoData,curMSA)
    saveMSAYearSubsets(linkedData,curMSA)

# georeference all perception scores and save as 4 year subsets
def geoReferencePerceptions():

    # load GSV metadata
    geoLink = loadGeoLink(PARENT_FOLDER + "BEACON_comparison_setup/rasterLink.csv")

    # get list of MSAs that are already processed
    processedMSAs = ps.read_csv(PARENT_FOLDER + "FinishedGeo.csv")
    processedMSAs = list((set(processedMSAs['MSA'])))
    MSAsToProcess = os.listdir(PERCEPTIONS_FOLDER)

    for MSAFile in MSAsToProcess:
        curMSA = MSAFile[0:len(MSAFile)- len('_perception_scores.csv')]
        if(curMSA not in processedMSAs):

            # join perceptions and GSV metadata and save 4 year subsets for the current MSA
            processMSA(geoLink,curMSA)

            # add the current MSA to the list of MSAs that have already been processed
            processedMSAs.append(curMSA)
            tempDF = ps.DataFrame({
                'MSA':processedMSAs
            })
            tempDF.to_csv(PARENT_FOLDER + "FinishedGeo.csv",index=False)
            print("completed processing %s" %(curMSA))
        else:
            print("already processed %s" %(curMSA))

geoReferencePerceptions()

