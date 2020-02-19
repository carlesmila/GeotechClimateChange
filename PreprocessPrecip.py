#####################################################
#           Preprocess precipitation data           #
#####################################################

# Import standard modules
import pandas as pd
from netCDF4 import Dataset, num2date

# Import our tailored module
import PreprocessUtils as ut

# Read NetCDF
file = 'Data/pr_wtr.mon.mean.nc'
nc = Dataset(file, mode='r')
# We store the four components (lon/lat/temp/time) in separate variables
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
precip = nc.variables['pr_wtr'][:]
time_var = nc.variables['time']

# We need to parse the time (extract year from months). First convert to date format.
dtime = num2date(time_var[:], time_var.units)
# Compute year of each of the dates
year = [row.year for row in dtime]

# We convert to pandas df and fix the longitudes (from -180 to 180)
names = ['year', 'lat', 'lon']
# We create a grid of possible vales
index = pd.MultiIndex.from_product([year, lat, lon], names=names)
# Add precipitation and keep indices as columns
dfp = pd.DataFrame({'precip': precip.flatten()}, index=index).reset_index()
# Fix coordinates with the function we defined in the PreprocessUtils module
dfp.lon = dfp.lon.transform(ut.convert_lons)

# We calculate yearly sum per pixel and discard data for 2020
dfp = dfp.groupby(['lon', 'lat', 'year']).sum().reset_index()
dfp = dfp[dfp.year != 2020]

# Calculate mean precipitation by pixel of the first 5 years as a reference
baseline = dfp[dfp.year <= 1952].groupby(['lon', 'lat']).mean().reset_index()
# Drop year column (we won't use it) and rename to baseline
baseline = baseline.drop(columns="year")
baseline = baseline.rename(columns={"precip": "baseline"})

# Now we merge the main table and the baseline and compute pixel-based anomalies by subtraction
dfp = pd.merge(left=dfp, right=baseline, left_on=['lon', 'lat'], right_on=['lon', 'lat'])
dfp['precipanom'] = (dfp['precip'] - dfp['baseline'])
dfp = dfp.drop(columns="baseline") # We don't need it anymore

# Now we compute trends by applying our function defined in the PreprocessUtils module to each pixel
preciptrends = dfp.groupby(['lat', 'lon']).apply(ut.extract_trend, indicator='precip').reset_index()
# We rename the components to make them specific to precipitation
preciptrends = preciptrends.rename(columns={"constant": "precipconstant",
                                            "slope": "precipslope",
                                            "trend": "preciptrend"})