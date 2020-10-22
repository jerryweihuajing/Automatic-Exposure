// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: script-Automatic Exposure
******************************************************************************/

// main.cpp: This file contains the "main" function.
// This is where program execution begins and ends

#include "init.h"

#include "Header\operation_array.h"
#include "Header\operation_vector.h"
#include "Header\calculation_contrast.h"

vector<vector<int>> VectorROI9Area(Mat img_bgr) {

	//size of img
	int height = img_bgr.rows;
	int width = img_bgr.cols;

	//construct img gray//
	Mat img_gray(height, width, CV_8UC1);

	//convert rgb image to gray level
	cvtColor(img_bgr, img_gray, CV_BGR2GRAY);

	//9-Area ROI vector
	vector<vector<int>> vector_ROI;
	
	for (int i = -1; i <= 1; i++) {
		
		for (int j = -1; j <= 1; j++) {
			
			//cout << i << "," << j << endl;
			//center index of ROI
			int i_this_ROI = int(height / 2 + i * height / 4);
			int j_this_ROI = int(width / 2 + j * width / 4);

			int center_this_ROI[2] = { i_this_ROI ,j_this_ROI };

			vector_ROI.push_back(VectorROI(img_gray, center_this_ROI));
		}
	}
	return vector_ROI;
}

double WeightedAverageLuminance(Mat img_bgr) {

	//vector of 9-Area ROI
	vector<vector<int>> vector_ROI = VectorROI9Area(img_bgr);

	//vector of 9-Area luminance
	vector<double>vector_luminance;

	for (int k = 0; k < vector_ROI.size(); k++) {
		
		vector_luminance.push_back(VectorAverage(vector_ROI[k]));
		//cout << vector_luminance[k] << endl;
	}
	
	//vector of 5-Area ROI weight
	vector<double> vector_weight = { 0.1,0.1,0.1,0.1,0.2,0.1,0.1,0.1,0.1 };

	return VectorMultiplication(vector_luminance, vector_weight);
}
bool Decision(frame frame_old, frame frame_now) {

	//diff of luminance between old and new frame
	double luminance_diff = 16;

	if (abs(frame_old.average_luminance - frame_now.average_luminance) < luminance_diff) {
		
		cout << "==> AE: no need" << endl;
		return false;
	}
	cout << "==> AE: needed" << endl;
	return true;
}
int main()
{
	frame frame_old, frame_now;

	//give them attribute of luminance
	frame_old.average_luminance = WeightedAverageLuminance(imread("dark.jpg"));
	frame_now.average_luminance = WeightedAverageLuminance(imread("bright.jpg"));
	//frame_old.average_luminance = WeightedAverageLuminance(imread("bright_blur.jpg"));
	
	Decision(frame_old, frame_now);

	//different frames at different exposure value
	vector<frame> vector_frame;

    cout << "Built with OpenCV " << CV_VERSION << endl;
}
