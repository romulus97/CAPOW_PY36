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
starttime = time.time()
#import calculate_cov
############################################################################

############################################################################
# STOCHASTIC WEATHER AND STREAMFLOW GENERATION

# Specify a number of synthetic weather years to be simulated. Then
# edit the /cord/data/input/base_inflows.json file, specifying the start and end 
# dates of the forecast_exp scenario flow files. Start date must be 1/1/1901.
# End dates must be stoch_years + 3 after start date. 

stoch_years=20

# Generate synthetic weather (wind speed and temperature) records. 
import synthetic_temp_wind_v2
synthetic_temp_wind_v2.synthetic(stoch_years)
print('synth weather')

# Generate synthetic streamflow records 
import synthetic_streamflow_v2
print('streamflows')

#############################################################################
#
#############################################################################
# DAILY HYDROPOWER SIMULATION

# Now specify a smaller subset of stochastic data to run (must be <= stoch years)
sim_years = 3

# Run ORCA to get California storage dam releases
import main
main.sim(sim_years)
print('ORCA')
#
# California Hydropower model
import CA_hydropower
CA_hydropower.hydro(sim_years)
print('CA hydropower')

#Willamette operational model
import Willamette_launch
Willamette_launch.launch(sim_years)
print('Willamette')


# Federal Columbia River Power System Model (mass balance in Python)
import ICF_calc_new
ICF_calc_new.calc(sim_years)
import FCRPS_New
FCRPS_New.simulate(sim_years)
print('FCRPS')

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
wind_speed2_wind_power.wind_sim(sim_years,PNW_cap,CAISO_cap)
print('wind')

# SOLAR
# Specify installed capacity of wind power for each zone
CAISO_solar_cap = 9890

# Generate synthetic hourly solar power production time series for 
# the CAISO zone for the entire simulation period
import solar_production_simulation
solar_production_simulation.solar_sim(sim_years,CAISO_solar_cap)
print('solar')
##############################################################################
#
##############################################################################
# ELECTRICITY DEMAND AND TRANSMISSION PATH FLOWS

# Calculate daily peak and hourly electricity demand for each zone and daily 
# flows of electricity along each WECC path that exchanges electricity between
# core UC/ED model (CAISO, Mid-C markets) and other WECC zones

import demand_pathflows
print('paths')
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





