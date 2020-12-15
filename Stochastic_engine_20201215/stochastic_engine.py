# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 09:59:48 2018

@author: YSu
"""

############################################################################
# HISTORICAL WEATHER AND STREAMFLOW ANALYSIS

# Perform statistical analysis of historical meteorological data
# Note: this script ('calculatte_cov') only needs to be performed once; after
# that stochastic input generation can occur as many times as desired.
import time
import sys
#import calculate_cov
############################################################################

############################################################################
# STOCHASTIC WEATHER AND STREAMFLOW GENERATION

# Specify a number of synthetic weather years to be simulated. Then
# edit the /cord/data/input/base_inflows.json file, specifying the start and end 
# dates of the forecast_exp scenario flow files. Start date must be 1/1/1901.
# End dates must be stoch_years + 3 after start date. 

stoch_years=3;yearbeg=2005;yearend=2034;
stoch_years2=stoch_years+3;

a=0;
# %% Generate synthetic weather (wind speed and temperature) records. 
# import synthetic_temp_wind
# starttime = time.time()
# synthetic_temp_wind.synthetic(stoch_years,yearbeg,yearend)
# print('synth weather')
# elapsed = time.time() - starttime
# print(elapsed)

# %% Generate synthetic streamflow records 
# =============================================================================
# import synthetic_streamflow
# starttime = time.time()
# synthetic_streamflow.synthetic(stoch_years,1901,yearbeg,yearend)
# print('streamflows')
# elapsed = time.time() - starttime
# print(elapsed)
# =============================================================================
#############################################################################
#
#############################################################################
# %% DAILY HYDROPOWER SIMULATION

# Now specify a smaller subset of stochastic data to run (must be < stoch years)
sim_years = 2



#%% change the end year by adding the start year with sim_years;
import json
file='cord/data/input/base_inflows.json'; file2='cord/data/input/base_inflows00.json'
from shutil import copyfile
copyfile(file2,file)
with open(file) as f:
  datas = json.load(f)
  
datas['file_end']['forecast_exp']['F_flow']=str('12/31/{}'.format(1901+stoch_years2-1))
datas['simulation_period_end']['forecast_exp']['F_flow']=1901+stoch_years2-1;
datas['inflow_series']['forecast_exp']['F_flow']='cord/data/input/forecast_flows_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)

#  copy the streamflow file to targeted directory
file1='forecast_flows_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
copyfile('Synthetic_streamflows/'+file1,'cord/data/input/'+file1)


with open(file, 'w') as f:
    json.dump(datas, f, indent=4)
# %%
# Run ORCA to get California storage dam releases
import ORCA    
starttime = time.time()
print('ORCA', file=sys.stderr)
print('will be running for {} seconds'.format(120*stoch_years2), file=sys.stderr)
sys.stdout.flush()
ORCA.sim_ORCA(sim_years)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)
print('ORCA', file=sys.stderr)
# %%
# California Hydropower model
import CA_hydropower
print('CA hydropower')
print('will be running for {} seconds'.format(10*stoch_years2), file=sys.stderr)
starttime = time.time()
CA_hydropower.hydro(sim_years+3,yearbeg, yearend, stoch_years2)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)

# %%
#Willamette operational model
import Willamette_launch
import sys
sys.path.append('Willamette/')
    
print('Willamette')
print('will be running for {} seconds'.format(146*(stoch_years2-1)), file=sys.stderr)
starttime = time.time()
Willamette_launch.launch(sim_years,yearbeg, yearend, stoch_years2)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)

# %%
# Federal Columbia River Power System Model (mass balance in Python)
import ICF_calc
print('FCRPS')
print('will be running for {} seconds'.format(0.01*stoch_years2), file=sys.stderr)
starttime = time.time()
ICF_calc.calc(sim_years,yearbeg, yearend, stoch_years2)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)

# %%
#############################################################################
#
#############################################################################
## HOURLY WIND AND SOLAR POWER PRODUCTION

## WIND
# Specify installed capacity of wind power for each zone
PNW_cap = 6445
CAISO_cap = 4915

# Generate synthetic hourly wind power production time series for the BPA and
# CAISO zones for the entire simulation period
import wind_speed2_wind_power

# %% copy all the files from climate change scenarios folder to copy-folders
from shutil import copyfile

src='Synthetic_weather/synthetic_weather_data_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
dst='Synthetic_weather/synthetic_weather_data.csv'
copyfile(src, dst)

print('wind')
print('will be running for {} seconds'.format(80*(sim_years+3)), file=sys.stderr)
starttime = time.time()
wind_speed2_wind_power.wind_sim(sim_years,PNW_cap,CAISO_cap)
elapsed = time.time() - starttime
print('{} seconds'.format(elapsed), file=sys.stderr)

#%% SOLAR
# Specify installed capacity of wind power for each zone
CAISO_solar_cap = 9890

# Generate synthetic hourly solar power production time series for 
# the CAISO zone for the entire simulation period
import solar_production_simulation

src='Synthetic_weather/synthetic_irradiance_data_{}-{}_{}.csv'.format(yearbeg, yearend, stoch_years2)
dst='Synthetic_weather/synthetic_irradiance_data.csv'
copyfile(src, dst)

print('solar')
print('will be running for {} seconds'.format(47*(sim_years+3)), file=sys.stderr)
starttime = time.time()
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
# NATURAL GAS PRICES

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

elapsed = time.time() - starttime
print(elapsed)





