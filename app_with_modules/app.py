#####################################################
#               Makefile of the app                 #
#####################################################

# To be run in pycharm

## REQUIREMENTS:
# A folder called "Data" with two files, "air.mon.mean.nc" and "basemap.npy"
# A folder called "Assets" with the file "s1.css"
# The following scripts: "CheckCachePreprocess.py" and "DefineApp.py"

# Moreover, the following modules must be installed:
# (here we will list them)

## 1. Check cache and preprocess
# This module checks whether there is an adequate cache stored. If not, it performs pre-processing and stores results
# in a database. If it is, this step is ignored.
# noinspection PyUnresolvedReferences
import CheckCachePreprocess

## 2. Prepare app
# This module defines the app and makes it ready to be used
# noinspection PyUnresolvedReferences
import DefineApp

## 3. Time to run the app!
DefineApp.app.run_server(debug=False)