# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 19:25:54 2019

@author: Joy Hill
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 12:03:41 2018

@author: Joy Hill
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:14:07 2017

@author: YSu
"""

from pyomo.opt import SolverFactory
from PNW_dispatch import model as m1
from PNW_dispatchLP import model as m2
from pyomo.core import Var
from pyomo.core import Constraint
from pyomo.core import Param
from operator import itemgetter
import pandas as pd
import numpy as np
from datetime import datetime
import pyomo.environ as pyo

def sim(days):
    
    instance = m1.create_instance('data.dat')
    instance2 = m2.create_instance('data.dat')
    
    instance2.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    opt = SolverFactory("cplex")
   
    
    H = instance.HorizonHours
    D = 2
    K=range(1,H+1)
    
    
    #Space to store results
    mwh_1=[]
    mwh_2=[]
    mwh_3=[]
    on=[]
    switch=[]
    srsv=[]
    nrsv=[]
    solar=[]
    wind=[]
    flow=[]
    Generator=[]
    Duals=[]
    
    df_generators = pd.read_csv('generators.csv',header=0)
    
    instance.ini_on["COLUMBIA_2"] = 1
    instance.ini_mwh_1["COLUMBIA_2"] = 300
        
    #max here can be (1,365)
    for day in range(1,days):
        
         #load time series data
        for z in instance.zones:
            
            instance.GasPrice[z] = instance.SimGasPrice[z,day]
            
            for i in K:
                instance.HorizonDemand[z,i] = instance.SimDemand[z,(day-1)*24+i]
                instance.HorizonWind[z,i] = instance.SimWind[z,(day-1)*24+i]
                instance.HorizonSolar[z,i] = instance.SimSolar[z,(day-1)*24+i]
                instance.HorizonMustRun[z,i] = instance.SimMustRun[z,(day-1)*24+i]
        
        for d in range(1,D+1):
            instance.HorizonPath3_imports[d] = instance.SimPath3_imports[day-1+d]
            instance.HorizonPath8_imports[d] = instance.SimPath8_imports[day-1+d]
            instance.HorizonPath14_imports[d] = instance.SimPath14_imports[day-1+d]
            instance.HorizonPath65_imports[d] = instance.SimPath65_imports[day-1+d]
            instance.HorizonPath66_imports[d] = instance.SimPath66_imports[day-1+d]
            instance.HorizonPNW_hydro[d] = instance.SimPNW_hydro[day-1+d]
            
        for i in K:
            instance.HorizonReserves[i] = instance.SimReserves[(day-1)*24+i] 
            instance.HorizonPath3_exports[i] = instance.SimPath3_exports[(day-1)*24+i] 
            instance.HorizonPath8_exports[i] = instance.SimPath8_exports[(day-1)*24+i] 
            instance.HorizonPath14_exports[i] = instance.SimPath14_exports[(day-1)*24+i]
            instance.HorizonPath65_exports[i] = instance.SimPath65_exports[(day-1)*24+i]             
            instance.HorizonPath66_exports[i] = instance.SimPath66_exports[(day-1)*24+i]  
            
            instance.HorizonPath3_minflow[i] = instance.SimPath3_imports_minflow[(day-1)*24+i]             
            instance.HorizonPath8_minflow[i] = instance.SimPath8_imports_minflow[(day-1)*24+i]             
            instance.HorizonPath14_minflow[i] = instance.SimPath14_imports_minflow[(day-1)*24+i]             
            instance.HorizonPath65_minflow[i] = instance.SimPath65_imports_minflow[(day-1)*24+i]  
            instance.HorizonPath66_minflow[i] = instance.SimPath66_imports_minflow[(day-1)*24+i]  
            instance.HorizonPNW_hydro_minflow[i] = instance.SimPNW_hydro_minflow[(day-1)*24+i]
    #            
        PNW_result = opt.solve(instance)
        instance.solutions.load_from(PNW_result)   
        
        for z in instance2.zones:
            
            instance2.GasPrice[z] = instance2.SimGasPrice[z,day]
            
            for i in K:
                instance2.HorizonDemand[z,i] = instance2.SimDemand[z,(day-1)*24+i]
                instance2.HorizonWind[z,i] = instance2.SimWind[z,(day-1)*24+i]
                instance2.HorizonSolar[z,i] = instance2.SimSolar[z,(day-1)*24+i]
                instance2.HorizonMustRun[z,i] = instance2.SimMustRun[z,(day-1)*24+i]
        
        for d in range(1,D+1):
            instance2.HorizonPath3_imports[d] = instance2.SimPath3_imports[day-1+d]
            instance2.HorizonPath8_imports[d] = instance2.SimPath8_imports[day-1+d]
            instance2.HorizonPath14_imports[d] = instance2.SimPath14_imports[day-1+d]
            instance2.HorizonPath65_imports[d] = instance2.SimPath65_imports[day-1+d]
            instance2.HorizonPath66_imports[d] = instance2.SimPath66_imports[day-1+d]
            instance2.HorizonPNW_hydro[d] = instance2.SimPNW_hydro[day-1+d]
            
        for i in K:
            instance2.HorizonReserves[i] = instance2.SimReserves[(day-1)*24+i] 
            instance2.HorizonPath3_exports[i] = instance2.SimPath3_exports[(day-1)*24+i] 
            instance2.HorizonPath8_exports[i] = instance2.SimPath8_exports[(day-1)*24+i] 
            instance2.HorizonPath14_exports[i] = instance2.SimPath14_exports[(day-1)*24+i]
            instance2.HorizonPath65_exports[i] = instance2.SimPath65_exports[(day-1)*24+i]             
            instance2.HorizonPath66_exports[i] = instance2.SimPath66_exports[(day-1)*24+i]  
            
            instance2.HorizonPath3_minflow[i] = instance2.SimPath3_imports_minflow[(day-1)*24+i]             
            instance2.HorizonPath8_minflow[i] = instance2.SimPath8_imports_minflow[(day-1)*24+i]             
            instance2.HorizonPath14_minflow[i] = instance2.SimPath14_imports_minflow[(day-1)*24+i]             
            instance2.HorizonPath65_minflow[i] = instance2.SimPath65_imports_minflow[(day-1)*24+i]  
            instance2.HorizonPath66_minflow[i] = instance2.SimPath66_imports_minflow[(day-1)*24+i]  
            instance2.HorizonPNW_hydro_minflow[i] = instance2.SimPNW_hydro_minflow[(day-1)*24+i]
    #            
        results = opt.solve(instance2)
        instance2.solutions.load_from(results)   
        
        
        print ("Duals")
    
        for c in instance2.component_objects(Constraint, active=True):
    #        print ("   Constraint",c)
            cobject = getattr(instance2, str(c))
            if str(c) == 'Bal5Constraint':
                for index in cobject:
                     if int(index>0 and index<25):
    #                print ("   Constraint",c)
                         Duals.append((str(c),index+((day-1)*24), instance2.dual[cobject[index]]))
    #            print ("      ", index, instance2.dual[cobject[index]])

     
        #The following section is for storing and sorting results
        for v in instance.component_objects(Var, active=True):
            varobject = getattr(instance, str(v))
            a=str(v)
            if a=='mwh_1':
             
             for index in varobject:
                 
               name = index[0]     
               g = df_generators[df_generators['name']==name]
               seg1 = g['seg1'].values
               seg1 = seg1[0]  
                 
                 
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                    
                    gas_price = instance.GasPrice['PNW'].value
                    
                    
                    if index[0] in instance.Gas:
                        marginal_cost = seg1*gas_price
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Gas',marginal_cost))                  
                    elif index[0] in instance.Coal:
                        marginal_cost = seg1*2
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg1*20
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Oil',marginal_cost))
                    elif index[0] in instance.Nuclear:
                        marginal_cost = 10
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Nuclear',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Slack',marginal_cost))               
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Hydro',marginal_cost))                
                        
                
        
                elif index[0] in instance.WECCImports:
                    mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'WECC','imports',0))
                      
    
            if a=='mwh_2':
           
             for index in varobject:
                 
               name = index[0]     
               g = df_generators[df_generators['name']==name]
               seg2 = g['seg2'].values
               seg2 = seg2[0]  
    
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                    
                    gas_price = instance.GasPrice['PNW'].value
                    
                    if index[0] in instance.Gas:
                        marginal_cost = seg2*gas_price
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Gas',marginal_cost))                  
                    elif index[0] in instance.Coal:
                        marginal_cost = seg2*2
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg2*20
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Oil',marginal_cost))
                    elif index[0] in instance.Nuclear:
                        marginal_cost = 10
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Nuclear',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Slack',marginal_cost))               
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Hydro',marginal_cost))         
                
                elif index[0] in instance.WECCImports:
                    mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'WECC','imports',0))
     
            
            if a=='mwh_3':
               
             for index in varobject:
                 
               name = index[0]     
               g = df_generators[df_generators['name']==name]
               seg3 = g['seg3'].values
               seg3 = seg3[0]  
                 
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                    
                    gas_price = instance.GasPrice['PNW'].value
                    
                    if index[0] in instance.Gas:
                        marginal_cost = seg3*gas_price
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Gas',marginal_cost))                  
                    elif index[0] in instance.Coal:
                        marginal_cost = seg3*2
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg3*20
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Oil',marginal_cost))
                    elif index[0] in instance.Nuclear:
                        marginal_cost = 10
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Nuclear',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Slack',marginal_cost))               
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW','Hydro',marginal_cost))         
                
                elif index[0] in instance.WECCImports:
                    mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'WECC','imports',0))
        
       
            if a=='on':
                
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                 on.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW'))
                 
          
             
            if a=='switch':
            
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                 switch.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW'))
               
        
             
            if a=='srsv':
            
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                 srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW'))
              
        
             
            if a=='nrsv':
           
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone5Generators:
                 nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PNW'))
               
             
             
            if a=='solar':
               
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                solar.append((index[0],index[1]+((day-1)*24),varobject[index].value))   
             
              
            if a=='wind':
               
             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                wind.append((index[0],index[1]+((day-1)*24),varobject[index].value))  
                   
            for j in instance.Generators:
                if instance.on[j,H] == 1:
                    instance.on[j,0] = 1
                else: 
                    instance.on[j,0] = 0
                instance.on[j,0].fixed = True
                           
                if instance.mwh_1[j,H].value <=0 and instance.mwh_1[j,H].value>= -0.0001:
                    newval_1=0
                else:
                    newval_1=instance.mwh_1[j,H].value
                instance.mwh_1[j,0] = newval_1
                instance.mwh_1[j,0].fixed = True
                              
                if instance.mwh_2[j,H].value <=0 and instance.mwh_2[j,H].value>= -0.0001:
                    newval=0
                else:
                    newval=instance.mwh_2[j,H].value
                                         
                if instance.mwh_3[j,H].value <=0 and instance.mwh_3[j,H].value>= -0.0001:
                    newval2=0
                else:
                    newval2=instance.mwh_3[j,H].value
                                          
                                          
                instance.mwh_2[j,0] = newval
                instance.mwh_2[j,0].fixed = True
                instance.mwh_3[j,0] = newval2
                instance.mwh_3[j,0].fixed = True 
                if instance.switch[j,H] == 1:
                    instance.switch[j,0] = 1
                else:
                    instance.switch[j,0] = 0
                instance.switch[j,0].fixed = True
              
                if instance.srsv[j,H].value <=0 and instance.srsv[j,H].value>= -0.0001:
                    newval_srsv=0
                else:
                    newval_srsv=instance.srsv[j,H].value
                instance.srsv[j,0] = newval_srsv 
                instance.srsv[j,0].fixed = True        
        
                if instance.nrsv[j,H].value <=0 and instance.nrsv[j,H].value>= -0.0001:
                    newval_nrsv=0
                else:
                    newval_nrsv=instance.nrsv[j,H].value
                instance.nrsv[j,0] = newval_nrsv 
                instance.nrsv[j,0].fixed = True        
                   
        print(day)
    
    mwh_1_pd=pd.DataFrame(mwh_1,columns=('Generator','Time','Value','Zones','Type','$/MWh'))
    mwh_2_pd=pd.DataFrame(mwh_2,columns=('Generator','Time','Value','Zones','Type','$/MWh'))
    mwh_3_pd=pd.DataFrame(mwh_3,columns=('Generator','Time','Value','Zones','Type','$/MWh'))
    on_pd=pd.DataFrame(on,columns=('Generator','Time','Value','Zones'))
    switch_pd=pd.DataFrame(switch,columns=('Generator','Time','Value','Zones'))
    srsv_pd=pd.DataFrame(srsv,columns=('Generator','Time','Value','Zones'))
    nrsv_pd=pd.DataFrame(nrsv,columns=('Generator','Time','Value','Zones'))
    solar_pd=pd.DataFrame(solar,columns=('Zone','Time','Value'))
    wind_pd=pd.DataFrame(wind,columns=('Zone','Time','Value'))
    shadow_price=pd.DataFrame(Duals,columns=('Constraint','Time','Value'))
        
    mwh_1_pd.to_csv('mwh_1.csv')
    mwh_2_pd.to_csv('mwh_2.csv')
    mwh_3_pd.to_csv('mwh_3.csv')
    on_pd.to_csv('on.csv')
    switch_pd.to_csv('switch.csv')
    srsv_pd.to_csv('srsv.csv')
    nrsv_pd.to_csv('nrsv.csv')
    solar_pd.to_csv('solar_out.csv')
    wind_pd.to_csv('wind_out.csv')
    shadow_price.to_csv('shadow_price.csv')
    
    return None
