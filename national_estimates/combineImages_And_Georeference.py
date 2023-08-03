########### CalcNationalTS.py ###########
# Author: Andrew Larkin
# Date Created: Aug 3rd, 2023
# Summary: calculate TS perception scores for all MSAs in the US


#import arcpy
import pandas as ps
import os

RASTER_YEARS = [2008,2012,2016,2020]
PARENT_FOLDER = "H:/BEACON/"
PERCEPTIONS_FOLDER = PARENT_FOLDER + "Perceptions/"
LINK_FOLDER = PARENT_FOLDER + "IdLink/"
GEOREFERENCED_FOLDER = PARENT_FOLDER + "GeoReferenced/"
GEODATABASE_FOLDER = PARENT_FOLDER + "PerceptionGDB.gdb"

def loadGeoLink(inFilepath):
    geoLink = ps.read_csv(inFilepath)
    geoLink.drop(['gridId','GEOID','county','imgMonth','fileName','rasterDiff','t'],axis=1,inplace=True)
    print("completed loading georeferenced data")
    return geoLink

def geoLinkData(geoData,curMSA):
    perceptionData = ps.read_csv(PERCEPTIONS_FOLDER + curMSA + "_perception_scores.csv")
    idLinker = ps.read_csv(LINK_FOLDER + curMSA + ".csv")
    idLinker = idLinker.rename({'filename': 'img_id'}, axis=1) 
    joined = ps.merge(idLinker,perceptionData,how='inner',on='img_id')
    joined.drop(['img_id'],axis=1,inplace=True)
    avgs = joined.groupby('panId').mean()
    joinedAvgs = ps.merge(avgs,geoData,how='inner',on='panId')
    return(joinedAvgs)

def saveMSAYearSubsets(msaData,curMSA):
    for year in RASTER_YEARS:
        outputFolder = GEOREFERENCED_FOLDER + str(year) + "/"
        outputFile = outputFolder + curMSA + "_geo.csv"
        tmp = msaData[msaData['rasterYear']==year]
        tmp.to_csv(outputFile,index=False)

def processMSA(geoData,curMSA):
    linkedData = geoLinkData(geoData,curMSA)
    saveMSAYearSubsets(linkedData,curMSA)


def geoReferencePerceptions():
    geoLink = loadGeoLink("E:/MTurkV2/BEACON_comparison_setup/rasterLink.csv")
    processedMSAs = ps.read_csv(PARENT_FOLDER + "FinishedGeo.csv")
    processedMSAs = list((set(processedMSAs['MSA'])))
    MSAsToProcess = os.listdir(PERCEPTIONS_FOLDER)
    for MSAFile in MSAsToProcess:
        curMSA = MSAFile[0:len(MSAFile)- len('_perception_scores.csv')]
        if(curMSA not in processedMSAs):
            processMSA(geoLink,curMSA)
            processedMSAs.append(curMSA)
            tempDF = ps.DataFrame({
                'MSA':processedMSAs
            })
            tempDF.to_csv(PARENT_FOLDER + "FinishedGeo.csv",index=False)
            print("completed processing %s" %(curMSA))
        else:
            print("already processed %s" %(curMSA))

geoReferencePerceptions()

