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
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator

from configuration_color import list_articulation_operator

import operation_import as O_I

import calculation_articulation as C_A
import calculation_texture_feature as C_T_F
import calculation_scene_discrimination as C_S_D

#basic parameters
ROI_weight_5_area=[0.14]*4
ROI_weight_5_area.insert(0,0.44)

ROI_weight_9_area=[0.1]*8
ROI_weight_9_area.insert(4,0.2)
            
zoom_factor=16

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
        
    '''Articulation'''
    if contrast_operator in list_articulation_operator:
        
        return C_A.Articulation(img_gray,contrast_operator)
            
#------------------------------------------------------------------------------
"""
Calculation of contrast with different mode with 5-Area

Args:
    img_gray: matrix of gray img
    contrast_operator: operator of contrast calculation
    ROI_weight: weight list: 1st is the center the others are the neighbor
    zoom_factor: module zoom factor 
    
Returns:
    contrast value
"""
def Contrast5Area(img_gray,
                  contrast_operator,
                  ROI_weight,
                  zoom_factor):
    
    print('')
    print('-- Contrast 5-Area')
    print('-> Operator:',contrast_operator)
    
    height,width=np.shape(img_gray)
    
    if contrast_operator=='ANSI':
        
        #size of img patch
        patch_height=int(height/4)
        patch_width=int(width/4)
    
        #list index
        list_index_white=[[0,0],[0,2],[1,1],[1,3],[2,0],[2,2],[3,0],[3,2]]
        list_index_black=[[0,1],[0,3],[1,0],[1,2],[2,1],[2,3],[3,1],[3,3]]

        #list patch
        list_patches_white=[img_gray[i*patch_height:(i+1)*patch_height,j*patch_width:(j+1)*patch_width] for i,j in list_index_white]
        list_patches_black=[img_gray[i*patch_height:(i+1)*patch_height,j*patch_width:(j+1)*patch_width] for i,j in list_index_black]
        
        #B and W
#        white_average=np.average([np.average(HistogramArray(this_patch)) for this_patch in list_patches_white])
#        black_average=np.average([np.average(HistogramArray(this_patch)) for this_patch in list_patches_black])
        white_average=np.average([np.average(this_patch.ravel()) for this_patch in list_patches_white])
        black_average=np.average([np.average(this_patch.ravel()) for this_patch in list_patches_black])
       
        return white_average/black_average

    else:
        
        list_5_points=[[ height/4, width/4],
                       [ height/4,-width/4],
                       [-height/4,-width/4],
                       [-height/4, width/4],
                       [ height/2, width/2]]
        
        #size of area
        area_half_height=int(np.shape(img_gray)[0]/zoom_factor)
        area_half_width=int(np.shape(img_gray)[1]/zoom_factor)
        
        #calculate contrast in each area
        list_contrast_5_areas=[]
        
        for i,j in list_5_points:
            
            this_area=img_gray[int(i)-area_half_height:int(i)+area_half_height,
                               int(j)-area_half_width:int(j)+area_half_width]

            #collect it
            list_contrast_5_areas.append(GlobalContrast(this_area,contrast_operator))

#        print(ROI_weight)
#        print(list_contrast_5_areas)
#        print(np.array(ROI_weight)*np.array(list_contrast_5_areas))
        
        return np.sum(np.array(ROI_weight)*np.array(list_contrast_5_areas))

#------------------------------------------------------------------------------
"""
Calculation block module of an img the centers of img and module are the same 

Args:
    img_gray: matrix of gray img
    ratio: size proportion module/img (default: 0.8)
    
Returns:
    block module matrix
"""
def BlockModule(img_gray,ratio=0.8):
        
    height,width=np.shape(img_gray)
    
    #center of module
    center=[int(np.round(height/2)),int(np.round(width/2))]
    
    #size of module
    half_height_module=int(np.round(ratio*height/2))
    half_width_module=int(np.round(ratio*width/2))
    
    return img_gray[center[0]-half_height_module:center[0]+half_height_module,
                    center[1]-half_width_module:center[1]+half_width_module]
    
#------------------------------------------------------------------------------
"""
Calculation of contrast with different mode with block module

Args:
    img_gray: matrix of gray img
    contrast_mode: mode of contrast calculation 
    ratio: size proportion module/img (default: 0.8)
    
Returns:
    contrast value
"""
def ContrastBlockModule(img_gray,contrast_operator,ratio):
    
    print('')
    print('-- Contrast Block Module')
    print('-> Operator:',contrast_operator)
    
    return GlobalContrast(BlockModule(img_gray,ratio),contrast_operator)
    
#------------------------------------------------------------------------------
"""
Plot contrast curve with pixel mode

Args:
    list_imgs_folder: images folder list
    series_mode: contrast series ['Constant','Advanced','Standard Deviation'] (default: 'Constant')
    view_mode: view of img ['5-Area','Block Module'] (default: '5-Area')
    ratio: size proportion module/img in 'Block Module' mode (default: 0.1)
    ROI_weight: weight list in '5-Area' mode (default: [0.44,0.14,0.14,0.14,0.14])
    zoom_factor: module zoom factor in '5-Area' mode (default: 18)
    
Returns:
    normalized contrast list of all contrast mode
"""
def ContrastCurve(list_imgs_folder,
                  series_mode='Constant',
                  view_mode='5-Area',
                  ratio=0.1,
                  ROI_weight=[0.44,0.14,0.14,0.14,0.14],
                  zoom_factor=18):
    
    #fetch the inpuy img data
#    list_imgs_bgr,list_imgs_gray,list_VCM_code=Im.BatchImages(list_imgs_folder[0])     
    list_imgs_bgr,list_imgs_gray,list_VCM_code=O_I.CombineImages(list_imgs_folder)
    
    if series_mode=='Constant':
        
        list_contrast_mode=['KK',
                            'Whittle',
                            'Burkhardt',
                            'Michelson',
                            'Peli',
                            'W3C',
                            'Weber',
                            'Stevens',
                            'Boccignone']
        
        list_contrast_color=['tan',
                             'cyan',
                             'teal',
                             'olive',
                             'maroon',
                             'orchid',
                             'sienna',
                             'fuchsia',
                             'crimson']
        
    if series_mode=='Advanced':
        
        list_contrast_mode=['RMSC-1',
                            'RMSC-2',
                            'Tadmor-1',
                            'Tadmor-2',
                            'Tadmor-3',
                            'Rizzi',
                            'CMSL',
                            'CMAN']
        
        list_contrast_color=['steelblue',
                             'slateblue',
                             'cadetblue',
                             'lightsalmon',
                             'mediumvioletred',
                             'mediumslateblue',
                             'mediumturquoise',
                             'mediumaquamarine']
            
    if series_mode=='Standard Deviation':
        
        list_contrast_mode=['SD',
                            'SDLG',
                            'SAM',
                            'SALGM',
                            'SAW',
                            'SALGW']
        
        list_contrast_color=['magenta',
                             'thistle',
                             'chocolate',
                             'firebrick',
                             'rosybrown',
                             'slategray']
        
    #map between mode and color     
    map_mode_color=dict(zip(list_contrast_mode,list_contrast_color))  
    
    fig,ax=plt.subplots(figsize=(10,6))
    
    #total value for plot
    total_normalized_contrast=[]
    
    #normalized contrast list of all contrast mode
    all_mode_normalized_contrast=[]
    
    for k in range(len(map_mode_color)):
        
        #color of this mode
        this_mode=list(map_mode_color.keys())[k]
        this_color=list(map_mode_color.values())[k]
        
        #contrast value 
        list_contrast=[]
        
        for this_img_gray in list_imgs_gray:

            #histogram equalization
#            this_img_gray=cv2.equalizeHist(this_img_gray)
            
            if view_mode=='5-Area':
            
                list_contrast.append(Contrast5Area(this_img_gray,this_mode,ROI_weight,zoom_factor))
                
            if view_mode=='Block Module':
            
                list_contrast.append(ContrastBlockModule(this_img_gray,this_mode,ratio))

        #generalized contrast value
        list_normalized_contrast=[]
        
        if np.min(list_contrast)==np.max(list_contrast):
            
            list_normalized_contrast=[1]*len(list_contrast)
            
        else:
                
            for this_contrast in list_contrast:
                
                '''Normalization'''
                list_normalized_contrast.append((this_contrast-np.min(list_contrast))/(np.max(list_contrast)-np.min(list_contrast)))
         
        #collect the generalized contrast list
        total_normalized_contrast+=list_normalized_contrast
        all_mode_normalized_contrast.append(list_normalized_contrast)
        
        plt.plot(list_VCM_code,
                 list_normalized_contrast,
                 color=this_color,
                 marker='.',
                 markersize=6,
                 linestyle='-',
                 label=this_mode)
        
        plt.legend(prop=legend_prop,loc='lower right')

    #set ticks
    plt.tick_params(labelsize=12)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title(view_mode+' Contrast-VCM Code Curve',FontProperties=title_font)  
    
    plt.xlabel('VCM Code',FontProperties=label_font)
    plt.ylabel('Contrast',FontProperties=label_font)
    
    #limit of x and y
    x_min,x_max=np.min(list_VCM_code),np.max(list_VCM_code)
    y_min,y_max=0,1
    
    #tick step
    x_major_step=np.ceil((x_max-x_min)/10/50)*50
    x_minor_step=np.ceil((x_max-x_min)/10/50)*25
    y_major_step=0.1
    y_minor_step=0.05
    
    #axis boundary
    plt.xlim([x_min-x_minor_step,x_max+x_minor_step])
    plt.ylim([y_min-y_minor_step,y_max+y_minor_step])
    
    #set locator
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))

    #add annotation
    if view_mode=='5-Area':
        
        plt.text(list_VCM_code[0]+x_major_step/10,
                 1+y_major_step/10,
                 'ROI Zoom Factor: %d Weight: %.2f-%.2f'%(zoom_factor/2,
                                                          ROI_weight[0],
                                                          ROI_weight[1]),
                 FontProperties=text_font)
           
    if view_mode=='Block Module':
        
        plt.text(list_VCM_code[0]+x_major_step/10,
                 1+y_major_step/10,
                 'Block Module Ratio: %.1f'%(ratio),
                 FontProperties=text_font)