// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Calculation on Peak Search
******************************************************************************/

#include "..\Header\calculation_peak_search.h"

int MaximumIndex(vector<double>& which_vector) {
    
    int index_maximum = 0;

    //traverse all element
    for (int k = 0; k < which_vector.size(); k++) {
        
        if (which_vector[k] > which_vector[index_maximum]){
            
            index_maximum=k;
        }
    }
    return index_maximum;
}
//------------------------------------------------------------------------------
/*
Calculation of peak value in contrast value coarsely

Args :
    list_contrast: contrast value list

Returns :
    start index and end index for fine search
*/
int JLSearch(vector<double>& vector_contrast) {

    //amount of consecutive ascending or descending points
    int amount_revert = 3;

    //real - time
    int amount_ascending = 0;
    int amount_descending = 0;

    //strat and end point for fine search
    int index_a = -1;
    int index_b = -1;

    //index of maximum
    int index_maximum = MaximumIndex(vector_contrast);

    for (int k=0; k < vector_contrast.size()-1; k++) {

        //ascending
        if (vector_contrast[k] < vector_contrast[k + 1]) {

            amount_ascending++;
            amount_descending = 0;
        }
        //equal
        if (vector_contrast[k] == vector_contrast[k + 1]) {

            continue;
        }
        //descending
        if (vector_contrast[k] > vector_contrast[k + 1]) {

            amount_descending++;
            amount_ascending = 0;
        }
        //end index of ascending
        if (amount_ascending >= amount_revert) {

            index_a = k + 1;
        }
        //start index of descending
        if (amount_descending >= amount_revert) {
            index_b = k - amount_descending + 1;
        }
        //expire the exception regard the maximum as peak
        if (index_a == index_maximum && index_b == index_maximum) {
        
            return index_maximum;
        }
    }
    return -1;
}
//------------------------------------------------------------------------------
/*
Calculation of peak value in contrast value finely

Args :
    list_contrast: contrast value list

Returns :
    index of VCM code of contrast peak value
*/
int GlobalSearch(vector<double>& vector_contrast){

    //index of maximum
    return MaximumIndex(vector_contrast);
}  