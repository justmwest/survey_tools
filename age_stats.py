4#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 14:56:19 2022

@author: justin

This is a script to get basic statistics on for age.
If nothing changes enter 4 when it asks for which dictionary you want (should be numbers)

"""

from setup_tidy import var_list, data_dict
# import var_class
from retrieval_functions import trim_data_by_year
from dictionaries import str_to_int



def stats(data):
    average = sum(data)/len(data)
    print(f'n = {len(data)}')
    print(f'average = {average}')
    print(f"minimum = {min(data)}")
    print(f"maximum = {max(data)}")
    print(f"range = {max(data) - min(data)}")



def main():
    
    # works
    col_no = 5
    var = var_list[col_no]
    dat = data_dict[var]
    out = str_to_int(dat, passthrough=True, ignore_zero=True)
 
    
    raw_data_list=[trim_data_by_year(5, i) for i in [2019, 2021]]
    data_list = [str_to_int(i, passthrough=True, ignore_zero=True) for i in raw_data_list]
    
    data_list.append(out)

    
    labellist=[ "2019:", "2021:", "all:"]
    
    for i, data in enumerate(data_list):
        print(labellist[i])
        stats(data)
        print("", end="")

    
    
if __name__ == '__main__':
    main()