# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 11:01:31 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Contrast
"""

import cv2
import copy as cp
import numpy as np

import calculation_texture_feature as C_T_F
import calculation_scene_discrimination as C_S_D

'''
Contrast (Luminance Contrast) is the relationship between the luminance
of a brighter area of interest and that of an adjacent darker area.
'''
#------------------------------------------------------------------------------
"""
Calculation of contrast with different operator

Args:
    img_gray: matrix of gray img
    contrast_operator: operator of contrast calculation
    
Returns:
    contrast value
"""
def GlobalContrast(img_gray,contrast_operator):
    
    amount_gray_level=256
    
    '''Constant'''
    #vectorization
#    gray_array=His.HistogramArray(img_gray,amount_gray_level)
    
    """
    1 np.uint8 256→0 so convert the data type
    2 avoid liminance minimum being 0
    3 but float type cost more
    """
    gray_array=img_gray.ravel()+0.5
    
    #luminance of background and foreground
    L_b,L_f=C_S_D.ForeAndBackLuminance(img_gray)

    #maximum and minimum of luminance
    L_max,L_min=np.max(gray_array),np.min(gray_array)
    
    #mean value of img gray
    gray_average=np.average(gray_array)
        
    '''King-Smith and Kulikowski (1975)'''
    if contrast_operator=='KK':
        
        return L_max-L_min
    
    '''Burkhardt (1984)'''
    if contrast_operator=='Burkhardt':
        
        return (L_max-L_min)/L_max
    
    '''Whittle (1986)'''
    if contrast_operator=='Whittle':
 
        return (L_max-L_min)/L_min
    
    '''Michelson (1927)'''
    if contrast_operator=='Michelson':
  
        return (L_max-L_min)/(L_max+L_min)
    
    '''Peli (1990)'''
    if contrast_operator=='Peli':
        
        return np.average(np.square(np.array(gray_array)-gray_average))
    
    '''Weber (1840)'''
    if contrast_operator=='Weber':
        
        return np.abs(L_f-L_b)/L_b
    
    '''Boccignone (1996)'''
    if contrast_operator=='Boccignone':
        
        return np.log(L_f/L_b)
    
    '''W3C (2006)'''
    if contrast_operator=='W3C':
        
        return (L_max+0.05)/(L_min+0.05)
    
    '''Stevens (1961)'''
    if contrast_operator=='Stevens':
        
        #filter the matrix
        img_gray_S=np.abs(116*(img_gray/255)**(1/3)-16)
        
        #foreground and background luminance
        '''histogram calculated from np.uint8 matrix'''
        L_b_S,L_f_S=C_S_D.ForeAndBackLuminance(img_gray_S.astype(np.uint8))
        
        return np.abs(L_b_S-L_f_S)
    
    '''Garalick (1979): GLCM'''
    if contrast_operator=='GLCM':
        
        return C_T_F.MapTextureFeature(img_gray)['Contrast']
    
    '''Moulden (1990): Standard Deviation'''    
    if 'S' in contrast_operator:

        """Essay: The standard deviation of luminance as a metric for contrast in random-dot images"""
        #for frequency calculation
        pixel_amount=len(list(img_gray.ravel()))
        
        #step between gray level nearby
        step_gray_level=int(np.ceil(256/amount_gray_level))
        
        '''column vector'''
        hist_gray=cv2.calcHist([img_gray],[0],None,[amount_gray_level],[0,256])
        
        #x axis gray level
        list_gray_level=np.array([step_gray_level*(k+0.5) for k in range(amount_gray_level)])
    
        #y axis frequency
        list_frequency=np.array([frequency_this_gray_level/pixel_amount for frequency_this_gray_level in hist_gray])
      
        #average value of luminance
        average_gray_level=np.sum(list_gray_level.ravel()*list_frequency.ravel())

        #simplism
    #    G=cp.deepcopy(amount_gray_level)
        L=cp.deepcopy(list_gray_level).ravel()
        P=cp.deepcopy(list_frequency).ravel()
        Lm=cp.deepcopy(average_gray_level)
    #    R=cp.deepcopy(range_gray_level)

        '''SD: standard deviation'''
        if contrast_operator=='SD':
            
            SD=np.sum(P*np.square(L-Lm))
    
            return SD
            
        '''SDLG: standard deviation of logarithm of luminance'''
        if contrast_operator=='SDLG':
            
            '''np.log() stands for ln() in mathamatics'''
            LG_L=np.log2(L)
            LG_Lm=np.sum(P*LG_L)

            SDLG=np.sum(P*np.square(LG_L-LG_Lm))
            
            return SDLG
            
        '''SAM: space-average of Michelson contrast'''
        if contrast_operator=='SAM':
            
            SAM=np.zeros((len(L),len(L)))
            
            for i in range(len(L)):
                
                for j in range(len(L)):
                    
                    if i==j:
                        
                        continue
                    
                    SAM[i,j]=P[i]*P[j]*np.abs(L[i]-L[j])/(L[i]+L[j])
                    
            return np.sum(SAM.ravel())
        
        '''SALGM: space-average logarithm of Michelson contrast'''
        if contrast_operator=='SALGM':
            
            SALGM=np.zeros((len(L),len(L)))
            
            for i in range(len(L)):
                
                for j in range(len(L)):
                    
                    if i==j:
                        
                        continue
                    
                    SALGM[i,j]=P[i]*P[j]*np.log2(np.abs(L[i]-L[j])/(L[i]+L[j]))
                    
            return np.sum(SALGM.ravel())
        
        '''SAW: space-average of Whittle contrast'''
        if contrast_operator=='SAW':
            
            SAW=np.zeros((len(L),len(L)))
            
            for i in range(len(L)):
                
                for j in range(len(L)):
                    
                    if i==j:
                        
                        continue
                    
                    SAW[i,j]=P[i]*P[j]*np.abs(L[i]-L[j])/np.min([L[i],L[j]])
                    
            return np.sum(SAW.ravel())
        
        '''SALGW: space-average logarithm of Whittle contrast'''
        if contrast_operator=='SALGW':
            
            SALGW=np.zeros((len(L),len(L)))
            
            for i in range(len(L)):
                
                for j in range(len(L)):
                    
                    if i==j:
                        
                        continue
                    
                    SALGW[i,j]=P[i]*P[j]*np.log2(np.abs(L[i]-L[j])/np.min([L[i],L[j]]))
                    
            return np.sum(SALGW.ravel())
    
    if 'RMSC' in contrast_operator:
        
        #center img
        center_img_gray=img_gray[+1:-1,+1:-1]
        
        #neighbor img
        neighbor_img_gray=[img_gray[+1:-1,+2:],
                           img_gray[+1:-1,:-2],
                           img_gray[+2:,+1:-1],
                           img_gray[:-2,+1:-1],
                           img_gray[+2:,+2:],
                           img_gray[:-2,+2:],
                           img_gray[+2:,:-2],
                           img_gray[:-2,:-2]]
        
        '''sum: 8I+(I1+I2+...+I8)'''
        sum_img_gray=np.zeros(np.shape(center_img_gray),dtype='uint8')
        
        '''diff: 8I-(I1+I2+...+I8)'''
        diff_img_gray=np.zeros(np.shape(center_img_gray),dtype='uint8')
        
        '''diff sqaure: (I-I1)**2+(I-I2)**2+...+(I-I8)**2'''
        diff_square_img_gray=np.zeros(np.shape(center_img_gray),dtype='uint8')
        
        #traverse nieghbor and calculate
        for this_neighbor_img_gray in neighbor_img_gray:
           
            sum_img_gray+=(center_img_gray+this_neighbor_img_gray)
            diff_img_gray+=(center_img_gray-this_neighbor_img_gray)
            diff_square_img_gray+=(center_img_gray-this_neighbor_img_gray)**2
    
        '''Rizzi: root-mean-square contrast (2004)'''
        if contrast_operator=='RMSC-1':
            
            return np.average((np.sqrt(diff_square_img_gray/8)).ravel())
        
        '''Panetta: root-mean-square contrast (2013)'''
        if contrast_operator=='RMSC-2':
            
            #expire denominatior being 0
            diff_img_gray[np.where(sum_img_gray==0)]=0
            sum_img_gray[np.where(sum_img_gray==0)]=1
            
            #valid pixel amount
            valid_amount=len(list(center_img_gray.ravel()))-len(np.where(sum_img_gray==0)[0])
            
            return np.sum((diff_img_gray/sum_img_gray).ravel())/valid_amount
    
    '''Reinagel (1999)'''
    if contrast_operator=='Reinagel':
        
        return np.average(np.square(np.array(gray_array)/gray_average))
    
    '''Tadmor (1998)'''
    if 'Tadmor' in contrast_operator:
        
        r_c=1
        r_s=1
        
        #Difference of Gaussian
        center=lambda x,y:np.exp(-(x**2+y**2)/r_c)
        surround=lambda x,y:np.exp(-(x**2+y**2)/r_s)*(r_c/r_s)**2*0.85
        
        R_c=0
        
        for i in range(-3*r_c,3*r_c+1):
            
            for j in range(-3*r_c,3*r_c+1):
                
                R_c+=np.average(center(i,j)*\
                                       img_gray[3*r_c+i:3*r_c+i+np.shape(img_gray)[0]-6*r_c,
                                                3*r_c+j:3*r_c+j+np.shape(img_gray)[1]-6*r_c])
        
        R_s=0
        
        for i in range(-3*r_s,3*r_s+1):
            
            for j in range(-3*r_s,3*r_s+1):
                
                R_s+=np.average(surround(i,j)*\
                                img_gray[3*r_s+i:3*r_s+i+np.shape(img_gray)[0]-6*r_s,
                                         3*r_s+j:3*r_s+j+np.shape(img_gray)[1]-6*r_s])
            
        if contrast_operator=='Tadmor-1':
            
            return (R_c-R_s)/R_c
        
        if contrast_operator=='Tadmor-2':
            
            return (R_c-R_s)/R_s
        
        if contrast_operator=='Tadmor-3':
            
            return (R_c-R_s)/(R_c+R_s)
    
    '''Rizzi (2004)'''
    if contrast_operator=='Rizzi':
        
        total_level=[]
        
        for level in range(6):
            
            img_gray=cv2.pyrDown(img_gray)
        
            #center img
            center_img_gray=img_gray[+1:-1,+1:-1]
            
            #neighbor img
            neighbor_img_gray=[img_gray[+1:-1,+2:],
                               img_gray[+1:-1,:-2],
                               img_gray[+2:,+1:-1],
                               img_gray[:-2,+1:-1],
                               img_gray[+2:,+2:],
                               img_gray[:-2,+2:],
                               img_gray[+2:,:-2],
                               img_gray[:-2,:-2]]

            '''diff sqaure: (I-I1)**2+(I-I2)**2+...+(I-I8)**2'''
            diff_square_img_gray=np.zeros(np.shape(center_img_gray),dtype='uint8')
        
            #traverse nieghbor and calculate
            for this_neighbor_img_gray in neighbor_img_gray:
               
                diff_square_img_gray+=(center_img_gray-this_neighbor_img_gray)**2
                
            total_level.append(np.average((np.sqrt(diff_square_img_gray/8)).ravel()))
            
        return np.average(total_level)
    
    '''Xu (2011)'''
    if 'CM' in contrast_operator:
        
        #neighbor img_gray matrix
        list_img_gray_neighbor=[img_gray[:-2,+1:-1],
                                img_gray[+2:,+1:-1],
                                img_gray[+1:-1,:-2],
                                img_gray[+1:-1,+2:]]
        
        #center img_gray matrix
        img_gray_center=img_gray[+1:-1,+1:-1]
        
        #result matrix
        img_gray_diff_sum=np.zeros(np.shape(img_gray_center))
        
        for this_img_gray_neighbor in list_img_gray_neighbor:
            
            img_gray_diff_sum+=np.abs(this_img_gray_neighbor-img_gray_center)
            
        #square of diff sum
        L=(img_gray_diff_sum**2)
        
        '''CMSL: Contrast Measure based on Squared Laplacian'''
        if contrast_operator=='CMSL':
            
            return np.average(L.ravel())
        
        '''CMAN: Contrast Measure Adaptive to Noise influence'''
        if contrast_operator=='CMAN':
            
            T1,T2=50,150
            
            #M<T1: n=1
            if L_max<T1:n=1
                    
            #T1<M<T2: n=2
            if T1<L_max<T2:n=2
            
            #M>T2: n=3
            if L_max>T2:n=3
                
            return np.average((L/n).ravel())
