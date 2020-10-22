// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Calculation on Histogram
******************************************************************************/

#include "..\Header\operation_array.h"
#include "..\Header\operation_vector.h"
#include "..\Header\calculation_histogram.h"

//Flatten img matrix as a vector
vector <int> VectorImgGray(Mat& img_gray) {

	//size of img
	int height = img_gray.rows;
	int width = img_gray.cols;

	//matrix as an array
	vector<int> vector_img_gray;

	//get the number of pixels under each gray level is obtained
	for (int i = 0; i < height; i++)
	{
		for (int j = 0; j < width; j++)
		{
			vector_img_gray.push_back(img_gray.at<uchar>(i, j));
		}
	}
	return vector_img_gray;
}

//Calculate gray level
vector<int> VectorGrayLevel(int step_gray_level) {

	//gray level vector
	vector<int>gray_level;

	//give value
	for (int i = 0; i < int(256 / step_gray_level); i++) {

		gray_level.push_back(i);
	}
	return gray_level;
}

//Calculate ROI matrix gray level amount vector
vector<int> VectorGrayLevelAmount(vector<int>& vector_img_gray) {

	//gray level amount vector
	vector<int>amount;

	//init
	for (int i = 0; i < 256; i++) {

		amount.push_back(0);
	}

	//accumulate
	for (int k = 0; k < vector_img_gray.size(); k++) {

		amount[int(vector_img_gray[k])]++;
	}
	return amount;
}

//Calculate ROI matrix gray level frequency vector
vector<double> VectorGrayLevelFrequency(vector<int>& vector_img_gray) {

	//ROI matrix gray level amount
	vector<int>amount = VectorGrayLevelAmount(vector_img_gray);

	//ROI matrix gray level frequency vector
	vector<double>frequency;

	//the probability distribution of each gray level is obtained
	for (int i = 0; i < amount.size(); i++) {

		frequency.push_back((double)amount[i] / vector_img_gray.size());
	}
	return frequency;
}
