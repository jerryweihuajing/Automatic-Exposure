// -*- coding: utf-8 -*-
/******************************************************************************
Created on Mon Oct 19 14:51:37 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: wei@kamerawerk.cn

@title: Source-Operation of string
******************************************************************************/

#include "..\Header\operation_string.h"

//------------------------------------------------------------------------------
/*
Split string like python does

Args:
	str: original string
	delim: separator string

Returns:
	separated string vector
*/
vector<string> StringSplit(const string& str, const string& delim) {

	vector<string> res;

	if ("" == str) {
		return res;
	}

	//the string to be cut is converted from string to char*
	char* strs = new char[str.length() + 1];
	strcpy(strs, str.c_str());

	char* d = new char[delim.length() + 1];
	strcpy(d, delim.c_str());

	char* p = strtok(strs, d);
	while (p) {

		//the split string is converted to string
		string s = p;

		//put into the result array
		res.push_back(s);
		p = strtok(NULL, d);
	}

	return res;
}