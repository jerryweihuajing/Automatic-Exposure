# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:59:21 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Curve Plot
"""

import numpy as np
import matplotlib.pyplot as plt

import calculation_numerical_analysis as C_N_A

from matplotlib.pyplot import MultipleLocator
from configuration_font import legend_prop,label_prop,title_prop,sample_prop

#------------------------------------------------------------------------------
"""
Plot Curve whose info was obtained from parameter list

Args:
    list_x: X seriel
    list_y: T seriel
    color_curve: color of corve
    str_title: title string
    str_xlabel: xlabel string
    str_ylabel: ylabel string
    str_legend: legend string
    
Returns:
    None
"""
def Curve(list_x,
          list_y,
          color_curve,
          str_legend,
          str_xlabel,
          str_ylabel,
          str_title,
          method_smoothing='optimized fitting'):
    
    #limit of x and y
    x_min,x_max=np.min(list_x),np.max(list_x)
    y_min,y_max=np.min(list_y),np.max(list_y)
    
    #tick step
    x_major_step=np.ceil((x_max-x_min)/10/50)*50
    x_minor_step=np.ceil((x_max-x_min)/10/50)*25
    
    scale='macro'
    
    if y_max-y_min<1:
        
        scale='micro'
        
    if scale=='macro':
        
        y_major_step=np.ceil((y_max-y_min)/10/50)*50
        y_minor_step=np.ceil((y_max-y_min)/10/50)*25
        
    if scale=='micro':
        
        y_major_step=np.ceil((y_max-y_min)*50)/10/50
        y_minor_step=np.ceil((y_max-y_min)*25)/10/50
        
    plt.figure(figsize=(13,6))
    
    '''p-chip interpolation'''
    if method_smoothing=='p-chip interpolation':
    
        smoothed_x_y=C_N_A.PChipInterpolation(list_x,list_y,1000)
        
        X=[this_x_y[0] for this_x_y in smoothed_x_y]
        Y=[this_x_y[1] for this_x_y in smoothed_x_y] 
    
    '''polynomial fitting'''
    if method_smoothing=='polynomial fitting':
        
        polyfitted_x_y=C_N_A.PolynomialFitting(list_x,list_y,3,1000)
        
        X=[this_x_y[0] for this_x_y in polyfitted_x_y]
        Y=[this_x_y[1] for this_x_y in polyfitted_x_y] 

    '''optimized fitting'''
    if method_smoothing=='optimized fitting':
        
        optimizedfitted_x_y=C_N_A.OptimizedFitting(list_x,list_y,1000)
        
        X=[this_x_y[0] for this_x_y in optimizedfitted_x_y]
        Y=[this_x_y[1] for this_x_y in optimizedfitted_x_y]
    
    plt.plot(X,Y,color=color_curve,label=str_legend)
    
    for k in range(len(list_x)):
        
        plt.scatter(list_x[k],list_y[k],color='k')
        
        if scale=='micro':
            
            value_format='%.2f'
            
        if scale=='macro':
            
            value_format='%.d'
            
        plt.annotate(value_format%list_y[k],
                     xy=(list_x[k],list_y[k]),
                     xytext=(list_x[k]+0.1*x_major_step,
                             list_y[k]+0.1*y_major_step),
                     color='k',
                     fontproperties=sample_prop)
        
    ax=plt.gca()
    
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
    
    #axis boundary
    plt.xlim([x_min-x_minor_step,x_max+x_minor_step])
    plt.ylim([y_min-y_minor_step,y_max+y_minor_step])  
     
    #set ticks fonts
    plt.tick_params(labelsize=12)
    labels=ax.get_xticklabels()+ax.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title(str_title,fontdict=title_prop)
    
    plt.xlabel(str_xlabel,fontdict=label_prop)
    plt.ylabel(str_ylabel,fontdict=label_prop)
    
    plt.legend(prop=legend_prop,loc='upper right')  
    
    #show the grid
    plt.grid()
    plt.show()
    
def CurveBatch(list_x_batch,
               list_y_batch,
               color_curve_batch,
               str_legend_batch,
               str_xlabel,
               str_ylabel,
               str_title,
               method_smoothing='optimized fitting'):
    
    #list x batch defined as a serial
    global_list_x=[]
    global_list_y=[]
    
    for k in range(len(list_x_batch)):
        
        global_list_x+=list(list_x_batch[k])
        global_list_y+=list(list_y_batch[k])
    
    #limit of x and y
    x_min,x_max=np.min(global_list_x),np.max(global_list_x)
    y_min,y_max=np.min(global_list_y),np.max(global_list_y)
    
    #tick step
    x_major_step=np.ceil((x_max-x_min)/10/50)*50
    x_minor_step=np.ceil((x_max-x_min)/10/50)*25
    
    scale='macro'
    
    if y_max-y_min<1:
        
        scale='micro'
        
    if scale=='macro':
        
        y_major_step=np.ceil((y_max-y_min)/10/50)*50
        y_minor_step=np.ceil((y_max-y_min)/10/50)*25
        
    if scale=='micro':
        
        y_major_step=np.ceil((y_max-y_min)*50)/10/50
        y_minor_step=np.ceil((y_max-y_min)*25)/10/50
        
    plt.figure(figsize=(13,6))
    
    for k in range(len(list_x_batch)):
            
        this_list_x=list_x_batch[k]
        this_list_y=list_y_batch[k]
        this_color_curve=color_curve_batch[k]
        this_str_legend=str_legend_batch[k]
        
        '''p-chip interpolation'''
        if method_smoothing=='p-chip interpolation':
        
            smoothed_x_y=C_N_A.PChipInterpolation(this_list_x,this_list_y,1000)
            
            X=[this_x_y[0] for this_x_y in smoothed_x_y]
            Y=[this_x_y[1] for this_x_y in smoothed_x_y] 
        
        '''polynomial fitting'''
        if method_smoothing=='polynomial fitting':
            
            polyfitted_x_y=C_N_A.PolynomialFitting(this_list_x,this_list_y,3,1000)
            
            X=[this_x_y[0] for this_x_y in polyfitted_x_y]
            Y=[this_x_y[1] for this_x_y in polyfitted_x_y] 
    
        '''optimized fitting'''
        if method_smoothing=='optimized fitting':
            
            optimizedfitted_x_y=C_N_A.OptimizedFitting(this_list_x,this_list_y,1000)
            
            X=[this_x_y[0] for this_x_y in optimizedfitted_x_y]
            Y=[this_x_y[1] for this_x_y in optimizedfitted_x_y]
        
        plt.plot(X,Y,color=this_color_curve,label=this_str_legend)
    
        for kk in range(len(this_list_x)):
            
            plt.scatter(this_list_x[kk],this_list_y[kk],color=this_color_curve)
            
    ax=plt.gca()
    
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
    
    #axis boundary
    plt.xlim([x_min-x_minor_step,x_max+x_minor_step])
    plt.ylim([y_min-y_minor_step,y_max+y_minor_step])  
     
    #set ticks fonts
    plt.tick_params(labelsize=12)
    labels=ax.get_xticklabels()+ax.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title(str_title,fontdict=title_prop)
    
    plt.xlabel(str_xlabel,fontdict=label_prop)
    plt.ylabel(str_ylabel,fontdict=label_prop)
    
    plt.legend(prop=legend_prop,loc='upper right')  
    
    #show the grid
    plt.grid()
    plt.show()