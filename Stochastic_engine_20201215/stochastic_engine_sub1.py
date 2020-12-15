# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 18:51:25 2020

@author: 11487
"""

import time
import sys
from shutil import copyfile

# %% settings
# Specify a number of synthetic weather years to be simulated. Then
# edit the /cord/data/input/base_inflows.json file, specifying the start and end 
# dates of the forecast_exp scenario flow files. Start date must be 1/1/1901.
# End dates must be stoch_years + 3 after start date. 

stoch_years=1000;yearbeg=2005;yearend=2034;
stoch_years2=stoch_years+3;
start_year=1901;
# %% DAILY HYDROPOWER SIMULATION
# Now specify a smaller subset of stochastic data to run (must be < stoch years)
sim_years = 999


# Run ORCA to get California storage dam releases
#%% change the end year by adding the start year with sim_years;
import json
file='cord/data/input/base_inflows.json'; file2='cord/data/input/base_inflows00.json'
from shutil import copyfile
try:
    copyfile(file2,file)
except:
    copyfile(file,file2)
    copyfile(file2,file)
    
with open(file) as f:
  datas = json.load(f)

datas['file_start']['forecast_exp']['F_flow']=str('1/1/{}'.format(start_year));  
datas['simulation_period_start']['forecast_exp']['F_flow']=start_year;

datas['file_end']['forecast_exp']['F_flow']=str('12/31/{}'.format(start_year+stoch_years2-1));
datas['simulation_period_end']['forecast_exp']['F_flow']=start_year+stoch_years2-1;
# datas['inflow_series']['forecast_exp']['F_flow']='cord/data/input/forecast_flows_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)

with open(file, 'w') as f:
    json.dump(datas, f, indent=4)



# %% 1. Run ORCA to get California storage dam releases   
#  copy the streamflow file to targeted directory
src='Synthetic_streamflows/forecast_flows_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
dst='cord/data/input/forecast_flows.csv' # this filename is used by default in CA_hydropower
copyfile(src, dst)

starttime = time.time()
print('ORCA', file=sys.stderr)
print('will be running for {} seconds'.format(120*(sim_years+4)), file=sys.stderr)
sys.stdout.flush()

import main
main.sim(sim_years)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)

# %% 2. California Hydropower model
src='Synthetic_streamflows/synthetic_streamflows_CA_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
dst='Synthetic_streamflows/synthetic_streamflows_CA.csv' # this filename is used by default in CA_hydropower
copyfile(src, dst)


print('CA hydropower', file=sys.stderr)
print('will be running for {} seconds'.format(10*(sim_years+1)), file=sys.stderr)
starttime = time.time()

import CA_hydropower
CA_hydropower.hydro(sim_years)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)

# %% 3. Willamette operational model
src='Synthetic_streamflows/synthetic_streamflows_Willamette_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
dst='Synthetic_streamflows/synthetic_streamflows_Willamette.csv' # this filename is used by default in CA_hydropower
copyfile(src, dst)
    
print('Willamette', file=sys.stderr)
print('will be running for {} seconds'.format(146*(sim_years+3)), file=sys.stderr)
starttime = time.time()

import Willamette_launch
Willamette_launch.launch(sim_years)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)

# %% 4. Federal Columbia River Power System Model (mass balance in Python)
src='Synthetic_streamflows/synthetic_streamflows_TDA_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
dst='Synthetic_streamflows/synthetic_streamflows_TDA.csv' # this filename is used by default in CA_hydropower
copyfile(src, dst)
src='Synthetic_streamflows/synthetic_streamflows_FCRPS_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
dst='Synthetic_streamflows/synthetic_streamflows_FCRPS.csv' # this filename is used by default in CA_hydropower
copyfile(src, dst)


print('FCRPS', file=sys.stderr)
print('will be running for {} seconds'.format(0.01*sim_years), file=sys.stderr)
starttime = time.time()


import ICF_calc
ICF_calc.calc(sim_years)
import FCRPS
FCRPS.simulate(sim_years)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)

# %%  HOURLY WIND AND SOLAR POWER PRODUCTION
## WIND
# Specify installed capacity of wind power for each zone
PNW_cap = 6445
CAISO_cap = 4915

# Generate synthetic hourly wind power production time series for the BPA and
# CAISO zones for the entire simulation period


# %% 2.1 Generate synthetic hourly wind power production time series for the BPA and CAISO zones for the entire simulation period
src='Synthetic_weather/synthetic_weather_data_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
dst='Synthetic_weather/synthetic_weather_data.csv'
copyfile(src, dst)

print('wind', file=sys.stderr)
print('will be running for {} seconds'.format(80*(sim_years+3)), file=sys.stderr)
starttime = time.time()

import wind_speed2_wind_power
wind_speed2_wind_power.wind_sim(sim_years,PNW_cap,CAISO_cap)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)

#%% 2.2 SOLAR
# Specify installed capacity of wind power for each zone
CAISO_solar_cap = 9890



src='Synthetic_weather/synthetic_irradiance_data_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
dst='Synthetic_weather/synthetic_irradiance_data.csv'
copyfile(src, dst)

print('solar', file=sys.stderr)
print('will be running for {} seconds'.format(47*(sim_years+3)), file=sys.stderr)
starttime = time.time()

# Generate synthetic hourly solar power production time series for 
# the CAISO zone for the entire simulation period
import solar_production_simulation
solar_production_simulation.solar_sim(sim_years,CAISO_solar_cap)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)
##############################################################################
#%%
##############################################################################
# ELECTRICITY DEMAND AND TRANSMISSION PATH FLOWS

# Calculate daily peak and hourly electricity demand for each zone and daily 
# flows of electricity along each WECC path that exchanges electricity between
# core UC/ED model (CAISO, Mid-C markets) and other WECC zones

src='Synthetic_weather/synthetic_weather_data_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
dst='Synthetic_weather/synthetic_weather_data.csv'
copyfile(src, dst)
src='Synthetic_streamflows/synthetic_discharge_Hoover_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
dst='Synthetic_streamflows/synthetic_discharge_Hoover.csv'
copyfile(src, dst)
print('paths')
print('will be running for {} seconds'.format(54*(sim_years+3)), file=sys.stderr)
starttime = time.time()
import demand_pathflows
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)
##############################################################################
#
##############################################################################
# %%NATURAL GAS PRICES

# NOTE: NEED SCRIPT HERE TO SIMULATE STOCHASTIC NATURAL GAS PRICES 
# *OR*
# ESTIMATE STATIC GAS PRICES FOR EACH ZONE

import numpy as np
ng = np.ones((sim_years*365,5))
ng[:,0] = ng[:,0]*4.47
ng[:,1] = ng[:,1]*4.47
ng[:,2] = ng[:,2]*4.66
ng[:,3] = ng[:,3]*4.66
ng[:,4] = ng[:,4]*5.13

import pandas as pd
NG = pd.DataFrame(ng)
NG.columns = ['SCE','SDGE','PGE_valley','PGE_bay','PNW']
NG.to_excel('Gas_prices/NG.xlsx')

