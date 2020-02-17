#####################################################
#      Preprocess pixel-based common indicators     #
#####################################################

import pandas as pd
import geopandas as gpd
from netCDF4 import Dataset, num2date
# Our tailored module
import PreprocessUtils as ut

# Read NetCDF
file = 'Data/air.mon.mean.nc'
nc = Dataset(file, mode='r')
# We store lat and lon in separate variables
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]

# We convert to pandas df and fix the longitudes (from -180 to 180)
names = ['lat', 'lon']
index = pd.MultiIndex.from_product([lat, lon], names=names)
dfu = pd.DataFrame(index=index).reset_index()
# Fix longitudes with the function we defined in the PreprocessUtils module
dfu.lon = dfu.lon.transform(ut.convert_lons)

# Create geopandas spatial object from pandas table (WGS84) as pixel grid
dfu = gpd.GeoDataFrame(dfu,
                       geometry=gpd.points_from_xy(dfu.lon, dfu.lat),
                       crs={'init': 'epsg:4326'})

# Read country data, select and rename country names
country = gpd.read_file('Data/countries.geojson').loc[:, ['NAME_EN', 'geometry']]
country = country.rename(columns={'NAME_EN': 'countryname'})
# Do spatial join to extract the country of each pixel
dfu = gpd.sjoin(dfu, country, how='left').loc[:, ['lon', 'lat', 'countryname', 'geometry']]
# Pixels for which we got no result fall on water, fill with string
dfu.countryname = dfu.countryname.fillna('Water body')

# Next, let's add climate zones. Read file.
climatezones = gpd.read_file('Data/climatezones.geojson')
# And perform spatial join
dfu = gpd.sjoin(dfu, climatezones, how='left').loc[:, ['lon', 'lat', 'countryname', 'climate']]
# For some record we got duplicates (more than one climate zone per point). Take the last match.
dfu = dfu.drop_duplicates(subset=['lon', 'lat'], keep='last')