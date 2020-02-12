#####################################################
#                    Check cache                    #
#####################################################

import sqlite3
import os
import pandas as pd
from netCDF4 import Dataset, num2date

# First, check cache. Check if the database already exists, if yes don't do anything
if os.path.isfile('Database/database.sqlite'):
    print("The database is cached, preprocessing is skipped!")

else:
    # Otherwise process data and create it
    print("Running pre-processing...")

    # Read NetCDF
    file = 'Data/air.mon.mean.nc'
    nc = Dataset(file, mode='r')
    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    air = nc.variables['air'][:]
    time_var = nc.variables['time']

    # We need to parse the time (extract year from months)
    dtime = num2date(time_var[:], time_var.units)
    year = [row.year for row in dtime]
    names = ['year', 'lat', 'lon']

    # We convert to pandas df and fix the longitudes (from -180 to 180)
    index = pd.MultiIndex.from_product([year, lat, lon], names=names)
    df = pd.DataFrame({'Air': air.flatten()}, index=index).reset_index()
    def convert_lons(l):
        if l > 180:
            return l - 360
        else:
            return l
    df.lon = df.lon.transform(convert_lons)

    # We calculate yearly averages per pixel and discard data for 2020
    df = df.groupby(['lon','lat','year']).mean().reset_index()
    df = df[df.year != 2020]

    # Calculate mean temperatures of the first 5 years
    baseline = df[df.year<=1952].groupby(['lon','lat']).mean().reset_index()
    baseline = baseline.drop(columns="year")
    baseline= baseline.rename(columns={"Air":"baseline"})
    
    # Merge with main table and compute anomalies
    df = pd.merge(left=df, right=baseline, left_on=['lon','lat'], right_on=['lon','lat'])
    df['anom'] =  (df['Air'] - df['baseline'] )
    df = df.drop(columns="baseline")

    # If the folder of the database does not exist, create it
    if not os.path.exists("Database"):
        os.makedirs("Database")

    # Write database
    conn = sqlite3.connect('Database/database.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE MAINTEMP
                 ([generated_id] INTEGER PRIMARY KEY,[lon] FLOAT, [lat] integer, [year] INTEGER, [Air] FLOAT, [anom] FLOAT)''')
    df.to_sql('MAINTEMP', conn, if_exists='replace', index=False)
    conn.commit()

    # We're done!
    print('Data preprocessed and database created!')