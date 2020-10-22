// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Header-Calculation on Contrast
******************************************************************************/

#include "..\init.h"
#include "object_frame.h"

#ifndef _CALCULATION_CONTRAST_H_
#define _CALCULATION_CONTRAST_H_

//Calculate ROI matrix as an vector
vector<int> VectorROI(Mat& img_gray, int center_ROI[2]);

//Calculate contrast of ROI vector
double ContrastROI(vector<int>& vector_ROI, const string& contrast_operator);

//Calculate 5-Area contrast of image
double Contrast5Area(Mat& img_gray, const string& contrast_operator);
double Contrast5Area(frame& which_frame, const string& contrast_operator);

//Calculate center contrast of image
double ContrastCenter(Mat& img_gray, const string& contrast_operator);
double ContrastCenter(frame& which_frame, const string& contrast_operator);

#endif