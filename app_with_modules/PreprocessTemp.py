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
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
temp = nc.variables['air'][:]
time_var = nc.variables['time']

# We need to parse the time (extract year from months)
dtime = num2date(time_var[:], time_var.units)
year = [row.year for row in dtime]
names = ['year', 'lat', 'lon']

# We convert to pandas df and fix the longitudes (from -180 to 180)
index = pd.MultiIndex.from_product([year, lat, lon], names=names)
dft = pd.DataFrame({'temp': temp.flatten()}, index=index).reset_index()
dft.lon = dft.lon.transform(ut.convert_lons)

# We calculate yearly averages per pixel and discard data for 2020
dft = dft.groupby(['lon', 'lat', 'year']).mean().reset_index()
dft = dft[dft.year != 2020]

# Calculate mean temperatures of the first 5 years
baseline = dft[dft.year <= 1952].groupby(['lon', 'lat']).mean().reset_index()
baseline = baseline.drop(columns="year")
baseline = baseline.rename(columns={"temp": "baseline"})

# Merge with main table and compute anomalies
dft = pd.merge(left=dft, right=baseline, left_on=['lon', 'lat'], right_on=['lon', 'lat'])
dft['tempanom'] = (dft['temp'] - dft['baseline'])
dft = dft.drop(columns="baseline")

# Now we compute trends
temptrends = dft.groupby(['lat', 'lon']).apply(ut.extract_trend, indicator='temp').reset_index()
temptrends = temptrends.rename(columns={"constant": "tempconstant",
                                        "slope": "tempslope",
                                        "trend": "temptrend"})