<img src = "/images/SafeWalkCrop.jpg" width="500">

# NationalStreetViewPerceptions
Scripts and datasets for creating national US estimates of street view perceptions


**Author:** [Andrew Larkin](https://www.linkedin.com/in/andrew-larkin-525ba3b5/) <br>
**Affiliation:** [Oregon State University, College of Health](https://health.oregonstate.edu/) <br>
**Principal Investigator:** [Peter James](https://www.hsph.harvard.edu/profile/peter-james/) <br>
**Principal Investiagor Affliation:** [Harvard T.H. Chan School of Public Health](https://www.hsph.harvard.edu/) <br>


**Summary** <br>
This github repository contains datasets and methods to create national US surfaces of street view perceptions.  Google Street View (GSV) images are not included due to user liscence restrictions.  However, those who are interested can download GSV images using the unique image ids and headings provided in the datasets.

**Repository Structure** <br>
Files are divided into five folders, with each folder corresponding to a unique stage of the study

- **[GSV_sampling](https://github.com/larkinandy/NationalStreetViewPerceptions/tree/master/GSV_sampling)** - create a GSV sampling strategy that maximizes variation in urbanicity and geography  <br>
- **[mturk_perceptions](https://github.com/larkinandy/NationalStreetViewPerceptions/tree/master/mturk_perceptions)** - street view perceptions and demographics collected from Amazon Mechanical Turk participants.
- **[deep_learning_models](https://github.com/larkinandy/NationalStreetViewPerceptions/tree/master/deep_learning_models)** -create and evaluate Siamese convolutional neural network perception models <br>
- **[five_cities_comparison](https://github.com/larkinandy/NationalStreetViewPerceptions/tree/master/five_cities)** -create TrueSkill perception scores for five large cities in the US at census tract, city, and national comparison levels <br>
- **[national surfaces](https://github.com/larkinandy/NationalStreetViewPerceptions/tree/master/national_estimates)** - create TrueSkill scores using deep learning model predictions for 30 million gridded locations across the US <br>

**External Links and Additional Resources**
- **Publication** - TODO: insert link once published
- **Related Repositories** - https://github.com/larkinandy/Perceptions_MTurk
- **Related Publications** - https://www.nature.com/articles/s41370-022-00489-8
- **Google Street View** - https://en.wikipedia.org/wiki/Google_Street_View
- **Amazon Mechanical Turk** - https://www.mturk.com/
- **Siamese Networks** - https://builtin.com/machine-learning/siamese-network
- **Microsoft True Skill Score** - https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/
- **Spatial Health Lab** - https://health.oregonstate.edu/labs/spatial-health
- **Funding:** - TODO: add funding id and link to funding source
