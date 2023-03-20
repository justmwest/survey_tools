#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 29 16:23:22 2022

@author: Justin
"""
from sklearn.linear_model import LinearRegression
import setup_tidy
import retrieval_functions
import dictionaries
import numpy as np


# year_1_dict = retrieval_functions.count_by_year(19)
# year_2_dict = retrieval_functions.count_by_year(20)
# # print(year_1_dict)
# print(year_2_dict)

# #retrieval_functions.
# print(dictionaries.agree_disagree_dict)

var_list = setup_tidy.get_var_list()
data_dict = setup_tidy.get_data_dict()

def get_average_response(col_number):
    '''
    This is only designed to work with agree-disagree type questions
    input: col_number (int) i.e. question number
    output: a single int value giving the average response.
    '''
    query_var = var_list[col_number]
    query_responses = data_dict[query_var]
    query_dict = retrieval_functions.count_responses(query_responses)
    
    print("Calculating average response for prompt: "+str(query_var))
    
    out_dict = {}
    sum_of_prod = 0
    total_responses = 0
    
    # list all keys in query_dict
    query_keys = list(query_dict.keys())
    
    # if key matches one in agree_disagree_dict, replace key with out of agree_disagree_dict
    for key in query_keys[:-1]: # last one is 'nan', which we will ignore.
        new_key = dictionaries.agree_disagree_dict[key] # pull numeric key from dictionaries.py
        out_dict[new_key] = query_dict[key] # Associate old values with new key
        total_responses += out_dict[new_key] # Sum of all responses so far
        sum_of_prod += new_key * out_dict[new_key] # Sum of the product so far (for averaging)
        
    return sum_of_prod/total_responses
    
# print(get_average_response(19))

def get_avg_by_year(col_number):
    '''
    This is only designed to work with agree-disagree type questions
    input: col_number (int) i.e. question number
    output: dictionary of the average repsonse with years as keys.
    '''
    # Retrieve metadata and data for input
    query_var = var_list[col_number]
    query_responses = data_dict[query_var]
    query_dict = retrieval_functions.count_responses(query_responses)
    # print("Calculating average response for prompt: "+str(query_var))
    # print('query_responses length: '+str(len(query_responses)))
     
    # Get the list of years in the data
    year_list = retrieval_functions.get_year_list()
    unique_years = retrieval_functions.unique_responses(year_list)
    
    
    # Setup 
    out_dict = {}
    query_keys = list(query_dict.keys()) # list all keys in query_dict
    
    for year in unique_years:
        total_responses, sum_of_prod = [0, 0]
        one_year_dict = {}
        
        for key in query_keys[:-1]: # last one is 'nan', which we will ignore.
            sum_for_one_key = 0 # We will use a counter this 
            for i in range(0,len(query_responses)):
                if year_list[i] == year and query_responses[i] == key: # Only count key if it's in this year
                    sum_for_one_key += 1
            # print("The sum for "+str(key)+" in "+str(year)+" is "+str(sum_for_one_key)+".")
            new_key = dictionaries.agree_disagree_dict[key] # pull numeric key from dictionaries.py
            one_year_dict[new_key] = sum_for_one_key # Associate old values with new key
            total_responses += one_year_dict[new_key] # Sum of all responses so far
            sum_of_prod += new_key * one_year_dict[new_key] # Sum of the product so far (for averaging)
        if total_responses >= 1:    
            average_response = sum_of_prod / total_responses
            # print("The average response for "+str(year)+" is "+str(average_response)+".")
            out_dict[year] = average_response
        else:
            # print("Skipping "+str(year)+" for "+query_var+". Not enough responses.")
            continue
    return out_dict

# print(get_avg_by_year(25))
    
    
def get_slope(col_number):
    '''
    This is only designed to work with agree-disagree type questions
    input: col_number (int) i.e. question number
    reference: https://realpython.com/linear-regression-in-python/#python-packages-for-linear-regression
    output: slope int.
    This function could be easily modified to return the fitted model.
    '''
    input_dict = get_avg_by_year(col_number)
    
    key_list = list(input_dict.keys())
    x = np.array(key_list).reshape((-1, 1))
    y = np.array([input_dict[key] for key in key_list])
    
    model = LinearRegression().fit(x, y)
    # r_sq = model.score(x, y)
    # print(f"r^2: {r_sq}")
    
    slope = model.coef_[0]
    return slope
    
# print(get_slope(19))
    
def ranked_slope_of_all():
    list_of_var_numbers_that_work = []
    [list_of_var_numbers_that_work.append(i) for i in range(35,51)]
    [list_of_var_numbers_that_work.append(i) for i in range(65,81)]
    [list_of_var_numbers_that_work.append(i) for i in range(99,103)]

    slope_list=[]
    for i in list_of_var_numbers_that_work:
        slope_list.append([i, var_list[i],get_slope(i)])
        
    sorted_list = sorted(slope_list, key=lambda x:x[2], reverse=True)
    for i in sorted_list:
        print("Q:"+str(i[0]),end=" ")
        print(i[1], end=". ")
        print("Slope: "+str(i[2]))
    
    
    return sorted_list
ranked_slope_of_all()

def check_get_slope_for_all():
    for i in range(len(var_list)):
        print(i,end=" ")
        try:
            get_slope(i)
            print(" works")
        except: 
            print(" don't work")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    