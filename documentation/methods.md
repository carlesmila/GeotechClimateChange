# Methods

We structured our app as indicated in the following figure:
![alt text](figures/workflow.png?raw=true)

The root script of our app, which is needed to execute to run the application is structured in three blocks. First, it calls the preprocessing (backend) module, then calls the layout and callback module (frontend), and finally runs the app. This script is available [here](https://github.com/carlesmila/GeotechClimateChange/blob/master/app.py). In the following subsections each of these steps will be explained in detail.

## Backend

The first step in the backend is to check whether a cache for the app exists, i.e. whether a sqlite with the data needed to run the app exists. If the answer this logical operation is positive, then all preprocessing (backend) modules are skipped and we jump into the frontend definition. If, however, it is not, they do need to be run. The motivation behind the cache is to avoid unnecessary processing when running the app while also considering updates in the database when new data are available. The code of this first backend module is available [here](https://github.com/carlesmila/GeotechClimateChange/blob/master/CheckCachePreprocess.py).

The first step of the preprocessing is to prepare the temperature data to be used in the app. The most important steps in this module are to read the temperature in the raw NetCDF file and transform it to pandas, fix the longitudes of the file to correspond to a WGS1984 coordinate reference system, to compute pixel-based temperature yearly averages from the monthly data, to calculate the temperature baseline (mean temperature between 1948-1952) and compute the difference between temperature in a given year and baseline. Furthermore, the linear trend of each pixel was computed as a linear regression model (temperature~time), and the values of the estimated intercepts and slopes were saved in an additional table, although we did not use these data in the current version of the app. The module in charge of the temperature preprocessing is available [here](https://github.com/carlesmila/GeotechClimateChange/blob/master/PreprocessTemp.py). 

The same steps were also performed for precipitable water, except for the fact that yearly pixel-based sums were extracted for the monthly data rather than yearly pixel-based means, and were coded in another module available [here](https://github.com/carlesmila/GeotechClimateChange/blob/master/PreprocessPrecip.py). Both temperature and precipitable water pre-processing used similar functions for longitude correction and linear trend extraction, which we defined in an additional utils module that can be consulted [here](https://github.com/carlesmila/GeotechClimateChange/blob/master/PreprocessUtils.py).

## Frontend

Link to frontend [here](https://github.com/carlesmila/GeotechClimateChange/blob/master/DefineApp.py).

## Deployment

The application was deployed using PythonAnywhere, an online development and web hosting service that uses Python programming language. Within the PythonAnywhere webpage, it is possible to create a virtual environment using Python version 3.7 (or other version) and install all the dependencies the application requires to run. The Python Web Framework used for this app was Flask. After uploading all files (data and codes) to the website platform, the working directory was set as well as the server details through the Web Server Gateway Interface (WSGI) configuration file.

Initially, we tried to deploy the application using the cloud platform Heroku (and its command line interface), which supports many programming languages including Python, Java, Node.js, Scala and PHP. However, after performing the required steps to deploy the app and make it available online, Heroku presented an unexpected error related to memory quota consumption even though the application was not big. The source of this error was not tracked, and this solution could not be adopted for this project.
