# Check the working directory
import os
os.getcwd()

# Import modules
import datetime as dt 
import numpy as np
from netCDF4 import Dataset 
# install using in cmd: pip install netCDF4
# Make sure pip.exe is in your environment path!
# Mine was in: C:\Users\carle\Anaconda3\Scripts
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
# Download using in cmd: conda install -c https://conda.anaconda.org/anaconda basemap
# I needed to set my environment variable "myUsername" to make it work