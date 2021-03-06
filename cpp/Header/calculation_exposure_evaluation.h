// -*- coding: utf-8 -*-
/******************************************************************************
Created on Mon Oct 19 14:51:37 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: wei@kamerawerk.cn

@title: Header-Calculation on Exposure Evaluation
******************************************************************************/

#include "..\init.h"

#include "object_frame.h"

#ifndef _CALCULATION_EXPOSURE_EVALUATION_H_
#define _CALCULATION_EXPOSURE_EVALUATION_H_

vector<vector<int>> VectorROI9Area(Mat img_bgr);

double WeightedAverageLuminance(Mat img_bgr);

bool Decision(frame frame_old, frame frame_now);

Mat MatROI(Mat img_gray, int center_ROI[2]);

Mat MatROICenter(Mat img_bgr);

vector<Mat> VectorMatROI9Area(Mat img_bgr);

vector<Mat> VectorMatROI5Area(Mat img_bgr);

#endif