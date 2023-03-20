#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 05:18:34 2021

@author: Justin

Inputs:
In this script, one can graph two variables by changing var1 and var2.
The inputs can be numbers, which will automatically be converted to variable numbers,
e.g., 1 -> VAR01. Otherwise, you can directly input strings in var format, 
e.g., VAR13_2 etc.

Outputs: the script will do three things:
    1. Print information about the variables,
    2. Display a graph of the data, and
    3. Print the r^2 between them.

"""
import setup


# User Input
var1, var2 = ['VAR20_11', 'VAR18_7']
bar_graph = True
frequency_on_y_axis = True



# Automated functions
setup.get_info(var1)
if var2 != None:
    setup.get_info(var2)
    setup.get_r_squared(var1, var2)
setup.plot_data(var1, var2, bar=bar_graph, frequency_mode=frequency_on_y_axis)
