# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:14:07 2017

@author: YSu
"""

from pyomo.opt import SolverFactory
from CA_dispatch import model as m1
from CA_dispatchLP import model as m2
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
            instance.HorizonPath66_imports[d] = instance.SimPath66_imports[day-1+d]
            instance.HorizonPath46_SCE_imports[d] = instance.SimPath46_SCE_imports[day-1+d]
            instance.HorizonPath61_imports[d] = instance.SimPath61_imports[day-1+d]
            instance.HorizonPath42_imports[d] = instance.SimPath42_imports[day-1+d]
            instance.HorizonPath24_imports[d] = instance.SimPath24_imports[day-1+d]
            instance.HorizonPath45_imports[d] = instance.SimPath45_imports[day-1+d]
            instance.HorizonPGE_valley_hydro[d] = instance.SimPGE_valley_hydro[day-1+d]
            instance.HorizonSCE_hydro[d] = instance.SimSCE_hydro[day-1+d]

        for i in K:
            instance.HorizonReserves[i] = instance.SimReserves[(day-1)*24+i]
            instance.HorizonPath42_exports[i] = instance.SimPath42_exports[(day-1)*24+i]
            instance.HorizonPath24_exports[i] = instance.SimPath24_exports[(day-1)*24+i]
            instance.HorizonPath45_exports[i] = instance.SimPath45_exports[(day-1)*24+i]
            instance.HorizonPath66_exports[i] = instance.SimPath66_exports[(day-1)*24+i]

            instance.HorizonPath46_SCE_minflow[i] = instance.SimPath46_SCE_imports_minflow[(day-1)*24+i]
            instance.HorizonPath66_minflow[i] = instance.SimPath66_imports_minflow[(day-1)*24+i]
            instance.HorizonPath42_minflow[i] = instance.SimPath42_imports_minflow[(day-1)*24+i]
            instance.HorizonPath61_minflow[i] = instance.SimPath61_imports_minflow[(day-1)*24+i]
            instance.HorizonPGE_valley_hydro_minflow[i] = instance.SimPGE_valley_hydro_minflow[(day-1)*24+i]
            instance.HorizonSCE_hydro_minflow[i] = instance.SimSCE_hydro_minflow[(day-1)*24+i]
    #
        CAISO_result = opt.solve(instance)
        instance.solutions.load_from(CAISO_result)

        for z in instance2.zones:

            instance2.GasPrice[z] = instance2.SimGasPrice[z,day]

            for i in K:
                instance2.HorizonDemand[z,i] = instance2.SimDemand[z,(day-1)*24+i]
                instance2.HorizonWind[z,i] = instance2.SimWind[z,(day-1)*24+i]
                instance2.HorizonSolar[z,i] = instance2.SimSolar[z,(day-1)*24+i]
                instance2.HorizonMustRun[z,i] = instance2.SimMustRun[z,(day-1)*24+i]

        for d in range(1,D+1):
            instance2.HorizonPath66_imports[d] = instance2.SimPath66_imports[day-1+d]
            instance2.HorizonPath46_SCE_imports[d] = instance2.SimPath46_SCE_imports[day-1+d]
            instance2.HorizonPath61_imports[d] = instance2.SimPath61_imports[day-1+d]
            instance2.HorizonPath42_imports[d] = instance2.SimPath42_imports[day-1+d]
            instance2.HorizonPath24_imports[d] = instance2.SimPath24_imports[day-1+d]
            instance2.HorizonPath45_imports[d] = instance2.SimPath45_imports[day-1+d]
            instance2.HorizonPGE_valley_hydro[d] = instance2.SimPGE_valley_hydro[day-1+d]
            instance2.HorizonSCE_hydro[d] = instance2.SimSCE_hydro[day-1+d]

        for i in K:
            instance2.HorizonReserves[i] = instance2.SimReserves[(day-1)*24+i]
            instance2.HorizonPath42_exports[i] = instance2.SimPath42_exports[(day-1)*24+i]
            instance2.HorizonPath24_exports[i] = instance2.SimPath24_exports[(day-1)*24+i]
            instance2.HorizonPath45_exports[i] = instance2.SimPath45_exports[(day-1)*24+i]
            instance2.HorizonPath66_exports[i] = instance2.SimPath66_exports[(day-1)*24+i]

            instance2.HorizonPath46_SCE_minflow[i] = instance2.SimPath46_SCE_imports_minflow[(day-1)*24+i]
            instance2.HorizonPath66_minflow[i] = instance2.SimPath66_imports_minflow[(day-1)*24+i]
            instance2.HorizonPath42_minflow[i] = instance2.SimPath42_imports_minflow[(day-1)*24+i]
            instance2.HorizonPath61_minflow[i] = instance2.SimPath61_imports_minflow[(day-1)*24+i]
            instance2.HorizonPGE_valley_hydro_minflow[i] = instance2.SimPGE_valley_hydro_minflow[(day-1)*24+i]
            instance2.HorizonSCE_hydro_minflow[i] = instance2.SimSCE_hydro_minflow[(day-1)*24+i]
        for j in instance.Generators:
            for t in K:
                if instance.on[j,t] == 1:
                    instance2.on[j,t] = 1
                    instance2.on[j,t].fixed = True
                else:
                    instance.on[j,t] = 0
                    instance2.on[j,t] = 0
                    instance2.on[j,t].fixed = True

                if instance.switch[j,t] == 1:
                    instance2.switch[j,t] = 1
                    instance2.switch[j,t].fixed = True
                else:
                    instance2.switch[j,t] = 0
                    instance2.switch[j,t] = 0
                    instance2.switch[j,t].fixed = True
        results = opt.solve(instance2)
        instance2.solutions.load_from(results)



        print ("Duals")

        for c in instance2.component_objects(Constraint, active=True):
    #        print ("   Constraint",c)
            cobject = getattr(instance2, str(c))
            if str(c) in ['Bal1Constraint','Bal2Constraint','Bal3Constraint','Bal4Constraint']:
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
                if index[0] in instance.Zone1Generators:

                    gas_price = instance.GasPrice['PGE_valley'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg1*gas_price
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg1*2
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg1*20
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Slack',marginal_cost))
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Hydro',marginal_cost))


                elif index[0] in instance.Zone2Generators:

                    gas_price = instance.GasPrice['PGE_bay'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg1*gas_price
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg1*2
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg1*20
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Slack',marginal_cost))

                elif index[0] in instance.Zone3Generators:

                    gas_price = instance.GasPrice['SCE'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg1*gas_price
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg1*2
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg1*20
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Slack',marginal_cost))
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Hydro',marginal_cost))

                elif index[0] in instance.Zone4Generators:

                    gas_price = instance.GasPrice['SDGE'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg1*gas_price
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg1*2
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg1*20
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Slack',marginal_cost))


                elif index[0] in instance.WECCImportsSDGE:

                    gas_price = instance.GasPrice['SDGE'].value
                    marginal_cost = 14.5+2.76*gas_price
                    mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','imports',marginal_cost))


                elif index[0] in instance.WECCImportsSCE:

                    gas_price = instance.GasPrice['SCE'].value
                    marginal_cost = 14.5+2.76*gas_price
                    mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','imports',marginal_cost))


                elif index[0] in instance.WECCImportsPGEV:

                    marginal_cost = 5
                    mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','imports',marginal_cost))


            if a=='mwh_2':

             for index in varobject:

               name = index[0]
               g = df_generators[df_generators['name']==name]
               seg2 = g['seg2'].values
               seg2 = seg2[0]

               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone1Generators:

                    gas_price = instance.GasPrice['PGE_valley'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg2*gas_price
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg2*2
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg2*20
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Slack',marginal_cost))
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Hydro',marginal_cost))


                elif index[0] in instance.Zone2Generators:

                    gas_price = instance.GasPrice['PGE_bay'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg2*gas_price
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg2*2
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg2*20
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Slack',marginal_cost))

                elif index[0] in instance.Zone3Generators:

                    gas_price = instance.GasPrice['SCE'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg2*gas_price
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg2*2
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg2*20
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Slack',marginal_cost))
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Hydro',marginal_cost))

                elif index[0] in instance.Zone4Generators:

                    gas_price = instance.GasPrice['SDGE'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg2*gas_price
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg2*2
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg2*20
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Slack',marginal_cost))


                elif index[0] in instance.WECCImportsSDGE:

                    gas_price = instance.GasPrice['SDGE'].value
                    marginal_cost = 14.5+2.76*gas_price
                    mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','imports',marginal_cost))


                elif index[0] in instance.WECCImportsSCE:

                    gas_price = instance.GasPrice['SCE'].value
                    marginal_cost = 14.5+2.76*gas_price
                    mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','imports',marginal_cost))


                elif index[0] in instance.WECCImportsPGEV:

                    marginal_cost = 5
                    mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','imports',marginal_cost))


            if a=='mwh_3':

             for index in varobject:

               name = index[0]
               g = df_generators[df_generators['name']==name]
               seg3 = g['seg3'].values
               seg3 = seg3[0]

               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone1Generators:

                    gas_price = instance.GasPrice['PGE_valley'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg3*gas_price
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg3*2
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg3*20
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Slack',marginal_cost))
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Hydro',marginal_cost))


                elif index[0] in instance.Zone2Generators:

                    gas_price = instance.GasPrice['PGE_bay'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg3*gas_price
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg3*2
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg3*20
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Slack',marginal_cost))

                elif index[0] in instance.Zone3Generators:

                    gas_price = instance.GasPrice['SCE'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg3*gas_price
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg3*2
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg3*20
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Slack',marginal_cost))
                    elif index[0] in instance.Hydro:
                        marginal_cost = 0
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Hydro',marginal_cost))

                elif index[0] in instance.Zone4Generators:

                    gas_price = instance.GasPrice['SDGE'].value

                    if index[0] in instance.Gas:
                        marginal_cost = seg3*gas_price
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Gas',marginal_cost))
                    elif index[0] in instance.Coal:
                        marginal_cost = seg3*2
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Coal',marginal_cost))
                    elif index[0] in instance.Oil:
                        marginal_cost = seg3*20
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Oil',marginal_cost))
                    elif index[0] in instance.PSH:
                        marginal_cost = 10
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','PSH',marginal_cost))
                    elif index[0] in instance.Slack:
                        marginal_cost = 700
                        mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Slack',marginal_cost))


                elif index[0] in instance.WECCImportsSDGE:

                    gas_price = instance.GasPrice['SDGE'].value
                    marginal_cost = 14.5+2.76*gas_price
                    mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','imports',marginal_cost))


                elif index[0] in instance.WECCImportsSCE:

                    gas_price = instance.GasPrice['SCE'].value
                    marginal_cost = 14.5+2.76*gas_price
                    mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','imports',marginal_cost))


                elif index[0] in instance.WECCImportsPGEV:

                    marginal_cost = 5
                    mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','imports',marginal_cost))


            if a=='on':

             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone1Generators:
                 on.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley'))
                elif index[0] in instance.Zone2Generators:
                 on.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay'))
                elif index[0] in instance.Zone3Generators:
                 on.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE'))
                elif index[0] in instance.Zone4Generators:
                 on.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE'))


            if a=='switch':

             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone1Generators:
                 switch.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley'))
                elif index[0] in instance.Zone2Generators:
                 switch.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay'))
                elif index[0] in instance.Zone3Generators:
                 switch.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE'))
                elif index[0] in instance.Zone4Generators:
                 switch.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE'))


            if a=='srsv':

             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone1Generators:
                 srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley'))
                elif index[0] in instance.Zone2Generators:
                 srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay'))
                elif index[0] in instance.Zone3Generators:
                 srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE'))
                elif index[0] in instance.Zone4Generators:
                 srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE'))


            if a=='nrsv':

             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                if index[0] in instance.Zone1Generators:
                 nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley'))
                elif index[0] in instance.Zone2Generators:
                 nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay'))
                elif index[0] in instance.Zone3Generators:
                 nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE'))
                elif index[0] in instance.Zone4Generators:
                 nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE'))


            if a=='solar':

             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                solar.append((index[0],index[1]+((day-1)*24),varobject[index].value))


            if a=='wind':

             for index in varobject:
               if int(index[1]>0 and index[1]<25):
                wind.append((index[0],index[1]+((day-1)*24),varobject[index].value))

            if a=='flow':

             for index in varobject:
               if int(index[2]>0 and index[2]<25):
                flow.append((index[0],index[1],index[2]+((day-1)*24),varobject[index].value))


            for j in instance.Generators:
                if instance.on[j,24] == 1:
                    instance.on[j,0] = 1
                else:
                    instance.on[j,0] = 0
                instance.on[j,0].fixed = True

                if instance.mwh_1[j,24].value <=0 and instance.mwh_1[j,24].value>= -0.0001:
                    newval_1=0
                else:
                    newval_1=instance.mwh_1[j,24].value
                instance.mwh_1[j,0] = newval_1
                instance.mwh_1[j,0].fixed = True

                if instance.mwh_2[j,24].value <=0 and instance.mwh_2[j,24].value>= -0.0001:
                    newval=0
                else:
                    newval=instance.mwh_2[j,24].value

                if instance.mwh_3[j,24].value <=0 and instance.mwh_3[j,24].value>= -0.0001:
                    newval2=0
                else:
                    newval2=instance.mwh_3[j,24].value


                instance.mwh_2[j,0] = newval
                instance.mwh_2[j,0].fixed = True
                instance.mwh_3[j,0] = newval2
                instance.mwh_3[j,0].fixed = True
                if instance.switch[j,24] == 1:
                    instance.switch[j,0] = 1
                else:
                    instance.switch[j,0] = 0
                instance.switch[j,0].fixed = True

                if instance.srsv[j,24].value <=0 and instance.srsv[j,24].value>= -0.0001:
                    newval_srsv=0
                else:
                    newval_srsv=instance.srsv[j,24].value
                instance.srsv[j,0] = newval_srsv
                instance.srsv[j,0].fixed = True

                if instance.nrsv[j,24].value <=0 and instance.nrsv[j,24].value>= -0.0001:
                    newval_nrsv=0
                else:
                    newval_nrsv=instance.nrsv[j,24].value
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
    flow_pd=pd.DataFrame(flow,columns=('Source','Sink','Time','Value'))
    shadow_price=pd.DataFrame(Duals,columns=('Constraint','Time','Value'))

    flow_pd.to_csv('flow.csv')
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
