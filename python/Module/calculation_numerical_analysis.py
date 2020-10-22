# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 17:00:23 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Numerical Calculation
"""

import numpy as np

from scipy import interpolate 
from scipy.optimize import curve_fit

#------------------------------------------------------------------------------
"""
Calculation of list normalization

Args:
    which_list: list to be operated
    
Returns:
    normalized list
"""
def Normalize(which_list):
    
    minimum=np.min(which_list)
    maximum=np.max(which_list)

    if minimum==maximum:
            
        return [0]*len(which_list)
            
    else:
            
        return list((np.array(which_list)-minimum)/(maximum-minimum))
    
#------------------------------------------------------------------------------
"""
List image matrix gray value of pixel in 8-neighbor

Args:
    img: image to be operated
    i,j: index of piexel
    
Returns:
    8-neighbor neighbor list
"""
def Neighbor(img,i,j):
    
    #image matrix index of pixel in 8-neighbor
    index_neighbor=[[i+diff_i,j+diff_j]for diff_i in [-1,0,1] for diff_j in [-1,0,1]]
    
    return [img[this_i,this_j] for this_i,this_j in index_neighbor if [this_i,this_j]!=[i,j]]

#------------------------------------------------------------------------------
"""
Calculation Polynomial fitting

Args:
    X: X array
    Y: Y array
    exp: exp index
    n_step: amount of step
    
Returns:
    Parabola Fitting value
"""
def PolynomialFitting(list_x,list_y,exp,n_step=100):
    
    x_min,x_max=np.min(list_x),np.max(list_x)
    
    #polyfit process
    list_x_polyfit=np.linspace(x_min,x_max,n_step)
    list_y_polifit=np.polyval(np.polyfit(list_x,list_y,exp),list_x_polyfit)

    return [[list_x_polyfit[k],list_y_polifit[k]] for k in range(len(list_x_polyfit))] 

#------------------------------------------------------------------------------
"""
B-Spline Interpolation on 1D

Args:
    X: X array
    Y: Y array
    n_step: amount of step
    
Returns:
    Interpolatd coordinates serial
""" 
def BSplineInterpolation(X,Y,n_step=100):
    
    X_new = np.linspace(min(X),max(X),n_step)

    Y_new = interpolate.splev(X_new,interpolate.splrep(X, Y))
    
    return [[X_new[k],Y_new[k]] for k in range(len(X_new))]

#------------------------------------------------------------------------------
"""
Optimized Fitting based on model function

Args:
    X: X array
    Y: Y array
    n_step: amount of step
    
Returns:
    Optimized fitting serial
""" 
def OptimizedFitting(list_x,list_y,n_step=100):
    
    def func(x, a, b, c):
    
        return c+b/(x)
     
    x_min,x_max=np.min(list_x),np.max(list_x)

    #polyfit process
    x_new=np.linspace(x_min,x_max,n_step)
    
    #curve fitting, POPT is the parameter list of the function
    popt,pcpv= curve_fit(func, list_x, list_y)
    
    #the function and the function argument list are used directly to calculate the y value
    y_new = [func(i, popt[0], popt[1], popt[2]) for i in x_new] 
    
    return [[x_new[k],y_new[k]] for k in range(len(x_new))]

#------------------------------------------------------------------------------
"""
P-Chip Interpolation on 1D

Args:
    X: X array
    Y: Y array
    n_step: amount of step
    
Returns:
    Interpolatd coordinates serial
""" 
def PChipInterpolation(X,Y,n_step=100):
    
    X_new = np.linspace(min(X),max(X),n_step)

    Y_new = interpolate.PchipInterpolator(X, Y)(X_new)
    
    return [[X_new[k],Y_new[k]] for k in range(len(X_new))]
