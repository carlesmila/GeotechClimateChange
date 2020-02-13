#####################################################
#               Makefile of the app                 #
#####################################################

## REQUIREMENTS:
# A folder called "Data" with four files: "air.mon.mean.nc", "basemap.npy", "climatezones.geojson", "countries.geojson"
# A folder called "Assets" with the file "s1.css"
# The following scripts: "CheckCachePreprocess.py", "DefineApp.py",
# "PreprocessTemp.py", "PreprocessUtils.py", "PreprocessCommon.py"

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