#####################################################
#                    Check cache                    #
#####################################################

import sqlite3
import os
import pandas as pd
import numpy as np
from netCDF4 import Dataset, num2date

# First, check cache. Check if the database already exists
if os.path.isfile('Database/database.sqlite'):
    print("The database is cached, preprocessing is skipped!")

else:
    print("Running pre-processing...")

    # Pre-processing
    file = 'Data/air.mon.mean.nc'
    nc = Dataset(file, mode='r')
    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    air = nc.variables['air'][:]
    time_var = nc.variables['time']
    dtime = num2date(time_var[:], time_var.units)
    tmp_lon = np.array([lon[n]-360 if l>=180 else lon[n]
                   for n,l in enumerate(lon)])  # => [0,180]U[-180,2.5]
    i_east, = np.where(tmp_lon>=0)
    i_west, = np.where(tmp_lon<0)
    lon = np.hstack((tmp_lon[i_west], tmp_lon[i_east]))
    year = [row.year for row in dtime]
    names = ['year', 'lat', 'lon']
    lon2 = nc.variables['lon'][:]
    index = pd.MultiIndex.from_product([year, lat, lon2], names=names)
    df = pd.DataFrame({'Air': air.flatten()}, index=index).reset_index()
    def convert_lons(l):
        if l > 180:
            return l - 360
        else:
            return l
    df.lon = df.lon.transform(convert_lons)
    df = df.groupby(['lon','lat','year']).mean().reset_index()
    df = df[df.year != 2020]

    # If the folder does not exist, create it
    if not os.path.exists("Database"):
        os.makedirs("Database")

    # Write database
    conn = sqlite3.connect('Database/database.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE MAINTEMP
                 ([generated_id] INTEGER PRIMARY KEY,[lon] FLOAT, [lat] integer, [year] INTEGER, [air] FLOAT)''')
    df.to_sql('MAINTEMP', conn, if_exists='replace', index=False)
    conn.commit()

    # df.to_csv('Database/database.csv')

    print('Data preprocessed and database created!')