# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 13:06:56 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Fourier Tranform
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

'''x y frequency is different'''

#------------------------------------------------------------------------------
"""
Plot contrast curve with pixel mode

Args:
    img: input image
    N: size of target image
    show: (bool) show the figure or not
    
Returns:
    frequency spectrum
"""
def FourierTransfromSpectrum(img,N=1000,show=False):
    
    '''texture MTF: Module Transfer Function'''
    center=[np.shape(img)[0]/2,np.shape(img)[1]/2]
    
    #target image matrix
    img_target=img[int(center[0]-N/2):int(center[0]+N/2),
                   int(center[1]-N/2):int(center[1]+N/2)]

    dft = cv2.dft(np.float32(img_target), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1]))

    if show:
        
        plt.figure(figsize=(10,6))
        
        plt.subplot(121),plt.imshow(img,cmap='gray')
        plt.title('Input Image')
        plt.xticks([]),plt.yticks([])
        
        plt.subplot(122),plt.imshow(magnitude_spectrum,cmap='gray')
        plt.title('Magnitude Spectrum')
        plt.xticks([]),plt.yticks([])
        
        plt.figure(figsize=(10,6))
        
        plt.subplot(311),plt.plot(magnitude_spectrum[0,:])
        plt.subplot(312),plt.plot(magnitude_spectrum[:,0])
        plt.subplot(313),plt.plot(np.average(magnitude_spectrum))
    
    return magnitude_spectrum