# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 10:54:44 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Configuration for Simulation of Auto Focus Calibration
"""

from __init__ import *

import numpy as np

offset_end=5
offset_start=0.5

#regard the distance grow meter by 125 millimeter
interval_offset=0.125

n_interval=int(np.floor((offset_end-offset_start)/interval_offset))

canvas=np.zeros((1920,1920))

'''add the circle lap by lap'''
radius_circle_original=8
interval_circle_original=36
