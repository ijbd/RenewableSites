'''
ijbd
4/2/2021

This is a complementary script providing an interface for accessing the capacity factors from `powGen-wtk-nsrdb.py` output.

'''
import numpy as np
import pandas as pd
import os

def _getAnnualCF(filename, cf_only=False):
    re = pd.read_csv(filename,index_col=0)

    # get locations
    lats = [float(c.split()[0]) for c in re.columns]
    lons = [float(c.split()[1]) for c in re.columns]
    
    cf = pd.DataFrame()
    if not cf_only:
        cf['Latitude'] = lats
        cf['Longitude'] = lons
    cf['Annual CF'] = np.average(re.values.T,axis=1)

    return cf

def getAnnualCF(solar_filename, wind_filename, cf_only=False):
    '''
    Args
    -------
        `solar_filename` (str) : Absolute path to the solar capacity factor file.
        `wind_filename` (wind) : Absolute path to the wind capacity factor file.

    Returns
    -------
        `renewableSites` (pd.Series) : Series of lat/lons
    '''
    solar = _getAnnualCF(solar_filename, cf_only)
    if not cf_only:
        solar['Technology'] = 's'

    wind = _getAnnualCF(wind_filename, cf_only)
    if not cf_only:
        wind['Technology'] = 'w'

    renewableSites = solar.append(wind)

    return renewableSites

def _getHourlyCF(filename, cf_only):
    re = pd.read_csv(filename,index_col=0)

    # get locations
    lats = [float(c.split()[0]) for c in re.columns]
    lons = [float(c.split()[1]) for c in re.columns]
    
    cf = pd.DataFrame()
    cf['Latitude'] = lats
    cf['Longitude'] = lons
    gen = re.values.T

    for i in range(gen.shape[1]):
        cf['Hr {}'.format(i)] = gen[:,i]

    return cf

def getHourlyCF(solar_filename, wind_filename, cf_only=False):
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
