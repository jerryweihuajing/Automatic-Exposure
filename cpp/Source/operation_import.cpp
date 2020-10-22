// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Operation on Import
******************************************************************************/

#include "..\Header\object_frame.h"

#include "..\Header\operation_import.h"
#include "..\Header\operation_string.h"
#include "..\Header\operation_vector.h"

#include "..\Header\calculation_contrast.h"

//------------------------------------------------------------------------------
/*
Read img name to a BGR Mat object

Args:
	img_name: name of image

Returns:
	BGR Mat object
*/
Mat ReadImgBGR(const string& img_name) {

	Mat img_bgr = imread(img_name, 1);

	if (!img_bgr.data) {

		cout << "Could not open or find the image" << endl;
	}
	return img_bgr;
}
//Transfrom image path to VCM Code
int ImagePath2VCMCode(const string& image_name) {

	//split str into a vector
	vector<string> vector_str = StringSplit(image_name, "\\");
	string str_image = vector_str[vector_str.size() - 1];

	//str with .jpg or .png
	vector<string> vector_str_image = StringSplit(str_image, "_");
	string str_code_image = vector_str_image[vector_str_image.size() - 1];

	//true code str
	vector<string> vector_str_code = StringSplit(str_code_image, ".");
	string str_code = vector_str_code[0];

	//transfrom str to int
	return atoi(str_code.c_str());
}
//------------------------------------------------------------------------------
/*
Calculate the path of all the files under the path

Args:
	folder_path: folder path of images

Returns:
	image files
*/
vector<string> VectorFilesPath(string& folder_path) {

	//final result
	vector<string> total_files;

	//File handle for later lookup
	intptr_t hFile = 0;

	//document information
	struct _finddata_t fileinfo;

	//temporary variable
	string path;

	//the first file is found
	if ((hFile = _findfirst(path.assign(folder_path).append("\\*").c_str(), &fileinfo)) != -1) {

		do {
			//condition: folder
			if ((fileinfo.attrib & _A_SUBDIR)) {

				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0) {

					//files which are from branch folder
					vector<string> branch_files = VectorFilesPath(path.assign(folder_path).append("\\").append(fileinfo.name));

					//collect them
					for (int k = 0; k < branch_files.size(); k++) {

						total_files.push_back(branch_files[k]);
					}
				}
			}
			//condition: file
			else {

				total_files.push_back(path.assign(folder_path).append("\\").append(fileinfo.name));
			}
		}
		//able to find other files
		while (_findnext(hFile, &fileinfo) == 0);

		//end the lookup and close the handle
		_findclose(hFile);
	}
	return total_files;
}
//------------------------------------------------------------------------------
/*
Get frame object and construct a vector

Args:
	folder_path: folder path of images

Returns:
	frame object series
*/
vector<frame> VectorFrame(string& folder_path) {

	//vector of input image path
	vector<string> vector_files_path = VectorFilesPath(folder_path);

	//vector if frame and VCM Code
	vector<frame> vector_frame;
	vector<int> vector_VCM_code;

	//generate matrix
	for (int k = 0; k < vector_files_path.size(); k++) {

		//cout << vector_files_path[k] << endl;
	
		Mat that_img_bgr = imread(vector_files_path[k], 1);

		if (!that_img_bgr.data) {

			cout << "Could not open or find the image" << endl;
		}
		else {

			//size of img
			int height = that_img_bgr.rows;
			int width = that_img_bgr.cols;

			//construct img gray//
			Mat that_img_gray(height, width, CV_8UC1);
			cvtColor(that_img_bgr, that_img_gray, CV_BGR2GRAY);

			//generate a frame object
			frame this_frame;

			this_frame.img_gray = that_img_gray;
			this_frame.img_bgr = that_img_bgr;
			this_frame.lens_position_code = ImagePath2VCMCode(vector_files_path[k]);

			clock_t launch = clock();
			this_frame.focus_value= ContrastCenter(this_frame, "Boccignone");
			//this_frame.contrast = Contrast5Area(this_frame, "Boccignone");
			clock_t finish = clock();
			cout << "--> time consumed: " << 1000 * (double)(finish - launch) / CLOCKS_PER_SEC << " (ms)" << endl;

			vector_frame.push_back(this_frame);
			vector_VCM_code.push_back(this_frame.lens_position_code);
		}
	}
	//copy the VCM code vector
	vector<int> original_vector_VCM_code= vector_VCM_code;
	vector<int> vector_index_sorted;

	//sort the VCM Code
	sort(vector_VCM_code.begin(), vector_VCM_code.end());

	for (int i = 0; i < vector_VCM_code.size(); i++) {

		vector_index_sorted.push_back(VectorIndex(original_vector_VCM_code, vector_VCM_code[i]));
	}
	return VectorFromIndex(vector_frame, vector_index_sorted);
}
//Read txt file line by line
vector<string> readTxt(string file)
{
	vector<string> vector_string_lines;

	ifstream infile;

	//connect a file flow object to a file
	infile.open(file.data());

	//if it fails, an error message is printed and the program is terminated
	assert(infile.is_open());

	string string_this_line;
	while (getline(infile, string_this_line)) {

		//cout << string_this_line << endl;
		vector_string_lines.push_back(string_this_line);
	}
	//close the file input stream
	infile.close();

	return vector_string_lines;
}