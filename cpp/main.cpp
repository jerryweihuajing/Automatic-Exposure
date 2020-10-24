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

#include "Header\operation_import.h"

#include "Header\calculation_exposure_evaluation.h"

int main()
{	
	cout << "Built with OpenCV " << CV_VERSION << endl;

	frame frame_old, frame_now;

	//give them attribute of luminance
	frame_old.average_luminance = WeightedAverageLuminance(imread("dark.jpg"));
	frame_now.average_luminance = WeightedAverageLuminance(imread("bright.jpg"));
	//frame_old.average_luminance = WeightedAverageLuminance(imread("bright_blur.jpg"));
	
	Decision(frame_old, frame_now);

	VectorMatROI9Area(imread("dark.jpg"));
	VectorMatROI5Area(imread("dark.jpg"));
	MatROICenter(imread("dark.jpg"));

	////different frames at different exposure value
	//string imgs_path = "C:\\Users\\ASUS\\Desktop\\Material\\Exposure\\A";

	//vector<frame> vector_frame = VectorFrame(imgs_path);

	////vector of code and contrast
	//vector<int> vector_code;
	//vector<double> vector_contrast;

	//for (int k = 0; k < vector_frame.size(); k++) {

	//	vector_code.push_back(vector_frame[k].lens_position_code);
	//	vector_contrast.push_back(vector_frame[k].focus_value);
	//}

	//cout << "" << endl;
	//cout << "-- Focused Lens Position Code: " << vector_frame[GlobalSearch(vector_contrast)].lens_position_code << endl;

}
 