// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Header-GLCM object
******************************************************************************/

#include "..\init.h"

#ifndef _OBJECT_GLCM_H_
#define _OBJECT_GLCM_H_

typedef vector<vector<int>>VecGLCM;

typedef struct _GLCMFeatures
{
    _GLCMFeatures()
        : energy(0.0)
        , entropy(0.0)
        , contrast(0.0)
        , idMoment(0.0)
    {

    }

    double energy;      // 能量 
    double entropy;     // 熵
    double contrast;    // 对比度
    double idMoment;    // 逆差分矩， inverse difference moment

} GLCMFeatures;

class GLCM
{
public:

    GLCM();
    ~GLCM();

public:

    // 枚举灰度共生矩阵的方向
    enum
    {
        GLCM_HORIZATION = 0,        // 水平
        GLCM_VERTICAL = 1,          // 垂直
        GLCM_ANGLE45 = 2,           // 45度角
        GLCM_ANGLE135 = 3           // 135度角
    };
public:

    // 计算灰度共生矩阵
    void calGLCM(IplImage* inputImg, VecGLCM& vecGLCM, int angle);
    void calGLCM(Mat& src, VecGLCM& vecGLCM, int angle);
    // 计算特征值
    void getGLCMFeatures(VecGLCM& vecGLCM, GLCMFeatures& features);
public:

    // 初始化灰度共生矩阵
    void initGLCM(VecGLCM& vecGLCM, int size = 16);
    // 设置灰度划分等级，默认值为 16
    void setGrayLevel(int grayLevel) { m_grayLevel = grayLevel; }
    // 获取灰度等级
    int getGrayLevel() const { return m_grayLevel; }
private:

    // 计算水平灰度共生矩阵
    void getHorisonGLCM(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight);
    // 计算垂直灰度共生矩阵
    void getVertialGLCM(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight);
    // 计算 45 度灰度共生矩阵
    void getGLCM45(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight);
    // 计算 135 度灰度共生矩阵
    void getGLCM135(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight);

private:

    int m_grayLevel;        // 将灰度共生矩阵划分为 grayLevel 个等级
};
#endif