#####################################################
#             Preprocess temperature data           #
#####################################################

# Standard modules
import pandas as pd
from netCDF4 import Dataset, num2date

# Our tailored module
import PreprocessUtils as ut

# Read NetCDF
file = 'Data/air.mon.mean.nc'
nc = Dataset(file, mode='r')
# We store the four components (lon/lat/temp/time) in separate variables
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
temp = nc.variables['air'][:]
time_var = nc.variables['time']

# We need to parse the time (extract year from months). First convert to date format.
dtime = num2date(time_var[:], time_var.units)
# Compute year of each of the dates
year = [row.year for row in dtime]

# We convert to pandas df and fix the longitudes (from -180 to 180)
names = ['year', 'lat', 'lon']
# We create a grid of possible vales
index = pd.MultiIndex.from_product([year, lat, lon], names=names)
# Add temperature and keep indices as columns
dft = pd.DataFrame({'temp': temp.flatten()}, index=index).reset_index()
# Fix coordinates with the function we defined in the PreprocessUtils module
dft.lon = dft.lon.transform(ut.convert_lons)

# We calculate yearly averages per pixel and discard data for 2020 (incomplete)
dft = dft.groupby(['lon', 'lat', 'year']).mean().reset_index()
dft = dft[dft.year != 2020]

# Calculate mean temperature by pixel of the first 5 years as a reference
baseline = dft[dft.year <= 1952].groupby(['lon', 'lat']).mean().reset_index()
# Drop year column (we won't use it) and rename to baseline
baseline = baseline.drop(columns="year")
baseline = baseline.rename(columns={"temp": "baseline"})

# Now we merge the main table and the baseline and compute pixel-based anomalies by subtraction
dft = pd.merge(left=dft, right=baseline, left_on=['lon', 'lat'], right_on=['lon', 'lat'])
dft['tempanom'] = (dft['temp'] - dft['baseline'])
dft = dft.drop(columns="baseline") # We don't need it anymore

# Now we compute trends by applying our function defined in the PreprocessUtils module to each pixel
temptrends = dft.groupby(['lat', 'lon']).apply(ut.extract_trend, indicator='temp').reset_index()
# We rename the components to make them specific to temperature
temptrends = temptrends.rename(columns={"constant": "tempconstant",
                                        "slope": "tempslope",
                                        "trend": "temptrend"})