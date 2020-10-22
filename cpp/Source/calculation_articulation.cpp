// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Calculation on Articulation
******************************************************************************/

#include "..\Header\calculation_articulation.h"

//Calculate articulation of gray image
double Articulation(Mat& img_gray, const string& articulation_operator) {

	cout << "" << endl;
	cout << "-- Articulation" << endl;

	//sobel gradient of gray image of ROI
	Mat img_articulation;

	//mean articulation of image
	double articulation_average = 0.0;

	//Variance Articulation
	if (articulation_operator == "Variance") {

		Mat meanValueImage;
		Mat meanStdValueImage;

		//calculate the variance of gray image
		meanStdDev(img_gray, meanValueImage, meanStdValueImage);
		articulation_average = meanStdValueImage.at<double>(0, 0);
	}
	else {
		//Sobel Articulation
		if (articulation_operator == "Sobel") {

			Sobel(img_gray, img_articulation, CV_8UC1, 1, 1);
		}
		//Laplacian Articulation
		if (articulation_operator == "Laplacian") {

			Laplacian(img_gray, img_articulation, CV_8UC1);
		}
		articulation_average = mean(img_articulation)[0];
	}
	////could only process the variable whose type is cv.Mat
	////sobel gradient of gray image of ROI
	//Mat ROI_sobel;
	//Sobel(ROI_gray, ROI_sobel, CV_16U, 1, 1);

	//double to string
	stringstream stream_articulation_average;
	string string_articulation_average;
	stream_articulation_average << articulation_average;
	stream_articulation_average >> string_articulation_average;
	string_articulation_average = articulation_operator+" Articulation: " + string_articulation_average;

	//this func allows gray type and a bgr version is in demand
	/*putText(img_gray, string_articulation_average, Point(20, 50), CV_FONT_HERSHEY_COMPLEX, 0.8, Scalar(255, 255, 25), 2);
	imshow("Articulation", img_gray);
	waitKey();*/

	cout << "-> operator: " << articulation_operator << endl;
	cout << "-> value: " << articulation_average << endl;

	return articulation_average;
}
