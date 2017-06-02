# Pydoxygen
Script which collects info about source file and generates doxygen header for each file. If such description is already exist, script will skip this source file.

This script adds the info in doxygen format for C\C++ languages (it can be changed for another languages).

At first the script checks for presence another doxygen comment in the top of the file. If no any header in the file then script will add its own header, like this:

/*! \file   	stl_helper.h
	\brief		Useful functions for work with STL containers. 
			
	Now it supports generic print for STL containers like: [elem1, elem2, elem3]
	Supported STL conrainers: vector, deque, list, set, unordered_set, map,
	unordered_map, array

    \author 	Skident
    \date   	02.09.2016
    \copyrigth	Skident Inc.
*/



Requirements: Python 2.7
