#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 09:29:13 2022

@author: justin
"""

from setup_tidy import data_dict, var_list
import numpy as np
import datetime
from dictionaries import zero_list

# data_dict = setup_tidy.get_data_dict()
# var_list = setup_tidy.get_var_list() # import the list of variables

def unique_responses(responses):
    '''
    Parameters
    ----------
    responses : list
        a list of repsonses, most likely the output of data_dict.

    Returns
    -------
    unique_list : list
        list of unique responses found in input.
    '''
    unique_list = []
    contains_nan = False
    for i in responses:
        
        if type(i) == float:
            if np.isnan(i):
                contains_nan = True
            
            else:
                if i not in unique_list:
                    unique_list.append(i)
                
        elif i not in unique_list:
            unique_list.append(i)
            
    if contains_nan:
        unique_list.append(float(np.nan))
    return unique_list




def is_np_nan(value):
    '''
    Returns True if response item is np.nan, False if not.
    This is specifically to deal with 'nan.' np.isnan() fails for strings
    '''
    if type(value) == float:
        if np.isnan(value):
            return True
        else:
            return False
    else:
        return False



def count_responses(responses, ignore_zero=False, frequency_mode=False, combine_zero=False):
    '''
    Input: responses : list
        a list of responses to any question. likely output of data_dict.

    Output: response_count_dict : dict
        a ditionary where the response is the key and the count is the value.
    '''

    response_count_dict = {}
    unique_list = unique_responses(responses)
    total_counter = 0
    
    
    
    for unique_response in unique_list:
        counter = 0
        
        
        # This section checks each response for a match.
        if ignore_zero and unique_response in zero_list:
            continue
        
        elif is_np_nan(unique_response):
            for response in responses:
                if is_np_nan(response):
                    counter += 1       
                    
        else: # This is for all other types like str, int, bool etc.
        # Not doing ignore zero here because it should be caught earlier.
            for response in responses:
                if response == unique_response:
                    counter += 1
        
        
        # This section adds the final tally to the scoreboard.
        if ignore_zero and unique_response in zero_list:
                continue 
        else:
            response_count_dict[unique_response] = counter
            total_counter += counter
    
    # this section combines the values with keys in zero_list
    if not ignore_zero and combine_zero:
        sum_of_zeroes = 0
        keys_to_remove = []
        for key, value in response_count_dict.items():
            if key in zero_list:
                sum_of_zeroes += value
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del response_count_dict[key] 
        response_count_dict[zero_list[0]] = sum_of_zeroes
    
    if frequency_mode:
        response_frequency_dict={}
        total=0
        for i in list(response_count_dict.values()):
            total += i
        for key in list(response_count_dict.keys()):
            response_frequency_dict[key] = response_count_dict[key] / total
        return response_frequency_dict
    else:
        return response_count_dict

def get_year_list():
    '''
    This reaturns a list of years that is the same length as the data for each key in data_dict.
    input none.
    returns a list of years.
    '''
    header = var_list[1] # retrieve the first header
    dates = data_dict[header] # list of pandas.timestamp objects
    year_list = []
    for date in dates:
        if type(date) == int:
            year_list.append(date)
        elif isinstance(date, datetime.datetime):
            year_list.append(date.year)
    return year_list
    # year_list = [i.year for i in dates] #convert to years. should be list of int.




def trim_data_by_year(q_number, requested_year):
    '''
    Input the column index of the data you want (int).
    Input the year that you want that data for (int).
    Outputs the list of data that you requested.
    '''
    year_list = get_year_list()
    unique_years = unique_responses(year_list)
    if requested_year not in unique_years: 
        print("Requested year not found!")
        return
    
    query_header = var_list[q_number]
    data = data_dict[query_header] # list of whatever kind of object
    
    out_list = []
    for i, year  in enumerate(year_list):
        if year == requested_year:
            out_list.append(data[i])
    print(f"Data trimmed from {len(data)} to {len(out_list)} responses to only include {requested_year} data.")
    return out_list
    



def count_by_year(col_number, ignore_zero=False, print_readable=False):
    '''
    The column number used as input because I need to match the index of each 
    datapoint to its year. Therefore I need to treat this like raw data 
    processing, so it will have similar features to count_responses. It makes
    me wonder if a standalone function is the best approach? Or would it be 
    better to make this a subfunction of a class?
    
    output:
        Oictionary of dictionaries. Each year has as its 'value' a dictionary
        of the unique responses.
        
    TODO: add frequency_mode option.
    '''
    
    year_list = get_year_list()
    unique_years = unique_responses(year_list)
    query_header = var_list[col_number]
    data = data_dict[query_header] # list of whatever kind of object
    
    data_by_year = []
    for year in unique_years:
        one_year_list = []
        
        for i, datum in enumerate(data):
            if year_list[i] == year:
                if ignore_zero and datum in zero_list:
                    continue
                else:
                    one_year_list.append(datum)        
        
        data_by_year.append(one_year_list)
    
    out_dict = {}
    for year, out_data in zip(unique_years, data_by_year):
        out_dict[year] = count_responses(out_data, ignore_zero=ignore_zero)
    
    print(query_header)
    
    if not print_readable:
        return out_dict # for each year, count_responses from that subset.
    else: 
        for i in out_dict.keys():
            print(i)
            for j in out_dict[i].keys():
                print(str(j)+":"+str(out_dict[i][j]))






def count_y_by_x(x_col_num, y_col_num, year=None, print_readable=False):
    '''
    Parameters
    ----------
    x_col_num : int
        the index of the column to be used as x values.
    y_col_num : int
        the index of the column to be used as y values.
    year : int
        the index of the column to be used as y values.
        
    Returns
    -------
    out_dict
        contains as keys the unique values of x. As values there are dictionaries
        of the response counts for y.

    '''
    # data_dict = setup_tidy.get_data_dict() # import data
    # var_list = setup_tidy.get_var_list() # import the list of variables
    xheader, yheader = [var_list[i] for i in [x_col_num, y_col_num]] # define headers
    if year != None:
        xdata, ydata = [trim_data_by_year(i, year) for i in [x_col_num, y_col_num]]
    else:
        xdata, ydata = [data_dict[i] for i in [xheader, yheader]] # get data
    uniquex, uniquey = [unique_responses(i) for i in [xdata, ydata]]
    
    if x_col_num < 2: # because the timestamp objects in columns 0 and 1 would mess this up.
        return count_by_year(y_col_num) 
    
    else:
        ydata_split_by_x = []
        for unique_response in uniquex:
            one_x_list = []
            for i in range(0,len(ydata)):
                if xdata[i] == unique_response:
                    one_x_list.append(ydata[i])
            ydata_split_by_x.append(one_x_list)
            
        out_dict = {}
        for i in range(0,len(uniquex)):
            out_dict[uniquex[i]] = count_responses(ydata_split_by_x[i])
        print([xheader, yheader])
        if not print_readable:
            return out_dict # for each year, count_responses from that subset.
        else: 
            for i in out_dict.keys():
                print(i)
                for j in out_dict[i].keys():
                    print(str(j)+":"+str(out_dict[i][j]))
        


# # functions

# def get_var(variable_number):
#     '''
#     Parameters
#     ----------
#     variable_number : Int or Str
#         Takes an int or str input number and converts it to VAR00 format.

#     Returns
#     -------
#     Str in the format VAR00.
#     '''
#     # Covert to string
#     if type(variable_number) == int:
#         str_number = str(variable_number)
#     elif type(variable_number) == str:
#         str_number = variable_number
#     elif variable_number == None:
#         #print("Error: NoneType")
#         return None
#     else:
#         print("Error: type of query is not str or int.")
    
#     # Convert to var format
#     if len(str_number) == 1:
#         var_str = "VAR0"+str_number
#     elif len(str_number) == 2:
#         var_str = "VAR"+str_number
#     else:
#         var_str = str_number
#         #print("Error: query is too long or already formatted. Must be one or two digits")
#     # print(var_str)
#     return var_str

# def get_info(variable_number):
#     '''

#     Parameters
#     ----------
#     variable_number : TYPE
#         DESCRIPTION.

#     Returns
#     -------
#     None.

#     '''
#     var_query = get_var(variable_number)
#     print(variable_dict[var_query])
    
# def get_dict(variable_number, inverted = False):
#     '''
#     Parameters
#     ----------
#     variable_number : TYPE
#         DESCRIPTION.

#     Returns
#     -------
#     None.

#     '''
#     var_query = get_var(variable_number)
#     tmp_dict = {}
    
#     if var_query in yes_no_vars:
#         tmp_dict = yes_no_dict
#     elif var_query in agree_disagree_vars:
#         tmp_dict = agree_disagree_dict
#     elif var_query in gender_vars:
#         tmp_dict = gender_dict
#     elif var_query in academic_vars:
#         tmp_dict = academic_dict
#     elif var_query in numeric_vars:
#         tmp_dict = numeric_dict
#     else:
#         return None
    
#     if inverted == True and var_query not in numeric_vars:
#         inv_dict = {v: k for k, v in tmp_dict.items()}
#         return inv_dict
#     else:
#         return tmp_dict
    
# def get_data(variable_number, numeric=True):
#     '''
#     Parameters
#     ----------
#     variable_number : Int or Str
#         This function looks up the question associated with the variable number
#         and returns the data for that question.

#     Returns
#     -------
#     Data from sheet 2.
    
#     TODO: I want to add a gender option here. Get data from males, females, nonbinary etc.

#     '''
#     var_query = get_var(variable_number)
#     tmp_dict = get_dict(var_query)
#     if tmp_dict == None: numeric = False
    
#     # Find the question
#     for i in variable_list:
#         if i == var_query:
#             if numeric == True:
#                 question = variable_dict[var_query][0]
#                 converted_data = []
#                 unconverted_data = data_dict[question]
#                 for datum in unconverted_data:
#                     converted_data.append(tmp_dict[datum])
#                 return converted_data
#             else:
#                 question = variable_dict[var_query][0]
#             # print(question)
#                 return data_dict[question]
    
# def get_count(variable_number, frequency_mode=False):
#     '''
#     Parameters
#     ----------
#     variable_number : str, int
#         Describes the variable number that  you want data for.

#     Returns
#     -------
#     A list of occurrences for each numeric value.
#     Example:
#         legend: [0,1,2,3,4,5] (this is the order of responses)
#         output: [351, 120, 96, 4, 6] (not sorted by size, but by response value)
#         freq. mode: [0.68, 0.25, 0.10, 0.05, 0.01] (this should add up to 1 but I'm lazy)
#     '''
#     var_query = get_var(variable_number)
#     data_list = get_data(var_query)
#     occurence_dict = {}
#     for value in data_list:
#         if value in occurence_dict:
#             occurence_dict[value] += 1
#         else:
#             occurence_dict[value] = 1
    
#     # set up frequencies if requested
#     if frequency_mode == True:
#         frequency_dict = {}
#         for i in occurence_dict:
#             frequency_dict[i] = occurence_dict[i]/len(data_list)
#         output_dict = frequency_dict
#     else:
#         output_dict = occurence_dict
    
#     # sort the keys in ascending order
#     sorted_dict = {}
#     for i in sorted(output_dict):
#         sorted_dict[i] = output_dict[i]
#     return sorted_dict
    
    
# # set up auxiliary plotting functions
# def plot_bar(input1, input2=None, width=0.4, frequency_mode=False):
#     '''
#     Parameters
#     ----------
#     input_data : Int, Str.
#         Describes the variable number you want to plot.
#     input_data2 : TYPE, optional
#         Describes the variable number you want to plot. The default is None.
#         If left out, the function will only plot one.

#     Returns
#     -------
#     A bar chart that can be used as a substitute for the default scatter.
#     notes: check here: https://www.geeksforgeeks.org/plotting-multiple-bar-charts-using-matplotlib-in-python/
#     TODO: Does something weird with numeric data. xticks show up only at populated values,
#     which makes for weird cases like VAR15. 
#     '''
#     input_var1, input_var2 = [get_var(input1), get_var(input2)]
#     input_dict1, input_dict2 = [get_dict(input_var1,True), get_dict(input_var2,True)]
    
#     # check number of inputs
#     if input2 == None:
#         input_list = [input1]
#     else:
#         input_list = [input1, input2]
    
#     # assemble the data
#     bar_data = []
#     for tmp_input in input_list:
#         if frequency_mode == True:
#             input_dict = get_count(tmp_input, frequency_mode=True)
#         else:
#             input_dict = get_count(tmp_input)
#         input_x , input_y = [[],[]]
            
#         for i in input_dict:
#             input_x.append(i)
#             input_y.append(input_dict[i])
#         bar_data.append([input_x , input_y])
    
#     # set up plots
#     if input2 == None:  
#         plt.bar(bar_data[0][0], bar_data[0][1], width, label = input_var1)
#         plt.xticks(bar_data[0][0], [input_dict1[i] for i in bar_data[0][0]], rotation=45, ha='right')
#         plt.title(input_var1+" - "+variable_dict[input_var1][0])
        
#     else:
#         plt.bar([x-width/2 for x in bar_data[0][0]], bar_data[0][1], width, label = input_var1)
#         plt.bar([x+width/2 for x in bar_data[1][0]], bar_data[1][1], width, label = input_var2)
#         if input_dict1 == input_dict2:
#             plt.xticks(bar_data[0][0], [input_dict1[i] for i in bar_data[0][0]], rotation=45, ha='right')
#         plt.title(input_var1+" - "+variable_dict[input_var1][0]+"\n"
#                   +input_var2+" - "+variable_dict[input_var2][0])
        
#     if frequency_mode==True:
#         plt.ylabel('Frequency (counts/responses)')
#     else:
#         plt.ylabel('Counts')
#     plt.show()
    
    
# # Plot the data
# def plot_data(input1, input2=None, bar=False, frequency_mode=False):
#     '''
#     Parameters
#     ----------
#     input_data : Int, Str.
#         Describes the variable number you want to plot.
#     input_data2 : Int, Str, optional
#         Describes the variable number you want to plot. The default is None.
#         If left out, the function will only plot one.
#     bar: bool
#         defines whether or not to use the auxiliary bar chart function to plot.

#     Returns
#     -------
#     A scatter plot with the data. 
#     Next:It would be cool to make this return violin plots or swarm plots,
#     Though it won't get around the issue that there's only data points at discrete values. 
#     How best to show this kind of data? Bars?

#     '''
#     input_var1, input_var2 = [get_var(input1), get_var(input2)]
    
#     if bar == True:
#         if frequency_mode == True:
#             plot_bar(input_var1, input_var2, frequency_mode=True)
#         else:
#             plot_bar(input_var1, input_var2)
#     else:
#         if input_var2 != None:
#             plt.scatter(get_data(input1), get_data(input2))
#             plt.title(input_var1+" vs. "+input_var2)
#             plt.xlabel(variable_dict[input_var1][0])
#             plt.ylabel(variable_dict[input_var2][0])
#         else:
#             plt.plot(ids, get_data(input_var1))
#             plt.title(input_var1+" - "+variable_dict[input_var1][0])
#         plt.show()



# def get_r_squared(input1, input2=None, verbose=False):
#     '''
#     Parameters
#     ----------
#     input1 : int or str
#         describes the var number
#     input2 : TYPE, optional
#         describes the var number. The default is None.

#     Returns
#     -------
#     prints the r squared value of the correlation between inputs 1 and 2

#     '''
#     input_var1, input_var2 = [get_var(input1), get_var(input2)]
#     data1, data2 = [np.array(get_data(i)).astype(float) for i in [input1, input2]]
#     stats = scipy.stats.linregress(data1, data2)
#     if verbose == True:
#         print(input_var1+" vs. "+input_var2)
#         print("r^2 = "+str(stats[2]))
#     return stats[2]


# Sandbox


# show all the plots    
# for i in variable_list:
#     try:
#         plot_data(get_data(i))
#     except:
#         print("Error on "+get_var(i))