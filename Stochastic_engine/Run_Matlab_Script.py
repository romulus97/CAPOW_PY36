# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:53:12 2018

@author: YSu
"""

import matlab.engine
eng = matlab.engine.start_matlab()
eng.ICF_calc_new(nargout=0)
eng.FCRPS_New(nargout=0)
