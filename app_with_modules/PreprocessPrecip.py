#####################################################
#           Preprocess precipitation data           #
#####################################################

# Standard modules
import pandas as pd
from netCDF4 import Dataset, num2date

# Our tailored module
import PreprocessUtils as ut

# Read NetCDF
file = 'Data/pr_wtr.mon.mean.nc'
nc = Dataset(file, mode='r')
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
precip = nc.variables['pr_wtr'][:]
time_var = nc.variables['time']

# We need to parse the time (extract year from months)
dtime = num2date(time_var[:], time_var.units)
year = [row.year for row in dtime]
names = ['year', 'lat', 'lon']

# We convert to pandas df and fix the longitudes (from -180 to 180)
index = pd.MultiIndex.from_product([year, lat, lon], names=names)
dfp = pd.DataFrame({'precip': precip.flatten()}, index=index).reset_index()
dfp.lon = dfp.lon.transform(ut.convert_lons)

# We calculate yearly sum per pixel and discard data for 2020
dfp = dfp.groupby(['lon', 'lat', 'year']).sum().reset_index()
dfp = dfp[dfp.year != 2020]

# Calculate mean precipitation of the first 5 years
baseline = dfp[dfp.year <= 1952].groupby(['lon', 'lat']).mean().reset_index()
baseline = baseline.drop(columns="year")
baseline = baseline.rename(columns={"precip": "baseline"})

# Merge with main table and compute anomalies
dfp = pd.merge(left=dfp, right=baseline, left_on=['lon', 'lat'], right_on=['lon', 'lat'])
dfp['precipanom'] = (dfp['precip'] - dfp['baseline'])
dfp = dfp.drop(columns="baseline")

# Now we compute trends
preciptrends = dfp.groupby(['lat', 'lon']).apply(ut.extract_trend, indicator='precip').reset_index()
preciptrends = preciptrends.rename(columns={"constant": "precipconstant",
                                            "slope": "precipslope",
                                            "trend": "preciptrend"})