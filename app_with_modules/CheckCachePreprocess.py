#####################################################
#                    Check cache                    #
#####################################################

import sqlite3
import os
import pandas as pd
import geopandas as gpd

# First, check cache. Check if the database already exists, if yes don't do anything
if os.path.isfile('Database/database.sqlite'):
    print("The database is cached, preprocessing is skipped!")

else:
    # Otherwise process data
    print("Cache not found, running pre-processing...")

    # Process temperature
    print("1. Processing temperature data. This may take a while.")
    import PreprocessTemp as ptemp

    # Process precipitation
    print("2. Processing precipitation data. This may take a while.")
    import PreprocessPrecip as pprecip

    # Derive pixel-based common indicators
    print("3. Processing pixel-based common indicators")
    import PreprocessCommon as pcom

    # Merge tables and make them ready to be uploaded
    print("4. Merging tables")
    dfshort = pd.merge(left=pcom.dfu, right=ptemp.temptrends, left_on=['lon', 'lat'], right_on=['lon', 'lat'])
    dfshort = pd.merge(left=dfshort, right=pprecip.preciptrends, left_on=['lon', 'lat'], right_on=['lon', 'lat'])
    dflong = pd.merge(left=ptemp.dft, right=pprecip.dfp, left_on=['lon', 'lat', 'year'], right_on=['lon', 'lat', 'year'])

    # Create database
    print("5. Creating database")
    # If the folder of the database does not exist, create it
    if not os.path.exists("Database"):
        os.makedirs("Database")
    # Write database: Two tables, main and supp
    conn = sqlite3.connect('Database/database.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE TEMPTAB
                 ([generated_id] INTEGER PRIMARY KEY,[lon] FLOAT, [lat] integer, [year] INTEGER, 
                 [temp] FLOAT, [tempanom] FLOAT, [precip] FLOAT, [precipanom] FLOAT)''')
    dflong.to_sql('TEMPTAB', conn, if_exists='replace', index=False)
    c.execute('''CREATE TABLE FIXEDTAB
                     ([generated_id] INTEGER PRIMARY KEY,[lon] FLOAT, [lat] integer, 
                     [countryname] STRING, [climatezone] STRING,
                     [tempconstant] FLOAT, [tempslope] FLOAT, [temptrend] STRING,
                     [precipconstant] FLOAT, [precipslope] FLOAT, [preciptrend] STRING)''')
    dfshort.to_sql('FIXEDTAB', conn, if_exists='replace', index=False)
    conn.commit()

    # We're done!
    print('Data preprocessed and database created! :)')