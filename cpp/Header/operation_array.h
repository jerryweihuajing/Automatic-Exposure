// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Header-Operation on Array
******************************************************************************/

#include "..\init.h"

#ifndef _OPERATION_ARRAY_H_
#define _OPERATION_ARRAY_H_

//Calculate length of array
size_t ArrayLength(int* which_array);
size_t ArrayLength(float* which_array);
size_t ArrayLength(double* which_array);
size_t ArrayLength(char* which_array);

//Calculate sum of array
int ArraySum(int* which_array);
float ArraySum(float* which_array);
double ArraySum(double* which_array);

//Calculate average of array
double ArrayAverage(int* which_array);
double ArrayAverage(float* which_array);
double ArrayAverage(double* which_array);

//The array elements are multiplied
int ArrayMultiplication(int* array_A, int* array_B);
float ArrayMultiplication(int* array_A, float* array_B);
double ArrayMultiplication(int* array_A, double* array_B);

#endif