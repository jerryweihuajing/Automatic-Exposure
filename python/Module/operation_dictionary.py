# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 10:44:22 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Dictionary Operation
"""

#------------------------------------------------------------------------------
"""
To arrange the dictionary index in the order of a list

Args:
    which_dict: dictionary object to be arranged
    which_keys: keys list of new dictionary
    
Returns:
    new dictionary object
"""
def DictSortByIndex(which_dict,which_keys):
    
    #The results of operation
    that_dict={}
    
    #Traverse the new list and populate the dictionary
    for this_key in which_keys:
        
        that_dict[this_key]=which_dict[this_key]
        
    return that_dict