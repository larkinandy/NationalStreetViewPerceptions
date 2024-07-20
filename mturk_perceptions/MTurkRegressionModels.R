######## MTurkRegressionModels.R ##########
# Author: Andrew Larkin
# Date Created: August 2nd, 2023
# Summary: Given perception scores for images rated by Amazon Mechanical Turk participants, 
#          create regression models to test for interactions between urban features, geographical location, 
#          and participant demographics

# load datasets into workspace
setwd("C:/users/larki/desktop/MturkPaper")
beautyData <- read.csv("mturk_regression_beauty_screened.csv")
natureData <- read.csv("mturk_regression_nature_screened.csv")
relaxingData <- read.csv("mturk_regression_relaxing_screened.csv")
crimeData <- read.csv("mturk_regression_safe_crime_screened.csv")
walkData<- read.csv("mturk_regression_safe_walk_screened.csv")



# create a linear regression model testing for interactions between urban features in street view images and adjusting for demographics
# INPUTS:
#    inData (dataframe) - values to use for the linear regresison model
createFeaturesModel <- function(inData) {
  cleanedData <- subset(inData,urban>0)
  cleanedData <- subset(cleanedData,covid>0)
  cleanedData <- subset(cleanedData,race>0)
  cleanedData <- subset(cleanedData,ethnicity>0)
  cleanedData <- subset(cleanedData,h_division>0)
  cleanedData <- subset(cleanedData,education>0)
  cleanedData <- subset(cleanedData,age>0)
  cleanedData <- within(cleanedData, urban <- relevel(factor(urban),ref=3))
  cleanedData <- within(cleanedData,division <- relevel(factor(division),ref=2))
  cleanedData <- within(cleanedData,road<-relevel(factor(road),ref=2))
  cleanedData <- within(cleanedData,race<-relevel(factor(race),ref="WH"))
  cleanedData <- within(cleanedData,age <- relevel(factor(age),ref=1))
  cleanedData <- within(cleanedData,education <- relevel(factor(education),ref=1))
  cleanedData <- within(cleanedData,covid <- relevel(factor(covid),ref='NE'))
  cleanedData <- within(cleanedData,h_division <- relevel(factor(h_division),ref=2))
  cleanedData <- within(cleanedData,ethnicity <- relevel(factor(ethnicity),ref=1))
  featuresModel <- lm(score ~
                        urban +
                        road + 
                        division + 
                        urban*age + 
                        urban*gender + 
                        urban*ethnicity + 
                        urban*race + 
                        urban*education + 
                        urban*covid + 
                        urban*h_division,data=cleanedData
  )
  summary(featuresModel)
}





# create a linear regression model testing for interactions between urban features in street view images and adjusting for demographics
# INPUTS:
#    inData (dataframe) - values to use for the linear regresison model
createFeaturesRoadModel <- function(inData) {
  cleanedData <- subset(inData,road>0)
  cleanedData <- subset(cleanedData,covid>0)
  cleanedData <- subset(cleanedData,race>0)
  cleanedData <- subset(cleanedData,ethnicity>0)
  cleanedData <- subset(cleanedData,h_division>0)
  cleanedData <- subset(cleanedData,education>0)
  cleanedData <- subset(cleanedData,age>0)
  cleanedData <- within(cleanedData, urban <- relevel(factor(urban),ref=3))
  cleanedData <- within(cleanedData,division <- relevel(factor(division),ref=2))
  cleanedData <- within(cleanedData,road<-relevel(factor(road),ref=3))
  cleanedData <- within(cleanedData,race<-relevel(factor(race),ref="WH"))
  cleanedData <- within(cleanedData,age <- relevel(factor(age),ref=1))
  cleanedData <- within(cleanedData,education <- relevel(factor(education),ref=1))
  cleanedData <- within(cleanedData,covid <- relevel(factor(covid),ref='NE'))
  cleanedData <- within(cleanedData,h_division <- relevel(factor(h_division),ref=2))
  cleanedData <- within(cleanedData,ethnicity <- relevel(factor(ethnicity),ref=1))
  featuresModel <- lm(score ~
                        urban +
                        road + 
                        division + 
                        road*age + 
                        road*gender + 
                        road*ethnicity + 
                        road*race + 
                        road*education + 
                        road*covid + 
                        road*h_division,data=cleanedData
  )
  summary(featuresModel)
}

# create a linear regression model testing for interactions between urbanicity and demographics, 
# adjusting for other environmental features in street view imagery
createAreaModel <- function(inData) {
  cleanedData <- subset(inData,division>0)
  cleanedData <- subset(cleanedData,covid>0)
  cleanedData <- subset(cleanedData,race>0)
  cleanedData <- subset(cleanedData,ethnicity>0)
  cleanedData <- subset(cleanedData,h_division>0)
  cleanedData <- subset(cleanedData,education>0)
  cleanedData <- subset(cleanedData,age>0)
  cleanedData <- within(cleanedData, urban <- relevel(factor(urban),ref=3))
  cleanedData <- within(cleanedData,division <- relevel(factor(division),ref=1))
  cleanedData <- within(cleanedData,road<-relevel(factor(road),ref=3))
  cleanedData <- within(cleanedData,race<-relevel(factor(race),ref="WH"))
  cleanedData <- within(cleanedData,age <- relevel(factor(age),ref=1))
  cleanedData <- within(cleanedData,education <- relevel(factor(education),ref=1))
  cleanedData <- within(cleanedData,covid <- relevel(factor(covid),ref='NE'))
  cleanedData <- within(cleanedData,h_division <- relevel(factor(h_division),ref=1))
  cleanedData <- within(cleanedData,ethnicity <- relevel(factor(ethnicity),ref=1))
  featuresModel <- lm(score ~
                        urban +
                        road + 
                        division*h_division + 
                        age + 
                        gender + 
                        ethnicity + 
                        race + 
                        education + 
                        covid, 
                        data=cleanedData
  )
  summary(featuresModel)
}

# beauty regression models
createFeaturesModel(beautyData)
createPersonalityModel(beautyData)
createAreaModel(beautyData)

# nature regression models
createFeaturesModel(natureData)
createPersonalityModel(natureData)
createAreaModel(natureData)

# relaxing regression models
createFeaturesModel(relaxingData)
createPersonalityModel(relaxingData)
createAreaModel(relaxingData)

# safe for walking regression models
createFeaturesModel(walkData)
createPersonalityModel(walkData)
createAreaModel(walkData)

# safe from crime regression models
createFeaturesModel(crimeData)
createPersonalityModel(crimeData)
createAreaModel(crimeData)

a <- subset(beautyData,urban==1)
summary(lm(score~ 0+
           
                                  
                                   factor(road) + 
                                   factor(division) + 
                                   factor(age) + 
                                   gender + 
                                   factor(ethnicity) + 
                                   factor(race) + 
                                   factor(education) + 
                                   factor(covid) + 
                                   factor(h_division),data=a
             ))
       
           
             