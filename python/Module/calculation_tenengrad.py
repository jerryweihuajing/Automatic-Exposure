# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 10:58:44 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Articulation
"""

import cv2
import numpy as np

#------------------------------------------------------------------------------
"""
Calculation of gradient with different operator

Args:
    img_gray: matrix of gray img
    articulation_operator: operator of articulation calculation
    
Returns:
    gradient value
"""
def Tenengrad(img_gray,tenengrad_operator):
    
    if tenengrad_operator=='Canny':
        
        return np.abs(np.average(cv2.Canny(img_gray,0,1000).ravel()))

    if tenengrad_operator=='Sobel':
        
        Sobel_x=cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=5).ravel()
        Sobel_y=cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=5).ravel()
        
        return np.average(np.sqrt(Sobel_x**2+Sobel_y**2))
        
    if tenengrad_operator=='Sobel-x':
        
        return np.abs(np.average(cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=5).ravel()))
    
    if tenengrad_operator=='Sobel-y':
    
        return np.abs(np.average(cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=5).ravel()))
    
    if tenengrad_operator=='Laplacian':
        
        return np.abs(np.average(cv2.Laplacian(img_gray, cv2.CV_64F).ravel()))
    
#------------------------------------------------------------------------------
"""
Calculation of articulation with different operator

Args:
    img_gray: matrix of gray img
    articulation_operator: operator of articulation calculation
    
Returns:
    articulation value
"""
def Articulation(img_gray,articulation_operator):
    
    if articulation_operator=='Variance':
        
        return np.sqrt(np.average((img_gray.ravel()-np.average(img_gray.ravel()))**2))