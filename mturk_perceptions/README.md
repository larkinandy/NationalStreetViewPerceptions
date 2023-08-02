<img src = "/images/ParticipantResponsesByCensus.jpg" width="700">

# Mturk Perceptions

**Summary** <br>
Perception and demographic data collected from Amazon Mechanical Turk (AMT).  This file also includes Jupyter notebooks for analysis.  Steps include:
1) Collecting data from participants
2) Normalizing records by participant propensity for slider placement (see external link below for more details)
3) Removing records where the QA question was incorrectly answered
4) Create summary statistics and test for perception differences across demographics and geographical location

**Scripts** <br>
- **[CalcMTurkDiffs.ipynb](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/mturk_perceptions/CalcMTurkDiffs.ipynb)** - calculate differences in perceptions between left and right images in am image comparison
- **[MTurkForestPlots.ipynb](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/mturk_perceptions/MTurkForstPlots.ipynb)** - create forest plots for each perception, with each row of the forest plot corresponding to a difference demographic classification level
- **[MTurkRegression.R]()** - test for significant differences between geography and demographics using multivariate linear regression

**Files** <br>
- **[Amazon_Mechanical_Turk_Demographic_Questions.docx](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/files/Amazon_Mechanical_Turk_Demographic_Questions.docx)** - specific wording used to collect demographic questions from AMT participants
- **[Forest_Plot_CSVs](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/files/Forest_Plot_CSVs.zip)** - csv files used as input to create forest plots with the Jupyter notebook MTurkForestPlots.ipynb
- **[Meta_link.csv](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/files/meta_link.csv)** - table to join image classification codes with mechanical turk records
- **[MTurk_Data_Dictionary_Aug2_23.xlsx](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/files/MTurk_Data_Dictionary_Aug2_23.xlsx)** - data dictionary for mechanical turk records
- **[MTurk_Records_May11_21.csv](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/files/MTurk_Records_May11_21.csv)** - perception records from AMT, after removing records that did not pass QA screening

**External links**
- **Related Publications** - https://www.nature.com/articles/s41370-022-00489-8
