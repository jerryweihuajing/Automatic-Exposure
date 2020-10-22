# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 13:06:56 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Calculation of Texture Feature
"""

import math
import numpy as np

#define the maximum grayscale series
gray_level = 256

#------------------------------------------------------------------------------
"""
Calculate maximal gray level

Args:
    img: image in gray level

Returns:
    maximal gray level
"""
def GrayLevelMaximum(img):
    
    max_gray_level=0
    (height,width)=img.shape

    for y in range(height):
        
        for x in range(width):
            
            if img[y][x] > max_gray_level:
                
                max_gray_level = img[y][x]
                
    return max_gray_level+1

#------------------------------------------------------------------------------
"""
Calculate Gray Level Co-occurrence Matrix

Args:
    input: src data
    dx, dy: offset in x,y to determine direction

Returns:
    Gray Level Co-occurrence Matrix
"""
def CalculateGLCM(input,d_x,d_y):
    
    srcdata=input.copy()
    
    GLCM=[[0.0 for i in range(gray_level)] for j in range(gray_level)]
    
    (height,width) = input.shape
    
    max_gray_level=GrayLevelMaximum(input)
    
    '''if the grayscale series is larger than Gray_level, the grayscale of the image
    is reduced to gray_level to reduce the size of the grayscale co-occurrence matrix'''
    if max_gray_level > gray_level:
        
        for j in range(height):
            
            for i in range(width):
                
                srcdata[j][i] = srcdata[j][i]*gray_level / max_gray_level

    for j in range(height-d_y):
        
        for i in range(width-d_x):
            
            try:
                
                rows = srcdata[j][i]
                cols = srcdata[j + d_y][i+d_x]
                GLCM[rows][cols]+=1.0
                
            except:
                
                pass

    #calculate total gray value
    total_gray_level=np.sum(np.array(GLCM).ravel())

    #normalization
    for i in range(gray_level):
        
        for j in range(gray_level):
            
            GLCM[i][j]/=total_gray_level
            # GLCM[i][j]/=float(height*width)
            
    return GLCM

#------------------------------------------------------------------------------
"""
Calculate list of texture feature

Args:
    img_gray: image in gray level
    direction: direction to calculate GLCM

Returns:
    list of texture feature
"""
def ListTextureFeature(img_gray,direction):
    
    if direction==0:
        
        GLCM=CalculateGLCM(img_gray,1,0)
        
    if direction==1:
       
        GLCM=CalculateGLCM(img_gray,0,1)
       
    if direction==2:
       
        GLCM=CalculateGLCM(img_gray,1,1)
       
    if direction==3:
       
        GLCM=CalculateGLCM(img_gray,-1,1)
    
    #initialization all texture feature
    Con=0.0
    Eng=0.0
    Asm=0.0
    Idm=0.0
    
    for i in range(gray_level):
        
        for j in range(gray_level):
            
            Con+=(i-j)*(i-j)*GLCM[i][j]
            Asm+=GLCM[i][j]*GLCM[i][j]
            Idm+=GLCM[i][j]/(1+(i-j)*(i-j))
            
            if GLCM[i][j]>0.0:
                
                Eng+=GLCM[i][j]*math.log(GLCM[i][j])
                
    return Asm,Con,-Eng,Idm

#------------------------------------------------------------------------------
"""
Calculate dictionary of texture feature

Args:
    img_gray: image in gray level

Returns:
    dictionary of texture feature
"""
def MapTextureFeature(img_gray):
    
    list_feature=['ASM','Contrast','Energy','IDM']
    
    #init feature value
    list_value=len(list_feature)*[0]
    
    for k in range(len(list_value)):
        
        for kk in range(4):

            list_value[k]+=ListTextureFeature(img_gray,kk)[k]

    return dict(zip(list_feature,list(np.array(list_value)/4)))