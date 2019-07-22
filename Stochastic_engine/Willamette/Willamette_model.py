
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 13:11:23 2018

@authors: Joy Hill, Simona Denaro
"""

#this code will read in ResSim Lite rule curves, control points, etc. for the 13 dams in the Williamette Basin

import pandas as pd
import numpy as np
from scipy.interpolate import interp2d
import datetime as dt
import os
#import logging



####################
#set log file
#logging.basicConfig(filename='PNW_hydro/Willamette/logfiles/run1.log',level=logging.DEBUG)


def DatetoDayOfYear(val, fmt):
#val = '2012/11/07'
#fmt = '%Y/%m/%d'
    date_d = dt.datetime.strptime(val,fmt)
    tt = date_d.timetuple()
    doy = tt.tm_yday

    return doy

def UpdateReservoirWaterYear(doy,t, volumes_all):
    waterYear=np.nan
    M3_PER_ACREFT = 1233.4
    resVolumeBasin = np.sum(volumes_all[t-1,:])
    resVolumeBasin = resVolumeBasin*M3_PER_ACREFT*1000000
    if resVolumeBasin > float(1.48):
        waterYear = float(1.48) #Abundant
    elif resVolumeBasin < float(1.48) and resVolumeBasin >  float(1.2):
        waterYear = float(1.2) #Adequate
    elif resVolumeBasin < float(1.2) and resVolumeBasin > float(0.9):
        waterYear = float(0.9) #Insufficient
    elif resVolumeBasin < float(0.9):
        waterYear = 0 #Deficit
            
    return waterYear
        
        


def GetPoolElevationFromVolume(volume,name):
    if name.AreaVolCurve is None:
        return 0
    else:
        poolElevation = np.interp(volume,name.AreaVolCurve['Storage_m3'],name.AreaVolCurve['Elevation_m'])

        return poolElevation #returns pool elevation (m)


def GetPoolVolumeFromElevation(pool_elev,name):
    if name.AreaVolCurve is None:
        return 0
    else:
        poolVolume = np.interp(pool_elev,name.AreaVolCurve['Elevation_m'],name.AreaVolCurve['Storage_m3'])

        return poolVolume #returns pool vol(m^3)


def GetBufferZoneElevation(doy,name):
    if name.Buffer is None:
        return 0
    else:
        bufferZoneElevation = np.interp(doy,name.Buffer['Day'],name.Buffer['Pool_elevation_m'])

        return bufferZoneElevation #returns what the buffer zone elevation level is for this time of year (in m)


def GetTargetElevationFromRuleCurve(doy,name): #target_table is same as rule_curve
    if name.RuleCurve is None:
        return 0
    else:
        target = np.interp(doy,name.RuleCurve['Day'],name.RuleCurve['Cons_Pool_elev_m'])

        return target #target pool elevation in m

def UpdateMaxGateOutflows(name,poolElevation): 
    name.maxPowerFlow=name.GateMaxPowerFlow    #does not depend on elevation but can change due to constraints
    name.maxRO_Flow = np.interp(poolElevation,name.RO['pool_elev_m'],name.RO['release_cap_cms'])
    name.maxSpillwayFlow = np.interp(poolElevation,name.Spillway['pool_elev_m'],name.Spillway['release_cap_cms'])
        
    return (name.maxPowerFlow, name.maxRO_Flow, name.maxSpillwayFlow)


def AssignReservoirOutletFlows(name,outflow):
    #flow file has a condition on reservoir not being null...dk if we need that here
    #outflow = outflow * 86400  # convert to daily volume    m3 per day 
    #initialize values to 0.0
    powerFlow = 0.0
    RO_flow = 0.0
    spillwayFlow = 0.0

    if outflow <= name.maxPowerFlow: #this value is stored
        powerFlow = outflow
    else:
        powerFlow = name.maxPowerFlow
        excessFlow = outflow - name.maxPowerFlow
        if excessFlow <= name.maxRO_Flow:
            RO_flow = excessFlow
            if RO_flow < name.minRO_Flow: #why is this condition less than where as the previous are <=
                RO_flow = name.minRO_Flow
                powerFlow = outflow - name.minRO_Flow
        else:
            RO_flow = name.maxRO_Flow
            excessFlow -= RO_flow

            spillwayFlow = excessFlow

            if spillwayFlow < name.minSpillwayFlow:
                spillwayFlow = name.minSpillwayFlow
                RO_flow =- name.minSpillwayFlow - excessFlow
            if spillwayFlow > name.maxSpillwayFlow:
                pass
                #logging.info('Maximum spillway volume exceed reservoir %s', name.name)

        
    massbalancecheck = outflow - (powerFlow + RO_flow + spillwayFlow)
    #does this equal 0?
    if abs(massbalancecheck - 0) > 1e-5:
        pass
        #logging.info ("Mass balance didn't close for %s massbalancecheck = %d Pow, Spill and RO %d,%d,%d=" %(name.name, massbalancecheck, powerFlow, spillwayFlow, RO_flow) )

    return(powerFlow,RO_flow,spillwayFlow)


def GetResOutflow(name, volume, inflow, lag_inflow , lag_outflow, doy, waterYear, CP_list, cp_discharge, lag_zone):
    currentPoolElevation = GetPoolElevationFromVolume(volume,name)    
    if name.Restype!='Storage_flood': #if it produces hydropower
        #reset gate specific flows
        [name.maxPowerFlow, name.maxRO_Flow, name.maxSpillwayFlow]=UpdateMaxGateOutflows( name, currentPoolElevation )
        #Reset min outflows to 0 for next timestep (max outflows are reset by the function UpdateMaxGateOutflows)
        name.minPowerFlow=0
        name.minRO_Flow =0
        name.minSpillwayFlow=0 
    
    if name.Restype=='RunOfRiver':
      outflow = inflow
    else:
      targetPoolElevation = GetTargetElevationFromRuleCurve( doy, name )
      targetPoolVolume    = GetPoolVolumeFromElevation(targetPoolElevation, name)
      currentVolume = GetPoolVolumeFromElevation(currentPoolElevation, name)
      bufferZoneElevation = GetBufferZoneElevation( doy, name )

      if currentVolume > name.maxVolume:
         currentVolume = name.maxVolume;   #Don't allow res volumes greater than max volume.This code may be removed once hydro model is calibrated.
         currentPoolElevation = GetPoolElevationFromVolume(currentVolume, name);  #Adjust pool elevation
         #logging.info ("Reservoir volume at %s on day of year %d exceeds maximum. Volume set to maxVolume. Mass Balance not closed." % (name.name, doy))
        

      desiredRelease = (currentVolume - targetPoolVolume)/86400     #This would bring pool elevation back to the rule curve in one timestep.  Converted from m3/day to m3/s  (cms).
                                                                          #This would be ideal if possible within the given constraints.
      if currentVolume < targetPoolVolume: #if we want to fill the reservoir
         desiredRelease=name.minOutflow

      actualRelease = desiredRelease   #Before any constraints are applied
      
      # ASSIGN ZONE:  zone 0 = top of dam, zone 1 = flood control high, zone 2 = conservation operations, zone 3 = buffer, zone 4 = alternate flood control 1, zone 5 = alternate flood control 2.  
      zone=[]
      if currentPoolElevation > name.Td_elev:
         #logging.info ("Reservoir elevation at %s on day of year %r exceeds dam top elevation." %(name.name, doy))
         currentPoolElevation = name.Td_elev - 0.1    #Set just below top elev to keep from exceeding values in lookup tables
         zone = 0    
      elif currentPoolElevation > name.Fc1_elev:
         zone = 0
      elif currentPoolElevation > targetPoolElevation:
         if name.Fc2_elev!=[] and currentPoolElevation <= name.Fc2_elev:
            zone = 4
         elif name.Fc3_elev!=[] and currentPoolElevation > name.Fc3_elev:
            zone = 5
         else:
            zone = 1
      elif currentPoolElevation <= targetPoolElevation:
         if currentPoolElevation <= bufferZoneElevation:   #in the buffer zone (HERE WE REMOVED THE PART THAT COUNTED THE DAYS IN THE BUFFER ZONE)
            if lag_zone == 3:
                #logging.info("buffer rule activated")
                zone = 2
            else:
                zone = 3  
         else:                                           #in the conservation zone
            zone = 2
      else:
          pass
         #logging.info ("*** GetResOutflow(): We should never get here. doy = %dreservoir = %s" % (doy, name.name))
      lag_zone=zone
      #logging.info('zone is %d', zone)   
      
        # Once we know what zone we are in, we can access the array of appropriate constraints for the particular reservoir and zone.       

      constraint_array=name.RulePriorityTable.iloc[:,zone]
      constraint_array=constraint_array[(constraint_array !='Missing')] #eliminate 'Missing' rows
      #Loop through constraints and modify actual release.  Apply the flood control rules in order here.
      for i in range (0, (len(constraint_array)-1)):
          #open the csv file and get first column label and appropriate data to use for lookup
          constraintRules = pd.read_csv(os.path.join(name.ruleDir, constraint_array[i])) 
          xlabel = list(constraintRules)[0]   
          xvalue = []
          yvalue = []
          if xlabel=="Date":                           # Date based rule?  xvalue = current date.
             xvalue = doy
          elif xlabel=="Release_cms":                  # Release based rule?  xvalue = release last timestep
               xvalue = lag_outflow       
          elif xlabel=="Pool_elev_m" :                 # Pool elevation based rule?  xvalue = pool elevation (meters)
               xvalue = currentPoolElevation
          elif xlabel=="Inflow_cms":                    # Inflow based rule?   xvalue = inflow to reservoir
               xvalue = inflow            
          elif xlabel=="Outflow_lagged_24h":            #24h lagged outflow based rule?   xvalue = outflow from reservoir at last timestep
               xvalue = lag_outflow               #placeholder (assumes that timestep=24 hours)
          elif xlabel=="Inflow_lagged_24h":            #24h lagged outflow based rule?   xvalue = outflow from reservoir at last timestep
               xvalue = lag_inflow               #placeholder (assumes that timestep=24 hours)
          elif xlabel=="Date_pool_elev_m":             # Lookup based on two values...date and pool elevation.  x value is date.  y value is pool elevation
               xvalue = doy
               yvalue = currentPoolElevation
          elif xlabel=="Date_Water_year_type":          #Lookup based on two values...date and wateryeartype (storage in 13 USACE reservoirs on May 20th).
               xvalue = doy
               yvalue = waterYear
          elif xlabel == "Date_release_cms": 
               xvalue = doy
               yvalue = lag_outflow 
          else:                                            #Unrecognized xvalue for constraint lookup table
             pass
              #logging.info ("Unrecognized x value for reservoir constraint lookup label = %s", xlabel) 
          #logging.info('The constraint array of i is %s',constraint_array[i])   
          if constraint_array[i].startswith('Max_'):  #case RCT_MAX  maximum
             if yvalue != [] :    # Does the constraint depend on two values?  If so, use both xvalue and yvalue
                 cols=constraintRules.iloc[0,1::]
                 rows=constraintRules.iloc[1::,0]
                 vals=constraintRules.iloc[1::,1::]
                 interp_table = interp2d(cols, rows, vals, kind='linear')
                 constraintValue =float(interp_table(yvalue, xvalue))    
                 #constraintValue =interp_table(xvalue, yvalue)  
             else:             #//If not, just use xvalue
                constraintValue = np.interp(xvalue,constraintRules.iloc[:,0],constraintRules.iloc[:,1])
             if actualRelease >= constraintValue:
                actualRelease = constraintValue;
             

          elif constraint_array[i].startswith('Min_'):  # case RCT_MIN:  //minimum
             if yvalue != [] :    # Does the constraint depend on two values?  If so, use both xvalue and yvalue
                 cols=constraintRules.iloc[0,1::]
                 rows=constraintRules.iloc[1::,0]
                 vals=constraintRules.iloc[1::,1::]
                 interp_table = interp2d(cols, rows, vals, kind='linear')
                 constraintValue =float(interp_table(yvalue, xvalue))                 
             else:             #//If not, just use xvalue
                 constraintValue = np.interp(xvalue,constraintRules.iloc[:,0],constraintRules.iloc[:,1])
             if actualRelease <= constraintValue:
                actualRelease = constraintValue
             #logging.info('The constraint value is %d',constraintValue)   



          elif constraint_array[i].startswith('MaxI_'):     #case RCT_INCREASINGRATE:  //Increasing Rate
             if yvalue != [] :    # Does the constraint depend on two values?  If so, use both xvalue and yvalue
                 cols=constraintRules.iloc[0,1::]
                 rows=constraintRules.iloc[1::,0]
                 vals=constraintRules.iloc[1::,1::]
                 interp_table = interp2d(cols, rows, vals, kind='linear')
                 constraintValue =float(interp_table(yvalue, xvalue)) 
                 constraintValue = constraintValue*24   #Covert hourly to daily                  
             else:             #//If not, just use xvalue
                 constraintValue = np.interp(xvalue,constraintRules.iloc[:,0],constraintRules.iloc[:,1])
                 constraintValue = constraintValue*24   #Covert hourly to daily
             if actualRelease >= lag_outflow  + constraintValue:  #Is planned release more than current release + contstraint? 
                actualRelease = lag_outflow  + constraintValue
             #logging.info('The constraint value is %d',constraintValue)   

                #If so, planned release can be no more than current release + constraint.
                 

          elif constraint_array[i].startswith('MaxD_'):    #case RCT_DECREASINGRATE:  //Decreasing Rate
             if yvalue != [] :    # Does the constraint depend on two values?  If so, use both xvalue and yvalue
                 cols=constraintRules.iloc[0,1::]
                 rows=constraintRules.iloc[1::,0]
                 vals=constraintRules.iloc[1::,1::]
                 interp_table = interp2d(cols, rows, vals, kind='linear')
                 constraintValue =float(interp_table(yvalue, xvalue)) 
                 constraintValue = constraintValue*24   #Covert hourly to daily                  
             else:             #//If not, just use xvalue
                 constraintValue = np.interp(xvalue,constraintRules.iloc[:,0],constraintRules.iloc[:,1])
                 constraintValue = constraintValue*24   #Covert hourly to daily
             if actualRelease <= lag_outflow  - constraintValue:  #Is planned release less than current release - contstraint? 
                actualRelease = lag_outflow  - constraintValue  #If so, planned release can be no less than current release - constraint.
             #logging.info('The constraint value is %d',constraintValue)   

          elif constraint_array[i].startswith('IRRM_'): #special case interim risk reduction measures for GPR
               constraintValue = xvalue
               actualRelease = constraintValue
               
          elif constraint_array[i].startswith('cp_'):  #case RCT_CONTROLPOINT:  #Downstream control point  
              #Determine which control point this is.....use COMID to identify
              for j in range(len(CP_list)):
                  if CP_list[j].COMID in constraint_array[i]:
                      cp_name = CP_list[j]
                      cp_id = CP_list[j].ID        
                      if str(name.ID) in cp_name.influencedReservoirs:  #Make sure that the reservoir is on the influenced reservoir list
                          resallocation=np.nan 
                          if yvalue != [] :    # Does the constraint depend on two values?  If so, use both xvalue and yvalue
                              cols=constraintRules.iloc[0,1::]
                              rows=constraintRules.iloc[1::,0]
                              vals=constraintRules.iloc[1::,1::]
                              interp_table = interp2d(cols, rows, vals, kind='linear')
                              constraintValue =float(interp_table(yvalue, xvalue)) 
                          else:             #//If not, just use xvalue
                              constraintValue = np.interp(xvalue,constraintRules.iloc[:,0],constraintRules.iloc[:,1])
                              #Compare to current discharge and allocate flow increases or decreases
                              #Currently allocated evenly......need to update based on storage balance curves in ResSIM 
                          if constraint_array[i].startswith('cp_Max'):  #maximum    
                              if cp_discharge[cp_id-1] > constraintValue:   #Are we above the maximum flow?   
                                  resallocation = (constraintValue - cp_discharge[cp_id-1])/len(cp_name.influencedReservoirs) #Allocate decrease in releases (should be negative) over "controlled" reservoirs if maximum, evenly for now
                              else:  
                                  resallocation = 0
                          elif constraint_array[i].startswith('cp_Min'):  #minimum
                              if cp_discharge[cp_id-1] < constraintValue:   #Are we below the minimum flow?  
                                 resallocation = (constraintValue - cp_discharge[cp_id-1])/len(cp_name.influencedReservoirs) 
                              else:  
                                  resallocation = 0
                          actualRelease += resallocation #add/subract cp allocation
#                          if resallocation != 0:
#                              logging.info('The resallocation is %d',resallocation)               
          #GATE SPECIFIC RULES:   
          elif constraint_array[i].startswith('Pow_Max'): # case RCT_POWERPLANT:  //maximum Power plant rule  Assign m_maxPowerFlow attribute.
               constraintValue = np.interp(xvalue,constraintRules.iloc[:,0],constraintRules.iloc[:,1])
               name.maxPowerFlow = constraintValue  #Just for this timestep.  name.MaxPowerFlow is the physical limitation for the reservoir.
          elif constraint_array[i].startswith('Pow_Min'): # case RCT_POWERPLANT:  //minimum Power plant rule  Assign m_minPowerFlow attribute.
               constraintValue = np.interp(xvalue,constraintRules.iloc[:,0],constraintRules.iloc[:,1])
               name.minPowerFlow = constraintValue 
           
            
          elif constraint_array[i].startswith('RO_Max'): #case RCT_REGULATINGOUTLET:  Max Regulating outlet rule, Assign m_maxRO_Flow attribute.
               constraintValue = np.interp(xvalue,constraintRules.iloc[:,0],constraintRules.iloc[:,1])
               name.maxRO_Flow  = constraintValue  
          elif constraint_array[i].startswith('RO_Min'): #Min Regulating outlet rule, Assign m_maxRO_Flow attribute.
               constraintValue = np.interp(xvalue,constraintRules.iloc[:,0],constraintRules.iloc[:,1])
               name.minRO_Flow  = constraintValue 


          elif constraint_array[i].startswith('Spill_Max'): #  case RCT_SPILLWAY:   //Max Spillway rule
               constraintValue = np.interp(xvalue,constraintRules.iloc[:,0],constraintRules.iloc[:,1])
               name.maxSpillwayFlow  = constraintValue  
          elif constraint_array[i].startswith('Spill_Min'): #Min Spillway rule
               constraintValue = np.interp(xvalue,constraintRules.iloc[:,0],constraintRules.iloc[:,1])
               name.minSpillwayFlow  = constraintValue 
                
               
          if actualRelease < 0:
             actualRelease = 0
          if actualRelease < name.minOutflow:         # No release values less than the minimum
             actualRelease = name.minOutflow
          if currentPoolElevation < name.inactive_elev:     #In the inactive zone, water is not accessible for release from any of the gates.
             actualRelease = lag_outflow *0.5

            
          outflow = actualRelease
    if name.Restype!='Storage_flood':
        [powerFlow,RO_flow,spillwayFlow]=AssignReservoirOutletFlows(name,outflow)
    else:
        [powerFlow,RO_flow,spillwayFlow]=[np.nan, np.nan, np.nan]
    return outflow, powerFlow,RO_flow,spillwayFlow, lag_zone
    #return outflow


def CalculateHydropowerOutput(name,elevation,powerFlow):
    head = elevation - name.Tailwater_elev 
    powerOut = (1000*powerFlow*9.81*head*0.9)/1000000  #assume a 0.9 turbine efficiency
    
    if powerOut > name.maxHydro:
        powerOut = name.maxHydro

    return powerOut

def UpdateVolume_elev (name, inflow, outflow, lag_volume):
    volume = lag_volume + (inflow - outflow)*86400
    elevation = GetPoolElevationFromVolume(volume,name)
    
    return(volume, elevation)
    