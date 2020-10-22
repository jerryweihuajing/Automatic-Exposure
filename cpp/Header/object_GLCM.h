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

    double energy;      // ���� 
    double entropy;     // ��
    double contrast;    // �Աȶ�
    double idMoment;    // ���־أ� inverse difference moment

} GLCMFeatures;

class GLCM
{
public:

    GLCM();
    ~GLCM();

public:

    // ö�ٻҶȹ�������ķ���
    enum
    {
        GLCM_HORIZATION = 0,        // ˮƽ
        GLCM_VERTICAL = 1,          // ��ֱ
        GLCM_ANGLE45 = 2,           // 45�Ƚ�
        GLCM_ANGLE135 = 3           // 135�Ƚ�
    };
public:

    // ����Ҷȹ�������
    void calGLCM(IplImage* inputImg, VecGLCM& vecGLCM, int angle);
    void calGLCM(Mat& src, VecGLCM& vecGLCM, int angle);
    // ��������ֵ
    void getGLCMFeatures(VecGLCM& vecGLCM, GLCMFeatures& features);
public:

    // ��ʼ���Ҷȹ�������
    void initGLCM(VecGLCM& vecGLCM, int size = 16);
    // ���ûҶȻ��ֵȼ���Ĭ��ֵΪ 16
    void setGrayLevel(int grayLevel) { m_grayLevel = grayLevel; }
    // ��ȡ�Ҷȵȼ�
    int getGrayLevel() const { return m_grayLevel; }
private:

    // ����ˮƽ�Ҷȹ�������
    void getHorisonGLCM(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight);
    // ���㴹ֱ�Ҷȹ�������
    void getVertialGLCM(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight);
    // ���� 45 �ȻҶȹ�������
    void getGLCM45(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight);
    // ���� 135 �ȻҶȹ�������
    void getGLCM135(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight);

private:

    int m_grayLevel;        // ���Ҷȹ������󻮷�Ϊ grayLevel ���ȼ�
};
#endif