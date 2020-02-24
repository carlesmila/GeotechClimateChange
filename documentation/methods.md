# Methods

We structured our app as indicated in the following figure:
![alt text](figures/workflow.png?raw=true)

The root script of our app, which is needed to execute to run the application is structured in three blocks. First, it calls the preprocessing (backend) module, then calls the layout and callback module (frontend), and finally runs the app. This script is available in [app.py](https://github.com/carlesmila/GeotechClimateChange/blob/master/app.py). In the following subsections each of these steps will be explained in detail.

## Backend

The first step in the backend is to check whether a cache for the app exists, i.e. whether a sqlite with the data needed to run the app exists. If the answer this logical operation is positive, then all preprocessing (backend) modules are skipped and we jump into the frontend definition. If, however, it is not, they do need to be run. The motivation behind the cache is to avoid unnecessary processing when running the app while also considering updates in the database when new data are available. The cache check code is available in the first part of [CheckCachePreprocess.py](https://github.com/carlesmila/GeotechClimateChange/blob/master/CheckCachePreprocess.py) script.

The first step of the preprocessing is to prepare the temperature data to be used in the app. The most important steps in this module are to read the temperature in the raw NetCDF file and transform it to a pandas data frame, fix the longitudes to correspond to a WGS1984 coordinate reference system, compute pixel-level temperature yearly averages from the monthly data, to calculate the pixel-level temperature baseline (mean temperature between 1948-1952) and compute the pixel-level difference between temperature in a given year and baseline. The resulting data are stored in a pandas data frame indexed by the pixel coordinates and year (i.e. one row per pixel per year). Furthermore, the pixel-level linear trend is computed as a linear regression model (temperature~time) and the values of the estimated intercepts and slopes are saved in an additional pandas table indexed by the pixel coordinates (i.e. one row per pixel), although we did not use these data in the current version of the app. The module in charge of the temperature preprocessing is available in [PreprocessTemp.py](https://github.com/carlesmila/GeotechClimateChange/blob/master/PreprocessTemp.py). 

The same steps are also performed for precipitable water, except for the fact that yearly pixel-level sums were extracted for the monthly data rather than yearly pixel-based means. The precipatable water preprocessing module is available in [PreprocessPrecip.py](https://github.com/carlesmila/GeotechClimateChange/blob/master/PreprocessPrecip.py). Both temperature and precipitable water preprocessing use the same functions for longitude correction and linear trend extraction, which we define in an additional utils module that can be consulted in [PreprocessUtils.py](https://github.com/carlesmila/GeotechClimateChange/blob/master/PreprocessUtils.py).

The next step is to extract time-invariant additional information at the pixel level, namely the country and climate that correspond to each pixel. To do so, the coordinate grid is converted into a geopandas object, and we perform spatial join to extract the country names and climate zone using auxiliary polygon data. For areas with no country/climate area, the pixel is labelled to be water body. The resulting data is stored in a pandas dataframe indexed by the pixel coordinates (i.e. one row per pixel). The code of this model is available in the [PreprocessCommon.py](https://github.com/carlesmila/GeotechClimateChange/blob/master/PreprocessCommon.py) script.

The last step in the preprocessing is to group all the data into two different pandas tables by joining tables. The first table is called TEMPTAB and is indexed by the pixel coordinates (lon, lat) and time, and contains temperature, precipitable water, and deviations from the respective baselines. The second table is called FIXEDTAB and is indexed by the coordinates (lon, lat), and contains the country, climate area, and temperature and precipitable water of each pixel. These two tables are then stored into an sqlite database that will be read in the frontend. This module is available in the last part of the [CheckCachePreprocess.py](https://github.com/carlesmila/GeotechClimateChange/edit/master/documentation/methods.md) script.

## Frontend

Given our previously defined objectives, what we needed was a library able to visualize data and create interactive plots. To do so, we decided to implement Plotly and Dash for building our frontend.
Plotly is both a company and an open source library that focuses on visualizations as .html files, however, it does not allow to connect our plots to changing data sources and comes with the limitation to re-run the .py script and re-generate the .html file to see any updates. What we needed for this app were plots able to interact with each other and to update in real time; to do so an interactive dashboard was the best option. Dash is a step beyond what Plotly can provide for us. It is a library from the Plotly company that, instead of a .html file, produces a dashboard web application at a local URL, all this using purely Python, since most .html tags are provided as Python classes. Implementing such solution, we were able to deploy our dashboard online for the public to use.

Let’s have a closer look to the way our frontend is organized.
As mentioned in previous sections, the entire process was carried out using PyCharm Python IDE. We started off by importing all the needed modules (pandas, plotly.graph_objs, numpy, dash, dash.dependencies, dash_html_components, dash_core_components and sqlite3) and querying our database; at this point, the actual frontend ([DefineApp.py](https://github.com/carlesmila/GeotechClimateChange/blob/master/DefineApp.py).) was divided into 2 sections:

1.	Creating the layout
2.	Creating 4 callbacks

Through the layout section we describe where our visualizations inside the application are going to be. To do so, we defined html division using dash html components as well as more complex elements such as tabs, slider and radio items using dash core components.
Our layout is composed of three tabs (“Temperature”, “Precipitable water” and “About”), where the last one is defined by a simple markdown, while the first two have a more complex structure that we are now going to briefly explain.
Inside the “Temperature” tab, we inserted:

- a title, defining the instructions for the user
- a slider, allowing the user to select a preferred year
-	a radio item element, allowing to choose which variable the user wants to visualize (yearly average temperatures or difference from a baseline)
-	a map with its legend, in a form of a raster graph, displaying the chosen variable
-	a line graph with its legend, showing on the x-axis the year and on the y-axis the chosen variable
The same schema was used for the “Precipitable water” tab.

Once the layout was set, we created a few callbacks in order to define the interactive part of our application. For both “Temperature” and “Precipitable water”, 2 callbacks were created.

-	The first callback has the purpose of, as an output, updating the figure displayed onto the raster graph created using Plotly (placed on the left-hand side or our layout) by taking as inputs the year selected from the slider as well as the variable chosen from the radio items element.

-	The second callback was created so as to update the line graph placed on the right-hand side of our layout, taking as inputs the year selected from the slider as well as the coordinates (clickData) defining the location clicked by the user. For this second callback, we defined as outputs both the line graph as well as showing the country name and climate zone of the selected location.

The same schema was used for the “Precipitable water” tab.

## Deployment

The application was deployed using PythonAnywhere, an online development and web hosting service that uses Python programming language. Within the PythonAnywhere webpage, it is possible to create a virtual environment using Python version 3.7 (or other version) and install all the dependencies the application requires to run. The Python Web Framework used for this app was Flask. After uploading all files (data and codes) to the website platform, the working directory was set as well as the server details through the Web Server Gateway Interface (WSGI) configuration file.

Initially, we tried to deploy the application using the cloud platform Heroku (and its command line interface), which supports many programming languages including Python, Java, Node.js, Scala and PHP. However, after performing the required steps to deploy the app and make it available online, Heroku presented an unexpected error related to memory quota consumption even though the application was not big. The source of this error was not tracked, and this solution could not be adopted for this project.
