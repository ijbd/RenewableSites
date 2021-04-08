'''
ijbd
4/2/2021

This is a complementary script providing an interface for accessing the capacity factors from `powGen-wtk-nsrdb.py` output.

'''
import numpy as np
import pandas as pd
import os

local_path = os.path.dirname(__file__)

default_solar_filename = os.path.join(local_path,'default/solar_cf_NY_PA_OH_WV_KY_TN_VA_MD_DE_NC_NJ_0.5_2014.csv')
default_wind_filename = os.path.join(local_path,'default/wind_cf_NY_PA_OH_WV_KY_TN_VA_MD_DE_NC_NJ_0.5_2014.csv')

def getAnnualCF(solar_filename=default_solar_filename, wind_filename=default_wind_filename, cf_only=False):
    '''
    Args
    -------
        `solar_filename` (str) : Absolute path to the solar capacity factor file.
        `wind_filename` (wind) : Absolute path to the wind capacity factor file.

    Returns
    -------
        `renewableSites` (pd.Series) : Series of lat/lons
    '''
    solar = pd.read_csv(solar_filename,index_col=0)
    wind = pd.read_csv(wind_filename,index_col=0)

    # get locations
    solarLats = [float(c.split()[0]) for c in solar.columns]
    solarLons = [float(c.split()[1]) for c in solar.columns]
    windLats = [float(c.split()[0]) for c in wind.columns]
    windLons = [float(c.split()[1]) for c in wind.columns]

    # fill
    renewableSites = pd.DataFrame()
    if not cf_only:
        renewableSites['Latitude'] = np.append(solarLats,windLats)
        renewableSites['Longitude'] = np.append(solarLons,windLons)

    # get generation 
    solarGen = np.average(solar.values.T,axis=1)
    windGen = np.average(wind.values.T,axis=1)

    # Annual CF
    renewableSites['Annual CF'] = np.append(solarGen,windGen)

    return renewableSites

def getHourlyCF(solar_filename=default_solar_filename, wind_filename=default_wind_filename, cf_only=False):
    '''
    Args
    -------
        `solar_filename` (str) : Absolute path to the solar capacity factor file.
        `wind_filename` (wind) : Absolute path to the wind capacity factor file.

    Returns
    -------
        `renewableSites` (pd.Series) : Series of lat/lons
    '''
    solar = pd.read_csv(solar_filename,index_col=0)
    wind = pd.read_csv(wind_filename,index_col=0)

    # get locations
    solarLats = [float(c.split()[0]) for c in solar.columns]
    solarLons = [float(c.split()[1]) for c in solar.columns]
    windLats = [float(c.split()[0]) for c in wind.columns]
    windLons = [float(c.split()[1]) for c in wind.columns]

    # fill
    renewableSites = pd.DataFrame()
    if not cf_only:
        renewableSites['Latitude'] = np.append(solarLats,windLats)
        renewableSites['Longitude'] = np.append(solarLons,windLons)

    # get generation 
    solarGen = solar.values.T
    windGen = wind.values.T

    gen = np.concatenate((solarGen,windGen))

    # Annual CF
    for i in range(gen.shape[1]):
        renewableSites['Hour {} CF'.format(i)] = gen[:,i]

    return renewableSites
