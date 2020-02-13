#####################################################
#       Preprocessing functions that we'll use      #
#####################################################

# Auxiliary modules we need to run our utils
import statsmodels.api as sm
import pandas as pd

# Now we define our functions
def convert_lons(l):
    """Fixes warped longitudes in the original NetCDF files to WGS84"""
    if l > 180:
        return l - 360
    else:
        return l

def extract_trend(gdf): # I need to document
    """Calculates linear trends using linear regression"""
    # Fit a linear regression with intercept
    mod = sm.OLS(gdf['temp'], sm.add_constant(gdf['year'])).fit()
    # Extract coefficients, intercept and slope
    constant = mod.params[0]
    slope = mod.params[1]
    # Write a nice string for the trend to show in a graph
    slope10 = str(round(mod.params[1] * 10, 2))
    lower10 = str(round(mod.conf_int()[0][1] * 10, 2))
    upper10 = str(round(mod.conf_int()[1][1] * 10, 2))
    trend = slope10 + 'ºC (95% CI: ' + lower10 + ', ' + upper10 + ') every 10 years'
    # Return a series that can be stacked when used with groupby +  apply
    return pd.Series({'constant': constant, 'slope': slope, ' trend': trend})