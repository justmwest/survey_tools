#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 14:34:42 2022

@author: Justin

Correlate two questions!
 - Graph of the two questions
 - R2 value between them
 - Specify year

"""

import setup_tidy
import numpy as np
import scipy.stats
import dictionaries
import retrieval_functions

data_dict = setup_tidy.get_data_dict()
var_list = setup_tidy.get_var_list()


### Inputs ###
variable_1 = 4
variable_2 = 72


### Functions ###

def get_r_squared(input1, input2, year='all', verbose=False, ignore_zero=True):
    '''
    Parameters
    ----------
    input1 : int
        column number
    input1 : int
        column number
    year : int or str
        can be int or 'all'/'All'
        for some reason if you use the option year='all' it changes the outcome
        there is a key error 'nan' in str_to_int out_list.append(ref_dict[i])
        If you don't add the year argument at all you're fine. Weird.
        
    Returns
    -------
    prints the r squared value of the correlation between inputs 1 and 2
    
    TODO: add ignore_zero

    '''
    input_var_list = [var_list[input1], var_list[input2]]
    input_data_list = [np.array(data_dict[i]) for i in input_var_list] # Need to use a dictionary to convert to numbers.
    if type(year) == int:
        input_data_list = [retrieval_functions.trim_data_by_year(i, year) for i in [input1, input2]]
    data1, data2 = [dictionaries.str_to_int(i) for i in input_data_list]
    
    
    stats = scipy.stats.linregress(data1, data2)
    if verbose == True:
        print(input_var_list[0]+" vs. "+input_var_list[1])
        print("r^2 = "+str(stats[2]))
    return stats[2]


### Running ###
get_r_squared(variable_1, variable_2, verbose=True, year=2015)