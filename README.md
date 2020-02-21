# Implementing a GIS web app for climate change awareness

According to the United Nations Intergovernmental Panel on Climate Change (IPCC), human-induced climate warming is estimated to be between 0.8°C and 1.2°C compared to pre-industrial levels (Allen et al, 2018). In spite of the severe consequences of climate change and its overwhelmingly scientific consensus, parts of the society still do not acknowledge its importance (Lee et al, 2015). We hypothesise that part of this issue is because a majority of the worldwide population do not have access to climate change reports, and so we think it is necessary to develop engaging solutions and tools to raise social awareness about climate change.

To answer this need, the objective this project is to develop a webGIS portal to raise climate change awareness with the following capabilities:
1. Spatiotemporal visualization of global temperature and precipitation data.
2. Time series temperature and precipitation visualization of a user-selected location.

Our developped tool, which we named the **Climage Change explorer**, is openly available at [http://climatechanges.pythonanywhere.com](http://climatechanges.pythonanywhere.com). This repository contains the code necessary to build the app.

## Data and methods of the project

We used the National Oceanic and Atmospheric Administration (NOAA) CNEP/NCAR Reanalysis 1 temperature and precipitable water gridded dataset (1948-2019), which we aggregated at the yearly level. Country boundaries and Köppen-Geiger climate areas were used as auxiliary data. Further information of the data sources and characteristics is available in the [data project documentation](https://github.com/carlesmila/GeotechClimateChange/blob/master/documentation/data.md).

Our app was coded in python and was structured in three blocks: backend, frontend and deployment. Briefly, the backend performs a cache check and constructs the sqlite database needed to run the app, and it is structured in a series of python modules. The fronted block is written in _Dash_ and defines the layout and the callbacks of the app. Finally, the app is deployed in an open _PythonAnywhere_ server. A detailed description of the project methods is available in the [methods project documentation](https://github.com/carlesmila/GeotechClimateChange/blob/master/documentation/methods.md).

## How can I run the app?

As mentioned above, our app is openly available at [http://climatechanges.pythonanywhere.com](http://climatechanges.pythonanywhere.com). For those users that want to built on the app or simply have their own build, these are the requirements:
* Python 3.7 or later.
* The following modules installed: sqlite3, os, pandas, geopandas, netCDF4, statsmodels.api, plotly, numpy, dash, dash_html_components, dash_core_components.
* One of the two, depending on whether the user is interested in running the backend blocks as well, or work directly with the preprocessed data:
  * A valid sqlite database with the parsed data that can be dowloaded from [here](https://drive.google.com/drive/folders/1appQrtK-mBgP-fUSU0a7jCNqQFlsrH0t?usp=sharing).
  * Raw data files that can be downloaded from [here](https://drive.google.com/drive/folders/1w_ekNjUI7VHdHt_XUvp05_bUIS779n4t?usp=sharing).

To run the app in your local environment, please follow these steps.
1. Download the repository.
2. Place the downloaded files in the corresponding folder within the repository:

   * If the sqlite database has been downloaded, place it in the folder "Database" in the repository.
   * If the raw data files have been downloaded, place them in the folder "Data" in the repository.
3. Run the file "app.py".

We kindly suggest to use the pycharm IDE tu run the app.

## App functionality

The Climate Change explorer app is structured in 3 tabs: temperature, precipitable water, and about. The temperature and precipitable water tabs consist of two side by side panels. In the left panel, the user can visualize the spatial distribution of the variable for a given year, or can otherwise select to visualize the difference with respect to the baseline level (mean values between 1948-1952). When clicking on a specific location on the map, the time series plot on the right is updated to the selected location, showing the country, climate area, temperature profile and moving average (7 years). A preview of the app (temperature tab) is available in the following figure:

![alt text](documentation/figures/appoverview.png?raw=true)

## References

Allen, M.R., O.P. Dube, W. Solecki, F. Aragón-Durand, W. Cramer, S. Humphreys, M. Kainuma, J. Kala, N. Mahowald, Y. Mulugetta, R. Perez, M. Wairiu, and K. Zickfeld, 2018: Framing and Context. In: _Global Warming of 1.5°C. An IPCC Special Report on the impacts of global warming of 1.5°C above pre-industrial levels and related global greenhouse gas emission pathways, in the context of strengthening the global response to the threat of climate change, sustainable development, and efforts to eradicate poverty_. In Press.

Lee, T., Markowitz, E., Howe, P. et al. _Predictors of public climate change awareness and risk perception around the world_. Nature Clim Change 5, 1014–1020 (2015). https://doi.org/10.1038/nclimate2728
