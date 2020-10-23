# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 17:54:22 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Simulation of AutoFocus
"""

import imageio
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator

import operation_path as O_P
import operation_import as O_I

import calculation_peak_search as C_P_S
import calculation_numerical_analysis as C_N_A

from configuration_font import legend_prop,\
                               text_prop,\
                               label_prop,\
                               title_prop,\
                               annotation_prop

from configuration_color import map_operator_color,\
                                list_contrast_operator,\
                                list_tenengrad_operator,\
                                list_exposure_evaluation_operator

from configuration_parameter import zoom_factor,\
                                    ROI_weight_5_area,\
                                    ROI_weight_9_area

#------------------------------------------------------------------------------
"""
Plot animation field of FOV

Args:
   imgs_folder: folder which contains a batch of images 
   operator: operator of contrast or tenengrad calculation 
   ROI mode: definition method of ROI ['5-Area', 'Center']
   peak_search_method: method of peak search
   
Returns:
    None
"""
def FOVAnimation(imgs_folder,operator,ROI_mode,peak_search_method):
    
    print('')
    print('-- AF Animation')
    print('-> operator:',operator)
    print('-> ROI mode:',ROI_mode)
    print('-> peak search method:',peak_search_method)
    print('')
    
    str_a,str_b=imgs_folder.split('Material')
    str_c,str_d=imgs_folder.split('Material')[-1].strip('\\').split('\\')

    #construct output folder
    output_folder_operator=str_a+'\\AE Simulation\\Scenario'+str_b
    
    try:
        
        output_folder_condition=output_folder_operator.split(str_c)[0].replace('\\Scenario','')+'\\Operator'
    
    except:
        
        output_folder_condition=str_a+'\\AE Simulation\Operator'
    
    output_folder_operator+='\\'+operator+'\\'
    output_folder_condition+='\\'+operator+'\\'
    
    O_P.GenerateFolder(output_folder_operator)
    O_P.GenerateFolder(output_folder_condition)
    
    #frame object for coarse and fine search
    list_frame=O_I.FramesConstruction(imgs_folder,operator,ROI_mode)
    list_contrast=[this_frame.exposure_evaluation for this_frame in list_frame]
    
    '''Global Search (Full Sweep)'''
    if peak_search_method=='Global':
        
        list_index_plotted=C_P_S.GlobalSearch(list_contrast)
        abbr_method='GS'
        
    '''Coarse to Fine Search'''
    if peak_search_method=='Coarse2Fine':
        
        list_index_plotted=C_P_S.Coarse2FineSearch(list_contrast)
        abbr_method='C2F'
        
    '''Binary Search (Fibonacci)'''
    if peak_search_method=='Binary':
        
        list_index_plotted=C_P_S.BinarySearch(list_contrast)
        abbr_method='BS'
    
    figures=[]
    
    for k in range(len(list_index_plotted)):
        
        list_frame_plotted=[list_frame[this_index] for this_index in list_index_plotted][:k+1]
        list_code_plotted=[this_frame.exposure_time for this_frame in list_frame_plotted]    
        list_contrast_plotted=[this_frame.exposure_evaluation for this_frame in list_frame_plotted]

        #normalization of code and contrast list
        list_code_plotted=list(np.array(list_code_plotted)//1000)
        list_normalized_contrast_plotted=C_N_A.Normalize(list_contrast_plotted)
        
        plt.figure(figsize=(17,6))
        
        #limit of x and y
        x_min,x_max=np.min(list_code_plotted)-250,np.max(list_code_plotted)+250
        y_min,y_max=0-.023*2,1+.023*2
        
        #tick step
        x_major_step=500
        x_minor_step=250
        y_major_step=0.1
        y_minor_step=0.05
        
        #text of parameter
        if ROI_mode=='5-Area':
                    
            str_text='ROI Zoom Factor: %d Weight: %.2f-%.2f'%(zoom_factor/2,
                                                              ROI_weight_5_area[0],
                                                              ROI_weight_5_area[1])
            
        if ROI_mode=='9-Area':
                
            str_text='ROI Zoom Factor: %d Weight: %.2f-%.2f'%(zoom_factor/2,
                                                              ROI_weight_9_area[4],
                                                              ROI_weight_9_area[0])
            
        if ROI_mode=='Center':              
    
            str_text='ROI Zoom Factor: %d'%(zoom_factor/2)  
            
        '''input image and bound'''
        ax_input_image=plt.subplot(121)
        
        plt.imshow(list_frame_plotted[k].img_gray,cmap='gray')
        plt.imshow(list_frame_plotted[k].img_ROI,cmap='seismic_r') 
        
        plt.title('Input Image',fontdict=title_prop)
        
        plt.xticks([])
        plt.yticks([])
        
        '''contrast curve'''
        ax_contrast_curve=plt.subplot(122)
        
        #set ticks fonts
        plt.tick_params(labelsize=12)
        labels=ax_contrast_curve.get_xticklabels()+ax_contrast_curve.get_yticklabels()
        
        #label fonts
        [this_label.set_fontname('Times New Roman') for this_label in labels]
            
        plt.xlabel('Exposure Time(ms)',fontdict=label_prop)   
        plt.ylabel('Evaluation Function',fontdict=label_prop)
        
        if operator in list_contrast_operator:
        
            str_focus_value=operator+' Contrast'
            
        if operator in list_tenengrad_operator:
            
            str_focus_value=operator+' Tenengrad'
           
        if operator in list_exposure_evaluation_operator:
            
            str_focus_value=operator
                
        plt.title('Exposure Evaluation-Exposure Time Curve',fontdict=title_prop)
        
        plt.plot(list_code_plotted,
                 list_normalized_contrast_plotted,
                 color=map_operator_color[operator],
                 marker='.',
                 markersize=8,
                 linestyle='-',
                 label=str_focus_value)
        
        plt.legend(prop=legend_prop,loc='lower right')
    
        #axis boundary
        plt.xlim([x_min,x_max])
        plt.ylim([y_min,y_max])

        #set locator
        ax_contrast_curve.xaxis.set_major_locator(MultipleLocator(x_major_step))
        ax_contrast_curve.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
        ax_contrast_curve.yaxis.set_major_locator(MultipleLocator(y_major_step))
        ax_contrast_curve.yaxis.set_minor_locator(MultipleLocator(y_minor_step))

        #basic parameter                     
        ax_contrast_curve.text(0+x_major_step/10,
                               0+y_major_step/10,
                               str_text,
                               fontdict=annotation_prop) 

        #peak search parameter
        ax_contrast_curve.text(0+x_major_step/10,
                               1+y_major_step/10,
                               'Method: %s Iter: %d'%(abbr_method,k),
                               fontdict=text_prop)
        
        #save the fig
        this_fig_path=output_folder_operator+'//Lens %d.png'%(list_code_plotted[k])
        
        plt.grid()
        
        plt.savefig(this_fig_path,dpi=300,bbox_inches='tight')
        plt.close()
        
        #collect fig to create GIF
        figures.append(imageio.imread(this_fig_path))
        
    '''operator experiment'''
    fig_path_operator=output_folder_operator+'//%s.gif'%peak_search_method
    
    '''condition experiment'''
    fig_path_condition=output_folder_condition+'%s %s (%s).gif'%(str_c,str_d,peak_search_method)
    
    #save GIF   
    '''operator experiment'''
    imageio.mimsave(fig_path_operator,figures,duration=0.23) 
    
    '''scenario experiment'''
    imageio.mimsave(fig_path_condition,figures,duration=0.23) 
    