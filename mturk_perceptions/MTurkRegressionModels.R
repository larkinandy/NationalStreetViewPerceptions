######## MTurkRegressionModels.R ##########
# Author: Andrew Larkin
# Date Created: August 2nd, 2023
# Summary: Given perception scores for images rated by Amazon Mechanical Turk participants, 
#          create regression models to test for interactions between urban features, geographical location, 
#          and participant demographics

# load datasets into workspace
setwd("insert absolute filepath where csv files are stored")
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
  featuresModel <- lm(score ~ 
                        factor(urban)*factor(road) + 
                        factor(urban)*factor(division) + 
                        factor(age) + 
                        gender + 
                        factor(ethnicity) + 
                        factor(race) + 
                        factor(education) + 
                        factor(covid) + 
                        factor(h_division),data=cleanedData
                      )
  summary(featuresModel)
}

# create a linear regression model testing for interactions between urbanicity and demographics, 
# adjusting for other environmental features in street view imagery
createPersonalityModel <- function(inData) {
  cleanedData <- subset(inData,urban>0)
  personalityModel <- lm(score ~ 
                           factor(urban) + 
                           factor(urban)*factor(covid) + 
                           factor(urban)*factor(race) + 
                           factor(urban)*factor(ethnicity) + 
                           factor(urban)*factor(education) +
                           factor(urban)*factor(age) +
                           factor(urban)*gender +
                           factor(urban)*h_division + 
                           factor(division) + 
                           factor(road),data=cleanedData
                         )
  summary(personalityModel)
}

# create a lineear regression model testing for interactions between participant census division and image census division,
# adjusting for other environmental features in street view imagery and participant demographics
createAreaModel <- function(inData) {
  cleanedData <- subset(inData,division>0)
  areaModel <- lm(score ~ 
                    factor(division)*factor(h_division) +
                    factor(urban) +
                    factor(road) + 
                    factor(race) + 
                    factor(ethnicity) + 
                    factor(education) + 
                    factor(age) + 
                    factor(covid) + 
                    gender,data=cleanedData
                  )
  summary(areaModel)
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