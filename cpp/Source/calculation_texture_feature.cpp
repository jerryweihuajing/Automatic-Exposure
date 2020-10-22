// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Calculation on GLCM
******************************************************************************/

#include "..\Header\object_GLCM.h"
#include "..\Header\calculation_texture_feature.h"

//Calculate texture features depending on feature name
double TextureFeatures(Mat& img,const string& feature_operator) {

    cout << "" << endl;
    cout << "-- Texture Features" << endl;

    GLCM glcm;
    VecGLCM vec;
    GLCMFeatures features;
    glcm.initGLCM(vec);

    //horizontal
    glcm.calGLCM(img, vec, GLCM::GLCM_HORIZATION);
    glcm.getGLCMFeatures(vec, features);
    double energy_hor = features.energy;
    double entropy_hor = features.entropy;
    double contrast_hor = features.contrast;
    double idMoment_hor = features.idMoment;

    //vertical
    glcm.calGLCM(img, vec, GLCM::GLCM_VERTICAL);
    glcm.getGLCMFeatures(vec, features);
    double energy_vetical = features.energy;
    double entropy_vetical = features.entropy;
    double contrast_vetical = features.contrast;
    double idMoment_vetical = features.idMoment;

    //45 degrees
    glcm.calGLCM(img, vec, GLCM::GLCM_ANGLE45);
    glcm.getGLCMFeatures(vec, features);
    double energy_45 = features.energy;
    double entropy_45 = features.entropy;
    double contrast_45 = features.contrast;
    double idMoment_45 = features.idMoment;

    //135 degrees
    glcm.calGLCM(img, vec, GLCM::GLCM_ANGLE135);
    glcm.getGLCMFeatures(vec, features);
    double energy_135 = features.energy;
    double entropy_135 = features.entropy;
    double contrast_135 = features.contrast;
    double idMoment_135 = features.idMoment;

    double energy_average = (energy_135 + energy_45 + energy_hor + energy_vetical) / 4;
    double entropy_average = (entropy_135 + entropy_45 + entropy_hor + entropy_vetical) / 4;
    double contrast_average = (contrast_135 + contrast_45 + contrast_hor + contrast_vetical) / 4;
    double idMoment_average = (idMoment_135 + idMoment_45 + idMoment_hor + idMoment_vetical) / 4;

    //final result
    double feature_average;

    //energy
    if (feature_operator == "Energy") {

        feature_average = energy_average;
    }
    //entropy
    if (feature_operator == "Entropy") {

        feature_average = entropy_average;
    }
    //contrast
    if (feature_operator == "Contrast") {

        feature_average = contrast_average;
    }
    //idMoment
    if (feature_operator == "IdMoment") {
        
        feature_average = idMoment_average;
    }
    cout << "-> operator: " << feature_operator << endl;
    cout << "-> value: " << feature_average << endl;

    return 0.0;
}