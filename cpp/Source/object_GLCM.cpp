// -*- coding: utf-8 -*-
/******************************************************************************
Created on Mon Oct 19 14:51:37 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: wei@kamerawerk.cn

@title: Source-GLCM object
******************************************************************************/

#include "..\Header\object_GLCM.h"

GLCM::GLCM() : m_grayLevel(16)
{

}

GLCM::~GLCM()
{

}

//==============================================================================
// ��������: initGLCM
// ����˵��: vecGLCM,Ҫ���г�ʼ���Ĺ�������,Ϊ��ά����
//          size, ��ά����Ĵ�С,������ͼ�񻮷ֵĻҶȵȼ����
// ��������: ��ʼ����ά����
//==============================================================================

void GLCM::initGLCM(VecGLCM& vecGLCM, int size)
{
    assert(size == m_grayLevel);
    vecGLCM.resize(size);
    for (int i = 0; i < size; ++i)
    {
        vecGLCM[i].resize(size);
    }

    for (int i = 0; i < size; ++i)
    {
        for (int j = 0; j < size; ++j)
        {
            vecGLCM[i][j] = 0;
        }
    }
}

//==============================================================================
// ��������: getHorisonGLCM
// ����˵��: src,Ҫ���д���ľ���,Դ����
//          dst,�������,�����ľ��󣬼�Ҫ��ĻҶȹ�������
//          imgWidth, ͼ����
//          imgHeight, ͼ��߶�
// ��������: ����ˮƽ����ĻҶȹ�������
//==============================================================================

void GLCM::getHorisonGLCM(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight)
{
    int height = imgHeight;
    int width = imgWidth;

    for (int i = 0; i < height; ++i)
    {
        for (int j = 0; j < width - 1; ++j)
        {
            int rows = src[i][j];
            int cols = src[i][j + 1];
            dst[rows][cols]++;
        }
    }


}

//==============================================================================
// ��������: getVertialGLCM
// ����˵��: src,Ҫ���д���ľ���,Դ����
//          dst,�������,�����ľ��󣬼�Ҫ��ĻҶȹ�������
//          imgWidth, ͼ����
//          imgHeight, ͼ��߶�
// ��������: ���㴹ֱ����ĻҶȹ�������
//==============================================================================

void GLCM::getVertialGLCM(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight)
{
    int height = imgHeight;
    int width = imgWidth;
    for (int i = 0; i < height - 1; ++i)
    {
        for (int j = 0; j < width; ++j)
        {
            int rows = src[i][j];
            int cols = src[i + 1][j];
            dst[rows][cols]++;
        }
    }
}

//==============================================================================
// ��������: getGLCM45
// ����˵��: src,Ҫ���д���ľ���,Դ����
//          dst,�������,�����ľ��󣬼�Ҫ��ĻҶȹ�������
//          imgWidth, ͼ����
//          imgHeight, ͼ��߶�
// ��������: ����45�ȵĻҶȹ�������
//==============================================================================

void GLCM::getGLCM45(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight)
{
    int height = imgHeight;
    int width = imgWidth;
    for (int i = 0; i < height - 1; ++i)
    {
        for (int j = 0; j < width - 1; ++j)
        {
            int rows = src[i][j];
            int cols = src[i + 1][j + 1];
            dst[rows][cols]++;
        }
    }
}


//==============================================================================
// ��������: getGLCM135
// ����˵��: src,Ҫ���д���ľ���,Դ����
//          dst,�������,�����ľ��󣬼�Ҫ��ĻҶȹ�������
//          imgWidth, ͼ����
//          imgHeight, ͼ��߶�
// ��������: ���� 135 �ȵĻҶȹ�������
//==============================================================================

void GLCM::getGLCM135(VecGLCM& src, VecGLCM& dst, int imgWidth, int imgHeight)
{
    int height = imgHeight;
    int width = imgWidth;
    for (int i = 0; i < height - 1; ++i)
    {
        for (int j = 1; j < width; ++j)
        {
            int rows = src[i][j];
            int cols = src[i + 1][j - 1];
            dst[rows][cols]++;
        }
    }
}

//==============================================================================
// ��������: calGLCM
// ����˵��: inputImg,Ҫ�����������������ͼ��,Ϊ�Ҷ�ͼ��
//          vecGLCM, �������,���ݻҶ�ͼ�������ĻҶȹ�����
//          angle,�Ҷȹ�������ķ���,��ˮƽ����ֱ��45�ȡ�135���ĸ�����
// ��������: ����Ҷȹ�������
//==============================================================================

void GLCM::calGLCM(IplImage* inputImg, VecGLCM& vecGLCM, int angle)
{
    assert(inputImg->nChannels == 1);
    IplImage* src = NULL;
    src = cvCreateImage(cvGetSize(inputImg), IPL_DEPTH_32S, inputImg->nChannels);
    cvConvert(inputImg, src);

    int height = src->height;
    int width = src->width;
    int maxGrayLevel = 0;
    // Ѱ��������ػҶ����ֵ
    for (int i = 0; i < height; ++i)
    {
        for (int j = 0; j < width; ++j)
        {
            int grayVal = int(cvGetReal2D(src, i, j));
            if (grayVal > maxGrayLevel)
            {
                maxGrayLevel = grayVal;
            }

        }
    }// end for i

    ++maxGrayLevel;
    VecGLCM tempVec;
    // ��ʼ����̬����
    tempVec.resize(height);
    for (int i = 0; i < height; ++i)
    {
        tempVec[i].resize(width);
    }

    if (maxGrayLevel > 16)//���Ҷȼ�������16����ͼ��ĻҶȼ���С��16������С�Ҷȹ�������Ĵ�С��
    {
        for (int i = 0; i < height; ++i)
        {
            for (int j = 0; j < width; ++j)
            {
                int tmpVal = int(cvGetReal2D(src, i, j));
                tmpVal /= m_grayLevel;
                tempVec[i][j] = tmpVal;
            }
        }

        if (angle == GLCM_HORIZATION)  // ˮƽ����
            getHorisonGLCM(tempVec, vecGLCM, width, height);
        if (angle == GLCM_VERTICAL)    // ��ֱ����
            getVertialGLCM(tempVec, vecGLCM, width, height);
        if (angle == GLCM_ANGLE45)     // 45 �ȻҶȹ�����
            getGLCM45(tempVec, vecGLCM, width, height);
        if (angle == GLCM_ANGLE135)    // 135 �ȻҶȹ�����
            getGLCM135(tempVec, vecGLCM, width, height);
    }
    else//���Ҷȼ���С��16����������Ӧ�ĻҶȹ�������
    {
        for (int i = 0; i < height; ++i)
        {
            for (int j = 1; j < width; ++j)
            {
                int tmpVal = int(cvGetReal2D(src, i, j));
                tempVec[i][j] = tmpVal;
            }
        }

        if (angle == GLCM_HORIZATION)  // ˮƽ����
            getHorisonGLCM(tempVec, vecGLCM, width, height);
        if (angle == GLCM_VERTICAL)    // ��ֱ����
            getVertialGLCM(tempVec, vecGLCM, width, height);
        if (angle == GLCM_ANGLE45)     // 45 �ȻҶȹ�����
            getGLCM45(tempVec, vecGLCM, width, height);
        if (angle == GLCM_ANGLE135)    // 135 �ȻҶȹ�����
            getGLCM135(tempVec, vecGLCM, width, height);
    }

    cvReleaseImage(&src);
}

void GLCM::calGLCM(Mat& src, VecGLCM& vecGLCM, int angle)
{

    int height = src.rows;
    int width = src.cols;

    int maxGrayLevel = 0;
    // Ѱ��������ػҶ����ֵ
    for (int i = 0; i < height; ++i)
    {
        for (int j = 0; j < width; ++j)
        {
            int grayVal = src.at<uchar>(i, j);
            if (grayVal > maxGrayLevel)
            {
                maxGrayLevel = grayVal;
            }

        }
    }// end for i

    ++maxGrayLevel;
    VecGLCM tempVec;
    // ��ʼ����̬����
    tempVec.resize(height);
    for (int i = 0; i < height; ++i)
    {
        tempVec[i].resize(width);
    }

    if (maxGrayLevel > 16)//���Ҷȼ�������16����ͼ��ĻҶȼ���С��16������С�Ҷȹ�������Ĵ�С��
    {
        for (int i = 0; i < height; ++i)
        {
            for (int j = 0; j < width; ++j)
            {
                int tmpVal = src.at<uchar>(i, j);
                tmpVal /= m_grayLevel;
                tempVec[i][j] = tmpVal;
            }
        }

        if (angle == GLCM_HORIZATION)  // ˮƽ����
            getHorisonGLCM(tempVec, vecGLCM, width, height);
        if (angle == GLCM_VERTICAL)    // ��ֱ����
            getVertialGLCM(tempVec, vecGLCM, width, height);
        if (angle == GLCM_ANGLE45)     // 45 �ȻҶȹ�����
            getGLCM45(tempVec, vecGLCM, width, height);
        if (angle == GLCM_ANGLE135)    // 135 �ȻҶȹ�����
            getGLCM135(tempVec, vecGLCM, width, height);
    }
    else//���Ҷȼ���С��16����������Ӧ�ĻҶȹ�������
    {
        for (int i = 0; i < height; ++i)
        {
            for (int j = 1; j < width; ++j)
            {
                int tmpVal = src.at<uchar>(i, j);
                tempVec[i][j] = tmpVal;
            }
        }
        // ˮƽ����
        if (angle == GLCM_HORIZATION) {

            getHorisonGLCM(tempVec, vecGLCM, width, height);
        }

        if (angle == GLCM_VERTICAL)    // ��ֱ����
            getVertialGLCM(tempVec, vecGLCM, width, height);
        if (angle == GLCM_ANGLE45)     // 45 �ȻҶȹ�����
            getGLCM45(tempVec, vecGLCM, width, height);
        if (angle == GLCM_ANGLE135)    // 135 �ȻҶȹ�����
            getGLCM135(tempVec, vecGLCM, width, height);
    }
}
//==============================================================================
// ��������: getGLCMFeatures
// ����˵��: vecGLCM, �������,�Ҷȹ�����
//          features,�Ҷȹ���������������ֵ,��Ҫ�������������ء��Աȶȡ����־�
// ��������: ���ݻҶȹ���������������ֵ
//==============================================================================

void GLCM::getGLCMFeatures(VecGLCM& vecGLCM, GLCMFeatures& features)
{
    int total = 0;

    for (int i = 0; i < m_grayLevel; ++i)
    {
        for (int j = 0; j < m_grayLevel; ++j)
        {
            total += vecGLCM[i][j];     // ������ͼ��ĻҶ�ֵ�ĺ�
        }
    }
    vector<vector<double>> temp;
    temp.resize(m_grayLevel);

    for (int i = 0; i < m_grayLevel; ++i)
    {
        temp[i].resize(m_grayLevel);
    }

    // ��һ��
    for (int i = 0; i < m_grayLevel; ++i)
    {
        for (int j = 0; j < m_grayLevel; ++j)
        {
            temp[i][j] = (double)vecGLCM[i][j] / (double)total;
        }
    }
    for (int i = 0; i < m_grayLevel; ++i)
    {
        for (int j = 0; j < m_grayLevel; ++j)
        {
            features.energy += temp[i][j] * temp[i][j];

            if (temp[i][j] > 0)

                features.entropy -= temp[i][j] * log(temp[i][j]);               //��     

            features.contrast += (double)(i - j) * (double)(i - j) * temp[i][j];        //�Աȶ�
            features.idMoment += temp[i][j] / (1 + (double)(i - j) * (double)(i - j));//����
        }
    }
}