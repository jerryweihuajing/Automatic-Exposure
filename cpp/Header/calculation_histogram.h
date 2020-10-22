// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Header-Calculation on Histogram
******************************************************************************/

#include "..\init.h"

#ifndef _CALCULATION_HISTOGRAM_H_
#define _CALCULATION_HISTOGRAM_H_

//Flatten img matrix as a vector
vector <int> VectorImgGray(Mat& img_gray);

//Calculate gray level
vector<int> VectorGrayLevel(int step_gray_level);

//Calculate ROI matrix gray level amount vector
vector<int> VectorGrayLevelAmount(vector<int>& vector_img_gray);

//Calculate ROI matrix gray level frequency vector
vector<double> VectorGrayLevelFrequency(vector<int>& vector_img_gray);

#endif