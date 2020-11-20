// -*- coding: utf-8 -*-
/******************************************************************************
Created on Mon Oct 19 14:51:37 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: wei@kamerawerk.cn

@title: Header-frame object
******************************************************************************/

#include "..\init.h"

#ifndef _OBJECT_FRAME_H_
#define _OBJECT_FRAME_H_

//frame object
class frame {

public:
	double exposure_time;
	double average_luminance;
	double exposure_evaluation;
	int lens_position_code;
	double object_distance;
	double focus_value;
	Mat img_bgr;
	Mat img_gray;
	frame();
};
	
#endif