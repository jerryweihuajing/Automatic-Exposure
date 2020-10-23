# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:47:58 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Search of best frame based on suitable luminance
"""

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
                               sample_prop,\
                               annotation_prop
                                


from configuration_parameter import zoom_factor,\
                                    ROI_weight_5_area,\
                                    ROI_weight_9_area,\
                                    luminance_threshold
                                 
#------------------------------------------------------------------------------
"""
Plot input image as well as suitable AE result

Args:
   imgs_folder: folder which contains a batch of images 
   ROI mode: definition method of ROI ['9-Area', '5-Area', 'Center']
   
Returns:
    None
"""
def SuitableLuminanceSearch(imgs_folder,ROI_mode):
    
    operator='Luminance'
    peak_search_method='Global'
    
    print('')
    print('-- Suitable Luminance Search')
    print('-> operator:',operator)
    print('-> ROI mode:',ROI_mode)
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
    list_frame=O_I.FramesConstruction(imgs_folder,'Boccignone',ROI_mode)
    list_average_luminance=[this_frame.average_luminance for this_frame in list_frame]
    
    '''Global Search (Full Sweep)'''
    if peak_search_method=='Global':
        
        list_index_plotted=C_P_S.GlobalSearch(list_average_luminance)
        abbr_method='GS'
        
    '''Coarse to Fine Search'''
    if peak_search_method=='Coarse2Fine':
        
        list_index_plotted=C_P_S.Coarse2FineSearch(list_average_luminance)
        abbr_method='C2F'
        
    '''Binary Search (Fibonacci)'''
    if peak_search_method=='Binary':
        
        list_index_plotted=C_P_S.BinarySearch(list_average_luminance)
        abbr_method='BS'
        
    list_frame_plotted=[list_frame[this_index] for this_index in list_index_plotted]
    
    #variable in axis X
    list_exposure_time_plotted=[this_frame.exposure_time for this_frame in list_frame]  
    list_exposure_time_plotted=list(np.array(list_exposure_time_plotted)//1000)
    
    #variable in axis Y
    list_average_luminance_plotted=[this_frame.average_luminance for this_frame in list_frame_plotted]

    #get suitable frame
    for k in range(len(list_average_luminance_plotted)):

        if list_average_luminance_plotted[k]>luminance_threshold:
            
            peak_index=k
            
            break

    plt.figure(figsize=(17,6))
    
    #tick step
    x_major_step=(np.max(list_exposure_time_plotted)-np.min(list_exposure_time_plotted))//10
    factor=10**(len(str(int(x_major_step)))-1)
    
    x_major_step=int(np.round(x_major_step/factor)*factor)
    x_minor_step=x_major_step/2

    y_major_step=32
    y_minor_step=16
    
    #limit of x and y
    x_min,x_max=np.min(list_exposure_time_plotted)-x_major_step,\
                np.max(list_exposure_time_plotted)+x_major_step
    y_min,y_max=0-13,256+13
    
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
    peak_average_luminance=list_average_luminance_plotted[peak_index]
    
    plt.imshow(list_frame[peak_index].img_gray,cmap='gray')
    plt.imshow(list_frame[peak_index].img_ROI,cmap='seismic_r') 
        
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
    plt.ylabel('Average Luminance',fontdict=label_prop)

    plt.title('Average Luminance-Exposure Time Curve',fontdict=title_prop)
        
    #everage luminance curve
    plt.plot(list_exposure_time_plotted,
             list_average_luminance_plotted,
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
    plt.hlines(peak_average_luminance,
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
                               xy=(peak_exposure_time,peak_average_luminance),
                               xytext=(peak_exposure_time+x_major_step/10,peak_average_luminance+y_major_step/10),
                               color='k',
                               fontproperties=sample_prop)
    
    #basic parameter                     
    ax_exposure_evaluation_curve.text(0+x_major_step/10,
                                      0+y_major_step/10,
                                      str_text,
                                      fontdict=annotation_prop) 
         
    #peak search parameter
    ax_exposure_evaluation_curve.text(0+x_major_step/10,
                                      256+y_major_step/10,
                                      'Method: %s Iters: %d'%(abbr_method,len(list_frame)),
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