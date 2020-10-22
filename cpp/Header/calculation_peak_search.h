// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Header-Calculation on Peak Search
******************************************************************************/

#include "..\init.h"

#ifndef _CALCULATION_PEAK_SEARCH_H_
#define _CALCULATION_PEAK_SEARCH_H_

//Calculate index of vector maximum
int MaximumIndex(vector<double>& which_vector);

//Calculation of peak value in contrast value coarsely
int JLSearch(vector<double>& vector_contrast);

//Calculation of peak value in contrast value finely
int GlobalSearch(vector<double>& vector_contrast);

#endif