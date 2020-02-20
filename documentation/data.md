# Data

## Main data
The climate dataset to be used in this project is developed by National Oceanic and Atmospheric Administration (NOAA) and National Center for Atmospheric Research (NCAR). The product is called CNEP/NCAR Reanalysis 1 and consists of a system to perform large data assimilation from 1948 to present time. The reanalysis dataset has many products (e.g. wind fields, temperature, humidity, pressure, precipitable water) at different temporal resolutions: 4-times daily, daily, monthly values. The different meteorological indicators are available in grid format with a spatial resolution from 1.875°x1.875° to 2.5°x2.5° depending on the indicator. Data are openly available in NetCDF format in the corresponding ESRL [portal](https://www.esrl.noaa.gov/psd/data/gridded/data.ncep.reanalysis.html).

In this project, we used air temperature and preciptable water content montlhy data, that was aggregated into yearly averages in order to provide a more comprehensive data visualization.

## Auxiliary data
Countries' names and climate zones were also used (in geojson format) in the application development to provide more information for the user about the location where he/she is consulting.
