// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Discrimination of Foreground and Background
******************************************************************************/

#include "..\Header\operation_vector.h"
#include "..\Header\calculation_histogram.h"
#include "..\Header\calculation_scene_discrimination.h"

//------------------------------------------------------------------------------
/*
Calculate average luminance of foreground and background

Args:
	vector_ROI: ROI whose type is vector of 1-D

Returns:
	vector average luminance of foreground and background
*/
vector<double> ForeAndBackLuminance(vector<int> vector_ROI) {

	//result vector
	vector<double> fore_back_luminance;

	//threshold of accuracy for iteration
	double e = 0.1;

	//gray level and their frequency
	vector<int> vector_gray_level = VectorGrayLevel(1);
	vector<double> vector_gray_frequency = VectorGrayLevelFrequency(vector_ROI);

	//calculate avearge gray level
	double average_gray_level = VectorMultiplication(vector_gray_level, vector_gray_frequency);

	//calculate index of gray value who is smaller or bigger than threshold
	vector<int> index_vector_b = VectorIndexBelowThreshold(vector_gray_level, average_gray_level);
	vector<int> index_vector_f = VectorIndexAboveThreshold(vector_gray_level, average_gray_level);

	//init threshold
	double threshold_pre = average_gray_level;
	double threshold_next = threshold_pre + 10 * e;

	//divide the gray level and frequency to background(b) and foreground(f)
	double average_gray_level_b, average_gray_level_f;
	vector<int>vector_gray_level_b, vector_gray_level_f;
	vector<double>vector_gray_frequency_b, vector_gray_frequency_f;
	vector<double>list_average_gray_level_b, list_average_gray_level_f;

	int count = 0;

	while (abs(threshold_next - threshold_pre) > e) {

		threshold_pre = (threshold_next);

		//divide gray level
		index_vector_b = VectorIndexBelowThreshold(vector_gray_level, threshold_pre);
		index_vector_f = VectorIndexAboveThreshold(vector_gray_level, threshold_pre);

		//divide gray level
		vector_gray_level_b = VectorFromIndex(vector_gray_level, index_vector_b);
		vector_gray_level_f = VectorFromIndex(vector_gray_level, index_vector_f);

		//divide gray level frequency
		vector_gray_frequency_b = VectorFromIndex(vector_gray_frequency, index_vector_b);
		vector_gray_frequency_f = VectorFromIndex(vector_gray_frequency, index_vector_f);

		//average value of gray level of b & f
		if (VectorSum(vector_gray_frequency_f) == 0.0) {

			if (count > 0) {

				average_gray_level_f = list_average_gray_level_f[list_average_gray_level_f.size() - 1];
			}
			else {

				average_gray_level_f = 0;
			}
		}
		else {

			//above average stands for foreground
			average_gray_level_f = VectorMultiplication(vector_gray_level_f, vector_gray_frequency_f) / VectorSum(vector_gray_frequency_f);
		}
		if (VectorSum(vector_gray_frequency_b) == 0.0) {

			if (count > 0) {

				average_gray_level_b = list_average_gray_level_b[list_average_gray_level_b.size() - 1];
			}
			else {

				average_gray_level_b = 0;
			}
		}
		else {

			//above average stands for background
			average_gray_level_b = VectorMultiplication(vector_gray_level_b, vector_gray_frequency_b) / VectorSum(vector_gray_frequency_b);
		}
		list_average_gray_level_f.push_back(average_gray_level_f);
		list_average_gray_level_b.push_back(average_gray_level_b);

		//update threhold
		threshold_next = 0.5 * (average_gray_level_f + average_gray_level_b);

		count++;
	}
	//collect them
	fore_back_luminance.push_back(average_gray_level_f);
	fore_back_luminance.push_back(average_gray_level_b);

	return fore_back_luminance;
}