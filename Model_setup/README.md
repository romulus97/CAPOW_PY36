# UC/ED Model setup
Once stochastic inputs are created, a single year is randomly sampled and that year's data is put in the .dat format that is required for the pyomo mathematical optimization library. This script can easily be interfaced with a data mining scheme for selecting specific years/scenarios to run on a cluster. 

<img src="https://github.com/romulus97/CAPOW_PY36/blob/master/Images/readme5.png" alt="alt text" width="500" height="300">

## min_hydro_ramping.py
This section uses historical hydropower production data and simulated hydropower to create time series of minimum hydropower production and "ramp rates" for dispatchable hydropower in each zone.

**Input files required:** <br/>
Hydro_setup/PNW_hydro_2001.xlsx <br/>
Hydro_setup/PNW_hydro_2005.xlsx <br/>
Hydro_setup/PNW_hydro_2010.xlsx <br/>
Hydro_setup/PNW_hydro_2011.xlsx <br/>
Hydro_setup/PGEV_hydro_2001.xlsx <br/>
Hydro_setup/PGEV_hydro_2005.xlsx <br/>
Hydro_setup/PGEV_hydro_2010.xlsx <br/>
Hydro_setup/PGEV_hydro_2011.xlsx <br/>
Hydro_setup/SCE_hydro_2001.xlsx <br/>
Hydro_setup/SCE_hydro_2005.xlsx <br/>
Hydro_setup/SCE_hydro_2010.xlsx <br/>
Hydro_setup/SCE_hydro_2011.xlsx <br/>

**Output files:** <br/>
Hydro_setup/Minimum_hydro.xlsx <br/>

<img src="https://github.com/romulus97/CAPOW_PY36/blob/master/Images/readme6.png" alt="alt text" width="530" height="270">

## CA_exchange_time_series.py
This file calculates "minimum flows" for zonal hydropower production and imports, dispatchable imports and hydropower, and hourly export demand for each zone in the CAISO system.

**Input files required:** <br/>
../Stochastic_engine/Synthetic_demand_pathflows/Load_Path_Sim.csv <br/>
../Stochastic_engine/CA_hydropower/CA_hydro_daily.xlsx <br/>
Hydro_setup/Minimum_hydro_profiles.xlsx <br/>
Path_setup/CA_imports_minflow_profiles.xlsx <br/>
Path_setup/CA_path_export_profiles.xlsx <br/>

**Output files:** <br/>
Path_setup/CA_exports.csv <br/>
Path_setup/CA_dispatchable_imports.csv <br/>
Path_setup/CA_imports.csv <br/>
Path_setup/CA_path_mins.csv <br/>
Hydro_setup/CA_dispatchable_hydro.csv <br/>
Hydro_setup/CA_hydro_mins.csv <br/>

## PNW_exchange_time_series.py
This file calculates "minimum flows" for zonal hydropower production and imports, dispatchable imports and hydropower, and hourly export demand for the PNW system.

**Input files required:** <br/>
../Stochastic_engine/Synthetic_demand_pathflows/Load_Path_Sim.csv <br/>
../Stochastic_engine/PNW_hydro/PNW_hydro_daily.xlsx <br/>
Hydro_setup/Minimum_hydro_profiles.xlsx <br/>
Path_setup/PNW_imports_minflow_profiles.xlsx <br/>
Path_setup/PNW_path_export_profiles.xlsx <br/>

**Output files:** <br/>
Path_setup/PNW_exports.csv <br/>
Path_setup/PNW_dispatchable_imports.csv <br/>
Path_setup/PNW_imports.csv <br/>
Path_setup/PNW_path_mins.csv <br/>
Hydro_setup/PNW_dispatchable_hydro.csv <br/>
Hydro_setup/PNW_hydro_mins.csv <br/>

<img src="https://github.com/romulus97/CAPOW_PY36/blob/master/Images/readme7.png" alt="alt text" width="530" height="240">

## CA_data_setup.py
This file populates the data.dat file needed to run the CAISO UC/ED model. Note that the user can specify **hist=1** in order to assign historical monthly production values (**hist_year = 2010 or 2011**) to the two nuclear power plants in the CAISO footprint. If **hist=0**, these plants are assumed to be retired.

**Input files required:** <br/>
CA_data_file/generators.csv<br/>
CA_data_file/paths.csv<br/>
CA_data_file/calendar.xlsx<br/>
CA_data_file/reserves.csv<br/>
CA_data_file/wind_caps.xlsx<br/>
CA_data_file/solar_caps.xlsx<br/>
CA_data_file/must_run.xlsx<br/>
../Stochastic_engine/Synthetic_demand_pathflows/Sim_hourly_load.xlsx<br/>
../Stochastic_engine/Synthetic_wind_power/wind_power_sim.csv<br/>
../Stochastic_engine/Synthetic_solar_power/solar_power_sim.xlsx<br/>
../Stochastic_engine/Gas_prices/NG.xlsx<br/>
Hydro_setup/CA_dispatchable_hydro.csv<br/>
Hydro_setup/CA_hydro_mins.csv<br/>
Path_setup/CA_dispatchable_imports.csv<br/>
Path_setup/CA_exports.csv<br/>
Path_setup/CA_path_mins.csv<br/>

**Output files:** 
data.dat <br/>

## PNW_data_setup.py
This file populates the data.dat file needed to run the PNW/Mid-C UC/ED model. 

**Input files required:** <br/>
PNW_data_file/generators.csv<br/>
PNW_data_file/reserves.csv<br/>
PNW_data_file/must_run.xlsx<br/>
../Stochastic_engine/Synthetic_demand_pathflows/Sim_hourly_load.xlsx<br/>
../Stochastic_engine/Synthetic_wind_power/wind_power_sim.csv<br/>
../Stochastic_engine/Gas_prices/NG.xlsx<br/>
Hydro_setup/PNW_dispatchable_hydro.csv<br/>
Hydro_setup/PNW_hydro_mins.csv<br/>
Path_setup/PNW_dispatchable_imports.csv<br/>
Path_setup/PNW_exports.csv<br/>
Path_setup/PNW_path_mins.csv<br/>

**Output files:** 
data.dat <br/>
