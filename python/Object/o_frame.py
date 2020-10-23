# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 18:03:19 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Object-frame
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

import calculation_contrast as C_C
import calculation_exposure_evaluation as C_E_E

from calculation_contrast import zoom_factor,\
                                 ROI_weight_5_area,\
                                 ROI_weight_9_area
                             
#==============================================================================
#object to operate image
#============================================================================== 
class frame:
    def __init__(self,
                 path=None,
                 pre_fix=None,
                 img_rgb=None,
                 img_bgr=None,
                 img_gray=None,
                 img_ROI=None,
                 focus_value=None,
                 lens_position_code=None,
                 average_luminance=None,
                 exposure_time=None,
                 exposure_evaluation=None):
        self.path=path
        self.pre_fix=pre_fix
        self.img_rgb=img_rgb
        self.img_bgr=img_bgr
        self.img_gray=img_gray
        self.img_ROI=img_ROI
        self.focus_value=focus_value
        self.lens_position_code=lens_position_code
        self.average_luminance=average_luminance
        self.exposure_time=exposure_time
        self.exposure_evaluation=exposure_evaluation
        
    def Init(self,operator,ROI_mode):
        
        #read image
        self.img_bgr=cv2.imread(self.path)
        self.img_rgb=plt.imread(self.path)
        
        #convert rgb img to gray img
        self.img_gray=cv2.cvtColor(self.img_bgr,cv2.COLOR_BGR2GRAY)
        
        #VCM code calculation
        try:
            
            self.exposure_time=int(self.path.strip('.jpg').split(self.pre_fix)[-1])
            
        except:
            
            if self.pre_fix!='':
                
                self.exposure_time=int(self.path.strip('.png').split(self.pre_fix)[-1])
            
            else:
                
                self.exposure_time=int(self.path.split('\\')[-1].strip('.png'))
                                            
        #size of img
        height,width=np.shape(self.img_gray)

        ROI_linewidth=int(height//300)
        
        #image of ROI
        self.img_ROI=np.full(np.shape(self.img_gray),np.nan)
        
        list_center_5_area=[[ height/2, width/2],
                            [ height/4, width/4],
                            [ height/4,-width/4],
                            [-height/4,-width/4],
                            [-height/4, width/4]]
        
        list_center_9_area=[[height/2+i*height/4,width/2+j*width/4] for i in [-1,0,1] for j in [-1,0,1]]
        
        #size of area
        area_half_height=int(np.shape(self.img_gray)[0]/zoom_factor)
        area_half_width=int(np.shape(self.img_gray)[1]/zoom_factor)
        
        if ROI_mode=='9-Area':
            
            #calculate value in each area
            list_value_9_areas=[]
            list_luminance_9_areas=[]
            
            for i,j in list_center_9_area:
 
                if operator=='Entropy-RGB':
                    
                    this_area=self.img_rgb[int(i)-area_half_height:int(i)+area_half_height,
                                           int(j)-area_half_width:int(j)+area_half_width]
                    
                    #collect it
                    list_value_9_areas.append(C_E_E.EntropyRGB(this_area))
                    
                    #luminance
                    this_area_average=this_area[:,:,0]+this_area[:,:,1]+this_area[:,:,2]
                    list_luminance_9_areas.append(np.average(this_area_average.ravel())/3)
                    
                else:
                    
                    this_area=self.img_gray[int(i)-area_half_height:int(i)+area_half_height,
                                            int(j)-area_half_width:int(j)+area_half_width]
                    
                    if operator=='Entropy-Gray':
                        
                        #collect it
                        list_value_9_areas.append(C_E_E.EntropyGray(this_area))
                    
                    else:
                        
                        #collect it
                        list_value_9_areas.append(C_C.GlobalContrast(this_area,operator))
                    
                    list_luminance_9_areas.append(np.average(this_area.ravel()))
                    
                #draw the bound of ROI
                for k in range(ROI_linewidth):
                    
                    self.img_ROI[int(i-k)-area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    self.img_ROI[int(i+k)+area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    self.img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j-k)-area_half_width]=1
                    self.img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j+k)+area_half_width]=1
            
            #collect the data
            self.exposure_evaluation=np.sum(np.array(ROI_weight_9_area)*np.array(list_value_9_areas))
            self.average_luminance=np.sum(np.array(ROI_weight_9_area)*np.array(list_luminance_9_areas))
            
        if ROI_mode=='5-Area':
            
            #calculate value in each area
            list_value_5_areas=[]
            list_luminance_5_areas=[]
            
            for i,j in list_center_5_area:
                        
                if operator=='Entropy-RGB':
                    
                    this_area=self.img_rgb[int(i)-area_half_height:int(i)+area_half_height,
                                           int(j)-area_half_width:int(j)+area_half_width]
                    
                    #collect it
                    list_value_5_areas.append(C_E_E.EntropyRGB(this_area))
                    
                    #luminance
                    this_area_average=this_area[:,:,0]+this_area[:,:,1]+this_area[:,:,2]
                    list_luminance_5_areas.append(np.average(this_area_average.ravel())/3)
                    
                else:
                    
                    this_area=self.img_gray[int(i)-area_half_height:int(i)+area_half_height,
                                            int(j)-area_half_width:int(j)+area_half_width]
                    
                    if operator=='Entropy-Gray':
                        
                        #collect it
                        list_value_5_areas.append(C_E_E.EntropyGray(this_area))

                    else:
                        
                        #collect it
                        list_value_5_areas.append(C_C.GlobalContrast(this_area,operator))
                    
                    list_luminance_5_areas.append(np.average(this_area.ravel()))
                        
                #draw the bound of ROI
                for k in range(ROI_linewidth):
                    
                    self.img_ROI[int(i-k)-area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    self.img_ROI[int(i+k)+area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    self.img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j-k)-area_half_width]=1
                    self.img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j+k)+area_half_width]=1
            
            #collect the data
            self.exposure_evaluation=np.sum(np.array(ROI_weight_5_area)*np.array(list_value_5_areas))
            self.average_luminance=np.sum(np.array(ROI_weight_5_area)*np.array(list_luminance_5_areas))
            
        if ROI_mode=='Center':
       
            i,j=height/2,width/2
            
            if operator=='Entropy-RGB':
                
                this_area=self.img_rgb[int(i)-area_half_height:int(i)+area_half_height,
                                       int(j)-area_half_width:int(j)+area_half_width]
                
                #collect it
                list_value_5_areas.append(C_E_E.EntropyRGB(this_area))
                
                #luminance
                this_area_average=this_area[:,:,0]+this_area[:,:,1]+this_area[:,:,2]
                self.average_luminance=np.average(this_area_average.ravel())/3
                    
            else:
                
                this_area=self.img_gray[int(i)-area_half_height:int(i)+area_half_height,
                                        int(j)-area_half_width:int(j)+area_half_width]
                
                if operator=='Entropy-Gray':
                    
                    #calculate
                    self.exposure_evaluation=C_E_E.EntropyGray(this_area)
                
                else:
                    
                    #calculate
                    self.exposure_evaluation=C_C.GlobalContrast(this_area,operator)
                    
                self.average_luminance=np.average(this_area.ravel())
                                                
                #draw the bound of ROI
                for k in range(ROI_linewidth):
                    
                    self.img_ROI[int(i-k)-area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    self.img_ROI[int(i+k)+area_half_height,int(j-k)-area_half_width:int(j+k+1)+area_half_width]=1
                    self.img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j-k)-area_half_width]=1
                    self.img_ROI[int(i-k)-area_half_height:int(i+k+1)+area_half_height,int(j+k)+area_half_width]=1
    
        print('--> Exposure Time:',self.exposure_time//1000,'(ms)')
        # print('--> Exposure Evaluation:',self.exposure_evaluation)
        # print('--> Average Luminance:',int(self.average_luminance))