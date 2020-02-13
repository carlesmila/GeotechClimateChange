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
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]

# We convert to pandas df and fix the longitudes (from -180 to 180)
names = ['lat', 'lon']
index = pd.MultiIndex.from_product([lat, lon], names=names)
dfu = pd.DataFrame(index=index).reset_index()
dfu.lon = dfu.lon.transform(ut.convert_lons)

# Create grid
file = 'Data/air.mon.mean.nc'
nc = Dataset(file, mode='r')
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]

dfu = gpd.GeoDataFrame(dfu,
                       geometry=gpd.points_from_xy(dfu.lon, dfu.lat),
                       crs={'init': 'epsg:4326'})

# Read country data, select and rename country names, and do spatial join to extract the country of the pixel
country = gpd.read_file('Data/countries.geojson').loc[:, ['NAME_EN', 'geometry']]
country = country.rename(columns={'NAME_EN': 'countryname'})
dfu = gpd.sjoin(dfu, country, how='left').loc[:, ['lon', 'lat', 'countryname', 'geometry']]
dfu.countryname = dfu.countryname.fillna('Water body')

# Next, let's add climate zones
climatezones = gpd.read_file('Data/climatezones.geojson')
dfu = gpd.sjoin(dfu, climatezones, how='left').loc[:, ['lon', 'lat', 'countryname', 'climate']]
dfu = dfu.drop_duplicates(subset=['lon', 'lat'], keep='last')


