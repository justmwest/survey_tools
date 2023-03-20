#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 21:54:11 2022

@author: Justin

This script is to print basic stats on the categories.


TODO: Make the output dictionary sorted.
TODO: Combine_zero but for not just zeroes. Maybe combine duplicates.

"""

from var_class import var
from setup_tidy import var_list, data_dict
from dictionaries import str_to_int
from retrieval_functions import trim_data_by_year, count_responses

def stats(data):

    n = len(data)
    midpoint = n // 2
    sorted_data = sorted(data)
    median = sorted_data[midpoint-1:midpoint+2]
    
    print(f'median = {median}. Range to show that odd vs even length does not change result.')
    print(f'n = {len(data)}')
    print(f'n // 2 = {midpoint}')
    print(f'counted = {count_responses(data)}')


def main():
    col_no = 6
    variable = var_list[col_no]
    dat = data_dict[variable]
    out = str_to_int(dat, passthrough=True, ignore_zero=True)
    
    
    raw_data_list=[trim_data_by_year(6, i) for i in [2015, 2017, 2019, 2021]]
    
    data_list = [str_to_int(i, passthrough=True, ignore_zero=True) for i in raw_data_list]
    data_list.append(out)

    labellist=["2015:", "2017:", "2019:", "2021:", "All:"]
    
    for i, data in enumerate(data_list):
        print(labellist[i])
        stats(data)
        print("", end="")
    
    

if __name__ == '__main__':
    main()
