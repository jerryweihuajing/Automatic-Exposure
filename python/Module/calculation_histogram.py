# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 10:59:44 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Histogram
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

#legned font
legend_font={'family':'Gill Sans MT','weight':'normal','size':12}

#title font
annotation_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=16)

#annotation font
title_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=20)
 
#------------------------------------------------------------------------------
"""
Calculation of gray histogram

Args:
    img_gray: matrix of gray img
    amount_gray_level: amount of gray level
    
Returns:
    None
"""
def GrayHistogramCurve(img_gray,amount_gray_level=256):
    
    #for frequency calculation
    pixel_amount=len(list(img_gray.ravel()))
    
    #step between gray level nearby
    step_gray_level=int(np.ceil(256/amount_gray_level))
    
    '''plot gray histogram'''
    fig,ax=plt.subplots(figsize=(10,6))
    
    hist_gray=cv2.calcHist([img_gray],[0],None,[amount_gray_level],[0,256])
    
    #transfrom it like a histogram
    histogram_gray=[]
    
    for frequency_this_gray_level in hist_gray:
        
        histogram_gray+=[frequency_this_gray_level/step_gray_level/pixel_amount]*step_gray_level
    
    plt.plot(histogram_gray,color='k',label='Gray')
    plt.legend(prop=legend_font)
    plt.xlim([0, 256])
    
    #set ticks
    plt.tick_params(labelsize=12)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title('Gray Histogram',FontProperties=title_font)  
    
    plt.xlabel('Gray Level',FontProperties=annotation_font)
    plt.ylabel('Frequency',FontProperties=annotation_font)

    #tick step
    x_major_step=16
    x_minor_step=8
    y_major_step=(max(histogram_gray)-min(histogram_gray))/10
    y_minor_step=(max(histogram_gray)-min(histogram_gray))/20
    
    #set locator
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))

#------------------------------------------------------------------------------
"""
Calculation of bgr histogram

Args:
    img_bgr: matrix of bgr img
    amount_gray_level: amount of gray level
    
Returns:
    None
"""
def BGRHistogramCurve(img_bgr,amount_gray_level=256):
    
    img_gray=img_bgr[:,:,0]
    
    #for frequency calculation
    pixel_amount=len(list(img_gray.ravel()))
    
    #step between gray level nearby
    step_gray_level=int(np.ceil(256/amount_gray_level))
    
    '''plot BGR histogram'''
    fig,ax=plt.subplots(figsize=(10,6))
    colors=('b','g','r')
    
    #3 channels
    for i, col in enumerate(colors):
        
        this_histogram=[]
        
        this_hist= cv2.calcHist([img_bgr],[i],None,[amount_gray_level],[0, 256])
        
        for frequency_this_level in this_hist:
        
            this_histogram+=[frequency_this_level/step_gray_level/pixel_amount]*step_gray_level
        
        plt.plot(this_histogram,color=col,label=col.upper())
        plt.legend(prop=legend_font)
        plt.xlim([0, 256])
        
    #set ticks
    plt.tick_params(labelsize=12)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title('BGR Histogram',FontProperties=title_font)  
    
    plt.xlabel('BGR Level',FontProperties=annotation_font)
    plt.ylabel('Frequency',FontProperties=annotation_font)

    #tick step
    x_major_step=16
    x_minor_step=8
    y_major_step=(max(this_histogram)-min(this_histogram))/10
    y_minor_step=(max(this_histogram)-min(this_histogram))/20
    
    #set locator
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
    
#------------------------------------------------------------------------------
"""
Calculation of histogram

Args:
    img_path: path of input image
    amount_gray_level: amount of gray level
    
Returns:
    None
"""
def HistogramCurve(img_path,amount_gray_level=256):
    
    #read image
    img_bgr=cv2.imread(img_path)
    
    #convert rgb img to gray img
    img_gray=cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)
        
    #for frequency calculation
    pixel_amount=len(list(img_gray.ravel()))
    
    #step between gray level nearby
    step_gray_level=int(np.ceil(256/amount_gray_level))
    
    '''plot gray histogram'''
    fig,ax=plt.subplots(figsize=(10,6))
    
    hist_gray=cv2.calcHist([img_gray],[0],None,[amount_gray_level],[0,256])
    
    #transfrom it like a histogram
    histogram_gray=[]
    
    for frequency_this_gray_level in hist_gray:
        
        histogram_gray+=[frequency_this_gray_level/step_gray_level/pixel_amount]*step_gray_level
    
    plt.plot(histogram_gray,color='k',label='Gray')
    plt.legend(prop=legend_font)
    plt.xlim([0, 256])
    
    #set ticks
    plt.tick_params(labelsize=12)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title('Gray Histogram',FontProperties=title_font)  
    
    plt.xlabel('Gray Level',FontProperties=annotation_font)
    plt.ylabel('Frequency',FontProperties=annotation_font)

    #tick step
    x_major_step=16
    x_minor_step=8
    y_major_step=(max(histogram_gray)-min(histogram_gray))/10
    y_minor_step=(max(histogram_gray)-min(histogram_gray))/20
    
    #set locator
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
    
    '''plot BGR histogram'''
    fig,ax=plt.subplots(figsize=(10,6))
    colors=('b','g','r')
    
    #3 channels
    for i, col in enumerate(colors):
        
        this_histogram=[]
        
        this_hist= cv2.calcHist([img_bgr],[i],None,[amount_gray_level],[0, 256])
        
        for frequency_this_level in this_hist:
        
            this_histogram+=[frequency_this_level/step_gray_level/pixel_amount]*step_gray_level
        
        plt.plot(this_histogram,color=col,label=col.upper())
        plt.legend(prop=legend_font)
        plt.xlim([0, 256])
        
    #set ticks
    plt.tick_params(labelsize=12)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title('BGR Histogram',FontProperties=title_font)  
    
    plt.xlabel('BGR Level',FontProperties=annotation_font)
    plt.ylabel('Frequency',FontProperties=annotation_font)

    #tick step
    x_major_step=16
    x_minor_step=8
    y_major_step=(max(this_histogram)-min(this_histogram))/10
    y_minor_step=(max(this_histogram)-min(this_histogram))/20
    
    #set locator
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
    
#------------------------------------------------------------------------------
"""
Calculation of classification histogram

Args:
    img_gray: matrix of gray img
    amount_gray_level: amount of gray level
    
Returns:
    gray ravel with gray_level
"""
def HistogramArray(img_gray,amount_gray_level=16):

    #vectorization
    gray_array=img_gray.ravel()
    
    gray_step=256/amount_gray_level

    return np.array(gray_array)//gray_step+1