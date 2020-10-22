// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Header-Operation on Import
******************************************************************************/

#include "..\init.h"
#include "object_frame.h"

#ifndef _OPERATION_IMPORT_H_
#define _OPERATION_IMPORT_H_

//Read img name to a BGR Mat object
Mat ReadImgBGR(const string& img_name);

//Transfrom image path to VCM Code
int ImagePath2VCMCode(const string& image_name);

//Calculate the path of all the files under the path
vector<string> VectorFilesPath(string& folder_path);

//Get gray image matrix and construct a vector
vector<frame> VectorFrame(string& folder_path);

//Read txt file line by line
vector<string> readTxt(string file);

#endif