# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 11:08:33 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Export
"""

def WriteTupleList2File(which_tuple_list,file_name):
    
    '''filename does not exist, it is automatically created'''
    #'w' means write data, and the original data in the file is cleared before writing!
    with open(file_name,'w') as file: 
        
        for k in range(len(which_tuple_list)):
            
            file.write('%d'%which_tuple_list[k][0])
            file.write(',')
            file.write('%d'%which_tuple_list[k][1])
            file.write('\n')