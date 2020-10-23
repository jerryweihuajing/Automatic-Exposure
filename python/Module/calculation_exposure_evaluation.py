# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:23:13 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Exposure Evaluation
"""

import cv2
import numpy as np

def EntropyRGB(img_rgb):
    
    amount_luminance_level=256
    
    entropy=0
    
    for k in range(3):
        
        img_this_channel=img_rgb[:,:,k]
        
        #for frequency calculation
        pixel_amount=len(list(img_this_channel.ravel()))
        
        '''column vector'''
        hist_this_channel=cv2.calcHist([img_this_channel],[0],None,[amount_luminance_level],[0,256])
        
        #y axis frequency
        list_frequency=np.array([frequency_this_gray_level/pixel_amount for frequency_this_gray_level in hist_this_channel])+10e-8
        
        list_log_frequency=np.log(list_frequency)
        
        entropy-=np.sum(list_frequency*list_log_frequency)
        
    return entropy

def EntropyGray(img_gray):
    
    amount_luminance_level=256

    #for frequency calculation
    pixel_amount=len(list(img_gray.ravel()))
    
    '''column vector'''
    hist_this_channel=cv2.calcHist([img_gray],[0],None,[amount_luminance_level],[0,256])
    
    #y axis frequency
    list_frequency=np.array([frequency_this_gray_level/pixel_amount for frequency_this_gray_level in hist_this_channel])+10e-8
    
    list_log_frequency=np.log(list_frequency)

    return -np.sum(list_frequency*list_log_frequency)

#------------------------------------------------------------------------------
"""
Calculation of tenengrad with different operator

Args:
    img_gray: matrix of gray img
    articulation_operator: operator of articulation calculation
    
Returns:
    tenengradient value
"""
def Gradient(img_gray,gradient_operator):
    
    if gradient_operator=='Gradient-x':
        
        return np.abs(np.average(np.gradient(img_gray,axis=1)))
    
    if gradient_operator=='Gradient-y':
        
        return np.abs(np.average(np.gradient(img_gray,axis=0)))
    
    if gradient_operator=='Gradient':
        
        Gradient_x=np.abs(np.average(np.gradient(img_gray,axis=1)))
        Gradient_y=np.abs(np.average(np.gradient(img_gray,axis=0)))

        return np.average(np.sqrt(Gradient_x**2+Gradient_y**2))
        