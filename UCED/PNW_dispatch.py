# -*- coding: utf-8 -*-
"""
Created on Fri Jul 07 12:23:45 2017

@author: jdkern
"""

#######################################################################################################
# a basic unit commitment model for CAISO system                                                       #
# This is the trial version of the electricity market model                                            #
# 4 Zone system                                                                                        #                                                                                #
#######################################################################################################


from __future__ import division # This line is used to ensure that int or long division arguments are converted to floating point values before division is performed 
from pyomo.environ import * # This command makes the symbols used by Pyomo known to Python
from pyomo.opt import SolverFactory
import itertools

##Create a solver
opt = SolverFactory('cplex')

model = AbstractModel()
#
######################################################################
## string indentifiers for the set of generators in different zones. #
######################################################################
#
model.Zone5Generators =  Set()
#PNW

model.Coal = Set()
model.Gas = Set()
model.Oil = Set()
model.Nuclear = Set()
model.PSH = Set()
model.Slack = Set()
model.Hydro = Set()
model.WECCImports = Set()
model.Ramping = model.Hydro | model.WECCImports
   
model.Generators = model.Zone5Generators | model.WECCImports

#
model.zones =Set()

#########################################################
# These are the generators parameters from model input  #
#########################################################


#Generator Type
model.typ = Param(model.Generators)

#Zone parameters
model.zone = Param(model.Generators)

#Max Generating Capacity
model.netcap = Param(model.Generators)

#Min Generating Capacity
model.mincap = Param(model.Generators,mutable=True)

#Minimun up time
model.minu = Param(model.Generators)

#Minmun down time
model.mind = Param(model.Generators)

#Ramp rate
model.ramp  = Param(model.Generators)

#Start cost
model.st_cost = Param(model.Generators)

#Piecewice varible cost segments
model.seg1= Param(model.Generators)
model.seg2= Param(model.Generators)
model.seg3= Param(model.Generators)

#Variable O&M
model.var_om = Param(model.Generators)

#No load cost
model.no_load  = Param(model.Generators)

###########################################################
### These are the detailed parameters for model runs      #
###########################################################
##
## Full range of time series information provided in .dat file (1 year)
model.SimHours = Param(within=PositiveIntegers)
model.SH_periods = RangeSet(1,model.SimHours)
model.SimDays = Param(within=PositiveIntegers)
model.SD_periods = RangeSet(1,model.SimDays)

# Operating horizon information 
model.HorizonHours = Param(within=PositiveIntegers)
model.HH_periods = RangeSet(0,model.HorizonHours)
model.hh_periods = RangeSet(1,model.HorizonHours)
model.HorizonDays = Param(within=PositiveIntegers)
model.hd_periods = RangeSet(1,model.HorizonDays)
model.h1_periods = RangeSet(1,24)
model.h2_periods = RangeSet(25,48)
model.ramp1_periods = RangeSet(2,24)
model.ramp2_periods = RangeSet(26,48)

#Demand over simulation period
model.SimDemand = Param(model.zones*model.SH_periods, within=NonNegativeReals)

#Must run generation over simulation period
model.SimMustRun = Param(model.zones*model.SH_periods, within=NonNegativeReals)

#Horizon demand
model.HorizonDemand = Param(model.zones*model.hh_periods,within=NonNegativeReals,mutable=True)

#Horizon must run generation
model.HorizonMustRun = Param(model.zones*model.hh_periods,within=NonNegativeReals,mutable=True)

#Reserve for the entire system
model.SimReserves = Param(model.SH_periods, within=NonNegativeReals)
model.HorizonReserves = Param(model.hh_periods, within=NonNegativeReals,mutable=True)

#Exchange - dispatchable
model.SimPath65_exports = Param(model.SH_periods, within=NonNegativeReals)
model.SimPath66_exports = Param(model.SH_periods, within=NonNegativeReals)
model.SimPath3_exports = Param(model.SH_periods, within=NonNegativeReals)
model.SimPath8_exports = Param(model.SH_periods, within=NonNegativeReals)
model.SimPath14_exports = Param(model.SH_periods, within=NonNegativeReals)

model.HorizonPath65_exports = Param(model.hh_periods, within=NonNegativeReals,mutable=True)
model.HorizonPath66_exports = Param(model.hh_periods, within=NonNegativeReals,mutable=True)
model.HorizonPath3_exports = Param(model.hh_periods, within=NonNegativeReals,mutable=True)
model.HorizonPath8_exports = Param(model.hh_periods, within=NonNegativeReals,mutable=True)
model.HorizonPath14_exports = Param(model.hh_periods, within=NonNegativeReals,mutable=True)

##
##Variable resources over simulation period
model.SimWind = Param(model.zones, model.SH_periods, within=NonNegativeReals)
model.SimSolar = Param(model.zones, model.SH_periods, within=NonNegativeReals)

#Natural gas prices over simulation period
model.SimGasPrice = Param(model.zones,model.SD_periods, within=NonNegativeReals)
model.GasPrice = Param(model.zones,within = NonNegativeReals, mutable=True,initialize=0)

#Daily path and hydro parameters
model.SimPath66_imports = Param(model.SD_periods, within=NonNegativeReals)
model.SimPath65_imports = Param(model.SD_periods, within=NonNegativeReals)
model.SimPath8_imports = Param(model.SD_periods, within=NonNegativeReals)
model.SimPath14_imports = Param(model.SD_periods, within=NonNegativeReals)
model.SimPath3_imports = Param(model.SD_periods, within=NonNegativeReals)
model.SimPNW_hydro = Param(model.SD_periods, within=NonNegativeReals)

model.HorizonPath66_imports = Param(model.hd_periods, within=NonNegativeReals,mutable=True)
model.HorizonPath65_imports = Param(model.hd_periods, within=NonNegativeReals,mutable=True)
model.HorizonPath8_imports = Param(model.hd_periods, within=NonNegativeReals,mutable=True) 
model.HorizonPath14_imports = Param(model.hd_periods, within=NonNegativeReals,mutable=True)
model.HorizonPath3_imports = Param(model.hd_periods, within=NonNegativeReals,mutable=True)
model.HorizonPNW_hydro = Param(model.hd_periods, within=NonNegativeReals,mutable=True)

#Variable resources over horizon
model.HorizonWind = Param(model.zones,model.hh_periods,within=NonNegativeReals,mutable=True)
model.HorizonSolar = Param(model.zones,model.hh_periods,within=NonNegativeReals,mutable=True)
model.HorizonHydro = Param(model.zones,model.hh_periods,within=NonNegativeReals,mutable=True)

#Minimum flows (hydro and paths)
model.SimPNW_hydro_minflow = Param(model.SH_periods, within=NonNegativeReals)
model.SimPath65_imports_minflow = Param(model.SH_periods, within=NonNegativeReals) 
model.SimPath66_imports_minflow = Param(model.SH_periods, within=NonNegativeReals) 
model.SimPath8_imports_minflow = Param(model.SH_periods, within=NonNegativeReals) 
model.SimPath14_imports_minflow = Param(model.SH_periods, within=NonNegativeReals)   
model.SimPath3_imports_minflow = Param(model.SH_periods, within=NonNegativeReals)  

model.HorizonPath65_minflow  = Param(model.hh_periods,within=NonNegativeReals,mutable=True)
model.HorizonPath66_minflow  = Param(model.hh_periods,within=NonNegativeReals,mutable=True)
model.HorizonPath8_minflow  = Param(model.hh_periods,within=NonNegativeReals,mutable=True)
model.HorizonPath14_minflow  = Param(model.hh_periods,within=NonNegativeReals,mutable=True)
model.HorizonPath3_minflow  = Param(model.hh_periods,within=NonNegativeReals,mutable=True)
model.HorizonPNW_hydro_minflow = Param(model.hh_periods,within=NonNegativeReals,mutable=True)

##Initial conditions
model.ini_on = Param(model.Generators, within=Binary, initialize=0,mutable=True) 
model.ini_mwh_1 = Param(model.Generators,initialize=0,mutable=True) #seg1
model.ini_mwh_2 = Param(model.Generators,initialize=0,mutable=True) #seg2
model.ini_mwh_3 = Param(model.Generators,initialize=0,mutable=True) #seg3

###########################################################
### Decision variables                                    #
###########################################################

##Amount of day-ahead energy generated by each thermal unit's 3 segments at each hour
model.mwh_1 = Var(model.Generators,model.HH_periods, within=NonNegativeReals,initialize=0)
model.mwh_2 = Var(model.Generators,model.HH_periods, within=NonNegativeReals,initialize=0)
model.mwh_3 = Var(model.Generators,model.HH_periods, within=NonNegativeReals,initialize=0)

#1 if unit is on in hour i
model.on = Var(model.Generators,model.HH_periods, within=Binary, initialize=0)

#1 if unit is switching on in hour i
model.switch = Var(model.Generators,model.HH_periods, within=Binary,initialize=0)

#Amount of spining reserce offered by each unit in each hour
model.srsv = Var(model.Generators,model.HH_periods, within=NonNegativeReals,initialize=0)

#Amount of non-sping reserve ovvered by each unit in each hour
model.nrsv = Var(model.Generators,model.HH_periods, within=NonNegativeReals,initialize=0)

#Renewable energy production
model.solar = Var(model.zones,model.HH_periods,within=NonNegativeReals)
model.wind = Var(model.zones,model.HH_periods,within=NonNegativeReals)

#Minimum flows for import paths and hydropower
model.P66I_minflow = Var(model.HH_periods,within=NonNegativeReals)
model.P65I_minflow = Var(model.HH_periods,within=NonNegativeReals)
model.P8I_minflow = Var(model.HH_periods,within=NonNegativeReals)
model.P14I_minflow = Var(model.HH_periods,within=NonNegativeReals)
model.P3I_minflow = Var(model.HH_periods,within=NonNegativeReals)
model.PNWH_minflow = Var(model.HH_periods,within=NonNegativeReals)

####################################################################
##Objective function                                               #
##To minimize overall system cost while satistfy system constraints#
####################################################################
#
##
def SysCost(model):
    coal1 = sum(model.mwh_1[j,i]*(model.seg1[j]*2 + model.var_om[j]) for i in model.hh_periods for j in model.Coal) 
    coal2 = sum(model.mwh_2[j,i]*(model.seg2[j]*2 + model.var_om[j]) for i in model.hh_periods for j in model.Coal) 
    coal3 = sum(model.mwh_3[j,i]*(model.seg3[j]*2 + model.var_om[j]) for i in model.hh_periods for j in model.Coal)
    nuc1 = sum(model.mwh_1[j,i]*(model.seg1[j]*1 + model.var_om[j]) for i in model.hh_periods for j in model.Nuclear) 
    nuc2 = sum(model.mwh_2[j,i]*(model.seg2[j]*1 + model.var_om[j]) for i in model.hh_periods for j in model.Nuclear) 
    nuc3 = sum(model.mwh_3[j,i]*(model.seg3[j]*1 + model.var_om[j]) for i in model.hh_periods for j in model.Nuclear)
    gas1_5 = sum(model.mwh_1[j,i]*(model.seg1[j]*model.GasPrice['PNW'] + model.var_om[j]) for i in model.hh_periods for j in model.Gas) 
    gas2_5 = sum(model.mwh_2[j,i]*(model.seg2[j]*model.GasPrice['PNW'] + model.var_om[j]) for i in model.hh_periods for j in model.Gas)  
    gas3_5 = sum(model.mwh_3[j,i]*(model.seg3[j]*model.GasPrice['PNW'] + model.var_om[j]) for i in model.hh_periods for j in model.Gas)  
    oil1 = sum(model.mwh_1[j,i]*(model.seg1[j]*20 + model.var_om[j]) for i in model.hh_periods for j in model.Oil) 
    oil2 = sum(model.mwh_2[j,i]*(model.seg2[j]*20 + model.var_om[j]) for i in model.hh_periods for j in model.Oil)  
    oil3 = sum(model.mwh_3[j,i]*(model.seg3[j]*20 + model.var_om[j]) for i in model.hh_periods for j in model.Oil)  
    psh1 = sum(model.mwh_1[j,i]*10 for i in model.hh_periods for j in model.PSH)
    psh2 = sum(model.mwh_2[j,i]*10 for i in model.hh_periods for j in model.PSH)
    psh3 = sum(model.mwh_3[j,i]*10 for i in model.hh_periods for j in model.PSH)
    slack1 = sum(model.mwh_1[j,i]*model.seg1[j]*10000 for i in model.hh_periods for j in model.Slack)
    slack2 = sum(model.mwh_2[j,i]*model.seg2[j]*10000 for i in model.hh_periods for j in model.Slack)
    slack3 = sum(model.mwh_3[j,i]*model.seg3[j]*10000 for i in model.hh_periods for j in model.Slack)
    fixed_coal = sum(model.no_load[j]*model.on[j,i]*2 for i in model.hh_periods for j in model.Coal)
    fixed_gas5 = sum(model.no_load[j]*model.on[j,i]*model.GasPrice['PNW'] for i in model.hh_periods for j in model.Gas)
    fixed_oil = sum(model.no_load[j]*model.on[j,i]*20 for i in model.hh_periods for j in model.Oil)
    fixed_slack = sum(model.no_load[j]*model.on[j,i]*10000 for i in model.hh_periods for j in model.Slack)
    starts = sum(model.st_cost[j]*model.switch[j,i] for i in model.hh_periods for j in model.Generators) 

    return fixed_slack + fixed_oil + fixed_gas5 + fixed_coal + coal1 + coal2 + coal3 + nuc1 + nuc2 + nuc3 + gas1_5 + gas2_5 + gas3_5 + oil1 + oil2 + oil3 + psh1 + psh2 + psh3 + slack1 + slack2 + slack3 + starts 
model.SystemCost = Objective(rule=SysCost, sense=minimize)
    
   
####################################################################
#   Constraints                                                    #
####################################################################
   
###Power Balance 
def Zone5_Balance(model,i):
    s1 = sum(model.mwh_1[j,i] for j in model.Zone5Generators)
    s2 = sum(model.mwh_2[j,i] for j in model.Zone5Generators)  
    s3 = sum(model.mwh_3[j,i] for j in model.Zone5Generators)  
    other = model.solar['PNW',i] + model.PNWH_minflow[i]\
    + model.wind['PNW',i] + model.HorizonMustRun['PNW',i]
    imports =  model.P66I_minflow[i] + model.P65I_minflow[i] + model.P8I_minflow[i] + model.P14I_minflow[i] + model.P3I_minflow[i] + model.mwh_1['P66I',i] + model.mwh_2['P66I',i] + model.mwh_3['P66I',i] + model.mwh_1['P65I',i] + model.mwh_2['P65I',i] + model.mwh_3['P65I',i] + model.mwh_1['P3I',i] + model.mwh_2['P3I',i] + model.mwh_3['P3I',i] + model.mwh_1['P8I',i] + model.mwh_2['P8I',i] + model.mwh_3['P8I',i] + model.mwh_1['P14I',i] + model.mwh_2['P14I',i] + model.mwh_3['P14I',i] 
    exports =  model.HorizonPath66_exports[i] + model.HorizonPath65_exports[i] + model.HorizonPath8_exports[i] + model.HorizonPath3_exports[i] + model.HorizonPath14_exports[i]
    return s1 + s2 + s3 + other + imports - exports >= model.HorizonDemand['PNW',i]
model.Bal5Constraint= Constraint(model.hh_periods,rule=Zone5_Balance)


# Daily production limits on dispatchable hydropower
def HydroC1(model,i):
    m1 = sum(model.mwh_1['PNWH',i] for i in model.h1_periods)
    m2 = sum(model.mwh_2['PNWH',i] for i in model.h1_periods)
    m3 = sum(model.mwh_3['PNWH',i] for i in model.h1_periods)
    return m1 + m2 + m3 <= model.HorizonPNW_hydro[1]
model.HydroConstraint1= Constraint(model.h1_periods,rule=HydroC1)

#Max capacity constraints on variable resources 
def SolarC(model,z,i):
    return model.solar[z,i] <= model.HorizonSolar[z,i]
model.SolarConstraint= Constraint(model.zones,model.hh_periods,rule=SolarC)

def WindC(model,z,i):
    return model.wind[z,i] <= model.HorizonWind[z,i]
model.WindConstraint= Constraint(model.zones,model.hh_periods,rule=WindC)

def P66minC(model,i):
    return model.P66I_minflow[i] <= model.HorizonPath66_minflow[i]
model.P66MinflowConstraint= Constraint(model.hh_periods,rule=P66minC)

def P65minC(model,i):
    return model.P65I_minflow[i] <= model.HorizonPath65_minflow[i]
model.P65MinflowConstraint= Constraint(model.hh_periods,rule=P65minC)

def P14minC(model,i):
    return model.P14I_minflow[i] <= model.HorizonPath14_minflow[i]
model.P14MinflowConstraint= Constraint(model.hh_periods,rule=P14minC)

def P8minC(model,i):
    return model.P8I_minflow[i] <= model.HorizonPath8_minflow[i]
model.P8MinflowConstraint= Constraint(model.hh_periods,rule=P8minC)

def P3minC(model,i):
    return model.P3I_minflow[i] <= model.HorizonPath3_minflow[i]
model.P3MinflowConstraint= Constraint(model.hh_periods,rule=P3minC)

def PNWHminC(model,i):
    return model.PNWH_minflow[i] <= model.HorizonPNW_hydro_minflow[i]
model.PNWHMinflowConstraint= Constraint(model.hh_periods,rule=PNWHminC)


# Daily production limits on imported power
def ImportsC1(model,i):
    m1 = sum(model.mwh_1['P66I',i] for i in model.h1_periods)
    m2 = sum(model.mwh_2['P66I',i] for i in model.h1_periods)
    m3 = sum(model.mwh_3['P66I',i] for i in model.h1_periods)
    return m1 + m2 + m3 <= model.HorizonPath66_imports[1]
model.ImportsConstraint1= Constraint(model.h1_periods,rule=ImportsC1)

def ImportsC2(model,i):
    m1 = sum(model.mwh_1['P66I',i] for i in model.h2_periods)
    m2 = sum(model.mwh_2['P66I',i] for i in model.h2_periods)
    m3 = sum(model.mwh_3['P66I',i] for i in model.h2_periods)
    return m1 + m2 + m3 <= model.HorizonPath66_imports[2]
model.ImportsConstraint2= Constraint(model.h2_periods,rule=ImportsC2)

def ImportsC3(model,i):
    m1 = sum(model.mwh_1['P65I',i] for i in model.h1_periods)
    m2 = sum(model.mwh_2['P65I',i] for i in model.h1_periods)
    m3 = sum(model.mwh_3['P65I',i] for i in model.h1_periods)
    return m1 + m2 + m3 <= model.HorizonPath65_imports[1]
model.ImportsConstraint3= Constraint(model.h1_periods,rule=ImportsC3)

def ImportsC4(model,i):
    m1 = sum(model.mwh_1['P65I',i] for i in model.h2_periods)
    m2 = sum(model.mwh_2['P65I',i] for i in model.h2_periods)
    m3 = sum(model.mwh_3['P65I',i] for i in model.h2_periods)
    return m1 + m2 + m3 <= model.HorizonPath65_imports[2]
model.ImportsConstraint4= Constraint(model.h2_periods,rule=ImportsC4)

def ImportsC5(model,i):
    m1 = sum(model.mwh_1['P8I',i] for i in model.h1_periods)
    m2 = sum(model.mwh_2['P8I',i] for i in model.h1_periods)
    m3 = sum(model.mwh_3['P8I',i] for i in model.h1_periods)
    return m1 + m2 + m3 <= model.HorizonPath8_imports[1]
model.ImportsConstraint5= Constraint(model.h1_periods,rule=ImportsC5)

def ImportsC6(model,i):
    m1 = sum(model.mwh_1['P8I',i] for i in model.h2_periods)
    m2 = sum(model.mwh_2['P8I',i] for i in model.h2_periods)
    m3 = sum(model.mwh_3['P8I',i] for i in model.h2_periods)
    return m1 + m2 + m3 <= model.HorizonPath8_imports[2]
model.ImportsConstraint6= Constraint(model.h2_periods,rule=ImportsC6)

def ImportsC7(model,i):
    m1 = sum(model.mwh_1['P14I',i] for i in model.h1_periods)
    m2 = sum(model.mwh_2['P14I',i] for i in model.h1_periods)
    m3 = sum(model.mwh_3['P14I',i] for i in model.h1_periods)
    return m1 + m2 + m3 <= model.HorizonPath14_imports[1]
model.ImportsConstraint7= Constraint(model.h1_periods,rule=ImportsC7)

def ImportsC8(model,i):
    m1 = sum(model.mwh_1['P14I',i] for i in model.h2_periods)
    m2 = sum(model.mwh_2['P14I',i] for i in model.h2_periods)
    m3 = sum(model.mwh_3['P14I',i] for i in model.h2_periods)
    return m1 + m2 + m3 <= model.HorizonPath14_imports[2]
model.ImportsConstraint8= Constraint(model.h2_periods,rule=ImportsC8)

def ImportsC9(model,i):
    m1 = sum(model.mwh_1['P3I',i] for i in model.h1_periods)
    m2 = sum(model.mwh_2['P3I',i] for i in model.h1_periods)
    m3 = sum(model.mwh_3['P3I',i] for i in model.h1_periods)
    return m1 + m2 + m3 <= model.HorizonPath3_imports[1]
model.ImportsConstraint9= Constraint(model.h1_periods,rule=ImportsC9)

def ImportsC10(model,i):
    m1 = sum(model.mwh_1['P3I',i] for i in model.h2_periods)
    m2 = sum(model.mwh_2['P3I',i] for i in model.h2_periods)
    m3 = sum(model.mwh_3['P3I',i] for i in model.h2_periods)
    return m1 + m2 + m3 <= model.HorizonPath3_imports[2]
model.ImportsConstraint10= Constraint(model.h2_periods,rule=ImportsC10)


#Max Capacity Constraint
def MaxC(model,j,i):
    return model.mwh_1[j,i] + model.mwh_2[j,i] + model.mwh_3[j,i] <= model.on[j,i] * model.netcap[j]
model.MaxCap= Constraint(model.Generators,model.hh_periods,rule=MaxC)


##Min Capacity Constraint
def MinC1(model,j,i):
    return model.mwh_1[j,i] + model.mwh_2[j,i] + model.mwh_3[j,i] >= model.on[j,i] * model.mincap[j]
model.MinCap1= Constraint(model.Generators,model.hh_periods,rule=MinC1)


##System Reserve Requirement (excludes pumped storage)
def SysReserve(model,i):
    return sum(model.srsv[j,i] for j in model.Coal) + sum(model.srsv[j,i] for j in model.Gas) + sum(model.srsv[j,i] for j in model.Oil) + sum(model.nrsv[j,i] for j in model.Coal) + sum(model.nrsv[j,i] for j in model.Gas) + sum(model.nrsv[j,i] for j in model.Oil) >= model.HorizonReserves[i]
model.SystemReserve = Constraint(model.hh_periods,rule=SysReserve)
##
def SpinningReq(model,i):
    return sum(model.srsv[j,i] for j in model.Generators ) >= 0.5 * model.HorizonReserves[i]
model.SpinReq = Constraint(model.hh_periods,rule=SpinningReq)           
#
#
##Spinning reserve can only be offered by units that are online
def SpinningReq2(model,j,i):
    return model.srsv[j,i] <= model.on[j,i]*model.netcap[j]
model.SpinReq2= Constraint(model.Generators,model.hh_periods,rule=SpinningReq2)
#
##
###Segment capacity requirements
def Seg1(model,j,i):
    return model.mwh_1[j,i] <= .6*model.netcap[j]
model.Segment1 = Constraint(model.Generators,model.hh_periods,rule=Seg1)
#
def Seg2(model,j,i):
    return model.mwh_2[j,i] <= .2*model.netcap[j]
model.Segment2 = Constraint(model.Generators,model.hh_periods,rule=Seg2)

def Seg3(model,j,i):
    return model.mwh_3[j,i] <= .2*model.netcap[j]
model.Segment3 = Constraint(model.Generators,model.hh_periods,rule=Seg3)
##
#
##Zero Sum Constraint
def ZeroSum(model,j,i):
    return model.mwh_1[j,i] + model.mwh_2[j,i] + model.mwh_3[j,i] + model.srsv[j,i] + model.nrsv[j,i] <= model.netcap[j]
model.ZeroSumConstraint=Constraint(model.Generators,model.hh_periods,rule=ZeroSum)
#
#
##Switch is 1 if unit is turned on in current period
def SwitchCon(model,j,i):
    return model.switch[j,i] >= 1 - model.on[j,i-1] - (1 - model.on[j,i])
model.SwitchConstraint = Constraint(model.Generators,model.hh_periods,rule = SwitchCon)
#
#
##Min Up time
def MinUp(model,j,i,k):
    if i > 0 and k > i and k < min(i+model.minu[j]-1,model.HorizonHours):
        return model.on[j,i] - model.on[j,i-1] <= model.on[j,k]
    else: 
        return Constraint.Skip
model.MinimumUp = Constraint(model.Generators,model.HH_periods,model.HH_periods,rule=MinUp)
#
##Min Down time
def MinDown(model,j,i,k):
   if i > 0 and k > i and k < min(i+model.mind[j]-1,model.HorizonHours):
       return model.on[j,i-1] - model.on[j,i] <= 1 - model.on[j,k]
   else:
       return Constraint.Skip
model.MinimumDown = Constraint(model.Generators,model.HH_periods,model.HH_periods,rule=MinDown)

#Pumped Storage constraints
def PSHC(model,j,i):
    days  = int(model.HorizonHours/24)
    for d in range(0,days):
        return sum(model.mwh_1[j,i] + model.mwh_2[j,i] + model.mwh_3[j,i] for i in range(d*24+1,d*24+25)) <= 10*model.netcap[j]
model.PumpTime = Constraint(model.PSH,model.hh_periods,rule=PSHC)

#Ramp Rate Constraints
def Ramp1(model,j,i):
    a = model.mwh_1[j,i] + model.mwh_2[j,i] + model.mwh_3[j,i]
    b = model.mwh_1[j,i-1] + model.mwh_2[j,i-1] + model.mwh_3[j,i-1]
    return a - b <= model.ramp[j] 
model.RampCon1 = Constraint(model.Ramping,model.ramp1_periods,rule=Ramp1)

def Ramp2(model,j,i):
    a = model.mwh_1[j,i] + model.mwh_2[j,i] + model.mwh_3[j,i]
    b = model.mwh_1[j,i-1] + model.mwh_2[j,i-1] + model.mwh_3[j,i-1]
    return b - a <= model.ramp[j] 
model.RampCon2 = Constraint(model.Ramping,model.ramp2_periods,rule=Ramp2)

#Nuclear constraint
def NucOn(model,i):
    return model.on["COLUMBIA_2",i] >= 1
model.NOn = Constraint(model.hh_periods,rule=NucOn)
    



