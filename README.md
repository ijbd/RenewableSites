# Renewable Sites Python Module

This module is used as an interface between the [powGen-wtk-nsrdb](https://github.com/ijbd/powGen-wtk-nsrdb) capacity factor outputs and the [EquitableRetirement](https://github.com/ijbd/EquitableRetirement) optimization formulation. CSV outputs from `powGen-wtk-nsrdb` are placed in the data folder, and values are extracted with the `getAnnualCF` and `getHourlyCF` functions. Both functions return a pandas DataFrame with site latitudes, longitudes, and capacity factors at their corresponding time frames. 

## Simple Use

1. Clone:

        git clone https://github.com/ijbd/RenewableSites.git

2. Given the following file structure:

        Project
        |--main.py
        |--solar_cf_<powGen-params>.csv
        |--wind_cf_<powGen-params>.csv
        |--RenewableSites
            |--RenewableSites.py
            
3. Use the `RenewableSites` module from main:

        ### main.py ###
        from RenewableSites import RenewableSites

        # Get annual capacity factors from default data files
        renewableSites = RenewableSites.getAnnualCF(solar_cf_<powGen-params>.csv, wind_cf_<powGen-params>.csv)

        # Get hourly capacity factors from default data files
        renewableSites = RenewableSites.getHourlyCF(solar_cf_<powGen-params>.csv, wind_cf_<powGen-params>.csv)

**Note:** The returned DataFrames include columns for each site's latitude and longitude *in addition to* capacity factors. To return capacity factors without latitudes and longitudes, use `RenewableSites.getHourlyCF(...,cf_only=True)`.
