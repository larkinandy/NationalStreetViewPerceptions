<img src = "/images/SampleSelection.jpg" width="500">

# GSV Sampling

**Summary** <br>
Strategy for sampling Google Street View Images to maximize the variation in urbanicity and geography across image comparisons.  Steps include:
1) Creating a superset of coordinate locations in ArcGIS.
2) Querying Google Street View API to test if images are available at coordinate locations
3) Identify road direction in ArcGIS and adjusting for differences betweeen compass heading and vehicle heading (Google Street View API stores image angles relative to compass heading, but we want image angles relative to road heading
4) Download GSV images using the adjusted headings
5) Visually inspect images and remove those with abnormal visual qualities (e.g. ghosting, excessive rain smearing)

**Scripts** <br>
- **[getGSVImagesForMTurkv2.ipynb]()** - Jupyter notebook for downloading GSV images, selecting a subset of images to meet the target range of images for each category, and removing images that were flagged during visual inspection.
- **[GSVMTurkv2Counts.ipynb]()** - Jupyter notebook for counting number of images per category in the final dataset

**Files** <br>
GSV_Images.shp - ArcGIS point shapefile with locations, categories (e.g. division) and metadata for images in the final dataset
unrbanizedAreas.shp - 2010 US Census Urban Areas
USCensusDivisions.shp - US Census Divisions


