########### tsPackage.py ###########
# Author: Andrew Larkin
# Date Created: Aug 3rd, 2023
# Summary: contains a custom class and functions for claculating TrueSkill perceptions scores from siamese neural network model predictions.

# import dependencies
from trueskill import Rating, quality_1vs1, rate_1vs1
import numpy as np
import pandas as ps

# Custom class for updating true skill image scores by processing a single siamese neural network model prediction.
# Note: this is a multinomial trueskill algorithm which differs from the original trueskill agorithm (https://www.nature.com/articles/s41370-022-00489-8).
class TS:

    # initialize a multinomial trueskill state, with 3 levels
    def __init__(self):
        self.strong = Rating(mu=25,sigma=6.8)
        self.mod = Rating(mu=25,sigma=6.8)
        self.slight = Rating(mu=25,sigma=6.8)
        self.n = 0
        
    # calculate the mean mu across all 3 levels
    def calcAvgTSMean(self):
        return((self.slight.mu + self.mod.mu + self.strong.mu)/3.0)
    
    # calulcate the  mean sigma across all 3 levels
    def calcAvgTSSigma(self):
        return((self.slight.sigma + self.mod.sigma + self.strong.sigma)/3.0)
    

# using the set of images listed in an input dataset, create a dictionary for storing and updating 
# image trueskill perception scores
# INPUTS:
#    dataset (pandas dataframe) - contains siamese network model predictions
# OUTPUTS:
#    imgDict (dictionary) - contains set of kv imageids:TrueSkill objects
def createPerceptionDict(dataset):

    # create a set of image ids
    leftImgs = list(set(dataset['l_id']))
    rightImgs = list(set(dataset['r_id']))
    uniqueImgs = list(set(leftImgs + rightImgs))
    print("completed creating unique list")
    imgDict = {}

    # for each image id, initiliaze a TS object and store in the imgDict dictionary
    for index in range(len(uniqueImgs)):
        imgDict[uniqueImgs[index]] = TS()
    return(imgDict)

# given a dictionary with TS objects, transform the dictionary and TS contents into a dataframe format
# INPUTS:
#    tsDict (dictionary) - contains kv pairs of image ids:TS objects
# OUTPUTS:
#    df (pandas dataframe) - contents of the input dictionary transformed into a pandas dataframe format
def convertDictToDF(tsDict):

    # arrays, one array for each column in the output data frame
    imgId,mu,sigma,n = [],[],[],[]

    # for each TS class object, extract the contents of  the object and store in the temporary arrays
    for key in list(tsDict.keys()):
        curTS = tsDict[key]
        mu.append(curTS.calcAvgTSMean())
        sigma.append(curTS.calcAvgTSSigma())
        imgId.append(key)
        n.append(curTS.n)

    # create the dataframe using the temporary arrays
    df = ps.DataFrame({
        'mu':mu,
        'sigma':sigma,
        'img_id':imgId,
        'n':n
    })
    return(df)

# given a result from an image comparison, update TS scores for a single level in the multinomial TS model
# INPUTS:
#    outcome (string) - outcome of the comparison. Can be 'win' ,'lose', or 'tie'
#    TSP1 (trueskill object) - trueskill object for a single level in the multinomial model, left image
#    TSP2 (trueskill object) - trueskill object for a single level in the multinomial model, right image
# OUTPUTS:
#    TSP1, after updating with the outcome
#    TSP2, after updating with the outcome
def updateOutcomes(outcome,TSP1,TSP2):
    # left image loses, right image wins
    if(outcome == "lose"):
        newp2,newp1 = rate_1vs1(TSP2,TSP1)
        return(newp1,newp2)
    # left image wins, right image loses
    if(outcome =="win"):
        return(rate_1vs1(TSP1, TSP2))
    # tie
    return(rate_1vs1(TSP1, TSP2, drawn=True))

# given the three outcomes for each level in a multinomial TS comparison, update multinomial true skill scores for the two compared images
# INPUTS:
#    ts1 (TS object) - multinomial TS object for left image
#    ts2 (TS object) - multinomial TS object for right image
#    outcomes (string array) - contains one outcome for each level in the multinomial model
# OUTPUTS:
#    ts1, after updating with the input outcomes
#    ts2, after updating with the input outcomes
def updateScores(ts1,ts2,outcomes):
        
        # update the trueskill scores for the first level in the multinomial TS model
        ts1.slight,ts2.slight = updateOutcomes(outcomes[0],ts1.slight,ts2.slight)

        # update the trueskill scores for the second level in the multinomial TS model
        ts1.mod,ts2.mod = updateOutcomes(outcomes[1],ts1.mod,ts2.mod)

        # update the trueskill scores for the third level in the multinomial TS model
        ts1.strong,ts2.strong = updateOutcomes(outcomes[2],ts1.strong,ts2.strong)
        ts1.n +=1
        ts2.n +=1
        return([ts1,ts2])

# given a siamese perception model prediction, convert into a multinomial outcome to update the multinomial TS scores
# INPUTS:
#    vote (int) - value between 0 to 100, indicating which image won and the extent to which the image won
# OUTPUTS:
#    string array, with one outcome for each level in the multinomial TS model
def convertVoteToOutcome(vote):
    vote = int(vote)

    # tie
    if(vote==50):
        return(['tie','tie','tie'])
    
    # right image wins
    if(vote<50):
        # right image strongly wins
        if(vote<16):
            return(['lose','lose','lose'])
        # right image moderately wins
        if(vote<33):
            return(['lose','lose','tie'])
        # right image slightly wins
        return(['lose','tie','tie'])
    
    # left image wins
    else:
        # left image strongly wins
        if(vote>84):
            return(['win','win','win'])
        # left image moderately wins
        if(vote>67):
            return(['win','win','tie'])
        # left image slightly wins
        return(['win','tie','tie'])

# given a single record from the dataset of siamese perception model predictions, upate TS scores for the two images used as model inputs
# INPUTS:
#    TS_Dict (dictionary) - contains multinomial TS objects for all images in the image dataset
#    id1 (string) - image id for the left image in the siamese network
#    id2 (string) - image id for the right image in the siamese network
#    score (int) - siamese model prediction for which image won, and by how much
# OUTPUTS:
#    TS_Dict, after updating the TS objects for the two image in the siamese network comparison
def performTSGame(TS_Dict,id1,id2,score):
    outcome = convertVoteToOutcome(score)
    ts1,ts2 = updateScores(TS_Dict[id1],TS_Dict[id2],outcome)
    TS_Dict[id1] = ts1
    TS_Dict[id2] = ts2
    return(TS_Dict)

# normalize a list of values
# INPUTS:
#   series (float array) - list of values to normalize
# OUTPUTS:
#   normalized values from the input series
def min_max_scaling(series):
    return (series - series.min()) / (series.max() - series.min())

# given a csv of siamese perception model predictions, create a dictionary of
# TS objects, one object for each image id, and calculate multinomial TS scores
# for each image using the siamese model predictions.
# INPUTS:
#    inputCSV (string) - absolute filepath to csv containing siamese perception model predictions
# OUTPUTS:
#    dictionary of multinomial TS scores based on the siamese model predictions
def createGameDict(inputCSV):

    # load dataset into memory and randomize the record order.  TS is a state-dependent model, so
    # randomization is important to avoid unforseen biases in record order
    testPerceptions = ps.read_csv(inputCSV)
    testPerceptions = testPerceptions.sample(frac=1).reset_index(drop=True)
    # reduce the dataset ram footprint to just the necessary information
    testPerceptions['l_id'] = testPerceptions['l_img'].str[:]
    testPerceptions['r_id'] = testPerceptions['r_img'].str[:]
    testPerceptions = testPerceptions[['pred','l_id','r_id']]
    print(testPerceptions.head())

    # create a mutlinomial TS dictionary, and update the dictionary with the siamese perception model predictions
    imgDict = createPerceptionDict(testPerceptions)
    for rowIndex in range(testPerceptions.count()[0]):
        curRow = testPerceptions.iloc[rowIndex]
        if(rowIndex%100000==0):
            print(rowIndex)
        imgDict = performTSGame(imgDict,curRow['l_id'],curRow['r_id'],curRow['pred'])
    return(imgDict)
