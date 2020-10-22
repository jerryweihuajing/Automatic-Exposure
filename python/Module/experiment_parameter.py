# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 17:30:30 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Experiment
"""

import os
import matplotlib.pyplot as plt

import operation_path as O_P
import calculation_contrast as C_C
import calculation_peak_search as C_P_S

list_contrast_operator=['KK',
                        'Whittle',
                        'Burkhardt',
                        'Michelson',
                        'Peli',
                        'W3C',
                        'Weber',
                        'Stevens',
                        'Boccignone',
                        'SD',
                        'SDLG',
                        'SAM',
                        'SALGM',
                        'SAW',
                        'SALGW',
                        'RMSC-1',
                        'RMSC-2',
                        'Tadmor-1',
                        'Tadmor-2',
                        'Tadmor-3',
                        'Rizzi']

#------------------------------------------------------------------------------
"""
Experiment: block module size factor

Args:
    imgs_folder: images folder  
    output_folder: figs output_folder
   
Returns:
    None
"""
def ExperimentBlockModuleRatio(imgs_folder,output_folder):
    
    final_folder=output_folder+'\\Block Module\\Ratio\\'
    
    #construct a folder
    O_P.GenerateFolder(final_folder)   
    
    imgs_folder=[imgs_folder]
    
    #ratio 0.1-0.9 step is 0.1
    for k in range(1,10):
        
        this_ratio=0.1*k
        
        '''Constant'''
        #plot curve
        C_C.ContrastCurve(imgs_folder,'Constant','Block Module',ratio=this_ratio)

        plt.grid()
        
        plt.savefig(final_folder+str(k)+' (Constant).png',dpi=300,bbox_inches='tight')
        plt.close()
  
        '''Standard Deviation'''
        #plot curve
        C_C.ContrastCurve(imgs_folder,'Standard Deviation','Block Module',ratio=this_ratio)
    
        plt.grid()
        
        plt.savefig(final_folder+str(k)+' (Standard Deviation).png',dpi=300,bbox_inches='tight')
        plt.close()
        
        '''Advanced'''
        #plot curve
        C_C.ContrastCurve(imgs_folder,'Advanced','Block Module',ratio=this_ratio)
    
        plt.grid()
        
        plt.savefig(final_folder+str(k)+' (Advanced).png',dpi=300,bbox_inches='tight')
        plt.close()
        
#------------------------------------------------------------------------------
"""
Experiment: weight in 5 area method

Args:
    imgs_folder: images folder  
    output_folder: figs output_folder

Returns:
    None
"""
def Experiment5AreaWeight(imgs_folder,output_folder):
    
    final_folder=output_folder+'\\5-Area\\Weight\\'
    
    #construct a folder
    O_P.GenerateFolder(final_folder)   
    
    imgs_folder=[imgs_folder]
    
    #ratio 0.1-0.9 step is 0.1
    for k in range(1,10):
        
        center_weight=0.16+0.04*k
        
        this_weight=[center_weight]+4*[(1-center_weight)/4]
        
#        print(this_weight)
        
        '''Constant'''
        #plot curve
        C_C.ContrastCurve(imgs_folder,'Constant','5-Area',ROI_weight=this_weight)
    
        plt.grid()
        
        plt.savefig(final_folder+str(k)+' (Constant).png',dpi=300,bbox_inches='tight')
        plt.close()
        
        '''Standard Deviation'''
        #plot curve
        C_C.ContrastCurve(imgs_folder,'Standard Deviation','5-Area',ROI_weight=this_weight)
    
        plt.grid()
        
        plt.savefig(final_folder+str(k)+' (Standard Deviation).png',dpi=300,bbox_inches='tight')
        plt.close()
        
        '''Advanced'''
        #plot curve
        C_C.ContrastCurve(imgs_folder,'Advanced','5-Area',ROI_weight=this_weight)
    
        plt.grid()
        
        plt.savefig(final_folder+str(k)+' (Advanced).png',dpi=300,bbox_inches='tight')
        plt.close()
        
#------------------------------------------------------------------------------
"""
Experiment: 5 area module factor

Args:
    imgs_folder: images folder  
    output_folder: figs output_folder

Returns:
    None
"""
def Experiment5AreaFactor(imgs_folder,output_folder):
    
    final_folder=output_folder+'\\5-Area\\Factor\\'
    
    #construct a folder
    O_P.GenerateFolder(final_folder)   
    
    imgs_folder=[imgs_folder]
    
    #ratio 0.1-0.9 step is 0.1
    for k in range(1,10):
         
        this_factor=10+2*k
        
#        print(this_weight)
        
        '''Constant'''
        #plot curve
        C_C.ContrastCurve(imgs_folder,'Constant','5-Area',zoom_factor=this_factor)
    
        plt.grid()
        
        plt.savefig(final_folder+str(k)+' (Constant).png',dpi=300,bbox_inches='tight')
        plt.close()
        
        '''Standard Deviation'''
        #plot curve
        C_C.ContrastCurve(imgs_folder,'Standard Deviation','5-Area',zoom_factor=this_factor)
        
        plt.grid()
        
        plt.savefig(final_folder+str(k)+' (Standard Deviation).png',dpi=300,bbox_inches='tight')
        plt.close()
        
        '''Advanced'''
        #plot curve
        C_C.ContrastCurve(imgs_folder,'Advanced','5-Area',zoom_factor=this_factor)
    
        plt.grid()
        
        plt.savefig(final_folder+str(k)+' (Advanced).png',dpi=300,bbox_inches='tight')
        plt.close()
            
#------------------------------------------------------------------------------
"""
Operate comparison experiment

Args:
    folder_experiment: experiment imgs total folder
    series_mode: contrast series ['Constant','Advanced','Standard Deviation']
    save_fig: whether to save fog (default: True)
    
Returns:
    None
"""
def ExperimentContrastComparison(folder_experiment,series_mode,save_fig=True):
    
    for name_this_group in os.listdir(folder_experiment):
        
        #join the path
        folder_this_group=folder_experiment+'\\'+name_this_group
        
    #    print(folder_this_group)
        
        #imgs of this group experiment
        list_imgs_folder=[]
        
        for name_this_imgs_folder in os.listdir(folder_this_group):
        
            if '.png' in name_this_imgs_folder:
                
                continue
            
            #join the path
            this_imgs_folder=folder_this_group+'\\'+name_this_imgs_folder
            
    #        print(this_imgs_folder)
            
            list_imgs_folder.append(this_imgs_folder)
               
        #Constant contrast mode
        C_C.ContrastCurve(list_imgs_folder,series_mode)
        
        if save_fig:
            
            plt.grid()
            
            plt.savefig(folder_this_group+'\\'+series_mode+'.png',dpi=300,bbox_inches='tight')
            plt.close()

#------------------------------------------------------------------------------
"""
Operate experiment among various contrast operator

Args:
    imgs_folder: imgs folder
    
Returns:
    None
"""
def ExperimentOperator(imgs_folder):
    
    print('')
    print('-- Experiment Operator')

    for this_contrast_operator in list_contrast_operator:
       
        S_A_F.ImageAndContrast(imgs_folder,this_contrast_operator)
        
#------------------------------------------------------------------------------
"""
Operate experiment among various contrast operator

Args:
    list_imgs_folder: imgs folder of various scenario
    contrast_operator: operator to calculate contrast
    
Returns:
    None
"""        
def ExperimentScenario(list_imgs_folder,contrast_operator):
        
    print('')
    print('-- Experiment Scenario')
    
    for this_imgs_folder in list_imgs_folder:
        
        S_A_F.ImageAndContrast(this_imgs_folder,contrast_operator)
        
#------------------------------------------------------------------------------
"""
Operate experiment among various experiment and scenario

Args:
    list_imgs_folder: imgs folder of various scenario
    
Returns:
    None
"""   
def ExperimentOverall(list_imgs_folder):
    
    print('')
    print('-- Experiment Overall')
    
    for this_contrast_operator in list_contrast_operator:
        
        for this_imgs_folder in list_imgs_folder:
            
#            S_A_F.ImageAndContrast(this_imgs_folder,this_contrast_operator)
            C_P_S.FullSweep(this_imgs_folder,this_contrast_operator)
    