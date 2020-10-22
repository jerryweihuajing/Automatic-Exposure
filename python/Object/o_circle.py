# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 15:00:06 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-circle
"""

import numpy as np

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())

    
import calculation_rasterization as C_R

#==============================================================================
#圆形
#==============================================================================
class circle:
    def __Init__(self,
                 Id=None,
                 area=None,
                 radius=None,
                 center=None,
                 points_above=None,
                 points_inside=None):      
        self.Id=Id
        self.area=area
        self.radius=radius
        self.center=center
        self.points_above=points_above
        self.points_inside=points_inside
        
    #初始化内部点points_above和points_inside
    def Init(self,method=2):
        
        self.area=np.pi*self.radius**2
        self.center=np.array(self.center)
        self.points_above=[]  
        self.points_inside=[] 
        
        #方向角
        alpha=np.linspace(-np.pi,np.pi,num=500)
           
        #圆上点         
        for this_alpha in alpha:
            
            this_pos=self.center+np.array([self.radius*np.cos(this_alpha),self.radius*np.sin(this_alpha)])
            
            #判断应不应该加入
            if list(this_pos.astype(int)) not in self.points_above:
                
                self.points_above.append(list(this_pos.astype(int)))
        
        '''1 极坐标填充法：计算量可能较大，会有大量重复'''
        if method==1:
            
            #填充点
            for this_radius in range(self.radius):
                
                for this_alpha in alpha:
                    
                    this_pos=self.center+np.array([this_radius*np.cos(this_alpha),this_radius*np.sin(this_alpha)])
                    
                    #判断应不应该加入
                    if list(this_pos.astype(int)) not in self.points_inside:
                        
                        self.points_inside.append(list(this_pos.astype(int)))        
                
        '''边界求内容：该方法要求points_above是个连通域，若非连通可用膨胀腐蚀解决''' 
        if method==2:
            
            C_R.Boundary2Content(self)
            
    #画出位置
    def Plot(self,which_canvas):
        
        C_R.GraphicPlot(self,which_canvas)
        
    #填充图形
    def Fill(self,which_canvas):
        
        C_R.GraphicFill(self,which_canvas)