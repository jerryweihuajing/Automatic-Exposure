// -*- coding: utf-8 -*-
/******************************************************************************
Created on Mon Oct 19 14:51:37 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: wei@kamerawerk.cn

@title: Source-Calculation on Exposure Evaluation
******************************************************************************/

#include "..\Header\operation_vector.h"

#include "..\Header\calculation_contrast.h"
#include "..\Header\calculation_articulation.h"
#include "..\Header\calculation_exposure_evaluation.h"

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
Mat MatROI(Mat img_gray, int center_ROI[2]) {

	//size of matrix
	int height = img_gray.rows;
	int width = img_gray.cols;

	//5-Area ROI size
	int height_ROI = int(height / 8);
	int width_ROI = int(width / 8);

	//half size
	int half_height_ROI = int(height / 16);
	int half_width_ROI = int(width / 16);

	return img_gray(Range(center_ROI[0] - half_height_ROI, center_ROI[0] + half_height_ROI),
					Range(center_ROI[1] - half_width_ROI, center_ROI[1] + half_width_ROI));
}
Mat MatROICenter(Mat img_bgr) {

	cout << "" << endl;
	cout << "Mat ROI Center" << endl;

	//size of img
	int height = img_bgr.rows;
	int width = img_bgr.cols;

	//construct img gray//
	Mat img_gray(height, width, CV_8UC1);

	//convert rgb image to gray level
	cvtColor(img_bgr, img_gray, CV_BGR2GRAY);

	//center of ROI
	int center_ROI[2] = { int(height / 2),int(width / 2) };

	return MatROI(img_gray, center_ROI);
}
vector<Mat> VectorMatROI9Area(Mat img_bgr) {

	cout << "" << endl;
	cout << "Vector Mat ROI 9-Area" << endl;

	//size of img
	int height = img_bgr.rows;
	int width = img_bgr.cols;

	//construct img gray//
	Mat img_gray(height, width, CV_8UC1);

	//convert rgb image to gray level
	cvtColor(img_bgr, img_gray, CV_BGR2GRAY);

	//9-Area ROI vector
	vector<Mat> vector_ROI_Mat;

	for (int i = -1; i <= 1; i++) {

		for (int j = -1; j <= 1; j++) {

			cout << i << "," << j << endl;

			//center index of ROI
			int i_this_ROI = int(height / 2 + i * height / 4);
			int j_this_ROI = int(width / 2 + j * width / 4);

			int center_this_ROI[2] = { i_this_ROI ,j_this_ROI };

			vector_ROI_Mat.push_back(MatROI(img_gray, center_this_ROI));
		}
	}
	return vector_ROI_Mat;
}
vector<Mat> VectorMatROI5Area(Mat img_bgr) {

	cout << "" << endl;
	cout << "Vector Mat ROI 5-Area" << endl;

	//size of img
	int height = img_bgr.rows;
	int width = img_bgr.cols;

	//construct img gray//
	Mat img_gray(height, width, CV_8UC1);

	//convert rgb image to gray level
	cvtColor(img_bgr, img_gray, CV_BGR2GRAY);

	//9-Area ROI vector
	vector<Mat> vector_ROI_Mat;

	//Center ROI
	vector_ROI_Mat.push_back(MatROICenter(img_bgr));

	for (int i = -1; i <= 1; i++) {

		for (int j = -1; j <= 1; j++) {

			if (i == 0 || j == 0) {

				continue;
			}
			else {

				cout << i << "," << j << endl;

				//center index of ROI
				int i_this_ROI = int(height / 2 + i * height / 4);
				int j_this_ROI = int(width / 2 + j * width / 4);

				int center_this_ROI[2] = { i_this_ROI ,j_this_ROI };

				vector_ROI_Mat.push_back(MatROI(img_gray, center_this_ROI));
			}
		}
	}
	return vector_ROI_Mat;
}
double Evaluate(Mat img_bgr, const string& exposure_operator) {

	//Mat object of ROI
	Mat ROI = MatROICenter(img_bgr);

	if (exposure_operator == "Center") {

		return Articulation(ROI, "Sobel");
	}
	if (exposure_operator == "5-Area") {

		return Articulation(ROI, "Sobel");
	}
	return 0.0;
}