
## Model Simulation
The user specifies a number of days out of the randomly sampled synthetic year to be simulated (**min = 2, max = 365**). Then the CAISO and PNW dispatch models are run in sequence.

<img src="https://github.com/romulus97/CAPOW_PY36/blob/master/Images/readme8.png" alt="alt text" width="500" height="400">

## CA_wrapper.py
This file iteratively loads power system inputs 48-hours at a time and dispatches the model over a 2-day operating horizon. Results (power flows, generation schedules) are dynamically stored for each simulation day (24-hour period).

**Input files required:** <br/>
..Model_setup/CA_data_file/data.dat<br/> 
CA_dispatch.py<br/>

**Output files:** <br/>
CAISO/flow.csv<br/>
CAISO/mwh_1.csv<br/>
CAISO/mwh_2.csv<br/>
CAISO/mwh_3.csv<br/>
CAISO/nrsv.csv<br/>
CAISO/on.csv<br/>
CAISO/solar_out.csv<br/>
CAISO/wind_out.csv<br/>
CAISO/switch.csv<br/>
CAISO/srsv.csv<br/>

## PNW_wrapper.py
This file iteratively loads power system inputs 48-hours at a time and dispatches the model over a 2-day operating horizon. Results (power flows, generation schedules) are dynamically stored for each simulation day (24-hour period).

**Input files required:** <br/>
..Model_setup/PNW_data_file/data.dat<br/> 
PNW_dispatch.py<br/>

**Output files:** <br/>
PNW/flow.csv<br/>
PNW/mwh_1.csv<br/>
PNW/mwh_2.csv<br/>
PNW/mwh_3.csv<br/>
PNW/nrsv.csv<br/>
PNW/on.csv<br/>
PNW/solar_out.csv<br/>
PNW/wind_out.csv<br/>
PNW/switch.csv<br/>
PNW/srsv.csv<br/>

## CA_price_calculation
Wholesale electricity prices for each zone are estimated as the marginalcost ($/MWh) of the most expensive unit online in each hour. These (somewhat crude) LMP estimates are then combined in a regression to predict prices for the CAISO market. 

**Input files required:** <br/>
CAISO/mwh_1.csv<br/>
CAISO/mwh_2.csv<br/>
CAISO/mwh_3.csv<br/>
CAISO/prices_2010_2011.csv<br/>
../Model_setup/CA_data_file/generators.csv<br/>

**Output files:** <br/>
CAISO/sim_hourly_prices.xlsx<br/>
CAISO/sim_daily_prices.xlsx<br/>
CAISO/weighted_daily_prices.xlsx<br/>
CAISO/weighted_hourly_prices.xlsx<br/>

## PNW_price_calculation
Wholesale electricity prices for each zone are estimated as the marginalcost ($/MWh) of the most expensive unit online in each hour. 

**Input files required:** <br/>
PNW/mwh_1.csv<br/>
PNW/mwh_2.csv<br/>
PNW/mwh_3.csv<br/>
PNW/prices_2010_2011.csv<br/>
../Model_setup/PNW_data_file/generators.csv<br/>

**Output files:** <br/>
PNW/sim_hourly_prices.xlsx<br/>
PNW/sim_daily_prices.xlsx<br/>
PNW/weighted_daily_prices.xlsx<br/>
PNW/weighted_hourly_prices.xlsx
