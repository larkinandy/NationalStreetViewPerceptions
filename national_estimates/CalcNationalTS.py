########### CalcNationalTS.py ###########
# Author: Andrew Larkin
# Date Created: Aug 3rd, 2023
# Summary: calculate TS perception scores for all MSAs in the US

# import dependencies
import pandas as ps
from tsPackage import * 
from sklearn import preprocessing
from multiprocessing import Pool
import os

# define global constants
LABELS = ['beauty','nature','relaxing','safe_walk','safe_crime'] # one label for each perception
COMPARISON_LEVELS = ['census_tract','city'] # siamese network models compared images at the city and census tract level
PARENT_FOLDER = "insert absolute folderpath where input datasets and results are stored"
COMPARISON_FOLDER = PARENT_FOLDER + "/All_Cities/MSA_Image_CSV/" # where siamese network model outputs are stored 
PERCEPTION_FOLDER = PARENT_FOLDER + "Perceptions/" # where output TS scores will be stored
WORKSTATION_NUMBERS = [3,4,5,8,9] # if using multiple workstations, divide the work across workstations using the first digit of each MSA

# given a large set of data, partition data into tuple subsets so tuples can be processed in parallel by multiple CPUs
# INPUTS:
#     inFolder (string)  - absolute filepath where image comparisons are stored
#     comparisonLevel (string) - either 'census_tract' or 'city'
# OUTPUTS:
#     parallelTuples (list of tuples) - one tuple for each CPU that will work in parallel
def prepParallel(inFolder,comparisonLevel):
    parallelTuples = []
    for label in LABELS:
        for comparison in comparisonLevel:
            parallelTuples.append(
                (inFolder,label,comparison)
        )
    return(parallelTuples)

# given tuple metadata, create TS scores for a single perception and comparison unit (city or census tract)
# INPUTS:
#    dataTuple (tuple) - contains
#           dataFolder (string) - folder where siamese network perception model comparisons are stored
#           label (string) - perception type (e.g. 'beauty')
#           comparisonLevel (string) - 'city' or 'census_tract'
def processSingleLabel(dataTuple):
    # extract values from tuple
    dataFolder = dataTuple[0]
    label = dataTuple[1]
    comparisonLevel = dataTuple[2]
    inFile = dataFolder + "mturk_cate_" + label + "_one_" + comparisonLevel + ".csv"
    outFile = dataFolder + "ts_scores_" + label + "_" + comparisonLevel + ".csv"

    # load perception model predictions from csv and create multinomial TS scores
    gameDict = createGameDict(inFile)
    df = convertDictToDF(gameDict)

    # normalize TS scores from 0 to 1000
    df[label + "_" + comparisonLevel] = min_max_scaling(df['mu'])*100
    df.to_csv(outFile,index=False)

# for a given MSA, combine city and census tract comparisons of all perceptions into a single csv file
# INPUTS:
#    inFolder (string) - absolute filepath where all TS scores for a single MSA are stored
#    MSA (string) - current MSA to combine records for
def combineTSScores(inFolder,MSA):
    firstData = True
    for label in LABELS:

        # two comparison levels, city and census tract
        for comparisonLevel in COMPARISON_LEVELS:
            df = ps.read_csv(inFolder + "ts_scores_" + label + "_" + comparisonLevel + ".csv")
            df.drop(['sigma','n','mu'],axis=1,inplace=True)
            if(firstData):
                joinedDF = df
                firstData = False
            else: joinedDF = ps.merge(joinedDF,df,how='inner',on='img_id')
    # remove name suffix that was added during siamese network processing
    joinedDF['img_id'] = joinedDF['img_id'].str[-len('04005_097627_08W.png'):] 

    joinedDF.to_csv(PERCEPTION_FOLDER + str(MSA) + "_perception_scores.csv",index=False)


# main fuction
if __name__ == '__main__':

    # get list of MSAs to process, are remove MSAs that have already been processed
    MSAs = os.listdir(COMPARISON_FOLDER)
    FinishedMSAs = ps.read_csv(PARENT_FOLDER + "FinishedMSA.csv")
    FinishedMSAs = list(set(FinishedMSAs['MSA']))

    # for each MSA that hasn't yet been processed, divide the work of calculating TS scores among multiple CPU workers,
    # calculate TS scores for all perceptions and comparison levels, and combine all MSA TS perception scores into a single CSV
    for curMSA in MSAs:
        testOutput = PERCEPTION_FOLDER + curMSA + "_perception_scores.csv"
        if(not os.path.exists(testOutput) and int(curMSA[4:5]) in WORKSTATION_NUMBERS):
            print("calculating true skill scores for MSA %s" %(curMSA))
            MSAFolder = COMPARISON_FOLDER + curMSA + "/"
            
            # partition work into tuples for spreading across multiple CPUS
            parallelTuples = prepParallel(MSAFolder,COMPARISON_LEVELS)
            pool = Pool(processes=len(parallelTuples))

            # give each CPU one comparison level (2 total) and one perception label (5 total) to process (5x2 = 10 parallel CPUs)
            # this required a lot of memory for large MSAs: needed 256GB RAM to parallel process large cities like NYC metro area.
            res = pool.map_async(processSingleLabel,parallelTuples)
            res.get()
            FinishedMSAs.append(curMSA)
            df = ps.DataFrame({
                'MSA':FinishedMSAs
            }).to_csv(PARENT_FOLDER + "FinishedMSA.csv",index=False)
            combineTSScores(COMPARISON_FOLDER + curMSA + "/",curMSA)
        else:
            print("already processed MSA %s" %(curMSA))