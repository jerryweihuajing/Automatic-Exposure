# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 15:28:43 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Calculation of Evaluation
"""

from configuration_color import list_contrast_operator,\
                                list_tenengrad_operator,\
                                list_texture_feature_operator

import calculation_contrast as C_C
import calculation_tenengrad as C_T
import calculation_texture_feature as C_T_F
import calculation_exposure_evaluation as C_E_E

#------------------------------------------------------------------------------
"""
Calculation of evaluation function with different operator

Args:
    img_gray: matrix of gray img
    contrast_operator: operator of contrast calculation
    
Returns:
    evaluation function value
"""
def Evaluate(img_gray,operator):
    
    '''Contrast'''
    if operator in list_contrast_operator:
    
        return C_C.GlobalContrast(img_gray,operator)
    
    '''Tenengrad'''
    if operator in list_tenengrad_operator:
        
        return C_T.Tenengrad(img_gray,operator)
    
    '''Gradient'''
    if 'Gradient' in operator:
        
        return C_E_E.Gradient(img_gray,operator)
            
    '''Texture Feature'''
    if operator in list_texture_feature_operator:
        
        return C_T_F.MapTextureFeature(img_gray)[operator]
