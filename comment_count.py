#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 13:02:28 2021

@author: justin
"""

import setup

# Var05C is 'where were you born?'
var1 = "VAR05C"

def get_comment_count(variable_name):
    '''

    Parameters
    ----------
    variable_name : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    if type(variable_name) != str:
        print("Please input the variable name as a string")
        
    data = setup.get_data(variable_name)
    count_dict = {}
    for i in data:
        if i not in count_dict:
            count_dict[i] = 1
        else:
            count_dict[i] = count_dict[i] + 1
    return count_dict

print(get_comment_count(var1))
        