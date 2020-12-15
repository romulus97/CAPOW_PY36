# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 16:20:03 2018

@author: sdenaro
"""
def launch(sim_years):
    
    import sys
    sys.path.append('Willamette/')
    import Willamette_model as inner #reading in the inner function
    #import time
    initial_doy=1 #Set the simulation initial_doy
    sys.argv = ["Willamette/settings.xml", str(initial_doy)] #simulation inputs
    #starttime = time.time()
    import Willamette_outer
    Willamette_outer.simulate(sim_years)
#elapsed = time.time() - starttime
    
    return None