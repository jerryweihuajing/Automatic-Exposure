# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:00:27 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Search of exposure evaluation peak value
"""

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator

import operation_path as O_P
import operation_import as O_I

import calculation_numerical_analysis as C_N_A

from configuration_font import legend_prop,\
                               text_prop,\
                               label_prop,\
                               title_prop,\
                               sample_prop,\
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
Calculation of peak value in exposure evaluation value coarsely

Args:
    list_exposure_evaluation: exposure evaluation value list
    
Returns:
    start index and end index for fine search
"""
def JLSearch(list_exposure_evaluation):
  
    #amount of consecutive ascending or descending points
    amount_revert=3
    
    #real-time
    amount_ascending,amount_descending=0,0
    
    #strat and end point for fine search
    index_a,index_b=None,None
    
    #index of maximum
    index_maximum=list_exposure_evaluation.index(np.max(list_exposure_evaluation))

    for k in range(len(list_exposure_evaluation)-1):
        
        '''ascending'''
        if list_exposure_evaluation[k]<list_exposure_evaluation[k+1]:
            
            amount_ascending+=1
            amount_descending=0  
                    
        if list_exposure_evaluation[k]==list_exposure_evaluation[k+1]:
        
            continue
        
        '''descending'''
        if list_exposure_evaluation[k]>list_exposure_evaluation[k+1]:
            
            amount_descending+=1
            amount_ascending=0
        
        #end index of ascending
        if amount_ascending>=amount_revert:

            index_a=k+1
   
        #start index of descending
        if amount_descending>=amount_revert:
            
            index_b=k-amount_descending+1

        if index_a!=None and index_b!=None:
    
            #expire the exception
            if index_a==index_maximum and index_b==index_maximum:
                
                return index_a-1,index_b+1
    
    return

#------------------------------------------------------------------------------
"""
Calculation of peak value in global search

Args:
    list_exposure_evaluation: exposure evaluation list
    step_frame: step of frame object (default: 1)
    
Returns:
    list of frame index to be plotted
"""   
def GlobalSearch(list_exposure_evaluation,step_frame=1):

    #final result
    list_index_plotted=[]
    
    for k in range(len(list_exposure_evaluation)):
        
        this_index=k*step_frame
        
        #out of bound
        if this_index>=len(list_exposure_evaluation):
            
            break
        
        list_index_plotted.append(this_index)
    
    return list_index_plotted

#------------------------------------------------------------------------------
"""
Calculation of peak value in coarse-to-fine search

Args:
    list_exposure_evaluation: exposure evaluation list
    step_frame: step of frame object (default: 5)
    
Returns:
    list of frame index to be plotted
"""   
def Coarse2FineSearch(list_exposure_evaluation,step_frame=5):
    
    #final result
    list_index_plotted=[]
    
    #collect frame coarsely
    for k in range(len(list_exposure_evaluation)):
        
        this_index=k*step_frame
        
        #out of bound
        if this_index>=len(list_exposure_evaluation):
            
            break
        
        list_index_plotted.append(this_index)
    
    step_fine=step_frame-1
    
    #start idx and end idx in fine search
    start_idx_fine=list_exposure_evaluation.index(np.max(list_exposure_evaluation))-step_fine
    end_idx_fine=list_exposure_evaluation.index(np.max(list_exposure_evaluation))+step_fine+1
    
    if start_idx_fine<0:
            
        start_idx_fine=0
            
    if end_idx_fine>=len(list_exposure_evaluation):
        
        end_idx_fine=len(list_exposure_evaluation)-1
    
    #collect frame finely
    for k in range(start_idx_fine,end_idx_fine):

        list_index_plotted.append(k)
        
    return list_index_plotted

#------------------------------------------------------------------------------
"""
Calculation of peak value in binary search

Args:
    list_exposure_evaluation: exposure evaluation list
    m: index of step
    
Returns:
    list of frame index to be plotted
"""   
def BinarySearch(list_exposure_evaluation,m=6):

    #final result
    list_index_plotted=[]
    
    m_this_round=cp.deepcopy(m)
    step_this_round=2**m_this_round
    
    #init start index and end index
    start_idx_this_round=0
    end_idx_this_round=int((len(list_exposure_evaluation)//step_this_round)*step_this_round)
    
    #loop
    while m_this_round:
        
        step_this_round=2**m_this_round
        
        if step_this_round>len(list_exposure_evaluation):
            
            m_this_round-=1
            
            continue
        
        if start_idx_this_round<0:
            
            start_idx_this_round=0
            
        if end_idx_this_round>=len(list_exposure_evaluation):
            
            end_idx_this_round=len(list_exposure_evaluation)-1-step_this_round
            
        #frame list for this iteration
        list_index_this_round=[k for k in range(start_idx_this_round, end_idx_this_round+step_this_round,step_this_round)]
        
        list_exposure_evaluation_this_round=[list_exposure_evaluation[this_index] for this_index in list_index_this_round]
        
        peak_idx_this_round=list_exposure_evaluation.index(np.max(list_exposure_evaluation_this_round))
        
        #redefine such parameters
        start_idx_this_round=int(peak_idx_this_round-1.5*step_this_round)
        end_idx_this_round=int(peak_idx_this_round+1.5*step_this_round)
         
        m_this_round-=1
        
        list_index_plotted+=list_index_this_round
        
    return list_index_plotted

#------------------------------------------------------------------------------
"""
Plot input image as well as exposure evaluation curve

Args:
   imgs_folder: folder which contains a batch of images 
   operator: operator of exposure evaluation or tenengrad calculation 
   ROI mode: definition method of ROI ['5-Area', 'Center']
   peak_search_method: method of peak search
   
Returns:
    None
"""
def PeakSearch(imgs_folder,operator,ROI_mode,peak_search_method):
    
    print('')
    print('-- Peak Search')
    print('-> operator:',operator)
    print('-> ROI mode:',ROI_mode)
    print('-> peak search method:',peak_search_method)
    print('')
    
    str_a,str_b=imgs_folder.split('Material')
    str_c,str_d=imgs_folder.split('Material')[-1].strip('\\').split('\\')

    #construct output folder
    output_folder_operator=str_a+'\\AE Curve\\Scenario'+str_b
    
    try:
        
        output_folder_condition=output_folder_operator.split(str_c)[0].replace('\\Scenario','')+'\\Operator'
    
    except:
        
        output_folder_condition=str_a+'\\AE Curve\Operator'
    
    output_folder_operator+='\\'+operator+'\\'
    output_folder_condition+='\\'+operator+'\\'
    
    O_P.GenerateFolder(output_folder_operator)
    O_P.GenerateFolder(output_folder_condition)
    
    #frame object for coarse and fine search
    list_frame=O_I.FramesConstruction(imgs_folder,operator,ROI_mode)
    list_exposure_evaluation=[this_frame.exposure_evaluation for this_frame in list_frame]

    '''Global Search (Full Sweep)'''
    if peak_search_method=='Global':
        
        list_index_plotted=GlobalSearch(list_exposure_evaluation)
        abbr_method='GS'
        
    '''Coarse to Fine Search'''
    if peak_search_method=='Coarse2Fine':
        
        list_index_plotted=Coarse2FineSearch(list_exposure_evaluation)
        abbr_method='C2F'
        
    '''Binary Search (Fibonacci)'''
    if peak_search_method=='Binary':
        
        list_index_plotted=BinarySearch(list_exposure_evaluation)
        abbr_method='BS'
    
    list_frame_plotted=[list_frame[this_index] for this_index in list_index_plotted]
    list_exposure_time_plotted=[this_frame.exposure_time for this_frame in list_frame_plotted]    
    list_exposure_evaluation_plotted=[this_frame.exposure_evaluation for this_frame in list_frame_plotted]
    list_average_luminance_plotted=[this_frame.average_luminance for this_frame in list_frame]

    peak_index=list_exposure_evaluation_plotted.index(np.max(list_exposure_evaluation_plotted))
    
    #normalization of exposure time and exposure evaluation list
    list_exposure_time_plotted=list(np.array(list_exposure_time_plotted)//1000)
    list_normalized_exposure_evaluation_plotted=C_N_A.Normalize(list_exposure_evaluation_plotted)
    list_normalized_average_luminance_plotted=C_N_A.Normalize(list_average_luminance_plotted)
    
    plt.figure(figsize=(17,6))
    
    #tick step
    x_major_step=(np.max(list_exposure_time_plotted)-np.min(list_exposure_time_plotted))//10
    factor=10**(len(str(int(x_major_step)))-1)
    
    x_major_step=int(np.round(x_major_step/factor)*factor)
    x_minor_step=x_major_step/2

    y_major_step=0.1
    y_minor_step=0.05
    
    #limit of x and y
    x_min,x_max=np.min(list_exposure_time_plotted)-x_major_step,\
                np.max(list_exposure_time_plotted)+x_major_step
    y_min,y_max=0-.023*2,1+.023*2
    
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
    
    peak_exposure_time=list_exposure_time_plotted[peak_index]
    peak_normalized_exposure_evaluation=list_normalized_exposure_evaluation_plotted[peak_index]
    
    plt.imshow(list_frame_plotted[peak_index].img_gray,cmap='gray')
    plt.imshow(list_frame_plotted[peak_index].img_ROI,cmap='seismic_r') 
        
    print('')
    print('---> Peak Exposure Time:',int(peak_exposure_time),'(ms)')
    
    plt.title('Input Image',fontdict=title_prop)
    
    plt.xticks([])
    plt.yticks([])
    
    '''exposure evaluation curve'''
    ax_exposure_evaluation_curve=plt.subplot(122)
    
    #set ticks fonts
    plt.tick_params(labelsize=12)
    labels=ax_exposure_evaluation_curve.get_xticklabels()+ax_exposure_evaluation_curve.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.xlabel('Exposure Time(ms)',fontdict=label_prop)   
    plt.ylabel('Evaluation Evaluation',fontdict=label_prop)
    
    if operator in list_contrast_operator:
        
        str_focus_value=operator+' Contrast'
        
    if operator in list_tenengrad_operator:
        
        str_focus_value=operator+' Tenengrad'
       
    if operator in list_exposure_evaluation_operator:
        
        str_focus_value=operator
        
    plt.title('Exposure Evaluation-Exposure Time Curve',fontdict=title_prop)
        
    #exposure evaluation curve
    plt.plot(list_exposure_time_plotted,
             list_normalized_exposure_evaluation_plotted,
             color=map_operator_color[operator],
             marker='.',
             markersize=8,
             linestyle='-',
             label=str_focus_value)
    
    #everage luminance curve
    plt.plot(list_exposure_time_plotted,
             list_normalized_average_luminance_plotted,
             color='gray',
             marker='.',
             markersize=8,
             linestyle='-',
             label='Average Luminance')
    
    plt.legend(prop=legend_prop,loc='lower right')

    #axis boundary
    plt.xlim([x_min,x_max])
    plt.ylim([y_min,y_max])
    
    #horizontal line
    plt.hlines(peak_normalized_exposure_evaluation,
               x_min,
               x_max,
               color='grey',
               linestyles="--")
    
    #vertical line
    plt.vlines(peak_exposure_time,
               y_min,
               y_max,
               color='grey',
               linestyles="--")

    #set locator
    ax_exposure_evaluation_curve.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax_exposure_evaluation_curve.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax_exposure_evaluation_curve.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax_exposure_evaluation_curve.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
    
    #annotation of peak exposure_time
    ax_exposure_evaluation_curve.annotate('Peak: %d'%(peak_exposure_time),
                               xy=(peak_exposure_time,peak_normalized_exposure_evaluation),
                               xytext=(peak_exposure_time+x_major_step/10,peak_normalized_exposure_evaluation+y_major_step/10),
                               color='k',
                               fontproperties=sample_prop)
    
    #basic parameter                     
    ax_exposure_evaluation_curve.text(0+x_major_step/10,
                                      0+y_major_step/10,
                                      str_text,
                                      fontdict=annotation_prop) 
         
    #peak search parameter
    ax_exposure_evaluation_curve.text(0+x_major_step/10,
                                      1+y_major_step/10,
                                      'Method: %s Iters: %d'%(abbr_method,len(list_frame_plotted)),
                                      fontdict=text_prop) 
    
    #save the fig
    '''operator experiment'''
    fig_path_operator=output_folder_operator+'//%s.png'%peak_search_method
    
    '''condition experiment'''
    fig_path_condition=output_folder_condition+'%s %s (%s).png'%(str_c,str_d,peak_search_method)
    
    plt.grid()  

    plt.savefig(fig_path_operator,dpi=300,bbox_inches='tight')
    plt.savefig(fig_path_condition,dpi=300,bbox_inches='tight')
    plt.close()
    