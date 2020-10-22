// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Operation on Array
******************************************************************************/

#include "..\Header\operation_array.h"

//Calculate length of array
//overloaded function 1: pointer array of int type
size_t ArrayLength(int* which_array) {

	size_t length = _msize(which_array) / sizeof(which_array[0]);

	return length;
}
//overloaded function 2: pointer array of float type
size_t ArrayLength(float* which_array) {

	size_t length = _msize(which_array) / sizeof(which_array[0]);

	return length;
}
//overloaded function 3: array pointer of double type
size_t ArrayLength(double* which_array) {

	size_t length = _msize(which_array) / sizeof(which_array[0]);

	return length;
}
//overloaded function 4: pointer array of char type
//char could be the pointer variable
size_t ArrayLength(char* which_array) {

	size_t length = _msize(which_array) / sizeof(which_array[0]);

	return length;
}

//Calculate sum of array
//overloaded function 1: pointer array of int type
int ArraySum(int* which_array) {

	//final result
	int sum = 0;

	for (int i = 0; i < ArrayLength(which_array); i++) {

		sum += which_array[i];
	}
	return sum;
}
//overloaded function 2: pointer array of float type
float ArraySum(float* which_array) {

	//final result
	float sum = 0;

	for (int i = 0; i < ArrayLength(which_array); i++) {

		sum += which_array[i];
	}
	return sum;
}
//overloaded function 3: pointer array of double type
double ArraySum(double* which_array) {

	//final result
	double sum = 0;

	for (int i = 0; i < ArrayLength(which_array); i++) {

		sum += which_array[i];
	}
	return sum;
}

//Calculate average of array
//overloaded function 1: pointer array of int type
double ArrayAverage(int* which_array) {

	int sum = ArraySum(which_array);

	return double(sum) / ArrayLength(which_array);
}
//overloaded function 1: pointer array of float type
double ArrayAverage(float* which_array) {

	float sum = ArraySum(which_array);

	return double(sum) / ArrayLength(which_array);
}
//overloaded function 1: pointer array of double type
double ArrayAverage(double* which_array) {

	double sum = ArraySum(which_array);

	return double(sum) / ArrayLength(which_array);
}

//The array elements are multiplied
//overloaded function 1: both array of int
int ArrayMultiplication(int* array_A, int* array_B) {

	//judge if the length is the same
	if (ArrayLength(array_A) == ArrayLength(array_B)) {

		//final result
		int sum = 0;

		for (int i = 0; i < ArrayLength(array_A); i++) {

			sum += array_A[i] * array_B[i];
		}
		return sum;
	}
	else {

		cout << "--> ERROR: Incorrct size of array";
		return 0;
	}
}
//overloaded function 2: array of int and float
float ArrayMultiplication(int* array_A, float* array_B) {

	//judge if the length is the same
	if (ArrayLength(array_A) == ArrayLength(array_B)) {

		//final result
		float sum = 0;

		for (int i = 0; i < ArrayLength(array_A); i++) {

			sum += array_A[i] * array_B[i];
		}
		return sum;
	}
	else {

		cout << "--> ERROR: Incorrct size of array";
		return 0;
	}
}
//overloaded function 3: array of int and double
double ArrayMultiplication(int* array_A, double* array_B) {

	//judge if the length is the same
	if (ArrayLength(array_A) == ArrayLength(array_B)) {

		//final result
		double sum = 0;

		for (int i = 0; i < ArrayLength(array_A); i++) {

			sum += array_A[i] * array_B[i];
		}
		return sum;
	}
	else {

		cout << "--> ERROR: Incorrct size of array";
		return 0;
	}
}

