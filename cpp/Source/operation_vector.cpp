// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Operation on Vector
******************************************************************************/

#include "..\Header\object_frame.h"
#include "..\Header\operation_array.h"
#include "..\Header\operation_vector.h"

//Calculate sum of vector
//overloaded function 1: vector of int type
int VectorSum(vector<int>& which_vector) {

	//final result
	int sum = 0;

	for (int i = 0; i < which_vector.size(); i++) {

		sum += which_vector[i];
	}
	return sum;
}
//overloaded function 2: vector of float type
float VectorSum(vector<float>& which_vector) {

	//final result
	float sum = 0;

	for (int i = 0; i < which_vector.size(); i++) {

		sum += which_vector[i];
	}
	return sum;
}
//overloaded function 3: vector of double type
double VectorSum(vector<double>& which_vector) {

	//final result
	double sum = 0;

	for (int i = 0; i < which_vector.size(); i++) {

		sum += which_vector[i];
	}
	return sum;
}

//Calculate average of vector
//overloaded function 1: vector of int type
double VectorAverage(vector<int>& which_vector) {

	int sum = VectorSum(which_vector);

	return double(sum) / which_vector.size();
}
//overloaded function 2: vector of float type
double VectorAverage(vector<float>& which_vector) {

	float sum = VectorSum(which_vector);

	return double(sum) / which_vector.size();
}
//overloaded function 2: vector of double type
double VectorAverage(vector<double>& which_vector) {

	double sum = VectorSum(which_vector);

	return double(sum) / which_vector.size();
}

//Calculate maximum in an vector
//overloaded function 1: vector of int type
int VectorMaximum(vector<int>& which_vector) {

	//init the maximum
	int maximum = which_vector[0];

	for (int i = 0; i < which_vector.size(); i++) {

		if (which_vector[i] > maximum) {

			maximum = which_vector[i];
		}
	}
	return maximum;
}
//overloaded function 2: vector of double type
double VectorMaximum(vector<double>& which_vector) {

	//init the maximum
	double maximum = which_vector[0];

	for (int i = 0; i < which_vector.size(); i++) {

		if (which_vector[i] > maximum) {

			maximum = which_vector[i];
		}
	}
	return maximum;
}

//Calculate minimum in an vector
//overloaded function 1: vector of int type
int VectorMinimum(vector<int>& which_vector) {

	//init the minimum
	int minimum = which_vector[0];

	for (int i = 0; i < which_vector.size(); i++) {

		if (which_vector[i] < minimum) {

			minimum = which_vector[i];
		}
	}
	return minimum;
}
//overloaded function 2: vector of double type
double VectorMinimum(vector<double>& which_vector) {

	//init the minimum
	double minimum = which_vector[0];

	for (int i = 0; i < which_vector.size(); i++) {

		if (which_vector[i] < minimum) {

			minimum = which_vector[i];
		}
	}
	return minimum;
}
//The vector elements are multiplied
//overloaded function 1: both array of int
int VectorMultiplication(vector<int>& vector_A, vector<int>& vector_B) {

	//judge if the length is the same
	if (vector_A.size() == vector_B.size()) {

		//final result
		int sum = 0;

		for (int i = 0; i < vector_A.size(); i++) {

			sum += vector_A[i] * vector_B[i];
		}
		return sum;
	}
	else {

		cout << "--> ERROR: Incorrct size of vector";
		return 0;
	}
}
//overloaded function 2: both array of double
double VectorMultiplication(vector<double>& vector_A, vector<double>& vector_B) {

	//judge if the length is the same
	if (vector_A.size() == vector_B.size()) {

		//final result
		double sum = 0;

		for (int i = 0; i < vector_A.size(); i++) {

			sum += vector_A[i] * vector_B[i];
		}
		return sum;
	}
	else {

		cout << "--> ERROR: Incorrct size of vector";
		return 0;
	}
}
//overloaded function 3: vector of int and double
double VectorMultiplication(vector<int>& vector_A, vector<double>& vector_B) {

	//judge if the length is the same
	if (vector_A.size() == vector_B.size()) {

		//final result
		double sum = 0;

		for (int i = 0; i < vector_A.size(); i++) {

			sum += double(vector_A[i]) * vector_B[i];
		}
		return sum;
	}
	else {

		cout << "--> ERROR: Incorrct size of vector";
		return 0;
	}
}
double VectorMultiplication(vector<double>& vector_A, vector<int>& vector_B) {

	//judge if the length is the same
	if (vector_A.size() == vector_B.size()) {

		//final result
		double sum = 0;

		for (int i = 0; i < vector_A.size(); i++) {

			sum += vector_A[i] * double(vector_B[i]);
		}
		return sum;
	}
	else {

		cout << "--> ERROR: Incorrct size of vector";
		return 0;
	}
}

//vector of index of value which is bigger than threshold which_vector
//overloaded function 1: pointer array of int type
vector<int> VectorIndexAboveThreshold(int* which_array, double threshold) {

	const size_t length = ArrayLength(which_array);

	//final result
	vector <int> list_index;

	for (int i = 0; i < length; i++) {

		if (which_array[i] > threshold) {

			list_index.push_back(i);
		}
	}
	return list_index;
}
//overloaded function 2: vector of int type
vector<int> VectorIndexAboveThreshold(vector<int>& which_array, double threshold) {

	//final result
	vector <int> list_index;

	for (int i = 0; i < which_array.size(); i++) {

		if (which_array[i] > threshold) {

			list_index.push_back(i);
		}
	}
	return list_index;
}

//list of index of value which is smaller than threshold which_array
//overloaded function 1: pointer array of int type
vector<int> VectorIndexBelowThreshold(int* which_array, double threshold) {

	const size_t length = ArrayLength(which_array);

	//final result
	vector <int> list_index;

	for (int i = 0; i < length; i++) {

		if (which_array[i] < threshold) {

			list_index.push_back(i);
		}
	}
	return list_index;
}
//overloaded function 2: vector of int type
vector<int> VectorIndexBelowThreshold(vector<int>& which_array, double threshold) {

	//final result
	vector <int> list_index;

	for (int i = 0; i < which_array.size(); i++) {

		if (which_array[i] < threshold) {

			list_index.push_back(i);
		}
	}
	return list_index;
}

/******************************************************************************
Gets the new vector based on the index list

Args:
	which_vector: vector to be processed
	index_vector: vector of index which is valid

Returns:
	new vector based on the index list
******************************************************************************/
//overloaded function 1: vector of int type
vector<int> VectorFromIndex(vector<int>& which_vector, vector<int>& index_vector) {

	//final result
	vector<int> new_vector;

	for (int i = 0; i < index_vector.size(); i++) {

		new_vector.push_back(which_vector[index_vector[i]]);
	}
	return new_vector;
}
//overloaded function 2: vector of double type
vector<double> VectorFromIndex(vector<double>& which_vector, vector<int>& index_vector) {

	//final result
	vector<double> new_vector;

	for (int i = 0; i < index_vector.size(); i++) {

		new_vector.push_back(which_vector[index_vector[i]]);
	}
	return new_vector;
}
//overloaded function 3: vector of frame type
vector<frame> VectorFromIndex(vector<frame>& which_vector, vector<int>& index_vector) {

	//final result
	vector<frame> new_vector;

	for (int i = 0; i < index_vector.size(); i++) {

		new_vector.push_back(which_vector[index_vector[i]]);
	}
	return new_vector;
}
//Print all element inside the vector
//overloaded function 1: vector of int type
void VectorPrint(vector<int>& which_vector) {

	//traverse and print
	for (int i = 0; i < which_vector.size(); i++) {

		cout << which_vector[i] << endl;
	}
}
//overloaded function 2: vector of double type
void VectorPrint(vector<double>& which_vector) {

	//traverse and print
	for (int i = 0; i < which_vector.size(); i++) {

		cout << which_vector[i] << endl;
	}
}
//overloaded function 3: vector of float type
void VectorPrint(vector<float>& which_vector) {

	//traverse and print
	for (int i = 0; i < which_vector.size(); i++) {

		cout << which_vector[i] << endl;
	}
}
//overloaded function 4: vector of string type
void VectorPrint(vector<string>& which_vector) {

	//traverse and print
	for (int i = 0; i < which_vector.size(); i++) {

		cout << which_vector[i] << endl;
	}
}
//Calculate index from a vector
int VectorIndex(vector<int>which_vector, int which_element) {

	for (int k = 0; k < which_vector.size(); k++) {

		if (which_vector[k] == which_element) {

			return k;
		}
	}
	return -1;
}