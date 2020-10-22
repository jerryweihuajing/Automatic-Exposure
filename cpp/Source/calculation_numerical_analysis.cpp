// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Calculation on Numerical Analysis
******************************************************************************/

#include "..\Header\operation_vector.h"
#include "..\Header\calculation_numerical_analysis.h"

//------------------------------------------------------------------------------
/*
Calculation of vector normalization

Args:
	which_vector: vector object to be calculated

Returns:
	normalized vector
*/
vector<double> Normalize(vector<double>& which_vector) {

	//maximum and minimum
	double minimum = VectorMinimum(which_vector);
	double maximum = VectorMaximum(which_vector);

	//final result
	vector<double> vector_normalized;

	if (minimum == maximum) {
		
		for (int i = 0; i < which_vector.size(); i++) {

			vector_normalized.push_back(0);
		}
	}
	else {

		for (int i = 0; i < which_vector.size(); i++) {
			
			vector_normalized.push_back((which_vector[i] - minimum) / (maximum - minimum));
		}
	}
	return vector_normalized;
}