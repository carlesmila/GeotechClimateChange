# Implementing a GIS web app for climate change awareness

According to the United Nations Intergovernmental Panel on Climate Change (IPCC), human-induced climate warming is estimated to be between 0.8°C and 1.2°C compared to pre-industrial levels (Allen et al, 2018). In spite of the severe consequences of climate change and its overwhelmingly scientific consensus, parts of the society still do not acknowledge its importance (Lee et al, 2015). We hypothesise that part of this issue is because a majority of the worldwide population do not have access to climate change reports, and so we think it is necessary to develop engaging solutions and tools to raise social awareness about climate change.

To answer this need, the objective this project is to develop a webGIS portal to raise climate change awareness with the following capabilities:
1. Spatiotemporal visualization of global temperature and precipitation data.
2. Time series temperature and precipitation visualization of a user-selected location.

Our developped tool, which we named the **Climage Change explorer** is openly available at [http://climatechanges.pythonanywhere.com](http://climatechanges.pythonanywhere.com). This repository contains the code necessary to build the app.

## Data and methods 

WE NEED TO COMPLETE 

Further information of the data sources and characteristics is available in the [data project documentation](https://github.com/carlesmila/GeotechClimateChange/blob/master/documentation/data.md). A detailed description of the project methods is available in the [methods project documentation](https://github.com/carlesmila/GeotechClimateChange/blob/master/documentation/methods.md).

## How can I run the app?

As mentioned above, our app is openly available at [http://climatechanges.pythonanywhere.com](http://climatechanges.pythonanywhere.com). For those users that want to built on the app or simply have their own build, these are the steps that need to be taken:

HERE THE STEPS.


## App functionality

The Climate Change explorer app is structured in two side by side panels (on different tabs for temperature and precipitable water). In the left panel, the user can visualize the spatial distribution of the variable for a given year, or can otherwise select to visualize the difference with respect to the baseline level (mean values between 1948-1952). When clicking on a specific location on the map, the time series plot on the right is updated to the selected location, showing the country, climate area, temperature profile and moving average (7 years). A preview of the app is available in the following figure:

![alt text](documentation/figures/appoverview.png?raw=true)
