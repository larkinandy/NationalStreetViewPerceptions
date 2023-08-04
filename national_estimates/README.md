<img src = "/images/MultipleAreasRelaxing.jpg" width="700">

# national estimates
Scripts and datasets for creating national US estimates of street view perceptions

**Summary** <br>
Methods for calculating TrueSkill scores and creating national US perception surfaces.  Steps include
1) Caculating multinomial trueskill scores from siamese neural network perception model outputs
2) Combining trueskill scores from multiple viewing angles into a single estimate for a single location
3) Joining trueskill scores with Google Street View metadata and creating a point geodatabase
4) Converting the point geodatabase into a set of rasters
5) Creating 500m and 1000m average estimates from the higher resolution raster created in step 4

**Scripts** <br>
- **[tsPackage.py](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/national_estimates/tsPackage.py)** - custom class and package for calculating multinomial trueskill scores
- **[CalcNationalTS.py](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/national_estimates/CalcNationalTS.py)** - calculate TrueSkill perception scores based on more than 3 billion siamese perception model outputs.
- **[combineImageTS.py](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/national_estimates/combineImageTS.py)** - combine TrueSkill scores of images taken from multiple viewing angles but at the same location.  Also join trueskill estimates with street view metdata.
- **[createPerceptionGeoDatabase.py](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/national_estimates/createPerceptionGeoDatabase.py)** - create a point geodatabase of national quadrennial perception estimates from 2008-2020 using csv files created from the previous script.
- **[convertPerceptionPointsToRaster.py](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/national_estimates/convertPerceptionPointsToRaster.py)** - convert the point geodatabase into quadrennial perception rasters from 2008-2020.
- **[createFocalRasters.py](https://github.com/larkinandy/NationalStreetViewPerceptions/blob/main/national_estimates/createFocalRasters.py)** - create rasters of perception estimates at 500m and 1000m resolution

**Files** <br>
Due to restrictions in the Google Street View API user agreement we are unable to provide files that contain perception scores for street view images or at street view locations.  We are looking into whether it is legally permissible to share aggregated averages at the census tract level.  
