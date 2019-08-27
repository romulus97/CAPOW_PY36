
## Introduction to the CAPOW Model
This is a general description of the **California and West Coast Power System (CAPOW)** model. CAPOW is Python based. The model was built to simulate the operations of the major markets comprising the West Coast bulk electric power system: the **Mid-Columbia (Mid-C)** market, and the **California Independent System Operator (CAISO)**. 


<img src="https://github.com/romulus97/CAPOW_PY36/blob/master/Images/figure1.png" alt="alt text" width="520" height= "390">

System dynamics are driven entirely by time series of spatially distributed meteorological (temperatures, wind speeds) and hydrologic (streamflows) variables. These natural system inputs are converted to relevant power system inputs (hourly electricity demand, solar power production and wind power production, daily hydropower production). Power system inputs then drive a **unit commitment/economic dispatch (UC/ED)** simulation model, which minimizes the cost of meeting system-wide electricity demand, given an existing generation portfolio. The default model formulation presented here simulates the Mid-C and CAISO markets using two separate objective functions, and power flows between these two systems (i.e, between the Pacific Northwest and California) are modeled statistically. However, this default formulation can (and in some cases should) be altered to consider both systems as a single objective function, and make predictions of power flows between these systems a model output.

The primary outputs of CAPOW are hourly records of power production at the roughly 300 individual generators considered, as well as power flows along relevant transmission pathways, and wholesale electricity prices. In general, the model does not accurately reproduce historical hourly price dynamics in either the Mid-C or CAISO markets; however, the model does quite well at reproducing daily average prices in both.

The figures below illustrate the spatial extent and resolution of the CAPOW model. The CAISO system is divided into 4 zones, which cover the operations of three major utilities in the state. Exchanges of electricity (imports/exports) between the zones of the core UC/ED model and other zones in the larger **Western Electricity Coordinating Council (WECC)** footprint are modeled statistically. 

<img src="https://github.com/romulus97/CAPOW_PY36/blob/master/Images/wiki_2.png" alt="alt text" width="528" height= "330">


## File structure, README files, and publications
There are three main parts of the CAPOW model. Each is associated with a separate sub-repository, and each is primary controlled by a single .py script.

**1. Stochastic_engine** - (_**stochastic_engine.py**_) performs analysis of historical weather/hydrologic data, and uses this analysis to generate synthetic records of temperatures, wind speeds, and streamflows; then converts these synthetic records to associated values of relevant power system inputs.

**2. Model_setup** - (_**UCED_setup.py**_) samples a single calendar year from the synthetic records, and converts these data to a format that can be interpreted by the UC/ED model

**3. UCED** - (_**simulation.py**_) simulates the operation of the CAISO and Mid-C markets, calculates hourly and daily electricity prices. 

The file structure presented on Github is meant to be downloaded as a single compressed zip file, extracted and run by executing the three .py files described above in sequence. **README files in each of the three main sub-repositories** details the function of each related .py script, as well as associated input and output data. 

Note that before running, it's likely that users will need to separately install the **pyomo** mathematical programming package (https://anaconda.org/conda-forge/pyomo) as well as the **CPLEX solver** (https://developer.ibm.com/docloud/blog/2016/11/24/cos-12-7-ai/) and the **xmltodict** package (https://anaconda.org/conda-forge/xmltodict). 

As publications become available that demonstrate the application the CAPOW model in different contexts, those papers, as well as additional code and data, will also be made available here. 
