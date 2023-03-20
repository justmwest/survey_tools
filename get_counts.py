#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:47:36 2022

@author: justin
"""

import setup_tidy
import retrieval_functions

var_list=setup_tidy.get_var_list()
data_dict=setup_tidy.get_data_dict()

# select which variable you want to investigate
q_number = 21

# Shows the variable and the first five responses
working_var = var_list[q_number]
print(working_var)
# print(data_dict[working_var][0:4])

# Check whether dictionaries are comprehensive with the following function:
# unique_list = retrieval_functions.unique_responses(data_dict[working_var])
# type_list = [type(i) for i in unique_list]
# print(unique_list)

# Check the number for each unique response
count_dict = retrieval_functions.count_responses(data_dict[working_var])
print(count_dict)