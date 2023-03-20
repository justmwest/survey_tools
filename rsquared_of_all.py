#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 05:30:02 2021

@author: Justin
"""
import setup


# run get_r_squared on every variable pair that will allow it.
r_squared_list = []
var_pair_list = []

for i in setup.variable_list:
    for j in setup.variable_list:
        try:
            r_squared_list.append(setup.get_r_squared(i,j))
            var_pair_list.append([i,j])
        except:
            None

# Match the r-squared value with the variable pair that produced it. 
annotated_list = []
for i in range(0, len(var_pair_list)):
    annotated_list.append([var_pair_list[i],r_squared_list[i]])


def sort_second(a_list):
    '''
    Inputs
    ------
    a_list: a list

    Returns
    -------
    Returns the seccond value in the list. This function is a sorting key.

    '''
    return a_list[1]

# sort the list by r-squared balues in descending order.
annotated_list.sort(key = sort_second, reverse = True)

# Print the top twenty values (there are 72 identity correlations, e.g. VAR01 vs VAR01)
[print(*line) for line in annotated_list[73:113:2]]

[print(*line) for line in annotated_list[113:193:2]]